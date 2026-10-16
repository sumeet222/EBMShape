"""Bounded SIP acquisition and calendar-aware candle audit. No model fitting."""
import argparse
from collections import Counter, defaultdict
import csv
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

import exchange_calendars as xcals
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[3]
ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
FIELDS = {"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume", "n": "trade_count", "vw": "vwap"}


def sha(path):
    """Content digest for a small config/artifact, once per acquisition/check."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    """Atomically replace this stage's small generated metadata, never input data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    tmp.replace(path)


def timestamp(value):
    """Parse an offset-aware source bar start; reject naive/minute-misaligned time."""
    t = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if t.tzinfo is None or t.second or t.microsecond:
        raise ValueError("Expected timezone-aware exact minute start")
    return t.astimezone(UTC)


def calendar(start, end):
    """NYSE regular-session calendar, expanded to include preceding full anchors."""
    return xcals.get_calendar("XNYS", start=(pd.Timestamp(start) - pd.Timedelta(days=20)).date().isoformat(), end=end, side="left")


def grid(cal, day):
    """Actual expected one-minute bar starts, including shortened trading sessions."""
    return [t.to_pydatetime() for t in cal.session_minutes(day)]


def prior_full(cal, day):
    """Preceding permissible full session; skip early closes per D1/B v1 rule."""
    prev = cal.previous_session(day)
    while cal.session_close(prev).tz_convert(ET).strftime("%H:%M") != "16:00":
        prev = cal.previous_session(prev)
    return prev.date().isoformat()


def window_flags(t):
    """Named possibly-overlapping scientific windows for a regular bar start."""
    hm = t.astimezone(ET).strftime("%H:%M")
    flags = []
    if "09:30" <= hm <= "09:59":
        flags.append("opening_rv")
    if hm in {"09:59", "14:59", "15:29", "15:59"}:
        flags.append("anchor")
    if "15:00" <= hm <= "15:29":
        flags.append("late_predictor")
    if "15:30" <= hm <= "15:59":
        flags.append("final_target")
    return flags or ["other"]


def valid_bar(b):
    """Finite positive consistent OHLC and nonnegative volume/count if present."""
    try:
        o, h, l, c = (float(b[k]) for k in ["o", "h", "l", "c"])
        return (all(math.isfinite(x) and x > 0 for x in [o, h, l, c])
                and h >= max(o, c) and l <= min(o, c) and h >= l
                and all(b.get(k) is None or (math.isfinite(float(b[k])) and float(b[k]) >= 0) for k in ["v", "n"]))
    except (KeyError, TypeError, ValueError):
        return False


def indexed(bars):
    """Keep all duplicate values for QA; parse errors remain counted separately."""
    by_time = defaultdict(list)
    parse_errors = 0
    ordering = 0
    prev = None
    for b in bars:
        try:
            t = timestamp(b["t"])
        except (KeyError, TypeError, ValueError):
            parse_errors += 1
            continue
        ordering += int(prev is not None and t < prev)
        prev = t
        by_time[t].append(b)
    return by_time, parse_errors, ordering


def usable(values):
    """A duplicated instant is usable only if identical and every bar is valid."""
    return bool(values) and all(valid_bar(b) for b in values) and len({json.dumps(b, sort_keys=True) for b in values}) == 1


