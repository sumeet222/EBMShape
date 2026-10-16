"""Explicitly selected minute overlays; the default reader remains Alpaca only."""
import csv
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from .acquisition import verify_files
from .pilot import ROOT, sha


def merge_overlay(original, patch, allowed_missing):
    """Union accepted genuine rows only, rejecting duplicates or original overlap."""
    keys = ["symbol", "timestamp_utc"]
    if original.duplicated(keys).any() or patch.duplicated(keys).any():
        raise ValueError("Duplicate source/patch key; no overlay applied")
    original_keys = set(zip(original.symbol, original.timestamp_utc))
    patch_keys = set(zip(patch.symbol, patch.timestamp_utc))
    if patch_keys.intersection(original_keys):
        raise ValueError("Patch collides with original Alpaca key; never overwrite")
    if not patch_keys.issubset(allowed_missing):
        raise ValueError("Patch contains a key not originally missing")
    if not patch.empty:
        if not patch.validation_status.eq("ACCEPTED_LOCAL_ALIGNMENT").all():
            raise ValueError("Unaccepted repair row")
        t = pd.to_datetime(patch.timestamp_utc)
        if str(t.dt.tz) != "UTC" or (t.dt.year >= 2024).any():
            raise ValueError("Expected aware UTC pre-test patch keys")
        ohlcv = patch[["open", "high", "low", "close", "volume"]]
        valid = (np.isfinite(ohlcv).all(axis=1) & ohlcv[["open", "high", "low", "close"]].gt(0).all(axis=1) & patch.volume.ge(0) & patch.high.ge(patch[["open", "close", "low"]].max(axis=1)) & patch.low.le(patch[["open", "close", "high"]].min(axis=1)))
        if not valid.all():
            raise ValueError("Invalid repaired OHLCV")
    return pd.concat([original, patch], ignore_index=True).sort_values(keys).reset_index(drop=True)


def load_minutes(data_root=None, repair_manifest=None):
    """Load frozen D2, optionally union an explicitly provided approved manifest.

    No repaired source is auto-discovered. A public clone requires authorized
    original source files. This small SPY-only loader creates no disk copy.
    """
    root = Path(data_root or os.environ.get("EBM_DATA_ROOT", ROOT / "data")).expanduser().resolve()
    baseline_path = root / "registry/D2_spy_source_manifest.json"
    baseline = json.loads(baseline_path.read_text())
    verify_files(root, [b["canonical"] for b in baseline["blocks"].values()])
    original = pd.concat([pd.read_parquet(root / b["canonical"]["path"]) for b in baseline["blocks"].values()], ignore_index=True)
    original = original.assign(source_provider="alpaca", is_repaired=False, repair_id=None, source_adjustment="split")
    if repair_manifest is None:
        return original.sort_values(["symbol", "timestamp_utc"]).reset_index(drop=True)
    m = json.loads(Path(repair_manifest).read_text())
    if sha(baseline_path) != m["baseline_manifest_sha256"]:
        raise ValueError("Overlay's baseline manifest identity changed")
    missing_ref = next(r for r in baseline["published_quality_files"] if r["path"] == "registry/D2_spy_missing_candles.csv")
    verify_files(root, [missing_ref])
    verify_files(root, [m["patch"]])
    patch = pd.read_parquet(root / m["patch"]["path"])
    missing = list(csv.DictReader((root / "registry/D2_spy_missing_candles.csv").open()))
    allowed = {("SPY", pd.Timestamp(r["timestamp_utc"])) for r in missing}
    return merge_overlay(original, patch, allowed)
