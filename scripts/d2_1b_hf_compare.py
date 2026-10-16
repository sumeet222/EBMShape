"""Local candle reconciliation only; no scientific response/model evaluation."""
import csv
import datetime as dt
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from ebm_research.experiment_b.pilot import ROOT, ET, sha, write_json, csv_write


def calibration_factor(pregap, minimum=10):
    """Median reference/HF close ratio on pre-gap observed overlaps only."""
    if len(pregap) < minimum:
        return None
    ratios = pregap.close / pregap.Close
    if not (np.isfinite(ratios).all() and ratios.gt(0).all()):
        raise ValueError("Invalid pre-gap scale ratio")
    return float(ratios.median())


def discrepancies(joined, factor=1.0):
    """Level/range/volume and consecutive matched-minute return diagnostics."""
    if joined.empty:
        return {"matched_closes": 0}
    joined = joined.sort_values("key")
    result = {"matched_closes": len(joined)}
    for upper, lower in [("Open", "open"), ("High", "high"), ("Low", "low"), ("Close", "close")]:
        errors = (factor*joined[upper]/joined[lower]-1).abs()*1e4
        result.update({lower+"_median_bp": float(errors.median()), lower+"_p95_bp": float(errors.quantile(.95)), lower+"_max_bp": float(errors.max())})
    ratio = joined.Close/joined.close
    result.update(scale_ratio_variance=float(ratio.var(ddof=0)), scale_ratio_sd_bp=float(ratio.std(ddof=0)/ratio.median()*1e4), median_volume_ratio=float((joined.Volume/joined.volume).median()))
    consecutive = joined.key.diff().eq(pd.Timedelta(minutes=1))
    error = (np.log(joined.Close/joined.Close.shift())-np.log(joined.close/joined.close.shift())).abs()[consecutive]*1e4
    result.update(matched_return_pairs=len(error), return_p95_bp=float(error.quantile(.95)) if len(error) else None, return_max_bp=float(error.max()) if len(error) else None, range_difference_p95_bp=float((((joined.High-joined.Low)*factor-(joined.high-joined.low))/joined.close*1e4).abs().quantile(.95)))
    return result


