"""Bounded D0 diagnostics; standard library only, no full-dataset acquisition."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
DATES = ["2016-01-05", "2019-07-15", "2023-07-17", "2024-07-15", "2026-09-15"]
MAX_BYTES = 2_000_000


def credentials():
    """Read simple local key=value credentials without printing values."""
    values = dict(os.environ)
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            s = line.strip().removeprefix("export ")
            if s and not s.startswith("#") and "=" in s:
                k, v = s.split("=", 1)
                values.setdefault(k.strip(), v.strip().strip("\"'"))
    return values


def request(url, params=None, headers=None):
    """Fetch at most 2 MB, returning sanitized status and parsed public/body data."""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=20) as r:
            body = r.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                return {"status": r.status, "error": "response exceeded 2 MB cap; not retained"}
            try:
                data = json.loads(body)
            except ValueError:
                data = body.decode(errors="replace")
            return {"status": r.status, "bytes": len(body), "data": data}
    except urllib.error.HTTPError as e:
        # Avoid echoing URLs (which can contain keys) or arbitrary provider error text.
        return {"status": e.code, "error": "HTTP error; no retry"}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"status": None, "error": type(e).__name__}


def audit(bars, day):
    """Check exactly 390 bar-start minutes in a requested full regular session."""
    stamps = [dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(ET) for b in bars]
    start = dt.datetime.fromisoformat(day + "T09:30:00").replace(tzinfo=ET)
    expected = {start + dt.timedelta(minutes=i) for i in range(390)}
    actual = set(stamps)
    return {"rows": len(bars), "unique_timestamps": len(actual),
            "first_et": stamps[0].isoformat() if stamps else None,
            "last_et": stamps[-1].isoformat() if stamps else None,
            "missing_minutes": len(expected - actual),
            "unexpected_minutes": len(actual - expected),
            "sorted": stamps == sorted(stamps),
            "opening_rows": sum(t.hour == 9 and t.minute >= 30 for t in stamps),
            "bad_ohlcv": sum(not (0 < b["l"] <= min(b["o"], b["c"]) <= max(b["o"], b["c"]) <= b["h"] and b["v"] >= 0) for b in bars),
            "fields": sorted(bars[0]) if bars else []}


def main():
    """Run named bounded probe and exclusively create a versioned evidence file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", choices=["alpaca", "massive", "public", "details", "anchors", "hf-range"])
    parser.add_argument("--id", required=True, help="Unique evidence ID; existing outputs are protected")
    args = parser.parse_args()
    out = ROOT / "data/registry" / f"{args.id}_{args.provider}.json"
    if out.exists():
        raise FileExistsError(out)
    c = credentials()
    started = time.monotonic()
    result = {"observed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "python": platform.python_version(), "provider": args.provider, "requests": []}
    if args.provider == "hf-range":
        url = "https://huggingface.co/datasets/mito0o852/OHLCV-1m/resolve/776328445b7ac6e7815ef3a483e9c8ded1eb6d56/data/ohlcv_2026-03.parquet"
        result["requests"].append({"url": url, "range": "bytes=0-3", **request(url, headers={"Range": "bytes=0-3"})})
    elif args.provider == "anchors":
        headers = {"APCA-API-KEY-ID": c["APCA_API_KEY_ID"], "APCA-API-SECRET-KEY": c["APCA_API_SECRET_KEY"]}
        for day in ["2016-01-04", "2019-07-12", "2023-07-14", "2024-07-12", "2026-09-14"]:
            start = dt.datetime.fromisoformat(day + "T15:59:00").replace(tzinfo=ET)
            params = {"timeframe": "1Min", "start": start.isoformat(), "end": start.replace(hour=16, minute=0, second=59).isoformat(), "feed": "sip", "adjustment": "raw", "limit": 10}
            result["requests"].append({"day": day, "params": params, **request("https://data.alpaca.markets/v2/stocks/SPY/bars", params, headers)})
    elif args.provider == "alpaca":
        key, secret = c.get("APCA_API_KEY_ID"), c.get("APCA_API_SECRET_KEY")
        result["credentials_present"] = bool(key and secret)
        if key and secret:
            headers = {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}
            for day in DATES:
                start = dt.datetime.fromisoformat(day + "T09:30:00").replace(tzinfo=ET)
                end = start.replace(hour=15, minute=59, second=59)
                params = {"timeframe": "1Min", "start": start.isoformat(), "end": end.isoformat(), "limit": 10000, "feed": "sip", "adjustment": "raw", "sort": "asc"}
                r = request("https://data.alpaca.markets/v2/stocks/SPY/bars", params, headers)
                entry = {"day": day, "params": params, "status": r.get("status"), "bytes": r.get("bytes"), "error": r.get("error")}
                if r.get("status") == 200 and isinstance(r.get("data"), dict):
                    bars = r["data"].get("bars") or []
                    entry["audit"] = audit(bars, day)
                    entry["next_page_token_present"] = bool(r["data"].get("next_page_token"))
                    p = ROOT / "data/raw/diagnostics" / f"{args.id}_alpaca_SPY_{day}_sip_raw.json"
                    with p.open("x") as f:
                        json.dump(r["data"], f, separators=(",", ":"))
                    entry["sample"] = {"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                result["requests"].append(entry)
                if r.get("status") in [401, 403, 429] or r.get("status") is None:
                    break
            # Five opening bars only: observe raw/split/dividend/all differences.
            if result["requests"] and result["requests"][-1]["status"] == 200:
                for adjustment in ["raw", "split", "dividend", "all"]:
                    params = {"timeframe": "1Min", "start": "2024-07-15T09:30:00-04:00", "end": "2024-07-15T09:34:59-04:00", "feed": "sip", "adjustment": adjustment, "limit": 10}
                    r = request("https://data.alpaca.markets/v2/stocks/SPY/bars", params, headers)
                    result["requests"].append({"kind": "adjustment_diagnostic", "params": params, **r})
    elif args.provider == "massive":
        key = c.get("MASSIVE_API_KEY") or c.get("POLYGON_API_KEY")
        result["credentials_present"] = bool(key)
        if key:
            r = request("https://api.massive.com/v2/aggs/ticker/SPY/range/1/minute/2026-09-15/2026-09-15", {"adjusted": "false", "sort": "asc", "limit": 2000}, {"Authorization": "Bearer " + key})
            result["requests"].append({"day": "2026-09-15", "adjusted": False, **r})
    elif args.provider == "details":
        urls = [
            "https://www.kaggle.com/api/v1/datasets/view/rockinbrock/spy-1-minute-data",
            "https://www.kaggle.com/api/v1/datasets/list/rockinbrock/spy-1-minute-data",
            "https://www.kaggle.com/api/v1/datasets/view/gratefuldata/intraday-stock-data-1-min-sp-500-200821",
            "https://www.kaggle.com/api/v1/datasets/list/gratefuldata/intraday-stock-data-1-min-sp-500-200821",
            "https://www.kaggle.com/api/v1/datasets/view/cesarecastro/cleaned-spy-and-qqq-1-minute-data",
            "https://www.kaggle.com/api/v1/datasets/list/cesarecastro/cleaned-spy-and-qqq-1-minute-data",
            "https://datasets-server.huggingface.co/filter?dataset=mito0o852%2FOHLCV-1m&config=default&split=train&where=%22ticker%22%3D%27SPY%27&length=1",
        ]
        for url in urls:
            result["requests"].append({"url": url, **request(url)})
    else:
        urls = [
            "https://huggingface.co/api/datasets/mito0o852/OHLCV-1m",
            "https://huggingface.co/api/datasets/mito0o852/OHLCV-1m/tree/main?recursive=true&limit=1000",
            "https://huggingface.co/datasets/mito0o852/OHLCV-1m/raw/main/README.md",
            "https://www.kaggle.com/api/v1/datasets/list?search=SPY%201%20minute&pageSize=5",
        ]
        for url in urls:
            result["requests"].append({"url": url, **request(url)})
    # Licensed rows stay in ignored raw storage; tracked evidence holds references.
    for i, entry in enumerate(result["requests"]):
        if args.provider in {"alpaca", "massive", "anchors"} and "data" in entry:
            p = ROOT / "data/raw/diagnostics" / f"{args.id}_{args.provider}_response_{i}.json"
            with p.open("x") as f:
                json.dump(entry.pop("data"), f, separators=(",", ":"))
            entry["sample"] = {"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    result["wall_seconds"] = round(time.monotonic() - started, 3)
    with out.open("x") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({"path": out.relative_to(ROOT).as_posix(), "statuses": [r.get("status") for r in result["requests"]], "wall_seconds": result["wall_seconds"]}))


if __name__ == "__main__":
    main()
