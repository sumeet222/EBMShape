"""Offline Stage2A: frozen state regressions, inference and chronological validation."""
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
from scipy.stats import norm
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.multitest import multipletests

from .acquisition import file_ref, verify_files
from .benchmarks import trio, volatility_tables
from .linear_diagnostics import load_training, compare_baseline
from .pilot import ROOT, sha, write_json
from .stage1 import manual_check
from .state_models import (specifications,guard_history,fit_preprocessing,design,fit_model,
                           covariance,evaluate_linear,vector_at,slope_vector,wald,preprocessing_hash)


def training_inputs(root):
    """Verify frozen daily/source lineage and read training plus date metadata only."""
    stage1=json.loads((ROOT/'config/B_stage1_dataset_selection.json').read_text())
    frame,manifest=load_training(root,stage1)
    for r in manifest['code']:
        if sha(ROOT/r['path'])!=r['sha256']:raise ValueError(f'Stage1 execution code changed: {r["path"]}')
    dates=pd.read_parquet(root/manifest['daily']['path'],columns=['session_et','eligible_primary'])
    actual={key:int((dates.eligible_primary & dates.session_et.astype(str).between(*stage1[key])).sum())
            for key in ['train','validation','sealed_test']}
    prior_coverage=pd.read_csv(root/'registry/B_stage1_coverage.csv')
    for key,value in actual.items():
        expected=int(prior_coverage.loc[prior_coverage.view.eq('principal') & prior_coverage.dimension.eq('split') & prior_coverage.period.eq(key),'eligible'].iloc[0])
        if value!=expected:raise ValueError(f'Split metadata count conflict: {key}')
    return frame,manifest,stage1,dict(rows=len(dates),eligible=int(dates.eligible_primary.sum()),**actual)


def march18_check(root,train):
    """Independently verify five original price anchors before influence interpretation."""
    baseline=json.loads((root/'registry/D2_spy_source_manifest.json').read_text())
    ref=baseline['blocks']['2020']['canonical'];verify_files(root,[ref])
    days=[dt.date(2020,3,17),dt.date(2020,3,18)]
    minutes=pd.read_parquet(root/ref['path'],filters=[('session_et','in',days)])
    row=train.loc[train.session_et.eq(days[1])]
    checked=manual_check(minutes,row)
    errors={p:abs(float(row[p].iloc[0])-v) for p,v in checked['source_prices'].items()}
    if max(errors.values())>1e-12:raise ValueError('INVALID—RERUN: March18 original price anchors disagree')
    gaps=pd.read_csv(root/'registry/D2_spy_missing_candles.csv')
    midday=gaps.loc[gaps.session_et.eq('2020-03-18')]
    if len(midday)!=14 or not midday.affected_windows.eq('other').all():
        raise ValueError('March18 gap metadata disagrees with frozen noncritical interval')
    private=root/'derived/B/B_stage2A_march18_anchor_check.json';write_json(private,checked)
    return dict(date='2020-03-18',original_source=ref,private_price_audit=file_ref(private,root),
                anchors=list(errors),max_price_error=max(errors.values()),all_manual_equations_match=True,
                gap_minutes=14,gap='12:57–13:10 ET',gap_outside_required_windows=True)


def choose_support(train,pre):
    """Predictor-only X/W anchors and coarse cells, fixed before curves/outcomes."""
    group=np.searchsorted(pre['cutoffs_raw'],train.rv_open_raw,side='left')
    inner=[]
    for g in range(3):
        lo,hi=np.quantile(train.loc[group==g,'x_open_bp'],[.1,.9])
        inner.append(min(-lo,hi))
    magnitude=float(np.floor(.8*min(inner)/5)*5)
    if magnitude<=0:raise ValueError('No symmetric X anchor inside common training support')
    wlo,whi=np.quantile(train.w_preclose_bp,[.1,.9])
    if not wlo<0<whi:raise ValueError('W=0 lacks central training support')
    return dict(x0=0.,x_magnitude=magnitude,x_grid=np.linspace(-magnitude,magnitude,9).tolist(),
                x_bins=[-magnitude/2,magnitude/2],w_fixed=0.,w_band=[float(wlo),float(whi)],
                z_representatives=pre['representatives'],minimum_n=50,minimum_blocks=20,
                strong_n=100,strong_blocks=30,block_unit='nonoverlapping groups of five eligible training rows',
                note='coarse state × X cells; L additionally restricts W to training10–90pct band; no raw point-identification claim')


