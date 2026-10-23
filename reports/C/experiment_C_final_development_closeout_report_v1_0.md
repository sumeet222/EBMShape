# Experiment C — Final Development Closeout Report

**Study:** State-dependent intraday volatility-profile shapes using interpretable models  
**Status:** `CLOSED — DEVELOPMENT COMPLETE; FULL VALIDATION DEFERRED`  
**Closeout date:** 22 October 2026  
**Scope of this report:** Completed P0 / C-spec preliminary audit, C1R, C2R, and C3. This is a **scientific and project-management closeout based on existing results**, **not** a new computational run, an independently replicated result, a new inferential certificate, or a claim that the original entire C0–C6 research specification was executed.  
**Scientific reference design:** `docs/specs/C/experiment_C_revised_complete_research_design_v1_1.md`, together with original `docs/specs/experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md` and revised transition handoff.  
**Central outcome:** Carefully implemented and diagnosed models recover a modest descriptive relationship between preceding-session RV and the following day's distribution of RV across trading hours. **Adding native EBM time×state interactions did not improve full-profile developmental prediction or establish better recovery of scientific shape contrasts than simpler approaches.**

---

## 1. Executive summary and decision

**Implementation verdict:** `PASS WITH QUALIFICATIONS` for data/source identity, basic numerical consistency, fitted model ladder, matched development backchecks, diagnostics, reproducibility, and data-preservation requirements.

**Scientific verdict:** `DEVELOPMENTAL STATE-ALLOCATION ASSOCIATION OBSERVED; ADDITIONAL EBM ADVANTAGE NOT ESTABLISHED; POPULATION SCIENTIFIC INFERENCE NOT CERTIFIED`.

**Project decision:** Close active Experiment C model development **now**, rather than use more resources on C4 additional market states, C5 fully calibrated selected-model scientific inference, or C6 reserved independent evaluation. Keep their names and scope in the archive as **DEFERRED / NOT RUN**, not as failed statistical tests. Work on other planned experiments can begin. This is a resource-allocation decision and **does not assert that more states are useless or that the conditional population shape is invariant**.

The principal source-inspired preliminary contrast was the percentage of daily realized variance allocated to **15:00–16:00 ET** when **the immediately prior complete trading session** was high-RV versus low-RV. On the explored 2016–2021 cohort, its raw difference was **+2.00498 percentage points**, with exploratory block-bootstrap intervals excluding zero under selected fixed-label settings. But its intervals did **not** establish an effect **greater than the predeclared 2-percentage-point materiality threshold**. It is not an independent historical replication of Andersen–Thyrsgaard–Todorov (2019), nor an independently confirmed result on new SPY dates.

The same one-state problem was investigated using direct averages; scalar and 78-bin OLS; time-only and varying-state splines; additive continuous/discrete EBMs; explicit time×continuous-state and time×discrete-state EBMs; and a normalized softmax-type profile model. On **489 matched chronological development-backcheck dates**, the **unconditional full-profile mean M0 was best for the main 78-vector MSE**, while a **simple state-dependent linear regression had the lowest closing-hour RMSE** among the listed models. Native interaction EBMs displayed nonzero state-dependent curves but **did not demonstrate incremental profile forecast performance**, and their fitted high-minus-low closing-hour allocation contrasts deviated more from the observed coarse group contrast than the simple linear and normalized comparators.

**Practical lesson:** **Detecting a state-related difference in a scalar aggregate is different from demonstrating a materially nonlinear 78-dimensional shape, and different again from showing that an EBM adds reliable scientific or predictive value.**

---

## 2. What Experiment C actually studied

### 2.1 Target and clock

Asset: **SPY**, ordinary full U.S. exchange sessions, **09:30–16:00 America/New_York**. Use exactly **390 genuine one-minute bars** per eligible session, labeled at the minute **start** in UTC and converted to ET. First minute return is opening-minute `log(C09:30/O09:30)`; subsequent minute returns are adjacent one-minute-close log ratios. **No overnight return** belongs in the intraday variance. There are **78 consecutive nonoverlapping five-minute bins**, each containing five squared one-minute log returns.

For day `d` and five-minute bin `k=0,...,77`:

```text
r[d,0] = log(C[d,09:30] / O[d,09:30])
r[d,j] = log(C[d,j] / C[d,j-1]), j=1,...,389
v[d,k] = sum_{j=5k}^{5k+4} r[d,j]^2
R[d] = sum_{k=0}^{77} v[d,k]
Q[d,k] = v[d,k] / R[d]
```

The scientific response is the **78-dimensional compositional daily variance-allocation curve** `Q[d,0:78]`: its components are nonnegative and sum to 1. A bin value of **0.01 means 1% of that day's RV** occurred in that five-minute interval. It is **not** a predicted return, instantaneous volatility, or a latent spot-variance estimate. The experimental unit for evaluation and sampling uncertainty is a **whole trading date**, not 78 supposedly independent observations.

Key declared windows, always fractions of **whole-day** RV:

| Window | ET clock | Zero-based `Q` slice | Status |
|---|---|---|---|
| `OPEN30` | 09:30–10:00 | `[0:6]` | Source-inspired early allocation |
| `MID_C` | **11:30–13:30** | `[24:48]` | Main C-study midday definition |
| `CLOSE_C` | **15:00–16:00** | `[66:78]` | **Main closing-hour target (H1)** |
| `MID_P0` | 12:00–13:00 | `[30:42]` | Preliminary compatibility sensitivity |
| `CLOSE_P0` | 15:30–16:00 | `[72:78]` | Preliminary compatibility sensitivity |
| `PRE_CLOSE_DIAG` | 15:00–15:30 | `[66:72]` | **Post-P0 exploratory**; not a replacement primary hypothesis |

