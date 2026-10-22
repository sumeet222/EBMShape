# C2R — direct curves, OLS and state-dependent splines

**Stage: PASS_WITH_QUALIFICATIONS. Implementation/QA PASS.** C2R is complete on the already explored 2016–2021 development data. The historical PREV closing-hour H−L is **2.0050 pp**, reproduced to -2.78e-15 pp. It is a compositional allocation association, not source-paper exact replication, independent confirmation, or a certified effect exceeding 2 pp. No EBM, added-state model, later-year C outcome or reserved evaluation was run.

The fixed 8×4 M4 changes pooled chronological profile MSE by **-1.66% relative to M0** and **-0.85% relative to linear P-OLS-Z** (positive means lower loss). Lowest pooled profile MSE among declared candidates: **M0**; lowest closing-share MSE: **P-OLS-Z**. These are developmental descriptions of predeclared candidates; no new hyperparameter was chosen from them.
Scalar OLS-L1 reduces pooled closing-share MSE by **2.43%** versus the intercept baseline, while its full-profile P-OLS-Z counterpart has higher profile MSE than M0. The scalar benefit therefore does not establish whole-curve predictive improvement.


## Data, identity and time scope

| year | Q_days | Z0_days |
|---|---|---|
| 2016 | 249 | 247 |
| 2017 | 249 | 247 |
| 2018 | 248 | 245 |
| 2019 | 248 | 244 |
| 2020 | 247 | 241 |
| 2021 | 250 | 248 |


All fits use exactly 1,472 Z0-valid keys; 1,491 Q-valid dates are counted separately. The two backchecks contain 241 dates in 2020 and 248 in 2021 (489 pooled). First/last main source dates are 2016-01-05/2021-12-31; auxiliary Jan 4 supplies prior state only. The pinned NPZ and two revised/original specifications pass SHA256. Original 6 annual D2 references plus 72 C missing-key monthly supplements match hashes; no minute rows were decoded for C2R. C1R's numeric state table hash is verified; exp(Z0) agrees with RV_prev at atol1e−18/rtol1e−12. Strict scheduled predecessors are independently checked. Full windows agree by independent cumulative sums to 1e−10.

Q is 390 within-session minute log squares grouped into 78 bins, normalized by each day's own R. First return is 09:30 close/open, with no overnight or missing-bar fill. UTC starts and XNYS/ET govern session timing. CLOSE_C [66:78], MID_C [24:48], OPEN30 [0:6] retain full-C priority; MID_P0 [30:42]/CLOSE_P0 [72:78] are secondary; PRE_CLOSE_DIAG [66:72] is post-P0 exploratory. Return prediction, latent spot volatility and ratio-of-group-RV totals are different objects.

Twelve early closes and seven incomplete ordinary days remain excluded: 2016-02-02, 2019-08-12, 2020-03-09/12/16/18, 2021-05-05; 100 missing minutes. Four March 2020 crisis dates are absent. This population concerns eligible complete sessions, with nonrandom missingness risk. B's 39-row HF repair, B return table, D1 pilot, VIX and FOMC are not used. R1 status remains SOURCE_INSPIRED_PROXY.

## Frozen protocol, models and information

`config/C_C2R_development_protocol_v1_1.json` was written before the real fits; SHA256 `24ef4122ce069df7f7e228ecfc1f05b48983005273c1e84da10cfb03cdb14bca`. It is a C2R exploratory development freeze. C1R's full-C draft remains unchanged/unlocked; official horizon/split/evaluation are pending. Date hashes, code/software/source hashes, exact fitted coefficients, knots, cutpoints, counts, and training/forecast dates are in `model_parameters.json`, `model_registry.csv` and `provenance_and_QA.json`.

D_FULL is descriptive on all 1,472 previously seen dates. DEV_2020 trains through 2019-12-31; DEV_2021 through 2020-12-31. Training scalers, natural-spline knots, tercile/quintile cuts and quantile grids are refitted separately at each origin, then held fixed. No eval-year target affects them; no randomized folds, early stopping or hidden search is used. The same chronological date keys score every core model. P0 fixed ranks remain D-only; full-sample quantile S0 differs from P0 rank labels on **1 date(s)**, explicitly disclosed rather than forcing them to agree.

Scalar formulas: L0=intercept; L1=1+standardized Z0; L2=1+mid+high indicators; L3 adds state-specific intercepts and z_s×mid/high slopes; L4=1+z_s+z_s². Low is the reference. A standard unit is one training population SD of log prior RV. L3 concerns scalar slope moderation, not time-of-day interaction. Rank-deficient designs abstain; none is silently pseudo-inverted for inference.

M0 is training Q mean; P-OLS-TIME is its algebraic alias, not an extra discovery/fit. M1 is train-S0 conditional Q mean, with frozen basic support and explicit M0 fallback. P-OLS-Z estimates a_k+b_k z_s by daily multioutput OLS; sum a≈1 and sum b≈0 are checked. M2 uses clamped cubic time B splines, 8 basis columns primary and 12 sensitivity. M4 is the nonredundant full tensor of that time basis and four natural-cubic state basis columns at train min/terciles/max, with linear tail continuation and **zero penalty**, full-rank least squares. Constants belong to both spans, avoiding redundant intercepts. The no-interaction control uses the same bases with centered additive state effects, not native EBM M3. For closed Q, a pure state-level vertical shift across all bins is algebraically constrained to zero. No log-Q transform, clipping/projection or M8 model was used.

| model | kind | train_n | rank | edf | condition | out_of_training_range_eval_n |
|---|---|---|---|---|---|---|
| OLS-L0 | scalar | 1472 | 1 | 1 | 1 | 0 |
| OLS-L1 | scalar | 1472 | 2 | 2 | 1 | 0 |
| OLS-L2 | scalar | 1472 | 3 | 3 | 3.73095 | 0 |
| OLS-L3 | scalar | 1472 | 6 | 6 | 17.7927 | 0 |
| OLS-L4 | scalar | 1472 | 3 | 3 | 2.80184 | 0 |
| M0 | profile | 1472 | 78 | 78 | 1 | 0 |
| M1 | profile | 1472 | 234 | 234 | 1 | 0 |
| P-OLS-Z | profile | 1472 | 156 | 156 | 1 | 0 |
| M2-T8 | profile | 1472 | 8 | 8 | 5.03227 | 0 |
| M4-T8-Z4 | profile | 1472 | 32 | 32 | 57.6714 | 0 |
| NOINT-T8-Z4 | profile | 1472 | 11 | 11 | 12.0443 | 0 |
| M2-T12 | profile | 1472 | 12 | 12 | 4.83304 | 0 |
| M4-T12-Z4 | profile | 1472 | 48 | 48 | 55.3881 | 0 |
| NOINT-T12-Z4 | profile | 1472 | 15 | 15 | 14.6685 | 0 |


Ranks/edf above are numerical model parameter counts, not independent-day sample sizes. A tensor with 32 parameters is not 32 independent shape tests; each date contributes a whole vector with equal weight. Complete origin cutpoints/ranges/occupancies and out-of-range eval counts are in the registry/parameters. Prediction outside training range is reported, not hidden; interpretation remains support gated.

## Direct and fitted scientific shapes

Raw whole-profile H3 TV is **0.048510**. The new fixed-label 20-session descriptive bootstrap H1 interval is **[0.832, 3.296] pp**. Historical P0 block5/10 intervals were reused, not rerun; the 20-session check is an additional sensitivity on the same viewed records. Every draw resamples whole scheduled date slots jointly; invalid slots never become filled outcomes. No learner was refitted in this bootstrap. `block_intervals.csv` gives all six window contrasts and the qualified 20-block TV interval. The TV percentile distribution may be biased near zero and is not a near-invariance certificate.