def freeze_protocol(root,path):
    """First-run predictor-only protocol freeze; never overwrite a previous protocol."""
    if path.exists():raise ValueError('Protocol already exists; use normal run to verify and reuse it')
    train,manifest,stage1,counts=training_inputs(root)
    influence=pd.read_csv(root/'registry/B_stage1_5_influence.csv')
    fixed=['2020-03-18','2020-03-13','2020-02-28','2020-03-27','2020-03-24']
    actual=influence.loc[influence.model.eq('OLS1_E')].sort_values('rank').session_et.tolist()
    if actual!=fixed:raise ValueError('Frozen Stage1.5 OLS1 influence ranking differs from authorized keys')
    march=march18_check(root,train)
    pre=fit_preprocessing(train,'2022-01-01')
    original_cuts=json.loads((root/'registry/B_stage1_state_metadata.json').read_text())[0]['rv_raw_cutoffs']
    np.testing.assert_allclose(pre['cutoffs_raw'],original_cuts,rtol=0,atol=1e-15)
    for spec in specifications():
        matrix=design(train,spec,pre)
        if np.linalg.matrix_rank(matrix)!=matrix.shape[1]:raise ValueError(f'Initial singular design {spec["model_id"]}')
        assert np.isfinite(design(train.head(8),spec,pre)).all().all()
    refs=['AGENTS.md','docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md',
          'docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md',
          'config/B_stage1_dataset_selection.json','data/registry/B_stage1_daily_manifest.json',
          'data/registry/B_stage1_coefficients.csv','data/registry/B_stage1_state_metadata.json',
          'data/registry/B_stage1_qa.json','data/registry/B_stage1_5_diagnostics_manifest.json',
          'data/registry/B_stage1_5_linear_diagnostics_summary.csv','data/registry/B_stage1_5_influence.csv',
          'data/registry/D2_spy_source_manifest.json','data/registry/D2_1c_hf_repair_manifest.json',
          'docs/experiment_B_source_method_crosswalk.md']
    protocol=dict(stage='B_stage2A',version=1,frozen_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  inputs={p:sha(root/p.removeprefix('data/') if p.startswith('data/') else ROOT/p) for p in refs},
                  dataset_id=manifest['dataset_id'],daily=manifest['daily'],counts=counts,train=stage1['train'],
                  validation=stage1['validation'],sealed=stage1['sealed_test'],preprocessing=pre,support=choose_support(train,pre),
                  source_check=march,models=specifications(),naive_models=['N0','N1'],
                  N1='Expanding mean of all prior eligible observed targets, initialized from full training mean for validation; updates after each prior validation close. Training descriptive first forecast0 then prior-only mean. Identical comparator in fixed/quarterly modes.',
                  sensitivity_variants=['FULL','DROP_TOP1','DROP_TOP5','EXCLUDE_2020','MATCHED_SOURCE'],
                  drop_top1=fixed[:1],drop_top5=fixed,source_exclusions=['2019-08-12','2019-08-13'],
                  sensitivity_preprocessing='All fixed-fit deletions preserve original FULL training cutoffs/knots/transforms/centering; validation rows unchanged; fixed prediction only.',
                  huber='C1/C2/S4 and optional C1/C2 Wmod: all-days HuberT1.345 MAD maxiter200 tol1e-8 point-only; fixed validation. S6 robust omitted as redundant complexity sensitivity.',
                  quarterly_schedule=[f'{y}-{m:02d}-01' for y in [2022,2023] for m in [1,4,7,10]],
                  quarterly_preprocessing='Keep categorical cutoffs fixed at original2016–2021 training values for all validation. Re-estimate Z centering and spline knots/scales on eligible history strictly before quarter start, including completed earlier validation Y; FULL selection only.',
                  inference=dict(hac_lags=[5,10,20],kernel='Bartlett',use_correction=True,use_t=False,ci=.95,
                                 family='Six primary tests: C1 X-state joint, C2 XZ, S4 added f/g curvature vs C2, separately E/L; Holm over6; additional tests exploratory',
                                 tails='Linear natural spline outside first/last knots, no clipping; count boundaries and observed training-range exceedance',
                                 knots='S4: .05,.35,.65,.95; S6: .05,.23,.41,.59,.77,.95. Function dimensions include intercept; E ranks8/12, L9/13.',
                                 transform='Restricted cubic curvature residualized on1,Zc using training predictors only, centered0 at medianZ, divided by training residual SD; C2 columns explicit and nested.'),
                  diagnostics=dict(lags=[5,10,20],acf=[1,5,10,20],arch=5,studentization='internal',top_cook=5,
                                   White='All full designs: expanded variance squares/products, actual matrix rank-1 df; NOT_APPLICABLE on instability/rank failure.',
                                   RESET='One fitted-square HAC5 for OLS references/C1/C2 only; spline uses nested curvature Wald instead.',
                                   bins=10,min_bin_n=20,temporal_models=['C1_E','C2_E','S4_E','C1_L','C2_L','S4_L'],
                                   temporal_periods={'2016_2019':['2016-01-05','2019-12-31'],'2020':['2020-01-01','2020-12-31'],'2021':['2021-01-01','2021-12-31']},
                                   leave_year_models=['C2_E','S4_E','C2_L','S4_L'],
                                   break_models=['C2_E','C2_L'],break_definition='Fixed2020 intercept+X×D2020, controlling original centeredZ/XZ and W when L; no breakpoint search'),
                  metrics=['MSE','RMSE','MAE','bias_prediction_minus_actual','R2_N0','R2_causal_N1','Pearson','directional_accuracy','majority_direction_baseline','p95_absolute_error'],
                  paired='Comparator squared loss minus candidate; HAC5 for C1/C2/S4 vs same-info OLS and best naive, plus S4 vs best C1/C2; lag10/20 for S4 comparisons. Save per-date differences in one prediction file; selected comparator inference exploratory.',
                  recommendation='Rank six primary FULL candidates by quarterly validation MSE within E/L; retain minimum as descriptive benchmark. Convincing improvement requires positive HAC5 CI for paired gain vs strongest same-info naive/OLS. Sensitivity variants never replace FULL; S6/Wmod are disclosed comparisons, not automatic primary replacements.',
                  figures=8,random_seed=None,no_sealed_scientific_access=True,no_new_data_downloads=True,
                  execution_data_budget_bytes=100_000_000)
    write_json(path,protocol)
    print(json.dumps(dict(action='PROTOCOL_FROZEN',path=str(path.relative_to(ROOT)),sha256=sha(path),
                          counts=counts,z_ref=pre['z_ref'],x_magnitude=protocol['support']['x_magnitude'],march18_check='PASS')))


def support_rows(frame,pre,protocol,cohort='train'):
    """Coarse empirical support with explicit low-count/block abstention."""
    g=np.searchsorted(pre['cutoffs_raw'],frame.rv_open_raw,side='left')
    s=protocol['support'];xbin=np.searchsorted(s['x_bins'],frame.x_open_bp,side='right')
    block=np.arange(len(frame))//5;rows=[]
    for info in ['E','L']:
        wmask=np.ones(len(frame),dtype=bool) if info=='E' else frame.w_preclose_bp.between(*s['w_band']).to_numpy()
        for j,state in enumerate(['low','middle','high']):
            for b,name in enumerate(['negative','zero','positive']):
                mask=(g==j)&(xbin==b)&wmask;n=int(mask.sum());blocks=int(len(np.unique(block[mask])))
                rows.append(dict(cohort=cohort,info=info,state=state,x_cell=name,n=n,blocks=blocks,
                                 supported=n>=s['minimum_n'] and blocks>=s['minimum_blocks'],
                                 strong_support=n>=s['strong_n'] and blocks>=s['strong_blocks'],
                                 x_min=float(frame.loc[mask,'x_open_bp'].min()) if n else None,
                                 x_max=float(frame.loc[mask,'x_open_bp'].max()) if n else None,
                                 W_band='all' if info=='E' else str(s['w_band'])))
    return rows


def cell_supported(support,info,state,x,protocol):
    cell=['negative','zero','positive'][np.searchsorted(protocol['support']['x_bins'],x,side='right')]
    return next(r['supported'] for r in support if r['info']==info and r['state']==state and r['x_cell']==cell)


