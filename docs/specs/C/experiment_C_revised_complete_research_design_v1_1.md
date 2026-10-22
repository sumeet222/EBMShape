# Experiment C — State-Dependent Intraday Volatility-Profile Shapes
## Revised complete scientific design and staged execution specification | **v1.1 — post-P0 review**

**Design date:** 17 October 2026. **Status:** Proposed authoritative update for the NEXT implementation stages; retains the original v1.0 scientific program, explicitly incorporates completed P0/C-spec feasibility evidence, and documents all changes. **Not** a Codex implementation command, fitted-model result, confirmation, or authorization to inspect Experiment B's reserved 2024–2026 outcomes. The companion `experiment_C_revised_transition_and_next_stage_handoff_v1_1.md` tells the implementation chat how to operationalize this design one stage at a time.

### Authority, inputs, and precedence

This design was prepared using the **three supplied original documents**, not by replacing them with a generic experiment: (i) `experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md` (uploaded here as `experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1(1).md`), (ii) `experiment_C_transition_prompt_for_experiment_B_chat_v1.md`, and (iii) `experiment_C_P0_supplied_handoff_v1_1.md`, plus the actual C P0 numerical report, C-spec supplemental report and 20 supplied figure/contact-sheet images. **Original v1.0 remains the detailed literature/methodological reference.** This v1.1 controls only where it explicitly clarifies/updates choices; never read P0's retrospective workflow as automatically superseding full-C v1.0. Repository code/data/config, sample sizes, and any additional scientific assumptions must be inspected by Codex, not inferred from this document.

If a scientific choice below is materially different from v1.0, the change is labeled **v1.1 decision** and must be versioned in the executed config before fitting. Previously observed 2016–2021 evidence **cannot be relabeled blind validation** by writing this new specification. Changes after outcome review must be logged and treated as exploratory on previously inspected dates.

---

## 1. Executive decision and scientific scope

**GO to staged Experiment C implementation, initially with the accessible preceding-session realized-variance (`Z0`) state and the pre-existing closing-hour question.** This is **GO to further scientific testing**, not `H1 confirmed`, `material positive`, `EBM effective`, `forecasting alpha`, or `R1 replicated`. The P0 evidence warrants study, but the full 78-component state-dependent shape program and original RQ1–RQ5 remain in scope.

**Central objective (unchanged):** Can interpretable state-dependent nonlinear models recover established intraday volatility shapes, characterize their continuous transitions, and explain residual shape variation through multiple interacting market states? The research contribution is the location, magnitude, uncertainty, stability and scientific fidelity of **changes in the conditional functional shape**. Forecasting utility is secondary, and trading profitability is not required or inferred.

**Scientific decisions retained:** SPY; 390-minute standard RTH sessions; 78 nonoverlapping five-minute realized-variance bins; per-day normalized allocation vector `Q`; previous regular-session realized variance as principal ex-ante state; the SAME underlying state represented numerically and via train-defined terciles; time-of-day as a focal variable; compare direct empirical curves, time-only smoothers, varying GAM/splines, EBMs and structurally normalized profile models; additional lagged states and environmental scientific fidelity; day-level dependence; no forced novelty/significance; no duplicate raw data.

**Two separate research modes:** `D` = source-inspired descriptive/retrospective scientific shape comparison (permitted ex-post state labels only if clearly tagged); `F` = genuinely ex-ante state-informed forecasting of the NEXT complete day's profile using information known before that session. A 10:00 reforecast is a **separate remaining-day outcome branch**, requiring its own frozen scope, not an at-open full-day forecast.

**Stage-level priority:** In the next minimal statistical stage, investigate `Z0 → 15:00–16:00` allocation with direct estimates and robust simple models; do **not** automatically run the full M0–M10 architecture. If support or stability fails, document failure and stop expansion. If evidence remains credible, implement the full bounded continuous/discrete EBM shape ladder and then the added-state questions without redesigning the target.

---

## 2. Actual preliminary evidence — frozen descriptive record, not new testing

### 2.1 What was executed

- P0 source: **Alpaca SIP SPY one-minute split-adjusted bars**, UTC timestamp = minute start, XNYS regular full sessions in ET; 2016-01-05 through 2021-12-31. First log return `log(C_09:30 / O_09:30)` and 389 subsequent minute close-to-close returns. Exactly 78 five-minute bins per retained day, no overnight return, no filled missing minutes. Complete source supplement retained only nonduplicated minute keys and reused Experiment B references; **not** a full independent TAQ data collection.
- **OPEN state (same-day realized 09:30–10:00 variance):** 1,491 complete days, 497/497/497 retrospective terciles. **PREV state:** 1,472 dates with an immediately preceding **scheduled** complete full session, low/mid/high 491/491/490. PREV does *not* skip over an intervening early-close/incomplete session. Overlap cohort 1,472 dates.
- Main-day exclusions: **12 scheduled early closes**, **7 incomplete ordinary days** (2016-02-02, 2019-08-12, 2020-03-09, 2020-03-12, 2020-03-16, 2020-03-18, 2021-05-05), with 100 missing minute bars in those seven sessions. Four excluded 2020 crisis dates are a serious selection limitation: interpret empirical conclusions for **eligible complete sessions**, not every turbulent market day.
- Additional P0 source acquisition was already authorized and completed: approximately **119,675,359 bytes of response-body transfer** and a **10,318,012-byte** C-only compressed supplemental cache, stored separately from B's immutable source; P0 QA and numerical reconciliation passed. The previous authorization of at most 1 GB was for **P0**; it is **not** a standing authorization for all future full-C data acquisition.
- P0 terciles/bootstraps were **retrospective fixed-label descriptions on the 2016–2021 cohort**; date-block percentile bands at 5 and 10 scheduled-session blocks, 1,000 draws. These are exploratory conditional-on-label uncertainty diagnostics, not global, familywise, post-selection, or stationarity-certified intervals. All subsequent stages must keep their own train-only cutoffs and separately frozen inference design.

