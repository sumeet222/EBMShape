"""Bounded, checkpointed, local-only C3 execution. CLI phases never acquire data."""
import argparse
import datetime as dt
import hashlib
import importlib.metadata as md
import inspect
import json
import os
from pathlib import Path
import pickle
import platform
import resource
import subprocess
import time
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingRegressor
from ..readiness import ROOT,digest,WINDOWS,transform_s0
from ..c2r_development import load_inputs,no_network,write_json,clean
from ..c2r_models import date_hash,Model
from . import models,m8_softmax

OUT=ROOT/'artifacts/C/C3_one_state_ebm_v1_1'
CONFIG=ROOT/'config/C_C3_development_protocol_v1_1.json'
REF=ROOT/'artifacts/C/C2R_development_v1_1'


def inputs():
    d=load_inputs()
    assert digest(ROOT/'config/C_C2R_development_protocol_v1_1.json')=='24ef4122ce069df7f7e228ecfc1f05b48983005273c1e84da10cfb03cdb14bca'
    for f in json.loads((REF/'files_manifest.json').read_text())['created_files']:
        if digest(ROOT/f['path'])!=f['sha256']:raise ValueError('BLOCKED_C2R_IDENTITY: '+f['path'])
    with np.load(REF/'descriptive_predictions.npz') as r:
        assert np.array_equal(d['dates'],r['dates'])
    return d


def prepare():
    """Write-once scientific freeze, after synthetic native compatibility audit."""
    if CONFIG.exists():raise FileExistsError('C3_FREEZE_EXISTS; resume, never overwrite')
    d=inputs();OUT.mkdir(parents=True,exist_ok=True)
    common=dict(max_bins=128,max_interaction_bins=96,validation_size=0,outer_bags=1,inner_bags=0,
        learning_rate=.025,greedy_ratio=0.,cyclic_progress=True,smoothing_rounds=0,
        interaction_smoothing_rounds=0,early_stopping_rounds=0,early_stopping_tolerance=1e-5,
        min_samples_leaf=25,min_hessian=0.,reg_alpha=0.,reg_lambda=0.,max_delta_step=0.,
        gain_scale=5.,min_cat_samples=10,cat_smooth=10.,missing='separate',objective='rmse',
        monotone_constraints=None,exclude=None,callback=None,n_jobs=1)
    configs={}
    for id,bins,leaves,rounds in [('A',8,2,200),('B',16,3,400)]:
        configs[id]=dict(numeric_bins=bins,kwargs=dict(common,max_leaves=leaves,max_rounds=rounds))
    folds=[]
    for year in [2018,2019]:
        tr=d['dates']<f'{year}-01-01';ev=np.char.startswith(d['dates'],str(year))
        folds.append(dict(id=f'INNER_{year}',train_end=f'{year-1}-12-31',eval_year=year,
                          train_n=int(tr.sum()),eval_n=int(ev.sum()),train_hash=date_hash(d['dates'][tr]),eval_hash=date_hash(d['dates'][ev])))
    cfg=dict(task_id='C3_ONE_STATE_EBM_COMPLETE_LADDER_SCIENTIFIC_AUDIT_v1_1',status='FROZEN_EXPLORATORY_DEVELOPMENT',
        frozen_local=dt.datetime.now(ZoneInfo('America/New_York')).isoformat(),configs=configs,
        models=models.IDS,inner_folds=folds,outer_years=[2020,2021],seeds=[42,123,2025],
        selection='equal inner-fold mean daily profile MSE; pair combined mean for M3c/M5 and M3d/M6; ties 1e-15 prefer A',
        T0_config='A',pair_selection=True,primary_comparator='M0',secondary_comparators=['M8','M4-T8-Z4','P-OLS-Z'],
        confirmatory_status='CONDITIONAL_DEVELOPMENTAL; 2020/21 previously explored',
        test_family=['M5-M3c profile','M6-M3d profile','M5-M6 profile','M5-M0 profile','M5-M3c CLOSE_C secondary'],
        block_lengths=[5,10,20],bootstrap_B=1000,bootstrap_seed=314159,HAC_lags=[5,10,20],
        support=dict(display=[30,10],basic=[50,20],strong=[100,30]),windows=WINDOWS,k0=30,
        H1_materiality=.02,H3_materiality=.05,m8_penalty=.001,m8_selection='one prespecified candidate; no score tuning',
        m8_objective='mean daily cross entropy + .001/2 sum centered b squared; standardized training Z0',
        postprocessing='NORM_ prefix: positive-part closure with uniform zero-mass fallback; distinct models',
        cohorts=dict(n_Q=1491,n_Z0=1472,n_DEV2020=241,n_DEV2021=248,date_hash=date_hash(d['dates'])),
        features=['nominal k=00..77','numeric Z0 or train-only nominal S0'],time_zone='America/New_York',
        source_definition='SPY Alpaca SIP split adjusted UTC minute starts; Q from 390 squared log returns; no overnight',
        source_refs=d['identities'],c2r_manifest_sha256=digest(REF/'files_manifest.json'),
        c2r_config_sha256=digest(ROOT/'config/C_C2R_development_protocol_v1_1.json'),
        full_C_draft_sha256=digest(ROOT/'config/C_full_protocol_v1_1.yaml'),
        authority=json.loads((ROOT/'config/C_C2R_development_protocol_v1_1.json').read_text())['authority'],
        versions={p:md.version(p) for p in ['interpret-core','scikit-learn','numpy','pandas','scipy','statsmodels','matplotlib','pyarrow']},
        python=platform.python_version(),platform=platform.platform(),signature=str(inspect.signature(ExplainableBoostingRegressor)),
        commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        budget=dict(inner_native=18,final_seed42=15,extra_seeds=16,stress=10,planned_native=59,hard_native=60,
                    compute_seconds=3600,memory_bytes=4*1024**3,retained_bytes=300*1024**2),
        stress_plan={'EXCLUDE_2020':models.IDS[1:],'DROP_TOP1_RV':models.IDS[1:],'DROP_TOP5_INFLUENTIAL':models.IDS[3:]},
        deferred=['LOYO native refits','full-learner/bootstrap selection intervals','native population CIs'],
        algorithm='fixed-round cyclic boosting; no greedy/smoothing/row validation; all unit rows equal day weight')
    write_json(CONFIG,cfg);write_json(OUT/'protocol_freeze_receipt.json',dict(sha256=digest(CONFIG),created=cfg['frozen_local']))
    print('FROZEN',digest(CONFIG),'inner folds',folds,flush=True)


