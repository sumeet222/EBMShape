# Codex Execution Prompt — Five State-Dependent EBM Preliminary Screens

**Prompt version:** v1.0  
**Execution type:** Autonomous, staged coding + data-acquisition + visual statistical feasibility screening  
**Authoritative scientific document:** `docs/ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md`  
**Experiment IDs:** `P01_INTRADAY_BETA`, `P02_SIGNED_RV`, `P03_TREASURY_HEDGE`, `P04_VOLUME_REVERSAL`, `P05_FOMC_RESPONSE`  
**Primary final deliverable:** **one consolidated, readable Markdown report with actual PNG figures embedded by relative Markdown image paths**, plus a compact review bundle containing the report and images.  
**Execution location:** The **same project/repository and experiment parent directory as existing Experiments A, B, C**. Discover the paths by inspection; do not assume a machine-specific absolute path.  
**No EBM training in this task.** This is a low-cost preliminary scientific feasibility screen, not alpha discovery, comprehensive model selection, or a full replication.

---

## 0. Read first and respect precedence

You are Codex acting as a careful quantitative research engineer, reproducibility auditor, and scientific diagnostics assistant. Carry out the actual implementation, tests, data acquisition **if needed**, five preliminary analyses, plot generation, and closeout in this execution—not just a plan.

1. **Read the complete authoritative design file** `docs/ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md` before editing code. Treat it as the scientific source of truth for sources, tickers, data definitions, experiments, literature motivations, and expected outcomes. If it is missing, locate it *within this repository only*; if absent, **stop** and request the file. Do **not** reconstruct or alter the five designs from memory.
2. Inspect applicable repository `AGENTS.md` files and established data/test conventions. Preserve existing code style, git rules, checksums, report conventions, and data protection requirements.
3. Inspect the directories and research assets for earlier **Experiments A, B, and C**. Create this work as a **new, separate sibling research run** under their actual parent; never rename, migrate, overwrite, remove, or silently edit the old experiments.
4. **Scientific precedence:** the design v1.0 controls over this operational prompt on scientific definitions. This execution prompt controls on implementation ordering, storage protection, source-experiment isolation, and final deliverables. If a genuine conflict remains, log it and stop before the affected stage rather than choosing an attractive substitute.
5. Your goal is to determine whether a **predeclared state-dependent slope or shape** seems supported strongly enough to justify later EBM modeling. A changing linear slope suffices for feasibility; nonlinear curvature is not presumed or necessary.
6. **Do not optimize toward positive plots**: freeze source, ticker subset, time windows, states, preprocessing and primary contrasts **before** looking at response relationships. Do not add ad hoc predictor/state grids, tune many windows, or replace a scientifically negative experiment with another target.
7. Work autonomously on small code/environment/API/schema exceptions. For fundamental scientific substitutions or violating resource limits, stop that branch with an explicit blocker; continue unaffected, valid branches when feasible.

### Hard rules — MUST pass

- **Only one common acquisition pass over the selected large Hugging Face minute archive.** Never download it five times or make a second full/monthly sweep for each experiment. Choose **one** of the two apparent dataset clones; never fetch both. Build the **union** of all needed tickers, months and columns before the first large data transfer.
- **Inspect and reuse valid local A/B/C/shared data first.** No new download merely because its source is convenient. Reuse immutable existing data by reference; do not duplicate the 99-stock/30-minute files, SPY minute files, or retained price tables.
- **10,000,000,000-byte hard cap on incremental local storage**, including all new retained data, temporary monthly files, Hugging Face caches, external package caches, outputs, interrupted files and review bundles. Measure peak usage and forecast the next step before downloading. If the physical workspace has a stricter limit, obey that too. **Fail closed** if a month cannot be processed below the cap.
- Download/process large market data **one month at a time** in bounded chunks; filter using the frozen union; validate the retained partition; delete the raw monthly download and attributable caches; **only then** advance. A validated month must never be downloaded again. Retry a failed incomplete month as necessary with a logged cause, not as an independent second source pass.
- **One authoritative shared market-data copy** (or existing validated shared copies referenced without duplication). Derived 5-minute/daily summaries are shared. Each experiment gets its **own immutable config, plots, summaries and diagnostics**, not its own copy of the underlying data.
- **Fail closed on source mismatch**. Validate experiment ID, source ID, expected symbols, timestamps, frequency, targets, state variables, availability times, schema/hash and output destination **immediately before each experiment**. A named CSV/Parquet file that “looks right” is not acceptable without provenance.
- **Do not use implied-volatility/VIX/options/LOB/paid data.** Do not substitute returns, volume, ETF prices, shocks, volatility measures, instruments, windows or state definitions beyond the design.
- **Do not run EBM or train ML models**. Use descriptive conditional means, literature-aligned OLS/state-interaction regressions, concise visualizations and dependence-aware exploratory uncertainty only.
- Do not use the exploratory test/evaluation period later as an “untouched confirmatory sample.” Mark the exact dates examined.
- Do not claim causality, replicable profit, default-EBM theory guarantees, or novelty because state overlays look different.