### 2.2 Numerical results, high minus low RV (fraction of **whole-day realized variance**, reported below as percentage points)

| Branch / window | Observed H−L (pp) | Exploratory 95% block-5 interval (pp) | Block-10 interval (pp) | Interpretation |
|---|---:|---:|---:|---|
| **PREV, full-C close 15:00–16:00** | **+2.005** | **[+0.927, +3.080]** | **[+0.839, +3.206]** | **Strongest preliminary lead**, ex-ante state, positive in reported robustness |
| PREV, P0 close 15:30–16:00 | +0.594 | [−0.247, +1.423] | [−0.343, +1.520] | Uncertain; the broad-hour effect is not simply the final 30 minutes |
| PREV, full-C midday 11:30–13:30 | +0.349 | [−0.664, +1.357] | [−0.742, +1.435] | Weak |
| PREV, opening 09:30–10:00 | −2.205 | [−3.193, −1.224] | [−3.169, −1.094] | Prior-high-RV group allocates less to the open; compositional redistribution, not causal |
| OPEN, full-C close 15:00–16:00 | −0.415 | [−1.607, +0.795] | [−1.731, +0.963] | Weak, opening state retrospective |
| OPEN, P0 close 15:30–16:00 | −1.196 | [−2.131, −0.294] | [−2.228, −0.102] | Separate short-window descriptive result; not source-style at-open prediction |
| OPEN, P0 close post-10:00-renormalized | −1.160 | [−2.188, −0.113] | [−2.355, +0.053] | Less robust to block length |

The **derived** point contrast for `PREV, 15:00–15:30` is about **+1.411 pp** (= +2.005 − +0.594). This was recognized *after reviewing P0 and full-C windows*; it is therefore an **exploratory diagnostic with NO computed interval yet**. A valid interval needs a **joint date-level resampling or other matched covariance calculation**, not subtraction of CI endpoints and not a novel independent hypothesis. Do not promote this interval's sign by selecting a better-looking half-hour. The pre-existing **15:00–16:00** remains the main full-C window.

### 2.3 Robustness and visual interpretation

- PREV full-C closing-hour effect when **renormalizing only post-10:00** realized variance: **+1.737 pp**, block-10 interval **[+0.459, +3.068] pp**. Full-day removing the top 1% of highest-RV days: **+1.839 pp**; median-of-daily-shares H−L: **+2.416 pp**. Corresponding remaining-day robustness approximately +1.553/+2.197 pp. These preserve the direction; they are not new independent replications or high-dimensional profile inference.
- PREV 15:00–16:00 standardized effect approximately **0.257 pooled daily SD** (post-10:00 version ~0.200). Meaningful for prioritization but modest versus daily noise.
- PREV and OPEN low/mid/high profile overlays show the same broad **U-shaped** intraday allocation; state curves are quite close, with a discernible PREV change in allocation from the opening toward ~15:00–15:55. **They do NOT show a radically different global functional geometry.** The last 5-minute bin is an important sensitivity target; apparent features near 14:00 can reflect scheduled announcement timing. Some pointwise ribbons straddle zero across most bins.
- Whole-profile post-opening TV point estimates: **OPEN 0.0361**, **PREV 0.0444**, compared with original 0.05 reporting tolerance. These are *point estimates*, not certified upper equivalence bounds. Neither `<0.05` nor failure to reject zero certifies profile invariance.
- All 2016–2021 samples were viewed during P0, and both P0 and full-C aggregated windows were examined on the **same records**. The supplementary C-spec review added no new dates. Neither is independent confirmatory validation. Missing crisis dates and time-varying conditional state frequencies could affect generalization.

### 2.4 Result-to-design decision register

| Decision | v1.1 resolution | Basis / caution |
|---|---|---|
| Principal accessible state | **Keep `Z0=log(R_{d-1})`** | Already v1.0 main state; promising PREV P0 evidence, ex-ante |
| Principal closing window | **KEEP 15:00–16:00** | Original full-C §2.1 source-anchored H1; do **not** replace with favorable 15:00–15:30 |
| Principal middle window | **KEEP 11:30–13:30** | Original C §2.1, notwithstanding narrower P0 definition |
| Opening window | 09:30–10:00 | Unchanged, source analogue for prior-return asymmetry |
| P0 windows | 12:00–13:00 midday and 15:30–16:00 close | **Secondary P0 compatibility views**, not full-C primary and not alternative primary tests |
| OPEN 09:30–10:00 RV state | Retain as **D-only retrospective** or separately approved after-10:00 remainder study | Overlaps the first six outcome bins; not a before-open state |
| PREV closing-hour H1 | **Promising lead for next stage**, NOT accepted significance/materiality | Band lower positive but <2 pp and no blind C holdout |
| H2 prior-return/early shape; H3 global TV; H4 added-state prediction; H5 environment drift | **Retain all** | P0 did not test these full research questions |
| VIX | Lagged close robustness if available; actual time-stamped open VIX optional | R1 used open VIX/E-mini; no same-day close masquerading as at-open |
| Full 78-bin representation | **Retain** | Window regression alone would fail C's primary functional objective |
| New market download | **Not automatically authorized beyond P0** | Full later periods need coverage/storage/budget review |

**Materiality conclusion:** Original closing-hour threshold **ε_L=0.02 (2 pp)** remains in force. P0 H−L point estimate ~2.005 pp and bootstrap lower bounds ~0.84–0.93 pp **do not** establish a material effect exceeding 2 pp. An exploratory interval excluding zero is a different and weaker statement than certified materiality or reliable predictive gain.

---

## 3. Frozen mathematical objects and genuine shape hypotheses

### 3.1 Within-session profile and observational unit

