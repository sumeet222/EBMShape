# C3 one-state EBM scientific results — development only

**C3_PASS_WITH_QUALIFICATIONS.** All five native families and the normalized M8 comparator were fitted on the exact matched cohort; architecture, source, time-resolution and daily score checks pass. Native interactions produce fitted state/time structure, but extra scientific fidelity and generalizing full-profile prediction are **NOT ESTABLISHED**. This is a sound negative developmental result, not proof that state information has zero population value.

This study uses 1,472 previously explored SPY dates (2016-01-05–2021-12-31), 78 five-minute allocation bins per date. The raw target is squared minute log returns normalized by the complete same-day RTH total; Z0 is log RV from the immediately preceding scheduled complete ordinary session. No overnight RV, same-day state, additional indicator, 2022+ C outcome, reserved B value, network transfer or raw source copy was used. The 1,491 Q-valid population is coverage only. Twelve early closes and seven incomplete ordinary days remain excluded, including four March 2020 crisis dates. R1 E-mini/open-VIX/latent periodicity is not replicated by this SPY proxy.

## What the ladder establishes

The native time feature retains all 78 nominal categories in main and pair mappings (with missing/unseen reserves). Exact graphs are T0 f(k); M3c f(k)+g(Z0); M3d f(k)+g(S0); M5 and M6 add exactly the k/state pair. Numeric Z0 is binned and stepwise; it is not a smooth derivative model. Unit rows give every date equal total fitting weight. Inference/evaluation always uses a whole date.

Fixed cyclic boosting uses validation_size=0, outer_bags=1, inner_bags=0, early_stopping_rounds=0, greedy_ratio=0, smoothing_rounds=0 and interaction_smoothing_rounds=0. Native error bands are not scientific intervals. T0 uses A (200 rounds, 2 leaves); matched additive/interaction pairs use selected B (400 rounds, 3 leaves, 16 numeric state bins). Both use max_bins=128 and max_interaction_bins=96. Configuration B won the predeclared combined-pair daily MSE criterion on inner folds 2016–17→2018 (494/245) and 2016–18→2019 (739/244). No 2020/21 scores selected settings. T0 versus M3 also changes time-training complexity; M0 supplies the stronger exact unsmoothed time-only comparator, and pairwise M3/M5 and M3d/M6 have identical complexity settings.

All balanced normalized Q rows have mean 1/78 across k. A pure native additive state shift consequently collapses to numerical zero here; observed raw M3c/M3d closure passes and their anchored D is zero. The general warning that additive vertical state shifts can violate closure still matters, but was not an empirical defect in these fits. Interactions do have small native closure defects. Their raw high-low half-L1 is not labeled TV. Separately named NORM variants use positive-part rescaling with uniform fallback when total positive mass is zero. These are different prediction maps and cannot inherit the native graph interpretation.

M8 is not an EBM: p=softmax(a+b*z_scaled), with a and b centered across 78 bins (154 identifiable coefficients). It minimizes mean daily cross entropy +0.001/2 Σb², using training-only Z0 mean/SD, stable logsumexp and analytic L-BFGS-B gradients. This is a proper log-score mean model, subsequently evaluated using the common MSE. One penalty was frozen without outcome tuning. All three solvers converged with max gradient <2e−6; all predictions are positive and sum to one.

## Predictive comparison on fixed forecasts

DEV2020 trains through 2019 (983 dates), forecasts 241 dates; DEV2021 trains through 2020 (1,224), forecasts 248. Pooled 489 dates are unique and matched. These years were explored in P0, so the term development backcheck is mandatory. D_FULL is in-sample. Stored C2R parameters/forecasts were reused without refitting their matrix.

Train-only transform register (origin-specific; full fit is descriptive):

| origin | n_train | Z0_mean | Z0_sd | S0_low_cut | S0_high_cut | Z0_min | Z0_max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D_FULL | 1472 | -10.457 | 1.0839 | -11.0456 | -10.1187 | -12.9858 | -5.97455 |
| DEV_2020 | 983 | -10.6625 | 0.998593 | -11.2021 | -10.3135 | -12.9858 | -7.21999 |
| DEV_2021 | 1224 | -10.4476 | 1.11977 | -11.0615 | -10.1078 | -12.9858 | -5.97455 |

Inner-fold mean daily MSE, including both screened settings:

| model | config | MSE |
| --- | --- | --- |
| M3c_EBM_ADDITIVE | A | 0.000242337 |
| M3c_EBM_ADDITIVE | B | 0.000242353 |
| M3d_EBM_ADDITIVE | A | 0.000242337 |
| M3d_EBM_ADDITIVE | B | 0.000242353 |
| M5_EBM_CONT_INTERACT | A | 0.000241636 |
| M5_EBM_CONT_INTERACT | B | 0.000241427 |
| M6_EBM_DISC_INTERACT | A | 0.000242147 |
| M6_EBM_DISC_INTERACT | B | 0.000242074 |
| T0_EBM_TIME_ONLY | A | 0.000242337 |

Pooled developmental scorecard:

| model | n_days | MSE_profile | versus_M0_percent | CLOSE_C_RMSE_pp | TV_valid_n | sum_defect_max |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | 489 | 0.000212644 | 0 | 9.16529 | 489 | 2.22045e-16 |
| M1 | 489 | 0.000213284 | 0.30104 | 9.10018 | 489 | 2.22045e-16 |
| P-OLS-Z | 489 | 0.000214366 | 0.809646 | 9.0531 | 489 | 8.88178e-16 |
| M2-T8 | 489 | 0.000215247 | 1.22384 | 9.25305 | 489 | 8.88178e-16 |
| M4-T8-Z4 | 489 | 0.000216181 | 1.66349 | 9.16377 | 489 | 2.88658e-15 |
| M2-T12 | 489 | 0.00021441 | 0.83066 | 9.23965 | 489 | 1.11022e-16 |
| M4-T12-Z4 | 489 | 0.000215398 | 1.29514 | 9.15082 | 489 | 1.77636e-15 |
| T0_EBM_TIME_ONLY | 489 | 0.000213858 | 0.570729 | 9.22335 | 489 | 0 |
| M3c_EBM_ADDITIVE | 489 | 0.000212654 | 0.00441262 | 9.16587 | 489 | 6.66134e-16 |
| M3d_EBM_ADDITIVE | 489 | 0.000212654 | 0.00441262 | 9.16587 | 489 | 3.33067e-16 |
| M5_EBM_CONT_INTERACT | 489 | 0.000213411 | 0.360768 | 9.13862 | 0 | 0.00910292 |
| M6_EBM_DISC_INTERACT | 489 | 0.00021287 | 0.106441 | 9.1066 | 0 | 0.00373103 |
| M8 | 489 | 0.000214098 | 0.683617 | 9.0554 | 489 | 1.11022e-15 |
| NORM_M3c_EBM_ADDITIVE | 489 | 0.000212654 | 0.00441262 | 9.16587 | 489 | 2.22045e-16 |
| NORM_M3d_EBM_ADDITIVE | 489 | 0.000212654 | 0.00441262 | 9.16587 | 489 | 0 |
| NORM_M5_EBM_CONT_INTERACT | 489 | 0.000213412 | 0.361152 | 9.12576 | 489 | 2.22045e-16 |
| NORM_M6_EBM_DISC_INTERACT | 489 | 0.000212867 | 0.10479 | 9.10084 | 489 | 4.44089e-16 |

Full training/year/pooled scores: [profile metrics](../../artifacts/C/C3_one_state_ebm_v1_1/profile_predictive_metrics.csv), all six window definitions and calibration: [window metrics](../../artifacts/C/C3_one_state_ebm_v1_1/window_prediction_metrics.csv). Closing-share improvements are a separate objective from profile prediction. Native M5/M6 recover some closing allocation, yet the simple P-OLS-Z has lower pooled closing RMSE.

## Named conditional comparison family

Negative first-minus-baseline favors the first model. Intervals below condition on the frozen selected forecasts; they do not cover learner selection or future-law change. HAC uses Bartlett scheduled-session score lags, with missing eligible sessions contributing zero scores rather than fabricated Q. Shared circular scheduled-slot block resamples use B=1,000 and lengths 5/10/20, with gaps kept and circular end wrap disclosed. Holm applies only to the five named HAC10 marginal reference tests under their unverified validity premises. No 78-bin p-value family was manufactured.