---

## 1. Repository discovery and safe physical layout

### 1.1 Discover, do not guess

At the start print and log: working-directory real path, git root/status/branch, nearby A/B/C experiment directory names, `docs` path, current shared-market directories, existing SPY minute files, current 99-stock 30-minute panel, any source manifests/config hashes, dataset provenance, current directory sizes, physical free space and available Python environment. Do not modify old experiments or raw data.

Once, **before any experiment runs**, freeze a resolved path map, for example:

```text
<verified-project-root>/
  docs/
    ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md
  <verified-existing-experiment-parent>/
    <existing A/B/C directories>       # READ ONLY
    five_state_shape_prelim_v1/        # NEW, unique sibling
      configs/
      manifests/
      logs/
      checkpoints/
      reports/
        figures/
        figure_data/
      experiments/
        P01_INTRADAY_BETA/{plots,results,diagnostics,report.md}
        P02_SIGNED_RV/{plots,results,diagnostics,report.md}
        P03_TREASURY_HEDGE/{plots,results,diagnostics,report.md}
        P04_VOLUME_REVERSAL/{plots,results,diagnostics,report.md}
        P05_FOMC_RESPONSE/{plots,results,diagnostics,report.md}
  <existing-valid-shared-data-root>/
    market_1m/                        # only needed month/ticker union, if missing locally
    derived/                          # canonical daily / 5-minute etc.
    etf_daily/
    fred_rates/
    fed_surprises/
```

The diagram is illustrative. Reuse the repository's established `data/shared` and config layout if already present. Do not create a parallel shared-data warehouse merely to match this diagram. Record actual paths in `manifests/resolved_paths.json`. Never use glob “first match” input selection after this freeze.

**Isolation:** write to a new run root only. Old A/B/C data are read-only and can be referenced by their exact path and checksum; do not import their *analytical conclusions* or reuse their plots/models as if they were current evidence. All five new experiments are immutable ID-namespaced. If files already exist at the desired new run path, use a new version or explicit safe resume, not overwrite.

### 1.2 A compact config registry

Create one shared sources plan and **five separately versioned config files**. Each experiment config must have at minimum:

```yaml
experiment_id: P01_INTRADAY_BETA            # different for each of the five
protocol_version: prelim-v1
scientific_design_file: docs/ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md
scientific_design_sha256: <actual hash>
source_ids: [...]                           # immutable registry IDs
input_paths: [...]                          # exact resolved immutable shared paths
input_fingerprints: {...}                   # hashes of referenced canonical partitions/files
instrument_ids: [...]
independent_unit: trading_day               # or FOMC_event for P05
input_frequency: 1min
response: ...                               # exact response definition and unit
focal_predictor: ...                        # exact predictor definition and unit
state: ...                                  # exact state definition/thresholds/time of availability
session_timezone: America/New_York
coverage: {start: ..., end: ..., eligibility_rule: ...}
split_or_period_rule: ...
contrast_definitions: [...]
bootstrap: {method: ..., block_length: ..., seed: ..., replicates: ...}
output_dir: <exact run root>/experiments/P01_INTRADAY_BETA
config_sha256: <sha256 computed after freezing>
```

Make **five actual distinct configs**, not a template instantiated with only a changed output path. Store a `frozen_configs.json` listing hashes, and ensure a run aborts if its on-disk config has changed without a new version. Never copy P01 parameters into P02 merely because they share SPY observations.

---

## 2. Required source × experiment contracts (never mix)

Treat this as a pre-execution assertion matrix; the design file supplies the complete estimands and literature details.

| Exact ID | Required original source(s) | Focal predictor | STATE / as-of meaning | RESPONSE | Time unit / forbidden substitution |
|---|---|---|---|---|---|
| `P01_INTRADAY_BETA` | Observed SPY + frozen 10–20-stock minute prices | Synchronous SPY **5-minute intraday** log return | **Clock time:** early 10:00–11:30, mid 11:30–14:00, late 14:00–16:00 ET | Synchronous **stock** 5-minute log return | One aligned stock-market bar; no overnight gap; no SPY target in place of stock return; exclude 09:30–10:00 in primary analysis |
| `P02_SIGNED_RV` | Genuine SPY/selected-stock observed 1-minute closes | `log(RV_d)` with controlled lagged RV | **Same completed-day downside semivariance share** `RS^-_d/RV_d`, declared bins 0–1/3, 1/3–2/3, 2/3–1 | **Next trading-session** `log(RV_{d+1})` | Daily; no future information in state; no synthetic/forward-filled 1-minute returns; no implied volatility |
| `P03_TREASURY_HEDGE` | Valid **SPY + IEF** daily open/close (TLT only labeled secondary), FRED prior-available rates | **Same-day SPY ETF** return | **Prior-available** 10Y−2Y spread terciles (10Y level only separate secondary config) | **Same-day IEF Treasury ETF** return | Contemporaneous stock–bond association; same return window for both; never swap SPY/IEF or bond returns/yield changes; adjustment status explicit |
| `P04_VOLUME_REVERSAL` | Original observed 99-stock 30-minute OHLCV, or audited minute-derived daily bars | **Stock** daily return `r_{i,d}` | **Stock's own relative log daily volume**, versus preceding 20 eligible days | **Next trading-day stock** return `r_{i,d+1}` | Daily; no current shares outstanding guessed; no same-day target, no pooled SPY volume as stock volume |
| `P05_FOMC_RESPONSE` | **San Francisco Fed monetary-policy surprises** + observed SPY event-window minute prices | Absolute **published surprise in basis points** | Surprise **sign** (+/− according to source metadata) | SPY **event-window** log return (standard 14:00–14:30 ET, verify exceptions) | Independent FOMC event, not independent minute/stock row; avoid treating non-events as zero surprises; not an ex-ante forecast |