def main():
    root = Path(os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    c = json.loads((ROOT / "config/D2_1b_hf_diagnostic.json").read_text())
    f = pd.read_parquet(root / "raw/diagnostics/D2_1b_hf_SPY_gap_context.parquet")
    m = json.loads((root / "registry/D2_spy_source_manifest.json").read_text())
    gaps = list(csv.DictReader((root / "registry/D2_spy_candle_gap_clusters.csv").open()))
    days = {g["session_et"] for g in gaps}
    original = pd.concat([pd.read_parquet(root / m["blocks"][str(y)]["canonical"]["path"]) for y in sorted({int(day[:4]) for day in days})])
    original = original[original.session_et.astype(str).isin(days)]
    extra = pd.read_parquet(root / "raw/diagnostics/D2_1b_alpaca_neighbors.parquet")
    reference = pd.concat([original, extra]).sort_values("timestamp_utc")
    if reference.duplicated(["symbol", "timestamp_utc"]).any():
        raise ValueError("Diagnostic neighbor/original key collision")
    results, timing = [], []
    for gap in gaps:
        day = gap["session_et"]
        start, end = pd.Timestamp(gap["start_et"]), pd.Timestamp(gap["end_et"])
        first = min(pd.Timestamp(g["start_et"]) for g in gaps if g["session_et"] == day)
        day_open, day_close = pd.Timestamp(day+"T09:30", tz=ET), pd.Timestamp(day+"T15:59", tz=ET)
        low, high = max(day_open, start-pd.Timedelta(minutes=20)), min(day_close, end+pd.Timedelta(minutes=20))
        for zone in ["America/New_York", "UTC"]:
            for shift in [-1, 0, 1]:
                hf = f.copy()
                hf["key"] = hf.datetime.dt.tz_localize(zone).dt.tz_convert("UTC")+pd.Timedelta(minutes=shift)
                calibration_join = hf.merge(reference, left_on="key", right_on="timestamp_utc")
                hf = hf[(hf.key >= low.tz_convert("UTC")) & (hf.key <= high.tz_convert("UTC")) | ((hf.key >= pd.Timestamp(day+"T14:35", tz=ET).tz_convert("UTC")) & (hf.key <= pd.Timestamp(day+"T14:54", tz=ET).tz_convert("UTC")) & (day == "2019-08-12"))]
                j = hf.merge(reference, left_on="key", right_on="timestamp_utc")
                raw = discrepancies(j)
                inferred = float((j.close/j.Close).median()) if len(j) else None
                aligned_diagnostic = discrepancies(j, inferred) if inferred else None
                timing.append({"session_et": day, "start_et": gap["start_et"], "zone_hypothesis": zone, "minute_shift_hypothesis": shift, "factor_for_timing_diagnostic_only": inferred, "raw": raw, "aligned": aligned_diagnostic})
                if zone != "America/New_York" or shift != 0:
                    continue
                pre = calibration_join[(calibration_join.key >= (first-pd.Timedelta(minutes=20)).tz_convert("UTC")) & (calibration_join.key < first.tz_convert("UTC"))]
                factor = calibration_factor(pre, c["minimum_neighboring_closes"])
                calibrated = discrepancies(j, factor) if factor else None
                holdout = j[~j.key.isin(pre.key)]
                validation = discrepancies(holdout, factor) if factor and len(holdout) else None
                proposed = hf[(hf.key >= start.tz_convert("UTC")) & (hf.key <= end.tz_convert("UTC"))]
                valid = (proposed[["Open", "High", "Low", "Close"]].gt(0).all(axis=1) & np.isfinite(proposed[["Open", "High", "Low", "Close", "Volume"]]).all(axis=1) & proposed.Volume.ge(0) & proposed.High.ge(proposed[["Open", "Close", "Low"]].max(axis=1)) & proposed.Low.le(proposed[["Open", "Close", "High"]].min(axis=1)))
                screen = bool(calibrated and validation and len(holdout) >= 10 and calibrated["close_median_bp"] <= c["median_absolute_level_bp_max"] and calibrated["close_p95_bp"] <= c["p95_absolute_level_bp_max"] and calibrated["return_p95_bp"] is not None and calibrated["return_p95_bp"] <= c["p95_absolute_log_return_difference_bp_max"] and all(calibrated[k+"_p95_bp"] <= 5 for k in ["open", "high", "low"]) and valid.all() and len(proposed))
                results.append({**gap, "candidate_rows": len(proposed), "candidate_invalid_rows": int((~valid).sum()), "source_labels": proposed.source.unique().tolist(), "pregap_calibration_rows": len(pre), "adjustment_factor": factor, "raw": raw, "calibrated": calibrated, "independent_holdout": validation, "numerical_screen_pass": screen, "accepted_rows": 0, "status": "PENDING_SOURCE_CONTRACT_REVIEW" if screen else "NO_ROWS_OR_RECONCILIATION_FAILURE", "clock_method": "ET bar-start hypothesis evaluated against UTC and +/-1 minute alternatives; not vendor-confirmed"})
    write_json(ROOT / "data/registry/D2_1b_hf_comparisons.json", {"script_sha256":sha(Path(__file__)), "config_sha256":sha(ROOT / "config/D2_1b_hf_diagnostic.json"), "clusters":results, "timing_hypotheses":timing, "accepted_rows":0, "note":"Diagnostic comparisons do not automatically authorize a patch"})
    print(json.dumps([{k:r.get(k) for k in ["session_et","start_et","length","candidate_rows","pregap_calibration_rows","adjustment_factor","calibrated","independent_holdout","numerical_screen_pass"]} for r in results],indent=2))


if __name__ == "__main__":
    main()
