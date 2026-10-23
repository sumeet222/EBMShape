"""Five-screen staged runner; immutable A/B/C are never output destinations."""
import argparse
import datetime as dt
import importlib.metadata as md
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
from urllib.parse import urljoin
import re
import pyarrow.parquet as pq
import pandas as pd
from .core import *

LSTM_PACKET='reports/data_audit/ta018d_hf1m_long_2026-10-22_155547'


def stage_note(n,text):
    p=RUN/f'logs/stage{n}_session_report.md'
    p.write_text(f'# Stage {n} checkpoint\n\nUTC: {now()}\n\n{text}\n\nAll writes use new five-screen namespaces. No old A/B/C outputs modified.\n')
    write_json(RUN/'checkpoints/current_stage.json',dict(stage=n,at=now(),state='COMPLETED',next_action=['metadata/freeze','derive','screen','report','verify'][n]))


def inventory():
    if (RUN/'manifests/initial_state.json').exists():raise FileExistsError('EXISTING_RUN; use explicit frozen resume')
    for d in ['configs','manifests','logs','checkpoints','reports/figures','reports/figure_data','cache','scratch','experiments']:(RUN/d).mkdir(parents=True,exist_ok=True)
    DATA.mkdir(parents=True,exist_ok=True)
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    protected={}
    for top in ['src','scripts','tests','config','docs','reports','artifacts','data']:
        for p in (ROOT/top).rglob('*'):
            if p.is_file() and '__pycache__' not in str(p) and not p.is_relative_to(RUN) and not p.is_relative_to(DATA) and '/five_prelim/' not in str(p) and p.name not in ['five_prelim.py','test_five_prelim.py']:
                protected[str(p.relative_to(ROOT))]=dict(bytes=p.stat().st_size,sha256=sha(p))
    for p in [ROOT/'AGENTS.md',ROOT/'pyproject.toml',ROOT/'.gitignore',ROOT/'README.md']:
        protected[str(p.relative_to(ROOT))]=dict(bytes=p.stat().st_size,sha256=sha(p))
    write_json(RUN/'manifests/protected_legacy_files.json',protected)
    state=dict(at=now(),git_branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_status=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
        physical_free_bytes=shutil.disk_usage(ROOT).free,python=platform.python_version(),
        versions={p:md.version(p) for p in ['numpy','pandas','pyarrow','scipy','statsmodels','matplotlib','pillow','exchange-calendars']},
        baseline_repo_bytes=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file() and '.git/' not in str(p) and not p.is_relative_to(RUN) and not p.is_relative_to(DATA)),
        controlling_design_sha256=sha(DESIGN),execution_prompt_sha256=sha(PROMPT))
    write_json(RUN/'manifests/initial_state.json',state)
    write_json(RUN/'manifests/resolved_paths.json',dict(project_root=str(ROOT),run_root=str(RUN),new_shared_data=str(DATA),
        legacy_parent='artifacts; existing B,C remain read only',external_roots={'sae':str(external('sae')),'lstm':str(external('lstm'))},
        portable_roots='ROOT/data or PRELIM_SAE_ROOT/PRELIM_LSTM_ROOT; defaults sibling directories; hashes required'))
    # Immutable existing source refs; decode no target/return relationships here.
    p0=json.loads((ROOT/'artifacts/C/preliminary_RV_profile_v1_1/source_manifest.json').read_text())
    registry=json.loads((ROOT/'data/registry/C_preliminary_RV_profile_v1_1.json').read_text())
    spy_refs=[]
    for r in registry['base_sources']+[v['supplement'] for v in p0['months'].values()]:
        path=ROOT/'data'/r['path']
        assert sha(path)==r['sha256'],str(path)
        spy_refs.append(reference(path))
    lstm=external('lstm');pack=lstm/LSTM_PACKET
    manifest=json.loads((pack/'complete_acquisition_manifest.json').read_text())
    assert manifest['dataset']=='mito0o852/OHLCV-1m'
    cached=[]
    for e in manifest['monthly']:
        if e['month'].startswith('2019-'):
            r=e['derived_files']['canonical_observed'];p=lstm/r['path'];assert sha(p)==r['sha256']
            cached.append(dict(month=e['month'],**reference(p,'lstm')))
    sae=external('sae');roster=[];selected=[]
    for p in sorted((sae/'data/metadata').glob('*.json')):
        meta=json.loads(p.read_text())
        if meta.get('schema_version')!=2 or 'universe_entry' not in meta:continue
        symbol=meta['ticker'];raw=sae/'data/raw'/(symbol+'.parquet')
        if not raw.exists():continue
        roster.append(dict(symbol=symbol,sector=meta['universe_entry'].get('sector'),rows=meta.get('row_count'),start=meta.get('requested_start'),end=meta.get('requested_end'),adjustment=meta.get('adjustment')))
        if symbol in STOCKS:
            assert meta['download_complete'] and sha(raw)==meta['parquet_sha256']
            selected.append(dict(symbol=symbol,**reference(raw,'sae'),metadata=reference(p,'sae'),schema=str(pq.ParquetFile(raw).schema_arrow)))
    assert len(selected)==10 and len(cached)==12
    pd.DataFrame(roster).to_csv(RUN/'manifests/local_30m_roster.csv',index=False)
    refs={'LOCAL_SPY_1M':dict(provider='Alpaca SIP',adjustment='split-only; no overnight in new RV',frequency='1min',source_id='LOCAL_SPY_1M',refs=spy_refs,coverage=['2016-01-04','2021-12-31'],observed=True),
        'HF_MINUTE_A':dict(provider='mito0o852/OHLCV-1m',revision=HF_REV,source_id='HF_MINUTE_A',refs=cached,local_symbols=['BAC','KO'],new_symbols=[x for x in STOCKS if x not in ['BAC','KO']],frequency='1min',observed_only=True,coverage=['2019-01-01','2019-12-31'],
            adjustment='publisher as reported; intraday ratios cancel fixed daily scale; corporate-action/reconciliation limitations retained',rights='Public user-design-approved private research source; separate existing maintainer-permission receipt is user-reported, not independent upstream legal certification; no raw redistribution',permission_receipt=reference(pack/'permission_receipt.json','lstm')),
        'LOCAL_OBSERVED_30M':dict(provider='Massive',source_id='LOCAL_OBSERVED_30M',frequency='30min',refs=selected,coverage=['2024-09-26','2025-09-25'],observed_only=True,adjustment='split-adjusted; not dividend-adjusted; native observed volume, no filled layer',rights='Existing personal research source; raw data remain external'),
        'HF_ETF_DAILY':dict(provider='thecharttruth/etf-data',source_id='HF_ETF_DAILY',status='NEEDS_METADATA_AND_SMALL_ACQUISITION',symbols=['SPY','IEF'],frequency='daily'),
        'FED_RATES':dict(provider='FRED',source_id='FED_RATES',status='NEEDS_SMALL_ACQUISITION',symbols=['DGS2','DGS10'],frequency='daily'),
        'FED_SHOCKS':dict(provider='FRBSF',source_id='FED_SHOCKS',status='NEEDS_SMALL_ACQUISITION',definition='published raw 30-minute path surprise in bp, not orthogonalized; source metadata must confirm')}
    write_json(RUN/'manifests/source_registry_draft.json',refs)
    files=json.loads((pack/'source_revision_manifest.json').read_text())
    months=[x for x in files['files'] if x['month'].startswith('2019-')]
    assert len(months)==12
    write_json(RUN/'manifests/hf_existing_metadata.json',dict(dataset=files['dataset'],revision=files['revision'],months=months,source=reference(pack/'source_revision_manifest.json','lstm')))
    budget=Budget();used=budget.check(0,'inventory')
    largest=max(x['bytes'] for x in months)
    forecast=dict(hard_cap_bytes=10_000_000_000,soft_replan_bytes=8_000_000_000,baseline_repo_bytes=state['baseline_repo_bytes'],physical_free_bytes=state['physical_free_bytes'],
        monthly_raw_max_bytes=largest,retained_new_minute_budget_bytes=100_000_000,derivatives_bytes=100_000_000,small_sources_bytes=30_000_000,plots_reports_logs_bundle_bytes=80_000_000,cache_bytes=20_000_000,
        conservative_incremental_peak_forecast_bytes=largest+330_000_000,safety_margin_bytes=10_000_000_000-largest-330_000_000,used_after_inventory=used,
        physical_workspace_total_cap='No stricter imposed cap discovered; 10GB is explicitly incremental; free space separately checked')
    if forecast['conservative_incremental_peak_forecast_bytes']>=8_000_000_000:raise RuntimeError('SOFT_STORAGE_REPLAN')
    write_json(RUN/'manifests/storage_budget.json',forecast)
    report=f'''# No-download shared source inventory\n\nCurrent project `{ROOT.name}`; sibling run under artifacts, existing B/C untouched. Existing repository footprint {state['baseline_repo_bytes']:,} bytes; free {state['physical_free_bytes']:,} bytes. No package installation.\n\nSPY: 6 annual D2 training references plus72 disjoint C supplement months, source hashes checked. Only2016–2021 decoded. C cached RV is **not reused**: new P02 uses389 within-session close-to-close intervals, whereas C used a first-minute open-to-close contribution.\n\nStocks: original native observed30min Massive roster metadata found externally, {len(roster)} metadata-backed symbols. Imputed/indicator/modeling layers are rejected. Ten sector-diverse liquid symbols frozen without seeing response relationships: {', '.join(STOCKS)}. CAT/JNJ are not members of this verified99-stock roster and are not silently added.\n\nMinute cache: existing12 verified2019 HF canonical-observed partitions supply BAC/KO by read-only reference; they contain genuine/imputed flags and no synthetic proxies will be read. Only the other8 stocks require one common12-month source pass. SPY already available, so no new SPY minute copy. Other local HF20 names are outside the specified roster and not substituted.\n\nNo ETF/FRED/FRBSF files found in this project's source registry; small original-source acquisition required. P03 dates2021-05-12–2023-12-29; P04 uses observed30min2024-09-26–2025-09-25. P01/stock P02 use2019; SPY P02/P05 can use their entire2016–2021 overlap. New later dates remain unexamined. All inspected dates are exploratory for these screens.\n\nRetained new-minute budget100MB, derivatives100MB, smallsources30MB, outputs/bundle80MB, cache20MB plus one raw monthly source of at most{largest:,} bytes; forecast peak{forecast['conservative_incremental_peak_forecast_bytes']:,} bytes. No old data removed. See JSON schemas, hashes, roster and resolved paths for exact references.\n'''
    (RUN/'reports/shared_data_inventory.md').write_text(report)
    stage_note(0,'No-download audit complete; source metadata and final contracts must freeze before any large acquisition. Current source draft and size forecast saved.')
    print('INVENTORY',len(protected),'legacy protected files; max monthly bytes',largest,flush=True)


