"""Stage2B native InterpretML models, predictor-only support and bounded diagnostics."""
import json
import time
import warnings

import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingRegressor
from scipy import stats
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch, het_breuschpagan, het_white
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.tsa.stattools import acf

from .stage2a import metric_row
from .state_models import guard_history

STATES = ['low', 'middle', 'high']


def specifications():
    """Exactly eleven families; names and interaction edges are scientifically fixed."""
    out = []
    for info in ['E', 'L']:
        for family in ['SB', 'A0c', 'A0d', 'A1d', 'A1c']:
            names = ['X'] + (['W'] if info == 'L' else [])
            if family != 'SB': names += ['S' if family.endswith('d') else 'Z']
            edges = [['X', names[-1]]] if family.startswith('A1') else []
            out.append(dict(model_id=f'{family}_{info}', family=family, info=info,
                            features=names, edges=edges))
    out.append(dict(model_id='A2c_L', family='A2c', info='L', features=['X', 'W', 'Z'],
                    edges=[['X', 'Z'], ['W', 'Z']]))
    return out


def groups(frame, protocol):
    """Original training terciles; equality belongs to lower category."""
    return np.searchsorted(protocol['cutoffs_raw'], frame.rv_open_raw.to_numpy(), side='left')


def features(frame, spec, protocol):
    """Explicit E/L projection; E does not access W and S is nominal text."""
    columns = {}
    for name in spec['features']:
        if name == 'S': columns[name] = np.asarray(STATES, dtype=object)[groups(frame, protocol)]
        else: columns[name] = frame[{'X':'x_open_bp', 'W':'w_preclose_bp', 'Z':'rv_open_log'}[name]].to_numpy()
    out=pd.DataFrame(columns, index=frame.index)
    # pandas 3 infers StringDtype; InterpretML 0.7.3 requires object for nominal text.
    if 'S' in out:out['S']=out['S'].astype(object)
    return out


def assert_graph(model, spec):
    """Check actual native edges and feature types, including nominal S."""
    names = list(model.feature_names_in_)
    expected = {tuple(sorted(names.index(f) for f in edge)) for edge in spec['edges']}
    actual = {tuple(sorted(t)) for t in model.term_features_ if len(t) > 1}
    if names != spec['features'] or actual != expected:
        raise ValueError(f'Native term graph differs for {spec["model_id"]}: {actual} != {expected}')
    for i, name in enumerate(names):
        if model.feature_types_in_[i] != ('nominal' if name == 'S' else 'continuous'):
            raise ValueError(f'Wrong native feature type {name}: {model.feature_types_in_[i]}')


def fit_native(frame, spec, protocol, setting, seed, asof, bags=8):
    """Past-only actual EBM, explicit parameters, warnings and algorithmic bag metadata."""
    guard_history(frame, asof)
    params = dict(protocol['effective_base'], **setting, outer_bags=bags, random_state=seed,
                  feature_names=spec['features'],
                  feature_types=['nominal' if c == 'S' else 'continuous' for c in spec['features']],
                  interactions=[tuple(spec['features'].index(c) for c in edge) for edge in spec['edges']] or 0)
    started = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        model = ExplainableBoostingRegressor(**params).fit(features(frame, spec, protocol), frame.y_last30_bp)
    elapsed = time.perf_counter()-started
    assert_graph(model, spec)
    meta = dict(n=len(frame), first=str(frame.session_et.iloc[0]), last=str(frame.session_et.iloc[-1]),
                asof=asof, fit_seconds=elapsed, effective_parameters=params,
                term_features=[list(t) for t in model.term_features_], term_names=list(model.term_names_),
                n_terms=len(model.term_features_), n_interactions=len(spec['edges']),
                best_iteration=np.asarray(model.best_iteration_).tolist(),
                bag_weights=np.asarray(model.bag_weights_).tolist(),
                bins=[[b if isinstance(b,dict) else np.asarray(b).tolist() for b in levels] for levels in model.bins_],
                warnings=[str(w.message) for w in caught],
                score_bytes=sum(t.nbytes for t in model.term_scores_),
                nonempty_bins=[int((w>0).sum()) for w in model.bin_weights_],
                term_ranges=[[float(t.min()),float(t.max())] for t in model.term_scores_],
                term_importances=model.term_importances().tolist(),
                max_native_cell_weight=[float(w.max()) for w in model.bin_weights_],
                sparse_occupied_bins=[int(((w>0)&(w<20)).sum()) for w in model.bin_weights_])
    return model, meta


