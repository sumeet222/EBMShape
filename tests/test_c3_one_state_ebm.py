"""Small computational guards; synthetic fits give no market power guarantee."""
import json
import pickle
from pathlib import Path
import tempfile
import unittest
import numpy as np
import pandas as pd
from scipy.optimize import check_grad
from interpret.glassbox import ExplainableBoostingRegressor
from ebm_research.experiment_c.c3 import models,m8_softmax
from ebm_research.experiment_c.c3.analysis import shape,support,score
from ebm_research.experiment_c.c3.run import select_configurations
from ebm_research.experiment_c.c2r_diagnostics import block_weights
from ebm_research.experiment_c.c2r_models import profile_losses,calendar_hac
from ebm_research.experiment_c.readiness import WINDOWS,transform_s0


def fixture():
    z=np.linspace(-2,2,60);dates=pd.bdate_range('2016-01-04',periods=60).strftime('%Y-%m-%d').to_numpy()
    base=np.linspace(1,2,78);base/=base.sum();slope=np.linspace(-.001,.001,78)
    return dates,z,np.broadcast_to(base,(60,78)).copy(),base[None,:]+z[:,None]*slope


def setting():
    return dict(numeric_bins=8,kwargs=dict(max_bins=128,max_interaction_bins=96,max_rounds=25,
        max_leaves=3,min_samples_leaf=5,validation_size=0,outer_bags=1,inner_bags=0,
        early_stopping_rounds=0,greedy_ratio=0.,cyclic_progress=True,smoothing_rounds=0,
        interaction_smoothing_rounds=0,learning_rate=.1,n_jobs=1))