def metadata():
    """Small metadata only; no monthly market Parquet, macro data or shock workbook."""
    dest=RUN/'manifests/remote_metadata';dest.mkdir(exist_ok=True)
    urls={
        'hf_minute_api.json':'https://huggingface.co/api/datasets/mito0o852/OHLCV-1m',
        'hf_etf_api.json':'https://huggingface.co/api/datasets/thecharttruth/etf-data',
        'frbsf.html':'https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/',
        'h15_about.html':'https://www.federalreserve.gov/releases/h15/about.htm',
        'h15_release.html':'https://www.federalreserve.gov/releases/h15/'}
    for name,url in urls.items():download(url,dest/name,2_000_000)
    minute=json.loads((dest/'hf_minute_api.json').read_text());assert minute['sha']==HF_REV
    etf=json.loads((dest/'hf_etf_api.json').read_text());rev=etf['sha']
    for name in ['LICENSE','README.md','manifest.json']:
        download(f'https://huggingface.co/datasets/thecharttruth/etf-data/resolve/{rev}/{name}',dest/('etf_'+name.replace('.','_')),1_000_000)
    html=(dest/'frbsf.html').read_text();links=re.findall(r'href=[\"\']([^\"\']+)[\"\']',html)
    files=[urljoin(urls['frbsf.html'],s) for s in links if '.xlsx' in s.lower() or '.csv' in s.lower()]
    write_json(dest/'frbsf_download_links.json',files)
    print('METADATA etree revision',rev,'FRBSF files',files,flush=True)


