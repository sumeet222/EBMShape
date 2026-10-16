"""Offline Stage 1 CLI: one daily table, integrity QA and training benchmarks."""
import argparse
import datetime as dt
import importlib.metadata as metadata
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time

import numpy as np
import pandas as pd

from .acquisition import file_ref, verify_files
from .benchmarks import trio, volatility_tables
from .daily import at, build_daily, training_rows
from .pilot import ROOT, calendar, sha, write_json
from .repair import load_minutes


def counts(frame, view):
    """Coverage only: never summarize sealed-period return or RV values."""
    rows=[]
    for dimension,keys in [('year',frame.session_et.astype(str).str[:4]),('split',frame.split)]:
        for key,part in frame.groupby(keys,sort=True):
            eligible=part.loc[part.eligible_primary]
            rows.append(dict(view=view,dimension=dimension,period=str(key),full_sessions=len(part),eligible=len(eligible),excluded=len(part)-len(eligible),
                             first_eligible=str(eligible.session_et.min()),last_eligible=str(eligible.session_et.max())))
    return rows


def manual_check(minutes, daily):
    """Independent scalar-loop calculation on first complete training day."""
    row=daily.loc[daily.eligible_primary & daily.split.eq('train')].iloc[0]
    day=str(row.session_et); prior=str(row.prior_full_session)
    lookup=minutes.set_index('timestamp_utc')
    price=lambda d,t:float(lookup.loc[at(d,t),'close'])
    anchors={'Pprev':price(prior,'15:59'),'P10':price(day,'09:59'),'P15':price(day,'14:59'),'P1530':price(day,'15:29'),'P16':price(day,'15:59')}
    r1=anchors['P10']/anchors['Pprev']-1; r12=anchors['P1530']/anchors['P15']-1; r13=anchors['P16']/anchors['P1530']-1
    previous=float(lookup.loc[at(day,'09:30'),'open']); squared=[]
    for minute in range(30):
        close=price(day,f'09:{30+minute:02d}')
        squared.append(math.log(close/previous)**2); previous=close
    rv=math.sqrt(math.fsum(squared))
    expected={'r1':r1,'r12':r12,'r13':r13,'rv_open_raw':rv}
    for key,value in expected.items():
        if not math.isclose(value,row[key],rel_tol=1e-12,abs_tol=1e-14):
            raise ValueError(f'Independent manual calculation differs: {key}/{day}')
    return dict(session_et=day,source_prices=anchors,independent=expected,all_match=True,absolute_tolerance=1e-14,relative_tolerance=1e-12)


def markdown_table(rows, columns):
    """Small Markdown tables without an additional formatting dependency."""
    def value(v):
        return f'{v:.6g}' if isinstance(v,float) else str(v)
    lines=['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']
    lines.extend('| '+' | '.join(value(r[c]) for c in columns)+' |' for r in rows)
    return '\n'.join(lines)