| first | baseline | metric | difference | relative_percent | HAC_lo | HAC_hi | block_lo | block_hi | Holm_p_conditional |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M5_EBM_CONT_INTERACT | M3c_EBM_ADDITIVE | MSE_profile | 7.57768e-07 | 0.356339 | 1.08275e-07 | 1.40726e-06 | 7.94328e-08 | 1.39903e-06 | 0.0818898 |
| M6_EBM_DISC_INTERACT | M3d_EBM_ADDITIVE | MSE_profile | 2.16957e-07 | 0.102024 | -3.20925e-07 | 7.54838e-07 | -3.33937e-07 | 7.46373e-07 | 0.858386 |
| M5_EBM_CONT_INTERACT | M6_EBM_DISC_INTERACT | MSE_profile | 5.40811e-07 | 0.254056 | 1.60848e-07 | 9.20775e-07 | 1.68711e-07 | 9.43759e-07 | 0.0263772 |
| M5_EBM_CONT_INTERACT | M0 | MSE_profile | 7.67151e-07 | 0.360768 | 1.18362e-07 | 1.41594e-06 | 8.78394e-08 | 1.40784e-06 | 0.0818898 |
| M5_EBM_CONT_INTERACT | M3c_EBM_ADDITIVE | CLOSE_C_MSE | -4.98819e-05 | -0.593738 | -0.000253866 | 0.000154102 | -0.000267499 | 0.000127414 | 0.858386 |

M5 has worse profile MSE than M0 and matched M3c; its apparent closing-error reduction is inconclusive. M5 is also worse than M6 on the conditional profile comparison (Holm reference p≈0.0264); this does not certify that terciles preserve population information. All 11 pairs, two objectives and lags, including M5/M8, M6/M8, T0/M0, are retained in [paired tests](../../artifacts/C/C3_one_state_ebm_v1_1/paired_loss_tests.csv) and [year/state differences](../../artifacts/C/C3_one_state_ebm_v1_1/paired_loss_by_year_state.csv).

## Same-row scientific fidelity

H1 is high-minus-low CLOSE_C [66:78], fractions converted to pp below. H3 is TV only for valid whole normalized profiles. D(k;30) is calculated from complete predictions, never an isolated native term. Historical P0 rank cells and origin-specific train S0 cells are labeled separately. Raw high-low means at continuous singleton Z0 are not identified by fitted slices.

| model | H1 | H1_error | H3_TV | half_L1 | D_max | last_bin | other_close_bins |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RAW | 2.00498 | 0 | 0.0485101 | 0.0485101 | 0.00740016 | -0.347111 | 2.35209 |
| M0 | -3.46945e-16 | -2.00498 | 1.60462e-17 | 1.60462e-17 | 3.46945e-18 | 0 | -3.46945e-16 |
| M1 | 2.04005 | 0.0350731 | 0.0486437 | 0.0486437 | 0.00742928 | -0.348849 | 2.3889 |
| P-OLS-Z | 2.04529 | 0.0403132 | 0.0463601 | 0.0463601 | 0.00754673 | -0.308702 | 2.354 |
| M2-T8 | -1.73472e-16 | -2.00498 | 1.25767e-17 | 1.25767e-17 | 6.93889e-18 | 0 | -1.73472e-16 |
| M4-T8-Z4 | 2.11664 | 0.111656 | 0.0445911 | 0.0445911 | 0.00763448 | -0.191637 | 2.30827 |
| M2-T12 | -3.46945e-16 | -2.00498 | 1.43115e-17 | 1.43115e-17 | 3.46945e-18 | 0 | -3.46945e-16 |
| M4-T12-Z4 | 2.10079 | 0.0958108 | 0.0454283 | 0.0454283 | 0.00859582 | -0.20722 | 2.30801 |
| T0_EBM_TIME_ONLY | 6.93889e-16 | -2.00498 | 1.30104e-17 | 1.30104e-17 | 3.46945e-18 | 0 | 6.93889e-16 |
| M3c_EBM_ADDITIVE | 5.0307e-15 | -2.00498 | 7.80626e-17 | 7.80626e-17 | 4.85723e-17 | 0 | 5.0307e-15 |
| M3d_EBM_ADDITIVE | 6.93889e-16 | -2.00498 | 3.51282e-17 | 3.51282e-17 | 8.67362e-18 | 0 | 6.93889e-16 |
| M5_EBM_CONT_INTERACT | 1.56544 | -0.439544 | — | 0.0338914 | 0.00741178 | -0.193504 | 1.75894 |
| M6_EBM_DISC_INTERACT | 1.39458 | -0.610403 | — | 0.0298352 | 0.00597904 | -0.236527 | 1.63111 |
| M8 | 1.90375 | -0.101233 | 0.0431457 | 0.0431457 | 0.00749889 | -0.2958 | 2.19955 |
| NORM_M3c_EBM_ADDITIVE | -1.73472e-16 | -2.00498 | 2.73219e-17 | 2.73219e-17 | 1.38778e-17 | -3.46945e-16 | 1.73472e-16 |
| NORM_M3d_EBM_ADDITIVE | 6.93889e-16 | -2.00498 | 3.25261e-17 | 3.25261e-17 | 8.67362e-18 | 0 | 6.93889e-16 |
| NORM_M5_EBM_CONT_INTERACT | 1.58665 | -0.418332 | 0.0338652 | 0.0338652 | 0.00737199 | -0.19053 | 1.77718 |
| NORM_M6_EBM_DISC_INTERACT | 1.4407 | -0.564285 | 0.0297908 | 0.0297908 | 0.00590434 | -0.229215 | 1.66991 |

