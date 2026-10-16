"""Offline Stage2B: frozen native EBM ladder, training-only selection and matched validation."""
import argparse
import datetime as dt
import importlib.metadata as metadata
import inspect
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

import joblib
import numpy as np
import pandas as pd

from .pilot import ROOT, sha, write_json
from .acquisition import file_ref
from .stage2a import training_inputs, load_validation
from .ebm_models import (specifications, features, fit_native, support_screen, contrast, metrics,
                         residual_diagnostics, groups, query_frame, candidate_rows, STATES)

PROTOCOL = ROOT/'config/B_stage2B_EBM_protocol_v1.json'


def data_root():
    """Portable default shared store; external EBM_DATA_ROOT is optional."""
    return Path(os.environ.get('EBM_DATA_ROOT',ROOT/'data')).resolve()


def read_development(path,start,end,columns=None):
    """Reject forbidden windows before Arrow scientific projection, including sealed dates."""
    if not ('2016-01-05'<=start<=end<='2023-12-31'):
        raise ValueError(f'Forbidden scientific read {start}..{end}; seal starts 2024-01-01')
    filters=[('session_et','>=',dt.date.fromisoformat(start)),('session_et','<=',dt.date.fromisoformat(end)),('eligible_primary','=',True)]
    f=pd.read_parquet(path,columns=columns,filters=filters)
    if not f.session_et.astype(str).between(start,end).all():raise ValueError('Arrow date predicate failed')
    return f


