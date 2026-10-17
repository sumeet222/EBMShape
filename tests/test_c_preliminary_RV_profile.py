"""Small independent C accounting/calendar/group/bootstrap tests; no API mocks."""
import datetime as dt
import unittest
import io
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
from ebm_research.experiment_b.pilot import calendar
from ebm_research.experiment_c.preliminary import profile_day,rank_groups,strict_previous,block_indices,bootstrap_means,BudgetClient
from ebm_research.experiment_c.profile_audit import joint_bootstrap


def synthetic(day='2019-03-11'):
    cal=calendar('2016-01-04','2021-12-31');times=cal.session_minutes(day)
    q=np.linspace(.00001,.0002,len(times));closes=100*np.exp(np.cumsum(q));opens=np.r_[100,closes[:-1]]
    f=pd.DataFrame(dict(timestamp_utc=times,open=opens,close=closes,high=np.maximum(opens,closes),low=np.minimum(opens,closes)))
    return cal,f,q


class CProfileTests(unittest.TestCase):
    def test_small_output_smoke_and_independent_bootstrap(self):
        p={'bootstrap':{'seed':42,'B':12,'max_attempts':20}}
        labels=np.tile([0,1,2],20);q=np.tile(np.arange(1,79),(60,1)).astype(float)
        q/=q.sum(axis=1)[:,None];labels[10]=-1;q[10]=np.nan
        for length in [5,10]:
            direct,log=joint_bootstrap(q,labels,p,length)
            weighted,other=joint_bootstrap(q,labels,p,length,independent=True)
            np.testing.assert_allclose(direct,weighted,atol=1e-14)
            self.assertEqual(log['valid'],12);self.assertEqual(other['failed'],0)
        with tempfile.TemporaryDirectory(prefix='c_p0_smoke_') as directory:
            path=Path(directory)/'profiles.npz'
            np.savez_compressed(path,q=q,labels=labels)
            saved=np.load(path);np.testing.assert_equal(saved['q'],q)

    def test_stream_budget_counts_partial_and_rejects_oversize(self):
        client=object.__new__(BudgetClient)
        stream=io.BytesIO(b'1234567890');stream.headers={}
        with self.assertRaisesRegex(RuntimeError,'STREAM_LIMIT'):
            client.body(stream,6)
        self.assertEqual(client.current_bytes,6);self.assertEqual(stream.tell(),6)
        stream=io.BytesIO(b'1234');stream.headers={'Content-Length':'4'}
        self.assertEqual(client.body(stream,4),b'1234');self.assertEqual(client.current_bytes,4)
        stream=io.BytesIO(b'1234567890');stream.headers={'Content-Length':'10'}
        with self.assertRaisesRegex(RuntimeError,'CONTENT_LENGTH'):
            client.body(stream,6)
        self.assertEqual(stream.tell(),0)

    def test_390_returns_and_five_minute_boundary(self):
        cal,f,q=synthetic();rv,status=profile_day(f,'2019-03-11',cal)
        np.testing.assert_array_equal(profile_day(f,np.str_('2019-03-11'),cal)[0],rv)
        self.assertEqual(status,'ELIGIBLE');self.assertEqual(len(rv),78)
        np.testing.assert_allclose(rv,[sum(q[5*k:5*k+5]**2) for k in range(78)],atol=1e-17)
        self.assertAlmostEqual(rv.sum(),sum(q*q),places=14)
        self.assertAlmostEqual(rv[0],sum(q[:5]**2),places=14)
        self.assertAlmostEqual(rv[1],sum(q[5:10]**2),places=14)
        self.assertAlmostEqual(rv[76],sum(q[380:385]**2),places=14)
        self.assertAlmostEqual(rv[77],sum(q[385:390]**2),places=14)

    def test_calendar_DST_holiday_half_day(self):
        cal,f,_=synthetic()
        self.assertEqual(cal.session_open('2019-03-08').hour,14)
        self.assertEqual(cal.session_open('2019-03-11').hour,13)
        self.assertFalse(cal.is_session('2019-12-25'))
        self.assertEqual(profile_day(f,'2019-11-29',cal)[1],'EARLY_CLOSE')

    def test_grid_defects_and_prices(self):
        cal,f,_=synthetic()
        self.assertEqual(profile_day(f.iloc[:-1],'2019-03-11',cal)[1],'INCOMPLETE_OR_WRONG_RTH_GRID')
        self.assertEqual(profile_day(pd.concat([f,f.iloc[:1]]),'2019-03-11',cal)[1],'DUPLICATE_MINUTE')
        self.assertEqual(profile_day(f.iloc[::-1],'2019-03-11',cal)[1],'OUT_OF_ORDER')
        naive=f.copy();naive.timestamp_utc=naive.timestamp_utc.dt.tz_localize(None)
        self.assertEqual(profile_day(naive,'2019-03-11',cal)[1],'NAIVE_TIMESTAMP')
        self.assertEqual(profile_day(f.iloc[:0],'2019-03-11',cal)[1],'MISSING_SESSION')
        shifted=f.copy();shifted.timestamp_utc+=pd.Timedelta(minutes=1)
        self.assertEqual(profile_day(shifted,'2019-03-11',cal)[1],'END_LABELLED_GRID')
        bad=f.copy();bad.loc[0,'open']=0
        self.assertEqual(profile_day(bad,'2019-03-11',cal)[1],'INVALID_PRICE')
        malformed=f.copy();malformed.loc[0,'high']=1
        self.assertEqual(profile_day(malformed,'2019-03-11',cal)[1],'INVALID_OHLC')
        zero=f.copy();zero[['open','high','low','close']]=100.
        self.assertEqual(profile_day(zero,'2019-03-11',cal)[1],'ZERO_DAILY_VARIANCE')

    def test_strict_previous_never_skips_half_or_missing(self):
        cal,_,_=synthetic();dates=['2019-11-27','2019-11-29','2019-12-02','2019-12-03']
        prior,reasons=strict_previous(np.array(dates),[1,np.nan,3,4],cal)
        self.assertTrue(np.isnan(prior[2]));self.assertEqual(prior[3],3)
        self.assertTrue(np.isnan(prior[0]));self.assertEqual(reasons[0],'PREDECESSOR_NOT_IN_SOURCE')
        gap,gap_reasons=strict_previous(['2019-12-02','2019-12-04'],[3,5],cal)
        self.assertTrue(np.isnan(gap[1]));self.assertEqual(gap_reasons[1],'PREDECESSOR_NOT_IN_SOURCE')
        self.assertEqual(reasons[2],'PREDECESSOR_INCOMPLETE_OR_EARLY')
        self.assertEqual(str(cal.previous_session('2019-12-02').date()),'2019-11-29')

    def test_stable_tercile_ties(self):
        values=np.ones(12);dates=np.array([f'2019-01-{i+1:02}' for i in range(12)])
        label,meta=rank_groups(values,dates)
        np.testing.assert_array_equal(label,np.repeat([0,1,2],4));self.assertTrue(meta['boundaries'][0]['tie_split'])
        self.assertEqual(sum(meta['counts']),12)

    def test_joint_bootstrap_reproducible(self):
        labels=np.tile([0,1,2],20);q=np.repeat(labels[:,None]+1.,78,axis=1)
        a=block_indices(60,5,np.random.default_rng(42));b=block_indices(60,5,np.random.default_rng(42))
        np.testing.assert_array_equal(a,b)
        np.testing.assert_allclose(bootstrap_means(q,labels,a),np.repeat([[1.],[2.],[3.]],78,axis=1))
        self.assertEqual(len(block_indices(60,10,np.random.default_rng(42))),60)


if __name__=='__main__':unittest.main()
