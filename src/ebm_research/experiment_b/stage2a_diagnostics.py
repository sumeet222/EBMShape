"""Tailored full-fit diagnostics for the Stage2A fixed regression designs."""
import numpy as np
import pandas as pd
import warnings
from scipy.stats import spearmanr
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.sm_exceptions import SingularMatrixWarning

from .linear_diagnostics import residual_records, ranked_influence
from .state_models import fit_model,slope_vector,evaluate_linear


def full_diagnostics(frame,fit,fit_id,stage1,protocol,refit=None):
    """Reuse the tested Stage1.5 residual battery, tailoring df and spline interpretation."""
    spec=fit['spec'];model=spec['model_id'];d=fit['design'];r=fit['result'];u=r.resid
    settings=dict(acf_lags=[1,5,10,20],ljung_box_lags=[5,10,20],ljung_box_model_df=0,
                  arch_lags=5,reset_models=[model] if not spec['family'].startswith('S') else [],
                  reset_power=2,residual_bins=10,sufficient_bin_count=20,
                  quantiles=[0,.001,.01,.05,.5,.95,.99,.999,1])
    # Candidate rank is checked before fitting. Only redundant auxiliary White
    # products trigger this library warning; its p-value is withheld below.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',SingularMatrixWarning)
        rows=residual_records(frame,model,r,d,stage1,settings)
    # White auxiliary products are algebraically redundant for interaction/spline
    # designs. Statsmodels uses their effective rank; report that actual df.
    a=d.to_numpy();i,j=np.triu_indices(a.shape[1])
    products=a[:,i]*a[:,j]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',SingularMatrixWarning)
        white=OLS(np.square(u),products).fit()
    for row in rows:
        row.update(fit_id=fit_id,model_id=model,info=spec['info'],variant='FULL')
        if row['statistic']=='White_LM':
            row['df']=int(white.df_model)
            row['assumption']='IID chi-square diagnostic on all design squares/products, SVD effective rank-1; algebraic redundancy retained only in auxiliary variance model'
            if np.linalg.matrix_rank(products)<products.shape[1]:
                row.update(status='NOT_APPLICABLE',estimate=None,p_value=None,
                           note='Auxiliary White squares/products algebraically rank-deficient; candidate design itself full rank. Do not report a singular auxiliary-test p-value.')
    def add(name,value,**extra):
        rows.append(dict(fit_id=fit_id,model_id=model,info=spec['info'],variant='FULL',n=len(frame),
                         first=str(frame.session_et.iloc[0]),last=str(frame.session_et.iloc[-1]),
                         statistic=name,estimate=float(value),status='DESCRIPTIVE_ONLY',**extra))
    add('adjusted_R_squared',r.rsquared_adj);add('residual_SD_bp',np.std(u,ddof=len(d.columns)))
    add('effective_design_rank',fit['rank']);add('condition_number_actual_design',fit['condition'])
    if spec['family'].startswith('S'):
        rows.append(dict(fit_id=fit_id,model_id=model,statistic='RESET',status='NOT_APPLICABLE',
                         note='Rich state spline: nested f/g curvature HAC Wald is the predeclared lack-of-fit comparison'))
        rows.append(dict(fit_id=fit_id,model_id=model,statistic='individual_spline_VIF',status='DESCRIPTIVE_ONLY',
                         note='Individual basis-column VIF is parameterization dependent; full rank/condition and basis correlations reported instead'))
        grid=np.linspace(frame.rv_open_log.min(),frame.rv_open_log.max(),200)
        curve=np.array([float(slope_vector(fit,z)@r.params) for z in grid])
        differences=np.diff(curve);sign=np.sign(differences[np.abs(differences)>1e-10])
        add('slope_curve_turns',np.sum(sign[1:]!=sign[:-1]),note='200 fixed points across observed training Z; fitted-projection wiggles, not raw derivatives')
        add('max_abs_fitted_X_slope_over_train_Z',np.max(np.abs(curve)),note='Fixed-basis projection only, including scientific support-masked high-state region')
    else:
        for term in ['X','Zc','W']:
            if term in d:
                add('VIF_named_predictor',variance_inflation_factor(a,d.columns.get_loc(term)),term=term)
    correlation=d.drop(columns='intercept').corr().to_numpy(copy=True)
    if correlation.size:
        np.fill_diagonal(correlation,0);add('max_abs_design_correlation',np.max(np.abs(correlation)))
    for label,values in [('Z',frame.rv_open_log)]:
        bins=pd.qcut(values,10,duplicates='drop')
        t=pd.DataFrame(dict(bin=bins,value=values,residual=u))
        for b,(_,part) in enumerate(t.groupby('bin',observed=True)):
            add('binned_residual_mean',part.residual.mean(),term=label,bin=b,bin_n=len(part),bin_predictor_mean=part.value.mean(),sufficient_support=len(part)>=20)
    group=np.searchsorted(protocol['preprocessing']['cutoffs_raw'],frame.rv_open_raw,side='left')
    for g,state in enumerate(['low','middle','high']):
        values=u[group==g];add('residual_mean_by_state',np.mean(values),state=state,group_n=len(values))
        add('residual_SD_by_state',np.std(values,ddof=1),state=state,group_n=len(values))
    dates=frame.session_et.astype(str)
    for period,bounds in protocol['diagnostics']['temporal_periods'].items():
        values=u[dates.between(*bounds)];add('residual_mean_by_period',np.mean(values),period=period,group_n=len(values))
        add('residual_SD_by_period',np.std(values,ddof=1),period=period,group_n=len(values))
    top=ranked_influence(frame,r,stage1).head(5)
    zlow,_,zhigh=protocol['support']['z_representatives']
    base_vector=slope_vector(fit,zhigh)-slope_vector(fit,zlow)
    baseline=float(base_vector@r.params)
    for rank,(_,entry) in enumerate(top.iterrows(),1):
        mask=~frame.session_et.eq(entry.session_et)
        # A small exact refit, fixed basis: this is influence on the fitted
        # projection, not a raw conditional-mean claim or a new deletion rule.
        subset=(refit(frame.loc[mask],spec,f'INFLUENCE_{entry.session_et}')
                if refit else fit_model(frame.loc[mask],spec,fit['pre'],'2022-01-01'))
        delta=float(base_vector@subset['result'].params)-baseline
        add('Cook_top5_influence',entry.cooks_distance,date=str(entry.session_et),influence_rank=rank,
            leverage=float(entry.leverage),studentized_internal=float(entry.studentized_internal),
            high_low_slope_single_delete_delta=delta,
            assumption='Fixed design/basis projection contrast; knots not re-estimated; no selected deletion in primary')
    add('max_leverage',r.get_influence().hat_matrix_diag.max())
    return rows


def prediction_diagnostics(frame,predictions,model_id,mode):
    """Coarse supported calibration, state/error magnitude checks on validation only."""
    error=frame.y_last30_bp.to_numpy()-predictions
    rows=[]
    bins=pd.qcut(predictions,10,duplicates='drop')
    t=pd.DataFrame(dict(bin=bins,actual=frame.y_last30_bp,forecast=predictions,error=error))
    for j,(_,part) in enumerate(t.groupby('bin',observed=True)):
        rows.append(dict(model_id=model_id,mode=mode,statistic='validation_prediction_decile',bin=j,
                         n=len(part),estimate=part.error.mean(),actual_mean=part.actual.mean(),forecast_mean=part.forecast.mean(),
                         status='DESCRIPTIVE_ONLY' if len(part)>=20 else 'ABSTAIN',null='calibration descriptive, not causal'))
    rows.append(dict(model_id=model_id,mode=mode,statistic='validation_abs_error_vs_abs_forecast_spearman',
                     n=len(frame),estimate=float(spearmanr(np.abs(error),np.abs(predictions)).statistic),
                     status='DESCRIPTIVE_ONLY'))
    return rows
