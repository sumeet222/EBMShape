"""Offline D2.1 abstention audit. No candle source is altered or downloaded.

This stage found no candidate satisfying the prerequisite gates. Do not reuse
this abstention-only publisher to approve future patches; those need genuine
OHLCV, local reconciliation and an explicitly selected, collision-safe view.
"""
from collections import Counter
import csv
import datetime as dt
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import time

import pyarrow.parquet as pq

from ebm_research.experiment_b.acquisition import verify_files, verify_request_ledger
from ebm_research.experiment_b.pilot import ROOT, ET, timestamp, sha, write_json, csv_write


def clusters(rows):
    """Group exact missing UTC keys into maximal consecutive same-session runs."""
    groups = []
    ordered = sorted(rows, key=lambda r: (r["session_et"], timestamp(r["timestamp_utc"])))
    keys = {(r["session_et"], timestamp(r["timestamp_utc"])) for r in ordered}
    if len(keys) != len(ordered):
        raise ValueError("Duplicate missing-minute key")
    for row in ordered:
        t = timestamp(row["timestamp_utc"])
        if t.astimezone(ET).isoformat() != row["timestamp_et"]:
            raise ValueError("ET/UTC missing key disagreement")
        if not groups or groups[-1][-1]["session_et"] != row["session_et"] or t - timestamp(groups[-1][-1]["timestamp_utc"]) != dt.timedelta(minutes=1):
            groups.append([])
        groups[-1].append(row)
    return groups