For date `d`, let the complete regular session comprise minute bars starting at `09:30,...,15:59 ET`. Form within-session one-minute log returns:

```
r[d,0] = log(C[d,09:30] / O[d,09:30]);
r[d,j] = log(C[d,j] / C[d,j-1]), j=1,...,389.
v[d,k] = sum_{j=5k}^{5k+4} r[d,j]^2, k=0,...,77.
R[d] = sum_{k=0}^{77} v[d,k].
Q[d,k] = v[d,k]/R[d], R[d]>0.
```

`Q[d,k]≥0`, and `sum_k Q[d,k]=1` to numerical tolerance `<1e-10`. Every eligible **day** (not each minute/bin) is one independent-*sampling-unit candidate*, but adjacent days may be dependent. This is a **compositional realized-variance proxy**, not latent spot volatility or a jump-robust integrated-volatility estimator. Keep exact bar-start conventions, no overnight increments, split-only price adjustment and no fake data; do not call Q an original-source statistic.

**Window indices in one place (0-based inclusive start, exclusive end):**

| Named target | ET window | k slice | Bin count | Scientific rank |
|---|---|---|---:|---|
| `OPEN30` | 09:30–10:00 | `Q[0:6]` | 6 | Original C H2; OPEN-state overlapping descriptive caveat |
| `MID_C` | **11:30–13:30** | **`Q[24:48]`** | **24** | Original full-C fixed middle |
| `CLOSE_C` | **15:00–16:00** | **`Q[66:78]`** | **12** | **Original full-C H1 primary** |
| `MID_P0` | 12:00–13:00 | `Q[30:42]` | 12 | P0 secondary compatibility |
| `CLOSE_P0` | 15:30–16:00 | `Q[72:78]` | 6 | P0 secondary compatibility |
| `PRE_CLOSE_DIAG` | 15:00–15:30 | `Q[66:72]` | 6 | **Post-P0 exploratory**, no inherited CI/confirmatory status |

Report fractions of **each day's total** `R[d]`; do not confuse `E[v/R]` with `E[v]/E[R]`, or compare different window durations as per-minute rates. The 78 Q components, and partial window shares, are dependent and not independent repeated responses.

### 3.2 States and interpretation

- **`Z0[d]=log(R[p(d)])`**, where `p(d)` is the **immediately preceding scheduled XNYS trading session** and has a complete admissible 390-minute profile. Require a positive variance; if the predecessor is early-close or incomplete, mark `NO_VALID_IMMEDIATE_PREDECESSOR` rather than skip backward to an older full day. `Z0` is known at today's open; choose a fixed numerical `log` floor only as a documented numerical guard, not to reorder positives. Train-defined terciles `S0` and numerical `Z0` arise from **the same RV source**. The P0 descriptive rank terciles cannot be used directly for F's validation/test.
- **`ZV`** = previous eligible session's published VIX *close*, with explicit calendar/timestamp and first-availability QA; secondary literature-proxy replacement, not automatically part of the principal model. **`Zopen`** = point-in-time VIX at/before 09:30 only if independently sourced/verified; source-style conditional quantiles in retrospective D, train-frozen in F. Cboe daily close is NOT opening VIX.
- **`Zret`** = previous full-session SPY close-to-close return sign, with consistent previous two relevant full-session anchors; additionally preserve return magnitude as secondary diagnostic without silently changing H2; distinguish previous full RTH-only return from total close-to-close.
- **`Zchg`** = `log(R[p(d)])−log(R[p(p(d))])` with **two consecutive valid immediately preceding scheduled sessions**; not contemporaneous same-day RV rise.
- **`Zvol`** = prior full-session share volume relative to the median over its **20 older eligible complete sessions** (full-C v1.0 uses `log((V_{d-1}+eps)/median(V_{d-21:d-2}+eps))`). Freeze the exact lookback and excluded/half-day behavior *before model fitting*. Training-only scale/median operations, chronology and split-adjusted volume units audited; no `Vsame` as F feature.
- **`Zfomc`** = announced FOMC decision-day flag from authentic dated historical calendar, optional diagnostic; known event schedule is not a causal model, and unscheduled emergency announcements are different. **`Zd=R[d]` / `Vsame`** = explicitly **D_ONLY**; forbidden as ex-ante predictors of Q[d].
- **`ZopenRV`** (P0 OPEN) = `sum_{k=0}^{5}v[d,k]` and its terciles, **RETROSPECTIVE_D_ONLY for full-day outcomes**. A future separate after-10:00 forecast may use it to predict **`Q_rem` with the remaining-day denominator**; do not contaminate primary at-open F-mode.

Prespecified source-style VIX-group sensitivity uses **[5%,25%]** vs **[75%,95%]** groups rather than mere terciles; excludes extreme tails for that comparison only. Original R1 may exclude FOMC days in the relevant figure. Those filters require exact source-method documentation and must not be conflated with the principal full-sample profile.

### 3.3 Conditional mean, contrasts, materiality

For fixed environment `e` and state configuration `z,w`, the scientific object is:

`m_e(k,z,w) = E[ Q_d(k) | Z0_d=z, W_d=w, environment=e, day eligible ]`.

For every supported conditional mean curve, `sum_k m_e(k,z,w)=1`. At continuous `z`, a pointwise scientific mean requires an appropriate regular conditional version and support/continuity/localization conditions. Software EBM values do not confer raw pointwise identification.

**Primary scientific contrasts**:

