# Experiment A — Turnover-Conditioned U.S. Stock Short-Term Reversal and Momentum
## Literature-grounded replication and nonlinear state-dependent EBM extension | Research specification v1.0

**Prepared:** 14 October 2026  
**Purpose:** Authoritative scientific specification for **Experiment A**, to be implemented and diagnosed in a **separate new chat**. That chat creates staged Codex prompts, reviews returned logs and numerical results, and sends a compact scientific conclusion to the EBM Theory/design thread. **This document is not a Codex implementation prompt, an executed experiment, or a claim of profitable trading.**  
**Scope:** **Experiment A only**: U.S. **monthly individual-stock** returns conditioned on **share turnover**. Experiment B, volatility-conditioned SPY intraday momentum, is a separate study with its own files and implementation chat. Do not mix their horizons, units, or states.  
**Research principle:** **Replicate established U.S. evidence, then extend the *same scientific relationship* to interpretable nonlinear, continuous/discrete-state, supported-shape and stability analyses.** The original authors already estimated an interaction and used conditional double sorts; merely adding an interaction or revealing nonlinear decile averages is *not* novel.

---

## 0. Authoritative decision register

| Item | Selected default | Binding boundary / allowed response to difficulty |
|---|---|---|
| Literature anchor | Medhat & Schmeling (2022), *Review of Financial Studies*; Yue, Li & Ruan (2023), *Pacific-Basin Finance Journal* | Fixed central works. Verify all source comparators from the exact version cited. |
| Scientific population | U.S. **NYSE/AMEX/NASDAQ ordinary common, nonfinancial stocks**, including historical exits/delistings when data permit | Full universe for faithful source replication. A present-day surviving 99-stock universe **is not equivalent**. |
| Observation | One **security-month** response, with **calendar month as primary common-shock unit** | Do not treat 99 × months as IID. Firm identity must survive ticker changes. |
| Dependent variable | Stock **next-month total simple return** with distributions and justified delisting treatment | **Frozen** monthly horizon; not the 8-future-30-minute-bar SAE target or a stock price level. |
| Return predictor | **Immediately preceding calendar month's total stock return** | **Frozen**; no 12−2-month substitution, no skip month, no overnight/intraday mixing in primary test. |
| Primary state | **Previous-month share turnover** = contemporaneous monthly share volume / shares outstanding, with matched units and corporate-action treatment | Frozen meaning. Historical volatility or market-wide VIX is **not** a substitute. |
| State representation | Same raw turnover underlying (i) continuous log-turnover input and (ii) predetermined **train-only** turnover categories | Paper's **return-first, conditional turnover deciles** are separately reproduced as a source benchmark; not silently identified with EBM groups. |
| Source benchmark I | Medhat–Schmeling **Table I**: value-weighted, return-first conditional 10×10 sorts using NYSE breakpoints; winner-minus-loser spreads | Do only with broad historical universe, NYSE labels and sufficiently populated cells. Otherwise tag `ADAPTED` or `NOT REPRODUCED`. |
| Source benchmark II | **Table IV**: monthly capitalization-weighted Fama–MacBeth WLS of returns on standardized lagged return, turnover and their product, without/with source controls | Historical explanatory benchmark. **Contemporaneous month-by-month fit is not an OOS trade forecast**. |
| Extended learners | Time-safe pooled/rolling linear interaction, varying-coefficient spline/GAM, additive EBM, prescribed return×turnover EBMs | Small predeclared search; no exploratory model zoo or unrestricted auto-interaction fishing. |
| Claims to test | Low-turnover reversal, high-turnover momentum, difference in their return shapes, EBM nonlinear increment, shape stability and economic value | Expected source-era signs, **not guaranteed** out of publication period or in biased/small subsamples. |
| Primary sealed modern test | **2023-01-01 through 2026-09-30**, inclusive, to extent verified data exist | **Frozen calendar**. Distinguish 2022 journal publication from accepted-manuscript/source data to 2018. |
| Weighting | Replicate source weights in Tables I/IV; pooled modeling **equal calendar-month contribution** with within-month market-cap weights | Equal-weight model is a separate sensitivity, not the official replica. |
| Research protocol | Commit `experiment_A_protocol_v1.yaml`, input/code/config hashes and output registries **before** test evaluation | Small engineering fixes logged; changing the universe, horizon, state or target needs approval/new protocol. |
| Storage | Reuse canonical files; at most one compact **monthly** modeling table, pointer-based raw data | Never clone historical daily/intraday Parquets per run/seed/fold. No uncontrolled 25-GB project growth. |

**Three evidence levels must remain separate:** **(R)** original-era reproduction using near-matched CRSP/Compustat; **(M)** contemporary U.S. test for 2023–2026; **(E)** exploratory/new nonlinear scientific structure. Success at one level does not imply success at the others.

### Important distinction from Experiment B

- **A:** across-stock, next-month relation of last month's stock return to next month's return, *moderated by that stock's own previous-month share turnover*.
- **B:** one SPY observation/day, opening-to-closing intraday momentum, *moderated by opening-period realized volatility*.
- Monthly data from the previous 99-stock 30-minute project may provide an **adapted prototype** if available, but its **2024–2026 time window is far too short** for credible monthly walk-forward research. Do not relabel it as a faithful reproduction of Experiment A.

---

## 1. Confirmed publications, precise claims and reproduction caveats

### 1.1 Main peer-reviewed study

**Medhat, Mamdouh, and Maik Schmeling (2022), “Short-term Momentum,” *The Review of Financial Studies*, 35(3), 1480–1526.** DOI: **10.1093/rfs/hhab055**.

- Published journal entry: <https://academic.oup.com/rfs/article-abstract/35/3/1480/6286969>
- Peer-reviewed author-accepted version (71-page repository PDF, not guaranteed byte-identical to journal version): <https://openaccess.city.ac.uk/id/eprint/31278/1/MS_short_term_mom_v27.pdf>
- Institution page with provenance: <https://openaccess.city.ac.uk/id/eprint/31278/>
- **Original PDF locations:** §2.1 (data/turnover, printed p.5–6); §2.2 & **Table I** (printed p.6–7); §2.6 & **Table IV** (printed p.13–15); §3.8 (volatility is *not* the same moderating variable); Appendix source-specific robustness.

**Main published U.S. sample:** monthly data **July 1963–December 2018**, NYSE/AMEX/NASDAQ securities appearing in CRSP and Compustat, **CRSP share codes 10/11**, excluding financial firms; available historical accounting variables lagged to mitigate lookahead.

**Table I source procedure:** at the month-end, form **conditional decile sorts using NYSE breakpoints**: (1) prior-month return deciles, then (2) prior-month **share turnover within each prior-return decile**. Form **value-weighted**, monthly rebalanced portfolios. A source "winner-minus-loser" row means the **prior-return-high portfolio minus the prior-return-low portfolio within the stated turnover category**; a negative sign denotes reversal, not a positive return earned by following winners.

**Key historical Table I source benchmarks** (monthly winner-minus-loser portfolio excess-return spreads, not individual-stock regression coefficients):

| Conditional turnover decile | Published spread | Source HAC t statistic | Interpretation |
|---|---:|---:|---|
| Lowest | **−1.41%/month** | **−7.13** | Previous winners underperform losers: reversal. |
| Highest | **+1.37%/month** | **+4.74** | Previous winners outperform losers: continuation. |