def cell_mask(frame, protocol, candidate, state, endpoint):
    """Local nonzero X window × RV tercile, additionally fixed W band for L."""
    g=groups(frame,protocol)
    m=(g==state)&(np.abs(frame.x_open_bp.to_numpy()-endpoint)<=candidate['h'])
    if candidate['info']=='L':
        m &= np.abs(frame.w_preclose_bp.to_numpy()-candidate['w'])<=candidate['w_halfwidth']
    return m


def candidate_rows(frame, protocol, candidate, cohort):
    """Four local cells with distinct fixed five-row blocks and predictor ranges."""
    rows=[]; block=np.arange(len(frame))//5
    for state in [0,2]:
        for endpoint in [-candidate['a'],candidate['a']]:
            m=cell_mask(frame,protocol,candidate,state,endpoint); sub=frame.loc[m]
            n=int(m.sum()); blocks=int(np.unique(block[m]).size)
            years=sub.session_et.astype(str).str[:4].value_counts().to_dict()
            rows.append(dict(candidate_id=candidate['candidate_id'],cohort=cohort,info=candidate['info'],
                             state=STATES[state],endpoint=endpoint,n=n,blocks=blocks,
                             supported=n>=50 and blocks>=20,strong=n>=100 and blocks>=30,
                             h=candidate['h'],w=candidate['w'],w_halfwidth=candidate['w_halfwidth'],
                             x_min=float(sub.x_open_bp.min()) if n else None,x_max=float(sub.x_open_bp.max()) if n else None,
                             z_min=float(sub.rv_open_log.min()) if n else None,z_max=float(sub.rv_open_log.max()) if n else None,
                             year_counts=json.dumps(years),max_year_fraction=max(years.values())/n if n else None))
    return rows


def support_screen(train, protocol):
    """Deterministic predictor-only ordered candidates; no fit or outcome input."""
    result={}; allrows=[]
    for info in ['E','L']:
        choices=[]
        for a in [10,20,30,50]:
            for h in [5,10,15]:
                if h>=a: continue
                for w in ([0.] if info=='E' else [0.,float(train.w_preclose_bp.median())]):
                    for width in ([None] if info=='E' else [5.,10.,20.]):
                        c=dict(info=info,a=float(a),h=float(h),w=w,w_halfwidth=width,
                               candidate_id=f'{info}_{len(choices):02d}')
                        rows=candidate_rows(train,protocol,c,'train'); allrows.extend(rows)
                        c['supported']=all(r['supported'] for r in rows); choices.append(c)
        chosen=next((c for c in choices if c['supported']),None)
        # Failed screens retain the first predeclared candidate only for masked diagnostics.
        result[info]=dict(status='SUPPORTED_BAND_DESIGN' if chosen else 'ABSTAIN',
                          chosen=chosen,display_candidate=chosen or choices[0],candidates=choices,
                          z_representatives=protocol['z_representatives'],
                          scientific_interval_status='NOT_CERTIFIED_POINTWISE')
    return result,allrows


def query_frame(x,z,w):
    """Full feature rows at training-defined coordinates, without outcomes."""
    x,z,w=np.broadcast_arrays(x,z,w)
    return pd.DataFrame(dict(x_open_bp=x.ravel(),rv_open_log=z.ravel(),
                             rv_open_raw=np.exp(z.ravel())-1e-8,w_preclose_bp=w.ravel()))


