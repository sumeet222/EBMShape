"""C2R scientific figures, independent saved-output checks and human reports."""
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd
from scipy import stats

from .c2r_models import Model, PROFILE_IDS, SCALAR_IDS, profile_losses
from .readiness import ROOT, P0, WINDOWS, digest, transform_s0

OUT=ROOT/'artifacts/C/C2R_development_v1_1'
REPORTS=ROOT/'reports/C'


def table(frame,columns=None,limit=None):
    frame=frame[columns] if columns else frame
    if limit:frame=frame.head(limit)
    def f(v):
        if isinstance(v,(float,np.floating)):return f'{v:.6g}' if np.isfinite(v) else 'NA / ABSTAIN'
        return str(v).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(frame.columns)+' |\n|'+'|'.join(['---']*len(frame.columns))+'|\n'+'\n'.join('| '+' | '.join(f(v) for v in row)+' |' for row in frame.itertuples(index=False,name=None))+'\n'


def render():
    from .c2r_development import load_inputs, write_json, CONFIG
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image,ImageOps,ImageDraw
    started=time.perf_counter();d=load_inputs();q=d['q'];z=d['z'];dates=d['dates'];labels=d['labels']
    qa=json.loads((OUT/'provenance_and_QA.json').read_text());cfg=json.loads(CONFIG.read_text());parameters=json.loads((OUT/'model_parameters.json').read_text())
    frames={p.stem:pd.read_csv(p) for p in OUT.glob('*.csv')}
    with np.load(OUT/'descriptive_predictions.npz') as f:dp={k:f[k] for k in f.files}
    with np.load(OUT/'chronological_predictions.npz') as f:cp={k:f[k] for k in f.files}
    with np.load(OUT/'plot_data.npz') as f:plots={k:f[k] for k in f.files}
    pred={name:dp['profile_predictions'][i] for i,name in enumerate(dp['profile_models'])}
    scalar={name:dp['scalar_predictions'][i] for i,name in enumerate(dp['scalar_models'])}
    # Independently recompute every saved core/pooled train/development score.
    score_checks=0
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        ps=parameters[context];t=ps['transform'];train=np.isin(dates,ps['train_dates']);ev=np.isin(dates,ps['forecast_dates'])
        for name,v in ps['models'].items():
            model=Model(name,np.array(v['coef']),v['metadata'])
            for part,mask in [('TRAIN',train),('EVAL',ev)]:
                prediction=model.predict(z[mask],t);row=frames['model_scores'][(frames['model_scores'].context==context)&(frames['model_scores'].part==part)&(frames['model_scores'].model==name)].iloc[0]
                close_error=q[mask,66:78].sum(axis=1)-(prediction if name in SCALAR_IDS else prediction[:,66:78].sum(axis=1))
                np.testing.assert_allclose(row.CLOSE_C_MSE,np.mean(close_error**2),atol=1e-12,rtol=1e-10)
                if name not in SCALAR_IDS:np.testing.assert_allclose(row.MSE_profile,np.mean((q[mask]-prediction)**2),atol=1e-12,rtol=1e-10)
                score_checks+=1
    idx=np.array([np.flatnonzero(dates==day)[0] for day in cp['dates']])
    for i,name in enumerate(cp['profile_models']):
        row=frames['model_scores'][(frames['model_scores'].context=='DEV_POOLED_2020_2021')&(frames['model_scores'].model==name)].iloc[0]
        np.testing.assert_allclose(row.MSE_profile,np.mean((q[idx]-cp['profile_predictions'][i])**2),atol=1e-12)
    direct=frames['direct_profiles'];historical=direct[(direct.context=='D_FULL')&(direct.label=='P0_D_ONLY')]
    for g in range(3):
        np.testing.assert_allclose(historical[historical.state==g].sort_values('bin')['mean'],q[labels==g].mean(axis=0),atol=1e-10,rtol=0)
    fidelity=frames['model_fidelity_by_state_bin']
    for name in PROFILE_IDS:
        for g in range(3):
            rows=fidelity[(fidelity.model==name)&(fidelity.cell_type=='P0_RETROSPECTIVE_S0')&(fidelity.cell==g)].sort_values('bin')
            np.testing.assert_allclose(rows.raw_mean,q[labels==g].mean(axis=0),atol=1e-10,rtol=0)
            np.testing.assert_allclose(rows.fitted_mean,pred[name][labels==g].mean(axis=0),atol=1e-10,rtol=0)
    scalar_full=frames['scalar_residual_influence'];scalar_full=scalar_full[(scalar_full.context=='D_FULL')&(scalar_full.model=='OLS-L1')].sort_values('date_et')
    np.testing.assert_allclose(scalar_full.fitted+scalar_full.residual,q[:,66:78].sum(axis=1),atol=1e-10)
    t=parameters['D_FULL']['transform'];dense=np.linspace(z.min(),z.max(),500)
    restored={name:Model(name,np.array(v['coef']),v['metadata']) for name,v in parameters['D_FULL']['models'].items()}
    colors=['#0072B2','#009E73','#D55E00'];state_names=['low','middle','high']
    figdir=OUT/'figures';figdir.mkdir(exist_ok=True);manifest=[];extra={}
    plt.rcParams.update({'font.size':11,'axes.titlesize':12,'axes.labelsize':11,'legend.fontsize':9})
    ticks=[0,6,18,30,42,54,66,77];clock=['09:30','10:00','11:00','12:00','13:00','14:00','15:00','15:55']
    def time_axis(ax):
        ax.set_xticks(ticks,clock);ax.set_xlabel('Five-minute bin start, America/New_York');ax.grid(alpha=.2)
    def save(fig,name,title,sources):
        fig.suptitle(title,fontsize=15)
        fig.text(.5,.008,'SPY split-only RV allocation · 2016–2021 explored development · day is the uncertainty unit · no independent C evaluation',ha='center',fontsize=9)
        fig.tight_layout(rect=[0,.025,1,.95]);path=figdir/name;fig.savefig(path,dpi=160);plt.close(fig)
        with Image.open(path) as im:
            im.load();assert im.width>=1600 and np.asarray(im).std()>5
            manifest.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=digest(path),width=im.width,height=im.height,n_dates=1472,
                                 data_sources=sources,numeric_QA='saved arrays/tables independently reconciled; not pixel OCR'))
    fig,axs=plt.subplots(1,3,figsize=(18,5.6),sharey=True)
    for ax,(context,label) in zip(axs,[('D_FULL','P0_D_ONLY'),('DEV_2020','ORIGIN_TRAIN_S0'),('DEV_2021','ORIGIN_TRAIN_S0')]):
        subset=direct[(direct.context==context)&(direct.label==label)]
        for g,color in enumerate(colors):
            row=subset[subset.state==g].sort_values('bin');ax.plot(row.bin,row['mean']*100,color=color,label=f'{state_names[g]} n={row.n.iloc[0]}')
        ax.set_title(context+'\n'+label);time_axis(ax);ax.legend()
    axs[0].set_ylabel('Mean daily RV allocation per bin (%)')
    save(fig,'01_direct_three_state_profiles.png','Direct profiles: historical P0 labels versus origin-training categories',['direct_profiles.csv','P0 NPZ'])
    fig,axs=plt.subplots(2,1,figsize=(12,8),sharex=True,gridspec_kw={'height_ratios':[3,1]})
    origin_labels=transform_s0(z,t['S0']);close=q[:,66:78].sum(axis=1)
    for g,color in enumerate(colors):axs[0].scatter(z[origin_labels==g],close[origin_labels==g]*100,s=7,alpha=.35,color=color,label=f'{state_names[g]} n={(origin_labels==g).sum()}')
    for name,ls in [('OLS-L1','-'),('OLS-L3','--'),('OLS-L4',':')]:axs[0].plot(dense,restored[name].predict(dense,t)*100,ls=ls,lw=2,label=name)
    axs[0].set_ylabel('15:00–16:00 share (% of daily RV)');axs[0].legend(ncol=2);axs[0].grid(alpha=.2)
    axs[1].hist(z,bins=35,color='#777777');axs[1].set_xlabel('Z0 = log(previous scheduled full-session RV)');axs[1].set_ylabel('Dates')
    save(fig,'02_closing_share_scatter_and_state_OLS.png','D_FULL n=1,472: scalar association and piecewise/quadratic alternatives',['daily_design_index.csv','model_parameters.json'])
    co=frames['scalar_ols_models_and_hac'];tests=frames['scalar_specification_tests'];family=tests[(tests.context=='D_FULL')&tests.p_holm_fixed_six_family.notna()]
    fig,axs=plt.subplots(1,2,figsize=(16,7),gridspec_kw={'width_ratios':[1.3,1]})
    terms=[('OLS-L1','z_s'),('OLS-L3','slope_state_0'),('OLS-L3','slope_state_1'),('OLS-L3','slope_state_2'),('OLS-L4','z_s^2')]
    for off,lag in zip([-.2,0,.2],[5,10,20]):
        rows=[co[(co.context=='D_FULL')&(co.model==m)&(co.term==term)&(co.lag==lag)].iloc[0] for m,term in terms]
        means=np.array([r.estimate for r in rows])*100;lo=np.array([r.lo for r in rows])*100;hi=np.array([r.hi for r in rows])*100
        axs[0].errorbar(means,np.arange(len(terms))+off,xerr=[means-lo,hi-means],fmt='o',capsize=3,label=f'HAC {lag}')
    axs[0].set_yticks(range(len(terms)),[m+' / '+term for m,term in terms]);axs[0].axvline(0,color='gray');axs[0].legend();axs[0].set_xlabel('Closing allocation pp per standardized design unit')
    text='Fixed six-test D_FULL family (HAC10)\n\n'+'\n'.join(f'{r.test}\n p={r.p_value:.4g}; Holm={r.p_holm_fixed_six_family:.4g}' for _,r in family.iterrows())
    axs[1].axis('off');axs[1].text(0,1,text,va='top',fontsize=11);axs[1].text(0,0,'Conditional exploratory p-values.\nHolm does not undo P0 selection.\nRaw H1>0 differs from H1>2 pp.',va='bottom')
    save(fig,'03_OLS_estimates_and_interaction_tests.png','Scalar daily OLS: slopes, curvature and joint moderation tests',['scalar_ols_models_and_hac.csv','scalar_specification_tests.csv'])
    e=scalar_full.residual.to_numpy();fitted=scalar_full.fitted.to_numpy()
    fig,axs=plt.subplots(2,2,figsize=(13,9))
    axs[0,0].scatter(fitted*100,e*100,s=8,alpha=.35);axs[0,0].axhline(0,color='black');axs[0,0].set(xlabel='Fitted closing share (%)',ylabel='Residual (pp)',title='OLS-L1 residual vs fit')
    axs[0,1].scatter(z,e*100,s=8,alpha=.35);axs[0,1].axhline(0,color='black');axs[0,1].set(xlabel='Z0',ylabel='Residual (pp)',title='Residual vs prior state')
    stats.probplot(e,dist='norm',plot=axs[1,0]);axs[1,0].set_title('Normal QQ: descriptive tails')
    axs[1,1].hist(e*100,bins=45,color=colors[0]);axs[1,1].set(xlabel='Residual (pp)',ylabel='Dates',title='No trimming of scalar residuals')
    save(fig,'04_scalar_OLS_residual_and_QQ.png','D_FULL OLS-L1 residuals: shape and heavy tails',['scalar_residual_influence.csv'])
    fig,axs=plt.subplots(2,2,figsize=(14,9))
    axs[0,0].plot(pd.to_datetime(dates),e*100,lw=.6);axs[0,0].axhline(0,color='black');axs[0,0].set(ylabel='Residual (pp)',title='Residual chronology; omitted crisis sessions unavailable')
    axs[0,1].bar(range(1,21),plots['scalar_acf'][1:],label='residual ACF');axs[0,1].plot(range(1,21),plots['scalar_squared_acf'][1:],'o-',label='squared residual ACF');axs[0,1].set(xlabel='Eligible-observation lag',title='Descriptive serial dependence');axs[0,1].legend()
    axs[1,0].boxplot([e[origin_labels==g]*100 for g in range(3)],tick_labels=state_names,showfliers=True);axs[1,0].set(ylabel='Residual (pp)',title='Origin-defined state dispersion')
    years=np.array([int(x[:4]) for x in dates]);variances=[np.var(e[years==y]*100,ddof=1) for y in range(2016,2022)]
    axs[1,1].bar(range(2016,2022),variances);axs[1,1].set(ylabel='Variance (pp²)',title='Year heteroskedasticity')
    extra['scalar_year_variances_pp2']=variances
    save(fig,'05_scalar_OLS_residual_time_ACF_and_variance.png','Daily residual serial and variance diagnostics (ACF gaps compressed; HAC uses scheduled gaps)',['scalar_residual_influence.csv','serial_diagnostics.csv','plot_data.npz'])
    contrasts=frames['contrasts_and_materiality'];sens=contrasts[(contrasts.model=='RAW_P0_LABELS')&(contrasts.window=='CLOSE_C')]
    top=scalar_full.nlargest(10,'cooks')
    fig,axs=plt.subplots(1,3,figsize=(18,6))
    axs[0].barh(top.date_et.iloc[::-1],top.cooks.iloc[::-1]);axs[0].set(xlabel="Cook's distance",title='Top ten OLS-L1 influential dates')
    axs[1].scatter(scalar_full.hat,scalar_full.student_external,c=np.log10(np.maximum(scalar_full.cooks,1e-12)),s=12,cmap='viridis');axs[1].set(xlabel='Hat diagonal',ylabel='External studentized residual',title='Leverage and unusual closing shares')
    axs[2].bar(range(len(sens)),sens.estimate_pp,color=colors[0]);axs[2].set_xticks(range(len(sens)),sens.context,rotation=35,ha='right');axs[2].axhline(2,color='red',ls='--',label='2 pp reference');axs[2].set(ylabel='Raw H−L closing share (pp)',title='Fixed P0 labels; sensitivities never replace FULL');axs[2].legend()
    save(fig,'06_influence_and_robustness.png','Influence and declared retrospective exclusions',['scalar_residual_influence.csv','contrasts_and_materiality.csv'])
    fig,axs=plt.subplots(1,2,figsize=(15,6))
    for name in ['M0','M2-T8','M2-T12']:axs[0].plot(np.arange(78),pred[name].mean(axis=0)*100,label=name)
    axs[0].set_ylabel('Mean bin allocation (%)');axs[0].set_title('Categorical time baseline vs low-df smoothers')
    for g,color in enumerate(colors):axs[1].plot(plots['P0_raw_means'][g]*100,color=color,label=f'P0 {state_names[g]}')
    axs[1].plot(pred['M2-T8'][0]*100,color='black',ls='--',label='M2-T8, same curve for every state')
    for ax in axs:time_axis(ax);ax.legend()
    save(fig,'07_M0_M1_M2_profile_fit.png','Time smoothing and direct conditional curves: inspect the 15:55 peak',['direct_profiles.csv','descriptive_predictions.npz'])
    fig,axs=plt.subplots(1,3,figsize=(18,6))
    for i,p in enumerate([.1,.25,.5,.75,.9]):axs[0].plot(plots['grid_P-OLS-Z'][i]*100,label=f'train q{int(p*100)}')
    axs[0].set_title('Linear time-bin × numerical Z0');axs[0].set_ylabel('Allocation per bin (%)');axs[0].legend()
    axs[1].plot(plots['raw_HL']*100,label='raw P0 H−L');axs[1].plot(plots['HL_P-OLS-Z']*100,label='whole-fit same-cell H−L');axs[1].set_title('Same observed coarse cells');axs[1].set_ylabel('H−L allocation (pp)');axs[1].legend()
    axs[2].plot(plots['raw_anchored']*100,label='raw');axs[2].plot(plots['anchored_P-OLS-Z']*100,label='P-OLS-Z');axs[2].set_title('Anchored D, k0=30 (12:00)');axs[2].set_ylabel('Anchored contrast (pp)');axs[2].legend()
    for ax in axs:time_axis(ax)
    save(fig,'08_state_dependent_profile_OLS.png','Interpretive linear profile coefficients: whole curves and anchored contrast',['plot_data.npz','model_parameters.json','model_fidelity_by_state_bin.csv'])
    fig=plt.figure(figsize=(14,10));gs=fig.add_gridspec(2,2,width_ratios=[4,1]);ax=fig.add_subplot(gs[0,0]);density=fig.add_subplot(gs[0,1]);slices=fig.add_subplot(gs[1,:])
    mesh=ax.pcolormesh(np.arange(78),plots['heat_z'],plots['heat_M4-T8-Z4']*100,shading='auto',cmap='viridis');fig.colorbar(mesh,ax=ax,label='Raw mean allocation per bin (%)');time_axis(ax);ax.set_ylabel('Numeric Z0');ax.set_title('D_FULL 8×4 tensor; supported local training bands')
    density.hist(z,bins=35,orientation='horizontal',color='#777777');density.set_xlabel('Dates');density.set_ylim(ax.get_ylim())
    for i,p in enumerate([.1,.25,.5,.75,.9]):slices.plot(plots['grid_M4-T8-Z4'][i]*100,label=f'training q{int(p*100)} Z0={plots["grid_z"][i]:.2f}')
    time_axis(slices);slices.set_ylabel('Raw allocation per bin (%)');slices.legend(ncol=3)
    save(fig,'09_M4_continuous_state_heatmap.png','Continuous prior-state spline surface; singleton queries are fitted values, not identified raw point means',['plot_data.npz','support_and_environment.csv'])
    fig,axs=plt.subplots(1,2,figsize=(15,6))
    for name in ['raw','P-OLS-Z','M4-T8-Z4']:
        delta=plots['raw_HL' if name=='raw' else 'HL_'+name];axs[0].plot(delta*100,label=name)
    time_axis(axs[0]);axs[0].set_ylabel('H−L allocation (pp per bin)');axs[0].set_title('Same P0 high/low rows, whole predictions');axs[0].legend()
    for j,name in enumerate(['P-OLS-Z','M4-T8-Z4','M4-T12-Z4']):
        rows=contrasts[(contrasts.context=='D_FULL')&(contrasts.model==name)].set_index('window')
        axs[1].bar(np.arange(3)+(j-1)*.23,[rows.loc[w,'difference_pp'] for w in ['OPEN30','MID_C','CLOSE_C']],width=.23,label=name)
    axs[1].set_xticks(range(3),['OPEN30','MID_C','CLOSE_C']);axs[1].axhline(0,color='black');axs[1].set_ylabel('Fitted minus raw H−L (pp)');axs[1].set_title('Scientific fidelity, not forecast error');axs[1].legend()
    save(fig,'10_raw_vs_spline_scientific_fidelity.png','Raw versus whole-fit conditional contrasts on matched observed state cells',['model_fidelity_by_state_bin.csv','contrasts_and_materiality.csv'])
    scores=frames['model_scores'];eval_scores=scores[(scores.part=='EVAL')&scores.context.isin(['DEV_2020','DEV_2021','DEV_POOLED_2020_2021'])]
    fig,axs=plt.subplots(2,2,figsize=(19,12))
    for off,context,color in zip([-.25,0,.25],['DEV_2020','DEV_2021','DEV_POOLED_2020_2021'],colors):
        sub=eval_scores[eval_scores.context==context].set_index('model')
        axs[0,0].bar(np.arange(len(PROFILE_IDS))+off,sub.loc[PROFILE_IDS,'MSE_profile']*1e4,width=.25,color=color,label=context)
        allnames=SCALAR_IDS+['M0','M1','P-OLS-Z','M2-T8','M4-T8-Z4','M4-T12-Z4']
        axs[0,1].bar(np.arange(len(allnames))+off,sub.loc[allnames,'CLOSE_C_RMSE_pp'],width=.25,color=color,label=context)
    axs[0,0].set_xticks(range(len(PROFILE_IDS)),PROFILE_IDS,rotation=50,ha='right');axs[0,0].set(ylabel='MSE_profile × 10⁴',title='Matched 241 / 248 / pooled 489 dates');axs[0,0].legend()
    axs[0,1].set_xticks(range(len(allnames)),allnames,rotation=50,ha='right');axs[0,1].set(ylabel='Closing-share RMSE (pp)',title='Scalar models and full-profile closing sums')
    pair=frames['paired_loss_sensitivities'];pair=pair[(pair.context=='DEV_POOLED_2020_2021')&(pair.lag==10)]
    for ax,metric in zip(axs[1],['profile_mse','close_mse']):
        sub=pair[pair.metric==metric];values=sub.mean_loss_difference.to_numpy();lo=sub.HAC_lo.to_numpy();hi=sub.HAC_hi.to_numpy();factor=1e4
        ax.errorbar(values*factor,np.arange(len(sub)),xerr=[(values-lo)*factor,(hi-values)*factor],fmt='o',capsize=4)
        ax.set_yticks(range(len(sub)),sub.model+' minus '+sub.baseline);ax.axvline(0,color='gray');ax.set(xlabel=metric+' difference ×10⁴ (negative favors model)',title='Pooled fixed forecasts, conditional HAC10 interval')
    save(fig,'11_development_chronological_model_scorecard.png','Past-only development backchecks; same dates, no independent validation',['model_scores.csv','paired_loss_sensitivities.csv','chronological_predictions.npz'])
    envs=['2016-2019','2020','2021'];env_masks=[dates<'2020',np.char.startswith(dates,'2020'),np.char.startswith(dates,'2021')]
    supp=frames['support_and_environment'];envtv=frames['environment_TV']
    fig,axs=plt.subplots(2,2,figsize=(15,10));bottom=np.zeros(3)
    for g,color in enumerate(colors):
        counts=np.array([int((mask&(labels==g)).sum()) for mask in env_masks]);axs[0,0].bar(envs,counts,bottom=bottom,color=color,label=state_names[g]);bottom+=counts
    axs[0,0].legend();axs[0,0].set(ylabel='Distinct dates',title='Fixed P0-state mixture shifts')
    env_h1=[]
    for env,mask in zip(envs,env_masks):
        rows=supp[(supp.context==env)&supp.group.isin(['0','2'])];ok=len(rows)==2 and bool(rows.basic_ok.all())
        value=(q[mask&(labels==2),66:78].sum(axis=1).mean()-q[mask&(labels==0),66:78].sum(axis=1).mean())*100 if ok else np.nan
        env_h1.append(value)
    axs[0,1].bar(envs,env_h1);axs[0,1].axhline(2,color='red',ls='--');axs[0,1].set(ylabel='Raw H−L closing allocation (pp)',title='Basic support required for both groups')
    for i,v in enumerate(env_h1):
        if not np.isfinite(v):axs[0,1].text(i,0,'ABSTAIN\nSUPPORT',ha='center',va='bottom')
    for env,color in zip(envs,colors):
        mask=env_masks[envs.index(env)];axs[1,0].hist(z[mask],bins=np.linspace(z.min(),z.max(),30),density=True,histtype='step',label=env,color=color)
    axs[1,0].legend();axs[1,0].set(xlabel='Z0',ylabel='Density',title='Different states observed in each environment')
    for i,env in enumerate(['2020','2021']):
        sub=envtv[(envtv.environment.astype(str)==env)&(envtv.cell!='MARGINAL')]
        axs[1,1].plot(np.arange(5),sub.TV,'o-',label=env)
    axs[1,1].set_xticks(range(5),[f'2016–19 Q{i+1}' for i in range(5)]);axs[1,1].axhline(.05,color='red',ls='--');axs[1,1].set(ylabel='Within-cell raw profile TV',title='Gaps = ABSTAIN; no standardization/causal claim');axs[1,1].legend()
    extra['environment_H1_pp']=env_h1
    save(fig,'12_environment_support_and_composition.png','Environmental mixture versus coarse conditional shape; four missing March 2020 sessions limit stress inference',['support_and_environment.csv','environment_TV.csv','P0 NPZ'])
    fig,axs=plt.subplots(2,2,figsize=(15,10));bins=frames['profile_bin_residuals']
    for name in ['M0','P-OLS-Z','M2-T8','M4-T8-Z4']:
        sub=bins[(bins.context=='D_FULL')&(bins.part=='TRAIN')&(bins.model==name)].sort_values('bin');axs[0,0].plot(sub.bin,sub.RMSE*100,label=name)
    time_axis(axs[0,0]);axs[0,0].set_ylabel('Bin residual RMSE (pp)');axs[0,0].legend()
    diag=frames['profile_diagnostics'];sub=diag[(diag.context=='D_FULL')&(diag.part=='TRAIN')]
    axs[0,1].barh(sub.model,sub.negative_below_tolerance);axs[0,1].set(xlabel='Components < −1e−12',title='Raw prediction validity; no clipping')
    with np.load(OUT/'residual_eigenvalues.npz') as f:
        for name in ['M0','M4-T8-Z4']:axs[1,0].semilogy(np.arange(1,79),np.maximum(f['D_FULL__TRAIN__'+name][::-1],1e-20),label=name)
    axs[1,0].set(xlabel='Residual covariance eigenvalue rank',ylabel='Eigenvalue',title='Closure forces a null direction, not 78 independent tests');axs[1,0].legend()
    axs[1,1].bar(range(4),plots['last_bin_HL']*100);axs[1,1].set_xticks(range(4),['15:55 bin','15:00–15:55\nlast bin omitted','CLOSE_C\nfull primary','14:00–14:10\nexploratory']);axs[1,1].set(ylabel='Raw H−L allocation (pp)',title='Contribution diagnostics: denominators remain whole-day')
    save(fig,'13_normalization_residuals_and_last_bin.png','Compositional residuals, low-df approximation and fixed last-bin sensitivity',['profile_diagnostics.csv','profile_bin_residuals.csv','residual_eigenvalues.npz','plot_data.npz'])
    np.savez_compressed(OUT/'figure_data_extra.npz',**extra)
    thumbs=[]
    for ref in manifest:
        with Image.open(ROOT/ref['path']) as im:
            thumb=ImageOps.contain(im.convert('RGB'),(640,430));tile=Image.new('RGB',(660,465),'white');tile.paste(thumb,((660-thumb.width)//2,25));ImageDraw.Draw(tile).text((8,5),Path(ref['path']).name,fill='black');thumbs.append(tile)
    sheet=Image.new('RGB',(1980,2325),'#dddddd')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*660,(i//3)*465))
    sheet.save(figdir/'contact_sheet.png')
    write_json(OUT/'plots_manifest.json',dict(figures=manifest,additional_data='figure_data_extra.npz',independent_score_checks=score_checks,
        direct_and_same_cell_reconciliation='PASS atol1e-10',image_decode_nonblank='PASS',source_Q_not_copied=True))
    # Scientific narrative uses the actual machine outputs, including negative
    # predictive findings and failed environment support.
    pooled=eval_scores[eval_scores.context=='DEV_POOLED_2020_2021'].set_index('model')
    m4_gain=(pooled.loc['M0','MSE_profile']-pooled.loc['M4-T8-Z4','MSE_profile'])/pooled.loc['M0','MSE_profile']*100
    m4_vslinear=(pooled.loc['P-OLS-Z','MSE_profile']-pooled.loc['M4-T8-Z4','MSE_profile'])/pooled.loc['P-OLS-Z','MSE_profile']*100
    strongest=pooled[pooled.kind=='profile'].MSE_profile.idxmin();bestscalar=pooled.CLOSE_C_MSE.idxmin()
    rawtv=float(abs(plots['raw_HL']).sum()/2);block=frames['block_intervals'];h20=block[(block.window=='CLOSE_C')&(block.block==20)].iloc[0]
    def testrow(name):return family[family.test==name].iloc[0]
    moderation=testrow('piecewise_slope_interactions');linear=testrow('linear_slope');quad=testrow('quadratic_curvature')
    dfd=diag[(diag.context=='D_FULL')&(diag.part=='TRAIN')]
    unique_scores=scores[(scores.context.isin(['D_FULL','DEV_2020','DEV_2021','DEV_POOLED_2020_2021']))&~((scores.context=='D_FULL')&(scores.part=='EVAL'))]
    reg=frames['model_registry'];dfreg=reg[reg.context=='D_FULL']
    summary=frames['scalar_summary'];sc=frames['scalar_contrasts_and_HAC'];envsupport=supp[supp.context.isin(envs)&supp.group.isin(['0','1','2'])]
    sens_models=frames['sensitivity_models'];selsens=sens_models[sens_models.model.isin(['OLS-L1','M2-T8','M4-T8-Z4'])]
    main=f'''# C2R — direct curves, OLS and state-dependent splines

**Stage: PASS_WITH_QUALIFICATIONS. Implementation/QA PASS.** C2R is complete on the already explored 2016–2021 development data. The historical PREV closing-hour H−L is **{qa['P0_H1_pp']:.4f} pp**, reproduced to {qa['P0_reproduction_error_pp']:.3g} pp. It is a compositional allocation association, not source-paper exact replication, independent confirmation, or a certified effect exceeding 2 pp. No EBM, added-state model, later-year C outcome or reserved evaluation was run.

The fixed 8×4 M4 changes pooled chronological profile MSE by **{m4_gain:+.2f}% relative to M0** and **{m4_vslinear:+.2f}% relative to linear P-OLS-Z** (positive means lower loss). Lowest pooled profile MSE among declared candidates: **{strongest}**; lowest closing-share MSE: **{bestscalar}**. These are developmental descriptions of predeclared candidates; no new hyperparameter was chosen from them.

## Data, identity and time scope

{table(frames['cohort_by_year'])}

All fits use exactly 1,472 Z0-valid keys; 1,491 Q-valid dates are counted separately. The two backchecks contain 241 dates in 2020 and 248 in 2021 (489 pooled). First/last main source dates are 2016-01-05/2021-12-31; auxiliary Jan 4 supplies prior state only. The pinned NPZ and two revised/original specifications pass SHA256. Original 6 annual D2 references plus 72 C missing-key monthly supplements match hashes; no minute rows were decoded for C2R. C1R's numeric state table hash is verified; exp(Z0) agrees with RV_prev at atol1e−18/rtol1e−12. Strict scheduled predecessors are independently checked. Full windows agree by independent cumulative sums to 1e−10.

Q is 390 within-session minute log squares grouped into 78 bins, normalized by each day's own R. First return is 09:30 close/open, with no overnight or missing-bar fill. UTC starts and XNYS/ET govern session timing. CLOSE_C [66:78], MID_C [24:48], OPEN30 [0:6] retain full-C priority; MID_P0 [30:42]/CLOSE_P0 [72:78] are secondary; PRE_CLOSE_DIAG [66:72] is post-P0 exploratory. Return prediction, latent spot volatility and ratio-of-group-RV totals are different objects.

Twelve early closes and seven incomplete ordinary days remain excluded: 2016-02-02, 2019-08-12, 2020-03-09/12/16/18, 2021-05-05; 100 missing minutes. Four March 2020 crisis dates are absent. This population concerns eligible complete sessions, with nonrandom missingness risk. B's 39-row HF repair, B return table, D1 pilot, VIX and FOMC are not used. R1 status remains SOURCE_INSPIRED_PROXY.

## Frozen protocol, models and information

`config/C_C2R_development_protocol_v1_1.json` was written before the real fits; SHA256 `{qa['protocol_sha256']}`. It is a C2R exploratory development freeze. C1R's full-C draft remains unchanged/unlocked; official horizon/split/evaluation are pending. Date hashes, code/software/source hashes, exact fitted coefficients, knots, cutpoints, counts, and training/forecast dates are in `model_parameters.json`, `model_registry.csv` and `provenance_and_QA.json`.

D_FULL is descriptive on all 1,472 previously seen dates. DEV_2020 trains through 2019-12-31; DEV_2021 through 2020-12-31. Training scalers, natural-spline knots, tercile/quintile cuts and quantile grids are refitted separately at each origin, then held fixed. No eval-year target affects them; no randomized folds, early stopping or hidden search is used. The same chronological date keys score every core model. P0 fixed ranks remain D-only; full-sample quantile S0 differs from P0 rank labels on **{qa['raw_rank_vs_D_FULL_quantile_label_differences']} date(s)**, explicitly disclosed rather than forcing them to agree.

Scalar formulas: L0=intercept; L1=1+standardized Z0; L2=1+mid+high indicators; L3 adds state-specific intercepts and z_s×mid/high slopes; L4=1+z_s+z_s². Low is the reference. A standard unit is one training population SD of log prior RV. L3 concerns scalar slope moderation, not time-of-day interaction. Rank-deficient designs abstain; none is silently pseudo-inverted for inference.

M0 is training Q mean; P-OLS-TIME is its algebraic alias, not an extra discovery/fit. M1 is train-S0 conditional Q mean, with frozen basic support and explicit M0 fallback. P-OLS-Z estimates a_k+b_k z_s by daily multioutput OLS; sum a≈1 and sum b≈0 are checked. M2 uses clamped cubic time B splines, 8 basis columns primary and 12 sensitivity. M4 is the nonredundant full tensor of that time basis and four natural-cubic state basis columns at train min/terciles/max, with linear tail continuation and **zero penalty**, full-rank least squares. Constants belong to both spans, avoiding redundant intercepts. The no-interaction control uses the same bases with centered additive state effects, not native EBM M3. For closed Q, a pure state-level vertical shift across all bins is algebraically constrained to zero. No log-Q transform, clipping/projection or M8 model was used.

{table(dfreg,['model','kind','train_n','rank','edf','condition','out_of_training_range_eval_n'])}

Ranks/edf above are numerical model parameter counts, not independent-day sample sizes. A tensor with 32 parameters is not 32 independent shape tests; each date contributes a whole vector with equal weight. Complete origin cutpoints/ranges/occupancies and out-of-range eval counts are in the registry/parameters. Prediction outside training range is reported, not hidden; interpretation remains support gated.

## Direct and fitted scientific shapes

Raw whole-profile H3 TV is **{rawtv:.6f}**. The new fixed-label 20-session descriptive bootstrap H1 interval is **[{h20.lo*100:.3f}, {h20.hi*100:.3f}] pp**. Historical P0 block5/10 intervals were reused, not rerun; the 20-session check is an additional sensitivity on the same viewed records. Every draw resamples whole scheduled date slots jointly; invalid slots never become filled outcomes. No learner was refitted in this bootstrap. `block_intervals.csv` gives all six window contrasts and the qualified 20-block TV interval. The TV percentile distribution may be biased near zero and is not a near-invariance certificate.

{table(contrasts[(contrasts.context=='D_FULL')&contrasts.window.isin(['CLOSE_C','OPEN30','MID_C','TV_HL'])],['model','window','estimate_pp','raw_pp','difference_pp','TV','raw_TV','simplex_mean_curves'])}

Fitted scientific contrasts average **whole predictions over the same observed P0 state rows**, not predictions at a group median or an isolated additive component. `model_fidelity_by_state_bin.csv` also records all per-bin raw/fitted means in three P0 cells and five train-quantile bins. The singleton training quantile slices in figures 8–9 are fitted surfaces; they do not identify pointwise population m(k,z). Anchored D uses k0=30 (12:00). All profile plots use the full 78 bins. Numerical discrepancy is model fidelity evidence, not proof that empirical means are population truth.

## Scalar coefficient, residual and specification diagnostics

HAC10 L1 slope nominal p={linear.p_value:.6g}, six-family Holm p={linear.p_holm_fixed_six_family:.6g}; L3 joint slope interactions nominal p={moderation.p_value:.6g}, Holm p={moderation.p_holm_fixed_six_family:.6g}; L4 curvature nominal p={quad.p_value:.6g}, Holm p={quad.p_holm_fixed_six_family:.6g}. These are conditional/asymptotic developmental associations. Within-state slopes do not by themselves establish differences between states; L3 uses a joint two-coefficient null. L2 levels, linear slope and quadratic curvature are distinct hypotheses.

{table(family,['test','statistic','df','p_value','p_holm_fixed_six_family','family_size'])}

The fixed six-member D_FULL family at lag10 contains L1 slope, L2 categorical levels, L3 slope interactions, L4 curvature, raw historical-label H1>0 and H1>0.02. H3 has a descriptive interval rather than an invented p-value. Holm covers this finite group only if the marginal p-values are valid; it does not undo P0-driven emphasis, dependent-data misspecification or post-inspection selection. The materiality null is separate from zero-direction. All conclusions of materiality/near-invariance remain NOT_CERTIFIED.

{table(summary,['context','model','n_days','rank','condition','R2','adjusted_R2','MSE','AIC','BIC','sd','skew','excess_kurtosis','white_p','koenker_p','jarque_bera_p'])}

All coefficients, ordinary descriptive SE and conditional HAC5/10/20 intervals/p-values are in `scalar_ols_models_and_hac.csv`; same-cell closing-effect intervals in pp are in `scalar_contrasts_and_HAC.csv`. `scalar_summary.csv` includes SSE, Gaussian OLS AIC/BIC and full residual location/scale/MAD/tail quantiles. These scalar R²/AIC semantics are not assigned to profile smoothers. Feature correlations/VIF appear in `feature_collinearity.csv` (intercept VIF omitted); state dummies and interactions can be correlated by construction.

White and BP/Koenker use only the fixed small auxiliary design 1+z_s (White expands it), not a 78-dummy matrix. Their usual IID-reference p-values, JB, ARCH LM and Ljung–Box are heuristic under serial dependence/nonstationarity. ACF/PACF and squared-residual diagnostics use ordered eligible dates, so gaps are compressed for these descriptive plots/tests; scheduled-gap HAC and block resampling are separate. `serial_diagnostics.csv` supplies lags5/10/20 for scalar residuals and profile close residual/PC1/vector norms. Low-degree RESET and ordinary linear-vs-quadratic F tests are in `scalar_specification_tests.csv`; a RESET augmentation already in the column span is explicitly skipped. No flattened 78N regression p-value was used.

HAC uses Bartlett estimating-score covariances across original scheduled slots with missing-slot scores zero and n/(n−p) correction. It matches statsmodels on consecutive-slot fixtures; gaps are not imputed returns. Its nominal normal/chi-square limits require adequate moments, a suitable weak-dependence/stability law and valid selected-complete-session sampling assumptions; these are not proven for this market series. These caveats also apply to calendar sensitivities. No empirical result supplies a theorem-certified confidence event.

Influence output covers every scalar training fit in D_FULL and the two chronological origins: leverage, internal/external studentization, Cook, DFFITS and every DFBETA. Exact OLS deletion formulas were independently checked against statsmodels; no N refits were required. Thresholds: hat>2p/n, Cook>4/n, |external student|>3, |DFFITS|>2√(p/n), |DFBETA|>2/√n. Flagging is not deletion or causal importance. Top ten D_FULL L1 dates:

{table(top,['date_et','hat','student_external','cooks','dffits'])}

## Profile residuals and raw normalization

{table(dfd,['model','n_days','MSE_profile','MAE_profile','raw_half_L1','TV_valid_n','negative_below_tolerance','negative_mass','prediction_min','sum_defect_max','covariance_rank','first_PC_variance_fraction','edge_close_bias'])}

`profile_diagnostics.csv` records raw negative/>1 components, mass/range/sum defects, genuine-TV valid counts, all six window errors and error contributions, roughness/adjacent variation and edge bias. Half-L1 is retained for every raw prediction; TV_prediction is calculated only on simplex-valid dates and its valid n is always displayed, so invalid raw models are not ranked using a hidden normalization. No negative prediction was silently clipped. Roundoff tolerance is −1e−12/closure1e−10.

`profile_bin_residuals.csv` reports binwise variance/RMSE/MAE/skew/tails and state-residual covariance. `profile_daily_errors.csv` reports vector norm, PC1, MSE/MAE, close residual and state/year keys. `residual_covariance.npz` and `residual_eigenvalues.npz` preserve the empirical covariance/eigenvalue spectrum. Closure imposes at least one null direction; eigenvalues do not provide 78 independent significance tests. Daily scalar features, not stacked bins, enter serial/ARCH diagnostics. Low-df time smoothers can miss a sharp last-bin/auction proxy; report their approximation gap instead of expanding the frozen basis after seeing errors.

## All matched train and developmental comparison scores

Rows below include full descriptive training, both origin-training sets and both/pooled chronological evaluations. D_FULL train scores are in-sample only. Every eval candidate uses the same valid keys. Full unrounded MSE/MAE/half-L1/valid-TV and closing-share scores are in `model_scores.csv`.

{table(unique_scores,['context','part','model','kind','n_days','MSE_profile','MAE_profile','raw_half_L1','TV_valid_n','CLOSE_C_MSE','CLOSE_C_RMSE_pp','CLOSE_C_MAE_pp'])}

{table(pair,['model','baseline','metric','n_days','mean_loss_difference','HAC_lo','HAC_hi','block_lo','block_hi'])}

The table above shows pooled HAC10 and joint-date block10 intervals; the CSV also includes each year and all lag/block5/10/20 settings. Negative loss difference favors the first model. Forecasts remain fixed within resampling; no full learner/selection bootstrap is claimed. A scalar closing-share improvement is not recovery of the whole 78-vector. The same M0 closing mean equals OLS-L0 and the sum of P-OLS-Z's closing bins equals OLS-L1, both checked numerically. The no-interaction spline ablation is constrained by response closure, not evidence from a software term chart.

## Support, environments and robustness

{table(envsupport,['context','group','n_days','five_session_groups','display_ok','basic_ok','strong_ok','Z0_mean','close_mean','close_sd'])}

Display/basic/strong gates are 30/10, 50/20, 100/30 distinct dates/five-session index groups. Groups are support bookkeeping, not certified independent clusters. The early training quintile cells define common coarse support for environment TV; unsupported comparisons are ABSTAIN in `environment_TV.csv` and the gallery. Marginal environment curves mix different state distributions; conditional cell comparisons are a different object. No reweighting, hidden pooling or causal explanation was introduced. Continuous query bands use train rank±0.1; ranges/density/counts and masks are in `support_and_environment.csv`.

Raw sensitivity contrasts use original P0 labels and fixed windows. Changed-training fits legitimately recompute means/SD/cutpoints/knots, all saved. FULL always leads. DROP_TOP1_RV removes {len(qa['drop_top1_dates'])} current-RV extremes (threshold {qa['top1_R_cutoff']:.6g}); it is outcome-conditioned D-only, never a deployable predictor. EXCLUDE_2020 changes the calendar distribution severely. DROP_TOP5_INFLUENTIAL uses the same five D_FULL OLS-L1 Cook dates for every model: {', '.join(qa['drop_cook5_dates'])}. No model-specific favorable exclusions were selected. LOYO refits exclude each calendar year; they can train on future years and are explicitly NOT walk-forward OOS. Unsupported left-year high/low scientific contrasts abstain.

{table(contrasts[(contrasts.model=='RAW_P0_LABELS')&contrasts.window.isin(['CLOSE_C','TV_HL'])],['context','window','n_days','estimate_pp','TV'])}

{table(selsens,['context','model','n_train','n_eval','mode','MSE_profile','CLOSE_C_RMSE_pp','scalar_model_HL_pp'])}

Last 15:55 bin contribution to raw H1: {plots['last_bin_HL'][0]*100:+.4f} pp. Closing numerator excluding only that bin: {plots['last_bin_HL'][1]*100:+.4f} pp, compared with primary {plots['last_bin_HL'][2]*100:+.4f} pp. This retains the whole-day denominator but changes the diagnostic numerator; it is not a selected replacement target. The predeclared 14:00–14:10 diagnostic is {plots['last_bin_HL'][3]*100:+.4f} pp; without an authentic FOMC calendar no event mechanism is inferred. No missing crisis date was filled or removed twice.

## QA, reproducibility, limitations and successor gate

Independent output checks recomputed {score_checks} core train/eval model scores, pooled profile scores, all historical group curves and same-cell fitted means from coefficients/original arrays, to 1e−10 (scores atol1e−12). All 13 principal PNGs decode, are nonblank and ≥1600px; numeric source references and hashes are in `plots_manifest.json`. A contact sheet supports human visual review. Synthetic checks cover tensor/explicit design equivalence, natural-tail/basis accounting, daily OLS/HAC/influence against trusted references, source/P0 math via existing tests, chronology cutpoints, immutable state features under target changes, rank failure, TV labels, joint blocks and output smoke. Exact executed test results and any repairs are in the dated session report/provenance QA. Images are not 78 independent tests.

Run commands: `.venv/bin/python -B scripts/c2r_development_models.py prepare`, then `run`, then `report`; `python -B -m unittest discover -s tests -p 'test_c*.py' -v`. The existing frozen protocol is never overwritten by prepare. Restore authorized matching P0 sources/state lookup, install the recorded existing package versions, export EBM_DATA_ROOT if needed, and use the installed package from a clean clone. No source/API/credentials are needed for C2R. Forecast files store dates/source-row references and predictions only, never a second Q matrix or per-fold input table.

Source/model/config/environment identities, timing, protected-file rechecks, zero socket/API transfer and retained bytes are recorded in provenance and the coding-session report. The prior C1R narrative has a pandas Series.mode formatting defect in its state table; its machine state ledger is correct and both were preserved unchanged. Current C2R uses explicit column access and its own verified state meanings. No scientific protocol redesign was required. No 2022–2026 scientific values, downloads, EBM fits or independent evaluation occurred.

**Recommendation:** C2R methods/QA support reviewing a bounded C3 **design** with strong M0/M1/P-OLS baselines and the declared spline approximation limitations exposed. The developmental score ranking does not establish an EBM opportunity or authorize fitting C3. Retain negative/unstable comparisons, raw normalization and support abstentions. Actual C3 execution requires a new user instruction and frozen stage settings. Full-C materiality, near-invariance, raw pointwise certification and independent forecast improvement remain NOT_CERTIFIED/DEFERRED.

## REQUESTED_DECISIONS_FOR_FULL_C

Only dependent future choices remain: exact full-C horizon; Q-first/mask-later versus Z0-first split population; Zret close-anchor/half-day policy; Zvol older-eligible/strict-chain lookback, epsilon and volume provenance; and explicit future-source/reserved-data authority. No official 60/20/20 dates or independent C evaluation are released here.
'''
    REPORTS.mkdir(exist_ok=True)
    (REPORTS/'C2R_OLS_state_dependent_splines_full_diagnostics.md').write_text(main)
    interpretations=[
        'The historical P0 curves use retrospective rank groups, while the two other panels use each training origin’s quantile cuts. These are different grouping rules; similar U shapes are compatible with a small localized compositional effect, not a new global geometry.',
        'Every point is a complete-day closing-hour share and prior-session log RV. Piecewise slopes and quadratic curvature are interpretive scalar descriptions. Density and tails matter; these curves do not replace the full profile.',
        'Slope intervals are conditional daily HAC diagnostics. Joint interaction and curvature tests are separate from within-state slopes. The fixed six-family Holm results do not supply post-P0 confirmation or a certified material effect.',
        'Residual plots retain extreme observations. Tail/normality and shape deviations limit classical Gaussian interpretations; they do not justify deleting days or changing the scientific target.',
        'Chronology, serial correlation and changing variance show why ordinary IID inference is insufficient. Eligible-order ACF is descriptive; scheduled-date HAC and block resampling retain calendar gaps separately.',
        'Cook and leverage identify influential observations under one declared scalar fit. The same fixed five exclusions apply across models; all sensitivities remain secondary to FULL and can change the estimand.',
        'M0 preserves the empirical categorical time curve while low-df M2 trades detail for smoothness. A sharp final-bin feature can be hard for eight/twelve basis columns; no basis expansion was selected from that appearance.',
        'P-OLS-Z maps one continuous state to all 78 bin slopes and satisfies coefficient-sum identities. Raw and modeled contrasts average identical observed coarse cells. Anchored D is a whole-curve difference, not an individual regression term.',
        'The 8×4 tensor gives a continuous fitted state/time surface and five training-derived slices. These are model evaluations on supported training bands, not pointwise conditional-mean identification or confidence bands.',
        'Scientific fidelity compares raw group means with average predictions over precisely the same rows. A small global predictive error can coexist with a closing-window discrepancy; direct means remain noisy empirical references.',
        f'All candidates face identical 2020/2021 dates. M4-T8-Z4 changes pooled profile MSE by {m4_gain:+.2f}% relative to M0; {strongest} has the lowest pooled profile MSE. Conditional fixed-forecast intervals are developmental sensitivity, not independent validation.',
        'Mixture counts and numeric state distributions differ across environments. Missing cells are ABSTAIN, not smooth evidence of invariance. The four omitted March 2020 crisis sessions remain a central generalization limitation.',
        f'Raw normalization/negative shares and residual covariance are visible. The last 15:55 bin contributes {plots["last_bin_HL"][0]*100:+.4f} pp to H1; omitting its numerator is a separately labeled diagnostic. The 14:00 region is exploratory without event data.']
    gallery='# C2R scientific visual gallery\n\n**PASS_WITH_QUALIFICATIONS — explored development, not independent confirmation.**\n\n'
    gallery+=f'The reproducible prior-RV closing-hour contrast is {qa["P0_H1_pp"]:.4f} pp, but materiality >2 pp and global near-invariance are not certified. Prior RV is plausibly associated with a redistribution of realized variance within a day; no causal mechanism follows. OLS moderation, support, robustness and the past-only spline score comparisons below describe how much of that exploratory pattern these small models capture.\n\n'
    for ref,interpretation in zip(manifest,interpretations):
        name=Path(ref['path']).name;gallery+=f'## {name}\n\n![{name}](../../{ref["path"]})\n\n{interpretation}\n\n'
    gallery+='## Handoff\n\nReview the main diagnostics report and machine tables before C3 design. Keep 2016–2021 labeled previously viewed, retain 2020 support/missingness warnings, and retain raw model defects. Full-C horizon/split, Zret/Zvol and reserved-data permissions remain pending. No C3 implementation is authorized by this gallery.\n'
    (REPORTS/'C2R_scientific_visual_gallery.md').write_text(gallery)
    theory='''# C2R theory applicability and limitations

| Object/method | Scope | Permissible interpretation / missing premises |
|---|---|---|
| Q closure and window summation | ALGEBRAIC_IDENTITY_ONLY | Exact finite-array accounting for the stated source convention; no market or latent-volatility theorem |
| Multioutput OLS and tensor factorization | ALGEBRAIC_IDENTITY_ONLY | Full-rank least-squares solution; balanced-date Frobenius loss equals the declared tensor fit, not raw mean identification |
| Scalar coefficient HAC5/10/20 | CONDITIONAL_STANDARD_INFERENCE | Bartlett calendar-score sandwich and asymptotic normal/Wald references; requires suitable moments, weak dependence/stability, design and selected-complete-session sampling law; not established merely by diagnostics |
| White/BP/Koenker/JB/ARCH/Ljung–Box/RESET/F | ADAPTED_DESCRIPTIVE | Usual reference p-values heuristic under serial dependence/nonstationarity; no diagnostic rejection alone identifies a scientific cause |
| OLS influence/deletion formulas | ALGEBRAIC_IDENTITY_ONLY | Actual finite-fit leverage/studentization/Cook/DFFITS/DFBETAs; no automatic deletion or population causal importance |
| Fixed-label circular date blocks | ADAPTED_DESCRIPTIVE | Exploratory percentile sensitivity under a defensible dependence/stability law; labels fixed, eligible selection and circular end wrap disclosed; TV percentile bias near zero remains |
| Paired fixed-forecast blocks/HAC | CONDITIONAL_STANDARD_INFERENCE / ADAPTED_DESCRIPTIVE | Conditional on frozen forecasts; not full-process learner/selection uncertainty; two nonstationary years and prior exposure limit calibration |
| Raw-vs-fitted same-cell discrepancy | ADAPTED_DESCRIPTIVE | Observed coarse-cell reference versus whole-model average on same rows, not exact raw pointwise m(k,z) |
| Support gates and masks | ADAPTED_DESCRIPTIVE | Operational counts of distinct dates/scheduled groups; not proof of independent blocks or identification |
| Holm six-test family | CONDITIONAL_STANDARD_INFERENCE | Controls the finite named family only with valid marginal p-values; does not repair P0-based selection or false asymptotic premises |
| Materiality / near-invariance | NOT_CERTIFIED | Requires calibrated interval lower >0.02 or justified joint upper within 0.02/0.05, not a point estimate, p>0.05 or pointwise ribbon |
| Native InterpretML theory or selective Gaussian pivots | NOT_APPLICABLE_THIS_STAGE | No EBM fit; no exact greedy-path, IID bounded concentration, selective pivot or population raw pointwise event instantiated |
| Tasks 10B/11/12/15–25 | DEFERRED_TO_C5 | Inspect exact source theorem/selection/sampling/support premises before use; do not import the corpus or invent a theorem from current diagnostics |

The sample unit is the trading date. All 78 bins share a denominator and closure; neither their covariance eigenvalues nor flattening supplies 78N independent trials. Scalar Gaussian likelihood AIC/BIC and adjusted R² belong to the actual daily OLS diagnostics, not generic profile smoothers or later EBMs. Splines may estimate a projection of coarse conditional structure and have approximation/localization bias; continuous fitted slices are not identified population m at unsupported singleton states.

Potential later C5 work, only after its own authorization: exact assumption/source crosswalk; common-support fixed-query direct means; justified simultaneous date/block raw events with multiplicity; fidelity inequalities conditional on a valid matched event; refit/selection resampling when claiming learner uncertainty; calibrated conditional environmental contrasts. Each route needs an explicit estimand, selection history, exposure ledger, missingness law and dependence premises. Current results do not establish any of those certificates.

R1–R6 remain the supplied v1.0 literature ledger. C2R is a SPY lagged-RV minute-square allocation proxy, not futures/open-VIX latent-periodicity replication. No publication novelty, alpha, trading profit, material population discovery or independent confirmation is asserted. Four incomplete March 2020 sessions, prior P0 exposure, state distribution shifts and potential source revisions remain limitations.
'''
    (REPORTS/'C2R_theory_applicability_and_limitations.md').write_text(theory)
    qa.update(status='PASS_WITH_QUALIFICATIONS',stage_decision='PASS_WITH_QUALIFICATIONS',plots=len(manifest),
        independent_score_checks=score_checks,plot_data_reconciliation='PASS',render_wall_seconds=time.perf_counter()-started,
        pooled_M4_vs_M0_profile_MSE_improvement_percent=m4_gain,pooled_best_profile_model=strongest,
        C3='DESIGN_REVIEW_ONLY_REQUIRES_SEPARATE_AUTHORIZATION',code_at_render={p.name:digest(p) for p in Path(__file__).parent.glob('c2r_*.py')})
    write_json(OUT/'provenance_and_QA.json',qa)
    print('C2R_RENDER_QA_PASS',len(manifest),'figures;',score_checks,'independent score checks;',round(time.perf_counter()-started,2),'seconds',flush=True)
