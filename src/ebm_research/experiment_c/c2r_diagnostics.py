"""Daily-unit C2R diagnostics; reference p-values are exploratory, not certified."""
import warnings

import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch, het_breuschpagan, het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.multitest import multipletests
from statsmodels.tsa.stattools import acf, pacf

from .c2r_models import calendar_hac, scalar_design, profile_losses
from .readiness import WINDOWS, transform_s0


def distribution(values):
    x = np.asarray(values,float)
    return dict(mean=float(x.mean()),sd=float(x.std(ddof=1)),median=float(np.median(x)),
                mad=float(np.median(abs(x-np.median(x)))),skew=float(stats.skew(x,bias=False)),
                excess_kurtosis=float(stats.kurtosis(x,bias=False)),
                **{f'q{int(p*1000):03}':float(np.quantile(x,p)) for p in [.001,.01,.05,.5,.95,.99,.999]})


def influence_arrays(fit):
    """Exact OLS deletion identities, avoiding N repeated leave-one-out fits."""
    x, e = fit.model.exog, np.asarray(fit.resid)
    bread = np.linalg.inv(x.T@x)
    hat = np.einsum('ij,jk,ik->i',x,bread,x)
    mse, p = fit.mse_resid, x.shape[1]
    internal = e/np.sqrt(mse*(1-hat))
    deleted_mse = (np.sum(e**2)-e**2/(1-hat))/(len(e)-p-1)
    external = e/np.sqrt(deleted_mse*(1-hat))
    beta_change = (x@bread)*(e/(1-hat))[:,None]
    dfbetas = beta_change/np.sqrt(deleted_mse[:,None]*np.diag(bread))
    return dict(hat=hat,student_internal=internal,student_external=external,
                cooks=(e**2/(p*mse))*hat/(1-hat)**2,
                dffits=external*np.sqrt(hat/(1-hat)),dfbetas=dfbetas)


def linear_contrast(beta, cov, contrast, null=0., one_sided=False):
    contrast = np.asarray(contrast,float)
    estimate = float(contrast@beta)
    se = float(np.sqrt(max(0,contrast@cov@contrast)))
    z = (estimate-null)/se if se > 0 else np.nan
    p = stats.norm.sf(z) if one_sided else 2*stats.norm.sf(abs(z))
    return dict(estimate=estimate,se=se,lo=estimate-1.95996398454*se,
                hi=estimate+1.95996398454*se,p_value=float(p),null=null)


def wald(beta,cov,indices):
    b = beta[indices]; v = cov[np.ix_(indices,indices)]
    if np.linalg.matrix_rank(v) < len(indices):
        return np.nan,np.nan
    value = float(b@np.linalg.solve(v,b))
    return value,float(stats.chi2.sf(value,len(indices)))


def series_diagnostics(values, name, context, model, ddof=0):
    """Eligible-date ordered scalar serial diagnostics, never bin-row IID tests."""
    x = np.asarray(values,float); rows=[]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        ac = acf(x,nlags=20,fft=True)
        pc = pacf(x,nlags=20,method='ywm')
        sqac = acf(x*x,nlags=20,fft=True)
        for lag in [5,10,20]:
            lb = acorr_ljungbox(x,lags=[lag],return_df=True).iloc[0]
            lb2 = acorr_ljungbox(x*x,lags=[lag],return_df=True).iloc[0]
            arch = het_arch(x,nlags=lag,ddof=ddof)
            rows.append(dict(context=context,model=model,series=name,lag=lag,n_days=len(x),
                acf=float(ac[lag]),pacf=float(pc[lag]),squared_acf=float(sqac[lag]),
                ljung_box=float(lb.lb_stat),ljung_box_p=float(lb.lb_pvalue),
                squared_ljung_box=float(lb2.lb_stat),squared_ljung_box_p=float(lb2.lb_pvalue),
                arch_lm=float(arch[0]),arch_p=float(arch[1]),
                status='HEURISTIC_REFERENCE_P_VALUES; eligible-order gaps compressed for ACF/LM only'))
    return rows, dict(acf=ac.tolist(),pacf=pc.tolist(),squared_acf=sqac.tolist())