The direct +2.005pp H1 is descriptive and not certified above 2pp. M5≈+1.565pp and M6≈+1.395pp attenuate it more than P-OLS-Z≈+2.045pp or M8≈+1.904pp. Raw TV≈0.04851 is not an upper confidence/equivalence certificate below 0.05. The 15:55 raw contribution is −0.347pp while the other closing bins contribute +2.352pp; omitting the last bin is explicitly exploratory and never changes primary CLOSE_C. Full 78-bin fidelity, D, window errors and cell counts are machine outputs, with joint fixed-fit descriptive intervals at all three block lengths.

## Support, environments and coarsening

Support gates count distinct dates and original five-session groups: display 30/10, basic 50/20, strong 100/30; these are operational gates rather than independence proofs. Low-state 2020 has 21 dates using the retrospective/full-S0 population and fails basic support. All high-low environmental claims involving that cell are ABSTAIN_SUPPORT, even when native model outputs are finite. Numeric state-bin occupancy, training quantile neighborhoods, extrapolation counts and native cutpoints are retained separately. DEV2020 has 11 numeric states above its training range. No imputation or extrapolated raw-mean identification is made.

Model environment residual curves and half-L1 differences versus 2016–19 are in `environment_residual_discrepancy.csv`; unsupported cells are excluded from the scientific plot. Raw marginal differences and conditional supported-cell diagnostics are separate, and do not identify a pandemic mechanism. The separately named D_FULL_S0_reference2016_19_reweighted_coarse_mean fixes the 2016–19 S0 frequencies and averages each year’s same-state raw/residual profiles. It is not the original marginal estimand: `environment_reference_reweighted.csv` reports the supported 2021 comparison and ABSTAIN for 2020 because low-state overlap fails. M5/M6 coarsening reports within-tercile M5 dispersion, 16 versus 3 bins, profile losses and whole-model contrast differences. These are finite learned-resolution diagnostics, not an information-preserving coarsening theorem.

## Residual, temporal and stress diagnostics

Daily residual L2/PC1, full covariance/eigenvalues/closure, per-bin/state bias/RMSE/MAE, annual/quarterly mean errors, calibration quintiles, close-share tails, residual QQ and ACF/PACF/Ljung–Box/squared-residual/ARCH5/10/20 diagnostics are retained. Usual diagnostic p-values are heuristic under heavy tails, serial dependence and regime shifts. Eligible-date ACF compresses gaps and is labeled; HAC/block inference preserves scheduled gaps. No EBM hat matrix, Cook statistic, classical regression AIC or Gaussian likelihood claim is fabricated. The five deleted Cook dates come unchanged from C2R OLS-L1, never native EBM influence.

| model | lag | acf | squared_acf | ljung_box_p | squared_ljung_box_p | arch_p |
| --- | --- | --- | --- | --- | --- | --- |
| M5_EBM_CONT_INTERACT | 5 | 0.123248 | -0.029574 | 0.000455246 | 0.95467 | 0.955575 |
| M5_EBM_CONT_INTERACT | 10 | 0.160904 | 0.0406774 | 1.63909e-12 | 0.763996 | 0.736832 |
| M5_EBM_CONT_INTERACT | 20 | 0.0983506 | 0.0255996 | 3.61934e-15 | 0.0217722 | 0.0195849 |
| M6_EBM_DISC_INTERACT | 5 | 0.13245 | -0.0274991 | 0.000151609 | 0.965854 | 0.966568 |
| M6_EBM_DISC_INTERACT | 10 | 0.158881 | 0.0392171 | 2.27784e-13 | 0.77508 | 0.753145 |
| M6_EBM_DISC_INTERACT | 20 | 0.109247 | 0.0238639 | 5.83693e-17 | 0.0238767 | 0.0226272 |
| M8 | 5 | 0.119242 | -0.0323469 | 0.00159814 | 0.92845 | 0.92953 |
| M8 | 10 | 0.152321 | 0.0427424 | 5.0113e-11 | 0.73684 | 0.706239 |
| M8 | 20 | 0.0975466 | 0.0247597 | 3.25935e-13 | 0.0215317 | 0.0187458 |