These windows have **different durations**; a window's allocation fraction is not an equal-time per-minute volatility rate. Since all components sum to one, a greater allocation to one period can reflect redistribution **away from another period**; it does not automatically mean that period has more absolute variance.

### 2.2 Predictor/state and experimental modes

**Primary ex-ante state:** `Z0[d] = log(R[p(d)])`, where `p(d)` is the **immediately preceding scheduled XNYS session**, valid only if that predecessor itself was a complete eligible 390-minute ordinary session. It does **not** skip an incomplete or early-close immediate predecessor to reach an older complete day.

**Discrete representation:** `S0` is a **low/middle/high tercile category of the same underlying Z0 series**, with cutpoints fitted exclusively on each modeling training window and applied unchanged to its next chronological evaluation dates. The exploratory P0 full-period rank labels were separate **retrospective descriptions**, not deployable training cutpoints.

- **D / descriptive:** historical full-cohort means and curves; can use ex-post categories if clearly disclosed. Not an independently confirmed population statement.
- **F / ex-ante information:** model uses only data known by the morning open to predict the entire day's subsequently realized profile. Historical chronological backchecks used past-only fits, but their 2020–2021 dates were already explored in P0; they are **developmental**, not untouched validation.
- Same-day 09:30–10:00 realized volatility was studied in P0 only as a **retrospective state of the full-day response**. It mechanically overlaps the first response bins; it is **not** an at-open input for predicting those bins.

### 2.3 Published-literature relation — precise limitation

The original C research design anchors the scientific idea in Andersen, Thyrsgaard & Todorov (2019), Tsai, Eom & Wang (2024), and later volatility-periodicity/stationarity/forecasting literature. The central published Andersen–Thyrsgaard–Todorov application used **E-mini S&P 500 futures, VIX observed at the start of the day, and a different periodicity/volatility-estimation and testing framework**. Experiment C used **SPY, preceding-day realized variance, and within-day squared-minute-return allocation**. Accordingly, results are **source-inspired SPY proxy comparisons**, **not exact replication**, and neither significance nor source-effect magnitudes transfer automatically.

---

## 3. Verified source, sample, and operational QA

### 3.1 Single reusable source graph

The successful 2016–2021 development data comprise:

```text
B_alpaca_sip_SPY_1m_split_D2_v1
   six B annual Parquet references, selected original 1-minute keys
      +
C_spy_1m_p0_v1_1_missing_keys
   72 C-only compressed monthly disjoint-key source partitions
      ↓
Existing P0 daily_profiles.npz: Q, v, RV, date/eligibility masks
      +
C1R keyed Z0/Zchg predecessor/state table
      ↓
C2R saved simple-model outputs → C3 matched EBM/model comparison
```

- Source: **Alpaca SIP SPY one-minute split-only-adjusted bars**; not dividend-total-return prices.
- The C supplement reuses the D2 historical dataset without copying overlapping raw bars; no separate Hugging Face repair rows entered this C source graph.
- In the C1R audit: **6 original annual references + 72 C supplemental partitions**, all identities/hash checks passed. The supplement is approximately **10.3 MB** and contains **448,173** disjoint new minute rows; reusing **136,337** D2 source rows produced **584,510** distinct observed minute keys in the audited development source view.
- The existing daily arrays were reused; C2R/C3 did **not** download another source or duplicate the original raw data. The earlier P0 acquisition used approximately **119.7 MB** response-body transfer under its then-approved limit; this does not authorize new future downloads.

### 3.2 Eligibility and known limitations

| Quantity | Verified development value |
|---|---:|
| Main dates | **2016-01-05–2021-12-31** |
| Full-profile-valid sessions (`Q`) | **1,491** |
| Strict immediately prior-RV-valid primary (`Z0`) | **1,472** |
| Two-prior RV-change-valid (`Zchg`; not modeled in C3) | **1,454** |
| Excluded early closes | **12** |
| Incomplete ordinary sessions | **7** |
| Missing one-minute bars on incomplete ordinary sessions | **100** |
| C2R/C3 matched modeling cohort | **1,472 distinct dates** |
| Chronological C2R/C3 backcheck dates | **2020: 241; 2021: 248; pooled: 489** |

Incomplete ordinary sessions: **2016-02-02, 2019-08-12, 2020-03-09, 2020-03-12, 2020-03-16, 2020-03-18, 2021-05-05**. Four missing dates are in the March 2020 shock period. None was forward-filled or silently reconstructed for this study. **Nonrandom omission of turbulent sessions limits stress-regime generalization.**

C1R verified source hashes; tested six reconstructed 390-bar dates; checked `Q` arithmetic, actual scheduled predecessor mapping, window indices and no overnight contamination; and reported max `|sum Q-1| ≈ 5.55×10^-16`. Subsequent modeling checks preserved those source identities. C2R finished a focused 22/22 test suite; C3 reported successful model, graph, transform and score reconciliation. These are **implementation QA claims**, not proofs of correct economic measurement or sampling-law assumptions.

### 3.3 Future-horizon status at closure

C1R identified a **proposed, not approved**, larger physical coverage horizon through **2026-09-30**. The B-preserved later-year source is generally **only selected 91-minute windows**, not complete C-study full-session bars. Complete 2022–2026 SPY C profiles were **not built, inspected, or evaluated** in C1R–C3. C1R estimated the separate future acquisition might require approximately 94 MB transfer under comparable Alpaca conditions, but this was **a proposal without download authority**. The full-C horizon and exact chronological 60/20/20 evaluation cutoffs were **not finalized**.

The **2024–September 2026 Experiment B reserved segment remains unopened for C scientific analysis**. Earlier B developmental work encountered 2022–2023 return outcomes, which also limits claims of universal historical blindness. The 2016–2021 C outcomes were thoroughly seen during P0, so backchecks inside them are **not independent C validation**.