def audit_session(day, bars, all_bars, cal, config):
    """Audit one requested whole session; return QA row, maximal gaps and minutes.

    Missing means absent timestamp; invalid/conflicting minutes are separate and
    fail scientific eligibility. No imputation, filtering or outlier clipping.
    """
    expected = grid(cal, day)
    wanted = set(expected)
    by_time, errors, ordering = indexed(bars)
    present = wanted & set(by_time)
    good = {t for t in present if usable(by_time[t])}
    absent = sorted(wanted - present)
    runs = []
    for t in absent:
        if runs and t == runs[-1][-1] + dt.timedelta(minutes=1):
            runs[-1].append(t)
        else:
            runs.append([t])
    clusters = [{"session_et": day, "start_et": r[0].astimezone(ET).isoformat(), "end_et": r[-1].astimezone(ET).isoformat(), "length": len(r), "affected_windows": ";".join(sorted({f for t in r for f in window_flags(t)}))} for r in runs]
    missing = [{"session_et": day, "timestamp_et": t.astimezone(ET).isoformat(), "affected_windows": ";".join(window_flags(t))} for t in absent]
    assert sum(c["length"] for c in clusters) == len(absent)
    assert len(present) + len(absent) == len(expected)
    full = cal.session_close(day).tz_convert(ET).strftime("%H:%M") == "16:00"
    prior = prior_full(cal, day)
    prior_t = dt.datetime.fromisoformat(prior + "T15:59:00").replace(tzinfo=ET).astimezone(UTC)
    prior_values = [b for b in all_bars if b.get("t") and _same_time(b["t"], prior_t)]
    prior_ok = usable(prior_values)
    anchor_ok = {}
    for hm in ["09:59", "14:59", "15:29", "15:59"]:
        t = dt.datetime.fromisoformat(day + "T" + hm + ":00").replace(tzinfo=ET).astimezone(UTC)
        anchor_ok[hm] = t in good
    req = {t for t in expected if window_flags(t) != ["other"]}
    # Use disjoint categories as well as explicitly overlapping window flags.
    category = lambda t: next((f for f in ["opening_rv", "late_predictor", "final_target", "anchor"] if f in window_flags(t)), "other")
    cats = Counter(category(t) for t in absent)
    bad = sum(not valid_bar(b) for b in bars)
    conflicts = sum(len({json.dumps(b, sort_keys=True) for b in v}) > 1 for v in by_time.values())
    extreme = 0
    last_close = None
    for t in sorted(present):
        b = by_time[t][0]
        if valid_bar(b):
            extreme += int((b["h"] - b["l"]) / b["o"] > config["manual_extreme_range_fraction"] or (last_close is not None and abs(b["c"] / last_close - 1) > config["manual_extreme_close_jump_fraction"]))
            last_close = b["c"]
    opening_good = sum("opening_rv" in window_flags(t) for t in good)
    row = {"session_et": day, "session_type": "full" if full else "early_close", "expected_minutes": len(expected), "observed_unique_regular": len(present), "observed_unique_valid_regular": len(good), "missing_count": len(absent), "missing_fraction": len(absent) / len(expected), "outside_session_count": sum(len(v) for t, v in by_time.items() if t not in wanted), "duplicates": sum(len(v) - 1 for v in by_time.values()), "conflicting_timestamps": conflicts, "raw_ordering_violations": ordering, "parse_errors": errors, "invalid_ohlcv_rows": bad, "invalid_unique_regular": len(present - good), "zero_volume_rows": sum(b.get("v") == 0 for b in bars), "zero_trade_rows": sum(b.get("n") == 0 for b in bars), "volume_missing_rows": sum(b.get("v") is None for b in bars), "trade_count_missing_rows": sum(b.get("n") is None for b in bars), "extreme_review_rows": extreme, "gap_clusters": len(runs), "gap_lengths_sum": len(absent), "longest_gap_length": max(map(len, runs), default=0), "longest_gap_start_et": max(clusters, key=lambda c: c["length"])["start_et"] if clusters else None, "longest_gap_end_et": max(clusters, key=lambda c: c["length"])["end_et"] if clusters else None, "singleton_gaps": sum(len(r) == 1 for r in runs), "gaps_2_4": sum(2 <= len(r) <= 4 for r in runs), "gaps_5_9": sum(5 <= len(r) <= 9 for r in runs), "gaps_ge10": sum(len(r) >= 10 for r in runs), "opening_valid_minutes": opening_good, "required_window_expected": len(req), "required_window_valid": len(req & good), "missing_required_window": len(req - present), "valid_required_window": full and req <= good, "prior_full_session": prior, "prior_anchor_valid": prior_ok}
    for flag in ["opening_rv", "anchor", "late_predictor", "final_target", "other"]:
        row["missing_" + flag + "_overlapping"] = sum(flag in window_flags(t) for t in absent)
        row["missing_" + flag + "_disjoint"] = cats[flag]
    for hm, ok in anchor_ok.items():
        row["anchor_" + hm.replace(":", "") + "_valid"] = ok
    row.update(eligible_r1=anchor_ok["09:59"] and prior_ok, eligible_r12=anchor_ok["14:59"] and anchor_ok["15:29"], eligible_r13=full and anchor_ok["15:29"] and anchor_ok["15:59"], eligible_rv=opening_good == 30)
    row["eligible_primary"] = full and row["valid_required_window"] and row["eligible_r1"] and row["eligible_r12"] and row["eligible_r13"] and row["eligible_rv"] and not (bad or conflicts or errors)
    reasons = []
    for condition, reason in [(not full, "HALF_DAY"), (not prior_ok, "MISSING_PRIOR_FULL_ANCHOR"), (opening_good < 30, "INCOMPLETE_OPENING_30"), (full and not all(anchor_ok.values()), "MISSING_OR_INVALID_CRITICAL_CANDLE"), (bad > 0, "INVALID_OHLCV"), (conflicts > 0, "CONFLICTING_DUPLICATE"), (errors > 0, "TIMESTAMP_PARSE_ERROR")]:
        if condition:
            reasons.append(reason)
    row["exclusion_reasons"] = ";".join(reasons)
    return row, clusters, missing


