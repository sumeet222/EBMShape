"""Fetch only one SPY row group's column chunks, retain local gap context.

The temporary sparse Parquet is deleted even on failure. Its unfetched ranges
are never read. Output retains naive vendor timestamps, not asserted UTC bars.
Public MIT-declared source is used only for private source-quality diagnostics.
"""
import csv
import datetime as dt
import importlib.metadata
import io
import json
import os
from pathlib import Path
import platform
import runpy
import shutil
import struct
import tempfile
import time

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from ebm_research.experiment_b.acquisition import verify_files
from ebm_research.experiment_b.pilot import ROOT, sha, write_json


def context_keys(missing, minutes):
    """Keep both declared-UTC and plausible local-clock hypotheses for diagnosis."""
    keys = set()
    for row in missing:
        for field in ["timestamp_et", "timestamp_utc"]:
            t = dt.datetime.fromisoformat(row[field]).replace(tzinfo=None)
            keys.update(t + dt.timedelta(minutes=i) for i in range(-minutes, minutes+1))
    # Terminal close gap needs separated same-session overlap, not fictitious right bars.
    for hour in [14, 18]:
        keys.update(dt.datetime(2019, 8, 12, hour, minute) for minute in range(35, 55))
    return keys


def main():
    started, cpu_started = time.monotonic(), time.process_time()
    config_path = ROOT / "config/D2_1b_hf_diagnostic.json"
    c = json.loads(config_path.read_text())
    root = Path(os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    output = root / "raw/diagnostics/D2_1b_hf_SPY_gap_context.parquet"
    manifest_path = ROOT / "data/registry/D2_1b_hf_extraction.json"
    if output.exists() or manifest_path.exists():
        raise FileExistsError("D2.1b output already exists; reuse manifest, do not re-download")
    original = json.loads((root / "registry/D2_spy_source_manifest.json").read_text())
    verify_files(root, [b["canonical"] for b in original["blocks"].values()])
    probe_class = runpy.run_path(str(ROOT / "scripts/d2_1_hf_inspect.py"))["Probe"]
    probe = probe_class({**c, "max_network_bytes": c["max_network_bytes"]-c["prior_task_body_bytes"]})
    uri = f"https://huggingface.co/datasets/{c['candidate_repository']}/resolve/{c['revision']}/{c['remote_path']}"
    result = {"observed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "repository": c["candidate_repository"], "revision": c["revision"], "remote_uri": uri, "declared_license": "mit", "diagnostic_only": True, "config_sha256": sha(config_path), "script_sha256": sha(Path(__file__)), "python": platform.python_version(), "pyarrow": importlib.metadata.version("pyarrow"), "auth": "anonymous public HF; no token", "baseline_manifest_sha256": sha(root / "registry/D2_spy_source_manifest.json")}
    temporary = None
    try:
        trailer = probe.get(uri, "bytes=-8")
        if trailer is None or len(trailer) != 8 or trailer[-4:] != b"PAR1":
            raise ValueError("Invalid Parquet trailer")
        footer_bytes = struct.unpack("<I", trailer[:4])[0]
        size = int(probe.events[-1]["content_range"].split("/")[-1])
        if size > c["max_temporary_disk_bytes"]:
            raise ValueError("Sparse temporary logical size exceeds150MB cap")
        footer_start = size-footer_bytes-8
        footer = probe.get(uri, f"bytes={footer_start}-{size-9}")
        metadata = pq.read_metadata(io.BytesIO(b"PAR1"+footer+trailer))
        group = metadata.row_group(c["row_group"])
        chunks = []
        for i in range(group.num_columns):
            col = group.column(i)
            offsets = [v for v in [col.dictionary_page_offset, col.data_page_offset] if v is not None and v > 0]
            chunks.append({"column": col.path_in_schema, "start": min(offsets), "bytes": col.total_compressed_size})
        estimated = sum(ch["bytes"] for ch in chunks)
        result.update(remote_bytes=size, row_group=c["row_group"], row_group_rows=group.num_rows, projected_column_bytes=estimated, chunks=chunks)
        if estimated + probe.bytes + c["prior_task_body_bytes"] > c["max_network_bytes"]:
            raise ValueError("Projected total exceeds approved500MB")
        cache = root / "cache"
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="D2_1b_", dir=cache) as folder:
            temporary = Path(folder) / "selected_row_group.parquet"
            result["temporary_path"] = temporary.relative_to(root).as_posix()
            with temporary.open("w+b") as f:
                f.truncate(size)
                f.seek(0); f.write(b"PAR1")
                f.seek(footer_start); f.write(footer+trailer)
                for chunk in chunks:
                    end = chunk["start"]+chunk["bytes"]-1
                    body = probe.get(uri, f"bytes={chunk['start']}-{end}")
                    event = probe.events[-1]
                    if body is None or event["content_range"] != f"bytes {chunk['start']}-{end}/{size}":
                        raise ValueError("Wrong/absent column chunk response")
                    f.seek(chunk["start"]); f.write(body)
                f.flush()
            result["temporary_logical_bytes"] = temporary.stat().st_size
            result["temporary_allocated_bytes"] = getattr(temporary.stat(), "st_blocks", 0)*512
            # Read only the populated group; unrelated row groups remain sparse.
            table = pq.ParquetFile(temporary).read_row_group(c["row_group"])
            frame = table.to_pandas()
            if set(frame) != {"datetime", "Open", "High", "Low", "Close", "Volume", "source"}:
                raise ValueError("Unexpected candidate schema")
            missing = list(csv.DictReader((root / "registry/D2_spy_missing_candles.csv").open()))
            wanted = context_keys(missing, c["retained_context_minutes"])
            selected = frame.loc[frame["datetime"].isin(wanted)].sort_values("datetime")
            output.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(pa.Table.from_pandas(selected, preserve_index=False), output, compression="zstd")
            result["extract"] = {"path": output.relative_to(root).as_posix(), "rows": len(selected), "bytes": output.stat().st_size, "sha256": sha(output), "columns": list(selected), "timestamp_semantics": "original naive candidate datetime; no localization performed", "source_counts": selected["source"].value_counts().to_dict(), "rows_by_naive_date": selected["datetime"].dt.strftime("%Y-%m-%d").value_counts().to_dict(), "duplicate_naive_timestamps": int(selected["datetime"].duplicated().sum())}
        result["status"] = "EXTRACTED_DIAGNOSTIC_ONLY"
    except Exception as error:
        result["status"] = "FAILED"
        result["error"] = {"type": type(error).__name__, "detail": str(error)[:300]}
    finally:
        result.update(requests=probe.events, downloaded_body_bytes=probe.bytes, prior_task_body_bytes=c["prior_task_body_bytes"], total_task_body_bytes=c["prior_task_body_bytes"]+probe.bytes, wall_seconds=time.monotonic()-started, cpu_seconds=time.process_time()-cpu_started, temporary_deleted=temporary is None or not temporary.exists(), free_disk_bytes=shutil.disk_usage(root).free)
        write_json(manifest_path, result)
    print(json.dumps({k: result.get(k) for k in ["status", "error", "extract", "downloaded_body_bytes", "temporary_deleted"]}))
    if result["status"] == "FAILED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