For every run: print the exact `experiment_id | source_ids | expected target name | state definition | independent unit | date range | config hash | input fingerprint` before computing anything. Assert actual data matches every column. A mismatch is **ERROR / DATA HOLD**, never “best effort” analysis on another table.

**Source registry:** require each table to include or be accompanied by `source_id`, remote repository/revision or original local provenance, unmodified source filename/partition, stored schema and units, timestamp convention, observed/imputed status, adjustment notes and SHA-256 (or immutable chunk-hash manifest). Include data lineage for each derived column.

---

## 3. Staged execution (with gates and checkpoint reports)

Work in stages 0–4 below. Create a short `logs/stage<N>_session_report.md` after each stage: files created/modified and their purposes, source audit decisions, tests run, observed blockers, bytes added/cleaned, git diff summary and next validated action. Stage outputs are **checkpoints**, not speculative future promises. A blocked experiment must not stop unaffected valid experiments, but missing global source integrity or unsafe disk usage blocks acquisition and analysis.

### STAGE 0 — No-download data inventory, source union, resource forecast, scientific freeze

**Absolutely no large downloads in Stage 0.** Read metadata, list existing directories, schemas and time coverage, and make a completeness report. Remote metadata-only queries for dataset listing/commit/size are permitted; no parquet full transfer.

A. Verify the scientific design file hash and precise project root. Inspect existing B/C SPY minute files and previous 99-stock 30-minute data. Determine whether the old 30-minute panel contains forward-filled OHLC, masked bars, and volume imputation. Only genuine observed bars may be used for realized variance and reported volume. Determine whether stock-minute and ETF-minute files already cover useful periods.

B. Inventory FRED/ETF/surprise files if already downloaded. Capture data provider, version, explicit permission/license restrictions, dividends/splits, frequency, timezone, missingness and whether their dates intersect candidate samples. Check file schemas using bounded row sampling; do not run a full-dataset `.to_pandas()`.

C. Build **one frozen union-acquisition plan** for all five experiments. State exactly which symbols, date spans, source monthly filenames/URLs and columns are needed; identify which are already satisfied locally. Freeze a diverse 10–20-stock list based on existing roster + **coverage/sector criteria only** (CAT/JNJ are literature-linked anchors if eligible). Do not choose stocks after looking at the response.

D. First prefer existing SPY/stock minute data for P01/P02/P05, the observed 30-minute panel for P04, and existing SPY/IEF + rates for P03. Only missing rows/sources belong in the remote plan. **No HF minute download if the verified local union is already sufficient.** Use one version-pinned source: `mito0o852/OHLCV-1m` OR `ggaddam/OHLCV-1m`—never both. Verify actual repository file names; do not assume the archive has all symbols/dates claimed in its description.

E. Compute explicit storage forecast in **bytes**, with current baseline, temporary single-month maximum, retained selected-minute estimates, shared derivative estimates, logs/figures, cache, and review archive. Check physical free space (`df`, `statvfs` or equivalent). **Hard incremental peak <10,000,000,000 bytes**. Soft pause for replanning when forecast exceeds 8,000,000,000 bytes. Prefer retained derived data under 3 GB and monthly temp/cache under 2 GB; any larger chunk needs proven headroom. Do not spawn unbounded remote dataset caches or huge dependency installations.

F. Validate source permissions. Do not bypass rate limits, auth or licensing restrictions. If a monthly file exceeds feasible staging capacity and streaming/range-reading cannot be supported safely, record `DATA HOLD` and seek approval; do not download the whole archive.

**Stage 0 artifacts:**

- `reports/shared_data_inventory.md`: current files, exact coverage, provenance and whether each experiment can proceed without downloads.
- `manifests/source_registry.json` and `manifests/union_acquisition_plan.json` (frozen source revision, file list, ticker set and month set).
- `manifests/storage_budget.json` (baseline + worst-case forecast + safety margin).
- `reports/experiment_input_contract_matrix.md` (five exact source→target/state mappings).
- Tests proving registry/config schema integrity and the absence of unapproved source aliases.

