"""Stage 2A state regressions and natural cubic varying slopes; no EBM code."""
import json

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.regression.linear_model import OLS
from statsmodels.robust.robust_linear_model import RLM
from statsmodels.robust.norms import HuberT


def specifications():
    """Bounded E/L candidates, including labeled late W-moderation sensitivities."""
    models=[]
    for info in ['E','L']:
        for family in ['C1','C2','S4','S6']:
            models.append(dict(model_id=f'{family}_{info}',family=family,info=info,w_moderation=False,
                               primary=family!='S6',complexity_role='primary' if family!='S6' else 'higher_df_sensitivity'))
    models += [dict(model_id=f'{f}_L_Wmod',family=f,info='L',w_moderation=True,primary=False,
                    complexity_role='optional_W_moderation') for f in ['C1','C2']]
    models += [dict(model_id=i,family=f,info=info,w_moderation=False,primary=False,complexity_role='reference')
               for i,f,info in [('OLS1_E','OLS1','E'),('OLS3_L','OLS3','L'),('OLS2_L','OLS2','L')]]
    return models


def guard_history(frame, asof):
    """Require unique ordered development dates with completed targets before asof."""
    dates=frame.session_et.astype(str)
    if (frame.empty or asof>'2024-01-01' or not dates.between('2016-01-05','2023-12-31').all()
            or not dates.lt(asof).all() or dates.duplicated().any() or not dates.is_monotonic_increasing):
        raise ValueError(f'Forbidden fit history/asof={asof}; ordered development rows strictly before forecast only')
    if 'eligible_primary' in frame and not frame.eligible_primary.all():
        raise ValueError('Ineligible observations in Stage2A history')


def raw_rcs(z,knots):
    """Restricted cubic curvature terms with linear tails, scaled by knot range².

    K knots span 1,Z and K-2 curvature terms, hence K dimensions per function.
    h_j=[(z-k_j)+³-A_j(z-k_penultimate)+³+B_j(z-k_last)+³]/range².
    """
    z=np.asarray(z,dtype=float).reshape(-1);k=np.asarray(knots,dtype=float)
    if len(k)<4 or np.any(np.diff(k)<=0):raise ValueError('Non-distinct spline knots')
    last,penultimate=k[-1],k[-2]
    return np.column_stack([(np.maximum(z-a,0)**3-(last-a)/(last-penultimate)*np.maximum(z-penultimate,0)**3
                             +(penultimate-a)/(last-penultimate)*np.maximum(z-last,0)**3)/(last-k[0])**2 for a in k[:-2]])


def fit_preprocessing(frame,asof):
    """Fit predictor-only cutoffs, centering and natural spline transforms on past."""
    guard_history(frame,asof)
    z=frame.rv_open_log.to_numpy();ref=float(np.median(z));centered=z-ref
    cuts=np.quantile(frame.rv_open_raw,[1/3,2/3],method='linear')
    groups=np.searchsorted(cuts,frame.rv_open_raw,side='left')
    out=dict(asof=asof,n=len(frame),first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),
             cutoffs_raw=cuts.tolist(),cutoffs_log=np.log(cuts+1e-8).tolist(),z_ref=ref,
             representatives=[float(np.median(z[groups==g])) for g in range(3)],
             z_quantiles_20_50_80=np.quantile(z,[.2,.5,.8]).tolist(),
             ranges={c:[float(frame[c].min()),float(frame[c].max())] for c in ['x_open_bp','w_preclose_bp','rv_open_log']},splines={})
    for dim,q in [(4,[.05,.35,.65,.95]),(6,[.05,.23,.41,.59,.77,.95])]:
        knots=np.quantile(z,q,method='linear');h=raw_rcs(z,knots)
        projection=np.linalg.lstsq(np.c_[np.ones(len(z)),centered],h,rcond=None)[0]
        residual=h-np.c_[np.ones(len(z)),centered]@projection
        offset=raw_rcs([ref],knots)[0]-np.array([1.,0.])@projection
        scale=np.std(residual,axis=0,ddof=0)
        if np.any(scale<=1e-12):raise ValueError('Degenerate spline curvature scale')
        out['splines'][str(dim)]=dict(dimension=dim,degree=3,quantiles=q,knots=knots.tolist(),
                                      projection=projection.tolist(),offset=offset.tolist(),scale=scale.tolist(),
                                      boundaries=[float(knots[0]),float(knots[-1])],tail='linear; never clipped')
    return out


def curvature(z,pre,dimension):
    """Apply training-frozen, centered/scaled natural curvature at any finite Z."""
    z=np.asarray(z,dtype=float).reshape(-1);s=pre['splines'][str(dimension)]
    h=raw_rcs(z,s['knots'])-np.c_[np.ones(len(z)),z-pre['z_ref']]@np.asarray(s['projection'])
    return (h-np.asarray(s['offset']))/np.asarray(s['scale'])


