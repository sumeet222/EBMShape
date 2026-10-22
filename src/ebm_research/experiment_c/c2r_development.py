"""C2R Z0-only development execution. No 2022+ scientific reads or network."""
import argparse
from contextlib import contextmanager
import datetime as dt
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import time
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

from .readiness import ROOT, P0, AUTHORITY, WINDOWS, digest, safe_path, calendar, transform_s0
from .c2r_models import (SCALAR_IDS, PROFILE_IDS, Model, fit_models, date_hash,
                         scalar_design, profile_losses, calendar_hac)
from .c2r_diagnostics import (scalar_diagnostics, profile_diagnostics, block_weights,
                              influence_arrays, linear_contrast, holm_family, series_diagnostics)

OUT=ROOT/'artifacts/C/C2R_development_v1_1'
CONFIG=ROOT/'config/C_C2R_development_protocol_v1_1.json'
PINS={
    AUTHORITY[0]:'d402d316e5bf37c43169091cf7377c5bc170a0c74626f51135ac51350cf8c57b',
    AUTHORITY[1]:'072871e0bdacd28324afa4ac4d8d73389b383e2e8c448477059ac94b9dd66ce7',
    AUTHORITY[2]:'5fa9fc0dba2d4dd31c6be6fa7ce226b27ffedf395f252a7116a30bf0fce3fd3e',
    str(P0/'daily_profiles.npz'):'2aa2554accde6cfeaadeb5b539b52931f76c1470cdb3a435eefef2e804de0c27',
    str(P0/'source_manifest.json'):'a63fe1d6314054240d8b2ac488922a8021f85d55434bfd49001298f5d5e4ff99'}


def clean(value):
    if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
    if isinstance(value,(tuple,list,np.ndarray)):return [clean(v) for v in value]
    if isinstance(value,np.generic):value=value.item()
    if isinstance(value,float) and not np.isfinite(value):return None
    return value


def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(clean(value),indent=2,allow_nan=False)+'\n')


@contextmanager
def no_network():
    """Reject attempted socket connections during local C2R execution."""
    original=socket.socket.connect
    count={'attempts':0}
    def blocked(*args,**kwargs):
        count['attempts']+=1
        raise RuntimeError('C2R_NETWORK_FORBIDDEN')
    socket.socket.connect=blocked
    try:yield count
    finally:socket.socket.connect=original


def load_inputs():
    """Hash references, then load only the pinned 2016–2021 Q and state table."""
    data=Path(os.environ.get('EBM_DATA_ROOT') or ROOT/'data').expanduser()
    if data.is_symlink():raise ValueError('C2R_SYMLINK_DATA_ROOT')
    data=data.resolve(); identities=[]; ledger=[]
    for rel,expected in PINS.items():
        path=safe_path(ROOT,rel);actual=digest(path)
        if actual!=expected:raise ValueError(f'BLOCKED_SOURCE_IDENTITY: {rel}')
        identities.append(dict(root='repo',path=rel,sha256=actual,bytes=path.stat().st_size))
    r=json.loads(safe_path(ROOT,'data/registry/C_preliminary_RV_profile_v1_1.json').read_text())
    source=json.loads(safe_path(ROOT,P0/'source_manifest.json').read_text())
    c1=json.loads(safe_path(ROOT,'artifacts/C/C1R/C1R_execution_QA.json').read_text())
    state_ref=c1['numeric_state_table']
    state_path=safe_path(data,'derived/C/c_development_states_v1_1.parquet')
    if digest(state_path)!=state_ref['sha256']:raise ValueError('BLOCKED_SOURCE_IDENTITY: C1R states')
    identities.append(dict(root='data',path='derived/C/c_development_states_v1_1.parquet',sha256=digest(state_path),bytes=state_path.stat().st_size))
    refs=r['base_sources']+[e['supplement'] for e in source['months'].values()]
    assert len(refs)==78
    for ref in refs:
        path=safe_path(data,ref['path'])
        if digest(path)!=ref['sha256'] or path.stat().st_size!=ref['bytes']:
            raise ValueError('BLOCKED_SOURCE_IDENTITY: '+ref['path'])
        identities.append(dict(root='data',**ref))
    ledger.append(dict(operation='digest_only_no_decode',paths=[r['path'] for r in refs],date_scope='2016..2021 source refs only'))
    with np.load(ROOT/P0/'daily_profiles.npz',allow_pickle=False) as f:
        z={key:f[key] for key in f.files}
    if min(z['dates'])<'2016-01-04' or max(z['dates'])>'2021-12-31':raise ValueError('C2R_FORBIDDEN_DATES')
    ledger.append(dict(path=str(P0/'daily_profiles.npz'),operation='npz',columns=list(z),dates=['2016-01-04','2021-12-31']))
    state_columns=['date_et','predecessor_et','Z0','Z0_reason']
    s=pd.read_parquet(state_path,columns=state_columns).set_index('date_et')
    ledger.append(dict(path='derived/C/c_development_states_v1_1.parquet',operation='parquet',columns=state_columns,dates=['2016-01-05','2021-12-31']))
    dates=z['dates']; qvalid=np.isfinite(z['q']).all(axis=1)&(dates>='2016-01-05')
    assert qvalid.sum()==1491 and len(set(dates))==len(dates) and np.all(dates[1:]>dates[:-1])
    assert set(s.index)==set(dates[qvalid]) and s.index.is_unique
    q=z['q'][qvalid]
    assert (q>=0).all() and np.isfinite(z['RV_day'][qvalid]).all() and (z['RV_day'][qvalid]>0).all()
    np.testing.assert_allclose(q.sum(axis=1),1,atol=1e-10,rtol=0)
    np.testing.assert_allclose(q,z['rv'][qvalid]/z['RV_day'][qvalid,None],atol=1e-10,rtol=0)
    match=qvalid.copy();match[qvalid]=s.loc[dates[qvalid],'Z0'].notna().to_numpy()
    assert match.sum()==1472
    ix=np.flatnonzero(match); d=dates[ix]; state=s.loc[d,'Z0'].to_numpy()
    np.testing.assert_allclose(np.exp(state),z['RV_prev'][ix],atol=1e-18,rtol=1e-12)
    cal=calendar('2016-01-04','2021-12-31');lookup={str(day):i for i,day in enumerate(dates)}
    for day in d:
        prev=str(cal.previous_session(str(day)).date());p=lookup[prev]
        assert prev==s.loc[day,'predecessor_et'] and len(cal.session_minutes(prev))==390
        assert np.isfinite(z['q'][p]).all() and z['RV_day'][p]>0
    for a,b in WINDOWS.values():
        np.testing.assert_allclose(z['q'][ix,a:b].sum(axis=1),
                                   np.cumsum(z['q'][ix],axis=1)[:,b-1]-(np.cumsum(z['q'][ix],axis=1)[:,a-1] if a else 0),atol=1e-10,rtol=0)
    labels=z['prev_labels'][ix]
    h1=float(z['q'][ix[labels==2],66:78].sum(axis=1).mean()-z['q'][ix[labels==0],66:78].sum(axis=1).mean())
    historical=pd.read_csv(ROOT/P0/'window_shares_by_state.csv')
    ref=historical[(historical.branch=='PREV')&(historical['mode']=='whole')&(historical.variant=='FULL')&(historical.window=='C_SPEC_CLOSE')&(historical.state=='high-minus-low')].iloc[0]
    np.testing.assert_allclose(h1,float(ref.summary),atol=1e-10,rtol=0)
    assert abs(h1*100-2.005)<.001
    return dict(dates=d,z=state,q=z['q'][ix],R=z['RV_day'][ix],labels=labels,slots=ix,
                source_arrays=z,source_ix=ix,identities=identities,read_ledger=ledger,
                P0_H1=h1,historical=historical,dataset_id=r['dataset_id'],data_root=data)


