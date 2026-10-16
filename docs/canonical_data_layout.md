# Canonical data layout — D0 operational contract

D0 status: layout established; no canonical source or model table materialized at D0. **D1 now adds the bounded canonical pilot described below.** The approved v1 A/B specifications are preserved under `docs/specs/`; original `ResearchSpec/` files remain intact. This document sets storage semantics, not a new scientific protocol.

## One shared physical root

Future acquisition resolves `Path(os.environ.get("EBM_DATA_ROOT") or PROJECT_ROOT / "data")`; no user-specific absolute paths. A local external path is private configuration, never a required symlink. D0 probe output remains under repository `data/` as documented in `data/README.md`.

| Location below data root | Contents and identity | Key / consumers |
|---|---|---|
| `raw/<provider>/<extract_id>/` | One immutable authorized extract, minimal columns/windows; original responses or source Parquet, never per-model copies | Manifest identifies content hashes and request/source revision |
| `raw/diagnostics/` | Existing 15 D0 response samples, diagnostic only | Do not promote raw-adjustment probes to split-adjusted research data |
| `canonical/stocks_monthly/<dataset_id>/` | A only: stable security-month source, annual Parquet partitions if useful | `(security_id, month_end)`; A assembly and source benchmarks |
| `canonical/spy_minute/<dataset_id>/` | B only: SPY, UTC minute starts and explicit ET session; annual Parquet partitions | `(symbol, timestamp_utc)`; B daily assembly |
| `derived/A/<dataset_id>.parquet` | One compact reusable formation-to-target monthly table | `(security_id, formation_month)` with `target_month=formation_month+1` |
| `derived/B/<dataset_id>.parquet` | One compact eligible SPY session table | `(symbol, session_et)` |
| `registry/` | Small tracked manifests, hashes, schema versions, provenance, QA and external references | All consumers |

Raw and canonical serve distinct purposes; do not retain two equivalent whole-data encodings without measured value. If an authorized raw columnar source already meets canonical semantics, the canonical dataset can be a manifest reference, with no copy. New immutable partitions only for new/corrected observations; obsolete generated versions require a documented retirement decision. No copied train/test files, seed-specific input tables or full inputs in `artifacts/`.

## A source and model schema

Retain source-native identity and documented units: `security_id` (PERMNO when authorized), PERMCO if needed, `month_end`, historical ticker, dated exchange/share/SIC classifications, monthly `ret`, `retx` where available, price, share volume, historical shares, adjustment factors, distribution events and delisting events/returns. Preserve missing/status codes before normalization. Market cap is formation price magnitude times historical shares in documented units; retain a vendor value if supplied and reconcile it. Never assume old CRSP unit multipliers in a new schema.

A's derived row explicitly carries `formation_month=s`, `target_month=s+1`, formation total return, turnover, formation cap, target total return and eligibility/source flags. Form turnover from contemporaneous volume/shares. Combine separate delisting return only after schema-specific verification against double counting. Accounting controls are optional and separate: use genuine historical Compustat data and dated CCM links, with the specification's availability lags. No A/B population pooling. A sealed target-month test remains 2023-01–2026-09.

## B source and model schema

Proposed columns: `symbol:string`, `timestamp_utc:timestamp[UTC]`, `session_et:date`, `open/high/low/close:float64`, `volume:numeric` (do not truncate fractional values), optional `trade_count:int64`, `vwap:float64`, dataset/source flags. A timestamp is a **bar start**. Preserve source timestamp precision and source revision in the manifest. No silent feed merges.

Canonical price convention follows B v1: **split-adjusted, without implicit dividend adjustment**. Alpaca `adjustment=split` maps to Massive `adjusted=true`; D0's full sessions were `raw` and are explicitly diagnostic. Dividend-adjusted and raw extracts have distinct IDs and cannot be stitched into the same series. Changes to adjustment factors require versioned provenance, not silent rewrites.

B needs 09:30–09:59 opening bars, 14:59 anchor, 15:00–15:59 closing bars, and prior eligible session 15:59 close: about 91 retained minutes per full session (prior close reused from that same store). Request boundaries must include 14:59. Half-days have no primary closing target and must be excluded with calendar reasons; their treatment as a preceding-session anchor must follow the approved full-session-anchor rule, never silently invent a 16:00 price. Use a real U.S. exchange calendar in acquisition/assembly; D0's five ordinary dates are not a general calendar implementation.

