"""Four small checks of Stage 1 scientific timing and inference invariants."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLS

from ebm_research.experiment_b.daily import at, build_daily, opening_rv, guard_training
from ebm_research.experiment_b.benchmarks import fit_table
from ebm_research.experiment_b.pilot import ROOT, calendar, prior_full


class Stage1Tests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'config/B_stage1_dataset_selection.json').read_text())

    def fixture(self):
        c={**self.config,'start':'2016-01-04','end':'2016-01-05'}
        rows=[]
        for day in ['2016-01-04','2016-01-05']:
            times=list(pd.date_range(at(day,'09:30'),periods=30,freq='min'))+[at(day,'14:59')]+list(pd.date_range(at(day,'15:00'),periods=60,freq='min'))
            for i,t in enumerate(times):
                close=100. if day.endswith('04') else 102.+i*.01
                rows.append(dict(symbol='SPY',timestamp_utc=t,session_et=dt.date.fromisoformat(day),open=101. if day.endswith('05') and i==0 else close,high=max(103.,close),low=99.,close=close,volume=10.,trade_count=2.,is_repaired=False))
        qa=pd.DataFrame([dict(session_et=d,daily_trade_count_available=True,daily_ge500=True,daily_count_basis='fixture') for d in ['2016-01-04','2016-01-05']])
        return c,pd.DataFrame(rows),qa

    def test_prices_rv_and_parquet_smoke(self):
        c,m,q=self.fixture(); f=build_daily(m,c,q); d=f.iloc[1]
        self.assertTrue(d.eligible_primary)
        self.assertAlmostEqual(d.r1,102.29/100.-1)
        self.assertAlmostEqual(d.r13,102.90/102.60-1)
        self.assertNotAlmostEqual(d.r1,d.r_open_intraday_only)
        closes=np.array([102.+i*.01 for i in range(30)])
        expected=np.linalg.norm(np.diff(np.log(np.r_[101.,closes])))
        self.assertAlmostEqual(d.rv_open_raw,expected,places=14)
        self.assertEqual(d.early_features_available_at,at('2016-01-05','10:00'))
        self.assertEqual(d.target_available_at,at('2016-01-05','16:00'))
        with tempfile.TemporaryDirectory(prefix='ebm_stage1_smoke_') as tmp:
            p=Path(tmp)/'daily.parquet'; f.to_parquet(p,index=False)
            self.assertEqual(len(pd.read_parquet(p)),2)

    def test_missing_opening_and_prior_not_filled(self):
        c,m,q=self.fixture()
        m=m.loc[~m.timestamp_utc.isin([at('2016-01-04','15:59'),at('2016-01-05','09:44')])]
        d=build_daily(m,c,q).iloc[1]
        self.assertFalse(d.eligible_primary)
        self.assertIn('MISSING_PRIOR_FULL_ANCHOR',d.eligibility_reason)
        self.assertIn('INCOMPLETE_OPENING_30',d.eligibility_reason)
        self.assertTrue(np.isnan(d.rv_open_raw)); self.assertTrue(np.isnan(d.r1))
        bars=[dict(open=100.,high=101.,low=99.,close=100.)]*30
        self.assertEqual(opening_rv(bars),0.)
        self.assertTrue(np.isnan(opening_rv(bars[:-1])))
        bars[0]={**bars[0],'low':102.}
        self.assertTrue(np.isnan(opening_rv(bars)))

    def test_calendar_dst_halfday_and_sealed_guard(self):
        self.assertEqual(at('2024-03-08','09:59').hour,14)
        self.assertEqual(at('2024-03-11','09:59').hour,13)
        cal=calendar('2024-11-27','2024-12-02')
        self.assertEqual(prior_full(cal,'2024-12-02'),'2024-11-27')
        self.assertFalse(cal.is_session('2024-11-28'))
        self.assertEqual(len(cal.session_minutes('2024-11-29')),210)
        for day in ['2022-01-03','2024-01-02']:
            with self.assertRaisesRegex(ValueError,'training dates only'):
                guard_training(pd.DataFrame({'session_et':[dt.date.fromisoformat(day)]}),self.config)

    def test_ols_and_hac_against_tiny_direct_calculation(self):
        x=np.linspace(-2,2,12); X=np.c_[np.ones(12),x]
        y=1.2+.3*x+np.array([.2,-.1,.3,0.,-.2,.1,-.3,.2,.1,-.1,.2,-.2])
        beta=np.linalg.lstsq(X,y,rcond=None)[0]; u=y-X@beta; scores=X*u[:,None]
        meat=scores.T@scores
        for lag in range(1,6):
            cross=scores[lag:].T@scores[:-lag]
            meat+=(1-lag/6)*(cross+cross.T)
        bread=np.linalg.inv(X.T@X); cov=bread@meat@bread*12/(12-2)
        f=pd.DataFrame({'session_et':[dt.date(2016,1,5)+dt.timedelta(days=i) for i in range(12)],'y_last30_bp':y})
        design=pd.DataFrame(X,columns=['intercept','x'])
        rows=fit_table(f,design,self.config,'fixture','OLS')
        got=[r for r in rows if r['hac_lag']==5]
        np.testing.assert_allclose([r['coefficient'] for r in got],beta,atol=1e-14)
        np.testing.assert_allclose([r['hac_se'] for r in got],np.sqrt(np.diag(cov)),rtol=1e-12)
        np.testing.assert_allclose(OLS(y,X).fit().bse,[r['ordinary_se'] for r in got],rtol=1e-12)


if __name__=='__main__':
    unittest.main()
