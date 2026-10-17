"""C P0 only: bounded source completion and fixed-label daily profile audit."""
import argparse
import datetime as dt
import hashlib
import importlib.metadata as metadata
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

from ..experiment_b.pilot import ROOT, ET, UTC, calendar, sha, write_json
from ..experiment_b.acquisition import file_ref, verify_files

OUT=ROOT/'artifacts/C/preliminary_RV_profile_v1_1'
CONFIG=ROOT/'config/C_preliminary_RV_profile_v1.json'
WINDOWS={'OPEN':(0,6),'MID':(30,42),'CLOSE':(72,78)}
SUPPLEMENTARY={'C_SPEC_MID':(24,48),'C_SPEC_CLOSE':(66,78)}
COLORS=['#0072B2','#009E73','#D55E00']
NAMES=['low','middle','high']


def read_json(path):
    return json.loads(path.read_text())


def local_env():
    """Read established local key names only; never report their values."""
    values=dict(os.environ)
    if (ROOT/'.env').exists():
        for line in (ROOT/'.env').read_text().splitlines():
            s=line.strip().removeprefix('export ')
            if s and not s.startswith('#') and '=' in s:
                k,v=s.split('=',1)
                if k.strip() in {'APCA_API_KEY_ID','APCA_API_SECRET_KEY','EBM_DATA_ROOT'}:
                    values.setdefault(k.strip(),v.strip().strip('\"\''))
    return values


def data_root():
    return Path(local_env().get('EBM_DATA_ROOT') or ROOT/'data').expanduser().resolve()


def freeze(handoff):
    """Preserve B; freeze C definitions/source policy before profiles are viewed."""
    if CONFIG.exists():raise FileExistsError('C protocol exists; use acquire/run, never overwrite it')
    data=data_root();baseline=read_json(data/'registry/D2_spy_source_manifest.json')
    refs=[baseline['blocks'][str(y)]['canonical'] for y in range(2016,2022)]
    verify_files(data,refs)
    specs=[p for directory in ['docs','ResearchSpec'] for p in (ROOT/directory).rglob('*')
           if p.is_file() and 'experiment_c_state_dependent_intraday_volatility_profiles_research_spec' in p.name.lower()]
    if len(specs)!=1:raise RuntimeError('Expected exactly one approved C specification')
    supplied=ROOT/'docs/specs/experiment_C_P0_supplied_handoff_v1_1.md'
    if supplied.exists():raise FileExistsError(supplied)
    supplied.write_bytes(Path(handoff).read_bytes())
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    preserved={ROOT/p for p in tracked if p and (ROOT/p).is_file()}
    preserved|={p for p in (ROOT/'artifacts/B').rglob('*') if p.is_file()}
    preserved|={data/r['path'] for r in refs}
    preserved|={p for p in (ROOT/'artifacts/figures').glob('*') if p.is_file()}
    snapshot=[dict(base='repo' if p.is_relative_to(ROOT) else 'data',
                   path=p.relative_to(ROOT if p.is_relative_to(ROOT) else data).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(preserved)]
    write_json(OUT/'start_snapshot.json',dict(branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),
        commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
        status=subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),files=snapshot,
        utc=dt.datetime.now(UTC).isoformat(),free_disk=shutil.disk_usage(ROOT).free))
    p=dict(task_id='C-P0-RV-PROFILE-v1.1',spec_status='READ_WITH_EXPLICIT_P0_WINDOW_EXCEPTION',
           spec_path=specs[0].relative_to(ROOT).as_posix(),spec_sha256=sha(specs[0]),handoff_sha256=sha(supplied),
           user_decision='2026-10-17: P0 windows primary; add C-spec windows as labeled supplementary summaries (Recommended)',
           start='2016-01-05',end='2021-12-31',source_start='2016-01-04',period_status='PROVISIONAL_DESCRIPTIVE_DEVELOPMENT',
           symbol='SPY',feed='sip',adjustment='split',bar_label='UTC start, available one minute later',timezone='America/New_York',
           base_refs=refs,cache='source_cache/C_spy_1m_p0_v1_1',
           source_policy='First usable Alpaca SIP split source; reuse immutable D2 keys and retain only newly missing RTH keys. Require all overlapping OHLC agree within relative1e-10 per retained date; exclude a date on price revision rather than stitch incompatible snapshots. Never use HF patch.',
           min_days=300,min_years=2,transfer_cap=1_000_000_000,max_response_bytes=8_000_000,
           limit=10000,max_pages_month=12,retries=2,timeout_seconds=30,request_spacing_seconds=.2,
           increments='390 terms: first log(C0930/O0930), then389 adjacent closes; variance=sum squared logs, not sqrt/log state',
           q='78 disjoint five-term variances / whole390-term variance',windows=WINDOWS,supplementary_windows=SUPPLEMENTARY,
           predecessor='immediately prior scheduled XNYS session; half/missing/invalid prior makes PREV ineligible; never skip it',
           terciles='independent branch cohorts, stable order(value,date), label=floor(3*rank/N); rank starts0; ties may split, report explicitly',
           bootstrap=dict(seed=42,B=1000,lengths=[5,10],
                          policy='joint circular blocks over original scheduled trading-date slots, including ineligible/half-day slots with label-1. Invalid slots excluded from means, never filled. Only wrap at source-cohort ends; no leap across missing dates. Fixed original labels/cuts in all draws.',
                          max_attempts=1100,percentiles=[2.5,97.5]),
           top_fraction=.01,fragility='ceil(.01*N) largest RV_day by branch, date ascending ties; preserve labels; original FULL primary',
           source_qualifications='SOURCE_PRELIMINARY; vendor SIP qualifying bars, not TAQ/VIX replication; source snapshots may have corrections; split-only not dividend adjustment; license/account restrictions remain',
           rubric=dict(GO='Reproducible interpretable nonopening normalized differences, relative to within-group dispersion, broadly robust to top1/median and both block lengths. Exploratory only.',
                       NO_GO='Almost indistinguishable nonopening profiles under robust comparisons in this SPY proxy/date span; not an equivalence proof.',
                       WEAK='Minor/uncertain or mechanically dominated opening contrast, fragile or discordant evidence; no numerical threshold selected from results.'),
           c_spec_reporting_tolerances=dict(closing_hour_share=.02,opening_half_hour_share=.02,profile_TV=.05),
           evaluation='P0 descriptive only, no fitted models or held-out claims. Full C 60/20/20 split not executed; 2022-2026 excluded.')
    write_json(CONFIG,p)
    write_json(OUT/'local_coverage_gate.json',dict(spec_status=p['spec_status'],D2_max_minutes_per_day=91,
        D1_pre2022_rows=0,full_local_cohort_available=False,source_policy=p['source_policy'],
        cache_estimate_bytes=25_000_000,transfer_estimate_bytes=220_000_000,
        permission='User-authorized additional SPY data <=1e9 cumulative response bytes, no purchase'))
    print('FROZEN',sha(CONFIG),'preserved',len(snapshot))