def _same_time(value, t):
    try:
        return timestamp(value) == t
    except (ValueError, TypeError):
        return False


def anchor_check(day, all_bars, cal):
    """Tiny actual-sample operational return/RV validation; not predictive analysis."""
    idx, _, _ = indexed(all_bars)
    def at(date, hm):
        t = dt.datetime.fromisoformat(date + "T" + hm + ":00").replace(tzinfo=ET).astimezone(UTC)
        if not usable(idx.get(t)):
            raise ValueError(f"SPY {date} {hm}: missing/invalid anchor")
        return idx[t][0]
    prev = prior_full(cal, day)
    pprev = at(prev, "15:59")["c"]
    opening = [at(day, f"09:{m:02}") for m in range(30, 60)]
    q = [math.log(opening[0]["c"] / opening[0]["o"])] + [math.log(b["c"] / a["c"]) for a, b in zip(opening, opening[1:])]
    p10, p15, p1530, p16 = (at(day, hm)["c"] for hm in ["09:59", "14:59", "15:29", "15:59"])
    rv = math.sqrt(sum(v * v for v in q))
    return {"session_et": day, "prior_full_session": prev, "Pprev": pprev, "P10": p10, "P15": p15, "P1530": p1530, "P16": p16, "r1": p10 / pprev - 1, "r12": p1530 / p15 - 1, "r13": p16 / p1530 - 1, "rv_open_raw": rv, "rv_open_log": math.log(rv + 1e-8), "n_open_minute_bars": 30, "purpose": "one actual-sample equation/anchor validation only; no model evaluation"}


def credentials():
    """Use only exported environment values; fail without disclosing secrets."""
    names = ["APCA_API_KEY_ID", "APCA_API_SECRET_KEY"]
    missing = [k for k in names if not os.environ.get(k)]
    if missing:
        raise RuntimeError("Missing environment variables: " + ", ".join(missing))
    return {"APCA-API-KEY-ID": os.environ[names[0]], "APCA-API-SECRET-KEY": os.environ[names[1]]}