**Stage 0 gate:** No large transfer until the union manifest, source identity, required data, disk forecast, output root and configs are frozen and validated.

### STAGE 1 — Acquire all missing common data ONCE

**The only stage allowed to fetch large market files.** Acquire **the union once**, for all five experiments, not sequential independent per-experiment downloads. Metadata listing may be reused from Stage 0. Download small FRED, ETF daily and SF Fed event series once each where required and licensed. Log URL, request date, revision/version, expected time columns, content hash and actual bytes.

#### HF minute-archive algorithm (strict)

1. Read `union_acquisition_plan.json` and check its hash. Check Stage-0 configs need no added tickers/months. Enumerate missing monthly Parquet files **only once** from the frozen manifest. A later newly desired ticker/month is a new protocol version, **not** permission to rescan everything.
2. For each `month` in the manifest, check `checkpoints/hf_months.jsonl`. Skip month when `validated` and its local selected output hashes and counts match. For `in_progress`, inspect/clean its own partial download without touching any old source data.
3. Prefer **bounded remote range/row-group reads with filtering**, if actually supported by the server and Parquet metadata. Otherwise download **one monthly Parquet** into a controlled temporary location, stream row groups/batches with PyArrow (or equivalent), filter to frozen tickers/date/session/frequency and selected columns immediately. **Never** clone/snapshot/download the repository or materialize the full file into one Pandas object.
4. Stream filtered rows into **one canonical selected-minute partition per month** (or reuse equal/hash-verified local partitions). Retain original source timestamp, ticker, observed OHLCV, and validity/adjustment flags. Use atomic staging→validate→commit. Deduplicate on the declared `(ticker, UTC bar timestamp)` key with explicit conflict detection; do not silently prefer one conflicting version.
5. Verify month identity, source revision, timezone, OHLC invariants, positive/nonnegative volume rules, distinct timestamps, regular-session filter, expected ticker/coverage counts, checksum, row/schema units, gap summaries and output byte size. If valid, mark `validated` with original source ETag/checksum, selected output SHA and row counts.
6. **Immediately delete that source monthly temporary Parquet and its attributable cache** after successful validated commit. Recalculate incremental usage, recorded peak and physical disk free. Only then process the next month.
7. A failed/partial month must be marked with exact failure cause; never claim it has been processed. Retry only that month when safe. A completed/validated month must not be fetched again merely for QA or a different experiment. Use the retained **filtered** canonical partition for all later checks.
8. Do not fetch the alternate HF mirror if the chosen repository fails or lacks data without explicit approval. The source change would affect provenance and the one-pass contract.

**Disk protection during each step:** include hidden `~/.cache/huggingface`, `HF_HOME`, package caches, temporary paths and any newly generated files attributable to this job. Prefer a dedicated cache under this run root so usage is measurable; if cache cannot be redirected safely, measure it explicitly. Reserve for the *whole compressed monthly file + staging + filtered output* before fetching; a download is not authorized if the projected peak approaches the cap. Stop at any actual hard-limit breach risk. **Never delete old A/B/C or user data to reclaim space.**

**Small sources:**

- `HF_ETF_DAILY`: download once if valid SPY/IEF/TLT daily inputs cannot be derived from a verified local instrument series. Respect custom license. Check dividends/splits/adjustments; unadjusted prices are not automatically total returns.
- `FED_RATES`: download FRED `DGS2`,`DGS10`, optional `DFF` once per defined date window; record vintage/time-availability limitations. Use previous available observation in P03, never back-fill from future dates.
- `FED_SHOCKS`: get the published SF Fed event-study / monetary-policy surprise table once. Preserve signed basis-point surprise, version, source event ID, exact event date/time and exclusion flags. Check actual event eligibility rather than assuming all FOMC announcements occur at one time.

**Stage 1 artifacts:** `reports/shared_download_integrity.md`, immutable canonical source registry and per-month acquisition ledger with bytes/network attempts/actual after-cleanup footprint, source-revision hashes, download failure list, one-pass compliance assertions, and final storage peak. Stage 1 is not complete until all eligible, expected sources are validated or explicitly marked unavailable for a specific affected experiment.

### STAGE 2 — Shared feature building and quality gates (NO downloads)

Construct shared compact market/macro/event feature tables **once**, from already verified immutable data, not once per experiment. Existing canonical shared returns/features may be reused when equivalent by formula, date, and source fingerprint.

Minimum shared derivatives:

