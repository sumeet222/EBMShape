"""Explicit native graph, training transforms and software audit; no selection here."""
import pickle
import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingRegressor
from ..readiness import fit_s0, transform_s0
from ..c2r_models import date_hash

IDS=['T0_EBM_TIME_ONLY','M3c_EBM_ADDITIVE','M3d_EBM_ADDITIVE','M5_EBM_CONT_INTERACT','M6_EBM_DISC_INTERACT']
LABELS=np.array([f'{k:02}' for k in range(78)])


def transform(dates,z,bins):
    """Freeze all state transforms on the supplied whole-date training sample."""
    return dict(S0=fit_s0(pd.DataFrame(dict(date_et=dates,Z0=z)),str(max(dates))),
                cuts=np.unique(np.quantile(z,np.arange(1,bins)/bins,method='linear')).tolist(),
                mean=float(np.mean(z)),sd=float(np.std(z)),minimum=float(min(z)),maximum=float(max(z)),
                quantiles=np.quantile(z,[.1,.25,.5,.75,.9]).tolist(),train_date_hash=date_hash(dates),
                n_days=len(z),first=str(min(dates)),last=str(max(dates)))


def design(z,model,t):
    """Exactly 78 rows per date; k nominal, numeric Z0 or nominal train S0."""
    n=len(z); x=np.empty((n*78,1 if model==IDS[0] else 2),object);x[:,0]=np.tile(LABELS,n)
    if model!=IDS[0]:
        values=np.asarray(z,float) if model in [IDS[1],IDS[3]] else np.array(['low','middle','high'])[transform_s0(z,t['S0'])]
        x[:,1]=np.repeat(values,78)
    return x


def kwargs(model,t,config,seed):
    values=dict(config['kwargs']);values['random_state']=int(seed)
    values['feature_names']=['k'] if model==IDS[0] else ['k','Z0' if model in [IDS[1],IDS[3]] else 'S0']
    values['feature_types']=['nominal'] if model==IDS[0] else ['nominal',t['cuts'] if model in [IDS[1],IDS[3]] else 'nominal']
    values['interactions']=[(0,1)] if model in IDS[3:] else []
    return values


def audit(model,z,name,t):
    """Fail invalid graphs/time maps; record native software quantities honestly."""
    expected=[(0,)] if name==IDS[0] else [(0,),(1,)]+([(0,1)] if name in IDS[3:] else [])
    if model.term_features_!=expected:raise ValueError('INVALID_GRAPH: '+str(model.term_features_))
    for resolution in model.bins_[0]:
        if set(resolution)!=set(LABELS) or len(set(resolution.values()))!=78:
            raise ValueError('INVALID_TIME_RESOLUTION')
    if name in IDS[3:]:
        pair_time=model.bins_[0][min(1,len(model.bins_[0])-1)]
        if max(pair_time.values())>=model.term_scores_[-1].shape[0]-1:
            raise ValueError('INVALID_PAIR_TIME_RESOLUTION')
    x=design(np.asarray(z)[:5],name,t)
    reconstructed=np.asarray(model.intercept_)+model.eval_terms(x).sum(axis=1)
    np.testing.assert_allclose(model.predict(x),reconstructed,atol=1e-12,rtol=0)
    np.testing.assert_allclose(model.predict(x),pickle.loads(pickle.dumps(model)).predict(x),atol=0,rtol=0)
    edge=design(np.array([-1e6,1e6]),name,t);edge[0,0]='UNKNOWN_TIME'
    if name in [IDS[2],IDS[4]]:edge[0,1]='UNKNOWN_STATE'
    assert np.isfinite(model.predict(edge)).all()
    params=model.get_params(); assert params['validation_size']==0 and params['outer_bags']==1 and params['inner_bags']==0 and params['early_stopping_rounds']==0
    return dict(graph=model.term_features_,term_names=model.term_names_,bins=model.bins_,
                term_scores=model.term_scores_,bin_weights=model.bin_weights_,intercept=model.intercept_,
                best_iteration=getattr(model,'best_iteration_','NOT_EXPOSED'),
                bagged_scores=getattr(model,'bagged_scores_','NOT_EXPOSED'),
                term_importances=model.term_importances(),parameters=params,
                time_levels=[len(x) for x in model.bins_[0]],
                reconstruction_max=float(abs(model.predict(x)-reconstructed).max()),serialization_parity=True,
                edge_finite=True,uncertainty='NO_POPULATION_CI',
                iteration_semantics='max_rounds cycles with n_terms steps each stage; no early stop',
                effective_shapes=[s.shape for s in model.term_scores_],
                score_levels=[len(np.unique(s)) for s in model.term_scores_])


def predict(bundle,z):
    return bundle['model'].predict(design(z,bundle['name'],bundle['transform'])).reshape(-1,78)


def normalized(raw):
    """Separately named positive-part closure map; uniform fallback if zero mass."""
    p=np.maximum(np.asarray(raw),0);s=p.sum(axis=1,keepdims=True)
    return np.divide(p,s,out=np.full_like(p,1/78),where=s>0)
