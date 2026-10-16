# D0 — Shared A+B data-source feasibility

Observed 16 October 2026, America/New_York. **Implementation/QA: PASS WITH QUALIFICATIONS. A: BLOCKED. B: PASS for bounded authenticated feasibility; canonical acquisition and research-readiness remain unverified.** No scientific effect, predictive model or trading result was evaluated.

## Evidence and scope

Starting Git: clean tracked tree on `main`, commit `24de8d01a115d1e4435d82e1091f8c772b6923aa`; ignored `.env` preserved. Initial files were AGENTS.md, README.md, .gitignore and .env. The user subsequently supplied four Markdown documents in `ResearchSpec/`. Both v1 research specifications and relevant starter sections were inspected; four byte-identical archival copies now reside in `docs/specs/`. Original files were preserved. Initial access probes preceded specification availability and were limited to the expressly requested diagnostics; no scientific definitions were implemented or changed.

Machine evidence: `data/registry/d0_20261016_1201_{alpaca,massive,public}.json`, `d0_20261016_1208_{anchors,details}.json`, `d0_20261016_1215_hf-range.json`, `d0_verification.json`, `d0_file_manifest.json`. ID suffixes are unique labels; authoritative observation times are the JSON UTC timestamps. [Source registry](../../docs/data_source_registry.md) contains endpoint findings, date table, source links and field-access prerequisites. [Canonical layout](../../docs/canonical_data_layout.md) defines the zero-duplication design.

## A — BLOCKED

No WRDS authentication was configured in the checked environment, repository `.env`, or standard PostgreSQL/netrc locations. No CRSP/Compustat SQL query or entitlement check could be made. CRSP's documented fields are suitable candidates, but historical shares/returns/distributions/delistings, dated classifications, units, schema permissions and September 2026 availability are **not verified** for this account.

Preferred scientific candidate: **authorized WRDS/CRSP**, optional Compustat/CCM for authentic accounting controls. **No verified primary or compatible backup is available**. Public minute OHLCV and current shares do not solve A's historical population/total-return/turnover requirements. Next safe action: configure existing authorized WRDS access and relevant subscriptions; inspect schema/column permissions, then query one PERMNO over two months and its distribution/delisting metadata. Do not buy access or acquire the market panel yet.

A remains monthly security × formation month, next-calendar-month total simple return, contemporaneous monthly shares-traded/historical-shares state; sealed target-month test 2023-01–2026-09. Source-era 1963-07–2018-12 fidelity is unexecuted, not inferred from advertised CRSP availability.

## B — PASS, limited feasibility

**Primary: Alpaca SIP**, based on authenticated requests rather than advertising. Five complete raw SPY one-minute regular sessions were observed: **2016-01-05, 2019-07-15, 2023-07-17, 2024-07-15, 2026-09-15**. Each has 390 distinct ordered starts from 09:30 through 15:59 ET, 30 opening minutes, no missing/extra regular minute or OHLCV integrity violation, and no unconsumed continuation token. Winter/summer offsets are −05/−04 via ZoneInfo. Small prior-session 15:59/16:00 requests succeeded on **2016-01-04, 2019-07-12, 2023-07-14, 2024-07-12, 2026-09-14**. The 16:00-start bar is after hours; it is not the scientific close anchor.

**Backup: Massive for recent cross-checks only.** One unadjusted request for **2026-09-15** returned 882 extended-session bars, including all 390 valid regular bars. The regular-minute closes match Alpaca exactly (maximum absolute difference 0). This confirms recent minute access, not the account's plan name, two-year entitlement boundary, independence of upstream feed, or full validation/test coverage.

Full-session probes used raw prices to diagnose feeds. Four five-minute Alpaca adjustment checks confirm explicit split-only access and visible dividend-adjustment differences. The future canonical source must use the specification's consistent **split-only adjustment**, with prior close on the same basis. No raw diagnostic file is a research-ready canonical input. Daily close/count reconciliation, split/ex-dividend audits and general calendar/half-day validation remain pending.