- `market_returns_5m`: observed synchronized intraday SPY/stock 5-minute log returns with `(symbol, NY trading date, 5m end-time)` unique keys; local ET session and UTC source timestamps retained; no overnight leakage, forward fill, partial-period contamination or split-adjustment surprises.
- `daily_rv_semivariance`: for each verified day/asset, `RV`, `RS_minus`, `RS_plus`, `q_down`, number of genuine one-minute return intervals, valid-day flag, `next_valid_session_RV`, and exact target-availability time; source day-to-day map. Validate `RS_minus+RS_plus≈RV`.
- `daily_stock_returns_volume`: observed actual-volume sums, original adjustment flags, next-trading-day log return, previous-20-*eligible-day* mean log volume, and predeclared controls. Preserve original 30-minute imputation masks and treat suspicious split days separately.
- `daily_spy_treasury_returns`: one consistent SPY/IEF (or explicitly allowed TLT secondary) return window per observation, adjustment status, lagged FRED level/spread states, and whether same-day rate publication could have been after the chosen return start.
- `fomc_events`: one row per published valid event with event ID, timestamp, source signed surprise in bp, observed SPY pre-window and 14:00–14:30 ET return when applicable, event eligibility, and joins with exact cardinality assertions.

**Data integrity invariants:**

1. Every output row has immutable `source_id`, partition/run fingerprint and definitions metadata; derived data lineage traces back to verified raw sources. No unlabeled generic `volatility`, `return` or `state` columns whose meaning changes across experiments.
2. All times are timezone-aware; source UTC→America/New_York correctly handles DST, normal sessions and valid half-days. Time-of-day gates are explicit and nonoverlapping. No duplicate join keys, no accidental Cartesian product when merging macro/event tables.
3. Before building labels, calculate coverage/observed counts. Do not use imputed one-minute prices for RV or signed semivariance. Do not use future outcomes to define current state or choose instruments.
4. Numerically validate log-return identities, RV nonnegativity, `RS_plus + RS_minus = RV`, per-day bar counts, 5-minute boundary aggregation, `next_valid_session` mapping, volume 20-day lookback excluding current day, and BP-versus-percent/yield-level conversion.
5. Test a handful of known timestamps/dates manually in an automated fixture, plus random deterministic-sample audits of each derived table against source rows.
6. No time collision: a P05 FOMC event/date cannot accidentally be used as a P03 rate observation at an unavailable timestamp; P03 cannot read a FOMC shock as a daily yield state; P04 cannot select SPY's target when computing stock target.

**Isolation/corruption tests, mandatory:** using disposable synthetic fixtures—not production data—deliberately swap SPY and IEF, substitute a P01 source for P02, remove `FED_SHOCKS` from P05, change P04 next-day target to same-day, modify a config after freeze, and tamper with one source hash. **Each must cause a descriptive validation failure before a plot is generated.** Also test an allowed read-only shared-data reference works across two different experiment IDs without copying the data. Do not assert these checks passed unless executed.

**Stage 2 outputs:** derived schemas, lineage manifest and column dictionary, quality/gap tables, tests, `reports/shared_features_QA.md` and verified exact source-to-experiment fingerprints. No EBM or expanded modeling.

### STAGE 3 — Five isolated, cheap preliminary analyses (NO downloads / NO EBM)

Run P01…P05 independently, preferably sequentially for easy diagnostics and disk control. For each:

- Load only **its own frozen config** and required read-only shared tables. Recalculate config/source hashes and enforce the exact experiment-input contract from §2.
- Write only to `experiments/<EXACT_ID>/`; do not read another experiment's result file to calculate its own curves. Shared canonical market data are allowed read-only.
- Freeze state thresholds using training/reference portion according to design, record all actual numeric cutpoints and support. Do not pick new regimes from result plots.
- Generate compact source/support table, per-state equal-x conditional mean overlays, varying-slope OLS reference, **anchored/difference** plot showing shape or slope shifts, date/event-aware uncertainty, and sensitivity to outliers/time slices.
- Flag `NO_COMMON_SUPPORT` explicitly where necessary. Never draw smoothed connecting curves across unobserved support as if measured. Print independent date/event counts directly on important plots.
- Use market-date or week-block bootstrap as appropriate; resample *entire dates* in pooled-stock models. For P05 resample whole FOMC events; if too few events, report abstention instead of unreliable curve fitting. Record resample seed, number of blocks/iterations and limitations.
- Record descriptive slope estimates and differences in **correct response units**, coverage/uncertainty, materiality judgments grounded in the prespecified question, negative findings and blockers. An interesting-looking graph alone is not GO.
- Run automated plot/data QA tests below before declaring the experiment complete.

#### P01_INTRADAY_BETA — exact screen

- Exclude 09:30–10:00 ET in the primary analysis; align SPY and stocks on **same five-minute periods**.
- Make early/mid/late conditional stock-return-versus-SPY-return curves on identical supported SPY-return x ranges; display CAT and JNJ when actually available, plus other predeclared liquid stocks.
- Fit OLS market beta by state with date-aware uncertainty, stock beta-dispersion by state and early–late differences. Examine negative/positive market returns only where each state has adequate observations.
- Document whether any result is merely a changing linear beta; curvature is a separate tentative conclusion. Plot with returns in **basis points**.
- Fail if source target is a market return rather than an individual stock return, minutes are nonsynchronous, or stocks were chosen by looking at plot results.

