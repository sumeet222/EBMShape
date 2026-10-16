"""Bounded public metadata/footer inspection; never fetches candle row groups.

Run with the existing environment. No token, gated acceptance, datasets cache,
full remote object, or vendor-price output is used. Saved evidence is metadata.
"""
import argparse
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import struct
import time
import urllib.error
import urllib.request

import pyarrow.parquet as pq

from ebm_research.experiment_b.pilot import ROOT, sha, write_json


class Probe:
    """Budget HTTP payloads, reject ignored ranges, and record sanitized evidence."""
    def __init__(self, config):
        self.config = config
        self.started = time.monotonic()
        self.cpu_started = time.process_time()
        self.events = []
        self.bytes = 0

    def get(self, url, byte_range=None):
        if time.monotonic() - self.started > self.config["max_acquisition_seconds"]:
            raise RuntimeError("Purposeful inspection time cap reached")
        cap = self.config["max_range_response_bytes"] if byte_range else self.config["max_metadata_response_bytes"]
        cap = min(cap, self.config["max_network_bytes"] - self.bytes)
        if cap <= 0:
            raise RuntimeError("Network budget exhausted")
        headers = {"User-Agent": "EBMShape-D2.1-bounded-metadata", "Accept-Encoding": "identity"}
        if byte_range:
            headers["Range"] = byte_range
        event = {"url": url, "range": byte_range, "bytes": 0}
        self.events.append(event)
        started = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
                event.update(status=response.status, content_length=response.headers.get("Content-Length"), content_range=response.headers.get("Content-Range"))
                if byte_range and response.status != 206:
                    raise RuntimeError("Range ignored; body not read, full object forbidden")
                body = response.read(cap + 1)
                self.bytes += len(body)
                event.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
                if len(body) > cap:
                    raise RuntimeError("Response cap exceeded; no further requests permitted")
                if byte_range:
                    match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", event["content_range"] or "")
                    if not match or len(body) != int(match[2]) - int(match[1]) + 1:
                        raise RuntimeError("Invalid range length/content-range")
                return body
        except urllib.error.HTTPError as error:
            event.update(status=error.code, error=type(error).__name__)
            return None
        except Exception as error:
            event.update(error=type(error).__name__, detail=str(error)[:250])
            raise
        finally:
            event["wall_seconds"] = round(time.monotonic() - started, 4)

    def repository(self, name):
        body = self.get("https://huggingface.co/api/datasets/" + name)
        if body is None:
            return {"repository": name, "status": "UNAVAILABLE"}
        metadata = json.loads(body)
        revision = metadata["sha"]
        card = self.get(f"https://huggingface.co/datasets/{name}/raw/{revision}/README.md")
        siblings = [row["rfilename"] for row in metadata.get("siblings", [])]
        return {"repository": name, "revision": revision, "gated": metadata.get("gated"), "private": metadata.get("private"), "card_data": metadata.get("cardData"), "files": siblings, "card_text": card.decode() if card else None, "license_paths": [s for s in siblings if re.search(r"licen[cs]e|terms|notice", s, re.I)]}

    def footer(self, repository, month, remote_path=None):
        """Read just 8-byte trailer and footer; estimate ticker row-group pushdown."""
        name, revision = repository["repository"], repository["revision"]
        remote_path = remote_path or f"data/ohlcv_{month}.parquet"
        url = f"https://huggingface.co/datasets/{name}/resolve/{revision}/{remote_path}"
        trailer = self.get(url, "bytes=-8")
        if trailer is None:
            return {"month": month, "status": "UNAVAILABLE"}
        if trailer[-4:] != b"PAR1":
            raise RuntimeError("Invalid Parquet trailer")
        footer_bytes = struct.unpack("<I", trailer[:4])[0]
        size = int(self.events[-1]["content_range"].split("/")[-1])
        if footer_bytes > self.config["max_range_response_bytes"] or footer_bytes > size - 12:
            return {"month": month, "remote_bytes": size, "footer_bytes": footer_bytes, "status": "FOOTER_TOO_LARGE"}
        footer = self.get(url, f"bytes={size-footer_bytes-8}-{size-9}")
        # Metadata offsets still refer to the original object. No column pages read.
        metadata = pq.read_metadata(io.BytesIO(b"PAR1" + footer + trailer))
        groups = []
        eligible = []
        for i in range(metadata.num_row_groups):
            group = metadata.row_group(i)
            columns = []
            for j in range(group.num_columns):
                column = group.column(j)
                stats = column.statistics
                entry = {"name": column.path_in_schema, "compressed_bytes": column.total_compressed_size, "statistics_present": stats is not None}
                if stats and column.path_in_schema in {"ticker", "symbol", "timestamp", "ts", "time", "date", "datetime", "source"}:
                    entry.update(min=str(stats.min), max=str(stats.max), null_count=stats.null_count)
                columns.append(entry)
            ticker = next((c for c in columns if c["name"] in {"ticker", "symbol"}), None)
            possible = ticker is None or "min" not in ticker or ticker["min"] <= "SPY" <= ticker["max"]
            if possible:
                eligible.append(i)
            groups.append({"row_group": i, "rows": group.num_rows, "could_contain_SPY": possible, "columns": columns})
        return {"month": month, "url": url, "remote_bytes": size, "footer_bytes": footer_bytes, "footer_sha256": hashlib.sha256(footer).hexdigest(), "rows": metadata.num_rows, "schema": str(metadata.schema), "row_groups": groups, "candidate_row_groups": eligible, "estimated_compressed_all_columns_candidate_bytes": sum(sum(c["compressed_bytes"] for c in groups[i]["columns"]) for i in eligible), "candle_rows_transferred": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=int, choices=[1, 2, 3], required=True)
    parser.add_argument("--instrument", action="store_true", help="Inspect candidate 2 stock SPY footer only, reusing saved repository metadata")
    args = parser.parse_args()
    config_path = ROOT / "config/D2_1_hf_repair.json"
    config = json.loads(config_path.read_text())
    if args.instrument and args.candidate != 2:
        raise ValueError("Only candidate 2 has an approved SPY instrument inspection")
    suffix = "_instrument" if args.instrument else ""
    output = ROOT / f"data/registry/D2_1_hf_candidate_{args.candidate}{suffix}.json"
    if output.exists():
        raise FileExistsError("Evidence exists; inspect it instead of repeating network transfer")
    probe = Probe(config)
    prior = [json.loads(p.read_text()) for p in (ROOT / "data/registry").glob("D2_1_hf_*.json") if p.name != "D2_1_hf_repair_manifest.json"]
    previous_bytes = sum(r["downloaded_body_bytes"] for r in prior)
    previous_seconds = sum(r["wall_seconds"] for r in prior)
    probe.config = {**config, "max_network_bytes": config["max_network_bytes"] - previous_bytes, "max_acquisition_seconds": config["max_acquisition_seconds"] - previous_seconds}
    result = {"observed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "python": platform.python_version(), "config_sha256": sha(config_path), "script_sha256": sha(Path(__file__)), "auth": "public anonymous; no token loaded"}
    try:
        repository = json.loads((ROOT / "data/registry/D2_1_hf_candidate_2.json").read_text())["source"] if args.instrument else probe.repository(config["candidate_repositories"][args.candidate - 1])
        result["source"] = repository
        if args.candidate == 1 and repository.get("revision"):
            result["footer_inspection"] = probe.footer(repository, config["months"][0])
        elif args.instrument:
            result["footer_inspection"] = probe.footer(repository, "instrument", "1m/stocks/SPY.parquet")
    except Exception as error:
        result["error"] = {"type": type(error).__name__, "detail": str(error)[:300]}
    finally:
        result.update(requests=probe.events, downloaded_body_bytes=probe.bytes, wall_seconds=time.monotonic()-probe.started, cpu_seconds=time.process_time()-probe.cpu_started, temporary_disk_bytes=0)
        write_json(output, result)
    print(json.dumps({"output": output.relative_to(ROOT).as_posix(), "bytes": probe.bytes, "error": result.get("error"), "source_revision": result.get("source", {}).get("revision"), "footer_summary": {k:v for k,v in result.get("footer_inspection", {}).items() if k not in {"row_groups", "schema"}}}))


if __name__ == "__main__":
    main()