class Client:
    """Small bounded HTTP client with diagnostic cache and hash-only candle lineage."""
    def __init__(self, raw_dir, config):
        self.raw_dir, self.config = raw_dir, config
        self.lineage = []
        self.network_calls = 0

    def get(self, name, endpoint, params, headers, retain=False):
        """Reuse verified auxiliary response; candle bodies retained only in canonical."""
        cache = self.raw_dir / (name + ".json")
        ledger = self.raw_dir / "requests.json"
        if cache.exists():
            obj = json.loads(cache.read_text())
            if obj["endpoint"] != endpoint or obj["params"] != params:
                raise RuntimeError(f"Cache parameters mismatch: {name}")
            if hashlib.sha256(json.dumps(obj["data"], sort_keys=True).encode()).hexdigest() != obj["data_hash"]:
                raise RuntimeError(f"Cache content hash mismatch: {name}")
            return obj["data"]
        time.sleep(self.config["request_spacing_seconds"])
        started = time.monotonic()
        safe = {"request_name": name, "endpoint": endpoint, "params": params, "observed_at_utc": dt.datetime.now(UTC).isoformat()}
        try:
            url = endpoint + "?" + urllib.parse.urlencode(params)
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
                body = response.read(2_000_001)
                if len(body) > 2_000_000:
                    raise RuntimeError("Response exceeds 2 MB D1 cap")
                data = json.loads(body)
                safe.update(status=response.status, response_bytes=len(body), response_sha256=hashlib.sha256(body).hexdigest())
        except urllib.error.HTTPError as exc:
            safe.update(status=exc.code, error="HTTP error; no retry or entitlement workaround")
            self.lineage.append(safe)
            write_json(ledger, self.lineage)
            raise RuntimeError(f"{name}: HTTP {exc.code}; inspect sanitized request ledger") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            safe.update(status=None, error=type(exc).__name__)
            self.lineage.append(safe)
            write_json(ledger, self.lineage)
            raise RuntimeError(f"{name}: {type(exc).__name__}; no response retained") from None
        self.network_calls += 1
        safe["wall_seconds"] = round(time.monotonic() - started, 4)
        self.lineage.append(safe)
        write_json(ledger, self.lineage)
        if retain:
            write_json(cache, {"endpoint": endpoint, "params": params, "data": data, "data_hash": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()})
        return data

    def alpaca(self, name, start, end, headers, timeframe="1Min", adjustment="split", retain=False):
        """Retrieve only explicit SPY intervals, inspecting continuation tokens."""
        params = {"timeframe": timeframe, "start": start.isoformat(), "end": end.isoformat(), "feed": "sip", "adjustment": adjustment, "sort": "asc", "limit": 10000}
        bars = []
        for page in range(self.config["max_pages_per_request"]):
            data = self.get(f"{name}_p{page}", "https://data.alpaca.markets/v2/stocks/SPY/bars", params, headers, retain)
            bars.extend(data.get("bars") or [])
            token = data.get("next_page_token")
            if not token:
                return bars
            params = {**params, "page_token": token}
        raise RuntimeError(f"{name}: pagination exceeded bounded page cap")


def csv_write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def runs_of_sessions(days, cal):
    """Actual contiguous exchange-session runs; missing date coverage breaks a run."""
    runs = []
    for day in sorted(days):
        if runs and cal.previous_session(day).date().isoformat() == runs[-1][-1]:
            runs[-1].append(day)
        else:
            runs.append([day])
    return [{"start": r[0], "end": r[-1], "length": len(r)} for r in runs]


