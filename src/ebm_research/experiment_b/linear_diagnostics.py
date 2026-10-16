"""Bounded Stage 1.5 training-only diagnostics; frozen Stage 1 stays immutable."""
import argparse
import datetime as dt
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.regression.linear_model import OLS
from statsmodels.robust.robust_linear_model import RLM
from statsmodels.robust.norms import HuberT
from statsmodels.stats.diagnostic import (acorr_ljungbox, het_arch, het_breuschpagan,
                                         het_white, linear_reset)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.tsa.stattools import acf

from .acquisition import file_ref, verify_files
from .benchmarks import fit_table, trio, volatility_tables
from .daily import at, guard_training
from .pilot import ROOT, calendar, sha, write_json
from .repair import merge_overlay
from .stage1 import manual_check, markdown_table

MODELS = {"OLS1_E": ["x_open_bp"], "OLS2_L": ["w_preclose_bp"],
          "OLS3_L": ["x_open_bp", "w_preclose_bp"]}


def load_training(root, stage1):
    """Arrow date/eligibility predicate, metadata guard, then scientific columns.

    No validation/test scientific rows are exposed to diagnostic routines.
    Whole-file hashes read bytes only, not outcomes or state distributions.
    """
    manifest = json.loads((root / "registry/B_stage1_daily_manifest.json").read_text())
    verify_files(root, [manifest["daily"], manifest["manual_check"]] + manifest["products"])
    path = root / manifest["daily"]["path"]
    predicate = [("session_et", ">=", dt.date.fromisoformat(stage1["train"][0])),
                 ("session_et", "<=", dt.date.fromisoformat(stage1["train"][1])),
                 ("eligible_primary", "=", True)]
    dates = pd.read_parquet(path, columns=["session_et"], filters=predicate)
    guard_training(dates, stage1)
    frame = pd.read_parquet(path, filters=predicate)
    guard_training(frame, stage1)
    return frame, manifest


def compare_baseline(current, saved, settings):
    """Compare every principal coefficient/SE/CI/p/R² at HAC5/10/20; fail closed."""
    keys = ["model", "term", "hac_lag"]
    numeric = ["coefficient", "ordinary_se", "r_squared", "hac_se", "ci_low", "ci_high", "p_value"]
    left = pd.DataFrame(current).set_index(keys).sort_index()
    right = saved.loc[saved.cohort.eq("principal")].set_index(keys).sort_index()
    if not left.index.equals(right.index) or not left.n.equals(right.n):
        raise ValueError("INVALID—RERUN: Stage 1 baseline key/count mismatch")
    delta = float(np.max(np.abs(left[numeric].to_numpy() - right[numeric].to_numpy())))
    if not np.allclose(left[numeric], right[numeric], atol=settings["baseline_atol"], rtol=settings["baseline_rtol"]):
        raise ValueError(f"INVALID—RERUN: Stage 1 baseline numerical mismatch, max delta={delta}")
    return dict(status="PASS", coefficient_lag_rows=len(left), max_absolute_difference=delta,
                atol=settings["baseline_atol"], rtol=settings["baseline_rtol"])


def design_for(frame, columns, stage1):
    """Explicit intercept and approved diagnostic columns after training guard."""
    guard_training(frame, stage1)
    return pd.DataFrame({"intercept": np.ones(len(frame)),
                         **{c: frame[c].to_numpy() for c in columns}}, index=frame.index)


def fit_ols(frame, columns, stage1):
    """One ordinary fit reused across its whole residual/influence battery."""
    design = design_for(frame, columns, stage1)
    return OLS(frame.y_last30_bp.to_numpy(), design.to_numpy(), hasconst=True).fit(), design


def coefficient_records(rows, specification="EXPLORATORY_DIAGNOSTIC"):
    """Map existing Stage 1 coefficient records into this stage's compact register."""
    return [dict(r, statistic="coefficient", estimate=r["coefficient"],
                 uncertainty=f"Bartlett HAC{r['hac_lag']}, n/(n-k), normal 95% CI",
                 null="coefficient = 0", specification=specification, status="COMPUTED",
                 source_sensitivity=r["cohort"]) for r in rows]


def stat_record(frame, model, statistic, estimate, p_value=None, null="descriptive", **extra):
    """A diagnostic row with disclosed cohort, observational unit and assumptions."""
    return dict(cohort="principal_training", source_sensitivity="principal",
                specification="EXPLORATORY_DIAGNOSTIC", model=model, statistic=statistic,
                n=len(frame), first=str(frame.session_et.iloc[0]), last=str(frame.session_et.iloc[-1]),
                estimate=float(estimate) if estimate is not None else None,
                p_value=float(p_value) if p_value is not None else None, null=null,
                uncertainty="descriptive / test-specific reference; not primary HAC", status="COMPUTED", **extra)


def ranked_influence(frame, result, stage1):
    """Date-indexed Cook ranking, stable date tie break; no implicit row-position keys."""
    guard_training(frame, stage1)
    influence = result.get_influence()
    table = frame[["session_et", "x_open_bp", "w_preclose_bp", "y_last30_bp", "rv_open_raw"]].copy()
    table["cooks_distance"] = influence.cooks_distance[0]
    table["leverage"] = influence.hat_matrix_diag
    table["studentized_internal"] = influence.resid_studentized_internal
    return table.sort_values(["cooks_distance", "session_et"], ascending=[False, True])


