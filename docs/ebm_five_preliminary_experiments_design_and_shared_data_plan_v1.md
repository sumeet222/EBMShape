# Five State-Dependent EBM Research Experiments — Preliminary Designs and Shared-Data Plan

**Document status:** Preliminary scientific designs **v1.0**, 22 October 2026. **Not** a Codex execution prompt, downloaded dataset, completed analysis, or commitment to full EBM fitting. Intended location: `docs/` in the SAE/trading project. The **next separate request** will turn this specification into a staged Codex prompt.

## 0. What this covers, and what it does not

The five experiments are the remaining ranked candidates **#1, #2, #3, #5 and #6** from the latest shortlist, *excluding #4 (the already pursued Experiment C)*. They are separate from the earlier Experiments A (monthly turnover), B (closing-half-hour returns), and C (normalized intraday volatility profiles). Do not reuse those experiment letters or overwrite their configurations/results.

| New immutable ID | Working name | Existing economic relation | Question for the preliminary screen |
|---|---|---|---|
| `P01_INTRADAY_BETA` | Intraday market-response shapes | Market betas change across the trading day | Do conditional stock-return versus SPY-return curves, especially their slopes and downside behavior, differ by clock-time state? |
| `P02_SIGNED_RV` | Downside composition and future volatility | Negative-return realized variation has a different relationship with future volatility than positive-return variation | Does the **future-volatility-versus-total-RV** curve change when the proportion of negative semivariance changes? |
| `P03_TREASURY_HEDGE` | Treasury hedge-response functions | Stock–bond comovement changes with economic conditions | Does the contemporaneous Treasury ETF return response to equity returns vary with *pre-observed* rate/yield-curve states, especially on equity down days? |
| `P04_VOLUME_REVERSAL` | Volume-conditioned daily reversal | The next-day return response to a return shock differs by trading volume | Do the next-day-return-versus-today-return curves have meaningfully different slopes or shapes in high and low *relative* volume states? |
| `P05_FOMC_RESPONSE` | Asymmetric monetary-policy surprise response | Intraday stock responses differ for positive and negative monetary-policy surprises | Do market event-return curves differ by surprise sign and/or magnitude? Are there enough independent events to make any shape claim? |

**Scientific objective:** This is a *cheap shape-feasibility screen*, not a search over many EBM configurations. A **reproducible state-dependent linear slope** is enough to justify subsequent EBM exploration. Nonlinear curvature is a separate and more demanding question. **No EBM fitting in this preliminary stage.** A negative screen can justify not proceeding, but visual differences alone are not confirmatory evidence.

## 1. Shared data requirements — inventory before downloading

### 1.1 Available inputs to look for first (no assumptions about actual path)

1. Existing SPY **1-minute** data and any other 1-minute stock/ETF data generated or retained for former Experiment B/C. Verify actual files, source and valid date coverage; do not infer availability from prior plans.
2. The earlier **99-stock, 30-minute** shared market dataset, if present. It can supply preliminary daily bars for `P04`, and limited broad intraday-beta diagnostics for `P01`; 5-minute beta analysis requires minute data. Inspect original/imputation masks: **never use forward-filled minutes as genuine trades** for realized-variation or event studies.
3. Existing daily/macro files or API-download manifests. Validate ticker, adjustment status, provenance, timestamp and permissible use before reuse.

**First output of the future Codex job:** a no-download inventory: file paths, checksums, schemas, tickers, exact day/time coverage, missing minutes, split/adjustment status, legal/license notes, existing byte footprint, and a source-to-experiment availability matrix. No multiple directory copies.

### 1.2 Only when missing, download from these verified free routes