def fit_metadata(fit,fit_id,variant,mode,frame,elapsed,pre,asof):
    """Every attempted successful fit has a dataset/date/preprocessing identity."""
    spec=fit['spec'];r=fit['result']
    return dict(fit_id=fit_id,model_id=spec['model_id'],family=spec['family'],info=spec['info'],
                variant=variant,mode=mode,n=len(frame),first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),
                fit_asof=asof,rank=fit['rank'],parameters=len(fit['columns']),condition=fit['condition'],
                columns=json.dumps(fit['columns']),coefficient_units='Y bp; X/W bp, Z dimensionless logRV, curvature standardized',
                status='PASS',fit_seconds=elapsed,design_bytes=int(fit['design'].memory_usage(deep=True).sum()),
                preproc_sha256=preprocessing_hash(pre),primary=spec['primary'],role=spec['complexity_role'],
                r_squared=float(r.rsquared) if hasattr(r,'rsquared') else None,
                adjusted_r_squared=float(r.rsquared_adj) if hasattr(r,'rsquared_adj') else None,
                huber_iterations=int(r.fit_history['iteration']) if hasattr(r,'fit_history') else None)


def coefficient_rows(fit,fit_id,kinds=None):
    rows=[]
    for kind in (kinds or ['OLS','HC3',5,10,20]):
        result=covariance(fit,kind);ci=result.conf_int(alpha=.05)
        for i,term in enumerate(fit['columns']):
            # Ordinary SE comparator also uses normal reference for consistent reporting.
            estimate=float(result.params[i]);se=float(result.bse[i])
            rows.append(dict(fit_id=fit_id,model_id=fit['spec']['model_id'],term=term,covariance=str(kind),
                             estimate=estimate,se=se,ci_low=estimate-1.95996398454*se,ci_high=estimate+1.95996398454*se,
                             p_value=float(2*norm.sf(abs(estimate/se))) if se else None,
                             units='bp for intercept/basis main effects; bp/bp for X/W slope coefficients',status='COMPUTED'))
    return rows


def inference_rows(fit,fit_id,protocol,support):
    """Whole-response/slope contrasts and correctly nested joint covariance tests."""
    spec=fit['spec'];cols=fit['columns'];family=spec['family'];rows=[];info=spec['info']
    base=dict(fit_id=fit_id,model_id=spec['model_id'],info=info,scope='EXPLORATORY',units='bp/bp for slope; bp for response/anchored contrasts')
    blocks={'overall_slopes':[c for c in cols if c!='intercept']}
    if family=='C1':blocks['X_state_moderation']=['X_DM','X_DH']
    if family=='C2':blocks['X_state_moderation']=['X_Zc']
    if family.startswith('S'):
        h=[c for c in cols if c.startswith('H') or c.startswith('X_H')]
        blocks.update(curvature_vs_C2=h,X_state_moderation=['X_Zc']+[c for c in cols if c.startswith('X_H')],
                      X_slope_curvature=[c for c in cols if c.startswith('X_H')])
    if spec['w_moderation']:blocks['W_state_moderation']=[c for c in cols if c.startswith('W_')]
    for name,terms in blocks.items():
        primary=spec['primary'] and ((family in ['C1','C2'] and name=='X_state_moderation') or (family=='S4' and name=='curvature_vs_C2'))
        for lag in [5,10,20]:
            rows.append(dict(base,kind='WALD',contrast=name,lag=lag,scope='PREDECLARED_FAMILY' if primary and lag==5 else 'EXPLORATORY',
                             null='named coefficient block =0',**wald(fit,terms,lag)))
    if family.startswith('OLS'):return rows
    reps=protocol['support']['z_representatives'];magnitude=protocol['support']['x_magnitude']
    for j,(state,z) in enumerate(zip(['low','middle','high'],reps)):
        ok=all(cell_supported(support,info,state,x,protocol) for x in [-magnitude,0,magnitude])
        for name,v in [('X_slope',slope_vector(fit,z)),('intercept_at_X0_W0',vector_at(fit,0,z))]:
            rows.append(dict(base,kind='CONTRAST',contrast=name,state=state,z=z,x=0.,lag=5,
                             status='COMPUTED' if ok else 'ABSTAIN',**(evaluate_linear(fit,v) if ok else {})))
        for x in protocol['support']['x_grid']:
            supported=cell_supported(support,info,state,x,protocol) and cell_supported(support,info,state,0,protocol)
            for name,v in [('total_response',vector_at(fit,x,z)),
                           ('anchored_X_response',vector_at(fit,x,z)-vector_at(fit,0,z))]:
                rows.append(dict(base,kind='CONTRAST',contrast=name,state=state,z=z,x=x,lag=5,
                                 status='COMPUTED' if supported else 'ABSTAIN',**(evaluate_linear(fit,v) if supported else {})))
    for lag in [5,10,20]:
        for name,v in [('high_minus_low_X_slope',slope_vector(fit,reps[2])-slope_vector(fit,reps[0])),
                       ('high_minus_middle_X_slope',slope_vector(fit,reps[2])-slope_vector(fit,reps[1]))]:
            ok=all(cell_supported(support,info,state,x,protocol) for state in ['low','middle','high'] for x in [-magnitude,0,magnitude])
            rows.append(dict(base,kind='CONTRAST',contrast=name,lag=lag,status='COMPUTED' if ok else 'ABSTAIN',
                             **(evaluate_linear(fit,v,lag) if ok else {})))
    for x in protocol['support']['x_grid']:
        v=(vector_at(fit,x,reps[2])-vector_at(fit,0,reps[2]))-(vector_at(fit,x,reps[0])-vector_at(fit,0,reps[0]))
        ok=all(cell_supported(support,info,state,q,protocol) for state in ['low','high'] for q in [0,x])
        rows.append(dict(base,kind='CONTRAST',contrast='four_point_D',x=x,lag=5,status='COMPUTED' if ok else 'ABSTAIN',
                         **(evaluate_linear(fit,v) if ok else {})))
    return rows


def paired_arrays(candidate,comparator):
    """Exact date-paired comparator loss minus model loss; reject mismatched keys."""
    if (candidate.session_et.duplicated().any() or comparator.session_et.duplicated().any()
            or set(candidate.session_et)!=set(comparator.session_et)):
        raise ValueError('Paired losses require exactly matched unique dates')
    aligned=comparator.set_index('session_et').loc[candidate.session_et]
    return aligned.loss.to_numpy()-candidate.loss.to_numpy()


