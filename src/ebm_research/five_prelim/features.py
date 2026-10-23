"""One shared derivation from observed prices: returns, semivariance, volume, rates and events."""
import json
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import exchange_calendars as xcals
import pyarrow.parquet as pq
from .core import *
from .sources import reconcile,read_xlsx,utc_timestamps

CAL=xcals.get_calendar('XNYS',start='2015-12-01',end='2026-10-01',side='left')


def next_session(day):return str(CAL.next_session(day).date())
def previous_session(day):return str(CAL.previous_session(day).date())


def minute_summary(frame,source_id):
    """Complete observed 390-row sessions; RV389 excludes overnight and first OC return."""
    if frame.empty:return [],[],[]
    frame=frame.copy();frame['timestamp']=utc_timestamps(frame.timestamp)
    local=frame.timestamp.dt.tz_convert('America/New_York');minute=local.dt.hour*60+local.dt.minute
    frame=frame[(minute>=570)&(minute<960)].copy()
    frame['date_et']=frame.timestamp.dt.tz_convert('America/New_York').dt.date.astype(str)
    daily=[];five=[];quality=[]
    for (ticker,date),g in frame.groupby(['ticker','date_et'],sort=True):
        if not CAL.is_session(date):
            quality.append(dict(symbol=ticker,date_et=date,observed=len(g),eligible=False,reason='NON_SESSION'));continue
        expected=CAL.session_minutes(date);g=g.sort_values('timestamp')
        observed=pd.DatetimeIndex(g.timestamp).as_unit('ns');full=len(expected)==390
        complete=full and len(g)==390 and not g.timestamp.duplicated().any() and np.array_equal(observed.asi8,expected.as_unit('ns').asi8)
        complete=complete and bool(g.get('is_valid',pd.Series(True,index=g.index)).all()) and not bool(g.get('is_imputed',pd.Series(False,index=g.index)).any())
        quality.append(dict(symbol=ticker,date_et=date,observed=len(g),expected=len(expected),eligible=complete,reason='COMPLETE' if complete else 'HALF_OR_MISSING_INVALID_OBSERVATION',source_id=source_id))
        if not complete:continue
        close=g.close.to_numpy(float);r=np.diff(np.log(close));rv=float(r@r);minus=float(np.sum(r[r<0]**2));plus=float(np.sum(r[r>0]**2))
        np.testing.assert_allclose(minus+plus,rv,atol=1e-18,rtol=1e-12)
        if rv<=0:continue
        c=dict(symbol=ticker,date_et=date,RV=rv,RS_minus=minus,RS_plus=plus,q_down=minus/rv,n_return_intervals=389,
            source_id=source_id,observed=True,is_imputed=False,large_minute_move=bool(np.max(abs(r))>np.log(1.25)),
            available_at=CAL.session_close(date).isoformat(),open=float(g.open.iloc[0]),close=float(close[-1]),volume=float(g.volume.sum()))
        if ticker=='SPY':
            # C13:59 is the close immediately before14:00; C14:29 ends14:30.
            c.update(event_return_bp=float(np.log(close[299]/close[269])*10000),pre_event_return_bp=float(np.log(close[269]/close[264])*10000),
                     event_start_reference='13:59 minute close at14:00',event_end_reference='14:29 minute close at14:30')
        daily.append(c)
        if date.startswith('2019-'):
            for k in range(6,78):
                start=570+5*k;end=expected[k*5+4]+pd.Timedelta(minutes=1)
                group='early' if start<690 else 'mid' if start<840 else 'late'
                five.append(dict(symbol=ticker,date_et=date,bin_start_minute_ET=start,bin_end_utc=end.isoformat(),
                    return_5m_log_bp=float(np.log(close[k*5+4]/close[k*5-1])*10000),clock_state=group,source_id=source_id,
                    n_genuine_intervals=5,observed=True))
    return daily,five,quality


def label_daily(frame):
    """Calendar-adjacent source date joins; missing/half-day labels remain unavailable."""
    f=frame.copy();f['previous_session']=f.date_et.map(previous_session);f['next_session']=f.date_et.map(next_session)
    if f.duplicated(['symbol','date_et']).any():raise ValueError('DAILY_DUPLICATE_KEY')
    lookup=f.set_index(['symbol','date_et'])
    def get(column,which):
        keys=pd.MultiIndex.from_arrays([f.symbol,f[which]])
        return lookup[column].reindex(keys).to_numpy()
    f['lag_RV']=get('RV','previous_session');f['next_session_RV']=get('RV','next_session')
    f['log_RV']=np.log(f.RV);f['lag_log_RV']=np.log(f.lag_RV);f['next_log_RV']=np.log(f.next_session_RV)
    f['next_target_available_at']=f.next_session.map(lambda d:CAL.session_close(d).isoformat())
    return f