---

## 4. Completed research phases

| Phase | Completed work | Result/status |
|---|---|---|
| **P0** | Complete-session acquisition/QA; raw three-state curves for same-day opening RV and previous-day RV; 78-bin mean profiles, H−L differences, block5/10 interval sensitivities, robustness | `PASS QA / WEAK overall`; narrow pre-close profile signal identified |
| **C-spec supplementary** | Wider predeclared 11:30–13:30 and 15:00–16:00 shares on **same P0 observations**, block sensitivity, mean/median/outliers | `GO for further descriptive investigation` **only** for PREV closing hour; not new replication |
| **C1R** | Read-only source/hash/coverage/eligibility protocol audit; Z0 and RV-change readiness; future acquisition and split assessment | `READY_FOR_C2R_DEV`, QA pass with qualifications; incomplete full-horizon and optional-state policies |
| **C2R** | Direct mean profiles; scalar OLS, piecewise/categorical/quadratic controls; 78-bin linear profile OLS; time-only splines; state×time tensor GAM; residual, influence, dependence, support and calendar diagnostics | `PASS WITH QUALIFICATIONS`; meaningful developmental scalar association, no reliable nonlinear/profile forecast gain |
| **C3** | T0 and complete one-state EBM ladder: continuous/discrete additive, continuous/discrete time×state interactions; M8 normalized model, normalization variants; same-date matched comparisons, extensive scientific diagnostics/theory-applicability audit | `PASS WITH QUALIFICATIONS`; EBM nonlinear advantage **not established** |
| **C4** | Additional-state EBMs (`Zret`, `Zchg`, relative volume; optional more complex interactions/VIX) | **DEFERRED / NOT RUN** |
| **C5** | Full methodological inference, simultaneous calibrated raw mean bands, rigorous selected-learner uncertainty, environmental shape certification | **DEFERRED / NOT CERTIFIED** |
| **C6** | Authorized complete-horizon independent C evaluation and final held-out test | **DEFERRED / NOT RUN** |

Important: the phase labels represent the approved C scientific architecture. A negative C3 result does **not** retrospectively turn the deferred phases into completed negative findings.

---

## 5. Descriptive state dependence and scalar statistical models

### 5.1 Primary historical high-minus-low closing-hour allocation

On the 2016–2021 **previous-RV** groups:

| Quantity | Observed value / status |
|---|---|
| High − low `CLOSE_C`, 15:00–16:00 | **+2.00498 pp** |
| Historical P0 95% block-5 interval | **[+0.927, +3.080] pp** |
| Historical P0 95% block-10 interval | **[+0.839, +3.206] pp** |
| C2R additional 95% block-20 interval | **[+0.832, +3.296] pp** |
| High − low 09:30–10:00 share | **−2.205 pp** |
| High − low 15:30–16:00 share | **+0.594 pp**; interval included zero |
| High − low whole-profile direct `TV` | **0.0485101** |
| Materiality reference for H1 | **+2 pp** |
| Confirmed population `H1 > 0` | **NOT CERTIFIED** (explored sample; conditional intervals) |
| Confirmed population `H1 > 2 pp` | **NOT CERTIFIED** |

The fixed-label block bands assume a particular resampling design for temporally dependent dates and condition on the observed retrospective group definitions. **Positive intervals on previously examined historical groups should not be called newly confirmed discovery.** The nominal comparison to the 2-pp threshold has inadequate separation: the estimates are near 2 pp and the lower interval bounds are below 2.

Removing the last five-minute bin gives a newly defined diagnostic numerator: **+2.352 pp** over 15:00–15:55 while the 15:55 bin contributes about **−0.347 pp**. Similarly **15:00–15:30 ≈ +1.411 pp** is an algebraic, **post-P0 noticed** contrast of nested 60-minute and last-30-minute differences. Neither is an approved replacement H1, an independent finding, or assigned an inherited confidence interval.

### 5.2 C2R scalar OLS (closing-hour share)

Models included: intercept-only L0; linear continuous `Z0` L1; discrete state levels L2; state-specific slope/level L3; and quadratic `Z0` L4. The main analytical distinction is **a linear state association** versus **extra nonlinear/within-category slope moderation**.

| Predeclared conditional test, D_FULL historical model | HAC10 nominal p | Six-test Holm reference p |
|---|---:|---:|
| Linear L1 RV-state slope | **0.0001219** | **0.0007315** |
| L2 categorical state levels | 0.002196 | 0.008784 |
| L3 joint piecewise state slopes | 0.06954 | 0.20861 |
| L4 quadratic curvature | 0.22821 | 0.45642 |
| Historical raw H1 direction > 0 | 0.0003543 | 0.001772 |
| Historical raw H1 > 2 pp | 0.49664 | 0.49664 |

These are **conditional/asymptotic developmental reference tests**, not proof under fully verified financial time-series assumptions, and Holm does not undo P0-driven attention to the close-hour relation. The scalar model L1 has training R² ≈ **0.0142**, indicating modest explanatory power and substantial day-to-day uncertainty even with a detectable association. The evidence did **not** establish that state-specific slopes or quadratic curvature improve the scalar scientific relationship.

### 5.3 Diagnostics materially affecting interpretation

