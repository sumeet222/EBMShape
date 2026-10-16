# Experiment B Stage 1 — modern-period partial-method reproduction / hypothesis check

**PASS WITH QUALIFICATIONS.** This is a daily-table implementation and training-only descriptive benchmark gate, not historical source-era replication, an OOS result, nonlinear shape evidence or a profitability claim. No EBM, spline, trading, permutation, validation-outcome analysis or sealed-test outcome analysis was performed. Experiment A remains on hold.

## Frozen source and daily definitions

Principal: immutable `B_alpaca_sip_SPY_1m_split_D2_v1` plus exactly `B_spy_hf_source1_D2_1c_v1`, selected in `config/B_stage1_dataset_selection.json` before scientific calculations. Original Alpaca-only and exclusion of all terminal-repair-dependent dates are predeclared sensitivities. No D2.1b rows are combined. Source manifests/config/code and the single daily table are hashed in [manifest](../../data/registry/B_stage1_daily_manifest.json).

The daily table has **2680 scheduled full-session rows / 2675 eligible**, 2016-01-04–2026-09-30; first eligible 2016-01-05. The 21 early sessions are excluded by the real XNYS schedule and linked by the original D2 QA. Pprev is the preceding permissible full-session 15:59 close, skipping scheduled early closes only; a missing full close invalidates the next day. P10/P15/P1530/P16 are minute closes at 09:59/14:59/15:29/15:59 bar starts. Simple r1=P10/Pprev−1, r12=P1530/P15−1, r13=P16/P1530−1; X/W/Y are 10,000 times these returns. No 16:00-start, daily aggregate or after-hours prices are substituted.

Opening RV uses log(C09:30/O09:30) and 29 consecutive close/close logs; RV=√Σq², Z=log(RV+1e−8), requiring all 30 positive valid OHLC bars. Overnight is included in X and excluded from RV. E uses X/RV only at 10:00; L can additionally use W at 15:30; Y completes at 16:00. Availability columns express earliest bar completion, **not observed vendor delivery latency or executable fills**.

## Coverage and chronology QA

| dimension | period | full_sessions | eligible | excluded | first_eligible | last_eligible |
| --- | --- | --- | --- | --- | --- | --- |
| year | 2016 | 251 | 250 | 1 | 2016-01-05 | 2016-12-30 |
| year | 2017 | 249 | 249 | 0 | 2017-01-03 | 2017-12-29 |
| year | 2018 | 248 | 248 | 0 | 2018-01-02 | 2018-12-31 |
| year | 2019 | 249 | 249 | 0 | 2019-01-02 | 2019-12-31 |
| year | 2020 | 251 | 248 | 3 | 2020-01-02 | 2020-12-31 |
| year | 2021 | 251 | 251 | 0 | 2021-01-04 | 2021-12-31 |
| year | 2022 | 250 | 250 | 0 | 2022-01-03 | 2022-12-30 |
| year | 2023 | 248 | 247 | 1 | 2023-01-03 | 2023-12-29 |
| year | 2024 | 249 | 249 | 0 | 2024-01-02 | 2024-12-31 |
| year | 2025 | 247 | 247 | 0 | 2025-01-02 | 2025-12-31 |
| year | 2026 | 187 | 187 | 0 | 2026-01-02 | 2026-09-30 |
| split | sealed_test | 683 | 683 | 0 | 2024-01-02 | 2026-09-30 |
| split | train | 1499 | 1495 | 4 | 2016-01-05 | 2021-12-31 |
| split | validation | 498 | 497 | 1 | 2022-01-03 | 2023-12-29 |

Original eligibility 2673 → principal 2675; newly eligible **2019-08-12, 2019-08-13**. Original 104 absent minutes −39 accepted keys =65 remaining; this full-session accounting reuses the saved complete-session audit because nonrequired prices were discarded at D2. Fresh retained-window checks reproduce 91-window eligibility and all original eligibility flags. Feb 2, 2016 repairs are midday only and do not change scientific features. Aug 12 closing repairs change that day's label/W and Aug 13 prior-close X. Both days are flagged for terminal-dependency sensitivity; Aug 12's terminal 28 repaired bars have one-sided support and documented maximum cross-feed discrepancies (close 5.557 bp, high 5.904 bp, low 10.767 bp; see D2.1c).

