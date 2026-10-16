"""Compact Stage2B publication, matched loss inference and scientific method audit."""
import json
import gzip
from pathlib import Path
import time
import platform
try:
    import resource
except ImportError:  # Windows: optional process high-water diagnostic unavailable.
    resource=None

import joblib
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from .pilot import ROOT,sha,write_json
from .acquisition import file_ref
from .ebm_models import (STATES,groups,features,query_frame,metrics,residual_diagnostics,
                         paired_losses,paired_hac,block_interval,cell_mask,candidate_rows)


def export_csv(root,name,rows):
    """Small trackable numeric registry; nested native metadata encoded as JSON."""
    f=pd.DataFrame(rows)
    for col in f:
        if f[col].map(lambda v:isinstance(v,(dict,list,tuple))).any():
            f[col]=f[col].map(lambda v:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list,tuple)) else v)
    path=root/f'registry/B_stage2B_ebm_{name}.csv';f.to_csv(path,index=False)
    return path


def make_predictions(state,train,val):
    """Exactly one long prediction table; quarter-one reuses the identical fixed fit."""
    source=pd.concat([train,val],ignore_index=True).assign(session_et=lambda f:f.session_et.astype(str)).set_index('session_et')
    parts=[]
    for rec in state['runs'].values():
        m=rec['meta'];keys={k:m[k] for k in ['fit_id','model_id','family','info','seed','setting','variant','mode']}
        dates=rec['eval_dates'];part=pd.DataFrame(dict(session_et=dates,forecast=rec['predictions']))
        part['actual']=source.loc[dates,'y_last30_bp'].to_numpy()
        part['state']=np.asarray(STATES)[source.loc[dates,'rv_group_stage2b'].to_numpy(dtype=int)]
        part=part.assign(**keys,cohort='development' if m['mode']=='screen' else 'validation',asof=m['asof'],history_last=m['last'])
        if m['mode']=='quarterly':part['mode']='quarterly'
        parts.append(part)
        if m['mode']=='fixed' and m['variant']=='FULL':
            first=part.loc[part.session_et.lt('2022-04-01')].copy();first['mode']='quarterly';parts.append(first)
            # Training predictions retained for all 55 selected family/seed FULL fits, no inputs cloned.
            t=pd.DataFrame(dict(session_et=rec['train_dates'],forecast=rec['train_predictions']))
            t['actual']=source.loc[rec['train_dates'],'y_last30_bp'].to_numpy()
            t['state']=np.asarray(STATES)[source.loc[rec['train_dates'],'rv_group_stage2b'].to_numpy(dtype=int)]
            parts.append(t.assign(**keys,cohort='train',asof=m['asof'],history_last=m['last']))
    out=pd.concat(parts,ignore_index=True);out['loss']=(out.forecast-out.actual)**2
    key=['model_id','setting','seed','variant','mode','cohort','session_et']
    if out.duplicated(key).any():raise ValueError('Duplicate prediction key in Stage2B publication')
    if out.session_et.ge('2024-01-01').any():raise ValueError('Sealed prediction/output row')
    return out


