"""Deterministic statistical and chronological C2R checks, no real data reads."""
import tempfile
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac

from ebm_research.experiment_c.c2r_models import (
    time_basis,natural_basis,fit_models,calendar_hac,check_design,
    scalar_design,profile_losses,date_hash)
from ebm_research.experiment_c.c2r_diagnostics import influence_arrays,block_weights
from ebm_research.experiment_c.readiness import transform_s0
from ebm_research.experiment_c.c2r_completion import calibration_rows, chronological_periods


def fixture(n=90):
    dates=pd.bdate_range('2017-01-02',periods=n).strftime('%Y-%m-%d').to_numpy()
    z=np.linspace(-2,2,n)+.1*np.sin(np.arange(n))
    mu=np.linspace(1,2,78);mu/=mu.sum()
    beta=np.linspace(-.001,.001,78)
    q=mu[None,:]+z[:,None]*beta[None,:]
    return dates,z,q,np.arange(n)


class C2RTests(unittest.TestCase):
    def test_numeric_block_keys_are_chronological(self):
        frame=pd.DataFrame({'period':['1','10','2'],'residual_mean_pp':[.1,.3,.2]})
        ordered=chronological_periods(frame)
        self.assertEqual(ordered.period_index.tolist(),[1,2,10])
        self.assertEqual(ordered.residual_mean_pp.tolist(),[.1,.2,.3])

    def test_calibration_constant_fit_marks_empty_bins(self):
        rows=calibration_rows(np.ones(10),np.arange(10)/100,'SYNTHETIC','OLS-L0')
        self.assertEqual(sum(r['n_days'] for r in rows),10)
        self.assertEqual(sum(r['n_days']==0 for r in rows),4)
        for row in rows:
            if row['n_days']==0:
                self.assertTrue(np.isnan(row['observed_mean_pp']))
                self.assertIn('ABSTAIN',row['status'])

    def test_basis_partition_endpoints_and_linear_extrapolation(self):
        for df in [8,12]:
            bt,spec=time_basis(df)
            self.assertEqual(bt.shape,(78,df))
            np.testing.assert_allclose(bt.sum(axis=1),1,atol=1e-14)
            self.assertAlmostEqual(bt[0,0],1,places=14);self.assertAlmostEqual(bt[-1,-1],1,places=14)
        knots=np.array([-2,-.4,.7,2.])
        b=natural_basis(np.array([-4,-3,-2,2,3,4]),knots)
        np.testing.assert_allclose(b.sum(axis=1),1,atol=1e-14)
        np.testing.assert_allclose(b[0]-b[1],b[1]-b[2],atol=1e-14)
        np.testing.assert_allclose(b[5]-b[4],b[4]-b[3],atol=1e-14)

    def test_multivariate_OLS_coefficients_and_closure(self):
        dates,z,q,slots=fixture();models,t=fit_models(dates,z,q,slots)
        pred=models['P-OLS-Z'].predict(z,t)
        np.testing.assert_allclose(pred,q,atol=1e-13)
        self.assertAlmostEqual(models['P-OLS-Z'].coef[0].sum(),1)
        self.assertAlmostEqual(models['P-OLS-Z'].coef[1].sum(),0)
        np.testing.assert_allclose(models['M0'].predict(z,t),np.broadcast_to(q.mean(axis=0),q.shape))
        self.assertFalse(any(models['M1'].metadata['supported_groups']))
        np.testing.assert_allclose(models['M1'].predict(z,t),models['M0'].predict(z,t))
        self.assertEqual(models['OLS-L3'].training_fit.nobs,len(z))

    def test_tensor_fit_matches_explicit_small_design(self):
        dates,z,q,slots=fixture(24);models,t=fit_models(dates,z,q,slots)
        bt=np.asarray(models['M4-T8-Z4'].metadata['time_basis'])
        bz=natural_basis((z-t['mean'])/t['sd'],t['state_knots_standardized'])
        design=np.array([np.kron(bz[i],bt[k]) for i in range(len(z)) for k in range(78)])
        reference=np.linalg.lstsq(design,q.ravel(),rcond=None)[0].reshape(4,8)
        np.testing.assert_allclose(models['M4-T8-Z4'].coef,reference,atol=1e-12)
        np.testing.assert_allclose(models['M4-T8-Z4'].predict(z,t).sum(axis=1),1,atol=1e-12)

    def test_hac_against_statsmodels_and_calendar_gaps(self):
        x=np.c_[np.ones(24),np.arange(24)/10]
        y=1+2*x[:,1]+.1*np.sin(np.arange(24))
        fit=sm.OLS(y,x).fit()
        for lag in [5,10,20]:
            np.testing.assert_allclose(calendar_hac(x,fit.resid,np.arange(24),lag),cov_hac(fit,nlags=lag,use_correction=True),atol=1e-12,rtol=1e-10)
        gap=calendar_hac(x,fit.resid,np.arange(24)*3,5)
        self.assertGreater(np.max(abs(gap-cov_hac(fit,nlags=5))),1e-10)

    def test_analytic_influence_against_trusted_deletions(self):
        x=np.c_[np.ones(14),np.arange(14)/10]
        fit=sm.OLS(1+x[:,1]+.07*np.cos(np.arange(14)),x).fit()
        actual=influence_arrays(fit);ref=fit.get_influence()
        for name,expected in [('hat',ref.hat_matrix_diag),('cooks',ref.cooks_distance[0]),
            ('student_internal',ref.resid_studentized_internal),('student_external',ref.resid_studentized_external),
            ('dffits',ref.dffits[0]),('dfbetas',ref.dfbetas)]:
            np.testing.assert_allclose(actual[name],expected,atol=1e-10,rtol=1e-10)

    def test_training_transform_unaffected_by_targets_and_future_extremes(self):
        dates,z,q,slots=fixture();m,t=fit_models(dates,z,q,slots)
        changed=q[:,::-1].copy();_,other=fit_models(dates,z,changed,slots)
        self.assertEqual(t,other)
        self.assertGreater(abs(q[:,66:78].sum()-changed[:,66:78].sum()),1e-5)
        before=t['S0']['cuts'].copy()
        labels=transform_s0([-100.,*before,100.],t['S0'])
        np.testing.assert_array_equal(labels,[0,1,2,2])
        self.assertEqual(t['S0']['cuts'],before)
        self.assertEqual(m['M4-T8-Z4'].predict(np.array([-100.,100.]),t).shape,(2,78))

    def test_rank_failure_and_invalid_TV(self):
        with self.assertRaisesRegex(ValueError,'ABSTAIN_DESIGN'):
            check_design(np.ones((8,2)))
        q=np.ones((2,78))/78;pred=q.copy();pred[1,0]=-.1
        losses=profile_losses(q,pred)
        self.assertAlmostEqual(losses['mse'][0],0)
        self.assertFalse(losses['simplex_valid'][1]);self.assertTrue(np.isnan(losses['tv'][1]))
        self.assertTrue(np.isfinite(losses['half_l1'][1]))

    def test_joint_date_block_weights_and_temporary_predictions(self):
        a=block_weights(np.array([0,1,4,5,6,8]),5,10,42)
        np.testing.assert_array_equal(a,block_weights(np.array([0,1,4,5,6,8]),5,10,42))
        self.assertEqual(a.shape,(10,6))
        q=np.tile(np.arange(1,79),(6,1)).astype(float);q/=q.sum(axis=1)[:,None]
        np.testing.assert_allclose(a@q/a.sum(axis=1)[:,None],np.broadcast_to(q[0],(10,78)))
        with tempfile.TemporaryDirectory(prefix='c2r_smoke_') as directory:
            p=Path(directory)/'predictions.npz';np.savez_compressed(p,pred=q)
            with np.load(p) as f:np.testing.assert_array_equal(f['pred'],q)
        self.assertEqual(date_hash(['2019-01-02']),date_hash(['2019-01-02']))


if __name__=='__main__':unittest.main()