Excluded full sessions:

| session_et | eligibility_reason |
| --- | --- |
| 2016-01-04 | MISSING_PRIOR_FULL_ANCHOR |
| 2020-03-09 | INCOMPLETE_OPENING_30;INCOMPLETE_REQUIRED_91 |
| 2020-03-12 | INCOMPLETE_OPENING_30;INCOMPLETE_REQUIRED_91 |
| 2020-03-16 | INCOMPLETE_OPENING_30;INCOMPLETE_REQUIRED_91 |
| 2023-06-05 | INCOMPLETE_OPENING_30;INCOMPLETE_REQUIRED_91 |

Missing/invalid counts and source use:

| view | missing_Pprev | missing_P10 | missing_P15 | missing_P1530 | missing_P16 | missing_opening_bars | incomplete_opening_days | invalid_ohlc_rows | zero_rv | negative_rv | invalid_rv_complete |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| principal | 1 | 0 | 0 | 0 | 0 | 46 | 4 | 0 | 0 | 0 | 0 |
| alpaca_only | 2 | 0 | 0 | 1 | 1 | 46 | 4 | 0 | 0 | 0 | 0 |

Repaired use: {"prior_anchor_repaired": 1, "repaired_1459": 0, "repaired_late": 1, "repaired_minutes_session": 39, "repaired_opening": 0, "repaired_other": 9, "repaired_target": 29, "terminal_repair_dependency": 2}. Zero duplicate daily keys; all minute keys/timezones/session mappings and information-time bounds checked. 21 full days skip an intervening scheduled early close; weekend/holiday elapsed periods remain explicit. QA examples show winter 09:59 ET=14:59 UTC and summer=13:59 UTC; 2024-12-02 uses 2024-11-27 full close and skips Nov 29 half-day. The leading 2016-01-04 lacks its 2015-12-31 anchor, with no fabrication or backward substitution. Incomplete opening sessions are March 9/12/16, 2020 and June 5, 2023; no filling. Strict RV losses are 4 / 2679 (0.1493%), below the frozen 2% QA screen.

All full-session daily-count-available and ≥500 flags are true (preserved from authenticated Alpaca daily counts, not recomputed from minute counts or asserted TAQ-equivalent). Daily close values were not retained in D2, so a new full-series close discrepancy cannot be calculated offline. D1 already observed daily-minus-minute −$0.045 to +$0.100 on its diagnostic cohort; no repeated sealed-price summary was produced here and minute anchors remain authoritative. Adjustment is split-only on original rows; community native-price adjustment semantics remain unverified beyond D2.1c local alignment. Actual split-event fidelity remains untested. Only the issuer-verified D1 ex-dividend example 2026-09-18 is flagged; other dates have **unknown** event status, not false/no-event assertions. No dividend subtraction or bad-gap filtering is applied to natural price returns.

Independent real-data scalar calculation on 2016-01-05 reproduces r1=-0.000348276033634, r12=-0.000592003973181, r13=0.000989908105519, RV=0.0036081229714, within atol1e−14/rtol1e−12. The five source price anchors and calculation are in the private, hashed manual-check artifact; no raw candle export is tracked. Four new focused tests plus seven existing tests cover RV/return formulas, missing inputs, timing/DST/half-day/calendar behavior, sealed guards, Parquet smoke and OLS/HAC against an independent tiny calculation.

## Required training regression trio