- **Residual distribution:** substantial right skew (~1.7) and excess kurtosis (~5.2) in full-sample closing-hour regression residuals; QQ plots deviate markedly in the positive tail. Ordinary Gaussian-reference residual diagnostics should be treated as warnings, not fully valid time-series p-values.
- **Serial and calendar structure:** residual autocorrelation in daily dates; 2020 stands out as a different residual regime. HAC score covariance with scheduled date gaps and shared date-block bootstrap were used as exploratory uncertainty methods; assumptions such as stationarity, moments, and stable process are not proved.
- **Influence:** predeclared FULL/top-1%-RV/top-five-Cook/exclude-2020 analyses; removing 2020 changed the historical raw H1 from **+2.005 pp to +1.337 pp**. Flagging influential observations is not a warrant to delete them from the primary sample.
- **Support and state distribution:** 2020 low-RV group has only **21 distinct dates** under full retrospective states; this fails the basic ≥50-date / ≥20-five-date-group comparison gate. Within-2020 raw high-minus-low comparisons **ABSTAIN**. Regime mixtures differ across years; marginal mean shifts are not necessarily changes at the same fixed state.
- **Profile smoothness mismatch:** low-df splines reproduce the broad volatility U shape but smooth over sharp **14:00** and **15:55** features. This is a model-approximation issue; a flexible EBM capturing a sharp time bin is not automatically evidence of *time×state* interaction.

---

## 6. C2R profile OLS and spline benchmark: what happened

**Core C2R 78-vector comparisons:** M0 unconditional 78-bin mean, M1 state-category direct means, `P-OLS-Z` separate linear-by-time conditional profile, M2 low-degree smooth time-only curves, M4 varying-state tensor splines (`T8×Z4` primary; `T12×Z4` sensitivity), and a no-interaction matched spline. The scalar L models predict **only** closing-hour share, not the entire daily vector.

C2R used fixed chronological developmental backchecks: training through 2019 → 2020, then training through 2020 → 2021. Every comparison used identical eligible outcome dates per backcheck; preprocessing and quantiles were fitted on its earlier training dates. The outcomes had already been visually examined during P0, so **not independent holdout performance**.

The 8×4 spline fitted elaborate state-varying mean surfaces yet **had pooled profile MSE 0.000216181 versus M0 0.000212644**, approximately **1.66% higher error**. `P-OLS-Z` scored 0.000214366 on the full curve but predicted the closing-hour share with RMSE **9.053 pp**, better than M0 at **9.165 pp**. Better scalar close-share prediction is **not equivalent** to better full 78-component profile prediction. The time-only M0 is an important difficult baseline because it preserves real sharp five-minute features rather than forcing an overly smooth U shape.

The C2R native OLS/profile comparisons were also checked for whole-profile closure, unsupported state ranges, training-versus-evaluation gaps, direct-versus-fitted state-bin differences and distribution-shift biases. They supplied benchmarks and saved forecasts for C3 rather than just attractive plots.

---

## 7. C3 — completed one-state EBM family and normalized comparator

### 7.1 Actual fitted model ladder

| Code | Learner | Intended function and scientific role |
|---|---|---|
| `T0` | Native time-only EBM | Flexible time-of-day curve `f(k)`; no state |
| `M3c` | Native additive continuous-state EBM | `f(k) + g(Z0)`; **no** `k×Z0` |
| `M3d` | Native additive discrete-state EBM | `f(k) + g(S0)`; **no** `k×S0` |
| `M5` | Native continuous-state EBM | Explicit `f(k)+g(Z0)+h(k,Z0)` |
| `M6` | Native discrete-state EBM | Explicit `f(k)+g(S0)+h(k,S0)` |
| `M8` | **Non-EBM** softmax/logistic-normal-like linear-state profile | Structurally nonnegative, sum-to-one 78-vector comparator |
| `NORM_M5`, `NORM_M6` etc. | Separately named postprocessed EBMs | Frozen positive-part and rescale map; **not native EBM predictions** |

All 78 five-minute **nominal time categories** were retained in native main/pair terms. This matters: it preserves the **14:00** and **15:55** features, unlike unnecessarily restrictive smooth splines. Direct same-row model comparisons used **whole fitted predictions**, not arbitrarily centered individual interaction-term heatmaps.

EBM training used a small predeclared A/B configuration screen on chronological inner training folds (2016–17→2018 and 2016–18→2019). Main matched additive/interaction settings were config B (**400 rounds, 3 leaves, 16 numeric RV bins**), `max_bins=128`, `max_interaction_bins=96`; T0 used config A (**200 rounds, 2 leaves**). It disabled internal random row-based early-stopping splits and bag-based error displays (`validation_size=0`, one outer bag, zero inner bags, no early-stopping/smoothing). As a result, changed random seeds gave effectively identical predictions: **algorithmic determinism, not independent-population stability**. Approximately 59 native fits were used under the predeclared ≤60-fit cap.

The M8 normalized competitor uses a learned 78-bin softmax of a time intercept plus scaled Z0 score with a fixed state-coefficient penalty. It is not an EBM, uses a different fitting loss, and always yields a valid simplex profile. It is necessary to distinguish **the ability to fit an unconstrained interaction** from **the ability to deliver a physically meaningful normalized profile**.

### 7.2 Matched chronological developmental predictive scorecard

**Pooled 2020 + 2021 development backchecks, N=489 unique dates. Lower is better.** Profile MSE averages squared errors across the 78 within-date shares and then across dates. Closing RMSE is in **percentage points of whole-day RV allocation**, not basis points of stock returns.

| Model | 78-bin profile MSE | Relative to M0 | 15:00–16:00 closing-share RMSE (pp) |
|---|---:|---:|---:|
| **M0: unsmoothed unconditional profile** | **0.000212644** | **Baseline / best** | 9.1653 |
| M1: direct three-state means | 0.000213284 | +0.301% worse | 9.1002 |
| **P-OLS-Z: time-specific linear state slope** | 0.000214366 | +0.810% worse | **9.0531 (lowest)** |
| M2-T8: smooth time-only | 0.000215247 | +1.224% worse | 9.2531 |
| M4-T8-Z4: varying-state smooth spline | 0.000216181 | +1.663% worse | 9.1638 |
| T0: time-only native EBM | 0.000213858 | +0.571% worse | 9.2234 |
| **M3c/M3d: matched additive EBM** | **0.000212654** | **+0.004% worse** | 9.1659 |
| **M5: continuous `k×Z0` EBM** | **0.000213411** | **+0.361% worse** | 9.1386 |
| **M6: discrete `k×S0` EBM** | **0.000212870** | **+0.106% worse** | 9.1066 |
| M8: structurally normalized profile | 0.000214098 | +0.684% worse | 9.0554 |