1. H1 directional **`G_C=E[CLOSE_C | S0=high]−E[CLOSE_C | S0=low]`**, with properly estimated train-frozen states for F. Distinguish direct retrospective 2016–2021 groups from evaluation-law high/low cohorts. Focus on `G_C>0` as source-inspired directional signature. Separately test `G_C>0.02` for *material* positive allocation only with a justified one-sided/simultaneous uncertainty lower bound.
2. H2 `G_O=E[OPEN30 | Zret<0]−E[OPEN30 | Zret≥0]` (prior-negative-return analogue of R2), and conditional versions adjusting for Z0 where support permits. This was **not** tested by P0.
3. H3 global state profile `TV(m_high,m_low)=0.5 sum_k |m_H(k)−m_L(k)|` and its uncertainty. A TV point estimate <0.05 does not establish near-stability.
4. `D(k;k0,zH,zL)=[m(k,zH)-m(k0,zH)]-[m(k,zL)-m(k0,zL)]`, with **k0 containing 12:00 ET** (0-based k=30). On compositional curves a state-only vertical shift is constrained; do not overinterpret a single EBM centered term. Evaluate all 78 k as an organized family, not 78 independent confirmations.
5. H4 incremental held-out whole-profile score of added lagged states over a strong `time×Z0`/smooth/compositional benchmark; H5 fixed-state residual across-period profile change after adding states, always on supported common state distribution. H4/H5 remain exploratory unless a prospective protocol and proper reserved confirmation are separately frozen.

**Keep v1.0 tolerances:** `ε_close60=0.02`, `ε_open30=0.02`, `ε_TV=0.05`, `ε_environment_TV=0.05`. These are effect-size references, **not** implicit p-values, and have no guaranteed detectability. Positive materiality requires a justified lower interval bound **above ε**, near-invariance requires the entire justified simultaneous confidence set to lie within ε, and otherwise status is `INCONCLUSIVE`. Distinguish predictive-loss economic/statistical materiality from scientific allocation materiality.

### 3.4 Compositional normalization, important scientific detail

All predictions describe a **78-dimensional probability-simplex vector** of realized-variance shares, not a scalar return. Unconstrained EBM predictions per bin may be negative or fail sum-to-one; report **raw** range and sum defects before any processing. If applying positive clipping plus renormalization, treat that as a **separate explicitly named postprocessed model** with a frozen fallback, not the same native EBM. A structurally normalized comparator (M8: softmax/logistic-normal/other explicitly defined, with train-only regularization) is required for a fair function-class comparison. No naive exponential back-transform of `log(Q+eps)` is allowed as if it were `E[Q]`.

---

## 4. Analysis populations, chronological splits, and information leakage

**Original v1.0 split rule remains:** after the **full-C** complete-session source QA, take chronologically ordered eligible full days and use **first 60% development-training / next 20% validation / final 20% designated C evaluation**, exact boundaries defined deterministically and frozen to machine-readable config. Use `floor(0.6N), floor(0.8N)` with an explicit convention for ties and the last remainder. Report source span, day counts and cutoff dates. A stage that only has 2016–2021 full-day bars **cannot pretend those are the full project's final splits**; P0's 1491/1472 are development-era cohorts, not C's confirmed full-horizon n. Any analysis requires full-period access/authorization, and eligible-date selection must use objective time/bar completeness before reading C outcomes for selection.

**Prior exposure ledger:** 2016–2021 P0 daily Q and both window sets are fully explored. Experiment B's earlier return-related work has looked at portions of 2022–2023 and otherwise stored raw source for later periods. Later C dates should be called **prospectively specified within C after this design freeze, not globally untouched historical data**. The 2024–2026 dates are **reserved under Experiment B's prior protocol**; do not inspect C outcomes derived from that period or call the segment sealed/unopened unless a specific release/authorization and firewall decision is recorded. Even after authorized C evaluation, disclosure about prior date exposure and financial dependence is mandatory.

**v1.1 procedural choice:** Stage the work so that ALL exploratory model selection, windows, state choices, bandwidth selection and support-grid tuning remain on **development-training** only. Validation is used for **predeclared tuning and model comparisons** with a documented fixed small selection path; if repeatedly inspected, label it developmental. Final evaluation of a strictly frozen **shortlist and tests** happens once on an authorized designated C-evaluation segment; otherwise leave evaluation status `DEFERRED`. Final test must not be consumed merely for plotting or choosing which time window is favorable. The original 60/20/20 split is not an instruction to automatically fetch or open future reserved bars.

**Temporal environments (predeclared descriptive calendar context):** 2016–2019; crisis/regime 2020; 2021; subsequent 2022–2023 and 2024–2026 only when data/permission allow. Do not treat small single-year state×state cells as identified; report abstention. Across-environment scientific contrasts fix the same `z,w` and matched support instead of comparing marginal curves with different mixture frequencies. Alternative contiguous-year groupings must be frozen before their outcomes are used; a specific pooled early-vs-late partition, if chosen, must be declared in the staged config before inference.

**Evaluation policies:** Train-only numerical scalers, tercile thresholds, model bin edges or standardized categories; no calendar peek; no using current-day R or future RV as a state; no random daily cross-validation; no 78× apparent sample inflation. Quarterly or walk-forward updating is OPTIONAL secondary F-mode only if defined and budgeted before fitting, with strict past-only state thresholds/labels and training refits; otherwise use fixed-date forecasts.

**Dataset caution:** P0 excluded four important 2020 March crisis days because bars were missing; never fill them to obtain flattering robustness. Report `eligible-complete-session population`, missing-date concentration by environment, and an objective optional source check before extrapolating conclusions to stress periods. If choosing to acquire second-source bars for these days, that is a **new source sensitivity** with provenance, conflicts and permission, not a replacement of the frozen P0 source.

---

## 5. Original RQ1–RQ5 and literature correspondence (preserved)