def metric_row(frame,forecast,n1,**keys):
    """Matched descriptive/OOS bp metrics, with named causal N1 denominator."""
    y=frame.y_last30_bp.to_numpy();p=np.asarray(forecast);e=p-y
    if len(p)!=len(y) or not np.isfinite(p).all():raise ValueError('Incomplete/nonfinite matched forecast')
    mse=float(np.mean(e*e));zero=float(np.mean(y*y));mean_loss=float(np.mean((np.asarray(n1)-y)**2))
    return dict(keys,n=len(y),first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),
                MSE=mse,RMSE=float(np.sqrt(mse)),MAE=float(np.mean(np.abs(e))),bias=float(np.mean(e)),
                R2_N0=1-mse/zero if zero else None,R2_causal_N1=1-mse/mean_loss if mean_loss else None,
                Pearson=float(np.corrcoef(p,y)[0,1]) if np.std(p)>1e-12 and np.std(y)>0 else None,
                directional_accuracy=float(np.mean(np.sign(p)==np.sign(y))),
                always_up_accuracy=float(np.mean(y>0)),always_down_accuracy=float(np.mean(y<0)),
                retrospective_majority_accuracy=float(max(np.mean(y>0),np.mean(y<0))),
                p95_absolute_error=float(np.quantile(np.abs(e),.95)),units='bp errors; bp² MSE',
                status='COMPUTED',note='Direction near zero exploratory; retrospective majority is descriptive, not a causal forecast')


def load_validation(root,protocol,with_outcome=True):
    """Read eligible 2022–2023 rows only; sealed scientific columns never requested."""
    path=root/protocol['daily']['path'];bounds=protocol['validation']
    predicate=[('session_et','>=',dt.date.fromisoformat(bounds[0])),('session_et','<=',dt.date.fromisoformat(bounds[1])),('eligible_primary','=',True)]
    dates=pd.read_parquet(path,columns=['session_et'],filters=predicate)
    if len(dates)!=protocol['counts']['validation'] or not dates.session_et.astype(str).between(*bounds).all():
        raise ValueError('Validation date metadata mismatch')
    cols=None if with_outcome else ['session_et','eligible_primary','x_open_bp','w_preclose_bp','rv_open_raw','rv_open_log']
    frame=pd.read_parquet(path,columns=cols,filters=predicate)
    if frame.session_et.duplicated().any():raise ValueError('Duplicate validation keys')
    return frame