class C3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dates,cls.z,cls.null,cls.alternative=fixture();cls.t=models.transform(cls.dates,cls.z,8)
        cls.fits={}
        for name,q in [(models.IDS[1],cls.alternative),(models.IDS[3],cls.alternative),(models.IDS[4],cls.null)]:
            e=ExplainableBoostingRegressor(**models.kwargs(name,cls.t,setting(),42)).fit(models.design(cls.z,name,cls.t),q.ravel())
            cls.fits[name]=dict(name=name,model=e,transform=cls.t)

    def test_native_graph_all78_numeric_nominal_unknown_serialization(self):
        for name,bundle in self.fits.items():
            a=models.audit(bundle['model'],self.z,name,self.t)
            self.assertTrue(all(n==78 for n in a['time_levels']))
            if name in models.IDS[3:]:
                self.assertEqual(bundle['model'].term_scores_[-1].shape[0],80)
            self.assertTrue(a['serialization_parity']);self.assertTrue(a['edge_finite'])
            p=models.predict(bundle,self.z)
            np.testing.assert_allclose(p,models.predict(pickle.loads(pickle.dumps(bundle)),self.z),atol=0,rtol=0)
        self.assertIsInstance(models.design(self.z,models.IDS[3],self.t)[0,1],float)
        self.assertIsInstance(models.design(self.z,models.IDS[4],self.t)[0,1],str)

    def test_day_rows_folds_train_only_future_perturbation(self):
        train=np.arange(40);future=np.arange(40,60);q=self.alternative.copy();t=models.transform(self.dates[train],self.z[train],8)
        q[future]*=100;future_z=self.z.copy();future_z[future]+=1000
        t2=models.transform(self.dates[train],future_z[train],8);self.assertEqual(t,t2)
        x=models.design(self.z,models.IDS[3],self.t)
        for i in range(60):np.testing.assert_array_equal(x[i*78:(i+1)*78,0],models.LABELS)
        self.assertLess(max(self.dates[train]),min(self.dates[future]));self.assertFalse(set(train)&set(future))

    def test_selection_excludes_future_score_perturbations(self):
        rows=[dict(fold=f,model=m,config=c,MSE=v) for f in ['INNER_2018','INNER_2019']
              for m in models.IDS[1:] for c,v in [('A',2.),('B',1.)]]
        first=select_configurations(rows)
        rows += [dict(fold='DEV_2020',model=m,config='B',MSE=1e10) for m in models.IDS[1:]]
        self.assertEqual(select_configurations(rows),first)

    def test_additive_anchored_identity_and_null_computation(self):
        p=models.predict(self.fits[models.IDS[1]],self.z);labels=transform_s0(self.z,self.t['S0']);delta=p[labels==2].mean(axis=0)-p[labels==0].mean(axis=0)
        np.testing.assert_allclose(delta-delta[30],0,atol=1e-13)
        null=models.predict(self.fits[models.IDS[4]],self.z)
        np.testing.assert_allclose(null[0],null[-1],atol=1e-13)
        interaction=models.predict(self.fits[models.IDS[3]],self.z)
        self.assertGreater(np.max(abs((interaction[-1]-interaction[0])-(interaction[-1,30]-interaction[0,30]))),1e-5)

    def test_additive_closure_artifact_and_named_normalization(self):
        p=np.ones((2,78))/78+np.array([0,.001])[:,None]
        self.assertAlmostEqual(p[1].sum()-1,.078)
        q=models.normalized(p);np.testing.assert_allclose(q.sum(axis=1),1,atol=1e-15)
        np.testing.assert_allclose(models.normalized(-np.ones((1,78))),np.ones((1,78))/78)
        loss=profile_losses(self.null[:2],p);self.assertFalse(loss['simplex_valid'][1]);self.assertTrue(np.isnan(loss['tv'][1]))
        before=p.copy();profile_losses(self.null[:2],p);np.testing.assert_array_equal(before,p)

    def test_m8_gradient_positive_closure_centered_solver(self):
        rng=np.random.default_rng(8);theta=rng.normal(0,.05,156);x=self.z[:9];q=self.alternative[:9]
        error=check_grad(lambda v:m8_softmax.objective(v,x,q,.001)[0],lambda v:m8_softmax.objective(v,x,q,.001)[1],theta)
        self.assertLess(error,2e-6)
        fit=m8_softmax.fit(self.z,self.alternative);p=m8_softmax.predict(fit,np.array([-50.,0.,50.]))
        self.assertTrue(fit['success']);self.assertLess(fit['gradient_max'],2e-6)
        self.assertTrue((p>0).all());np.testing.assert_allclose(p.sum(axis=1),1,atol=1e-14)
        np.testing.assert_allclose(np.array(fit['ab']).sum(axis=1),0,atol=1e-13)

    def test_independent_score_window_arithmetic(self):
        rng=np.random.default_rng(41);p=self.alternative+rng.normal(0,.0001,self.alternative.shape)
        r,dd,ww=score(self.alternative,p,self.dates,self.z,np.repeat([0,1,2],20),np.arange(60),'FIXTURE','TEST')
        manual=np.array([sum((a-b)**2 for a,b in zip(qa,pa))/78 for qa,pa in zip(self.alternative,p)])
        np.testing.assert_allclose(manual,dd.MSE_profile,atol=1e-18);self.assertAlmostEqual(manual.mean(),r['MSE_profile'])
        close=(self.alternative[:,66:78].sum(axis=1)-p[:,66:78].sum(axis=1))**2
        np.testing.assert_allclose(close,dd.CLOSE_C_MSE,atol=1e-18)
        self.assertEqual(WINDOWS['CLOSE_C'],[66,78]);self.assertEqual(WINDOWS['MID_C'],[24,48])
        self.assertEqual(9*60+30+54*5,14*60);self.assertEqual(9*60+30+77*5,15*60+55)

    def test_H1_D_last_bin_support(self):
        labels=np.repeat([0,1,2],20);p=self.null.copy();p[labels==2,0]-=.005;p[labels==2,77]+=.005
        sh,delta=shape(p,labels,np.arange(60));self.assertAlmostEqual(sh['H1']*100,.5)
        self.assertAlmostEqual(sh['last_bin']+sh['other_close_bins'],sh['H1']);self.assertAlmostEqual(sh['H3_TV'],.005)
        self.assertFalse(sh['basic_ok']);self.assertEqual(sh['status'],'ABSTAIN_SUPPORT')
        self.assertFalse(support(np.ones(60,bool),np.zeros(60,int))['basic_ok'])
        self.assertAlmostEqual(np.max(abs(delta-delta[30])),.005)

    def test_scheduled_blocks_joint_reproducibility_HAC(self):
        slots=np.array([0,1,4,5,9,10,12]);a=block_weights(slots,5,20,42);b=block_weights(slots,5,20,42)
        np.testing.assert_array_equal(a,b);self.assertEqual(a.shape,(20,7))
        values=np.arange(7.);np.testing.assert_allclose(a@values-a@values,0)
        e=values-values.mean();v=calendar_hac(np.ones((7,1)),e,slots,5)
        self.assertTrue(np.isfinite(v).all());self.assertGreater(v[0,0],0)

    def test_smoke_small_output_and_config_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'result.json';path.write_text(json.dumps(self.t));self.assertEqual(json.loads(path.read_text()),self.t)
        self.assertEqual(len(self.t['cuts']),7);self.assertLessEqual(self.t['last'],'2016-03-31')

if __name__=='__main__':unittest.main()