| model | window | estimate_pp | raw_pp | difference_pp | TV | raw_TV | simplex_mean_curves |
|---|---|---|---|---|---|---|---|
| M0 | OPEN30 | 0 | -2.20523 | 2.20523 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M0 | MID_C | 2.60209e-16 | 0.348534 | -0.348534 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M0 | CLOSE_C | -3.46945e-16 | 2.00498 | -2.00498 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M0 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 1.60462e-17 | 0.0485101 | True |
| M1 | OPEN30 | -2.1946 | -2.20523 | 0.0106202 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M1 | MID_C | 0.335582 | 0.348534 | -0.0129513 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M1 | CLOSE_C | 2.04005 | 2.00498 | 0.0350731 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M1 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0486437 | 0.0485101 | True |
| P-OLS-Z | OPEN30 | -2.0934 | -2.20523 | 0.111824 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| P-OLS-Z | MID_C | 0.35639 | 0.348534 | 0.0078566 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| P-OLS-Z | CLOSE_C | 2.04529 | 2.00498 | 0.0403132 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| P-OLS-Z | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0463601 | 0.0485101 | True |
| M2-T8 | OPEN30 | -3.46945e-16 | -2.20523 | 2.20523 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M2-T8 | MID_C | -2.60209e-16 | 0.348534 | -0.348534 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M2-T8 | CLOSE_C | -1.73472e-16 | 2.00498 | -2.00498 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M2-T8 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 1.25767e-17 | 0.0485101 | True |
| M4-T8-Z4 | OPEN30 | -2.51502 | -2.20523 | -0.309792 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M4-T8-Z4 | MID_C | 0.53831 | 0.348534 | 0.189776 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M4-T8-Z4 | CLOSE_C | 2.11664 | 2.00498 | 0.111656 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M4-T8-Z4 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0445911 | 0.0485101 | True |
| NOINT-T8-Z4 | OPEN30 | -3.46945e-16 | -2.20523 | 2.20523 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| NOINT-T8-Z4 | MID_C | -2.60209e-16 | 0.348534 | -0.348534 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| NOINT-T8-Z4 | CLOSE_C | -1.73472e-16 | 2.00498 | -2.00498 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| NOINT-T8-Z4 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 1.25767e-17 | 0.0485101 | True |
| M2-T12 | OPEN30 | 0 | -2.20523 | 2.20523 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M2-T12 | MID_C | -8.67362e-17 | 0.348534 | -0.348534 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M2-T12 | CLOSE_C | -3.46945e-16 | 2.00498 | -2.00498 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M2-T12 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 1.43115e-17 | 0.0485101 | True |
| M4-T12-Z4 | OPEN30 | -2.35395 | -2.20523 | -0.148728 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M4-T12-Z4 | MID_C | 0.420798 | 0.348534 | 0.0722642 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M4-T12-Z4 | CLOSE_C | 2.10079 | 2.00498 | 0.0958108 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| M4-T12-Z4 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0454283 | 0.0485101 | True |
| NOINT-T12-Z4 | OPEN30 | 0 | -2.20523 | 2.20523 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| NOINT-T12-Z4 | MID_C | -8.67362e-17 | 0.348534 | -0.348534 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| NOINT-T12-Z4 | CLOSE_C | -3.46945e-16 | 2.00498 | -2.00498 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN |
| NOINT-T12-Z4 | TV_HL | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 1.43115e-17 | 0.0485101 | True |


Fitted scientific contrasts average **whole predictions over the same observed P0 state rows**, not predictions at a group median or an isolated additive component. `model_fidelity_by_state_bin.csv` also records all per-bin raw/fitted means in three P0 cells and five train-quantile bins. The singleton training quantile slices in figures 8–9 are fitted surfaces; they do not identify pointwise population m(k,z). Anchored D uses k0=30 (12:00). All profile plots use the full 78 bins. Numerical discrepancy is model fidelity evidence, not proof that empirical means are population truth.

## Scalar coefficient, residual and specification diagnostics

HAC10 L1 slope nominal p=0.000121918, six-family Holm p=0.000731508; L3 joint slope interactions nominal p=0.0695374, Holm p=0.208612; L4 curvature nominal p=0.22821, Holm p=0.45642. These are conditional/asymptotic developmental associations. Within-state slopes do not by themselves establish differences between states; L3 uses a joint two-coefficient null. L2 levels, linear slope and quadratic curvature are distinct hypotheses.

| test | statistic | df | p_value | p_holm_fixed_six_family | family_size |
|---|---|---|---|---|---|
| linear_slope | 14.7628 | 1 | 0.000121918 | 0.000731508 | 6 |
| categorical_levels | 12.2421 | 2 | 0.00219612 | 0.00878447 | 6 |
| piecewise_slope_interactions | 5.33178 | 2 | 0.0695374 | 0.208612 | 6 |
| quadratic_curvature | 1.45198 | 1 | 0.22821 | 0.45642 | 6 |
| RAW_H1_direction | 3.3862 | NA / ABSTAIN | 0.00035434 | 0.0017717 | 6 |
| RAW_H1_gt_0.02 | 0.00841311 | NA / ABSTAIN | 0.496644 | 0.496644 | 6 |


The fixed six-member D_FULL family at lag10 contains L1 slope, L2 categorical levels, L3 slope interactions, L4 curvature, raw historical-label H1>0 and H1>0.02. H3 has a descriptive interval rather than an invented p-value. Holm covers this finite group only if the marginal p-values are valid; it does not undo P0-driven emphasis, dependent-data misspecification or post-inspection selection. The materiality null is separate from zero-direction. All conclusions of materiality/near-invariance remain NOT_CERTIFIED.

| context | model | n_days | rank | condition | R2 | adjusted_R2 | MSE | AIC | BIC | sd | skew | excess_kurtosis | white_p | koenker_p | jarque_bera_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D_FULL | OLS-L0 | 1472 | 1 | 1 | 3.33067e-16 | 3.33067e-16 | 0.00629749 | -3280.16 | -3274.86 | 0.0793837 | 1.68505 | 5.16118 | 0.386685 | 0.218872 | 0 |
| D_FULL | OLS-L1 | 1472 | 2 | 1 | 0.0142434 | 0.0135728 | 0.00620779 | -3299.28 | -3288.69 | 0.0788163 | 1.69503 | 5.19967 | 0.459684 | 0.357876 | 0 |
| D_FULL | OLS-L2 | 1472 | 3 | 3.73095 | 0.0116467 | 0.0103011 | 0.00622414 | -3293.4 | -3277.52 | 0.0789201 | 1.68382 | 5.12241 | 0.398403 | 0.27663 | 0 |
| D_FULL | OLS-L3 | 1472 | 6 | 17.7927 | 0.0182562 | 0.0149079 | 0.00618252 | -3297.28 | -3265.51 | 0.0786557 | 1.7007 | 5.24031 | 0.371736 | 0.317258 | 0 |
| D_FULL | OLS-L4 | 1472 | 3 | 2.80184 | 0.0156603 | 0.0143201 | 0.00619887 | -3299.39 | -3283.51 | 0.0787596 | 1.70573 | 5.27877 | 0.419067 | 0.334981 | 0 |
| DEV_2020 | OLS-L0 | 983 | 1 | 1 | 0 | 0 | 0.00538751 | -2343.24 | -2338.35 | 0.073437 | 1.95144 | 7.92618 | 0.238564 | 0.11912 | 0 |
| DEV_2020 | OLS-L1 | 983 | 2 | 1 | 0.00843854 | 0.00742777 | 0.00534205 | -2349.57 | -2339.79 | 0.0731265 | 1.93694 | 7.79812 | 0.354901 | 0.195491 | 0 |
| DEV_2020 | OLS-L2 | 983 | 3 | 3.73041 | 0.0106191 | 0.00859994 | 0.0053303 | -2349.73 | -2335.06 | 0.0730461 | 1.91336 | 7.63354 | 0.295298 | 0.147624 | 0 |
| DEV_2020 | OLS-L3 | 983 | 6 | 17.2438 | 0.0229556 | 0.0179554 | 0.00526384 | -2356.06 | -2326.72 | 0.0725892 | 1.92046 | 7.82814 | 0.325083 | 0.140271 | 0 |
| DEV_2020 | OLS-L4 | 983 | 3 | 2.76414 | 0.0179764 | 0.0159722 | 0.00529066 | -2357.07 | -2342.4 | 0.072774 | 1.95189 | 8.04238 | 0.344312 | 0.155058 | 0 |
| DEV_2021 | OLS-L0 | 1224 | 1 | 1 | 0 | 0 | 0.00651191 | -2686.2 | -2681.09 | 0.0807294 | 1.78511 | 5.65304 | 0.299783 | 0.176408 | 0 |
| DEV_2021 | OLS-L1 | 1224 | 2 | 1 | 0.0199843 | 0.0191824 | 0.00638178 | -2708.91 | -2698.69 | 0.0799187 | 1.80034 | 5.73907 | 0.371082 | 0.309332 | 0 |
| DEV_2021 | OLS-L2 | 1224 | 3 | 3.73205 | 0.0173842 | 0.0157747 | 0.00639871 | -2703.67 | -2688.34 | 0.0800246 | 1.7783 | 5.58873 | 0.303835 | 0.22643 | 0 |
| DEV_2021 | OLS-L3 | 1224 | 6 | 18.0163 | 0.0279316 | 0.0239412 | 0.00633002 | -2710.88 | -2680.22 | 0.079594 | 1.79671 | 5.76572 | 0.258806 | 0.248257 | 0 |
| DEV_2021 | OLS-L4 | 1224 | 3 | 2.81695 | 0.0212227 | 0.0196195 | 0.00637371 | -2708.46 | -2693.13 | 0.0798682 | 1.81233 | 5.82522 | 0.3346 | 0.28528 | 0 |