def design(frame,spec,pre):
    """Explicit E/L matrix; E never reads W, and C2 is literally nested in S1."""
    n=len(frame);family=spec['family'];x=frame.x_open_bp.to_numpy()
    columns={'intercept':np.ones(n)}
    if family=='OLS2':columns['W']=frame.w_preclose_bp.to_numpy()
    else:columns['X']=x
    if family=='C1':
        g=np.searchsorted(pre['cutoffs_raw'],np.exp(frame.rv_open_log.to_numpy())-1e-8,side='left')
        if 'rv_open_raw' in frame:g=np.searchsorted(pre['cutoffs_raw'],frame.rv_open_raw,side='left')
        for j,name in [(1,'M'),(2,'H')]:columns['D'+name]=(g==j).astype(float);columns['X_D'+name]=x*(g==j)
    elif family in ['C2','S4','S6']:
        z=frame.rv_open_log.to_numpy();zc=z-pre['z_ref']
        columns['Zc']=zc;columns['X_Zc']=x*zc
        if family.startswith('S'):
            h=curvature(z,pre,int(family[1:]))
            for j in range(h.shape[1]):columns[f'H{j+1}']=h[:,j];columns[f'X_H{j+1}']=x*h[:,j]
    if spec['info']=='L' and family!='OLS2':columns['W']=frame.w_preclose_bp.to_numpy()
    if spec['w_moderation']:
        w=frame.w_preclose_bp.to_numpy()
        if family=='C1':columns['W_DM']=w*(g==1);columns['W_DH']=w*(g==2)
        else:columns['W_Zc']=w*(frame.rv_open_log.to_numpy()-pre['z_ref'])
    out=pd.DataFrame(columns,index=frame.index)
    if not np.isfinite(out.to_numpy()).all():raise ValueError(f'Nonfinite design {spec["model_id"]}')
    return out


def fit_model(frame,spec,pre,asof,robust=False):
    """Guard then SVD OLS or point-only Huber; reject rank loss explicitly."""
    guard_history(frame,asof);d=design(frame,spec,pre);x=d.to_numpy()
    rank=int(np.linalg.matrix_rank(x));condition=float(np.linalg.cond(x))
    if rank!=x.shape[1] or condition>1e12:
        raise ValueError(f'Rank/conditioning failure {spec["model_id"]}: rank={rank}, p={x.shape[1]}, cond={condition}')
    y=frame.y_last30_bp.to_numpy()
    if not np.isfinite(y).all():raise ValueError('Nonfinite fit outcome')
    result=(RLM(y,x,M=HuberT(t=1.345)).fit(maxiter=200,tol=1e-8,scale_est='mad') if robust
            else OLS(y,x,hasconst=True).fit(method='pinv'))
    return dict(result=result,design=d,columns=list(d.columns),pre=pre,spec=spec,rank=rank,condition=condition)


def covariance(fit,kind=5):
    """Bartlett HAC with n/(n-k), normal reference; OLS and HC3 comparators."""
    result=fit['result']
    if kind=='OLS':return result
    if kind=='HC3':return result.get_robustcov_results(cov_type='HC3',use_t=False)
    return result.get_robustcov_results(cov_type='HAC',maxlags=int(kind),kernel='bartlett',use_correction=True,use_t=False)


def evaluate_linear(fit,vector,lag=5):
    """Covariance propagation for one fixed linear contrast, not CI subtraction."""
    v=np.asarray(vector,dtype=float);result=covariance(fit,lag);estimate=float(v@result.params)
    variance=float(v@result.cov_params()@v)
    if variance < -1e-9:raise ValueError('Negative contrast variance')
    se=float(np.sqrt(max(variance,0)));p=float(2*norm.sf(abs(estimate/se))) if se>0 else None
    return dict(estimate=estimate,se=se,ci_low=estimate-1.959963984540054*se,ci_high=estimate+1.959963984540054*se,p_value=p)


def vector_at(fit,x,z,w=0):
    """Whole response design row at one named state, including all intercept terms."""
    f=pd.DataFrame(dict(x_open_bp=[x],rv_open_log=[z],w_preclose_bp=[w]))
    return design(f,fit['spec'],fit['pre']).to_numpy()[0]


def slope_vector(fit,z,w=0):
    """Full-row difference at X=1 and X=0, valid since these models are linear in X."""
    return vector_at(fit,1,z,w)-vector_at(fit,0,z,w)


def wald(fit,columns,lag=5):
    """Independent coefficient restrictions; withhold singular covariance p-values."""
    indices=[fit['columns'].index(c) for c in columns]
    if not indices:return dict(status='NOT_APPLICABLE',note='empty block')
    r=np.eye(len(fit['columns']))[indices];cov=covariance(fit,lag)
    if np.linalg.matrix_rank(r@cov.cov_params()@r.T)!=len(indices):
        return dict(status='ABSTAIN',note='singular restriction covariance',df=len(indices))
    test=cov.wald_test(r,use_f=False,scalar=True)
    return dict(status='COMPUTED',statistic=float(test.statistic),p_value=float(test.pvalue),df=len(indices))


def preprocessing_hash(pre):
    """Portable identity of predictor-only preprocessing, including quarterly fits."""
    import hashlib
    return hashlib.sha256(json.dumps(pre,sort_keys=True,allow_nan=False).encode()).hexdigest()
