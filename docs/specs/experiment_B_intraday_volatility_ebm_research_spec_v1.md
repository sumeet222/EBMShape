# Experiment B — Volatility-Conditioned U.S. Market Intraday Momentum
## Literature-grounded replication and nonlinear EBM extension | Research specification v1.0

**Prepared:** 14 October 2026  
**Purpose:** Authoritative scientific and experimental specification for a *new implementation/results chat*. That chat will produce staged Codex instructions, run diagnostics on returned artifacts, and report results back to the EBM Theory/design thread. This document is **not** a Codex prompt, a completed experiment, or a claim of financial success.  
**Scope:** **Experiment B only.** The turnover-conditioned monthly short-term reversal/momentum study (**Experiment A**) is deliberately excluded and will have its own chat.  
**Research posture:** **Replicate a documented U.S. relationship, then investigate conditional nonlinear shape, representation, stability, and economic value**. A failed modern replication or a simpler model outperforming the EBM is an acceptable and reportable result. Do not tune until positive findings appear.

---

## 0. Decision register and what is frozen

| Dimension | Chosen design / default | Status and allowed change |
|---|---|---|
| Market and security | U.S. **SPY ETF**; one observation per eligible trading date | **FROZEN primary universe**. QQQ/IWM only separately named secondary portability checks, never silently pooled into SPY. |
| Literature | Gao, Han, Li & Zhou (2018), JFE; Limkriangkrai, Chai & Zheng (2023), PBFJ | **FROZEN principal references**. Source-era access may be restricted. |
| Dependent variable | Final regular-session 30-minute **SPY price return**, 15:30–16:00 America/New_York | **FROZEN scientific target**. A realizable post-signal trade P&L is a *different* economic outcome. |
| Opening predictor | Previous regular-session close to **10:00 ET current date**, including overnight | **FROZEN**. Do not silently substitute 09:30–10:00 alone. |
| Late predictor | **15:00–15:30 ET** return | Primary conditional model at a 15:30 decision. A separate early-information model excludes it. |
| Primary state | **Realized opening-half-hour SPY volatility calculated from one-minute regular-session prices** | **FROZEN concept**; exact operational proxy in §4. The exact paper formula must be checked/qualified. Not VIX and not overnight/trailing 20-day volatility. |
| State representations | **Same numerical state** both as predeclared terciles and as continuous log-volatility input | **FROZEN principal comparison**; terciles may be retrospective for source-style tables versus past-only for live prediction. |
| Learner | OLS source benchmarks, simple interaction and smooth varying-coefficient alternatives, then deliberately small EBMs | EBM is an **extension**, not the source estimator. No unrestricted feature discovery. |
| Primary scientific question | Does volatility change the **shape/strength** of the relation between opening and closing-half-hour returns? | Distinguish within-state significance from a *between-state difference*; distinguish nonlinear model display from raw conditional mean. |
| Data policy | Reuse existing data where exact definitions match; download SPY minute data only as needed | **FROZEN no-duplication constraint**. No new 99-stock copies and no 25 GB run directories. |
| Final test | 2024-01-01 through **2026-09-30**, subject to verified coverage | **FROZEN** final test calendar. Source-era and train-period alternatives are specified below, not improvised after seeing outcomes. |
| Protocol changes | Freeze a machine-readable `experiment_B_protocol_v1.yaml` and hashes before final model evaluation | Small operational substitutions can be logged; **scientific changes** require explicit approval/versioning. |

**Three categories must be kept separate:** (i) **historical source-era partial replication**, (ii) **modern U.S. out-of-sample hypothesis validation**, and (iii) **new scientific/EBM shape analysis**. None automatically proves the others.

## 1. Verified published foundation and limits of replication

### 1.1 Primary source: Gao et al. (2018)

Lei Gao, Yufeng Han, Sophia Zhengzi Li, and Guofu Zhou, **“Market intraday momentum,”** *Journal of Financial Economics* **129**(2), 394–414 (2018), DOI **10.1016/j.jfineco.2018.05.009**.

- Journal article: <https://www.sciencedirect.com/science/article/pii/S0304405X18301351>
- DOI: <https://doi.org/10.1016/j.jfineco.2018.05.009>
- Author working-paper record: <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866> (preprint versions need not be identical to the final journal article).

**Published finding.** Using intraday **SPY** data covering **1993–2013**, the authors find that the return measured **from the preceding session close to 10:00** predicts the **15:30–16:00** return. The effect was stronger in higher-volatility, higher-volume, recession, and some macroeconomic-news settings. They also examine a second-to-last-half-hour return. They used the TAQ data source and exclude trading days with fewer than 500 trades. The published paper establishes a historical U.S. benchmark, **not** a guarantee for 2024–2026 or a theorem about EBMs.

### 1.2 U.S. replication and volatility state: Limkriangkrai et al. (2023)

Manapon Limkriangkrai, Daniel Chai, and Gaoping Zheng, **“Market intraday momentum: APAC evidence,”** *Pacific-Basin Finance Journal* **80**, 102086 (2023), DOI **10.1016/j.pacfin.2023.102086**.

- Publisher article (substantial methods/results text): <https://www.sciencedirect.com/science/article/pii/S0927538X2300152X>
- DOI: <https://doi.org/10.1016/j.pacfin.2023.102086>
- Institutional publication record: <https://research.monash.edu/en/publications/market-intraday-momentum-apac-evidence/>

**Relevant published methods and results:**

1. As an internal validation before analyzing Asia-Pacific ETFs, the authors replicate the U.S. S&P 500 ETF analysis over **January 1996–December 2013**. They identify 13 regular-session half-hour periods: `r1` is **prior close to 10:00**, `r12` is **15:00–15:30**, and `r13` is **15:30–16:00**.
2. Their baseline regressions are `r13 ~ r1`, `r13 ~ r12`, and `r13 ~ r1 + r12`; they report HAC/Newey–West-adjusted p-values.
3. **Table 4** divides days into **low/medium/high first-half-hour realized-volatility groups**; volatility is computed from **valid one-minute returns within the opening half hour**. In the U.S. Table 4, the `r1` coefficient is positive and reported statistically significant in **all three** volatility groups, with the largest point estimate in the high group. **This alone does not prove a statistically significant high-minus-low slope difference.**
4. They also investigate opening volume. Their broader cross-market results are mixed, so a U.S. effect must not be described as universal.
5. Their U.S. replication is historical. Their COVID-specific check is an additional period/analysis, not evidence that our sealed modern test must be positive.