These averages are historical, before our implementation; **they are not performance targets for a modern EBM or guaranteed to reproduce in a new universe**. Table I uses the source's specific conditional portfolio definition, not an unconditional turnover percentile, an EBM double difference, or an individual alpha forecast.

**Table IV source regressions:** monthly **market-capitalization-weighted, Fama–MacBeth cross-sectional WLS**, predicting the current calendar month's stock return using **prior month's** return `r_{1,0}`, turnover `TO_{1,0}` and their product. The authors **trim predictors cross-sectionally at the 1st/99th percentiles, then standardize**, and use the product of those standardized variables. Their no-control all-stock interaction estimate has **t=5.45**; with source controls, **t=9.06**. The prior-return coefficient is **negative** in both specifications (t=−4.16 and −8.05). Their printed Table IV reports slopes multiplied by 100. Replicate signs/t statistics with compatible units; do not confuse them with a realized annual alpha.

**Source-controlled variables:** prior 12−2-month performance; annual cash-based operating profitability divided by lagged assets; annual asset growth; book-to-market; size (with the source's lag conventions). **These need Compustat point-in-time/historical data and matching.** Reproducing Table IV's *no-controls* column is an honest limited benchmark when accounting data are unavailable; representing a replacement proxy as the exact controlled regression is not.

**Historical exchange-volume adjustments:** the accepted manuscript states that NASDAQ share volumes are adjusted **÷2.0 before Feb 2001**, **÷1.8 from Feb–Dec 2001**, **÷1.6 during 2002–2003**, and **no adjustment from Jan 2004**. Those rules apply only when reproducing the corresponding older data and original measurement units; do **not** blindly adjust modern vendor volume again.

**Important finding not to ignore:** the authors themselves study nonlinearities via conditional sorts and explicitly caution that a parametric interaction's implied sign-crossing magnitude should not be taken literally. Further, their §3.8 compares volatility-sorted rather than turnover-sorted strategies and does **not** find analogous high-volatility continuation. **Turnover is the primary state for A, not a shorthand for volatility.**

### 1.2 Follow-up replication and external boundary

**Yue, Tian, Tianjiao Li, and Xinfeng Ruan (2023), “Does short-term momentum exist in China?” *Pacific-Basin Finance Journal*, 77, 101920.** DOI: **10.1016/j.pacfin.2022.101920**.

- Publisher text: <https://www.sciencedirect.com/science/article/pii/S0927538X22002153>
- DOI: <https://doi.org/10.1016/j.pacfin.2022.101920>

They **confirm the U.S. coexistence pattern in their U.S. replication** but find **no analogous short-term momentum in China** (short-term reversal remains). This is a *geographic portability boundary*, not evidence that the U.S. finding failed, and does not establish its existence in **2023–2026**.

### 1.3 Interpretation and novelty discipline

**Evidence supports** a historically signed, state-varying U.S. relationship under the publication's sample and definitions. The new study asks whether it reproduces, how its *full supported conditional mean* varies with turnover, what the nonlinear EBM adds beyond the strongest **simple state-aware** comparator, and whether it remains empirically supported in later U.S. dates.

**Not established:** a modern-sample sign switch, continuous smoothness, state causal mechanism, persistent financial alpha, benefit of EBM, profitability after costs, or a theorem equating native InterpretML software with the project's idealized shallow-tree research learner.

### 1.4 Statistical/software/data references

- **Fama, Eugene F., and James D. MacBeth (1973)**, “Risk, Return, and Equilibrium: Empirical Tests,” *Journal of Political Economy* 81(3), 607–636. <https://doi.org/10.1086/260061>.
- **Newey, Whitney K., and Kenneth D. West (1987)**, “A Simple, Positive Semi-definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix,” *Econometrica* 55(3), 703–708. <https://doi.org/10.2307/1913610>.
- **WRDS/CRSP monthly stock data official documentation**, including prices, volumes, shares outstanding, delisting history and security identifiers: <https://wrds-www.wharton.upenn.edu/demo/crsp/form/>; CRSP product overview: <https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/center-for-research-in-security-prices-crsp/>.
- **NYU Stern WRDS access guidance** (affiliation/authorization-dependent; verify the user's own access): <https://research.stern.nyu.edu/services/research-datasets>.
- **InterpretML `ExplainableBoostingRegressor`** API, explicitly chosen interaction pairs and bin resolution: <https://interpret.ml/docs/python/api/ExplainableBoostingRegressor.html>.
- **Kenneth R. French Data Library**, factors and benchmark portfolios: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>.
- Related general finance-ML benchmarks: **Gu, Kelly & Xiu (2020)**, “Empirical Asset Pricing via Machine Learning,” *Review of Financial Studies* 33(5): 2223–2273, <https://doi.org/10.1093/rfs/hhaa009>; **Freyberger, Neuhierl & Weber (2020)**, “Dissecting Characteristics Nonparametrically,” *Review of Financial Studies* 33(5), 2326–2377, <https://doi.org/10.1093/rfs/hhz123>. These motivate nonlinear extensions; their statistical results are **not** proof that turnover×return EBM shapes will be nonlinear in our dates.
- Internal theory: `state_dependent_ebm_paper1_experiment_theory_v1.pdf/.tex` (planning/estimands); P3 (scientific display versus raw science); P6 (environmental invariance/composition); P7 (selection); P8 (support); P2 (coarsening and uncertain representations); Tasks 10B–10C, 12, 15–25 (exact distinct scoped results). User's archived theory is **not an automatic inference guarantee** for actual market panels or native software.

---

## 2. Scientific question, targets and hypothesis ledger

Let `t` index calendar month-ends and `i` a historical **security identifier** (CRSP PERMNO when available). The primary outcome at month `t` is stock `i`'s **total simple return during month t**, `Y_{i,t}`. The lagged predictors are formed at **month t−1 close**:

\[
R_{i,t-1}=\mathrm{TotalReturn}_{i,t-1},\qquad
TO_{i,t-1}=\frac{\text{shares traded during }t-1}{\text{time-consistent shares outstanding}},\qquad
Z_{i,t-1}=\log(TO_{i,t-1}+\epsilon_{TO}).
\]

**Numerical convention:** store total simple returns as decimals (`0.01` = +1%); report expected-return contrasts in **basis points** (`100 bp`=+1%) and portfolio spreads in **percent per month**. Use true share volume and shares outstanding in consistent units; any within-month share-count changes must be audited. `epsilon_TO` is a small **numerical guard chosen only from valid training data**; do not use it to make zero/missing shares eligible. Positive finite turnover remains the primary supported domain.

The unweighted *observational* mean is `m(x,z,c)=E[Y_{i,t} | X_{i,t-1}=x, Z_{i,t-1}=z, C_{i,t-1}=c]` under a specified pooled unit-month law. A market-cap-weighted empirical regression targets a **different weighted projection**; it is not a causal law, nor automatically the pointwise raw mean. Pooled feature controls `c` are kept fixed for scientific comparisons. The source's monthly Fama–MacBeth weighted coefficients, a pooled EBM prediction, a conditional portfolio spread, and this conditional mean are **distinct estimands**.

### 2.1 Hypothesis hierarchy (do not merge)

| ID | Scientific/statistical claim | Appropriate test and meaning |
|---|---|---|
| `A-H0a` source portfolio sign | Under **Table I conditions**, is low-turnover winner-minus-loser <0 and high-turnover winner-minus-loser >0? | Value-weighted monthly source-style portfolio time series, HAC CIs; report missing era and absent NYSE breakpoints. |
| `A-H0b` source regression interaction | Under **Table IV conditions**, is standardized `lag_return × lag_turnover` coefficient positive? | Month-by-month cap-WLS slopes, across-month time-series mean + HAC uncertainty, with/without controls as data allow. |
| `A-H1` modern survival | Are the documented signs/interaction still supported in **2023–2026**? | Prespecified modern period inference, historical benchmark comparison; absence or reversal is reportable. |
| `A-H2` state moderation | Does the **same prior-return** association vary with turnover? | Predeclared supported total-response **double-difference** and direct/simple interaction comparisons; significance of separate curves does not prove their difference. |
| `A-H3` nonlinear enrichment | Does nonlinear state-varying curvature, threshold, saturation or asymmetry add **reproducible** information over linear/spline state-aware alternatives? | Held-out model-to-model paired loss and predeclared nonlinear scientific contrasts with uncertainty and support masks. |
| `A-H4` coarsening | What changes when the **same turnover state** is categorized (e.g., 3 bins) instead of retained numerically? | Same raw observations, predeclared train-only cutoffs, matched model budget and target contrasts; no inference that coarse labels recover raw turnover. |
| `A-H5` stability | At fixed prior-return, turnover and partner controls, are anchored shapes **approximately stable across two calendar environments**? | Affirmative equivalence requires a **confidence upper bound under a materiality tolerance**, not failure to reject difference. |
| `A-H6` future utility | Does the model predict returns/ranks or inform feasible monthly trades **beyond strong simple state-aware rules**? | Sealed chronological OOS prediction and strategy comparisons, costs, turnover and dependence-aware confidence. |
| `A-H7` scientific display fidelity | Does a **fitted EBM model-output** contrast agree with a supported *direct/simpler scientific comparator* at prespecified cells? | Separately audit `D_F`, supported raw/bin evidence and the strength of assumptions; **no generic raw-EBM-CI claim**. |

### 2.2 Intrinsic contrast and economically useful shape

For a fixed additional control setting `c`, prior-return values `x` and anchor `x_0`, and **two identical-scale turnover levels** `z_L,z_H` in joint support, define

\[
D_m(x;x_0,z_H,z_L,c)=
[m(x,z_H,c)-m(x_0,z_H,c)]
-[m(x,z_L,c)-m(x_0,z_L,c)].
\]

On a prior-return scale standardized **using each formation month's available cross section**, predeclare `x_0=−1`, `x=+1` (two standard deviations apart), *only if each corresponding pair of states has adequate data*. The `+1/−1` rule is a **scientific comparison** not a source decile strategy. If support fails, report `UNSUPPORTED`; do not quietly change x or z after seeing outcomes.

Let `S_m(z;c)=m(+1,z,c)-m(−1,z,c)`; a reversal→momentum *sign transition* requires evidence of negative `S` at lower z and positive `S` at higher z on supported locations. An `S` crossing in a fitted EBM grid **is not itself a population finding**. When no supported sign switch occurs, retain a weaker moderation result, if justified.

For continuous turnover, an EBM is a binned/piecewise function, **not intrinsically differentiable in z**. Use finite differences and support-qualified comparisons; optional varying-coefficient smooth model provides an explicitly smoothed alternative.

**Purification caution:** `D_F` must be computed from **the full fitted prediction function**, not a single displayed interaction component (which depends on allocation and correlated features). `D_F` is not necessarily `D_m` under model misspecification or state/feature coarsening.

### 2.3 Default thresholds and evidence vocabulary

Predeclared ***planning*** quantities to freeze in `experiment_A_protocol_v1.yaml` before opening test results:

- `alpha_primary = 0.05` two-sided; adjust a **fixed family** of predeclared shape contrasts using simultaneous/max/Bonferroni or disclosed Holm. Never use nominal 0.05 for dozens of visually selected x–z cells.
- **Illustrative materiality for a change of anchored `−1σ→+1σ` prior-return shape across states:** `epsilon_shape=25 bp` of **expected next-month return**. Treat `25 bp` as a prospective research decision, **not** source effect size. Results with confidence bounds overlapping ±25 bp are **INCONCLUSIVE for materiality**. Require an honest uncertainty interval for affirmative equivalence.
- `z_L,z_H` are **training sample** 20th/80th percentiles of the primary numerical state; use continuous z in same scale at both dates. For the categorical EBM, report corresponding fixed training-only tercile states. If data support these levels only poorly, abstain rather than invent a better contrast.
- Set **no guaranteed predictive return gain**. Report both statistical and economic materiality against the **strongest simple time-safe state-aware comparator**. A **proposed** economically interesting rank-IC gain is `+0.005` in mean monthly rank IC, or a matched cost-adjusted turnover-constrained return increment with uncertainty; these are *screening thresholds*, not an a priori promise of power or a claim of success.
- Scientific evidence status per claim: `SUPPORTED`, `NOT SUPPORTED`, `INCONCLUSIVE`, `NOT EXECUTED`, `INVALID/NEEDS REBUILD`; status must state whether the claim concerns `SOURCE-ERA`, `MODERN`, `MODEL DISPLAY` or `ECONOMIC DECISION`.

---

## 3. Data prerequisites, entitlements, source-era faithfulness

### 3.1 Preferred data: CRSP plus optional Compustat

**CRSP monthly/daily U.S. security history**, preferably accessed through an authorized WRDS subscription: identifiers (**PERMNO**, PERMCO), time-varying ticker/exchange/share-code/SIC, monthly total returns and delisting returns, prices, volume, **historical shares outstanding**, distributions and splits, market capitalization, listing/delisting eligibility. WRDS documentation explicitly lists these fields in its monthly stock data. An eligible historical full-universe query must include companies that later delisted; present-day API ticker lists are biased for this study.

**Compustat** adds accounting controls for Table IV column (2): as-of-available annual accounting inputs with source six-month minimum availability convention, linkage to CRSP, negative book-equity treatment. Do not pretend that today's fundamentals existed at historical month t−1.

**Access is NOT assumed.** NYU Stern describes WRDS via Stern/community resources and registration; whether a Courant student has the relevant **dataset permission** must be checked at Stage 0. Having WRDS login access does not prove entitlement to CRSP or Compustat. Vendor data may be licensing-restricted and cannot be redistributed in a published Git repository.

**Alternative modern broad panel:** a legitimately sourced historically point-in-time universe with total returns, delist events, **historical** share count, timestamped exchange status, and time-consistent volume adjustments. A provider listing daily aggregates alone does not guarantee that historical shares outstanding or delisting returns are available. **Do not substitute a current `shares_outstanding` snapshot** into 2005 turnover. Check Massive credentials/access and provider documentation, but avoid irreversible large downloads while feasibility is unverified.

**Not source replication:** the user's approximately **99 surviving equities** with **30-minute bars covering roughly 2024-10 through 2026-09**. Monthly aggregation would yield too few independent months, omit delistings and shares history, and cannot support a 10×10 conditional source sort. This may support **code-path unit QA** or a labeled short-horizon adapted descriptive check, not headline evidence.

### 3.2 Feasibility ladder — deliberately conservative

| Tier | Data actually available | Permitted scientific scope / next action |
|---|---|---|
| `A-FULL` | Broad historical CRSP-style eligible universe from source period **1963–2018** or substantial coverage **with original characteristics** | Attempt formal **Table I and/or IV** replication on exact matching dates; then modern evaluation if eligible 2019–2026 data also exist. Distinguish exact full-period versus partial source-era. |
| `A-MODERN-BROAD` | Historical point-in-time U.S. universe **at least ~10 years before 2023**, hundreds of tradable names per month, with accurate share count, total returns and exits | Complete **modern adjusted version**, simplified 3×3 or 5×5 sorts when original 10×10 conditional cells are unreliable; **no exact 1963–2018 replication claim**. |
| `A-MODERN-RESTRICTED` | ~100 securities, but **at least 96 pre-test monthly clusters** and as-of survivor/universe history traceable | **Exploratory small-universe** 2×3 / 3×3 shapes only; no Table I deciles or broad-market claim. Delisting/survivorship caveat remains fundamental. |
| `A-SHORT-PILOT` | **60–95** pre-test monthly clusters with legitimate formation features and labels | Only constrained descriptive source-style comparisons and modeling prototyping; **hold confirmatory nonlinear, equivalence and trading claims** until longer history. |
| `A-TOO-SHORT` | Fewer than **60** usable pre-test monthly clusters, or too few viable formation→target observations | **STOP inference-heavy monthly EBMs and walk-forward claims.** Only schema/data-validation prototype; seek better history. |
| `A-NO-TURNOVER` | Long stock-return panel, but historical shares outstanding/volume missing or materially inconsistent | **STOP the turnover hypothesis**; request correct data. Do **not** replace state by volatility or trade count without a new explicitly authorized experiment. |

The 96-/60-month figures are **practical sufficiency screens**, not mathematical power guarantees. The new chat may choose a cheaper *descriptive* proof-of-concept within its tier, but must not promote it to confirmatory replication. Explicitly record calendar month count, number of unique past-and-present securities, median/5th-percentile names per month, group occupancy, and securities with historical exits.

### 3.3 Minimal fields and retention

Core canonical security-month row:

`month_end, security_id, historical_ticker, exchcd, shrcd, siccd/sector, valid_at_month_end, ret_total_t, ret_total_tminus1, shares_volume_month_tminus1, shares_outstanding_reference, turnover_tminus1, market_cap_tminus1, size_bucket, source_winsor_x, source_zscore_x, source_winsor_TO, source_zscore_TO, EBM_log_TO, EBM_category, y_next_month, delisting_flag, sample_eligibility_reason, source_availability_flags, source_file_hash`.

Index as `security_id, formation_month`; use a consistent label convention to avoid the common confusion of `ret_t` being both last month's predictor and target. The **canonical physical row** should be one security observed at formation month end `s`, with features from s and target return over **s+1**; document `formation_month=s, target_month=s+1` instead of shifting ambiguous variable names.

**Raw values to retain or reference**: the minimum vendor-authorized monthly/Daily CRSP extract or immutable original daily bar path; **one** compressed columnar security-month modeling table with reproducible feature derivation and time-invariant schema. No daily OHLC copied into every EBM fold and no 99-stock intraday Parquet duplication. Downstream folds reference shared canonical data and write small predictions/statistics only.

### 3.4 Eligibility, returns, splits, volume and delists — QA rules

1. **Identity:** prefer permanent security identifier. Corporate name/ticker changes are not new firms. Document duplicate security-months and multi-share-class/issuer choices.
2. **Historic universe:** source stock exchanges, ordinary common-share code 10/11, nonfinancial sector policy. Year-specific provider codes must be mapped audibly. Source Table I vs IV may have **different** negative book-equity filters; do not merge them silently.
3. **Return:** use monthly **total shareholder return** as defined by source, not an overnight-only or unadjusted last price ratio. Include dividends/distributions. If a delisting return is separately provided, combine using the vendor's authorized convention (often `(1+RET)*(1+DLRET)-1` when both valid); **verify double-counting, status and missing-field rules** against CRSP documentation. Missing delisting returns need explicit treatment, not automatic zero.
4. **Share turnover:** ensure numerator monthly **shares traded**, denominator shares outstanding with identical scale (source old CRSP `VOL×100` / `SHROUT×1000`); for modern schemas **derive from field documentation**, do not assume old scale factors. Audit splitting/merging share counts and corporate actions.
5. **Tradability:** exclude or flag inactive, nonpositive price, missing returns, nonpositive/missing shares, very low prior-priced stocks according to a predeclared source-equivalent rule, not a results-driven performance filter. Market cap for source WLS/value-weighting must be previous **formation** month end, not next month's realized cap.
6. **No future availability:** formation-month turnover/return/share count available at order placement; accounting controls lag at least source-prescribed period with actual vintage when possible; monthly NYSE breakpoints based on **formation** date membership, not post-formation survival.
7. **Corporate actions:** count/verify splits, distributions, symbol changes and exchange transfers. Pre-2004 NASDAQ volumes require source-specific adjustments only in archival replication.
8. **QA diagrams/tables:** distribution of raw turnover by date and exchange; share-count jumps; missing/dead names; return–turnover monthly rank correlation; large-cap vs microcap; occupancy of every purported sort cell; coverage of delisted/unlisted stocks; monthly Y and X alignment.
9. **Availability:** if source history cannot be acquired or licensed, fail appropriately rather than inventing an inferred `shares_outstanding` from stale company profile data.

---

## 4. Source reproduction — do these before EBMs

### 4.1 Source Table I: dependent double sorts

For each formation month `s`, on every eligible stock observed *as of s*:

1. Use **NYSE** eligible stocks' **previous-month return** to determine 10 decile breakpoints.
2. Place all eligible NYSE/AMEX/NASDAQ stocks into these lagged-return bins, using a fixed tie/edge rule.
3. **Within each return bin**, calculate **NYSE-only** prior-month share-turnover decile thresholds, then assign all corresponding stocks to conditional turnover categories.
4. Form each valid cell's **value-weighted next-month total-return** portfolio using formation-month market cap. Rebalance monthly. Track empty and low-name-count cells, actual gross/short positions and missing/delisting return exits.
5. For low/high turnover categories report the **winner-minus-loser across return deciles**, monthly average excess return, sample months, HAC t/CI, factor alphas if legitimately available, and a signed benchmark difference. State when source cells are missing.

**SOURCE FIDELITY WARNING:** conditional decile index `TO_{decile | return_decile}` is **not** a universally comparable absolute turnover magnitude across return bins, nor the same as an unconditional turnover tercile or fixed log-turnover threshold. Do not call the Table I turnover label the EBM's numerical turnover state. The later EBM tests scientifically comparable supported fixed `z` values.

### 4.2 Source Table IV: monthwise cap-weighted Fama–MacBeth

For each prediction month t with source-eligible firms, compute **formation-month** covariates, trim all regressor columns at formation-month 1st/99th percentiles, calculate formation-month cross-sectional mean/sd standardization (document whether source uses all stocks vs eligible subset), and create the standardized interaction. Fit **cross-sectional WLS for realized month-t returns**, weight by formation cap. Across t months, report time-average slopes and HAC/Newey–West-adjusted t stats. Implement two identifiable branches:

- `IV1` lag return + turnover + interaction, **no accounting controls** (source Table IV specification 1).
- `IV2` add source accounting/size/12−2 controls **only if real historical point-in-time fields exist** (Table IV specification 2).

Source target to compare for source era: lagged return negative, interaction positive, with source t statistics −4.16/5.45 (`IV1`) and −8.05/9.06 (`IV2`). Estimated slope scales and t stats are *source conditional*—don't optimize to match them. Report adjusted R² with the exact source definition and sample, rather than reading % as OOS R².

**DO NOT USE TEST MONTH'S FAMA–MACBETH REGRESSION FIT TO PREDICT THE SAME MONTH'S RETURN.** It estimates slopes *after* observing the target returns; it is an explanatory historical regression. For prospective prediction, train coefficients solely on earlier labeled months (pooled WLS or rolling historical FMB slope averages) and forecast t from covariates known at t−1. Report the historical inference benchmark and the time-safe forecasting baseline under different names.

### 4.3 Only one source-era claim per fidelity level

- `EXACT-SOURCE-SAMPLE` only if authorized full dates, eligibility, accounting, definitions and returns actually match.
- `PARTIAL-SOURCE-SAMPLE` if source-era years overlap but older years/controls are unavailable; compare source sign, not exact t/average promises.
- `MODERN-PORTABILITY` if only post-2018 U.S. data exist; do not say replicated the 1963–2018 paper.
- `RESTRICTED-UNIVERSE` if just 99 or other surviving stocks; portfolio/risk restrictions must say so in every table/plot caption.

---

## 5. Time-safe nonlinear extension (the main new experiment)

### 5.1 One numerical state, two encodings

For **scientific extension**, define `Z=log(TO)` for positive turnover. Any numerical guard and training-support trimming must be frozen. **The categorical state derives from this same Z** using fixed **tercile boundaries computed solely from the training asset-month rows, with the same weighting convention across folds**. Retain physical `TO` in diagnostics. The continuous-EBM version receives `Z` numerically, and the discrete version receives its `low/medium/high` ordinal group.

**Training-only cutoff rule:** do not recompute terciles using held-out outcomes or held-out period turnover values. Source Table I uses a **different**, each-month, return-conditional sorting; it remains the source benchmark, not this encoding. Optional relative-turnover percentile is a separately labeled robustness target and cannot replace the primary numeric `Z` based on actual turnover without approval.

The focal return input for the main EBM is `X`, the **formation-month trimmed then cross-sectionally standardized stock return**, computed using only *the formation cross section*. Store `X_raw` as well. Since this standardization redefines one X unit each month, a reported `x=+1` means one **contemporaneously observed formation-cross-sectional sd**, not a fixed 1% simple return. To interpret fixed return magnitudes, add a **separate** raw-return sensitivity with its own support checks, not an unlabeled axis change.

The matched simple nonlinear baselines must use **the same `(X,Z)` information** as the EBM models. They need not impose the old Table IV raw standardized turnover axis; the historical Table IV regression is separately labeled.

### 5.2 Frozen primary comparison families

| Code | Model | Purpose / distinction |
|---|---|---|
| `N0` | Train-only historical expected monthly return (by date), and **zero-return forecast** | Naive regression baselines; no future cross-section targets. |
| `N1` | Historical rolling past-only Fama–MacBeth slope average or pooled past-only linear WLS | Time-safe closest **predictive** cousin of Table IV. |
| `L0` | `Y ~ X + Z` pooled linear WLS | No state interaction. |
| `L1` | `Y ~ X + Z + X:Z` with exactly the same transformed X/Z | **Primary strong parametric state-aware comparator**. |
| `S1` | Low-degree penalized spline varying coefficient: `Y ~ s_X(X)+s_Z(Z)+X*s_Z(Z)` or predeclared smooth interaction | Smooth threshold/curvature competitor; hyperparameters chosen only inside development/validation. |
| `E0` | Additive EBM `f(X)+g(Z)` (`interactions=0`) | Interpretable nonlinear but without moderation. |
| `E1` | **Prescribed** EBM `f(X)+g(Z)+h(X,Z)` with **discrete Z** (train cutoffs) | State-varying tabular shapes. |
| `E2` | Same EBM with **numerical continuous Z** (binned internally) and **exact pair `(X,Z)`** | Primary nonlinearity/continuous-state comparison. |
| `C1` | One modest expanded baseline with genuine as-of available **size** and longer-horizon momentum; same explicit `X:Z` | Check composition/size effect; no Compustat need for this minimal controlled branch. |
| `E3` | E2 plus the same controls as C1; preserve only the prescribed `(X,Z)` interaction | Optional secondary extension, no post hoc third-order interaction. |

**No category error:** replacing the source's high-vs-low conditional portfolio return with a pointwise EBM contrast needs a scientific mapping and support. We report the **source portfolio spread** and the **EBM supported scientific shape** as related but different estimands.

### 5.3 Model fitting and compute controls

- Use `interpret.glassbox.ExplainableBoostingRegressor` with an **explicit `interactions=[('X','Z')]` pair** or correct version-specific feature indices. Do not use auto-selected `interactions='5x'` for the primary scientific claim. `max_interaction_bins=16` or `32` predeclared candidate resolutions; `max_bins=64` or `128`; fixed low `max_leaves` (default 2) and `min_samples_leaf` ≥20 as initial regularization. Choose hyperparameters via **training→validation only**, prioritizing stability. Exact API and seeds are logged rather than relying on evolving defaults.
- Suggested bounded search: two interaction bin resolutions × two leaf-minimum values × seed 42 first; promote at most **two** configurations to five-seed diagnostics based solely on validation and fit resource budget. No 100s of search combinations.
- Outer bagging, smoother defaults, gain settings and term bin counts may vary with pinned `interpret` release; record physical package version and `.get_params()`; default InterpretML EBMs are **not** identical to theoretical literal three-leaf tree learners from Tasks 3–25.
- Train only on **prior months**, with train/validation split by calendar, no random row-level internal validation that includes future months across assets. If `interpret` internal random `validation_size` uses future observations, either set proper time-isolated validation strategy or explicitly disable internal early stopping/validate external; record the operational compromise. Do not quietly accept a random sample across train and test dates.
- Cap-weight normalization for pooled training: within each *training month*, weight stocks by their **formation market cap normalized to sum one**, so each training month contributes equal total loss. This reproduces the monthwise WLS economic weighting more closely than raw global cap-weight pooling. Unweighted row losses are a secondary sensitivity.
- Time features (calendar month label, future realized aggregate return), ticker ID or raw price **must not** become unrestricted EBM features to memorize stock/time; no latent embeddings. Control additions require fixed consent if they change primary estimand.

### 5.4 Chronological samples and target availability

**Primary proposed training/development if coverage exists:**

| Segment | Calendar period | Role |
|---|---|---|
| Historical reproduction | **1963-07 through 2018-12** if source-permitted; otherwise available overlap (declare exact sample) | Historical Table I/IV replication; source evidence, not untouched new validation. |
| Development training | **earliest eligible date through 2018-12** (prefer ≥2004 if sources permit) | Learn normalizations, categorical thresholds, EBM parameters (on appropriate train-only folds). |
| Development validation | **2019-01 through 2022-12** | Freeze model choices, support rules, materiality comparisons, scenario budgets; post-publication 2022 should be labeled if used as validation. |
| **Sealed final test** | **2023-01 through 2026-09** | OOS predictive/economic and independent modern scientific confirmation; **do not tune on this period**. |

If legitimate data begin after 2004, start on first verified available month, preserving the 2019/2023 cutoffs when enough months exist. Need at least **~96 complete pretest formation→target month pairs** to attempt restrained nonlinear analysis; otherwise stay descriptive. Every training fold's monthly formation-cross-sectional standardization may use **only that month’s formation-time observable predictor distribution**, not future response.

The source study includes data through 2018, so 2019–2022 validation is post-source-sample but not necessarily all post-publication; final 2023+ is an explicitly later test. If only 2021–2026 data exist, **stop** as substantive confirmatory Experiment A rather than compress the theory into 2–4 years of monthly clusters to get a spurious good fit. A change of primary sealed test window requires user approval.

### 5.5 Full-fidelity vs affordable minimal branch

- `A-FULL`: source-compatible Tables I/IV **plus** C1/E0/E1/E2 and modern sealed test.
- `A-MODERN-BROAD`: source **style** returns and `IV1` only if covariate coverage; main model ladder, 3×3 or 5×5 summary with named shape estimands, no exact Table I claims.
- `A-MODERN-RESTRICTED`: 2×3 exploratory shapes with strong abstention and descriptive uncertainty, no confident population turnover→momentum sign switch claim. A 99-stock surviving universe is one possible restricted population, not a broad-market sample.
- `A-SHORT-PILOT`, `A-TOO-SHORT` or `A-NO-TURNOVER`: only the explicitly allowed descriptive/data-audit/prototype work; do **not** silently turn experiment into daily returns, a stock-level toy regression, VIX state or a 30-minute EBM.

---

## 6. Scientific shape, support and calibrated interpretation

### 6.1 Primary visual/scientific outputs

1. Source Table I **10×10** return-first/turnover-conditional portfolio heatmap (only when fully eligible); low/high winner-minus-loser with HAC CI and source t-stat reference lines.
2. Monthly Table IV fitted interaction coefficients distribution and HAC time-average; source controls/no controls separated.
3. EBM **supported** 2D `(X,Z)` total-prediction surface, masked in unsupported regions; continuous Z binned semantics disclosed.
4. Return-vs-X anchored curves in **low/median/high numeric turnover** with **same partner controls** and consistent Y units; categorical and continuous fitted surfaces side by side.
5. Predeclared `S(z)=F(+1,z)−F(−1,z)` with support counts and uncertainty; mark empirically defensible negative/near-zero/positive regions, without labeling a graphical crossing as a population sign change.
6. `D_F` for high-versus-low Z, simple-model contrast, and **direct bin-conditional** contrasts on **supported local cells**; distinguish raw pointwise from bin means and market-cap-weighted projection.
7. Curve variation across fixed calendar windows and distribution/cap-weight changes; margins/joint support/representation shifts separately plotted.
8. Strongest simple spline/interaction comparator plus EBM seed/bag stability; show when a simple model is sufficient.

### 6.2 Direct science versus displayed model

- Total response contrasts are invariant to additive component reallocations; arbitrary displayed EBM term shapes under correlated characteristics are not.
- A **supported binned, sample-mean contrast** estimates a **bin-conditional target** under its sampling design, **not** automatically `m(x,z,c)` at a continuous point. Control for within-bin turnover/return composition and other characteristics; market-cap weighting changes the target.
- Theoretical Task 12 exact Gaussian whole-tree selected pivots do **not** apply to general `interpret` bagged/adaptive EBMs. Tasks 17/18 all-future **same-frozen-data** path certificates do not prove feature relationships stable across months or native software equivalent.
- Restrict plots to **joint supported** X×Z rectangles, with minimum month coverage and enough independent months. Raw cross-sectional row counts can be large yet high-turnover observations concentrated in a few calendar shocks; both dimensions matter.
- Prefer sample-split or joint confidence for fixed predeclared rows; do not claim ordinary EBM error bars are valid post-selection scientific CIs.
- If proper-model approximation is poor, report the fit as a weighted projection of the observed panel, not the intrinsic truth. A model may predict well and still distort a rare scientific query (P3/P8; Tasks 10C/23).

### 6.3 Affirmative stability/materiality

For two dated periods `e=0,1`, compare *the same* anchored shapes at fixed X, Z and controls. Use a **single declared family** (for example, x∈{−1,0,+1}, z∈{z_L,z_H} and selected controls), and disclose the exact sampling/CI assumptions. Stability of `S_e(z)` across environments is a distinct question from constancy across turnover states *inside one environment*.

- `|difference|` CI entirely within ±25 bp (or a formally frozen alternate epsilon): **AFFIRMATIVELY APPROXIMATELY STABLE** for that row under its stated CI law.
- CI entirely outside the declared stability range in one direction: **MATERIAL CHANGE** for that row, with appropriate multiplicity control.
- Otherwise: **INCONCLUSIVE**. An insignificant zero test is *not* proof of stability.

A transition from reversal to momentum is different from temporal stability. A scientifically supported sign switch at a z contrast does not establish it holds forever or explains causally *why* momentum exists.

---

## 7. Evaluation, dependence, inference and null testing

### 7.1 Statistical unit and cross-asset dependence

The model panel contains correlated equities observed in the **same calendar month**, with common market shocks, industry dependence, firm serial persistence, and possibly changing universe. Treat monthly blocks as primary replicates for source returns and score differences; DO NOT use row-iid p-values based on `N_firms×T_months`.

- Source Table I: report **monthly portfolio return series**, HAC/Newey–West over calendar months; disclose lag convention and sensitivity to e.g. 3/6/12 months. Source control factor alphas only if available with as-of factor dates.
- Source Table IV: Fama–MacBeth **monthly slope** time series with HAC across months, not one giant pooled IID t statistic.
- EBM prediction: collapse per-stock loss to **monthly weighted cross-sectional loss**, then do paired calendar-month loss-difference inference using block/bootstrap HAC; name actual working assumptions. Multiway firm-month cluster methods can be a sensitivity comparator, not automatically equated to the paper's stricter finite-dependence theoretical CLT.
- Scientific curves: **resample complete months**, preserving all cross-sectional rows and, with blocks, temporal dependence; refit all necessary discovery steps for selection-aware uncertainty. For clustered/weak support, honest abstention is essential.

**No false theoretical guarantee:** archived dependent-panel theorems use specific fixed-unit, finite-dependent or bounded-process laws; they do **not** automatically validate arbitrary long-memory equity panels, randomly chosen turnover cutoffs, sparse cross-sectional cells or bagged InterpretML confidence intervals. HAC/block methods have their own approximation assumptions; disclose them.

### 7.2 Prediction metrics and strong baselines

Compute on identical eligible test security-month rows and separately equal-calendar and market-cap-weighted objectives:

- **Out-of-sample monthly return RMSE/MAE and OOS R²** relative to zero and historical-month-mean predictions; state the same test rows for all models.
- **Cross-sectional monthly Spearman rank IC and Pearson IC**, with mean, dispersion and month-block CIs; top/bottom-decile/quintile spreads only when name counts warrant.
- **Directional accuracy** of return sign, but compare to class-frequency / always-positive and market-only naive baselines; do not use a 50% baseline reflexively.
- **Paired loss difference** E2 minus stronger of L1/S1 (selection of "stronger" on **validation only**), HAC/block CI; separate in-sample explanatory fit from prospective forecasting.
- Shape reproduction: return–turnover sign difference of held-out fully supported groups; magnitude and uncertainty under source-era vs modern law, with materiality threshold.
- Model cost: wall-clock time, memory, disk bytes, bins/terms/leaf counts, number of simulations/seeds.

### 7.3 Four-stage project-wide validation

1. **In-sample assessment:** source-style regressions/sorts, nested model fit and scientific contrasts in historical/development sample, with proper selection disclosure.
2. **In-sample full-pipeline negative controls/permutations:** freeze a transparent null mechanism that disrupts lag-return-specific predictability while preserving a meaningful subset of calendar/size/turnover structure; **rerun feature processing, tuning and selection** for every synthetic null. **Null exchangeability is not automatic**: a within-month label shuffle is a diagnostic under conditional assumptions, not necessarily an exact scientific p-value for the true time-series panel.
3. **Walk-forward OOS:** models trained/tuned solely on earlier calendar months, apply time-safe past-only coefficients, freeze 2023–2026 final test; report subgroup/size/market-period splits as **predeclared diagnostics**, not new train/test horizons selected after seeing returns.
4. **Walk-forward full-pipeline null:** same valid null-generation mechanism but rebuild the entire discovery/selection procedure for each iteration and then evaluate on genuinely forward held-out months. Suggested start 199 null draws with one frozen seed (Monte Carlo p-value resolution ≥0.005); if computationally infeasible, record reduced draws and limitations rather than silently treating 20 randomizations as conclusive.

**Preferred null implementation for Stage 0 review:** month-preserving outcome reassignment **within broad, predetermined size/turnover strata** as a *conditional negative control*. It preserves date-level realized cross-sectional outcome distribution but disrupts some firm/time dependence and within-group composition; conditional exchangeability must be justified before attaching an exact randomization-test interpretation. A whole-calendar-block shift can be an additional sensitivity if timestamp/index-matching permits. If neither null is scientifically defensible at the required level, report the null as an **exploratory falsification diagnostic** and rely on forward paired inference for confirmatory claims. Never write "valid exact permutation p" without its null/exchangeability assumptions.

### 7.4 Multiplicity, tests and validation leaks

- Predeclare **primary** historical replication signs, modern low/high source-style spread signs, primary high-low scientific double difference, and E2-vs-strong-simple-compared predictive loss. Later discovered x–z thresholds are **exploratory**, not independent tests.
- Familywise adjustment for co-examined states/contrast grid; show unconditional model comparison and state-stratified results with selection masks.
- EBM training must not randomly split across test months; fold-specific preprocessing includes turnover cutoffs, winsorization, control imputation and any causal historical parameter estimation.
- If the final test is inspected and hyperparameters changed, mark evaluation as contaminated, create protocol v1.1 and require **new, truly unseen** test data for fresh confirmatory validation. Rerunning on the same 2023–2026 period does not recreate an untouched test.

---

## 8. Trading/economic usefulness — separate and execution-timed

**Monthly strategies only**, formed at the end of formation month s and held through s+1 under explicitly approximated fills. The statistical label is the next-month **total shareholder return**; an implementable execution return may differ because of cutoff, closing auction, splits, corporate actions and short availability.

Comparators (equal eligible universe/month and constraints):

1. Source-inspired **high-turnover winner-minus-loser** (momentum orientation); **low-turnover winner-minus-loser** should be negative historically, so if taking reversal positions report its **negative** orientation separately (short past winners / long past losers).
2. Matched **linear state-aware L1** and spline S1 ranking/position strategies, not only state-blind EBM.
3. E0/E1/E2 prespecified top/bottom K, long-only top K and/or long-short quintile where supported, with **same exposure, gross/net leverage, size/liquidity requirements, rebalance timing and portfolio construction** as comparators.
4. Equally constrained randomized top/bottom selection, zero/hold-cash, source-style market-cap buy-and-hold, and possibly relevant broad-market ETF exposure (latter is a benchmark, not a matched dollar-neutral strategy).

Cost scenarios: **0, 10, 25 and 50 bps per side per dollar traded**, plus separate qualitative spread/slippage/borrow feasibility flags. These are **assumed scenarios**, not observed effective costs. Report actual turnover (defined using notional traded), one-way and roundtrip interpretation, size capacity, transaction-cost drag, months with empty source double-sort cells, gross/net Sharpe with dependence-aware uncertainty, annualized turnover/return conventions, downside drawdown and factor exposures if possible.

Historical source's positive high-turnover spread does not guarantee that **shorting**, **monthly close executions**, capacity or net profits can be implemented in the user's account. Failures after costs do not invalidate an observational statistical relationship; nor does a positive regression coefficient establish a profitable decision.

---

## 9. Quality-control hard-fail list and honest unexpected outcomes

### 9.1 STOP / INVALIDATE the affected run if any occur

- Y and X are from the **same month** due to a `shift` error or a month-end mapping; the model uses future monthly market return/market cap/turnover or controls before their availability.
- **Historical shares outstanding** are replaced by current shares, mixed `VOL/SHROUT` units are not corrected, splits inflate volume ratios, or modern volume gets old NASDAQ adjustment applied without justification.
- Source 10×10 sorts use modern full-universe breakpoints instead of **NYSE-only/return-first conditional** breakpoints but are labeled "exact Table I".
- Table IV's **realized month-t WLS coefficients** leak month-t labels into prospective predictions.
- Delisted or disappeared stocks are silently dropped from realized next-month response; firms included only because they survived through 2026; no universe/selection disclosure.
- 2023–2026 test outcomes influence winsor thresholds, state bins, feature selection, early stopping or hyperparameter search.
- 99 stock-months treated as independent time clusters; native EBM bag standard deviations called inferential standard errors for selected raw shape.
- Continuous turnover plotting extrapolates to absent return×turnover×size configurations, with graph interpreted as identified population science.
- Historical/source Table IV baseline and live pooled model assigned the same estimator/target label; or an adapted 3×3 panel claimed equal to the published Table I.

**Response:** quarantine invalid outputs, version the repair, rebuild all affected downstream results, preserve log of what was wrong and what was rerun.

### 9.2 Diagnostic interpretations (including negative results)

| Observation | Leading valid interpretations/checks | Honest status/next action |
|---|---|---|
| Source-period low negative/high positive successfully reproduced | Benchmark construction and historical evidence plausibly consistent, **subject to exact sample/return/cap/volume** QA | `SOURCE-REPLICATION SUPPORTED`; modern survival still open. |
| Signs absent with 99 current large stocks | Universe selection/conditional decile support bias, later-period change, missing/incorrect historical shares, few independent months | `ADAPTED-NOT-REPLICATION`; do **not** search new horizons or state. |
| FMB interaction positive, but EBM shape no reliable sign crossing | One coefficient measures average conditional relationship; local shape support/inference more demanding | Moderation may hold; nonlinear transition `INCONCLUSIVE`/not observed. |
| Raw turnover percentiles predict differently than source conditional sorts | Their scientific targets/cutoffs/conditioning differ | Report methods, not a contradiction by default. |
| EBM wins over L0 but not L1/S1 | Added value likely due to **existing state interaction** captured by simpler model | Do not advertise novel nonlinear model superiority. |
| EBM low/high display flips at extreme turnover with 4-month concentration | Unsupported cells, outlier, fund turnover stress, model projection artifact | Mask/abstain; avoid confident transition claim. |
| EBM highly stable over seeds but between-period fitted curves move | Data-law, support, factor composition, market cap weights and calendar shift all candidates | Compare raw supported fixed-state shapes, not pure term charts. |
| Wide valid monthly-cluster confidence interval | Few independent months or extreme-return dispersion | `INCONCLUSIVE`, no false stability/equivalence. |
| Strongest effect in firms omitted by large-cap screen | Sampling restriction changes target | Wider sample needed; restricted result not a failed exact replication. |
| Historical source alpha positive but 2023–2026 alpha absent/negative | Post-publication decay or noise; later markets differ | Strong **honest replication/portability finding**, not engineering failure if QA passes. |
| EBM predicts ranks but strategy net after costs negative | Economic implementation/costs separate from predictability | Science may still be useful; profitability claim fails. |
| Prediction better in test but original source-style interaction insignificant | Different statistical target, objective or selection; may be nonlinear other covariates | Keep claims separated, investigate but do not re-label stronger finding as a source replication. |

---

## 10. Minimal reproducible artifacts and staged work

**Directory layout is a suggestion; new chat/Codex must adapt to preexisting `AGENTS.md` and repo without copying giant data:**

```text
experiment_A_monthly_turnover/
  README.md
  config/experiment_A_protocol_v1.yaml
  docs/
    source_table_I_IV_crosswalk.md
    dataset_entitlement_and_survivorship_audit.md
    outcome_and_turnover_timing_audit.md
    exception_log.md
  data/
    links_to_existing_authorized_raw.md
    derived/monthly_security_panel_v1.parquet
  src/  # extract/month labeling/cap accounting/benchmarks/baselines/EBM/support/tests/report
  tests/  # synthetic corporate actions, lag, conditional breakpoints, delists, lookahead
  reports/
    A0_data_go_nogo.md
    A1_source_replication.md
    A2_state_models.md
    A3_scientific_shapes_and_support.md
    A4_walk_forward_and_nulls.md
    A5_economic_value_and_final_report.md
    experiment_A_final_research_report.md
  artifacts/ # compact model objects, test predictions, figures, manifests only
```

Required final materials:

1. A clean **scientific abstract** with explicit source vs modern sample and supported/failed/inconclusive outcomes.
2. **Publication crosswalk:** Table I/IV original definition, original sign/t, exact our scheme, mismatches, our interval, and source-era applicability.
3. Complete **data QA**: dates, unique firms, firms per month, NYSE-only thresholds, delist count, missing returns, share count coverage, volume-unit/adjustment audit, file hashes.
4. **OLS/Fama–MacBeth/portfolio benchmarks** with monthwise estimates, HAC sensitivity and correct target information time.
5. **Model scorecard** N0–N1, L0–L1, S1, E0–E2, and controls when actually available; chronological train/val/sealed test, paired loss and monthly rank IC, wall time/disk.
6. **Scientific contrasts**: fixed x/z/c, sign and materiality, support, main effect vs true total response caution, discrete-vs-continuous comparison, temporal stability, multiplicity.
7. **Null/permutation artifacts** with validity classification and full selection-loop reruns, not just shuffled outcome p values.
8. **Economic report**: end-of-month tradability, long/short definitions and source spread sign, execution assumptions, costs, matched random/buy-and-hold and simple state-aware baselines.
9. **Claim/limitation ledger** A-H0a–H7, source-era/modern labels, signed effect CIs, explanatory vs predictive outcomes, negative findings and follow-up requests.
10. **Environment + integrity:** version-controlled config, source/code/environment hashes, per-stage file changes, tests, logs, input licensing restrictions and disk-use totals.

### 10.1 Stages, acceptance gates and necessary human authority

| Gate | Stage | Acceptance requirement before next stage |
|---|---|---|
| `A0` | Inspect repo/`AGENTS.md`, WRDS/CRSP/other entitlements, shares-history, delist and date coverage; choose honest tier | Evidence that usable monthly panel is truly possible, exact sample tier and storage plan. If not possible: `BLOCKED`, **no phantom modeling**. |
| `A1` | Create immutable canonical month panel and source Table I/IV when entitled | Security-month lag QA, share-unit/delist tests; NYSE return-first sorts; historical FMB results and source mismatch log. |
| `A2` | Small source-aware linear/spline/EBM ladder | Past-only train/val fitting, identical test rows, no normalizing future data, predeclared bins/weights/resource budgets. |
| `A3` | Support, total-response shape and scientific fidelity | Explicit supported x/z contrasts, direct-bin comparators, seed/complexity stability, abstention on sparse cells. |
| `A4` | Walk-forward and valid/qualified nulls | 2023–2026 sealed test, calendar-block paired loss/IC inference and full-pipeline null experiment with limits disclosed. |
| `A5` | Source-inspired and model economic evaluation; final report | No same-period coefficient lookahead; net monthly returns/costs, matched naive/random/state-aware baselines, source-vs-modern claim ledger. |

**Minor exception authority:** API pagination/retry; WRDS table/column naming migration; safe schema/key/type fixes; equivalent timezone/month-end handling; one-off documented bad record quarantine; source-era partial window because of license; non-result-driven downscaling of tree/bag/permutation budget; activating the predeclared `A-SHORT-PILOT` descriptive-only tier; existing repo layout; static output/chart-format changes. Log exact changes and rerun affected tests.

**Require user approval (no silent change):** switching monthly to 30-minute horizon, changing primary turnover to realized volatility/VIX, dropping total return/delist obligation while retaining exact-source language, changing modern sealed window, swapping the universe due to model outcomes, selecting feature controls or turnover thresholds by significance, treating survived 99 stocks as whole U.S., buying a data subscription, an unaudited shift to native default EBM interactions, or lifting materiality/multiple-test constraints after seeing test results.

---

## 11. Priority interpretation for future EBM theory discussion

When the results return to this theory thread, distinguish:

1. **A true supported turnover-conditioned scientific return-shape change** versus ordinary composition and market-cap weighting effects (P1/P6; T19/T22).
2. **Coarse turnover category loss** versus a more flexible fitted shape; the same raw Z must underlie both experiments (P2; T24/T25).
3. **Excellent global prediction but a misleading local scientific shape** (P3; T10C/T20/T23).
4. **Supported group scientific stability** despite correlated indicators, thin stock-month support or weak return×turnover crossings (P8; T7/T8/T23).
5. **Model selection** and post-discovery caveats, especially the difference between predeclared confidence and exact conditional winner inference for a *different literal tree algorithm* (P7; T12).
6. **Greedy path reproducibility** during model fitting is not across-environment stability, and archived original path theorems are *not* native software theory (P5; T17/T18).
7. **Scientific nonlinearity, predictive information, cross-asset portability and positive net decisions are separate outputs** (T21/T22). A negative economic test need not erase a meaningful conditional response-shape finding.

**Expected information value (not expected guaranteed performance):** a clear answer about whether the classic sign-changing relationship remains present, whether turnover moderates only an average *slope* or a more complicated *supported nonlinear shape*, whether coarse turnover states hide shape movement, and how a scientific EBM display differs from source decile portfolio results. All four outcomes are valuable if source-faithful and uncertainty-qualified.

---

## 12. Final scope and companion handoff

This file is the scientific authority for Experiment A. Its companion `experiment_A_new_chat_codex_and_diagnostics_instructions_v1.md` governs the new chat's Codex-prompt stages, small-exception permissions, diagnostics and final copy-back. An implementation assistant may adjust minor engineering choices, but **must not silently change the scientific question to obtain attractive results**. If quality of CRSP-style history is insufficient, an honest data-stage `BLOCKED` report is a valid scientific outcome, not license to invent a substitute experiment.

**Experiment B is out of scope here.** After the A and B implementation chats are handed off, this original EBM Theory thread resumes with independent mathematical and research-novelty discussion.