def volume_lookback(values):
    """Log-volume deviation from previous20eligible sessions, excluding the current value."""
    values=pd.Series(values,dtype=float)
    logs=np.log(values.where(values>0))
    return logs-logs.shift(1).rolling(20,min_periods=20).mean()


def stock_daily(registry):
    daily=[];issues=[]
    for ref in registry['LOCAL_OBSERVED_30M']['refs']:
        p=path_for(ref);meta=json.loads(path_for(ref['metadata']).read_text())
        if meta['schema_version']!=2 or not meta['download_complete'] or meta['parquet_sha256']!=sha(p):raise ValueError('NATIVE_30M_PROVENANCE')
        if meta['adjustment']!='split-adjusted; not dividend-adjusted':raise ValueError('30M_ADJUSTMENT_CHANGED')
        f=pd.read_parquet(p,filters=[('session','>=','2024-09-26'),('session','<=','2025-09-25')])
        if set(f.ticker)!={ref['symbol']} or not (f.bar_minutes==30).all():raise ValueError('30M_SYMBOL_FREQUENCY_MISMATCH')
        for day,g in f.groupby('session'):
            if not CAL.is_session(day):raise ValueError('NATIVE_NON_SESSION')
            exp=CAL.session_minutes(day)[::30];g=g.sort_values('timestamp')
            valid=len(exp)==13 and len(g)==13 and np.array_equal(pd.DatetimeIndex(g.timestamp).as_unit('ns').asi8,exp.as_unit('ns').asi8)
            numeric=g[['open','high','low','close','volume']].to_numpy(float)
            valid=valid and np.isfinite(numeric).all() and (numeric[:,:4]>0).all() and (numeric[:,4]>=0).all()
            issues.append(dict(symbol=ref['symbol'],date_et=day,observed=len(g),eligible=bool(valid),reason='COMPLETE13' if valid else 'HALF_MISSING_INVALID'))
            if valid:daily.append(dict(symbol=ref['symbol'],date_et=day,open=g.open.iloc[0],close=g.close.iloc[-1],volume=g.volume.sum(),source_id='LOCAL_OBSERVED_30M',adjustment=meta['adjustment'],observed=True))
    f=pd.DataFrame(daily).sort_values(['symbol','date_et']);records=[]
    for symbol,g in f.groupby('symbol',sort=False):
        g=g.copy();lookup=g.set_index('date_et');prev=g.date_et.map(previous_session);nxt=g.date_et.map(next_session)
        g['stock_return_bp']=10000*np.log(g.close.to_numpy()/lookup.close.reindex(prev).to_numpy())
        returns=pd.Series(g.stock_return_bp.to_numpy(),index=g.date_et)
        g['stock_next_return_bp']=returns.reindex(nxt).to_numpy();g['next_session']=nxt.to_numpy()
        g['relative_log_volume']=volume_lookback(g.volume.to_numpy()).to_numpy();g['prior20_count']=np.minimum(np.arange(len(g)),20)
        g['state_available_at']=g.date_et.map(lambda d:CAL.session_close(d).isoformat())
        g['target_available_at']=g.next_session.map(lambda d:CAL.session_close(d).isoformat())
        records.append(g)
    return pd.concat(records,ignore_index=True),pd.DataFrame(issues)


def lag_rates(rates,returns):
    """Conservative publication rule: next federal business day17:00ET, strict prior-open join."""
    rates=rates.sort_values('date_et').copy();bday=CustomBusinessDay(calendar=USFederalHolidayCalendar())
    dates=pd.DatetimeIndex(pd.to_datetime(rates.date_et))
    publish=pd.DatetimeIndex([d+bday+pd.Timedelta(hours=17) for d in dates]).tz_localize('America/New_York').tz_convert('UTC')
    rates['available_at']=publish;rates['yield_spread_pp']=rates.DGS10-rates.DGS2
    f=returns.sort_values('date_et').copy();f['session_open']=pd.DatetimeIndex(pd.to_datetime(f.date_et)).tz_localize('America/New_York').tz_convert('UTC')+pd.Timedelta(hours=9,minutes=30)
    joined=pd.merge_asof(f.sort_values('session_open'),rates.rename(columns={'date_et':'rate_observation_date'}).sort_values('available_at'),left_on='session_open',right_on='available_at',direction='backward',allow_exact_matches=False)
    has=joined.available_at.notna();assert (joined.loc[has,'available_at']<joined.loc[has,'session_open']).all()
    assert (joined.loc[has,'rate_observation_date']<joined.loc[has,'date_et']).all()
    return joined