def paired_comparisons(root,p,pred,val):
    """Matched E/L comparators by reference; developmental HAC and compact block sensitivity."""
    baseline=pd.read_parquet(root/p['stage2A_predictions']['path'])
    baseline.session_et=baseline.session_et.astype(str)
    rows=[];multiplicity=[]
    for mode in ['fixed','quarterly']:
        for s in p['models']:
            candidate=pred.loc[pred.model_id.eq(s['model_id'])&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq(mode)&pred.cohort.eq('validation')]
            if len(candidate)!=497:raise ValueError(f'Incomplete comparable validation {s["model_id"]}/{mode}')
            info=s['info'];family=s['family']
            comparators=['N0','N1','OLS1_E' if info=='E' else 'OLS3_L',f'C1_{info}',f'C2_{info}',f'S4_{info}',f'S6_{info}']
            if family!='SB':comparators += [f'SB_{info}']
            if family=='A1c':comparators += [f'A0c_{info}',f'A1d_{info}']
            if family=='A1d':comparators += [f'A0d_{info}',f'A1c_{info}']
            if family=='A2c':comparators += ['A1c_L','C1_L_Wmod','C2_L_Wmod']
            if info=='L':comparators+=['OLS2_L']
            for comp in dict.fromkeys(comparators):
                b=pred.loc[pred.model_id.eq(comp)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq(mode)&pred.cohort.eq('validation')]
                if b.empty:
                    b=baseline.loc[baseline.model_id.eq(comp)&baseline.variant.eq('FULL')&baseline['mode'].eq(mode)]
                    b=b.rename(columns={'prediction':'forecast','y':'actual'})
                d=paired_losses(candidate,b)
                n0=float(np.mean(val.y_last30_bp.to_numpy()**2))
                for lag in p['paired_inference']['lags']:
                    r=dict(candidate=s['model_id'],comparator=comp,info=info,mode=mode,seed=42,variant='FULL',n=497,
                           method=f'Bartlett_HAC{lag}_normal',lag=lag,**paired_hac(d,lag),
                           status='DEVELOPMENTAL_ASYMPTOTIC',assumptions='Fixed forecasts; weak dependence, finite loss moments, bandwidth adequacy; reused development labels, not independent confirmation')
                    r['R2_gain_vs_N0_denominator']=r['mean_loss_gain']/n0
                    r['materiality_met']=r['mean_loss_gain']/n0>=p['materiality']['incremental_R2'] and r['ci_low']>0
                    rows.append(r)
                    if lag==5:
                        primary=mode=='quarterly' and [s['model_id'],comp] in p['primary_comparisons']
                        multiplicity.append(dict(r,hypothesis_family='PRIMARY_E_L_CONTINUOUS_INTERACTION' if primary else 'EXPLORATORY',primary=primary))
                if mode=='quarterly' and [s['model_id'],comp] in p['paired_inference']['bootstrap_subset']:
                    for block in [5,20]:
                        rows.append(dict(candidate=s['model_id'],comparator=comp,info=info,mode=mode,seed=42,n=497,
                                         mean_loss_gain=float(d.mean()),status='DESCRIPTIVE_BLOCK_SENSITIVITY',
                                         **block_interval(d,block,500,42)))
    selected=[i for i,r in enumerate(multiplicity) if r['primary']]
    q=multipletests([multiplicity[i]['p_value'] for i in selected],method='holm')[1]
    for i,v in zip(selected,q):multiplicity[i]['p_holm']=float(v)
    return rows,multiplicity


def empirical_bands(train,val,p,pred):
    """Predetermined broad-cell estimand, dependence-conscious diagnostic; never raw point inference."""
    rows=[];cells=[]
    for info in ['E','L']:
        g=p['contrast_grid'][info];c=g['display_candidate']
        for cohort,f in [('train',train),('validation',val)]:
            cr=candidate_rows(f,p,c,cohort)
            masks=[cell_mask(f,p,c,s,x) for s in [0,2] for x in [-c['a'],c['a']]]
            for r,m in zip(cr,masks):
                sub=f.loc[m];r.update(selected_candidate=g['chosen'] is not None,
                                     X_mean=float(sub.x_open_bp.mean()) if len(sub) else None,
                                     W_mean=float(sub.w_preclose_bp.mean()) if len(sub) else None,
                                     Z_mean=float(sub.rv_open_log.mean()) if len(sub) else None,
                                     Y_mean=float(sub.y_last30_bp.mean()) if len(sub) else None,
                                     Y_SD=float(sub.y_last30_bp.std()) if len(sub)>1 else None,
                                     interpretation='broad RV-tercile local-X band, not a continuous pointwise conditional mean')
                cells.append(r)
            supported=g['chosen'] is not None and all(r['supported'] for r in cr)
            y=f.y_last30_bp.to_numpy();means=[float(y[m].mean()) if m.any() else None for m in masks]
            d=means[3]-means[2]-means[1]+means[0] if supported else None
            rows.append(dict(info=info,cohort=cohort,estimand='empirical_local_X_by_RV_tercile_band_mean_D',
                             estimate=d,status='EXPLORATORY' if supported else 'ABSTAIN',
                             interval_status='DEPENDENCE_SENSITIVE_BAND_ONLY' if supported else 'UNSUPPORTED',
                             reason='Broad band distributions differ; no pointwise equality claim; validation used for development comparisons'))
            if supported:
                n=len(f);rng=np.random.default_rng(42)
                for block in [5,20]:
                    draws=[]
                    for b in range(500):
                        starts=rng.integers(n,size=int(np.ceil(n/block)))
                        idx=((starts[:,None]+np.arange(block))%n).ravel()[:n]
                        mm=[m[idx] for m in masks]
                        if all(t.any() for t in mm):
                            v=[y[idx][t].mean() for t in mm];draws.append(v[3]-v[2]-v[1]+v[0])
                    enough=len(draws)>=450
                    rows.append(dict(info=info,cohort=cohort,estimand='empirical_band_D_block_interval',
                                     estimate=d,ci_low=float(np.quantile(draws,.025)) if enough else None,
                                     ci_high=float(np.quantile(draws,.975)) if enough else None,
                                     block=block,B=len(draws),status='EXPLORATORY' if enough else 'ABSTAIN',
                                     assumptions='Circular block resampling of complete eligible daily rows; stationarity/mixing/moments and coarse-band bias required; training estimate not held out'))
            # Model-predicted band averages on EXACTLY the same observed row distributions.
            for model in ['SB','A0c','A0d','A1d','A1c']+(['A2c'] if info=='L' else []):
                mid=f'{model}_{info}';q=pred.loc[pred.model_id.eq(mid)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq('fixed')&pred.cohort.eq(cohort)]
                if q.empty:continue
                vv=q.set_index('session_et').loc[f.session_et.astype(str),'forecast'].to_numpy()
                v=[float(vv[m].mean()) if m.any() else None for m in masks]
                rows.append(dict(info=info,cohort=cohort,model_id=mid,estimand='model_predicted_identical_band_distribution_D',
                                 estimate=v[3]-v[2]-v[1]+v[0] if supported else None,
                                 status='EXPLORATORY_FIDELITY' if supported else 'ABSTAIN',
                                 reason='Same row distributions as empirical band mean; differs from pointwise four-prediction D_F'))
    return rows,cells