def run(root,protocol_path):
    """Execute the bounded frozen train→sensitivity→validation workflow offline."""
    wall=time.perf_counter();cpu=time.process_time();free=shutil.disk_usage(root).free
    protocol=json.loads(protocol_path.read_text());protocol_hash=sha(protocol_path)
    for name,digest in protocol['inputs'].items():
        path=root/name.removeprefix('data/') if name.startswith('data/') else ROOT/name
        if sha(path)!=digest:raise ValueError(f'Frozen input changed: {name}')
    train,prior,stage1,counts=training_inputs(root);pre=protocol['preprocessing']
    if counts!=protocol['counts']:raise ValueError('Frozen metadata counts changed')
    # Existing source-style fits must reproduce before any new inference.
    old=trio(train,stage1,'principal');state_rows,_=volatility_tables(train,stage1,'principal',pre['cutoffs_raw'])
    baseline=compare_baseline(old+state_rows,pd.read_csv(root/'registry/B_stage1_coefficients.csv'),
                              dict(baseline_atol=1e-10,baseline_rtol=1e-9))
    matched=train.loc[~train.session_et.astype(str).isin(protocol['source_exclusions'])]
    source_trio=trio(matched,stage1,'matched')
    source_saved=pd.read_csv(root/'registry/B_stage1_coefficients.csv')
    source_saved=source_saved.loc[source_saved.cohort.eq('alpaca_only')&source_saved.model.isin(['OLS1_E','OLS2_L','OLS3_L'])].assign(cohort='principal')
    baseline['matched_source_trio']=compare_baseline(source_trio,source_saved,dict(baseline_atol=1e-10,baseline_rtol=1e-9))
    registry=[];coefficients=[];inferences=[];diagnostics=[];sensitivity=[];metric=[];prediction=[]
    preprocessing={preprocessing_hash(pre):pre};fits={};variant_fits={}
    support=support_rows(train,pre,protocol)
    # Record legacy verification fits as audit entries, not candidate replacements.
    for model,part in pd.DataFrame(old+state_rows).groupby('model'):
        r=part.iloc[0]
        registry.append(dict(fit_id='VERIFY_'+model,model_id=model,family='legacy_verification',info='E' if 'OLS1' in model or 'RV_' in model else 'L',
                             variant='FULL',mode='baseline_verification',n=int(r.n),first=r['first'],last=r['last'],status='VERIFIED',
                             parameters=part.term.nunique(),rank=part.term.nunique(),role='prior_stage_verification'))
    for model,part in pd.DataFrame(source_trio).groupby('model'):
        r=part.iloc[0]
        registry.append(dict(fit_id='VERIFY_MATCHED_'+model,model_id=model,family='legacy_verification',info='E' if model=='OLS1_E' else 'L',
                             variant='MATCHED_SOURCE',mode='baseline_verification',n=int(r.n),first=r['first'],last=r['last'],status='VERIFIED',
                             parameters=part.term.nunique(),rank=part.term.nunique(),role='source_equivalence_verification'))

    def attempt(frame,spec,variant='FULL',mode='fixed',p=pre,asof='2022-01-01',fit_id=None,robust=False):
        fid=fit_id or f'{spec["model_id"]}_{variant}_{mode}';started=time.perf_counter()
        try:
            fit=fit_model(frame,spec,p,asof,robust)
        except (ValueError,np.linalg.LinAlgError) as error:
            registry.append(dict(fit_id=fid,model_id=spec['model_id'],family=spec['family'],info=spec['info'],variant=variant,mode=mode,
                                 n=len(frame),fit_asof=asof,status='FAILED',error=str(error),fit_seconds=time.perf_counter()-started))
            return None
        fit['fit_id']=fid;fit['variant']=variant;fit['mode']=mode
        meta=fit_metadata(fit,fid,variant,mode,frame,time.perf_counter()-started,p,asof)
        meta['parameters_json']=json.dumps(dict(zip(fit['columns'],map(float,fit['result'].params))))
        if robust and meta['huber_iterations']>=200:meta['status']='QUALIFIED_MAXITER'
        registry.append(meta);preprocessing[preprocessing_hash(p)]=p
        fit['history_last_date']=meta['last']
        return fit

    n1train=train.y_last30_bp.expanding().mean().shift(1).fillna(0).to_numpy()
    for spec in protocol['models']:
        fit=attempt(train,spec)
        if fit is None:continue
        fits[spec['model_id']]=fit
        coefficients+=coefficient_rows(fit,fit['fit_id'])
        inferences+=inference_rows(fit,fit['fit_id'],protocol,support)
        from .stage2a_diagnostics import full_diagnostics
        def refit(subset,spec,label):
            return attempt(subset,spec,label,'influence',fit_id=f'{spec["model_id"]}_{label}')
        diagnostics+=full_diagnostics(train,fit,fit['fit_id'],stage1,protocol,refit=refit)
        metric.append(metric_row(train,fit['result'].fittedvalues,n1train,model_id=spec['model_id'],info=spec['info'],variant='FULL',mode='train_descriptive'))
    for name,p in [('N0',np.zeros(len(train))),('N1',n1train)]:
        metric.append(metric_row(train,p,n1train,model_id=name,info='SHARED',variant='FULL',mode='train_descriptive'))
        registry.append(dict(fit_id=name,model_id=name,family='naive',info='SHARED',variant='FULL',mode='rule',
                             n=len(train),parameters=0 if name=='N0' else 1,status='PASS',role='causal_reference',
                             note=protocol['N1'] if name=='N1' else 'zero return, no fit'))

    # FULL preprocessing fixed for every training-row stress/source comparison.
    selections={'DROP_TOP1':~train.session_et.astype(str).isin(protocol['drop_top1']),
                'DROP_TOP5':~train.session_et.astype(str).isin(protocol['drop_top5']),
                'EXCLUDE_2020':~train.session_et.astype(str).str.startswith('2020'),
                'MATCHED_SOURCE':~train.session_et.astype(str).isin(protocol['source_exclusions'])}
    for variant,mask in selections.items():
        subset=train.loc[mask]
        for spec in protocol['models']:
            if spec['family'].startswith('OLS'):continue
            fit=attempt(subset,spec,variant)
            if fit:
                variant_fits[(spec['model_id'],variant)]=fit;coefficients+=coefficient_rows(fit,fit['fit_id'])
                sensitivity.append(sensitivity_row(fit,subset,protocol,'fixed_design_stress'))
    for spec in protocol['models']:
        if spec['family'].startswith('OLS') or spec['family']=='S6':continue
        fit=attempt(train,spec,'HUBER',robust=True)
        if fit:
            variant_fits[(spec['model_id'],'HUBER')]=fit
            sensitivity.append(sensitivity_row(fit,train,protocol,'Huber_point_only',robust=True))
    # Fixed-basis temporal comparisons; period support is separately audited.
    for period,bounds in protocol['diagnostics']['temporal_periods'].items():
        subset=train.loc[train.session_et.astype(str).between(*bounds)]
        period_support=support_rows(subset,pre,protocol,period);support+=period_support
        for mid in protocol['diagnostics']['temporal_models']:
            spec=next(s for s in protocol['models'] if s['model_id']==mid);fit=attempt(subset,spec,period,'temporal')
            if fit:
                coefficients+=coefficient_rows(fit,fit['fit_id'])
                sensitivity.append(sensitivity_row(fit,subset,protocol,'period_fixed_basis',support=period_support))
    for year in range(2016,2022):
        subset=train.loc[~train.session_et.astype(str).str.startswith(str(year))]
        for mid in protocol['diagnostics']['leave_year_models']:
            spec=next(s for s in protocol['models'] if s['model_id']==mid);fit=attempt(subset,spec,f'LEAVE_{year}','temporal')
            if fit:sensitivity.append(sensitivity_row(fit,subset,protocol,'leave_year_fixed_basis'))
    # Parsimonious fixed 2020 break: no search and original C2 design controlled.
    for mid in protocol['diagnostics']['break_models']:
        fit=fits[mid];d=fit['design'].copy();dummy=train.session_et.astype(str).str.startswith('2020').to_numpy()
        d['D2020']=dummy.astype(float);d['X_D2020']=train.x_open_bp.to_numpy()*dummy
        r=OLS(train.y_last30_bp.to_numpy(),d.to_numpy(),hasconst=True).fit()
        extended={**fit,'result':r,'design':d,'columns':list(d.columns),'rank':int(np.linalg.matrix_rank(d)),'condition':float(np.linalg.cond(d))}
        fid=mid+'_BREAK2020';registry.append(fit_metadata(extended,fid,'BREAK2020','temporal',train,0,pre,'2022-01-01'))
        inferences.append(dict(fit_id=fid,model_id=mid,info=fit['spec']['info'],kind='WALD',contrast='2020_X_slope_break',lag=5,scope='EXPLORATORY',**wald(extended,['X_D2020'])))

    # Primary training inference is complete before validation outcomes are read.
    features=load_validation(root,protocol,with_outcome=False)
    validation_predictor_audit=predictor_audit(features,pre,protocol)
    validation=load_validation(root,protocol,with_outcome=True)
    both=pd.concat([train,validation],ignore_index=True)
    n1all=both.y_last30_bp.expanding().mean().shift(1).fillna(0).to_numpy()
    n1val=n1all[len(train):]
    original_state=np.searchsorted(pre['cutoffs_raw'],validation.rv_open_raw,side='left')

    def add_prediction(fit,frame,forecast,mode,variant='FULL',asof='2022-01-01'):
        model=fit['spec']['model_id'];info=fit['spec']['info']
        for i,(_,row) in enumerate(frame.iterrows()):
            prediction.append(dict(session_et=row.session_et,model_id=model,info=info,mode=mode,variant=variant,source_view='D2_plus_source1' if variant!='MATCHED_SOURCE' else 'Alpaca_matched_equivalent',
                                   fit_asof=asof,history_last_date=fit['history_last_date'],fit_id=fit['fit_id'],actual=float(row.y_last30_bp),forecast=float(forecast[i]),
                                   loss=float((forecast[i]-row.y_last30_bp)**2),state=['low','middle','high'][np.searchsorted(pre['cutoffs_raw'],row.rv_open_raw,side='left')]))
    for mid,fit in fits.items():
        forecast=design(validation,fit['spec'],pre).to_numpy()@fit['result'].params
        add_prediction(fit,validation,forecast,'fixed')
    for (mid,variant),fit in variant_fits.items():
        forecast=design(validation,fit['spec'],pre).to_numpy()@fit['result'].params
        add_prediction(fit,validation,forecast,'fixed',variant)
    schedule=protocol['quarterly_schedule']
    for j,asof in enumerate(schedule):
        stop=schedule[j+1] if j+1<len(schedule) else '2024-01-01'
        history=both.loc[both.session_et.astype(str).lt(asof)]
        future=validation.loc[validation.session_et.astype(str).ge(asof)&validation.session_et.astype(str).lt(stop)]
        guard_history(history,asof)
        qp=fit_preprocessing(history,asof)
        # The explicit prompt freezes predictive categories throughout validation.
        qp['cutoffs_raw']=pre['cutoffs_raw'];qp['cutoffs_log']=pre['cutoffs_log']
        qgroups=np.searchsorted(pre['cutoffs_raw'],history.rv_open_raw,side='left')
        qp['representatives']=[float(history.loc[qgroups==g,'rv_open_log'].median()) for g in range(3)]
        validation_predictor_audit.setdefault('quarterly',{})[asof]=predictor_audit(future,qp,protocol)
        for spec in protocol['models']:
            fit=attempt(history,spec,'FULL','quarterly',qp,asof,fit_id=f'{spec["model_id"]}_Q_{asof}')
            if fit:
                coefficients+=coefficient_rows(fit,fit['fit_id'],['OLS'])
                forecast=design(future,spec,qp).to_numpy()@fit['result'].params
                add_prediction(fit,future,forecast,'quarterly',asof=asof)
    for mode in ['fixed','quarterly']:
        for model,forecast in [('N0',np.zeros(len(validation))),('N1',n1val)]:
            for i,(_,row) in enumerate(validation.iterrows()):
                prediction.append(dict(session_et=row.session_et,model_id=model,info='SHARED',mode=mode,variant='FULL',source_view='same_validation',
                                       fit_asof=str(row.session_et) if model=='N1' else 'none',fit_id=model,
                                       history_last_date=str(both.session_et.iloc[len(train)+i-1]) if model=='N1' else None,
                                       actual=float(row.y_last30_bp),forecast=float(forecast[i]),loss=float((forecast[i]-row.y_last30_bp)**2),
                                       state=['low','middle','high'][original_state[i]]))
    predictions=pd.DataFrame(prediction).sort_values(['variant','mode','model_id','session_et']).reset_index(drop=True)
    if predictions.duplicated(['variant','mode','model_id','session_et']).any():raise ValueError('Duplicate validation prediction keys')
    for (variant,mode,mid),part in predictions.groupby(['variant','mode','model_id'],sort=False):
        if list(part.session_et)!=list(validation.session_et):raise ValueError(f'Unmatched validation prediction dates: {mid}/{variant}/{mode}')
        metric.append(metric_row(validation,part.forecast,n1val,model_id=mid,info=part['info'].iloc[0],variant=variant,mode=mode))
        if variant=='FULL':
            from .stage2a_diagnostics import prediction_diagnostics
            if part.forecast.std()>1e-12:diagnostics+=prediction_diagnostics(validation,part.forecast.to_numpy(),mid,mode)
            else:diagnostics.append(dict(model_id=mid,mode=mode,statistic='validation_calibration_correlation',status='NOT_APPLICABLE',
                                         note='Constant forecast: no meaningful prediction-decile partition or Pearson/Spearman variation; overall bias/MSE reported'))
        for state in ['low','middle','high']:
            group=part.loc[part.state.eq(state)]
            diagnostics.append(dict(model_id=mid,variant=variant,mode=mode,statistic='validation_error_by_state',
                                    state=state,n=len(group),estimate=float(np.mean(group.forecast-group.actual)),
                                    RMSE=float(np.sqrt(group.loss.mean())),status='DESCRIPTIVE_ONLY'))
    metrics=pd.DataFrame(metric)
    full_errors=metrics.loc[metrics.variant.eq('FULL')].set_index(['mode','model_id'])
    metrics['delta_MSE_vs_FULL']=[float(r.MSE-full_errors.loc[(r['mode'],r.model_id),'MSE']) for _,r in metrics.iterrows()]
    metrics['delta_RMSE_vs_FULL']=[float(r.RMSE-full_errors.loc[(r['mode'],r.model_id),'RMSE']) for _,r in metrics.iterrows()]
    paired,recommendations=paired_tests(predictions,metrics,protocol)
    # Loss differences remain in this single lean date-by-model prediction file.
    for mode in ['fixed','quarterly']:
        for info,reference in [('E','OLS1_E'),('L','OLS3_L')]:
            for comparator in [reference,'N0','N1']:
                b=predictions.loc[predictions.variant.eq('FULL')&predictions['mode'].eq(mode)&predictions.model_id.eq(comparator)].set_index('session_et').loss
                mask=predictions['mode'].eq(mode)&predictions['info'].eq(info)
                predictions.loc[mask,'loss_difference_vs_'+('OLS' if comparator==reference else comparator)]=predictions.loc[mask,'session_et'].map(b).to_numpy()-predictions.loc[mask,'loss'].to_numpy()
            linear=metrics.loc[metrics['mode'].eq(mode)&metrics.variant.eq('FULL')&metrics.model_id.isin([f'C1_{info}',f'C2_{info}'])].sort_values(['MSE','model_id']).model_id.iloc[0]
            b=predictions.loc[predictions.variant.eq('FULL')&predictions['mode'].eq(mode)&predictions.model_id.eq(linear)].set_index('session_et').loss
            mask=predictions['mode'].eq(mode)&predictions['info'].eq(info)
            predictions.loc[mask,'loss_difference_vs_best_linear']=predictions.loc[mask,'session_et'].map(b).to_numpy()-predictions.loc[mask,'loss'].to_numpy()
            predictions.loc[mask,'selected_linear_reference']=linear
    # Fixed-basis multiple testing is a small explicit family, not an EBM discovery certificate.
    family=[r for r in inferences if r.get('scope')=='PREDECLARED_FAMILY' and r.get('status')=='COMPUTED']
    if family:
        adjusted=multipletests([r['p_value'] for r in family],method='holm')[1]
        for row,value in zip(family,adjusted):row['holm_p_value']=float(value)
    manifest=publish(root,protocol_path,protocol,baseline,registry,coefficients,inferences,diagnostics,support,
                     metrics,pd.DataFrame(paired),sensitivity,predictions,preprocessing,validation_predictor_audit,recommendations,
                     fits,train,validation,wall,cpu,free)
    return manifest