def freeze():
    """Coverage-only scientific decisions and source union frozen before any fit/response plot."""
    if (RUN/'manifests/frozen_configs.json').exists():raise FileExistsError('EXISTING_SCIENTIFIC_FREEZE')
    refs=json.loads((RUN/'manifests/source_registry_draft.json').read_text());meta=RUN/'manifests/remote_metadata'
    etf=json.loads((meta/'hf_etf_api.json').read_text());rev=etf['sha']
    refs['HF_ETF_DAILY'].update(revision=rev,status='FROZEN_PENDING_ACQUISITION',symbols=['SPY','IEF'],coverage=['2021-05-12','2025-09-25'],
        adjustment='Published daily OHLC; primary P03 open-to-close avoids unverifiable total-return treatment',rights=(meta/'etf_LICENSE').read_text())
    refs['FED_RATES'].update(status='FROZEN_PENDING_ACQUISITION',coverage=['2021-04-01','2023-12-29'],
        availability='Observation t treated available no earlier than17:00ET on next US federal business day; strict prior-to-open join; current vintage not a real-time revision archive')
    links=json.loads((meta/'frbsf_download_links.json').read_text())
    workbook=next(u for u in links if '.xlsx' in u.lower())
    refs['FED_SHOCKS'].update(status='FROZEN_PENDING_ACQUISITION',url=workbook,coverage=['2016-01-01','2021-12-31'],
        primary_selection='Raw surprises sheet/column verified from source workbook; never orthogonalized residuals; standard14:00FOMC only')
    write_json(RUN/'manifests/source_registry.json',refs,exclusive=True)
    months=json.loads((RUN/'manifests/hf_existing_metadata.json').read_text())['months']
    union=dict(dataset='mito0o852/OHLCV-1m',revision=HF_REV,months=months,union_symbols=['SPY']+STOCKS,
        acquire_symbols=refs['HF_MINUTE_A']['new_symbols'],reused_minute_symbols=['SPY','BAC','KO'],
        columns=['timestamp','ticker','open','high','low','close','volume'],regular_session_only=True,
        one_authoritative_copy='existing SPY/BAC/KO references plus eight new symbols per2019month; no mirror; raw monthly temp deleted after validation',
        date_rule='P01/stockP02 common2019; SPYP02/P05 all available2016–2021; P04 native observed30min separate era; no alignment by manufacturing data')
    write_json(RUN/'manifests/union_acquisition_plan.json',union,exclusive=True)
    cfgs={}
    for id in IDS:
        base=CONTRACTS[id];coverage={IDS[0]:['2019-01-01','2019-12-31'],IDS[1]:['2016-01-04','2021-12-31'],IDS[2]:['2021-05-12','2023-12-29'],IDS[3]:['2024-09-26','2025-09-25'],IDS[4]:['2016-01-01','2021-12-31']}[id]
        c=dict(experiment_id=id,protocol_version='prelim-v1',scientific_design_file=str(DESIGN.relative_to(ROOT)),scientific_design_sha256=sha(DESIGN),
            **base,instrument_ids=(['SPY','IEF'] if id==IDS[2] else STOCKS if id in [IDS[0],IDS[3]] else ['SPY']+STOCKS if id==IDS[1] else ['SPY']),
            session_timezone='America/New_York',storage_timezone='UTC',coverage=coverage,
            output_dir=str((RUN/'experiments'/id).relative_to(ROOT)),input_paths=[s for source in base['source_ids'] for s in refs[source].get('refs',[])],
            input_fingerprints={source:{r['path']:r['sha256'] for r in refs[source].get('refs',[])} for source in base['source_ids']},
            validated_new_input_manifest='manifests/validated_inputs.json; each immutable derived/source hash required immediately before screen',
            source_registry_sha256=sha(RUN/'manifests/source_registry.json'),union_sha256=sha(RUN/'manifests/union_acquisition_plan.json'),
            eligibility_rule='Complete ordinary390-minute sessions for RV/5m;13 genuine30min bars for stock daily; no leap over a missing target session; no fill/imputation',
            reference_period_end={IDS[0]:'2019-06-30',IDS[1]:'2019-12-31',IDS[2]:'2022-06-30',IDS[3]:'2025-03-31',IDS[4]:'2018-12-31'}[id],
            split_or_period_rule='All observed screen dates exploratory; half-period temporal sensitivity only; later dates outside coverage untouched',
            support=dict(min_state_days=30,min_bin_independent=10,min_events_per_sign=15,min_bin_events=6),
            bins=7,bootstrap=dict(method='circular scheduled-session blocks' if id!=IDS[4] else 'event pairs bootstrap',block_length=5,replicates=500,seed=20261022),
            contrast_definitions='high-minus-low slope; anchored response between fixed common-support x anchors; primary linear effect, curvature not tested',
            materiality={IDS[0]:.10,IDS[1]:.10,IDS[2]:.10,IDS[3]:.02,IDS[4]:1.0}[id],
            materiality_units='slope response units per predictor unit',
            x_anchors={IDS[0]:[-10,10],IDS[1]:[-11,-9],IDS[2]:[-100,0],IDS[3]:[-100,0],IDS[4]:[0,10]}[id],
            primary_raw_no_winsorization=True,sensitivity='exclude top1percent absolute focal x per date/event uniformly; period halves; no promotion based on outliers',
            adjusted_returns='Log price returns; no total-return claim',minute_RV_definition='389 adjacent genuine closes; no09:30open term; epsilon0, strictlypositiveRV only',
            p02_q_bins=[0,1/3,2/3,1],p02_lag_control='immediately preceding eligible scheduled session logRV',
            p04_volume_definition='log(volume today)-mean(logvolume previous20eligiblefullsessions), current excluded; per-stock reference-period terciles',
            p04_market_control='same-day SPY open-close log price return in bp; broad control, not stock target replacement',
            p05_zero_tolerance_bp=.01,p05_event_window='C14:29/C13:59 proxies14:30/14:00; preQA C13:59/C13:54; genuine6/31minutes required',
            notes='No EBM, ML, profit, causality or untouched validation claims; universe/years selected before response relationships')
        contract(c,id,source_registry=refs);path=RUN/'configs'/(id+'.json');write_json(path,c,exclusive=True);cfgs[id]=sha(path)
    write_json(RUN/'manifests/frozen_configs.json',cfgs,exclusive=True)
    (RUN/'reports/experiment_input_contract_matrix.md').write_text('# Five immutable input contracts\n\n'+pd.DataFrame([dict(experiment_id=id,**CONTRACTS[id]) for id in IDS]).to_markdown(index=False) if False else '# Five immutable input contracts\n\n'+json.dumps(CONTRACTS,indent=2)+'\n\nSHA registry: manifests/frozen_configs.json. Every source/target/state/horizon checked before each screen.\n')
    stage_note(0,'Scientific freeze COMPLETE. Exactly ten original-roster stocks;2019minute union; no response-dependent decisions. Metadata and all five configs hashed; acquisition authorized only by this frozen union.')
    print('FROZEN',cfgs,flush=True)


def acquire():
    from .sources import acquire_all
    acquire_all();stage_note(1,'One shared acquisition pass and small-source intake executed; see monthly ledger, source receipts, holds and storage trace.')


def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['inventory','metadata','freeze','acquire','derive','screen','report','verify']);a=p.parse_args()
    if a.phase in ['inventory','metadata','freeze','acquire']:globals()[a.phase]()
    elif a.phase=='derive':
        from .features import derive
        derive();stage_note(2,'Shared derivatives and feature QA completed; no downloads or EBM.')
    elif a.phase=='screen':
        from .statistics import screen
        screen();stage_note(3,'All five isolated screens or explicit DATA HOLD branches executed.')
    elif a.phase=='report':
        from .reporting import report
        report();stage_note(4,'Consolidated report, six reviewer images, sidecars, exact plot data and review ZIP produced.')
    else:
        from .reporting import verify
        verify()
    print(a.phase,'COMPLETE',flush=True)

if __name__=='__main__':main()