`P10=C09:59`, `P15=C14:59`, `P1530=C15:29`, `P16=C15:59`; `Pprev` is prior permissible regular-session close. `r1=P10/Pprev-1`, `r12=P1530/P15-1`, `r13=P16/P1530-1`. Opening RV is `sqrt(sum(q**2))`, first increment `log(C09:30/O09:30)` then consecutive opening-minute close ratios; log state `log(RV+1e-8)`. Require all 30 opening bars. These definitions are documented, **not computed as research outcomes in D0**. B test remains 2024-01-01–2026-09-30; the approved 2016-start fallback preserves 2022–2023 validation. Daily aggregate close/trade-count reconciliation remains pending.

## Manifest and retention contract

Every production dataset must register `dataset_id`, provider, source product/feed/revision, symbol/universe, requested and observed coverage, frequency, adjustment semantics, timezone/bar label, schema version, extraction parameters/time, entitlement/license reference, file paths/bytes/SHA-256, correction lineage and QA exclusions. D0 actual samples are indexed by `d0_file_manifest.json` and provider evidence. Candidate future IDs: `A_crsp_monthly_<schema>_<release>_v1`, `B_alpaca_sip_SPY_1m_split_utc_start_v1`; these are **unmaterialized proposals**, not validated datasets.

Keep licensed rows ignored. A public clone has code, protocol and restore instructions only. Estimate before writing; target <1 GB newly retained, stop and flag unexpected >2 GB. Compression and partitioning must be measured on a small sample first. No schema framework, database server, automatic polling or model-cache infrastructure is needed.


## D1 bounded pilot — actual materialization, 16 October 2026

Dataset `B_alpaca_sip_SPY_1m_split_D1_v1` now has **one** ignored canonical file at `canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet` below the selected data root. It contains 4,113 rows: 4,110 whole-session regular candles across 11 sessions (10 full, one early close), plus three explicitly marked prior-anchor-only candles. Its 152,721 bytes are not replicated as raw whole-day JSON or as a separate 91-window file. No daily model table exists.

Actual canonical columns are `symbol`, `timestamp_utc` (UTC-aware bar start), `session_et` (date), `requested_session` (ISO date string), `request_role` (`full_session` or `prior_anchor_only`), `source_request`, `open`, `high`, `low`, `close`, `volume`, `trade_count`, `vwap`. The artifact preserves response ordering and duplicates, if any, for auditing; the D1 audit found none. Dataset identity explicitly fixes consolidated SIP and split-only adjustment. No D0 raw file was copied/promoted into this source.

`registry/D1_spy_source_manifest.json` registers config/spec/audit-code identities, canonical hash/size/row count, auxiliary hashes and request lineage. `raw/alpaca/<dataset_id>/requests.json` holds endpoint/parameters/response hashes; full-session bodies are transformed in memory into the sole canonical artifact. Separate tiny daily/ex-dividend/Massive diagnostics and the actual-anchor check remain ignored under that extract directory. Those are cross-checks, not an alternative primary source. The numerical one-day equation check is QA only; no outcome/model table or prediction analysis is produced.

The reusable entry point is `python scripts/d1_spy_pilot.py --source-config config/D1_spy_source.json [--data-root PATH] [--start YYYY-MM-DD --end YYYY-MM-DD] [--dry-run]`, after `pip install -e .`. `--data-root` overrides `EBM_DATA_ROOT`; default is repository `data/`. Explicit ranges remain capped at 15 sessions and must match the configured event/overlap conditions for acquisition; custom event pilots require a matching source config/dataset ID. The output manifest rejects a conflicting identity or changed canonical/auxiliary hashes. A cached same-identity rerun performs **zero HTTP calls**. An interrupted acquisition preserves its sanitized ledger and requires inspection rather than automatic repeated network calls.

Calendar semantics: `exchange_calendars` XNYS, left-labelled minutes, cross-checked against NYSE's announced early close; half-days are 210 expected regular candles, not 180 missing full-day candles. For 2024-12-02 the D1 prompt's permissible-full-session rule uses 2024-11-27 15:59, skipping 2024-11-29's early close. This rule is explicit, not a newly invented 13:00 or 16:00 price. Future D2 must retain/label that temporal span consistently.

Measured pilot compression suggests about **9.74 MB** for 243,881 minimal-window/anchor rows over the calendar 2016-01-04–2026-09-30, versus about **38.97 MB** for full regular-session candles; these are projections, not provider coverage. D2 must acquire/audit complete expected session grids before discarding unused minutes if it elects minimal-window retention, so whole-session completeness remains observable. Keep the compact QA/lineage, not both full-day and minimal-window data copies. `registry/D1_spy_storage_projection.json` records assumptions and the in-memory compression measurement; no second file was retained.