**Critical source fidelity note:** The accessible source states that opening volatility is calculated using valid **one-minute returns**, but does not, in the portions verified for this specification, unambiguously settle every detail of its normalizing constant, opening-minute return treatment, and calendar-group cutoff construction. The formula in §4 is therefore an **explicit, reproducible study proxy**, not asserted to be a bit-for-bit reconstruction of the published volatility estimator. The implementing chat must consult full methods/source as available, preserve discrepancies in a replication-difference log, and not silently call a proxy an exact replication.

### 1.3 Scientific claims we can and cannot anticipate

**Evidence-supported expectation:** A *historically* positive opening-to-closing return slope in U.S. SPY, with potential strengthening at high opening realized volatility. An unconditional OOS `R²` on daily noisy returns can be **small** even if a slope is statistically significant. **No theorem or paper guarantees a particular EBM performance gain, sign change, trading profit, or 2024–2026 significance.**

**Our extension, not a published Gao/Limkriangkrai result:** a controlled EBM response surface, continuous versus discretized volatility, support-aware shape contrasts, chronological scientific stability, a transparent selected-model/display audit, and matched trading baselines/costs.

### 1.4 Supporting methodological sources

- Newey, W. K., and West, K. D. (1987), **“A Simple, Positive Semi-definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix,”** *Econometrica* 55(3), 703–708. <https://doi.org/10.2307/1913610>.
- InterpretML, **`ExplainableBoostingRegressor`** API and its explicit `interactions=[(...)]`, categorical/continuous binning, bagging, greedy/smoothing, and version-dependent defaults. <https://interpret.ml/docs/python/api/ExplainableBoostingRegressor.html>; <https://interpret.ml/docs/hyperparameters.html>.
- Massive, **Stocks Aggregate Bars API**: <https://massive.com/docs/rest/stocks/aggregates/custom-bars>; **historical coverage and plan windows**: <https://massive.com/knowledge-base/article/how-much-historical-stock-data-does-massive-have>.
- Internal EBM theory: `state_dependent_ebm_paper1_experiment_theory_v1.tex/.pdf` (scientific targets and experiment protocol), P3 (scientific fidelity), P5 (specified greedy paths are not native software paths), P6 (conditional environmental stability), P7 (selection), P8 (support), plus the **original Task 19, 22–25 reports and v0.25.1 living state**. Their mathematical assumptions are *not automatically satisfied* by stock-market data.

## 2. Research hypotheses, distinct estimands, and falsifiable outcomes

Let `t` denote an eligible U.S. regular trading date, and let

\[
 X_t=r_{1,t},\quad W_t=r_{12,t},\quad Z_t=\log(\mathrm{RV}^{\mathrm{open}}_t+10^{-8}),\quad Y_t=r_{13,t}.
\]

All returns are computed in consistent **simple-return basis-point units**, while `Z` is the log of a dimensionless realized-volatility number; alternative log-return inputs are secondary sensitivity only. Define the observational conditional regression function

\[
 m(x,w,z)=E[Y_t\mid X_t=x,W_t=w,Z_t=z].
\]

No causal interpretation is claimed. The **early-information** function is `m_early(x,z)=E[Y | X=x,Z=z]`, not a late function with `W` artificially held to its mean.

### Hypothesis hierarchy — not interchangeable

| ID | Question and null | Correct evidence |
|---|---|---|
| `H0` historical replication | Is `beta_1 > 0` in the source-style `r13 ~ r1` U.S. historical benchmark? | Source-window OLS coefficient, HAC CI, sample definition, period comparison. No source-era claim if that period is inaccessible. |
| `H1` present-period predictability | Does `r1` add predictive information for `r13` over a rolling-mean/zero benchmark on held-out modern dates? | OOS loss difference and its time-aware uncertainty; separately source-style regression coefficient. |
| `H2` state moderation | Does the opening-return relationship **change with Z**? | A formal **cross-state contrast** or interaction-coefficient difference; significance in one bin alone is inadequate. |
| `H3` nonlinear enrichment | Are there reproducible thresholds, curvature, saturation, or asymmetry **beyond a linear/varying-slope competitor**? | Prespecified held-out contrasts, finite-difference/smooth comparators, complexity and support diagnostics, ideally OOS improvement. |
| `H4` state discretization | What is lost by turning the **same observed RV** into 3 categories? | Direct comparison of predictive risk and the *same supported response contrasts*, not comparison of unrelated states. |
| `H5` environmental shape stability | Is a **fixed-state, fixed-partner anchored response shape** approximately unchanged across two dated windows? | CIs on predeclared between-window shape differences and a materiality tolerance; not failure to reject equality. |
| `H6` economic usefulness | Does any information translate into a feasible end-of-day decision after costs? | Execution-timed simulated net P&L, matched exposure/random baselines and risk metrics, separate from statistical tests. |

**Main scientific shape:** at a *declared* late predictor value `w`, anchor `x0`, and volatility states `z0`, `z1`,

\[
 D_m(x;x_0,z_1,z_0,w) =
 [m(x,w,z_1)-m(x_0,w,z_1)]
 -[m(x,w,z_0)-m(x_0,w,z_0)].
\]

For an EBM display, `D_F` is computed by substituting its **total fitted prediction surface** `F`, not by reading a single purifiable/aliased interaction term. `D_F` is a model-output contrast, not necessarily `D_m`. `w` may be fixed to zero only when joint support makes this comparison credible.

Use sign/size asymmetry and curved slices as **named questions**, not required findings. A population `m` at a continuous point is not automatically identified without a regular version and joint support; EBM interaction tables are piecewise/binned and should **not be differentiated as if smooth**.

### Predeclared materiality conventions