def freeze(root):
    """Write once before pilot/model fit; grids use only training predictors."""
    if PROTOCOL.exists():raise ValueError('Protocol exists; verify/reuse, never overwrite')
    train,prior,stage1,counts=training_inputs(root)
    a=json.loads((ROOT/'config/B_stage2A_linear_spline_protocol.json').read_text())
    m=json.loads((root/'registry/B_stage2A_manifest.json').read_text())
    if counts!=dict(rows=2680,eligible=2675,train=1495,validation=497,sealed_test=683):
        raise ValueError(f'Frozen input counts disagree: {counts}')
    if sha(root/prior['daily']['path'])!=a['daily']['sha256']:raise ValueError('Daily hash changed')
    refs=['AGENTS.md','README.md','.gitignore','docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md',
          'docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md',
          'config/B_stage1_dataset_selection.json','config/B_stage2A_linear_spline_protocol.json',
          'reports/B/stage1_replication_benchmarks.md','reports/B/stage1_5_linear_replication_diagnostics.md',
          'reports/B/stage2A_state_linear_and_spline_results.md','docs/experiment_B_stage2A_methods_and_model_registry.md']
    p=dict(stage='B_STAGE2B_EBM_LADDER_SHAPE_FIDELITY_AND_INFERENCE_V1',version=1,
           frozen_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),dataset_id=stage1['dataset_id'],daily=prior['daily'],
           counts=counts,train=stage1['train'],validation=stage1['validation'],sealed=stage1['sealed_test'],
           symbol='SPY',timezone='America/New_York',adjustment=stage1['adjustment'],
           X='preceding scheduled full close to 10:00 simple return bp; includes overnight',
           W='15:00–15:30 simple return bp, L only',Y='15:30–16:00 signed simple return bp',
           Z='log(opening 30 one-minute RV + 1e-8)',cutoffs_raw=a['preprocessing']['cutoffs_raw'],
           z_representatives=a['preprocessing']['representatives'],categorical_ties='lower',
           categorical_validation='Original 2016–2021 thresholds fixed for all variants/refits',
           models=specifications(),settings=[dict(max_bins=32,max_interaction_bins=8,min_samples_leaf=25,learning_rate=.025),
                                            dict(max_bins=64,max_interaction_bins=16,min_samples_leaf=10,learning_rate=.025)],
           selection=dict(fit=['2016-01-05','2020-12-31'],development=['2021-01-01','2021-12-31'],
                          seed=42,bags=4,criterion='minimum 2021 MSE; exact ties lower setting index',
                          one_setting_per_family=True,external_validation_not_used=True),
           seeds=[42,123,2025,7,314159],primary_seed=42,
           effective_base=dict(objective='rmse',max_rounds=1000,early_stopping_rounds=50,early_stopping_tolerance=1e-5,
                               validation_size=.15,inner_bags=0,greedy_ratio=0.,cyclic_progress=True,
                               smoothing_rounds=100,interaction_smoothing_rounds=50,max_leaves=2,
                               min_hessian=0.,reg_alpha=0.,reg_lambda=0.,max_delta_step=0.,gain_scale=5.,
                               min_cat_samples=10,cat_smooth=10.,missing='separate',monotone_constraints=None,
                               exclude=None,callback=None,n_jobs=1),final_bags=8,
           internal_validation='Native stochastic training-only bags; not time-series evaluation or scientific CI',
           native_binning='Refit native quantile bins on each actual past training subset; cutoffs/state reps and query grid frozen. Native binning cannot freeze separate main/interaction cuts via public API; deletion sensitivities include learner bin changes.',
           quarterly_schedule=a['quarterly_schedule'],
           quarterly_policy='Use selected training-only setting, same seed, all eligible targets strictly before cutoff; original terciles frozen',
           variants=dict(DROP_TOP1=a['drop_top1'],DROP_TOP5=a['drop_top5'],EXCLUDE_2020=['2020'],MATCHED_SOURCE=a['source_exclusions']),
           sensitivities='All 11 selected families seed42 only; no repeated sensitivity quarterly fits',
           learning_rate_sensitivity=.05,clipping='none, inputs and Y unchanged',
           temporal_periods={'2016_2019':['2016-01-05','2019-12-31'],'2020':['2020-01-01','2020-12-31'],'2021':['2021-01-01','2021-12-31']},
           leave_year_out=dict(models=['A1c_E','A1c_L'],years=list(range(2016,2022))),
           support=dict(a=[10,20,30,50],h=[5,10,15],constraint='h<a',w=['zero','training_median'],
                        w_halfwidth=[5,10,20],state_neighborhood='whole frozen RV tercile, not a pointwise Z neighborhood',
                        min_n=50,min_blocks=20,strong_n=100,strong_blocks=30,
                        blocks='distinct nonoverlapping 5 eligible chronological row groups; fixed within each cohort',
                        candidate_order='a,h,w,width nested ascending; first passing; if none ABSTAIN'),
           sparse_plot=dict(x=[-50,-30,-20,-10,0,10,20,30,50],x_halfwidth=10,
                            z_quantiles=[.1,.3,.5,.7,.9],z_halfwidth=.2,w_halfwidth=20,min_n=50,min_blocks=20),
           primary_comparisons=[['A1c_E','A0c_E'],['A1c_L','A0c_L']],
           paired_inference=dict(lags=[5,10,20],primary='quarterly seed42 FULL; Holm across two E/L A1c-A0c HAC5 tests',
                                 bootstrap=dict(blocks=[5,20],B=500,seed=42),
                                 bootstrap_subset=[['A1c_E','A0c_E'],['A1c_L','A0c_L'],['A1c_E','N0'],['A1c_L','N0']],
                                 interpretation='Developmental, asymptotic fixed-prediction comparisons; no exact selected-model independent confirmation'),
           materiality=dict(shape_bp=1.,incremental_R2=.0025,rule='gain interval excludes zero and R2 gain≥.0025 vs stronger simple state-aware; additionally compare strongest naive'),
           shape_inference='Whole four-prediction D_F; no bag-SD population CI. Seed/time-window stability only, NOT_CERTIFIED; raw band means distinct from continuous pointwise m.',
           conditional_band_bootstrap=dict(blocks=[5,20],B=500,minimum_valid=450,seed=42),
           shape_pipeline_bootstrap='DEFERRED: bounded seed/time-window sensitivity, no certified fitted/raw CIs',
           full_pipeline_null='DEFERRED_TO_STAGE4: 100 shortlisted full-selection+quarter-refit replicates exceed 1h cap; future circular-block destroyed-alignment null, not RV shuffle',
           resource=dict(max_wall_seconds=3600,max_retained_bytes=100_000_000,max_single_fit_seconds=60,
                         screened=22,selected_full=55,additional_quarterly=385,sensitivities=44,temporal=33,leave_year_out=12,learning_rate=11,total_planned=662),
           environment={k:metadata.version(k) for k in ['interpret-core','scikit-learn','numpy','pandas','pyarrow','scipy','statsmodels','matplotlib','joblib']},
           git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
           inputs={r:sha(ROOT/r) for r in refs},stage2A_manifest_sha256=sha(root/'registry/B_stage2A_manifest.json'),
           stage2A_predictions=m['predictions'],no_sealed_scientific_access=True,new_market_data_requests=0,
           theory_materials='Only B spec §§2,6–8 and companion plus AGENTS and current prompt; original theorem/task/consolidation files absent from repository and ResearchSpec')
    # Pin all machine results used as references without duplicating their rows.
    p['registry_inputs']={str(f.relative_to(root)):sha(f) for f in root.glob('registry/B_stage2A*')}
    grid,rows=support_screen(train.drop(columns=['y_last30_bp']),p)
    p['contrast_grid']=grid
    p['outputs']='B_stage2B_ebm_* registries; one predictions parquet; 11 selected primary native model artifacts; 11 PNG; reports and session'
    write_json(PROTOCOL,p)
    write_json(root/'registry/B_stage2B_ebm_contrast_grid.json',dict(protocol_sha256=sha(PROTOCOL),grid=grid))
    pd.DataFrame(rows).to_csv(root/'registry/B_stage2B_ebm_support.csv',index=False)
    print(json.dumps(dict(action='FROZEN',protocol_sha256=sha(PROTOCOL),counts=counts,
                          support={i:g['status'] for i,g in grid.items()})),flush=True)