def sensitivity_row(fit,frame,protocol,kind,robust=False,support=None):
    """Fixed-design fitted state slopes; distinguish parameter projections from raw cells."""
    reps=protocol['support']['z_representatives'];rows={}
    for state,z in zip(['low','middle','high'],reps):
        v=slope_vector(fit,z);rows[state+'_slope']=float(v@fit['result'].params)
    v=slope_vector(fit,reps[2])-slope_vector(fit,reps[0])
    if support is None:support=support_rows(frame,fit['pre'],protocol,fit['variant'])
    allowed=all(cell_supported(support,fit['spec']['info'],s,x,protocol)
                for s in ['low','high'] for x in [-protocol['support']['x_magnitude'],0,protocol['support']['x_magnitude']])
    out=dict(fit_id=fit['fit_id'],model_id=fit['spec']['model_id'],info=fit['spec']['info'],variant=fit['variant'],
             comparison=kind,n=len(frame),first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),
             **rows,projection_high_low_slope=float(v@fit['result'].params),
             status='POINT_ONLY' if robust else 'COMPUTED' if allowed else 'ABSTAIN_RAW_CELL',
             estimand='fixed-basis linear projection slope; raw-cell claims separately support-gated',units='bp/bp')
    if robust:out['high_low_slope']=float(v@fit['result'].params)
    elif allowed:out.update({('high_low_slope' if k=='estimate' else k):value for k,value in evaluate_linear(fit,v).items()})
    return out


