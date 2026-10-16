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


## D2 authoritative source freeze — 16 October 2026

The B full-history authority is now **B_alpaca_sip_SPY_1m_split_D2_v1**, under `canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year=YYYY.parquet` below the configured data root (**11 files, years 2016–2026**). D1 remains an immutable diagnostic pilot, not a parallel full-history authority. No historical artifacts were deleted. D2 reacquired its few overlapping dates within coherent monthly queries, rather than mixing extraction lineages.

Retained schema v1: `symbol:string`, `timestamp_utc:timestamp[us, UTC]`, `session_et:date32`, `open/high/low/close/volume/trade_count/vwap:float64`, `source_batch:string`, `role:string`. Key `(symbol,timestamp_utc)` is sorted/unique; exact duplicates would be explicitly counted/deduplicated and conflicts block freezing. Numeric volume/count retains source scale without integer truncation. Source policy is SPY/SIP/1Min/split only; no raw/dividend/all series is merged.

All **1,049,610 expected** regular-minute starts were audited; **104 absent** and **1,049,506 valid/present** are recorded. Retention is the specified **91 bar starts per full session**, minus **76 absent required starts**, giving **243,804 rows / 8,975,163 bytes**. Early-close minutes were audited then discarded; those dates remain explicitly excluded in QA. The optional initial prior full anchor is absent and was not fabricated/stored. There is no full-day/raw JSON duplicate, alternate window store, split/fold copy or scientific daily feature table.

`registry/D2_spy_source_manifest.json` indexes annual Parquet/QA hashes, source/config/spec identity, execution/maintenance code versions and extraction/freeze timestamps. `registry/D2_blocks/YYYY.json` holds resumable annual **QA counters and gap metadata**, not candle rows. Consolidated session/absence/gap/invalid/year/month/quarter/summary files are the downstream data-quality reference. A source row's existence does not itself mean scientific eligibility; Stage 1 must use the explicit flags and permissible-full-session prior-anchor rule. The 21 half-day boundaries retain their elapsed-time qualification. No forward fill or older fallback for a missing ordinary full-session close is allowed.

`raw/alpaca/<dataset_id>/requests.json` holds only sanitized request parameters, response hashes/status/bytes/times. Monthly request spans return some intervening extended-hours rows, which are filtered by the real calendar before QA. No source-body archive is retained. The append-only request ledger uses a committed-prefix check for interrupted-run resume; immutable source/QA files use whole-file SHA-256. Changed checkpoints, orphan/partial outputs or changed repeated source responses are flagged for inspection rather than overwritten. One runner at a time; completed annual blocks are verified and skipped.

Run `python scripts/d2_spy_acquire.py --dry-run`, then the authorized first block with `--max-years 1`, and `--resume` for remaining years. `--verify-only` checks registered immutable hashes/ledger prefix and makes zero network calls. `--source-config`, `--data-root` and `EBM_DATA_ROOT` follow the existing portable conventions. A public clone contains QA/instructions, not licensed Parquets; use an authorized backup or a new empty data root for a fresh vendor snapshot. Whole discarded-minute audits cannot be recomputed from retained windows alone; preserve their QA/hashes or perform a separately authorized retrieval. No multi-year re-audit is needed for a documentation edit.

The observed canonical footprint is 8.98 MB; detailed QA/lineage brings retained source/registry material to about 17.6 MB, still far below 1 GB. No new dependency/environment was added in D2. See the full D2 report for exact quality counts and Stage 1 conditions; no model evaluation or source-era replication was run.
## D2.1c — explicitly selected first-source repair view

The immutable Alpaca D2 files remain unchanged. The first-source alternative stores only `patches/B/B_spy_hf_source1_D2_1c_v1.parquet` below the data root: 39 missing-key rows, 22,077 bytes, with source revision/URI/group, hashes and validation metadata. Native archive prices pass local comparison without scaling; missing trade counts and VWAP remain null. The manifest is `data/registry/D2_1c_hf_repair_manifest.json`.

Use `ebm_research.experiment_b.repair.load_minutes(repair_manifest=Path('data/registry/D2_1c_hf_repair_manifest.json'))` to select this view explicitly. Omitting the manifest retains Alpaca-only behavior. The older `B_spy_hf_repair_D2_1b_v1` patch is an immutable alternative from a different source; never concatenate both repair versions because their 39 keys overlap. No complete composite Parquet or per-year repaired replica is written. Only small source contexts remain under ignored `raw/diagnostics/`; all five large full/sparse temporary source files were deleted. License, native-adjustment and terminal-gap qualifications remain in the manifest and stage report.