def contrast(model,spec,protocol,grid):
    """Four total predictions; not an isolated centered software interaction."""
    c=grid[spec['info']]['display_candidate']; lo,_,hi=protocol['z_representatives']
    f=query_frame([-c['a'],c['a'],-c['a'],c['a']],[lo,lo,hi,hi],c['w'])
    p=model.predict(features(f,spec,protocol)); d=float(p[3]-p[2]-p[1]+p[0])
    if not spec['edges'] and abs(d)>1e-9: raise ValueError('Additive whole-response contrast is nonzero')
    return dict(D_F=d,increment_low=float(p[1]-p[0]),increment_high=float(p[3]-p[2]),
                x_minus=-c['a'],x_plus=c['a'],w=c['w'],z_low=lo,z_high=hi,
                support_status=grid[spec['info']]['status'],interval_status='NOT_CERTIFIED',
                scientific_status='EXPLORATORY_FITTED' if grid[spec['info']]['chosen'] else 'ABSTAIN')


def metrics(frame,pred,n1,**keys):
    """Reuse Stage2A matched metrics and add named nonlinear diagnostics."""
    row=metric_row(frame,pred,n1,**keys)
    y=frame.y_last30_bp.to_numpy(); p=np.asarray(pred)
    row.update(Spearman=float(stats.spearmanr(p,y).statistic) if np.std(p)>1e-12 else None,
               forecast_SD=float(p.std()),forecast_min=float(p.min()),forecast_max=float(p.max()),
               positive_forecast_fraction=float(np.mean(p>0)),
               in_sample_R2=1-float(np.sum((p-y)**2)/np.sum((y-y.mean())**2)))
    return row


def residual_diagnostics(frame,pred,protocol,**keys):
    """Nonlinear residual battery; classical references disclosed, no OLS pseudo-inference."""
    y=frame.y_last30_bp.to_numpy(); p=np.asarray(pred); u=y-p; rows=[]
    def add(name,value=None,p_value=None,status='DESCRIPTIVE',**extra):
        rows.append(dict(keys,statistic=name,estimate=None if value is None else float(value),
                         p_value=None if p_value is None else float(p_value),n=len(y),status=status,**extra))
    for name,value in [('skewness',stats.skew(u)),('Pearson_kurtosis',stats.kurtosis(u,fisher=False)),
                       ('Durbin_Watson',durbin_watson(u))]: add(name,value)
    jb=jarque_bera(u); add('Jarque_Bera',jb[0],jb[1],assumptions='IID asymptotic diagnostic only; fitted nonlinear residuals and dependence limit reference')
    for q in [0,.001,.01,.05,.5,.95,.99,.999,1]:add(f'residual_quantile_{q}',np.quantile(u,q))
    for label,v in [('residual',u),('squared_residual',u*u)]:
        a=acf(v,nlags=20,fft=False)
        lb=acorr_ljungbox(v,lags=[5,10,20],model_df=0,return_df=True)
        for lag in [1,5,10,20]:add(f'{label}_ACF_{lag}',a[lag])
        for lag,r in lb.iterrows():add(f'{label}_LjungBox_{lag}',r.lb_stat,r.lb_pvalue,
                                     assumptions='Asymptotic weak-dependence diagnostic; fitted learner df not subtracted, not an exact conditional-mean test')
    arch=het_arch(u,nlags=5,ddof=0,result_object=False); add('ARCH_LM5',arch[0],arch[1],assumptions='Asymptotic ARCH reference on fitted residuals; descriptive, not EBM consistency proof')
    z=frame.rv_open_log.to_numpy(); x=frame.x_open_bp.to_numpy()
    aux=np.c_[np.ones(len(x)),(x-x.mean())/x.std(),(z-z.mean())/z.std()]
    bp=het_breuschpagan(u,aux,robust=True);white=het_white(u,aux)
    for name,result in [('Koenker_BP_small_XZ',bp),('White_small_XZ',white)]:
        add(name,result[0],result[1],assumptions='Small predeclared 1+standardized X+Z auxiliary design; IID chi-square reference is heuristic under temporal dependence/nonlinear fitting')
    for label,values in [('X',x),('Z',z),('forecast',p),('time_index',np.arange(len(u)))]+([('W',frame.w_preclose_bp.to_numpy())] if keys.get('info')=='L' else []):
        for transform,v in [('absolute',abs(u)),('squared',u*u)]:
            add(f'{transform}_residual_spearman_{label}',stats.spearmanr(values,v).statistic if np.std(values)>1e-12 else None)
        b=pd.qcut(values,10,duplicates='drop')
        t=pd.DataFrame(dict(bin=b,x=values,u=u))
        for j,(_,part) in enumerate(t.groupby('bin',observed=True)):
            add('residual_bin_mean',part.u.mean(),predictor=label,bin=j,bin_n=len(part),predictor_mean=part.x.mean(),supported=len(part)>=20)
    g=groups(frame,protocol)
    for j,name in enumerate(STATES):
        v=u[g==j]
        if len(v):add('state_residual_SD',v.std(),state=name,group_n=len(v));add('state_residual_mean',v.mean(),state=name,group_n=len(v))
    for date_index in np.argsort(abs(u))[-5:][::-1]:
        add('largest_absolute_residual',abs(u[date_index]),session_et=str(frame.session_et.iloc[date_index]),
            signed_residual=float(u[date_index]),note='Descriptive rank; not Cook/leverage and no selection for deletion')
    if p.std()>1e-12:
        cal=OLS(y,np.c_[np.ones(len(y)),p]).fit()
        add('calibration_intercept',cal.params[0]);add('calibration_slope',cal.params[1])
    else:add('calibration_slope',status='NOT_APPLICABLE',note='Constant forecast')
    for name in ['OLS_Cook_leverage_DFBETA','ordinary_adjusted_R2','OLS_joint_parameter_Wald','RESET_native_EBM_design']:
        add(name,status='NOT_APPLICABLE',note='No fixed unpenalized OLS coefficient/design df for the native boosted bagged learner')
    return rows