| Question | Proposed full-C inference / target | Main source comparator | Decision status after P0 |
|---|---|---|---|
| **RQ1** Source analogue: volatility state changes normalized periodicity, especially close hour | Direct H1 source-inspired close-hour; opening/midday/windows; risk of composition; lagged VIX close and optional actual opening VIX contrasted honestly | **Andersen, Thyrsgaard & Todorov (2019, JASA)** | PREV close-hour **promising exploratory** in SPY RV proxy; **source's VIX/futures estimator not replicated** |
| **RQ2** Map whole `m(k,z)` continuously; smooth vs local nonlinear and coarsened discrete representations | Continuous curve heatmap/supported slices/TV/D and band-to-point fidelity; compare GAM M4, EBMs M5/M6 and normalized M8 | Andersen et al. 2024 curves; 2025 stationarity | **Untested by actual fitted models** |
| **RQ3** Multiple predeclared lagged states and contribution beyond main state | Zret, Zchg, Zvol, limited FOMC and VIX; incremental profile loss and conditional response | **Tsai, Eom & Wang (2024)**; volume-driven intraday research | **Untested**; no claims of volume originality |
| **RQ4** Matched-state environmental stability/near-invariance and scientific fidelity | Matched calendar environments, support/coarsening/composition and direct/raw vs total fitted response | Andersen et al. (2025); state-dependent EBM theory | **Untested**, neither stable nor drift certified |
| **RQ5** Out-of-date ex-ante profile forecast quality | Correct 78-vector normalization, day-level score, strong time-only/GAM/compositional and domain comparators | **Clements & Preve (2026)**, possibly Martins et al. (2025/2026) | **Untested**, no trading claim |

**Source boundary:** R1 uses **E-mini S&P futures (2005–2015), actual VIX at the start of the trading day, a latent periodicity/spot volatility estimator and source-specific transform test**. P0 uses SPY 2016–2021 lagged or realized opening RV, minute-square proxies, complete-session allocation and ad-hoc tercile grouping. The observed positive `PREV × CLOSE_C` sign is a **qualitative source-inspired analogue**, not reproduction of R1's exact data, estimator, significance or source open-VIX grouping. R2 uses international indices, five-minute GARCH and jump-robust alternatives—not reproduced here. Intraday U shape and volume effects are pre-existing literature, not patent/priority claims.

**Preserve literature R1–R6 and URLs from original frozen C v1.0** rather than inventing a new prior-art claim. For each published comparator, record operational target differences and whether an implementation is `EXACT`, `ADAPTED`, `INFEASIBLE`, or `NOT_RUN`.

---

## 6. Complete small-to-rich model comparison ladder (retain M0–M10)

Scientific *functions* and model fidelity, not lowest training loss, are the primary objective. Each model is evaluated on the same **days** and the same frozen outcome Q/available information set. In flattened `(d,k)` training data each day contributes all its 78 rows and equal total weight; loss/statistical inference are aggregated at the **day** level. The 78 bin rows are NOT 78 independent samples.

| ID | Operational model / contrast | Role | Next-stage disposition |
|---|---|---|---|
| `M0` | Training unconditional 78-vector `mean_d Q[d,k]` | Essential fixed-state-blind baseline | **Run first** |
| `M1` | Train-frozen low/mid/high direct conditional 78-vector means + coherent date-block uncertainty | Direct raw scientific reference / R1 analogue | **Run first** |
| `M2` | Time-of-day-only smooth spline/kernel profile fitted on train; fixed modest df/bandwidth | Credible smooth U-shaped time pattern | **Run first** |
| `M3` | Additive time + state model `f(k)+g(z)` with **no k×z** | Negative control for *true shape interaction*; raw output may violate closure | Run core model stage |
| `M4` | Low-df varying-coefficient tensor smooth / GAM `f(k)+g(z)+h(k,z)` | Strong **smooth continuous shape** challenger | **Run before EBM** |
| `M5` | Native InterpretML EBM with explicit `k×Z0` pair, Z0 numerical | Principal nonlinear full-function comparison | Run only after M0–M4 sanity gate |
| `M6` | Native EBM with explicit `k×S0` pair, S0 train-frozen nominal low/mid/high | Discretization/coarsening of SAME `Z0` data | Same core EBM stage; match M5 budgets |
| `M7` | EBM with time×Z0 plus time×Zret/time×Zvol, optionally prescribed Zchg | Add-state explanation; no unrestricted 3-way synergy | Later only if supported and justified |
| `M8` | Constrained normalized 78-vector model, e.g. regularized softmax-of-time/state scores | Nonnegative/sum-to-one comparator; crucial compositional safeguard | **Run before any claim of EBM-specific advantage** |
| `M9` | Small explicitly predeclared **true** 3-way time×state×volume/sign tensor or supported stratified-GAM | Separately tests synergy beyond M7 pairwise | **Conditional optional gate**; abstain unless enough independent days/joint support |
| `M10` | Domain-specific time-indexed volatility regression / lagged volume benchmark matched to usable published method | Specialized competitor; distinguish target/estimator differences | Conditional on method/data availability, no false exact replication |

**Non-negotiable model formulas/term graphs:** M5 `k, Z0, (k,Z0)`; M6 `k, S0, (k,S0)`; M7 adds `(k,Zret)` and `(k,Zvol)` to `(k,Z0)` but *no native 3-way interaction*. If numeric Z0 is already included, don't silently swap to discretized S0 as a different measurement. Native software versions and binning must be pinned. EBM term tables, term centering, importance and bag variability are *software diagnostics*, not unique scientific effects or raw-population confidence intervals. All reported scientific fitted contrasts use **the entire prediction surface** at identical supported inputs.

**Bounded resource plan, to freeze in stage configs:** At the core EBM stage, allow **at most two predeclared parameter settings per M5/M6 family**, screen using *training-era* contiguous inner folds only; expand the chosen setting to **three seeds** for descriptive algorithmic stability. No automatic interaction search. One compact `M7` add-state family at a time, ≤2 settings and ≤3 seeds for at most one shortlisted configuration. M9 optional only on explicit support/go gate. Model-count and actual hyperparameters (max_bins, interactions bins, leaves, learning rate, rounds, bags, early stopping, smoothing, regularization, seeds) must be written to `protocol_C_v1_1.yaml` **before the relevant fitting stage** and cannot be optimized on final evaluation outcomes. Prefer fixed 30–60 minute stage run caps, monitor RAM/disk, record fitted-model hash/seed/score. Complexity controls are operational planning defaults—not assertions these are the source's exact specification or all InterpretML API defaults. Do not create a 562-fit analogue of Experiment B without substantial independent scientific justification.