def scalar_diagnostics(model, transform, dates, z, q, slots, context):
    """OLS coefficients/HAC, design, tails, heteroskedasticity and influence."""
    fit = model.training_fit; x = fit.model.exog; e = np.asarray(fit.resid)
    n,p = x.shape; coef=[]; tests=[]; contrasts=[]; influence=[]; features=[]
    labels = transform_s0(z,transform['S0']); zs = (z-transform['mean'])/transform['sd']
    small = np.c_[np.ones(n),zs]  # fixed small auxiliary for BP/White in all models
    jb = jarque_bera(e); white = het_white(e,small)
    koenker = het_breuschpagan(e,small,robust=True)
    bp = het_breuschpagan(e,small,robust=False)
    summary = dict(context=context,model=model.name,n_days=n,rank=p,df_resid=n-p,
        condition=model.metadata['condition'],R2=float(fit.rsquared),adjusted_R2=float(fit.rsquared_adj),
        SSE=float(np.sum(e**2)),MSE=float(np.mean(e**2)),AIC=float(fit.aic),BIC=float(fit.bic),
        jarque_bera=float(jb[0]),jarque_bera_p=float(jb[1]),
        white_lm=float(white[0]),white_p=float(white[1]),BP_lm=float(bp[0]),BP_p=float(bp[1]),
        koenker_lm=float(koenker[0]),koenker_p=float(koenker[1]),
        diagnostic_reference='usual OLS/IID reference p-values are heuristic under dependence',**distribution(e))
    covs={0:np.asarray(fit.cov_params())}
    for lag in [5,10,20]:
        covs[lag]=calendar_hac(x,e,slots,lag)
    # Piecewise slope differences, categorical level differences and curvature
    # are separate nulls. There is no 78-bin significance family here.
    joint={'OLS-L1':('linear_slope',[1]),'OLS-L2':('categorical_levels',[1,2]),
           'OLS-L3':('piecewise_slope_interactions',[4,5]),'OLS-L4':('quadratic_curvature',[2])}
    for lag,cov in covs.items():
        for j,term in enumerate(model.metadata['columns']):
            r=linear_contrast(fit.params,cov,np.eye(p)[j])
            coef.append(dict(context=context,model=model.name,term=term,lag=lag,
                uncertainty='ORDINARY_DESCRIPTIVE' if lag==0 else 'CALENDAR_SCORE_HAC_CONDITIONAL',
                n_days=n,df_resid=n-p,units='closing share fraction per design unit',**r))
        if lag and model.name in joint:
            name,ix=joint[model.name]; stat,pval=wald(fit.params,cov,ix)
            tests.append(dict(context=context,model=model.name,test=name,lag=lag,statistic=stat,p_value=pval,
                              df=len(ix),status='CONDITIONAL_ASYMPTOTIC_EXPLORATORY'))
        # Actual P0 retrospective cells are passed separately in the runner;
        # scalar model contrasts here average the origin-defined S0 cells.
        delta=x[labels==2].mean(axis=0)-x[labels==0].mean(axis=0)
        contrasts.append(dict(context=context,model=model.name,target='CLOSE_C',lag=lag,
            definition='mean whole-model predictions in origin-defined S0 high minus low',
            estimate_pp=float(delta@fit.params*100),
            **{k:(v*100 if k in ['estimate','se','lo','hi'] else v) for k,v in linear_contrast(fit.params,cov,delta).items()},
            materiality='NOT_CERTIFIED',unit='percentage points'))
        if model.name=='OLS-L3':
            for g in range(3):
                delta=np.zeros(p);delta[1]=1
                if g:delta[3+g]=1
                r=linear_contrast(fit.params,cov,delta)
                coef.append(dict(context=context,model=model.name,term=f'slope_state_{g}',lag=lag,
                    uncertainty='ORDINARY_DESCRIPTIVE' if lag==0 else 'CALENDAR_SCORE_HAC_CONDITIONAL',
                    n_days=n,df_resid=n-p,units='closing share fraction per training SD Z0',**r))
    if model.name!='OLS-L0':
        augment=np.asarray(fit.fittedvalues)
        augment=(augment-augment.mean())/augment.std()
        xa=np.c_[x,augment**2]
        if np.linalg.matrix_rank(xa)==p+1:
            reset=sm.OLS(fit.model.endog,xa).fit()
            stat,pval=wald(reset.params,calendar_hac(xa,reset.resid,slots,10),[p])
            f,pf,_=reset.compare_f_test(fit)
            tests.extend([dict(context=context,model=model.name,test='RESET_power2_HAC',lag=10,statistic=stat,p_value=pval,df=1,status='CONDITIONAL_ASYMPTOTIC_EXPLORATORY'),
                          dict(context=context,model=model.name,test='RESET_power2_F',lag=0,statistic=float(f),p_value=float(pf),df=1,status='IID_REFERENCE_HEURISTIC')])
        else:
            tests.append(dict(context=context,model=model.name,test='RESET_power2',lag=0,statistic=np.nan,p_value=np.nan,df=0,status='SKIPPED_AUGMENTATION_IN_EXISTING_COLUMN_SPAN'))
    nonconstant=np.flatnonzero(np.std(x,axis=0)>1e-12)
    for j in nonconstant:
        vif=float(variance_inflation_factor(x,j))
        for k in nonconstant:
            features.append(dict(context=context,model=model.name,term=model.metadata['columns'][j],
                partner=model.metadata['columns'][k],correlation=float(np.corrcoef(x[:,j],x[:,k])[0,1]),
                VIF=vif,high_collinearity=vif>10))
    ia=influence_arrays(fit)
    for i,day in enumerate(dates):
        influence.append(dict(context=context,model=model.name,date_et=str(day),state=int(labels[i]),Z0=float(z[i]),
            fitted=float(fit.fittedvalues[i]),residual=float(e[i]),standardized_residual=float(e[i]/e.std(ddof=1)),
            hat=float(ia['hat'][i]),student_internal=float(ia['student_internal'][i]),student_external=float(ia['student_external'][i]),
            cooks=float(ia['cooks'][i]),dffits=float(ia['dffits'][i]),
            **{f'DFBETA_{j}':float(v) for j,v in enumerate(ia['dfbetas'][i])},
            flag_hat=bool(ia['hat'][i]>2*p/n),flag_cook=bool(ia['cooks'][i]>4/n),
            flag_student=bool(abs(ia['student_external'][i])>3),flag_dffits=bool(abs(ia['dffits'][i])>2*np.sqrt(p/n)),
            flag_DFBETA=bool(np.max(abs(ia['dfbetas'][i]))>2/np.sqrt(n))))
    serial,curves=series_diagnostics(e,'scalar_residual',context,model.name,p)
    return dict(summary=summary,coef=coef,tests=tests,contrasts=contrasts,influence=influence,
                features=features,serial=serial,serial_curves=curves)