#### P02_SIGNED_RV — exact screen

- Verify observed intraday minute returns; calculate `RV_d`, negative/positive semivariances, their sum and downside share `q`.
- Compare *next-day* log RV versus *current-day* log RV across frozen downside-share bins and a continuous q plot, on common current-RV support.
- Include a reference regression with positive and negative semivariance terms and a lagged-RV controlled regression; report state/slope contrasts.
- Ensure chosen log epsilon and comparison convention are globally declared and not adjusted after seeing results. Validate next **trading** day rather than calendar day and no overnight return inside intraday RV.
- Keep separate SPY-only and pooled-stock estimates when both can be supported. Do not treat stock rows as independent calendar days.

#### P03_TREASURY_HEDGE — exact screen

- Confirm **both** SPY and IEF (primary) are actual securities in the chosen source, dates align, and the same open-to-close (or separately validated adjusted-total-return) convention applies to both.
- Plot Treasury-vs-SPY response functions by **lagged yield-spread** state; fit state-wise OLS and downside-response contrasts only over intersecting supported SPY-return ranges. Record ETF dividend/adjustment problems.
- A Treasury-yield **level/change is not a bond ETF return**. If no valid Treasury price series is found, **DATA HOLD** rather than substitution. TLT and lagged 10Y level may be additional separately labeled sensitivity outputs, never silent replacements for primary IEF/spread.
- Do not use a FRED observation not demonstrably available by the state cutoff.

#### P04_VOLUME_REVERSAL — exact screen

- Aggregate original observed stock OHLCV into daily returns and **real** volumes (verify any 30-minute forward-fill/imputation conventions).
- Calculate log-volume relative to *previous 20 eligible trading sessions*, current-day daily return and **next-trading-day** return.
- Compare next-day-return-versus-today-return slopes/curves across frozen relative-volume terciles, especially negative current-return moves. State the universe and survivorship limitations; add a simple market-return control as prespecified.
- Report when corporate-action adjustments or observed/filled records render the inference unusable. Do not change to monthly share turnover or a closing-half-hour target.

#### P05_FOMC_RESPONSE — exact screen

- Validate official announcement dates and event times for each event. Standard 14:00–14:30 ET SPY log return is the primary response **only for standard 14:00 releases**; exceptions must be separately audited and excluded/held rather than time-shifted silently.
- Use the **published signed shock in bp**; focal predictor is absolute magnitude and state is shock sign. Draw signed-surprise scatter and separate sign/magnitude plots only if supported.
- Label independent **event count** and positive/negative breakdown. Use event bootstrap/leave-one-event-out. A small number of shocks cannot justify a precise nonlinear curve; if insufficient, `WEAK` or `DATA HOLD`.
- Explain any overlap between the surprise construction window and the equity-return event window; report *contemporaneous association*, not forecastability or clean causality.

#### Status vocabulary for all five

- `GO`: a material and reasonably supported state-dependent slope or shape contrast merits a later EBM experiment. Not a statistically confirmed new effect.
- `WEAK`: suggestive but unstable/small/wide; additional genuinely independent data or stronger preliminary design needed.
- `NO-GO`: valid data and an informative preliminary analysis but no convincing material state-dependent relationship for this predeclared target/sample.
- `DATA HOLD`: missing/untrusted/wrong-source data, insufficient event/sample support, licensing/adjustment issue, or definition mismatch prevents a valid test.

**Do not reclassify `DATA HOLD` as `NO-GO`.** A failed relationship is not the same as unavailable data. Report both visually and quantitatively supported negatives without hiding them.

### STAGE 4 — One consolidated human-readable report with ChatGPT-readable pictures

Create these **required** files:

1. `reports/five_experiment_prelim_closeout_v1.md` — the primary **consolidated Markdown report**, covering all five IDs and their actual measured outcomes (including honest negative/blocked branches).
2. `reports/figures/five_experiment_overview.png` — readable comparison/contact sheet of the five summaries, **with measured plot content or truthful DATA HOLD indications**; no simulated result presented as actual data.
3. `reports/figures/P01_INTRADAY_BETA_summary.png`, ..., `reports/figures/P05_FOMC_RESPONSE_summary.png` — **one readable key-plot summary PNG per experiment**, showing its conditional curves and counts/uncertainty where possible. If blocked, render a clear data-status diagnostic graphic only, labeled `NO VALID RESULT`.
4. `reports/figures/<ID>_support.png` and `reports/figures/<ID>_shape_contrast.png` when that experiment was valid and informative enough; cap nonessential figures.
5. `reports/figure_data/` — small CSV/Parquet tables containing **the exact x/y/CI/count coordinates plotted**; include source and config hashes in accompanying metadata. No copies of raw datasets.
6. `reports/five_experiment_prelim_review_bundle_v1.zip` — contains the consolidated report, its image files, plot-source data/manifest, five per-experiment `report.md` files, source/config summary and enough QA evidence to review without downloading the 80+ GB archive. **Do not include raw Parquet market data.**
7. `reports/five_experiment_execution_integrity_v1.md` — source hashes, config hashes, actual command invocations, test results, final/peak disk usage, one-pass monthly ledger, warnings and failures. Include per-experiment QA status.