def theory_ledger():
    """Explicitly audit source availability and assumptions, applying feasible diagnostics."""
    return [dict(method=m,reference=ref,target=target,required_assumptions=assumptions,evidence=evidence,
                 classification=status,computation=artifact,permitted_claim=claim,
                 original_theorem_access='NOT_AVAILABLE: task numbers supplied in current prompt, not consulted original statements')
            for m,ref,target,assumptions,evidence,status,artifact,claim in [
        ('query_specific_support','Tasks10B/11/23; Bspec§7','local X×RV×W cells','Joint overlap and adequate time-separated observations; continuity needed for points',
         'Exact ordered predictor-only local-cell and fixed-block screen; E broad-band design passes, L fails','ADAPTED_DESCRIPTIVE','support.csv; contrast_grid.json; figure01','Finite-sample support/ABSTAIN, not a population identification theorem'),
        ('whole_response_contrast','Tasks11/15/22; Bspec§2,7','four-total-prediction D_F','Fixed coordinates, correct full response and partner; population fidelity separately justified',
         'Full native predictions and additive zero invariant checked; no pointwise scientific coverage','ADAPTED_DESCRIPTIVE','shape_contrasts.csv; surfaces.csv; figure04','Model-output nonadditivity, not proven D_m'),
        ('state_composition_stability','Tasks18/19/23; Bspec§7','fixed-state/window conditional summaries','Common support, fixed environments, equivalent conditional law for invariance',
         'Original cutoffs fixed; time-window/leave-year refits, state counts and composition decomposition','ADAPTED_DESCRIPTIVE','stability.csv; state_composition.csv; figure11','Distinguish mixture change from within-state observed drift, no equivalence certification'),
        ('scientific_fidelity','Tasks16/20/22/23; Bspec§7','same-band empirical vs predicted D','Independent supported raw response estimates and bias/dependence control',
         'Training E broad bands descriptive; validation lacks common local-cell support, late fails','BLOCKED_ASSUMPTIONS','empirical_bands.csv; empirical_cells.csv; figure11','No independent raw pointwise shape confirmation'),
        ('three_state_information_loss','Tasks24/25; BspecH4','within-tercile Z and model-prediction dispersion','Known moment law/finite dictionary required for exact affine inverse',
         'Empirical Z/prediction spreads available; exact dictionary, moments, observation law absent','ADAPTED_DESCRIPTIVE','discretization.csv; figure05','Finite-panel information compression diagnostics only'),
        ('exact_affine_inverse','Tasks24/25 (original absent)','exact retained/inverse spaces','Literal finite dictionary and known moments under specified observation law',
         'Not instantiated by native InterpretML terciles','NOT_APPLICABLE','theory report','No exact inverse-space theorem applied'),
        ('selection_adjusted_exact_pivot','Tasks12/15/22; Bspec§8','selected fitted shape','Specified Gaussian/polyhedral/spherical selection event and known conditioning law',
         'Heavy tails, temporal dependence, native stochastic boosting and training development selection','NOT_APPLICABLE','complete models.csv; interaction_and_multiplicity.csv','No exact selected-shape p-value'),
        ('native_greedy_learner','Tasks16–18/22; Bspec§6.3','native fitting path and stability','Literal theorem tree dictionary, optimization gap and specified path',
         'Actual terms, bins, iterations, bags and seeds registered; different software learner','ADAPTED_DESCRIPTIVE','models.csv; term_importance.csv; seed comparison','Software graph and empirical stability only; no optimizer certificate'),
        ('paired_loss_HAC','Tasks6/19/21/22; Bspec§8','mean paired squared-loss gain','Weak dependence, sufficient loss moments, bandwidth adequate; forecasts treated fixed',
         'Heavy-tailed/dependent residuals, lags5/10/20 and blocks5/20; no theorem verifies mixing','DIRECTLY_VALID','paired_loss_tests.csv','Asymptotic on stated assumptions; developmental conditional comparison, not exact guarantee'),
        ('raw_shape_or_bag_CI','Tasks11/19/22; Bspec§7','pointwise scientific D_m','Joint support, justified estimator bias and dependence theory, selection coverage',
         'Native bag spread only algorithmic, no certified raw estimator or whole-pipeline bootstrap','BLOCKED_ASSUMPTIONS','shape_contrasts interval_status=NOT_CERTIFIED','ABSTAIN/INCONCLUSIVE, never bagSD-as-population-CI'),
        ('full_pipeline_null','Bspec§8.2; Stage2B scope','selected discovery destroyed-alignment null','Rerun tuning/refits; block/circular null invariance not automatic',
         'Core662 fit budget;100×full shortlisted selection/refit exceeds allocated hour','BLOCKED_ASSUMPTIONS','manifest DEFERRED_TO_STAGE4; theory report future command plan','No permutation p-value claimed')]]