**What success requires:** If M5 beats M3 but does not exceed M4/M8, do not claim EBM-specific superiority. If predictive loss improves but direct supported shapes disagree with fitted surfaces, report a scientific-fidelity warning. If M5/M6 curves look almost identical and supported differences are tiny, that is a valid negative finding. Keep modest complexity under the small per-day sample even though flattening makes n×78 rows.

---

## 7. Scientific inference, multiplicity, support, and proof applicability

### 7.1 The actual uncertainty unit and family

The observational cluster is the **full session/date**, with all 78 Q bins coupled by `sum Q=1` and serial dependence between days. Predeclare joint date/contiguous scheduled-date block resampling, block lengths **5, 10, 20** for major science sensitivity, seed and B≥1,000 for descriptive methods when affordable. The P0 5/10 fixed-label bootstrap is already computed; do not claim repeating it on the same records yields new confirmation. A bootstrap on held-out fixed forecasts tests a **different object** from a bootstrap that refits the entire selected learner; clearly separate these routes. Do not interpret EBM bag-SD as a population CI or 78 marginal ribbons as a simultaneous global test. For dependent/heteroskedastic processes, state and evaluate plausible moment, stationarity/mixing/FCLT or finite-dependence assumptions; absent proof, call intervals **conditional/descriptive sensitivity**.

**Primary v1.0 hypotheses, not cherry-picked:** H1 close hour (direction and separately >2pp); H2 early allocation after prior negative return; H3 global TV; H4 held-out incremental multi-state profile loss; H5 fixed-state environmental residual TV. For any *confirmatory* p-values/intervals, freeze the finite relevant family and apply Holm/simultaneous max-statistic/block approach only with justified sampling assumptions; use interval thresholds for meaningful gains. H4/H5 exploratory if no independent test reserve/sufficient support. P0-derived 15:00–15:30 contrast is *secondary newly observed*, and wider/narrower window sensitivity should not enter the same family later as an unreported search. No 78 separately unadjusted claims.

### 7.2 Support/estimands and date regimes

Support decisions require **counts of actual distinct dates**, not 78× pseudo-replicates. Provisional operational gates (not theorems): display ≥30 dates and ≥10 five-session blocks per state×environment cell; basic scientific comparison ≥50 dates and ≥20 distinct five-session blocks per required group; stronger ≥100/30. These gates must be specified before inspecting model-output surfaces, and for 3-way joint cells may trigger `ABSTAIN` rather than smoothing them into invented identification. For continuous `Z0`, show local joint-support in the numerical state and time rather than assuming each exact point is estimable merely because there are many time rows. Predeclare an interpretable state grid using *training-only* 10/25/50/75/90% quantiles, matching group support; automatically mask unsupported cells. For environment comparisons require common support and quantify state-frequency changes and weight alignment; standardization to a declared reference state distribution changes the estimand and must be labeled.

### 7.3 Scientific fidelity vs prediction and model dependence

- Show **direct raw conditional profile means** and uncertainty on the same supported coarse cells as M4/M5/M6/M8 predictions. Distinguish cell-averaged targets from continuous-state point queries; localization bias may persist.
- Compare whole-model `D_F`/TV/window contrasts to empirical coarse-cell estimates on **the same dates, state cuts and covariate/partner distributions**. A visually smooth surface may be unsupported; a low whole-vector prediction loss may not preserve a rare target-specific shape contrast.
- Check stability across seed changes, outlier deletions, 2020 crisis exclusions, predeclared environments, interaction-graph ablation, normalization transformation and state discretization. Never relabel sensitivity-specific positive results as the primary fit.
- Audit projection/representation effects: `Q` raw population mean vs actual empirical bin mean vs proper model class vs fitted native EBM. For the native learner, estimate practical fidelity/descriptive uncertainty only where support permits; **no broad raw pointwise certified bands without an appropriate calibrated joint raw mean event**.

### 7.4 Crosswalk to the project's novel state-dependent EBM theory

Use the actual mathematical assumptions in the project's Tasks **10B, 11, 12, 15–25**, along with the consolidation theorem/assumption crosswalks, to classify EACH scientific method: `EXACT_SCOPE_INSTANTIATION`, `CONDITIONAL_STANDARD_INFERENCE`, `ALGEBRAIC_IDENTITY_ONLY`, `ADAPTED_DESCRIPTIVE`, `BLOCKED_ASSUMPTIONS`, `NOT_APPLICABLE`, or `DEFERRED`. The Experiment B Stage2C audit established that native InterpretML in a dependent heavy-tailed sample **does not automatically instantiate** the idealized finite-tree greedy/path proofs, exact conditional Gaussian selection pivots, IID bounded-Hoeffding coarsening bounds or native pointwise Q confidence events. However, some **current-output** algebraic fidelity bounds are algorithm-independent **once a genuinely valid matched simultaneous raw event exists**. Do not call the entire theory inapplicable just because the package differs, nor claim an event without establishing it. Keep paper/theorem novelty and empirical application separate; record original source lines/assumptions, exact data law, missing hypotheses, computation, and permissible claim.

---

## 8. Evaluation metrics and forecast interpretation

### 8.1 Scientific metrics (primary)

`G_C` and other predeclared allocation contrasts in percentage points; 78-vector TV and per-bin H−L curve; profile entropy/concentration, center-of-variance time, supported peak/close share and shape contrasts; close-hour and open-hour effect-size vs daily within-group SD; pointwise vs simultaneous interval status; scientifically supported state transition and curvature relative to smooth M4; same-state common-support across-period TV and state-mixture decomposition; native-fit-vs-direct discrepancy and unsupported/ABSTAIN proportion; continuous-vs-tercile resolution loss descriptive and (only if valid assumptions) inferential.