The specification preapproves a 2016-start modern branch: train 2016–2021, validate 2022–2023, sealed test 2024–2026-09-30. The sparse dates support proceeding to a small acquisition pilot; they **do not prove continuous 2016–2026 completeness or the ≥3 complete-year research gate**. Source-era access is **UNKNOWN**; no 1993–2013 replication is claimed. No test-period returns/RV, model scores or scientific hypotheses were analyzed; sealed-date requests were QA only.

## Community archives and secondary sources

HF's pinned tree has **411 monthly Parquets, 1992-01–2026-03**, totaling **87.72 GB**; April–September 2026 files are absent. Finnhub attribution is visible, but license, SPY inclusion, adjustment policy and extraction lineage remain unresolved. SPY-only dataset-server filter timed out. Four-byte HTTP range retrieval succeeded, showing partial byte access but not effective ticker predicate pushdown. No monthly file was retained. HF is not approved as a full-period backup.

Three Kaggle candidates were inspected using public descriptions/file manifests only. Two declare 2008–2021 SPY history; a cleaned SPY/QQQ candidate lacks verified coverage. All lack sufficient original-feed/adjustment/timezone evidence. They are potential historical investigations, not validated source-era inputs or September 2026 backups. No Kaggle data file was downloaded. Schwab was not contacted because no credentials/token were configured. No existing external user dataset/path was supplied or assumed.

## Storage and acquisition estimates

Disk check before sample acquisition: **65,536,000,000 free bytes (~65.54 GB / 61.04 GiB)**. This is a point-in-time observation. HF's whole monthly archive exceeds that free space and is prohibited by scope anyway.

| Category | Observed or estimated bytes | Basis |
|---|---:|---|
| Retained provider rows | **304,952** in 15 ignored JSON files | 5 full Alpaca sessions + 4 five-minute adjustment responses + 5 prior-close pairs + one Massive day |
| Registry/evidence | About **0.34 MB** | Public metadata, references, hashes, QA; final manifest also records data README |
| Spec archival copies | **171,800** | Four supplied Markdown files, hash-matched to originals |
| Canonical / derived data | **0** | Reserved layout only |
| B 2016–2026-09 full regular minutes | About **1.06m rows, 115 MB compact JSON** | Illustrative 2,709 full sessions × 390 × observed 108.49 bytes/row; holidays/half-days not yet counted |
| B selected scientific windows | About **246,519 rows, 27 MB compact JSON** | 91 minutes/session × illustrative 2,709; retains 14:59 anchor and reuses prior close |
| B projected Parquet payload | About **18 MB selected windows / 76 MB full regular sessions uncompressed fixed-width payload** | Approximate 72 bytes/row; not a measured Parquet footprint; strings/metadata/compression change size |
| A illustrative monthly panel | **0.38–0.76 GB uncompressed payload**, before optional controls/raw retention | Assumed 5,000 average names × 759 months × 100–200 bytes; actual universe/field plan unknown, not an authorization |

No compression ratio was measured and no large file was written. Download/query one symbol and minimal columns/windows; partition by year only if useful. HF byte ranges may avoid full-file retention but efficient SPY extraction is unverified. Kaggle single-file selection avoids the unrelated QQQ/combined files but not necessarily downloading the entire selected SPY CSV. WRDS can select columns/security/date predicates once authorized.

## Checks, limitations and next safe action

`python3 -B scripts/d0_verify.py` **PASS**: 15 sample hash/size checks, five full exact-date grids, prior-close availability, Massive regular-session integrity/overlap, wrong-date regression guard and temporary JSON I/O smoke. Python 3.14.6, standard library only. No dependency installation, package environment, large transformation, regression or model pipeline was needed. General exchange-calendar logic, continuous historical QA, corporate-action fidelity, daily close reconciliation and scientific inference were **not tested**.

A's next step is the bounded WRDS schema/sample check after credentials/permissions are available. B's next step is a **small split-adjusted acquisition pilot** covering a normal week, an ex-dividend boundary and a half-day/DST boundary, including prior anchors and daily close/count comparison; then quantify calendar coverage gaps before approving the full minimal-window extraction. Keep all providers separate by dataset ID. No full acquisition, new subscription, upstream-license assumption or scientific redesign is authorized by this report.