- Scientific target units: **basis points of expected `r13` return**.
- Default **illustrative** shape materiality: **1 bp** for a declared `x` comparison; calibrate that `x` contrast and support *on the development sample*, then freeze both before test evaluation. If support or sampling makes a 1-bp decision impossible, report **INCONCLUSIVE**, not `stable`.
- Test the shape variation itself and whether it exceeds a material threshold. A `p>0.05` for zero does **not** certify approximate invariance.
- Predicted-loss materiality for an ambitious *incremental forecasting* finding: out-of-sample `R²` improvement at least **0.25 percentage points** versus the stronger simple state-aware comparator **and** time-aware interval excluding no improvement. This is a planned decision threshold, not a prediction or a claim that anything below is scientifically worthless.
- Economic interpretation separately requires the forecast to clear assumed **round-trip trading costs**; those assumptions are not an empirically observed transaction-cost estimate.

## 3. Data sources, actual availability, and go/no-go gates

### 3.1 Primary data

**SPY one-minute historical OHLCV and, if present, per-minute trade counts; daily SPY aggregate trade counts and price close.** Use the user's existing Massive provider **only after confirming current entitlements**. Massive's listed-stock archive goes back to **10 September 2003**, but as of the vendor documentation inspected on 14 October 2026, individual stock plans differ: Basic roughly 2 years, Starter 5, Developer 10, and Advanced all available history. **Archive existence is not account entitlement.** Data retained from an older lawful download may be reusable if its provenance and rights are clear.

**Do not assume SPY is in the preexisting 99-stock project.** Verify actual existing files, tickers, bar time conventions, splits, and whether 09:30–10:00 **minute returns** are available. Prior 30-minute bars may support `r1`, `r12`, `r13` but **cannot reproduce one-minute opening RV**. The original project last used ~99 individual equities, 30-minute bars, and separate modeling splits; those splits are not this study's sampling unit or dates.

**Optional, explicitly secondary:** previous-day closing VIX from a legitimately available index series; preceding-day trailing realized volatility; first-half-hour volume. They test robustness. VIX is not substituted for the primary realized-volatility state and no options-contract data are required for primary Experiment B. Source-era implied-volatility comparison is *not* a replication of Gao's opening RV experiment.

### 3.2 Feasibility tiers — fixed fallbacks rather than result hunting

| Available historical SPY minute coverage | Permitted claim and fixed design |
|---|---|
| Source-era overlap, ideally ~**2004–2013**, plus modern data | **Partial historical replication** of the 1993–2013 paper, **plus** modern held-out experiment. Label the original 1993–2003 segment unavailable from Massive. |
| At least **2016–2026** but no source-era overlap | **Modern U.S. hypothesis corroboration / failure**, **not historical replication**. Run frozen 2016–2021 train, 2022–2023 validation, 2024–2026 sealed test. |
| Only approximately **2021–2026** | Small-sample **exploratory/pilot** branch: 2021–2022 train, 2023 validation, 2024–2026 test; severely restrict EBMs/shapes and report low scientific power. No claim of robust replication. |
| <3 complete years of usable minute data | **STOP** substantive nonlinear/stability claims and request better history; a data QA or descriptive prototype is allowed. Do not manufacture statistical power by duplicating stock/day rows. |
| Missing minute RV but adequate matching 30-minute data | Can run **price-return benchmark only**, separately labeled; primary volatility experiment remains unexecuted until opening-minute RV or a formally approved changed state is available. |

**Default primary historical split, only if data exist:** source-window **2004-01-01–2013-12-31**; development **2014-01-01–2021-12-31**; validation **2022-01-01–2023-12-31**; sealed final test **2024-01-01–2026-09-30**. Exact data start moves to the *first verified eligible session*, not to an invented prior price. Source-era dataset is for historical benchmarking; **do not** tune modern EBMs to match source-era coefficients then falsely treat it as untouched OOS.

### 3.3 Data download/storage restrictions

- **One canonical, immutable raw SPY minute store** or a reference to existing immutable files, one small derived **one-row-per-day table**, plus small configurations/results. Do not create one complete copy of raw data per feature version, model, seed, fold, or permutation.
- Fetch only the smallest necessary symbol/date range and **retain only necessary minute windows** if rebuilding a new canonical store (opening ~09:30–10:00 and close ~15:00–16:00, plus prior session close). For requested trade fills retain 15:30–16:00 minute bars. A source may deliver whole-day bars, but unused bars need not be redundantly stored.
- Do not download the entire market's daily minute flat files to recover SPY unless this is demonstrably more efficient and already authorized. Do not duplicate the 25 GB dataset from the previous EBM experiment.
- Use compressed Parquet with a stable schema; do not store intermediate uncompressed CSV copies or repeated frozen folds. Model outputs should be predictions, contrasts, small fitted artifacts, manifests, and checksums rather than full duplicated datasets.
- Initial disk budget suggestion: **target under 1 GB of newly retained files**, flag before exceeding 2 GB. This is an operational target, not a proven file-size estimate.
- Never print, log, upload, or embed `MASSIVE_API_KEY`. Load secrets from the environment or preexisting secrets manager only.

## 4. Exact timestamps, variables, and timing-safe feature definitions

All clock times below are **America/New_York** with daylight saving handled by timezone-aware conversion. Massive's `t` timestamp marks the **start** of an aggregate, and is represented as epoch milliseconds; convert to ET before assigning a session and return. The 09:30 bar is `[09:30,09:31)`, and the 15:59 bar is `[15:59,16:00)`. Reject after-hours and accidental 16:00–16:30 bars. Exclude shortened sessions where the canonical 15:30–16:00 target is unavailable. Never fill across the overnight gap.

### 4.1 Reproducible price anchors

Let `Pprev` = **last valid regular-session close ending at the previous regular session's 16:00** (the 15:59 minute bar close); `P10` = last one-minute regular-session bar ending at **10:00**; `P15` = last bar ending at **15:00**; `P1530` = last bar ending at **15:30**; and `P16` = last bar ending at **16:00**. All prices must use a *consistent* split-adjustment convention, currently vendor `adjusted=true` (document whether split-only; **do not** silently assume dividend adjustment). Reconcile minute-derived and daily close fields before research use.

In unitless simple returns,

\[
 r_{1,t}=P10_t/Pprev_t-1,\qquad
 r_{12,t}=P1530_t/P15_t-1,\qquad
 r_{13,t}=P16_t/P1530_t-1.
\]