All coefficients, ordinary descriptive SE and conditional HAC5/10/20 intervals/p-values are in `scalar_ols_models_and_hac.csv`; same-cell closing-effect intervals in pp are in `scalar_contrasts_and_HAC.csv`. `scalar_summary.csv` includes SSE, Gaussian OLS AIC/BIC and full residual location/scale/MAD/tail quantiles. These scalar R²/AIC semantics are not assigned to profile smoothers. Feature correlations/VIF appear in `feature_collinearity.csv` (intercept VIF omitted); state dummies and interactions can be correlated by construction.

White and BP/Koenker use only the fixed small auxiliary design 1+z_s (White expands it), not a 78-dummy matrix. Their usual IID-reference p-values, JB, ARCH LM and Ljung–Box are heuristic under serial dependence/nonstationarity. ACF/PACF and squared-residual diagnostics use ordered eligible dates, so gaps are compressed for these descriptive plots/tests; scheduled-gap HAC and block resampling are separate. `serial_diagnostics.csv` supplies lags5/10/20 for scalar residuals and profile close residual/PC1/vector norms. Low-degree RESET and ordinary linear-vs-quadratic F tests are in `scalar_specification_tests.csv`; a RESET augmentation already in the column span is explicitly skipped. No flattened 78N regression p-value was used.

HAC uses Bartlett estimating-score covariances across original scheduled slots with missing-slot scores zero and n/(n−p) correction. It matches statsmodels on consecutive-slot fixtures; gaps are not imputed returns. Its nominal normal/chi-square limits require adequate moments, a suitable weak-dependence/stability law and valid selected-complete-session sampling assumptions; these are not proven for this market series. These caveats also apply to calendar sensitivities. No empirical result supplies a theorem-certified confidence event.

Influence output covers every scalar training fit in D_FULL and the two chronological origins: leverage, internal/external studentization, Cook, DFFITS and every DFBETA. Exact OLS deletion formulas were independently checked against statsmodels; no N refits were required. Thresholds: hat>2p/n, Cook>4/n, |external student|>3, |DFFITS|>2√(p/n), |DFBETA|>2/√n. Flagging is not deletion or causal importance. Top ten D_FULL L1 dates:

| date_et | hat | student_external | cooks | dffits |
|---|---|---|---|---|
| 2017-08-08 | 0.00437697 | 4.16537 | 0.0377183 | 0.27618 |
| 2018-02-05 | 0.00105162 | 7.85134 | 0.0311613 | 0.254742 |
| 2020-04-06 | 0.00474662 | 3.16898 | 0.0238011 | 0.218849 |
| 2020-04-07 | 0.00338357 | 3.53974 | 0.0211041 | 0.20625 |
| 2018-12-31 | 0.00368974 | 3.2052 | 0.0189038 | 0.195054 |
| 2020-03-11 | 0.00796046 | 2.05448 | 0.0168978 | 0.184037 |
| 2018-10-29 | 0.0042377 | 2.35995 | 0.0118142 | 0.153954 |
| 2018-03-27 | 0.00155447 | 3.82053 | 0.0112584 | 0.150749 |
| 2020-12-03 | 0.000719094 | 5.30405 | 0.00993893 | 0.142284 |
| 2018-09-26 | 0.00155486 | 3.53249 | 0.009641 | 0.139401 |


## Profile residuals and raw normalization

| model | n_days | MSE_profile | MAE_profile | raw_half_L1 | TV_valid_n | negative_below_tolerance | negative_mass | prediction_min | sum_defect_max | covariance_rank | first_PC_variance_fraction | edge_close_bias |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M0 | 1472 | 0.000215414 | 0.0082809 | 0.322955 | 1472 | 0 | 0 | 0.00687315 | 0 | 77 | 0.10214 | -3.01691e-17 |
| M1 | 1472 | 0.000214702 | 0.00826334 | 0.32227 | 1472 | 0 | 0 | 0.00632264 | 2.22045e-16 | 77 | 0.1015 | -1.05592e-17 |
| P-OLS-Z | 1472 | 0.000214759 | 0.00826176 | 0.322209 | 1472 | 0 | 0 | 0.00563734 | 5.55112e-16 | 77 | 0.101217 | 4.22367e-18 |
| M2-T8 | 1472 | 0.000218335 | 0.00834197 | 0.325337 | 1472 | 0 | 0 | 0.00728204 | 8.88178e-16 | 77 | 0.10214 | 0.00267688 |
| M4-T8-Z4 | 1472 | 0.000217619 | 0.00832316 | 0.324603 | 1472 | 0 | 0 | 0.0061651 | 2.44249e-15 | 77 | 0.101158 | 0.00267688 |
| NOINT-T8-Z4 | 1472 | 0.000218335 | 0.00834197 | 0.325337 | 1472 | 0 | 0 | 0.00728204 | 8.88178e-16 | 77 | 0.10214 | 0.00267688 |
| M2-T12 | 1472 | 0.000217682 | 0.00832715 | 0.324759 | 1472 | 0 | 0 | 0.00740528 | 1.11022e-16 | 77 | 0.10214 | 0.000478579 |
| M4-T12-Z4 | 1472 | 0.00021694 | 0.00830756 | 0.323995 | 1472 | 0 | 0 | 0.0068749 | 1.66533e-15 | 77 | 0.101174 | 0.000478579 |
| NOINT-T12-Z4 | 1472 | 0.000217682 | 0.00832715 | 0.324759 | 1472 | 0 | 0 | 0.00740528 | 1.11022e-16 | 77 | 0.10214 | 0.000478579 |


`profile_diagnostics.csv` records raw negative/>1 components, mass/range/sum defects, genuine-TV valid counts, all six window errors and error contributions, roughness/adjacent variation and edge bias. Half-L1 is retained for every raw prediction; TV_prediction is calculated only on simplex-valid dates and its valid n is always displayed, so invalid raw models are not ranked using a hidden normalization. No negative prediction was silently clipped. Roundoff tolerance is −1e−12/closure1e−10.

