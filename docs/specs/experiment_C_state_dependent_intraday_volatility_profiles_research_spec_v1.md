# Experiment C — State-Dependent Intraday Volatility-Profile Shapes
## Frozen scientific specification and end-to-end design — v1.0

**Status:** SCIENTIFIC DESIGN FROZEN for implementation planning; not yet executed.  
**Date:** 17 October 2026.  
**Owner:** EBM Theory / scientific-design thread.  
**Implementation:** Hand over to the existing Experiment B implementation/results chat via the separate `experiment_C_transition_prompt_for_experiment_B_chat_v1.md`.  
**Boundary:** Experiment B's closing-half-hour *return* prediction and its nine exploratory extensions are completed negative/weak-evidence historical analyses. Experiment C asks a **different question about volatility-profile composition**; it must not be represented as an untouched replication or as a rescued positive B result. Experiment A remains separate.

> **Frozen central objective:** **Can interpretable state-dependent nonlinear models recover established intraday volatility shapes, characterize their continuous transitions, and explain residual shape variation through multiple interacting market states?** The primary scientific contribution is the **nature, location, magnitude, uncertainty and stability of changes in the conditional functional shape**; predictive improvement is secondary and not required for a scientifically informative result.

## 0. Scope, decisions and source-vs-extension status

- Primary observed asset: **SPY**, on regular full U.S. equity sessions, using existing **1-minute OHLCV** collected or referenced during Experiment B. Reuse data *without copying the raw bars*. A prior conversation describes approximately 2,675 eligible SPY days, but this count is **unverified until Stage 0** and Experiment B's eligibility criteria are not sufficient for complete-day Experiment C.
- Main analysis unit: **one day containing a full intraday curve**. Use its 5-minute interval rows as a convenient modeling representation, never as independent days.
- Primary observation/target: the **78-component compositional vector of each day's relative intraday realized variance**, estimated from 1-minute price changes. It is a *realized-volatility proxy*, not the latent instantaneous or jump-robust volatility curve of the reference papers.
- Primary source-replication target: **a qualitative and empirical analogue** of the volatility-shape findings in Andersen, Thyrsgaard & Todorov (2019), using SPY and a transparent realized-variance proxy. The source uses **E-mini S&P 500 futures (2005–2015), five-minute returns and a VIX-at-open state**; it is **not exact source replication**. We will also test source-motivated lagged-return/volatility-change patterns from Tsai, Eom & Wang (2024). The explicit primary state tier is defined below.
- Core experiment modes: **D = descriptive/retrospective scientific comparison** and **F = ex-ante information/forecasting and period-stability analysis**. Never mix them or label D as tradable.
- Secondary purpose: determine how much *conditional profile-shape instability across environments* is explained by individual and combined market states, above simple baselines; no causal or institutional-mechanism attribution without separate evidence.
- No options-contract dataset, trading profitability claim, or financial alpha discovery is required. A simple VIX daily **previous-close** series is publicly obtainable and does not require option contract histories. Same-day opening VIX is source-faithful only if point-in-time intraday VIX data are demonstrably available.
- **Freeze v1.0** scientific targets, state hierarchy, central nulls, date-handling and model ladder before fitting. Codex can fix minor coding/data issues with logs. Scientific changes require written approval and a new v1.x/v2.0 protocol, not a silent revision after looking at curves.

### 0.1 What counts as progress even if EBM shows no novel patterns

(1) Faithful operational reconstruction of known state-dependent profiles; (2) quantifying how specific parts of the curve change under a continuous state, with uncertainty and joint-support guards; (3) showing whether an EBM adds *scientific* detail relative to kernel/spline/time-specific models; (4) a justified affirmative **near-stability**, **material variation**, or **inconclusive** result across fixed environments; (5) demonstrating that a simpler model captures the evidence; (6) documenting a negative source-analogue result without changing the target. Do not score success solely by visually interesting plots.

---

## 1. Primary literature: what is already known, and what is not being claimed