def predictor_audit(validation,pre,protocol):
    """Validation feature occupancy/range only, performed before validation Y read."""
    groups=np.searchsorted(pre['cutoffs_raw'],validation.rv_open_raw,side='left')
    out=dict(n=len(validation),state_counts={s:int((groups==j).sum()) for j,s in enumerate(['low','middle','high'])},
             ranges={},spline_boundary_exceedance={})
    for col,bounds in pre['ranges'].items():
        out['ranges'][col]=dict(below=int(validation[col].lt(bounds[0]).sum()),above=int(validation[col].gt(bounds[1]).sum()),
                                min=float(validation[col].min()),max=float(validation[col].max()))
    for dim,spline in pre['splines'].items():
        lo,hi=spline['boundaries']
        out['spline_boundary_exceedance'][dim]=dict(below=int(validation.rv_open_log.lt(lo).sum()),above=int(validation.rv_open_log.gt(hi).sum()),policy='linear tails, no clipping')
    return out


def paired_tests(predictions,metrics,protocol):
    """Date-paired validation loss inference and the predeclared recommendation rule."""
    rows=[];recommend=[]
    for mode in ['fixed','quarterly']:
        scores=metrics.loc[metrics['mode'].eq(mode)&metrics.variant.eq('FULL')]
        naive=scores.loc[scores.model_id.isin(['N0','N1'])].sort_values(['MSE','model_id']).model_id.iloc[0]
        def part(mid):
            return predictions.loc[predictions['mode'].eq(mode)&predictions.variant.eq('FULL')&predictions.model_id.eq(mid)]
        for info,ols in [('E','OLS1_E'),('L','OLS3_L')]:
            primary=[f'{family}_{info}' for family in ['C1','C2','S4']]
            bestlinear=scores.loc[scores.model_id.isin([f'C1_{info}',f'C2_{info}'])].sort_values(['MSE','model_id']).model_id.iloc[0]
            comparisons=[(mid,reference) for mid in primary for reference in [ols,naive]]
            comparisons.append((f'S4_{info}',bestlinear))
            # Retain pairwise evidence against both state-blind L references.
            if info=='L':comparisons.append(('S4_L','OLS2_L'))
            for mid,reference in comparisons:
                delta=paired_arrays(part(mid),part(reference))
                for lag in ([5,10,20] if mid.startswith('S4') else [5]):
                    result=OLS(delta,np.ones((len(delta),1))).fit().get_robustcov_results(cov_type='HAC',maxlags=lag,kernel='bartlett',use_correction=True,use_t=False)
                    ci=result.conf_int()[0]
                    rows.append(dict(model_id=mid,comparator=reference,info=info,mode=mode,n=len(delta),first=str(part(mid).session_et.iloc[0]),last=str(part(mid).session_et.iloc[-1]),
                                     mean_loss_gain=float(np.mean(delta)),se=float(result.bse[0]),ci_low=float(ci[0]),ci_high=float(ci[1]),
                                     p_value=float(result.pvalues[0]),lag=lag,units='bp² comparator MSE minus candidate MSE',status='COMPUTED',
                                     scope='EXPLORATORY_SELECTED_VALIDATION',null='mean paired squared-loss gain =0'))
            winner=scores.loc[scores.model_id.isin(primary)].sort_values(['MSE','model_id']).iloc[0]
            reference=scores.loc[scores.model_id.isin([naive,ols]+(['OLS2_L'] if info=='L' else []))].sort_values(['MSE','model_id']).iloc[0]
            delta=paired_arrays(part(winner.model_id),part(reference.model_id))
            test=OLS(delta,np.ones((len(delta),1))).fit().get_robustcov_results(cov_type='HAC',maxlags=5,kernel='bartlett',use_correction=True,use_t=False)
            ci=test.conf_int()[0]
            recommend.append(dict(info=info,mode=mode,descriptive_best_primary=winner.model_id,best_reference=reference.model_id,
                                  candidate_MSE=float(winner.MSE),reference_MSE=float(reference.MSE),mean_loss_gain=float(np.mean(delta)),
                                  gain_ci_low=float(ci[0]),gain_ci_high=float(ci[1]),gain_p_value=float(test.pvalues[0]),
                                  status='CONVINCING_VALIDATION_GAIN' if ci[0]>0 else 'ABSTAIN_SUPERIORITY',
                                  note='same validation used to rank candidates; interval is exploratory after selection, not independent confirmation'))
    return rows,recommend