`profile_bin_residuals.csv` reports binwise variance/RMSE/MAE/skew/tails and state-residual covariance. `profile_daily_errors.csv` reports vector norm, PC1, MSE/MAE, close residual and state/year keys. `residual_covariance.npz` and `residual_eigenvalues.npz` preserve the empirical covariance/eigenvalue spectrum. Closure imposes at least one null direction; eigenvalues do not provide 78 independent significance tests. Daily scalar features, not stacked bins, enter serial/ARCH diagnostics. Low-df time smoothers can miss a sharp last-bin/auction proxy; report their approximation gap instead of expanding the frozen basis after seeing errors.

## All matched train and developmental comparison scores

Rows below include full descriptive training, both origin-training sets and both/pooled chronological evaluations. D_FULL train scores are in-sample only. Every eval candidate uses the same valid keys. Full unrounded MSE/MAE/half-L1/valid-TV and closing-share scores are in `model_scores.csv`.

| context | part | model | kind | n_days | MSE_profile | MAE_profile | raw_half_L1 | TV_valid_n | CLOSE_C_MSE | CLOSE_C_RMSE_pp | CLOSE_C_MAE_pp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D_FULL | TRAIN | OLS-L0 | scalar | 1472 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00629749 | 7.93567 | 5.91276 |
| D_FULL | TRAIN | OLS-L1 | scalar | 1472 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00620779 | 7.87895 | 5.85852 |
| D_FULL | TRAIN | OLS-L2 | scalar | 1472 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00622414 | 7.88932 | 5.8578 |
| D_FULL | TRAIN | OLS-L3 | scalar | 1472 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00618252 | 7.8629 | 5.82812 |
| D_FULL | TRAIN | OLS-L4 | scalar | 1472 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00619887 | 7.87329 | 5.84739 |
| D_FULL | TRAIN | M0 | profile | 1472 | 0.000215414 | 0.0082809 | 0.322955 | 1472 | 0.00629749 | 7.93567 | 5.91276 |
| D_FULL | TRAIN | M1 | profile | 1472 | 0.000214702 | 0.00826334 | 0.32227 | 1472 | 0.00622414 | 7.88932 | 5.8578 |
| D_FULL | TRAIN | P-OLS-Z | profile | 1472 | 0.000214759 | 0.00826176 | 0.322209 | 1472 | 0.00620779 | 7.87895 | 5.85852 |
| D_FULL | TRAIN | M2-T8 | profile | 1472 | 0.000218335 | 0.00834197 | 0.325337 | 1472 | 0.00630667 | 7.94146 | 5.8584 |
| D_FULL | TRAIN | M4-T8-Z4 | profile | 1472 | 0.000217619 | 0.00832316 | 0.324603 | 1472 | 0.00619649 | 7.87178 | 5.77763 |
| D_FULL | TRAIN | NOINT-T8-Z4 | profile | 1472 | 0.000218335 | 0.00834197 | 0.325337 | 1472 | 0.00630667 | 7.94146 | 5.8584 |
| D_FULL | TRAIN | M2-T12 | profile | 1472 | 0.000217682 | 0.00832715 | 0.324759 | 1472 | 0.00630304 | 7.93917 | 5.8697 |
| D_FULL | TRAIN | M4-T12-Z4 | profile | 1472 | 0.00021694 | 0.00830756 | 0.323995 | 1472 | 0.00619285 | 7.86947 | 5.78917 |
| D_FULL | TRAIN | NOINT-T12-Z4 | profile | 1472 | 0.000217682 | 0.00832715 | 0.324759 | 1472 | 0.00630304 | 7.93917 | 5.8697 |
| DEV_2020 | TRAIN | OLS-L0 | scalar | 983 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00538751 | 7.33997 | 5.38688 |
| DEV_2020 | EVAL | OLS-L0 | scalar | 241 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0116517 | 10.7943 | 7.50898 |
| DEV_2020 | TRAIN | OLS-L1 | scalar | 983 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00534205 | 7.30893 | 5.36017 |
| DEV_2020 | EVAL | OLS-L1 | scalar | 241 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0111082 | 10.5395 | 7.32981 |
| DEV_2020 | TRAIN | OLS-L2 | scalar | 983 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0053303 | 7.30089 | 5.36425 |
| DEV_2020 | EVAL | OLS-L2 | scalar | 241 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.011261 | 10.6118 | 7.32386 |
| DEV_2020 | TRAIN | OLS-L3 | scalar | 983 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00526384 | 7.25523 | 5.29371 |
| DEV_2020 | EVAL | OLS-L3 | scalar | 241 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0111422 | 10.5557 | 7.35023 |
| DEV_2020 | TRAIN | OLS-L4 | scalar | 983 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00529066 | 7.27369 | 5.31662 |
| DEV_2020 | EVAL | OLS-L4 | scalar | 241 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.011356 | 10.6564 | 7.46212 |
| DEV_2020 | TRAIN | M0 | profile | 983 | 0.000217393 | 0.00825795 | 0.32206 | 983 | 0.00538751 | 7.33997 | 5.38688 |
| DEV_2020 | EVAL | M0 | profile | 241 | 0.000214031 | 0.00840917 | 0.327958 | 241 | 0.0116517 | 10.7943 | 7.50898 |
| DEV_2020 | TRAIN | M1 | profile | 983 | 0.000216224 | 0.00823326 | 0.321097 | 983 | 0.0053303 | 7.30089 | 5.36425 |
| DEV_2020 | EVAL | M1 | profile | 241 | 0.000214534 | 0.00842739 | 0.328668 | 241 | 0.011261 | 10.6118 | 7.32386 |
| DEV_2020 | TRAIN | P-OLS-Z | profile | 983 | 0.000216285 | 0.00822594 | 0.320812 | 983 | 0.00534205 | 7.30893 | 5.36017 |
| DEV_2020 | EVAL | P-OLS-Z | profile | 241 | 0.000216973 | 0.00847823 | 0.330651 | 241 | 0.0111082 | 10.5395 | 7.32981 |
| DEV_2020 | TRAIN | M2-T8 | profile | 983 | 0.000220215 | 0.00831734 | 0.324376 | 983 | 0.00539525 | 7.34524 | 5.33063 |
| DEV_2020 | EVAL | M2-T8 | profile | 241 | 0.000215482 | 0.00843853 | 0.329103 | 241 | 0.0119544 | 10.9336 | 7.59812 |
| DEV_2020 | TRAIN | M4-T8-Z4 | profile | 983 | 0.000219072 | 0.00828539 | 0.32313 | 983 | 0.0052721 | 7.26092 | 5.24308 |
| DEV_2020 | EVAL | M4-T8-Z4 | profile | 241 | 0.000216641 | 0.00848206 | 0.3308 | 241 | 0.0114391 | 10.6954 | 7.41631 |
| DEV_2020 | TRAIN | NOINT-T8-Z4 | profile | 983 | 0.000220215 | 0.00831734 | 0.324376 | 983 | 0.00539525 | 7.34524 | 5.33063 |
| DEV_2020 | EVAL | NOINT-T8-Z4 | profile | 241 | 0.000215482 | 0.00843853 | 0.329103 | 241 | 0.0119544 | 10.9336 | 7.59812 |
| DEV_2020 | TRAIN | M2-T12 | profile | 983 | 0.000219662 | 0.00830385 | 0.32385 | 983 | 0.00539319 | 7.34383 | 5.33812 |
| DEV_2020 | EVAL | M2-T12 | profile | 241 | 0.0002147 | 0.00843132 | 0.328821 | 241 | 0.0119101 | 10.9133 | 7.58505 |
| DEV_2020 | TRAIN | M4-T12-Z4 | profile | 983 | 0.000218476 | 0.00826985 | 0.322524 | 983 | 0.00527004 | 7.2595 | 5.25066 |
| DEV_2020 | EVAL | M4-T12-Z4 | profile | 241 | 0.000215849 | 0.00847869 | 0.330669 | 241 | 0.0113995 | 10.6769 | 7.40873 |
| DEV_2020 | TRAIN | NOINT-T12-Z4 | profile | 983 | 0.000219662 | 0.00830385 | 0.32385 | 983 | 0.00539319 | 7.34383 | 5.33812 |
| DEV_2020 | EVAL | NOINT-T12-Z4 | profile | 241 | 0.0002147 | 0.00843132 | 0.328821 | 241 | 0.0119101 | 10.9133 | 7.58505 |
| DEV_2021 | TRAIN | OLS-L0 | scalar | 1224 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00651191 | 8.06964 | 5.96581 |
| DEV_2021 | EVAL | OLS-L0 | scalar | 248 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00524059 | 7.23919 | 5.59421 |
| DEV_2021 | TRAIN | OLS-L1 | scalar | 1224 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00638178 | 7.9886 | 5.88757 |
| DEV_2021 | EVAL | OLS-L1 | scalar | 248 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00536575 | 7.32513 | 5.63994 |
| DEV_2021 | TRAIN | OLS-L2 | scalar | 1224 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00639871 | 7.99919 | 5.88679 |
| DEV_2021 | EVAL | OLS-L2 | scalar | 248 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00538573 | 7.33875 | 5.66182 |
| DEV_2021 | TRAIN | OLS-L3 | scalar | 1224 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00633002 | 7.95615 | 5.83354 |
| DEV_2021 | EVAL | OLS-L3 | scalar | 248 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.005523 | 7.43169 | 5.68111 |
| DEV_2021 | TRAIN | OLS-L4 | scalar | 1224 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00637371 | 7.98355 | 5.87584 |
| DEV_2021 | EVAL | OLS-L4 | scalar | 248 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00535228 | 7.31593 | 5.62618 |
| DEV_2021 | TRAIN | M0 | profile | 1224 | 0.000216403 | 0.00828118 | 0.322966 | 1224 | 0.00651191 | 8.06964 | 5.96581 |
| DEV_2021 | EVAL | M0 | profile | 248 | 0.000211296 | 0.00831769 | 0.32439 | 248 | 0.00524059 | 7.23919 | 5.59421 |
| DEV_2021 | TRAIN | M1 | profile | 1224 | 0.000215429 | 0.00825936 | 0.322115 | 1224 | 0.00639871 | 7.99919 | 5.88679 |
| DEV_2021 | EVAL | M1 | profile | 248 | 0.00021207 | 0.00833836 | 0.325196 | 248 | 0.00538573 | 7.33875 | 5.66182 |
| DEV_2021 | TRAIN | P-OLS-Z | profile | 1224 | 0.000215539 | 0.0082575 | 0.322043 | 1224 | 0.00638178 | 7.9886 | 5.88757 |
| DEV_2021 | EVAL | P-OLS-Z | profile | 248 | 0.000211832 | 0.0083283 | 0.324804 | 248 | 0.00536575 | 7.32513 | 5.63994 |
| DEV_2021 | TRAIN | M2-T8 | profile | 1224 | 0.000219092 | 0.00833912 | 0.325226 | 1224 | 0.00652007 | 8.0747 | 5.9118 |
| DEV_2021 | EVAL | M2-T8 | profile | 248 | 0.000215017 | 0.00838764 | 0.327118 | 248 | 0.00526518 | 7.25615 | 5.56489 |
| DEV_2021 | TRAIN | M4-T8-Z4 | profile | 1224 | 0.000218127 | 0.00831455 | 0.324267 | 1224 | 0.00635945 | 7.97462 | 5.79369 |
| DEV_2021 | EVAL | M4-T8-Z4 | profile | 248 | 0.000215735 | 0.00840462 | 0.32778 | 248 | 0.00544172 | 7.3768 | 5.62275 |
| DEV_2021 | TRAIN | NOINT-T8-Z4 | profile | 1224 | 0.000219092 | 0.00833912 | 0.325226 | 1224 | 0.00652007 | 8.0747 | 5.9118 |
| DEV_2021 | EVAL | NOINT-T8-Z4 | profile | 248 | 0.000215017 | 0.00838764 | 0.327118 | 248 | 0.00526518 | 7.25615 | 5.56489 |
| DEV_2021 | TRAIN | M2-T12 | profile | 1224 | 0.00021849 | 0.00832569 | 0.324702 | 1224 | 0.00651733 | 8.073 | 5.9212 |
| DEV_2021 | EVAL | M2-T12 | profile | 248 | 0.00021413 | 0.00837183 | 0.326501 | 248 | 0.00525939 | 7.25216 | 5.57001 |
| DEV_2021 | TRAIN | M4-T12-Z4 | profile | 1224 | 0.000217478 | 0.00829982 | 0.323693 | 1224 | 0.0063567 | 7.97289 | 5.8037 |
| DEV_2021 | EVAL | M4-T12-Z4 | profile | 248 | 0.00021496 | 0.00839288 | 0.327322 | 248 | 0.00543338 | 7.37114 | 5.62633 |
| DEV_2021 | TRAIN | NOINT-T12-Z4 | profile | 1224 | 0.00021849 | 0.00832569 | 0.324702 | 1224 | 0.00651733 | 8.073 | 5.9212 |
| DEV_2021 | EVAL | NOINT-T12-Z4 | profile | 248 | 0.00021413 | 0.00837183 | 0.326501 | 248 | 0.00525939 | 7.25216 | 5.57001 |
| DEV_POOLED_2020_2021 | EVAL | M0 | profile | 489 | 0.000212644 | 0.00836278 | 0.326148 | 489 | 0.00840025 | 9.16529 | 6.53789 |
| DEV_POOLED_2020_2021 | EVAL | M1 | profile | 489 | 0.000213284 | 0.00838224 | 0.326907 | 489 | 0.00828133 | 9.10018 | 6.48094 |
| DEV_POOLED_2020_2021 | EVAL | P-OLS-Z | profile | 489 | 0.000214366 | 0.00840219 | 0.327686 | 489 | 0.00819586 | 9.0531 | 6.47278 |
| DEV_POOLED_2020_2021 | EVAL | M2-T8 | profile | 489 | 0.000215247 | 0.00841272 | 0.328096 | 489 | 0.0085619 | 9.25305 | 6.56695 |
| DEV_POOLED_2020_2021 | EVAL | M2-T12 | profile | 489 | 0.00021441 | 0.00840115 | 0.327645 | 489 | 0.00853712 | 9.23965 | 6.56311 |
| DEV_POOLED_2020_2021 | EVAL | M4-T8-Z4 | profile | 489 | 0.000216181 | 0.00844279 | 0.329269 | 489 | 0.00839747 | 9.16377 | 6.50669 |
| DEV_POOLED_2020_2021 | EVAL | M4-T12-Z4 | profile | 489 | 0.000215398 | 0.00843517 | 0.328972 | 489 | 0.00837374 | 9.15082 | 6.50477 |
| DEV_POOLED_2020_2021 | EVAL | NOINT-T8-Z4 | profile | 489 | 0.000215247 | 0.00841272 | 0.328096 | 489 | 0.0085619 | 9.25305 | 6.56695 |
| DEV_POOLED_2020_2021 | EVAL | NOINT-T12-Z4 | profile | 489 | 0.00021441 | 0.00840115 | 0.327645 | 489 | 0.00853712 | 9.23965 | 6.56311 |
| DEV_POOLED_2020_2021 | EVAL | OLS-L0 | scalar | 489 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00840025 | 9.16529 | 6.53789 |
| DEV_POOLED_2020_2021 | EVAL | OLS-L1 | scalar | 489 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00819586 | 9.0531 | 6.47278 |
| DEV_POOLED_2020_2021 | EVAL | OLS-L2 | scalar | 489 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00828133 | 9.10018 | 6.48094 |
| DEV_POOLED_2020_2021 | EVAL | OLS-L3 | scalar | 489 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.0082924 | 9.10626 | 6.50372 |
| DEV_POOLED_2020_2021 | EVAL | OLS-L4 | scalar | 489 | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | NA / ABSTAIN | 0.00831115 | 9.11655 | 6.53101 |