def paired_hac(loss_gain,lag=5):
    """Fixed paired daily losses, Bartlett HAC n/(n-1), normal asymptotic 95%."""
    d=np.asarray(loss_gain,dtype=float)
    r=OLS(d,np.ones((len(d),1))).fit().get_robustcov_results(cov_type='HAC',maxlags=lag,
                                                          kernel='bartlett',use_correction=True,use_t=False)
    return dict(mean_loss_gain=float(r.params[0]),se=float(r.bse[0]),
                ci_low=float(r.conf_int()[0,0]),ci_high=float(r.conf_int()[0,1]),p_value=float(r.pvalues[0]))


def paired_losses(candidate,comparator):
    """Match session keys and identical outcomes before constructing loss gains."""
    if (candidate.session_et.duplicated().any() or comparator.session_et.duplicated().any()
            or set(candidate.session_et)!=set(comparator.session_et)):
        raise ValueError('Paired EBM comparisons require identical unique date keys')
    other=comparator.set_index('session_et').loc[candidate.session_et]
    if not np.array_equal(candidate.actual.to_numpy(),other.actual.to_numpy()):
        raise ValueError('Paired EBM comparison has different actual Y')
    return (other.forecast.to_numpy()-other.actual.to_numpy())**2-(candidate.forecast.to_numpy()-candidate.actual.to_numpy())**2


def block_interval(values,block=5,repetitions=500,seed=42):
    """Circular moving-block percentile sensitivity, fixed forecasts, no learner refit."""
    v=np.asarray(values,dtype=float);rng=np.random.default_rng(seed);n=len(v)
    starts=rng.integers(n,size=(repetitions,int(np.ceil(n/block))))
    idx=(starts[...,None]+np.arange(block))%n
    samples=v[idx.reshape(repetitions,-1)[:,:n]].mean(axis=1)
    return dict(ci_low=float(np.quantile(samples,.025)),ci_high=float(np.quantile(samples,.975)),
                bootstrap_repetitions=repetitions,block=block,method='fixed-loss circular moving-block percentile; stationarity/weak-dependence/moments assumed; selection not rerun')
