"""Small C2R OLS/spline benchmarks for daily 78-component allocation curves.

No source access or model selection occurs here. All transforms are fitted on
the supplied training dates; raw predictions are retained without projection.
"""
from dataclasses import dataclass
import hashlib

import numpy as np
import pandas as pd
from scipy.interpolate import BSpline, CubicSpline
import statsmodels.api as sm

from .readiness import fit_s0, transform_s0, WINDOWS

SCALAR_IDS = [f'OLS-L{i}' for i in range(5)]
PROFILE_IDS = ['M0', 'M1', 'P-OLS-Z', 'M2-T8', 'M2-T12',
               'M4-T8-Z4', 'M4-T12-Z4', 'NOINT-T8-Z4', 'NOINT-T12-Z4']


def date_hash(dates):
    return hashlib.sha256(('\n'.join(map(str, dates))+'\n').encode()).hexdigest()


def check_design(x, max_condition=1e10):
    """Reject unidentifiable fits rather than manufacture coefficient tests."""
    rank = np.linalg.matrix_rank(x)
    condition = float(np.linalg.cond(x))
    if rank != x.shape[1] or condition > max_condition:
        raise ValueError(f'ABSTAIN_DESIGN: rank={rank}/{x.shape[1]}, condition={condition:.6g}')
    return int(rank), condition


def time_basis(df):
    """Clamped cubic B splines on k=0..77, uniform fixed knots, row sum one."""
    degree = 3
    interior = np.linspace(0, 77, df-degree+1)[1:-1]
    knots = np.r_[np.zeros(4), interior, np.full(4, 77.)]
    basis = BSpline.design_matrix(np.arange(78.), knots, degree).toarray()
    check_design(basis)
    np.testing.assert_allclose(basis.sum(axis=1), 1., atol=1e-14)
    return basis, dict(df=df, degree=degree, knots=knots.tolist(), boundary=[0,77],
                       convention='clamped_uniform_B_spline_partition_of_unity')


def natural_basis(values, knots):
    """Four-knot natural cardinal cubic basis, with linear continuation outside.

    The four columns span a constant, a linear trend and two nonlinear terms.
    Boundary and internal knots come only from the origin's training Z0.
    """
    values = np.asarray(values, float)
    knots = np.asarray(knots, float)
    if len(knots) != 4 or not np.all(np.diff(knots) > 0):
        raise ValueError('ABSTAIN_STATE_KNOTS: four distinct ordered training knots required')
    spline = CubicSpline(knots, np.eye(4), bc_type='natural', axis=0)
    bounded = np.clip(values, knots[0], knots[-1])
    basis = spline(bounded)
    left, right = values < knots[0], values > knots[-1]
    basis[left] += (values[left]-knots[0])[:,None]*spline(knots[0],1)
    basis[right] += (values[right]-knots[-1])[:,None]*spline(knots[-1],1)
    return basis


def scalar_design(zs, labels, model):
    """Fixed column order for scalar closing-share OLS; intercept always first."""
    zs, labels = np.asarray(zs), np.asarray(labels)
    one = np.ones(len(zs)); mid = (labels == 1).astype(float); high = (labels == 2).astype(float)
    values = {'intercept':one, 'z_s':zs, 'mid':mid, 'high':high,
              'z_s:mid':zs*mid, 'z_s:high':zs*high, 'z_s^2':zs**2}
    names = {'OLS-L0':['intercept'], 'OLS-L1':['intercept','z_s'],
             'OLS-L2':['intercept','mid','high'],
             'OLS-L3':['intercept','z_s','mid','high','z_s:mid','z_s:high'],
             'OLS-L4':['intercept','z_s','z_s^2']}[model]
    return np.column_stack([values[k] for k in names]), names