Persist `x_open_bp = 1e4*r1`, `w_preclose_bp = 1e4*r12`, and `y_last30_bp = 1e4*r13`; the baseline regression uses consistent units for regressors/target. Keep the unitless `r1/r12/r13` columns for source-style tables. Also persist the *intraday-only* 09:30→10:00 return as an audit item but **do not call it `r1`**.

**QA requirements:** explicitly test the prior-day anchor, DST and half-day handling, signs and basis-point conversion, last-30-minute label, split/ex-dividend anomalies, bar start versus end timestamps, valid session calendar, no future prices in predictors, and consistency with available source 30-minute aggregates. If daily vendor trade count `n` is available, record a source-style **>=500 daily trades** restriction; note that vendor qualifying-trade counts need not exactly reproduce TAQ counting. Do **not** filter based on the target return's magnitude or sign.

### 4.2 Primary opening realized-volatility proxy

Within 09:30–10:00, define 30 consecutive eligible one-minute regular-session bars, with opening price `O_09:30`, minute closes `C_09:30, ..., C_09:59` (the last close is known at 10:00). Use the predeclared within-opening-half-hour log increments

\[
 q_{t,1}=\log(C_{09{:}30}/O_{09{:}30}),\qquad
 q_{t,k}=\log(C_{09{:}(29+k)}/C_{09{:}(28+k)})\quad(k=2,\ldots,30),
\]

where the second line means **each next consecutive minute close divided by the immediately preceding minute close**; implement it by array shifts rather than by interpreting the shorthand minute indices. Then

\[
 \mathrm{RV}^{open}_t=\sqrt{\sum_{k=1}^{30} q_{t,k}^2},\qquad
 Z_t=\log(\mathrm{RV}^{open}_t+10^{-8}).
\]

This is **our deterministic operational RV proxy**. It excludes the previous-close-to-opening overnight move, is known by 10:00, and is **not** claimed identical to the source authors' undocumented normalization. An alternative source-compatibility sensitivity is the within-window sample standard deviation of minute log returns. Record the difference; do not choose a formula by which one produces a stronger test result.

**Minute completeness default:** all 30 opening minute bars must exist with legitimate positive OHLC prices; otherwise exclude the day from primary RV analysis and log the reason. Source-style “valid 1-minute returns” with missing minutes is a separate **predeclared sensitivity**, never silent forward filling. If the strict rule loses >2% of otherwise eligible full sessions, **flag data QA** and request a source check before science. Missingness correlated with volatility can bias conclusions.

Store also `rv_open_raw`, `rv_open_log`, `n_open_minute_bars`, `volume_open_30`, `trades_open_30` if available, `open_overnight_part`, and a source/data-quality flag. **Never use realized volatility computed from 10:00–16:00, the full day, or the target 15:30–16:00 as the predictor state.**

### 4.3 Discrete versus continuous representations: same underlying state