All principal models use **1495 eligible dates, 2016-01-05–2021-12-31**. Validation 2022–2023 is deliberately reserved for Stage 2; combined pretest and sealed outcome summaries are not run. Intercepts are bp; slopes are bp/bp, hence dimensionless. R² here is **in-sample**. Ordinary OLS standard errors are descriptive comparators. Statsmodels 0.15.0 HAC uses Bartlett weights, lag5 primary, covariance correction n/(n−k), asymptotic normal two-sided p-values/CIs (`use_t=False`); lag10/20 are sensitivity, not source-paper settings. Serial lags count successive eligible daily observations (gaps not padded). HAC validity relies on appropriate weak dependence/regularity; crisis missingness and finite-sample uncertainty remain qualifications.

| model | term | n | coefficient | ordinary_se | r_squared | hac_se | ci_low | ci_high | p_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OLS1_E | intercept | 1495 | -0.37131 | 0.87013 | 0.000711736 | 1.08904 | -2.50579 | 1.76317 | 0.73314 |
| OLS1_E | x_open_bp | 1495 | -0.0130066 | 0.0126131 | 0.000711736 | 0.030629 | -0.0730385 | 0.0470252 | 0.671092 |
| OLS2_L | intercept | 1495 | -0.44082 | 0.866824 | 0.000522399 | 1.05147 | -2.50167 | 1.62003 | 0.675041 |
| OLS2_L | w_preclose_bp | 1495 | -0.0385155 | 0.0436004 | 0.000522399 | 0.134167 | -0.301477 | 0.224446 | 0.774057 |
| OLS3_L | intercept | 1495 | -0.362183 | 0.870268 | 0.00121251 | 1.0901 | -2.49875 | 1.77438 | 0.739703 |
| OLS3_L | x_open_bp | 1495 | -0.0128096 | 0.0126162 | 0.00121251 | 0.0306374 | -0.0728578 | 0.0472386 | 0.675872 |
| OLS3_L | w_preclose_bp | 1495 | -0.037716 | 0.0436071 | 0.00121251 | 0.132585 | -0.297578 | 0.222146 | 0.776053 |

### HAC lag sensitivity (unchanged coefficients)

| model | term | hac_lag | hac_se | ci_low | ci_high | p_value |
| --- | --- | --- | --- | --- | --- | --- |
| OLS1_E | x_open_bp | 5 | 0.030629 | -0.0730385 | 0.0470252 | 0.671092 |
| OLS1_E | x_open_bp | 10 | 0.0278928 | -0.0676756 | 0.0416623 | 0.640996 |
| OLS1_E | x_open_bp | 20 | 0.0274012 | -0.066712 | 0.0406987 | 0.635019 |
| OLS2_L | w_preclose_bp | 5 | 0.134167 | -0.301477 | 0.224446 | 0.774057 |
| OLS2_L | w_preclose_bp | 10 | 0.13012 | -0.293545 | 0.216514 | 0.76723 |
| OLS2_L | w_preclose_bp | 20 | 0.13013 | -0.293566 | 0.216535 | 0.767248 |
| OLS3_L | x_open_bp | 5 | 0.0306374 | -0.0728578 | 0.0472386 | 0.675872 |
| OLS3_L | w_preclose_bp | 5 | 0.132585 | -0.297578 | 0.222146 | 0.776053 |
| OLS3_L | x_open_bp | 10 | 0.028359 | -0.0683923 | 0.0427731 | 0.65149 |
| OLS3_L | w_preclose_bp | 10 | 0.12884 | -0.290238 | 0.214806 | 0.769725 |
| OLS3_L | x_open_bp | 20 | 0.0281893 | -0.0680597 | 0.0424405 | 0.649532 |
| OLS3_L | w_preclose_bp | 20 | 0.128183 | -0.28895 | 0.213518 | 0.768578 |

## Retrospective RV terciles and direct moderation contrast

Eligible principal **training-only** linear empirical RV cutoffs: [0.001558374721607106, 0.0024281183976187152]; log equivalents [-6.46410542902094, -6.02063452513255]. Units: dimensionless √Σlog-return² and natural log(RV+1e−8). Counts {'low': 499, 'middle': 498, 'high': 498}; equality goes in lower bin. These are retrospective descriptive states on this cohort. They are also **preliminary train-only candidate cutoffs** for future validation, not claimed as past-known historical forecasts. No validation/test distributions set boundaries. Separate original-only own-cohort retrospective metadata and matched-cohort fixed-principal cutoffs are recorded in the state JSON.