def publish(root,protocol_path,protocol,baseline,registry,coefficients,inferences,diagnostics,support,
            metrics,paired,sensitivity,predictions,preprocessing,feature_audit,recommendations,fits,train,validation,wall,cpu,free):
    """Write compact registries, one prediction file, figures/report and hash manifest."""
    path=root/'derived/B/B_stage2A_validation_predictions.parquet'
    if not predictions.session_et.astype(str).between(*protocol['validation']).all():raise ValueError('Forbidden prediction outcome dates')
    history=predictions.history_last_date.dropna()
    if not (history.astype(str)<predictions.loc[history.index,'session_et'].astype(str)).all():
        raise ValueError('Within-day/future target history in prediction registry')
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.parquet.tmp');predictions.to_parquet(tmp,index=False,compression='zstd');tmp.replace(path)
    products=[]
    meta_by_id={r['fit_id']:r for r in registry}
    for rows in [coefficients,inferences,diagnostics,sensitivity]:
        for row in rows:
            meta=meta_by_id.get(row.get('fit_id'))
            if meta:
                for key in ['info','variant','mode','n','first','last','fit_asof','family']:
                    if key not in row or row[key] is None:row[key]=meta.get(key)
                row['cohort']='training' if meta['mode']!='quarterly' else 'prior_expanding_development'
                row['source_view']='Alpaca_matched_equivalent' if meta['variant']=='MATCHED_SOURCE' else 'D2_plus_source1'
            elif row.get('mode') in ['fixed','quarterly']:
                row.setdefault('cohort','validation');row.setdefault('variant','FULL')
                row.setdefault('first',protocol['validation'][0]);row.setdefault('last',str(validation.session_et.iloc[-1]))
    winners={r['descriptive_best_primary'] for r in recommendations if r['mode']=='quarterly'}
    for row in registry:
        row['library']='deterministic_rule' if row.get('family')=='naive' else 'statsmodels'
        row['library_version']=metadata.version('statsmodels') if row['library']=='statsmodels' else 'not_applicable'
        row['random_seed']='not_used_deterministic'
        row['validation_unique_dates']=int(predictions.loc[predictions.fit_id.eq(row['fit_id']),'session_et'].nunique())
        row['formula']='y_last30_bp ~ '+ ' + '.join(json.loads(row['columns'])) if row.get('columns') else row.get('note','legacy verification')
        row['selection_status']=('DESCRIPTIVE_BEST_PRIMARY_NOT_PROVEN' if row['model_id'] in winners and row['mode']=='fixed' and row['variant']=='FULL'
                                 else 'REFERENCE' if row.get('role') in ['reference','causal_reference']
                                 else 'COMPARISON_OR_SENSITIVITY')
    tables={'models':registry,'coefficients':coefficients,'inference':inferences,'model_diagnostics':diagnostics,'support':support,
            'validation_metrics':metrics,'paired_loss_tests':paired,'sensitivity':sensitivity}
    for name,values in tables.items():
        dest=root/'registry'/f'B_stage2A_{name}.csv';pd.DataFrame(values).to_csv(dest,index=False,lineterminator='\n');products.append(file_ref(dest,root))
    manifest=dict(stage='B_stage2A',verdict='PASS WITH QUALIFICATIONS',protocol=dict(path=str(protocol_path.relative_to(ROOT)),sha256=sha(protocol_path),version=protocol['version']),
                  dataset_id=protocol['dataset_id'],daily=protocol['daily'],inputs=protocol['inputs'],counts=protocol['counts'],
                  baseline_verification=baseline,march18_check=protocol['source_check'],preprocessing_runs=preprocessing,
                  validation_predictor_audit=feature_audit,recommendations=recommendations,products=products,
                  predictions=file_ref(path,root),prediction_rows=len(predictions),
                  failed_fits=[r for r in registry if r['status']=='FAILED'],
                  validation_target_access='only2022–2023; quarterly fitting dates strictly earlier than forecast; original categorical cutoffs fixed',
                  sealed_scientific_rows_exposed=0,new_market_data_requests=0,
                  versions={p:metadata.version(p) for p in ['numpy','pandas','scipy','statsmodels','pyarrow','matplotlib']},python=platform.python_version(),
                  git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    from .stage2a_report import make_figures,write_report
    figures=make_figures(train,validation,fits,protocol,predictions,metrics,inferences,diagnostics)
    manifest['figures']=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p)) for p in figures]
    report,methods=write_report(manifest,protocol,registry,metrics,inferences,diagnostics,support,sensitivity,paired,coefficients=coefficients)
    manifest['reports']=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p)) for p in [report,methods]]
    code=[Path(__file__).resolve(),ROOT/'src/ebm_research/experiment_b/state_models.py',ROOT/'src/ebm_research/experiment_b/stage2a_diagnostics.py',
          ROOT/'src/ebm_research/experiment_b/stage2a_report.py']
    manifest['code']=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in code]
    manifest['wall_seconds']=time.perf_counter()-wall;manifest['cpu_seconds']=time.process_time()-cpu
    manifest['free_before']=free;manifest['free_after']=shutil.disk_usage(root).free
    manifest['new_product_bytes']=sum(r['bytes'] for r in products)+manifest['predictions']['bytes']+sum(r['bytes'] for r in manifest['figures'])
    if manifest['new_product_bytes']>protocol['execution_data_budget_bytes']:raise ValueError('Stage2A output budget exceeded')
    write_json(root/'registry/B_stage2A_manifest.json',manifest)
    print(json.dumps({k:manifest[k] for k in ['verdict','counts','prediction_rows','new_product_bytes','wall_seconds','cpu_seconds','recommendations']}))
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root',type=Path,default=Path(os.environ.get('EBM_DATA_ROOT',ROOT/'data')))
    parser.add_argument('--protocol',type=Path,default=ROOT/'config/B_stage2A_linear_spline_protocol.json')
    parser.add_argument('--freeze-protocol',action='store_true')
    args=parser.parse_args()
    if args.freeze_protocol:freeze_protocol(args.data_root.resolve(),args.protocol.resolve())
    else:run(args.data_root.resolve(),args.protocol.resolve())


if __name__=='__main__':main()