- **Source-style retrospective tertiles:** low/middle/high partitions of opening RV within the **disclosed historical sample** (and, if exactly documented, within the paper's calendar grouping convention). They are *descriptive ex-post sorting*, not necessarily tradable in real time. Label `source_retro_tercile` and never use it for honest historical forecast simulations unless each cutoff was known as of that date.
- **Predictive terciles:** cutpoints estimated from **past/training data only**. In the development/validation setup, freeze the development-training cutpoints for the validation period, and use strictly lagged rolling/expanding past data if a walk-forward refit updates them. Cutpoints can be estimated from **252 prior eligible days** as a predeclared rolling sensitivity, using information no later than `t-1`; exclude first 252 lookback dates if this branch is used. Avoid global percentile ranks based on test dates.
- **Continuous-input branch:** feed `Z_t` from the very same RV series to EBM/OLS/spline. Do not treat an EBM binned input as a smooth, differentiable estimator. Use finite differences or validated smoother as necessary.
- Log the training distributions, percentile thresholds, cutoffs, occupancy, and train-vs-test out-of-range proportions. The low-RV bin may contain little large-|r1| overlap; check *joint* support before plotting cross-state shape contrast at fixed `x`.

### 4.4 Information-set distinction

**Early-information study E:** at **10:00** only `x_open_bp` and `rv_open_log/tercile` (possibly opening volume in a *separate* sensitivity) are available. It predicts the `15:30–16:00` outcome, but the actual trade may be deferred to late afternoon without updating the forecast.

**Late-information study L (main complete regression):** at **15:30**, `w_preclose_bp` is additionally known. Fit the published-style multivariate `r13 ~ r1 + r12` and its state-dependent extensions. `r12` must **never** enter a model portrayed as a forecast issued at 10:00.

Document the **forecast timestamp** for every model and a distinct **entry timestamp** for every trading backtest.

## 5. Target samples, splits, and controlled expansion

- **Unit of inference and modeling:** trading **day**, not each SPY minute and not each of 99 equities; SPY days can be serially dependent.
- **One daily record** per eligible session; log calendar discontinuities and all exclusions.
- **Historical 2004–2013 study:** original-source partial overlap only when entitlement/QA allow. Compare source-style coefficients, HAC p-values, volatility regime grouping, OOS `R²` definition and filters with full honesty about 1993–2003 absence and vendor TAQ differences. **This is NOT the modern sealed test.**
- **Modern long-history default:** train 2014–2021; validation 2022–2023; test 2024–2026-09-30. If 2014 unavailable, use **preapproved** 2016–2021 train and keep validation and test unchanged. If 2016 unavailable, use short-history exploratory tier (§3) with prominently reduced claims.
- **Development only:** choose feature clipping, model hyperparameters, thresholds, and scientific target grids with the train/validation periods. Do not inspect test performance to select these.
- **Walk-forward:** on validation, simulate chronological expanding-window predictions; freeze the winning *protocol* (model family, hyperparameter decision rule, thresholds, fit cadence) before test. On sealed test, refit **quarterly** using only dates whose outcomes are fully known before each refit; a new refit may incorporate earlier test-period data *chronologically*, but test-based changes to hyperparameters, target definition or performance selection are prohibited. Retain a one-shot fixed-fit diagnostic in addition to the walk-forward series.
- **Embargo/overlap:** each `Y_t` ends at 16:00 of day `t` and is known before the following session; no within-day label leakage is allowed. For monthly lookbacks and split boundaries check all rolling features are computed past-only. If future variants introduce overlapping horizons, add appropriate purge/embargo rather than copying the no-overlap logic.
- **Calendar subgroup reports:** predeclare e.g. 2014–2019, 2020–2021, 2022–2023, 2024–2026 for scientific descriptions. Avoid treating crisis-specific subgroups as independent and avoid too many formal tests.

## 6. Exact baseline and nonlinear model ladder

Run **E (early)** and **L (late)** in parallel only when data are fully valid; the primary historical replication uses published models without needing EBMs.

### 6.1 Historical benchmark regression trio

In original **simple returns** (or bps consistently; explicitly record scaling):

\[
 \mathrm{OLS}_1:\ Y=\alpha+\beta_1 X+\varepsilon;\quad
 \mathrm{OLS}_2:\ Y=\alpha+\beta_{12} W+\varepsilon;\quad
 \mathrm{OLS}_3:\ Y=\alpha+\beta_1 X+\beta_{12} W+\varepsilon.
\]

Report intercept, slopes, `R²`, sample count, classical SE for comparison and **Newey–West/HAC SE** with **lag 5** primary and lags **10/20** sensitivity (lag choice is our convention; do not attribute it to the source). Report source-era versus modern independently. Test cross-bin slopes with an explicit pooled interaction model instead of comparing separate p-values.

### 6.2 Minimum competitive models

| ID | Candidate | Inputs and structure | Purpose |
|---|---|---|---|
| `N0` | Predict zero final-30m return | None | A genuine no-predictability benchmark. |
| `N1` | Past-only rolling mean / training intercept | Past `Y` only | Stronger naive mean benchmark where applicable. |
| `M1` | OLS opening return | `X` | Source benchmark. |
| `M2` | OLS preclose return | `W` | Source late-time benchmark. |
| `M3` | OLS both | `X,W` | Strong source late-time baseline. |
| `C1` | OLS with **categorical state × opening-return** | `X`, state main effects, `X×tercile` (and `W` when L) | Explicit **between-state slope** test. Includes main effects and respects information time. |
| `C2` | OLS with **continuous RV × opening-return** | `X,W(optional),Z,X·Z` | Simple smooth-moderation competitor. |
| `S1` | Modest spline varying-slope GAM/OLS | low-df `s(Z)` and `X·s(Z)`; late controls as appropriate | **Strong smoother alternative** to a piecewise EBM state surface. |
| `A0` | **Additive EBM**, no interactions | `X,Z` or `X,W,Z` | Tests whether state has value without shape interaction. |
| `A1d` | EBM with fixed `X×discrete_state` | `X,tercile` (and `W` late) | Same RV but discrete. |
| `A1c` | EBM with fixed **`X×Z`** interaction | `X,Z` (and `W` late) | **Principal continuous-RV shape extension**. |
| `A2c` | Late EBM with **`X×Z` and `W×Z`** | `X,W,Z` | Secondary, nested two-interaction extension; no new adaptive interaction discovery. |

**Model discipline:** keep the feature list at 2–3 variables. Do not automatically search many technical indicators, macro variables, alternative states, higher-order interactions or architectures. Interactions are **declared by feature name**, not guessed from numeric indices that may change during preprocessing. For a fair increment, compare `A1c` to `A0`, **`C2` and `S1`**, as well as `N0/N1/M3`; a state-blind EBM is not the only baseline.

### 6.3 Default EBM fitting/search budget (implementation may resolve minor API details)

- Algorithm: actual **version-pinned InterpretML `ExplainableBoostingRegressor`**, squared-error `objective='rmse'`, no monotonicity constraint, no automated interaction search. Its software greedy/bagging path is **not** the literal idealized tree learner from the project's theorem reports.
- Inputs: `max_bins` in `{32,64}`; `max_interaction_bins` in `{8,16}`; `min_samples_leaf` in `{10,25}`; `learning_rate` default `0.025` with a single `0.05` sensitivity; `max_rounds` cap `3000`; `outer_bags=8` for final fits and `4` for quick screening if computationally necessary; `random_state` deterministic; use train-only internal bagging/early stopping and **never shuffle across validation/test**. Document exact `greedy_ratio`, `smoothing_rounds`, early stopping and any version defaults. No full Cartesian grid sweep is authorized by default.
- **Max initial candidate budget:** **8 prespecified or deterministic screened configurations per EBM family**, seed 42. Select at most **2** based on development/validation; expand those to 5 seeds `{42,123,2025,7,314159}` for robustness. Do not expand all 8 × models × permutations by default. Keep the best comparators on equal valid days and report fit time, effective complexity, and storage.
- Avoid multiple different hidden validations: either rely on strictly train-internal EBM bagging and external chronology validation or use an explicitly temporal internal scheme; document whichever is implemented. Outer bag error bars are **not** automatically scientifically valid confidence intervals.
- **L1/L2 penalization:** start with InterpretML default, record version. Regularization sensitivity is optional **only if** model overfitting is observed on *development/validation*, and requires a documented config revision, not test-driven rescue.
- **Clipping:** primary raw inputs retained; optionally clip `X,W,Z` at frozen training quantiles `[0.005,0.995]` in a declared secondary robustness experiment. **Do not clip the target** or delete high-volatility days simply because they are challenging. Report clipped percentage, especially in test.
- **Interpretability checks:** actual prediction surface and `X×Z` total-response slices on joint supported grids, interaction support/occupancy, shape stability across bags and seeds, dependence on `r12`, exposure to extreme days, and strong spline comparison.

### 6.4 Model complexity and train/test comparability

Use identical eligible dates, label construction, price adjustments, primary RV series, and train/validation/test boundaries within each E/L information set. Separate early and late models: adding `W` is extra information, not a fair same-information model improvement. Do not compare raw-price regression without a persistence baseline; this experiment uses returns by design. Controls are limited and declared. Model comparison is paired **by date**.

## 7. Scientific shape analysis: an EBM plot is not the population truth

### 7.1 Required visual outputs

1. Source-style OLS scattered/decile plots and state-group slope estimates with **CIs** (label any ex-post state threshold).
2. `X` versus `Y` conditional response slices for low/middle/high **RV**, **on common supported X values**, for both discrete and continuous RV models. Show observed density/rug and support mask. Display raw predicted bps, not just purified component scores.
3. Heatmap `\widehat m(x,z)` for continuous RV (and late `W=0` or other declared supported fixed `w`), **with unsupported cells masked**; show the actual cut/bin boundaries. Colorbar unit bps.
4. Anchored `\widehat g(x;z)=\widehat m(x,w,z)-\widehat m(0,w,z)` and its four-point cross-state contrast `D_F`; surface should come from **total model predictions**. Do not treat a purified interaction table as unique science.
5. Spline/varying-slope and simple interaction curves on the same axes; nonlinearity/threshold claims require comparison to them.
6. Model residuals by date, RV tercile, `X` sign/magnitude and market stress; train/test shift and missing-data diagnostics.
7. Early and late forecasts separately; 15:30 results cannot be presented as available at 10:00.

### 7.2 Support and inference safeguards

- Predeclare `x0=0 bps` only if supported. Prefer an additional symmetric nonzero pair `x-`,`x+` selected using **development-period common conditional support**, then freeze values. Do **not** take a test-specific high-RV extreme point and contrast it with low RV where no comparable `X` exists.
- For informative **held-out empirical cell estimates**, use a prespecified coarse `(X band × RV tercile)` table; source it from the **same original daily observations**, not the EBM predictions. Require at least **50 eligible observations and 20 separated five-day blocks** per compared cell for exploratory reported intervals, **100 and 30 blocks** for strong affirmative claims; these are practical safeguards, not mathematical guarantee. Otherwise abstain/mark INCONCLUSIVE. Restrict comparisons to actual joint support.
- For continuous raw point comparisons, an EBM surface is a **projection/fitted approximation**. Formal `D_m` inference requires separately justified continuity/smoothness, support and estimator theory or a predeclared finite-bin estimand. Do not silently apply the idealized Tasks 11/13/19 bands to finance with unknown tails/serial dependence.
- For regression slopes and predeclared finite-group contrasts, HAC or suitably time-blocked resampling can quantify uncertainty **under its actual assumptions**. A block bootstrap of the *whole fitted pipeline* offers useful **descriptive estimator-stability intervals**, not automatic selective conditional inference for arbitrary optimized EBMs.
- Protect multiplicity: predeclare one `X×Z` primary interaction question, one primary `x-→x+` high-minus-low shape contrast, and treat threshold/curvature scanning across many points as **exploratory**; if reporting several point claims, use a simultaneous family or adjusted tests. Never label selected exploratory maxima as fixed-p value results.
- For affirmative near-invariance, compute an interval for a *fixed-state between-period* contrast and require its entire confidence set lie inside predeclared `±1 bp` (or correctly frozen revised tolerance). Intervals that straddle decision thresholds are INCONCLUSIVE.
- Report projection/display fidelity: where meaningful, compare model-predicted contrasts to independent supported coarse cell-mean contrasts with uncertainty. A small RMSE does **not** prove local model fidelity, and the technical EBM papers do not certify the default InterpretML implementation.

### 7.3 Three possible honest result interpretations

1. **Strong replication, weak new shape:** significant historical/modern OLS, but simple interaction/spline matches EBM. This is a **successful replication plus parsimony finding**, not a failed project.
2. **Strong replication, reproducible shape enrichment:** EBM contains supported nonlinear/state interactions stable across validation windows and useful against strongest simple comparator. This is the preferred new scientific result, **not promised**.
3. **Modern failure or reversal:** published historical effect is absent/unstable OOS; report structural break and diagnostic robustness; do not change time horizon, state, universe or thresholds to rescue a significant result.

## 8. Predictive evaluation and dependent uncertainty

### 8.1 Required statistical/predictive metrics

- Chronological **train / validation / sealed test** regression tables and fixed pre-specified comparison dates.
- RMSE/MAE in basis points, signed error, mean absolute Y, and MSE against `N0` and `N1`.
- Out-of-sample `R² = 1 - Σ(y-ŷ)^2 / Σ(y-ŷ_benchmark)^2`, naming benchmark, period and its *past-only* fitting rule. Avoid denominators based on target test means known only ex post for claimed real-time forecasts.
- Predictive correlation, directional accuracy **versus naive base rate**, precision conditional on |forecast| threshold, calibration-by-prediction quantiles, residual mean/variance by RV state.
- Coefficient estimates/SEs and explicit `β_high−β_low` significance for source-style volatility groups; distinguish within-state p-values from interaction p-values.
- Paired date-level differential loss `d_t = (y-ŷ_simple)^2 − (y-ŷ_EBM)^2` and Newey–West **lag 5** primary HAC CI, 10/20 sensitivity. A 5-/20-trading-day **block bootstrap** on held-out prediction/loss pairs is a robustness summary. These are not automatically exact for an arbitrary unstable process.
- Support/cell occupancy, effective number of time blocks, calendar drift, possible crisis concentration, interval width, and whether findings survive sensible alternative window endpoints and source-compatible volatility normalization.

### 8.2 Four-stage validation (project-wide research requirement)

1. **In-sample descriptive fit** and source-style regression; do not call it predictive confirmation.
2. **In-sample null control:** approximate blocked/circular-shift permutations, including the **entire fitting/tuning/selection discovery procedure**, to assess whether a selected in-sample pattern could arise under a declared destroyed-alignment null.
3. **Chronological walk-forward OOS** with a sealed final period; choose models on validation only and report matched losses/uncertainty on final dates.
4. **Walk-forward permutation/null study**, **rerunning training and selection under each null**, not permuting an already chosen final prediction vector. Include simple shuffled-signal/random-exposure controls and document the empirical null construction, dates and number of repetitions.

**Prespecified compute budget:** start with **100 full-pipeline permutations** during screening; increase to **at least 500** for a final highlighted selected-discovery null *if feasible*. If computational limits prevent this, disclose reduced Monte Carlo resolution; do not report `p=0.000` for 100 permutations. A valid permutation p-value depends on exchangeability/invariance; **market time series rarely meet exact exchangeability**, so interpret these as **design-specific stress/null diagnostics**, not exact finite-sample significance under general dependence.

**Two nulls must not be confused:** (i) no usable opening-to-closing temporal alignment (block/circular-shift response null); (ii) no *incremental* state moderation given `X,W` (requires a different conditional/interaction null). Shuffling RV indiscriminately changes its dependence with `X` and calendar time, so is not an automatically valid test of `H2`. Use regression/HAC interaction inference for the primary direct slope-difference test, and label nonparametric state-shuffles exploratory unless a defensible conditional null is implemented.

## 9. Economic / trading evaluation — explicitly subordinate and execution-safe

The **scientific label** is a historical market return `P16/P1530 - 1`. For a strategy, do **not** assume that observing the 15:30 completed bar lets the investor execute *at its already observed closing price*.

- Freeze the decision time: **15:30** for L; for E the signal may have been computed at 10:00 but order entry still occurs near 15:30. Record the actual available data time of every feature.
- **Execution proxy:** earliest default simulated entry = **15:31 minute open** or next clearly obtainable bar after a documented signal-latency rule; exit = **15:59 minute open** to avoid pretending a 16:00 bar close is freely executable after observation. If reliable closing-auction/quotes data become available, a separately named execution experiment can use them. OHLC opens are not guaranteed fills; call this a simulated bar-price proxy.
- Both sides of a position: **long**, **short**, **flat**. Default position only if predicted last-half-hour return exceeds estimated **round-trip cost** by a predeclared buffer; compare sign-only and thresholded exposure on validation, then freeze. If SPY borrow/short constraints or quote quality cannot be verified, report idealized price-return results clearly.
- **Costs:** evaluate 0, 1, 2 and **5 bps round-trip** as *assumptions/scenarios*, including stated spread/slippage/fees components where possible. Do not call these measured execution costs without quote data.
- Baselines: zero/flat, SPY long in the **same entry/exit window** (not a full-day or multi-year buy-and-hold unless separately labeled), sign(`r1`) trade, simple OLS/interaction signal, **matched-opportunity/matched-exposure random long/short** strategy, and if desired a full-day buy-and-hold market reference **on a distinct horizon**.
- Required metrics: mean/median daily net bps, net cumulative return under stated capital deployment, annualized Sharpe with assumptions, max drawdown, exposure fraction, long/short fraction, trade counts, turnover, downside tail, costs/gross decomposition, and paired bootstrap/HAC uncertainty. Because this is one ETF and a very short holding window, avoid unexamined compounding/margin/overnight assumptions.
- A statistically detectable conditional shape need not produce net profits. Economic success is **not required** to conclude that the scientific replication worked.

## 10. Data and modeling QA: explicit fail conditions

### 10.1 Data quality gate (must pass before model fitting)

- Correct U.S. regular-session calendar and DST conversion; no 16:00-start bars inside `r13`.
- One record per eligible date; exactly 13 half-hour *regular-session* intervals for full sessions if compared; no resampling from shifted midnight-time UTC groups.
- Price anchors positive, plausible, internally time-consistent; source r1 includes overnight; r12 and r13 do not overlap and have correct 15:00/15:30/16:00 endpoints.
- Full price/split policy and ex-dividend log; no mixing adjusted minute prices with unadjusted prior close.
- Realized volatility uses **only 09:30–10:00 minute data**; strict/minute completeness record; zero/near-zero state values diagnosed rather than hidden.
- End-of-day label absent from all available predictor fields and all preprocessing fits; no state cutoff learned on sealed test distribution.
- Source count filter and differences from original TAQ sample documented; no imputation of unavailable early prices or minute volume from later bars.
- Historical coverage and `MASSIVE_API_KEY` entitlement explicitly verified; a plan’s archive start date is not enough.

**If any critical leakage or time misalignment is found: STOP, invalidate affected results and rerun them after a versioned code/data correction.** No charts or numerical significance from invalid labels may be treated as provisional scientific evidence.

### 10.2 Modeling and scientific gate

- OLS coefficients in consistent units, proper dates and HAC method, no out-of-sample data in feature scaler/bin thresholds.
- At least one **state-aware simple comparator** (`C1`/`C2`/`S1`) in every claim that EBM added value.
- Every tested shape contrast has support in each state and partner configuration used. Insufficient support = **ABSTAIN** rather than extrapolated confident interval.
- Native `interpret` software version, defaults, term indexing, bagging, selected interactions, run seeds and hashes recorded. A plotted component score is not a unique raw effect.
- Every reported inference result names IID/serial/HAC/bootstrap/source assumption; do not transplant a theoretical theorem about a different literal tree dictionary or dependence law.
- Temporal structural breaks and extreme events documented without ex-post excluding unfavorable regimes.
- Positive discovery survives sealed test and at least one simple competing model; otherwise explicitly label exploratory or inconclusive.

## 11. Minimum output package and report layout

**Small, reusable, versioned project structure** (adapt to actual repository/AGENTS.md conventions; do not copy a large database):

```text
experiment_B_intraday_spy/
  README.md
  config/experiment_B_protocol_v1.yaml
  config/run_manifest.schema.json  # optional
  docs/source_replication_differences.md
  docs/data_entitlement_and_timestamp_audit.md
  data/reference_to_existing_raw_or_minute_store.txt
  data/derived/spy_intraday_daily_v1.parquet
  src/          # data audit, feature assembly, baselines, EBM, tests, reporting
  tests/        # deterministic synthetic time/price/vol/leakage tests
  reports/
    stage0_data_feasibility.md
    stage1_replication_benchmarks.md
    stage2_nonlinear_models.md
    stage3_shape_inference_and_fidelity.md
    stage4_walk_forward_and_permutations.md
    stage5_trading_and_conclusions.md
    experiment_B_final_research_report.md
  artifacts/    # compact figures, prediction tables, selected fitted models, hashes
```

**Must provide at the end:**

1. **Research abstract and claim ledger**: each of H0–H6 classified **SUPPORTED / NOT SUPPORTED / INCONCLUSIVE / NOT EXECUTED**, by source-era vs modern sample and by E/L information timing.
2. **Literature-replication crosswalk**: source equation/table/definition, our version, deviation, observed coefficient/CI and source claim; paper-year differences labeled.
3. **Data QA and coverage**: sample dates, row/day counts, bad/missing minute windows, precise return-time windows, split adjustments, hashes, API entitlements, disk growth.
4. **Model results**: all baselines, train/val/sealed test, matched date counts, HAC and paired prediction loss, conditional R²; fitted complexity/time; model seed variability.
5. **State/shape report**: discrete/continuous same-RV curves, supported contrasts, cross-state difference tests and multiple-testing status, confidence interval widths, masks/abstentions, environmental stability and raw-vs-fitted caveats.
6. **Null/permutation report**: full discovery-loop rerun, null design, test horizon, p-value Monte Carlo resolution, limitations.
7. **Economic report**: actual decision/entry/exit timestamp, matched exposure and random baselines, 0/1/2/5 bps cost scenarios, risk and uncertainty.
8. **Decision memo**: whether the experiment **replicated**, whether EBM provided credible *additional* information, what failed and why, and what can be stated responsibly on a CV or in subsequent research. Distinguish scientific insights from profitability.
9. **Reproducibility**: frozen protocol, environment, code/data manifests, hashes, seeds and compact run registry; stage-by-stage files changed and tests passed. Historical source data must remain unmodified.

## 12. Stage gates, high-level workflow and explicit exceptions

The *new chat* owns detailed Codex-prompt construction, **not** changes to the scientific hypothesis. Stages:

| Gate | Work | Required evidence before progressing |
|---|---|---|
| **0** | Environment/repo/AGENTS audit, SPY entitlement/history, minute windows, QA schema and strict storage plan | Source entitlement report; ≥3-year feasibility; source-era partial-replication possible/impossible; timezone & synthetic price tests. |
| **1** | Daily dataset and source-style U.S. OLS/tercile replication | Price-anchor and RV QC; OLS trio; at least one year-window benchmark; source difference register; no mislabeled 09:30-only opening signal. |
| **2** | Simple state-aware competitors and small EBM ladder | Matched dates; chronological train/validation; state overlap; resource/tuning audit; no final-test leakage. |
| **3** | Shape and fidelity/instability diagnostics | Finite common-support grid; sourced D_F and supported empirical contrasts; testable materiality; abstention and caution labels. |
| **4** | Frozen walk-forward OOS and full-pipeline null checks | Both OOS baseline and EBM, paired loss CIs, source-specific and modern null outcomes, no rescues from test. |
| **5** | Execution-timed economic evaluation and final report | No impossible fills, stated costs, proper same-window baselines, no exaggerated CV claim. |

**Preapproved small exceptions:** a vendor column renamed; isolated documented bad minute bars excluded uniformly; an API pagination fix; corrected UTC-to-ET handling; pinning a compatible package version; reducing outer bags/permutation count with a documented compute limitation; canonical-directory adaptation; source-era start moved to first authorized date; using 2016–2021 train rather than 2014–2021 when historical entitlement is insufficient. Each is logged **before reviewing scientific outcomes** and may force reruns.

**Not preapproved:** substituting a different security/state/target, using VIX in place of morning RV, using only 09:30–10:00 for `r1`, fitting `r12` in a purported 10:00 model, selecting high-vol days or a new return horizon to make results significant, replacing SPY with a 99-stock pooled panel, changing the sealed test period, choosing a richer feature set or adaptive interaction search, constructing official scientific CIs from InterpretML term error bars, mislabeling vendor-derived results as exact TAQ replication, or weakening QA without disclosure. **Escalate** those choices to the user/design thread rather than letting Codex decide silently.

## 13. Diagnostics guide: expected, surprising, and invalid outcomes

| Result encountered | Interpretation/check | Decision |
|---|---|---|
| Source-window `β1` positive but high-vol `β1` not significantly different from low | Compatible with within-bin significance and weak moderation; do **not** claim established state-effect difference. Check conditional support, slope-difference HAC test and paper Table 4. | Continue with *exploratory* shape comparisons; H2 unresolved. |
| Modern `β1` near zero / negative | Possible structural change, different data vendor/period, measurement mismatch, or noise. Check exact `r1` prior-close definition, exclusion/filter, and timing *before* interpretation. | Report null/changed result; no target/horizon rescue. |
| EBM beats plain OLS but not interaction regression or spline | Nonlinearity/state moderation may be captured by simpler model. | **No incremental EBM advantage**; retain financially valid replication. |
| EBM has highly curved RV×X surface in cells with very few observations | Potential unsupported extrapolation/high variance; compare empirical joint occupancy and bootstrap/seed stability. | Mask, abstain, or mark exploratory. |
| Large training effect but no held-out gain | Overfit, state drift, tuning optimism or selection. | Fail modern incremental prediction claim; preserve descriptive differences. |
| Low-RV curves seem flat and high-RV curves steep | May reflect narrower range of X in low volatility rather than a true slope difference. | Restrict to common supported X, run pooled interaction test. |
| Good raw `r1` OLS but EBM state predictions differ by calendar regime | Check changing `P(X,Z)` composition, normalization, sample weighting and conditional drift. | Compare raw fixed-state science with model projections separately. |
| Valid but wide shape intervals | State is supported weakly, noise large or dependence severe. | **INCONCLUSIVE** at declared tolerance; do not certify stability. |
| `r12` late model improves but early model does not | Valid additional information at 15:30; not performance available at 10:00. | Report timing distinction; no early claim. |
| Sharpe positive gross but negative at 1–5 bps costs | Likely weak/uneconomic execution edge. | Scientific result may stand; **trading claim fails**. |
| Randomized benchmark beats EBM | Exposure/timing or alpha signal may be weak; investigate evaluation/time-label and null procedures. | Do not omit unfavorable matched random result. |
| Inconsistent 15:30 bar boundary or future RV included | Data leakage/label corruption. | **STOP, INVALIDATE, FIX, VERSION and RERUN**. |

## 14. Final bounded scope and next handoff

**A successful study is an auditable answer to the scientific questions, not predetermined profits or fabricated nonlinear findings.** The source establishes historically documented U.S. intraday momentum; the new experiment checks how well it generalizes to accessible U.S. periods and whether constrained state-dependent EBM analysis yields **additional supported information**. No claim is made that a continuous EBM interpolates a uniquely identified raw shape beyond support or that the supplied EBM theory automatically proves the native software's confidence intervals.

The second document, `experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md`, governs the receiving chat's workflow and exception policy. **Experiment A belongs to a different chat.**
