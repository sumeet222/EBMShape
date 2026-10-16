"""D2 bounded monthly retrieval, full-candle QA and annual immutable checkpoints.

Only input availability is analyzed. No scientific returns, RV, models or tests
of financial relationships are calculated. D1's pilot safety cap is unchanged.
"""
import argparse
from collections import Counter, defaultdict
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import statistics
import subprocess
import time

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .pilot import (
    ROOT, ET, UTC, Client, aggregate, audit_session, calendar, credentials,
    csv_write, grid, indexed, prior_full, sha, timestamp, usable, valid_bar,
    window_flags, write_json,
)

SCHEMA = pa.schema([
    ("symbol", pa.string()), ("timestamp_utc", pa.timestamp("us", tz="UTC")),
    ("session_et", pa.date32()), ("open", pa.float64()), ("high", pa.float64()),
    ("low", pa.float64()), ("close", pa.float64()), ("volume", pa.float64()),
    ("trade_count", pa.float64()), ("vwap", pa.float64()),
    ("source_batch", pa.string()), ("role", pa.string()),
])
GAP_FIELDS = ["session_et", "start_et", "end_et", "start_utc", "end_utc", "length", "affected_windows", "reason"]
MISSING_FIELDS = ["session_et", "timestamp_et", "timestamp_utc", "affected_windows", "reason"]


class IntegrityError(RuntimeError):
    """An output/pagination/source conflict requires inspection, never overwrite."""


def record(bar, batch, role="required_window"):
    """Normalize native numeric scales without truncating fractional volume/count."""
    t = timestamp(bar["t"])
    return {
        "symbol": "SPY", "timestamp_utc": t, "session_et": t.astimezone(ET).date(),
        **{v: bar.get(k) for k, v in {"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume", "n": "trade_count", "vw": "vwap"}.items()},
        "source_batch": batch, "role": role,
    }


def from_record(row):
    """Restore one native-format anchor from a verified canonical partition."""
    return {"t": row["timestamp_utc"].isoformat(), **{k: row[v] for k, v in {"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume", "n": "trade_count", "vw": "vwap"}.items()}}


def verify_files(data_root, references):
    """Cheap immutable checkpoint validation; fail instead of overwriting a conflict."""
    for ref in references:
        p = data_root / ref["path"]
        if not p.exists() or p.stat().st_size != ref["bytes"] or sha(p) != ref["sha256"]:
            raise IntegrityError(f"Checkpoint integrity conflict: {ref['path']}; preserve and inspect")