| Source ID | Public source | Required subset; do **not** download entire archive | Experiments | Qualification |
|---|---|---|---|---|
| `HF_MINUTE_A` | [mito0o852/OHLCV-1m](https://huggingface.co/datasets/mito0o852/OHLCV-1m), or documented duplicate [ggaddam/OHLCV-1m](https://huggingface.co/datasets/ggaddam/OHLCV-1m) | Monthly Parquet **once per needed month**, filter a frozen **union of requested tickers** and regular-session minutes. Main symbols: `SPY`, `CAT`, `JNJ`, and a small diverse group of other liquid equities that pass an independent coverage check; optionally `IEF`/`TLT` if present and trustworthy | P01, P02, P04, P05; possibly P03 | Enormous (~84 GB) full archive; files are monthly. Documented 1-minute OHLCV fields: `timestamp` UTC, `ticker`, OHLC, volume. Monthly availability and ticker presence must be checked from metadata before claiming coverage. Data accuracy/adjustments are **not guaranteed**. **Choose either dataset clone, not both.** |
| `HF_ETF_DAILY` | [thecharttruth/etf-data](https://huggingface.co/datasets/thecharttruth/etf-data) | Tiny `etf_daily_prices.parquet` and instrument metadata; filter `SPY`,`IEF`,`TLT` (or other preapproved Treasury ETF). Advertised snapshot ~2021-05 through 2026-06 | P03 | Teaching/research snapshot, custom license, OHLCV; dividends/splits and total-return adjustments must be checked. Do not pretend unadjusted ETF close-to-close is a Treasury total return. |
| `FED_RATES` | [FRED](https://fred.stlouisfed.org): [DGS2](https://fred.stlouisfed.org/series/DGS2), [DGS10](https://fred.stlouisfed.org/series/DGS10), [DFF](https://fred.stlouisfed.org/series/DFF); [ALFRED](https://fred.stlouisfed.org/) vintages if needed | Daily observed rate/term-structure levels; convert units and lag to information time | P03 | The *calendar date* of a published macro series does not necessarily equal the time it became available. For a preliminary lagged-rate state, prior-day available observations are preferred; log any publication-lag uncertainty. |
| `FED_SHOCKS` | [San Francisco Fed Monetary Policy Surprises](https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/); optionally [US Monetary Policy Event-Study Database](https://www.frbsf.org/research-and-insights/data-and-indicators/us-monetary-policy-event-study-database/) | Small published XLSX/CSV; FOMC dates and signed shock magnitudes | P05 | The primary shock series is a **30-minute futures-based monetary-policy surprise**, not a quoted target-rate change and not necessarily the original Chuliá et al. measure. Inspect whether dates overlap SPY minute records. |

**No VIX, options, implied-volatility, order-book, or paid-data dependencies.** `P03` need not download `HF_MINUTE_A` for bond prices if valid ETF daily data already suffice. `P05` requires the published shock file, but not raw interest-rate futures data.

**Date approach:** Before inspecting response patterns, set a common date *intersection* for minute-based P01/P02/P04/P05 wherever feasible; the FOMC sample can also use its entire valid SPY-minute overlap. The source archive's documented monthly minute files extend through at least early 2026, but **do not assume any particular month/ticker is present**. The existing local 2026 data may extend further. P03 uses its own validated ETF/FRED overlap. Report dates **per source and per experiment**; never silently pool distinct eras or infer an overlap from a dataset title.

**Universe scope:** For the initial screen use SPY plus **roughly 10–20 liquid equities at most** from the existing 99-stock roster (e.g., CAT and JNJ as literature-linked anchors), selected by *data coverage and predeclared sector/beta diversity*, not by seeing the response plots. Tickers must be logged in an immutable union list. The selected surviving-stock sample is **not** a replication of a historical S&P 500 membership panel.

## 2. One-pass extraction and hard storage constraints

### 2.1 Storage and downloads

**Hard upper limit: 10 GB of *incremental* local disk usage attributable to this project**, including retained data, temporary monthly files, Hugging Face/Datasets caches, outputs, models, virtual-environment additions and archives. Record the existing directory's pre-job usage separately. If the physical 10 GB limit applies to the entire workspace rather than the new job, verify that explicitly before processing; do not assume existing files count as zero. **Stop before crossing the limit.** Recommended targets: ≤3 GB permanent shared data, ≤2 GB maximum transient/cache, ≤1 GB experiment artifacts, remaining capacity as safety margin. These are planning caps, not evidence that downloads will fit.

**Only one source-pass for the big archive:**

1. First audit all existing local data; construct a frozen union of all required tickers, date ranges and columns **across all five experiments**. Compute a single metadata inventory before transferring large files.
2. Choose one official Hugging Face repository/revision and record commit hash, file manifest, source checksum or ETag when available, and rights/terms. **Do not use `load_dataset(...).to_pandas()` on the complete dataset or clone/snapshot the 84 GB repository.**
3. Process **one month at a time**, preferably with remote Parquet row-group/range reads and predicate pushdown if the remote format/server supports them. If not, download *only that single monthly Parquet*, stream its row groups in bounded batches, filter immediately by ticker/date/regular-session, and drop all irrelevant rows.
4. Write each accepted month **once** to a small partition in `data/shared/market_1m/`; retain original timestamp, observed OHLCV and validity flags. Derive compact, reusable 5-minute, 30-minute and daily features in shared `data/shared/derived/`, not in five separate experiment copies. Preserve raw selected 1-minute data only if needed; avoid duplicating it with pre-existing good files. `P03` and `P05` reference small shared macro/event tables.
5. After each month: validate row counts and OHLC invariants, flush outputs and manifest, verify checksum, delete the **raw monthly temporary file**, evict attributable cache, check disk usage, then proceed. The peak must remain below the limit even during downloading and decompression.
6. Make the pipeline **idempotent/resumable**: store per-month status `not_started/in_progress/validated`, revision, date, ticker list, checksum and row counts. Resume without re-downloading validated chunks. No second full sweep of Hugging Face for a later experiment.
7. If monthly files are too large for temporary storage or random-access reads do not work, **STOP** with a technical feasibility report; do not exceed 10 GB and do not substitute a different source without approval.

**Budget/cleanliness checks:** run `du` or equivalent before/after every month; retain compact manifests, plots and summaries; do not move or delete unrelated archived experiment files. The 10 GB constraint covers hidden caches and interrupted partial downloads too.

### 2.2 Physical layout: one canonical data copy, five isolated analyses

```text
docs/
  ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md
configs/
  prelim_shared_sources_v1.yaml
  prelim_P01_INTRADAY_BETA_v1.yaml
  prelim_P02_SIGNED_RV_v1.yaml
  prelim_P03_TREASURY_HEDGE_v1.yaml
  prelim_P04_VOLUME_REVERSAL_v1.yaml
  prelim_P05_FOMC_RESPONSE_v1.yaml
data/
  shared/
    source_manifest.json
    market_1m/                 # only retained needed dates/tickers; partitioned
    derived/                   # reusable daily / 5min / 30min summaries
    etf_daily/
    fred_rates/
    fed_surprises/
experiments/
  P01_INTRADAY_BETA/  results/ plots/ diagnostics/ report.md
  P02_SIGNED_RV/      results/ plots/ diagnostics/ report.md
  P03_TREASURY_HEDGE/ results/ plots/ diagnostics/ report.md
  P04_VOLUME_REVERSAL/results/ plots/ diagnostics/ report.md
  P05_FOMC_RESPONSE/  results/ plots/ diagnostics/ report.md
reports/
  shared_data_inventory.md
  shared_download_integrity.md
  five_experiment_prelim_comparison.md
```

Exact directory names may be adapted to the existing repository **once**, before experiments begin, to avoid collisions. Experiments must reference shared data read-only and write only under their own `experiments/<ID>/` folder. No repeated full market-data exports in results folders. All plots/data tables must carry `experiment_id`, `config_hash`, `source_manifest_hash`, and date range in accompanying machine-readable metadata.

### 2.3 Mandatory cross-experiment isolation gates

Before **each** experiment starts, fail closed unless:

- Its exact experiment ID, own immutable config/version, output directory and expected target/predictor/state definitions agree.
- Its actual input asset symbols, frequencies, UTC-to-New-York conversion, date intersections, source identifiers, and validation counts match the declared specification. In particular, `P03` must include a **Treasury instrument**, `P05` must use the published FOMC surprise file, and `P02` must use observed minute returns rather than fake filled bars.
- Its `input_fingerprint` (hashes of all referenced shared partitions plus macro/event files) is computed and logged. A checksum mismatch aborts analysis; it does **not** fall back to an identically named file from Experiment A/B/C.
- Its config explicitly points to its own report/plot paths and is never modified in place after a screen begins. Corrections create a versioned replacement; no stale plot/model reuse.
- A machine-readable schema asserts variables, units, expected frequency, time-of-availability, primary-versus-sensitivity definition and dependency source. Date joins use unique keys with `many_to_one` / `one_to_one` validation; duplicates or unexpected missing joins raise an error rather than silently expand records.

## 3. Five *minimal* preliminary experiment designs

All states and contrasts below are **screening proposals**, not claims of reproduced source statistics. Use **simple conditional means, grouped regressions/plots, and date-aware uncertainty; do not run EBMs now**. Record common-support restrictions and sample size directly on every plot. Reserve chronologically later data for potential confirmatory EBM experiments; exploratory screens must not claim untouched-test significance.

### P01_INTRADAY_BETA — intraday market-response curves

**Reference:** Andersen, Thyrsgaard & Todorov (2021), *Recalcitrant betas: Intraday variation in the cross-sectional dispersion of systematic risk*, *Quantitative Economics*, [DOI](https://doi.org/10.3982/QE1570). Published evidence: beta dispersion is elevated early and declines toward the close. Original research uses SPY, three-minute returns and excludes the opening half-hour; our sample/universe may differ.

- **Required inputs:** SPY and a prespecified 10–20-stock minute subset, regular U.S. sessions. Five-minute synchronous SPY/stock close-to-close intraday returns from genuine minutes; preserve original 3-minute method only as a possible later closer replication. No overnight price jumps.
- **Response:** stock five-minute log return `r_i(t)`. **Focal predictor:** simultaneous SPY five-minute log return `r_M(t)`. **State:** clock-time group `early` (10:00–11:30 ET), `mid` (11:30–14:00 ET), `late` (14:00–16:00 ET); endpoints must be assigned exactly once. This primary exploratory grouping excludes 09:30–10:00.
- **Minimal tests:** per-state scatter/hexbin, equal-support binned conditional means, per-state OLS slopes plus uncertainty, pooled state-interaction slope tests, a panel of CAT/JNJ and other frozen symbols, cross-stock dispersion of fitted slopes. Plot fixed same-x anchors and separately examine down/up-market bins. Check returns in basis points rather than raw prices.
- **Expected historical benchmark:** systematic intraday beta-dispersion change; **nonlinear curvature is not promised**. A plain beta change qualifies as state dependence but must be distinguished from nonlinear shape. Compare strong downward/upward exposure patterns if enough independent days.
- **Sampling/QA:** SPY and stocks at exact same five-minute times; no forward-filled artificial returns; date/time-group masks; stock/day clustering and block-by-date bands. Do not treat correlated stocks as independent days.
- **GO screen:** supported slope contrasts across times, or credible response-shape contrasts for a meaningful x-range, recurring across temporal slices. **WEAK/NO-GO:** unstable/unsupported large-return tails; little time variation; only spurious results created by missing synchronous prices.

### P02_SIGNED_RV — realized-volatility persistence conditioned on downside composition

**Reference:** Patton & Sheppard (2015), *Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility*, *Review of Economics and Statistics*, [DOI](https://doi.org/10.1162/REST_a_00503). Published evidence: past negative-return variance is more strongly related to subsequent variance than past positive-return variance. The benchmark is **realized semivariance**, not implied volatility.

- **Required inputs:** verified observed intraday one-minute closes for SPY and, if adequate, a frozen subset of liquid stocks. Form only within-session minute returns. Omit suspect/gap-filled days, include valid day flags.
- **Derived at end of day d:** `RV_d = Σ r_{d,k}²`; `RS_minus_d = Σ r² 1(r<0)`; `RS_plus_d = Σ r² 1(r>0)`; downside share `q_d = RS_minus_d/RV_d` when positive. Confirm `RS_minus + RS_plus == RV` to numerical tolerance. `RV_{d+1}` is the target on the next observed session. In displayed curves use `log(RV+epsilon)` only with one globally declared legitimate epsilon; compare raw RV and volatility-scaled choices in sensitivity, not arbitrarily.
- **Response:** next-session `log RV`. **Focal predictor:** current `log RV`. **State:** current downside share q, grouped into prespecified 0–1/3, 1/3–2/3, 2/3–1 buckets, and continuous-q scatter/smooth binned views. A group may be merged *only through a new declared sensitivity configuration* if sparse.
- **Minimal tests:** (i) OLS using separate positive and negative semivariances, (ii) controlled baseline using current total RV and short lagged RV history, (iii) q-conditional `log RV_d` versus `log RV_{d+1}` curve overlays on shared log-RV support, (iv) signed slope and anchored shape contrasts; optional market-only and pooled-stock displays separately.
- **Expected benchmark:** stronger future-volatility response to negative than positive realized semivariance; **nonlinear q-specific curve changes remain to be evaluated**, not guaranteed by the paper. The algebraically changing slope implied by unequal coefficients is a useful expected structure.
- **QA:** no overnight changes inside RV, no fake 1-minute bars, no use of `d+1` information in states, remove holidays/short sessions or handle separately, correct calendar-next trading day, independent date/week block intervals. If within-day return sampling frequency differs from source, mark as approximation.
- **GO screen:** replicated sign asymmetry and supported changes in slopes/curves across q; **WEAK/NO-GO:** insufficient one-minute coverage; missingness drives semivariance ratios; no reliable effect after controlling for lagged RV.

### P03_TREASURY_HEDGE — conditional Treasury response in rate/yield states

**References:** Campbell, Sunderam & Viceira (2017), *Inflation Bets or Deflation Hedges? The Changing Risks of Nominal Bonds*, *Critical Finance Review*, and Aslanidis & Christiansen (2012), *Smooth transition patterns in the realized stock–bond correlation*, *Journal of Empirical Finance*. These motivate state dependence, **not** a guaranteed nonlinear conditional-mean curve without IV.

- **Required inputs:** daily equity `SPY` and Treasury `IEF` (primary, if valid) or `TLT` (predeclared secondary) ETF prices from verified local minute data aggregated to daily **or** `HF_ETF_DAILY`; FRED prior-available `DGS2`,`DGS10`, optionally `DFF`. Use ETF *intraday open-to-close* returns for the initial screen if total-return adjustments cannot be verified. For an economic close-to-close hedge study require correctly adjusted total returns; report if unavailable.
- **Response:** same-day Treasury ETF return (`IEF` primary). **Focal predictor:** same-day SPY return under the *same clock-window convention*. **State:** prior-available 10Y–2Y yield spread (low/mid/high terciles of training/historical state distribution). Secondary state: prior-available 10Y yield level; do **not** mix these state definitions.
- **Minimal tests:** state-stratified stock-versus-Treasury scatter/conditional means; fitted OLS beta per state; anchored Treasury response between predeclared SPY loss/neutral points; compare downside and upside segments only on overlapping observed support. Separate periods (e.g., inflation/stress eras) when sample dates permit, reporting independent day counts.
- **Expected benchmark:** comovement varies with economic conditions, but the sign/shape under **this specific** rate-only state and time sample is **not guaranteed**. A state-specific sign reversal would be interesting, but it is not the only acceptable finding.
- **QA:** synchronize ETF date/session; corporate-action/dividend adjustments; prove rate observation was already available (use lag), holiday alignment, do not substitute yield *change* for bond return without naming a different target. CI with week/month blocks. If no credible Treasury return series and adjustment protocol exist, mark **DATA HOLD**, not fake results.

### P04_VOLUME_REVERSAL — daily return response conditioned on stock volume

**Reference:** Campbell, Grossman & Wang (1993), *Trading Volume and Serial Correlation in Stock Returns*, *Quarterly Journal of Economics*, [DOI](https://doi.org/10.2307/2118454). They report that daily return autocorrelation tends to decline as volume increases. The optional nonlinear comparator is McMillan (2007), *Non-linear forecasting of stock returns: Does volume help?*, *International Journal of Forecasting*.

- **Required inputs:** existing 99-stock **original observed** 30-minute OHLCV aggregated to daily, preferably reusing already audited price/volume fields; supplement only missing chosen symbols/date coverage from shared `HF_MINUTE_A`. Do not use the full 99 unless necessary; freeze ~10–20 liquid stocks first. Handle splits/corporate actions; close-to-close source-compatible daily returns need adjustment verification.
- **Response:** next-trading-day return `r_{i,d+1}`. **Focal predictor:** same-stock daily return `r_{i,d}`. **State:** same-stock log volume relative to **prior 20 eligible trading days** (e.g. `log V_d − mean(log V_{d-20:d-1})`); freeze definition, and make sure today's volume is known at the prediction timestamp after close. Distinguish raw volume from share turnover (no historical shares outstanding required).
- **Minimal tests:** volume-state tercile return-autocorrelation slope comparisons, daily-return binned conditional means (same `x` grid) by volume state, high-volume negative-move versus low-volume negative-move response; market-wide versus stock-level analysis separately. Basic controls: broad-market same-day return, optionally one volatility scale, predeclared only.
- **Expected benchmark:** more negative daily return autocorrelation at higher volume, in the *historical reference*. It may be weak in a recent, liquid, survivorship-biased sample. An apparent EBM-friendly nonlinear curve is exploratory until held-out confirmation.
- **QA:** verify daily volume is sum of *real*, non-imputed bar volume; do not use price-adjusted volume naively across splits; account for adjacent-day overlap, date-level cross-sectional correlation, block/week uncertainty; pre-specified extreme-return winsorization only as sensitivity, not data-dependent deletion.
- **GO screen:** directional difference in high/low volume slopes and supported curves; **WEAK/NO-GO:** inconsistent across dates or outlier-dependent; evidence only on improperly adjusted prices; no relevant common x support.

### P05_FOMC_RESPONSE — tightening/easing surprise magnitude and intraday stock response

**References:** Chuliá, Martens & van Dijk (2010), *Asymmetric effects of federal funds target rate changes on S&P100 stock returns, volatilities and correlations*, *Journal of Banking & Finance*, [DOI](https://doi.org/10.1016/j.jbankfin.2009.09.012); Bauer & Swanson (2023), *A Reassessment of Monetary Policy Surprises and High-Frequency Identification*. The San Francisco Fed series is an updated *futures-based* shock measure, so it is a **related modern adaptation**, not exact original-measure replication.

- **Required inputs:** SPY minute OHLCV on official FOMC announcement dates, and the free SF Fed **signed** surprise series. Stock-level minute response is an *optional* secondary branch; never treat stocks on one event as independent surprises.
- **Response:** SPY same-event market log return in a predeclared, fully available window, e.g. **14:00–14:30 ET** for standard 2 p.m. announcements. Record event timestamps and alternate release schedules; use exact window endpoints and carry a 13:55–14:00 pre-window for QA, not as an arbitrary redefinition. If published shock uses overlapping 30-minute futures windows, label the analysis **contemporaneous event association**, not an ex-ante return forecast or independent causal identification.
- **Focal predictor:** `abs(policy_surprise_bp)`. **State:** surprise sign (`positive` tightening-path surprise versus `negative` easing-path surprise), with zero/near-zero handled explicitly. Plot also signed surprise versus return for a benchmark. This is a distinct sign-versus-magnitude nonlinear screen.
- **Minimal tests:** event scatterplots with labeled dates, per-sign binned/smoothed conditional return curves only when enough events, OLS signed slope and sign×magnitude interactions, outlier/large-event leave-one-out plots, uncertainty **by independent event** (not number of stock-minute records). Include comparison with a nonannouncement-day distribution as context, not as synthetic surprise=0 events.
- **Expected benchmark:** asymmetric immediate stock responses to policy news as reported historically. **Sample size is the hard limiter.** If the usable overlap has too few independent positive/negative events or the magnitude support is sparse, return `WEAK` or `DATA HOLD` rather than claiming a recovered functional shape.
- **QA:** verify actual policy release times, surprise sign convention and bp units, shock coverage and vintage, minute timestamp boundaries, early closing days and missing bars, event-day duplicates, overlapping shock-window interpretation. A few 2024–2026 FOMC events cannot support a richly flexible curve.

## 4. Common preliminary diagnostics and visual QA (automatic in subsequent Codex job)

For **each** `P01`–`P05`, the screening job must generate only a small set of plots and tables:

1. **Source/support panel:** exact date range, ticker/event counts, per-state independent days/events, state×predictor support bins; missingness and extreme-value summary.
2. **Core curves:** observed conditional binned means across a **common feature grid**, state overlays with confidence bands; one plot of state contrast/difference, with baseline varying-slope fitted lines. For P01 show representative stock curves and cross-stock beta distribution; for P02 log-RV and semivariance controls; P03 down/up SPY range; P04 high/low volume; P05 event scatter/annotations.
3. **Sensitivity panel:** split-period or block-resampled profiles, with axes fixed across states; negative result needs plots too. Do not add an enormous grid of unconstrained exploratory figures.
4. **Machine tests on plots:** arrays actually used to generate each plot saved in compact CSV/Parquet; verify axes, units, counts, equal x comparisons, legend names, state labels, date boundaries, nonempty/error-free bands, source hash; automatically flag clipping, empty bins, zero-variance estimates and visual contrast driven by ≤5 independent dates/events.
5. **Report:** `GO` / `WEAK` / `NO-GO` / `DATA HOLD`, plus **why**, direction and magnitude of predeclared slope/shape contrasts, bootstrap/block uncertainty, independent-unit count, failures, and known limitations. `GO` means worth further modeling, **not** a new discovery or statistical validation.

Use day-block or week-block bootstrap for market data as appropriate, and event-level resampling for P05; declare block size and repeat seed in each config. For pooled stocks, resample whole trading dates so cross-stock shocks stay together. Do not imply a justified finite-order dependence theorem merely because a bootstrap was run. Bootstrap distributions may be unstable in scarce-event or sparse-tail states; explicitly abstain.

**No-look-ahead:** All future-response screens must construct predictors/states using information known before their target period. P01/P03 contemporaneous conditional response and P05 event association are **descriptive/risk relationships**, not trade-entry forecasts. Do not claim profitability.

### Universal freeze/decision gate

- **Pre-screen freeze:** symbol universe, dates or freeze rule based on *data coverage only*, source revision, state thresholds (training-sample terciles where applicable), raw target definition, normalization, plot specifications, statistical uncertainty method, split dates and material effect scale.
- **Pass** if a stated relation is directionally meaningful and reasonably supported over common predictor support; curvature not necessary. No-go if only high-noise extrapolation, an invalid data proxy, or a mismatched target accounts for the pattern. Separate `SCIENTIFICALLY NEGATIVE` from `DATA INVALID` and `INCONCLUSIVE`.
- **Post-screen:** Keep the preliminary screen's inspected period marked exploratory. If promoting an experiment, reserve genuinely untouched later dates/events, or explicitly acknowledge that no clean confirmatory holdout exists.

## 5. Source-specific research expectations and references

The links below identify **literature motivation** and **data**; they are not proof that the user's local data reproduce the findings:

1. Andersen, T., Thyrsgaard, M. & Todorov, V. (2021), [*Recalcitrant betas: Intraday variation in the cross-sectional dispersion of systematic risk*](https://doi.org/10.3982/QE1570), *Quantitative Economics*. Source uses SPY proxy and 3-minute stock observations, excluding first half hour.
2. Patton, A. & Sheppard, K. (2015), [*Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility*](https://doi.org/10.1162/REST_a_00503), *Review of Economics and Statistics*. Signed realized semivariance and next-volatility predictability.
3. Campbell, J., Sunderam, A. & Viceira, L. (2017), [*Inflation Bets or Deflation Hedges? The Changing Risks of Nominal Bonds*](https://doi.org/10.1561/104.00000043), *Critical Finance Review*; Aslanidis, N. & Christiansen, C. (2012), *Smooth transition patterns in the realized stock–bond correlation*, *Journal of Empirical Finance*.
4. Campbell, J., Grossman, S. & Wang, J. (1993), [*Trading Volume and Serial Correlation in Stock Returns*](https://doi.org/10.2307/2118454), *Quarterly Journal of Economics*; McMillan, D. (2007), *Non-linear forecasting of stock returns: Does volume help?*, *International Journal of Forecasting*.
5. Chuliá, H., Martens, M. & van Dijk, D. (2010), [*Asymmetric effects of federal funds target rate changes on S&P100 stock returns, volatilities and correlations*](https://doi.org/10.1016/j.jbankfin.2009.09.012), *Journal of Banking & Finance*; [FRBSF Monetary Policy Surprises](https://www.frbsf.org/research-and-insights/data-and-indicators/monetary-policy-surprises/).
6. [HF OHLCV-1m, primary candidate](https://huggingface.co/datasets/mito0o852/OHLCV-1m); [HF OHLCV-1m mirror](https://huggingface.co/datasets/ggaddam/OHLCV-1m); [HF ETF daily research dataset](https://huggingface.co/datasets/thecharttruth/etf-data); [FRED](https://fred.stlouisfed.org/); [FRBSF US Monetary Policy Event-Study Database](https://www.frbsf.org/research-and-insights/data-and-indicators/us-monetary-policy-event-study-database/).

## 6. Contract for the **next** Codex-prompt-generation step

The next chat/prompt should **not redesign these five experiments**. It should convert this file into a staged Codex execution plan with, in order:

1. **Stage 0 — inventory and zero-download audit:** inspect repo, storage, existing files, source coverage and access/terms, output data-union manifest and disk forecast; stop on incompatible assumptions.
2. **Stage 1 — common-source acquisition only once:** small Fed/ETF downloads plus one streaming/month-by-month union-filtering pass over Hugging Face **only if needed**, storing unique shared outputs, purging each raw month before moving on; enforce <10 GB incremental peak.
3. **Stage 2 — shared-feature validation:** time-aligned one-minute/5-minute/daily returns, RV/semivariance, correctly lagged rates, FOMC event joins, metadata/hashes and consistency tests. No model fitting.
4. **Stage 3 — independent P01–P05 preliminary screens:** each must check source/target/experiment ID and write its own plots, results, diagnostics, small report. Parallel computation is optional only when shared-data immutability and disk headroom are guaranteed.
5. **Stage 4 — joint *comparison report only*:** summarize GO/WEAK/NO-GO/DATA HOLD, strengths/limitations and recommended full-experiment selection, while leaving all original outputs intact. No EBM or optimization hyperparameter search.

**Exception authority:** Codex may autonomously handle minor file path/schema differences, pagination, failed network chunk retries, plot-layout issues and finite floating-point precision if source, estimand, horizon, universe and statistical meaning stay unchanged. Escalate any substitution of predictors/states/responses, different financial instrument, change from genuine 1-minute to imputed data, redefining event time, unvalidated adjustment, dropping a requested experiment, or change to the storage budget.

**Final requested deliverables from that subsequent execution**: per-experiment compact QA report, plots and plot-source data, immutable configs + hashes, common data provenance/index, storage-usage logs with peak, bibliography/assumption notes, and summary decision matrix. No user-facing conclusion of strong EBM scientific shape effects should be issued before reviewing these preliminary results.