**Shape recovery is not equivalent to pure-vertical level differences or a higher raw daily RV**. A `Z0`-based state predicts future *allocation*, not necessarily the day's total integrated variance. A post-10:00 denominator sensitivity changes the response target and should be named separately. Be cautious when the same normalization can redistribute shares algebraically.

### 8.2 Predictive metrics (secondary F-mode)

For each evaluation date d, obtain a **78-vector** from model trained without d's outcomes. Report day-level:

- `MSE_profile = (1/78) Σ_k (Q[d,k]−Qhat[d,k])²` and its daily average; `MAE_profile=(1/78)Σ|...|`.
- `TV_prediction = 0.5 Σ_k |Q[d,k]−Qhat[d,k]|` **only for valid normalized profiles** (else labeled raw `L1/2`, not TV distance); optionally proper bounded compositional scores for M8.
- RMSE/MAE for `CLOSE_C`, `OPEN30`, `MID_C` daily shares, with meaningful effect sizes in **percentage points**. Don't train a scalar close-share-only EBM and claim recovery of an entire curve.
- Normalization defect: negative component count/magnitude, total sum error and fraction requiring fallback. Raw and postprocessed scores **separate**.
- Paired day-wise loss improvement versus M0, M2, M4, M8 and best legitimate source/domain benchmark on **exact same eligible dates**; use date-block uncertainty and declared multiplicity. Do not report one favorable metric alone or rank D and F information sets as though identical.

Simple extra closing-hour predictive utility is *secondary to* full-function characterization; even a good Q forecaster does not imply gross/net trading profit or usable intraday order execution.

---

## 9. Staged next implementation, decisions, and explicit work ceilings

**Stage C0/P0 STATUS: COMPLETED WITH QUALIFICATIONS** — P0 source verification, partial C-only minute supplement, canonical 2016–2021 `day × 78` curves and direct OPEN/PREV visualization, interval checks, C-spec supplemental window sensitivity. **Reuse, do not redo** the verified data and source QA, except small alignment/hashing checks. C0 in original transition prompt was written BEFORE P0; a fresh empty C0 Codex run is obsolete.

| Stage | What Codex actually does | Primary artifact(s) | Gate |
|---|---|---|---|
| **C1R — consolidated source, long-horizon feasibility & frozen split** | Read P0 cache/method/QA, root rules, source manifests; inventory complete-day coverage for full C, prior states and VIX/FOMC access, additional bytes/cost; compute *metadata-only* objective eligibility and prospective 60/20/20 split boundaries when feasible; source/period/permission ledger; no model fitting | `reports/C/C1R_protocol_and_coverage.md`, `config/C_full_protocol_v1_1.yaml` draft, source/split manifest | STOP if defining evaluation demands unauthorized reserved period or costly download; user approval on source/test release |
| **C2R — direct scientific profiling & simple models** | Reuse Q, independently check results/construct full C windows; H1/H2/H3 direct estimator; add Zret/Zchg optionally Zvol once historical source supports; raw open/mid/close/78 profile and direct continuous state smooth/kernel, time-only M0–M2, low-df GAM M4; environment/outlier/last-bin and sample-support analysis; report P0 observed dates as development | `reports/C/C2R_scientific_direct_and_GAM.md`, figs and compact tables | Continue only if method QA/support is sound, irrespective of significance; stop expansion if no credible shape or fit/coverage |
| **C3 — one-state models** | Freeze tiny train-only M3/M4/M5/M6/M8 ladder with 2 bounded configs/3 seeds maximum for EBMs; exact same days/grid; complete normalized predictions, native graph, supported continuous/discrete state plots, direct fidelity, held-out developmental validation | `C3_EBM_and_composition.md`, model registry/plot gallery | Do not infer EBM advantage without stronger GAM/M8 and direct curves; no automatic test peeking |
| **C4 — added lagged states** | Evaluate `Zret`, `Zchg`, `Zvol` one at a time; limited M7 combined pairwise; conditional M9 if support; later separately optional lagged VIX and FOMC/calendar; M10 if feasible | `C4_incremental_states.md` | If simple controls dominate or cells sparse, stop at negative result |
| **C5 — scientific inference/fidelity/environment** | Date-block dependence/selection sensitivity, simultaneous shape where assumptions permit, joint support, scientific-fidelity ledger, environment mixtures vs conditional shapes, 0.02/0.05 materiality decisions | `C5_inference_environment_and_theory.md` | Abstain if no calibrated raw event; don't claim certified invariance from point TV |
| **C6 — reserved evaluation and final writeup** | Execute frozen final comparison ONCE only after explicit reserved-data permission and full config freeze, verify all hashes and time stamps, final scientific + forecasting scores and a CV-accurate handback | `experiment_C_full_research_report.md`, README/figure atlas/source crosswalk | Without permission/independence: `EVALUATION_DEFERRED`, report development only |

**Next Codex task should be C1R (lightweight reuse/coverage/split design), not a redundant C0 nor the entire C1–C6 run.** C2R may follow C1R after data/authority gates and should be the earliest stage with new results. Do not issue a giant prompt fitting everything, auto-downloading VIX and opening the test.

### 9.1 Resource and data policy

Read full-session C P0 SPY minutes from the existing B references plus **one** C-only disjoint supplementary cache; the existing P0 record is ~10.3 MB and its previous source-body transfer ~119.7 MB. No new duplicate Parquet copies, repeated folds, duplicated raw tables or downloaded multi-asset universe. Compact derived `N×78` array and shared state/day table with references/hashes. Stop/ask before expanding source beyond currently authorized years or purchasing vendor access. Future data transfers require an explicit new cumulative GB ceiling and storage estimate; prior P0 1 GB is **not** a perpetual unused budget. No need to download massive options contract histories for VIX. Complete prior-day VIX close can be considered separately from official Cboe daily series once approved; true open VIX requires actual timestamps. Preserve all B and old P0 artifacts hash-unchanged.

