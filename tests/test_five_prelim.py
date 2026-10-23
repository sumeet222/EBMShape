"""Tiny synthetic safeguards; no network, EBM, ML, or licensed source values."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from ebm_research.five_prelim.core import CONTRACTS,IDS,STOCKS,Budget,contract,sha,write_json
from ebm_research.five_prelim.features import CAL,minute_summary,volume_lookback,label_daily,lag_rates,next_session
from ebm_research.five_prelim.sources import reconcile
from ebm_research.five_prelim import core
from ebm_research.five_prelim.sources import validated_month_output
from ebm_research.five_prelim.features import parse_events,etf_rates
from ebm_research.five_prelim.statistics import fit_daily,design,block_weights


def config(id):
 return dict(experiment_id=id,**copy.deepcopy(CONTRACTS[id]),instrument_ids=['SPY','IEF'] if id==IDS[2] else STOCKS if id in [IDS[0],IDS[3]] else ['SPY'],output_dir='new/experiments/'+id)


def minute_fixture(unit='ns',day='2019-03-11'):
 ts=CAL.session_minutes(day).as_unit(unit);close=100*np.exp(np.arange(len(ts))*.0001)
 return pd.DataFrame(dict(timestamp=ts,ticker='SPY',open=close,high=close+.01,low=close-.01,close=close,volume=10.,is_valid=True,is_imputed=False))


class FivePrelimTests(unittest.TestCase):
 def test_microsecond_calendar_regression_and_5m_alignment(self):
  for unit in ['us','ns']:
   daily,five,q=minute_summary(minute_fixture(unit),'SYNTHETIC')
   self.assertEqual(len(daily),1);self.assertEqual(len(five),72);self.assertEqual(daily[0]['n_return_intervals'],389)
   self.assertAlmostEqual(daily[0]['RV'],389*.0001**2,places=15)
   self.assertAlmostEqual(five[0]['return_5m_log_bp'],5.,places=10)
   self.assertEqual(five[0]['clock_state'],'early');self.assertEqual(five[18]['clock_state'],'mid');self.assertEqual(five[48]['clock_state'],'late')
   self.assertEqual(pd.Timestamp(five[0]['bin_end_utc']).tz_convert('America/New_York').strftime('%H:%M'),'10:05')
   self.assertAlmostEqual(daily[0]['event_return_bp'],30.,places=10)
 def test_semivariance_closure_zero_returns_and_missing_minutes(self):
  f=minute_fixture();f.loc[20,'close']=f.loc[19,'close'];f.loc[21,'close']=f.loc[20,'close']*.999
  d,_,_=minute_summary(f,'SYNTHETIC');r=np.diff(np.log(f.close));self.assertAlmostEqual(d[0]['RS_minus'],sum(r[r<0]**2),places=15)
  self.assertAlmostEqual(d[0]['RS_minus']+d[0]['RS_plus'],d[0]['RV'],places=15)
  self.assertEqual(len(minute_summary(f.drop(index=5),'SYNTHETIC')[0]),0)
 def test_timezone_DST_and_half_day(self):
  self.assertEqual(CAL.session_open('2019-03-08').hour,14);self.assertEqual(CAL.session_open('2019-03-11').hour,13)
  self.assertEqual(len(minute_summary(minute_fixture(day='2019-11-29'),'SYNTHETIC')[0]),0)
 def test_calendar_next_target_does_not_skip_missing_session(self):
  f=pd.DataFrame(dict(symbol=['SPY']*3,date_et=['2019-03-08','2019-03-11','2019-03-13'],RV=[1.,2.,4.]))
  x=label_daily(f);self.assertEqual(x.next_session.iloc[0],'2019-03-11');self.assertEqual(x.next_session_RV.iloc[0],2.)
  self.assertTrue(np.isnan(x.next_session_RV.iloc[1]));self.assertEqual(next_session('2019-03-08'),'2019-03-11')
 def test_volume20_excludes_current_and_future(self):
  v=np.exp(np.arange(25)/100);x=volume_lookback(v)
  self.assertTrue(np.isnan(x.iloc[19]));self.assertAlmostEqual(x.iloc[20],.2-np.mean(np.arange(20)/100))
  v[21:]*=100;np.testing.assert_allclose(volume_lookback(v).iloc[:21],x.iloc[:21],equal_nan=True)
 def test_treasury_identity_and_wrong_sources_targets_rejected(self):
  registry={k:{} for c in CONTRACTS.values() for k in c['source_ids']}
  for id in IDS:self.assertTrue(contract(config(id),id,source_registry=registry))
  c=config(IDS[2]);c['instrument_ids']=['IEF','SPY']
  with self.assertRaisesRegex(ValueError,'TREASURY'):contract(c,IDS[2])
  for id,field,value in [(IDS[0],'experiment_id',IDS[1]),(IDS[1],'source_ids',CONTRACTS[IDS[0]]['source_ids']+['WRONG']),
                         (IDS[3],'target','same_day_stock_return'),(IDS[4],'source_ids',['LOCAL_SPY_1M'])]:
   c=config(id);c[field]=value
   with self.assertRaisesRegex(ValueError,'MISMATCH'):contract(c,id)
 def test_fred_prior_availability_not_future(self):
  r=pd.DataFrame(dict(date_et=['2021-05-14','2021-05-17'],DGS2=[.1,.2],DGS10=[1.,1.1]))
  f=pd.DataFrame(dict(date_et=['2021-05-17','2021-05-18','2021-05-19']))
  x=lag_rates(r,f);self.assertTrue(pd.isna(x.rate_observation_date.iloc[0]));self.assertEqual(x.rate_observation_date.iloc[1],'2021-05-14')
  self.assertTrue((x.loc[x.available_at.notna(),'available_at']<x.loc[x.available_at.notna(),'session_open']).all())
 def test_duplicates_conflicts_no_silent_preference(self):
  f=minute_fixture().iloc[:3];dup=pd.concat([f,f.iloc[:1]],ignore_index=True);clean,qa=reconcile(dup);self.assertEqual(len(clean),3)
  wrong=f.iloc[:1].copy();wrong['close']*=2;clean,qa=reconcile(pd.concat([f,wrong],ignore_index=True));self.assertEqual(len(clean),2);self.assertEqual(qa['conflicting_rows_excluded'],2)
 def test_storage_cap_prevents_next_write(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'run').mkdir();(root/'data').mkdir();(root/'data/test').write_bytes(b'x'*100)
   b=Budget(root/'run',root/'data',cap=200)
   with self.assertRaisesRegex(RuntimeError,'STORAGE_CAP'):b.check(101,'SYNTHETIC')
 def test_hash_tamper_and_atomic_json(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'test.json';write_json(p,{'fixture':'SYNTHETIC'});before=sha(p)
   p.write_text('tampered');self.assertNotEqual(sha(p),before)
   with self.assertRaises(FileExistsError):write_json(p,{},exclusive=True)
 def test_extended_hours_do_not_invalidate_RTH_cached_fixture(self):
  f=minute_fixture();extra=f.iloc[:2].copy();extra['timestamp']=extra.timestamp-pd.Timedelta(hours=2)
  d,_,_=minute_summary(pd.concat([f,extra],ignore_index=True),'SYNTHETIC_EXTENDED')
  self.assertEqual(len(d),1);self.assertEqual(d[0]['n_return_intervals'],389)
 def test_stale_frozen_config_rejected_before_source_access(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'configs').mkdir();(root/'manifests').mkdir();p=root/'configs'/(IDS[0]+'.json')
   write_json(p,config(IDS[0]));write_json(root/'manifests/frozen_configs.json',{IDS[0]:sha(p)})
   p.write_text(p.read_text()+' ')
   with patch.object(core,'RUN',root),self.assertRaisesRegex(ValueError,'FROZEN_CONFIG_CHANGED'):core.load_config(IDS[0])
 def test_source_hash_and_allowed_readonly_shared_reference(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);p=root/'SYNTHETIC_shared.json';p.write_text('{"source":"SYNTHETIC"}')
   ref=dict(root='repo',path=p.name,sha256=sha(p));initial=list(root.iterdir())
   with patch.object(core,'ROOT',root):
    # Both valid distinct contracts can read the exact same immutable object.
    for id in IDS[:2]:self.assertTrue(contract(config(id),id));self.assertEqual(core.path_for(ref),p)
    self.assertEqual(list(root.iterdir()),initial)
    p.write_text('SYNTHETIC_TAMPER')
    with self.assertRaisesRegex(ValueError,'SOURCE_HASH_MISMATCH'):core.path_for(ref)
 def test_month_checkpoint_verified_resume_and_tamper(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'SYNTHETIC.parquet';pd.DataFrame({'ticker':['SYNTHETIC','SYNTHETIC']}).to_parquet(p)
   e=dict(month='2019-01',status='validated',revision=core.HF_REV,output=dict(sha256=sha(p),rows=2,symbol_counts={'SYNTHETIC':2}))
   with patch('ebm_research.five_prelim.sources.download',side_effect=AssertionError('NETWORK_MUST_NOT_RUN')) as net:
    self.assertTrue(validated_month_output(e,'2019-01',p));net.assert_not_called()
   e['output']['rows']=3
   with self.assertRaisesRegex(ValueError,'COUNT_CONFLICT'):validated_month_output(e,'2019-01',p)
   e['output']['rows']=2;e['output']['sha256']='wrong'
   with self.assertRaisesRegex(ValueError,'HASH_CONFLICT'):validated_month_output(e,'2019-01',p)
 def test_fed_raw_shock_sign_bp_and_official_event_join(self):
  day=pd.Timestamp('2019-01-30');serial=(day-pd.Timestamp('1899-12-30')).days
  sheets={'FOMC (update 2023)':[['Date','Time','MPS','MPS_ORTH'],[serial,'2:00 pm',-.025,999.],
       [serial+1,'2:00 pm',.015,-999.]]}
  with patch('ebm_research.five_prelim.features.read_xlsx',return_value=sheets):
   f=parse_events('SYNTHETIC.xlsx',{'20190130':{'standard_1400':True},'20190131':{'standard_1400':False}})
  np.testing.assert_allclose(f.surprise_bp,[-2.5,1.5]);self.assertEqual(f.standard_1400.tolist(),[True,False]);self.assertEqual(len(set(f.event_id)),2)
 def test_actual_ETF_identity_and_same_OC_return_window(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);prices=root/'SYNTHETIC_prices.parquet';meta=root/'SYNTHETIC_identity.parquet'
   pd.DataFrame(dict(symbol=['SPY','IEF'],date=[pd.Timestamp('2021-05-14')]*2,open=[100.,200.],high=[102.,201.],low=[99.,197.],close=[101.,198.])).to_parquet(prices)
   pd.DataFrame(dict(symbol=['SPY','IEF'],asset_type=['ETF','ETF'])).to_parquet(meta)
   refs={'etf_daily_prices.parquet':prices,'instrument_metadata.parquet':meta}
   for name,value in [('DGS2',.1),('DGS10',1.)]:
    p=root/(name+'.csv');pd.DataFrame({'DATE':['2021-05-10'],name:[value]}).to_csv(p,index=False);refs[name]=p
   with patch('ebm_research.five_prelim.features.path_for',side_effect=lambda p:p):
    f,_=etf_rates({'small_sources':refs});self.assertAlmostEqual(f.spy_oc_bp.iloc[0],10000*np.log(1.01));self.assertAlmostEqual(f.ief_oc_bp.iloc[0],10000*np.log(.99))
    pd.DataFrame(dict(symbol=['SPY','IEF'],asset_type=['ETF','YIELD_LEVEL'])).to_parquet(meta)
    with self.assertRaisesRegex(ValueError,'IDENTITY_FAILED'):etf_rates({'small_sources':refs})
 def test_OLS_hand_calculation_and_trusted_regression(self):
  import statsmodels.api as sm
  dates=CAL.sessions_in_range('2019-01-02','2019-02-28').strftime('%Y-%m-%d').to_numpy()
  rows=[]
  for i,d in enumerate(dates):
   for state,slope,intercept in [('low',2.,1.),('high',5.,-1.)]:
    x=(i%7)-3.;rows.append(dict(date_et=d,state=state,x=x,y=intercept+slope*x,symbol='SYNTHETIC'))
  f=pd.DataFrame(rows);r,draws,W,ds=fit_daily(f,['low','high'],B=40)
  np.testing.assert_allclose(list(r['state_slopes'].values()),[2,5],atol=1e-10);self.assertAlmostEqual(r['contrast'],3.)
  x,_=design(f,['low','high']);np.testing.assert_allclose(r['coefficients'],sm.OLS(f.y,x).fit().params,atol=1e-10)
  # Same date column weights apply to every symbol/row; calendar gaps remain slots.
  np.testing.assert_array_equal(W,block_weights(ds,5,40,20261022));self.assertTrue(np.isfinite(draws).all())
 def test_P01_five_minute_table_cannot_replace_P02_RV_table(self):
  from ebm_research.five_prelim.statistics import load_frame
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'SYNTHETIC_wrong_frequency.parquet';pd.DataFrame(dict(symbol=['SPY'],return_5m_log_bp=[1.],date_et=['2019-01-02'])).to_parquet(p)
   with patch('ebm_research.five_prelim.statistics.path_for',return_value=p),self.assertRaises(KeyError):
    load_frame(IDS[1],config(IDS[1]),dict(derived={'daily_rv_semivariance':{}}))
 def test_sidecar_wrong_ID_target_and_broken_image_link(self):
  from ebm_research.five_prelim.reporting import check_sidecar,check_links,LABELS,COLORS
  expected=dict(experiment_id=IDS[0],target=CONTRACTS[IDS[0]]['target'])
  valid=dict(**expected,axis_semantics=list(LABELS[IDS[0]]),series=['early','mid','late'],series_colors=dict(zip(['early','mid','late'],COLORS)));self.assertTrue(check_sidecar(valid,expected))
  for key,value in [('experiment_id',IDS[1]),('target','WRONG_SYNTHETIC_TARGET')]:
   bad=copy.deepcopy(valid);bad[key]=value
   with self.assertRaisesRegex(ValueError,'FIGURE_METADATA_MISMATCH'):check_sidecar(bad,expected)
  bad=copy.deepcopy(valid);bad['series']=list(reversed(bad['series']))
  with self.assertRaisesRegex(ValueError,'STATE_SERIES_ORDER_MISMATCH'):check_sidecar(bad,expected)
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'SYNTHETIC.md';p.write_text('![SYNTHETIC](missing.png)')
   with self.assertRaisesRegex(ValueError,'BROKEN_EMBEDDED_IMAGE'):check_links(p)
   (Path(temp)/'missing.png').write_bytes(b'SYNTHETIC_REFERENCE_ONLY');self.assertEqual(check_links(p),['missing.png'])

if __name__=='__main__':unittest.main()