#### Mandatory report structure

```markdown
# Preliminary screen of five state-dependent EBM research ideas

## Executive decision matrix
| Experiment ID | Source and period | Scientific target | Independent days/events | Main state contrast | Uncertainty/support | Status | Figure |
...

## Shared data sources, provenance and storage
- Existing data reused; exact files and SHA-256.
- New sources, revisions and monthly source-pass ledger.
- Disk baseline, incremental peak, post-cleanup usage; single-pass evidence.
- Known limitations: adjustment, coverage, imputation, FRED releases, event alignment.

## P01_INTRADAY_BETA — results and limitations
![P01 measured summary](figures/P01_INTRADAY_BETA_summary.png)
![P01 shape contrast](figures/P01_INTRADAY_BETA_shape_contrast.png)
<!-- same structure for P02–P05; omit nonexistent extra figures and state reason -->

## Cross-experiment methodological comparison
- Reproduced literature direction? state changes only slope or richer shape?
- Support, negative results, near-empty tails, instrument/time differences.
- Which results are descriptive versus forecast-related?

## Ranked recommendations for possible next EBM studies
- Explain GO / WEAK / NO-GO / DATA HOLD transparently; no test-set cherry-picking.

## QA and artifacts index
- Per-experiment metadata/config/source fingerprints, image data, audit reports.
- Actual experimental period marked exploratory.
```

**Actual images, not just names:** include literal Markdown `![caption](figures/filename.png)` references to real PNG files, with all referenced paths verified. Make pictures at least about 1200 px wide or otherwise legible at normal viewing scale; titles, color/linestyle legends, time axes, return/variance units, sample sizes and CI labels must be unambiguous. Provide each experiment summary as a standalone PNG and the overview/contact sheet. These six images **must be packaged with the Markdown** for posting back to ChatGPT.

**Crucial portability note:** a relative Markdown image path is not automatically available when someone uploads **only** the `.md` text to ChatGPT. Therefore the closeout message must instruct the user to attach **(a) the Markdown, (b) the review ZIP, and ideally (c) the five summary PNGs and overview PNG as image attachments**. Do **not** rely on pasted local paths, broken external links, or an HTML-only report. If the chat environment can inspect a ZIP or mounted folder, the bundle preserves relative links; the PNG attachments ensure native visual analysis here. Do not paste base64 megabytes into the Markdown.

---

## 4. Automated visual and statistical QA (required and executed)

For every generated chart, use a small reusable figure QA routine that:

1. Verifies the corresponding source-data table exists, is finite where drawn, uses the same x grid for overlaid state comparisons, and has a defensible `n_independent_days` / `n_events` for each state and bin.
2. Checks all plot-level labels, titles, legends, state IDs, series count, response units, date span, and state cutpoints against **that experiment's frozen config**. Do not copy “opening volatility” labels from Experiment C or “turnover” labels from Experiment A.
3. Reconstructs the plotted x/y/interval/count values from saved figure-data tables and compares to the chart inputs with numerical tolerance. Protect against reversed state legend and swapped target/predictor.
4. Validates bootstrap intervals (low ≤ center ≤ high where appropriate), flags singular/empty bands, and does not extrapolate line segments across missing predictor support. Use consistent x limits when overlays are compared.
5. Opens the actual exported PNG via Pillow or equivalent: readable image size, no corrupt/truncated file, no blank/near-uniform image, no inexplicable white panel, no text clipped at image boundaries when detectable. Additionally render a compact contact sheet for manual image inspection.
6. Runs an outlier/rare-support stress diagnostic: compare main contrast with/without predeclared extreme observations as *sensitivity only*, inspect contributions from days/events and flag a visual change driven by very few independent dates. Don't silently exclude extremes from primary charts.
7. Crosschecks a small deterministic sample of plotted points against source rows and reported OLS/conditional-mean statistics. Use controlled seeds and report passed/failed assertions.
8. If the execution environment supports image opening, **visually inspect** the five summary images and the overview before finalizing; if not, explicitly state that the QA is programmatic only. Do not claim subjective visual verification that did not occur.
9. For intentionally blocked experiments, still produce a readable status graphic showing the actual missing source/coverage check. It must **not contain fabricated plotted economic curves**.

**Mandatory automated anti-mixup test:** each figure must carry a sidecar `*.meta.json` with `experiment_id`, `config_sha256`, `source_manifest_sha256`, `input_fingerprint`, `target`, `predictor`, `state`, `independent_unit`, `time_range`, `plot_data_sha256`, `figure_sha256`. Confirm the metadata matches the folder and data. Inject a wrong-ID or wrong-target sidecar in a disposable fixture and prove the verifier rejects it. The consolidated report may include only **verified** figures; replace failed charts with explicit `QA FAIL` blocks rather than silently presenting them.