def prepare():
    """Write the C2R-only pre-fit protocol, never mutate the full-C draft."""
    if CONFIG.exists():raise FileExistsError('C2R protocol exists; inspect it rather than overwrite')
    with no_network():d=load_inputs()
    versions={x:importlib.metadata.version(x) for x in ['numpy','pandas','scipy','statsmodels','patsy','matplotlib','pillow','exchange-calendars']}
    code={p.name:digest(p) for p in Path(__file__).parent.glob('c2r_*.py')}
    origins=[dict(id='DEV_2020',train_end='2019-12-31',eval_year=2020),dict(id='DEV_2021',train_end='2020-12-31',eval_year=2021)]
    config=dict(task_id='C2R_DEVELOPMENT_v1_1',status='C2R_EXPLORATORY_DEVELOPMENT_FROZEN',
        frozen_local=dt.datetime.now(ZoneInfo('America/New_York')).isoformat(),
        repo_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        authority=[dict(path=p,sha256=digest(ROOT/p)) for p in AUTHORITY],pins=PINS,
        C1R_draft_sha256=digest(ROOT/'config/C_full_protocol_v1_1.yaml'),
        code_at_freeze=code,versions=versions,python=platform.python_version(),
        dataset_id=d['dataset_id'],source_refs=d['identities'],cohort_date_hash=date_hash(d['dates']),
        date_range=['2016-01-05','2021-12-31'],n_Q=1491,n_Z0=1472,
        date_keys=d['dates'].tolist(),response='original day-normalized Q_78; no overnight, split-only SPY',
        windows=WINDOWS,primary_window='CLOSE_C',k0=30,
        features=['Z0=log(R of immediate scheduled valid ordinary predecessor)','deterministic bin k'],
        prohibited_features=['RV_open','R_current','signed return','Zchg','Zret','Zvol','VIX','FOMC'],
        modes={'D_FULL':'all explored 1472 days, descriptive fit and retrospective P0 reference',
               'DEV_CHRONO':'two past-only development-era backchecks; previously explored, not independent validation'},
        origins=origins,scaling='training mean and population SD (ddof=0)',
        S0='C1R fit_s0 linear empirical terciles; boundary ties upper; origin training only',
        P0_labels='D_ONLY fixed-rank reference; not reused for chronological model categories',
        models={'scalar':{name:formula for name,formula in zip(SCALAR_IDS,
            ['1','1+z_s','1+I_mid+I_high','1+z_s+I_mid+I_high+z_s:I_mid+z_s:I_high','1+z_s+z_s^2'])},
            'profile':PROFILE_IDS,'P-OLS-TIME':'algebraic alias of M0, no duplicate fit',
            'P-OLS-Z':'time-specific intercept and numerical state slope; 2x78 multioutput OLS',
            'M2':'cubic clamped uniform B-spline at k0..77; 8 primary,12 sensitivity; intercept in spline span',
            'M4':'nonredundant Bz(4) x Btime(8 or12) tensor; unpenalized full-rank least squares',
            'state_basis':'four natural cardinal cubic knots at train min,1/3,2/3,max of standardized Z0; linear extrapolation',
            'ablation':'same time/state bases, centered additive main effects, no tensor; not EBM M3',
            'penalty':0.,'rank_failure':'ABSTAIN, no p-values; stop affected core path',
            'max_condition':1e10,'postprocessing':'NONE; raw output mandatory, no clipping, M8 not fitted'},
        support={'display':[30,10],'basic':[50,20],'strong':[100,30],
                 'blocks':'distinct original scheduled-session index//5 groups, not independent units',
                 'M1_fallback':'M0 if any applicable train cell fails basic gate; flag dates',
                 'continuous_bins':5,'grid_quantiles':[.1,.25,.5,.75,.9],
                 'grid_local_support':'training quantile rank band +/-0.1; display gate'},
        sensitivity={'FULL':'primary unchanged','DROP_TOP1_RV':'ceil(.01*N) highest current R, date tie-break; D-only',
            'EXCLUDE_2020':'D-only calendar shift','DROP_TOP5_INFLUENTIAL':'five highest Cook values from D_FULL OLS-L1, date tie-break; shared keys',
            'LEAVE_ONE_YEAR_OUT':[2016,2017,2018,2019,2020,2021],
            'transform_policy':'refit training scalers/knots/cuts per changed training cohort; raw reference keeps P0 labels',
            'contexts':12,'fits_per_context':14,'no_adaptive_expansion':True},
        inference={'lags':[5,10,20],'HAC':'Bartlett calendar-score NW; n/(n-p); normal coefficient intervals; missing slots zero scores only',
            'block_lengths':[5,10,20],'B':1000,'seed':42,'bootstrap':'joint circular scheduled-date slots; fixed labels/forecasts, no learner refit',
            'P0_intervals':'reuse matching fixed-label block5/10 windows; new direct20 only',
            'paired_comparisons':['M1-M0','P-OLS-Z-M0','M4-T8-Z4-M0','M4-T8-Z4-M2-T8','M4-T8-Z4-P-OLS-Z','M4-T12-Z4-M4-T8-Z4'],
            'paired_metrics':['profile_mse','close_mse'],'paired_scope':'each 2020/2021 year and pooled matched fixed forecasts; HAC and blocks 5/10/20',
            'finite_primary_family_lag':10,'finite_primary_family':['L1 slope','L2 levels','L3 slope interactions','L4 curvature','raw H1>0','raw H1>0.02'],
            'adjustment':'Holm within this six-member D_FULL exploratory family only; not protection from prior P0 selection',
            'diagnostics':'OLS reference tests heuristic under dependence; no flattened-bin IID inference',
            'certification':'NONE; no theorem or raw pointwise population confidence event'},
        influence_thresholds={'hat':'2p/n','Cook':'4/n','external_student':3,'DFFITS':'2*sqrt(p/n)','DFBETAS':'2/sqrt(n)'},
        environments=['2016-2019','2020','2021'],environment_reweighting='NONE; same training-defined quintile cells only',
        last_bin_diagnostic='leave 15:55 bin out of closing numerator without renormalizing; changed estimand',
        announcement_diagnostic='k54:56 (14:00..14:10) post-P0 exploratory; no event calendar claim',
        materiality={'closing_pp':2.,'profile_TV':.05,'status':'NOT_CERTIFIED'},
        full_C_split_population='PENDING_APPROVAL',full_C_official_dates=None,reserved_evaluation='NOT_AUTHORIZED',
        deferred={'H2_Zret':'DEFERRED_DEFINITION','Zvol':'DEFERRED_DEFINITION','Zchg':'INVENTORY_ONLY','VIX_FOMC':'ABSENT_NOT_AUTHORIZED'},
        network_bytes=0,new_source_bytes=0,retained_nonfigure_target_bytes=100_000_000,
        output_directory=str(OUT.relative_to(ROOT)))
    write_json(CONFIG,config)
    print('C2R_PRE_FIT_FROZEN',digest(CONFIG),len(d['dates']),'days; no scientific model fit')


