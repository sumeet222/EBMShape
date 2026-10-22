"""Daily scores, whole-response science, conditional uncertainty and C3 verification."""
import json
from pathlib import Path
import pickle
import platform
import resource
import re
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from ..readiness import ROOT,WINDOWS,digest,transform_s0
from ..c2r_models import profile_losses,calendar_hac,date_hash
from ..c2r_diagnostics import block_weights,series_diagnostics,distribution
from .run import OUT,REF,CONFIG,config,inputs,load_bundle,reference_predictions,write_json
from . import models,m8_softmax


def support(mask,slots):
    n=int(np.sum(mask));g=len(set(np.asarray(slots)[mask]//5))
    return dict(n_days=n,five_session_groups=g,display_ok=n>=30 and g>=10,basic_ok=n>=50 and g>=20,
                strong_ok=n>=100 and g>=30,status='SUPPORTED_DESCRIPTIVE' if n>=50 and g>=20 else 'ABSTAIN_SUPPORT')


def shape(p,labels,slots):
    """Whole-prediction matched high-minus-low vector and closure-qualified TV."""
    lo=np.asarray(p)[labels==0].mean(axis=0);hi=np.asarray(p)[labels==2].mean(axis=0);delta=hi-lo
    ok=min(lo.min(),hi.min())>=-1e-12 and max(abs(lo.sum()-1),abs(hi.sum()-1))<1e-10
    gates=[support(labels==g,slots) for g in [0,2]]
    return dict(H1=float(delta[66:78].sum()),half_L1=float(abs(delta).sum()/2),
                H3_TV=float(abs(delta).sum()/2) if ok else np.nan,valid_profile=bool(ok),
                last_bin=float(delta[77]),other_close_bins=float(delta[66:77].sum()),
                D_max=float(abs(delta-delta[30]).max()),
                basic_ok=all(g['basic_ok'] for g in gates),
                status='SUPPORTED_DESCRIPTIVE' if all(g['basic_ok'] for g in gates) else 'ABSTAIN_SUPPORT'),delta


def score(q,p,dates,z,labels,slots,context,name):
    """Raw daily scores, retaining defects without clipping or renormalizing."""
    loss=profile_losses(q,p);e=q-p;close=e[:,66:78].sum(axis=1)
    row=dict(context=context,model=name,n_days=len(q),MSE_profile=loss['mse'].mean(),
             MAE_profile=loss['mae'].mean(),raw_half_L1=loss['half_l1'].mean(),TV_valid_n=loss['simplex_valid'].sum(),
             TV_prediction=np.nanmean(loss['tv']) if np.isfinite(loss['tv']).any() else np.nan,
             CLOSE_C_MSE=np.mean(close**2),CLOSE_C_RMSE_pp=np.sqrt(np.mean(close**2))*100,
             sum_defect_max=np.max(abs(p.sum(axis=1)-1)),negative_components=int((p<-1e-12).sum()),
             negative_mass=float(-np.minimum(p,0).sum()),above_one=int((p>1).sum()),minimum=p.min(),maximum=p.max(),
             outside_simplex_fraction=1-loss['simplex_valid'].mean())
    daily=pd.DataFrame(dict(context=context,model=name,date_et=dates,Z0=z,state=labels,source_slot=slots,
        MSE_profile=loss['mse'],MAE_profile=loss['mae'],raw_half_L1=loss['half_l1'],TV_prediction=loss['tv'],
        simplex_valid=loss['simplex_valid'],sum_defect=p.sum(axis=1)-1,negative_mass=-np.minimum(p,0).sum(axis=1),
        close_residual=close,CLOSE_C_MSE=close**2))
    windows=[]
    for window,(a,b) in WINDOWS.items():
        actual=q[:,a:b].sum(axis=1);pred=p[:,a:b].sum(axis=1);err=actual-pred
        slope=np.linalg.lstsq(np.c_[np.ones(len(pred)),pred],actual,rcond=None)[0] if np.ptp(pred)>1e-12 else [np.nan,np.nan]
        windows.append(dict(context=context,model=name,window=window,n_days=len(q),MSE=np.mean(err**2),
            RMSE_pp=np.sqrt(np.mean(err**2))*100,MAE_pp=np.mean(abs(err))*100,bias_pp=err.mean()*100,
            q01_error_pp=np.quantile(err,.01)*100,q99_error_pp=np.quantile(err,.99)*100,
            calibration_intercept=slope[0],calibration_slope=slope[1]))
    return row,daily,windows


def get_context(d,context):
    ix=np.arange(len(d['z'])) if context=='D_FULL' else np.flatnonzero(np.char.startswith(d['dates'],context[-4:]))
    pred=reference_predictions(d,context,ix)
    for name in models.IDS:
        bundle,_=load_bundle(context,name);pred[name]=models.predict(bundle,d['z'][ix])
    pred['M8']=m8_softmax.predict(json.loads((OUT/(context+'__M8.json')).read_text()),d['z'][ix])
    for name in models.IDS[1:]:pred['NORM_'+name]=models.normalized(pred[name])
    t=load_bundle(context,models.IDS[3])[0]['transform']
    return ix,pred,transform_s0(d['z'][ix],t['S0'])


def refresh_registry(d):
    """Rebuild small native/M8 fit registry from verified completed checkpoints."""
    fields=['key','context','name','config','seed','n_train','n_eval','eval_MSE','wall_seconds','peak_rss_bytes','blob_sha256','blob_bytes']
    registry=[{k:r[k] for k in fields} for r in [json.loads(p.read_text()) for p in sorted((OUT/'checkpoints').glob('*.json'))]]
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        mpath=OUT/(context+'__M8.json');m=json.loads(mpath.read_text())
        ntrain=1472 if context=='D_FULL' else int(np.sum(d['dates']<context[-4:]+'-01-01'))
        ix=np.arange(len(d['z'])) if context=='D_FULL' else np.flatnonzero(np.char.startswith(d['dates'],context[-4:]))
        registry.append(dict(key=context+'__M8',context=context,name='M8',config='LAMBDA_0.001',seed='DETERMINISTIC',
            n_train=ntrain,n_eval=len(ix),eval_MSE=np.mean((m8_softmax.predict(m,d['z'][ix])-d['q'][ix])**2),
            wall_seconds=np.nan,peak_rss_bytes=np.nan,blob_sha256=digest(mpath),blob_bytes=mpath.stat().st_size))
    pd.DataFrame(registry).to_csv(OUT/'model_registry.csv',index=False)


def diagnose():
    cfg=config();d=inputs();all_scores=[];daily=[];windows=[];bins=[];serial=[];features=[];calibration=[]
    shapes=[];fidelity=[];group_curves=[];sup=[];environment=[];native={};stability=[];coarsening=[];residual_summary=[]
    predictions={};covariances={};cached={}
    records=[json.loads(p.read_text()) for p in sorted((OUT/'checkpoints').glob('*.json'))]
    assert len(records)==59
    for r in records:
        native[r['key']]=r['audit']
    write_json(OUT/'native_terms_and_bins.json',native);refresh_registry(d)
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        ix,pred,labels=get_context(d,context);cached[context]=(ix,pred,labels)
        predictions[context+'__dates']=d['dates'][ix];predictions[context+'__models']=np.array(list(pred))
        predictions[context+'__predictions']=np.array(list(pred.values()));predictions[context+'__source_indices']=ix
    ix=np.r_[cached['DEV_2020'][0],cached['DEV_2021'][0]]
    pred={n:np.concatenate([cached[c][1][n] for c in ['DEV_2020','DEV_2021']]) for n in cached['DEV_2020'][1]}
    labels=np.r_[cached['DEV_2020'][2],cached['DEV_2021'][2]];cached['POOLED']=(ix,pred,labels)
    # Include train scores for each origin without storing duplicate target arrays.
    for context in ['DEV_2020','DEV_2021']:
        tr=d['dates']<context[-4:]+'-01-01';ti=np.flatnonzero(tr);pp=reference_predictions(d,context,ti)
        for name in models.IDS:pp[name]=models.predict(load_bundle(context,name)[0],d['z'][ti])
        pp['M8']=m8_softmax.predict(json.loads((OUT/(context+'__M8.json')).read_text()),d['z'][ti])
        tt=load_bundle(context,models.IDS[3])[0]['transform'];cached[context+'_TRAIN']=(ti,pp,transform_s0(d['z'][ti],tt['S0']))
    for context,(ix,pred,labels) in cached.items():
        q=d['q'][ix];slots=d['slots'][ix];dates=d['dates'][ix];z=d['z'][ix]
        for name,p in pred.items():
            r,dd,ww=score(q,p,dates,z,labels,slots,context,name);all_scores.append(r);daily.append(dd);windows.extend(ww)
            if context.endswith('TRAIN'):continue
            e=q-p
            for g in [-1,0,1,2]:
                mask=np.ones(len(q),bool) if g==-1 else labels==g
                for k in range(78):bins.append(dict(context=context,model=name,state=g,bin=k,n_days=int(mask.sum()),
                    mean_residual=float(e[mask,k].mean()),RMSE=float(np.sqrt(np.mean(e[mask,k]**2))),MAE=float(abs(e[mask,k]).mean())))
            if name in models.IDS+['M8']:
                covariance=np.cov(e,rowvar=False);eig,vec=np.linalg.eigh(covariance);pc=e@vec[:,-1]
                residual_summary.append(dict(context=context,model=name,**distribution(e[:,66:78].sum(axis=1)),
                    covariance_rank=int(np.linalg.matrix_rank(covariance)),PC1_fraction=eig[-1]/eig.sum(),
                    first5_PC_fraction=eig[-5:].sum()/eig.sum(),covariance_closure_max=abs(covariance.sum(axis=1)).max(),
                    time_roughness=np.mean(np.sum(np.diff(p,axis=1)**2,axis=1)),
                    residual_1400_bias=e[:,54].mean(),residual_1555_bias=e[:,77].mean()))
                covariances[context+'__'+name+'__covariance']=covariance
                covariances[context+'__'+name+'__eigenvalues']=eig
                for j in range(len(q)):
                    features.append(dict(context=context,model=name,date_et=dates[j],Z0=z[j],state=labels[j],
                        close_actual=q[j,66:78].sum(),close_pred=p[j,66:78].sum(),close_residual=e[j,66:78].sum(),
                        residual_L2=np.linalg.norm(e[j]),PC1=pc[j],squared_norm=np.sum(e[j]**2),
                        covariance_closure_max=float(abs(covariance.sum(axis=1)).max()),PC1_variance_fraction=eig[-1]/eig.sum()))
                for series,values in [('close_residual',e[:,66:78].sum(axis=1)),('PC1',pc),('residual_L2',np.linalg.norm(e,axis=1))]:
                    rr,_=series_diagnostics(values,series,context,name);serial.extend(rr)
                for grouping,groups in [('year',np.array([s[:4] for s in dates])),('quarter',np.array([s[:4]+'Q'+str((int(s[5:7])-1)//3+1) for s in dates]))]:
                    for group in np.unique(groups):
                        a=groups==group;environment.append(dict(context=context,model=name,kind=grouping,environment=group,state=-1,n_days=int(a.sum()),
                            close_residual_pp=e[a,66:78].sum(axis=1).mean()*100,MSE_profile=(e[a]**2).mean(),
                            mean_variance_correlation=float(np.corrcoef(p[a].mean(axis=1),e[a].var(axis=1))[0,1]) if np.std(p[a].mean(axis=1))>1e-14 else np.nan))
                cuts=np.quantile(p[:,66:78].sum(axis=1),[.2,.4,.6,.8]);cats=np.searchsorted(cuts,p[:,66:78].sum(axis=1),side='right')
                for g in range(5):
                    a=cats==g;calibration.append(dict(context=context,model=name,bin=g,n_days=int(a.sum()),
                        observed_mean_pp=q[a,66:78].sum(axis=1).mean()*100 if a.any() else np.nan,
                        predicted_mean_pp=p[a,66:78].sum(axis=1).mean()*100 if a.any() else np.nan,
                        status='DISPLAY' if a.any() else 'ABSTAIN_EMPTY_CONSTANT_FIT'))
        # Same-row raw/fit cell comparisons, separately historical ranks and training S0.
        for origin,lab in [('HISTORICAL_P0',d['labels'][ix]),('TRAIN_S0',labels)]:
            for env in ['ALL','2016-2019','2020','2021']:
                a=np.ones(len(ix),bool) if env=='ALL' else (dates<'2020-01-01' if env=='2016-2019' else np.char.startswith(dates,env))
                if not a.any():continue
                for g in range(3):
                    cell=a&(lab==g);gate=support(cell,slots)
                    sup.append(dict(context=context,label_origin=origin,environment=env,state=g,**gate,
                        Z0_min=float(z[cell].min()) if cell.any() else np.nan,Z0_max=float(z[cell].max()) if cell.any() else np.nan))
                raw,rawdelta=shape(q[a],lab[a],slots[a])
                for name,p in {'RAW':q,**pred}.items():
                    sh,delta=shape(p[a],lab[a],slots[a]);shapes.append(dict(context=context,label_origin=origin,environment=env,model=name,**sh,
                        raw_H1=raw['H1'],H1_error=sh['H1']-raw['H1'],H3_error=sh['H3_TV']-raw['H3_TV'],
                        materiality='INCONCLUSIVE_NO_POPULATION_CI',population_interval='NO_POPULATION_CI'))
                    if env!='ALL':continue
                    for g in range(3):
                        cell=lab==g;mean=p[cell].mean(axis=0);actual=q[cell].mean(axis=0)
                        for k in range(78):group_curves.append(dict(context=context,label_origin=origin,model=name,state=g,bin=k,
                            mean=mean[k],raw_mean=actual[k],error=mean[k]-actual[k],n_days=int(cell.sum()),sum_defect=mean.sum()-1,
                            state_difference=delta[k],anchored_D=delta[k]-delta[30],raw_anchored_D=rawdelta[k]-rawdelta[30]))
                        for window,(start,end) in WINDOWS.items():fidelity.append(dict(context=context,label_origin=origin,model=name,state=g,window=window,
                            raw=actual[start:end].sum(),fitted=mean[start:end].sum(),error_pp=(mean[start:end]-actual[start:end]).sum()*100))
        if context in ['D_FULL','DEV_2020','DEV_2021']:
            bundle,_=load_bundle(context,models.IDS[3]);t=bundle['transform']
            train_dates=d['dates']<=t['last'];nativecuts=np.asarray(t['cuts']);b=np.searchsorted(nativecuts,z,side='right')
            for g in range(len(nativecuts)+1):
                for env in ['ALL','2020','2021']:
                    a=(b==g)&(np.ones(len(z),bool) if env=='ALL' else np.char.startswith(dates,env));gate=support(a,slots)
                    sup.append(dict(context=context,label_origin='NATIVE_Z0_MAIN_AND_PAIR',environment=env,state=g,**gate,
                        Z0_min=float(z[a].min()) if a.any() else np.nan,Z0_max=float(z[a].max()) if a.any() else np.nan))
            for g in range(3):
                a=labels==g;cont=pred[models.IDS[3]][a];disc=pred[models.IDS[4]][a]
                shc,_=shape(pred[models.IDS[3]],labels,slots);shd,_=shape(pred[models.IDS[4]],labels,slots)
                coarsening.append(dict(context=context,state=g,n_days=int(a.sum()),continuous_bins=len(nativecuts)+1,discrete_bins=3,
                    continuous_MSE=np.mean((q[a]-cont)**2),discrete_MSE=np.mean((q[a]-disc)**2),
                    within_tercile_predicted_dispersion=np.mean(np.var(cont,axis=0)),
                    H1_continuous=shc['H1'],H1_discrete=shd['H1'],Dmax_continuous=shc['D_max'],Dmax_discrete=shd['D_max'],
                    status='CONTINUOUS_VS_DISCRETE_INFORMATION_LOSS_DESCRIPTIVE',extrapolated_dates=int(((z<t['minimum'])|(z>t['maximum'])).sum())))
    for context in ['DEV_2020','DEV_2021']:
        ix=cached[context][0]
        for name in models.IDS[1:]:
            base=models.predict(load_bundle(context,name,42)[0],d['z'][ix])
            for seed in cfg['seeds']:
                p=models.predict(load_bundle(context,name,seed)[0],d['z'][ix]);lab=cached[context][2]
                sh,_=shape(p,lab,d['slots'][ix]);stability.append(dict(context=context,model=name,seed=seed,**sh,
                    MSE_profile=np.mean((p-d['q'][ix])**2),max_prediction_difference_vs42=float(abs(p-base).max()),
                    interpretation='ALGORITHMIC_STABLE_ONLY; seeds are not population draws'))
    # FULL models scored on fixed stress cohorts and separate actual stress refits.
    stress=[];params=json.loads((REF/'model_parameters.json').read_text());fullpred=cached['D_FULL'][1]
    for context,names in cfg['stress_plan'].items():
        ix=np.flatnonzero(np.isin(d['dates'],params[context]['train_dates']))
        for name in models.IDS+['M8']:
            p=fullpred[name][ix];sh,_=shape(p,d['labels'][ix],d['slots'][ix]);stress.append(dict(context=context,model=name,fit='FIXED_FULL_SCORE',n_days=len(ix),**sh,MSE_profile=np.mean((p-d['q'][ix])**2)))
            if name in names:
                p=models.predict(load_bundle(context,name)[0],d['z'][ix]);sh,_=shape(p,d['labels'][ix],d['slots'][ix]);stress.append(dict(context=context,model=name,fit='ACTUAL_REFIT_RELEARNED_TRAIN_CUTS',n_days=len(ix),**sh,MSE_profile=np.mean((p-d['q'][ix])**2)))
    pd.DataFrame(stress).to_csv(OUT/'stress_refits_and_fixed_scores.csv',index=False)
    # Native slices share training-only representatives; no singleton population claim.
    slices=[];surface=[];bundle,_=load_bundle('D_FULL',models.IDS[3]);t=bundle['transform'];grid=np.linspace(t['minimum'],t['maximum'],160)
    reps=np.asarray(t['quantiles']);refparams=json.loads((REF/'model_parameters.json').read_text())['D_FULL']
    allgrid=reference_predictions(dict(d,z=np.r_[d['z'],reps,grid]),'D_FULL',np.arange(len(d['z']),len(d['z'])+len(reps)+len(grid)))
    for name in models.IDS:allgrid[name]=models.predict(load_bundle('D_FULL',name)[0],np.r_[reps,grid])
    allgrid['M8']=m8_softmax.predict(json.loads((OUT/'D_FULL__M8.json').read_text()),np.r_[reps,grid])
    width=float(np.median(np.diff(np.r_[t['minimum'],t['cuts'],t['maximum']]))/2)
    for name,p in allgrid.items():
        for i,rep in enumerate(reps):
            count=np.abs(d['z']-rep)<=width;gate=support(count,d['slots'])
            for k in range(78):slices.append(dict(model=name,quantile=[.1,.25,.5,.75,.9][i],Z0=rep,bin=k,prediction=p[i,k],width=width,**gate))
    for i,z in enumerate(grid):
        g=np.searchsorted(t['cuts'],z,side='right');counts=np.searchsorted(t['cuts'],d['z'],side='right')==g;gate=support(counts,d['slots'])
        for k in range(78):surface.append(dict(model=models.IDS[3],Z0=z,native_state_bin=g,bin=k,prediction=allgrid[models.IDS[3]][5+i,k],**gate))
    tables={'profile_predictive_metrics':all_scores,'window_prediction_metrics':windows,'model_shapes_and_scientific_contrasts':shapes,
        'raw_vs_model_scientific_fidelity':fidelity,'group_mean_profiles':group_curves,'state_support_and_masks':sup,
        'conditional_profile_error_by_bin':bins,'residual_daily_features':features,'serial_diagnostics':serial,'calibration_quintiles':calibration,
        'temporal_composition_and_stability':environment,'native_seed_and_complexity_stability':stability,
        'continuous_vs_discrete_coarsening':coarsening,'continuous_slices':slices,'continuous_total_surface':surface,
        'residual_distribution_and_covariance_summary':residual_summary}
    for name,rows in tables.items():pd.DataFrame(rows).to_csv(OUT/(name+'.csv'),index=False)
    means=pd.DataFrame(group_curves)
    full=means[(means.context=='D_FULL')&(means.label_origin=='HISTORICAL_P0')].copy()
    full['weighted_mean']=full['mean']*full.n_days
    global_curves=full.groupby(['model','bin']).agg(weighted_mean=('weighted_mean','sum'),n_days=('n_days','sum')).reset_index()
    global_curves['mean']=global_curves.weighted_mean/global_curves.n_days
    raw=global_curves[global_curves.model=='RAW'].set_index('bin')['mean']
    global_curves['bias']=global_curves['mean']-global_curves.bin.map(raw)
    global_curves.to_csv(OUT/'global_mean_profiles.csv',index=False)
    adequacy=pd.DataFrame(shapes).copy()
    adequacy['fidelity_status']=np.where(adequacy.basic_ok,'SUPPORTED_DESCRIPTIVE','ABSTAIN_SUPPORT')
    adequacy['population_status']='BLOCKED_ASSUMPTIONS_NO_POPULATION_CI'
    adequacy['EBM_increment']='NOT_ESTABLISHED'
    adequacy.to_csv(OUT/'scientific_adequacy_matrix.csv',index=False)
    daily=pd.concat(daily,ignore_index=True);daily.to_csv(OUT/'scorecard_daily_compact.csv',index=False)
    daily.groupby(['context','model']).agg(sum_min=('sum_defect','min'),sum_max=('sum_defect','max'),
        sum_sd=('sum_defect','std'),negative_mass_mean=('negative_mass','mean'),outside_simplex=('simplex_valid',lambda x:1-x.mean())).reset_index().to_csv(OUT/'simplex_validity.csv',index=False)
    np.savez_compressed(OUT/'predictions.npz',**predictions);np.savez_compressed(OUT/'residual_covariance.npz',**covariances)
    paired(d,cached,daily,cfg);joint_shapes(d,cached['D_FULL'],cfg);environment_tests(d,cached);theory()
    verify()


def paired(d,cached,daily,cfg):
    ix,pred,lab=cached['POOLED'];q=d['q'][ix];slots=d['slots'][ix];rows=[];groups=[]
    A,B,C,D,E=models.IDS
    pairs=[(D,B),(E,C),(B,A),(C,A),(D,E),(D,'M0'),(D,'P-OLS-Z'),(D,'M4-T8-Z4'),(D,'M8'),(E,'M8'),(A,'M0')]
    for metric in ['MSE_profile','CLOSE_C_MSE']:
        losses={name:((p-q)**2).mean(axis=1) if metric=='MSE_profile' else ((p-q)[:,66:78].sum(axis=1))**2 for name,p in pred.items()}
        diffs=np.array([losses[first]-losses[base] for first,base in pairs]).T
        for length in cfg['block_lengths']:
            W=block_weights(slots,length,cfg['bootstrap_B'],cfg['bootstrap_seed']+length)
            draws=W@diffs/W.sum(axis=1,keepdims=True)
            for j,(first,base) in enumerate(pairs):
                delta=diffs[:,j];cov=calendar_hac(np.ones((len(ix),1)),delta-delta.mean(),slots,length);se=float(np.sqrt(max(cov[0,0],0)))
                primary=(metric=='MSE_profile' and (first,base) in [(D,B),(E,C),(D,E),(D,'M0')]) or (metric=='CLOSE_C_MSE' and (first,base)==(D,B))
                rows.append(dict(first=first,baseline=base,metric=metric,n_days=len(ix),lag_or_block=length,difference=delta.mean(),
                    relative_percent=delta.mean()/losses[base].mean()*100,HAC_se=se,HAC_lo=delta.mean()-1.96*se,HAC_hi=delta.mean()+1.96*se,
                    p_value=2*stats.norm.sf(abs(delta.mean()/se)) if se>0 else 1.,
                    block_lo=np.quantile(draws[:,j],.025),block_hi=np.quantile(draws[:,j],.975),primary_family=primary,
                    status='CONDITIONAL_DEVELOPMENTAL_FIXED_FORECASTS',selection_uncertainty='NOT_INCLUDED'))
        for j,(first,base) in enumerate(pairs):
            for year in ['2020','2021','ALL']:
                for state in [-1,0,1,2]:
                    a=(np.ones(len(ix),bool) if year=='ALL' else np.char.startswith(d['dates'][ix],year))&(np.ones(len(ix),bool) if state==-1 else lab==state)
                    groups.append(dict(first=first,baseline=base,metric=metric,year=year,state=state,n_days=int(a.sum()),difference=diffs[a,j].mean(),**{k:v for k,v in support(a,slots).items() if k!='n_days'}))
    frame=pd.DataFrame(rows);frame['Holm_p_conditional']=np.nan
    sel=frame.primary_family&(frame.lag_or_block==10);frame.loc[sel,'Holm_p_conditional']=multipletests(frame.loc[sel,'p_value'],method='holm')[1]
    frame.to_csv(OUT/'paired_loss_tests.csv',index=False);pd.DataFrame(groups).to_csv(OUT/'paired_loss_by_year_state.csv',index=False)


def joint_shapes(d,full,cfg):
    ix,pred,lab=full;lab=d['labels'][ix];slots=d['slots'][ix];rows=[]
    for length in cfg['block_lengths']:
        W=block_weights(slots,length,cfg['bootstrap_B'],cfg['bootstrap_seed']+length)
        lo=W*(lab==0);hi=W*(lab==2);lo/=lo.sum(axis=1,keepdims=True);hi/=hi.sum(axis=1,keepdims=True)
        contrast=hi-lo;raw=contrast@d['q'][ix];rawH=raw[:,66:78].sum(axis=1)
        for name,p in {'RAW':d['q'][ix],**pred}.items():
            delta=contrast@p;h=delta[:,66:78].sum(axis=1);half=np.abs(delta).sum(axis=1)/2
            anchored_max=abs(delta-delta[:,30,None]).max(axis=1)
            raw_half=abs(raw).sum(axis=1)/2
            for target,draws in [('H1',h),('H1_model_minus_raw',h-rawH),('raw_half_L1',half),
                                 ('anchored_D_max',anchored_max),('half_L1_model_minus_raw',half-raw_half)]:
                rows.append(dict(model=name,target=target,block_length=length,B=cfg['bootstrap_B'],lo=np.quantile(draws,.025),hi=np.quantile(draws,.975),
                    status='FIXED_LABEL_FIXED_FIT_JOINT_DESCRIPTIVE; NOT_REFIT_POPULATION_CI'))
    pd.DataFrame(rows).to_csv(OUT/'joint_fixed_fit_shape_intervals.csv',index=False)


def environment_tests(d,cached):
    ix,pred,lab=cached['D_FULL'];rows=[];dates=d['dates'][ix];q=d['q'][ix];slots=d['slots'][ix]
    for name,p in pred.items():
        for g in range(3):
            reference=(dates<'2020-01-01')&(lab==g);ref=q[reference].mean(axis=0);re=(q-p)[reference].mean(axis=0)
            for year in ['2020','2021']:
                a=np.char.startswith(dates,year)&(lab==g);gate=support(a,slots);rg=support(reference,slots)
                rows.append(dict(model=name,state=g,environment=year,n_days=int(a.sum()),reference_n=int(reference.sum()),
                    raw_group_TV=abs(q[a].mean(axis=0)-ref).sum()/2,
                    residual_group_half_L1=abs((q-p)[a].mean(axis=0)-re).sum()/2,
                    status='SUPPORTED_DESCRIPTIVE' if gate['basic_ok'] and rg['basic_ok'] else 'ABSTAIN_SUPPORT',
                    stability='INCONCLUSIVE_NO_POPULATION_CI'))
    pd.DataFrame(rows).to_csv(OUT/'environment_residual_discrepancy.csv',index=False)
    reference=dates<'2020-01-01'
    weights=np.array([np.mean(lab[reference]==g) for g in range(3)])
    reweighted=[]
    for name,p in pred.items():
        reference_residual=np.array([(q-p)[reference&(lab==g)].mean(axis=0) for g in range(3)])
        reference_raw=np.array([q[reference&(lab==g)].mean(axis=0) for g in range(3)])
        for year in ['2020','2021']:
            cells=[np.char.startswith(dates,year)&(lab==g) for g in range(3)]
            ok=all(support(a,slots)['basic_ok'] and support(reference&(lab==g),slots)['basic_ok'] for g,a in enumerate(cells))
            raw=np.array([q[a].mean(axis=0) for a in cells]);residual=np.array([(q-p)[a].mean(axis=0) for a in cells])
            reweighted.append(dict(model=name,environment=year,reference_weights=json.dumps(weights.tolist()),
                estimand='D_FULL_S0_reference2016_19_reweighted_coarse_mean; descriptive; not original marginal',
                reweighted_raw_TV=float(abs(weights@(raw-reference_raw)).sum()/2) if ok else np.nan,
                reweighted_residual_half_L1=float(abs(weights@(residual-reference_residual)).sum()/2) if ok else np.nan,
                status='SUPPORTED_DESCRIPTIVE' if ok else 'ABSTAIN_SUPPORT'))
    pd.DataFrame(reweighted).to_csv(OUT/'environment_reference_reweighted.csv',index=False)


def theory():
    source='docs/specs/experiment_B_stage2C_supplied_theorem_extracts_v1.md'
    text=(ROOT/source).read_text()
    originals=sorted(set(re.findall(r'Source: .*? — ([^\n]+?\.md), original line',text)))
    originals+=['state_dependent_ebm_consolidation_assumptions_and_issues_v1.md']
    available=[str(p.relative_to(ROOT)) for p in (ROOT/'docs').rglob('*.md') if 'theor' in p.name or 'consolid' in p.name]
    write_json(OUT/'theory_source_availability.json',dict(inspected=[source],inspected_sha256=digest(ROOT/source),
        discovered_related=available,missing_requested_names=originals,
        requested_material_not_located=['Full consolidation verification (exact filename not supplied)',
          'Full consolidation theorem crosswalk (exact filename not supplied)','Task6 standalone','Task17 standalone','Task19 standalone','Task21 standalone'],
        existing_excerpt_crosswalk_inspected='data/registry/B_stage2C_theorem_diagnostic_crosswalk.csv',
        note='Original basenames extracted literally from supplied Source headers; full settings/proofs absent. Existing B excerpt crosswalk is not the full consolidation crosswalk.'))
    rows=[]
    methods=[
      ('Q closure/additive normalized shift','ALGEBRAIC_IDENTITY_ONLY','C3 §2; sum f+78g=1','balanced 78 bins; complete predictions','actual closure and D computed','finite array identity; pure vertical shift cannot change normalized shape'),
      ('Support-specific identification','ADAPTED_DESCRIPTIVE','T10B.B1 KNOWN/DERIVED; T11.A1','positive cells, deterministic dictionary; FD covariance/conditional independence unverified','distinct dates/groups/masks; native fit not least squares projector','coarse observed-cell means; no unsupported singleton identification'),
      ('Raw versus fitted adequacy','ADAPTED_DESCRIPTIVE','T10B.B2 PROVED; T15.F1; T25.F1 PROVED','known proper projection/response class or calibrated joint raw event absent','same-row H1/D/full-vector discrepancies','observed fidelity; no raw confidence certificate'),
      ('Gaussian selection pivot','BLOCKED_ASSUMPTIONS','T12.C1 KNOWN CONDITIONAL GAUSSIAN','known scale Gaussian errors and exact whole-tree selection event','heavy tails/dependence; no native selection polyhedron','no exact selected pivot'),
      ('Ideal greedy path','BLOCKED_ASSUMPTIONS','T16.I2; T18.A1 scope excerpts','proper finite tree dictionary, specific greedy histories/corrections','native cyclic categorical boosting with quantile bins; not ideal projection history','audit software graph only'),
      ('Environment composition','ADAPTED_DESCRIPTIVE','T18.A1; T18.R1; Tasks19/21 scope only','matched conditional kernels, overlap, sampling law','year occupancy/residual TV and ABSTAIN masks','finite environment differences, no causal pandemic mechanism'),
      ('Continuous coarsening','ADAPTED_DESCRIPTIVE','T24.E1 PROVED; T24.I1 CLASSICAL scope-specific','IID records, fixed partitions, known range and supplied localization bias','Q bounded but dependent; bins train estimated; no smoothness bound','M5/M6 finite prediction resolution, no certified risk loss'),
      ('Estimated moments','BLOCKED_ASSUMPTIONS','T25.I1/I2 PROVED','joint moment/response event, supplied affine class/admissibility','training empirical cuts/moments only; no joint inversion','no estimated-moment population inversion'),
      ('Paired fixed forecasts HAC','CONDITIONAL_STANDARD_INFERENCE','T22.E1 classical; C2R calendar sandwich','stable weak dependence/moments and selection-conditioned evaluation; independent held-out law absent','489 prior-explored dates; calendar HAC5/10/20','conditional developmental sensitivity, not confirmation'),
      ('Joint scheduled blocks','ADAPTED_DESCRIPTIVE','Tasks6/19/21 scope; existing C2R circular algorithm','defensible dependence/stability law; fixed forecasts and labels','shared scheduled-slot weights; no fill, circular wrap','conditional fixed-fit sensitivity only'),
      ('Holm named family','CONDITIONAL_STANDARD_INFERENCE','standard Holm; C3 freeze','valid marginal p values; selection prior exposure not repaired','five conditional HAC10 comparisons','finite family under premises only'),
      ('Softmax normalization','EXACT_SCOPE_INSTANTIATION','C3 M8 definition','finite logits positive denominator; centered coefficients','stable logsumexp, gradient/solver checks','normalized fitted probabilities, not raw-law theorem'),
      ('Information-value identity','ALGEBRAIC_IDENTITY_ONLY','T22.D1 CLASSICAL','square integrable single law; actual conditional means','fitted prediction differences only','fitted ranking not equality with true state-information value'),
      ('Refit shape inference','DEFERRED','C3 resource cap; C5 future authorization','rebuild source selection/cuts/tuning/fits under valid dependence law','59/60 native fit budget used','NO_POPULATION_CI; full inner selection+fit ~19 fits per bootstrap, B1000 ~19000 native fits'),
      ('Trading decisions','NOT_APPLICABLE','T22.E1 action branch','executable action map/costs','no trading stage','none')]
    for method,classification,src,premises,evidence,claim in methods:
        rows.append(dict(method=method,classification=classification,source=source+' :: '+src,required_conditions=premises,
            evidence=evidence,computation='C3 numerical tables and QA_C3.json',permissible_claim=claim,
            blocker='full theorem settings/proofs and raw-law event not established' if classification in ['BLOCKED_ASSUMPTIONS','DEFERRED','ADAPTED_DESCRIPTIVE'] else 'see required_conditions'))
    pd.DataFrame(rows).to_csv(OUT/'theoretical_method_ledger.csv',index=False)


def verify():
    cfg=config();d=inputs();baseline=json.loads((OUT/'protected_input_baseline.json').read_text());changed=[]
    for ref in cfg['authority']:assert digest(ROOT/ref['path'])==ref['sha256'],ref['path']
    assert digest(ROOT/'config/C_full_protocol_v1_1.yaml')==cfg['full_C_draft_sha256']
    for path,ref in baseline.items():
        p=ROOT/path
        if not p.exists() or digest(p)!=ref['sha256']:changed.append(path)
    assert not changed,changed
    scores=pd.read_csv(OUT/'profile_predictive_metrics.csv');daily=pd.read_csv(OUT/'scorecard_daily_compact.csv')
    np.testing.assert_allclose(daily.groupby(['context','model']).MSE_profile.mean().sort_index(),scores.set_index(['context','model']).MSE_profile.sort_index(),atol=1e-15,rtol=0)
    for context,n in [('D_FULL',1472),('DEV_2020',241),('DEV_2021',248),('POOLED',489)]:assert (scores[scores.context==context].n_days==n).all()
    maxparity=0
    c2r_error=0.
    with np.load(OUT/'predictions.npz') as saved:
        for context in ['D_FULL','DEV_2020','DEV_2021']:
            ix,pred,labels=get_context(d,context)
            for i,name in enumerate(saved[context+'__models']):
                maxparity=max(maxparity,float(abs(saved[context+'__predictions'][i]-pred[name]).max()))
            file='descriptive_predictions.npz' if context=='D_FULL' else 'chronological_predictions.npz'
            with np.load(REF/file) as old:
                oi=np.searchsorted(old['dates'],d['dates'][ix])
                assert np.array_equal(old['dates'][oi],d['dates'][ix])
                for j,name in enumerate(old['profile_models']):
                    if name in pred:c2r_error=max(c2r_error,float(abs(old['profile_predictions'][j,oi]-pred[name]).max()))
    assert maxparity<1e-10
    assert c2r_error<1e-10
    shape_table=pd.read_csv(OUT/'group_mean_profiles.csv')
    maxplot=0.
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        ix,pred,labels=get_context(d,context)
        for name,p in {'RAW':d['q'][ix],**pred}.items():
            for g in range(3):
                a=shape_table[(shape_table.context==context)&(shape_table.model==name)&(shape_table.label_origin=='TRAIN_S0')&(shape_table.state==g)].sort_values('bin')
                maxplot=max(maxplot,float(abs(a['mean'].to_numpy()-p[labels==g].mean(axis=0)).max()))
    assert maxplot<1e-10
    records=[json.loads(p.read_text()) for p in (OUT/'checkpoints').glob('*.json')]
    assert len(records)<=60 and all(r['audit']['serialization_parity'] for r in records)
    assert all(all(v==78 for v in r['audit']['time_levels']) for r in records)
    params=json.loads((REF/'model_parameters.json').read_text())
    for r in records:
        ctx=r['context']
        if ctx=='D_FULL':tr=np.ones(len(d['z']),bool)
        elif ctx.startswith(('INNER_','DEV_')):tr=d['dates']<ctx[-4:]+'-01-01'
        else:tr=np.isin(d['dates'],params[ctx]['train_dates'])
        expected=models.transform(d['dates'][tr],d['z'][tr],cfg['configs'][r['config']]['numeric_bins'])
        assert expected==r['transform'] and date_hash(d['dates'][tr])==r['identity']['train_hash']
        b=pickle.loads((OUT/'checkpoints'/(r['key']+'.pkl')).read_bytes())
        models.audit(b['model'],d['z'][tr],r['name'],b['transform'])
    from .run import select_configurations
    screen=pd.read_csv(OUT/'inner_selection_scores.csv').to_dict('records')
    assert select_configurations(screen)==json.loads((OUT/'selected_configurations.json').read_text())['chosen']
    surface=pd.read_csv(OUT/'continuous_total_surface.csv');zz=np.sort(surface.Z0.unique())
    expected=models.predict(load_bundle('D_FULL',models.IDS[3])[0],zz)
    surface_error=float(abs(surface.pivot(index='Z0',columns='bin',values='prediction').to_numpy()-expected).max())
    assert surface_error<1e-10
    rew=pd.read_csv(OUT/'environment_reference_reweighted.csv')
    assert (rew[rew.environment==2020].status=='ABSTAIN_SUPPORT').all()
    assert rew[rew.environment==2020].reweighted_raw_TV.isna().all()
    fi,fp,fl=get_context(d,'D_FULL');ref=d['dates'][fi]<'2020-01-01';year=np.char.startswith(d['dates'][fi],'2021')
    weights=np.array([np.mean(fl[ref]==g) for g in range(3)])
    daily_weights=np.array([weights[g]/np.sum(year&(fl==g)) for g in fl[year]])
    raw_difference=daily_weights@d['q'][fi][year]-d['q'][fi][ref].mean(axis=0)
    reweight_error=0.
    for name,p in fp.items():
        residual=d['q'][fi]-p
        value=float(abs(daily_weights@residual[year]-residual[ref].mean(axis=0)).sum()/2)
        row=rew[(rew.model==name)&(rew.environment==2021)].iloc[0]
        reweight_error=max(reweight_error,abs(value-row.reweighted_residual_half_L1),abs(abs(raw_difference).sum()/2-row.reweighted_raw_TV))
    assert reweight_error<1e-10
    m8=[json.loads((OUT/(c+'__M8.json')).read_text()) for c in ['D_FULL','DEV_2020','DEV_2021']]
    assert all(m['success'] and m['gradient_max']<2e-6 for m in m8)
    prior=json.loads((OUT/'QA_C3.json').read_text()) if (OUT/'QA_C3.json').exists() else {}
    qa=dict(prior,status='C3_PASS_WITH_QUALIFICATIONS',native_fits=len(records),M8_fits=3,protected_files=len(baseline),protected_changed=changed,
        protocol_sha256=digest(CONFIG),cohort_sha256=date_hash(d['dates']),source_n=1472,forecast_n=489,
        no_internal_validation=True,time78_main_and_pair=True,exact_graphs=True,prediction_reload_error=maxparity,C2R_reference_parity_error=c2r_error,
        plot_numeric_reconciliation_error=maxplot,surface_reconciliation_error=surface_error,
        all_training_transforms_reconstructed=True,reference_reweight_parity_error=reweight_error,no_population_ci=True,network_bytes=0,
        new_source_bytes=0,retained_bytes=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),
        native_fit_seconds=sum(r['wall_seconds'] for r in records),peak_rss_bytes=max(prior.get('peak_rss_bytes',0),max(r['peak_rss_bytes'] for r in records),
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)),
        not_performed=['native LOYO','full-selection learner bootstrap','population/raw singleton confidence intervals'],
        count_note='59 empirical native fits; synthetic compatibility/unit fits separately logged; no empirical fit retries')
    if (OUT/'plots_manifest.json').exists():
        from PIL import Image
        figures=json.loads((OUT/'plots_manifest.json').read_text())
        for fig in figures:
            path=ROOT/fig['path'];assert digest(path)==fig['sha256']
            with Image.open(path) as im:assert im.width>=1600 and np.asarray(im.convert('RGB')).std()>5
        assert len(figures)>=17
        qa.update(figures=len(figures),PNG_decode_nonblank=True)
    if (OUT/'visual_review.json').exists():
        qa['visual_review']=json.loads((OUT/'visual_review.json').read_text())['verdict']
    if (OUT/'tests_all.log').exists():
        testlog=(OUT/'tests_all.log').read_text()
        if re.search(r'Ran 62 tests.*?\nOK',testlog,re.S):qa.update(unit_tests_passed=62,unit_tests_status='PASS')
    write_json(OUT/'QA_C3.json',qa)
    write_json(OUT/'run_source_config_environment_hashes.json',dict(protocol_sha256=digest(CONFIG),source=d['identities'],versions=cfg['versions'],
        code={str(p.relative_to(ROOT)):digest(p) for p in Path(__file__).parent.glob('*.py')},cohort=date_hash(d['dates']),
        read_ledger=d['read_ledger'],network_bytes=0,C2R_manifest=digest(REF/'files_manifest.json')))
    print('QA',qa,flush=True)