Native interacting EBMs have minor numerical gains in **closing-hour error** versus M0, but neither is best on that target. **Neither improves the predeclared full-profile MSE over M0 or the matched additive EBM.** Predictive differences are small compared with the inherent variability in daily profiles; they have not been independently validated on later C dates.

A notable operational observation: M3c and M3d are nearly exactly the unconditional fitted time curve. For balanced daily-normalized Q rows, a `g(Z0)` term **constant across all 78 time slots of a day** cannot change the allocation shape; the learned scalar effect collapses near zero under the balanced squared-loss construction. This is **largely structural** and **must not be interpreted as evidence that prior volatility has no scientific impact**. State variation in the *allocation curve* requires a time×state response or another normalized state-varying profile map.

### 7.3 Paired developmental model comparisons

The named comparisons calculate **per-day loss differences (first minus baseline)** on identical saved 2020–2021 forecasts; negative favors the first. HAC10 and 5/10/20-date-block intervals concern **these fixed forecasts**, and neither refits selected models nor establishes general post-selection population coverage.

| Paired comparison | Pooled daily MSE difference | Interpretation |
|---|---:|---|
| `M5 − M3c`, full profile | **+7.578×10⁻⁷** | Interaction has *higher* MSE; fixed-forecast HAC10 interval positive, but the report's five-test Holm reference p≈0.0819 |
| `M6 − M3d`, full profile | **+2.170×10⁻⁷** | No reliable improvement; uncertainty interval spans zero |
| `M5 − M6`, full profile | **+5.408×10⁻⁷** | M5 worse than M6 on this development comparison; Holm reference p≈0.0264, conditional on unproved assumptions |
| `M5 − M0`, full profile | **+7.672×10⁻⁷** | M5 worse than unsmoothed baseline on point estimate |
| `M5 − M3c`, closing-share MSE | **−4.988×10⁻⁵** | Possible close-target gain, uncertainty interval spans zero |

**Inference boundary:** A positive HAC confidence interval for an adverse loss difference is a *developmental fixed-prediction diagnostic*. Validity depends on the loss-process assumptions and prechosen comparison family. In particular, any multiplicity reference p-value is conditional on its marginal sampling approximation and does **not** erase selection/previously inspected data. Do not convert the p≈0.0264 M5–M6 comparison into a general theorem that coarse terciles retain the relevant information.

### 7.4 Scientific shape fidelity: compare the actual same-cell contrast

The crucial scientific question was not only loss, but whether the model reproduced the *observed high-minus-low state difference at identical input rows and time bins*.

| Raw data or fitted model | Historical high−low closing-hour H1 (pp) | Difference from raw H1 (pp) |
|---|---:|---:|
| **Direct raw historical groups** | **+2.00498** | — |
| M1 direct state means | +2.04005 | +0.03507 |
| **P-OLS-Z** | **+2.04529** | **+0.04031** |
| M4-T8-Z4 spline | +2.11664 | +0.11166 |
| **M8 normalized** | **+1.90375** | **−0.10123** |
| **M5 continuous EBM** | **+1.56544** | **−0.43954** |
| **M6 discrete EBM** | **+1.39458** | **−0.61040** |
| NORM_M5 | +1.58665 | −0.41833 |
| NORM_M6 | +1.44070 | −0.56428 |
| M0/time-only/additive M3 | approximately 0 | approximately −2.00498 |

These are **in-sample D_FULL model-output comparisons against observed group means**. They are **not raw population truth**, independently held-out shape fidelity, or proof of actual population nonlinearity. M5/M6 show nonzero fitted interactions, but **attenuate the target historical H1 more** than simple P-OLS-Z and M8. This undermines any claim that the EBMs improved *scientific contrast recovery* by exploiting nonlinearity.

The raw whole-profile high–low `TV = 0.0485101` is near the original **0.05** reporting tolerance, but **point TV below 0.05 is not an equivalence certificate**. The raw M5/M6 fitted 78-vectors sometimes do not sum exactly to 1, so their `0.5×L1` is reported as a **raw half-L1 difference, not probability TV**. Normalized variants restore simplex validity and have separate model identities. Standard state singleton fit slices (e.g., training 10th/25th/50th/75th/90th percentile) are **software query outputs**, not separately identified pointwise conditional population means.

---

## 8. Advanced diagnostics and why no further EBM search was justified

### 8.1 Native architecture, complexity and numerical QA

- Model term graph: `T0: k`; `M3c: k,Z0`; `M3d: k,S0`; `M5: k,Z0,(k,Z0)`; `M6: k,S0,(k,S0)`.
- Same 78 actual time categories in main and pair mappings. Numeric state binning, effective terms, iteration counts, learned term scores and missing/unseen bins were audited; feature-importance and centered term magnitudes remain **software diagnostics, not uniquely defined scientific effects**.
- Native raw held-out profile closure defects reached **0.00910292 for M5** and **0.00373103 for M6** in max `|sum predicted bins−1|`; these prevent indiscriminate use of probability TV or calling raw predictions valid simplex curves. Separate NORM projection/positive-rescaling is a different estimand/predictor.
- Identical predictions across tested seeds arose from fixed deterministic settings; do not call this independent bootstrap stability.
- The smooth spline shape oversmoothing and sharp time-bin features were explicitly handled with flexible categorical EBM time coordinates **and** the exact raw-time M0 baseline. Any fit of the 14:00/15:55 peak is not by itself evidence of learned interaction.