Actual stress refits (all seed42, D_FULL descriptive; training transforms relearned on each retained cohort, historical P0 comparison labels held fixed):

| context | model | n_days | H1_pp | MSE_profile |
| --- | --- | --- | --- | --- |
| EXCLUDE_2020 | M3c_EBM_ADDITIVE | 1231 | 8.32667e-15 | 0.00021618 |
| EXCLUDE_2020 | M3d_EBM_ADDITIVE | 1231 | 8.50015e-15 | 0.00021618 |
| EXCLUDE_2020 | M5_EBM_CONT_INTERACT | 1231 | 0.776722 | 0.000215324 |
| EXCLUDE_2020 | M6_EBM_DISC_INTERACT | 1231 | 0.90006 | 0.000215653 |
| DROP_TOP1_RV | M3c_EBM_ADDITIVE | 1457 | 8.50015e-15 | 0.000215183 |
| DROP_TOP1_RV | M3d_EBM_ADDITIVE | 1457 | 4.68375e-15 | 0.000215183 |
| DROP_TOP1_RV | M5_EBM_CONT_INTERACT | 1457 | 1.49698 | 0.000214431 |
| DROP_TOP1_RV | M6_EBM_DISC_INTERACT | 1457 | 1.20607 | 0.000214728 |
| DROP_TOP5_INFLUENTIAL | M5_EBM_CONT_INTERACT | 1467 | 1.45148 | 0.000212431 |
| DROP_TOP5_INFLUENTIAL | M6_EBM_DISC_INTERACT | 1467 | 1.1715 | 0.000212725 |

TOP1 removes the exact C2R 15 current-day largest R dates; EXCLUDE_2020 and the fixed five OLS Cook dates are identical across native families. Separately labeled FIXED_FULL_SCORE rows retain the full model and change only the scored dates. EXCLUDE2020 and TOP1 have both additive/interaction pairs; TOP5 has M5/M6 only. Native LOYO and TOP5 additive refits are NOT_PERFORMED_RESOURCE under the frozen 59-fit plan. Three named seeds (42,123,2025) on both development origins differ at most about 1.1e−17 in predictions: algorithmic determinism, not population robustness. Full-process learner/bootstrap selection uncertainty is deferred: a single resample rebuilding 18 inner native fits plus one final fit would cost about 19 fits, roughly 19,000 fits for B=1,000, well outside 60. No nominal 95% raw population curve CI is supplied.

## Results ledger and stage decision

| Claim | Verdict | Reason |
|---|---|---|
| ADDITIVE_VS_INTERACTION_SUPPORTED | NOT_ESTABLISHED as reliable increment | Nonzero fitted D is real software structure; developmental profile MSE does not improve and raw-law uncertainty is uncalibrated |
| EBM_EXTRA_FIDELITY_SUPPORTED | NOT_ESTABLISHED | M5/M6 attenuate raw H1 more than P-OLS-Z/M8; full shape discrepancies remain |
| EBM_PREDICTION_INCREMENT_SUPPORTED | NOT_ESTABLISHED | Neither interaction beats M0; M5 worse than matched additive control |
| CONTINUOUS_VS_DISCRETE_INFORMATION_LOSS_DESCRIPTIVE | COMPLETED | Same raw state, train-only terciles versus numeric bins, finite losses/dispersion retained |
| SHAPE_STABILITY | INCONCLUSIVE; ABSTAIN for low-2020 | Composition, incomplete crisis dates, stress sensitivity and no joint raw event |
| POPULATION_INFERENCE | NOT_CERTIFIED | Dependence/selection/smoothness/support hypotheses unverified |

The implementation/QA verdict is separate from the negative scientific increment conclusion. Read [the theory audit](C3_one_state_EBM_theory_applicability.md) and [17-figure gallery](C3_one_state_EBM_figures_for_human_review.md). Any C4 proposal should first justify an added state against the strong M0/simple/M8 controls and support failures. C4/C5/C6 execution is not authorized by this result; no reserved outcomes were opened.
