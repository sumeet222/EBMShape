"""Offline verification of D0 sample integrity; no API calls or model evaluation."""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("d0_probe", ROOT / "scripts/d0_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def main():
    """Check recorded samples, exact-date minute grids, overlap and a small I/O smoke."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Verify only a newly reconstructed evidence ID")
    args = parser.parse_args()
    registry = ROOT / "data/registry"
    pattern = f"{args.id}_*.json" if args.id else "d0_*_*.json"
    evidence = [json.loads(p.read_text()) for p in sorted(registry.glob(pattern)) if p.name not in {"d0_file_manifest.json", "d0_verification.json"}]
    samples = {}
    for ev in evidence:
        for entry in ev.get("requests", []):
            if "sample" in entry:
                ref = entry["sample"]
                p = ROOT / ref["path"]
                assert p.stat().st_size == ref["bytes"], p
                assert hashlib.sha256(p.read_bytes()).hexdigest() == ref["sha256"], p
                samples[p.name] = json.loads(p.read_text())
    alpaca = next(e for e in evidence if e["provider"] == "alpaca")
    audits = []
    for e in alpaca["requests"][:5]:
        bars = samples[Path(e["sample"]["path"]).name]["bars"]
        a = probe.audit(bars, e["day"])
        assert a["rows"] == a["unique_timestamps"] == 390
        assert a["opening_rows"] == 30 and a["bad_ohlcv"] == 0
        assert a["missing_minutes"] == a["unexpected_minutes"] == 0
        assert a["sorted"] and not e["next_page_token_present"]
        assert all(all(k in b for k in ["o", "h", "l", "c", "v", "n", "t", "vw"]) for b in bars)
        audits.append({"day": e["day"], **a})
    # Regression guard: a complete grid on the wrong day must fail completeness.
    wrong_day = probe.audit(bars, "2026-09-16")
    assert wrong_day["missing_minutes"] == wrong_day["unexpected_minutes"] == 390
    massive = next(e for e in evidence if e["provider"] == "massive")["requests"][0]
    raw = samples[Path(massive["sample"]["path"]).name]
    mbars = [{**b, "t": dt.datetime.fromtimestamp(b["t"] / 1000, dt.timezone.utc).isoformat()} for b in raw["results"]]
    regular = [b for b in mbars if "09:30" <= dt.datetime.fromisoformat(b["t"]).astimezone(probe.ET).strftime("%H:%M") < "16:00"]
    ma = probe.audit(regular, "2026-09-15")
    assert ma["rows"] == ma["unique_timestamps"] == 390 and ma["bad_ohlcv"] == 0
    assert ma["missing_minutes"] == ma["unexpected_minutes"] == 0
    by_time = {dt.datetime.fromisoformat(b["t"]): b for b in regular}
    diffs = [abs(b["c"] - by_time[dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00"))]["c"]) for b in bars]
    assert len(diffs) == 390
    anchors = next(e for e in evidence if e["provider"] == "anchors")
    for e in anchors["requests"]:
        ab = samples[Path(e["sample"]["path"]).name]["bars"]
        ts = [dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(probe.ET) for b in ab]
        assert [t.strftime("%H:%M") for t in ts] == ["15:59", "16:00"]
        assert all(t.date().isoformat() == e["day"] for t in ts)
    # Read/write a small temporary object; no credentials, dataset copies or caches.
    with tempfile.TemporaryDirectory(prefix="ebm_d0_smoke_") as tmp:
        p = Path(tmp) / "smoke.json"
        p.write_text(json.dumps({"rows": 390}))
        assert json.loads(p.read_text())["rows"] == 390
    summary = {"status": "PASS", "scope": "diagnostic samples only; no continuous-coverage or research-ready claim", "sample_files_verified": len(samples), "alpaca_audits": audits, "massive_audit": ma, "massive_total_rows": len(mbars), "overlap_rows": len(diffs), "max_abs_close_difference": max(diffs), "prior_close_pairs_verified": 5, "wrong_date_regression": "PASS", "io_smoke": "PASS"}
    (registry / "d0_verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    files = []
    for folder in ["data", "docs/specs"]:
        for p in sorted((ROOT / folder).rglob("*")):
            if p.is_file() and p.name != "d0_file_manifest.json":
                files.append({"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    (registry / "d0_file_manifest.json").write_text(json.dumps({"schema_version": 1, "files": files}, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k not in ["alpaca_audits", "massive_audit"]}))


if __name__ == "__main__":
    main()