### 8.2 Residual, dependence, influence and regime

- Date-level closing-share/whole-profile residuals; per-bin bias/MAE/RMSE and covariance eigenvalues; feature/error distribution by state; QQ residual shape; ACF/PACF, Ljung–Box and squared-residual/ARCH; annual/quarterly mean calibration; predicted versus observed; train-evaluation gap; 14:00 and final-bin sensitivities; and same-date matched model comparisons were implemented.
- Daily residuals exhibit **serial dependence**, and return-like standard normal assumptions are visibly poor. Standard reference p-values for residual diagnostics remain heuristic under heavy tails/nonstationarity.
- Date-level residual covariance has a **closure-induced null direction**. The 78 time bins are not 78 independent shape hypothesis tests; the eigenvalue spectrum is diagnostic, not independent discoveries.
- Fixed stress refits used the **same named exclusions for the models**: top 1% of current-RV days, all of 2020, and C2R's top five influential scalar OLS dates. FULL always remains the primary sample; exclusion of top current-day RV is **retrospective D-only**.

| Model raw historical H1 (pp) | FULL | Exclude 2020 | Drop top 1% RV | Drop fixed five OLS-influential dates |
|---|---:|---:|---:|---:|
| **M5 continuous EBM** | **1.565** | **0.777** | **1.497** | **1.451** |
| **M6 discrete EBM** | **1.395** | **0.900** | **1.206** | **1.172** |

The decreased H1 values on excluding 2020 show that the numerical shape contrast is **regime/sample sensitive**, not a uniformly stable learned scientific law. Some resource-bounded diagnostics, including all native leave-one-year-out refits and top-five *additive* control refits, were not performed; their absence is recorded rather than replaced by invented tests.

### 8.3 Temporal overlap and state composition

- The high/low RV mixture changed markedly between **2016–2019, 2020, and 2021**. A 2020 low-volatility group had only **21 dates** in the full-cohort categorization (and **15 under one past-origin classification**); basic scientific high-versus-low comparison **ABSTAIN**.
- 11 2020 numeric states exceeded the earlier DEV2020 training range. Predicting there may be feasible, but an extrapolated model output is **not local raw-data shape identification**.
- Conditional same-state environmental comparisons were performed only where ≥50 dates / 20 distinct five-session groups per required cell; sparse cell failures remain ABSTAIN rather than hypothetical smooth imputation. Coarse-state reweighting is labeled a **different standardized estimand**.
- 2020 crisis session gaps may be disproportionately consequential, so no pandemic-specific mechanism or temporal stability certification follows.

### 8.4 Novel state-dependent EBM theory — status

C3 included an applicability ledger and practical diagnostics inspired by the project's state-dependent EBM theorem program: query-specific support, raw-versus-fitted whole-response contrasts, discretization/coarsening, model capacity versus scientific fidelity, state-composition differences, learner/seed/stress behavior, dependence-aware fixed-loss comparisons and abstention.

**What is not proved or instantiated for default native InterpretML on SPY dates:** exact finite-Gaussian selection pivots, calibrated simultaneous raw pointwise profile confidence events, closed-form selected-learner population coverage, idealized greedy path/near-stability certificates, exact affine inverse/coarsening preservation, or transport of the original restricted-estimator theorems without verifying their assumptions. Fixed date-block intervals and algorithmic seed spread do **not** create these guarantees.

Appropriate methodological claim: **the experiment operationalized support-aware and scientific-fidelity diagnostics, documented practical limitations of native EBMs, and identified specific assumptions blocking direct application of certain new theoretical results**. It did **not** prove a new financial-market theorem or a generally valid EBM shape confidence band.

---

## 9. Claim register — what we can and cannot say

| Potential scientific claim | Closure status | Permitted interpretation |
|---|---|---|
| Correctly constructed SPY full-day normalized RV allocation and predecessor Z0 | **IMPLEMENTATION SUPPORTED** | Within the audited source/sample and verified conventions |
| U-shaped average intraday variance-allocation profile with sharp time bins | **DESCRIPTIVELY OBSERVED** | A known type of financial time-of-day pattern, not original discovery |
| High preceding-day RV associated with a larger 15:00–16:00 share in 2016–2021 | **EXPLORATORY DEVELOPMENTAL ASSOCIATION** | +2.005 pp raw H–L; conditional intervals/reference p-values as qualified |
| Reliable population effect greater than 2 pp | **NOT CERTIFIED** | Interval lower bound below 2 pp; no independent C validation |
| Nonzero fitted EBM `k×Z0` and `k×S0` structure | **MODEL-OUTPUT OBSERVED** | Visible fitted terms and whole-response contrasts, not population interaction theorem |
| Extra EBM full-profile predictive gain over M0 or additive EBMs | **NOT ESTABLISHED** | Both M5/M6 worse than M0 in pooled development MSE |
| Better EBM fidelity to raw H1 than linear/GAM/normalized alternatives | **NOT ESTABLISHED** | EBM H1 attenuated; P-OLS-Z and M8 closer to observed H1 |
| Population shape stationarity, drift or near-invariance | **INCONCLUSIVE** | Non-overlap, instability, and unc ertainty validity unresolved |
| Three-state discretization retains all useful continuous state information | **NOT ESTABLISHED** | Only finite-model empirical comparison conducted |
| Exact source-paper replication of E-mini / open-VIX tests | **NOT DONE** | Different asset, state, estimator and sample period |
| Additional-state `Zret`, `Zchg`, `Zvol`, VIX model contributions | **NOT TESTED IN C4** | No result is positive or negative |
| Independent held-out prediction for full-C 2022–2026 | **NOT TESTED** | Later complete-session sources and final authorization withheld |
| Trading alpha, strategy profits or risk-adjusted net returns | **NOT STUDIED** | A forecast of variance allocation is not a trading strategy |

