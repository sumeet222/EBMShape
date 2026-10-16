"""Stage2B compact scientific figures and explicit negative/abstention reports."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

from .pilot import ROOT
from .ebm_models import STATES,groups,features,query_frame,candidate_rows


def figures(root,p,train,val,pred,vm,shapes,surfaces,heat,stability,diag,composition,primary):
    """Eleven reproducible figures; population shape claims always support masked."""
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'logs/stage2B_matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    folder=ROOT/'artifacts/B/stage2B';folder.mkdir(parents=True,exist_ok=True);paths=[]
    def save(fig,name,title):
        fig.suptitle(title,fontsize=11);fig.tight_layout(rect=[0,0,1,.96])
        path=folder/(name+'.png');fig.savefig(path,dpi=125,facecolor='white');plt.close(fig);paths.append(path)
    def axes_grid():return plt.subplots(1,2,figsize=(12,4.8))
    def selected(frame,info=None):
        q=frame.loc[frame.seed.eq(42)&frame.variant.eq('FULL')&frame['mode'].eq('fixed')]
        return q.loc[q['info'].eq(info)] if info else q
    fig,axes=axes_grid()
    for ax,info in zip(axes,['E','L']):
        c=p['contrast_grid'][info]['display_candidate'];m=np.ones(len(train),bool)
        if info=='L':m=abs(train.w_preclose_bp-c['w'])<=c['w_halfwidth']
        g=groups(train,p)
        for j,s in enumerate(STATES):ax.scatter(train.loc[m&(g==j),'x_open_bp'],train.loc[m&(g==j),'rv_open_log'],s=8,alpha=.35,label=s)
        for sign in [-1,1]:ax.axvspan(sign*c['a']-c['h'],sign*c['a']+c['h'],alpha=.1,color='black')
        rows=candidate_rows(train,p,c,'train')
        text='; '.join(f'{r["state"]} {r["endpoint"]:+g}: n{r["n"]}/b{r["blocks"]}' for r in rows)
        ax.set(title=f'{info}: {p["contrast_grid"][info]["status"]}',xlabel='X prior close→10:00 (bp)',ylabel='log opening RV')
        ax.text(.02,.02,text,transform=ax.transAxes,fontsize=6.5,wrap=True);ax.legend(fontsize=8)
    save(fig,'01_ebm_input_support','Training 2016–2021: local nonzero contrast bands; b = distinct 5-row blocks (full X range)')
    fig,axes=plt.subplots(2,3,figsize=(16,9))
    colors=dict(SB='gray',A0c='tab:blue',A0d='tab:cyan',A1d='tab:orange',A1c='tab:red',A2c='tab:purple')
    for ax,(info,state_name) in zip(axes.flat,[(i,s) for i in ['E','L'] for s in STATES]):
        q=selected(surfaces,info)
        for mid,part in q.loc[q.state.eq(state_name)].groupby('model_id'):
            part=part.sort_values('x');family=mid.split('_')[0]
            ax.plot(part.x,np.where(part.supported,part.forecast,np.nan),'o-',ms=3,color=colors[family],label=mid)
        # Reconstruct simple C1/C2/S4 on same points from registered coefficients only.
        from .state_models import specifications as linear_specs,design
        a=json.loads((ROOT/'config/B_stage2A_linear_spline_protocol.json').read_text())
        co=pd.read_csv(root/'registry/B_stage2A_coefficients.csv')
        for spec in linear_specs():
            if spec['info']!=info or spec['family'] not in ['C1','C2','S4'] or spec['w_moderation']:continue
            part=q.loc[q.model_id.eq('A1c_'+info)&q.state.eq(state_name)].sort_values('x')
            f=query_frame(part.x,p['z_representatives'][STATES.index(state_name)],p['contrast_grid'][info]['display_candidate']['w']);d=design(f,spec,a['preprocessing'])
            b=co.loc[co.fit_id.eq(spec['model_id']+'_FULL_fixed')&co.covariance.astype(str).eq('OLS')].set_index('term').reindex(d.columns).estimate.to_numpy()
            ax.plot(part.x,np.where(part.supported,d.to_numpy()@b,np.nan),'--',lw=1,label=spec['model_id'])
        ax.set(title=f'{info}: total F, {state_name} RV; W fixed for L',xlabel='X (bp)',ylabel='predicted signed Y (bp)');ax.legend(fontsize=6,ncol=3)
        ax.text(.02,.02,'Local ≥50 dates / ≥20 blocks only',transform=ax.transAxes,fontsize=7)
        if not q.loc[q.state.eq(state_name),'supported'].any():
            ax.text(.5,.5,'ABSTAIN\nNo supported local slice cells',ha='center',va='center',transform=ax.transAxes)
    save(fig,'02_ebm_model_ladder_shapes','FULL training fits, seed42; common supported total-response slices, no population confidence bands')
    fig,axes=axes_grid()
    for ax,info in zip(axes,['E','L']):
        h=heat.loc[heat['info'].eq(info)];table=h.pivot(index='z',columns='x',values='forecast');support=h.pivot(index='z',columns='x',values='supported')
        image=ax.pcolormesh(table.columns.to_numpy(float),table.index.to_numpy(float),np.ma.masked_where(~support.to_numpy(bool),table.to_numpy()),cmap='coolwarm',shading='nearest')
        fig.colorbar(image,ax=ax,label='total F (bp)')
        model=primary['A1c_'+info]
        for edge in model.bins_[0][0]:
            if -50<=edge<=50:ax.axvline(edge,alpha=.18,lw=.5,color='black')
        zi=model.feature_names_in_.index('Z')
        for edge in model.bins_[zi][0]:ax.axhline(edge,alpha=.15,lw=.5,color='black')
        ax.scatter(np.full(len(train),-53),train.rv_open_log,s=1,alpha=.12,color='black',clip_on=False)
        ax.set(title=f'{info}: local |ΔX|≤10bp, |ΔZ|≤0.2; W band±20 L',xlabel='X (bp)',ylabel='log opening RV',ylim=(table.index.min()-.1,table.index.max()+.1))
    save(fig,'03_ebm_continuous_heatmap','FULL A1c seed42; masked cells <50 dates/20 blocks; lines are actual native main-bin edges; left rug = train Z')
    fig,axes=axes_grid()
    for ax,info in zip(axes,['E','L']):
        q=selected(shapes,info);q=q.loc[q.model_id.str.startswith(('SB','A0','A1','A2'))]
        if p['contrast_grid'][info]['chosen']:
            ax.bar(q.model_id,q.D_F,color=['gray' if x.startswith(('SB','A0')) else 'tab:orange' for x in q.model_id])
            ax.tick_params(axis='x',rotation=35);ax.axhspan(-1,1,color='green',alpha=.1,label='±1bp materiality only')
            ax.legend(fontsize=7)
        else:ax.text(.5,.5,'ABSTAIN\nNo local joint-support candidate passes',ha='center',va='center',transform=ax.transAxes)
        c=p['contrast_grid'][info]['display_candidate'];ax.set(title=f'{info}: X={-c["a"]:g}→{c["a"]:g}bp; W={c["w"]:g}',ylabel='high−low fitted X increment D_F (bp)')
    save(fig,'04_supported_nonzero_contrasts','Four whole-model predictions at frozen state medians; no certified pointwise CI; broad-band support ≠ population identification')
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    g=groups(train,p)
    for j,s in enumerate(STATES):axes[0,0].hist(train.loc[g==j,'rv_open_log'],bins=25,alpha=.45,label=s)
    for cut in np.log(np.asarray(p['cutoffs_raw'])+1e-8):axes[0,0].axvline(cut,color='black',ls='--')
    axes[0,0].set(xlabel='log RV',ylabel='training dates',title='Same underlying continuous state / frozen terciles');axes[0,0].legend()
    for ax,info in zip(axes[1],['E','L']):
        for mid in ['A1d_'+info,'A1c_'+info]:
            q=selected(surfaces,info);q=q.loc[q.model_id.eq(mid)&q.state.eq('middle')].sort_values('x')
            ax.plot(q.x,np.where(q.supported,q.forecast,np.nan),'o-',ms=3,label=mid)
        ax.set(title=f'{info}: middle-state total slice, support masked',xlabel='X (bp)',ylabel='F (bp)');ax.legend()
    for info in ['E','L']:
        s=next(s for s in p['models'] if s['model_id']=='A1c_'+info);d=next(s for s in p['models'] if s['model_id']=='A1d_'+info)
        cp=primary[s['model_id']].predict(features(train,s,p));dp=primary[d['model_id']].predict(features(train,d,p))
        axes[0,1].scatter(train.rv_open_log,cp-dp,s=5,alpha=.2,label=info)
    axes[0,1].set(xlabel='log opening RV',ylabel='A1c−A1d prediction (bp)',title='Observed rows: also depends on X/W; descriptive');axes[0,1].legend()
    save(fig,'05_ebm_discrete_continuous_comparison','FULL seed42: discretization changes state resolution; no exact retained-space theorem is instantiated')
    fig,axes=plt.subplots(2,4,figsize=(14,7))
    for j,mid in enumerate(['SB_E','A0c_E','A1d_E','A1c_E']):
        q=pred.loc[pred.model_id.eq(mid)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq('fixed')&pred.cohort.eq('train')]
        u=(q.actual-q.forecast).to_numpy();axes[0,j].hist(u,bins=45,color='tab:blue',alpha=.7)
        extreme=q.session_et.eq('2020-03-18');axes[0,j].axvline(u[extreme][0],color='red',label='2020-03-18')
        theoretical,ordered=stats.probplot((u-u.mean())/u.std(),fit=False)
        axes[1,j].scatter(theoretical,ordered,s=5);axes[1,j].plot([-3,3],[-3,3],color='gray')
        axes[0,j].set(title=mid,xlabel='residual Y−F (bp)',ylabel='count');axes[0,j].legend(fontsize=6)
        axes[1,j].set(xlabel='normal quantile',ylabel='residual / SD')
    save(fig,'06_ebm_residual_qq','FULL training residuals with entire tail range; normality reference is diagnostic, not EBM scientific inference')
    fig,axes=plt.subplots(2,3,figsize=(13,7))
    for i,info in enumerate(['E','L']):
        q=pred.loc[pred.model_id.eq('A1c_'+info)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq('fixed')&pred.cohort.eq('train')].sort_values('session_et')
        u=q.actual.to_numpy()-q.forecast.to_numpy();axes[i,0].plot(pd.to_datetime(q.session_et),u,lw=.5)
        axes[i,0].axvspan(pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31'),color='orange',alpha=.15)
        axes[i,0].set(title='A1c_'+info+' chronological residual',ylabel='residual (bp)')
        axes[i,1].scatter(train.rv_open_log,abs(u),s=5,alpha=.25);axes[i,1].set(xlabel='log RV',ylabel='absolute residual (bp)')
        axes[i,2].scatter(train.rv_open_log,u*u,s=5,alpha=.25);axes[i,2].set(xlabel='log RV',ylabel='squared residual (bp²)',yscale='symlog')
    save(fig,'07_ebm_variance_time','FULL A1c seed42: state-dependent conditional scale does not imply useful prediction of signed mean Y')
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    for i,info in enumerate(['E','L']):
        q=pred.loc[pred.model_id.eq('A1c_'+info)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq('quarterly')&pred.cohort.eq('validation')]
        axes[i,0].scatter(q.forecast,q.actual,s=8,alpha=.3);axes[i,0].set(title='A1c_'+info+' quarterly, all497days',xlabel='forecast (bp)',ylabel='actual signed Y (bp)')
        bins=pd.qcut(q.forecast,10,duplicates='drop');t=q.assign(bin=bins).groupby('bin',observed=True).agg(f=('forecast','mean'),y=('actual','mean'),n=('actual','size'))
        axes[i,1].plot(t.f,t.y,'o-')
        for _,r in t.iterrows():axes[i,1].annotate(f'n={int(r.n)}',(r.f,r.y),fontsize=6)
        lo=min(t.f.min(),t.y.min());hi=max(t.f.max(),t.y.max());axes[i,1].plot([lo,hi],[lo,hi],color='gray',ls='--')
        axes[i,1].set(title='Prediction-decile calibration, descriptive',xlabel='mean forecast (bp)',ylabel='mean actual (bp)')
    save(fig,'08_ebm_validation_calibration','Development validation 2022–2023, quarterly past-only refits, seed42; quantile summaries have no certified CI')
    fig,axes=axes_grid()
    q=vm.loc[vm.seed.eq(42)&vm.variant.eq('FULL')&vm['mode'].eq('quarterly')&vm.cohort.eq('validation_subgroup')&vm.dimension.eq('state')]
    for ax,info in zip(axes,['E','L']):
        for model in ['SB','A0c','A0d','A1d','A1c']+(['A2c'] if info=='L' else []):
            part=q.loc[q.model_id.eq(model+'_'+info)].sort_values('group');ax.plot(part['group'].astype(int),part.RMSE,'o-',label=model)
        ax.set(title=info+' matched validation, frozen states',xticks=[0,1,2],xticklabels=['low n31','middle n151','high n315'],ylabel='RMSE (bp)');ax.legend(fontsize=7)
    save(fig,'09_ebm_validation_error_by_state','497 validation dates per model/seed; state errors are exploratory with uneven occupancy')
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    for i,info in enumerate(['E','L']):
        q=stability.loc[stability.model_id.eq('A1c_'+info)&stability['mode'].eq('fixed')]
        labels=[f'{r.variant}/s{r.seed}' for _,r in q.iterrows()]
        axes[i,0].plot(np.arange(len(q)),q.validation_RMSE,'o');axes[i,0].axhline(q.loc[q.variant.eq('FULL')&q.seed.eq(42),'validation_RMSE'].iloc[0],color='gray',ls='--',lw=.8)
        axes[i,0].set(xticks=np.arange(len(q)),xticklabels=labels,ylabel='validation RMSE (bp)',title='A1c_'+info+' FULL/stress/rate/seed; dashed=FULL42');axes[i,0].tick_params(axis='x',rotation=70,labelsize=6)
        if p['contrast_grid'][info]['chosen']:
            axes[i,1].scatter(np.arange(len(q)),q.D_F);axes[i,1].set(xticks=np.arange(len(q)),xticklabels=labels,ylabel='fitted D_F (bp)',title='Seed/deletion stability; no sampling CI');axes[i,1].tick_params(axis='x',rotation=70,labelsize=6)
        else:axes[i,1].text(.5,.5,'Late scientific contrast ABSTAIN\nNo accepted local partner support',ha='center',va='center',transform=axes[i,1].transAxes)
    save(fig,'10_ebm_seed_outlier_stability','All5seeds and fixed FULL/top1/top5/2020/matched/rate sensitivities shown; FULL remains primary')
    fig,axes=plt.subplots(1,3,figsize=(14,4.8))
    c=composition.loc[composition.cohort.isin(['train','validation'])]
    for j,cohort in enumerate(['train','validation']):
        v=c.loc[c.cohort.eq(cohort)].set_index('state').loc[STATES];axes[0].bar(np.arange(3)+j*.35,v.fraction,width=.35,label=cohort)
    axes[0].set(xticks=np.arange(3)+.175,xticklabels=STATES,ylabel='fraction',title='Frozen terciles: composition shift');axes[0].legend()
    d=composition.loc[composition.cohort.eq('train_to_validation_MSE_decomposition')]
    for j,(_,r) in enumerate(d.iterrows()):axes[1].bar(np.arange(2)+j*.3,[r.composition_term,r.within_state_term],width=.3,label=r.model_id)
    axes[1].set(xticks=[.15,1.15],xticklabels=['mixture term','within-state term'],ylabel='MSE change (bp²)',title='Exact observed error decomposition');axes[1].legend(fontsize=7)
    axes[2].text(.5,.5,'Independent validation band fidelity:\nABSTAIN if any cell <50dates/20blocks\n\nTraining E band ≠ pointwise D_m\nLate joint-support design: ABSTAIN\nNo ±1bp equivalence certification',ha='center',va='center',transform=axes[2].transAxes)
    axes[2].set_title('Scientific fidelity / materiality limits')
    save(fig,'11_ebm_state_composition_fidelity','Observed error decomposition also includes training optimism; no causal correction, population shape or stability proof')
    fig,axes=plt.subplots(2,3,figsize=(13,8))
    for i,info in enumerate(['E','L']):
        model=primary['A1c_'+info]
        for j,name in enumerate(['X','Z']):
            index=next(k for k,t in enumerate(model.term_features_) if t==(model.feature_names_in_.index(name),))
            score=model.term_scores_[index];axes[i,j].step(np.arange(len(score)),score,where='mid')
            axes[i,j].set(title=f'A1c_{info}: {name} native centered main',xlabel='native bin index (actual cuts in registry)',ylabel='software term score (bp)')
        index=next(k for k,t in enumerate(model.term_features_) if len(t)==2)
        image=axes[i,2].imshow(model.term_scores_[index].T,origin='lower',aspect='auto',cmap='coolwarm')
        fig.colorbar(image,ax=axes[i,2],label='software term score (bp)')
        axes[i,2].set(title=f'A1c_{info}: X×Z centered software component',xlabel='X interaction-bin index',ylabel='Z interaction-bin index')
    save(fig,'12_ebm_native_components','Software diagnostic including missing/unknown bins; centered terms are not unique scientific effects or population confidence statements')
    return paths


def markdown(frame,columns):
    """Dependency-free short table of exact saved numeric results."""
    rows=['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']
    for _,r in frame.iterrows():
        cells=[]
        for c in columns:
            v=r.get(c)
            if isinstance(v,(list,tuple,dict)):v=json.dumps(v)
            cells.append('—' if pd.isna(v) else f'{v:.6g}' if isinstance(v,(float,np.floating)) else str(v))
        rows.append('| '+' | '.join(cells)+' |')
    return '\n'.join(rows)


def write_reports(root,p,m,vm,shapes,paired,multi,stability):
    """Scientific verdict from the complete matched results; no winner-only filtering."""
    method=ROOT/'docs/experiment_B_stage2B_methods_and_model_registry.md'
    specs=pd.DataFrame(p['models']);cols=['model_id','features','edges','info']
    method.write_text(f'''# Experiment B Stage 2B methods and model registry

Protocol [v1](../config/B_stage2B_EBM_protocol_v1.json) froze before all pilot/full fits. Dataset {p['dataset_id']}, SHA256 {p['daily']['sha256']}. One daily table; all prior Stage2A forecasts referenced without copying their input histories. Original SIP/split source plus exactly39 D2.1c native missing-key repairs; source rights/adjustment qualifications unchanged.

{markdown(specs,cols)}

X is overnight-inclusive prior full close→10:00; Z=log(one-minute opening RV+1e−8); S is nominal text from original training terciles {p['cutoffs_raw']}, equality lower. W15:00–15:30 is available only to L15:30. Y is signed15:30–16:00 price return in bp. E10:00 never reads W. No financial target or feature changes; A is on hold.

Actual InterpretML core {p['environment']['interpret-core']} ExplainableBoostingRegressor, objective rmse; declared edges are runtime-index verified, no mining. Two settings: {p['settings']}. All defaults used are explicitly pinned in effective_base. Four bags for screening, eight final; primary seed42, confirmation seeds123/2025/7/314159. No clipping. Max1000rounds, early50, stochastic15% internal validation within available history only. Internal bagging shuffles past rows and is algorithmic; no bag interval is a scientific CI. Native greedy_ratio=0 uses cyclic boosting; native leaf dictionary/bag path is not the project's idealized learner.

Each family's candidate fits use2016–2020 targets and select minimum2021 MSE (ties first setting); settings chosen once before2022–23 evaluation, never reselect at future quarters. State coding retains original2016–2021 predictor-derived cuts even in training-era development; that internal screen is developmental rather than an honest live2021 forecast. Final fixed fits train1495days through2021. Quarterly Jan/Apr/Jul/Oct2022–23 histories use strictly completed targets, selected setting/seed frozen, original terciles unchanged. Jan2022 fixed fit is reused. All55 family/seed FULL models receive fixed and complete497date quarterly evaluation. No2024–2026 outcome read; date metadata/hash only.

All11 families seed42 receive DROP_TOP1 (2020-03-18), fixed Stage1.5 TOP5, EXCLUDE_2020, MATCHED_SOURCE (2019-08-12/13), one learning_rate=.05 sensitivity, and2016–19/2020/2021 fits. A1c E/L additionally leave each training year out. Native learner bins update on changed histories; frozen scientific cutoffs/coordinates remain fixed. These are learning-pipeline perturbations, not a literal fixed-linear-basis deletion. No variant replaces FULL based on better results.

Support screen: endpoints ±a, a10/20/30/50; local halfwidth5/10/15 with h<a; ordered candidates; late W0 then training median with halfwidth5/10/20. Minimum50dates/20 distinct disjoint5row blocks, strong100/30. Broad RV tercile neighborhoods are not pointwise Z support. E accepted ±20bp/h15; L no candidate, ABSTAIN. Exact cell counts/ranges/year mix in support registry. Sparse curves independently mask local cells below thresholds; continuous heatmap uses local Z±.2. No anchoredX0 contrast. Full D_F uses four total predictions at original low/high state medians. Additive D_F must be zero within1e−9. E model-output contrast remains EXPLORATORY/NOT_CERTIFIED; broad cell means estimate a different band functional. L model extrapolations may remain in audit tables labeled ABSTAIN but are not drawn as supported discoveries.

Paired loss comparator−candidate is positive for improvement. Bartlett HAC5 with n/(n−1), normal95%; lags10/20 sensitivity. Primary Holm family comprises quarterlyseed42 A1c_E−A0c_E and A1c_L−A0c_L comparisons only; other comparisons exploratory. Fixed-forecast circular block5/20 percentile bootstrap500 for four declared comparisons, not learner/post-selection bootstrap. Heavy tails, moments, weak-dependence and approximate stationarity matter. Scientific±1bp materiality never established by nonsignificance; predictive gain requires≥.0025 R² over stronger state-aware simple and interval excludingzero, also stronger naive comparison. State composition and within-state loss decomposition are descriptive, not covariate-shift correction.

Selected parameters/bins/terms: data/registry/B_stage2B_ebm_selected_parameters.json. All562 fits, including22screen/55FULL/385additionalquarter/44deletion/33subperiod/12leaveyear/11rate, registered; v1 total_planned662 was a conservative arithmetic typo, component counts unchanged and fully executed. Eleven primary seed42 native artifacts are ignored under artifacts/B/checkpoints/stage2B; no hundreds of serialized exploratory models. Single shared predictionParquet stores development/train/FULL/sensitivity/quarterly predictions, no sealed rows or input replicas.

Reproduce with authorized existing canonical data and matching Stage2A manifests: install requirements-stage2B.lock.txt, editable package, then python -B -m ebm_research.experiment_b.stage2b run (resume matching checkpoint) or publish (publication checkpoint). On a fresh authorized rebuild remove no existing user artifacts; use a fresh checkout, run freeze then pilot then run. Frozen protocol input hashes must match. EBM_DATA_ROOT may point to a portable shared store. No provider credentials/API needed for this offline stage. See session report for exact commands, recovery, errors and versions.

Native API consulted: [official regressor documentation](https://interpret.ml/docs/python/api/ExplainableBoostingRegressor.html); installed0.7.3 signature/source governs actual parameters. Original project theorem/task/consolidation files were absent from repository/ResearchSpec. Only explicit Bspec/AGENTS/current-prompt assumptions were applied; see theory audit for missing material.
''')
    full=vm.loc[vm.cohort.eq('validation')&vm.n.eq(497)&vm.variant.eq('FULL')&vm.seed.eq(42)&vm['mode'].isin(['fixed','quarterly'])]
    training=pd.read_csv(root/'registry/B_stage2B_ebm_training_metrics.csv')
    training=training.loc[training.seed.eq(42)&training.variant.eq('FULL')&training['mode'].eq('fixed')]
    diagnostics=pd.read_csv(root/'registry/B_stage2B_ebm_diagnostics.csv',low_memory=False)
    diagnostics=diagnostics.loc[diagnostics.seed.eq(42)&diagnostics.variant.eq('FULL')&diagnostics['mode'].eq('fixed')&diagnostics.cohort.eq('train')&diagnostics.statistic.isin(['Pearson_kurtosis','Jarque_Bera','ARCH_LM5','residual_LjungBox_5','squared_residual_LjungBox_5','Koenker_BP_small_XZ','White_small_XZ'])]
    decisions=pd.read_csv(root/'registry/B_stage2B_ebm_decisions.csv')
    primary_tests=multi.loc[multi.primary.eq(True)]
    contrasts=shapes.loc[shapes.seed.eq(42)&shapes.variant.eq('FULL')&shapes['mode'].eq('fixed')]
    qpaired=paired.loc[paired.method.eq('Bartlett_HAC5_normal')&paired['mode'].eq('quarterly')&paired.candidate.isin(['A1c_E','A1c_L','A1d_E','A1d_L','A2c_L'])]
    result=ROOT/'reports/B/stage2B_EBM_ladder_scientific_results.md'
    result.write_text(f'''# Experiment B Stage 2B — native EBM ladder, shape fidelity and inference

**PASS WITH QUALIFICATIONS — STAGE2B_MODEL_LADDER_COMPLETE.** All11 required native EBM families fitted, all562 planned component fits successful, with55 FULL family/seed fits and fixed plus identical497date quarterly validation. Training1495; validation497; sealed683unexamined. Negative/weak gains and unsupported contrasts are retained. E/L are different information sets and cannot be ranked as equal-information alternatives.

The interpretation is governed by matched additive, simple state-aware and naive comparators below. A lowest RMSE alone is not credible incremental EBM superiority. Validation is developmental/reused, not independent final confirmation. **E scientific raw shape: INCONCLUSIVE**, because adequate broad local-X×tercile cells do not certify continuous-point conditional means or fitted-model coverage. **L scientific shape: ABSTAIN**, because no declared joint X/RV/W candidate passes. No ±1bp environmental equivalence certification; no bagSD population intervals.

{markdown(decisions,['info','primary_model','incremental_prediction','strongest_state_aware','simple_gain','simple_ci_low','simple_ci_high','strongest_naive_OLS','reference_gain','reference_ci_low','reference_ci_high','shape_status'])}

## Data, selection and fitting

Frozen source/daily identity{p['daily']['sha256']}; source D2 SIPsplit plus exactly39 D2.1c native repairs, original shares/return/time fields unchanged. Match-source excludes2019Aug12/13 only; no new recovery. March18,2020 five prices independently verified at Stage2A; midday gap outside scientific windows does not justify deletion. Ordinary OLS Cook/leverage/DFBETA/adjustedR² are NOT_APPLICABLE to native EBMs; exact fixed-date/group refit influence used instead.

Two settings per family, training2016–2020→2021 developmental selection, selected once; five seeds and eight bags final. All features untrimmed, signedY unchanged. Screen/bagging/preprocessing caveats, exact formulas and graph in [methods registry](../../docs/experiment_B_stage2B_methods_and_model_registry.md). Original tercile cutoffs fixed for all validation, quarterly native bins use only past history. No indicators, new data, A, A3–A6, trading or sealed science.

## Train and validation evidence

Training metrics for every fit in training_metrics.csv, including in-sample mean-baselineR² and explicitly NOT_APPLICABLE OLS-adjustedR² in diagnostics. FULL training seed42:

{markdown(training,['model_id','n','RMSE','MAE','in_sample_R2','forecast_SD','forecast_min','forecast_max'])}

Full validation seed42:

{markdown(full,['model_id','mode','n','RMSE','MAE','MSE','bias','R2_N0','R2_causal_N1','Pearson','Spearman'])}

Stage2A benchmarks on identical497dates: N0RMSE30.306832bp, N130.313865; quarterlyC1_E30.329061/C1_L30.362602, C2_E30.432765/C2_L30.468995 and S4_E31.427071/S4_L31.486693. Actual baseline prediction hashes/keys/outcomes verified before each paired comparison; no rerun of unchanged simple fits.

Primary continuous-interaction family (positive gain improves; bp²):

{markdown(primary_tests,['candidate','comparator','mean_loss_gain','ci_low','ci_high','p_value','p_holm','R2_gain_vs_N0_denominator','materiality_met'])}

These are asymptotic development comparisons conditional on saved forecasts, not exact scientific shape tests or independent selected-model confirmation. Six hundred sixty-two in frozen v1 total field was an arithmetic typo: all seven component counts sum562, which is the actual complete plan. No candidate grid/seed/sensitivity was omitted.

Matched quarterly primary/secondary paired HAC5 comparisons (all alternatives and lag/block sensitivity in registry):

{markdown(qpaired,['candidate','comparator','mean_loss_gain','ci_low','ci_high','p_value','R2_gain_vs_N0_denominator','materiality_met'])}

## Supported total-response contrasts and empirical fidelity

Predictor-only screen chose E−20→+20bp with local±15bp neighborhoods in broad frozen low/high RVterciles; exactn, five-rowblocks, X/Zranges and yearconcentrations saved. Lallcandidates fail, no outcome-based enlargement. D_F uses four full native predictions at original within-tercile medianZ and fixedW; additive zero invariant tested. Audit-only late numerical values are unsupported and do not constitute a claim.

{markdown(contrasts,['model_id','info','x_minus','x_plus','D_F','increment_low','increment_high','support_status','scientific_status','interval_status'])}

Broad raw cell means and same-distribution model averages are in empirical_bands/cells.csv. They do not estimate the same continuous pointwise functional as D_F. Training E band intervals use500 circular block5/20 resamples under stationarity/dependence/moment assumptions; validation low-state occupancy makes independent local-band confirmation unsupported. No selected scientific population p-value or certified confidence band is supplied. ±1bp equivalence is INCONCLUSIVE, not implied by nonsignificance. Shape resampling of the entire tuning/learning pipeline was not run; all5seed and fixed-time-window refits give descriptive instability only.

## Diagnostics, sensitivity and composition

Every fit has training/evaluation residual statistics, tail quantiles, skew/kurtosis, Jarque–Bera, ACF and residual/squaredLjungBox5/10/20, ARCH5, small nonsingular X/Z variance auxiliary tests, residualbins and scale summaries. Classical reference p-values are heuristic under fitted nonlinear residuals/time dependence and do not establish/deny consistency. No giant EBM design enters an OLS variance or RESET test. Residual mean/variance vsX/W/Z/time and representative QQ show full tails; extreme/crisisdates retained. Score ranges, bags/iterations, sparse native bins, feature importance and graph metadata appear for every fit. Validation state/year/quarter/fixed|X|bands and prediction-quantile calibration retain small/degenerate support statuses.

Selected numerical FULL-training diagnostics (references heuristic as above, not scientific EBM p-values):

{markdown(diagnostics,['model_id','statistic','estimate','p_value','status'])}

All11 families receive fixedtop1/top5/2020/matched and rate sensitivities; every comparison retains497validationdates. Native bins refit on changed training histories, so deletion changes the learner as well as fittedscores; scientific categories/coordinates fixed. All11 subperiod fits2016–19/2020/2021 plus A1cE/Lleaveyear-out saved. Some short-window fixed-coordinate model predictions extrapolate; registry masks prevent raw scientific claims. Seed stability is algorithmic, not sampling uncertainty.

Frozen state composition shifts from near thirds in train to31/151/315 validation. Within-state errors and exact loss decomposition distinguish observed mixture changes from within-state error differences; latter includes trainingoptimism and conditionaldistributiondrift and is not a causal transport theorem. Continuous-to-discrete diagnostics report same-RV within-tercile Zspread, predictiondispersion and discontinuities, no known-moment finitebasis inverse guarantee.

## Figures

'''+ '\n'.join(f'![{f["path"].split("/")[-1]}](../../{f["path"]})' for f in m['figures'])+'''

## Handoff and remaining stages

All11 model families, matched saved predictions, exact terms/bins, supported/non-supported total-surface queries, complete negative/sensitivity evidence and [theory applicability audit](stage2B_theory_applicability_and_implementation.md) are reviewable. No scientific novelty or positive alpha follows from implementation alone. Review exact losses/CIs and support before any selection. Later Stage4 requires separately frozen shortlisted full-pipeline null/permutation and sealed walk-forward protocol; Stage5 requires execution/cost economics. Stage2B completes neither and leaves2024–2026 sealed. Optional100nullreplicates deferred with a concrete future plan in theory report, no counterfeitp-value.
''')
    theory=ROOT/'reports/B/stage2B_theory_applicability_and_implementation.md'
    theory.write_text('''# Experiment B Stage 2B — theory applicability and actual implementation

**NOVEL_METHODS_APPLIED_WITH_ASSUMPTIONS.** This is a methodological application/audit of support-aware scientific targets and fidelity, not a claim of accepted novel inference or a proof for native InterpretML. Original task/consolidation/theory statements were absent from `rg --files` inventory of the repository and ResearchSpec. Consulted: Bspecv1 §§2,6.3,7,8, companion §§1,3, rootAGENTS, Stage2A methods and current Stage2B prompt. Task numbers below come from the prompt; original mathematical statements were not available. Missing materials needed for exact audit: consolidation_assumptions_and_issues_v1.md; consolidation_theorem_crosswalk_v1.md; original Tasks10B/11/12/15/16–25 (especially18–20/22–25); exact finite-dictionary/observation-law/learner assumptions and theorem versions. Do not claim those papers were read.

'''+markdown(pd.read_csv(root/'registry/B_stage2B_ebm_theory_method_ledger.csv'),['method','reference','classification','computation','permitted_claim'])+'''

The machine ledger adds target, required assumptions, SPY evidence and explicit theorem access status. DIRECTLY_VALID for HAC means a standard asymptotic procedure **on stated weak-dependence/moment/bandwidth and fixed-forecast assumptions**, not a verified finite-sample financial theorem. Heavy tails and volatility dependence make finite fourth/higher moments and stationarity doubtful/untestable from this short panel; lag and circular-block sensitivities expose rather than solve that fragility. Forecasts fitted on evolving histories share estimation uncertainty; fixed-loss inference conditions on saved forecasts and is developmental, not general post-selection coverage.

Implemented, with actual computation: query-specific local support/bock counts and masks E/L; first-qualifying nonzero two-endpoint grid; four entire-model prediction contrasts, additive-zero invariant and savedC1/C2/S4 comparator contrasts; empirical band means versus model means on identical rows and circular block intervals when support permits; fixed-environment refits/state-mixture error decomposition; same underlying RV resolution and within-tercile finite-panel dispersion; complete candidate/seed/refit path; native graph/bins/bag/iteration and empirical stability audit; paired loss HAC5/10/20 plus block5/20 bootstrap500. Rows/figures link to exact computations. These instantiate diagnostics inspired by theory, without asserting all population assumptions.

Not instantiated: exact affine finite-basis inverse/retaining spaces of Tasks24/25 (unknown moment law and no literal dictionary); Gaussian/polyhedral/spherical exact selective pivots (native stochastic boosting and heavy-tailed dependent panel); optimization gap/persistence certificate for idealized learners (native bagged cyclic trees, fixed bins/smoothing/early stopping differ); certified scientific pointwise D_m confidence bands or ±1bp invariance. InterpretML component/bagSD displays do not supply these. D_F uses whole surfaces; raw band contrast and pointwiseD_m are different functionals. Even Epassing broad-cell counts does not prove a regular continuous conditional mean at medianZ, eliminate bias or certify its interval. Late support fails and remainsABSTAIN.

Future bounded null plan, DEFERRED_TO_STAGE4: after scientific review freeze one A1c family and its matched A0c/null/simple references; use fixed circular shifts of the full chronological Yseries by ≥20eligible rows or a prespecified20rowblock destroyed-alignment null, retaining predictorjoint distribution. For each of100replicates rerun both settings on2016–2020→2021, select per frozenrule, refitpast-only quarterly, calculate same selected paired and shape statistics. Whole result includes seed/shift/calendar assumptions, failures and (1+exceedances)/(B+1); no exact exchangeability under arbitrary SPYdependence. This is not the incremental conditional interactionnull and RVshuffling is forbidden as a substitute. A full two-family comparison retaining the actual five-seed confirmation path needs (2screen+5seeds×8quarterfits)×2families×100=8400 native fits before optional diagnostics. The measured conservative4×overhead projection is about10,575seconds, above the frozen3600second cap. A cheaper seed42-only conditional null would omit the five-seed discovery/stability path and needs a separately frozen scope and interpretation. No nullp-value is manufactured. A subsequent final-test protocol must be frozen separately before any2024–2026 labels are used. No tradingP&L/cost claim here.

CV-ready technical accomplishment: implemented and audited a reproducible native11family additive/discrete/continuous-state EBM ladder with exact information-time and interaction-graph guards; training-only complexity selection;5seed chronological matchedvalidation; support-masked whole-response contrasts, fitted-versus-band-empirical fidelity diagnostics, dependence-sensitive pairedloss intervals, and a machine-readable theorem-assumption applicability register. This is a concrete research-engineering/methodology result even if no predictiveincrement or scientific shape is established; it is distinct from unverified novel inferential validity or alpha.
''')
    return [method,result,theory]