| model | n | first | last | coefficient | ordinary_se | hac_se | ci_low | ci_high | p_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RV_low | 499 | 2016-03-14 | 2021-11-18 | -0.000968466 | 0.0199161 | 0.0182316 | -0.0367018 | 0.0347649 | 0.957636 |
| RV_middle | 498 | 2016-02-17 | 2021-12-31 | -0.0491743 | 0.0185906 | 0.0244701 | -0.0971348 | -0.00121387 | 0.0444767 |
| RV_high | 498 | 2016-01-05 | 2021-12-21 | -0.00761854 | 0.022687 | 0.0378442 | -0.0817918 | 0.0665547 | 0.840454 |

Pooled model has group-specific intercepts and X slopes; `high_minus_low_slope` is the explicit two-sided H0:βhigh−βlow=0 contrast. HAC is computed on the entire chronological training cohort, retaining cross-group error dependence, rather than subtracting separately estimated variances. Separate-bin HAC uses within-bin observation order. Inference **conditions on estimated tercile boundaries**, without a full cutoff-estimation bootstrap; it tests an association in this saturated linear projection, not causal moderation, raw conditional means, nonlinear shape, or EBM benefit.

| term | n | coefficient | ordinary_se | hac_lag | hac_se | ci_low | ci_high | p_value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_minus_low_slope | 1495 | -0.00665008 | 0.0543679 | 5 | 0.0425233 | -0.0899942 | 0.076694 | 0.875728 |
| high_minus_low_slope | 1495 | -0.00665008 | 0.0543679 | 10 | 0.0394481 | -0.0839669 | 0.0706668 | 0.866129 |
| high_minus_low_slope | 1495 | -0.00665008 | 0.0543679 | 20 | 0.0390253 | -0.0831383 | 0.0698382 | 0.864692 |

All three X-only RV-bin slopes are negative; ordering by point estimate is low > high > middle. The middle-bin HAC5 interval just excludes zero, while the other two and the pooled high-minus-low interval span zero. The required unconditional/multivariate trio slopes are also negative with HAC5 intervals spanning zero. Thus this training description does not corroborate the published positive-slope pattern or establish a high-minus-low difference. This is not evidence of population equality, a confirmed structural break, or a failed implementation. A significant slope in one state alone would not establish a between-state difference. These are descriptive exploratory diagnostics with multiple coefficients/lags, not familywise-confirmed discoveries.

## Source and terminal-repair sensitivity

Training-only own eligible cohorts, exact matched dates, and terminal-dependency exclusions use the same frozen formulas. All share principal training state cutoffs for fixed-cutoff comparisons; the original's own retrospective state table is additionally explicit in machine outputs. Exact matched scientific columns agree: **True** on 1493 training dates. Cohort entry (two repair-dependent dates), rather than replacement of Alpaca values, explains principal versus original changes. The terminal exclusion removes **2019-08-12, 2019-08-13** and propagates the prior-anchor dependency. No sensitivity was selected by coefficient sign.