def publish(root,p,state,primary,train,val,n1train,n1val):
    """Publish complete fitting inventory and all matched comparisons without new EBM fits."""
    started=time.perf_counter()
    for f in [train,val]:f['rv_group_stage2b']=groups(f,p)
    runs=list(state['runs'].values())
    # V1's total_planned is a conservative arithmetic typo (662); its seven
    # frozen component counts sum to 562. No scientific fit branch is removed.
    expected=sum(p['resource'][k] for k in ['screened','selected_full','additional_quarterly','sensitivities','temporal','leave_year_out','learning_rate'])
    if len(runs)!=expected or any(r['meta']['status']!='PASS' for r in runs):
        raise ValueError(f'Incomplete Stage2B ladder: {len(runs)} fits')
    pred=make_predictions(state,train,val)
    trainmetrics=[r['training_metric'] for r in runs]
    valmetrics=[dict(r['validation_metric'],cohort='validation_quarter' if r['meta']['mode']=='quarterly' else r['validation_metric']['cohort']) for r in runs]
    diagnostics=[d for r in runs for d in r['diagnostics']]
    surfaces=[v for r in runs for v in r['surfaces']];importance=[v for r in runs for v in r['importance']]
    shapes=[r['shape'] for r in runs]
    finite=[]
    surface_frame=pd.DataFrame(surfaces)
    for (fid,state_name),q in surface_frame.groupby(['fit_id','state']):
        q=q.sort_values('x')
        for j in range(1,len(q)):
            a,b=q.iloc[j-1],q.iloc[j];ok=bool(a.supported and b.supported)
            finite.append(dict(fit_id=fid,model_id=b.model_id,info=b['info'],state=state_name,
                               x_minus=a.x,x_plus=b.x,increment_bp=b.forecast-a.forecast,
                               finite_increment_per_bp=(b.forecast-a.forecast)/(b.x-a.x),
                               supported=ok,status='DESCRIPTIVE_FITTED' if ok else 'ABSTAIN',
                               note='Finite total-prediction difference of a stepwise learner; not a population partial derivative'))
    for (mid,seed),q in pred.loc[pred['mode'].eq('quarterly')&pred.cohort.eq('validation')].groupby(['model_id','seed']):
        q=q.sort_values('session_et')
        if len(q)!=497 or not np.array_equal(q.session_et.to_numpy(),val.session_et.astype(str).to_numpy()):
            raise ValueError(f'Quarterly date mismatch {mid}/{seed}')
        if not (q.history_last<q['asof']).all() or not (q.history_last<q.session_et).all():raise ValueError('Quarterly chronology failed')
        s=next(s for s in p['models'] if s['model_id']==mid)
        keys=dict(model_id=mid,family=s['family'],info=s['info'],seed=int(seed),setting=state['selected'][mid],variant='FULL',mode='quarterly')
        valmetrics.append(metrics(val,q.forecast.to_numpy(),n1val,**keys,cohort='validation'))
        diagnostics+=residual_diagnostics(val,q.forecast.to_numpy(),p,**keys,cohort='validation')
    # State/year/quarter/magnitude/calibration diagnostics for every saved validation series.
    for key,q in pred.loc[pred.cohort.eq('validation')].groupby(['model_id','seed','variant','mode']):
        q=q.sort_values('session_et');mid,seed,variant,mode=key
        if len(q)!=497:raise ValueError(f'Sensitivity changed validation dates: {key}')
        f=val.set_index(val.session_et.astype(str)).loc[q.session_et]
        subdivisions=[('state',f.rv_group_stage2b.to_numpy()),('year',q.session_et.str[:4].to_numpy()),
                      ('quarter',pd.to_datetime(q.session_et).dt.to_period('Q').astype(str).to_numpy()),
                      ('abs_X_training_fixed',np.digitize(abs(f.x_open_bp.to_numpy()),[10,30,100]))]
        n1map=pd.Series(n1val,index=val.session_et.astype(str))
        for dimension,labels in subdivisions:
            for label in np.unique(labels):
                mask=labels==label;sub=f.loc[mask]
                valmetrics.append(metrics(sub,q.forecast.to_numpy()[mask],n1map.loc[sub.session_et.astype(str)].to_numpy(),
                                          model_id=mid,seed=int(seed),variant=variant,mode=mode,cohort='validation_subgroup',dimension=dimension,group=str(label)))
        bins=pd.qcut(q.forecast,10,duplicates='drop')
        for j,(_,part) in enumerate(q.assign(bin=bins).groupby('bin',observed=True)):
            diagnostics.append(dict(model_id=mid,seed=int(seed),variant=variant,mode=mode,cohort='validation',
                                    statistic='prediction_quantile_calibration',bin=j,n=len(part),
                                    forecast_mean=part.forecast.mean(),actual_mean=part.actual.mean(),
                                    estimate=(part.actual-part.forecast).mean(),status='DESCRIPTIVE' if len(part)>=20 else 'ABSTAIN'))
    for row in diagnostics:
        name=row['statistic']
        if name.startswith('Jarque'):null='Gaussian residual skewness=0 and Pearson kurtosis=3'
        elif 'LjungBox' in name:null='No serial correlation through named eligible-day lag'
        elif name=='ARCH_LM5':null='No ARCH through 5 eligible observations'
        elif name.startswith(('Koenker','White')):null='Constant residual variance against small declared X/Z auxiliary functions'
        else:null='Descriptive, no formal null'
        row['null']=null
        row['uncertainty']='Test-specific asymptotic/IID reference only; not calibrated scientific EBM inference' if row.get('p_value') is not None else 'Descriptive / NOT_CERTIFIED; no sampling CI'
    paired,multiplicity=paired_comparisons(root,p,pred,val)
    decisions=[]
    for info in ['E','L']:
        mid='A1c_'+info
        q=[r for r in paired if r['candidate']==mid and r['mode']=='quarterly' and r.get('method')=='Bartlett_HAC5_normal']
        additive=next(r for r in q if r['comparator']=='A0c_'+info)
        simple=min((r for r in q if r['comparator'] in ['C1_'+info,'C2_'+info,'S4_'+info]),key=lambda r:r['mean_loss_gain'])
        naive=min((r for r in q if r['comparator'] in ['N0','N1','OLS1_E','OLS3_L','OLS2_L']),key=lambda r:r['mean_loss_gain'])
        adjusted=next(r['p_holm'] for r in multiplicity if r['primary'] and r['candidate']==mid)
        convincing=adjusted<.05 and additive['ci_low']>0 and simple['materiality_met'] and naive['ci_low']>0
        decisions.append(dict(info=info,primary_model=mid,incremental_prediction='CREDIBLE_DEVELOPMENTAL_INCREMENT' if convincing else 'NO_CREDIBLE_INCREMENT',
                              strongest_state_aware=simple['comparator'],simple_gain=simple['mean_loss_gain'],simple_ci_low=simple['ci_low'],simple_ci_high=simple['ci_high'],
                              strongest_naive_OLS=naive['comparator'],reference_gain=naive['mean_loss_gain'],reference_ci_low=naive['ci_low'],reference_ci_high=naive['ci_high'],
                              additive_gain=additive['mean_loss_gain'],primary_p_holm=adjusted,
                              shape_status='INCONCLUSIVE_NOT_CERTIFIED_POINTWISE' if p['contrast_grid'][info]['chosen'] else 'ABSTAIN',
                              interpretation='Developmental reused validation; no independent final confirmation; fixed-reference selection disclosed'))
    band,empirical_cells=empirical_bands(train,val,p,pred)
    stability=[]
    for rec in runs:
        m=rec['meta'];v=rec['validation_metric'];c=rec['shape']
        if m['mode']=='screen' or m['mode']=='quarterly':continue
        base=next(r for r in runs if r['meta']['model_id']==m['model_id'] and r['meta']['seed']==42 and r['meta']['variant']=='FULL' and r['meta']['mode']=='fixed')
        a=np.asarray(rec['predictions']);b=np.asarray(base['predictions'])
        stability.append(dict(model_id=m['model_id'],info=m['info'],variant=m['variant'],mode=m['mode'],seed=m['seed'],n=m['n'],
                              validation_RMSE=v['RMSE'],delta_MSE_vs_FULL42=v['MSE']-base['validation_metric']['MSE'],
                              forecast_RMS_difference=float(np.sqrt(np.mean((a-b)**2))),max_abs_forecast_difference=float(np.max(abs(a-b))),
                              D_F=c['D_F'],delta_D_F=c['D_F']-base['shape']['D_F'],support_status=c['support_status'],
                              uncertainty='Descriptive seed/subperiod/deletion sensitivity, not sampling CI or equivalence',
                              interval_status='NOT_CERTIFIED',materiality_bp=p['materiality']['shape_bp']))
    comp=[];discrete=[]
    for cohort,f in [('train',train),('validation',val)]:
        for j,name in enumerate(STATES):
            sub=f.loc[f.rv_group_stage2b.eq(j)]
            comp.append(dict(cohort=cohort,state=name,n=len(sub),fraction=len(sub)/len(f),Z_mean=sub.rv_open_log.mean(),Y_mean=sub.y_last30_bp.mean(),Y_SD=sub.y_last30_bp.std(),
                             note='Observed composition/response summary, not causal adjustment or invariant conditional law'))
            for info in ['E','L']:
                cp=primary['A1c_'+info].predict(features(sub,next(s for s in p['models'] if s['model_id']=='A1c_'+info),p))
                dp=primary['A1d_'+info].predict(features(sub,next(s for s in p['models'] if s['model_id']=='A1d_'+info),p))
                discrete.append(dict(cohort=cohort,info=info,state=name,n=len(sub),Z_SD=sub.rv_open_log.std(),Z_min=sub.rv_open_log.min(),Z_max=sub.rv_open_log.max(),
                                     continuous_prediction_SD=float(cp.std()),discrete_prediction_SD=float(dp.std()),prediction_difference_RMS=float(np.sqrt(np.mean((cp-dp)**2))),
                                     note='Same observed X/W distribution; prediction dispersion also includes X/W, not isolated Z causal information'))
    # Decompose observed MSE difference: mixture term + within-state term, exact algebra, descriptive.
    for info in ['E','L']:
        mid='A1c_'+info
        a=pred.loc[pred.model_id.eq(mid)&pred.seed.eq(42)&pred.variant.eq('FULL')&pred['mode'].eq('fixed')]
        pt=np.array([(train.rv_group_stage2b==j).mean() for j in range(3)])
        pv=np.array([(val.rv_group_stage2b==j).mean() for j in range(3)])
        lt=np.array([a.loc[a.cohort.eq('train')&a.state.eq(s),'loss'].mean() for s in STATES])
        lv=np.array([a.loc[a.cohort.eq('validation')&a.state.eq(s),'loss'].mean() for s in STATES])
        comp.append(dict(cohort='train_to_validation_MSE_decomposition',state='all',model_id=mid,
                         composition_term=float((pv-pt)@lt),within_state_term=float(pv@(lv-lt)),total=float(pv@lv-pt@lt),
                         note='Exact descriptive decomposition; training optimism and conditional drift confounded, not density-ratio correction'))
    # Dense supported continuous slices at actual native bins and empirical mask counts.
    heat=[];components=[]
    for info in ['E','L']:
        s=next(s for s in p['models'] if s['model_id']=='A1c_'+info);model=primary[s['model_id']]
        w=p['contrast_grid'][info]['display_candidate']['w']
        for z in np.quantile(train.rv_open_log,p['sparse_plot']['z_quantiles']):
            xs=np.asarray(p['sparse_plot']['x']);q=query_frame(xs,z,w);fp=model.predict(features(q,s,p))
            for x,v in zip(xs,fp):
                m=(abs(train.x_open_bp-x)<=10)&(abs(train.rv_open_log-z)<=.2)
                if info=='L':m &= abs(train.w_preclose_bp-w)<=20
                n=int(m.sum());b=int(np.unique((np.arange(len(train))//5)[m]).size)
                heat.append(dict(model_id=s['model_id'],info=info,x=x,z=z,w=w,forecast=v,n=n,blocks=b,supported=n>=50 and b>=20))
        for term,scores,weights in zip(model.term_names_,model.term_scores_,model.bin_weights_):
            for index in np.ndindex(scores.shape):
                components.append(dict(model_id=s['model_id'],term=term,index=json.dumps(index),score=float(scores[index]),weight=float(weights[index]),
                                       interpretation='Centered native software component, not unique raw effect; whole-model contrasts separate'))
    # Stage2A models on the same new nonzero pointwise functional, without refitting.
    a=json.loads((ROOT/'config/B_stage2A_linear_spline_protocol.json').read_text())
    co=pd.read_csv(root/'registry/B_stage2A_coefficients.csv')
    from .state_models import specifications as linear_specs,design
    for s in linear_specs():
        if s['family'] not in ['C1','C2','S4']:continue
        c=p['contrast_grid'][s['info']]['display_candidate'];lo,_,hi=p['z_representatives']
        q=query_frame([-c['a'],c['a'],-c['a'],c['a']],[lo,lo,hi,hi],c['w']);d=design(q,s,a['preprocessing'])
        b=co.loc[co.fit_id.eq(f'{s["model_id"]}_FULL_fixed')&co.covariance.astype(str).eq('OLS')].set_index('term').reindex(d.columns).estimate.to_numpy()
        if not np.isfinite(b).all():raise ValueError(f'Missing Stage2A saved coefficients {s["model_id"]}')
        v=d.to_numpy()@b
        shapes.append(dict(model_id=s['model_id'],info=s['info'],variant='FULL',mode='fixed',seed=None,D_F=v[3]-v[2]-v[1]+v[0],
                           increment_low=v[1]-v[0],increment_high=v[3]-v[2],x_minus=-c['a'],x_plus=c['a'],w=c['w'],
                           support_status=p['contrast_grid'][s['info']]['status'],interval_status='NOT_CERTIFIED_IN_THIS_STAGE',
                           scientific_status='EXPLORATORY_PROJECTION' if p['contrast_grid'][s['info']]['chosen'] else 'ABSTAIN',
                           note='Reconstructed original saved coefficients/basis; no baseline refit'))
    outputs=[]
    for name,rows in [('models',[r['meta'] for r in runs]),('training_metrics',trainmetrics),('validation_metrics',valmetrics),
                      ('diagnostics',diagnostics),('shape_contrasts',shapes),('paired_loss_tests',paired),
                      ('interaction_and_multiplicity',multiplicity),('stability',stability),('theory_method_ledger',theory_ledger()),
                      ('surfaces',surfaces),('term_importance',importance),('empirical_bands',band),('empirical_cells',empirical_cells),
                      ('state_composition',comp),('discretization',discrete),('continuous_grid',heat),('software_components',components)]:
        outputs.append(export_csv(root,name,rows))
    outputs.append(export_csv(root,'finite_differences',finite))
    outputs.append(export_csv(root,'decisions',decisions))
    out=root/'derived/B/B_stage2B_ebm_predictions_v1.parquet';pred.to_parquet(out,index=False,compression='zstd');outputs.append(out)
    effective=root/'registry/B_stage2B_ebm_selected_parameters.json'
    write_json(effective,{mid:dict(setting=state['selected'][mid],effective=primary[mid].get_params(),
                                 feature_types=list(primary[mid].feature_types_in_),terms=list(primary[mid].term_names_),
                                 bins=[[b if isinstance(b,dict) else np.asarray(b).tolist() for b in bs] for bs in primary[mid].bins_]) for mid in primary})
    outputs.append(effective)
    from .stage2b_report import figures,write_reports
    figurepaths=figures(root,p,train,val,pred,pd.DataFrame(valmetrics),pd.DataFrame(shapes),pd.DataFrame(surfaces),
                        pd.DataFrame(heat),pd.DataFrame(stability),pd.DataFrame(diagnostics),pd.DataFrame(comp),primary)
    manifest=dict(stage=p['stage'],verdict='PASS WITH QUALIFICATIONS',model_ladder='STAGE2B_MODEL_LADDER_COMPLETE',
                  protocol=file_ref(ROOT/'config/B_stage2B_EBM_protocol_v1.json',ROOT),counts=p['counts'],
                  daily=p['daily'],dataset_id=p['dataset_id'],stage2A_predictions=p['stage2A_predictions'],
                  selected=state['selected'],fitted_runs=len(runs),required_families=len(primary),failed_fits=0,
                  planned_count_arithmetic=dict(component_sum=expected,v1_total_field=662,
                                                note='V1 total field mis-summed; all seven frozen fit categories executed unchanged'),
                  seeds=p['seeds'],predictions=file_ref(out,root),prediction_rows=len(pred),
                  support={i:g['status'] for i,g in p['contrast_grid'].items()},
                  shape_status={'E':'INCONCLUSIVE_MODEL_SHAPE_NOT_CERTIFIED_RAW','L':'ABSTAIN'},
                  prediction_decisions=decisions,
                  seal_intact=True,sealed_scientific_rows_exposed=0,new_market_data_requests=0,
                  null_status='DEFERRED_TO_STAGE4',shape_pipeline_bootstrap='NOT_RUN; seed/time-window stability only',
                  resources=state['resources'],publication_seconds=time.perf_counter()-started,
                  peak_process_RSS_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)) if resource else None,
                  memory_note='Process high-water RSS observed at publication; score_bytes per fit covers native score arrays only, not per-fit peak memory',
                  effective_environment=p['environment'],git_commit=p['git_commit'],
                  code=[file_ref(f,ROOT) for f in (ROOT/'src/ebm_research/experiment_b').glob('*2b*.py')]+[file_ref(ROOT/'src/ebm_research/experiment_b/ebm_models.py',ROOT)],
                  products=[file_ref(f,root) for f in outputs],figures=[file_ref(f,ROOT) for f in figurepaths],
                  models=[r['meta']['model_artifact'] for r in runs if 'model_artifact' in r['meta']],
                  recovery=state.get('engineering_recovery',[]),failed_attempts=state.get('failed_attempts',[]),
                  previous_code_identity=state['identity'],scientific_qualifications=['Heavy tails/dependence','training 2021 hyperparameter selection','validation previously reused in Stage2A','No certified pointwise contrast intervals','L support fails'])
    reports=write_reports(root,p,manifest,pd.DataFrame(valmetrics),pd.DataFrame(shapes),pd.DataFrame(paired),pd.DataFrame(multiplicity),pd.DataFrame(stability))
    manifest['reports']=[file_ref(f,ROOT) for f in reports]
    manifest['new_product_bytes']=sum(f['bytes'] for f in manifest['products']+manifest['figures']+manifest['models']+manifest['reports'])
    if manifest['new_product_bytes']>p['resource']['max_retained_bytes']:raise RuntimeError('Publication storage cap exceeded; inspect outputs')
    write_json(root/'registry/B_stage2B_ebm_manifest.json',manifest)
    print(json.dumps(dict(action='PUBLISHED',fits=len(runs),families=len(primary),prediction_rows=len(pred),bytes=manifest['new_product_bytes'])),flush=True)


def publish_cached(root,p):
    """Resume publication from bounded private checkpoint; no additional EBM fitting."""
    from .stage2b import PROTOCOL,verify,read_development
    verify(root,p)
    checkpoint=ROOT/'logs/stage2B_checkpoint.json'
    if checkpoint.exists():s=json.loads(checkpoint.read_text())
    else:
        with gzip.open(checkpoint.with_suffix('.json.gz'),'rt') as f:s=json.load(f)
    if s['identity']['protocol']!=sha(PROTOCOL):raise ValueError('Checkpoint protocol mismatch')
    models={spec['model_id']:joblib.load(ROOT/f'artifacts/B/checkpoints/stage2B/{spec["model_id"]}.joblib') for spec in p['models']}
    train=read_development(root/p['daily']['path'],*p['train']);val=read_development(root/p['daily']['path'],*p['validation'])
    yt=train.y_last30_bp.to_numpy();yv=val.y_last30_bp.to_numpy()
    n1t=np.r_[0.,np.cumsum(yt)[:-1]/np.arange(1,len(yt))]
    n1v=(yt.sum()+np.r_[0.,np.cumsum(yv)[:-1]])/(len(yt)+np.arange(len(yv)))
    publish(root,p,s,models,train,val,n1t,n1v)
