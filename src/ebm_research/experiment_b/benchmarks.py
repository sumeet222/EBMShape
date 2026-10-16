"""Training-only source-style OLS and descriptive RV moderation diagnostics."""
import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLS

from .daily import guard_training


def fit_table(frame, design, config, label, model):
    """OLS ordinary SE plus Bartlett HAC normal inference at frozen lag choices.

    Design must have an explicit intercept. Lags count eligible daily rows;
    finite-sample covariance correction is n/(n-k), with asymptotic normal CIs.
    """
    guard_training(frame, config)
    if not np.isfinite(design.to_numpy()).all() or not np.isfinite(frame.y_last30_bp).all():
        raise ValueError(f"Nonfinite regression input: {label}/{model}")
    if np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError(f"Rank deficient design: {label}/{model}")
    result = OLS(frame.y_last30_bp.to_numpy(), design.to_numpy(), hasconst=True).fit()
    rows = []
    for lag in config["hac_lags"]:
        robust = result.get_robustcov_results(cov_type="HAC", maxlags=lag, kernel="bartlett", use_correction=config["hac_use_correction"], use_t=config["hac_use_t"])
        ci = robust.conf_int(alpha=.05)
        for j, term in enumerate(design.columns):
            rows.append(dict(cohort=label, model=model, term=term, n=len(frame), first=str(frame.session_et.iloc[0]), last=str(frame.session_et.iloc[-1]),
                             coefficient=float(result.params[j]), ordinary_se=float(result.bse[j]), r_squared=float(result.rsquared),
                             hac_lag=lag, hac_se=float(robust.bse[j]), ci_low=float(ci[j,0]), ci_high=float(ci[j,1]), p_value=float(robust.pvalues[j])))
    return rows


def trio(frame, config, label):
    """Required regression trio, with explicit E versus L design names."""
    guard_training(frame, config)
    rows=[]
    for name, cols in [("OLS1_E",["x_open_bp"]),("OLS2_L",["w_preclose_bp"]),("OLS3_L",["x_open_bp","w_preclose_bp"])]:
        design=pd.DataFrame({"intercept":np.ones(len(frame))},index=frame.index)
        for col in cols:
            design[col]=frame[col]
        rows.extend(fit_table(frame,design,config,label,name))
    return rows


def volatility_tables(frame, config, label, cutoffs=None):
    """Retrospective group slopes and saturated pooled high-minus-low slope.

    Separate-group HAC counts successive observations within that group. Pooled
    interactions use the complete cohort chronology, preserving cross-group
    residual dependence. All intervals condition on estimated group boundaries.
    """
    guard_training(frame, config)
    cuts=np.quantile(frame.rv_open_raw,[1/3,2/3],method="linear") if cutoffs is None else np.array(cutoffs)
    if not np.isfinite(cuts).all() or cuts[0]>=cuts[1]:
        raise ValueError("Training RV tercile boundaries are invalid/non-distinct")
    group=np.searchsorted(cuts,frame.rv_open_raw.to_numpy(),side="left")
    rows=[]
    counts={}
    for j,name in enumerate(["low","middle","high"]):
        sub=frame.loc[group==j]
        counts[name]=len(sub)
        design=pd.DataFrame({"intercept":1.,"x_open_bp":sub.x_open_bp},index=sub.index)
        rows.extend(fit_table(sub,design,config,label,"RV_"+name))
    design=pd.DataFrame({"intercept":np.ones(len(frame)),"middle_intercept":(group==1).astype(float),"high_intercept":(group==2).astype(float),
                         "low_slope":frame.x_open_bp.to_numpy(),"middle_minus_low_slope":frame.x_open_bp.to_numpy()*(group==1),
                         "high_minus_low_slope":frame.x_open_bp.to_numpy()*(group==2)},index=frame.index)
    rows.extend(fit_table(frame,design,config,label,"RV_pooled_interaction"))
    meta=dict(cohort=label,n=len(frame),first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),
              rv_raw_cutoffs=cuts.tolist(),rv_log_cutoffs=np.log(cuts+config["rv_epsilon"]).tolist(),counts=counts,
              units="RV: dimensionless sqrt(sum log minute return squared); Z: natural log(RV+1e-8)",
              convention="linear empirical quantiles; boundary equality assigned lower group; pooled full-cohort HAC contrast conditional on cutoffs")
    return rows,meta
