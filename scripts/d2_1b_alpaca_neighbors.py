"""Three isolated SIP/split neighbor requests absent from retained D2 windows."""
import datetime as dt
import json
import os
from pathlib import Path
import time

import pyarrow as pa
import pyarrow.parquet as pq

from ebm_research.experiment_b.acquisition import record, SCHEMA
from ebm_research.experiment_b.pilot import ROOT, ET, UTC, Client, credentials, sha, write_json


def main():
    started = time.monotonic()
    # Existing local credentials are loaded privately, never printed or copied.
    for line in (ROOT / ".env").read_text().splitlines():
        s = line.strip()
        if s and not s.startswith("#") and "=" in s:
            key, value = s.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip(chr(34)+chr(39)))
    root = Path(os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    path = root / "raw/diagnostics/D2_1b_alpaca_neighbors.parquet"
    manifest_path = ROOT / "data/registry/D2_1b_alpaca_neighbors.json"
    if path.exists() or manifest_path.exists():
        raise FileExistsError("Neighbor evidence exists; reuse it")
    headers = credentials()
    client = Client(root / "raw/diagnostics/D2_1b_alpaca_ledger", {"request_spacing_seconds": .5, "max_pages_per_request": 1})
    ledger = client.raw_dir / "requests.json"
    if ledger.exists():
        client.lineage = json.loads(ledger.read_text())
    intervals = [("2016-02-02", "10:59", "11:47"), ("2019-08-12", "14:35", "14:54"), ("2023-06-05", "10:00", "10:15")]
    result = {"source": "Alpaca SIP split diagnostic neighbors only", "script_sha256": sha(Path(__file__)), "started_at_utc": dt.datetime.now(UTC).isoformat(), "intervals_et": intervals}
    rows = []
    try:
        for day, begin, end in intervals:
            start = dt.datetime.fromisoformat(day+"T"+begin).replace(tzinfo=ET).astimezone(UTC)
            finish = dt.datetime.fromisoformat(day+"T"+end).replace(tzinfo=ET).astimezone(UTC)
            bars = client.alpaca("D2_1b_neighbors_"+day, start, finish, headers)
            rows.extend(record(b, "D2_1b_neighbors_"+day, "diagnostic_neighbor") for b in bars)
        path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(pa.Table.from_pylist(rows, schema=SCHEMA), path, compression="zstd")
        result.update(status="COMPLETE", output={"path":path.relative_to(root).as_posix(),"rows":len(rows),"bytes":path.stat().st_size,"sha256":sha(path)})
    except Exception as error:
        result.update(status="FAILED",error={"type":type(error).__name__})
    finally:
        result.update(requests=client.lineage, wall_seconds=time.monotonic()-started)
        write_json(manifest_path,result)
    print(json.dumps({k:result.get(k) for k in ["status","error","output","wall_seconds"]}))
    if result["status"]=="FAILED":raise SystemExit(1)


if __name__=="__main__":
    main()
