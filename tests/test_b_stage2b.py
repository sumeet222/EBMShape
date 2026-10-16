"""Four targeted Stage2B checks: native graph, total contrasts, support and timing/losses."""
import datetime as dt
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingRegressor

from ebm_research.experiment_b.ebm_models import (specifications,features,assert_graph,contrast,
    query_frame,support_screen,candidate_rows,paired_losses,paired_hac,block_interval)
from ebm_research.experiment_b.stage2b import read_development
from ebm_research.experiment_b.state_models import guard_history


class Stage2BTests(unittest.TestCase):
    def setUp(self):
        self.p=dict(cutoffs_raw=[.002,.004],z_representatives=np.log([.001,.003,.006]).tolist())
        self.f=pd.DataFrame(dict(session_et=[dt.date(2020,1,1)+dt.timedelta(days=i) for i in range(120)],
            x_open_bp=np.tile([-10.,10.,-10.,10.],30),w_preclose_bp=np.zeros(120),
            rv_open_raw=np.tile([.001,.001,.006,.006],30)))
        self.f['rv_open_log']=np.log(self.f.rv_open_raw+1e-8)

    def test_information_read_and_history_guards(self):
        with self.assertRaises(ValueError):read_development(Path('never-read.parquet'),'2024-01-01','2024-01-02')
        with self.assertRaises(ValueError):guard_history(self.f,'2020-01-10')
        for s in specifications():
            if s['info']=='E':self.assertNotIn('W',features(self.f.drop(columns='w_preclose_bp'),s,self.p))

    def test_native_graph_nominal_and_whole_response(self):
        grid={i:dict(display_candidate=dict(a=10.,w=0.),chosen=True,status='SUPPORTED_BAND_DESIGN') for i in ['E','L']}
        y=self.f.x_open_bp.to_numpy()*(self.f.rv_open_raw.to_numpy()>.004)+np.arange(120)%3
        for s in specifications():
            names=s['features'];model=ExplainableBoostingRegressor(feature_names=names,
                feature_types=['nominal' if n=='S' else 'continuous' for n in names],
                interactions=[tuple(names.index(n) for n in e) for e in s['edges']] or 0,
                max_rounds=10,outer_bags=2,validation_size=.15,min_samples_leaf=2,
                smoothing_rounds=0,interaction_smoothing_rounds=0,n_jobs=1,random_state=42)
            model.fit(features(self.f,s,self.p),y);assert_graph(model,s)
            d=contrast(model,s,self.p,grid)['D_F']
            lo,_,hi=self.p['z_representatives'];q=query_frame([-10,10,-10,10],[lo,lo,hi,hi],0)
            v=model.predict(features(q,s,self.p));self.assertAlmostEqual(d,v[3]-v[2]-v[1]+v[0])
            if not s['edges']:self.assertLess(abs(d),1e-9)

    def test_exact_local_support_and_block_abstention(self):
        # 30 per cell fails minimum 50 even though all queried coordinates exist.
        grid,rows=support_screen(self.f,self.p)
        self.assertEqual(grid['E']['status'],'ABSTAIN')
        f=pd.concat([self.f,self.f],ignore_index=True)
        grid,rows=support_screen(f,self.p)
        self.assertEqual(grid['E']['chosen']['a'],10)
        self.assertEqual(grid['E']['chosen']['h'],5)
        r=candidate_rows(f,self.p,grid['E']['chosen'],'train')
        self.assertTrue(all(x['n']==60 and x['blocks']>=20 for x in r))
        near=f.copy();near['x_open_bp']=0.
        self.assertEqual(support_screen(near,self.p)[0]['E']['status'],'ABSTAIN')

    def test_paired_keys_and_independent_hac_variance(self):
        c=pd.DataFrame(dict(session_et=['2022-01-03','2022-01-04'],actual=[2.,-1.],forecast=[1.,0.]))
        b=c.assign(forecast=[0.,0.]).iloc[::-1]
        np.testing.assert_array_equal(paired_losses(c,b),[3.,0.])
        with self.assertRaises(ValueError):paired_losses(c,b.iloc[:1])
        d=np.array([1.,4.,2.,-3.,2.,0.,1.,2.]);n=len(d);v=d-d.mean();lag=2
        meat=np.sum(v*v)+sum(2*(1-k/(lag+1))*np.dot(v[k:],v[:-k]) for k in range(1,lag+1))
        self.assertAlmostEqual(paired_hac(d,lag)['se'],np.sqrt(meat/n**2*n/(n-1)),places=12)
        self.assertEqual(block_interval(d,2,50,42),block_interval(d,2,50,42))
        # Regression: two screened settings legitimately predict the same dates.
        from ebm_research.experiment_b.stage2b_results import make_predictions
        f=self.f.assign(y_last30_bp=1.,rv_group_stage2b=0)
        runs={}
        for setting in [0,1]:
            meta=dict(fit_id=f'screen{setting}',model_id='SB_E',family='SB',info='E',seed=42,
                      setting=setting,variant='FULL',mode='screen',asof='2021-01-01',last='2020-12-31')
            runs[str(setting)]=dict(meta=meta,eval_dates=[str(f.session_et.iloc[0])],predictions=[0.])
        result=make_predictions(dict(runs=runs),f,f.iloc[:0])
        self.assertEqual(len(result),2);self.assertEqual(result.setting.nunique(),2)


if __name__=='__main__':unittest.main()