def aggregate(rows, clusters, missing, cal):
    """Reconcile dataset totals and stratified missingness without IID inflation."""
    total = lambda key: sum(r[key] for r in rows)
    full = [r for r in rows if r["session_type"] == "full"]
    groups = {}
    for group, key in [("year", lambda r: r["session_et"][:4]), ("month", lambda r: r["session_et"][:7]), ("session_type", lambda r: r["session_type"])]:
        groups[group] = {}
        for value in sorted({key(r) for r in rows}):
            selected = [r for r in rows if key(r) == value]
            n, gaps = sum(r["expected_minutes"] for r in selected), sum(r["missing_count"] for r in selected)
            groups[group][value] = {"sessions": len(selected), "expected": n, "missing": gaps, "missing_fraction": gaps / n}
    windows = {}
    for flag in ["opening_rv", "anchor", "late_predictor", "final_target", "other"]:
        exp = sum(sum(flag in window_flags(t) for t in grid(cal, r["session_et"])) for r in rows)
        miss = sum(r["missing_" + flag + "_overlapping"] for r in rows)
        windows[flag] = {"expected": exp, "missing": miss, "fraction": miss / exp if exp else None, "overlapping": True}
    time_of_day = {}
    for r in rows:
        for t in grid(cal, r["session_et"]):
            hm = t.astimezone(ET).strftime("%H:%M")
            time_of_day.setdefault(hm, {"expected": 0, "missing": 0})["expected"] += 1
    for m in missing:
        time_of_day[m["timestamp_et"][11:16]]["missing"] += 1
    for v in time_of_day.values():
        v["fraction"] = v["missing"] / v["expected"]
    assert total("missing_count") == sum(c["length"] for c in clusters) == len(missing)
    return {"sessions": len(rows), "full_sessions": len(full), "early_sessions": len(rows) - len(full), "expected": total("expected_minutes"), "observed_unique": total("observed_unique_regular"), "valid_unique": total("observed_unique_valid_regular"), "missing": total("missing_count"), "missing_fraction": total("missing_count") / total("expected_minutes"), "gap_clusters": len(clusters), "gap_size_distribution": dict(Counter(c["length"] for c in clusters)), "max_gap_length": max((c["length"] for c in clusters), default=0), "top_10_gaps": sorted(clusters, key=lambda c: (-c["length"], c["session_et"], c["start_et"]))[:10], "affected_sessions": sum(r["missing_count"] > 0 for r in rows), "incomplete_full_sessions": sum(r["missing_count"] > 0 or r["invalid_unique_regular"] > 0 for r in full), "affected_opening_full_sessions": sum(not r["eligible_rv"] for r in full), "affected_label_full_sessions": sum(not r["eligible_r13"] for r in full), "complete_full_day_rate": sum(r["observed_unique_valid_regular"] == r["expected_minutes"] for r in full) / len(full), "complete_required_window_rate_full": sum(r["valid_required_window"] for r in full) / len(full), "eligible_day_clusters": sum(r["eligible_primary"] for r in rows), "eligible_contiguous_runs": runs_of_sessions([r["session_et"] for r in rows if r["eligible_primary"]], cal), "missingness_session_runs": runs_of_sessions([r["session_et"] for r in rows if r["missing_count"]], cal), "strata": groups, "windows": windows, "time_of_day": time_of_day, "integrity_totals": {k: total(k) for k in ["duplicates", "conflicting_timestamps", "raw_ordering_violations", "parse_errors", "invalid_ohlcv_rows", "zero_volume_rows", "zero_trade_rows", "outside_session_count", "extreme_review_rows"]}}