class BudgetClient:
    """Count every streamed body, including errors/retries, with no secret logging."""
    def __init__(self,p):
        self.p=p;self.ledger=OUT/'download_budget.jsonl'
        self.total=sum(json.loads(s)['response_bytes'] for s in self.ledger.read_text().splitlines()) if self.ledger.exists() else 0
        v=local_env();missing=[k for k in ['APCA_API_KEY_ID','APCA_API_SECRET_KEY'] if not v.get(k)]
        if missing:raise RuntimeError('Missing prerequisite: '+', '.join(missing))
        self.headers={'APCA-API-KEY-ID':v['APCA_API_KEY_ID'],'APCA-API-SECRET-KEY':v['APCA_API_SECRET_KEY'],'Accept-Encoding':'identity'}

    def body(self,response,limit):
        """Read no more than the remaining budget; reject a bounded partial object."""
        chunks=[];n=0;length=response.headers.get('Content-Length')
        if length and int(length)>limit:raise RuntimeError('CONTENT_LENGTH_EXCEEDS_REQUEST_BUDGET')
        try:
            while n<limit:
                b=response.read(min(65536,limit-n))
                if not b:break
                chunks.append(b);n+=len(b)
                self.current_bytes=n
            if n==limit and (length is None or int(length)!=n):raise RuntimeError('STREAM_LIMIT_REACHED_INCOMPLETE_DISCARDED')
            return b''.join(chunks)
        finally:
            self.current_bytes=n

    def get(self,params,tag):
        endpoint='https://data.alpaca.markets/v2/stocks/SPY/bars'
        for attempt in range(self.p['retries']+1):
            remaining=self.p['transfer_cap']-self.total
            if remaining<self.p['max_response_bytes']:raise RuntimeError('BLOCKED_SOURCE_OR_BUDGET: conservative per-request reserve unavailable')
            self.current_bytes=0;started=time.perf_counter();status=None;error=None;result=None
            time.sleep(self.p['request_spacing_seconds'])
            try:
                request=urllib.request.Request(endpoint+'?'+urllib.parse.urlencode(params),headers=self.headers)
                try:response=urllib.request.urlopen(request,timeout=self.p['timeout_seconds'])
                except urllib.error.HTTPError as exc:response=exc
                with response:
                    status=response.status
                    body=self.body(response,min(remaining,self.p['max_response_bytes']))
                if status!=200:raise RuntimeError('HTTP_'+str(status))
                result=json.loads(body)
                if not isinstance(result.get('bars'),list):raise ValueError('Alpaca bars schema unavailable')
            except Exception as exc:
                error=type(exc).__name__+(':'+str(exc) if isinstance(exc,(RuntimeError,ValueError)) else '')
            self.total+=self.current_bytes
            record=dict(utc=dt.datetime.now(UTC).isoformat(),provider='alpaca',endpoint=endpoint,tag=tag,
                start=params['start'],end=params['end'],attempt=attempt,response_bytes=self.current_bytes,
                retry_bytes=self.current_bytes if attempt else 0,cumulative_bytes=self.total,status=status,
                success=error is None,error=error,seconds=time.perf_counter()-started,
                response_sha256=hashlib.sha256(body).hexdigest() if error is None else None)
            with self.ledger.open('a') as f:f.write(json.dumps(record)+'\n');f.flush();os.fsync(f.fileno())
            if result is not None and error is None:return result
            if status in [401,403] or attempt==self.p['retries'] or 'LIMIT' in (error or ''):
                raise RuntimeError(f'Bounded source request failed {tag}: {error}; see sanitized ledger') from None
            time.sleep(2**attempt)