@dataclass
class Model:
    name: str
    coef: np.ndarray
    metadata: dict
    training_fit: object = None

    def predict(self, z, transform):
        z = np.asarray(z, float)
        zs = (z-transform['mean'])/transform['sd']
        labels = transform_s0(z, transform['S0'])
        if self.name in SCALAR_IDS:
            x, _ = scalar_design(zs, labels, self.name)
            return x@self.coef
        if self.name == 'M0':
            return np.broadcast_to(self.coef, (len(z),78)).copy()
        if self.name == 'M1':
            return self.coef[labels]
        if self.name == 'P-OLS-Z':
            return np.c_[np.ones(len(z)),zs]@self.coef
        bt = np.asarray(self.metadata['time_basis'])
        if self.name.startswith('M2'):
            return np.broadcast_to(bt@self.coef, (len(z),78)).copy()
        bz = natural_basis(zs, transform['state_knots_standardized'])
        if self.name.startswith('M4'):
            return bz@self.coef@bt.T
        # No-interaction additive control: centered state main effect is
        # constant over time, and almost zero for a closed response.
        state = (bz-transform['bz_mean'])@np.asarray(self.metadata['state_directions'])
        return bt@self.coef[:bt.shape[1]] + (state@self.coef[bt.shape[1]:])[:,None]