def comparisons(client, config, all_bars, cal, headers, days):
    """Auxiliary daily, ex-dividend, split-adjusted cross-feed QA only."""
    results = {}
    selected = set(days)
    # Request short contiguous calendar windows, not the years between them.
    daily = []
    groups = [sorted(d for d in days if d.startswith(prefix)) for prefix in sorted({d[:7] for d in days})]
    for group in filter(None, groups):
        a = dt.datetime.fromisoformat(group[0] + "T00:00:00").replace(tzinfo=ET)
        z = dt.datetime.fromisoformat(group[-1] + "T23:59:59").replace(tzinfo=ET)
        daily.extend(client.alpaca("daily_" + group[0], a, z, headers, "1Day", retain=True))
    by_day = defaultdict(list)
    for b in all_bars:
        by_day[timestamp(b["t"]).astimezone(ET).date().isoformat()].append(b)
    reconciliation = []
    for b in daily:
        day = timestamp(b["t"]).astimezone(ET).date().isoformat()
        if day not in selected:
            continue
        minute = sorted(by_day[day], key=lambda b: timestamp(b["t"]))
        last = minute[-1]
        reconciliation.append({"session_et": day, "daily_timestamp_utc": b["t"], "daily_close": b["c"], "session_last_minute_close": last["c"], "close_difference_usd": b["c"] - last["c"], "daily_trades": b.get("n"), "regular_minute_trades_sum": sum(x.get("n", 0) for x in minute), "daily_ge500": b.get("n", 0) >= 500, "daily_volume": b["v"], "regular_minute_volume_sum": sum(x["v"] for x in minute)})
    results["daily_reconciliation"] = reconciliation
    exday = config["ex_date"]
    if exday not in selected or config["massive_overlap"] not in selected:
        raise ValueError("D1 comparisons require configured ex-date and overlap; use a matching source config for a custom range")
    prev = prior_full(cal, exday)
    nextday = cal.next_session(exday).date().isoformat()
    checks = []
    idx, _, _ = indexed(all_bars)
    for day, start_hm, end_hm in [(prev, "15:59", "15:59"), (exday, "09:30", "09:34"), (nextday, "09:30", "09:34")]:
        start = dt.datetime.fromisoformat(day + "T" + start_hm + ":00").replace(tzinfo=ET)
        end = dt.datetime.fromisoformat(day + "T" + end_hm + ":59").replace(tzinfo=ET)
        for adjustment in ["raw", "dividend"]:
            aux = client.alpaca(f"ex_{day}_{adjustment}", start, end, headers, adjustment=adjustment, retain=True)
            for b in aux:
                t = timestamp(b["t"])
                split = idx[t][0]
                checks.append({"timestamp_utc": b["t"], "adjustment": adjustment, "split_close": split["c"], "diagnostic_close": b["c"], "close_ratio_to_split": b["c"] / split["c"], "max_abs_ohlc_difference_usd": max(abs(b[k] - split[k]) for k in ["o", "h", "l", "c"])})
    results["ex_dividend_comparison"] = checks
    results["split_boundary"] = config["split_boundary_status"]
    key = os.environ.get("MASSIVE_API_KEY")
    if key:
        day = config["massive_overlap"]
        start = cal.session_open(day).value // 1_000_000
        end = cal.session_close(day).value // 1_000_000 - 1
        endpoint = f"https://api.massive.com/v2/aggs/ticker/SPY/range/1/minute/{start}/{end}"
        data = client.get("massive_split_overlap", endpoint, {"adjusted": "true", "sort": "asc", "limit": 1000}, {"Authorization": "Bearer " + key}, retain=True)
        other = {dt.datetime.fromtimestamp(b["t"] / 1000, UTC): b for b in data.get("results", [])}
        alp = {timestamp(b["t"]): b for b in by_day[day]}
        common = sorted(set(other) & set(alp))
        results["massive_overlap"] = {"session_et": day, "alpaca_rows": len(alp), "massive_rows": len(other), "matched": len(common), "adjusted": data.get("adjusted"), "continuation_present": bool(data.get("next_url")), "tolerance_usd": config["price_tolerance_usd"], "fields": {k: {"max_abs_difference_usd": max((abs(alp[t][k] - other[t][k]) for t in common), default=None), "outside_tolerance": sum(abs(alp[t][k] - other[t][k]) > config["price_tolerance_usd"] for t in common)} for k in ["o", "h", "l", "c"]}, "feed_independence": "not established"}
    else:
        results["massive_overlap"] = {"status": "not configured"}
    return results