def etf_rates(acquired):
    refs=acquired['small_sources'];p=path_for(refs['etf_daily_prices.parquet'])
    identity=pd.read_parquet(path_for(refs['instrument_metadata.parquet']))
    identity=identity[identity.symbol.isin(['SPY','IEF'])]
    if set(identity.symbol)!={'SPY','IEF'} or identity.symbol.duplicated().any() or not identity.asset_type.eq('ETF').all():raise ValueError('ETF_INSTRUMENT_IDENTITY_FAILED')
    f=pd.read_parquet(p,filters=[('symbol','in',['SPY','IEF']),('date','>=',pd.Timestamp('2021-05-12')),('date','<=',pd.Timestamp('2025-09-25'))])
    if f.duplicated(['date','symbol']).any() or set(f.symbol)!={'SPY','IEF'}:raise ValueError('ETF_SYMBOL_OR_KEY_MISMATCH')
    prices=f[['open','high','low','close']].to_numpy(float)
    if not np.isfinite(prices).all() or (prices<=0).any():raise ValueError('ETF_INVALID_PRICE')
    if not ((f.high>=f[['open','close','low']].max(axis=1))&(f.low<=f[['open','close','high']].min(axis=1))).all():raise ValueError('ETF_OHLC_MISMATCH')
    f['date_et']=pd.to_datetime(f.date).dt.strftime('%Y-%m-%d');f['oc_return_bp']=10000*np.log(f.close/f.open)
    pivot=f.pivot(index='date_et',columns='symbol',values='oc_return_bp').dropna().reset_index().rename(columns={'SPY':'spy_oc_bp','IEF':'ief_oc_bp'})
    pivot['source_id']='HF_ETF_DAILY';primary=pivot[pivot.date_et<='2023-12-29'].copy()
    rates=[]
    for name in ['DGS2','DGS10']:
        x=pd.read_csv(path_for(refs[name]));datecol='observation_date' if 'observation_date' in x else 'DATE'
        if name not in x:raise ValueError('FRED_SERIES_MISMATCH')
        x=x.rename(columns={datecol:'date_et'});x[name]=pd.to_numeric(x[name],errors='coerce');rates.append(x[['date_et',name]].dropna())
    rates=rates[0].merge(rates[1],on='date_et',how='inner',validate='one_to_one')
    primary=lag_rates(rates,primary);primary['macro_source_id']='FED_RATES'
    return primary,pivot


def parse_events(workbook,official):
    """Choose published updated FOMC raw MPS, normalize percentage points to basis points."""
    sheets=read_xlsx(workbook);rows=sheets['FOMC (update 2023)'];columns=rows[0]
    required=['Date','Time','MPS','MPS_ORTH']
    if not set(required)<=set(columns):raise ValueError('FED_SHOCK_DEFINITION_UNVERIFIED')
    frame=pd.DataFrame([r+[None]*(len(columns)-len(r)) for r in rows[1:]],columns=columns)
    # The paper/workbook ED contracts are rate percentage-point changes; MPS has
    # ED4 unit loading. The publisher chart (in bp) is independently reconciled.
    dates=pd.to_datetime(pd.to_numeric(frame.Date),unit='D',origin='1899-12-30');frame['date_et']=dates.dt.strftime('%Y-%m-%d')
    frame=frame[(frame.date_et>='2016-01-01')&(frame.date_et<='2021-12-31')].copy()
    frame['published_MPS_percentage_points']=pd.to_numeric(frame.MPS,errors='coerce');frame['surprise_bp']=frame.published_MPS_percentage_points*100
    frame['release_time_source']=frame.Time.astype(str)
    frame['official_1400']=[official.get(day.replace('-',''),{}).get('standard_1400',False) for day in frame.date_et]
    frame['sheet_1400']=frame.release_time_source.str.fullmatch(r'2:00\s*pm',case=False)
    frame['standard_1400']=frame.official_1400&frame.sheet_1400
    frame['source_id']='FED_SHOCKS';frame['event_id']='FRBSF_FOMC_'+frame.date_et
    if frame.event_id.duplicated().any():raise ValueError('FED_EVENT_DUPLICATE')
    return frame[['event_id','date_et','release_time_source','published_MPS_percentage_points','surprise_bp','official_1400','sheet_1400','standard_1400','source_id']]