def config():
    cfg=json.loads(CONFIG.read_text());receipt=json.loads((OUT/'protocol_freeze_receipt.json').read_text())
    assert digest(CONFIG)==receipt['sha256'],'C3_PROTOCOL_CHANGED'
    assert md.version('interpret-core')==cfg['versions']['interpret-core']
    return cfg


def reference_predictions(d,context,indices):
    """Use stored parameters or saved forecasts, never refit C2R models."""
    params=json.loads((REF/'model_parameters.json').read_text())[context]
    return {n:Model(n,np.asarray(m['coef']),m['metadata']).predict(d['z'][indices],params['transform'])
            for n,m in params['models'].items() if not n.startswith('OLS-') and not n.startswith('NOINT')}


def checkpoint(d,train,ev,context,name,cid,seed,cfg,start):
    """Resume only complete hash-verified model+data+protocol keys; persist each fit."""
    folder=OUT/'checkpoints';folder.mkdir(exist_ok=True)
    key=f'{context}__{name}__{cid}__{seed}';meta=folder/(key+'.json');blob=folder/(key+'.pkl')
    identity=dict(protocol=digest(CONFIG),train_hash=date_hash(d['dates'][train]),eval_hash=date_hash(d['dates'][ev]),model=name,config=cid,seed=seed)
    if meta.exists():
        record=json.loads(meta.read_text());assert record['identity']==identity and digest(blob)==record['blob_sha256']
        return pickle.loads(blob.read_bytes()),record
    count=len(list(folder.glob('*.json')))
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes=rss if platform.system()=='Darwin' else rss*1024
    elapsed=time.monotonic()-start
    retained=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
    if count>=cfg['budget']['hard_native'] or elapsed>=cfg['budget']['compute_seconds'] or rss_bytes>cfg['budget']['memory_bytes'] or retained>cfg['budget']['retained_bytes']:
        raise RuntimeError(f'RESOURCE_CAP_REACHED fits={count} elapsed={elapsed:.1f} rss={rss_bytes} bytes={retained}')
    t=models.transform(d['dates'][train],d['z'][train],cfg['configs'][cid]['numeric_bins'])
    params=models.kwargs(name,t,cfg['configs'][cid],seed);tic=time.monotonic()
    print('FIT',count+1,key,'train',sum(train),'eval',sum(ev),flush=True)
    native=ExplainableBoostingRegressor(**params).fit(models.design(d['z'][train],name,t),d['q'][train].ravel())
    audit=models.audit(native,d['z'][train],name,t)
    bundle=dict(model=native,transform=t,name=name,identity=identity)
    raw=pickle.dumps(bundle,protocol=5);temporary=blob.with_suffix('.tmp');temporary.write_bytes(raw);temporary.replace(blob)
    pred=models.predict(bundle,d['z'][ev]);loss=float(((pred-d['q'][ev])**2).mean())
    record=dict(key=key,context=context,name=name,config=cid,seed=seed,identity=identity,transform=t,
        n_train=int(sum(train)),n_eval=int(sum(ev)),eval_MSE=loss,wall_seconds=time.monotonic()-tic,
        peak_rss_bytes=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)),
        blob_sha256=digest(blob),blob_bytes=len(raw),audit=audit,code_sha256={p.name:digest(p) for p in Path(__file__).parent.glob('*.py')})
    write_json(meta,record);print('DONE',key,'MSE',loss,'seconds',record['wall_seconds'],flush=True)
    return bundle,record