def source_frame(data,p,year):
    """Read only authorized training-year B minute columns; never later science."""
    ref=p['base_refs'][year-2016];verify_files(data,[ref])
    return pd.read_parquet(data/ref['path'],columns=['symbol','timestamp_utc','session_et','open','high','low','close','volume'])


def acquire():
    """Stream monthly queries; retain only keys missing from reusable B sources."""
    wall=time.perf_counter();p=read_json(CONFIG);data=data_root();cache=data/p['cache'];cache.mkdir(parents=True,exist_ok=True)
    manifest_path=OUT/'source_manifest.json'
    m=read_json(manifest_path) if manifest_path.exists() else dict(protocol_sha256=sha(CONFIG),months={},provider='alpaca',feed='sip',adjustment='split',source_preliminary=True)
    if m['protocol_sha256']!=sha(CONFIG):raise ValueError('C source protocol identity mismatch')
    if m.get('complete_months')==72:
        verify_files(data,p['base_refs'])
        verify_files(data,[v['supplement'] for v in m['months'].values()])
        print('VERIFIED_CACHE_REUSED; no network or manifest mutation',m['cumulative_body_bytes'],'prior bytes')
        return
    client=BudgetClient(p);cal=calendar(p['source_start'],p['end'])
    for year in range(2016,2022):
        base=source_frame(data,p,year)
        for month in range(1,13):
            tag=f'{year}-{month:02}'
            if tag in m['months']:
                verify_files(data,[m['months'][tag]['supplement']]);continue
            first=max(pd.Timestamp(tag+'-01'),pd.Timestamp(p['source_start']))
            last=min(first+pd.offsets.MonthEnd(0),pd.Timestamp(p['end']))
            sessions=cal.sessions_in_range(str(first.date()),str(last.date()))
            full=[s for s in sessions if cal.session_close(s).tz_convert(ET).strftime('%H:%M')=='16:00']
            expected=pd.DatetimeIndex(np.concatenate([cal.session_minutes(s).to_numpy() for s in full]))
            # Construct aware UTC grid explicitly after calendar-array concatenation.
            expected=pd.to_datetime(expected,utc=True)
            params=dict(timeframe='1Min',start=cal.session_open(sessions[0]).isoformat(),end=(cal.session_close(sessions[-1])-pd.Timedelta(microseconds=1)).isoformat(),
                        feed='sip',adjustment='split',sort='asc',limit=p['limit'])
            received=[];raw_count=0;last_timestamp=None
            for page in range(p['max_pages_month']):
                reply=client.get(params,f'{tag}_p{page}')
                for b in reply['bars']:
                    timestamp=pd.Timestamp(b['t'])
                    if timestamp.tzinfo is None:raise ValueError('Source timestamp is naive')
                    timestamp=timestamp.tz_convert('UTC')
                    if last_timestamp is not None and timestamp<=last_timestamp:raise ValueError('Duplicate or out-of-order source page timestamp')
                    last_timestamp=timestamp;raw_count+=1
                    if timestamp in expected:
                        received.append(dict(symbol='SPY',timestamp_utc=timestamp,session_et=timestamp.tz_convert(ET).date(),
                            **{long:float(b[short]) for short,long in [('o','open'),('h','high'),('l','low'),('c','close'),('v','volume')]}))
                token=reply.get('next_page_token')
                if not token:break
                params['page_token']=token
            else:raise RuntimeError('Month pagination cap reached; no partial partition retained')
            fresh=pd.DataFrame(received)
            original=base.loc[base.timestamp_utc.isin(expected)].copy()
            overlap=original.merge(fresh,on='timestamp_utc',suffixes=('_old','_new'),validate='one_to_one')
            bad_dates=set();max_error=0.
            if len(overlap):
                a=overlap[[c+'_old' for c in ['open','high','low','close']]].to_numpy()
                b=overlap[[c+'_new' for c in ['open','high','low','close']]].to_numpy()
                error=np.max(np.abs(a/b-1),axis=1);max_error=float(error.max())
                bad_dates=set(overlap.loc[error>1e-10,'session_et_old'].astype(str))
            missing_original=original.loc[~original.timestamp_utc.isin(fresh.timestamp_utc),'session_et'].astype(str).unique().tolist()
            bad_dates.update(missing_original)
            supplement=fresh.loc[~fresh.timestamp_utc.isin(original.timestamp_utc)].copy()
            file=cache/(tag+'.parquet');tmp=file.with_suffix('.parquet.tmp')
            supplement.to_parquet(tmp,index=False,compression='zstd');tmp.replace(file)
            m['months'][tag]=dict(supplement=file_ref(file,data),fetched_regular_rows=len(fresh),supplement_rows=len(supplement),
                reused_rows=len(original),overlap_rows=len(overlap),max_relative_OHLC_difference=max_error,
                excluded_snapshot_revision_dates=sorted(bad_dates),raw_response_rows=raw_count,
                expected_regular_rows=len(expected),observed_missing_minutes=len(expected)-len(fresh),base_source= p['base_refs'][year-2016])
            m.update(cumulative_body_bytes=client.total,acquisition_seconds=time.perf_counter()-wall)
            write_json(manifest_path,m)
            print(tag,'RTH',len(fresh),'supplement',len(supplement),'bytes',client.total,flush=True)
            retained=sum(x.stat().st_size for x in cache.glob('*.parquet'))
            if retained>=1_000_000_000:raise RuntimeError('C cache disk cap reached')
    m.update(status='SOURCE_SELECTED_BEFORE_PROFILES',complete_months=len(m['months']),wall_seconds=time.perf_counter()-wall,
             retained_cache_bytes=sum(x.stat().st_size for x in cache.glob('*.parquet')),transfer_cap=p['transfer_cap'])
    write_json(manifest_path,m)
    print('ACQUISITION_COMPLETE',client.total,'bytes',flush=True)


