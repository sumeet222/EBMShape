"""Four small tests of frozen spline, information, contrast and pairing logic."""
import datetime as dt
import unittest

import numpy as np
import pandas as pd

from ebm_research.experiment_b.state_models import (specifications,fit_preprocessing,design,
    curvature,fit_model,guard_history,covariance,evaluate_linear,slope_vector)


class StateModelTests(unittest.TestCase):
    def fixture(self):
        i=np.arange(100);z=np.linspace(-7.6,-4.9,100);x=np.sin(i*1.7)*30+i*.03
        return pd.DataFrame(dict(session_et=pd.bdate_range('2016-01-05',periods=100).date,
                                eligible_primary=True,x_open_bp=x,w_preclose_bp=np.cos(i*.73)*10,
                                rv_open_log=z,rv_open_raw=np.exp(z)-1e-8,
                                y_last30_bp=1+.2*x+.4*(z+6)+.1*x*(z+6)+np.cos(i*.31)))

    def test_training_guard_and_linear_tails(self):
        f=self.fixture();p=fit_preprocessing(f,'2022-01-01')
        with self.assertRaisesRegex(ValueError,'Forbidden'):
            fit_preprocessing(pd.DataFrame({'session_et':[dt.date(2022,1,3)]}),'2022-01-01')
        for dim in [4,6]:
            a,b=p['splines'][str(dim)]['boundaries']
            for z in [a-1,b+1]:
                h=curvature([z-.1,z,z+.1],p,dim)
                np.testing.assert_allclose(h[0]-2*h[1]+h[2],0,atol=2e-10)
        # Transforming future/outside points does not alter fitted knots/scales.
        import json
        frozen=json.dumps(p,sort_keys=True);curvature([100,-100],p,4)
        self.assertEqual(frozen,json.dumps(p,sort_keys=True))

    def test_categorical_formula_equality_and_E_excludes_W(self):
        f=self.fixture();p=fit_preprocessing(f,'2022-01-01')
        spec=next(s for s in specifications() if s['model_id']=='C1_E')
        probe=pd.DataFrame(dict(x_open_bp=[10.,10.,10.],
                                rv_open_raw=[p['cutoffs_raw'][0],np.mean(p['cutoffs_raw']),p['cutoffs_raw'][1]+.01],
                                rv_open_log=[-7.,-6.,-5.]))
        d=design(probe,spec,p)
        self.assertEqual(d.DM.tolist(),[0.,1.,0.]);self.assertEqual(d.DH.tolist(),[0.,0.,1.])
        beta=pd.Series({'intercept':1,'X':.2,'DM':2,'X_DM':.3,'DH':3,'X_DH':.4})
        np.testing.assert_allclose(d@beta.reindex(d.columns),[3,8,10])
        self.assertNotIn('W',d.columns)

    def test_spline_nests_C2_and_delta_variance(self):
        f=self.fixture();p=fit_preprocessing(f,'2022-01-01')
        c2=next(s for s in specifications() if s['model_id']=='C2_E')
        base=design(f,c2,p)
        for dim in [4,6]:
            spec=next(s for s in specifications() if s['model_id']==f'S{dim}_E')
            mat=design(f,spec,p)
            np.testing.assert_array_equal(mat[base.columns],base)
            self.assertEqual(np.linalg.matrix_rank(mat),2*dim)
        fit=fit_model(f,c2,p,'2022-01-01')
        v=slope_vector(fit,p['representatives'][2])-slope_vector(fit,p['representatives'][0])
        check=evaluate_linear(fit,v);r=covariance(fit,5)
        self.assertAlmostEqual(check['se']**2,float(v@r.cov_params()@v),places=13)
        np.testing.assert_allclose([check['ci_low'],check['ci_high']],r.t_test(v).conf_int()[0],rtol=1e-10)

    def test_timeline_and_paired_date_matching(self):
        from ebm_research.experiment_b.stage2a import paired_arrays
        f=self.fixture()
        guard_history(f,'2022-01-01')
        with self.assertRaisesRegex(ValueError,'Forbidden'):guard_history(f,'2024-04-01')
        a=pd.DataFrame({'session_et':['2022-01-03','2022-01-04'],'loss':[1.,4.]})
        b=pd.DataFrame({'session_et':['2022-01-04','2022-01-03'],'loss':[2.,3.]})
        np.testing.assert_array_equal(paired_arrays(a,b),[2.,-2.])
        with self.assertRaisesRegex(ValueError,'matched'):paired_arrays(a,b.iloc[:1])


if __name__=='__main__':
    unittest.main()