*(Editorial precision: any inference conditional on previously viewed dates does not become confirmatory merely because a p-value was adjusted over the six registered models/tests.)*

---

## 10. Where the figures and underlying tables live

The experimental artifacts below are in **the user's local Codex repository**, not embedded as new copies in this closeout report. File references below are intended for navigating the research archive after moving this report into `reports/C/` or a similarly appropriate location. This closeout does not alter Git history, repository files or remote data.

### 10.1 Primary source reports

- **Original scientific design:** `docs/specs/C/experiment_C_revised_complete_research_design_v1_1.md`, original v1.0 source spec.
- **P0:** `reports/C/C_preliminary_RV_profile_results.md` and `reports/C/C_preliminary_RV_profile_visual_gallery.md`; machine outputs in `artifacts/C/preliminary_RV_profile_v1_1/`.
- **C-spec supplementary:** `artifacts/C/C_spec_window_preliminary_v1/` with seven figures and an independent report/galleries in `reports/C/`.
- **C1R:** the uploaded **C1R source, state and protocol readiness report**, plus `config/C_full_protocol_v1_1.yaml` draft, C1R QA registries and `data/derived/C/c_development_states_v1_1.parquet`.
- **C2R:** the uploaded **C2R direct curves, OLS and state-dependent splines report** and its saved `model_scores.csv`, `scalar_ols_models_and_hac.csv`, `profile_diagnostics.csv`, `paired_loss_tests.csv`, `support_and_environment.csv`, calibration and influence registries; C2R figures 01–14.
- **C3:** the uploaded **C3 one-state EBM scientific results report**; `C3_one_state_EBM_theory_applicability.md`; `C3_one_state_EBM_figures_for_human_review.md` / the 10-page PDF; and numeric artifacts under `artifacts/C/C3_one_state_ebm_v1_1/` (including `profile_predictive_metrics.csv`, `window_prediction_metrics.csv`, `paired_loss_tests.csv`, `model_shapes_and_scientific_contrasts.csv`, `state_support_and_masks.csv`, `native_terms_and_bins.json`, stability and source/hash registers).

**Source file warning:** Some copied narrative filenames may differ from the exact names in the live repository. The machine registries, Git tree and the final Codex coding-session reports are authoritative for actual local paths; do not invent a reconstructed path to a table if it is not found.

### 10.2 Suggested figure-reading map for the future teaching sessions

The following is **a reading order**, not a demand to redo inference. Keep one experiment's scientific target and units on screen while interpreting.

**C P0 — first understand the raw data:**

1. `01_open_three_state_profiles.png` and `02_prev_three_state_profiles.png`: why the baseline U-shape is similar while small time differences arise; distinguish retrospective opening RV from prior-day RV.
2. `03_open_high_minus_low_pointwise.png`, `04_prev_high_minus_low_pointwise.png`: signed difference curves, pointwise block ribbon, multiple-bin selection caveat.
3. `05_open_window_share_summary.png`, `06_prev_window_share_summary.png`, and the C-spec closing-hour window figure: why different window durations yield different results and why 15:00–16:00 must stay the primary C target.
4. `09_open_nonoverlap_post1000.png`, `10_prev_nonoverlap_post1000.png`, plus outlier sensitivity: mechanical numerator overlap and post-opening denominator interpretation.

**C2R — next learn what regressions/splines are predicting:**

1. `01_direct_three_state_profiles.png` and `02_closing_share_scatter_and_state_OLS.png`: raw conditional profiles versus the **scalar** closing-hour mean/regression.
2. `03_OLS_estimates_and_interaction_tests.png`: which confidence bar or joint test corresponds to linear state effect, scalar slope moderation, or curvature.
3. `04_scalar_OLS_residual_and_QQ.png`, `05_scalar_OLS_residual_time_ACF_and_variance.png`, `06_influence_and_robustness.png`: tails, HAC caveats and sensitivity to calendar regimes.
4. `07_M0_M1_M2_profile_fit.png`, `08_state_dependent_profile_OLS.png`, `09_M4_continuous_state_heatmap.png`, `10_raw_vs_spline_scientific_fidelity.png`: the **full profile**, different `Z0` values, coarse-cell contrasts, and why smoothing can miss sharp bins.
5. `11_development_chronological_model_scorecard.png`, `12_environment_support_and_composition.png`, `13_normalization_residuals_and_last_bin.png`, `14_scalar_calibration_period_means_and_PACF.png`: head-to-head loss, interpretation/support, simplex constraints, calibration and drift.

**C3 — finally interpret native EBMs:** The **17-figure human gallery PDF** is ordered to build from raw profiles to model curves, to the learned interaction, then scientific fidelity and loss: figures **01–02** baselines/time resolution, **03–07** additive/interacting families and matched three-state curves, **08–09** continuous total-response surface and numeric state slices, **10–11** contrasts and fidelity, **12** developmental errors, **13–15** support/residuals/stability, **16** software components and bins, **17** normalization/coarsening/adequacy. In particular, examine **Figures 10–12 and 15–17** before assigning a scientific meaning to an attractive M5/M6 plot.

### 10.3 Minimum table dictionary (for interpreting A/B/C later)