def profile_diagnostics(q,pred,dates,z,labels,model,context,part,slots):
    """78-vector residual distribution/covariance, scores and calibration."""
    loss=profile_losses(q,pred);e=q-pred
    covariance=np.cov(e,rowvar=False)
    eig,vec=np.linalg.eigh(covariance);rank=int(np.linalg.matrix_rank(covariance,tol=max(eig[-1],1e-30)*1e-10))
    first=vec[:,-1]
    if first[np.argmax(abs(first))]<0:first=-first
    pc=e@first;norm=np.linalg.norm(e,axis=1)
    summary=dict(context=context,part=part,model=model.name,n_days=len(q),
        MSE_profile=float(loss['mse'].mean()),MAE_profile=float(loss['mae'].mean()),
        raw_half_L1=float(loss['half_l1'].mean()),TV_prediction=float(np.nanmean(loss['tv'])) if np.isfinite(loss['tv']).any() else np.nan,
        TV_valid_n=int(loss['simplex_valid'].sum()),negative_components=int((pred<0).sum()),negative_below_tolerance=int((pred < -1e-12).sum()),
        negative_mass=float(-np.minimum(pred,0).sum()),above_one_components=int((pred>1).sum()),
        prediction_min=float(pred.min()),prediction_max=float(pred.max()),
        sum_min=float(pred.sum(axis=1).min()),sum_max=float(pred.sum(axis=1).max()),
        sum_defect_max=float(abs(pred.sum(axis=1)-1).max()),covariance_rank=rank,
        residual_sum_max=float(abs(e.sum(axis=1)).max()),
        first_PC_variance_fraction=float(eig[-1]/eig.sum()),
        profile_roughness=float(np.mean(np.sum(np.diff(pred,axis=1)**2,axis=1))),
        adjacent_bin_absolute_variation=float(np.mean(np.sum(abs(np.diff(pred,axis=1)),axis=1))),
        max_daily_vector_norm=float(norm.max()),edge_open_bias=float(e[:,0].mean()),edge_close_bias=float(e[:,-1].mean()))
    for name,(a,b) in WINDOWS.items():
        win=e[:,a:b].sum(axis=1)
        summary.update({f'{name}_MSE':float(np.mean(win**2)),f'{name}_RMSE_pp':float(np.sqrt(np.mean(win**2))*100),
                        f'{name}_MAE_pp':float(np.mean(abs(win))*100),f'{name}_bias_pp':float(win.mean()*100),
                        f'{name}_sum_bin_SSE_fraction':float(np.sum(e[:,a:b]**2)/np.sum(e**2))})
    bins=[];daily=[]
    for k in range(78):
        bins.append(dict(context=context,part=part,model=model.name,bin=k,mean=float(e[:,k].mean()),
            variance=float(e[:,k].var(ddof=1)),RMSE=float(np.sqrt(np.mean(e[:,k]**2))),
            MAE=float(np.mean(abs(e[:,k]))),skew=float(stats.skew(e[:,k])),excess_kurtosis=float(stats.kurtosis(e[:,k])),
            state_covariance=float(np.cov(z,e[:,k])[0,1])))
    for i,day in enumerate(dates):
        daily.append(dict(context=context,part=part,model=model.name,date_et=str(day),state=int(labels[i]),
            MSE_profile=float(loss['mse'][i]),MAE_profile=float(loss['mae'][i]),raw_half_L1=float(loss['half_l1'][i]),
            simplex_valid=bool(loss['simplex_valid'][i]),close_residual=float(e[i,66:78].sum()),
            vector_norm=float(norm[i]),PC1=float(pc[i]),Z0=float(z[i]),sum_defect=float(pred[i].sum()-1)))
    serial=[]
    for name,v in [('close_residual',e[:,66:78].sum(axis=1)),('PC1',pc),('vector_norm',norm)]:
        rows,_=series_diagnostics(v,name,context,model.name)
        serial.extend(rows)
    return summary,bins,daily,serial,eig,covariance


def block_weights(slots,length,B,seed):
    """Shared circular draws over scheduled slots; no filling missing responses."""
    slots=np.asarray(slots,int);span=int(max(slots)-min(slots)+1)
    rng=np.random.default_rng(seed);weights=np.empty((B,len(slots)),float)
    for b in range(B):
        starts=rng.integers(0,span,size=int(np.ceil(span/length)))
        ix=((starts[:,None]+np.arange(length))%span).ravel()[:span]
        weights[b]=np.bincount(ix,minlength=span)[slots-min(slots)]
    return weights


def holm_family(rows,context='D_FULL'):
    names={'linear_slope','categorical_levels','piecewise_slope_interactions','quadratic_curvature',
           'RAW_H1_direction','RAW_H1_gt_0.02'}
    selected=[r for r in rows if r['context']==context and r['lag']==10 and r['test'] in names and np.isfinite(r['p_value'])]
    adjusted=multipletests([r['p_value'] for r in selected],method='holm')[1]
    for r,p in zip(selected,adjusted):
        r['p_holm_fixed_six_family']=float(p)
        r['family_size']=len(selected)
    return rows