def file_ref(path, data_root):
    return {"path": path.relative_to(data_root).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def verify_request_ledger(data_root, manifest):
    """Verify the committed prefix of an append-only ledger after interruption.

    New requests may legitimately follow the last clean checkpoint. Canonical
    and QA files remain immutable; applying their whole-file rule to this growing
    ledger would incorrectly reject a safe interrupted-run resume.
    """
    ref = manifest.get("request_ledger")
    if not ref:
        return
    rows = json.loads((data_root / ref["path"]).read_text())
    count = manifest["requests_total"]
    prefix = (json.dumps(rows[:count], indent=2, allow_nan=False) + "\n").encode()
    # Path.write_text uses native line endings on Windows; preserve logical JSON
    # prefix identity across supported LF/CRLF writers without accepting edits.
    digests = {hashlib.sha256(p).hexdigest() for p in [prefix, prefix.replace(b"\n", b"\r\n")]}
    if len(rows) < count or ref["sha256"] not in digests:
        raise IntegrityError("Committed request-ledger prefix changed; preserve and inspect")


class HistoryClient(Client):
    """Reuse D1's sanitized hash-only transport with bounded D2 transient retries."""
    def __init__(self, raw_dir, config):
        super().__init__(raw_dir, config)
        ledger = raw_dir / "requests.json"
        self.lineage = json.loads(ledger.read_text()) if ledger.exists() else []
        self.retries = 0

    def get(self, name, endpoint, params, headers, retain=False):
        if retain:
            raise ValueError("D2 forbids retaining source response bodies")
        previous = [r for r in self.lineage if r["request_name"] == name and r.get("status") == 200]
        for attempt in range(len(self.config["retry_backoff_seconds"]) + 1):
            try:
                data = super().get(name, endpoint, params, headers, False)
                if previous and previous[-1]["response_sha256"] != self.lineage[-1]["response_sha256"]:
                    raise IntegrityError(f"Changed provider response on repeated incomplete-block request: {name}; inspection required")
                return data
            except RuntimeError:
                status = self.lineage[-1].get("status") if self.lineage else None
                transient = status in {429, 500, 502, 503, 504} or (status is None and self.lineage[-1].get("error") in {"URLError", "TimeoutError"})
                if not transient or attempt == len(self.config["retry_backoff_seconds"]) or self.retries >= self.config["max_transient_retries_total"]:
                    raise
                self.retries += 1
                time.sleep(self.config["retry_backoff_seconds"][attempt])
        raise RuntimeError("Unreachable retry exhaustion")


def fetch_pages(client, name, start, end, headers, timeframe="1Min"):
    """Explicit inclusive range; reject repeated tokens, overlaps and page disorder."""
    params = {"timeframe": timeframe, "start": start.isoformat(), "end": end.isoformat(), "feed": "sip", "adjustment": "split", "sort": "asc", "limit": 10000}
    bars, tokens, previous_last = [], set(), None
    for page in range(client.config["max_pages_per_request"]):
        data = client.get(f"{name}_p{page}", "https://data.alpaca.markets/v2/stocks/SPY/bars", params, headers)
        part = data.get("bars") or []
        times = [timestamp(b["t"]) for b in part]
        if any(not start <= t <= end for t in times):
            raise IntegrityError(f"{name}: returned timestamp outside requested inclusive interval")
        if previous_last is not None and times and times[0] <= previous_last:
            raise IntegrityError(f"{name}: pagination overlap/disorder; do not classify as candle loss")
        if times:
            previous_last = times[-1]
        bars.extend(part)
        token = data.get("next_page_token")
        if not token:
            return bars
        if token in tokens or not part:
            raise IntegrityError(f"{name}: repeated/empty continuation page")
        tokens.add(token)
        params = {**params, "page_token": token}
    raise IntegrityError(f"{name}: page cap exceeded; coverage unknown, not missing candles")


def audit_day(day, bars, prior_anchor, cal, config, daily_count):
    """Reuse D1 QA and enrich D2 field/session/retrieval/retention availability."""
    row, gaps, missing = audit_session(day, bars, prior_anchor, cal, config)
    expected = grid(cal, day)
    by_time, _, _ = indexed(bars)
    opening, closing = cal.session_open(day), cal.session_close(day)
    row.update(
        open_et=opening.tz_convert(ET).isoformat(), close_et=closing.tz_convert(ET).isoformat(),
        open_utc=opening.isoformat(), close_utc=closing.isoformat(),
        observed_raw_count=len(bars), retrieval_status="COMPLETE", retrieval_complete=True,
        zero_returned_candles=not bars,
        missing_price_fields_rows=sum(any(b.get(k) is None for k in ["o", "h", "l", "c"]) for b in bars),
        invalid_price_rows=sum(not valid_bar({**b, "v": None, "n": None}) for b in bars),
        invalid_volume_rows=sum(b.get("v") is not None and (not math.isfinite(float(b["v"])) or b["v"] < 0) for b in bars),
        invalid_trade_count_rows=sum(b.get("n") is not None and (not math.isfinite(float(b["n"])) or b["n"] < 0) for b in bars),
        daily_trade_count_available=daily_count is not None,
        daily_ge500=daily_count >= 500 if daily_count is not None else None,
        daily_count_basis="Alpaca SIP split 1Day; not summed regular-minute/TAQ count",
        has_all_91_required_window_starts=row["session_type"] == "full" and row["required_window_expected"] == 91 and row["missing_required_window"] == 0,
        prior_full_anchor_elapsed_calendar_days=(dt.date.fromisoformat(day) - dt.date.fromisoformat(row["prior_full_session"])).days,
        preceding_session_was_early_close=cal.session_close(cal.previous_session(day)).tz_convert(ET).strftime("%H:%M") != "16:00",
    )
    # A present-but-invalid instant is never disguised as an absent candle.
    invalid = [{"session_et": day, "timestamp_utc": t.isoformat(), "reason": "INVALID_OR_CONFLICTING_CANDLE"} for t, v in by_time.items() if not usable(v)]
    for g in gaps:
        g.update(start_utc=timestamp(g["start_et"]).isoformat(), end_utc=timestamp(g["end_et"]).isoformat(), reason="UNKNOWN_NO_QUALIFYING_BAR_OR_VENDOR_GAP")
    for m in missing:
        m.update(timestamp_utc=timestamp(m["timestamp_et"]).isoformat(), reason="UNKNOWN_NO_QUALIFYING_BAR_OR_VENDOR_GAP")
    assert row["observed_unique_regular"] + row["missing_count"] == len(expected)
    return row, gaps, missing, invalid


def partition_write(destination, rows):
    """Sorted, stable-key, atomic first write; identical duplicates removed explicitly."""
    unique = {}
    duplicates = 0
    for row in rows:
        key = (row["symbol"], row["timestamp_utc"])
        if key in unique:
            if unique[key] != row:
                raise IntegrityError("Conflicting canonical primary key; partition not frozen")
            duplicates += 1
        unique[key] = row
    if destination.exists() or destination.with_suffix(".parquet.tmp").exists():
        raise IntegrityError(f"Unregistered/partial output exists: {destination.name}; preserve for inspection")
    destination.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist([unique[k] for k in sorted(unique)], schema=SCHEMA)
    tmp = destination.with_suffix(".parquet.tmp")
    pq.write_table(table, tmp, compression="zstd")
    tmp.replace(destination)
    return table.num_rows, duplicates


def coverage_rows(rows, frequency):
    """Complete-audit denominators by year/month/quarter, not hypothetical coverage."""
    groups = defaultdict(list)
    for r in rows:
        day = r["session_et"]
        key = day[:4] if frequency == "year" else day[:7] if frequency == "month" else day[:4] + "-Q" + str((int(day[5:7]) - 1) // 3 + 1)
        groups[key].append(r)
    out = []
    for key, group in sorted(groups.items()):
        expected, absent = sum(r["expected_minutes"] for r in group), sum(r["missing_count"] for r in group)
        full = [r for r in group if r["session_type"] == "full"]
        out.append({"period": key, "sessions_retrieved": len(group), "full_sessions": len(full), "expected": expected, "observed_unique": sum(r["observed_unique_regular"] for r in group), "valid_unique": sum(r["observed_unique_valid_regular"] for r in group), "missing": absent, "missing_fraction": absent / expected, "affected_sessions": sum(r["missing_count"] > 0 for r in group), "eligible_full_days": sum(r["eligible_primary"] for r in group)})
    return out


def publish(data_root, manifest, config, cal, all_days):
    """Publish only saved QA; unknown/uncommitted years never become zero-bar days."""
    registry = data_root / "registry"
    rows, gaps, missing, invalid = [], [], [], []
    for block in manifest["blocks"].values():
        saved = json.loads((data_root / block["qa"]["path"]).read_text())
        rows.extend(saved["sessions"])
        gaps.extend(saved["gaps"])
        missing.extend(saved["missing"])
        invalid.extend(saved["invalid"])
    if not rows:
        return None
    rows.sort(key=lambda r: r["session_et"])
    totals = aggregate(rows, gaps, missing, cal)
    lengths = [g["length"] for g in gaps]
    longest = max(lengths, default=0)
    audited = {r["session_et"] for r in rows}
    unknown = sorted(set(all_days) - audited)
    # Publish explicit unknown rows, with null candle counts, after an interruption.
    unknown_rows = [{"session_et": d, "retrieval_status": "UNRETRIEVED_OR_UNCOMMITTED_BLOCK", "retrieval_complete": False, "exclusion_reasons": "COVERAGE_UNKNOWN"} for d in unknown]
    csv_write(registry / "D2_spy_candle_qa_sessions.csv", sorted(rows + unknown_rows, key=lambda r: r["session_et"]), list(rows[0]))
    csv_write(registry / "D2_spy_candle_gap_clusters.csv", gaps, GAP_FIELDS)
    csv_write(registry / "D2_spy_missing_candles.csv", missing, MISSING_FIELDS)
    csv_write(registry / "D2_spy_invalid_candles.csv", invalid, ["session_et", "timestamp_utc", "reason"])
    for frequency in ["year", "month", "quarter"]:
        cov = coverage_rows(rows, frequency)
        csv_write(registry / f"D2_spy_coverage_{frequency}.csv", cov, list(cov[0]))
    totals.update(
        requested_session_count=len(all_days), audited_session_count=len(rows), unknown_session_count=len(unknown),
        retrieval_complete=not unknown, unknown_dates=unknown,
        largest_gap_ties=[g for g in gaps if g["length"] == longest],
        gap_length_mean=statistics.mean(lengths) if lengths else 0,
        gap_length_median=statistics.median(lengths) if lengths else 0,
        gap_length_p95=float(pd.Series(lengths).quantile(.95)) if lengths else 0,
        gap_size_bins={"1": sum(x == 1 for x in lengths), "2_4": sum(2 <= x <= 4 for x in lengths), "5_9": sum(5 <= x <= 9 for x in lengths), "10_29": sum(10 <= x <= 29 for x in lengths), "30_plus": sum(x >= 30 for x in lengths)},
        top_20_gaps=sorted(gaps, key=lambda r: (-r["length"], r["session_et"], r["start_et"]))[:20],
        maximum_affected_day_run=max((r["length"] for r in totals["missingness_session_runs"]), default=0),
        longest_affected_day_runs=[], maximum_eligible_day_run=max((r["length"] for r in totals["eligible_contiguous_runs"]), default=0),
        zero_returned_sessions=[r["session_et"] for r in rows if r["zero_returned_candles"]],
        exclusion_reason_counts=dict(Counter(reason for r in rows for reason in r["exclusion_reasons"].split(";") if reason)),
        daily_trade_count_available_sessions=sum(r["daily_trade_count_available"] for r in rows),
        daily_ge500_sessions=sum(r["daily_ge500"] is True for r in rows),
        full_sessions_after_early_close=sum(r["preceding_session_was_early_close"] for r in rows if r["session_type"] == "full"),
    )
    totals["longest_affected_day_runs"] = [r for r in totals["missingness_session_runs"] if r["length"] == totals["maximum_affected_day_run"]]
    totals["disjoint_window_missing"] = {flag: sum(r["missing_"+flag+"_disjoint"] for r in rows) for flag in ["opening_rv", "anchor", "late_predictor", "final_target", "other"]}
    assert sum(totals["disjoint_window_missing"].values()) == totals["missing"]
    totals["cluster_distribution"] = {}
    for frequency in ["year", "month", "quarter"]:
        summary = coverage_rows(rows, frequency)
        for group in summary:
            def period(day):
                return day[:4] if frequency == "year" else day[:7] if frequency == "month" else day[:4]+"-Q"+str((int(day[5:7])-1)//3+1)
            subset = [g for g in gaps if period(g["session_et"]) == group["period"]]
            group["clusters"] = len(subset)
            group["proportion_of_all_missing_bars"] = group["missing"] / totals["missing"] if totals["missing"] else 0
            group["proportion_of_all_clusters"] = len(subset) / len(gaps) if gaps else 0
        totals["cluster_distribution"][frequency] = summary
    totals["splits"] = {}
    for name, (start, end) in config["splits"].items():
        full = [r for r in rows if start <= r["session_et"] <= end and r["session_type"] == "full"]
        # Otherwise eligible means all non-opening primary inputs valid; never relax RV.
        otherwise = [r for r in full if r["eligible_r1"] and r["eligible_r12"] and r["eligible_r13"] and not r["invalid_ohlcv_rows"]]
        loss = sum(not r["eligible_rv"] for r in otherwise)
        totals["splits"][name] = {"full_days": len(full), "eligible_full_days": sum(r["eligible_primary"] for r in full), "ineligible_full_days": sum(not r["eligible_primary"] for r in full), "opening_rv_loss_full_days": sum(not r["eligible_rv"] for r in full), "otherwise_eligible_denominator": len(otherwise), "opening_rv_loss_otherwise": loss, "opening_rv_loss_fraction_otherwise": loss / len(otherwise) if otherwise else None}
    complete_years = [v for v in coverage_rows(rows, "year") if v["period"] < config["end"][:4] and v["eligible_full_days"] == v["full_sessions"] and v["sessions_retrieved"] == len(cal.sessions_in_range(v["period"]+"-01-01", v["period"]+"-12-31"))]
    totals["fully_eligible_complete_calendar_years"] = [v["period"] for v in complete_years]
    loss_exceeds = any((v["opening_rv_loss_fraction_otherwise"] or 0) > config["opening_rv_loss_stop_fraction"] for v in totals["splits"].values())
    totals["stage1_permitted"] = not unknown and not loss_exceeds and len(complete_years) >= 3 and not invalid
    totals["status"] = ("PARTIAL" if unknown else "BLOCKED" if not totals["stage1_permitted"] else "PASS WITH QUALIFICATIONS" if totals["missing"] or any(not r["eligible_primary"] for r in rows if r["session_type"] == "full") else "PASS")
    totals["eligible_year_screen_note"] = "Literal complete-calendar-year coverage with every scheduled full session eligible; shortened sessions excluded by protocol; no nonlinear power claim"
    write_json(registry / "D2_spy_candle_qa_summary.json", totals)
    return totals


def main():
    """Acquire one verified year at a time; resume skips immutable completed blocks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-config", type=Path, default=ROOT / "config/D2_spy_source.json")
    parser.add_argument("--data-root", type=Path, default=Path(os.environ.get("EBM_DATA_ROOT") or ROOT / "data"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--max-years", type=int, help="Bound this invocation for first-block measurement")
    args = parser.parse_args()
    config = json.loads(args.source_config.read_text())
    if (config["symbol"], config["feed"], config["adjustment"], config["start"], config["end"]) != ("SPY", "sip", "split", "2016-01-04", "2026-09-30"):
        raise ValueError("D2 fixed SPY/SIP/split/2016-01-04..2026-09-30 identity mismatch")
    cal = calendar(config["start"], config["end"])
    days = [t.date().isoformat() for t in cal.sessions_in_range(config["start"], config["end"])]
    full = [d for d in days if cal.session_close(d).tz_convert(ET).strftime("%H:%M") == "16:00"]
    identity = {"config_sha256": sha(args.source_config), "dataset_id": config["dataset_id"], "scientific_spec_sha256": sha(ROOT / config["scientific_spec"])}
    if args.dry_run:
        print(json.dumps({**identity, "calendar_sessions": len(days), "full_sessions": len(full), "early_sessions": len(days)-len(full), "expected_minutes": sum(len(grid(cal, d)) for d in days), "projected_retained_rows": 91*len(full)+1, "initial_anchor_date": prior_full(cal, days[0]), "retained_size_projection_mb": 10, "network_transfer_projection_mb": "120-300 including extended hours inside monthly request spans", "data_root": str(args.data_root)}, indent=2))
        return
    registry, canonical = args.data_root / "registry", args.data_root / "canonical/spy_minute" / config["dataset_id"]
    raw = args.data_root / "raw/alpaca" / config["dataset_id"]
    out = registry / "D2_spy_source_manifest.json"
    if out.exists():
        manifest = json.loads(out.read_text())
        if manifest["identity"] != identity:
            raise RuntimeError("D2 existing config/spec identity mismatch; preserve prior outputs")
        if not (args.resume or args.verify_only):
            raise RuntimeError("D2 manifest exists: use --resume or --verify-only; no blind repeat")
    else:
        manifest = {"identity": identity, "source": {k: config[k] for k in ["symbol", "feed", "adjustment", "timeframe", "start", "end", "calendar", "timezone", "storage_timezone", "bar_label", "retention", "source_revision"]}, "blocks": {}, "status": "PARTIAL", "started_at_utc": dt.datetime.now(UTC).isoformat(), "initial_anchor": None, "active_year": None, "d1_reuse_decision": "D1 preserved as immutable diagnostic; overlapping 11 sessions reacquired in D2 contiguous requests for consistent extraction lineage; no data copied"}
    manifest.setdefault("schema_version", 1)
    manifest.setdefault("canonical_schema", {field.name: str(field.type) for field in SCHEMA})
    manifest.setdefault("primary_key", ["symbol", "timestamp_utc"])
    manifest.setdefault("splits", config["splits"])
    for block in manifest["blocks"].values():
        verify_files(args.data_root, [block["canonical"], block["qa"]])
    verify_request_ledger(args.data_root, manifest)
    if args.verify_only:
        print(json.dumps({"status": manifest["status"], "verified_years": sorted(manifest["blocks"]), "rows": sum(b["rows"] for b in manifest["blocks"].values()), "canonical_bytes": sum(b["canonical"]["bytes"] for b in manifest["blocks"].values()), "network_calls": 0}))
        return
    raw.mkdir(parents=True, exist_ok=True)
    client = HistoryClient(raw, config)
    headers = credentials()
    started = time.monotonic()
    exceptions_path = registry / "D2_spy_exception_log.json"
    exceptions = json.loads(exceptions_path.read_text()) if exceptions_path.exists() else []
    code_identity = {str(Path(__file__).relative_to(ROOT)): sha(__file__), "src/ebm_research/experiment_b/pilot.py": sha(ROOT / "src/ebm_research/experiment_b/pilot.py")}
    if manifest.get("code_sha256") and "execution_history" not in manifest:
        manifest["execution_history"] = [{"code_sha256": manifest["code_sha256"], "completed_years_at_end": sorted(manifest["blocks"]), "wall_seconds": manifest.get("last_invocation_wall_seconds"), "note": "First measured annual invocation; preserved before summary-only additions"}]
    manifest.setdefault("execution_history", []).append({"started_at_utc": dt.datetime.now(UTC).isoformat(), "code_sha256": code_identity, "completed_years_at_start": sorted(manifest["blocks"]), "max_years": args.max_years})
    manifest["code_sha256"] = code_identity
    manifest["versions"] = {k: importlib.metadata.version(k) for k in ["exchange-calendars", "pandas", "numpy", "pyarrow", "tzdata"]}
    manifest["python"] = platform.python_version()
    manifest["code_commit_at_invocation"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    write_json(out, manifest)
    prior_anchor, initial_records = [], []
    completed = sorted(manifest["blocks"])
    if completed != sorted({d[:4] for d in days})[:len(completed)]:
        raise IntegrityError("Completed year checkpoints are not a contiguous prefix; inspect manifest")
    if completed:
        last = manifest["blocks"][completed[-1]]
        t = last["last_full_session"]
        table = pq.read_table(args.data_root / last["canonical"]["path"], filters=[("session_et", "=", dt.date.fromisoformat(t))])
        prior_anchor = [from_record(r) for r in table.to_pylist() if r["timestamp_utc"].astimezone(ET).strftime("%H:%M") == "15:59"]
    try:
        if not completed:
            anchor_day = prior_full(cal, days[0])
            a = cal.session_close(anchor_day).to_pydatetime()-dt.timedelta(minutes=1)
            prior_anchor = fetch_pages(client, "initial_prior_anchor", a, a+dt.timedelta(seconds=59), headers)
            manifest["initial_anchor"] = {"session_et": anchor_day, "available": usable(prior_anchor), "returned_rows": len(prior_anchor), "purpose": "optional leading r1 anchor only"}
            initial_records = [record(b, "initial_prior_anchor", "initial_prior_anchor") for b in prior_anchor]
            write_json(out, manifest)
        count = 0
        for year in sorted({d[:4] for d in days}):
            if year in manifest["blocks"]:
                continue
            manifest["active_year"] = year
            write_json(out, manifest)
            destination = canonical / f"year={year}.parquet"
            qa_path = registry / "D2_blocks" / f"{year}.json"
            if destination.exists() or qa_path.exists():
                raise IntegrityError(f"Unregistered/orphan year output {year}; preserve for inspection")
            year_days = [d for d in days if d.startswith(year)]
            daily_start = dt.datetime.fromisoformat(year_days[0]+"T00:00:00").replace(tzinfo=ET)
            daily_end = dt.datetime.fromisoformat(year_days[-1]+"T23:59:59").replace(tzinfo=ET)
            daily_bars = fetch_pages(client, f"daily_{year}", daily_start, daily_end, headers, "1Day")
            daily_counts = {timestamp(b["t"]).astimezone(ET).date().isoformat(): b.get("n") for b in daily_bars}
            selected, qa, gaps, missing, invalid, batches = list(initial_records), [], [], [], [], []
            initial_records = []
            last_full_session = None
            for month in sorted({d[:7] for d in year_days}):
                batch_days = [d for d in year_days if d.startswith(month)]
                a, z = cal.session_open(batch_days[0]).to_pydatetime(), cal.session_close(batch_days[-1]).to_pydatetime()-dt.timedelta(seconds=1)
                before = len(client.lineage)
                bars = fetch_pages(client, f"minute_{month}", a, z, headers)
                by_day = defaultdict(list)
                after_hours = 0
                for b in bars:
                    t = timestamp(b["t"])
                    day = t.astimezone(ET).date().isoformat()
                    if day in batch_days and cal.session_open(day).to_pydatetime() <= t < cal.session_close(day).to_pydatetime():
                        by_day[day].append(b)
                    else:
                        after_hours += 1
                for day in batch_days:
                    current = by_day[day]
                    row, cg, cm, ci = audit_day(day, current, prior_anchor, cal, config, daily_counts.get(day))
                    if row["conflicting_timestamps"] or row["parse_errors"] or row["raw_ordering_violations"]:
                        raise IntegrityError(f"{day}: conflicting/timestamp/order integrity failure; partition not frozen")
                    qa.append(row); gaps.extend(cg); missing.extend(cm); invalid.extend(ci)
                    if row["session_type"] == "full":
                        selected.extend(record(b, month) for b in current if window_flags(timestamp(b["t"])) != ["other"])
                        close_t = cal.session_close(day).to_pydatetime()-dt.timedelta(minutes=1)
                        prior_anchor = [b for b in current if timestamp(b["t"]) == close_t]
                        last_full_session = day
                batch = {"month": month, "requested_start": a.isoformat(), "requested_end": z.isoformat(), "retrieval_complete": True, "returned_rows_including_extended": len(bars), "after_hours_rows_discarded": after_hours, "regular_rows": sum(len(x) for x in by_day.values()), "requests": len(client.lineage)-before}
                batches.append(batch)
                if "first_batch_measurement" not in manifest:
                    buf = pa.BufferOutputStream(); pq.write_table(pa.Table.from_pylist(selected, schema=SCHEMA), buf, compression="zstd")
                    manifest["first_batch_measurement"] = {"month": month, "retained_rows": len(selected), "compressed_bytes_in_memory": buf.tell(), "source_transfer_bytes": sum(r.get("response_bytes", 0) for r in client.lineage[before:]), "projected_canonical_bytes": round(buf.tell()/max(len(selected),1)*(91*len(full)+1))}
                    write_json(out, manifest)
                print(json.dumps({"audited_month": month, "regular_rows": batch["regular_rows"], "missing": sum(r["missing_count"] for r in qa if r["session_et"].startswith(month)), "retained_year_rows": len(selected)}), flush=True)
            row_count, dedup = partition_write(destination, selected)
            saved = {"year": year, "sessions": qa, "gaps": gaps, "missing": missing, "invalid": invalid, "batches": batches, "identical_duplicate_rows_removed": dedup}
            write_json(qa_path, saved)
            manifest["blocks"][year] = {"canonical": file_ref(destination, args.data_root), "qa": file_ref(qa_path, args.data_root), "rows": row_count, "sessions": len(qa), "last_full_session": last_full_session, "completed_at_utc": dt.datetime.now(UTC).isoformat()}
            manifest["active_year"] = None
            retained_bytes = sum(b["canonical"]["bytes"]+b["qa"]["bytes"] for b in manifest["blocks"].values())
            if retained_bytes >= config["warn_retained_bytes"]:
                raise RuntimeError("Unexpected retained storage >=1 GB; stop before 2 GB and inspect")
            write_json(out, manifest)
            print(json.dumps({"completed_year": year, "rows": row_count, "parquet_bytes": destination.stat().st_size, "missing": len(missing)}), flush=True)
            count += 1
            if args.max_years and count >= args.max_years:
                break
        totals = publish(args.data_root, manifest, config, cal, days)
        manifest["status"] = totals["status"] if totals else "PARTIAL"
        manifest["retrieval_complete"] = bool(totals and totals["retrieval_complete"])
        manifest["last_invocation_wall_seconds"] = round(time.monotonic()-started, 3)
        manifest["execution_history"][-1].update(wall_seconds=manifest["last_invocation_wall_seconds"], completed_years_at_end=sorted(manifest["blocks"]))
        manifest["requests_total"] = len(client.lineage)
        manifest["successful_requests_total"] = sum(r.get("status") == 200 for r in client.lineage)
        manifest["response_bytes_total"] = sum(r.get("response_bytes", 0) for r in client.lineage)
        manifest["retry_count_this_invocation"] = client.retries
        manifest["request_ledger"] = file_ref(raw / "requests.json", args.data_root)
        manifest["frozen_at_utc"] = dt.datetime.now(UTC).isoformat() if manifest["retrieval_complete"] else None
        write_json(out, manifest)
        write_json(exceptions_path, exceptions)
        print(json.dumps({"status": manifest["status"], "years_complete": len(manifest["blocks"]), "canonical_rows": sum(b["rows"] for b in manifest["blocks"].values()), "canonical_bytes": sum(b["canonical"]["bytes"] for b in manifest["blocks"].values()), "requests_total": len(client.lineage), "response_bytes": manifest["response_bytes_total"]}), flush=True)
    except Exception as exc:
        # Keep unknown coverage separate from successfully retrieved empty sessions.
        manifest["status"] = "INVALID—RERUN" if isinstance(exc, (IntegrityError, ValueError, AssertionError)) else "BLOCKED"
        exceptions.append({"observed_at_utc": dt.datetime.now(UTC).isoformat(), "active_year": manifest["active_year"], "type": type(exc).__name__, "message": str(exc)[:500], "coverage": "uncommitted year unknown; completed verified blocks preserved"})
        write_json(out, manifest); write_json(exceptions_path, exceptions)
        publish(args.data_root, manifest, config, cal, days)
        raise


if __name__ == "__main__":
    main()
