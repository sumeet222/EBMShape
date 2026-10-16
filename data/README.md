# Shared research data

One physical store serves A and B. Set `EBM_DATA_ROOT` to an authorized external storage root for future acquisition, otherwise use repository-relative `data/`. D0 diagnostics intentionally use this repository's ignored `data/raw/diagnostics/`; the diagnostic scripts do not implement `EBM_DATA_ROOT` routing. See `docs/canonical_data_layout.md` for the future acquisition contract.

Git contains instructions and hashed manifests, not licensed input rows. No canonical dataset has been built. Empty canonical directories are created locally and ignored; an acquisition command must create its own parents on a fresh clone.

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