Use a small test suite covering bar start semantics, DST/holidays/early closes, exactly 390 minute returns/78 bins, no first-return overnight, first/last bin, positive prices/zero denominators, predecessor full-session rule, train-only state boundaries, date level not bin-level leakage, q closure and out-of-sample shape normalization. Unit tests, reproducibility script, fixed seed, environment lock and code/data/config hashes every stage. A failed core invariant => `INVALID_QA` and no scientific claims.

### 9.2 Decision authority

Codex may autonomously fix mundane engineering bugs; it must log every file and resource use in a dated `.md` coding-session report, run tests and report intermediate negatives. It **must not** change Q, the original full-C windows, H1 tolerances, ex-ante state meaning, reserved testing calendar, exact source-comparison claims, or predeclared models merely because P0 found a promising sign. Any scientific change is a new documented protocol version and rerun of affected results. Never make unapproved downloads, purchases, or expose API credentials.

---

## 10. Required scientific output and truthfulness checklist

Each report must show: actual asset/source/date counts, missing-day bars and year concentration, source-era match/difference; target convention/window indices; information-time state definitions; P0 observed exposure disclosure; direct vs fit and native component separation; support/ABSTAIN; window allocation pp, TV, intervals, multiplicity and materiality; whole-curve 78-bin visualization; matched environments & composition; baseline metrics and paired uncertainty; model graph/seed/parameter provenance; normalization violations; null/permutation scope if ever run; actual code/data/config/environment hashes, space usage and **which source data were not copied**; permitted and forbidden theorem claims; results status ledger `PROXY_SOURCE_SIGNATURE / INCONCLUSIVE / NOT_REPRODUCED`, `ADDITIVE_VS_INTERACTION_SUPPORTED / NOT_SUPPORTED`, `EBM_EXTRA_FIDELITY_SUPPORTED / NOT_SUPPORTED`, `ADDED_STATE_INCREMENT_SUPPORTED / NOT_SUPPORTED`, `MATERIAL / NEAR_STABLE / INCONCLUSIVE`, `FORECASTING_GAIN / NO_GAIN / NOT_TESTED`, plus explicit `SEALED_TEST_NOT_ACCESSED` or evidence of authorized release.

**Mandatory final writeup:** `experiment_C_full_research_report.md`, a human-first `C_scientific_figures_gallery.md`, a versioned theorem/applicability crosswalk, result machine registry, and dated Codex session reports. Include a CV-ready description of **actual work**, not hypothetical statistical successes; publication originality is not established by using EBMs to model a known volatility U-shape.

**Scientific failure is reportable:** If simple direct conditional means and M4/M8 explain the state effect but EBMs do not improve, the project still supports a careful empirical shape comparison and a technically honest negative EBM result. If later times/markets do not reproduce PREV closing-hour effect, retain both outcomes and report temporal instability. If no global changes appear beyond localized close-hour allocation, state exactly that rather than describing an entirely different state-dependent periodicity function.

---

## 11. Explicit v1.0 → v1.1 change log

| Area | Original | Revised action | Why / not allowed to infer |
|---|---|---|---|
| Implementation stage | C0 feasibility before any C data | **C0/P0 already done; next C1R then C2R** | No duplicated source/plots/fits |
| Evidence | No C data evaluated | Insert P0 n/source/contrasts and actual QA, tagged observed 2016–2021 | No retroactive confirmatory status |
| Source access | Prior full-source status unknown | One P0 Alpaca-based full-session supplement now exists; later years still need audit/approval | Prior 1 GB is not standing authorization |
| State ordering | `Z0` primary with other states later | Keep Z0 primary; **front-load** direct PREV close-hour supported H1 | Selective emphasis transparently disclosed |
| Windows | C spec MID 11:30–13:30, CLOSE 15:00–16:00 | **Unchanged as full-C primary**; P0 narrower windows secondary | Do not choose whichever gives a smaller p-value |
| Interpretation | Source-inspired shape | Mark PREV +2.005pp and OPEN differences as preliminary; missing-crisis sessions and near-U-shape similarity | No source replication or materiality certified |
| Exploratory window | Not a predeclared half-hour target | Label newly derived 15:00–15:30 +1.411pp **post-P0 exploratory** | Requires new joint interval; not a new independent confirmatory hypothesis |
| Final test | 60/20/20 after eligibility, prior B exposure disclosure | Preserve split; **do not open B reserved outcome segment without explicit release**, no pseudo-blind historical claim | Post-P0 selection confounds naive full-sample inference |
| EBM ladder | M0–M10 staged | **Preserved**, conditional lean resource gates, M4 and M8 fair benchmarks | No large run without signal/support |
| Theory | Adapt as applicable | Explicit correspondence/assumption ledger; no native EBM theorem shortcuts | Previous B theory audit found no exact native fit instantiation |
| Forecast objective | Secondary | Preserved, at-open information only; no automatic trading extension | Allocation does not imply returns or profit |

## 12. First action for the next implementation chat

Read original C v1.0 **in full** and these v1.1 documents, read repo `AGENTS.md`, P0 reports/config/QA and original B immutable source manifests, then author a **single focused `C1R` Codex prompt**. That prompt should *first* confirm existing source coverage/provenance and objectively derive eligible full-day calendars and prospective split boundaries without opening 2024–2026 C outcomes; audit access to lagged states; specify minimal new transfers and the exact approval gate. The design of M0–M10 is completed here; their actual fitting must wait for later controlled prompts. No need to repeat C0/P0 visual audit.
