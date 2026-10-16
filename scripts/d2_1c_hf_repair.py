"""Audit all five source1 extracts and publish a native-price optional delta.

Original Alpaca and previous alternate-source repair remain immutable. This
manifest selects source1 alone for its accepted missing keys, not both repairs.
"""
from collections import Counter
import csv
import datetime as dt
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import runpy
import time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from ebm_research.experiment_b.acquisition import verify_files
from ebm_research.experiment_b.pilot import ROOT, ET, sha, write_json, csv_write
from ebm_research.experiment_b.repair import load_minutes


def main():
    started,cpu_started=time.monotonic(),time.process_time()
    cp=ROOT/'config/D2_1c_hf_source1.json';c=json.loads(cp.read_text())
    root=Path(os.environ.get('EBM_DATA_ROOT',ROOT/'data')).expanduser().resolve()
    mp=ROOT/'data/registry/D2_1c_hf_repair_manifest.json'
    dest=root/f"patches/B/{c['repair_id']}.parquet"
    if mp.exists() or dest.exists():raise FileExistsError('Source1 repair already exists; reuse it')
    bp=root/'registry/D2_spy_source_manifest.json';baseline=json.loads(bp.read_text())
    refs=[r for b in baseline['blocks'].values() for r in [b['canonical'],b['qa']]]+baseline['published_quality_files']+[baseline['request_ledger']]
    verify_files(root,refs)
    read_csv=lambda name:list(csv.DictReader((root/'registry'/name).open()))
    missing=read_csv('D2_spy_missing_candles.csv');gaps=read_csv('D2_spy_candle_gap_clusters.csv')
    evidence=[json.loads(p.read_text()) for p in sorted((ROOT/'data/registry').glob('D2_1c_source1_????-??.json'))]
    if len(evidence)!=5 or any(e['status']!='EXTRACTED' or not e['temporary_deleted'] for e in evidence):raise ValueError('Five completed clean extracts required')
    by_month={e['month']:e for e in evidence}
    parts=[]
    for e in evidence:
        ref=e['extract'];p=root/ref['path']
        if sha(p)!=ref['sha256']:raise ValueError('Source1 context checksum conflict')
        frame=pd.read_parquet(p).rename(columns={'timestamp':'key',**{n:n.capitalize() for n in ['open','high','low','close','volume']}})
        if not frame.ticker.eq('SPY').all() or frame.key.duplicated().any():raise ValueError('Source1 symbol/duplicate conflict')
        parts.append(frame)
    hf=pd.concat(parts,ignore_index=True).sort_values('key')
    original=load_minutes(root)
    extra=pd.read_parquet(root/'raw/diagnostics/D2_1b_alpaca_neighbors.parquet')
    reference=pd.concat([original,extra],ignore_index=True)
    if reference.duplicated(['symbol','timestamp_utc']).any():raise ValueError('Reference-key collision')
    functions=runpy.run_path(str(ROOT/'scripts/d2_1b_hf_compare.py'))
    diagnostics=functions['discrepancies'];ratios=functions['calibration_factor']
    rows=[];comparisons=[];timing=[]
    for g in gaps:
        day=g['session_et'];start,end=pd.Timestamp(g['start_utc']),pd.Timestamp(g['end_utc'])
        low=max(start-pd.Timedelta(minutes=20),pd.Timestamp(day+'T09:30',tz=ET).tz_convert('UTC'))
        high=min(end+pd.Timedelta(minutes=20),pd.Timestamp(day+'T15:59',tz=ET).tz_convert('UTC'))
        separated=(hf.key>=pd.Timestamp(day+'T14:35',tz=ET).tz_convert('UTC'))&(hf.key<=pd.Timestamp(day+'T14:54',tz=ET).tz_convert('UTC')) if day=='2019-08-12' else pd.Series(False,index=hf.index)
        local=hf[((hf.key>=low)&(hf.key<=high))|separated].copy()
        j=local.merge(reference,left_on='key',right_on='timestamp_utc')
        native=diagnostics(j,1.)
        first=min(pd.Timestamp(x['start_utc']) for x in gaps if x['session_et']==day)
        all_join=hf.merge(reference,left_on='key',right_on='timestamp_utc')
        pre=all_join[(all_join.key>=first-pd.Timedelta(minutes=20))&(all_join.key<first)]
        independent=j[~j.key.isin(pre.key)]
        validation=diagnostics(independent,1.)
        estimated_ratio=ratios(pre,c['minimum_neighboring_closes'])
        proposed=hf[(hf.key>=start)&(hf.key<=end)]
        prices=proposed[['Open','High','Low','Close','Volume']]
        valid=np.isfinite(prices).all(axis=1)&proposed[['Open','High','Low','Close']].gt(0).all(axis=1)&proposed.Volume.gt(0)&proposed.High.ge(proposed[['Open','Close','Low']].max(axis=1))&proposed.Low.le(proposed[['Open','Close','High']].min(axis=1))
        screen=bool(len(proposed) and valid.all() and len(pre)>=10 and len(independent)>=10 and native.get('close_median_bp',float('inf'))<=c['median_absolute_level_bp_max'] and native.get('close_p95_bp',float('inf'))<=c['p95_absolute_level_bp_max'] and native.get('return_p95_bp') is not None and native['return_p95_bp']<=c['p95_absolute_log_return_difference_bp_max'] and all(native[k+'_p95_bp']<=5 for k in ['open','high','low']))
        for shift in [-1,0,1]:
            shifted=local.copy();shifted['key']=shifted.key+pd.Timedelta(minutes=shift)
            timing.append({'session_et':day,'start_utc':g['start_utc'],'shift_minutes':shift,'metrics':diagnostics(shifted.merge(reference,left_on='key',right_on='timestamp_utc'))})
        comparisons.append({**g,'candidate_rows':len(proposed),'invalid_candidate_rows':int((~valid).sum()),'pregap_matches':len(pre),'independent_matches':len(independent),'native_metrics':native,'independent_metrics':validation,'diagnostic_pregap_ratio_only':estimated_ratio,'applied_factor':1.,'accepted_rows':len(proposed) if screen else 0,'status':'ACCEPTED_NATIVE_PRICE' if screen else ('UNAVAILABLE' if not len(proposed) else 'REJECTED_LOCAL_SCREEN'),'one_sided_terminal':g['end_et'][11:16]=='15:59'})
        if not screen:continue
        e=by_month[day[:7]]
        for _,r in proposed.iterrows():
            rows.append({'symbol':'SPY','timestamp_utc':r.key.to_pydatetime(),'session_et':r.key.tz_convert(ET).date(),**{k:float(r[k.capitalize()]) for k in ['open','high','low','close']},'volume':float(r.Volume),'trade_count':float('nan'),'vwap':float('nan'),'source_batch':'D2_1c_'+day[:7],'role':'repair_missing_minute','source_provider':'huggingface:mito0o852/OHLCV-1m','source_origin':'Finnhub claimed by uploader; not independently verified','is_repaired':True,'repair_id':c['repair_id'],'source_revision':c['revision'],'source_uri':e['uri'],'source_row_group':';'.join(str(x['row_group']) for x in e['SPY_row_groups']),'source_hash':e['extract']['sha256'],'source_hash_kind':'retained_context_parquet_sha256','source_range_manifest_sha256':sha(ROOT/f"data/registry/D2_1c_source1_{day[:7]}.json"),'source_adjustment':'native archive basis locally compatible with SIP split; vendor adjustment unspecified','adjustment_method':'none_native_prices_pass_local_screen','adjustment_factor':1.,'calibration_rows':0,'scale_ratio_variance':native['scale_ratio_variance'],'timestamp_method':'native UTC bar start; zero minute shift verified locally','validation_status':'ACCEPTED_LOCAL_ALIGNMENT','one_sided_terminal_gap':g['end_et'][11:16]=='15:59'})
    patch=pd.DataFrame(rows).sort_values('timestamp_utc')
    if len(patch)!=39 or patch.duplicated(['symbol','timestamp_utc']).any():raise ValueError('Unexpected source1 accepted-key result; inspect before publication')
    allowed={pd.Timestamp(r['timestamp_utc']) for r in missing}
    accepted=set(patch.timestamp_utc)
    if not accepted.issubset(allowed) or any(t.year>=2024 for t in accepted):raise ValueError('Nonmissing/test source1 key')
    dest.parent.mkdir(parents=True,exist_ok=True);pq.write_table(pa.Table.from_pandas(patch,preserve_index=False),dest,compression='zstd')
    remaining=[r for r in missing if pd.Timestamp(r['timestamp_utc']) not in accepted]
    group_fn=runpy.run_path(str(ROOT/'scripts/d2_1_hf_audit.py'))['clusters'];groups=group_fn(remaining)
    decision_rows=[{**r,'accepted':pd.Timestamp(r['timestamp_utc']) in accepted,'provider':c['candidate_repository'],'status':next(g['status'] for g in comparisons if g['session_et']==r['session_et'] and g['start_utc']<=r['timestamp_utc']<=g['end_utc'])} for r in missing]
    csv_write(ROOT/'data/registry/D2_1c_hf_repair_decisions.csv',decision_rows,list(decision_rows[0]))
    csv_write(ROOT/'data/registry/D2_1c_hf_remaining_candles.csv',remaining,list(missing[0]))
    write_json(ROOT/'data/registry/D2_1c_hf_comparisons.json',{'clusters':comparisons,'timing_hypotheses':timing,'script_sha256':sha(Path(__file__))})
    manifest={'dataset_id':c['repair_id'],'status':'PARTIAL','baseline_manifest_sha256':sha(bp),'baseline_files':refs,'patch':{'path':dest.relative_to(root).as_posix(),'rows':len(patch),'bytes':dest.stat().st_size,'sha256':sha(dest)},'source_definition':'Immutable Alpaca D2 UNION39 source1-native missing rows; optional alternative to previous39-row pitrading view, never union both repair versions','native_factor':1.,'license':'Undeclared/unverified source1 license and upstream rights; explicit user-directed private use, no raw publication or exact source-fidelity claim','remaining_minutes':len(remaining),'remaining_clusters':[{**g[0],'last_timestamp_utc':g[-1]['timestamp_utc'],'length':len(g)} for g in groups],'previous_optional_manifest':'registry/D2_1b_hf_repair_manifest.json','previous_optional_patch_unchanged':json.loads((ROOT/'data/registry/D2_1b_hf_repair_manifest.json').read_text())['patch'],'resources':{'new_http_body_bytes':sum(e['downloaded_body_bytes'] for e in evidence),'prior_repair_body_bytes':c['prior_task_body_bytes'],'cumulative_repair_body_bytes':c['prior_task_body_bytes']+sum(e['downloaded_body_bytes'] for e in evidence),'all_source_temps_deleted':all(e['temporary_deleted'] for e in evidence),'acquisition_wall_seconds':sum(e['wall_seconds'] for e in evidence),'acquisition_cpu_seconds':sum(e['cpu_seconds'] for e in evidence),'largest_temporary_logical_bytes':max(e['temporary_logical_bytes'] for e in evidence),'largest_temporary_allocated_bytes':max(e['temporary_allocated_bytes'] for e in evidence)},'source_evidence':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted((ROOT/'data/registry').glob('D2_1c_source1_????-??.json'))],'config_sha256':sha(cp),'scripts':[{'path':s,'sha256':sha(ROOT/s)} for s in ['scripts/d2_1c_hf_source1.py','scripts/d2_1c_hf_ranges.py','scripts/d2_1c_hf_repair.py']],'environment':{'python':platform.python_version(),**{p:importlib.metadata.version(p) for p in ['numpy','pandas','pyarrow','exchange-calendars']}}}
    write_json(mp,manifest)
    once=load_minutes(root,mp);twice=load_minutes(root,mp);pd.testing.assert_frame_equal(once,twice)
    cols=['symbol','timestamp_utc','session_et','open','high','low','close','volume','trade_count','vwap','source_batch','role']
    pd.testing.assert_frame_equal(original[cols].reset_index(drop=True),once.loc[~once.is_repaired,cols].reset_index(drop=True))
    keys=set(zip(once.symbol,once.timestamp_utc));sessions=read_csv('D2_spy_candle_qa_sessions.csv');full=[r for r in sessions if r['session_type']=='full']
    def key(day,h,m):return ('SPY',pd.Timestamp(dt.datetime.combine(dt.date.fromisoformat(day),dt.time(h,m)),tz=ET).tz_convert('UTC'))
    records=[]
    for r in full:
        day=r['session_et'];opening=all(key(day,9,i) in keys for i in range(30,60));required=opening and key(day,14,59) in keys and all(key(day,15,i) in keys for i in range(60));prior=key(r['prior_full_session'],15,59) in keys
        records.append({'day':day,'opening':opening,'required':required,'prior':prior,'eligible':required and prior,'anchor1529':key(day,15,29) in keys,'anchor1559':key(day,15,59) in keys})
    remaining_by_day=Counter(r['session_et'] for r in remaining)
    totals={'primary_eligible':sum(r['eligible'] for r in records),'train_eligible':sum(r['eligible'] and r['day']<'2022-01-01' for r in records),'validation_eligible':sum(r['eligible'] and '2022-01-01'<=r['day']<'2024-01-01' for r in records),'sealed_test_eligible':sum(r['eligible'] and r['day']>='2024-01-01' for r in records),'opening_complete':sum(r['opening'] for r in records),'required_complete':sum(r['required'] for r in records),'prior_anchor_valid':sum(r['prior'] for r in records),'anchor1529_valid':sum(r['anchor1529'] for r in records),'anchor1559_valid':sum(r['anchor1559'] for r in records),'full_session_complete':sum(remaining_by_day[r['session_et']]==0 for r in full),'early_close_excluded':len(sessions)-len(full),'original_rows':len(original),'view_rows':len(once),'patch_rows':len(patch),'missing_minutes':len(remaining),'missing_clusters':len(groups)}
    if totals['primary_eligible']!=2675 or len(once)!=243843:raise ValueError('Source1 view mechanical QA mismatch')
    verify_files(root,refs)
    manifest.update(totals=totals,qa={'loader_twice_identical':True,'all_original_columns_unchanged':True,'original_registered_files_unchanged':len(refs),'test_patch_rows':int((patch.timestamp_utc.dt.year>=2024).sum()),'patch_trade_count_vwap_null':bool(patch.trade_count.isna().all() and patch.vwap.isna().all())},publish_wall_seconds=time.monotonic()-started,publish_cpu_seconds=time.process_time()-cpu_started)
    write_json(mp,manifest)
    print(json.dumps({'patch':manifest['patch'],'totals':totals,'resources':manifest['resources'],'qa':manifest['qa']},indent=2))


if __name__=='__main__':main()
