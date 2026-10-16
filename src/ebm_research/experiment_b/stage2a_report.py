"""Eight compact Stage2A figures and standalone scientific/method reports."""
import os
import json
import numpy as np
import pandas as pd
from scipy import stats
from .pilot import ROOT
from .stage1 import markdown_table
from .state_models import evaluate_linear,slope_vector,vector_at


def table(rows,columns):
    return markdown_table([{c:'—' if c not in r or pd.isna(r[c]) else r[c] for c in columns} for r in rows],columns)


def make_figures(train,validation,fits,protocol,predictions,metrics,inferences,diagnostics):
    """Training fixed-basis shapes plus explicitly labeled2022–23 validation."""
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'logs/stage2A_matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    out=ROOT/'artifacts/B/stage2A';out.mkdir(parents=True,exist_ok=True);paths=[]
    def save(fig,name):
        fig.tight_layout();p=out/(name+'.png');fig.savefig(p,dpi=120,bbox_inches='tight',facecolor='white');plt.close(fig);paths.append(p)
    inf=pd.DataFrame(inferences);pre=protocol['preprocessing']
    groups=np.searchsorted(pre['cutoffs_raw'],train.rv_open_raw,side='left')
    a=protocol['support']['x_magnitude'];edges=protocol['support']['x_bins']
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,info in zip(axes,['E','L']):
        counts=np.zeros((3,3),dtype=int);blocks=counts.copy()
        w=np.ones(len(train),dtype=bool) if info=='E' else train.w_preclose_bp.between(*protocol['support']['w_band']).to_numpy()
        xb=np.searchsorted(edges,train.x_open_bp,side='right')
        for j in range(3):
            for k in range(3):
                mask=(groups==j)&(xb==k)&w;counts[j,k]=mask.sum();blocks[j,k]=len(np.unique((np.arange(len(train))//5)[mask]))
        ax.imshow(counts,cmap='Blues',vmin=0)
        for j in range(3):
            for k in range(3):
                label=f'n={counts[j,k]}\nblocks={blocks[j,k]}'
                if counts[j,k]<50 or blocks[j,k]<20:label+='\nABSTAIN'
                ax.text(k,j,label,ha='center',va='center',color='darkred' if counts[j,k]<50 else 'black')
        ax.set(xticks=range(3),xticklabels=[f'X < {edges[0]:g}',f'{edges[0]:g} ≤ X < {edges[1]:g}',f'X ≥ {edges[1]:g}'],
               yticks=range(3),yticklabels=['low RV','middle RV','high RV'],title=info+' training joint support')
    fig.suptitle('Training support: ≥50 observations and ≥20 disjoint five-row blocks',y=1.02);save(fig,'01_joint_support')
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,info in zip(axes,['E','L']):
        for j,state in enumerate(['low','middle','high']):
            for k,family in enumerate(['C1','C2','S4','S6']):
                part=inf.loc[inf.model_id.eq(f'{family}_{info}')&inf.contrast.eq('X_slope')&inf.state.eq(state)]
                r=part.iloc[0]
                if r.status=='COMPUTED':ax.errorbar(k+(j-1)*.19,r.estimate,yerr=[[r.estimate-r.ci_low],[r.ci_high-r.estimate]],fmt='o',color=['tab:blue','tab:orange','tab:red'][j],capsize=2,label=state if k==0 else None)
        ax.axhline(0,color='gray',lw=.7);ax.set(xticks=range(4),xticklabels=['C1','C2','S1 df4','S1 df6'],ylabel='X slope (bp/bp)',title=info+' training fitted slopes / HAC5')
        ax.text(.02,.03,'High state: ABSTAIN, insufficient X≈0 cell',transform=ax.transAxes,color='darkred',fontsize=8);ax.legend()
    save(fig,'02_state_slopes')
    fig,axes=plt.subplots(2,2,figsize=(11,7));zgrid=np.linspace(*np.quantile(train.rv_open_log,[.05,.95]),90)
    for col,info in enumerate(['E','L']):
        for family,color in [('C2','black'),('S4','tab:blue'),('S6','tab:orange')]:
            fit=fits[f'{family}_{info}'];mask=zgrid<=pre['cutoffs_log'][1]
            for row,kind in [(0,'intercept'),(1,'slope')]:
                vals=[evaluate_linear(fit,vector_at(fit,0,z) if kind=='intercept' else slope_vector(fit,z)) for z in zgrid]
                est=np.array([r['estimate'] for r in vals]);lo=np.array([r['ci_low'] for r in vals]);hi=np.array([r['ci_high'] for r in vals])
                axes[row,col].plot(zgrid[mask],est[mask],color=color,label=family)
                axes[row,col].fill_between(zgrid[mask],lo[mask],hi[mask],color=color,alpha=.12)
        for ax in axes[:,col]:
            ax.axvspan(pre['cutoffs_log'][1],zgrid.max(),color='gray',alpha=.15)
            ax.set(xlabel='Z = log(opening RV + 1e−8)',title=info+' fixed training basis, pointwise HAC5');ax.legend()
        axes[0,col].set_ylabel('intercept at X=0,W=0 (bp)');axes[1,col].set_ylabel('X slope (bp/bp)')
    fig.suptitle('Fitted varying coefficients; gray high-state anchor region ABSTAIN',y=1.01);save(fig,'03_varying_coefficients')
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    for j,info in enumerate(['E','L']):
        for family in ['C1','C2','S4']:
            p=inf.loc[inf.model_id.eq(f'{family}_{info}')&inf.contrast.eq('anchored_X_response')&inf.state.eq('low')&inf.status.eq('COMPUTED')].sort_values('x')
            axes[0,j].plot(p.x,p.estimate,label=family);axes[0,j].fill_between(p.x.to_numpy(float),p.ci_low.to_numpy(float),p.ci_high.to_numpy(float),alpha=.12)
        axes[0,j].set(title=info+' supported low-RV anchored fitted response',xlabel='X (bp), x0=0',ylabel='m(X,z)−m(0,z) (bp)');axes[0,j].legend()
        axes[1,j].text(.5,.5,'High-minus-low four-point contrast\nABSTAIN\nHigh-RV X≈0 joint cell below support minimum',ha='center',va='center',transform=axes[1,j].transAxes,color='darkred')
        axes[1,j].set(xlim=(-a,a),xlabel='X (bp)',ylabel='D(X) (bp)',title=info+' support-masked scientific contrast')
    fig.suptitle('Whole-response contrast vectors; HAC5 pointwise fixed-basis intervals',y=1.01);save(fig,'04_supported_anchored_contrasts')
    fig,axes=plt.subplots(3,4,figsize=(15,9))
    for i,family in enumerate(['C1','C2','S4']):
        for j,info in enumerate(['E','L']):
            r=fits[f'{family}_{info}']['result'];u=np.asarray(r.resid)
            ax=axes[i,2*j];ax.scatter(r.fittedvalues,u,s=4,alpha=.2);ax.axhline(0,color='black',lw=.6)
            ax.set(title=f'{family}_{info}',xlabel='fitted Y (bp)',ylabel='residual (bp)')
            qq,ordered=stats.probplot((u-u.mean())/u.std(ddof=1),fit=False)
            ax=axes[i,2*j+1];ax.scatter(qq,ordered,s=4,alpha=.4);ax.plot([-3.4,3.4],[-3.4,3.4],color='orange')
            ax.set(title=f'{family}_{info} normal QQ reference',xlabel='normal quantile',ylabel='standardized residual')
    fig.suptitle('FULL training diagnostics; normality is not a prerequisite for HAC',y=1.01);save(fig,'05_residual_and_qq')
    fig,axes=plt.subplots(2,3,figsize=(14,6))
    for i,info in enumerate(['E','L']):
        u=np.asarray(fits[f'S4_{info}']['result'].resid);date=pd.to_datetime(train.session_et)
        axes[i,0].plot(date,u,lw=.5);axes[i,0].axvspan(pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31'),color='orange',alpha=.15)
        axes[i,0].set(title=f'S4_{info} training residual time',ylabel='residual (bp)',xlim=(date.min(),date.max()))
        axes[i,1].scatter(train.rv_open_raw,np.abs(u),s=4,alpha=.25)
        axes[i,1].set(xscale='log',yscale='symlog',xlabel='opening RV (log axis)',ylabel='|residual| (bp)',title='Conditional variance ≠ conditional mean');axes[i,1].set_ylim(bottom=0)
        predictor=train.x_open_bp if info=='E' else train.w_preclose_bp
        axes[i,2].scatter(predictor,u,s=4,alpha=.2);axes[i,2].axhline(0,color='black',lw=.6)
        axes[i,2].set(xlabel='X (bp)' if info=='E' else 'W (bp)',ylabel='residual (bp)',title='Original information-time predictor')
    save(fig,'06_variance_and_time')
    fig,axes=plt.subplots(2,2,figsize=(11,8))
    for j,info in enumerate(['E','L']):
        score=metrics.loc[metrics['mode'].eq('quarterly')&metrics.variant.eq('FULL')&metrics.model_id.isin([f'{f}_{info}' for f in ['C1','C2','S4']])].sort_values(['MSE','model_id'])
        best=score.model_id.iloc[0];p=predictions.loc[predictions['mode'].eq('quarterly')&predictions.variant.eq('FULL')&predictions.model_id.eq(best)]
        axes[0,j].hexbin(p.forecast,p.actual,gridsize=30,mincnt=1,bins='log',cmap='Blues')
        axes[0,j].set(title=f'{info} best primary descriptively: {best}',xlabel='forecast (bp)',ylabel='actual Y (bp)')
        for family in ['C1','C2','S4']:
            p=predictions.loc[predictions['mode'].eq('quarterly')&predictions.variant.eq('FULL')&predictions.model_id.eq(f'{family}_{info}')]
            means=p.assign(bin=pd.qcut(p.forecast,10,duplicates='drop')).groupby('bin',observed=True)[['forecast','actual']].mean()
            axes[1,j].plot(means.forecast,means.actual,'o-',ms=3,label=family)
        axes[1,j].axhline(0,color='gray',lw=.6);axes[1,j].set(xlabel='decile mean forecast (bp)',ylabel='decile mean actual Y (bp)',title='Validation calibration: ≈49–50 observations/bin');axes[1,j].legend()
    fig.suptitle('2022–2023 quarterly validation; selection and calibration exploratory',y=1.01);save(fig,'07_validation_predictions_calibration')
    fig,axes=plt.subplots(2,2,figsize=(13,8))
    for j,info in enumerate(['E','L']):
        ids=['N0','N1','OLS1_E' if info=='E' else 'OLS3_L']+[f'{f}_{info}' for f in ['C1','C2','S4','S6']]
        p=metrics.loc[metrics['mode'].eq('quarterly')&metrics.variant.eq('FULL')&metrics.model_id.isin(ids)].set_index('model_id').loc[ids]
        axes[0,j].bar(ids,p.RMSE,color=['gray','gray','gray','tab:blue','tab:orange','tab:green','tab:red']);axes[0,j].tick_params(axis='x',rotation=35)
        axes[0,j].set(title=info+' quarterly validation RMSE',ylabel='RMSE (bp)')
        for mid in ids[:3]+[f'C2_{info}',f'S4_{info}']:
            p=predictions.loc[predictions['mode'].eq('quarterly')&predictions.variant.eq('FULL')&predictions.model_id.eq(mid)]
            vals=[float(np.sqrt(p.loc[p.state.eq(state),'loss'].mean())) for state in ['low','middle','high']]
            axes[1,j].plot(range(3),vals,'o-',ms=3,label=mid)
        axes[1,j].set(xticks=range(3),xticklabels=['low RV','middle RV','high RV'],ylabel='RMSE (bp)',title='Same frozen states for every model');axes[1,j].legend(fontsize=7)
    save(fig,'08_validation_error_by_state')
    return paths


def write_report(manifest,protocol,registry,metrics,inferences,diagnostics,support,sensitivity,paired,coefficients=None):
    """Standalone results and compact exact-method register, all linked to machine rows."""
    report=ROOT/'reports/B/stage2A_state_linear_and_spline_results.md'
    methods=ROOT/'docs/experiment_B_stage2A_methods_and_model_registry.md'
    models=pd.DataFrame(registry);inf=pd.DataFrame(inferences);diag=pd.DataFrame(diagnostics);sens=pd.DataFrame(sensitivity)
    full=models.loc[models.variant.eq('FULL')&models['mode'].eq('fixed')]
    train_metrics=metrics.loc[metrics['mode'].eq('train_descriptive')]
    val_metrics=metrics.loc[metrics.variant.eq('FULL')&metrics['mode'].isin(['fixed','quarterly'])]
    stress_metrics=metrics.loc[~metrics.variant.eq('FULL')&metrics['mode'].eq('fixed')]
    family=inf.loc[inf.scope.eq('PREDECLARED_FAMILY')]
    extra=inf.loc[inf.kind.eq('WALD')&inf.lag.eq(5)&~inf.scope.eq('PREDECLARED_FAMILY')]
    slopes=inf.loc[inf.contrast.isin(['X_slope','intercept_at_X0_W0','high_minus_low_X_slope'])&inf.lag.eq(5)]
    overview=[]
    tests=['Koenker_BP_LM','White_LM','ARCH_LM_5','residual_LjungBox_5','squared_residual_LjungBox_5','Jarque_Bera','RESET_fitted_squared_HAC5']
    for _,m in full.iterrows():
        d=diag.loc[diag.fit_id.eq(m.fit_id)]
        row=dict(model_id=m.model_id,n=m.n,rank=m['rank'],parameters=m.parameters,condition=m.condition,R2=m.r_squared)
        for name in tests:
            part=d.loc[d.statistic.eq(name)];row[name+'_p']=part.p_value.iloc[0] if len(part) else None
        for name in ['Pearson_kurtosis','max_leverage']:
            part=d.loc[d.statistic.eq(name)];row[name]=part.estimate.iloc[0] if len(part) else None
        overview.append(row)
    recs=manifest['recommendations']
    validation_audit=manifest['validation_predictor_audit']
    headline='; '.join(f"{r['info']}: {r['descriptive_best_primary']} vs {r['best_reference']}, quarterly loss gain {r['mean_loss_gain']:.3f}bp², CI[{r['gain_ci_low']:.3f},{r['gain_ci_high']:.3f}], {r['status']}" for r in recs if r['mode']=='quarterly')
    shape_abstain=int(inf.status.eq('ABSTAIN').sum())
    full_support=[r for r in support if r['cohort']=='train']
    coeff=pd.DataFrame(coefficients)
    selected=coeff.loc[coeff.fit_id.str.endswith('_FULL_fixed')&coeff.covariance.eq('5')&coeff.term.isin(['X','X_DM','X_DH','X_Zc','W','W_DM','W_DH','W_Zc'])]
    image=lambda name:f'![{name}](../../artifacts/B/stage2A/{name}.png)'
    text=f"""# Experiment B Stage2A — state-dependent linear and varying-coefficient splines

**PASS WITH QUALIFICATIONS.** Completed C1,C2 and two S1 complexities for E10:00/L15:30, including optional labeled W moderation, naive and state-blind references. {len(full)} FULL regression candidates (10 state specifications,3 OLS references),2 naive rules. Training1,495 eligible dates2016-01-05–2021-12-31; validation497 eligible dates2022–2023; sealed683 dates received metadata/hash checks only. No EBM, source download, extra indicator, target/split change or trading analysis.

**Executive validation finding:** {headline}. Minimum observed MSE does not establish superiority. FULL stays primary regardless of exclusion results. These validation years are now development/model-comparison data and will be reused for EBMs; no independent final confirmation is claimed.

**Plain-language verdict: no convincing incremental benefit is established for C1/C2/S1 here.** None of the six predeclared training tests survives Holm adjustment. C1 is the best primary state-model benchmark descriptively, while the zero forecast has lower quarterly validation error and the splines lose more. Some fixed-fit late-model deletion/Huber sensitivities improve error, documenting instability rather than permission to replace FULL. Conditional variance remains strongly state-dependent even when the fitted mean is not predictively useful.

## Frozen source, design and baseline check

Single canonical daily table B_SPY_daily_split_source1_stage1_v1: immutable Alpaca SIP adjustment=split D2 plus exactly39 native-price source1 missing-key repairs. D2.1b never combined. X includes overnight and ends10:00; W is15:00–15:30; Y15:30–16:00, simple returns×10,000bp. Opening30minute RV and log(RV+1e−8) unchanged. E never uses W; L adds information and is not a model-only advantage over E.

Stage1 **{manifest['baseline_verification']['coefficient_lag_rows']} coefficient/lag rows reproduce**, maximum numeric difference{manifest['baseline_verification']['max_absolute_difference']:.3g}. March18,2020 five original price anchors and scalar return/RV calculation match the daily table. Its14minute12:57–13:10 gap lies outside required windows and is not a reason to discard the day. Actual prices stay in a tiny ignored, hashed audit; no raw vendor export in Git. Source-era/modern period, TAQ/vendor trade-count, native community adjustment/rights and actual split-event limitations remain as in the source crosswalk.

Protocol version{protocol['version']} froze preprocessing and choices before fitting/validation labels. A pre-fit wording clarification preserves original2016–2021 categorical cutoffs for **all** validation, including quarterly; earlier draft retained. Quarterly centering/spline knots/scales use strictly earlier history. No fitted-curve or validation-driven change to grids/variants.

Exact models (explicit intercept):

- C1-E: 1+X+D_M+D_H+XD_M+XD_H, low reference. C1-L adds common W; C1-L-Wmod additionally WD_M,WD_H.
- C2-E: 1+X+Zc+XZc, with Zc=Z−training median. C2-L adds common W; C2-L-Wmod additionally WZc.
- S1: natural restricted cubic spans of dimensions4(primary) or6(sensitivity) for both intercept and X slope. Matrices contain literal C2 columns plus K−2 curvature columns H_j and XH_j; E ranks8/12,L9/13. L common W. No extra W spline, penalization or model-family search.
- N0=0. N1 is daily expanding past eligible-target mean: first training prediction0 then prior targets; validation initialized from training and updated only after each prior validation close. Same causal N1 denominator for fixed/quarterly. OLS1-E,OLS3-L and OLS2-L retained.

[Exact methods/model registry](../../docs/experiment_B_stage2A_methods_and_model_registry.md) defines knots, basis normalization, linear tails, dates, units and covariance. [Protocol](../../config/B_stage2A_linear_spline_protocol.json) and manifest preserve numerical preprocessing and all attempts. No silent rank/column deletion.

## Training fit and parameter inference

{table(full.to_dict('records'),['model_id','info','n','parameters','rank','condition','r_squared','adjusted_r_squared','fit_seconds'])}

{table(train_metrics.to_dict('records'),['model_id','n','RMSE','MAE','MSE','bias','R2_N0','R2_causal_N1','Pearson','directional_accuracy','p95_absolute_error'])}

Ordinary OLS SE are descriptive; primary Bartlett HAC5 uses n/(n−k) and normal two-sided95% CI/p, with HC3 and HAC10/20. Ordinary comparator CIs also use normal reference for consistency. Lag unit is surviving eligible daily observations. Severe tail/dependence/influence findings do not disappear by adding state functions; no test proves exogeneity/finite moments/weak dependence.

Six predeclared tests, Holm-adjusted across C1 X-state joint, C2 XZ and lower-df spline f/g curvature versus nestedC2, separately E/L:

{table(family.to_dict('records'),['model_id','contrast','df','statistic','p_value','holm_p_value','status'])}

Additional overall, pure-g curvature, nonconstant slope, optional W moderation and fixed2020 tests are exploratory:

{table(extra.to_dict('records'),['model_id','contrast','df','statistic','p_value','status'])}

Selected original/categorical interaction parameters, HAC5. These are **fixed-model projection coefficients**: C1 X_DH is its high-minus-low slope restriction, not an observed raw X0 cell mean. Unsupported raw anchored contrasts below remain ABSTAIN.

{table(selected.to_dict('records'),['model_id','term','estimate','se','ci_low','ci_high','p_value'])}

All intercepts/basis/original/interaction coefficients with ordinary/HC3/HAC5/10/20 are in B_stage2A_coefficients.csv. Correct whole-row contrast covariance vΣv′ is used; no subtraction of CI endpoints, and no comparison of bin p-values to establish a cross-bin difference.

## Supported response/slopes and abstentions

Frozen raw RV cutoffs{protocol['preprocessing']['cutoffs_raw']}, equality lower bin; Zref={protocol['preprocessing']['z_ref']}; within-tercile median Z={protocol['support']['z_representatives']}. X0=0; symmetric ±{protocol['support']['x_magnitude']}bp chosen strictly inside common training within-state10–90percentile range. L W0=0 screened within training central80% Wband{protocol['support']['w_band']}.

{table(full_support,['info','state','x_cell','n','blocks','supported','strong_support'])}

Pragmatic exploratory minimum50 observations/20nonoverlapping five-eligible-row blocks; strong100/30. **High-RV X≈0 has only22 E and15 L observations**. The grid was not widened after that discovery. Hence high-minus-low anchored scientific four-point contrasts ABSTAIN; {shape_abstain} support-abstained rows. Model projections remain estimable under parametric assumptions, but unsupported raw-cell claims/confident lines are withheld. Low/middle fitted slopes and whole-response/anchored comparisons with pointwise HAC fixed-basis CIs:

{table(slopes.to_dict('records'),['model_id','contrast','state','estimate','se','ci_low','ci_high','p_value','status'])}

Spline f and g include linear Z and nonlinear curvature explicitly; zero curvature nestsC2. Natural tails are linear outside first/last knot, never clipped. Validation predictor-only range/state/tail counts were computed before Y read and saved in the manifest. No raw conditional-mean derivative, causal effect, purification or EBM theorem is invoked.

Validation frozen-state occupancy is {validation_audit['state_counts']}; spline boundary-tail counts are {validation_audit['spline_boundary_exceedance']}. No validation Z exceeds the observed full-training Z range, while65 dates lie outside the inner boundary knots (linear tails). One validation W is below its full-training observed range. Per-quarter feature/extrapolation counts are separately registered for the past-only refits.

{image('01_joint_support')}
{image('02_state_slopes')}
{image('03_varying_coefficients')}
{image('04_supported_anchored_contrasts')}

## Full regression diagnostics

Every FULL state/reference fit receives the adapted Stage1.5 battery; full numeric statistics/nulls/assumptions/status in B_stage2A_model_diagnostics.csv. Below are exploratory test-reference p-values:

{table(overview,['model_id','Koenker_BP_LM_p','White_LM_p','ARCH_LM_5_p','residual_LjungBox_5_p','squared_residual_LjungBox_5_p','Jarque_Bera_p','RESET_fitted_squared_HAC5_p','Pearson_kurtosis','max_leverage'])}

Koenker BP uses each original design. White uses SVD auxiliary rank−1 where nonsingular; expanded interaction/spline squares/products are algebraically rank-deficient, so those White p-values are explicitly NOT_APPLICABLE rather than reported as valid inference. Candidate forecast matrices themselves remain full rank. IID-asymptotic diagnostic p-values under dependence are reference checks. ARCH5 uses parameter-count ddof; residual and squared Ljung–Box5/10/20 model_df0, ACF1/5/10/20,DW, JB/skew/Pearson kurtosis/extreme quantiles retained. Underflowed p0 is not mathematically zero. Normality is not an OLS/HAC prerequisite; nonrejection cannot prove independence.

Residual versus fitted/X/W/Z fixed10-bin means(min20), absolute/squared residual–RV correlations, state and2016–19/2020/2021 residual means/SD are saved. **Conditional variance is not conditional-mean improvement:** absolute residual versus RV Spearman remains about0.369–0.413 across full fits. Full rank/condition, named non-spline VIF and design correlations are reported; individual spline VIF is parameterization-dependent. Linear/C1/C2 fitted-square HAC RESET is exploratory; rich S1 uses nested curvature instead. Fixed-grid spline-slope turning points and maximum projected slopes are registered as wiggle/extrapolation diagnostics, not fitted raw derivatives.

All FULL fits report Cook/leverage/internal studentization top5 and small fixed-basis exact single-delete changes in high-minus-low projection slope. New Stage2 rankings are diagnostic only, never deletion keys. Knot re-estimation uncertainty is not represented by fixed-basis influence.

{image('05_residual_and_qq')}
{image('06_variance_and_time')}

## Outlier/stress/source and temporal sensitivity

Every C1/C2/S1 E/L (also higher-df/W variants) has FULL, DROP_TOP1(2020-03-18), DROP_TOP5(fixed Stage1.5 OLS1 ranking), EXCLUDE_2020 and MATCHED_SOURCE. Original preprocessing held fixed; all497validation days unchanged. HuberT1.345/MAD point comparisons for C1/C2/S4 and optional Wmod use different loss/estimand and no OLS/HAC claims. S6 Huber omitted as redundant sensitivity.

{table(sens.loc[sens.comparison.isin(['fixed_design_stress','Huber_point_only'])].to_dict('records'),['model_id','variant','n','low_slope','middle_slope','high_slope','projection_high_low_slope','status'])}

These point slopes quantify fitted projection instability; unsupported raw-cell uncertainty is withheld. Fixed-validation error changes for every variant are in B_stage2A_validation_metrics.csv; FULL is not replaced based on favorable p/sign/error. Matched-source removes Aug12/13 only, preserving the hashed Stage1 proof of identical original scientific fields for1,493 training dates. No second original/patch daily dataset made.

{table(stress_metrics.to_dict('records'),['model_id','variant','n','RMSE','MSE','delta_RMSE_vs_FULL','delta_MSE_vs_FULL'])}

Predeclared2016–19,2020,2021 and leave-year-out C2/S4 E/L are stored with sample/period support, fixed basis, fit IDs and covariance. Short-period unsupported raw contrasts abstain; there is no optimized breakpoint/rolling-window search. C2's parsimonious fixed2020 intercept+X interaction controls original state terms/W.

{table(sens.loc[sens.comparison.eq('period_fixed_basis')].to_dict('records'),['model_id','variant','n','low_slope','middle_slope','high_slope','status'])}

## Chronology-safe matched validation

Fixed models train only2016–2021. Quarterly Jan/Apr/Jul/Oct2022–2023 refits see only fully completed targets before each cutoff; original categorical cutoffs fixed, centering/spline transformations past-only. Every forecast stores cutoff and last target date; N1 uses prior days only.

{table(val_metrics.to_dict('records'),['model_id','info','mode','n','RMSE','MAE','MSE','bias','R2_N0','R2_causal_N1','Pearson','directional_accuracy','p95_absolute_error'])}

Bias=forecast−actual. Direction near zero exploratory; always-up/down and retrospective-majority baselines saved (latter explicitly descriptive). R² denominators name N0 and causal expandingN1. No financialP&L/cost/trade computation.

{image('07_validation_predictions_calibration')}
{image('08_validation_error_by_state')}

Supported prediction-decile calibration shows n; degenerate/tiny bins abstain. Validation state errors and absolute-error/forecast-magnitude correlations saved. All FULL/stress/Huber date predictions plus losses/differences againstOLS/N0/N1 in **one long Parquet**; no per-model input replicas. Paired mean comparator squared loss−candidate squared loss is positive for improvement. HAC5 and10/20 on a small spline subset:

{table(paired.loc[paired.lag.eq(5)].to_dict('records'),['model_id','comparator','info','mode','n','mean_loss_gain','ci_low','ci_high','p_value'])}

Forecast-loss uncertainty differs from parameter inference. Candidate/comparator ranking on these same validation years introduces selection/multiplicity; intervals are exploratory, not independent confirmation. No broad block/bootstrap/permutation program was necessary.

## Decision and EBM handoff

{table(recs,['info','mode','descriptive_best_primary','best_reference','candidate_MSE','reference_MSE','mean_loss_gain','gain_ci_low','gain_ci_high','status'])}

Retain FULL state-aware/OLS and observed stronger naive benchmarks on the same dates. Weak/reversed slopes and diagnostic failures remain valid results, not targets to rescue. Carry heavy tails/dependence, crisis influence, finite support, extrapolation, source rights/native one-sided repair and selected-validation inference caveats.

**Ready for a separate Stage2B EBM task**: canonical rows, correct E/L features, original predictive cutoffs, fixed/quarterly schedules, untrimmed primary and naive/OLS/C1/C2/S1 benchmarks are now explicit. Use matched validation and preserve2024–September2026 for later sealed protocol; no EBM fitted here. Unsupported high-state X0 four-point claims need a separately predeclared supported future-stage design or continued ABSTAIN.

Machine artifacts: B_stage2A_models/coefficients/inference/model_diagnostics/support/validation_metrics/paired_loss_tests/sensitivity.csv, one predictionParquet, protocol and manifest. Every displayed number is traceable to these or input hashes/preprocessing in the protocol.
"""
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(text)
    method_text=f"""# Experiment B Stage2A methods and exact model registry

Numerical results: [scientific report](../reports/B/stage2A_state_linear_and_spline_results.md). Exact numeric preprocessing and schedules: [protocol](../config/B_stage2A_linear_spline_protocol.json). All chronological fit/preprocessing/attempt identities: manifest/modelCSV.

{table(full.to_dict('records'),['model_id','family','info','parameters','rank','columns','role','status'])}

## Basis, units and nesting

For K=4/6 training Z knots, j=1…K−2:

h_j(z)=[(z−k_j)_+³−(kK−k_j)/(kK−k(K−1))·(z−k(K−1))_+³+(k(K−1)−k_j)/(kK−k(K−1))·(z−kK)_+³]/(kK−k1)².

Restricted/natural cubic: linear in both tails and span includes1,Z. Curvature projected off1,Zc by predictor-only training least squares, centered0 at Zref and divided by training residual SD. The invertible span transform aids conditioning. Matrices contain literal1,X,Zc,XZc plusH_j,XH_j; E2K parameters,L2K+1 withcommonW. Zero nonlinear blocks exactly nestsC2; testdf=2(K−2). Pureg curvature onlyXH; g nonconstant includesXZc. Full design/restriction covariance rank checked; no silent original-column dropping.

Y/X/W are simple-return bp, Z dimensionless logRV; coefficients on intercept/state main terms inbp, X/W slope and interaction coefficients scaled per stated basis unit. C1 low-reference indicators use exact raw RV cuts, equality lower bin. E does not readW; optional L-W moderation separate from primaryX question.

Zref={protocol['preprocessing']['z_ref']}; cutoffs={protocol['preprocessing']['cutoffs_raw']}.

{table([dict(dimension=k,quantiles=json.dumps(s['quantiles']),knots=json.dumps(s['knots']),boundaries=json.dumps(s['boundaries'])) for k,s in protocol['preprocessing']['splines'].items()],['dimension','quantiles','knots','boundaries'])}

Linear tails outside boundary knots, no clipping/future bounds; validation boundary/observed-range counts recorded before labels. Fixed deletion fits preserve full training preprocessing. Quarterly original categorical cuts unchanged; spline knots/Zref/scales fitted only on prior history. Basis inference conditions on these transforms and does not incorporate post-validation model-selection uncertainty.

## Estimation, uncertainty, choices

OLS stable SVD, full rank; ordinary/HC3/BartlettHAC5 primary10/20 sensitivity,n/(n−k),normal95%. vΣv′ for whole fitted contrasts; restrictioncovariance rank checked for jointWald. Six primarymoderation/curvature tests withHolm; everything else exploratory. Whiteauxiliary products may be algebraically redundant; actualSVD rank−1df. RESET used onlylinear/C1/C2, nestedcurvature forS1. No Gaussian/independence/exogeneity guarantee from residual tests.

FULL includesall1,495. DROP_TOP1/5 use priorOLS1keys,EXCLUDE_2020 distinct,MATCHED_SOURCE removesAug12/13; originalbasisfixed. Huberpoint-onlydifferentloss,noHAC. Everycandidate/refit/failure/influence attempt is inmodelsCSV; internalvariance/RESET auxiliaryregressions are diagnostic tests, not extraforecast candidates. Temporal2016–19/2020/2021 and leaveyearC2/S4 comparefixedbasis; no breakpointsearch.

Quarter starts {protocol['quarterly_schedule']}. Fit targetdate <forecastcutoff/date. N1 initializedtrainingmean, expandsdailyonlypreviousY; firsttrainforecast0. Samefixed/quarterlynaivecomparison. Rank sixprimaryFULL candidates byquarterlyMSE withinE/L; retainbestdescriptively, requirepositivepairedHAC5gainCI vsstrongestnaive/OLS forconvincingimprovement. FULL neverreplacedbytrimmedvariant. Higherdf/Wmod sensitivities notautomaticprimaryreplacements. Validationselectioninferenceexploratory andperiodreusedforfutureEBM; testsealed.

## Support, plots and reproduce

Xgrid±{protocol['support']['x_magnitude']}bp,x0=0; coarseboundaries±{protocol['support']['x_magnitude']/2:g}. LrequiresWoriginalcentral80%bandaround0. Cellminimum50/20nonoverlapfive-rowblocks,100/30strong, practicalnotformal. HighstateX0fails: anchoredhigh-lowscientificcontrastABSTAIN. Projectioncoefficientsare distinctfromrawconditionalmeans.

Existingrequirements-stage1_5.lock.txt+editablepackage, then python -B -m ebm_research.experiment_b.stage2a (optional --data-root PATH). Restoreauthorizedmatchingdaily/sourcefilesbyhash, noAPIcredentials/networkneeded. No newdependency/modelbinary/fulldatareplica/EBM. Protocolpreserved andstage-owned outputsregenerate.
"""
    methods.write_text(method_text)
    return report,methods
