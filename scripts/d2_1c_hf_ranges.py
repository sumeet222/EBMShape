"""Ticker-first row-group reads for remaining source1 months, under shared cap."""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import struct
import tempfile
import time

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from ebm_research.experiment_b.pilot import ROOT, ET, sha, write_json, timestamp


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month",choices=["2020-03","2021-05","2019-08","2016-02"],required=True)
    month=parser.parse_args().month
    cp=ROOT/"config/D2_1c_hf_source1.json"
    c=json.loads(cp.read_text())
    root=Path(os.environ.get("EBM_DATA_ROOT",ROOT/"data")).expanduser().resolve()
    mp=ROOT/f"data/registry/D2_1c_source1_{month}.json"
    output=root/f"raw/diagnostics/D2_1c_source1_{month}_SPY_context.parquet"
    if mp.exists() or output.exists():raise FileExistsError("Source1 month already inspected; reuse evidence")
    old=[json.loads(p.read_text()) for p in (ROOT/"data/registry").glob("D2_1c_source1_????-??.json")]
    used=c["prior_task_body_bytes"]+sum(r["downloaded_body_bytes"] for r in old)
    probe=runpy.run_path(str(ROOT/"scripts/d2_1_hf_inspect.py"))["Probe"]({**c,"max_network_bytes":c["max_network_bytes"]-used})
    uri=f"https://huggingface.co/datasets/{c['candidate_repository']}/resolve/{c['revision']}/data/ohlcv_{month}.parquet"
    result={"at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"repository":c["candidate_repository"],"revision":c["revision"],"month":month,"uri":uri,"script_sha256":sha(Path(__file__)),"config_sha256":sha(cp),"previous_repair_body_bytes":used,"license":"Undeclared; explicit private source1 inspection only, no publication or source-fidelity claim"}
    temp=None
    try:
        trailer=probe.get(uri,"bytes=-8")
        if trailer is None or len(trailer)!=8 or trailer[-4:]!=b"PAR1":raise ValueError("Invalid footer trailer")
        size=int(probe.events[-1]["content_range"].split('/')[-1]); n=struct.unpack('<I',trailer[:4])[0]
        footer=probe.get(uri,f"bytes={size-n-8}-{size-9}")
        metadata=pq.read_metadata(io.BytesIO(b"PAR1"+footer+trailer))
        result.update(remote_file_bytes=size,footer_sha256=hashlib.sha256(footer).hexdigest(),row_groups=metadata.num_row_groups)
        cache=root/'cache';cache.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='D2_1c_range_',dir=cache) as folder:
            temp=Path(folder)/f'ohlcv_{month}_sparse.parquet'
            result['temporary_path']=temp.relative_to(root).as_posix()
            with temp.open('w+b') as f:
                f.truncate(size);f.write(b'PAR1');f.seek(size-n-8);f.write(footer+trailer)
            groups=[];all_chunks={}
            for i in range(metadata.num_row_groups):
                columns={}
                group=metadata.row_group(i)
                for j in range(group.num_columns):
                    col=group.column(j);offset=min(v for v in [col.dictionary_page_offset,col.data_page_offset] if v is not None and v>0)
                    columns[col.path_in_schema]={'start':offset,'bytes':col.total_compressed_size}
                all_chunks[i]=columns;col=columns['ticker'];end=col['start']+col['bytes']-1
                body=probe.get(uri,f"bytes={col['start']}-{end}")
                if body is None or probe.events[-1]['content_range']!=f"bytes {col['start']}-{end}/{size}":raise ValueError('Ticker range mismatch')
                with temp.open('r+b') as f:f.seek(col['start']);f.write(body)
                with pq.ParquetFile(temp) as reader:tickers=reader.read_row_group(i,columns=['ticker'])
                count=pc.sum(pc.cast(pc.equal(tickers['ticker'],'SPY'),pa.int64())).as_py()
                if count:groups.append({'row_group':i,'SPY_rows':count})
            price_cost=sum(col['bytes'] for g in groups for name,col in all_chunks[g['row_group']].items() if name!='ticker')
            result.update(SPY_row_groups=groups,projected_additional_price_bytes=price_cost)
            if used+probe.bytes+price_cost>c['max_network_bytes']:raise RuntimeError('NOT ECONOMICALLY FEASIBLE: selected price chunks exceed remaining500MB')
            if price_cost+probe.bytes>150000000:raise RuntimeError('NOT ECONOMICALLY FEASIBLE: sparse allocation projection exceeds150MB')
            wanted=set()
            for r in csv.DictReader((root/'registry/D2_spy_missing_candles.csv').open()):
                if r['session_et'].startswith(month):
                    t=timestamp(r['timestamp_utc']);wanted.update(t+dt.timedelta(minutes=i) for i in range(-20,21))
            if month=='2019-08':wanted.update(dt.datetime(2019,8,12,14,m,tzinfo=ET).astimezone(dt.timezone.utc) for m in range(35,55))
            kept=[]
            for g in groups:
                i=g['row_group']
                for name,col in all_chunks[i].items():
                    if name=='ticker':continue
                    end=col['start']+col['bytes']-1;body=probe.get(uri,f"bytes={col['start']}-{end}")
                    if body is None or probe.events[-1]['content_range']!=f"bytes {col['start']}-{end}/{size}":raise ValueError('Price range mismatch')
                    with temp.open('r+b') as f:f.seek(col['start']);f.write(body)
                with pq.ParquetFile(temp) as reader:table=reader.read_row_group(i)
                table=table.filter(pc.equal(table['ticker'],'SPY'))
                field=table.schema.field('timestamp')
                if field.type.tz!='UTC':raise ValueError('Expected aware UTC source1 timestamp')
                kept.append(table.filter(pc.is_in(table['timestamp'],value_set=pa.array(sorted(wanted),type=field.type))))
            if not kept:raise ValueError('No SPY rows found')
            selected=pa.concat_tables(kept).sort_by('timestamp')
            output.parent.mkdir(parents=True,exist_ok=True);pq.write_table(selected,output,compression='zstd')
            result.update(status='EXTRACTED',temporary_logical_bytes=temp.stat().st_size,temporary_allocated_bytes=getattr(temp.stat(),'st_blocks',0)*512,extract={'path':output.relative_to(root).as_posix(),'rows':selected.num_rows,'bytes':output.stat().st_size,'sha256':sha(output)})
    except Exception as error:result.update(status='FAILED',error={'type':type(error).__name__,'detail':str(error)[:250]})
    finally:
        result.update(requests=probe.events,downloaded_body_bytes=probe.bytes,cumulative_repair_body_bytes=used+probe.bytes,temporary_deleted=temp is None or not temp.exists(),wall_seconds=time.monotonic()-probe.started,cpu_seconds=time.process_time()-probe.cpu_started)
        write_json(mp,result)
    print(json.dumps({k:result.get(k) for k in ['month','status','error','extract','SPY_row_groups','downloaded_body_bytes','cumulative_repair_body_bytes','temporary_deleted']}))
    if result['status']=='FAILED':raise SystemExit(1)


if __name__=='__main__':main()
