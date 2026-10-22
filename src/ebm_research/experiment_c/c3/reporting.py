"""Numerically sourced, full-resolution static C3 scientific gallery and reports."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image,ImageOps,ImageDraw
from ..readiness import ROOT,digest
from .run import OUT,CONFIG,config,inputs,load_bundle,write_json,reference_predictions
from . import models,m8_softmax
from .analysis import verify,theory,refresh_registry

COLORS=['#2878b5','#249d82','#e68a25'];STATES=['LOW','MIDDLE','HIGH']
SHORT={models.IDS[0]:'T0 time only',models.IDS[1]:'M3c additive numeric',models.IDS[2]:'M3d additive terciles',models.IDS[3]:'M5 numeric interaction',models.IDS[4]:'M6 tercile interaction','M8':'M8 softmax'}
TICKS=[0,6,18,30,42,54,66,77];TIMES=['09:30','10:00','11:00','12:00','13:00','14:00','15:00','15:55']
plt.rcParams.update({'font.size':10,'axes.titlesize':12,'axes.labelsize':10,'legend.fontsize':8,'figure.titlesize':15,'axes.spines.top':False,'axes.spines.right':False})


def table(frame,columns=None):
    f=frame[columns].copy() if columns else frame.copy()
    def fmt(v):
        if isinstance(v,(float,np.floating)):return f'{v:.6g}' if np.isfinite(v) else '—'
        return str(v).replace('|','/')
    return '| '+' | '.join(f.columns)+' |\n| '+' | '.join(['---']*len(f.columns))+' |\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in f.itertuples(index=False,name=None))


def report():
    cfg=config();d=inputs();folder=OUT/'figures';folder.mkdir(exist_ok=True)
    theory();refresh_registry(d)
    read=lambda n:pd.read_csv(OUT/(n+'.csv'))
    groups=read('group_mean_profiles');scores=read('profile_predictive_metrics');shapes=read('model_shapes_and_scientific_contrasts')
    paired=read('paired_loss_tests');support=read('state_support_and_masks');features=read('residual_daily_features');seed=read('native_seed_and_complexity_stability')
    historical=(groups.context=='D_FULL')&(groups.label_origin=='HISTORICAL_P0');native=json.loads((OUT/'native_terms_and_bins.json').read_text())
    figures=[]
    def axes(nrows=1,ncols=1,title='',size=None):
        f,a=plt.subplots(nrows,ncols,figsize=size or (12,max(5.5,3.4*nrows)),squeeze=False,layout='constrained');f.suptitle(title+'\n2016–2021 explored development • SPY allocation proxy • no population certificate');return f,a
    def clock(a,ylabel='Mean Q bin share (pp)'):
        a.set_xticks(TICKS,TIMES,rotation=35);a.set_xlabel('Bin start, America/New_York');a.set_ylabel(ylabel);a.grid(alpha=.18)
    def curves(a,name,context='D_FULL',origin='HISTORICAL_P0',raw=False):
        x=groups[(groups.context==context)&(groups.label_origin==origin)&(groups.model==name)]
        for g in range(3):
            row=x[x.state==g].sort_values('bin')
            gate=support[(support.context==context)&(support.label_origin==origin)&(support.environment=='ALL')&(support.state==g)].iloc[0]
            if not gate.display_ok:
                a.plot([],[],color=COLORS[g],label=f'{STATES[g]} n={int(row.n_days.iloc[0])}: ABSTAIN')
                continue
            a.plot(row.bin,row['mean']*100,color=COLORS[g],label=f'{STATES[g]} n={int(row.n_days.iloc[0])}',lw=1.5)
            if raw:a.plot(row.bin,row.raw_mean*100,color=COLORS[g],alpha=.35,ls='--')
        a.set_title(SHORT.get(name,name));clock(a);a.legend()
    def save(f,name,source,note):
        p=folder/name;f.savefig(p,dpi=150);plt.close(f)
        with Image.open(p) as im:assert im.width>=1600 and np.array(im.convert('RGB')).std()>5
        figures.append(dict(path=str(p.relative_to(ROOT)),source=source,interpretation=note,sha256=digest(p)))
    # Each plotted value comes from saved aggregates or explicitly registered saved native state.
    f,a=axes(2,2,'1. Direct and simple reference profiles')
    for ax,name in zip(a.flat,['RAW','M0','M1','P-OLS-Z']):
        curves(ax,name);ax.axvline(54,color='gray',lw=.6);ax.axvline(77,color='gray',lw=.6)
    save(f,'01_direct_and_simple_reference_profiles.png','group_mean_profiles.csv: D_FULL/HISTORICAL_P0; mean,bin,state','Raw H1 +2.005pp; sharp 14:00 and 15:55 bins persist. P-OLS-Z is a strong simple shape comparator.')
    f,a=axes(2,1,'2. Time flexibility and sharp-bin fit')
    x=read('global_mean_profiles')
    for name,color in zip(['RAW','M0',models.IDS[0],'M2-T8','M2-T12'],['#444444','#347db2','#d38829','#a24962','#7f69b4']):
        row=x[x.model==name].sort_values('bin');a[0,0].plot(row.bin,row['mean']*100,label=SHORT.get(name,name),color=color)
        if name!='RAW':a[1,0].plot(row.bin,row.bias*100,label=SHORT.get(name,name),color=color)
    for ax in a.flat:clock(ax);ax.legend()
    a[1,0].set_ylabel('Model − all-date raw mean (pp)')
    save(f,'02_time_only_ebm_vs_unsmoothed_and_splines.png','global_mean_profiles.csv: means/bias','T0 retains all 78 time categories. Its conservative finite-round fit still shrinks sharp time structure; M0 is the exact unsmoothed mean.')
    for number,name in [(3,models.IDS[1]),(4,models.IDS[2]),(5,models.IDS[3]),(6,models.IDS[4])]:
        f,a=axes(1,3,f'{number}. {SHORT[name]}: whole raw predictions',size=(15,5.8))
        for ax,context in zip(a.flat,['D_FULL','DEV_2020','DEV_2021']):
            curves(ax,name,context,'TRAIN_S0',True);ax.set_title(SHORT[name]+'\n'+context+(' • low-state ABSTAIN' if context=='DEV_2020' else ''))
            row=scores[(scores.context==context)&(scores.model==name)].iloc[0];ax.text(.02,.96,f'max |sum−1|={row.sum_defect_max:.3g}',va='top',transform=ax.transAxes,fontsize=9)
        cuts=load_bundle('D_FULL',name)[0]['transform']['S0']['cuts'];f.supxlabel(f'Dashed: same-cell raw Q. D_FULL S0 cuts {cuts[0]:.4f}, {cuts[1]:.4f}; other origins use their own train-only cuts.')
        save(f,f'{number:02}_'+{3:'additive_ebm_continuous_three_state_curves',4:'additive_ebm_discrete_three_state_curves',5:'continuous_interaction_ebm_three_state_curves',6:'discrete_interaction_ebm_three_state_curves'}[number]+'.png','group_mean_profiles.csv: TRAIN_S0; profile_predictive_metrics.csv: sum_defect_max','Additive state effects collapse to numerical zero on balanced normalized targets; native interactions redistribute allocation but do not enforce closure. Forecast curves are fixed at the origin. 2020 low n=15 under past-origin S0 (n=21 under full-S0): ABSTAIN for raw high-low inference.')
    f,a=axes(2,3,'7. Matched observed-state curves: all EBMs and M8',size=(15,9))
    for ax,name in zip(a.flat,models.IDS+['M8']):curves(ax,name)
    for ax in a.flat:ax.set_ylim(0,4.8)
    save(f,'07_all_ebms_matched_shapes_overview.png','group_mean_profiles.csv: D_FULL/HISTORICAL_P0; identical rows','Same state colors and y scale. The additive fits share one shape; M5/M6 retain modest state/time structure; M8 is intrinsically normalized.')
    surf=read('continuous_total_surface');grid=np.sort(surf.Z0.unique());matrix=surf.pivot(index='Z0',columns='bin',values='prediction').to_numpy();mask=surf.groupby('Z0').basic_ok.first().to_numpy()
    f,a=axes(1,2,'8. M5 TOTAL response surface and native state support',size=(13,6))
    display=np.ma.masked_where(np.broadcast_to(~mask[:,None],matrix.shape),matrix*100)
    im=a[0,0].pcolormesh(np.arange(78),grid,display,shading='nearest',cmap='viridis');f.colorbar(im,ax=a[0,0],label='Whole predicted Q bin (pp)');clock(a[0,0],'Numeric Z0');a[0,0].set_ylabel('log previous scheduled-session R')
    t=load_bundle('D_FULL',models.IDS[3])[0]['transform']
    counts,edges=np.histogram(d['z'],bins=35)
    pd.DataFrame(dict(lower=edges[:-1],upper=edges[1:],n_days=counts)).to_csv(OUT/'state_density_histogram.csv',index=False)
    a[0,1].stairs(counts,edges,orientation='horizontal',fill=True,color='#617a91');a[0,1].set_xlabel('Distinct dates / equal-width numeric interval');a[0,1].set_ylabel('Numeric Z0')
    for cut in t['cuts']:
        for ax in a.flat:ax.axhline(cut,color='white' if ax==a[0,0] else 'gray',lw=.4,alpha=.7)
    save(f,'08_continuous_ebm_total_surface_and_support.png','continuous_total_surface.csv; checkpoint D_FULL M5 transform.cuts','Stepwise numeric EBM total prediction, never an isolated interaction term. Bands failing basic date/group support are masked; all D_FULL 16 quantile bins currently pass.')
    slices=read('continuous_slices');f,a=axes(2,2,'9. Training quantile singleton slices (model outputs)',size=(13,8))
    for ax,name in zip(a.flat,[models.IDS[3],'P-OLS-Z','M4-T8-Z4','M8']):
        for j,quantile in enumerate([.1,.25,.5,.75,.9]):
            row=slices[(slices.model==name)&np.isclose(slices['quantile'],quantile)].sort_values('bin');valid=row.basic_ok.to_numpy();ax.plot(row.bin,np.where(valid,row.prediction*100,np.nan),color=plt.cm.viridis(j/4),label=f'q{int(quantile*100)}; n={row.n_days.iloc[0]}')
        ax.set_title(SHORT.get(name,name));clock(ax);ax.legend()
    save(f,'09_continuous_ebm_five_numeric_state_slices.png','continuous_slices.csv: prediction; neighborhood width and date/group counts','All models evaluated at identical train-only quantiles. A singleton fitted curve is not an identified population conditional mean; neighborhoods describe support.')
    allsh=shapes[(shapes.context=='D_FULL')&(shapes.environment=='ALL')&(shapes.label_origin=='HISTORICAL_P0')]
    f,a=axes(1,3,'10. Matched additive → interaction: total predictions',size=(15,5.8))
    names=models.IDS[1:];ss=allsh.set_index('model').loc[names]
    a[0,0].bar(range(4),ss.H1*100,color=['#888','#aaa','#ad5572','#e68a25']);a[0,0].axhline(2,color='red',ls='--',label='2pp materiality');a[0,0].set_ylabel('H1 CLOSE_C high − low (pp)');a[0,0].legend()
    a[0,1].bar(range(4),ss.half_L1,color=['#888','#aaa','#ad5572','#e68a25']);a[0,1].set_ylabel('Raw half-L1; TV only if closure valid')
    for ax in a[0,:2]:ax.set_xticks(range(4),['M3c','M3d','M5','M6'])
    for name in names:
        row=groups[historical&(groups.model==name)&(groups.state==0)].sort_values('bin');a[0,2].plot(row.bin,row.anchored_D*100,label=SHORT[name])
    clock(a[0,2],'Anchored D(k;30) (pp)');a[0,2].legend()
    save(f,'10_native_additive_vs_interaction_contrast.png','model_shapes_and_scientific_contrasts.csv; group_mean_profiles.csv anchored_D','Raw M3 anchored D is zero to roundoff. M5/M6 whole-model contrasts are nonzero but attenuate raw H1. Invalid-closure half-L1 is explicitly not TV.')
    f,a=axes(2,1,'11. Raw versus fitted scientific fidelity',size=(13,8))
    for name in ['RAW',models.IDS[3],models.IDS[4],'P-OLS-Z','M4-T8-Z4','M8']:
        row=groups[historical&(groups.model==name)&(groups.state==0)].sort_values('bin');a[0,0].plot(row.bin,row.state_difference*100,label=SHORT.get(name,name))
        a[1,0].plot(row.bin,(row.anchored_D-row.raw_anchored_D)*100,label=SHORT.get(name,name))
    for ax in a.flat:clock(ax);ax.legend(ncols=3)
    a[0,0].set_ylabel('High − low curve (pp)');a[1,0].set_ylabel('Model D − direct D (pp)')
    save(f,'11_raw_versus_fitted_scientific_fidelity.png','group_mean_profiles.csv: matched historical P0 state_difference/anchored_D/raw_anchored_D','M5 H1≈1.565pp, M6≈1.395pp versus raw≈2.005pp. P-OLS-Z and M8 are stronger H1 fidelity references; no extra EBM fidelity certificate.')
    f,a=axes(1,3,'12. Daily developmental prediction and paired uncertainty',size=(17,6.5))
    names=['M0','M1','P-OLS-Z','M2-T8','M2-T12','M4-T8-Z4','M4-T12-Z4']+models.IDS+['M8'];colors=['#777','#999','#225e99','#bba272']
    for j,context in enumerate(['D_FULL','DEV_2020','DEV_2021','POOLED']):
        ss=scores[(scores.context==context)&scores.model.isin(names)].set_index('model').loc[names]
        y=np.arange(len(names))+(j-1.5)*.18
        a[0,0].scatter(ss.MSE_profile*1e6,y,s=18,label=context);a[0,1].scatter(ss.CLOSE_C_RMSE_pp,y,s=18,label=context)
    labels=[SHORT.get(n,n) for n in names]
    for ax in a[0,:2]:ax.set_yticks(range(len(names)),labels);ax.invert_yaxis();ax.legend(fontsize=7);ax.grid(alpha=.2)
    a[0,0].set_xlabel('Daily profile MSE ×10⁶');a[0,1].set_xlabel('CLOSE_C RMSE (pp)')
    p=paired[(paired.metric=='MSE_profile')&(paired.lag_or_block==10)&paired.primary_family]
    y=np.arange(len(p));a[0,2].errorbar(p.difference*1e6,y,xerr=np.array([p.difference-p.HAC_lo,p.HAC_hi-p.difference])*1e6,fmt='o',label='HAC10 conditional')
    a[0,2].hlines(y+.12,p.block_lo*1e6,p.block_hi*1e6,color='orange',label='Block10 fixed forecasts');a[0,2].set_yticks(y,[('M5' if n==models.IDS[3] else 'M6')+'−'+{'M3c_EBM_ADDITIVE':'M3c','M3d_EBM_ADDITIVE':'M3d',models.IDS[4]:'M6','M0':'M0'}[b] for n,b in zip(p['first'],p.baseline)]);a[0,2].axvline(0,color='gray');a[0,2].set_xlabel('Paired MSE difference ×10⁶\nnegative favors first, n=489');a[0,2].legend()
    save(f,'12_developmental_error_scorecard.png','profile_predictive_metrics.csv; paired_loss_tests.csv HAC10 and block10','2020 n=241, 2021 n=248, pooled n=489. Native interaction adds no established profile increment over matched additive/M0. Confidence labels condition on saved selected forecasts.')
    f,a=axes(1,3,'13. Support, composition shift and environmental discrepancy',size=(15,6))
    ss=support[(support.context=='D_FULL')&(support.label_origin=='TRAIN_S0')&support.environment.isin(['2016-2019','2020','2021'])]
    for j,g in enumerate(range(3)):
        rows=ss[ss.state==g].set_index('environment').loc[['2016-2019','2020','2021']];a[0,0].bar(np.arange(3)+(j-1)*.25,rows.n_days,width=.25,color=COLORS[g],label=STATES[g])
    a[0,0].set_xticks(range(3),['2016–19','2020','2021']);a[0,0].set_ylabel('Distinct dates');a[0,0].legend();a[0,0].text(.02,.94,'Low 2020: ABSTAIN',transform=a[0,0].transAxes,color='red')
    ns=support[(support.context=='D_FULL')&(support.label_origin=='NATIVE_Z0_MAIN_AND_PAIR')&(support.environment=='ALL')].sort_values('state');a[0,1].bar(ns.state,ns.n_days);a[0,1].axhline(50,color='red',ls='--');a[0,1].set_xlabel('Actual numeric state bin (main/pair)');a[0,1].set_ylabel('Distinct dates (all 78 k each)')
    er=read('environment_residual_discrepancy');rr=er[(er.model==models.IDS[3])&(er.status=='SUPPORTED_DESCRIPTIVE')]
    for g in range(3):
        row=rr[rr.state==g];a[0,2].scatter(row.environment.astype(str),row.residual_group_half_L1,color=COLORS[g],label=STATES[g])
    a[0,2].set_ylabel('M5 residual environment half-L1');a[0,2].legend();a[0,2].set_xlabel('Versus 2016–2019; masked if unsupported')
    save(f,'13_state_support_year_composition_and_drift.png','state_support_and_masks.csv; environment_residual_discrepancy.csv','Quantile occupancy over full development does not ensure yearly overlap. Basic gates ≥50 dates/20 original groups are operational; absent overlap remains ABSTAIN.')
    f,a=axes(2,3,'14. M5 daily close-share residual diagnostics',size=(15,9));rr=features[(features.context=='POOLED')&(features.model==models.IDS[3])];res=rr.close_residual.to_numpy()*100
    stats.probplot(res,plot=a[0,0]);a[0,0].set_title('Exploratory normal QQ (pp)');a[0,1].hist(res,bins=35,color='#537da8');a[0,1].set_xlabel('Close residual actual − fitted (pp)');a[0,2].scatter(rr.Z0,res,s=8,alpha=.45);a[0,2].set_xlabel('Z0');a[0,2].set_ylabel('Close residual (pp)')
    from statsmodels.tsa.stattools import acf
    ac=acf(res,nlags=20);sq=acf(res*res,nlags=20);a[1,0].plot(range(21),ac,label='residual');a[1,0].plot(range(21),sq,label='squared');a[1,0].legend();a[1,0].set_xlabel('Eligible-date lag (gaps compressed here)');a[1,0].set_ylabel('ACF')
    a[1,1].scatter(rr.close_pred*100,res,s=8,alpha=.5);a[1,1].set_xlabel('Fitted closing share (pp)');a[1,1].set_ylabel('Residual (pp)')
    cal=read('calibration_quintiles');cal=cal[(cal.context=='POOLED')&(cal.model==models.IDS[3])];a[1,2].plot(cal.predicted_mean_pp,cal.observed_mean_pp,'o-');limits=[min(cal.predicted_mean_pp.min(),cal.observed_mean_pp.min()),max(cal.predicted_mean_pp.max(),cal.observed_mean_pp.max())];a[1,2].plot(limits,limits,'--',color='gray');a[1,2].set_xlabel('Fitted quintile mean (pp)');a[1,2].set_ylabel('Observed mean (pp)')
    save(f,'14_residual_qq_acf_arch_and_calibration.png','residual_daily_features.csv: POOLED/M5; calibration_quintiles.csv; serial_diagnostics.csv','Heavy tails and residual dependence persist. ARCH/Ljung–Box references are heuristic; native EBM has no classical OLS Cook/hat inference.')
    f,a=axes(1,3,'15. Actual refit, regime, edge and algorithmic seed sensitivity',size=(16,6))
    stress=read('stress_refits_and_fixed_scores');xlabels=['FULL','DROP_TOP1_RV','EXCLUDE_2020','DROP_TOP5_INFLUENTIAL']
    for name,color in [(models.IDS[3],COLORS[0]),(models.IDS[4],COLORS[2])]:
        primary=allsh[allsh.model==name].iloc[0];y=[primary.H1*100]+[stress[(stress.context==c)&(stress.model==name)&stress['fit'].str.startswith('ACTUAL')].iloc[0].H1*100 for c in xlabels[1:]]
        a[0,0].plot(range(4),y,'o-',color=color,label=SHORT[name])
    a[0,0].set_xticks(range(4),['FULL','Top1 RV','No 2020','Top5 Cook'],rotation=25);a[0,0].set_ylabel('Refitted H1 on fixed P0 cells (pp)');a[0,0].legend()
    for name in models.IDS[1:]:
        row=seed[(seed.model==name)&(seed.context=='DEV_2021')];a[0,1].plot(row.seed.astype(str),row.MSE_profile*1e6,'o-',label=SHORT[name])
    a[0,1].set_ylabel('2021 profile MSE ×10⁶');a[0,1].set_xlabel('Named seed; differences ≤1.1e−17');a[0,1].legend(fontsize=7)
    nn=['RAW',models.IDS[3],models.IDS[4],'M8'];r=allsh.set_index('model').loc[nn];a[0,2].bar(np.arange(4)-.18,r.last_bin*100,.36,label='15:55 signed contribution');a[0,2].bar(np.arange(4)+.18,r.other_close_bins*100,.36,label='Other 11 closing bins');a[0,2].set_xticks(range(4),['RAW','M5','M6','M8']);a[0,2].set_ylabel('H1 contribution (pp)');a[0,2].legend(fontsize=7)
    save(f,'15_outlier_regime_seed_stability.png','stress_refits_and_fixed_scores.csv; native_seed_and_complexity_stability.csv; model_shapes_and_scientific_contrasts.csv','Ten actual stress refits completed; top5 additive controls and native LOYO deferred. All three seeds are deterministic to roundoff. Last-bin exclusion is exploratory, primary CLOSE_C unchanged.')
    f,a=axes(2,2,'16. SOFTWARE COMPONENTS — not unique scientific effects',size=(14,8))
    e=load_bundle('D_FULL',models.IDS[3])[0]['model'];mapping=e.bins_[0][0];a[0,0].plot(range(78),[e.term_scores_[0][mapping[f'{k:02}']]*100 for k in range(78)]);clock(a[0,0],'Native time score (pp)')
    edges=np.asarray(e.bins_[1][0]);a[0,1].stairs(e.term_scores_[1][1:-1]*100,np.r_[t['minimum'],edges,t['maximum']]);a[0,1].set_xlabel('Numeric Z0 native main cuts');a[0,1].set_ylabel('Native state score (pp)');a[0,1].set_title('State main effect is numerical zero; inspect exponent')
    pair=e.term_scores_[2];im=a[1,0].imshow(pair[1:-1,1:-1].T*100,aspect='auto',origin='lower',cmap='coolwarm');f.colorbar(im,ax=a[1,0],label='Native pair score (pp)');clock(a[1,0],'Native numeric state bin')
    weights=e.bin_weights_[2];a[1,1].bar(range(weights.shape[1]),weights.sum(axis=0)/78);a[1,1].set_xlabel('Native state index incl missing/unknown');a[1,1].set_ylabel('Training row weight / 78 = dates');a[1,1].text(.02,.95,f'Pair tensor {pair.shape}; time mapping 78 unique\nMissing/unseen reserves weight 0',transform=a[1,1].transAxes,va='top',bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
    save(f,'16_native_software_terms_and_binning.png','native_terms_and_bins.json + hash-verified D_FULL M5 checkpoint: term_scores_,bins_,bin_weights_','Main and pair components depend on centering and software conventions. Scientific contrasts elsewhere use total native predict. Shared category mappings may be stored once and reused at both resolutions.')
    f,a=axes(1,3,'17. Normalization, coarsening and adequacy',size=(16,6));nn=models.IDS+['M8','NORM_'+models.IDS[3],'NORM_'+models.IDS[4]]
    row=scores[scores.context=='POOLED'].set_index('model').loc[nn];a[0,0].bar(range(len(nn)),row.sum_defect_max*100);a[0,0].set_xticks(range(len(nn)),['T0','M3c','M3d','M5','M6','M8','Norm M5','Norm M6'],rotation=45);a[0,0].set_ylabel('Maximum |sum Qhat−1| (pp)')
    coarse=read('continuous_vs_discrete_coarsening');coarse=coarse[coarse.context=='D_FULL'];a[0,1].bar(range(3),coarse.within_tercile_predicted_dispersion*1e6,color=COLORS);a[0,1].set_xticks(range(3),STATES);a[0,1].set_ylabel('M5 within-tercile bin variance ×10⁶');a[0,1].set_xlabel('Finite learned resolution; no risk-loss theorem')
    r=allsh.set_index('model').loc[['RAW',models.IDS[3],models.IDS[4],'M8','NORM_'+models.IDS[3],'NORM_'+models.IDS[4]]];a[0,2].bar(range(len(r)),r.H1*100);a[0,2].axhline(2,color='red',ls='--',label='2pp materiality ≠ certificate');a[0,2].set_xticks(range(len(r)),['RAW','M5','M6','M8','Norm M5','Norm M6'],rotation=45);a[0,2].set_ylabel('D_FULL H1 (pp)');a[0,2].legend(fontsize=7)
    save(f,'17_normalization_coarsening_model_adequacy.png','profile_predictive_metrics.csv; continuous_vs_discrete_coarsening.csv; model_shapes_and_scientific_contrasts.csv','NORM variants apply the frozen positive-part closure map and have distinct model identities. They cannot inherit native additive interpretation. No model supplies a raw materiality/equivalence certificate.')
    # Contact sheet is only navigation; individual originals retain readable labels.
    thumbs=[]
    for item in figures:
        with Image.open(ROOT/item['path']) as im:
            canvas=Image.new('RGB',(600,365),'white');thumb=im.convert('RGB');thumb.thumbnail((600,340));canvas.paste(thumb,((600-thumb.width)//2,20));ImageDraw.Draw(canvas).text((10,3),Path(item['path']).name[:72],fill='black');thumbs.append(canvas)
    sheet=Image.new('RGB',(1800,365*6),'#eeeeee')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*600,(i//3)*365))
    sheet.save(folder/'contact_sheet.png');write_json(OUT/'plots_manifest.json',figures)
    results(scores,shapes,paired,read,figures,cfg,d)
    verify()
    qa=json.loads((OUT/'QA_C3.json').read_text());qa.update(figures=len(figures),PNG_decode_nonblank=True,visual_review='PENDING_HUMAN_AGENT_CONTACT_SHEET_INSPECTION');write_json(OUT/'QA_C3.json',qa)


def results(scores,shapes,paired,read,figures,cfg,d):
    dest=ROOT/'reports/C';p=scores[scores.context=='POOLED'].copy();p['versus_M0_percent']=(p.MSE_profile/p[p.model=='M0'].MSE_profile.iloc[0]-1)*100
    s=shapes[(shapes.context=='D_FULL')&(shapes.environment=='ALL')&(shapes.label_origin=='HISTORICAL_P0')].copy()
    for c in ['H1','raw_H1','H1_error','last_bin','other_close_bins']:s[c]*=100
    family=paired[(paired.primary_family)&(paired.lag_or_block==10)]
    qa=json.loads((OUT/'QA_C3.json').read_text())
    text='''# C3 one-state EBM scientific results — development only

**C3_PASS_WITH_QUALIFICATIONS.** All five native families and the normalized M8 comparator were fitted on the exact matched cohort; architecture, source, time-resolution and daily score checks pass. Native interactions produce fitted state/time structure, but extra scientific fidelity and generalizing full-profile prediction are **NOT ESTABLISHED**. This is a sound negative developmental result, not proof that state information has zero population value.

This study uses 1,472 previously explored SPY dates (2016-01-05–2021-12-31), 78 five-minute allocation bins per date. The raw target is squared minute log returns normalized by the complete same-day RTH total; Z0 is log RV from the immediately preceding scheduled complete ordinary session. No overnight RV, same-day state, additional indicator, 2022+ C outcome, reserved B value, network transfer or raw source copy was used. The 1,491 Q-valid population is coverage only. Twelve early closes and seven incomplete ordinary days remain excluded, including four March 2020 crisis dates. R1 E-mini/open-VIX/latent periodicity is not replicated by this SPY proxy.

## What the ladder establishes

The native time feature retains all 78 nominal categories in main and pair mappings (with missing/unseen reserves). Exact graphs are T0 f(k); M3c f(k)+g(Z0); M3d f(k)+g(S0); M5 and M6 add exactly the k/state pair. Numeric Z0 is binned and stepwise; it is not a smooth derivative model. Unit rows give every date equal total fitting weight. Inference/evaluation always uses a whole date.

Fixed cyclic boosting uses validation_size=0, outer_bags=1, inner_bags=0, early_stopping_rounds=0, greedy_ratio=0, smoothing_rounds=0 and interaction_smoothing_rounds=0. Native error bands are not scientific intervals. T0 uses A (200 rounds, 2 leaves); matched additive/interaction pairs use selected B (400 rounds, 3 leaves, 16 numeric state bins). Both use max_bins=128 and max_interaction_bins=96. Configuration B won the predeclared combined-pair daily MSE criterion on inner folds 2016–17→2018 (494/245) and 2016–18→2019 (739/244). No 2020/21 scores selected settings. T0 versus M3 also changes time-training complexity; M0 supplies the stronger exact unsmoothed time-only comparator, and pairwise M3/M5 and M3d/M6 have identical complexity settings.

All balanced normalized Q rows have mean 1/78 across k. A pure native additive state shift consequently collapses to numerical zero here; observed raw M3c/M3d closure passes and their anchored D is zero. The general warning that additive vertical state shifts can violate closure still matters, but was not an empirical defect in these fits. Interactions do have small native closure defects. Their raw high-low half-L1 is not labeled TV. Separately named NORM variants use positive-part rescaling with uniform fallback when total positive mass is zero. These are different prediction maps and cannot inherit the native graph interpretation.

M8 is not an EBM: p=softmax(a+b*z_scaled), with a and b centered across 78 bins (154 identifiable coefficients). It minimizes mean daily cross entropy +0.001/2 Σb², using training-only Z0 mean/SD, stable logsumexp and analytic L-BFGS-B gradients. This is a proper log-score mean model, subsequently evaluated using the common MSE. One penalty was frozen without outcome tuning. All three solvers converged with max gradient <2e−6; all predictions are positive and sum to one.

## Predictive comparison on fixed forecasts

DEV2020 trains through 2019 (983 dates), forecasts 241 dates; DEV2021 trains through 2020 (1,224), forecasts 248. Pooled 489 dates are unique and matched. These years were explored in P0, so the term development backcheck is mandatory. D_FULL is in-sample. Stored C2R parameters/forecasts were reused without refitting their matrix.

'''
    transforms=[]
    for context in ['D_FULL','DEV_2020','DEV_2021']:
        t=load_bundle(context,models.IDS[3])[0]['transform']
        transforms.append(dict(origin=context,n_train=t['n_days'],Z0_mean=t['mean'],Z0_sd=t['sd'],S0_low_cut=t['S0']['cuts'][0],S0_high_cut=t['S0']['cuts'][1],Z0_min=t['minimum'],Z0_max=t['maximum']))
    text+='Train-only transform register (origin-specific; full fit is descriptive):\n\n'+table(pd.DataFrame(transforms))+'\n\n'
    screen=read('inner_selection_scores').groupby(['model','config']).MSE.mean().reset_index()
    text+='Inner-fold mean daily MSE, including both screened settings:\n\n'+table(screen)+'\n\nPooled developmental scorecard:\n\n'
    text+=table(p,['model','n_days','MSE_profile','versus_M0_percent','CLOSE_C_RMSE_pp','TV_valid_n','sum_defect_max'])
    text+='\n\nFull training/year/pooled scores: [profile metrics](../../artifacts/C/C3_one_state_ebm_v1_1/profile_predictive_metrics.csv), all six window definitions and calibration: [window metrics](../../artifacts/C/C3_one_state_ebm_v1_1/window_prediction_metrics.csv). Closing-share improvements are a separate objective from profile prediction. Native M5/M6 recover some closing allocation, yet the simple P-OLS-Z has lower pooled closing RMSE.\n\n## Named conditional comparison family\n\nNegative first-minus-baseline favors the first model. Intervals below condition on the frozen selected forecasts; they do not cover learner selection or future-law change. HAC uses Bartlett scheduled-session score lags, with missing eligible sessions contributing zero scores rather than fabricated Q. Shared circular scheduled-slot block resamples use B=1,000 and lengths 5/10/20, with gaps kept and circular end wrap disclosed. Holm applies only to the five named HAC10 marginal reference tests under their unverified validity premises. No 78-bin p-value family was manufactured.\n\n'
    text+=table(family,['first','baseline','metric','difference','relative_percent','HAC_lo','HAC_hi','block_lo','block_hi','Holm_p_conditional'])
    text+='\n\nM5 has worse profile MSE than M0 and matched M3c; its apparent closing-error reduction is inconclusive. M5 is also worse than M6 on the conditional profile comparison (Holm reference p≈0.0264); this does not certify that terciles preserve population information. All 11 pairs, two objectives and lags, including M5/M8, M6/M8, T0/M0, are retained in [paired tests](../../artifacts/C/C3_one_state_ebm_v1_1/paired_loss_tests.csv) and [year/state differences](../../artifacts/C/C3_one_state_ebm_v1_1/paired_loss_by_year_state.csv).\n\n## Same-row scientific fidelity\n\nH1 is high-minus-low CLOSE_C [66:78], fractions converted to pp below. H3 is TV only for valid whole normalized profiles. D(k;30) is calculated from complete predictions, never an isolated native term. Historical P0 rank cells and origin-specific train S0 cells are labeled separately. Raw high-low means at continuous singleton Z0 are not identified by fitted slices.\n\n'
    text+=table(s,['model','H1','H1_error','H3_TV','half_L1','D_max','last_bin','other_close_bins'])
    text+='\n\nThe direct +2.005pp H1 is descriptive and not certified above 2pp. M5≈+1.565pp and M6≈+1.395pp attenuate it more than P-OLS-Z≈+2.045pp or M8≈+1.904pp. Raw TV≈0.04851 is not an upper confidence/equivalence certificate below 0.05. The 15:55 raw contribution is −0.347pp while the other closing bins contribute +2.352pp; omitting the last bin is explicitly exploratory and never changes primary CLOSE_C. Full 78-bin fidelity, D, window errors and cell counts are machine outputs, with joint fixed-fit descriptive intervals at all three block lengths.\n\n## Support, environments and coarsening\n\nSupport gates count distinct dates and original five-session groups: display 30/10, basic 50/20, strong 100/30; these are operational gates rather than independence proofs. Low-state 2020 has 21 dates using the retrospective/full-S0 population and fails basic support. All high-low environmental claims involving that cell are ABSTAIN_SUPPORT, even when native model outputs are finite. Numeric state-bin occupancy, training quantile neighborhoods, extrapolation counts and native cutpoints are retained separately. DEV2020 has 11 numeric states above its training range. No imputation or extrapolated raw-mean identification is made.\n\nModel environment residual curves and half-L1 differences versus 2016–19 are in `environment_residual_discrepancy.csv`; unsupported cells are excluded from the scientific plot. Raw marginal differences and conditional supported-cell diagnostics are separate, and do not identify a pandemic mechanism. The separately named D_FULL_S0_reference2016_19_reweighted_coarse_mean fixes the 2016–19 S0 frequencies and averages each year’s same-state raw/residual profiles. It is not the original marginal estimand: `environment_reference_reweighted.csv` reports the supported 2021 comparison and ABSTAIN for 2020 because low-state overlap fails. M5/M6 coarsening reports within-tercile M5 dispersion, 16 versus 3 bins, profile losses and whole-model contrast differences. These are finite learned-resolution diagnostics, not an information-preserving coarsening theorem.\n\n## Residual, temporal and stress diagnostics\n\nDaily residual L2/PC1, full covariance/eigenvalues/closure, per-bin/state bias/RMSE/MAE, annual/quarterly mean errors, calibration quintiles, close-share tails, residual QQ and ACF/PACF/Ljung–Box/squared-residual/ARCH5/10/20 diagnostics are retained. Usual diagnostic p-values are heuristic under heavy tails, serial dependence and regime shifts. Eligible-date ACF compresses gaps and is labeled; HAC/block inference preserves scheduled gaps. No EBM hat matrix, Cook statistic, classical regression AIC or Gaussian likelihood claim is fabricated. The five deleted Cook dates come unchanged from C2R OLS-L1, never native EBM influence.\n\n'
    serial=read('serial_diagnostics');r=serial[(serial.context=='POOLED')&(serial.model.isin([models.IDS[3],models.IDS[4],'M8']))&(serial.series=='close_residual')]
    text+=table(r,['model','lag','acf','squared_acf','ljung_box_p','squared_ljung_box_p','arch_p'])
    stress=read('stress_refits_and_fixed_scores');r=stress[stress['fit'].str.startswith('ACTUAL')].copy();r['H1_pp']=r.H1*100
    text+='\n\nActual stress refits (all seed42, D_FULL descriptive; training transforms relearned on each retained cohort, historical P0 comparison labels held fixed):\n\n'+table(r,['context','model','n_days','H1_pp','MSE_profile'])
    text+='\n\nTOP1 removes the exact C2R 15 current-day largest R dates; EXCLUDE_2020 and the fixed five OLS Cook dates are identical across native families. Separately labeled FIXED_FULL_SCORE rows retain the full model and change only the scored dates. EXCLUDE2020 and TOP1 have both additive/interaction pairs; TOP5 has M5/M6 only. Native LOYO and TOP5 additive refits are NOT_PERFORMED_RESOURCE under the frozen 59-fit plan. Three named seeds (42,123,2025) on both development origins differ at most about 1.1e−17 in predictions: algorithmic determinism, not population robustness. Full-process learner/bootstrap selection uncertainty is deferred: a single resample rebuilding 18 inner native fits plus one final fit would cost about 19 fits, roughly 19,000 fits for B=1,000, well outside 60. No nominal 95% raw population curve CI is supplied.\n\n## Results ledger and stage decision\n\n| Claim | Verdict | Reason |\n|---|---|---|\n| ADDITIVE_VS_INTERACTION_SUPPORTED | NOT_ESTABLISHED as reliable increment | Nonzero fitted D is real software structure; developmental profile MSE does not improve and raw-law uncertainty is uncalibrated |\n| EBM_EXTRA_FIDELITY_SUPPORTED | NOT_ESTABLISHED | M5/M6 attenuate raw H1 more than P-OLS-Z/M8; full shape discrepancies remain |\n| EBM_PREDICTION_INCREMENT_SUPPORTED | NOT_ESTABLISHED | Neither interaction beats M0; M5 worse than matched additive control |\n| CONTINUOUS_VS_DISCRETE_INFORMATION_LOSS_DESCRIPTIVE | COMPLETED | Same raw state, train-only terciles versus numeric bins, finite losses/dispersion retained |\n| SHAPE_STABILITY | INCONCLUSIVE; ABSTAIN for low-2020 | Composition, incomplete crisis dates, stress sensitivity and no joint raw event |\n| POPULATION_INFERENCE | NOT_CERTIFIED | Dependence/selection/smoothness/support hypotheses unverified |\n\nThe implementation/QA verdict is separate from the negative scientific increment conclusion. Read [the theory audit](C3_one_state_EBM_theory_applicability.md) and [17-figure gallery](C3_one_state_EBM_figures_for_human_review.md). Any C4 proposal should first justify an added state against the strong M0/simple/M8 controls and support failures. C4/C5/C6 execution is not authorized by this result; no reserved outcomes were opened.\n'
    (dest/'C3_one_state_EBM_scientific_results.md').write_text(text)
    ledger=read('theoretical_method_ledger');availability=json.loads((OUT/'theory_source_availability.json').read_text())
    theorytext='# C3 theory applicability — actual sources and missing premises\n\nInspected the v1.1 design/handoff and the actual local `docs/specs/experiment_B_stage2C_supplied_theorem_extracts_v1.md` (selected original statements with theorem IDs, status and original line references). The original consolidation, crosswalk, verification and full Tasks were not present under their requested names. Selected excerpt availability does not establish complete original settings or proofs. Missing discovery targets and exact source hash are in `theory_source_availability.json`; these are not fabricated local files.\n\n'+table(ledger)+'\n\nThe nontrivial applications are source-specific rather than name-based: T10B.B1 distinguishes sampled model estimability from raw cell identification; counts and ABSTAIN implement the latter restriction. T24.E1 motivates separating within-state allocation from composition; no raw population kernels are known. T22.D1 is a conditional-expectation algebra identity but installed M5/M6 are fitted approximations, so their risk gap cannot equal true information value. T24.I1 needs an IID full-record experiment, a fixed partition and supplied localization bias; bounded Q alone supplies none of the missing dependence/bias assumptions. T25.I1/I2 needs a calibrated joint moment/response event and an admissibility class, not merely empirical training cuts. T25.F1 gives |model query−raw truth| ≤ observed fidelity discrepancy + valid raw-event radius only if that event already exists; C3 does not build it.\n\nT12.C1 needs Gaussian known-scale errors and the actual whole-tree selection slice; native cyclic categorical boosting on dependent SPY does not supply either. T16–18 ideal finite proper tree projection/greedy-path theory does not describe the installed cyclic learner by default. Task19 standalone statements are absent even from the excerpt; Tasks6/19/21 dependence scope cannot be promoted to an established m-dependence law. T11 continuous raw-point inference requires identification and supplied regularity; train-bin counts do not bound localization bias. Native bagged scores/error bars and three deterministic seeds are not confidence events.\n\nFull-process selection/refit inference is DEFERRED to a separately authorized C5 design. No exact Gaussian selective pivot, simultaneous raw 78-bin band, near-invariance certificate or raw singleton m CI is claimed. Finite-array closure/D identities and normalized M8 are exact computational statements; conditional HAC and exploratory scheduled blocks retain explicitly unmet population premises.\n'
    (dest/'C3_one_state_EBM_theory_applicability.md').write_text(theorytext)
    gallery='# C3 scientific gallery for human review\n\nAll figures use SPY 2016–2021 previously explored development profiles. LOW is blue, MIDDLE teal, HIGH orange. Curves are complete prediction averages over the same observed state rows, except explicitly named singleton model slices. All means and contrasts use 78-bin whole-day Q. D_FULL n=1,472 is in-sample; DEV2020/2021 n=241/248 are prior-explored backchecks. No plot establishes population truth or certified materiality.\n\n'
    overview=s[s.model.isin(models.IDS+['M8','RAW'])]
    gallery+=table(overview,['model','H1','H1_error','H3_TV','half_L1'])+'\n\nH1/H1 error columns above are pp. H3/half-L1 are fractions; H3 blank means raw closure invalid. The three state colors identify the same states across models; line style and panel title identify model and source.\n\n'
    for i,item in enumerate(figures,1):
        gallery+=f"## {i:02}. {Path(item['path']).stem[3:].replace('_',' ')}\n\n![Figure {i}](../../{item['path']})\n\n{item['interpretation']}\n\nNumerical source: `{item['source']}`. All paths refer to `artifacts/C/C3_one_state_ebm_v1_1/`.\n\n"
    gallery+='## Figure/source provenance register\n\n'+table(pd.DataFrame([dict(figure=Path(f['path']).name,numerical_source=f['source'],sha256=f['sha256']) for f in figures]))+'\n\n[Full results](C3_one_state_EBM_scientific_results.md) · [Theory applicability](C3_one_state_EBM_theory_applicability.md) · [Contact sheet](../../artifacts/C/C3_one_state_ebm_v1_1/figures/contact_sheet.png)\n'
    (dest/'C3_one_state_EBM_figures_for_human_review.md').write_text(gallery)