**R1 — Andersen, T. G., Thyrsgaard, M. and Todorov, V. (2019).** *Time-Varying Periodicity in Intraday Volatility*. **Journal of the American Statistical Association**, 114(528), 1695–1707, DOI [10.1080/01621459.2018.1512864](https://doi.org/10.1080/01621459.2018.1512864). [Author-accepted manuscript](https://pure.au.dk/ws/files/192079536/Andersen2018_Time_varying_periodicity_in_intraday_volatility_AM.pdf). **Verified details:** The empirical study is based on E-mini S&P 500 futures from Jan 2005–Jan 2015; 2,516 retained days, five-minute sampling, and **VIX recorded at the start of the trading day**. High- and low-VIX *illustrative* groups are the **75th–95th** and **5th–25th** sample quantile intervals, excluding extreme tails and FOMC days for the relevant figure. The authors find that high-volatility regimes allocate a larger share of daily integrated volatility to the pre-close period. Their method is a nonparametric intraday periodicity estimator and a studentized-return/empirical-transform test, **not ordinary least squares on normalized daily squared-minute returns**. Our visual replication is therefore a **source-inspired analogue**, not a reproduction of their Figure 4 statistic or their published p-values.

**R2 — Tsai, P. C., Eom, C. and Wang, C. W. (2024).** *State-dependent intra-day volatility pattern and its impact on price jump detection—Evidence from international equity indices*. **International Review of Financial Analysis**, 95(B), article 103412, DOI [10.1016/j.irfa.2024.103412](https://doi.org/10.1016/j.irfa.2024.103412). [Publisher abstract/highlights](https://www.sciencedirect.com/science/article/abs/pii/S1057521924003442), [accessible working-paper version](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4445944). **Established patterns:** greater early-session weights after negative previous returns and changes in periodicity when realized variance increases; estimation uses five-minute intraday GARCH and a jump-robust alternative. We may reproduce **directional profile signatures**, not claim to recreate their GARCH, jump-robust estimator, markets, sample or formal tests unless separately implemented and audited.

**R3 — Andersen, T. G., Tan, Y., Todorov, V. and Zhang, Z. (2025).** *Testing mean stationarity of intraday volatility curves*. **Quantitative Economics**, 16(3), 1059–1091, DOI [10.3982/QE2644](https://doi.org/10.3982/QE2644), [open full article](https://onlinelibrary.wiley.com/doi/10.3982/QE2644). Tests nonstationarity of latent intraday volatility curves and documents strong time variation in E-mini futures. Includes potential sources (trading patterns, calendar/announcement changes), but no claim that our proposed state set explains all variation. **Important comparator for across-period profile stability and forecast relevance**, not a result automatically inherited by EBMs.

**R4 — Andersen, Su, Todorov and Zhang (2024).** *Intraday Periodic Volatility Curves*. **JASA**, DOI [10.1080/01621459.2023.2177546](https://doi.org/10.1080/01621459.2023.2177546). Existing flexible intraday curve estimation/inference; don't claim that estimating intraday curves itself is new.

**R5 — Clements, A. and Preve, D. P. A. (2026).** *Modeling and forecasting intraday spot volatility*. **International Journal of Forecasting**, 42(3), 816–832, DOI [10.1016/j.ijforecast.2025.11.009](https://doi.org/10.1016/j.ijforecast.2025.11.009), [article and linked replication code](https://www.sciencedirect.com/science/article/pii/S0169207025001189). They model time intervals as separate series and report strong forecasting results. An important model benchmark, but their latent spot-volatility estimator and per-time regression task differ from our normalized SPY profile target.

**R6 — Martins, I. F. B., Virbickaite, A., Nguyen, H. and Lopes, H. F. (2025 manuscript; posted 2026).** *Volume-Driven Time-of-Day Effects in Intraday Volatility Models*. [SSRN record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5795584), [institution working-paper record](https://swoba.hhs.se/oruesi/abs/oruesi2025_014.htm). Already models lagged trading-activity effects on volatility time-of-day patterns. **Adding volume alone is not novel**. Our proposed unanswered *empirical* question is whether a small combination of predeclared states explains *residual environmental changes of normalized intraday shape*, more than credible time-specific, smooth, and volume-driven alternatives.

**External state/calendar data:** [Cboe official daily VIX history](https://www.cboe.com/tradable_products/vix/vix_historical_data) supplies **daily closes**, *not source-equivalent market-open VIX*. [Federal Reserve FOMC calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) supply published meeting/announcement information, subject to historical timestamp audits.

### 1.1 Literature-result ledger and expected signs (not guaranteed)

| Code | Evidence already published | Our operational analogue | Status/what not to claim |
|---|---|---|---|
| L1 | High VIX at open -> larger relative pre-close volatility share (R1) | Compare conditional normalized closing-hour shares between high/low **lagged VIX** or independently available open VIX | Different asset/proxy/sample; sign plausible, **not guaranteed** |
| L2 | FOMC days have announcement-time spike (R1/R3) | Direct day-classified SPY variance-share profile around scheduled 14:00 ET announcements | Known effect, **not novelty**; calendar sensitivity only |
| L3 | Negative previous returns -> higher early-session pattern weight (R2) | Previous-session negative return vs nonnegative; opening 30m relative variance share | Other markets/estimators; direction not guaranteed in SPY |
| L4 | Increasing RV relative to yesterday changes IVP (R2) | Lagged RV level/change as distinct ex-ante states; descriptive realized-current-day rising RV sensitivity only as separate D-mode | Lagged change != same-day RV-rise classification |
| L5 | Volume helps time-of-day volatility (R6) | Prior-day/rolling volume *interaction with time of day*, above lagged RV and return sign | Existing mechanism; new result only if conditional refinement validated |
| L6 | Changes through calendar time (R3) | Compare matched fixed-state curves across predefined historical environments | Not a causal explanation or proof of stable future conditions |

**No invented effect sizes or guaranteed statistical significance.** A failure to match a source sign requires a data/target/proxy audit before theorizing about the market.

---

## 2. Statistical objects and immutable scientific questions

For a full regular session d and K=78 ordered five-minute bins k=1,...,78, let `r_{d,j}^{(1m)}` be a permitted one-minute log return and define

\[
  v_{d,k}=\sum_{j=5(k-1)+1}^{5k}(r_{d,j}^{(1m)})^2, \qquad
  R_d=\sum_{k=1}^{78}v_{d,k},\qquad
  Q_d(k)=v_{d,k}/R_d \quad (R_d>0).
\]

Every valid Q is nonnegative and sums exactly to one (up to floating-point tolerance). It is a **within-regular-session realized-variance allocation**. Treat a day as a stochastic vector `Q_d`; its compositional nature and closure constraint matter. It is neither a latent spot-volatility curve nor the raw realized *variance level*.

The primary conditional scientific curve is

\[
  m_e(k,z)=E[Q_d(k)\mid Z_d=z,E_d=e, d\text{ eligible}],
\]

for named environment e and known-at-open state Z_d. With additional states `W_d`:

\[
  m_e(k,z,w)=E[Q_d(k)\mid Z_d=z,W_d=w,E_d=e].
\]

For full support, `sum_k m_e(k,z,w)=1`. For a numeric continuous state, a smooth *version* of the mean needs an appropriate support/regularity assumption; a binned EBM table cannot be differentiated as a smooth population function.

**Do not conflate:**

1. `E[v_{d,k}/R_d | state]` (our primary **mean of daily shares**) with `E[v_{d,k}|state]/E[R_d|state]` (**share of group-average realized variance**)—generally unequal.
2. `Q_d(k)` with the R1 model's estimated latent intraday periodic component.
3. Actual conditional mean m, population low-order projection F*, empirical fit, raw InterpretML term, and the **full predicted surface**.
4. Differences in *normalized profile shape* with differences only in total realized variance.
5. Descriptive same-day state definitions with genuinely ex-ante states.

### 2.1 Scientific contrasts

- **Global normalized profile:** `m(k,z)` over k.
- **Window shares:** closing hour `L_d=sum_{k=67}^{78} Q_d(k)` (15:00–16:00 ET); opening half-hour `O_d=sum_{k=1}^6 Q_d(k)`; middle 11:30–13:30 share `M_d=sum_{k=25}^{48}Q_d(k)`. These windows do **not** exhaust the day, and they are not independent.
- **High-minus-low window response:** `G_L(z_H,z_L)=E[L|z_H]-E[L|z_L]`, analogously O and M.
- **Anchored shape shift:** `D(k;k0,zH,zL)=[m(k,zH)-m(k0,zH)]-[m(k,zL)-m(k0,zL)]`, with fixed `k0` containing **12:00 ET** (k=31). This cancels state-level additive shifts, but the compositional target already encodes relative allocation.
- **Total-variation shape separation:** `TV(m_H,m_L) = (1/2) sum_{k=1}^{78}|m_H(k)-m_L(k)|`; distributions over intraday intervals give the natural scale [0,1].
- **Across-environment residual shift:** fixed state `z,w`, compare m_1(k,z,w)-m_0(k,z,w), not marginal curves weighted by different state mixtures.
- **Whole-curve shape-change magnitude:** `Delta_{e,e'}(z,w)=(1/2)sum_k |m_e(k,z,w)-m_e'(k,z,w)|`, only on jointly supported comparisons.

Set fixed, scientifically interpretable **tolerances** prior to final analysis: **closing-hour allocation shift 0.02** (2 percentage points of the day's realized variance), **opening-half-hour shift 0.02**, **global profile TV shift 0.05**, and **across-period residual TV tolerance 0.05**. These are reporting/materiality thresholds chosen for interpretability, *not* previously demonstrated power-optimal values; the new chat may calculate training-only standard errors/power and request a v1.1 change **before any held-out testing**, but may not silently choose a tolerance that makes results significant. Report effect and full interval regardless of threshold. For signed differences, near-invariance requires a simultaneous upper bound on the absolute magnitude below tolerance; p>0.05 is **not** evidence of invariance.

### 2.2 Prespecified primary research questions

**RQ1 / Replication analogue:** Are time-of-day normalized profiles different across volatility states? In particular, is closing-hour allocation larger in high volatility than low volatility, and does the opening/midday/close contrast match the qualitative source figures?

**RQ2 / Shape mapping:** How does the *entire* profile evolve over the **same numerical continuous volatility state** (not an unrelated discretization variable)? Does state-specific change concentrate in particular times, and is it gradual or localized? Is additional curvature beyond the varying-slope/GAM comparator supported?

**RQ3 / Multiple market states:** Do a small, prespecified combination of lagged volatility, lagged return sign, and past trading activity (with optional calendar flags) explain **additional** shape differences and reduce residual instability across historical environments?

**RQ4 / Stability and fidelity:** After matching states and support, do fitted profiles remain approximately equivalent across named environments? Could apparent changes arise from changing state distributions, support, composition, coarsening, or low-order model misspecification?

**RQ5 / Forecasting (secondary):** Are **ex-ante** predicted daily variance *allocation* profiles better than the unconditional/time-specific/volume-driven benchmarks on new dates? No trading alpha/profits are implied.

---

## 3. Canonical data: provenance, timestamps and quality

### 3.1 Universe, clock and file reuse

- Asset SPY, regular full session **09:30:00–16:00:00 America/New_York**, DST-aware. One-minute aggregate timestamps mark the **interval start**; explicitly verify vendor semantics in reused B data. 390 eligible one-minute bars for each complete standard day; last starts at 15:59. Do not merge after-hours with the regular session.
- Exclude short sessions, halted/incomplete days and known corrupt rows from the *primary strict sample*, with counts and exclusions; use controlled missing-minute sensitivity, never hidden forward filling. Be especially careful if missingness rises in volatile years.
- Source one-minute OHLCV exactly once via **read-only** reference from existing B data. Reuse whatever canonical minute files are already present; do not copy/duplicate data (past EBM experiments grew to ~25 GB). No wholesale new vendor downloads until coverage audit.
- **Definition of minute return:** first return `log(close_09:30 / open_09:30)` within the first 09:30 minute (not previous close→09:30 gap); subsequent returns `log(C_t/C_(t-1))` for consecutive minute bars through 15:59. Thus 390 minute returns and 78 groups of five, no overnight increment. This is an operational OHLCV-proxy convention, not the source paper's underlying transaction-price estimator. Audit adjusted/unadjusted split policy, discontinuities, corrupted first opens, crossed/inconsistent prices, and zero/negative price errors. Reproduce this exact choice in unit tests.
- Use numerical double precision; calculate `R_d>0`, vector sums, range checks `Q∈[0,1]`, `|sum Q-1|<1e-10` under reasonable rounding. Record share extremes, zero-share frequency, nonzero count, open/close contribution and 1-min RV breakdown.
- Raw SPY 1-minute data need **not** be duplicated in a daily-by-k Parquet if an existing canonical file is safe to reference. Retain one compact derived day×78 matrix (or long view) and small day-level state table keyed by `(session_date,k)`, with immutable hashes and versioned transforms.
- Existing B eligibility/counts and B's late-session target definition are **not** C's daily volatility eligibility. Run a fresh full-session audit.

### 3.2 Daily state variables and information availability

| Code | State or covariate | Exact operational default | Available when? | Role |
|---|---|---|---|---|
| Z0 | **lagged market variance level** | `Z0_d=log(R_{d-1})`, previous complete **regular-session** RV, with a fixed log floor used only if numerically essential | Before today's open | **Primary accessible continuous state**, common for discrete/continuous analysis |
| ZV | **lagged VIX close** | Previous eligible trading day's published VIX closing observation (not today's closing value) | Before today's open | Strong literature-proxy robustness; preferred when reliable alignment exists |
| Zopen | **VIX at market open** | Actual point-in-time VIX observation at/just before 09:30 ET if source entitlement and timestamps allow | At open | **Closest R1 source-style descriptive state**; **not mandatory** if absent |
| Zret | Previous-session return sign | sign of `(previous regular-session close)/(prior session close)−1`; explicitly separate close-to-close from regular-session open-to-close | Before today's open | R2 directional state |
| Zchg | Lagged change in RV | `log(R_{d-1})-log(R_{d-2})` | Before today's open | R2-motivated alternative, not contemporaneous rise |
| Zvol | Past relative share volume | `log((V_{d-1}+ε)/median(V_{d-21:d-2}+ε))`, volume totals from complete earlier full sessions; fixed positive ε for numerical guard | Before today's open | Trading activity extension |
| Zfomc | Scheduled FOMC announcement day | Indicator for actually scheduled decision/statement during trading session; use timestamped historical releases and exclude surprise emergency events or tag separately | Announcement schedule generally known in advance | Optional small subgroup (sparse) |
| Zd | **same-day total RV** | `R_d` constructed from all realized intraday returns | After close only | **Retrospective D-mode diagnostic ONLY**, not in primary ex-ante C model |
| Vsame | Same-day total volume | total regular-session shares | After close only | D-mode explanatory sensitivity only; prohibited in F-mode |

**State priority:** `Z0` accessible main state. If reliable lagged VIX is available, run the same scientific analysis in a **clearly separate replacement-state sensitivity**, not collapse the states or optimize which one "looks better." If true Zopen is available, additionally attempt source-inspired VIX grouping with [5,25] and [75,95] full-sample quantiles **in retrospective D mode**, and with train-only quantiles in F mode. Do not label lagged VIX, opening 30m realized volatility, and opening VIX as the same state. Previous-session RV and previous-day close VIX are distinct economically. B's opening 30-minute RV can be carried into **a separately labeled after-10:00 descriptive/predictive-day remainder analysis**, never used as a predictor of the full-day profile if claiming an at-open forecast.

### 3.3 Reference sorting and state support

- **R1 source analogue:** source exact high/low VIX windows `[75th,95th]` and `[5th,25th]`; VIX-at-open if available, else explicitly "lagged VIX proxy" or "lagged RV proxy". Use training-only quantile cutoffs for held-out tests. The extremes are omitted **only for the particular source-style comparison**, not silently dropped from the full continuous-state study.
- **General discrete state:** train-only terciles for Z0; keep labels and edges fixed for held-out period. Primary continuous input is exactly the **same Z0** numeric data.
- **Support:** report days per state, time bin, environment and joint-state subgroup; numerical distributions and common-state overlap. For joint states use train-defined coarse bins; abstain on sparse cells. Do not extrapolate fitted table values as identified raw responses at unsupported state combinations. A continuous state is conditional on a distribution; state-grid evaluations may require smoothing and support assumptions.
- **Ex-post normalization:** Q_d uses realized complete-day denominator. This is **an outcome construction**, not lookahead in a descriptive scientific regression, and is a legitimate *forecast target* if predictors are earlier; but it cannot be used as a same-day predictor.

### 3.4 Schema / allowed storage

Minimum immutable day table: `date_et, data_source_id, regular_390_ok, exclude_reason, rv_daily, share_open30, share_close60, share_midday, daily_return, daily_volume, prior_close_vix (optional), vix_open (optional), z0_lag_rv, zret, zchg, zvol, fomc_flag, source_era_tag, calendar_environment, normalization_valid, raw_minute_reference, hashes`. Day×interval table: `date_et, interval_k, start_et, end_et, rv_k, q_k, valid`. Prefer one physical compact table plus lightweight joins/views rather than repeated state/model-specific copies.

### 3.5 Mandatory QA / negative controls

Synthetic day with known 390 one-minute increments; check 78×5 segmentation, 1st minute opening price anchor, final 15:59 minute, no overnight, partition sum, Q window indexing, DST transition, regular vs half day, previous-session lag identity, monotonic timestamp ordering, duplicate minutes, no filling missing minute into squared returns, min-volume and missing-price anomalies. Exclude or tag split/outlier discontinuities by objective QA, not Y's observed scientific effect. Compare `sum_k rv_k` to total minute-return RV and sanity-check 5-minute close-return RV as **different, nonidentical** measurement.

Negative controls: (i) permute day-state assignments in broad contiguous time blocks as an exploratory falsification without claiming universally valid p-values; (ii) time-shift state forward (`Z_{d+1}`) as an expressly **leaky placebo**, never a candidate predictor; (iii) compare fitted curves against day-level direct means; (iv) confirm profile shift persists after excluding clearly irregular sessions; (v) spurious percentage-change effects from tiny low-RV denominators.

---

## 4. Time splits, hypothesis scope and discovery discipline

### 4.1 Sample eligibility first; split freeze second

Before computing any fitted scientific results, Stage 0 determines actual full-session coverage. The **default** split is chronological **first 60% eligible days development-training, next 20% validation, final 20% evaluation**, with boundaries recorded as exact dates in `protocol_v1.0.yaml`, along with all exclusions and source-access limitations. This fraction rule—not selected calendar years—avoids assuming B's full accessible history. If sufficient source-era dates are available, provide a separate *historical comparison window* similar to R1, keeping it out of the claim of source-exact replication. If data are short (e.g., <~750 complete days), downgrade quantitative reliability and request review before ambitious state×state interaction work.

**Critical prior-inspection disclosure:** B's 2024–2026 test segment and some related intraday return plots were previously examined. Thus reused dates are **not a pristine untouched research holdout**. Still freeze protocol before new Experiment C profiles, and label later-period evidence as predeclared within-C but **not historically blind**, with no stronger claim unless new untouched dates/external assets become available. Never hide this issue or manufacture a new random split to call it sealed.

### 4.2 Frozen hypothesis families and multiplicity

Prespecified *primary* scientific contrasts for reporting: (H1) closing-hour high-versus-low volatility share, directional based on R1; (H2) opening-half-hour prior-negative-return vs prior-nonnegative-return share (R2-motivated); (H3) whole-day profile TV distance by primary state; (H4) incremental **held-out** change in joint profile score when adding lagged return sign + lagged relative volume beyond volatility state; (H5) change in across-environment **same-state** residual profile discrepancy upon adding states. H4/H5 are exploratory **unless confirmatory thresholds and held-out sample allocation are fixed prior to tests**. An illustrative FOMC comparison is secondary; no claim of novel FOMC effect.

Report p-values/CIs after correcting within the **declared primary family** (Holm or simultaneous block-bootstrap max statistic if assumptions justified). Explore many times of day with **whole-profile bands or max-statistic** rather than 78 isolated unadjusted p-values. Exploratory subgroup plots are labeled exploratory, not evidence of a newly confirmed state threshold.

**Materiality:** the tolerances from §2.1 apply on a **fixed supported universe**, measured in daily profile allocation units. For observed confidence band `[L,U]` for signed difference δ: conclude `MATERIAL POSITIVE` if L>ε, `MATERIAL NEGATIVE` if U<−ε, `APPROXIMATELY INVARIANT` if max(|L|,|U|)<ε, else `INCONCLUSIVE`. For TV ≥0: equivalent upper <ε or lower >ε. Confidence-event validity must be scoped; otherwise report descriptive uncertainty rather than a theoretical guarantee.

---

## 5. Model ladder — from scientific empirical baseline to EBM

**Comparison set is chosen for scientific meaning, not only minimum forecast error.** Every estimated model must predict on the *same* eligible dates, information set, day-level target, and supported state range.

| ID | Model | Mathematical target / role | Main restrictions |
|---|---|---|---|
| M0 | Direct unconditional mean `bar Q(k)` | Established intraday pattern | Train days only for forecasting; descriptive sample averages separately labeled |
| M1 | Direct high/low conditional means + date-block uncertainty | Reproduce state-conditioned profile signatures | Retrospective source-style groups and predictive train-defined groups not interchanged |
| M2 | Time-of-day-only smooth spline / kernel periodic curve | Established functional nonparametric comparator | Fixed train-chosen bandwidth/df |
| M3 | Additive state-level model `f(k)+g(z)` | Negative control: no k×z shape modulation | Not naturally normalized to sum one without constraint |
| M4 | Varying-coefficient spline/GAM `f(k)+g(z)+h_smooth(k,z)` | Smooth continuous state transition | Tensor spline complexity predeclared |
| M5 | EBM with **explicit k × Z0 pair** | Main nonlinear interpretable **one-state** profile | State numeric; engineered time k; interactions frozen/predeclared |
| M6 | EBM with k × *discrete* Z0 | Same state in low/mid/high quantile representation | No different state measurement; quantify coarsening loss |
| M7 | EBM with `k×Z0`, `k×Zret`, `k×Zvol` | Additive-in-states conditional profile extensions | **No unrestricted k×Z0×Zvol synergy**, even though joint predictions depend on multiple states |
| M8 | Structured normalized conditional profile comparator | Satisfy predicted shares sum one and nonnegativity | E.g. regularized softmax-of-scores or logistic-normal time profile, evaluated on same days |
| M9 | Small, specifically declared higher-order comparator | Does mixed-state **joint** effect beyond pairwise sum matter? | Stratified GAM or selected 3-way tensor spline only if enough independent days/support; else abstain |
| M10 | Domain-specific comparison | Time-specific volatility regression / lagged-volume model | Match obtainable published benchmark; do not falsely claim exact implementation of R5/R6 |

**Main EBM form (actual software model, not theorem about its path):**

\[
\widehat q(k,z,w)=\widehat\beta_0+f_k(k)+g_0(z)+\sum_j g_j(w_j)+h_{k0}(k,z)+\sum_j h_{kj}(k,w_j),
\]

with explicit interactions and controlled complexity. For a full k curve, use **predictions of the whole fitted model**. Raw EBM component tables can be reallocated/purified, and therefore should not be interpreted as uniquely defined scientific effects. The role of each other state depends on the terms included. **A standard 2-way EBM cannot fit arbitrary k×Z0×Zvol surfaces**. If a corresponding claim is sought, use M9 and a clearly labeled alternative model/fit, not a purported native 3-way EBM result.

**Simple baseline details:** direct conditional day averages (the decisive sanity check), low-order varying-slope interaction, splines/tensor GAM, and a normalized profile method. A very large feature zoo is prohibited. Use a strictly bounded hyperparameter matrix, such as `{max_leaves ∈ [2,3,5], learning_rate ∈ [0.01,0.05]}` with a fixed small bag/seed budget; these are candidate grid *ideas*, not software-validated settings. All exact fitting knobs must be frozen in a version-controlled config **before** Stage 3. Model selection uses chronological validation only. State-dependent effects are specified in advance; don't rely on automatic interaction discovery in the main scientific model.

### 5.1 Compositional-response safeguards

- Raw per-bin EBM squared-loss predictions can be negative or sum to !=1. **Do not silently clip and call the resulting vector the original EBM regression.** Report the raw output's range and sum-to-one defect. Evaluate any optional *renormalized* vector as a clearly separate postprocessed predictor (clip negatives at zero, sum-normalize with a frozen zero-sum fallback). Compare against M8 which models normalization structurally. This postprocessing changes the map and can create artificial interactions.
- A log-transformed `log(q+ε)` model does **not** directly estimate `E[Q|state]`; back-transform has bias and changes the estimand. Do not make it primary without target change approval.
- Squared share error across 78 intervals overweights different parts than an integrated-profile discrepancy; report MAE/TV and proper scoring appropriate to compositional predictions. For day-level predictive scoring use Brier/mean squared profile error and TV/absolute-profile loss on *held-out complete days*, plus window-level loss. Log score/KL only for strictly positive normalized predictions with disclosed epsilon and proper denominator.
- Report day-level joint curve predictions and intervals/uncertainty across days rather than treating 78 interval rows as 78 independent outcome draws.

### 5.2 Forecast mode F versus descriptive mode D

In **D**, one may retrospectively group by `R_d`, realized full-day volume, or same-day event occurrence to describe the relationship, but every such predictor is marked `D_ONLY` and excluded from any forecasting claim. In **F**, only `Z0`, previous close VIX, past return, past volume, and known preannounced calendar flags are allowed. For any 10:00 reforecast using opening RV, predict **the remaining-day profile** conditional on information through 10:00 and define a new target/denominator; require a new approved branch, not silent reuse of full-day at-open forecasting performance.

---

## 6. Scientific plots and numeric shape diagnostics (required outputs)

Use actual supported predictions and direct empirical means on the **same query grid**. Produce both discrete and continuous state views.

**Minimum plots** (labeled with exact target/state/period):

1. Unconditional `Q(k)` mean with 5–95% distribution quantiles and date-block uncertainty. Include per-day raw squared-minute RV and aggregate component shares.
2. Low/mid/high `Z0` profile overlays and the R1 source-style `ZV` high/low overlay where data permit. Show open/mid/close windows and direct empirical curves vs EBM vs GAM, with uncertainty.
3. Continuous Z0 profile heatmap (time k × Z0), 5 representative train-defined quantiles (10,25,50,75,90%) and their curves. Mark unsupported portions, observed state densities and bin/tile occupancy.
4. Signed shape contrast `D(k;k0,zH,zL)`, window-share differences and TV distance with simultaneous uncertainty where defensible. State whether difference is vertical allocation, slope/curvature within profile, or due to state mixing.
5. R2-like increment and residual variance reduction from added prior return sign / lagged relative volume *at each k*, and total `TV`/profile score. Avoid interpreting small numerical improvements as discoveries.
6. Matched-state across-period profiles; compare marginal drift with fixed-state drift; report reference-weight standardization as **a new estimand** if used.
7. Negative/failure figures: unsupported tails, null controls, and cases where EBM and direct estimates disagree or predictive gain is absent.

**No forced curvature:** shape descriptors include close-hour fraction, open-hour fraction, peak location, center-of-volatility time, profile entropy/concentration, monotonic rise after 15:00, slopes/curvature of the state-dependence of **window shares** (estimated using justified smooth models, not raw EBM table differentiation), sign and crossing of prespecified profile contrasts, and distances between state-specific functions. For smoothness parameters or threshold locations, give uncertainty and selection warnings; no post-hoc dramatic threshold story.

### 6.1 Model-fidelity audit

Scientific target is **Q conditional mean**, not a displayed component of fitted model. Audit `m` (via heldout/direct cell summaries), `F*` (population proper-class target, generally not known), `Fhat`, its total-response predictions, and individual plotted components separately. Compute empirical comparison of total-response contrasts at supported joint inputs; summarize model–direct discrepancy with uncertainty and model-adequacy checks. A low global Q-prediction loss does not guarantee fidelity of a rare state/time-bin contrast. Consult the project's Paper P1 and Paper P6; their proofs for restricted physical shallow-tree learners do **not** automatically transfer to default InterpretML's greedy/bagged optimizer or arbitrary time-series data.

---

## 7. Inference, dependence, selection, and environmental stability

- **Primary sampling unit:** full day. The 78 intervals have deterministic `sum Q=1` coupling, and consecutive days are temporally dependent. Never use naive individual interval row IID standard errors.
- Predeclare **contiguous-day moving-block bootstrap** and/or a valid HAC sensitivity for window-share contrasts over time. For exploratory planning consider block lengths 5, 10 and 20 trading days; these are robustness choices, **not a theorem that real markets are m-dependent**. Record blocks and effective independent-day units. Avoid naive i.i.d. row permutation.
- For honest tests of fitted-EBM shapes, either **refit the entire learner** in each resampled development block (including fixed selection protocol) or use separately declared model-free direct held-out summaries where the fitted queries were frozen on training. No confidence interval from EBM bag variability alone should be treated as a scientifically valid raw-mean CI.
- Use one or more *complete held-out calendar environments* with fixed state definitions; note past B analyses already inspected several dates. Use date-aware sample splitting and block-based uncertainty as applicable. Confidence statements conditional on a fixed discovered query need independent data or full selection protection; unadjusted maxima over many plotted days/states are exploratory.
- **Across-environment shape test:** report `m_e(k,z,w)` at the **same** supported state configuration. Distinguish differences from changes in `P_e(Z,W)`, different support, changes in total RV, and model projections under different Q. Prefer standardization on an explicitly declared common support distribution and label the standardized target.
- **Adequacy:** compare direct conditional profiles, M4 and M8, and the appropriate EBM on the same support. If curves disagree, audit because proper low-order interactions can distort even well-predicted raw contrasts. Do not claim that a shape inferred from SPY tells why market institutions caused a shift.
- **Near invariance:** choose numerical epsilon from §2.1 and require the entire relevant uncertainty set under a justified procedure to fall inside tolerance; do not infer invariance from high p-value of exact equality test.
- **Dependence:** only apply an existing proof (e.g., fixed-m-dependent cluster results) after checking full process assumptions. Otherwise report block-based empirical sensitivity and uncertainty qualifiers; no generic mixing/HAC coverage theorem is invented.
- **Multiple states / multiple comparisons:** limit predeclared primary tests, use familywise/multiplicity controls, disclose exploratory interaction search, and do not recycle previously observed B results as new hypothesis-free confirmatory evidence.

---

## 8. Evaluation, success criteria, expected findings and failures

### 8.1 Non-exhaustive evaluation metrics

**Scientific:** recovered conditional qualitative signatures; high-low closing/open share difference (pp); whole-profile TV; simultaneous band coverage/width diagnostics; additive versus nonlinear contrast; continuum stability/evolution; across-period same-state TV; residual environmental variation explained by new states; subgroup support and abstention rates; agreement between direct scientific summaries and full model predictions.

**Predictive secondary:** heldout daily-profile MSE/Brier; mean absolute deviation across 78 bins; TV prediction loss; normalized-profile validity; loss on close-hour/open-hour share and FOMC-time windows; paired improvement over M0/M2/M4/M8/M10 on same dates with date-block intervals; robustness to spread/transaction effects only if an actual decision/trading task is separately approved. Costed evaluation, no automatic trade profitability.

### 8.2 Explicit evaluation of additional states

For model `M_base` containing time×volatility and model `M_plus` adding prescribed time×previous-return-sign and time×relative-volume terms, evaluate **incremental held-out error** and **reduction in same-state cross-period profile discrepancy** on common support. Condition on the volatility state to isolate additional information; if adding states merely changes its distribution and produces no incremental conditional improvement, record this as a negative result. Treat the interaction hierarchy truthfully; M7 cannot discover arbitrary 3-way effects, and M9 is a separate restricted comparator.

### 8.3 Expectations (not guarantees)

- A U-shaped average volatility profile is expected and serves as a **data sanity check**.
- Intraday profile differs across volatility regimes in published index futures studies; SPY lagged RV may show a weaker or different response than **concurrent opening VIX**.
- Previous-day negative return may increase early-session relative variance, but the R2 estimator/markets are different.
- Past volume may account for some profile variation but literature already contains volume-driven intraday models.
- Fine interaction curves can be unstable at state extremes even when prediction improves; require supported statistics.
- A strong EBM with no extra explanatory gain over a spline/GAM is scientifically informative. Mixed-state interactions may be unsupported or not useful; **do not force a positive claim**.

### 8.4 Failure and interpretation matrix

| Finding | Required diagnostic/action | Defensible conclusion |
|---|---|---|
| No U shape | Check session anchors, missing bars, overnight inclusion, split adjustment, source and daily denominator, extreme days | **DATA / CONSTRUCTION REVIEW**, not immediately a finance discovery |
| Source high-low sign absent | Verify which VIX measurement was used, exact quantile groups, SPY-vs-E-mini, era, windows, source estimator | **NONREPLICATION OF PROXY SIGNATURE**, no model rescue |
| Distinct curves only in raw variance, not Q | Check normalization, denoms, conditioning | State affects overall level, **not relative profile** by this evidence |
| EBM curves dramatic, direct cell means flat | Check effective days, supports, joint composition, bag/purification bias, model complexity | **POTENTIAL FIT/PROJECTION ARTIFACT**, abstain |
| High-low differences but confidence covers zero | Quantify SE and detectable magnitude; no significance claim | **INCONCLUSIVE**, not invariant |
| Upper simultaneous band < meaningful ε | Verify target and valid coverage conditions | **SCOPED AFFIRMATIVE NEAR-STABILITY** |
| EBM outperforms M0 but not M4/M8 | Report paired losses and shape corroboration | **NO DEMONSTRATED EBM-SPECIFIC ADVANTAGE** |
| Additional states help in-sample but not heldout | Retain negative result; assess support and complexity | **NO GENERALIZING INCREMENTAL EXPLANATION** |
| Full-day realized RV used in at-open feature | Record `INVALID-LEAKAGE`, remove from F, allow D-only sensitivity | **INVALID FORECAST** |
| Pre/post curves differ, but state distributions drift | Match/fix states on common support and repeat; report standardized target separately | **COMPOSITION / RAW-SHAPE DISTINCTION** |
| Narrow new subgroup contains few days | Predeclared abstention, collapse only with approved protocol, show uncertainty | **INSUFFICIENT SUPPORT** |
| Dataset from prior B test already inspected | Disclose; use fresh future/external asset for true independent replication if feasible | **NOT AN UNTOUCHED HOLDOUT** |

No successful-trading gate. CV success can be: careful literature replication, valid shape analysis, evidence for/against explanatory states, and rigorous negative results.

---

## 9. Phased implementation and strict stop/go gates

**S0 — Repository/data feasibility and source-method reconciliation.** Read `AGENTS.md`, inspect Experiment B repository/artifacts, data provenance, minute completeness distribution and existing source scripts; verify SPY available days, source VIX measurement vs lagged VIX, FOMC calendar, storage and CPU. Deliver `C_S0_feasibility.md`, no model fitting and no large downloads. **STOP** if minute data absent/mostly incomplete or key data cannot be justified. Minor API/filesystem adjustments logged.

**S1 — Canonical profiles and states.** Build one source-referenced canonical day×k research view, exact Q construction and all lagged states; 30+ synthetic and calendar/data-integrity tests (not a mandated test number if better justified). Reconcile percentages/composition, losses, source meanings; compute sample flow chart. **STOP** on time leakage or systemic missingness until fixed.

**S2 — Scientific reproduction before EBM.** Direct normalized means, source-style group curves, simple splines/kernel, Tsai sign/volatility-change analogues; predeclared H1/H2 differences, dates, confidence sensitivity. Do not reselect outcomes because curves weak. **PASS** means scientifically valid construction, *not* significant results.

**S3 — EBM and varying-state shape mapping.** Fit modest M3–M6 and normalized comparator M8. Freeze tuning/splits; plot discrete & continuous state curves, supported contrasts, window summaries, cross-check raw output sum. Evaluate on validation only for model choices, then designated evaluation sample under disclosure. Avoid indiscriminate run expansion.

**S4 — Mixed state/residual explanation.** Incrementally fit M7 with one added state at a time then small predeclared combination; compare M4/M8 and at most one M9 higher-order competitor after support/complexity gate. Quantify residual environmental profile drift and heldout loss. If no added evidence, STOP exploratory expansion and write an honest negative result.

**S5 — Distribution-shift, scientific adequacy and inference.** Date-block uncertainty, fixed-state environment comparisons, common support and composition, direct-vs-model gap, simultaneous or multiplicity-corrected window/curve contrasts, materiality versus inconclusive. Theory-applicability matrix and software caveats required.

**S6 — Independent validation, final report and handback.** Frozen-protocol heldout performance, all scientific results and failed models, caveat on reused B period, compact reproducible figures, complete source methods, limitation assessment, CV wording (no invented success). Produce final `experiment_C_full_research_report.md` and a one-page project abstract/README; separate persistent raw data from lightweight derived products.

### 9.1 Codex prompt requirements for each stage

Every separate Codex prompt must declare allowed edits, data paths, cryptographic hashes, reuse/no-copy rule, code/data QA, split/seed settings, resource budget, expected artifacts, error handling, stop conditions and a **mandatory coding-session Markdown report**. Codex must follow the user's `AGENTS.md`. No source archive alteration, secrets in logs, giant redundant parquet dumps or software-posterior error bars misrepresented as raw science. Large new downloads and scientific modifications need user approval.

### 9.2 Scientific escalation vs routine fixes

**Autonomously fix, with a change log:** type conversions, DST parsing, endpoint inclusive/exclusive errors, API pagination, schema differences, minor package pinning, small data gaps under predeclared exclusions, spelling and plot readability, code organization/test fixes.

**Escalate to scientific-design thread:** replacing SPY or the target Q, switching from five-minute intervals to 30 without versioning, redefining state to contemporaneous info for ex-ante mode, changing source grouping or main windows, changing date/testing protocol after viewing results, adding unplanned selected indicators, concluding source replication from incomparable estimators, weakening uncertainty standards to get a result.

---

## 10. Mandatory final reporting template

| Item | Report |
|---|---|
| Input asset/date range/full-session valid day count | Exact sourced counts and QA exclusions |
| Historical source | R1/R2 and actual definitions sampled |
| SPY proxy deviation | Trading instrument, session, estimator, VIX timing, era |
| Target | `Q_d(k)`, 78 bins, daily denominator; alternate ratio target if reported |
| Scientific state | Name, timing, continuous/discrete, retrospective or ex-ante, quantiles |
| Curve comparison | Which states, common support, time bins, direct means + EBM + smoother |
| Shape findings | Window percentage-point shifts, TV, curve contrast, valid CI and materiality |
| Added state findings | Incremental heldout effect relative to strongest benchmark |
| Stability | Fixed-state across-period vs marginal; reference standardization if any |
| Scientific fidelity | Whole-model predictions vs direct state-conditional truth proxy |
| Forecasting | Ex-ante info time, normalized constraints, baseline paired errors |
| Dependence/selection | Units, bootstrap/HAC assumptions, multiplicity, exploratory/confirmatory |
| Diagnostic exceptions | Changes, invalid branches, sparse state groups, negative outcomes |
| Implementation | Git commit/config/data hashes, no-dup storage, environment pins |
| Scientific conclusion | Established, new empirical, no incremental evidence, inconclusive, or invalid |

Include an explicit findings-status ledger: `SOURCE REPRODUCED QUALITATIVELY / NOT REPRODUCED`, `EBM ADDITIONAL SHAPE DETAIL SUPPORTED / NOT SUPPORTED`, `ADDITIONAL STATE INCREMENT SUPPORTED / NOT SUPPORTED`, `SCIENTIFIC STABILITY CERTIFIED / DRIFT CERTIFIED / INCONCLUSIVE`, `FORECASTING GAIN SUPPORTED / NOT SUPPORTED` with uncertainty and source-boundary annotations.

**No generated outcome is asserted by this specification.** Task C should begin at S0 in the existing Experiment B chat and conclude with a results handback to the originating EBM Theory chat.