def profile_day(frame,day,cal):
    """Validate one full source day and return78 variances; never impute/fill."""
    day=str(day)  # pandas 3 calendar parsing rejects NumPy string scalars.
    expected=cal.session_minutes(day)
    if len(expected)!=390:return None,'EARLY_CLOSE'
    if frame.empty:return None,'MISSING_SESSION'
    timestamps=pd.DatetimeIndex(frame.timestamp_utc)
    if timestamps.tz is None:return None,'NAIVE_TIMESTAMP'
    if timestamps.duplicated().any():return None,'DUPLICATE_MINUTE'
    if not timestamps.is_monotonic_increasing:return None,'OUT_OF_ORDER'
    if len(timestamps)==390 and timestamps[0]==expected[0]+pd.Timedelta(minutes=1) and timestamps[-1]==expected[-1]+pd.Timedelta(minutes=1):
        return None,'END_LABELLED_GRID'
    if not timestamps.equals(expected):return None,'INCOMPLETE_OR_WRONG_RTH_GRID'
    prices=frame[['open','high','low','close']].to_numpy(float)
    if not np.isfinite(prices).all() or (prices<=0).any():return None,'INVALID_PRICE'
    o,h,l,c=prices.T
    if not ((l<=np.minimum(o,c))&(h>=np.maximum(o,c))&(l<=h)).all():return None,'INVALID_OHLC'
    increments=np.log(c/np.r_[o[0],c[:-1]])
    rv=(increments**2).reshape(78,5).sum(axis=1)
    if not np.isfinite(rv).all() or (rv<0).any():return None,'INVALID_VARIANCE'
    if rv.sum()<=0:return None,'ZERO_DAILY_VARIANCE'
    q=rv/rv.sum()
    if not np.isclose(q.sum(),1,atol=1e-10,rtol=0):raise ValueError(f'INVALID_QA normalization {day}')
    return rv,'ELIGIBLE'