def verify(root,p):
    """Verify immutable input identities before fitting/resuming."""
    for f,d in p['inputs'].items():
        if sha(ROOT/f)!=d:raise ValueError(f'Frozen input changed: {f}')
    for f,d in p['registry_inputs'].items():
        if sha(root/f)!=d:raise ValueError(f'Stage2A result changed: {f}')
    for ref in [p['daily'],p['stage2A_predictions']]:
        if sha(root/ref['path'])!=ref['sha256']:raise ValueError(f'Input changed {ref["path"]}')
    for k,v in p['environment'].items():
        if metadata.version(k)!=v:raise ValueError(f'Environment drift {k}')


def pilot(root,p):
    """Small actual training fit with no external validation or sealed rows."""
    verify(root,p)
    f=read_development(root/p['daily']['path'],'2016-01-05','2016-12-31').head(100)
    s=next(s for s in p['models'] if s['model_id']=='A1c_L')
    model,meta=fit_native(f,s,p,p['settings'][0],42,'2017-01-01',bags=4)
    out=dict(meta,protocol_sha256=sha(PROTOCOL),purpose='100-row real-data runtime/API pilot, no model selection',
             planned_fit_count=p['resource']['total_planned'],projected_seconds=meta['fit_seconds']*p['resource']['total_planned']*20,
             estimate_note='Conservative 20× small-fit multiplier; enforce actual wall and per-fit cap')
    write_json(root/'registry/B_stage2B_ebm_pilot.json',out)
    print(json.dumps({k:out[k] for k in ['fit_seconds','planned_fit_count','projected_seconds']}),flush=True)