def derive():
    checkpoint=RUN/'manifests/validated_inputs.json'
    if checkpoint.exists():
        saved=json.loads(checkpoint.read_text())
        for id in IDS:load_config(id)
        for ref in saved['original_source_refs']+list(saved['derived'].values()):path_for(ref)
        print('SKIP_VERIFIED_SHARED_DERIVATIVES; immutable validated inputs already exist',flush=True)
        return
    registry=json.loads((RUN/'manifests/source_registry.json').read_text());acq=json.loads((RUN/'manifests/acquired_sources.json').read_text())
    for id in IDS:load_config(id)
    budget=Budget();budget.check(120_000_000,'all compact derived tables');dest=DATA/'derived';dest.mkdir(exist_ok=True)
    rows=[];five=[];qa=[];sources={};originals=[]
    # One source traversal shared by P01/P02/P05. Only training-era SPY is decoded.
    spyrefs=registry['LOCAL_SPY_1M']['refs']
    annual={str(year):next(r for r in spyrefs if r['path'].endswith('year='+str(year)+'.parquet')) for year in range(2016,2022)}
    for year in range(2016,2022):
        a=pd.read_parquet(path_for(annual[str(year)]),columns=['symbol','timestamp_utc','open','high','low','close','volume'])
        annual_month=a.timestamp_utc.dt.month
        for month in range(1,13):
            label=f'{year}-{month:02}';ref=next(r for r in spyrefs if r['path'].endswith('/'+label+'.parquet'))
            s=pd.read_parquet(path_for(ref));native=a[annual_month==month]
            f=pd.concat([native,s],ignore_index=True).rename(columns={'symbol':'ticker','timestamp_utc':'timestamp'})
            if f.duplicated(['ticker','timestamp']).any():raise ValueError('SPY_CANONICAL_SOURCE_COLLISION')
            f,_=reconcile(f);rr,ff,qq=minute_summary(f,'LOCAL_SPY_1M');rows+=rr;five+=ff;qa+=qq
            originals.extend([annual[str(year)],ref])
        print('DERIVE_SPY',year,len(rows),flush=True)
    # Completed selected union + read-only cached BAC/KO. Never read fill proxies.
    for ref in acq['minute_partitions']:
        month=Path(ref['path']).stem;f=pd.read_parquet(path_for(ref));originals.append(ref)
        cached=next(r for r in registry['HF_MINUTE_A']['refs'] if r['month']==month)
        c=pd.read_parquet(path_for(cached),columns=['timestamp','ticker','open','high','low','close','volume','is_genuine','is_imputed'],filters=[('ticker','in',['BAC','KO'])])
        if not c.is_genuine.all() or c.is_imputed.any():raise ValueError('IMPUTED_MINUTES_FORBIDDEN')
        combined=pd.concat([f,c],ignore_index=True);combined,_=reconcile(combined)
        rr,ff,qq=minute_summary(combined,'HF_MINUTE_A');rows+=rr;five+=ff;qa+=qq;originals.append(cached)
        print('DERIVE_STOCKS',month,flush=True)
    rv=label_daily(pd.DataFrame(rows));market=pd.DataFrame(five);quality=pd.DataFrame(qa)
    if int((rv.symbol=='SPY').sum())<1000:raise ValueError('SPY_COMPLETE_SESSION_QA_FAILED; no screens authorized')
    rv.to_parquet(dest/'daily_rv_semivariance.parquet',index=False);market.to_parquet(dest/'market_returns_5m.parquet',index=False)
    quality.to_csv(RUN/'manifests/minute_session_quality.csv',index=False)
    derived={'daily_rv_semivariance':reference(dest/'daily_rv_semivariance.parquet'),'market_returns_5m':reference(dest/'market_returns_5m.parquet')}
    holds=dict(acq['holds'])
    if set(market.symbol)!={'SPY',*STOCKS}:
        holds['P01_MINUTE_SUPPORT']='Frozen symbols without any complete session: '+str(sorted({'SPY',*STOCKS}-set(market.symbol)))
    sd,sqa=stock_daily(registry);sd.to_parquet(dest/'daily_stock_returns_volume.parquet',index=False);sqa.to_csv(RUN/'manifests/stock30_session_quality.csv',index=False)
    derived['daily_stock_returns_volume']=reference(dest/'daily_stock_returns_volume.parquet')
    originals.extend([r for r in registry['LOCAL_OBSERVED_30M']['refs']]);originals.extend(acq['small_sources'].values())
    try:
        treasury,etf=etf_rates(acq);treasury.to_parquet(dest/'daily_spy_treasury_returns.parquet',index=False);etf.to_parquet(dest/'daily_etf_oc_controls.parquet',index=False)
        derived['daily_spy_treasury_returns']=reference(dest/'daily_spy_treasury_returns.parquet');derived['daily_etf_oc_controls']=reference(dest/'daily_etf_oc_controls.parquet')
        sd=sd.merge(etf[['date_et','spy_oc_bp']],on='date_et',how='left',validate='many_to_one');sd.to_parquet(dest/'daily_stock_returns_volume.parquet',index=False);derived['daily_stock_returns_volume']=reference(dest/'daily_stock_returns_volume.parquet')
    except Exception as e:holds['P03_FEATURES']=type(e).__name__+': '+str(e)[:200]
    try:
        official=json.loads((RUN/'manifests/official_event_times.json').read_text())
        event=parse_events(path_for(acq['small_sources']['FED_SHOCKS']),official)
        event=event.merge(rv[rv.symbol=='SPY'][['date_et','event_return_bp','pre_event_return_bp']],on='date_et',how='left',validate='one_to_one')
        event['eligible']=event.standard_1400&event.event_return_bp.notna()&event.surprise_bp.notna()
        event['exclusion_reason']=np.where(~event.standard_1400,'NON1400_OR_OFFICIAL_UNVERIFIED',np.where(event.event_return_bp.isna(),'SPY_INCOMPLETE','ELIGIBLE'))
        event.to_parquet(dest/'fomc_events.parquet',index=False);derived['fomc_events']=reference(dest/'fomc_events.parquet')
        event.to_csv(RUN/'manifests/fomc_event_eligibility.csv',index=False)
    except Exception as e:holds['P05_FEATURES']=type(e).__name__+': '+str(e)[:200]
    unique={r['root']+':'+r['path']:r for r in originals}
    tables={}
    for name,ref in derived.items():
        t=pq.read_table(path_for(ref));tables[name]=dict(rows=len(t),columns=t.schema.names,schema=str(t.schema),input_frequency={'market_returns_5m':'5min','fomc_events':'event'}.get(name,'daily'))
    write_json(RUN/'manifests/validated_inputs.json',dict(derived=derived,original_source_refs=list(unique.values()),schema=tables,holds=holds,
        source_registry_sha256=sha(RUN/'manifests/source_registry.json'),at=now(),RV='389 adjacent close-to-close one-minute returns, no overnight, epsilon0',
        column_dictionary={'RS_minus':'sum squared negative minute log returns','q_down':'RS_minus/RV','stock_return_bp':'same-stock split-adjusted close-to-close price log return×10000',
        'relative_log_volume':'own logvolume minus previous20eligible mean logvolume; current excluded','surprise_bp':'updated FOMC sheet rawMPS percentage points×100; never MPS_ORTH'},
        source_time='UTC minute/bar starts; full390 ordinary XNYS only; 5m label end; event14:00=C13:59 and14:30=C14:29',
        exploratory_periods={id:load_config(id)[0]['coverage'] for id in IDS}))
    (RUN/'reports/shared_features_QA.md').write_text('# Shared feature QA\n\n'+json.dumps(dict(tables=tables,holds=holds,complete_rv_days=len(rv),minute_days_checked=len(quality)),indent=2)+'\n\nEvery derivative is unique-keyed and source-hash bound; no missing minute is filled. New RV389 intentionally differs from old C RV390. Calendar-adjacent next/previous labels never jump over ineligible sessions. Rates use next federal-business-day17:00 assumed publication plus strict prior-open join; current vintage and historical revision uncertainty remain explicit. Stock volume is native observed volume, not a filled/imputed series or share turnover.\n')
    budget.check(0,'shared features complete')
    print('DERIVATIVES',tables,'HOLDS',holds,flush=True)