def rank_groups(values,dates):
    """Deterministic value/date ranks; equal values can split, explicitly recorded."""
    values=np.asarray(values,float);labels=np.full(len(values),-1,dtype=int)
    valid=np.flatnonzero(np.isfinite(values)&(values>0))
    order=valid[np.lexsort((np.asarray(dates)[valid],values[valid]))]
    labels[order]=(3*np.arange(len(order))//len(order))
    boundaries=[]
    for g in [0,1]:
        a=values[labels==g].max();b=values[labels==g+1].min()
        boundaries.append(dict(lower_group_max=float(a),upper_group_min=float(b),tie_split=bool(a==b)))
    return labels,dict(n=len(valid),counts=[int((labels==g).sum()) for g in range(3)],
        boundaries=boundaries,unique_values=len(np.unique(values[valid])),tied_rows=int(len(valid)-len(np.unique(values[valid]))))


def strict_previous(dates,rv_day,cal):
    """Immediate scheduled prior session only; invalid/half-day predecessors block."""
    lookup=dict(zip(dates,rv_day));values=[];reasons=[]
    for day in dates:
        previous=str(cal.previous_session(str(day)).date())
        if previous not in lookup:values.append(np.nan);reasons.append('PREDECESSOR_NOT_IN_SOURCE')
        elif not np.isfinite(lookup[previous]):values.append(np.nan);reasons.append('PREDECESSOR_INCOMPLETE_OR_EARLY')
        else:values.append(lookup[previous]);reasons.append('ELIGIBLE')
    return np.array(values),reasons


def block_indices(n,length,rng):
    """Joint circular blocks in original exchange-date slots, including invalid slots."""
    starts=rng.integers(0,n,size=int(np.ceil(n/length)))
    return ((starts[:,None]+np.arange(length))%n).reshape(-1)[:n]


def bootstrap_means(q,labels,indices):
    """One joint date draw, shared across every bin/state; empty groups reject."""
    sampled=labels[indices];means=[]
    for g in range(3):
        rows=indices[sampled==g]
        rows=rows[np.isfinite(q[rows]).all(axis=1)]
        if not len(rows):return None
        means.append(q[rows].mean(axis=0))
    return np.array(means)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['check','freeze','acquire','run','verify','report'])
    parser.add_argument('--handoff',type=Path)
    args=parser.parse_args()
    if args.action=='check':
        print(json.dumps(dict(status='FROZEN' if CONFIG.exists() else 'NOT_FROZEN',
            network_bytes=sum(json.loads(s)['response_bytes'] for s in (OUT/'download_budget.jsonl').read_text().splitlines()),
            protocol_sha256=sha(CONFIG) if CONFIG.exists() else None)))
    elif args.action=='freeze':
        if args.handoff is None:parser.error('freeze requires --handoff')
        freeze(args.handoff)
    else:
        if not CONFIG.exists():raise RuntimeError('No approved C P0 protocol frozen; acquisition not started')
        if args.action=='acquire':acquire()
        elif args.action=='run':
            from .profile_audit import run
            run()
        elif args.action=='verify':
            from .profile_audit import verify_tables
            print(json.dumps(verify_tables(read_json(CONFIG))))
        else:
            from .reporting import generate
            verdict=read_json(OUT/'scientific_verdict.json')
            generate(verdict['verdict'],verdict['interpretation'])