| model | baseline | metric | n_days | mean_loss_difference | HAC_lo | HAC_hi | block_lo | block_hi |
|---|---|---|---|---|---|---|---|---|
| M1 | M0 | profile_mse | 489 | 6.40144e-07 | -6.69154e-08 | 1.3472e-06 | -1.04632e-08 | 1.33642e-06 |
| M1 | M0 | close_mse | 489 | -0.000118925 | -0.000327923 | 9.0072e-05 | -0.000320975 | 8.05452e-05 |
| P-OLS-Z | M0 | profile_mse | 489 | 1.72167e-06 | 5.00539e-07 | 2.94279e-06 | 6.89039e-07 | 2.941e-06 |
| P-OLS-Z | M0 | close_mse | 489 | -0.000204395 | -0.000436319 | 2.75285e-05 | -0.000446007 | -8.45617e-06 |
| M4-T8-Z4 | M0 | profile_mse | 489 | 3.53731e-06 | 2.33175e-06 | 4.74286e-06 | 2.37418e-06 | 4.70965e-06 |
| M4-T8-Z4 | M0 | close_mse | 489 | -2.78186e-06 | -0.000341758 | 0.000336195 | -0.000346113 | 0.000297684 |
| M4-T8-Z4 | M2-T8 | profile_mse | 489 | 9.34884e-07 | 1.19827e-07 | 1.74994e-06 | 1.13279e-07 | 1.76095e-06 |
| M4-T8-Z4 | M2-T8 | close_mse | 489 | -0.000164426 | -0.000513581 | 0.000184729 | -0.000521901 | 0.00013645 |
| M4-T8-Z4 | P-OLS-Z | profile_mse | 489 | 1.81564e-06 | 1.26148e-07 | 3.50513e-06 | 9.78774e-08 | 3.30342e-06 |
| M4-T8-Z4 | P-OLS-Z | close_mse | 489 | 0.000201613 | 4.8275e-05 | 0.000354952 | 5.67862e-05 | 0.000338573 |
| M4-T12-Z4 | M4-T8-Z4 | profile_mse | 489 | -7.83256e-07 | -1.10424e-06 | -4.62276e-07 | -1.11894e-06 | -4.42313e-07 |
| M4-T12-Z4 | M4-T8-Z4 | close_mse | 489 | -2.37263e-05 | -3.56505e-05 | -1.1802e-05 | -3.60462e-05 | -1.25336e-05 |