def save_csv(name,rows):
    pd.DataFrame(rows).to_csv(OUT/(name+'.csv'),index=False,float_format='%.17g')


def support_row(context,group,mask,d,labels,origin):
    n=int(mask.sum());blocks=len(set(d['slots'][mask]//5))
    return dict(context=context,group=str(group),n_days=n,five_session_groups=blocks,
        display_ok=n>=30 and blocks>=10,basic_ok=n>=50 and blocks>=20,strong_ok=n>=100 and blocks>=30,
        Z0_mean=float(d['z'][mask].mean()) if n else np.nan,
        Z0_min=float(d['z'][mask].min()) if n else np.nan,Z0_max=float(d['z'][mask].max()) if n else np.nan,
        close_mean=float(d['q'][mask,66:78].sum(axis=1).mean()) if n else np.nan,
        close_sd=float(d['q'][mask,66:78].sum(axis=1).std(ddof=1)) if n>1 else np.nan,
        R_mean_context_only=float(d['R'][mask].mean()) if n else np.nan,label_origin=origin)


def metrics(q,pred,name,context,part,kind):
    close=q[:,66:78].sum(axis=1)
    if kind=='scalar':
        e=close-pred
        return dict(context=context,part=part,model=name,kind=kind,n_days=len(q),
            CLOSE_C_MSE=float(np.mean(e**2)),CLOSE_C_RMSE_pp=float(np.sqrt(np.mean(e**2))*100),CLOSE_C_MAE_pp=float(np.mean(abs(e))*100))
    loss=profile_losses(q,pred);e=close-pred[:,66:78].sum(axis=1)
    return dict(context=context,part=part,model=name,kind=kind,n_days=len(q),MSE_profile=float(loss['mse'].mean()),
        MAE_profile=float(loss['mae'].mean()),raw_half_L1=float(loss['half_l1'].mean()),
        TV_prediction=float(np.nanmean(loss['tv'])) if np.isfinite(loss['tv']).any() else np.nan,
        TV_valid_n=int(loss['simplex_valid'].sum()),CLOSE_C_MSE=float(np.mean(e**2)),
        CLOSE_C_RMSE_pp=float(np.sqrt(np.mean(e**2))*100),CLOSE_C_MAE_pp=float(np.mean(abs(e))*100))


def run():
    start=time.perf_counter()
    if not CONFIG.exists():raise RuntimeError('C2R_PREPARE_REQUIRED_BEFORE_FIT')
    cfg=json.loads(CONFIG.read_text())
    for name,h in cfg['code_at_freeze'].items():
        if digest(Path(__file__).parent/name)!=h:raise ValueError('C2R_CODE_CHANGED_AFTER_FREEZE: '+name)
    if digest(ROOT/'config/C_full_protocol_v1_1.yaml')!=cfg['C1R_draft_sha256']:raise ValueError('C1R_DRAFT_CHANGED')
    with no_network() as network:
        d=load_inputs();dates,z,q,slots=d['dates'],d['z'],d['q'],d['slots']
        assert date_hash(dates)==cfg['cohort_date_hash']
        OUT.mkdir(parents=True,exist_ok=True)
        registry=[];parameters={};scores=[];coeff=[];residual=[];scalar_summaries=[];tests=[];scalar_contrasts=[];features=[];serial=[]
        profiles=[];bin_stats=[];daily_stats=[];fidelity=[];contrast=[];support=[];direct=[];window_rows=[];sensitivity_rows=[];spectra={};covariances={}
        contexts=[('D_FULL',np.ones(len(z),bool),np.ones(len(z),bool),'DESCRIPTIVE')]
        for origin in cfg['origins']:
            contexts.append((origin['id'],dates<=origin['train_end'],np.char.startswith(dates,str(origin['eval_year'])),'PAST_ONLY_DEVELOPMENT'))
        primary_models,primary_transform=fit_models(dates,z,q,slots)
        cooks=influence_arrays(primary_models['OLS-L1'].training_fit)['cooks']
        cook_order=np.lexsort((dates,-cooks));top5=cook_order[:5]
        rv_order=np.lexsort((dates,-d['R']));top1=rv_order[:int(np.ceil(.01*len(z)))]
        drop_rules={'DROP_TOP1_RV':~np.isin(np.arange(len(z)),top1),'EXCLUDE_2020':~np.char.startswith(dates,'2020'),
                    'DROP_TOP5_INFLUENTIAL':~np.isin(np.arange(len(z)),top5)}
        for name,mask in drop_rules.items():contexts.append((name,mask,mask,'RETROSPECTIVE_SENSITIVITY'))
        for year in range(2016,2022):
            test=np.char.startswith(dates,str(year));contexts.append((f'LOYO_{year}',~test,test,'LEAVE_YEAR_OUT_NOT_WALK_FORWARD'))
        assert len(contexts)==12
        chrono={name:[] for name in PROFILE_IDS+SCALAR_IDS};chrono_ix=[];chrono_context=[]
        d_full_predictions={};context_transforms={};plot_arrays={}
        for context,train,ev,mode in contexts:
            tick=time.perf_counter()
            models,transform=(primary_models,primary_transform) if context=='D_FULL' else fit_models(dates[train],z[train],q[train],slots[train])
            if mode=='PAST_ONLY_DEVELOPMENT':assert max(dates[train])<min(dates[ev])
            context_transforms[context]=transform
            train_labels=transform_s0(z[train],transform['S0']);eval_labels=transform_s0(z[ev],transform['S0'])
            parameters[context]=dict(mode=mode,transform=transform,train_dates=dates[train].tolist(),forecast_dates=dates[ev].tolist(),
                train_date_hash=date_hash(dates[train]),forecast_date_hash=date_hash(dates[ev]),models={})
            for g in range(3):
                support.append(support_row(context+'_TRAIN',g,train&(transform_s0(z,transform['S0'])==g),d,None,'origin training S0'))
                support.append(support_row(context+'_EVAL',g,ev&(transform_s0(z,transform['S0'])==g),d,None,'origin training S0'))
            for g in range(3):
                raw=q[train][train_labels==g].mean(axis=0)
                for k,v in enumerate(raw):direct.append(dict(context=context,label='ORIGIN_TRAIN_S0',state=g,bin=k,mean=v,n=int((train_labels==g).sum())))
            for name,model in models.items():
                kind='scalar' if name in SCALAR_IDS else 'profile'
                pred_train=model.predict(z[train],transform);pred_eval=model.predict(z[ev],transform)
                parameters[context]['models'][name]=dict(coef=model.coef,metadata=model.metadata)
                registry.append(dict(context=context,mode=mode,model=name,kind=kind,**{k:v for k,v in model.metadata.items() if k in ['rank','edf','condition','n_days']},
                    train_first=str(min(dates[train])),train_last=str(max(dates[train])),eval_first=str(min(dates[ev])),eval_last=str(max(dates[ev])),
                    train_n=int(train.sum()),eval_n=int(ev.sum()),train_date_hash=date_hash(dates[train]),forecast_date_hash=date_hash(dates[ev]),
                    out_of_training_range_eval_n=int(((z[ev]<min(z[train]))|(z[ev]>max(z[train]))).sum()),
                    unsupported_M1_eval_n=int(sum((eval_labels==g).sum() for g in range(3) if name=='M1' and not model.metadata['supported_groups'][g])),
                    coefficient_path='model_parameters.json',status='FITTED_RAW_NO_PROJECTION'))
                scores.append(metrics(q[train],pred_train,name,context,'TRAIN',kind))
                scores.append(metrics(q[ev],pred_eval,name,context,'EVAL',kind))
                if mode=='PAST_ONLY_DEVELOPMENT':chrono[name].append(pred_eval)
                if context=='D_FULL':d_full_predictions[name]=pred_eval
                if name=='M0':
                    np.testing.assert_allclose(pred_eval[:,66:78].sum(axis=1),models['OLS-L0'].predict(z[ev],transform),atol=1e-12)
                if name=='P-OLS-Z':
                    np.testing.assert_allclose(pred_eval[:,66:78].sum(axis=1),models['OLS-L1'].predict(z[ev],transform),atol=1e-12)
                if context in ['D_FULL','DEV_2020','DEV_2021'] and kind=='scalar':
                    diag=scalar_diagnostics(model,transform,dates[train],z[train],q[train],slots[train],context)
                    scalar_summaries.append(diag['summary']);coeff.extend(diag['coef']);tests.extend(diag['tests']);scalar_contrasts.extend(diag['contrasts'])
                    residual.extend(diag['influence']);features.extend(diag['features']);serial.extend(diag['serial'])
                    if context=='D_FULL' and name=='OLS-L1':
                        for key,value in diag['serial_curves'].items():plot_arrays['scalar_'+key]=value
                if context in ['D_FULL','DEV_2020','DEV_2021'] and kind=='profile':
                    parts=[('TRAIN',train,pred_train)] if context=='D_FULL' else [('TRAIN',train,pred_train),('EVAL',ev,pred_eval)]
                    for part,mask,pred in parts:
                        pdg,bs,ds,sr,eg,cov=profile_diagnostics(q[mask],pred,dates[mask],z[mask],transform_s0(z[mask],transform['S0']),model,context,part,slots[mask])
                        profiles.append(pdg);bin_stats.extend(bs);daily_stats.extend(ds);serial.extend(sr)
                        spectra[f'{context}__{part}__{name}']=eg
                        if context=='D_FULL':covariances[name]=cov
                # Scientific comparisons use exactly the same observed P0
                # coarse cells, averaging complete model predictions per cell.
                if mode!='PAST_ONLY_DEVELOPMENT' and kind=='profile':
                    mask=ev; labels=d['labels'][mask];pred=pred_eval
                    means=[];rawmeans=[]
                    for g in range(3):
                        cell=labels==g;means.append(pred[cell].mean(axis=0));rawmeans.append(q[mask][cell].mean(axis=0))
                        if context=='D_FULL':
                            for k in range(78):fidelity.append(dict(context=context,model=name,cell_type='P0_RETROSPECTIVE_S0',cell=g,bin=k,n=int(cell.sum()),
                                raw_mean=rawmeans[-1][k],fitted_mean=means[-1][k],fitted_minus_raw=means[-1][k]-rawmeans[-1][k]))
                    delta=means[2]-means[0];rawdelta=rawmeans[2]-rawmeans[0]
                    science_ok=all(int((labels==g).sum())>=50 and len(set(slots[mask][labels==g]//5))>=20 for g in [0,2])
                    for win,(a,b) in WINDOWS.items():contrast.append(dict(context=context,model=name,window=win,n_days=int(mask.sum()),
                        estimate_pp=float(delta[a:b].sum()*100) if science_ok else np.nan,raw_pp=float(rawdelta[a:b].sum()*100) if science_ok else np.nan,
                        difference_pp=float((delta[a:b]-rawdelta[a:b]).sum()*100) if science_ok else np.nan,
                        support_status='SUPPORTED_COARSE_CELLS' if science_ok else 'ABSTAIN_SUPPORT',
                        definition='P0-cell means of whole fitted predictions on same observed rows',materiality='NOT_CERTIFIED'))
                    contrast.append(dict(context=context,model=name,window='TV_HL',n_days=int(mask.sum()),estimate_pp=np.nan,
                        TV=float(abs(delta).sum()/2) if science_ok else np.nan,raw_TV=float(abs(rawdelta).sum()/2) if science_ok else np.nan,
                        support_status='SUPPORTED_COARSE_CELLS' if science_ok else 'ABSTAIN_SUPPORT',definition='half-L1 of state mean curves; TV only when both means simplex',
                        simplex_mean_curves=bool(min(np.r_[means[0],means[2]])>=-1e-12 and max(abs(np.array(means).sum(axis=1)-1))<1e-10),materiality='NOT_CERTIFIED'))
                    if context=='D_FULL':
                        plot_arrays['HL_'+name]=delta;plot_arrays['anchored_'+name]=delta-delta[30]
                if context in drop_rules or context.startswith('LOYO'):
                    sensitivity_rows.append(dict(context=context,model=name,n_train=int(train.sum()),n_eval=int(ev.sum()),
                        mode=mode,**{k:v for k,v in metrics(q[ev],pred_eval,name,context,'EVAL',kind).items() if k not in ['context','model']},
                        scalar_model_HL_pp=float((pred_eval[d['labels'][ev]==2].mean()-pred_eval[d['labels'][ev]==0].mean())*100)
                            if kind=='scalar' and all(int((d['labels'][ev]==g).sum())>=50 and len(set(slots[ev][d['labels'][ev]==g]//5))>=20 for g in [0,2]) else np.nan))
            if mode=='PAST_ONLY_DEVELOPMENT':
                chrono_ix.extend(np.flatnonzero(ev));chrono_context.extend([context]*int(ev.sum()))
            print(context,'train',int(train.sum()),'eval',int(ev.sum()),'seconds',round(time.perf_counter()-tick,2),flush=True)
        ci=np.asarray(chrono_ix,int);preds={name:np.concatenate(v) for name,v in chrono.items()}
        assert len(ci)==489 and np.all(dates[ci][1:]>dates[ci][:-1])
        for name,pred in preds.items():scores.append(metrics(q[ci],pred,name,'DEV_POOLED_2020_2021','EVAL','scalar' if name in SCALAR_IDS else 'profile'))
        np.savez_compressed(OUT/'chronological_predictions.npz',dates=dates[ci],source_slot_indices=slots[ci],
            contexts=np.array(chrono_context),profile_models=np.array(PROFILE_IDS),profile_predictions=np.array([preds[n] for n in PROFILE_IDS]),
            scalar_models=np.array(SCALAR_IDS),scalar_predictions=np.array([preds[n] for n in SCALAR_IDS]))
        np.savez_compressed(OUT/'descriptive_predictions.npz',dates=dates,source_slot_indices=slots,
            profile_models=np.array(PROFILE_IDS),profile_predictions=np.array([d_full_predictions[n] for n in PROFILE_IDS]),
            scalar_models=np.array(SCALAR_IDS),scalar_predictions=np.array([d_full_predictions[n] for n in SCALAR_IDS]))
        np.savez_compressed(OUT/'residual_covariance.npz',**covariances)
        np.savez_compressed(OUT/'residual_eigenvalues.npz',**spectra)
        # Fixed raw historical reference; no empirical P0 bootstrap repeated.
        raw=np.array([q[d['labels']==g].mean(axis=0) for g in range(3)])
        raw_delta=raw[2]-raw[0]
        plot_arrays['P0_raw_means']=raw;plot_arrays['raw_HL']=raw_delta;plot_arrays['raw_anchored']=raw_delta-raw_delta[30]
        for g in range(3):
            for k,v in enumerate(raw[g]):direct.append(dict(context='D_FULL',label='P0_D_ONLY',state=g,bin=k,mean=v,n=int((d['labels']==g).sum())))
            for win,(a,b) in WINDOWS.items():
                vals=q[d['labels']==g,a:b].sum(axis=1)
                window_rows.append(dict(context='D_FULL',label='P0_D_ONLY',state=g,window=win,n=len(vals),mean=float(vals.mean()),sd=float(vals.std(ddof=1))))
        for name,mask in [('FULL',np.ones(len(z),bool)),*drop_rules.items()]:
            diff=q[mask&(d['labels']==2)].mean(axis=0)-q[mask&(d['labels']==0)].mean(axis=0)
            contrast.extend([dict(context=name,model='RAW_P0_LABELS',window=win,n_days=int(mask.sum()),estimate_pp=float(diff[a:b].sum()*100),
                                 definition='fixed historical P0 labels; subset mean of original daily shares',materiality='NOT_CERTIFIED') for win,(a,b) in WINDOWS.items()])
            contrast.append(dict(context=name,model='RAW_P0_LABELS',window='TV_HL',n_days=int(mask.sum()),TV=float(abs(diff).sum()/2),materiality='NOT_CERTIFIED'))
        bootstrap=[]
        historic_names={'OPEN30':'OPEN','MID_C':'C_SPEC_MID','CLOSE_C':'C_SPEC_CLOSE','MID_P0':'MID','CLOSE_P0':'CLOSE'}
        for win,old in historic_names.items():
            row=d['historical'][(d['historical'].branch=='PREV')&(d['historical']['mode']=='whole')&(d['historical'].variant=='FULL')&(d['historical'].window==old)&(d['historical'].state=='high-minus-low')].iloc[0]
            for length in [5,10]:bootstrap.append(dict(object='RAW_P0_FIXED_LABELS',window=win,block=length,B=1000,
                estimate=float(row.summary),lo=float(row[f'lo_{length}']),hi=float(row[f'hi_{length}']),scope='REUSED_HISTORICAL_P0_POINTWISE_CONDITIONAL_LABELS'))
        w20=block_weights(slots,20,1000,42);bmeans=[]
        for g in [0,2]:
            wg=w20*(d['labels']==g);bmeans.append((wg@q)/wg.sum(axis=1)[:,None])
        diffs=bmeans[1]-bmeans[0]
        for win,(a,b) in WINDOWS.items():
            lo,hi=np.percentile(diffs[:,a:b].sum(axis=1),[2.5,97.5])
            bootstrap.append(dict(object='RAW_P0_FIXED_LABELS',window=win,block=20,B=1000,
                estimate=float(raw_delta[a:b].sum()),lo=float(lo),hi=float(hi),scope='NEW_EXPLORATORY_FIXED_LABELS_NOT_CONFIRMATION'))
        lo,hi=np.percentile(np.abs(diffs).sum(axis=1)/2,[2.5,97.5])
        bootstrap.append(dict(object='RAW_P0_FIXED_LABELS',window='TV_HL',block=20,B=1000,estimate=float(abs(raw_delta).sum()/2),lo=float(lo),hi=float(hi),scope='DESCRIPTIVE_PERCENTILE_TV_BIASED_NEAR_ZERO_NOT_EQUIVALENCE'))
        # Raw historical-label daily regression for nominal H1 nulls.
        xp=np.c_[np.ones(len(z)),d['labels']==1,d['labels']==2].astype(float)
        rawfit=sm.OLS(q[:,66:78].sum(axis=1),xp).fit()
        for lag in [5,10,20]:
            cov=calendar_hac(xp,rawfit.resid,slots,lag)
            for null,name in [(0.,'RAW_H1_direction'),(.02,'RAW_H1_gt_0.02')]:
                res=linear_contrast(rawfit.params,cov,[0,0,1],null,True)
                tests.append(dict(context='D_FULL',model='RAW_P0_LABELS',test=name,lag=lag,statistic=(res['estimate']-null)/res['se'],
                                  p_value=res['p_value'],df=np.nan,status='CONDITIONAL_ASYMPTOTIC_EXPLORATORY'))
        f,pf,df=primary_models['OLS-L4'].training_fit.compare_f_test(primary_models['OLS-L1'].training_fit)
        tests.append(dict(context='D_FULL',model='OLS-L4',test='linear_vs_quadratic_F',lag=0,statistic=f,p_value=pf,df=df,status='IID_REFERENCE_HEURISTIC'))
        tests=holm_family(tests)
        # Pooled chronological paired losses, shared date draws across all
        # contrasts. Fixed forecasts, no refitting or selection in bootstrap.
        comparisons=[('M1','M0'),('P-OLS-Z','M0'),('M4-T8-Z4','M0'),('M4-T8-Z4','M2-T8'),('M4-T8-Z4','P-OLS-Z'),('M4-T12-Z4','M4-T8-Z4')]
        pairs=[];loss_columns=[];pair_names=[]
        for a,b in comparisons:
            for metric in ['profile_mse','close_mse']:
                pa,pb=preds[a],preds[b]
                if metric=='profile_mse':diff=((q[ci]-pa)**2).mean(axis=1)-((q[ci]-pb)**2).mean(axis=1)
                else:diff=((q[ci,:,][...,66:78]-pa[:,66:78]).sum(axis=1))**2-((q[ci,:,][...,66:78]-pb[:,66:78]).sum(axis=1))**2
                loss_columns.append(diff);pair_names.append((a,b,metric))
        loss_matrix=np.array(loss_columns).T
        for era,era_mask in [('DEV_POOLED_2020_2021',np.ones(len(ci),bool)),('DEV_2020',np.char.startswith(dates[ci],'2020')),('DEV_2021',np.char.startswith(dates[ci],'2021'))]:
            for lag in [5,10,20]:
                weights=block_weights(slots[ci][era_mask],lag,1000,42+lag)
                lm=loss_matrix[era_mask];draws=(weights@lm)/weights.sum(axis=1)[:,None]
                for j,(a,b,metric) in enumerate(pair_names):
                    x=np.ones((int(era_mask.sum()),1));res=sm.OLS(lm[:,j],x).fit();cov=calendar_hac(x,res.resid,slots[ci][era_mask],lag)
                    se=float(np.sqrt(cov[0,0]));mean=float(lm[:,j].mean());lo,hi=np.percentile(draws[:,j],[2.5,97.5])
                    pairs.append(dict(context=era,model=a,baseline=b,metric=metric,n_days=int(era_mask.sum()),lag=lag,
                        mean_loss_difference=mean,HAC_se=se,HAC_lo=mean-1.959964*se,HAC_hi=mean+1.959964*se,
                        p_nominal=2*stats.norm.sf(abs(mean/se)),block_B=1000,block_lo=float(lo),block_hi=float(hi),
                        interpretation='negative favors model; fixed forecasts, developmental reuse, conditional intervals'))
        environment_rows=[]
        env_masks={'2016-2019':dates<'2020','2020':np.char.startswith(dates,'2020'),'2021':np.char.startswith(dates,'2021')}
        early_t=context_transforms['DEV_2020'];coarse=np.searchsorted(early_t['quintile_cuts'],z,side='right')
        for env,mask in env_masks.items():
            support.append(support_row(env,'ALL',mask,d,None,'marginal'))
            for g in range(3):support.append(support_row(env,g,mask&(d['labels']==g),d,None,'fixed P0 retrospective S0'))
            for g in range(5):support.append(support_row(env,f'Q5_{g}',mask&(coarse==g),d,None,'2016-2019 training quintiles'))
        for env,mask in env_masks.items():
            if env=='2016-2019':continue
            base=env_masks['2016-2019']
            environment_rows.append(dict(environment=env,cell='MARGINAL',TV=float(abs(q[mask].mean(axis=0)-q[base].mean(axis=0)).sum()/2),status='DESCRIPTIVE_MIXTURE_DIFFERENCE'))
            for g in range(5):
                m0=base&(coarse==g);m1=mask&(coarse==g)
                ok=all(int(m.sum())>=50 and len(set(slots[m]//5))>=20 for m in [m0,m1])
                environment_rows.append(dict(environment=env,cell=f'Q5_{g}',n_reference=int(m0.sum()),n_environment=int(m1.sum()),
                    TV=float(abs(q[m0].mean(axis=0)-q[m1].mean(axis=0)).sum()/2) if ok else np.nan,status='SUPPORTED_COARSE_CELL_DESCRIPTIVE' if ok else 'ABSTAIN_SUPPORT'))
        # Frozen continuous state grids; local support masks are saved.
        grid=np.array(list(primary_transform['quantiles'].values()))
        heat=np.quantile(z,np.linspace(.02,.98,80))
        plot_arrays['grid_z']=grid;plot_arrays['heat_z']=heat
        for name in PROFILE_IDS:
            plot_arrays['grid_'+name]=primary_models[name].predict(grid,primary_transform)
            if name=='M4-T8-Z4':plot_arrays['heat_'+name]=primary_models[name].predict(heat,primary_transform)
        for query in np.r_[grid,heat]:
            rank=float(np.mean(z<=query));lo,hi=np.quantile(z,[max(0,rank-.1),min(1,rank+.1)])
            support.append(support_row('D_FULL_CONTINUOUS_GRID',query,(z>=lo)&(z<=hi),d,None,'train-only local rank band +/-0.1'))
        # Quantile-cell fidelity is a cell-averaged target, never pointwise m.
        quint=np.searchsorted(primary_transform['quintile_cuts'],z,side='right')
        for name in PROFILE_IDS:
            for g in range(5):
                mask=quint==g;rawmean=q[mask].mean(axis=0);fitmean=d_full_predictions[name][mask].mean(axis=0)
                for k in range(78):fidelity.append(dict(context='D_FULL',model=name,cell_type='TRAIN_QUINTILE_BIN',cell=g,bin=k,n=int(mask.sum()),
                    raw_mean=rawmean[k],fitted_mean=fitmean[k],fitted_minus_raw=fitmean[k]-rawmean[k]))
        plot_arrays['last_bin_HL']=np.array([raw_delta[77],raw_delta[66:77].sum(),raw_delta[66:78].sum(),raw_delta[54:56].sum()])
        np.savez_compressed(OUT/'plot_data.npz',**plot_arrays)
        save_csv('model_registry',registry);write_json(OUT/'model_parameters.json',parameters)
        for name,rows in [('scalar_ols_models_and_hac',coeff),('scalar_residual_influence',residual),('scalar_summary',scalar_summaries),
            ('scalar_specification_tests',tests),('scalar_contrasts_and_HAC',scalar_contrasts),('feature_collinearity',features),
            ('serial_diagnostics',serial),('profile_diagnostics',profiles),('profile_bin_residuals',bin_stats),('profile_daily_errors',daily_stats),
            ('model_fidelity_by_state_bin',fidelity),('support_and_environment',support),('environment_TV',environment_rows),
            ('direct_profiles',direct),('direct_window_summaries',window_rows),('model_scores',scores),('sensitivity_models',sensitivity_rows),
            ('contrasts_and_materiality',contrast),('block_intervals',bootstrap),('paired_loss_sensitivities',pairs)]:save_csv(name,rows)
        save_csv('daily_design_index',[dict(date_et=str(dates[i]),source_slot_index=int(slots[i]),Z0=float(z[i]),R_context_only=float(d['R'][i]),
            CLOSE_C=float(q[i,66:78].sum()),P0_retrospective_state=int(d['labels'][i]),
            drop_top1=bool(i in top1),drop_cook5=bool(i in top5)) for i in range(len(z))])
        save_csv('cohort_by_year',[dict(year=year,
            Q_days=int((np.isfinite(d['source_arrays']['q']).all(axis=1)&(d['source_arrays']['dates']>='2016-01-05')&np.char.startswith(d['source_arrays']['dates'],str(year))).sum()),
            Z0_days=int(np.char.startswith(dates,str(year)).sum())) for year in range(2016,2022)])
        raw_gap=d_full_predictions['M0'].sum(axis=1)-1
        np.testing.assert_allclose(raw_gap,0,atol=1e-12)
        assert np.isfinite(np.array([r['MSE_profile'] for r in scores if r['kind']=='profile'])).all()
        # Independent scalar aggregation of direct-profile tables.
        reconstructed=np.array([[sum(float(v) for v in q[d['labels']==g,k])/int((d['labels']==g).sum()) for k in range(78)] for g in range(3)])
        np.testing.assert_allclose(reconstructed,raw,atol=1e-10,rtol=0)
        for ref in d['identities']:
            path=(ROOT if ref['root']=='repo' else d['data_root'])/ref['path']
            if digest(path)!=ref['sha256']:raise ValueError('PROTECTED_SOURCE_CHANGED: '+ref['path'])
        runqa=dict(status='NUMERIC_QA_PASS_RENDER_PENDING',task_id=cfg['task_id'],protocol_sha256=digest(CONFIG),
            dataset_id=d['dataset_id'],cohort_date_hash=date_hash(dates),n_Q=1491,n_Z0=1472,n_chronological=489,
            P0_H1_pp=d['P0_H1']*100,P0_reproduction_error_pp=(raw_delta[66:78].sum()-d['P0_H1'])*100,
            source_identities=d['identities'],read_ledger=d['read_ledger'],network_attempts=network['attempts'],network_bytes=0,
            later_scientific_values_read=False,source_cache_growth=0,duplicate_Q_arrays_written=0,
            scalar_fit_count=len(contexts)*len(SCALAR_IDS),profile_fit_count=len(contexts)*len(PROFILE_IDS),
            chronological_origins=cfg['origins'],full_C_draft_unchanged=True,
            raw_rank_vs_D_FULL_quantile_label_differences=int((d['labels']!=transform_s0(z,primary_transform['S0'])).sum()),
            drop_top1_dates=dates[top1].tolist(),drop_cook5_dates=dates[top5].tolist(),
            top1_R_cutoff=float(min(d['R'][top1])),
            final_code={p.name:digest(p) for p in Path(__file__).parent.glob('c2r_*.py')},
            fit_wall_seconds=time.perf_counter()-start,versions=cfg['versions'],python=cfg['python'],
            findings_status={'source':'SOURCE_INSPIRED_PROXY','materiality':'NOT_CERTIFIED','independent_evaluation':'NOT_AUTHORIZED','EBM':'NOT_FITTED'})
        write_json(OUT/'provenance_and_QA.json',runqa)
        print('C2R_NUMERIC_QA_PASS',runqa['fit_wall_seconds'],'seconds',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','report'])
    args=parser.parse_args()
    if args.action=='prepare':prepare()
    elif args.action=='run':run()
    else:
        from .c2r_reporting import render
        with no_network():render()


if __name__=='__main__':main()