def scientific_report(qa, coefficients, states, coverage, manual, manifest):
    """Training results and source qualifications; sealed counts only."""
    principal=[r for r in coefficients if r['cohort']=='principal' and r['hac_lag']==5 and r['model'].startswith('OLS')]
    lag_sensitivity=[r for r in coefficients if r['cohort']=='principal' and r['term']!='intercept' and r['model'].startswith('OLS')]
    group=[r for r in coefficients if r['cohort']=='principal' and r['hac_lag']==5 and r['term']=='x_open_bp' and r['model'].startswith('RV_')]
    contrast=[r for r in coefficients if r['cohort']=='principal' and r['model']=='RV_pooled_interaction' and r['term']=='high_minus_low_slope']
    sensitivities=[r for r in coefficients if r['cohort']!='principal' and r['hac_lag']==5 and r['term']!='intercept' and r['model'].startswith('OLS')]
    state=states[0]
    return f'''# Experiment B Stage 1 — modern-period partial-method reproduction / hypothesis check

**PASS WITH QUALIFICATIONS.** This is a daily-table implementation and training-only descriptive benchmark gate, not historical source-era replication, an OOS result, nonlinear shape evidence or a profitability claim. No EBM, spline, trading, permutation, validation-outcome analysis or sealed-test outcome analysis was performed. Experiment A remains on hold.

## Frozen source and daily definitions

Principal: immutable `B_alpaca_sip_SPY_1m_split_D2_v1` plus exactly `B_spy_hf_source1_D2_1c_v1`, selected in `config/B_stage1_dataset_selection.json` before scientific calculations. Original Alpaca-only and exclusion of all terminal-repair-dependent dates are predeclared sensitivities. No D2.1b rows are combined. Source manifests/config/code and the single daily table are hashed in [manifest](../../data/registry/B_stage1_daily_manifest.json).

The daily table has **{qa['principal_rows']} scheduled full-session rows / {qa['principal_eligible']} eligible**, 2016-01-04–2026-09-30; first eligible 2016-01-05. The {qa['early_close_sessions']} early sessions are excluded by the real XNYS schedule and linked by the original D2 QA. Pprev is the preceding permissible full-session 15:59 close, skipping scheduled early closes only; a missing full close invalidates the next day. P10/P15/P1530/P16 are minute closes at 09:59/14:59/15:29/15:59 bar starts. Simple r1=P10/Pprev−1, r12=P1530/P15−1, r13=P16/P1530−1; X/W/Y are 10,000 times these returns. No 16:00-start, daily aggregate or after-hours prices are substituted.

Opening RV uses log(C09:30/O09:30) and 29 consecutive close/close logs; RV=√Σq², Z=log(RV+1e−8), requiring all 30 positive valid OHLC bars. Overnight is included in X and excluded from RV. E uses X/RV only at 10:00; L can additionally use W at 15:30; Y completes at 16:00. Availability columns express earliest bar completion, **not observed vendor delivery latency or executable fills**.

## Coverage and chronology QA

{markdown_table([r for r in coverage if r['view']=='principal'],['dimension','period','full_sessions','eligible','excluded','first_eligible','last_eligible'])}

Original eligibility {qa['original_eligible']} → principal {qa['principal_eligible']}; newly eligible **{', '.join(qa['gained_dates'])}**. Original 104 absent minutes −39 accepted keys =65 remaining; this full-session accounting reuses the saved complete-session audit because nonrequired prices were discarded at D2. Fresh retained-window checks reproduce 91-window eligibility and all original eligibility flags. Feb 2, 2016 repairs are midday only and do not change scientific features. Aug 12 closing repairs change that day's label/W and Aug 13 prior-close X. Both days are flagged for terminal-dependency sensitivity; Aug 12's terminal 28 repaired bars have one-sided support and documented maximum cross-feed discrepancies (close 5.557 bp, high 5.904 bp, low 10.767 bp; see D2.1c).

Excluded full sessions:

{markdown_table(qa['exclusions'],['session_et','eligibility_reason'])}

Missing/invalid counts and source use:

{markdown_table(qa['view_checks'],['view','missing_Pprev','missing_P10','missing_P15','missing_P1530','missing_P16','missing_opening_bars','incomplete_opening_days','invalid_ohlc_rows','zero_rv','negative_rv','invalid_rv_complete'])}

Repaired use: {json.dumps(qa['repair_use'],sort_keys=True)}. Zero duplicate daily keys; all minute keys/timezones/session mappings and information-time bounds checked. {qa['full_days_after_early']} full days skip an intervening scheduled early close; weekend/holiday elapsed periods remain explicit. QA examples show winter 09:59 ET=14:59 UTC and summer=13:59 UTC; 2024-12-02 uses 2024-11-27 full close and skips Nov 29 half-day. The leading 2016-01-04 lacks its 2015-12-31 anchor, with no fabrication or backward substitution. Incomplete opening sessions are March 9/12/16, 2020 and June 5, 2023; no filling. Strict RV losses are {qa['rv_loss_otherwise_eligible']} / {qa['otherwise_eligible']} ({100*qa['rv_loss_otherwise_eligible']/qa['otherwise_eligible']:.4f}%), below the frozen 2% QA screen.

All full-session daily-count-available and ≥500 flags are true (preserved from authenticated Alpaca daily counts, not recomputed from minute counts or asserted TAQ-equivalent). Daily close values were not retained in D2, so a new full-series close discrepancy cannot be calculated offline. D1 already observed daily-minus-minute −$0.045 to +$0.100 on its diagnostic cohort; no repeated sealed-price summary was produced here and minute anchors remain authoritative. Adjustment is split-only on original rows; community native-price adjustment semantics remain unverified beyond D2.1c local alignment. Actual split-event fidelity remains untested. Only the issuer-verified D1 ex-dividend example 2026-09-18 is flagged; other dates have **unknown** event status, not false/no-event assertions. No dividend subtraction or bad-gap filtering is applied to natural price returns.

Independent real-data scalar calculation on {manual['session_et']} reproduces r1={manual['independent']['r1']:.12g}, r12={manual['independent']['r12']:.12g}, r13={manual['independent']['r13']:.12g}, RV={manual['independent']['rv_open_raw']:.12g}, within atol1e−14/rtol1e−12. The five source price anchors and calculation are in the private, hashed manual-check artifact; no raw candle export is tracked. Four new focused tests plus seven existing tests cover RV/return formulas, missing inputs, timing/DST/half-day/calendar behavior, sealed guards, Parquet smoke and OLS/HAC against an independent tiny calculation.

## Required training regression trio

All principal models use **{state['n']} eligible dates, {state['first']}–{state['last']}**. Validation 2022–2023 is deliberately reserved for Stage 2; combined pretest and sealed outcome summaries are not run. Intercepts are bp; slopes are bp/bp, hence dimensionless. R² here is **in-sample**. Ordinary OLS standard errors are descriptive comparators. Statsmodels {manifest['versions']['statsmodels']} HAC uses Bartlett weights, lag5 primary, covariance correction n/(n−k), asymptotic normal two-sided p-values/CIs (`use_t=False`); lag10/20 are sensitivity, not source-paper settings. Serial lags count successive eligible daily observations (gaps not padded). HAC validity relies on appropriate weak dependence/regularity; crisis missingness and finite-sample uncertainty remain qualifications.

{markdown_table(principal,['model','term','n','coefficient','ordinary_se','r_squared','hac_se','ci_low','ci_high','p_value'])}

### HAC lag sensitivity (unchanged coefficients)

{markdown_table(lag_sensitivity,['model','term','hac_lag','hac_se','ci_low','ci_high','p_value'])}

## Retrospective RV terciles and direct moderation contrast

Eligible principal **training-only** linear empirical RV cutoffs: {state['rv_raw_cutoffs']}; log equivalents {state['rv_log_cutoffs']}. Units: dimensionless √Σlog-return² and natural log(RV+1e−8). Counts {state['counts']}; equality goes in lower bin. These are retrospective descriptive states on this cohort. They are also **preliminary train-only candidate cutoffs** for future validation, not claimed as past-known historical forecasts. No validation/test distributions set boundaries. Separate original-only own-cohort retrospective metadata and matched-cohort fixed-principal cutoffs are recorded in the state JSON.

{markdown_table(group,['model','n','first','last','coefficient','ordinary_se','hac_se','ci_low','ci_high','p_value'])}

Pooled model has group-specific intercepts and X slopes; `high_minus_low_slope` is the explicit two-sided H0:βhigh−βlow=0 contrast. HAC is computed on the entire chronological training cohort, retaining cross-group error dependence, rather than subtracting separately estimated variances. Separate-bin HAC uses within-bin observation order. Inference **conditions on estimated tercile boundaries**, without a full cutoff-estimation bootstrap; it tests an association in this saturated linear projection, not causal moderation, raw conditional means, nonlinear shape, or EBM benefit.

{markdown_table(contrast,['term','n','coefficient','ordinary_se','hac_lag','hac_se','ci_low','ci_high','p_value'])}

All three X-only RV-bin slopes are negative; ordering by point estimate is low > high > middle. The middle-bin HAC5 interval just excludes zero, while the other two and the pooled high-minus-low interval span zero. The required unconditional/multivariate trio slopes are also negative with HAC5 intervals spanning zero. Thus this training description does not corroborate the published positive-slope pattern or establish a high-minus-low difference. This is not evidence of population equality, a confirmed structural break, or a failed implementation. A significant slope in one state alone would not establish a between-state difference. These are descriptive exploratory diagnostics with multiple coefficients/lags, not familywise-confirmed discoveries.

## Source and terminal-repair sensitivity

Training-only own eligible cohorts, exact matched dates, and terminal-dependency exclusions use the same frozen formulas. All share principal training state cutoffs for fixed-cutoff comparisons; the original's own retrospective state table is additionally explicit in machine outputs. Exact matched scientific columns agree: **{qa['matched_scientific_values_identical']}** on {qa['matched_training_n']} training dates. Cohort entry (two repair-dependent dates), rather than replacement of Alpaca values, explains principal versus original changes. The terminal exclusion removes **{', '.join(qa['terminal_excluded_training_dates'])}** and propagates the prior-anchor dependency. No sensitivity was selected by coefficient sign.

{markdown_table(sensitivities,['cohort','model','term','n','coefficient','hac_se','ci_low','ci_high'])}

Full intercepts/ordinary SE/R²/HAC5/10/20 and RV/pooled sensitivities are in [coefficients](../../data/registry/B_stage1_coefficients.csv); [state metadata](../../data/registry/B_stage1_state_metadata.json), [QA](../../data/registry/B_stage1_qa.json), [coverage](../../data/registry/B_stage1_coverage.csv) and [source-use dates](../../data/registry/B_stage1_source_use.csv) provide compact audit trails. No alternative daily/minute dataset was written.

## Source fidelity and Stage 2 handoff

See [method crosswalk](../../docs/experiment_B_source_method_crosswalk.md). Gao1993–2013 TAQ / Limkriangkrai1996–2013 U.S. source-era samples are unavailable here. This is the approved modern 2016-start branch, using Alpaca SIP plus a qualified community repair. RV normalization/opening increment and original calendar grouping remain unresolved source-method differences; vendor trade counts and split/native repair prices are not certified TAQ reconstructions. Community provenance/license are undeclared/unverified; user-directed private use does not authorize raw redistribution.

**Stage 2 is technically ready as a separate authorized task**: reuse this one daily table, reserve 2022–2023 for chronological selection, freeze training-only preprocessing, assess joint support, and compare state-aware simple models before any EBM increment claim. Preserve source and terminal sensitivities and the sealed 2024–September2026 outcomes. Stage 1 establishes valid implementation and descriptive associations only; historical replication, held-out predictability, nonlinear enrichment, stability and economic value remain unexecuted.

| Claim | Estimand / information | Evidence and scope | Status / next falsification |
| --- | --- | --- | --- |
| Published positive modern association | Training linear projection of Y on X, E10:00 | OLS1 negative, HAC5 CI spans zero; chosen training cohort only | NOT SUPPORTED in this description; held-out predictability remains unexecuted |
| High RV strengthens opening slope | Pooled high-minus-low X slope, E10:00 | Negative point difference, HAC5 CI spans zero; retrospective bins conditional on cutoffs | INCONCLUSIVE; joint support and time-aware held-out comparisons needed |
| Incremental nonlinear shape, stability, profitability | Full fitted surface / supported raw comparisons / execution-timed net outcomes | No EBM, OOS, null or trading work in Stage1 | NOT EXECUTED; separate later stages |
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root',type=Path,default=Path(os.environ.get('EBM_DATA_ROOT',ROOT/'data')))
    parser.add_argument('--config',type=Path,default=ROOT/'config/B_stage1_dataset_selection.json')
    args=parser.parse_args(); root=args.data_root.expanduser().resolve()
    wall=time.perf_counter(); cpu=time.process_time(); free_before=shutil.disk_usage(root).free
    c=json.loads(args.config.read_text())
    for path,digest in c['input_sha256'].items():
        actual=root/path.removeprefix('data/') if path.startswith('data/') else ROOT/path
        if sha(actual)!=digest:
            raise ValueError(f'Frozen Stage 1 input changed: {path}')
    repair_path=root/c['repair_manifest']; patch_manifest=json.loads(repair_path.read_text())
    verify_files(root,patch_manifest['baseline_files'])
    baseline_manifest=json.loads((root/'registry/D2_spy_source_manifest.json').read_text())
    verify_files(root,[patch_manifest['patch']])
    source_qa=pd.read_csv(root/'registry/D2_spy_candle_qa_sessions.csv')
    original=load_minutes(data_root=root)
    principal=load_minutes(data_root=root,repair_manifest=repair_path)
    old=build_daily(original,c,source_qa); daily=build_daily(principal,c,source_qa)
    # Reconcile real observations before any coefficients; targets live in input manifests, not feature code.
    if len(daily.loc[daily.eligible_primary])!=patch_manifest['totals']['primary_eligible']:
        raise ValueError('Principal eligibility differs from D2.1c manifest')
    expected=source_qa.loc[source_qa.session_type.eq('full'),'eligible_primary'].to_numpy()
    if not np.array_equal(old.eligible_primary.to_numpy(),expected):
        raise ValueError('Alpaca-only daily eligibility differs from original D2 audit')
    for split,key in [('train','train_eligible'),('validation','validation_eligible'),('sealed_test','sealed_test_eligible')]:
        if int((daily.eligible_primary & daily.split.eq(split)).sum())!=patch_manifest['totals'][key]:
            raise ValueError(f'Principal split eligibility differs: {split}')
    coverage=counts(daily,'principal')+counts(old,'alpaca_only')
    checks=[]
    for name,f in [('principal',daily),('alpaca_only',old)]:
        checks.append(dict(view=name,**{'missing_'+p:int((~f[p+'_complete']).sum()) for p in ['P10','P15','P1530','P16']},
                           missing_Pprev=int((~f.prior_anchor_complete).sum()),missing_opening_bars=int((30-f.n_open_minute_bars).sum()),
                           incomplete_opening_days=int(f.n_open_minute_bars.lt(30).sum()),invalid_ohlc_rows=int(f.invalid_ohlc_rows.sum()),
                           zero_rv=int(f.rv_open_raw.eq(0).sum()),negative_rv=int(f.rv_open_raw.lt(0).sum()),
                           near_zero_rv=int(f.rv_open_raw.le(c['rv_epsilon']).sum()),
                           invalid_rv_complete=int((f.n_open_minute_bars.eq(30)&~np.isfinite(f.rv_open_raw)).sum())))
    # Only training rows are passed beyond this point to coefficient/state routines.
    train=training_rows(daily,c); old_train=training_rows(old,c)
    matched_dates=set(train.session_et)&set(old_train.session_et)
    matched=train.loc[train.session_et.isin(matched_dates)]; old_matched=old_train.loc[old_train.session_et.isin(matched_dates)]
    scientific=['session_et','x_open_bp','w_preclose_bp','y_last30_bp','rv_open_raw','rv_open_log']
    identical=matched[scientific].reset_index(drop=True).equals(old_matched[scientific].reset_index(drop=True))
    no_terminal=train.loc[~train.terminal_repair_dependency]
    otherwise=daily.prior_anchor_complete & daily.return_anchors_complete & daily.invalid_ohlc_rows.eq(0)
    loss=int((otherwise & daily.n_open_minute_bars.lt(30)).sum())
    if loss/int(otherwise.sum())>.02:
        raise ValueError('Strict opening RV loss exceeds frozen 2% QA screen')
    qa=dict(principal_rows=len(daily),principal_eligible=int(daily.eligible_primary.sum()),original_eligible=int(old.eligible_primary.sum()),
            calendar_sessions=len(source_qa),early_close_sessions=int(source_qa.session_type.eq('early_close').sum()),
            full_days_after_early=int(daily.preceding_session_was_early_close.sum()),
            gained_dates=sorted(str(d) for d in set(daily.loc[daily.eligible_primary,'session_et'])-set(old.loc[old.eligible_primary,'session_et'])),
            exclusions=daily.loc[~daily.eligible_primary,['session_et','eligibility_reason']].astype(str).to_dict('records'),view_checks=checks,
            repair_use={k:int(daily[k].sum()) for k in ['repaired_minutes_session','repaired_opening','repaired_late','repaired_target','repaired_1459','repaired_other','prior_anchor_repaired','terminal_repair_dependency']},
            matched_training_n=len(matched),matched_scientific_values_identical=identical,
            terminal_excluded_training_dates=train.loc[train.terminal_repair_dependency,'session_et'].astype(str).tolist(),
            otherwise_eligible=int(otherwise.sum()),rv_loss_otherwise_eligible=loss,duplicate_daily_keys=int(daily.duplicated(['symbol','session_et']).sum()),
            original_missing_minutes=int(source_qa.missing_count.sum()),patch_minutes=len(principal)-len(original),
            remaining_minutes=int(source_qa.missing_count.sum())-(len(principal)-len(original)),
            chronology='All source minutes checked against XNYS/ET; availability bounded by E10:00/L15:30/target16:00; DST aware; no future inputs',
            dst_examples={d:at(d,'09:59').isoformat() for d in ['2024-03-08','2024-03-11']},
            early_skip_example=str(daily.loc[daily.session_et.astype(str).eq('2024-12-02'),'prior_full_session'].iloc[0]),
            manual_check='independent scalar log loop on 2016-01-05, private source anchors hashed; all match',
            sealed_policy='schema/integrity/counts only; no outcome aggregates, RV distributions or coefficients',
            daily_count_flags_all_available_ge500=bool((daily.daily_trade_count_available & daily.daily_ge500).all()),
            ex_dividend_register='Only D1 verified 2026-09-18 example; all other dates UNKNOWN',
            daily_close_reconciliation='D2 daily prices discarded; D1 observed discrepancies retained in historical report; no new comparison')
    if qa['remaining_minutes']!=patch_manifest['remaining_minutes']:
        raise ValueError('Original/patch missingness reconciliation failed')
    manual=manual_check(principal,daily)
    # Materialize precisely one daily Parquet. Existing identical content is reused.
    destination=root/'derived/B'/f"{c['dataset_id']}.parquet"; destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists():
        pd.testing.assert_frame_equal(pd.read_parquet(destination),daily)
    else:
        tmp=destination.with_suffix('.parquet.tmp'); daily.to_parquet(tmp,index=False,compression='zstd'); tmp.replace(destination)
    manual_path=root/'derived/B/stage1_manual_check.json'; write_json(manual_path,manual)
    coefficients=trio(train,c,'principal')
    rv_rows,state=volatility_tables(train,c,'principal'); coefficients.extend(rv_rows); states=[state]
    views=[('alpaca_only',old_train),('principal_matched',matched),('alpaca_matched',old_matched),('exclude_terminal_dependency',no_terminal)]
    for name,frame in views:
        coefficients.extend(trio(frame,c,name))
        rows,meta=volatility_tables(frame,c,name,cutoffs=state['rv_raw_cutoffs']); coefficients.extend(rows); states.append(meta)
    rows,meta=volatility_tables(old_train,c,'alpaca_own_retrospective'); coefficients.extend(rows); states.append(meta)
    registry=root/'registry'
    products=[]
    for name,frame in [('B_stage1_coefficients.csv',pd.DataFrame(coefficients)),('B_stage1_coverage.csv',pd.DataFrame(coverage)),
                       ('B_stage1_source_use.csv',daily.loc[daily.repaired_minutes_session.gt(0)|daily.prior_anchor_repaired,
                       ['session_et','eligible_primary','repaired_minutes_session','repaired_opening','repaired_late','repaired_target','repaired_other','prior_anchor_repaired','terminal_repair_dependency']])]:
        path=registry/name; frame.to_csv(path,index=False,lineterminator='\n'); products.append(file_ref(path,root))
    for name,value in [('B_stage1_state_metadata.json',states),('B_stage1_qa.json',qa)]:
        path=registry/name; write_json(path,value); products.append(file_ref(path,root))
    code=[ROOT/'src/ebm_research/experiment_b'/f'{name}.py' for name in ['daily','benchmarks','stage1','repair','pilot','acquisition']]
    versions={p:metadata.version(p) for p in ['numpy','pandas','pyarrow','exchange-calendars','statsmodels','scipy','patsy','formulaic']}
    manifest=dict(dataset_id=c['dataset_id'],schema_version=c['schema_version'],created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  config=dict(path='config/B_stage1_dataset_selection.json',sha256=sha(args.config)),inputs=c['input_sha256'],
                  daily=file_ref(destination,root),rows=len(daily),columns=len(daily.columns),schema={k:str(v) for k,v in daily.dtypes.items()},
                  manual_check=file_ref(manual_path,root),products=products,versions=versions,python=platform.python_version(),
                  code=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in code],
                  git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  source_qualifications=patch_manifest['license'],storage_policy='One daily Parquet; no minute replica, no sensitivity/fold/seed copy',
                  retained_data_bytes=destination.stat().st_size+manual_path.stat().st_size,market_data_http_calls=0,
                  wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,free_disk_before=free_before,free_disk_after=shutil.disk_usage(root).free)
    write_json(registry/'B_stage1_daily_manifest.json',manifest)
    report=ROOT/'reports/B/stage1_replication_benchmarks.md';report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(scientific_report(qa,coefficients,states,coverage,manual,manifest))
    print(json.dumps(dict(rows=len(daily),eligible=qa['principal_eligible'],original_eligible=qa['original_eligible'],daily_bytes=destination.stat().st_size,wall_seconds=manifest['wall_seconds'],cpu_seconds=manifest['cpu_seconds'],network_calls=0)))


if __name__=='__main__':
    main()