def fit_models(dates, z, q, slots):
    """Fit the frozen five scalar/nine profile candidates, one small origin."""
    z, q, dates, slots = np.asarray(z), np.asarray(q), np.asarray(dates), np.asarray(slots)
    if q.shape != (len(z),78) or len(set(dates)) != len(dates):
        raise ValueError('C2R_INPUT: require distinct dates and N x 78 Q')
    if not np.isfinite(q).all() or not np.isfinite(z).all():
        raise ValueError('C2R_INPUT: nonfinite training features or response')
    mean, sd = float(z.mean()), float(z.std(ddof=0))
    if sd <= 0:
        raise ValueError('ABSTAIN_STATE: no training Z0 variation')
    s0 = fit_s0(pd.DataFrame(dict(date_et=dates, Z0=z)), str(max(dates)))
    labels = transform_s0(z, s0); zs = (z-mean)/sd
    knots = np.quantile(zs, [0,1/3,2/3,1], method='linear')
    bz = natural_basis(zs, knots); rz, cz = check_design(bz)
    counts = [int((labels == i).sum()) for i in range(3)]
    groups = [len(set(slots[labels == i]//5)) for i in range(3)]
    transform = dict(mean=mean, sd=sd, S0=s0, state_knots_standardized=knots.tolist(),
                     training_range=[float(min(z)),float(max(z))],
                     quantiles={str(p):float(np.quantile(z,p)) for p in [.1,.25,.5,.75,.9]},
                     quintile_cuts=np.quantile(z,[.2,.4,.6,.8]).tolist(),
                     train_counts=counts, train_five_session_groups=groups,
                     train_date_hash=date_hash(dates), train_first=str(min(dates)), train_last=str(max(dates)))
    models = {}
    closing = q[:,66:78].sum(axis=1)
    for name in SCALAR_IDS:
        x, names = scalar_design(zs, labels, name)
        rank, cond = check_design(x)
        result = sm.OLS(closing,x,hasconst=True).fit()
        models[name] = Model(name, result.params,
                            dict(columns=names,rank=rank,condition=cond,n_days=len(z),edf=rank), result)
    mu = q.mean(axis=0)
    models['M0'] = Model('M0',mu,dict(rank=78,edf=78,condition=1.,n_days=len(z)))
    # Frozen basic support gate; unsupported group predictions fall back to M0.
    ok = [counts[g] >= 50 and groups[g] >= 20 for g in range(3)]
    curves = np.array([q[labels==g].mean(axis=0) if ok[g] else mu for g in range(3)])
    models['M1'] = Model('M1',curves,dict(rank=78*sum(ok),edf=78*sum(ok),condition=1.,
                                        supported_groups=ok, fallback='M0',n_days=len(z)))
    x = np.c_[np.ones(len(z)),zs]; rank,cond = check_design(x)
    coef = np.linalg.lstsq(x,q,rcond=None)[0]
    models['P-OLS-Z'] = Model('P-OLS-Z',coef,dict(rank=rank*78,edf=rank*78,rank_per_bin=rank,
        condition=cond,n_days=len(z),sum_intercepts=float(coef[0].sum()),sum_slopes=float(coef[1].sum())))
    np.testing.assert_allclose([coef[0].sum(),coef[1].sum()],[1.,0.],atol=1e-12)
    centered = bz-bz.mean(axis=0)
    _, singular, directions = np.linalg.svd(centered,full_matrices=False)
    directions = directions[:3].T
    state_columns = centered@directions
    transform['bz_mean'] = bz.mean(axis=0).tolist()
    for df in [8,12]:
        bt, spec = time_basis(df); rt,ct = check_design(bt)
        if ct*cz>1e10:
            raise ValueError('ABSTAIN_TENSOR_CONDITION: combined time/state design exceeds 1e10')
        common = dict(time_basis=bt.tolist(),basis=spec,penalty=0.,n_days=len(z))
        tc = np.linalg.lstsq(bt,mu,rcond=None)[0]
        models[f'M2-T{df}'] = Model(f'M2-T{df}',tc,dict(**common,rank=rt,edf=rt,condition=ct))
        # Balanced multioutput least squares equals the full time x state
        # tensor design, without materializing 78*N redundant training rows.
        coef = np.linalg.lstsq(bt,np.linalg.lstsq(bz,q,rcond=None)[0].T,rcond=None)[0].T
        models[f'M4-T{df}-Z4'] = Model(f'M4-T{df}-Z4',coef,dict(**common,rank=rt*rz,edf=rt*rz,
            condition=ct*cz,state_rank=rz,state_condition=cz,parameterization='nonredundant_full_tensor; constant in both spans'))
        statecoef = np.linalg.lstsq(state_columns, q.mean(axis=1)-mu.mean(),rcond=None)[0]
        gs = np.r_[np.sqrt(len(z))*np.linalg.svd(bt,compute_uv=False),np.sqrt(78)*singular[:3]]
        models[f'NOINT-T{df}-Z4'] = Model(f'NOINT-T{df}-Z4',np.r_[tc,statecoef],dict(**common,
            rank=rt+3,edf=rt+3,condition=float(max(gs)/min(gs)),state_directions=directions.tolist(),
            parameterization='time main effect + centered rank-three state main effect; no tensor'))
    return models, transform


def profile_losses(q, pred):
    """Daily vector scores; TV is defined only for numerically simplex output."""
    error = q-pred
    valid = (pred.min(axis=1) >= -1e-12) & (abs(pred.sum(axis=1)-1) < 1e-10)
    half_l1 = np.abs(error).sum(axis=1)/2
    return dict(mse=np.mean(error**2,axis=1),mae=np.mean(abs(error),axis=1),half_l1=half_l1,
                tv=np.where(valid,half_l1,np.nan),simplex_valid=valid)


def calendar_hac(x, resid, slots, lag):
    """Bartlett Newey–West score covariance with scheduled-session gaps.

    Missing dates have zero estimating scores, not imputed responses/prices.
    With consecutive slots this equals statsmodels cov_hac(use_correction=True).
    Coverage still needs appropriate moments, weak dependence and selection law.
    """
    x, resid, slots = np.asarray(x), np.asarray(resid), np.asarray(slots,int)
    n,p = x.shape
    if n <= p or len(set(slots)) != n:
        raise ValueError('HAC_INVALID_DAILY_DESIGN')
    scores = np.zeros((int(max(slots)-min(slots)+1),p))
    scores[slots-min(slots)] = x*resid[:,None]
    meat = scores.T@scores
    for ell in range(1,min(lag+1,len(scores))):
        cross = scores[ell:].T@scores[:-ell]
        meat += (1-ell/(lag+1))*(cross+cross.T)
    bread = np.linalg.inv(x.T@x)
    return (bread@meat@bread)*n/(n-p)