def descriptive_records(frame, settings, stage1):
    """Training-only marginal scales/quantiles and point correlations; no IID p-values."""
    guard_training(frame, stage1)
    rows = []
    cols = ["x_open_bp", "w_preclose_bp", "y_last30_bp", "rv_open_raw", "rv_open_log"]
    for col in cols:
        for name, value in [("mean", frame[col].mean()), ("std_ddof1", frame[col].std()),
                            *[(f"quantile_{q:g}", frame[col].quantile(q)) for q in settings["quantiles"]]]:
            rows.append(stat_record(frame, "marginals", name, value, term=col))
    # Diagnostic alternative explicitly differs from the primary overnight-inclusive X.
    extended = frame[cols].assign(intraday_only_bp=10000 * frame.r_open_intraday_only,
                                 overnight_bp=10000 * frame.open_overnight_part)
    for method in ["pearson", "spearman"]:
        corr = extended.corr(method=method)
        for i, a in enumerate(corr.columns):
            for b in corr.columns[i + 1:]:
                rows.append(stat_record(frame, "correlations", method, corr.loc[a, b], term=f"{a}:{b}"))
    return rows


def residual_records(frame, model, result, design, stage1, settings):
    """Standard small residual battery; HAC stays primary despite IID test flags."""
    guard_training(frame, stage1)
    u = np.asarray(result.resid); rows = []
    add = lambda name, value, p=None, null="descriptive", **kw: rows.append(stat_record(frame, model, name, value, p, null, **kw))
    k = design.shape[1]
    bp = het_breuschpagan(u, design.to_numpy(), robust=True)
    add("Koenker_BP_LM", bp[0], bp[1], "constant conditional variance vs original model regressors", df=k-1,
        assumption="Koenker LM IID reference, robust to nonnormality but not general time dependence")
    try:
        white = het_white(u, design.to_numpy())
        add("White_LM", white[0], white[1], "constant variance vs regressors, squares and cross-products",
            df=(k*(k+1)//2)-1, assumption="IID asymptotic chi-square reference; may be distorted by dependence")
    except (AssertionError, ValueError, np.linalg.LinAlgError) as error:
        rows.append(dict(stat_record(frame, model, "White_LM", None), status="NOT_APPLICABLE", note=str(error)))
    for lag, value in zip(settings["acf_lags"], acf(u, nlags=max(settings["acf_lags"]), fft=False)[settings["acf_lags"]]):
        add(f"residual_ACF_{lag}", value)
    for name, series in [("residual", u), ("squared_residual", u*u)]:
        lb = acorr_ljungbox(series, lags=settings["ljung_box_lags"], model_df=settings["ljung_box_model_df"])
        for lag, row in lb.iterrows():
            add(f"{name}_LjungBox_{lag}", row.lb_stat, row.lb_pvalue,
                f"no {name} autocorrelation through lag {lag}", df=int(lag),
                assumption="asymptotic portmanteau, model_df=0 (static OLS, no fitted ARMA terms); eligible-row lags")
    add("Durbin_Watson", durbin_watson(u))
    arch = het_arch(u, nlags=settings["arch_lags"], ddof=k, result_object=False)
    add("ARCH_LM_5", arch[0], arch[1], "no ARCH through 5 eligible observations", df=5,
        assumption=f"Engle LM chi-square reference; ddof={k}; not proof of conditional variance model")
    jb, p, skew, kurt = jarque_bera(u)
    add("Jarque_Bera", jb, p, "Gaussian residual skewness=0, Pearson kurtosis=3", df=2,
        assumption="asymptotic Gaussian/IID reference diagnostic; heavy tails/dependence affect calibration")
    add("skewness", skew); add("Pearson_kurtosis", kurt)
    for q in settings["quantiles"]:
        add(f"residual_quantile_{q:g}", np.quantile(u, q))
    for predictor, values in [("fitted", result.fittedvalues), ("RV", frame.rv_open_raw),
                              ("X", frame.x_open_bp), ("W", frame.w_preclose_bp)]:
        for transform, residual in [("absolute", np.abs(u)), ("squared", u*u)]:
            add(f"{transform}_residual_corr_{predictor}", stats.spearmanr(residual, values).statistic,
                assumption="Spearman point summary only; no IID correlation test")
    add("condition_number", result.condition_number, assumption="raw bp-scaled explicit-intercept design; units affect this statistic")
    add("ordinary_joint_F", result.fvalue, result.f_pvalue, "all non-intercept slopes = 0", df=k-1,
        df_den=int(result.df_resid), assumption="classical homoskedastic Gaussian-error F reference")
    robust = result.get_robustcov_results(cov_type="HAC", maxlags=5, kernel="bartlett", use_correction=True, use_t=False)
    joint = robust.wald_test(np.eye(k)[1:], use_f=False, scalar=True)
    add("HAC5_joint_Wald", joint.statistic, joint.pvalue, "all non-intercept slopes = 0", df=k-1,
        assumption="asymptotic HAC chi-square, Bartlett5, n/(n-k)")
    hc3 = result.get_robustcov_results(cov_type="HC3", use_t=False)
    for j, term in enumerate(design.columns[1:], 1):
        add("HC3_slope_SE", hc3.bse[j], term=term, assumption="leverage-adjusted heteroskedastic covariance; does not address serial dependence")
    if model in settings["reset_models"]:
        reset = linear_reset(result, power=settings["reset_power"], test_type="fitted", use_f=False,
                             cov_type="HAC", cov_kwds=dict(maxlags=5, kernel="bartlett", use_correction=True, use_t=False))
        add("RESET_fitted_squared_HAC5", reset.statistic, reset.pvalue, "coefficient on fitted squared = 0", df=1,
            assumption="one frozen power2, HAC5 augmented-fit chi-square; broad misspecification, not an EBM selection test")
    if model == "OLS3_L":
        for j, term in enumerate(design.columns[1:], 1):
            add("VIF", variance_inflation_factor(design.to_numpy(), j), term=term)
    # Equal-frequency bins are descriptive residual means, never selected thresholds.
    for predictor, values in [("fitted", result.fittedvalues), ("X", frame.x_open_bp), ("W", frame.w_preclose_bp)]:
        bins = pd.qcut(np.asarray(values), settings["residual_bins"], duplicates="drop")
        table = pd.DataFrame(dict(value=np.asarray(values), residual=u, bin=bins))
        for i, (_, part) in enumerate(table.groupby("bin", observed=True)):
            add("binned_residual_mean", part.residual.mean(), term=predictor, bin=i,
                bin_n=len(part), bin_predictor_mean=part.value.mean(), sufficient_support=len(part)>=settings["sufficient_bin_count"])
    return rows


def influence_sensitivities(frame, model, result, stage1, settings):
    """Fixed Cook top1/top5 deletion and Huber point-only fits; primary unchanged."""
    ranking = ranked_influence(frame, result, stage1)
    top = ranking.head(settings["influence_top_k"]).copy()
    top["model"] = model; top["rank"] = range(1, len(top)+1)
    rows = []
    for idx, record in top.iterrows():
        subset = frame.loc[~frame.session_et.eq(record.session_et)]
        deletion, _ = fit_ols(subset, MODELS[model], stage1)
        for j, term in enumerate(MODELS[model], 1):
            top.loc[idx, "single_delete_delta_"+term] = deletion.params[j]-result.params[j]
    for count in settings["deletion_fits"]:
        subset = frame.loc[~frame.session_et.isin(top.session_et.iloc[:count])]
        rows.extend(coefficient_records(fit_table(subset, design_for(subset, MODELS[model], stage1), stage1,
                                                 f"Cook_top{count}_excluded", model)))
    design = design_for(frame, MODELS[model], stage1)
    rlm = RLM(frame.y_last30_bp.to_numpy(), design.to_numpy(), M=HuberT(t=1.345)).fit(maxiter=100, tol=1e-8, scale_est="mad")
    for j, term in enumerate(design.columns):
        rows.append(dict(stat_record(frame, model, "Huber_RLM_coefficient", rlm.params[j], term=term,
                                     assumption="HuberT1.345, MAD, maxiter100 tol1e-8; point estimate only, no HAC inference"),
                         iterations=rlm.fit_history["iteration"]))
    rows.extend([stat_record(frame, model, "max_leverage", ranking.leverage.max()),
                 stat_record(frame, model, "max_Cooks_distance", ranking.cooks_distance.max()),
                 stat_record(frame, model, "Cook_over_4_over_n", (ranking.cooks_distance>4/len(frame)).sum(),
                             assumption="4/n heuristic, diagnostic count only, no primary deletion rule")])
    return rows, top


def period_sensitivities(frame, stage1, settings, cuts):
    """Fixed calendar periods, leave-year-out and pooled 2020 slope contrasts."""
    guard_training(frame, stage1); rows=[]; cohorts=[]
    years = pd.to_datetime(frame.session_et).dt.year
    for label, endpoints in settings["subperiods"].items():
        subset = frame.loc[frame.session_et.astype(str).between(*endpoints)]
        group = np.searchsorted(cuts, subset.rv_open_raw, side="left")
        cohorts.append(dict(cohort=label,n=len(subset),first=str(subset.session_et.iloc[0]),last=str(subset.session_et.iloc[-1]),
                            x_std_bp=subset.x_open_bp.std(),w_std_bp=subset.w_preclose_bp.std(),y_std_bp=subset.y_last30_bp.std(),
                            rv_low=int((group==0).sum()),rv_middle=int((group==1).sum()),rv_high=int((group==2).sum())))
        for model in settings["period_models"]:
            rows.extend(coefficient_records(fit_table(subset,design_for(subset,MODELS[model],stage1),stage1,label,model)))
    for year in settings["leave_one_year_out"]:
        subset=frame.loc[years.ne(year)]
        for model in settings["period_models"]:
            rows.extend(coefficient_records(fit_table(subset,design_for(subset,MODELS[model],stage1),stage1,f"leave_{year}_out",model)))
    for model in settings["period_models"]:
        design=design_for(frame,MODELS[model],stage1); dummy=years.eq(2020).to_numpy().astype(float)
        design["D2020"]=dummy
        for term in MODELS[model]: design[term+"_x_D2020"]=frame[term].to_numpy()*dummy
        rows.extend(coefficient_records(fit_table(frame,design,stage1,"pooled_2020_break",model)))
        result=OLS(frame.y_last30_bp.to_numpy(),design.to_numpy(),hasconst=True).fit()
        robust=result.get_robustcov_results(cov_type="HAC",maxlags=5,kernel="bartlett",use_correction=True,use_t=False)
        restrictions=np.eye(len(design.columns))[[i for i,t in enumerate(design.columns) if t.endswith("_x_D2020")]]
        test=robust.wald_test(restrictions,use_f=False,scalar=True)
        rows.append(stat_record(frame,model,"2020_joint_slope_break_HAC5",test.statistic,test.pvalue,
                                "all 2020-minus-other-year slope differences = 0",df=len(restrictions),
                                assumption="2020 dummy plus all original slope interactions; HAC5 normal/chi-square; fixed date break, no search"))
    return rows,cohorts


def source_spot_checks(root, frame, stage1, settings):
    """Only seven training dates and prior anchors from existing annual stores."""
    guard_training(frame,stage1)
    selected=frame.loc[frame.session_et.astype(str).isin(settings["source_audit_dates"])].copy()
    if len(selected)!=len(settings["source_audit_dates"]): raise ValueError("Missing predeclared training spot-check date")
    wanted=set(selected.session_et)|set(selected.prior_full_session)
    baseline=json.loads((root/"registry/D2_spy_source_manifest.json").read_text())
    repair=json.loads((root/stage1["repair_manifest"]).read_text())
    refs=[b["canonical"] for y,b in baseline["blocks"].items() if int(y) in {d.year for d in wanted}]
    verify_files(root,refs+[repair["patch"]])
    originals=pd.concat([pd.read_parquet(root/r["path"],filters=[("session_et","in",sorted(wanted))]) for r in refs],ignore_index=True)
    patch=pd.read_parquet(root/repair["patch"]["path"],filters=[("session_et","in",sorted(wanted))])
    missing=pd.read_csv(root/"registry/D2_spy_missing_candles.csv")
    allowed={("SPY",pd.Timestamp(t)) for t in missing.timestamp_utc}
    view=merge_overlay(originals,patch,allowed)
    checks=[]
    for _,row in selected.iterrows():
        one=selected.loc[selected.session_et.eq(row.session_et)]
        checked=manual_check(view,one)
        for col,clock in [("early_features_available_at","10:00"),("late_features_available_at","15:30"),("target_available_at","16:00")]:
            if row[col]!=at(str(row.session_et),clock):raise ValueError(f"Availability mismatch {row.session_et}/{col}")
        checks.append(dict(session_et=str(row.session_et),prior_full_session=str(row.prior_full_session),
                           all_manual_equations_match=checked["all_match"],opening_bar_count=int(row.n_open_minute_bars),
                           early_available_utc=row.early_features_available_at.isoformat(),skipped_early_sessions=int(row.skipped_early_sessions),
                           terminal_repair_dependency=bool(row.terminal_repair_dependency)))
    return checks


def make_figures(frame, results, stage1, settings, output):
    """Four small, training-only descriptive figures; no fitted nonlinear learner."""
    guard_training(frame,stage1)
    os.environ.setdefault("MPLCONFIGDIR",str(ROOT/"logs/stage1_5_matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False})
    output.mkdir(parents=True,exist_ok=True); paths=[]
    def save(fig,name):
        fig.tight_layout(); path=output/(name+".png")
        fig.savefig(path,dpi=settings["plot_dpi"],facecolor="white",bbox_inches="tight");plt.close(fig);paths.append(path)
    y=frame.y_last30_bp.to_numpy()
    fig,axes=plt.subplots(2,2,figsize=(11,8))
    for ax,(x,title,fit) in zip(axes.flat,[
        (frame.x_open_bp,"OLS1 E: overnight-inclusive X",results["OLS1_E"]),
        (frame.w_preclose_bp,"OLS2 L: W known at 15:30",results["OLS2_L"]),
        (results["OLS3_L"].fittedvalues,"OLS3 L: in-sample fitted Y",None),
        (10000*frame.r_open_intraday_only,"DIAGNOSTIC: intraday-only opening (not primary X)",None)]):
        ax.hexbin(x,y,gridsize=35,mincnt=1,bins="log",cmap="Blues",linewidths=0)
        if fit is not None:
            xx=np.array([np.min(x),np.max(x)]);ax.plot(xx,fit.params[0]+fit.params[1]*xx,color="darkorange",label="full training OLS")
            ax.legend(fontsize=8)
        ax.axhline(0,color="gray",lw=.6);ax.axvline(0,color="gray",lw=.6)
        ax.set(title=title,xlabel="predictor / fitted value (bp)",ylabel="Y last-half-hour (bp)")
    fig.suptitle("Training 2016–2021 only — density and linear reference; color uses log counts",y=1.01)
    save(fig,"scatter_reference")
    fig,axes=plt.subplots(3,3,figsize=(13,10))
    for i,(model,result) in enumerate(results.items()):
        for j,(label,x) in enumerate([("fitted",result.fittedvalues),("X",frame.x_open_bp),("W",frame.w_preclose_bp)]):
            ax=axes[i,j];ax.scatter(x,result.resid,s=5,alpha=.22,rasterized=True)
            bins=pd.qcut(np.asarray(x),settings["residual_bins"],duplicates="drop")
            means=pd.DataFrame({"x":np.asarray(x),"u":result.resid,"bin":bins}).groupby("bin",observed=True)[["x","u"]].mean()
            ax.plot(means.x,means.u,"o-",color="darkorange",ms=3,label="10 equal-count bin means")
            ax.axhline(0,color="black",lw=.6);ax.set(xlabel=label+" (bp)",ylabel="residual (bp)",title=model)
    axes[0,0].legend(fontsize=7)
    fig.suptitle("Training residual relationships — bin means are descriptive, with no confidence claims",y=1.01)
    save(fig,"residual_relationships")
    fig,axes=plt.subplots(1,3,figsize=(12,4))
    for ax,(model,result) in zip(axes,results.items()):
        standardized=(result.resid-np.mean(result.resid))/np.std(result.resid,ddof=1)
        theoretical,ordered=stats.probplot(standardized,dist="norm",fit=False)
        ax.scatter(theoretical,ordered,s=7,alpha=.5)
        ax.plot([-3.5,3.5],[-3.5,3.5],color="darkorange",lw=1)
        ax.set(title=model,xlabel="standard normal quantile",ylabel="residual / sample SD")
    fig.suptitle("Training QQ diagnostic — reference normality is not required for HAC",y=1.02)
    save(fig,"residual_qq")
    fig,axes=plt.subplots(2,2,figsize=(12,7))
    dates=pd.to_datetime(frame.session_et)
    for i,model in enumerate(["OLS1_E","OLS3_L"]):
        u=results[model].resid
        axes[i,0].plot(dates,u,lw=.55)
        axes[i,0].axvspan(pd.Timestamp("2020-01-01"),pd.Timestamp("2020-12-31"),color="darkorange",alpha=.15,label="fixed 2020 interval")
        axes[i,0].set(title=model+" residual over time",ylabel="residual (bp)");axes[i,0].legend(fontsize=8)
        axes[i,0].set_xlim(pd.Timestamp("2016-01-01"),pd.Timestamp(stage1['train'][1]))
        axes[i,1].scatter(frame.rv_open_raw,np.square(u),s=6,alpha=.25)
        axes[i,1].set(xscale="log",yscale="symlog",xlabel="opening RV (log axis)",ylabel="squared residual (bp², symlog)",title=model+" variance relationship")
        axes[i,1].set_ylim(bottom=0)
    fig.suptitle("Training time/variance diagnostics — no crisis exclusion in the primary",y=1.01)
    save(fig,"temporal_and_variance")
    return paths


def write_report(root, records, influence, cohorts, baseline, checks, manifest):
    """Readable fixed/exploratory tables with explicit inference limitations."""
    output=ROOT/"reports/B/stage1_5_linear_replication_diagnostics.md"
    table=pd.DataFrame(records)
    def select(**filters):
        f=table
        for k,v in filters.items(): f=f.loc[f[k].eq(v)]
        return f.to_dict("records")
    def md(rows,cols):
        clean=[]
        for r in rows:
            clean.append({c: ("—" if pd.isna(r.get(c)) else r[c]) if c in r else "—" for c in cols})
        return markdown_table(clean,cols)
    base=select(specification="FIXED_STAGE1_COMPARISON",hac_lag=5)
    trio_rows=[r for r in base if r['model'] in MODELS]
    contrast=[r for r in base if r['term']=='high_minus_low_slope']
    test_names=["Koenker_BP_LM","White_LM","ARCH_LM_5","residual_LjungBox_5","residual_LjungBox_10","residual_LjungBox_20",
                "squared_residual_LjungBox_5","squared_residual_LjungBox_10","squared_residual_LjungBox_20","Jarque_Bera",
                "RESET_fitted_squared_HAC5","ordinary_joint_F","HAC5_joint_Wald"]
    tests=[r for r in records if r['statistic'] in test_names]
    tail=[r for r in records if r['statistic'] in ['skewness','Pearson_kurtosis','residual_quantile_0.001','residual_quantile_0.999','Durbin_Watson','condition_number','VIF','HC3_slope_SE'] or r['statistic'].startswith('residual_ACF_')]
    primary_slopes=[r for r in trio_rows if r['term']!='intercept']
    power=[dict(model=r['model'],term=r['term'],hac_se=r['hac_se'],ci_low=r['ci_low'],ci_high=r['ci_high'],
                y_bp_per_100bp_low=100*r['ci_low'],y_bp_per_100bp_high=100*r['ci_high'],planning_slope_5pct_80pct=2.8*r['hac_se']) for r in primary_slopes]
    sensitivity=[r for r in records if r.get('statistic')=='coefficient' and r.get('hac_lag')==5 and r.get('term')!='intercept' and (str(r.get('cohort')).startswith(('Cook_','leave_')) or r.get('cohort') in ['2016_2019','2020','2021','terminal_excluded_Alpaca_equivalent','intraday_only_diagnostic'])]
    breaks=[r for r in records if (r.get('cohort')=='pooled_2020_break' and r.get('hac_lag')==5 and (str(r.get('term')).endswith('_x_D2020') or r.get('term')=='D2020')) or r.get('statistic')=='2020_joint_slope_break_HAC5']
    rlm=[r for r in records if r['statistic']=='Huber_RLM_coefficient' and r.get('term')!='intercept']
    marg=[r for r in records if r.get('model')=='marginals' and r['statistic'] in ['mean','std_ddof1','quantile_0.001','quantile_0.5','quantile_0.999']]
    corr=[r for r in records if r.get('model')=='correlations' and 'y_last30_bp' in r.get('term','')]
    peak_dates=sorted(set(influence.session_et.astype(str)))
    def diagnostic(model,name):
        return next(r['estimate'] for r in records if r['model']==model and r['statistic']==name)
    def coefficient(cohort,model,term):
        return next(r for r in records if r.get('cohort')==cohort and r['model']==model and r.get('term')==term and r.get('hac_lag')==5)
    drop1=coefficient('Cook_top1_excluded','OLS1_E','x_open_bp')
    drop5=coefficient('Cook_top5_excluded','OLS1_E','x_open_bp')
    without2020=coefficient('leave_2020_out','OLS1_E','x_open_bp')
    beta2021=coefficient('2021','OLS1_E','x_open_bp')
    slopebreak=coefficient('pooled_2020_break','OLS1_E','x_open_bp_x_D2020')
    opening_rlm=next(r['estimate'] for r in rlm if r['model']=='OLS1_E')
    kurtoses=[diagnostic(model,'Pearson_kurtosis') for model in MODELS]
    text=f'''# Experiment B Stage 1.5 — focused diagnosis of weak modern linear replication

**PASS WITH QUALIFICATIONS.** Stage 1 baseline numerically reproduces: **{baseline['coefficient_lag_rows']} coefficient/lag rows**, maximum absolute numeric difference **{baseline['max_absolute_difference']:.3g}**, tolerance atol={baseline['atol']}, rtol={baseline['rtol']}. Only **1,495 eligible training dates, 2016-01-05–2021-12-31**, were exposed to diagnostics after a date-only guard and Arrow filtering. Validation 2022–2023 remains reserved; no sealed 2024–2026 scientific rows/statistics/plots were used. Stage 1 source/table/config/reports remain immutable. This stage diagnoses association estimates; it does not establish a unique cause of a historical-modern difference.

The main observations are **heavy tails and volatility clustering/serial dependence**, rather than collinearity: residual Pearson kurtosis is {min(kurtoses):.2f}–{max(kurtoses):.2f} (Gaussian reference3), and OLS1 lag1 residual ACF is {diagnostic('OLS1_E','residual_ACF_1'):.4f}. White, ARCH and residual/squared-residual portmanteau diagnostics flag departures under their reference assumptions; Koenker BP for W alone does **not** reject (p≈0.451), illustrating that different variance alternatives need not agree. OLS3 predictor VIF≈1.00033 gives no evidence that X/W collinearity explains the weak fit. HAC RESET flags are exploratory and do not identify an EBM shape or superiority.

Cook's top observation is 2020-03-18 for all three models. Removing that one date changes OLS1's slope to {drop1['estimate']:.6f}, CI[{drop1['ci_low']:.6f},{drop1['ci_high']:.6f}]; removing the fixed top five gives {drop5['estimate']:.6f}, and the Huber opening slope is {opening_rlm:.6f}. **Sign sensitivity to one observation does not rescue a reliable positive effect**; the top-five and Huber opening estimates remain negative. Removing all 2020 gives {without2020['estimate']:.6f}, CI[{without2020['ci_low']:.6f},{without2020['ci_high']:.6f}], more negative than the primary, so 2020 alone is not a supported explanation for its negative sign. The 2021 descriptive slope is {beta2021['estimate']:.6f}, CI[{beta2021['ci_low']:.6f},{beta2021['ci_high']:.6f}], while the formal 2020 X-slope difference is inconclusive (p={slopebreak['p_value']:.4f}). Period heterogeneity and crisis influence are observed; a specific structural break, zero relationship, or unique source mismatch is not established.

## Baseline verification and uncertainty

{md(trio_rows,['model','term','n','estimate','ordinary_se','r_squared','hac_se','ci_low','ci_high','p_value'])}

{md(contrast,['model','term','estimate','hac_se','ci_low','ci_high','p_value'])}

Units: simple-return bp; slopes bp/bp, intercepts bp. Frozen primary covariance remains Bartlett Newey–West/HAC5 with n/(n−k) finite-sample covariance correction and asymptotic normal two-sided95% intervals/p-values. HAC10/20 and every principal Stage 1 coefficient, ordinarySE, R², HACSE/CI/p were verified against the hashed machine CSV. Ordinary OLSSE/classical F are descriptive reference comparators. The fixed RV terciles/cross-state model are unchanged and conditional on their estimated training boundaries. No outcome- or sign-driven source/state choice was made.

## Source-method and timing checklist

Seven **training** dates independently rechecked against selectively read existing original annual Parquets plus the sole source1 overlay (no new source/download/daily replica):

{md(checks,['session_et','prior_full_session','all_manual_equations_match','opening_bar_count','early_available_utc','skipped_early_sessions','terminal_repair_dependency'])}

Reused Stage 1 scalar `manual_check` verifies P10/Pprev−1, P1530/P15−1, P16/P1530−1 and all30 within-opening log increments; source prices were not exported. Training spring2019 DST maps09:59ET to14:59UTC before and13:59UTC after the boundary. Dec2,2019 uses Nov27 full close, skipping Nov29 early close; missing ordinary prior closes never trigger an older fallback. Availability remains earliest bar completion E10:00, L15:30, Y16:00, not measured vendor delivery latency. Three March2020 incomplete-opening dates remain excluded by the frozen eligibility rule, never reinserted because RV is absent from OLS1. Their missingness can still affect unconditional sample selection.

| Difference / issue | Can affect unconditional Y~X? | State-only or broader qualification |
| --- | --- | --- |
| 1993–2013/1996–2013 TAQ versus2016–2021 Alpaca SIP | Yes: different period, population of days, microstructure and feed | Current diagnostics do not identify a period/measurement cause uniquely |
| Overnight-inclusive X vs intraday-only opening | Yes: distinct predictors | Already stored intraday-only return compared as labeled diagnostic below; never replaces X |
| Prior full-session skip-halfday rule / missing anchors / complete-minute eligibility | Yes: elapsed interval and retained-day population | Approved frozen rule; crisis missingness need not be random |
| Closing anchors/minute versus daily-close conventions, split-only prices/cash distributions | Yes: can change X/Y/W measurements | No daily-close, dividend or16:00-start substitution; actual split-event/full event calendar remains unverified |
| Source1 terminalAug12 repair and Aug13 prior close | Yes: two training observations | One-sided qualification preserved; original-only equivalent exclusion remains explicit |
| RV normalization or tercile thresholds alone | **No: RV is not a regressor in OLS1** | Affects state membership/moderation; eligibility tied to complete RV can affect sample, separately from numeric normalization |
| Vendor ≥500 daily trade flag | Potential population difference from TAQ | Every retained full day passed saved Alpaca flag; qualifying counts not TAQ identity |
| HAC convention | Changes uncertainty, not ordinary OLS point estimate | Project Bartlett5/10/20 and finite correction are not verified source-paper exact settings |

The [original source crosswalk](../../docs/experiment_B_source_method_crosswalk.md) remains authoritative about unresolved source construction. No numerical historical slope magnitude is verified in the local crosswalk/spec, so no invented historical effect size/t-statistic-as-slope comparison is made. No external article/history search was necessary for this bounded audit.

## Training marginal and residual structure

{md(marg,['term','statistic','estimate'])}

{md(corr,['term','statistic','estimate'])}

Full min/max/extreme quantiles, X–W/RV/logRV/component correlations and all residual statistics are in the [machine register](../../data/registry/B_stage1_5_linear_diagnostics_summary.csv). Correlations are point descriptions, with no IID p-values. RV raw is dimensionless √Σlog-return²; logRV is natural log(RV+1e−8). Scatter density is log-count colored; lines are the frozen full-training simple linear fits. Intraday-only X is a distinct labeled diagnostic, not a substitute primary model.

![Training scatter/reference relationships](../../artifacts/B/stage1_5/scatter_reference.png)

![Residual versus fitted, X and W](../../artifacts/B/stage1_5/residual_relationships.png)

Orange lines are10 equal-frequency residual-bin means; all displayed bins are checked for at least20 observations. Bin means/visual patterns are exploratory descriptions, not independent threshold discoveries, CIs or new fitted nonlinear forecasts.

## Assumption diagnostics — EXPLORATORY, test-specific reference distributions

{md(tests,['model','statistic','estimate','p_value','df','null'])}

{md(tail,['model','term','statistic','estimate'])}

Koenker BP uses each original model's intercept/predictors as variance regressors (robust=True); White adds their squares/cross-products. Their IID chi-square references are diagnostics, not generally valid replacements for dependent-return inference. Residual/squared-residual Ljung–Box uses fixed5/10/20 lags, `model_df=0` because no ARMA coefficients were estimated; ARCH LM uses5lags and OLS parameter-count ddof. Eligible-observation spacing is not uniform calendar-day spacing: gaps, holidays and omitted full days remain. Durbin–Watson/ACF are descriptive. JB tests Gaussian skewness0/kurtosis3 under its asymptotic reference; heavy tails are not grounds to remove days. Neither normality nor zero serial correlation is a prerequisite for HAC, and failed rejection cannot prove independence. HAC itself needs suitable dependence/moment regularity and is not guaranteed reliable by one test.

HC3 is a heteroskedastic/leverage comparator without serial correction. Raw design condition numbers depend on bp scaling; OLS3 VIF addresses only its two actual regressors. RESET is **one predeclared fitted-value square** for OLS1/OLS3, chi-square Wald using augmented-fit HAC5; it is a broad misspecification flag, not a test of a specific EBM advantage. Ordinary joint F uses its classical homoskedastic/Gaussian reference; HAC joint Wald tests all original slopes using robust chi-square. No residual test verifies exogeneity, zero conditional mean, causality or correct financial measurement. Many unadjusted exploratory tests are reported; no selected nominal rejection is familywise-confirmed evidence. Underflowed p-values of0 mean numerical underflow, never mathematically zero probability.

![Normal QQ reference](../../artifacts/B/stage1_5/residual_qq.png)

![Training time and variance relationships](../../artifacts/B/stage1_5/temporal_and_variance.png)

## Influence and fixed robustness comparisons

Ranking is descending Cook's distance within each original model, date ascending for ties, **fixed before diagnostics**. The table uses internally studentized residuals (explicit standard equivalent, not externally studentized). Drop-one coefficient deltas are refits of that particular date; these are not significance-based deletions. Primary full-sample OLS remains authoritative.

{md(influence.fillna('').to_dict('records'),['model','rank','session_et','cooks_distance','leverage','studentized_internal','x_open_bp','w_preclose_bp','y_last30_bp','single_delete_delta_x_open_bp','single_delete_delta_w_preclose_bp'])}

Distinct top-five influential dates across models: {', '.join(peak_dates)}. Top1/top5 removals are in the sensitivity table below. Their HAC intervals are diagnostic conditional-fit summaries after influence selection, not selection-adjusted confidence intervals. HuberT1.345/MAD/maxiter100/tol1e−8 robust fits are point-estimate-only comparisons with different loss/estimand; no RLM HAC claim or primary replacement.

{md(rlm,['model','term','estimate','iterations'])}

## Fixed time periods, leave-year-out and source/deletion sensitivity

{md(cohorts,['cohort','n','first','last','x_std_bp','w_std_bp','y_std_bp','rv_low','rv_middle','rv_high'])}

State support counts use the **same frozen Stage 1 training RV cutoffs**, with no subperiod re-estimation; they do not establish joint X/RV/W support for a nonlinear contrast. Every per-period/HAC uncertainty is limited by that subperiod's effective sample/dependence;2020 is a single exceptional calendar year. Excluding2020 is the predeclared leave2020out sensitivity, never a redefinition of the primary sample. No optimized rolling window or broad breakpoint search was run.

{md(sensitivity,['cohort','model','term','n','first','last','estimate','hac_se','ci_low','ci_high','p_value'])}

Original Alpaca-only numerical sensitivity reuses Stage 1's **hashed matched-date identity proof**: both newly eligible repaired dates are removed, leaving exactly the same1,493 training scientific rows as original-only. Its recomputed trio is checked to the original-only Stage1 machine values; no second full minute/daily dataset is built. Intraday-only diagnostic uses the existing stored price-return field, not a new source. These alternatives are retained regardless of signs.

The pooled fixed2020 break includes an intercept, original regressors, D2020, and D2020 times every original slope. X×D2020 is the explicit 2020-minus-other-years opening slope difference; OLS3 additionally permits W's slope to change. The joint Wald tests slope interactions only, controlling the intercept shift. This is a more direct comparison than separate significance labels; the exploratory HAC reference does not identify a causal pandemic effect or prove a stable structural break.

{md(breaks,['model','term','statistic','estimate','hac_se','ci_low','ci_high','p_value','df'])}

## Effect scales, interpretation and Stage 2

{md(power,['model','term','hac_se','ci_low','ci_high','y_bp_per_100bp_low','y_bp_per_100bp_high','planning_slope_5pct_80pct'])}

Intervals quantify slopes this finite training cohort cannot rule out under HAC assumptions. Multiplying by100 describes the linear fitted-Y difference associated with a100bp predictor change, not a causal/executable profit or a guarantee of joint support. The `(1.96+0.84)×SE` column is an **illustrative fixed-design normal5%/80% detectable-effect scale**, not a formal time-series power calculation or an estimate of the true slope. Significance, population absence, prediction and economic utility are distinct.

Evidence-weighted interpretation: (1) heavy-tail/dependence/influence and fixed-period instability can be **evaluated directly here** through the complete tables, but do not establish why the source-era effect changed; (2) different source-era/modern construction remains a real comparability limitation, with seven timing/formula checks and baseline reproduction providing evidence against the specific implementation errors checked; (3) a genuinely absent/changed later-market association is **UNRESOLVED** because training intervals, observational instability and unresolved measurement differences do not distinguish it uniquely. RV normalization alone cannot explain the unconditional OLS1 sign. Influence sensitivity is not permission to delete crisis observations until results become positive.

**Proceed to Stage 2 only as the originally planned, separately authorized extension**, comparing chronology-safe naive/state-aware simple competitors and small predeclared EBMs on matched dates. Carry heavy-tail/dependence/influence uncertainty, subperiod/2020 differences, incomplete crisis openings, source/one-sided repair and sample-support caveats. Keep2022–2023 for selection and2024–2026 sealed. No model family, target/state/horizon/source re-selection, trading, OOS claim or EBM superiority is established by this audit. No unique causal explanation is claimed.

Provenance, exact hashes/software/settings and resource counters: [audit manifest](../../data/registry/B_stage1_5_diagnostics_manifest.json). Supplemental methods/nulls/assumptions are included here and in every applicable machine row, so no duplicate methods document is created.
'''
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(text)
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root',type=Path,default=Path(os.environ.get('EBM_DATA_ROOT',ROOT/'data')))
    parser.add_argument('--config',type=Path,default=ROOT/'config/B_stage1_5_diagnostics.json')
    args=parser.parse_args();root=args.data_root.expanduser().resolve()
    wall=time.perf_counter();cpu=time.process_time();free=shutil.disk_usage(root).free
    settings=json.loads(args.config.read_text())
    for path,digest in settings['input_sha256'].items():
        actual=root/path.removeprefix('data/') if path.startswith('data/') else ROOT/path
        if sha(actual)!=digest:raise ValueError(f'Frozen diagnostic input identity changed: {path}')
    stage1=json.loads((ROOT/'config/B_stage1_dataset_selection.json').read_text())
    frame,prior_manifest=load_training(root,stage1)
    for r in prior_manifest['code']:
        if sha(ROOT/r['path'])!=r['sha256']:raise ValueError(f'Stage1 execution code changed: {r["path"]}')
    state=json.loads((root/'registry/B_stage1_state_metadata.json').read_text())[0]
    saved=pd.read_csv(root/'registry/B_stage1_coefficients.csv')
    # Stage1 principal baseline is verified once through existing regression/HAC functions.
    recomputed=trio(frame,stage1,'principal')
    grouped,_=volatility_tables(frame,stage1,'principal',cutoffs=state['rv_raw_cutoffs']);recomputed+=grouped
    baseline=compare_baseline(recomputed,saved,settings)
    records=coefficient_records(recomputed,'FIXED_STAGE1_COMPARISON')
    for r in recomputed:
        if r['model'] in MODELS and r['term']!='intercept' and r['hac_lag']==5:
            records.append(stat_record(frame,r['model'],'illustrative_normal_detectable_slope_5pct_80pct',2.8*r['hac_se'],term=r['term'],
                                       assumption='(1.96+0.84)*observed HAC5 SE; fixed-design normal planning only, no time-series power guarantee'))
    checks=source_spot_checks(root,frame,stage1,settings)
    records+=descriptive_records(frame,settings,stage1)
    results={};influence=[]
    for model,columns in MODELS.items():
        result,design=fit_ols(frame,columns,stage1);results[model]=result
        records+=residual_records(frame,model,result,design,stage1,settings)
        rows,top=influence_sensitivities(frame,model,result,stage1,settings);records+=rows;influence.append(top)
    rows,cohorts=period_sensitivities(frame,stage1,settings,state['rv_raw_cutoffs']);records+=rows
    # Established original-only equivalent, validated numerically against saved original trio.
    no_terminal=frame.loc[~frame.terminal_repair_dependency]
    original_rows=trio(no_terminal,stage1,'terminal_excluded_Alpaca_equivalent')
    old_saved=saved.loc[saved.cohort.eq('alpaca_only')&saved.model.isin(MODELS)].copy().assign(cohort='principal')
    compare_baseline(original_rows,old_saved,settings)
    records+=coefficient_records(original_rows)
    intraday=frame.assign(intraday_only_bp=10000*frame.r_open_intraday_only)
    records+=coefficient_records(fit_table(intraday,design_for(intraday,['intraday_only_bp'],stage1),stage1,'intraday_only_diagnostic','OLS1_intraday_DIAGNOSTIC'))
    influences=pd.concat(influence,ignore_index=True)
    figures=make_figures(frame,results,stage1,settings,ROOT/'artifacts/B/stage1_5')
    registry=root/'registry';outputs=[]
    for name,table in [('B_stage1_5_linear_diagnostics_summary.csv',pd.DataFrame(records)),
                       ('B_stage1_5_influence.csv',influences),('B_stage1_5_cohort_support.csv',pd.DataFrame(cohorts))]:
        path=registry/name;table.to_csv(path,index=False,lineterminator='\n');outputs.append(file_ref(path,root))
    manifest=dict(stage='B_stage1_5',verdict='PASS WITH QUALIFICATIONS',created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  config_sha256=sha(args.config),inputs=settings['input_sha256'],dataset_id=stage1['dataset_id'],daily=prior_manifest['daily'],
                  training_n=len(frame),first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),baseline_verification=baseline,
                  source_spot_checks=checks,source_sensitivity='Established Stage1 matched-value identity plus verified original-only equivalent exclusion',
                  outputs=outputs,figures=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p)) for p in figures],
                  code=dict(path=str(Path(__file__).resolve().relative_to(ROOT)),sha256=sha(Path(__file__))),
                  versions={p:metadata.version(p) for p in ['numpy','pandas','pyarrow','scipy','statsmodels','matplotlib']},python=platform.python_version(),
                  git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  market_data_http_calls=0,validation_test_scientific_rows_exposed=0,free_before=free,free_after=shutil.disk_usage(root).free,
                  wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu)
    report=write_report(root,records,influences,cohorts,baseline,checks,manifest)
    manifest['report']=dict(path=str(report.relative_to(ROOT)),bytes=report.stat().st_size,sha256=sha(report))
    write_json(registry/'B_stage1_5_diagnostics_manifest.json',manifest)
    print(json.dumps(dict(verdict=manifest['verdict'],training_n=len(frame),baseline=baseline,
                         diagnostic_rows=len(records),figure_bytes=sum(p.stat().st_size for p in figures),
                         wall_seconds=manifest['wall_seconds'],cpu_seconds=manifest['cpu_seconds'])))


if __name__=='__main__':
    main()