The table above shows pooled HAC10 and joint-date block10 intervals; the CSV also includes each year and all lag/block5/10/20 settings. Negative loss difference favors the first model. Forecasts remain fixed within resampling; no full learner/selection bootstrap is claimed. A scalar closing-share improvement is not recovery of the whole 78-vector. The same M0 closing mean equals OLS-L0 and the sum of P-OLS-Z's closing bins equals OLS-L1, both checked numerically. The no-interaction spline ablation is constrained by response closure, not evidence from a software term chart.

## Support, environments and robustness

| context | group | n_days | five_session_groups | display_ok | basic_ok | strong_ok | Z0_mean | close_mean | close_sd |
|---|---|---|---|---|---|---|---|---|---|
| 2016-2019 | 0 | 391 | 132 | True | True | True | -11.5865 | 0.157419 | 0.067078 |
| 2016-2019 | 1 | 337 | 146 | True | True | True | -10.61 | 0.15998 | 0.068908 |
| 2016-2019 | 2 | 255 | 93 | True | True | True | -9.31488 | 0.174321 | 0.0864402 |
| 2020 | 0 | 21 | 10 | False | False | False | -11.3948 | 0.227846 | 0.110698 |
| 2020 | 1 | 62 | 30 | True | True | False | -10.5199 | 0.239329 | 0.118166 |
| 2020 | 2 | 158 | 43 | True | True | True | -8.95634 | 0.204818 | 0.078897 |
| 2021 | 0 | 79 | 30 | True | True | False | -11.4575 | 0.184615 | 0.0783027 |
| 2021 | 1 | 92 | 42 | True | True | False | -10.5864 | 0.166263 | 0.0680261 |
| 2021 | 2 | 77 | 30 | True | True | False | -9.4267 | 0.178785 | 0.070997 |


Display/basic/strong gates are 30/10, 50/20, 100/30 distinct dates/five-session index groups. Groups are support bookkeeping, not certified independent clusters. The early training quintile cells define common coarse support for environment TV; unsupported comparisons are ABSTAIN in `environment_TV.csv` and the gallery. Marginal environment curves mix different state distributions; conditional cell comparisons are a different object. No reweighting, hidden pooling or causal explanation was introduced. Continuous query bands use train rank±0.1; ranges/density/counts and masks are in `support_and_environment.csv`.

Raw sensitivity contrasts use original P0 labels and fixed windows. Changed-training fits legitimately recompute means/SD/cutpoints/knots, all saved. FULL always leads. DROP_TOP1_RV removes 15 current-RV extremes (threshold 0.000507293); it is outcome-conditioned D-only, never a deployable predictor. EXCLUDE_2020 changes the calendar distribution severely. DROP_TOP5_INFLUENTIAL uses the same five D_FULL OLS-L1 Cook dates for every model: 2017-08-08, 2018-02-05, 2020-04-06, 2020-04-07, 2018-12-31. No model-specific favorable exclusions were selected. LOYO refits exclude each calendar year; they can train on future years and are explicitly NOT walk-forward OOS. Unsupported left-year high/low scientific contrasts abstain.

| context | window | n_days | estimate_pp | TV |
|---|---|---|---|---|
| FULL | CLOSE_C | 1472 | 2.00498 | NA / ABSTAIN |
| FULL | TV_HL | 1472 | NA / ABSTAIN | 0.0485101 |
| DROP_TOP1_RV | CLOSE_C | 1457 | 1.83902 | NA / ABSTAIN |
| DROP_TOP1_RV | TV_HL | 1457 | NA / ABSTAIN | 0.0469033 |
| EXCLUDE_2020 | CLOSE_C | 1231 | 1.33669 | NA / ABSTAIN |
| EXCLUDE_2020 | TV_HL | 1231 | NA / ABSTAIN | 0.0509409 |
| DROP_TOP5_INFLUENTIAL | CLOSE_C | 1467 | 1.7791 | NA / ABSTAIN |
| DROP_TOP5_INFLUENTIAL | TV_HL | 1467 | NA / ABSTAIN | 0.0478376 |