def fit():
    cfg=config();d=inputs();start=time.monotonic();scores=[]
    initial_count=len(list((OUT/'checkpoints').glob('*.json')))
    for fold in cfg['inner_folds']:
        tr=d['dates']<=fold['train_end'];ev=np.char.startswith(d['dates'],str(fold['eval_year']))
        assert max(d['dates'][tr])<min(d['dates'][ev])
        for name in models.IDS:
            for cid in (['A'] if name==models.IDS[0] else ['A','B']):
                _,r=checkpoint(d,tr,ev,fold['id'],name,cid,42,cfg,start)
                scores.append(dict(fold=fold['id'],model=name,config=cid,MSE=r['eval_MSE']))
    pd.DataFrame(scores).to_csv(OUT/'inner_selection_scores.csv',index=False)
    chosen=select_configurations(scores)
    selection=dict(chosen=chosen,criterion=cfg['selection'],inner_scores=scores)
    target=OUT/'selected_configurations.json'
    if target.exists():assert json.loads(target.read_text())==selection
    else:write_json(target,selection)
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        year=int(context[-4:]) if context!='D_FULL' else None
        tr=np.ones(len(d['z']),bool) if year is None else d['dates']<f'{year}-01-01'
        ev=tr if year is None else np.char.startswith(d['dates'],str(year))
        for name in models.IDS:
            checkpoint(d,tr,ev,context,name,chosen[name],42,cfg,start)
        path=OUT/(context+'__M8.json')
        if not path.exists():write_json(path,m8_softmax.fit(d['z'][tr],d['q'][tr],cfg['m8_penalty']))
    for year in [2020,2021]:
        tr=d['dates']<f'{year}-01-01';ev=np.char.startswith(d['dates'],str(year))
        for seed in [123,2025]:
            for name in models.IDS[1:]:checkpoint(d,tr,ev,f'DEV_{year}',name,chosen[name],seed,cfg,start)
    design=pd.read_csv(REF/'daily_design_index.csv')
    print('Design columns',design.columns.tolist(),flush=True)
    for context,names in cfg['stress_plan'].items():
        tr=np.isin(d['dates'],json.loads((REF/'model_parameters.json').read_text())[context]['train_dates'])
        for name in names:checkpoint(d,tr,tr,context,name,chosen[name],42,cfg,start)
    prior=json.loads((OUT/'fit_execution.json').read_text()) if (OUT/'fit_execution.json').exists() else None
    history=[] if prior is None else prior.get('invocations',[dict(wall_seconds=prior['current_invocation_seconds'],new_native_fits=prior['native_fits'])])
    count=len(list((OUT/'checkpoints').glob('*.json')))
    history.append(dict(wall_seconds=time.monotonic()-start,new_native_fits=count-initial_count))
    write_json(OUT/'fit_execution.json',dict(status='COMPLETED',native_fits=count,invocations=history,
        current_invocation_seconds=time.monotonic()-start,network_bytes=0,selection=chosen,
        code_hashes={str(p.relative_to(ROOT)):digest(p) for p in Path(__file__).parent.glob('*.py')}))


def select_configurations(scores):
    """Frozen matched-pair criterion sees only the two named inner fold scores."""
    chosen={models.IDS[0]:'A'}
    s=pd.DataFrame(scores);s=s[s.fold.isin(['INNER_2018','INNER_2019'])]
    for pair in [(models.IDS[1],models.IDS[3]),(models.IDS[2],models.IDS[4])]:
        means=s[s.model.isin(pair)].groupby('config').MSE.mean()
        winner='A' if means['A']<=means['B']+1e-15 else 'B'
        chosen.update({name:winner for name in pair})
    return chosen


def load_bundle(context,name,seed=42):
    chosen=json.loads((OUT/'selected_configurations.json').read_text())['chosen']
    key=f'{context}__{name}__{chosen[name]}__{seed}'
    meta=json.loads((OUT/'checkpoints'/(key+'.json')).read_text());path=OUT/'checkpoints'/(key+'.pkl')
    assert digest(path)==meta['blob_sha256']
    return pickle.loads(path.read_bytes()),meta


def main():
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','fit','diagnose','report','verify']);args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    with no_network() as network:
        if args.phase=='prepare':prepare()
        elif args.phase=='fit':fit()
        else:
            from .analysis import diagnose,verify
            if args.phase=='report':
                from .reporting import report
            else:
                report=None
            {'diagnose':diagnose,'report':report,'verify':verify}[args.phase]()
        assert network['attempts']==0
    print(args.phase,'COMPLETE; network attempts',network['attempts'],flush=True)

if __name__=='__main__':main()