---

## 5. Coding, testing, and reproducibility requirements

- Implement shared data-discovery, data-source registry, one-pass streaming extraction, feature computation, experiment-contract assertions, exploratory statistics and rendering as **small documented modules**. Avoid five divergent copies of identical aggregation code.
- Keep test fixtures tiny, synthetic and separate from real plots; tag every test fixture as synthetic. No software dependency download large enough to endanger the 10 GB budget. Use installed common packages where feasible (PyArrow, Pandas, NumPy, statsmodels, matplotlib, Pillow).
- Follow existing repo testing conventions and `AGENTS.md`, including docstrings, clear exception messages, deterministic seeds and reproducibility snapshots. No touching source raw data; write no accidental notebooks with inline duplicated datasets.
- Provide unit/integration tests: source hash/provenance; dataset-to-experiment contract; timezone and DST; correct 5-minute synchronized bars; semivariance identity; next-trading-day mapping; volume lookback excluding current day; Treasury source identity/return-window; FRED lag availability; Fed shock sign/bp/event join; month-checkpoint resumes; stale-config detection; disk-cap simulation; negative “intentional mismatch” fixtures; plot metadata and embedded links.
- All shared data and configs read-only after validation; data updates require a new source/version or atomic, validated partition repair. Never silently edit frozen v1 configs after the first screen.
- Record any actual deviation from proposed bootstrap, instrument universe, state thresholds, sample eligibility or sources. Minor nonsemantic fixes may be automatic; significant design changes are **STOP / ESCALATE**.
- If runtime or context ends early, produce a resumable `checkpoints/current_stage.json` with completed months/sources, hashes and next action. Resume from this without re-fetching completed months or recomputing completed verified experiments. A partial result must not claim five completed screens.

### Permission / escalation boundary

You may autonomously repair minor API paths, CSV separators, expected schema aliases **after verifying meaning**, timezone parsing, temp-file cleanup, retry interrupted months, adjust plot cosmetics, and optimize bounded-memory processing.

You **may not** silently: change X/Z/Y, horizon, clock window, return adjustment convention, source provider, stock universe based on results, state thresholds based on target plots, observed bars into forward-filled synthetic 1-minute prices, FOMC shock definition, minute to 30-minute substitute for P01/P02/P05, ETF instrument substitution, total 10 GB cap, or the primary estimand. If a needed variable is genuinely inaccessible, produce `DATA HOLD` for that experiment and proceed with other valid ones.

---

## 6. Definition of done and final Codex response

**The job is complete only when:**

- [ ] Original A/B/C and unrelated repository data are unmodified.
- [ ] One data union, one approved large HF source/revision, and **at most one validated acquisition per needed month** are evidenced in machine-readable logs; no duplicate full passes or mirror mixing.
- [ ] Peak **incremental** storage and any stricter physical cap are verified below 10 GB, including raw monthly temps and caches; remaining temporary raw monthly archives are deleted after validation.
- [ ] Five separate configurations, source/target/state contracts and input hashes exist and have passed **preflight isolation checks**.
- [ ] All available inputs were derived from the correct sources and time conventions; deliberately corrupted fixtures fail closed.
- [ ] Each P01–P05 has a separate readable `report.md`, results, plots, plot-data tables and QA; or a precise `DATA HOLD` with reason and no fabricated results.
- [ ] `reports/five_experiment_prelim_closeout_v1.md` summarizes **all five** and contains verified Markdown image references to actual files.
- [ ] Six standalone reviewer images (five summaries + overview) and `reports/five_experiment_prelim_review_bundle_v1.zip` exist and match the final report. All figure paths are valid.
- [ ] Programmatic image/plot QA, consistency tests, storage/source-integrity checks and explicit negative-case tests have **actually run** and are logged.
- [ ] All dates examined are marked exploratory. Decisions are `GO/WEAK/NO-GO/DATA HOLD`, with distinctions between changing slopes, curvature and uncertainty.
- [ ] Reproducible git/code/config/source hashes, dependency environment and per-stage session reports are included.

**In the final Codex message:** present a concise status matrix P01–P05 with valid days/events, outcome, GO/WEAK/NO-GO/DATA HOLD, blockers, run/storage peak, and the exact relative paths to the consolidated Markdown, review bundle and six reviewer PNGs. Explicitly tell the user to **upload the consolidated `.md`, the review ZIP and the six PNGs to the EBM Theory ChatGPT chat** for scientific interpretation. Do not claim a result if its actual data and figure have not been generated. Preserve every genuine negative result.

**Stop after reporting.** Do not launch a full EBM architecture sweep, trading backtest, another research project, or a second Hugging Face data pass.