| context | model | n_train | n_eval | mode | MSE_profile | CLOSE_C_RMSE_pp | scalar_model_HL_pp |
|---|---|---|---|---|---|---|---|
| DROP_TOP1_RV | OLS-L1 | 1457 | 1457 | RETROSPECTIVE_SENSITIVITY | NA / ABSTAIN | 7.85044 | 1.78664 |
| DROP_TOP1_RV | M2-T8 | 1457 | 1457 | RETROSPECTIVE_SENSITIVITY | 0.000218105 | 7.89836 | NA / ABSTAIN |
| DROP_TOP1_RV | M4-T8-Z4 | 1457 | 1457 | RETROSPECTIVE_SENSITIVITY | 0.00021747 | 7.8433 | NA / ABSTAIN |
| EXCLUDE_2020 | OLS-L1 | 1231 | 1231 | RETROSPECTIVE_SENSITIVITY | NA / ABSTAIN | 7.31796 | 1.23459 |
| EXCLUDE_2020 | M2-T8 | 1231 | 1231 | RETROSPECTIVE_SENSITIVITY | 0.000219138 | 7.34425 | NA / ABSTAIN |
| EXCLUDE_2020 | M4-T8-Z4 | 1231 | 1231 | RETROSPECTIVE_SENSITIVITY | 0.000218399 | 7.29254 | NA / ABSTAIN |
| DROP_TOP5_INFLUENTIAL | OLS-L1 | 1467 | 1467 | RETROSPECTIVE_SENSITIVITY | NA / ABSTAIN | 7.59342 | 1.83215 |
| DROP_TOP5_INFLUENTIAL | M2-T8 | 1467 | 1467 | RETROSPECTIVE_SENSITIVITY | 0.00021609 | 7.64622 | NA / ABSTAIN |
| DROP_TOP5_INFLUENTIAL | M4-T8-Z4 | 1467 | 1467 | RETROSPECTIVE_SENSITIVITY | 0.000215443 | 7.59557 | NA / ABSTAIN |
| LOYO_2016 | OLS-L1 | 1225 | 247 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | NA / ABSTAIN | 6.67644 | 1.84438 |
| LOYO_2016 | M2-T8 | 1225 | 247 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000180493 | 6.57833 | NA / ABSTAIN |
| LOYO_2016 | M4-T8-Z4 | 1225 | 247 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000179575 | 6.50594 | NA / ABSTAIN |
| LOYO_2017 | OLS-L1 | 1225 | 247 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | NA / ABSTAIN | 7.1571 | NA / ABSTAIN |
| LOYO_2017 | M2-T8 | 1225 | 247 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.00021657 | 7.2455 | NA / ABSTAIN |
| LOYO_2017 | M4-T8-Z4 | 1225 | 247 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000218025 | 7.10882 | NA / ABSTAIN |
| LOYO_2018 | OLS-L1 | 1227 | 245 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | NA / ABSTAIN | 8.60308 | 1.71187 |
| LOYO_2018 | M2-T8 | 1227 | 245 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000180501 | 8.7562 | NA / ABSTAIN |
| LOYO_2018 | M4-T8-Z4 | 1227 | 245 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000178888 | 8.57906 | NA / ABSTAIN |
| LOYO_2019 | OLS-L1 | 1228 | 244 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | NA / ABSTAIN | 7.14565 | 2.07297 |
| LOYO_2019 | M2-T8 | 1228 | 244 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000307573 | 7.01129 | NA / ABSTAIN |
| LOYO_2019 | M4-T8-Z4 | 1228 | 244 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000307335 | 7.10742 | NA / ABSTAIN |
| LOYO_2020 | OLS-L1 | 1231 | 241 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | NA / ABSTAIN | 10.4685 | NA / ABSTAIN |
| LOYO_2020 | M2-T8 | 1231 | 241 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000214957 | 10.8102 | NA / ABSTAIN |
| LOYO_2020 | M4-T8-Z4 | 1231 | 241 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000215188 | 10.6191 | NA / ABSTAIN |
| LOYO_2021 | OLS-L1 | 1224 | 248 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | NA / ABSTAIN | 7.32513 | 2.06887 |
| LOYO_2021 | M2-T8 | 1224 | 248 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000215017 | 7.25615 | NA / ABSTAIN |
| LOYO_2021 | M4-T8-Z4 | 1224 | 248 | LEAVE_YEAR_OUT_NOT_WALK_FORWARD | 0.000215735 | 7.3768 | NA / ABSTAIN |


Last 15:55 bin contribution to raw H1: -0.3471 pp. Closing numerator excluding only that bin: +2.3521 pp, compared with primary +2.0050 pp. This retains the whole-day denominator but changes the diagnostic numerator; it is not a selected replacement target. The predeclared 14:00–14:10 diagnostic is -0.0710 pp; without an authentic FOMC calendar no event mechanism is inferred. No missing crisis date was filled or removed twice.

## QA, reproducibility, limitations and successor gate

Independent output checks recomputed 84 core train/eval model scores, pooled profile scores, all historical group curves and same-cell fitted means from coefficients/original arrays, to 1e−10 (scores atol1e−12). All 14 principal PNGs decode, are nonblank and ≥1600px; numeric source references and hashes are in `plots_manifest.json`. A contact sheet supports human visual review. Synthetic checks cover tensor/explicit design equivalence, natural-tail/basis accounting, daily OLS/HAC/influence against trusted references, source/P0 math via existing tests, chronology cutpoints, immutable state features under target changes, rank failure, TV labels, joint blocks and output smoke. Exact executed test results and any repairs are in the dated session report/provenance QA. Images are not 78 independent tests.

Run commands: `.venv/bin/python -B scripts/c2r_development_models.py prepare`, then `run`, then `report`; `python -B -m unittest discover -s tests -p 'test_c*.py' -v`. The existing frozen protocol is never overwritten by prepare. Restore authorized matching P0 sources/state lookup, install the recorded existing package versions, export EBM_DATA_ROOT if needed, and use the installed package from a clean clone. No source/API/credentials are needed for C2R. Forecast files store dates/source-row references and predictions only, never a second Q matrix or per-fold input table.

Source/model/config/environment identities, timing, protected-file rechecks, zero socket/API transfer and retained bytes are recorded in provenance and the coding-session report. The prior C1R narrative has a pandas Series.mode formatting defect in its state table; its machine state ledger is correct and both were preserved unchanged. Current C2R uses explicit column access and its own verified state meanings. No scientific protocol redesign was required. No 2022–2026 scientific values, downloads, EBM fits or independent evaluation occurred.

**Recommendation:** C2R methods/QA support reviewing a bounded C3 **design** with strong M0/M1/P-OLS baselines and the declared spline approximation limitations exposed. The developmental score ranking does not establish an EBM opportunity or authorize fitting C3. Retain negative/unstable comparisons, raw normalization and support abstentions. Actual C3 execution requires a new user instruction and frozen stage settings. Full-C materiality, near-invariance, raw pointwise certification and independent forecast improvement remain NOT_CERTIFIED/DEFERRED.

## REQUESTED_DECISIONS_FOR_FULL_C

Only dependent future choices remain: exact full-C horizon; Q-first/mask-later versus Z0-first split population; Zret close-anchor/half-day policy; Zvol older-eligible/strict-chain lookback, epsilon and volume provenance; and explicit future-source/reserved-data authority. No official 60/20/20 dates or independent C evaluation are released here.

## Completion of conditional means, calibration and environment residual audits

These requested diagnostics use the saved frozen coefficients and original dated arrays, **without refitting or changing any candidate/forecast**. Group-mean intervals condition on the fitted training cuts/design; they are conditional-mean estimation intervals, not individual-day prediction intervals or selection-aware confidence statements. The direct P0 fixed-label reference and origin-training model S0 remain distinct.

| model | state | n_group | mean_pp | SE_pp | lo_pp | hi_pp |
|---|---|---|---|---|---|---|
| OLS-L0 | 0 | 491 | 17.3606 | 0.296158 | 16.7801 | 17.941 |
| OLS-L0 | 1 | 490 | 17.3606 | 0.296158 | 16.7801 | 17.941 |
| OLS-L0 | 2 | 491 | 17.3606 | 0.296158 | 16.7801 | 17.941 |
| OLS-L1 | 0 | 491 | 16.3989 | 0.374261 | 15.6654 | 17.1325 |
| OLS-L1 | 1 | 490 | 17.2399 | 0.275305 | 16.7003 | 17.7795 |
| OLS-L1 | 2 | 491 | 18.4426 | 0.387766 | 17.6826 | 19.2026 |
| OLS-L2 | 0 | 491 | 16.4806 | 0.42937 | 15.6391 | 17.3222 |
| OLS-L2 | 1 | 490 | 17.0798 | 0.440103 | 16.2172 | 17.9424 |
| OLS-L2 | 2 | 491 | 18.5207 | 0.430921 | 17.6761 | 19.3653 |
| OLS-L3 | 0 | 491 | 16.4806 | 0.430673 | 15.6365 | 17.3248 |
| OLS-L3 | 1 | 490 | 17.0798 | 0.433962 | 16.2292 | 17.9303 |
| OLS-L3 | 2 | 491 | 18.5207 | 0.399657 | 17.7374 | 19.304 |
| OLS-L4 | 0 | 491 | 16.5773 | 0.374889 | 15.8425 | 17.3121 |
| OLS-L4 | 1 | 490 | 17.0624 | 0.331283 | 16.4131 | 17.7117 |
| OLS-L4 | 2 | 491 | 18.4414 | 0.366127 | 17.7238 | 19.159 |

