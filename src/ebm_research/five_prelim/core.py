"""Immutable experiment contracts, hashes, atomic checkpoints and hard disk accounting."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'artifacts/five_state_shape_prelim_v1'
DATA=ROOT/'data/shared/five_state_shape_prelim_v1'
DESIGN=ROOT/'docs/ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md'
PROMPT=ROOT/'docs/ebm_five_preliminary_experiments_codex_execution_prompt_v1.md'
IDS=['P01_INTRADAY_BETA','P02_SIGNED_RV','P03_TREASURY_HEDGE','P04_VOLUME_REVERSAL','P05_FOMC_RESPONSE']
STOCKS=['BAC','KO','HON','ORCL','DHR','KLAC','LOW','HCA','SLB','IP']
HF_REV='776328445b7ac6e7815ef3a483e9c8ded1eb6d56'
CONTRACTS={
 IDS[0]:dict(target='stock_5m_log_return_bp',predictor='spy_synchronous_5m_log_return_bp',state='clock_start_ET_early_mid_late',independent_unit='trading_day',source_ids=['HF_MINUTE_A','LOCAL_SPY_1M'],frequency='1min'),
 IDS[1]:dict(target='next_session_log_RV_389',predictor='current_log_RV_389',state='current_q_down_fixed_thirds',independent_unit='trading_day',source_ids=['HF_MINUTE_A','LOCAL_SPY_1M'],frequency='1min'),
 IDS[2]:dict(target='IEF_same_day_open_close_log_return_bp',predictor='SPY_same_day_open_close_log_return_bp',state='prior_available_DGS10_minus_DGS2_terciles',independent_unit='trading_day',source_ids=['HF_ETF_DAILY','FED_RATES'],frequency='daily'),
 IDS[3]:dict(target='same_stock_next_session_close_close_log_return_bp',predictor='same_stock_current_close_close_log_return_bp',state='own_log_volume_minus_prior20_mean_log_volume',independent_unit='trading_day',source_ids=['LOCAL_OBSERVED_30M','HF_ETF_DAILY'],frequency='30min'),
 IDS[4]:dict(target='SPY_standard_1400_1430_log_return_bp',predictor='absolute_published_surprise_bp',state='published_raw_surprise_sign',independent_unit='FOMC_event',source_ids=['FED_SHOCKS','LOCAL_SPY_1M'],frequency='1min_event')}


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    return h.hexdigest()


def clean(x):
    import numpy as np
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple,np.ndarray)):return [clean(v) for v in x]
    if isinstance(x,np.generic):x=x.item()
    if isinstance(x,float) and not np.isfinite(x):return None
    return x


def write_json(path,value,exclusive=False):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    if exclusive and p.exists():raise FileExistsError('IMMUTABLE_EXISTS: '+str(p))
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(clean(value),indent=2,allow_nan=False)+'\n');tmp.replace(p)


def append_json(path,value):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:f.write(json.dumps(clean(value),allow_nan=False)+'\n')


def now():return dt.datetime.now(dt.timezone.utc).isoformat()


def external(alias):
    defaults={'sae':'SAE_Project','lstm':'LSTM'}
    p=Path(os.environ.get('PRELIM_'+alias.upper()+'_ROOT') or ROOT.parent/defaults[alias]).expanduser().resolve()
    if not p.is_dir():raise FileNotFoundError('EXTERNAL_ROOT_MISSING: '+alias)
    return p


def path_for(ref):
    root=ROOT if ref.get('root','repo')=='repo' else external(ref['root'])
    rel=Path(ref['path'])
    if rel.is_absolute() or '..' in rel.parts:raise ValueError('UNSAFE_REFERENCE')
    p=root/rel
    if sha(p)!=ref['sha256']:raise ValueError('SOURCE_HASH_MISMATCH: '+ref['path'])
    return p


def reference(path,root='repo'):
    base=ROOT if root=='repo' else external(root);p=Path(path)
    return dict(root=root,path=str(p.relative_to(base)),sha256=sha(p),bytes=p.stat().st_size)


class Budget:
    """Count every newly attributable disk file in explicit roots; reserve before writes."""
    def __init__(self,run=RUN,data=DATA,cap=10_000_000_000):
        self.roots=[Path(run),Path(data)];self.cap=cap;self.peak=0
    def used(self):
        total=sum(p.stat().st_size for root in self.roots if root.exists() for p in root.rglob('*') if p.is_file())
        if self.roots[0].resolve()!=RUN.resolve():return total
        for p in (ROOT/'src/ebm_research/five_prelim').rglob('*'):
            if p.is_file():total+=p.stat().st_size
        for p in [ROOT/'scripts/five_prelim.py',ROOT/'tests/test_five_prelim.py']:
            if p.exists():total+=p.stat().st_size
        for p in (ROOT/'tests/__pycache__').glob('test_five_prelim*.pyc'):
            total+=p.stat().st_size
        for p in (ROOT/'reports/sessions').glob('*_SHARED_five_prelim_session.md'):
            total+=p.stat().st_size
        return total
    def check(self,reserve=0,operation='check'):
        used=self.used();self.peak=max(self.peak,used)
        free=shutil.disk_usage(self.roots[0].parent).free
        if used+reserve>=self.cap or reserve+100_000_000>=free:
            raise RuntimeError(f'STORAGE_CAP: {operation}; used={used}, reserve={reserve}, cap={self.cap}, free={free}')
        append_json(self.roots[0]/'logs/storage.jsonl',dict(at=now(),operation=operation,used_bytes=used,reserved_bytes=reserve,peak_measured_bytes=self.peak,free_bytes=free))
        return used


def download(url,path,max_bytes,*,expected_sha=None,headers=None,budget=None):
    """One bounded, resumable whole-object acquisition. No hidden HF/package cache."""
    p=Path(path);receipt=p.with_suffix(p.suffix+'.receipt.json');budget=budget or Budget()
    if receipt.exists():
        saved=json.loads(receipt.read_text())
        if saved['url']!=url or not p.exists() or sha(p)!=saved['sha256']:raise ValueError('DOWNLOAD_RESUME_IDENTITY')
        return saved
    if p.exists():raise ValueError('UNRECEIPTED_EXISTING_FILE: '+str(p))
    budget.check(max_bytes+20_000_000,'reserve '+p.name);p.parent.mkdir(parents=True,exist_ok=True)
    part=p.with_suffix(p.suffix+'.part')
    if part.exists():raise ValueError('INTERRUPTED_PART_PRESERVED: '+str(part))
    count=0;started=now()
    try:
        req=Request(url,headers={'User-Agent':'EBMShape-preliminary-research/1.0',**(headers or {})})
        with urlopen(req,timeout=60) as response,part.open('wb') as f:
            status=response.status;etag=response.headers.get('ETag');length=response.headers.get('Content-Length')
            if length and int(length)>max_bytes:raise RuntimeError('REMOTE_SIZE_EXCEEDS_RESERVATION')
            while True:
                block=response.read(2**20)
                if not block:break
                if count+len(block)>max_bytes:raise RuntimeError('DOWNLOAD_SIZE_CAP')
                f.write(block);count+=len(block)
                budget.check(0,'download chunk '+p.name)
        actual=sha(part)
        if expected_sha and actual!=expected_sha:raise ValueError('REMOTE_OBJECT_HASH_MISMATCH')
        part.replace(p)
        saved=dict(url=url,sha256=actual,bytes=count,status=status,etag=etag,started=started,finished=now())
        write_json(receipt,saved);append_json(RUN/'logs/network.jsonl',dict(**saved,path=str(p.relative_to(ROOT))))
        return saved
    except Exception as e:
        append_json(RUN/'logs/network.jsonl',dict(url=url,path=str(p.relative_to(ROOT)),at=now(),bytes=count,status='FAILED',error=type(e).__name__+': '+str(e)[:200]))
        raise


def contract(config,experiment_id,*,source_registry=None):
    """Reject wrong source, X/Z/Y, instrument, horizon, output namespace or frozen hash."""
    expected=CONTRACTS[experiment_id]
    if config.get('experiment_id')!=experiment_id:raise ValueError('EXPERIMENT_ID_MISMATCH')
    for key,val in expected.items():
        if config.get(key)!=val:raise ValueError('CONTRACT_MISMATCH: '+key)
    instruments=config['instrument_ids']
    if experiment_id==IDS[2] and instruments!=['SPY','IEF']:raise ValueError('TREASURY_INSTRUMENT_MISMATCH')
    if experiment_id in [IDS[0],IDS[3]] and instruments!=STOCKS:raise ValueError('STOCK_UNIVERSE_MISMATCH')
    if not config['output_dir'].endswith('/experiments/'+experiment_id):raise ValueError('OUTPUT_NAMESPACE_MISMATCH')
    if source_registry is not None:
        for id in expected['source_ids']:
            if id not in source_registry:raise ValueError('REQUIRED_SOURCE_MISSING: '+id)
    return True


def load_config(id):
    p=RUN/'configs'/(id+'.json');frozen=json.loads((RUN/'manifests/frozen_configs.json').read_text())
    if sha(p)!=frozen[id]:raise ValueError('FROZEN_CONFIG_CHANGED: '+id)
    c=json.loads(p.read_text());contract(c,id,source_registry=json.loads((RUN/'manifests/source_registry.json').read_text()))
    if sha(DESIGN)!=c['scientific_design_sha256']:raise ValueError('DESIGN_CHANGED')
    return c,frozen[id]