| cohort | model | term | n | coefficient | hac_se | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- |
| alpaca_only | OLS1_E | x_open_bp | 1493 | -0.0127794 | 0.030775 | -0.0730974 | 0.0475385 |
| alpaca_only | OLS2_L | w_preclose_bp | 1493 | -0.0388392 | 0.134245 | -0.301954 | 0.224276 |
| alpaca_only | OLS3_L | x_open_bp | 1493 | -0.0125661 | 0.0307851 | -0.0729038 | 0.0477717 |
| alpaca_only | OLS3_L | w_preclose_bp | 1493 | -0.0379997 | 0.132704 | -0.298095 | 0.222096 |
| principal_matched | OLS1_E | x_open_bp | 1493 | -0.0127794 | 0.030775 | -0.0730974 | 0.0475385 |
| principal_matched | OLS2_L | w_preclose_bp | 1493 | -0.0388392 | 0.134245 | -0.301954 | 0.224276 |
| principal_matched | OLS3_L | x_open_bp | 1493 | -0.0125661 | 0.0307851 | -0.0729038 | 0.0477717 |
| principal_matched | OLS3_L | w_preclose_bp | 1493 | -0.0379997 | 0.132704 | -0.298095 | 0.222096 |
| alpaca_matched | OLS1_E | x_open_bp | 1493 | -0.0127794 | 0.030775 | -0.0730974 | 0.0475385 |
| alpaca_matched | OLS2_L | w_preclose_bp | 1493 | -0.0388392 | 0.134245 | -0.301954 | 0.224276 |
| alpaca_matched | OLS3_L | x_open_bp | 1493 | -0.0125661 | 0.0307851 | -0.0729038 | 0.0477717 |
| alpaca_matched | OLS3_L | w_preclose_bp | 1493 | -0.0379997 | 0.132704 | -0.298095 | 0.222096 |
| exclude_terminal_dependency | OLS1_E | x_open_bp | 1493 | -0.0127794 | 0.030775 | -0.0730974 | 0.0475385 |
| exclude_terminal_dependency | OLS2_L | w_preclose_bp | 1493 | -0.0388392 | 0.134245 | -0.301954 | 0.224276 |
| exclude_terminal_dependency | OLS3_L | x_open_bp | 1493 | -0.0125661 | 0.0307851 | -0.0729038 | 0.0477717 |
| exclude_terminal_dependency | OLS3_L | w_preclose_bp | 1493 | -0.0379997 | 0.132704 | -0.298095 | 0.222096 |

Full intercepts/ordinary SE/R²/HAC5/10/20 and RV/pooled sensitivities are in [coefficients](../../data/registry/B_stage1_coefficients.csv); [state metadata](../../data/registry/B_stage1_state_metadata.json), [QA](../../data/registry/B_stage1_qa.json), [coverage](../../data/registry/B_stage1_coverage.csv) and [source-use dates](../../data/registry/B_stage1_source_use.csv) provide compact audit trails. No alternative daily/minute dataset was written.

## Source fidelity and Stage 2 handoff

See [method crosswalk](../../docs/experiment_B_source_method_crosswalk.md). Gao1993–2013 TAQ / Limkriangkrai1996–2013 U.S. source-era samples are unavailable here. This is the approved modern 2016-start branch, using Alpaca SIP plus a qualified community repair. RV normalization/opening increment and original calendar grouping remain unresolved source-method differences; vendor trade counts and split/native repair prices are not certified TAQ reconstructions. Community provenance/license are undeclared/unverified; user-directed private use does not authorize raw redistribution.

**Stage 2 is technically ready as a separate authorized task**: reuse this one daily table, reserve 2022–2023 for chronological selection, freeze training-only preprocessing, assess joint support, and compare state-aware simple models before any EBM increment claim. Preserve source and terminal sensitivities and the sealed 2024–September2026 outcomes. Stage 1 establishes valid implementation and descriptive associations only; historical replication, held-out predictability, nonlinear enrichment, stability and economic value remain unexecuted.

| Claim | Estimand / information | Evidence and scope | Status / next falsification |
| --- | --- | --- | --- |
| Published positive modern association | Training linear projection of Y on X, E10:00 | OLS1 negative, HAC5 CI spans zero; chosen training cohort only | NOT SUPPORTED in this description; held-out predictability remains unexecuted |
| High RV strengthens opening slope | Pooled high-minus-low X slope, E10:00 | Negative point difference, HAC5 CI spans zero; retrospective bins conditional on cutoffs | INCONCLUSIVE; joint support and time-aware held-out comparisons needed |
| Incremental nonlinear shape, stability, profitability | Full fitted surface / supported raw comparisons / execution-timed net outcomes | No EBM, OOS, null or trading work in Stage1 | NOT EXECUTED; separate later stages |
