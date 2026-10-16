"""Publish the tiny locally reconciled sensitivity overlay and gap accounting."""
from collections import Counter
import csv
import datetime as dt
import json
import os
from pathlib import Path
import runpy

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from ebm_research.experiment_b.acquisition import verify_files
from ebm_research.experiment_b.pilot import ROOT, ET, sha, write_json, csv_write
from ebm_research.experiment_b.repair import load_minutes


def main():
    root = Path(os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    config = json.loads((ROOT / "config/D2_1b_hf_diagnostic.json").read_text())
    patch_id = config["repair_id"]
    destination = root / f"patches/B/{patch_id}.parquet"
    manifest_path = ROOT / "data/registry/D2_1b_hf_repair_manifest.json"
    if destination.exists() or manifest_path.exists():
        raise FileExistsError("Immutable overlay exists; reuse it")
    baseline_path = root / "registry/D2_spy_source_manifest.json"
    baseline = json.loads(baseline_path.read_text())
    refs = [ref for b in baseline["blocks"].values() for ref in [b["canonical"], b["qa"]]] + baseline["published_quality_files"] + [baseline["request_ledger"]]
    verify_files(root, refs)
    comparison_path = ROOT / "data/registry/D2_1b_hf_comparisons.json"
    comparisons = json.loads(comparison_path.read_text())
    extraction = json.loads((ROOT / "data/registry/D2_1b_hf_extraction.json").read_text())
    raw = root / extraction["extract"]["path"]
    if sha(raw) != extraction["extract"]["sha256"]:
        raise ValueError("Diagnostic extract hash changed")
    hf = pd.read_parquet(raw)
    hf["key"] = hf.datetime.dt.tz_localize(ET).dt.tz_convert("UTC")
    read_csv = lambda name: list(csv.DictReader((root / "registry" / name).open()))
    missing = read_csv("D2_spy_missing_candles.csv")
    missing_keys = {pd.Timestamp(r["timestamp_utc"]):r for r in missing}
    rows = []
    for g in comparisons["clusters"]:
        accepted = g["numerical_screen_pass"] and g["source_labels"] == ["pitrading"]
        g["accepted_rows"] = g["candidate_rows"] if accepted else 0
        g["decision"] = "ACCEPTED_LOCAL_ALIGNMENT" if accepted else ("UNAVAILABLE_AT_ALIGNED_CLOCK" if not g["candidate_rows"] else "REJECTED_LEVEL_AND_RETURN_SCREEN")
        g["terminal_uncertainty"] = g["end_et"][11:16] == "15:59"
        if not accepted:
            continue
        selected = hf[(hf.key >= pd.Timestamp(g["start_utc"])) & (hf.key <= pd.Timestamp(g["end_utc"]))]
        for _, row in selected.iterrows():
            t = row.key
            if t not in missing_keys or t.year >= 2024:
                raise ValueError("Nonmissing/test key cannot be repaired")
            factor = g["adjustment_factor"]
            rows.append({"symbol":"SPY", "timestamp_utc":t.to_pydatetime(), "session_et":t.tz_convert(ET).date(), **{k:float(row[k.capitalize()])*factor for k in ["open","high","low","close"]}, "volume":float(row.Volume), "trade_count":None, "vwap":None, "source_batch":"D2_1b_HF_group1", "role":"repair_missing_minute", "source_provider":"huggingface:valtermedeiros/ohlcv", "source_origin":row.source, "is_repaired":True, "repair_id":patch_id, "source_revision":extraction["revision"], "source_uri":extraction["remote_uri"], "source_row_group":1, "source_hash":extraction["extract"]["sha256"], "source_hash_kind":"retained_raw_context_parquet_sha256", "source_range_manifest_sha256":sha(ROOT / "data/registry/D2_1b_hf_extraction.json"), "source_adjustment":"vendor basis undocumented; locally aligned to Alpaca SIP split", "adjustment_method":"pre_gap_median_alpaca_over_hf_close", "adjustment_factor":factor, "calibration_rows":g["pregap_calibration_rows"], "scale_ratio_variance":g["calibrated"]["scale_ratio_variance"], "timestamp_method":"naive America/New_York bar start; empirical overlap validation across EST/EDT; no shift", "validation_status":"ACCEPTED_LOCAL_ALIGNMENT", "one_sided_terminal_gap":g["terminal_uncertainty"]})
    patch = pd.DataFrame(rows).sort_values("timestamp_utc")
    if len(patch) != 39 or patch.duplicated(["symbol","timestamp_utc"]).any():
        raise ValueError("Unexpected accepted-key count/conflict; inspect before writing")
    patch[["trade_count","vwap"]] = patch[["trade_count","vwap"]].astype("float64")
    destination.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pandas(patch, preserve_index=False), destination, compression="zstd")
    accepted = set(patch.timestamp_utc)
    remaining = [r for r in missing if pd.Timestamp(r["timestamp_utc"]) not in accepted]
    group_fn = runpy.run_path(str(ROOT / "scripts/d2_1_hf_audit.py"))["clusters"]
    groups = group_fn(remaining)
    sessions = read_csv("D2_spy_candle_qa_sessions.csv")
    full = [r for r in sessions if r["session_type"] == "full"]
    remaining_by_day = Counter(r["session_et"] for r in remaining)
    original_missing_by_day = Counter(r["session_et"] for r in missing)
    def anchor(day, time):
        return pd.Timestamp(day+"T"+time,tz=ET).tz_convert("UTC")
    eligible, recovered = [], []
    for r in full:
        day = r["session_et"]
        prior = r["prior_anchor_valid"] == "True" or anchor(r["prior_full_session"],"15:59") in accepted
        required = [x for x in remaining if x["session_et"] == day and x["affected_windows"] != "other"]
        now = not required and prior and int(r["invalid_unique_regular"]) == 0
        eligible.append((day,now))
        if now and r["eligible_primary"] != "True":
            recovered.append(day)
    totals = {"expected_regular_minutes":1049610, "observed_regular_minutes":1049506+len(patch), "missing_minutes":len(remaining), "remaining_clusters":len(groups), "remaining_dates":len(remaining_by_day), "full_session_complete":sum(remaining_by_day[r["session_et"]] == 0 for r in full), "required_91_complete":sum(not any(x["session_et"]==r["session_et"] and x["affected_windows"]!="other" for x in remaining) for r in full), "opening_30_complete":sum(not any(x["session_et"]==r["session_et"] and "opening_rv" in x["affected_windows"] for x in remaining) for r in full), "anchors_1529_valid":sum(not any(x["session_et"]==r["session_et"] and pd.Timestamp(x["timestamp_et"]).strftime("%H:%M")=="15:29" for x in remaining) for r in full), "anchors_1559_valid":sum(not any(x["session_et"]==r["session_et"] and pd.Timestamp(x["timestamp_et"]).strftime("%H:%M")=="15:59" for x in remaining) for r in full), "prior_anchor_valid":sum(r["prior_anchor_valid"]=="True" or anchor(r["prior_full_session"],"15:59") in accepted for r in full), "primary_eligible_full_days":sum(ok for _,ok in eligible), "recovered_primary_days":recovered, "early_close_excluded":21, "initial_prior_close_excluded":"2016-01-04", "train_eligible":sum(ok and day<"2022-01-01" for day,ok in eligible), "validation_eligible":sum(ok and "2022-01-01"<=day<"2024-01-01" for day,ok in eligible), "sealed_test_eligible":sum(ok and day>="2024-01-01" for day,ok in eligible)}
    decisions = [{**r,"symbol":"SPY","accepted":pd.Timestamp(r["timestamp_utc"]) in accepted,"decision":"ACCEPTED_LOCAL_ALIGNMENT" if pd.Timestamp(r["timestamp_utc"]) in accepted else next(g["decision"] for g in comparisons["clusters"] if g["start_utc"]<=r["timestamp_utc"]<=g["end_utc"] and g["session_et"]==r["session_et"])} for r in missing]
    csv_write(ROOT / "data/registry/D2_1b_hf_repair_decisions.csv",decisions,list(decisions[0]))
    csv_write(ROOT / "data/registry/D2_1b_hf_remaining_candles.csv",remaining,list(missing[0]))
    write_json(ROOT / "data/registry/D2_1b_hf_cluster_decisions.json",comparisons)
    patch_ref = {"path":destination.relative_to(root).as_posix(),"bytes":destination.stat().st_size,"sha256":sha(destination),"rows":len(patch)}
    manifest = {"dataset_id":patch_id,"view_definition":"Alpaca-only D2 UNION39 accepted HF rows; optional composite sensitivity, never default", "status":"PARTIAL", "baseline_manifest_sha256":sha(baseline_path), "baseline_files":refs, "patch":patch_ref,"remaining":remaining,"totals":totals,"candidate_rows":43,"accepted_rows":39,"rejected_rows":4,"unavailable_rows":61,"revision":extraction["revision"],"license":"Repository-declared MIT for private research; upstream redistribution rights not independently established; no price publication", "source_clock":"Empirically ET bar starts for accepted pitrading rows, tested EST and EDT; vendor card UTC claim is not accepted", "adjustment":"Locally estimated multiplicative factors from20 genuinely overlapping pre-gap closes per accepted date; no volume scaling; no claimed known split/dividend factor", "terminal_review":{"date":"2019-08-12","one_sided":True,"pre_overlap":"15:09–15:28 ET","separated_overlap":"14:35–14:54 ET","only_later_original_minute":"15:31 ET","max_close_discrepancy_bp":5.652459437932578,"max_high_discrepancy_bp":6.026395648495164,"mixed_1531_1532_boundary_log_bp":4.208693500078056,"hf_only_boundary_log_bp":-1.4421690247096535,"decision":"Accept with one-sided uncertainty flag: p95 screens pass; source closing rows internally valid with positive volume and nonconstant observed prices; boundary discrepancy retained transparently, original15:31 never replaced"}, "trade_count_vwap":"Null in HF repair rows; no fabricated Alpaca fields. Primary RV/return inputs require OHLC; source trade-count diagnostics must retain missing provenance", "scientific_work":"None; no model, outcome correlation, test returns, or state-cutoff fitting", "scripts":[{"path":s,"sha256":sha(ROOT/s)} for s in ["scripts/d2_1b_hf_extract.py","scripts/d2_1b_alpaca_neighbors.py","scripts/d2_1b_hf_compare.py","scripts/d2_1b_hf_overlay.py","src/ebm_research/experiment_b/repair.py"]], "config_sha256":sha(ROOT / "config/D2_1b_hf_diagnostic.json")}
    write_json(manifest_path,manifest)
    original = load_minutes(root)
    once = load_minutes(root,manifest_path)
    twice = load_minutes(root,manifest_path)
    pd.testing.assert_frame_equal(once,twice)
    if len(original)!=243804 or len(once)!=243843 or len(once[once.is_repaired])!=39:
        raise ValueError("Overlay loader count failure")
    verify_files(root,refs)
    manifest["qa"]={"default_rows":len(original),"composite_rows":len(once),"repaired_rows":39,"loader_twice_equal":True,"original_registered_files_unchanged":len(refs),"test_rows_unchanged":len(original[original.timestamp_utc.dt.year>=2024])==len(once[once.timestamp_utc.dt.year>=2024])}
    write_json(manifest_path,manifest)
    print(json.dumps({"patch":patch_ref,"totals":totals,"qa":manifest["qa"]},indent=2))


if __name__ == "__main__":
    main()