| Column/quantity | Meaning and common error |
|---|---|
| `Q[d,k]` | Fraction of **one day's** variance in time bin `k`; not return or annualized volatility |
| `R[d]` | Sum of squared within-day minute log returns; state `Z0[d]` uses **prior** day `R`, never current `R` |
| `CLOSE_C` / closing-share level | Fractions such as `0.17` = **17%** of daily RV, not a 17% stock return |
| `H1_pp` / `high−low` | Percentage-point difference between state-group allocation fractions: 2.005 pp = fractional difference 0.02005 |
| `profile_MSE` | Mean over **78 within-day bins** and then days of squared fractional allocation errors; smaller is better |
| `CLOSE_C_RMSE_pp` | Root mean-square error in **percentage points of daily RV share**, not basis points of SPY price return |
| `loss difference first−baseline` | Negative favors the **first** named model; compare on exactly the same dates |
| `HAC5/10/20` | Lag-window sensitivity to temporal dependence under asymptotic assumptions, **not** arbitrary guaranteed protection |
| `block5/10/20` interval | Whole-date block resampling; report whether labels/fits/selection were refitted or fixed |
| `TV` | 0.5×L1 **between valid normalized probability profiles**; native non-closed EBMs can only use raw half-L1 |
| `S0` | Three categories of lagged Z0; historical P0 ranks are not the same as origin-training cutpoints |
| `D(k;k0,...)` | Anchored across-state **whole-response** contrast; not raw centering-sensitive native interaction score |
| `ABSTAIN_SUPPORT` | Insufficient distinct dates in a required comparison cell; finite fitted values do not override this |
| `MSE_profile versus_M0_percent` | **Positive = worse** if defined as (model MSE/M0 MSE−1)×100 |
| `NORM_M5/M6` | Postprocessed normalized predictions; different maps from native M5/M6 |
| `D_FULL` vs `DEV_2020/DEV_2021` | Same-period fitted/scientific description versus **past-only developmental** out-of-time forecasts, **neither independent C final evaluation** |

---

## 11. Why close now, and when to reopen

**Reasons for closure now:** (a) the planned one-state OLS→spline→complete EBM ladder has been executed and audited; (b) an authentic descriptive state-conditional mean difference has been characterized without establishing added nonlinear EBM benefits; (c) full-profile developmental errors do not improve with M5/M6; (d) heavy tails, shifting state distributions and sparse crisis cells make expanding parameter searches unattractive; (e) future validation/source acquisition plus multi-state work would consume resources while several other independent EBM experiments remain available.

**Reasons *not* to claim final negative proof:** even a good forecast comparison on a viewed training-era backcheck is not a rigorous statement about unseen dates; nonlinear state effects could change by market period or asset; continuous RV, VIX, other predictors or a compositional learner may behave differently; the strict eligibility rule omits crucial crisis dates; no model-independent near-stability proof was obtained.

**Conditions for an optional later reopening** (only if specifically approved): new truly independent dates/assets or a separately authorized and documented C evaluation release; a tightly declared incremental prior-return/volume state hypothesis; a justified calibrated raw-shape event for specialized theorem application; a credible evidence-based model need beyond the current M0/OLS/M8 baselines; or a proposed historical-source replication with genuinely comparable data and estimator. A reopening would require a **new frozen protocol version** and clearly identified previously inspected versus genuinely independent samples. Never rebrand the old 2020–2021 development backchecks as new test evidence.

At closeout, **no new C data acquisition, C4, C5, C6, 60/20/20 evaluation release, model fitting, source repair or future scheduled task is authorized** by this report.

---

## 12. Reproducibility and CV/report wording

**Reproducibility status from returned Codex reports:** source/config/code/fit hashes and native graph audits recorded; 2016–2021 source identity verified; matched day-level scores and plotted means independently reconciled; no duplicate full-minute dataset; no hidden post-2021 C scientific outcome access. The closeout report itself does not rerun or independently verify the local repository computations—its judgments are grounded in the uploaded result reports and visual gallery. Keep the original detailed Codex session reports, machine outputs, source IDs and settings as authoritative evidence.

**Accurate CV-ready description (optional, use only if project completed work is still accurately represented in the eventual application):**

> Developed and audited a reproducible, state-conditioned intraday volatility-profile modeling study on SPY one-minute data, comparing linear and varying-coefficient regressions, splines/GAMs, additive and interacting Explainable Boosting Machines, and normalized compositional models. Implemented support-aware functional contrasts, residual/dependence/influence diagnostics, chronological backchecks, and scientific-fidelity audits; found no demonstrated EBM advantage over strong simple benchmarks in the explored development sample.

**Do not claim:** validated trading alpha, successful exact 2019 futures/VIX replication, independent held-out generalization, a confirmed >2-pp population effect, novel model-specific theoretical confidence-band validity, or proof that volatility-state shapes are invariant.

---

## 13. Suggested next learning/interpretation phase in this chat

The user plans to study **Experiment A, Experiment B's broader empirical exploration, and Experiment C**. Keep the projects scientifically separate and use this report as **the Experiment C reference**, not an imagined result for A or B. For each project, follow the same pedagogy:

1. **Define the data, prediction/scientific target, predictor, state, and information time**; identify units and dates.
2. **Read raw three-state plots before fitted curves**; clarify what each line represents and how support/counts change the interpretation.
3. **Read a model table**: fitted function, baseline, scalar-vs-profile objective, train/validation distinction, error metric direction and magnitude.
4. **Read diagnostics**: residual QQ, autocorrelation, outliers, state overlap, chronology, feature/sample dependence.
5. **Interpret a scientific claim**: raw conditional association versus model output versus supported population inference versus independent prediction; determine what is supported, inconclusive, abstained, or not run.

**Final Experiment C archive verdict:** `CLOSED — DEVELOPMENT COMPLETE; SOURCE-INSPIRED PRIOR-RV ALLOCATION ASSOCIATION OBSERVED; NO ESTABLISHED INCREMENTAL NONLINEAR EBM ADVANTAGE; FULL C VALIDATION/SELECTED-MODEL SCIENTIFIC CERTIFICATION DEFERRED`.
