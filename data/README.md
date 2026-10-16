# Shared research data

One physical store serves A and B. Set `EBM_DATA_ROOT` to an authorized external storage root for future acquisition, otherwise use repository-relative `data/`. D0 diagnostics intentionally use this repository's ignored `data/raw/diagnostics/`; the diagnostic scripts do not implement `EBM_DATA_ROOT` routing. See `docs/canonical_data_layout.md` for the future acquisition contract.

Git contains instructions and hashed manifests, not licensed input rows. **D2 now freezes the authoritative B history (2016-01-04–2026-09-30): 11 annual Parquets, 243,804 required-window rows, 8,975,163 bytes.** See [D2 report](../reports/shared/D2_full_spy_sip_acquisition_and_candle_quality.md), `registry/D2_spy_source_manifest.json` and per-session QA for the seven ineligible full days and half-day exclusions. D0/D1 text below describes historical diagnostics. D0 created no canonical data; D1 now adds one bounded split-adjusted SPY pilot (4,113 rows, 152,721 bytes). See [D1 report](../reports/shared/D1_spy_sip_pilot_and_candle_audit.md) and `registry/D1_spy_source_manifest.json` for setup, audit and restoration. The diagnostic commands below describe D0; D1 uses the installed package and environment credentials. Acquisition commands create their own data directories on a fresh clone.

- `raw/diagnostics/`: 15 immutable, bounded provider response files (304,952 bytes); restore via the commands below with a **new** ID, subject to current access.
- `registry/`: public metadata, request parameters without secrets, sample references/hashes and offline QA evidence.
- `canonical/stocks_monthly/`: reserved for A's historical security-month source; never substitute current shares or survivor-only OHLCV.
- `canonical/spy_minute/`: reserved for B's SPY minute store with explicit feed, split policy, UTC bar starts and ET sessions.
- Future `derived/A/` and `derived/B/`: one reusable model table each. Folds store row keys/date masks, not input copies.

## Reproduce only the bounded diagnostics

Python 3.14.6 was used; standard library only, no package installation. Python >=3.10 with IANA timezone data is required. On systems without timezone data install `tzdata`. Copy `.env.example` to local `.env` and privately populate the three provider keys, or export them. Never overwrite an existing `.env`.

```sh
python3 -B scripts/d0_probe.py --help
python3 -B scripts/d0_verify.py
```

The offline check requires the local ignored diagnostic samples whose paths/hashes are in `data/registry/d0_file_manifest.json`. It intentionally fails when they are absent. An authorized fresh clone can reconstruct observations (not necessarily historical bytes, since vendors revise data) with:

```sh
python3 -c "from pathlib import Path; [Path(p).mkdir(parents=True, exist_ok=True) for p in ['data/registry','data/raw/diagnostics']]"
python3 -B scripts/d0_probe.py alpaca --id NEW_UNIQUE_ID
python3 -B scripts/d0_probe.py massive --id NEW_UNIQUE_ID
python3 -B scripts/d0_probe.py anchors --id NEW_UNIQUE_ID
python3 -B scripts/d0_probe.py public --id NEW_UNIQUE_ID
python3 -B scripts/d0_probe.py details --id NEW_UNIQUE_ID
python3 -B scripts/d0_probe.py hf-range --id NEW_UNIQUE_ID
python3 -B scripts/d0_verify.py --id NEW_UNIQUE_ID
```

`d0_verify.py --id NEW_UNIQUE_ID` selects a reconstructed evidence set; omit `--id` for the recorded D0 set. Inspect existing evidence before any network rerun; do not accumulate/reprobe sets blindly. `--id` protects prior outputs rather than providing a general acquisition cache. Each response is capped at 2 MB, one attempt, 20-second timeout. No pagination or bulk acquisition is implemented. WRDS requires separate authorized CRSP/Compustat permissions and secure authentication; no login was attempted. Public availability of an archive does not establish redistribution rights.


## D2 restore and safe resume

Use the existing `requirements-d1.lock.txt` and editable package install; no new dependency is required. Export authorized `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` privately. The runner reads environment only.

```sh
.venv/bin/python -B scripts/d2_spy_acquire.py --dry-run
.venv/bin/python -B scripts/d2_spy_acquire.py --verify-only
# New authorized snapshot in an empty configured data root:
.venv/bin/python -B scripts/d2_spy_acquire.py --data-root PATH --max-years 1
.venv/bin/python -B scripts/d2_spy_acquire.py --data-root PATH --resume
```

`--data-root` overrides `EBM_DATA_ROOT`, otherwise repository `data/`. Restore registered ignored files from an authorized backup before `--verify-only`; manifests alone do not restore data. A fresh vendor snapshot may differ, so use a new data root and preserve original provenance. Resume verifies/skips completed annual source/QA files; legitimate appended request-ledger records are allowed but a changed committed prefix is rejected. Preserve orphan/hash-conflicting files for inspection. Do not re-download a verified source to reproduce a model fold, and do not create copied train/test or full-day-plus-window stores. Stage 1's daily scientific table is a separate future task.