def run(root,p):
    """Checkpoint the bounded fixed design; quarterly fits never select using future labels."""
    verify(root,p);wall=time.perf_counter();cpu=time.process_time();free=shutil.disk_usage(root).free
    train=read_development(root/p['daily']['path'],*p['train'])
    val=read_development(root/p['daily']['path'],*p['validation'])
    if (len(train),len(val))!=(1495,497):raise ValueError('Training/validation keys changed')
    allpast=pd.concat([train,val],ignore_index=True)
    n1train=np.r_[0.,np.cumsum(train.y_last30_bp.to_numpy())[:-1]/np.arange(1,len(train))]
    n1val=(train.y_last30_bp.sum()+np.r_[0.,np.cumsum(val.y_last30_bp.to_numpy())[:-1]])/(len(train)+np.arange(len(val)))
    checkpoint=ROOT/'logs/stage2B_checkpoint.json';checkpoint.parent.mkdir(exist_ok=True)
    code_hash={str(f.relative_to(ROOT)):sha(f) for f in (ROOT/'src/ebm_research/experiment_b').glob('*2b*.py')}
    code_hash['src/ebm_research/experiment_b/ebm_models.py']=sha(ROOT/'src/ebm_research/experiment_b/ebm_models.py')
    identity=dict(protocol=sha(PROTOCOL),code=code_hash)
    state=json.loads(checkpoint.read_text()) if checkpoint.exists() else dict(identity=identity,runs={},selected={},resources=[])
    if state['identity']!=identity:raise ValueError('Checkpoint code/protocol identity differs; preserve and inspect before resuming')
    modeldir=ROOT/'artifacts/B/checkpoints/stage2B';modeldir.mkdir(parents=True,exist_ok=True)
    primary={}; grid=p['contrast_grid']

    def perform(frame,spec,setting_idx,seed,variant,mode,asof,evaluation,cohort='validation',bags=8,lr=None):
        fid=f'{spec["model_id"]}__c{setting_idx}__s{seed}__{variant}__{mode}__{asof}'
        if fid in state['runs']:
            rec=state['runs'][fid]
            if rec['meta']['status']!='PASS':raise RuntimeError(f'Previously failed checkpoint {fid}')
            if mode=='fixed' and variant=='FULL' and seed==42:
                primary[spec['model_id']]=joblib.load(modeldir/(spec['model_id']+'.joblib'))
            return rec
        if time.perf_counter()-wall>p['resource']['max_wall_seconds']:raise RuntimeError('Wall budget exceeded; checkpoint retained')
        setting=dict(p['settings'][setting_idx])
        if lr is not None:setting['learning_rate']=lr
        try:
            model,meta=fit_native(frame,spec,p,setting,seed,asof,bags)
        except Exception as error:
            state['runs'][fid]=dict(meta=dict(fit_id=fid,model_id=spec['model_id'],status='FAILED',error=repr(error)))
            write_json(checkpoint,state);raise
        keys=dict(fit_id=fid,model_id=spec['model_id'],family=spec['family'],info=spec['info'],seed=seed,
                  setting=setting_idx,variant=variant,mode=mode)
        meta.update(keys,status='PASS',native_binning_policy=p['native_binning'])
        tp=model.predict(features(frame,spec,p));vp=model.predict(features(evaluation,spec,p))
        # N1 is always past-only; subset diagnostics use original chronology reference.
        nmap=pd.Series(np.r_[n1train,n1val],index=allpast.session_et)
        tm=metrics(frame,tp,nmap.loc[frame.session_et].to_numpy(),**keys,cohort='train')
        vm=metrics(evaluation,vp,nmap.loc[evaluation.session_et].to_numpy(),**keys,cohort=cohort)
        diag=residual_diagnostics(frame,tp,p,**keys,cohort='train')
        diag+=residual_diagnostics(evaluation,vp,p,**keys,cohort=cohort)
        shape=dict(keys,**contrast(model,spec,p,grid))
        # One reusable sparse total-surface table for every fit; scientific masks derive only from predictors.
        surfaces=[]
        c=grid[spec['info']]['display_candidate']
        for state_index,z in enumerate(p['z_representatives']):
            xs=np.asarray(p['sparse_plot']['x'],dtype=float)
            q=query_frame(xs,z,c['w']);fp=model.predict(features(q,spec,p))
            for x,forecast in zip(xs,fp):
                mask=(groups(frame,p)==state_index)&(abs(frame.x_open_bp.to_numpy()-x)<=10)
                if spec['info']=='L':mask &= abs(frame.w_preclose_bp.to_numpy()-c['w'])<=20
                n=int(mask.sum());blocks=int(np.unique((np.arange(len(frame))//5)[mask]).size)
                surfaces.append(dict(keys,state=STATES[state_index],z=z,x=float(x),w=c['w'],forecast=float(forecast),n=n,blocks=blocks,supported=n>=50 and blocks>=20))
        importance=[dict(keys,term=term,importance=float(imp),score_min=ra[0],score_max=ra[1],
                         nonempty_bins=nb,sparse_bins=sp) for term,imp,ra,nb,sp in zip(meta['term_names'],meta['term_importances'],meta['term_ranges'],meta['nonempty_bins'],meta['sparse_occupied_bins'])]
        rec=dict(meta=meta,training_metric=tm,validation_metric=vm,diagnostics=diag,shape=shape,
                 eval_dates=evaluation.session_et.astype(str).tolist(),predictions=vp.tolist(),
                 train_dates=frame.session_et.astype(str).tolist(),train_predictions=tp.tolist(),
                 surfaces=surfaces,importance=importance)
        if mode=='fixed' and variant=='FULL' and seed==42:
            artifact=modeldir/(spec['model_id']+'.joblib');joblib.dump(model,artifact,compress=3)
            reloaded=joblib.load(artifact)
            np.testing.assert_allclose(reloaded.predict(features(evaluation.head(8),spec,p)),vp[:8],atol=1e-12,rtol=0)
            meta['model_artifact']=file_ref(artifact,ROOT);primary[spec['model_id']]=model
        state['runs'][fid]=rec
        write_json(checkpoint,state)
        if meta['fit_seconds']>p['resource']['max_single_fit_seconds']:raise RuntimeError('Single fit exceeded budget; successful fit checkpointed')
        return rec

    # Training-only, chronologically later 2021 selects the setting once per family.
    screen_fit=train.loc[train.session_et.astype(str).le('2020-12-31')]
    screen_eval=train.loc[train.session_et.astype(str).ge('2021-01-01')]
    for s in p['models']:
        candidates=[perform(screen_fit,s,i,42,'FULL','screen','2021-01-01',screen_eval,'development',4) for i in range(2)]
        chosen=min(range(2),key=lambda i:(candidates[i]['validation_metric']['MSE'],i))
        state['selected'][s['model_id']]=chosen
        for seed in p['seeds']:
            full=perform(train,s,chosen,seed,'FULL','fixed','2022-01-01',val)
            for cutoff in p['quarterly_schedule']:
                # Jan2022 is the identical fixed fit; reuse its forecast prefix by reference.
                if cutoff=='2022-01-01':continue
                end=(pd.Timestamp(cutoff)+pd.DateOffset(months=3)).strftime('%Y-%m-%d')
                h=allpast.loc[allpast.session_et.astype(str).lt(cutoff)]
                v=val.loc[val.session_et.astype(str).ge(cutoff)&val.session_et.astype(str).lt(end)]
                perform(h,s,chosen,seed,'FULL','quarterly',cutoff,v)
        for variant,dates in p['variants'].items():
            mask=~train.session_et.astype(str).isin(dates) if variant!='EXCLUDE_2020' else ~train.session_et.astype(str).str.startswith('2020')
            perform(train.loc[mask],s,chosen,42,variant,'fixed','2022-01-01',val)
        perform(train,s,chosen,42,'LR_005','fixed','2022-01-01',val,lr=.05)
        for label,bounds in p['temporal_periods'].items():
            sub=train.loc[train.session_et.astype(str).between(*bounds)]
            perform(sub,s,chosen,42,label,'temporal','2022-01-01',val)
        if s['model_id'] in p['leave_year_out']['models']:
            for year in p['leave_year_out']['years']:
                sub=train.loc[~train.session_et.astype(str).str.startswith(str(year))]
                perform(sub,s,chosen,42,f'LEAVE_{year}','temporal','2022-01-01',val)
        print(json.dumps(dict(family=s['model_id'],selected_setting=chosen,completed_fits=len(state['runs']),elapsed=time.perf_counter()-wall)),flush=True)
    state['resources'].append(dict(wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                                   free_before=free,free_after=shutil.disk_usage(root).free))
    write_json(checkpoint,state)
    from .stage2b_results import publish
    publish(root,p,state,primary,train,val,n1train,n1val)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['freeze','pilot','run','publish'])
    args=parser.parse_args();root=data_root()
    if args.action=='freeze':freeze(root);return
    p=json.loads(PROTOCOL.read_text())
    if args.action=='pilot':pilot(root,p)
    elif args.action=='run':run(root,p)
    else:
        from .stage2b_results import publish_cached
        publish_cached(root,p)


if __name__=='__main__':main()
