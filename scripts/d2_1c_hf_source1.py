"""One explicitly authorized monthly HF file; retain only SPY gap context.

Full source bytes are streamed to one temporary file and SHA-256 hashed. The
file is always removed after extraction. No datasets cache or archive clone.
"""
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import tempfile
import time
import urllib.request

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from ebm_research.experiment_b.pilot import ROOT, sha, write_json, timestamp


def main():
    started, cpu_started = time.monotonic(), time.process_time()
    cp = ROOT / "config/D2_1c_hf_source1.json"
    c = json.loads(cp.read_text())
    root = Path(os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    out = root / "raw/diagnostics/D2_1c_source1_2023-06_SPY_context.parquet"
    mp = ROOT / "data/registry/D2_1c_source1_2023-06.json"
    if out.exists() or mp.exists():
        raise FileExistsError("Source1 evidence already exists; reuse rather than re-download")
    prior = json.loads((ROOT / "data/registry/D2_1_hf_candidate_1.json").read_text())["footer_inspection"]
    size = prior["remote_bytes"]
    if size+c["prior_task_body_bytes"] > c["max_network_bytes"] or size > c["max_temporary_disk_bytes"]:
        raise ValueError("Explicit transfer or temporary-file budget exceeded before download")
    if shutil.disk_usage(root).free < 2*size:
        raise ValueError("Insufficient disk for one authorized temporary file")
    uri = f"https://huggingface.co/datasets/{c['candidate_repository']}/resolve/{c['revision']}/{c['remote_path']}?download=true"
    result = {"at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"repository":c["candidate_repository"],"revision":c["revision"],"uri":uri,"month":"2023-06","expected_file_bytes":size,"downloaded_body_bytes":0,"prior_repair_body_bytes":c["prior_task_body_bytes"],"config_sha256":sha(cp),"script_sha256":sha(Path(__file__)),"python":platform.python_version(),"license":"Not declared/verified; explicit user-directed private source inspection; no publication or source-fidelity claim"}
    temp = None
    try:
        cache = root / "cache"
        cache.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="D2_1c_",dir=cache) as folder:
            temp = Path(folder)/"ohlcv_2023-06.parquet"
            result["temporary_path"] = temp.relative_to(root).as_posix()
            request = urllib.request.Request(uri,headers={"User-Agent":"EBMShape-bounded-source1-recovery","Accept-Encoding":"identity"})
            digest = hashlib.sha256()
            with urllib.request.urlopen(request,timeout=30) as response, temp.open("wb") as f:
                result.update(http_status=response.status,content_length=response.headers.get("Content-Length"))
                if response.status != 200:
                    raise ValueError("Expected full-object HTTP200, not a cached range")
                last_progress = 0
                while True:
                    if time.monotonic()-started > c["max_acquisition_seconds"]:
                        raise RuntimeError("Purposeful acquisition time cap exceeded")
                    body = response.read(min(1048576,size-result["downloaded_body_bytes"]+1))
                    if not body:
                        break
                    result["downloaded_body_bytes"] += len(body)
                    if result["downloaded_body_bytes"] > size:
                        raise ValueError("Source larger than frozen remote size; stop")
                    f.write(body); digest.update(body)
                    if result["downloaded_body_bytes"]-last_progress >= 64000000:
                        print(json.dumps({"downloaded_MB":round(result["downloaded_body_bytes"]/1e6,2),"elapsed_seconds":round(time.monotonic()-started,2)}),flush=True)
                        last_progress = result["downloaded_body_bytes"]
            if result["downloaded_body_bytes"] != size:
                raise ValueError("Incomplete monthly object; no extraction accepted")
            result.update(source_file_sha256=digest.hexdigest(),temporary_logical_bytes=temp.stat().st_size,temporary_allocated_bytes=getattr(temp.stat(),"st_blocks",0)*512)
            reader = pq.ParquetFile(temp)
            needed = set()
            for r in csv.DictReader((root/"registry/D2_spy_missing_candles.csv").open()):
                if r["session_et"].startswith("2023-06"):
                    t = timestamp(r["timestamp_utc"])
                    needed.update(t+dt.timedelta(minutes=i) for i in range(-20,21))
            kept, groups = [], []
            spy_total = 0
            for i in range(reader.num_row_groups):
                tickers = reader.read_row_group(i,columns=["ticker"])
                count = pc.sum(pc.cast(pc.equal(tickers["ticker"],"SPY"),pa.int64())).as_py()
                if not count:
                    continue
                spy_total += count
                groups.append({"row_group":i,"SPY_rows":count})
                table = reader.read_row_group(i)
                table = table.filter(pc.equal(table["ticker"],"SPY"))
                field = table.schema.field("timestamp")
                if not pa.types.is_timestamp(field.type) or field.type.tz != "UTC":
                    raise ValueError("Unexpected source1 timestamp semantics")
                wanted = pa.array(sorted(needed),type=field.type)
                kept.append(table.filter(pc.is_in(table["timestamp"],value_set=wanted)))
            if not kept:
                raise ValueError("SPY absent; no repair possible from this file")
            selected = pa.concat_tables(kept).sort_by("timestamp")
            out.parent.mkdir(parents=True,exist_ok=True)
            pq.write_table(selected,out,compression="zstd")
            result.update(status="EXTRACTED",source_rows=reader.metadata.num_rows,source_row_groups=reader.num_row_groups,SPY_rows_in_month=spy_total,SPY_row_groups=groups,extract={"path":out.relative_to(root).as_posix(),"rows":selected.num_rows,"bytes":out.stat().st_size,"sha256":sha(out),"schema":str(selected.schema)})
        result["temporary_deleted"] = True
    except Exception as error:
        result.update(status="FAILED",error={"type":type(error).__name__,"detail":str(error)[:250]})
    finally:
        result.update(temporary_deleted=temp is None or not temp.exists(),cumulative_repair_body_bytes=c["prior_task_body_bytes"]+result["downloaded_body_bytes"],wall_seconds=time.monotonic()-started,cpu_seconds=time.process_time()-cpu_started,free_disk_bytes=shutil.disk_usage(root).free)
        write_json(mp,result)
    print(json.dumps({k:result.get(k) for k in ["status","error","extract","SPY_rows_in_month","SPY_row_groups","downloaded_body_bytes","cumulative_repair_body_bytes","temporary_deleted"]}),flush=True)
    if result["status"]=="FAILED":raise SystemExit(1)


if __name__=="__main__":
    main()
