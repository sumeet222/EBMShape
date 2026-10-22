"""Complete requested C2R calibration/conditional-mean audits from saved fits.

This post-fit audit changes no coefficient, candidate, cutoff, basis or forecast.
It adds conditional group-mean intervals, residual calibration/period summaries
and explicit train/backcheck gaps using the already frozen methods.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .readiness import ROOT, digest, transform_s0
from .c2r_models import SCALAR_IDS, scalar_design, calendar_hac
from .c2r_diagnostics import linear_contrast
from .c2r_development import OUT, load_inputs, no_network, save_csv, write_json
from .c2r_reporting import table


def calibration_rows(fitted,residual,context,model):
    """Fixed quintiles with explicit empty-bin status when fitted values tie."""
    fitted,residual=np.asarray(fitted),np.asarray(residual)
    cuts=np.quantile(fitted,[.2,.4,.6,.8]);bins=np.searchsorted(cuts,fitted,side='right')
    rows=[]
    for b in range(5):
        m=bins==b;n=int(m.sum())
        rows.append(dict(context=context,model=model,bin=b,n_days=n,
            fitted_mean_pp=float(fitted[m].mean()*100) if n else np.nan,
            observed_mean_pp=float((fitted[m]+residual[m]).mean()*100) if n else np.nan,
            residual_mean_pp=float(residual[m].mean()*100) if n else np.nan,
            status='AVAILABLE' if n else 'ABSTAIN_EMPTY_BIN_FROM_FITTED_VALUE_TIES'))
    return rows


def chronological_periods(frame):
    """Sort numeric period keys as time indices, never lexicographically."""
    return frame.assign(period_index=frame.period.astype(int)).sort_values('period_index')


def complete():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image,ImageOps,ImageDraw
    d=load_inputs();q,z,dates,slots=d['q'],d['z'],d['dates'],d['slots']
    parameters=json.loads((OUT/'model_parameters.json').read_text())
    parameter_hash=digest(OUT/'model_parameters.json');prediction_hash=digest(OUT/'chronological_predictions.npz')
    conditional=[];period=[];calibration=[];inventory=[]
    scalar_all=pd.read_csv(OUT/'scalar_residual_influence.csv')
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        par=parameters[context];t=par['transform'];mask=np.isin(dates,par['train_dates'])
        state=transform_s0(z[mask],t['S0']);zs=(z[mask]-t['mean'])/t['sd']
        for name in SCALAR_IDS:
            x,_=scalar_design(zs,state,name);beta=np.asarray(par['models'][name]['coef']);resid=q[mask,66:78].sum(axis=1)-x@beta
            n,p=x.shape;ordinary=(resid@resid)/(n-p)*np.linalg.inv(x.T@x)
            for lag in [0,5,10,20]:
                cov=ordinary if lag==0 else calendar_hac(x,resid,slots[mask],lag)
                for group in range(3):
                    cell=state==group;c=x[cell].mean(axis=0);r=linear_contrast(beta,cov,c)
                    conditional.append(dict(context=context,model=name,state=group,n_group=int(cell.sum()),lag=lag,
                        mean_pp=r['estimate']*100,SE_pp=r['se']*100,lo_pp=r['lo']*100,hi_pp=r['hi']*100,
                        scope='training same-cell mean of fitted closing shares; conditional on cuts/design; not prediction interval'))
            sf=scalar_all[(scalar_all.context==context)&(scalar_all.model==name)].sort_values('date_et')
            train_slots=np.array([slots[np.flatnonzero(dates==day)[0]] for day in sf.date_et])
            for kind,keys in [('year',sf.date_et.str[:4].to_numpy()),('scheduled_index_block5',(train_slots//5).astype(str))]:
                for key in np.unique(keys):
                    m=keys==key;v=sf.residual.to_numpy()[m]
                    period.append(dict(context=context,model=name,period_type=kind,period=str(key),n_days=int(m.sum()),
                        residual_mean_pp=float(v.mean()*100),residual_SD_pp=float(v.std(ddof=1)*100) if m.sum()>1 else np.nan))
            # Fixed five fitted-value quantile bins: descriptive calibration,
            # not a target-chosen smoothing bandwidth or extra model.
            calibration.extend(calibration_rows(sf.fitted.to_numpy(),sf.residual.to_numpy(),context,name))
        for part,key in [('TRAIN','train_dates'),('EVAL','forecast_dates')]:
            m=np.isin(dates,par[key]);values=z[m]
            inventory.append(dict(context=context,part=part,n_days=int(m.sum()),Z0_min=float(values.min()),Z0_max=float(values.max()),
                low_cut=t['S0']['cuts'][0],high_cut=t['S0']['cuts'][1],
                q10=float(np.quantile(values,.1)),q25=float(np.quantile(values,.25)),q50=float(np.quantile(values,.5)),
                q75=float(np.quantile(values,.75)),q90=float(np.quantile(values,.9)),
                out_of_training_range_n=int(((values<t['training_range'][0])|(values>t['training_range'][1])).sum())))
    save_csv('scalar_conditional_means_and_hac',conditional);save_csv('scalar_residual_period_means',period)
    save_csv('scalar_calibration',calibration);save_csv('origin_state_inventory',inventory)
    scores=pd.read_csv(OUT/'model_scores.csv');gaps=[]
    for context in ['DEV_2020','DEV_2021']:
        train=scores[(scores.context==context)&(scores.part=='TRAIN')].set_index('model')
        ev=scores[(scores.context==context)&(scores.part=='EVAL')].set_index('model')
        for name in train.index:
            gaps.append(dict(context=context,model=name,train_n=int(train.loc[name,'n_days']),eval_n=int(ev.loc[name,'n_days']),
                close_MSE_gap=float(ev.loc[name,'CLOSE_C_MSE']-train.loc[name,'CLOSE_C_MSE']),
                profile_MSE_gap=float(ev.loc[name,'MSE_profile']-train.loc[name,'MSE_profile']) if pd.notna(train.loc[name,'MSE_profile']) else np.nan))
    save_csv('model_train_eval_gaps',gaps)
    # Same-coarse-cell residual environmental shifts. Residual vectors are not
    # probability vectors; their distance is half-L1, not probability TV.
    with np.load(OUT/'descriptive_predictions.npz') as f:pred={str(name):f['profile_predictions'][i] for i,name in enumerate(f['profile_models'])}
    early=dates<'2020';bins=np.searchsorted(parameters['DEV_2020']['transform']['quintile_cuts'],z,side='right');envres=[]
    for year in [2020,2021]:
        env=np.char.startswith(dates,str(year))
        for cell in range(5):
            a=early&(bins==cell);b=env&(bins==cell)
            ok=all(m.sum()>=50 and len(set(slots[m]//5))>=20 for m in [a,b])
            for name in ['M0','P-OLS-Z','M4-T8-Z4']:
                residual=q-pred[name]
                value=float(abs(residual[a].mean(axis=0)-residual[b].mean(axis=0)).sum()/2) if ok else np.nan
                envres.append(dict(environment=year,cell=cell,model=name,n_early=int(a.sum()),n_environment=int(b.sum()),
                    residual_half_L1_shift=value,status='SUPPORTED_DESCRIPTIVE_COARSE_CELL' if ok else 'ABSTAIN_SUPPORT',
                    caveat='D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift'))
    save_csv('environment_residual_discrepancy',envres)
    daily=pd.read_csv(OUT/'profile_daily_errors.csv');state_errors=daily.groupby(['context','part','model','state'],as_index=False).agg(
        n_days=('date_et','count'),MSE_profile=('MSE_profile','mean'),MAE_profile=('MAE_profile','mean'),
        close_residual_mean=('close_residual','mean'),vector_norm_mean=('vector_norm','mean'),vector_norm_max=('vector_norm','max'))
    state_errors.to_csv(OUT/'profile_errors_by_state.csv',index=False,float_format='%.17g')
    pdiag=pd.read_csv(OUT/'profile_diagnostics.csv');reg=pd.read_csv(OUT/'model_registry.csv');evdiag=pdiag[pdiag.part=='EVAL']
    # Explicit development-tail normalization and extrapolation review.
    sf=scalar_all[(scalar_all.context=='D_FULL')&(scalar_all.model=='OLS-L1')].sort_values('date_et')
    cal=pd.DataFrame(calibration);cal=cal[(cal.context=='D_FULL')&(cal.model=='OLS-L1')]
    per=pd.DataFrame(period);per=per[(per.context=='D_FULL')&(per.model=='OLS-L1')]
    fig,axs=plt.subplots(2,2,figsize=(14,10))
    axs[0,0].plot(cal.fitted_mean_pp,cal.observed_mean_pp,'o-',label='bin means');lo=min(cal.fitted_mean_pp.min(),cal.observed_mean_pp.min());hi=max(cal.fitted_mean_pp.max(),cal.observed_mean_pp.max());axs[0,0].plot([lo,hi],[lo,hi],'--',color='gray');axs[0,0].set(xlabel='Fitted mean closing share (%)',ylabel='Observed mean closing share (%)',title='Fixed five-bin residual calibration')
    annual=per[per.period_type=='year'];axs[0,1].bar(annual.period,annual.residual_mean_pp);axs[0,1].axhline(0,color='black');axs[0,1].set(ylabel='Residual mean (pp)',title='Year residual means')
    block=chronological_periods(per[per.period_type=='scheduled_index_block5']);axs[1,0].plot(block.period_index,block.residual_mean_pp,'.-',lw=.6);axs[1,0].axhline(0,color='black');axs[1,0].set(xlabel='Original scheduled-session index // 5',ylabel='Residual mean (pp)',title='Five-session block means (gaps preserved)')
    from statsmodels.tsa.stattools import pacf
    pc=pacf(sf.residual,nlags=20,method='ywm');axs[1,1].bar(range(1,21),pc[1:]);axs[1,1].set(xlabel='Eligible-observation lag',ylabel='Partial autocorrelation',title='PACF (descriptive, not calendar-gap HAC)')
    fig.suptitle('Additional requested scalar calibration and period diagnostics · D_FULL OLS-L1 n=1,472',fontsize=15)
    fig.text(.5,.008,'Explored SPY development · fixed fitted coefficients · no new model or outcome/source selection',ha='center',fontsize=10)
    fig.tight_layout(rect=[0,.025,1,.95]);path=OUT/'figures/14_scalar_calibration_period_means_and_PACF.png';fig.savefig(path,dpi=160);plt.close(fig)
    with Image.open(path) as im:
        im.load();assert im.width>=1600 and np.asarray(im).std()>5
        ref=dict(path=path.relative_to(ROOT).as_posix(),sha256=digest(path),width=im.width,height=im.height,n_dates=1472,
                 data_sources=['scalar_calibration.csv','scalar_residual_period_means.csv','scalar_residual_influence.csv','serial_diagnostics.csv'],
                 numeric_QA='derived from verified saved scalar coefficients/residuals, no refit')
    manifest=json.loads((OUT/'plots_manifest.json').read_text());manifest['figures']=[v for v in manifest['figures'] if Path(v['path']).name!=path.name]+[ref]
    # Make the normal-QQ unit explicit: all other residual panels use pp.
    from scipy import stats
    fig,axs=plt.subplots(2,2,figsize=(13,9));e=sf.residual.to_numpy();fitted=sf.fitted.to_numpy()
    axs[0,0].scatter(fitted*100,e*100,s=8,alpha=.35);axs[0,0].axhline(0,color='black');axs[0,0].set(xlabel='Fitted closing share (%)',ylabel='Residual (pp)',title='OLS-L1 residual vs fit')
    axs[0,1].scatter(z,e*100,s=8,alpha=.35);axs[0,1].axhline(0,color='black');axs[0,1].set(xlabel='Z0',ylabel='Residual (pp)',title='Residual vs prior state')
    stats.probplot(e,dist='norm',plot=axs[1,0]);axs[1,0].set(title='Normal QQ: descriptive tails',ylabel='Residual (fraction of daily RV)',xlabel='Theoretical normal quantile')
    axs[1,1].hist(e*100,bins=45,color='#0072B2');axs[1,1].set(xlabel='Residual (pp)',ylabel='Dates',title='No trimming of scalar residuals')
    fig.suptitle('D_FULL OLS-L1 residuals: shape and heavy tails',fontsize=15);fig.text(.5,.008,'SPY split-only RV allocation · 2016–2021 explored development · n=1,472 dates',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.025,1,.95]);qqpath=OUT/'figures/04_scalar_OLS_residual_and_QQ.png';fig.savefig(qqpath,dpi=160);plt.close(fig)
    for item in manifest['figures']:
        if Path(item['path']).name==qqpath.name:
            item.update(sha256=digest(qqpath),width=2080,height=1440,numeric_QA='same saved residuals; QQ fraction versus pp axis units explicit')
    write_json(OUT/'plots_manifest.json',manifest)
    thumbs=[]
    for ref in manifest['figures']:
        with Image.open(ROOT/ref['path']) as im:
            tile=Image.new('RGB',(660,465),'white');thumb=ImageOps.contain(im.convert('RGB'),(640,430));tile.paste(thumb,((660-thumb.width)//2,25));ImageDraw.Draw(tile).text((8,5),Path(ref['path']).name,fill='black');thumbs.append(tile)
    sheet=Image.new('RGB',(1980,2325),'#dddddd')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*660,(i//3)*465))
    sheet.save(OUT/'figures/contact_sheet.png')
    main=ROOT/'reports/C/C2R_OLS_state_dependent_splines_full_diagnostics.md'
    marker='\n## Completion of conditional means, calibration and environment residual audits\n'
    before=main.read_text().split(marker)[0]
    appendix=marker+'''
These requested diagnostics use the saved frozen coefficients and original dated arrays, **without refitting or changing any candidate/forecast**. Group-mean intervals condition on the fitted training cuts/design; they are conditional-mean estimation intervals, not individual-day prediction intervals or selection-aware confidence statements. The direct P0 fixed-label reference and origin-training model S0 remain distinct.

'''+table(pd.DataFrame(conditional).query("context == 'D_FULL' and lag == 10"),['model','state','n_group','mean_pp','SE_pp','lo_pp','hi_pp'])
    appendix+='\nAll ordinary/HAC5/10/20 group means for the three core training contexts are in `scalar_conditional_means_and_hac.csv`. Fixed fitted-value quintile calibration, year and scheduled-five-session block residual means are in `scalar_calibration.csv` and `scalar_residual_period_means.csv`; figure14 displays them and PACF. Train/eval error/bias gaps, exact origin state ranges/cuts/quantiles and state-specific vector errors are in `model_train_eval_gaps.csv`, `origin_state_inventory.csv` and `profile_errors_by_state.csv`.\n\n'
    appendix+=table(pd.DataFrame(inventory))
    appendix+='\nRaw normalization on **each chronological evaluation** (including state extrapolation) follows. TV scores only cover simplex-valid dates; half-L1 always covers all dates.\n\n'+table(evdiag,['context','model','n_days','TV_valid_n','negative_below_tolerance','prediction_min','sum_defect_max'])
    appendix+='\nResidual environment discrepancies are in `environment_residual_discrepancy.csv`: same 2016–2019 training-defined coarse quintile cells and the same D_FULL fitted model, basic-support masks enforced. Residual vectors are not probability curves, so the statistic is explicitly **residual half-L1 shift**, not probability TV. It remains descriptive; numeric state distributions can differ inside a cell, and the shared full-development fit is not independent. No reweighting or causal attribution is implied.\n\n'
    appendix+=table(pd.DataFrame(envres))
    main.write_text(before+appendix)
    gallery=ROOT/'reports/C/C2R_scientific_visual_gallery.md'
    content=gallery.read_text().split('\n## 14_scalar_calibration_period_means_and_PACF.png')[0]
    content+='\n## 14_scalar_calibration_period_means_and_PACF.png\n\n![Scalar calibration and temporal residual means](../../artifacts/C/C2R_development_v1_1/figures/14_scalar_calibration_period_means_and_PACF.png)\n\nFitted-value quintile calibration and residual year/five-session means expose departures obscured by an average zero residual. The PACF is a daily-series descriptive check. These diagnostics preserve every fitted coefficient and do not add a candidate model or choose a new transformation from outcomes. Conditional group-mean intervals and chronological extrapolation/normalization are tabulated in the main report.\n'
    gallery.write_text(content)
    assert parameter_hash==digest(OUT/'model_parameters.json') and prediction_hash==digest(OUT/'chronological_predictions.npz')
    qa=json.loads((OUT/'provenance_and_QA.json').read_text());qa.update(plots=14,completion_diagnostics='PASS: saved coefficients, no new fits',
        completion_code_sha256=digest(Path(__file__)),coefficient_and_forecast_hashes_unchanged=True,
        chronological_normalization={'invalid_dates_by_model_context':evdiag[['context','model','n_days','TV_valid_n']].to_dict('records')})
    write_json(OUT/'provenance_and_QA.json',qa)
    print('C2R_COMPLETION_PASS; conditional means/calibration/environment residuals; 14 figures; no refitting')


if __name__=='__main__':
    with no_network():complete()