All ordinary/HAC5/10/20 group means for the three core training contexts are in `scalar_conditional_means_and_hac.csv`. Fixed fitted-value quintile calibration, year and scheduled-five-session block residual means are in `scalar_calibration.csv` and `scalar_residual_period_means.csv`; figure14 displays them and PACF. Train/eval error/bias gaps, exact origin state ranges/cuts/quantiles and state-specific vector errors are in `model_train_eval_gaps.csv`, `origin_state_inventory.csv` and `profile_errors_by_state.csv`.

| context | part | n_days | Z0_min | Z0_max | low_cut | high_cut | q10 | q25 | q50 | q75 | q90 | out_of_training_range_n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D_FULL | TRAIN | 1472 | -12.9858 | -5.97455 | -11.0456 | -10.1187 | -11.7085 | -11.2611 | -10.6109 | -9.79972 | -8.94778 | 0 |
| D_FULL | EVAL | 1472 | -12.9858 | -5.97455 | -11.0456 | -10.1187 | -11.7085 | -11.2611 | -10.6109 | -9.79972 | -8.94778 | 0 |
| DEV_2020 | TRAIN | 983 | -12.9858 | -7.21999 | -11.2021 | -10.3135 | -11.8182 | -11.3972 | -10.8264 | -10.0797 | -9.22207 | 0 |
| DEV_2020 | EVAL | 241 | -12.0321 | -5.97455 | -11.2021 | -10.3135 | -10.9631 | -10.3846 | -9.68466 | -8.82878 | -8.06667 | 11 |
| DEV_2021 | TRAIN | 1224 | -12.9858 | -5.97455 | -11.0615 | -10.1078 | -11.7285 | -11.2713 | -10.6109 | -9.76933 | -8.83847 | 0 |
| DEV_2021 | EVAL | 248 | -12.1983 | -7.93195 | -11.0615 | -10.1078 | -11.6091 | -11.1684 | -10.6138 | -9.94113 | -9.22427 | 0 |

Raw normalization on **each chronological evaluation** (including state extrapolation) follows. TV scores only cover simplex-valid dates; half-L1 always covers all dates.

| context | model | n_days | TV_valid_n | negative_below_tolerance | prediction_min | sum_defect_max |
|---|---|---|---|---|---|---|
| DEV_2020 | M0 | 241 | 241 | 0 | 0.00709475 | 2.22045e-16 |
| DEV_2020 | M1 | 241 | 241 | 0 | 0.0060168 | 2.22045e-16 |
| DEV_2020 | P-OLS-Z | 241 | 241 | 0 | 0.0061573 | 3.33067e-16 |
| DEV_2020 | M2-T8 | 241 | 241 | 0 | 0.00753396 | 4.44089e-16 |
| DEV_2020 | M4-T8-Z4 | 241 | 241 | 0 | 0.00704988 | 2.88658e-15 |
| DEV_2020 | NOINT-T8-Z4 | 241 | 241 | 0 | 0.00753396 | 4.44089e-16 |
| DEV_2020 | M2-T12 | 241 | 241 | 0 | 0.00771142 | 1.11022e-16 |
| DEV_2020 | M4-T12-Z4 | 241 | 241 | 0 | 0.00725289 | 1.77636e-15 |
| DEV_2020 | NOINT-T12-Z4 | 241 | 241 | 0 | 0.00771142 | 1.11022e-16 |
| DEV_2021 | M0 | 248 | 248 | 0 | 0.00695951 | 1.11022e-16 |
| DEV_2021 | M1 | 248 | 248 | 0 | 0.00639525 | 1.11022e-16 |
| DEV_2021 | P-OLS-Z | 248 | 248 | 0 | 0.00605168 | 8.88178e-16 |
| DEV_2021 | M2-T8 | 248 | 248 | 0 | 0.00737867 | 8.88178e-16 |
| DEV_2021 | M4-T8-Z4 | 248 | 248 | 0 | 0.00703876 | 1.55431e-15 |
| DEV_2021 | NOINT-T8-Z4 | 248 | 248 | 0 | 0.00737867 | 8.88178e-16 |
| DEV_2021 | M2-T12 | 248 | 248 | 0 | 0.00754025 | 1.11022e-16 |
| DEV_2021 | M4-T12-Z4 | 248 | 248 | 0 | 0.00716194 | 9.99201e-16 |
| DEV_2021 | NOINT-T12-Z4 | 248 | 248 | 0 | 0.00754025 | 1.11022e-16 |

Residual environment discrepancies are in `environment_residual_discrepancy.csv`: same 2016–2019 training-defined coarse quintile cells and the same D_FULL fitted model, basic-support masks enforced. Residual vectors are not probability curves, so the statistic is explicitly **residual half-L1 shift**, not probability TV. It remains descriptive; numeric state distributions can differ inside a cell, and the shared full-development fit is not independent. No reweighting or causal attribution is implied.

| environment | cell | model | n_early | n_environment | residual_half_L1_shift | status | caveat |
|---|---|---|---|---|---|---|---|
| 2020 | 0 | M0 | 197 | 6 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 0 | P-OLS-Z | 197 | 6 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 0 | M4-T8-Z4 | 197 | 6 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 1 | M0 | 196 | 15 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 1 | P-OLS-Z | 196 | 15 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 1 | M4-T8-Z4 | 196 | 15 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 2 | M0 | 197 | 29 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 2 | P-OLS-Z | 197 | 29 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 2 | M4-T8-Z4 | 197 | 29 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 3 | M0 | 196 | 53 | 0.0880213 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 3 | P-OLS-Z | 196 | 53 | 0.0880073 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 3 | M4-T8-Z4 | 196 | 53 | 0.0879493 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 4 | M0 | 197 | 138 | 0.0629972 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 4 | P-OLS-Z | 197 | 138 | 0.064207 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2020 | 4 | M4-T8-Z4 | 197 | 138 | 0.0611755 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 0 | M0 | 197 | 32 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 0 | P-OLS-Z | 197 | 32 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 0 | M4-T8-Z4 | 197 | 32 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 1 | M0 | 196 | 47 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 1 | P-OLS-Z | 196 | 47 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 1 | M4-T8-Z4 | 196 | 47 | NA / ABSTAIN | ABSTAIN_SUPPORT | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 2 | M0 | 197 | 52 | 0.0680267 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 2 | P-OLS-Z | 197 | 52 | 0.068001 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 2 | M4-T8-Z4 | 197 | 52 | 0.0683315 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 3 | M0 | 196 | 58 | 0.0752276 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 3 | P-OLS-Z | 196 | 58 | 0.0749569 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 3 | M4-T8-Z4 | 196 | 58 | 0.0747439 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 4 | M0 | 197 | 59 | 0.106206 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 4 | P-OLS-Z | 197 | 59 | 0.104794 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |
| 2021 | 4 | M4-T8-Z4 | 197 | 59 | 0.106112 | SUPPORTED_DESCRIPTIVE_COARSE_CELL | D_FULL shared fit; within-cell Z0 mixtures can still differ; not pointwise or causal drift |

Final reporting completion command: `python -B -m ebm_research.experiment_c.c2r_completion` after the `report` action. It computes the requested additional diagnostics from saved coefficients, with no new fit. On a clone containing the frozen protocol, use `run` directly; `prepare` deliberately refuses to overwrite an existing freeze. The final focused suite is **22/22 PASS**; the final audit preserves all 417 baseline files and all original source hashes. `fit_hashes.csv` records all 168 context/model identities.

In the conditional-mean table, mean_pp/lo_pp/hi_pp are closing share fractions multiplied by 100 (a level of 17 means 17% of daily variance); high-minus-low differences are percentage points. QQ residual values use fractions, while the other scalar residual panels use pp. The empty fitted-value calibration bins caused by ties are explicitly ABSTAIN, not zero means.