def main():
    """Bounded explicit pilot; cached rerun verifies inputs and performs no HTTP."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-config", type=Path, default=ROOT / "config/D1_spy_source.json")
    parser.add_argument("--data-root", type=Path, default=Path(os.environ.get("EBM_DATA_ROOT") or ROOT / "data"))
    parser.add_argument("--start", help="Optional bounded calendar date range (requires --end)")
    parser.add_argument("--end")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    config = json.loads(args.source_config.read_text())
    if (config["symbol"], config["feed"], config["adjustment"]) != ("SPY", "sip", "split"):
        raise ValueError("D1 requires SPY / sip / split; do not redesign the scientific source")
    if bool(args.start) != bool(args.end):
        raise ValueError("--start and --end must be supplied together")
    dates = sorted(config["sessions"])
    if args.start:
        cal = calendar(args.start, args.end)
        dates = [t.date().isoformat() for t in cal.sessions_in_range(args.start, args.end)]
    else:
        cal = calendar(dates[0], dates[-1])
    if not dates or len(dates) > config["max_sessions"]:
        raise ValueError("D1 bounds: 1 to max_sessions dates only; full D2 acquisition is not authorized")
    for day in dates:
        if not cal.is_session(day):
            raise ValueError(f"{day}: requested nontrading date")
    if not args.dry_run and not {config["ex_date"], config["massive_overlap"], cal.next_session(config["ex_date"]).date().isoformat()} <= set(dates):
        raise ValueError("D1 range must include configured ex-date, next session and overlap; use a matching source config for a different bounded pilot")
    anchors = sorted({prior_full(cal, d) for d in dates} - set(dates))
    artifact = Path("canonical/spy_minute") / config["dataset_id"] / "pilot.parquet"
    raw = Path("raw/alpaca") / config["dataset_id"]
    registry = args.data_root / "registry"
    out = registry / "D1_spy_source_manifest.json"
    identity = {"config_sha256": sha(args.source_config), "sessions": dates, "anchor_only_dates": anchors}
    plan = {**identity, "expected_session_minutes": sum(len(grid(cal, d)) for d in dates), "expected_anchor_rows": len(anchors), "data_root": str(args.data_root), "projected_candle_payload_bytes": (sum(len(grid(cal, d)) for d in dates) + len(anchors)) * 100, "free_disk_bytes": shutil.disk_usage(args.data_root if args.data_root.exists() else ROOT).free}
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return
    client = Client(args.data_root / raw, config)
    client.raw_dir.mkdir(parents=True, exist_ok=True)
    cached = out.exists()
    if cached:
        old = json.loads(out.read_text())
        if old["identity"] != identity or sha(args.data_root / artifact) != old["canonical"]["sha256"]:
            raise RuntimeError("D1 cached identity/hash mismatch; preserve data, inspect manifest")
        for ref in old.get("auxiliary_files", []):
            if sha(args.data_root / ref["path_relative_to_data_root"]) != ref["sha256"]:
                raise RuntimeError("D1 auxiliary hash mismatch; preserve input and inspect manifest")
        frame = pq.read_table(args.data_root / artifact).to_pylist()
        all_bars = [{"t": r["timestamp_utc"].isoformat(), **{k: r[v] for k, v in FIELDS.items()}, "_role": r["request_role"], "_day": r["requested_session"], "_request": r["source_request"]} for r in frame]
        comps = json.loads((client.raw_dir / "comparison_results.json").read_text())
    else:
        if (args.data_root / artifact).exists():
            raise RuntimeError("Unregistered canonical artifact exists; preserve and inspect before retry")
        headers = credentials()
        all_bars = []
        try:
            for day in dates + anchors:
                role = "full_session" if day in dates else "prior_anchor_only"
                start = cal.session_open(day).to_pydatetime() if role == "full_session" else cal.session_close(day).to_pydatetime() - dt.timedelta(minutes=1)
                end = cal.session_close(day).to_pydatetime() - dt.timedelta(seconds=1)
                name = "minute_" + day
                fetched = client.alpaca(name, start, end, headers)
                for b in fetched:
                    all_bars.append({**b, "_role": role, "_day": day, "_request": name})
            comps = comparisons(client, config, all_bars, cal, headers, dates)
            write_json(client.raw_dir / "comparison_results.json", comps)
            records = [{"symbol": "SPY", "timestamp_utc": timestamp(b["t"]), "session_et": timestamp(b["t"]).astimezone(ET).date(), "requested_session": b["_day"], "request_role": b["_role"], "source_request": b["_request"], **{v: b.get(k) for k, v in FIELDS.items()}} for b in all_bars]
            table = pa.Table.from_pylist(records)
            destination = args.data_root / artifact
            destination.parent.mkdir(parents=True, exist_ok=True)
            tmp = destination.with_suffix(".parquet.tmp")
            pq.write_table(table, tmp, compression="zstd")
            tmp.replace(destination)
        except Exception as exc:
            # Failure report retains no raw dumps or sensitive exception URLs.
            write_json(registry / "D1_spy_failure.json", {"status": "BLOCKED", "exception_type": type(exc).__name__, "safe_next_step": "Inspect ignored raw request ledger; preserve partial files; no automatic retries", "identity": identity})
            raise
    qa, clusters, missing = [], [], []
    for day in dates:
        row, gaps, minutes = audit_session(day, [b for b in all_bars if b["_day"] == day and b["_role"] == "full_session"], all_bars, cal, config)
        qa.append(row)
        clusters.extend(gaps)
        missing.extend(minutes)
    totals = aggregate(qa, clusters, missing, cal)
    totals["longest_gap"] = totals["top_10_gaps"][0] if totals["top_10_gaps"] else None
    totals["gap_distribution_bands"] = {name: sum(r[key] for r in qa) for name, key in [("singletons", "singleton_gaps"), ("length_2_4", "gaps_2_4"), ("length_5_9", "gaps_5_9"), ("length_ge10", "gaps_ge10")]}
    totals["maximum_eligible_run_sessions"] = max((r["length"] for r in totals["eligible_contiguous_runs"]), default=0)
    totals["maximum_consecutive_missingness_sessions"] = max((r["length"] for r in totals["missingness_session_runs"]), default=0)
    csv_write(registry / "D1_spy_candle_qa_sessions.csv", qa, list(qa[0]))
    csv_write(registry / "D1_spy_candle_gap_clusters.csv", clusters, ["session_et", "start_et", "end_et", "length", "affected_windows"])
    csv_write(registry / "D1_spy_missing_candles.csv", missing, ["session_et", "timestamp_et", "affected_windows"])
    write_json(registry / "D1_spy_candle_qa_summary.json", totals)
    # Keep sealed-date numeric outcome checks out of tracked summaries.
    if not cached:
        example = next(r["session_et"] for r in qa if r["eligible_primary"])
        write_json(client.raw_dir / "actual_anchor_check.json", anchor_check(example, all_bars, cal))
    blocked = (totals["affected_opening_full_sessions"] / totals["full_sessions"] > 0.02 or any(totals["integrity_totals"][k] for k in ["conflicting_timestamps", "parse_errors", "invalid_ohlcv_rows", "outside_session_count"]) or totals["affected_label_full_sessions"] > 0 or any(not r["prior_anchor_valid"] for r in qa if r["session_type"] == "full"))
    status = "BLOCKED" if blocked else "PASS WITH QUALIFICATIONS"
    auxiliary = [{"path_relative_to_data_root": p.relative_to(args.data_root).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(client.raw_dir.glob("*.json"))]
    manifest = {"dataset_id": config["dataset_id"], "status": status, "identity": identity, "symbol": "SPY", "feed": "sip", "adjustment": "split", "schema_version": 1, "timezone": "UTC", "bar_label": "start; interval left-inclusive, right-exclusive", "calendar": "XNYS", "canonical": {"path_relative_to_data_root": artifact.as_posix(), "bytes": (args.data_root / artifact).stat().st_size, "sha256": sha(args.data_root / artifact), "rows": len(all_bars), "observed_dates": sorted({timestamp(b["t"]).astimezone(ET).date().isoformat() for b in all_bars})}, "auxiliary_files": auxiliary, "source_lineage": "raw/alpaca/" + config["dataset_id"] + "/requests.json", "response_bodies_policy": "whole-session minute bodies hashed in ledger, transformed directly to sole canonical store; auxiliary diagnostics cached separately", "versions": {k: importlib.metadata.version(k) for k in ["exchange-calendars", "pandas", "numpy", "pyarrow", "tzdata"]}, "python": platform.python_version(), "observed_at_utc": old["observed_at_utc"] if cached else dt.datetime.now(UTC).isoformat(), "license_caveat": "Personal noncommercial research only; account and exchange agreements apply; no public redistribution", "config_evidence": config["ex_date_evidence"], "summary": {k: v for k, v in totals.items() if k not in ["time_of_day", "strata", "windows"]}, "cached_run": cached, "network_calls_this_run": client.network_calls, "wall_seconds_this_run": round(time.monotonic() - started, 3)}
    manifest["audit_code_sha256"] = {"src/ebm_research/experiment_b/pilot.py": sha(__file__), "scripts/d1_spy_pilot.py": sha(ROOT / "scripts/d1_spy_pilot.py")}
    manifest["scientific_spec_sha256"] = sha(ROOT / "docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md")
    write_json(out, manifest)
    print(json.dumps({"status": status, "sessions": len(dates), "canonical_rows": len(all_bars), "canonical_bytes": manifest["canonical"]["bytes"], "expected": totals["expected"], "observed": totals["observed_unique"], "missing": totals["missing"], "clusters": totals["gap_clusters"], "eligible_full_days": totals["eligible_day_clusters"], "network_calls": client.network_calls, "wall_seconds": manifest["wall_seconds_this_run"]}))


if __name__ == "__main__":
    main()