def main():
    started, cpu_started = time.monotonic(), time.process_time()
    root = Path(os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    registry = root / "registry"
    manifest_path = registry / "D2_spy_source_manifest.json"
    baseline = json.loads(manifest_path.read_text())
    refs = [ref for block in baseline["blocks"].values() for ref in [block["canonical"], block["qa"]]] + baseline["published_quality_files"] + [baseline["request_ledger"]]
    verify_files(root, refs)
    verify_request_ledger(root, baseline)
    config_path = ROOT / "config/D2_1_hf_repair.json"
    config = json.loads(config_path.read_text())
    if baseline["identity"]["dataset_id"] != config["baseline_dataset_id"]:
        raise ValueError("Unexpected baseline identity")
    if sha(ROOT / "config/D2_spy_source.json") != baseline["identity"]["config_sha256"] or sha(ROOT / "docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md") != baseline["identity"]["scientific_spec_sha256"]:
        raise ValueError("Frozen scientific/config identity changed")
    read_csv = lambda name: list(csv.DictReader((registry / name).open()))
    missing = read_csv("D2_spy_missing_candles.csv")
    original_clusters = read_csv("D2_spy_candle_gap_clusters.csv")
    groups = clusters(missing)
    recomputed = {(g[0]["session_et"], g[0]["timestamp_utc"], g[-1]["timestamp_utc"], len(g)) for g in groups}
    saved = {(g["session_et"], g["start_utc"], g["end_utc"], int(g["length"])) for g in original_clusters}
    if recomputed != saved or len(missing) != 104 or len(groups) != 9:
        raise ValueError("Material D2 starting-gap difference; stop before any patch")
    keys = set()
    total_rows = 0
    for block in baseline["blocks"].values():
        table = pq.ParquetFile(root / block["canonical"]["path"]).read(columns=["symbol", "timestamp_utc"])
        part = {(r["symbol"], r["timestamp_utc"]) for r in table.to_pylist()}
        if len(part) != table.num_rows or keys.intersection(part):
            raise ValueError("Original candle-key collision")
        keys.update(part)
        total_rows += table.num_rows
    if total_rows != baseline["canonical_totals"]["rows"] or any(("SPY", timestamp(r["timestamp_utc"])) in keys for r in missing):
        raise ValueError("Retained D2 keys conflict with missing registry")
    sessions = read_csv("D2_spy_candle_qa_sessions.csv")
    full = [r for r in sessions if r["session_type"] == "full"]
    summary = json.loads((registry / "D2_spy_candle_qa_summary.json").read_text())
    for row in sessions:
        if int(row["observed_unique_regular"]) + int(row["missing_count"]) != int(row["expected_minutes"]):
            raise ValueError("Session expected/observed/missing accounting disagreement")
    if Counter(r["session_et"] for r in missing) != Counter({r["session_et"]: int(r["missing_count"]) for r in sessions if int(r["missing_count"])}):
        raise ValueError("Per-date missing registry mismatch")
    bool_count = lambda key: sum(r[key] == "True" for r in full)
    totals = {
        "expected_regular_minutes": sum(int(r["expected_minutes"]) for r in sessions),
        "observed_regular_minutes": sum(int(r["observed_unique_regular"]) for r in sessions),
        "missing_minutes": len(missing), "gap_clusters": len(groups), "affected_dates": len({r["session_et"] for r in missing}),
        "full_sessions": len(full), "early_close_excluded": len(sessions)-len(full),
        "full_session_complete": sum(int(r["missing_count"]) == 0 for r in full),
        "required_91_window_complete": bool_count("valid_required_window"),
        "opening_30_complete": sum(int(r["opening_valid_minutes"]) == 30 for r in full),
        "anchor_1529_valid": bool_count("anchor_1529_valid"), "anchor_1559_valid": bool_count("anchor_1559_valid"),
        "prior_full_anchor_valid": bool_count("prior_anchor_valid"), "primary_eligible_full_days": bool_count("eligible_primary"),
        "splits": summary["splits"], "canonical_rows": total_rows,
        "required_missing_minutes": sum(int(r["missing_required_window"]) for r in full),
    }
    assert totals["expected_regular_minutes"] == 1049610 and totals["primary_eligible_full_days"] == 2673
    assert not any(r["session_et"] >= "2024-01-01" for r in missing)
    candidates = [json.loads((ROOT / f"data/registry/D2_1_hf_candidate_{i}.json").read_text()) for i in [1, 2, 3]]
    evidence_paths = sorted((ROOT / "data/registry").glob("D2_1_hf_*.json"))
    evidence_paths = [p for p in evidence_paths if p.name != "D2_1_hf_repair_manifest.json"]
    evidence = [json.loads(p.read_text()) for p in evidence_paths]
    # Abstention is a prerequisite-gate result, not failed price comparisons.
    reasons = "P1_NO_DECLARED_LICENSE_NO_ROW_GROUP_PRUNING;P2_NAIVE_TIMESTAMPS_MIXED_LINEAGE_ADJUSTMENT_AND_UPSTREAM_RIGHTS_UNVERIFIED;P3_MANUAL_GATE_NO_AUTHORIZATION"
    decisions = [{**r, "symbol": "SPY", "decision": "UNRESOLVED_NOT_EXTRACTED", "candidate_rows_retrieved": 0, "accepted": False, "reason": reasons} for r in missing]
    decision_path = registry / "D2_1_hf_repair_decisions.csv"
    csv_write(decision_path, decisions, list(decisions[0]))
    comparisons = [{"session_et": g["session_et"], "start_et": g["start_et"], "end_et": g["end_et"], "original_missing_minutes": g["length"], "providers_attempted": ";".join(c["source"]["repository"] for c in candidates), "inspection_scope": "repository metadata; P1 June2023 footer; P2 stock SPY footer; P3 public metadata only", "candidate_rows_retrieved": 0, "matched_neighbor_closes": 0, "median_level_bp": None, "p95_level_bp": None, "max_level_bp": None, "p95_log_return_difference_bp": None, "scale_factor": None, "scale_ratio_variance": None, "accepted_rows": 0, "status": "NOT_RUN_PREREQUISITE_GATES", "reason": reasons, "boundary_note": "ONE_SIDED_TERMINAL_GAP" if g["end_et"][11:16] == "15:59" else "NO_CANDIDATE_CANDLES", "eligibility_recovered": False} for g in original_clusters]
    comparison_path = registry / "D2_1_hf_repair_comparisons.csv"
    csv_write(comparison_path, comparisons, list(comparisons[0]))
    references = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in evidence_paths]
    output = {
        "task_id": config["task_id"], "verdict": "NO FEASIBLE SOURCE", "implementation_qa": "PASS WITH QUALIFICATIONS",
        "observed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "data_root": "EBM_DATA_ROOT when set, otherwise repository data/", "using_default_data_root": root == ROOT / "data",
        "baseline_manifest": {"path": manifest_path.relative_to(root).as_posix(), "sha256": sha(manifest_path)},
        "baseline_files_unchanged": refs, "baseline_identity": baseline["identity"],
        "baseline_totals": totals, "empty_overlay_totals": totals, "restored_minutes": 0, "days_recovered": 0,
        "patch": None, "patch_sha256": None, "composite_dataset_materialized": False,
        "remaining_clusters": original_clusters, "persistent_primary_exclusions": [{"session_et": r["session_et"], "reason": r["exclusion_reasons"]} for r in full if r["eligible_primary"] != "True"],
        "candidate_rows_retrieved": 0, "accepted_rows": 0, "rejected_candle_rows": 0, "duplicate_candidate_rows": 0, "unresolved_unextracted_keys": len(missing),
        "source_gate_decisions": [
            {"repository": candidates[0]["source"]["repository"], "revision": candidates[0]["source"]["revision"], "status": "INELIGIBLE_RIGHTS_UNVERIFIED", "reason": "No license in card metadata or file listing; all26 row groups survive ticker min/max, projected332421407 bytes for all candidate columns; finer ticker/page extraction not attempted before rights gate"},
            {"repository": candidates[1]["source"]["repository"], "revision": candidates[1]["source"]["revision"], "declared_license": "mit", "status": "ABSTAIN_UNRECONCILED_SOURCE_CONTRACT", "reason": "Actual stock SPY schema has timezone-naive datetime, mixed pitrading/iex source; card UTC semantics insufficient; original price adjustments, bar labeling and upstream data rights not documented"},
            {"repository": candidates[2]["source"]["repository"], "revision": candidates[2]["source"]["revision"], "status": "INELIGIBLE_GATED", "reason": "gated=manual; anonymous README HTTP401; no configured HF token or authorized grant verified; no restricted data requested"}
        ],
        "timestamp_policy": "UTC aware bar starts only; naive candidate timestamps not localized or shifted", "adjustment_policy": "Baseline split only; no candidate calibration or adjustment performed",
        "license_policy": "No raw price publication; public metadata/footer evidence only; card license alone does not establish upstream provenance",
        "config": {"path": config_path.relative_to(ROOT).as_posix(), "sha256": sha(config_path)},
        "scripts": [{"path": p, "sha256": sha(ROOT / p)} for p in ["scripts/d2_1_hf_inspect.py", "scripts/d2_1_hf_audit.py"]],
        "environment": {"python": platform.python_version(), **{p: importlib.metadata.version(p) for p in ["pyarrow", "pandas", "exchange-calendars"]}},
        "evidence": references,
        "outputs": [{"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)} for p in [decision_path, comparison_path]],
        "resources": {"http_body_bytes_read": sum(r.get("downloaded_body_bytes", 0) for r in evidence), "wire_protocol_and_redirect_bytes": "unmeasured; body-byte count excludes headers/TLS/unread HTTP401 error body", "http_requests_attempted": sum(len(r.get("requests", [])) for r in evidence), "purposeful_acquisition_wall_seconds": sum(r.get("wall_seconds", 0) for r in evidence), "purposeful_acquisition_cpu_seconds": sum(r.get("cpu_seconds", 0) for r in evidence), "temporary_source_data_disk_bytes": 0, "peak_atomic_metadata_temporary_bytes": max(p.stat().st_size for p in evidence_paths), "retained_candle_bytes": 0, "free_disk_at_audit_bytes": shutil.disk_usage(ROOT).free},
        "errors": [{"evidence": p.relative_to(ROOT).as_posix(), "detail": r.get("error"), "http_errors": [e for e in r.get("requests", []) if e.get("error")]} for p, r in zip(evidence_paths, evidence) if r.get("error") or any(e.get("error") for e in r.get("requests", []))],
        "checks": {"registered_baseline_files_verified": len(refs), "unique_canonical_keys": total_rows, "gap_csv_matches_recomputed_clusters": True, "all_missing_keys_absent_from_canonical": True, "ET_UTC_keys_agree_with_ZoneInfo": True, "test_population_unchanged": True, "no_overlay_means_idempotent_baseline": True},
        "audit_wall_seconds": time.monotonic()-started, "audit_cpu_seconds": time.process_time()-cpu_started,
        "next_stage": "Separate Stage1 prompt should predeclare Alpaca-only D2 principal source view; use2673 eligible days with documented exclusions. No Stage1 work executed."
    }
    write_json(registry / "D2_1_hf_repair_manifest.json", output)
    print(json.dumps({"verdict": output["verdict"], "checks": output["checks"], "totals": totals, "resources": output["resources"]}))


if __name__ == "__main__":
    main()
