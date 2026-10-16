# Experiment B — Initial audit of nine remaining directions

**PASS_WITH_QUALIFICATIONS.** Nine data-supported sections, 44 figures (36 mandatory + 8 robustness). ABSTAIN is intentional for inadequate support. There were no predictive fits, new downloads, validation-response reads or sealed scientific reads.

[Visual gallery](../../artifacts/B/initial_audit/NINE_EXPERIMENTS_VISUAL_REVIEW.md).

## Sources, sample and timing

Daily source **B_SPY_daily_split_source1_stage1_v1**, SHA256 `2aa3e2df1cab897abd679ed9cbeff8f6fcb004ecc01a7b32c5938aa6c23b5c2f`. Immutable Alpaca SIP split-adjusted D2 + exactly 39 D2.1c native missing-key repairs, never D2.1b. This run projects only 2016–2021 minute/daily scientific columns before transforms: 136376 minute rows, 39 training patch rows, 1,495 eligible days. Full-file byte hashes may include later periods; they do not deserialize scientific values. The full table 2680 / 2675 eligible and later 497 / 683 split counts are frozen metadata only. Session keys are unique; opening-missing days remain excluded; the original primary training population is intact.

UTC timestamps label bar starts; ET conversion uses zoneinfo and XNYS schedule. E uses completed bars through 09:59 at 10:00; L through 15:29 at 15:30. Y=10000(C15:59/C15:29−1) is observed 16:00. One-minute RV includes first open→close plus 29 adjacent-close increments. Vendor latency is unknown. Half-days are skipped only in prior-full anchors; missing full anchors never fall back. B3 uses all scheduled full-session historical close anchors, including days with incomplete opening RV, and requires every anchor in the lag window.

## Precommit, features and masks

Protocol SHA256 `da9fbe99f4d64842ec8a76b7f5026f1683e20578361c845c5ca3c13567c3bf96` frozen before response exploration. Numerical predictor-only bins, masks, endpoint candidates and recent-state cuts were written before loading Y; their hash is in the manifest. Opening logcuts [-6.46410542902094, -6.02063452513255]; **separate recent logcuts** [-7.0040583024795176, -6.413856387887993]. Equality belongs to the lower state. TRAIN meanX for centered square=6.15601545548bp. These TRAIN retrospectives are descriptive, not historical live cutoffs.

| feature | formula | unit | earliest_usable_time_ET | n | missing | warmup |
| --- | --- | --- | --- | --- | --- | --- |
| x_open_bp | 10000*(C09:59/Pprev-1) | bp | 10:00 | 1495 | 0 | none |
| w_preclose_bp | 10000*(C15:29/C14:59-1) | bp | 15:30 | 1495 | 0 | none |
| rv_open_log | log(sqrt(log(C09:30/O09:30)^2+29 adjacent close logs squared)+1e-8) | log RV | 10:00 | 1495 | 0 | all 30 valid |
| gap_bp | 10000*open_overnight_part =10000*(O09:30/Pprev-1) | bp | 10:00 | 1495 | 0 | prior full anchor required |
| morning_bp | 10000*r_open_intraday_only =10000*(C09:59/O09:30-1) | bp | 10:00 | 1495 | 0 | none |
| late_accel_bp | late_return_5m_bp -10000*(C15:24/C15:19-1) | bp | 15:30 | 1495 | 0 | all endpoints genuine |
| abs_x_bp | abs(x_open_bp) | bp | 10:00 | 1495 | 0 | none; sign facets X<0/X>=0 |
| x_squared_bp2 | x_open_bp**2 | bp² | 10:00 | 1495 | 0 | none; removes direction |
| x_centered_squared_bp2 | (x_open_bp - TRAIN mean X)**2 | bp² | 10:00 | 1495 | 0 | center known after training; not live historical transform |
| abs_w_bp | abs(w_preclose_bp) | bp | 15:30 | 1495 | 0 | none |
| rv_late_30 | sqrt(log(C15:00/O15:00)^2+29 adjacent close logs squared) | dimensionless RV | 15:30 | 1495 | 0 | all 30 valid; no overnight |
| rv_late_log | log(rv_late_30+1e-8) | log RV | 15:30 | 1495 | 0 | all 30 valid |
| late_volume_30m | sum(volume15:00..15:29) | shares | 15:30 | 1495 | 0 | all 30 finite/nonnegative |
| late_volume_5m | sum(volume15:25..15:29) | shares | 15:30 | 1495 | 0 | all 5 finite/nonnegative |
| relative_late_volume | late_volume_30m / mean(previous 20 eligible full-session late_volume_30m) | ratio | 15:30 | 1475 | 20 | first20 eligible days missing; positive denominator |
| late_return_5m_bp | 10000*(C15:29/C15:24-1) | bp | 15:30 | 1495 | 0 | genuine completed endpoints |
| late_return_10m_bp | 10000*(C15:29/C15:19-1) | bp | 15:30 | 1495 | 0 | genuine completed endpoints |
| late_return_15m_bp | 10000*(C15:29/C15:14-1) | bp | 15:30 | 1495 | 0 | genuine completed endpoints |
| lag_close_1_bp | 10000*(C[t-1]/C[t-1-1]-1) | bp | 10:00 | 1494 | 1 | 2 consecutive full close anchors; half-days skipped only; missing anchors invalidate |
| lag_close_5_bp | 10000*(C[t-1]/C[t-1-5]-1) | bp | 10:00 | 1490 | 5 | 6 consecutive full close anchors; half-days skipped only; missing anchors invalidate |
| lag_close_20_bp | 10000*(C[t-1]/C[t-1-20]-1) | bp | 10:00 | 1475 | 20 | 21 consecutive full close anchors; half-days skipped only; missing anchors invalidate |
| B1_event | 1{y_last30_bp < -20} | probability | 16:00 LABEL ONLY | 1495 | 0 |  |
| C1_payoff | sign(W)*Y - cost_bp*1{W!=0}; costs0/2/5/10 | bp | 16:00 OUTCOME ONLY | 1495 | 0 |  |

The feature-only Parquet has (1495, 19) (including session key), no target/price/original-daily copies. B2 relative volume initializes after 20 eligible days; common all-feature n=1475. Sign facets use the pooled magnitude bin boundaries. Exact per-variant n/effective dates and missing masks are in predictor_only_design.json; ALL families additionally have the common-date mask in the contrast/bin registries. Rankings do not compare bp/probability/shares scales as if commensurable.

Fixed sensitivities: FULL, DROP_TOP1=['2020-03-18'], DROP_TOP5=['2020-03-18', '2020-03-13', '2020-02-28', '2020-03-27', '2020-03-24'], NO_2020, PRE_2020, YEAR_2020, YEAR_2021, COMMON_DATES. All endpoints/bins/cutoffs remain FULL-training fixed; no outlier reranking. The optional VWAP, reversal rule,−40bp event, past-volatility and late5 recent-RV expansion are intentionally omitted.

## Raw bins, uncertainty and support

Pooled predictor-only 8 quantile bins, deterministic unique-edge ties; a 5-bin sensitivity is retained in metadata/results and not used for ranking. Heatmaps use8×6 predictor/log-RV quantile cells, spaced evenly for legibility with numerical X medians and log-RV interval labels; they retain all tails. Scatter/curve display limits are predictor0.5/99.5percentiles; all tails remain in numerical estimates. Means/lines display at 20 dates / 10 five-row groups; uncertainty and cross-state contrasts require 50/20 per necessary cell, strong 100/30. Heatmaps below display support are gray; no interpolation. Group identifiers are floor(original eligible row/5), unchanged under masks; occupancy does not prove independent blocks.

Candidate endpoint quantile bands, in order: [[0.1, 0.3, 0.7, 0.9], [0.05, 0.35, 0.65, 0.95], [0.0, 0.4, 0.6, 1.0]]. Select first passing all six predictor-band×state date/group cells before reading Y. B1 subsequently requires 5 events, 5 nonevents and 3 event-bearing groups in each necessary cell; failure abstains without trying a different endpoint pair. Reported D_HL=(mean_b,H−mean_a,H)−(mean_b,L−mean_a,L), plus M−L and H−M. These broad-band, partner-marginal empirical means differ from pointwise D_m and from a fixed-partner EBM surface. Missing intervals/estimates are not zeros; separately labeled descriptive-only values at weaker 20/10 support are used only for the predeclared temporal feasibility screen.

Circular joint eligible-day block bootstrap: seed 20261016, length 5, 300 replicates shared across all states/variants, fixed bins and already-causal lagged features; 2.5/97.5percentiles, at least 270 finite draws and nondegenerate width. Resampling conditions on feature construction and thresholds; no raw-minute resampling, full learner/selection reconstruction or formal event-probability coverage is claimed. For fixed masks the original joint sequence is resampled with that mask, so excluded dates do not create artificial adjacency. Nonstationarity, heavy tails, dependent events and eight-family exploration qualify every interval. No independent state shuffle or Gaussian event bars. Optional block10 sensitivity omitted without response-based selection.

## Nine-family results and frozen rubric

| ID | X | state | n | evidence | support | caveat | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A2 | w_preclose_bp | rv_open_log | 1495 | D_HL 3.33bp [-6.96, 13.4] | 71% primary cells; 3 contrasts | A2 is already explored in Stage2B; this is a training-only raw-view audit, not an independent discovery | INCONCLUSIVE |
| A3 | late_return_5m_bp | rv_open_log | 1495 | D_HL -5.62bp [-15.5, 5.41] | 67% primary cells; 12 contrasts | These overlapping recent-return features are strongly related | INCONCLUSIVE |
| A4 | gap_bp | rv_open_log | 1495 | D_HL -19.5bp [-35.8, -5.94] | 62% primary cells; 6 contrasts | Simple returns compose multiplicatively: X/10000=(1+G/10000)(1+I/10000)-1 | INCONCLUSIVE |
| A5 | x_open_bp | rv_open_log | 668–1495 | D_HL -6.84bp [-18.2, 5.88] | 58% primary cells; 15 contrasts | Magnitude/squares remove direction and are dependent transforms, not independent replications | INCONCLUSIVE |
| A6 | w_preclose_bp | rv_late_log | 1495 | D_HL 2.6bp [-8.69, 12.5] | 62% primary cells; 6 contrasts | Recent RV shares 15:00–15:30 prices with W; changed state occupancy can alter composition | INCONCLUSIVE |
| B1 | x_open_bp | rv_open_log | 1495 | D_HL ABSTAIN [ABSTAIN, ABSTAIN] | 46% primary cells; 4 contrasts | Event scarcity and clustering restrict local probability contrasts | INCONCLUSIVE |
| B2 | late_volume_30m | rv_open_log | 1475–1495 | D_HL 3.55bp [-5.66, 11.8] | 71% primary cells; 9 contrasts | Volume units and normalization change the question; a volume/RV level effect is not moderation | INCONCLUSIVE |
| B3 | lag_close_1_bp | rv_open_log | 1475–1494 | D_HL 0.642bp [-7.85, 11.3] | 62% primary cells; 9 contrasts | The lag calendar skips scheduled half-days, but retains full sessions with missing opening data | LOW_PRIORITY |
| C1 | abs_w_bp | rv_open_log | 1495 | D_HL 2.27bp [-9.42, 13.3] | 71% primary cells; 3 contrasts | Entry at C15:29/exit at C15:59 assumes immediate availability and fills | MODEL_DEPENDENT / DEFER |

Ratings apply the exact conjunctive protocol rubric to the first prespecified panel, never the best variant. PROMISING needs support, an interval excluding 0, a nontrivial raw effect relative to noise, all three exclusion signs, at least two temporal signs with disclosed weaker support, and ≥50% cell support. LOW_PRIORITY requires a supported small/interval-inconclusive effect or severe supported sign instability; unavailable/weak support is INCONCLUSIVE, not proof of absence. C1 is always MODEL_DEPENDENT / DEFER. No composite score or winner is forced.

### A2

W directly tests late momentum/reversal, with other information marginalized. A2 is already explored in Stage2B; this is a training-only raw-view audit, not an independent discovery. Broad bands do not hold opening X fixed.

The high-state W increment is positive in the selected bands, but its difference from the low-state increment has a wide interval crossing zero. The orange raw curve is jagged rather than a stable continuation slope.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W: 15:00–15:30 | 1495 | 17/24 | -9.03 to 7.19 | 3.33 | [-6.96, 13.4] | -1.29 | 2.04 | EXPLORATORY_BLOCK_PERCENTILE | 4.01 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 3/3; temporal display-level 1/1.

### A3

All last5/10/15 and disjoint5-minute acceleration variants are shown; none is selected for a better response. These overlapping recent-return features are strongly related. Acceleration is a difference of disjoint returns, not a second independent trial.

The last 5 and last 10 contrasts point in opposite directions; last 15 and acceleration are nearer zero. None of their H−L intervals excludes zero. That endpoint dependence argues against treating the visually strongest recent-return panel as a discovery.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Last 5 minutes | 1495 | 16/24 | -9.51 to 2.92 | -5.62 | [-15.5, 5.41] | 0.651 | -4.97 | EXPLORATORY_BLOCK_PERCENTILE | -6.22 |
| Last 10 minutes | 1495 | 16/24 | -11 to 4.86 | 7.63 | [-0.698, 15.9] | -0.815 | 6.81 | EXPLORATORY_BLOCK_PERCENTILE | 7.38 |
| Last 15 minutes | 1495 | 16/24 | -7.32 to 7.75 | -0.841 | [-9.1, 8.36] | -1.07 | -1.91 | EXPLORATORY_BLOCK_PERCENTILE | -0.739 |
| Recent 5m minus disjoint earlier 5m | 1495 | 17/24 | -10.2 to 6.53 | 1.63 | [-11.5, 13.1] | 3.72 | 5.35 | EXPLORATORY_BLOCK_PERCENTILE | 0.653 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 3/3; temporal display-level 1/1.

### A4

Gap G and morning I isolate two components of the overnight-inclusive opening predictor. Simple returns compose multiplicatively: X/10000=(1+G/10000)(1+I/10000)-1. Opening RV shares the morning price path; gap and morning facets do not control for each other.

Gap G has a negative H−L increment contrast whose nominal exploratory interval excludes zero; the morning I contrast remains interval-inconclusive. All three fixed exclusions retain the gap sign, but only one temporal comparison meets even the weaker display-support gate. The gap deserves visual scrutiny, with multiplicity and missing temporal confirmation kept explicit.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Overnight gap G | 1495 | 15/24 | -25.7 to 6.19 | -19.5 | [-35.8, -5.94] | 0.416 | -19.1 | EXPLORATORY_BLOCK_PERCENTILE | -19.9 |
| 09:30–10:00 intraday I | 1495 | 16/24 | -7.51 to 9.39 | -2.64 | [-13.5, 8.29] | -1.44 | -4.08 | EXPLORATORY_BLOCK_PERCENTILE | -2.83 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 3/3; temporal display-level 1/1.

### A5

Signed X, magnitude, two squares and both sign-specific magnitude facets are all retained. Magnitude/squares remove direction and are dependent transforms, not independent replications. Low-RV large-magnitude support is structurally thin; TRAIN centering is retrospective.

|X| and X² give identical rank-bin contrasts because squaring is monotone on nonnegative magnitude; these are the same observations, not replication. Signed-X, magnitude, centered-square and positive-sign intervals cross zero. The negative-sign magnitude contrast abstains for joint support.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Signed opening X | 1495 | 14/24 | -9.24 to 7.22 | -6.84 | [-18.2, 5.88] | 3.11 | -3.73 | EXPLORATORY_BLOCK_PERCENTILE | -7.92 |
| /X/ | 1495 | 17/24 | -7.12 to 7.05 | 0.808 | [-12.8, 14.1] | -2.76 | -1.95 | EXPLORATORY_BLOCK_PERCENTILE | 1.51 |
| X² (direction removed) | 1495 | 17/24 | -7.12 to 7.05 | 0.808 | [-12.8, 14.1] | -2.76 | -1.95 | EXPLORATORY_BLOCK_PERCENTILE | 1.51 |
| (X − TRAIN mean X)² | 1495 | 15/24 | -9.6 to 5.75 | 2.27 | [-9.49, 13.7] | -3.13 | -0.854 | EXPLORATORY_BLOCK_PERCENTILE | 2.25 |
| /X/ conditional on X < 0 | 668 | 1/24 | -5.89 to 7.34 | ABSTAIN | [ABSTAIN, ABSTAIN] | ABSTAIN | ABSTAIN | ABSTAIN_SUPPORT | ABSTAIN |
| /X/ conditional on X ≥ 0 | 827 | 4/24 | -8 to 9.06 | -1.34 | [-16.5, 11.7] | 1.41 | 0.0655 | EXPLORATORY_BLOCK_PERCENTILE | -1.14 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 3/3; temporal display-level 0/1.

### A6

The principal recent state and opening-state comparison use exactly the same W/Y dates. Recent RV shares 15:00–15:30 prices with W; changed state occupancy can alter composition. Distinct named cutoffs prevent conflating this with opening-RV discretization.

Replacing opening RV by recent RV leaves an interval-inconclusive W increment contrast. Only 61.1% of days keep the same state, so visually different curves partly reflect regrouping. Neither state specification establishes moderation or a preference for a new model.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W; recent RV PRINCIPAL | 1495 | 15/24 | -6.67 to 9.5 | 2.6 | [-8.69, 12.5] | -0.775 | 1.83 | EXPLORATORY_BLOCK_PERCENTILE | 3.37 |
| W; opening RV COMPARISON | 1495 | 17/24 | -9.03 to 7.19 | 3.33 | [-6.96, 13.4] | -1.29 | 2.04 | EXPLORATORY_BLOCK_PERCENTILE | 4.01 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 3/3; temporal display-level 1/1.

### B1

Both early X and late W panels show the fixed Y<−20bp adverse event. Event scarcity and clustering restrict local probability contrasts. These resampled event rates are not Gaussian-return inference, classifier calibration or forecasts.

There are 217 adverse days out of 1,495 (14.5%), with 52 adjacent event pairs. The early-X H−L contrast fails because one necessary cell has only four events. The supported late-W contrast is near zero with a broad probability interval; a higher high-state event level is not changed momentum response.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Opening X — early information | 1495 | 11/24 | 0.0649 to 0.312 | ABSTAIN | [ABSTAIN, ABSTAIN] | ABSTAIN | ABSTAIN | ABSTAIN_SUPPORT | ABSTAIN |
| Late W — late information | 1495 | 11/24 | 0.0741 to 0.355 | -0.0134 | [-0.168, 0.132] | 0.00158 | -0.0118 | EXPLORATORY_BLOCK_PERCENTILE | -0.0238 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 0/0; temporal display-level 0/0.

### B2

Raw30m volume, raw5m volume and strictly prior20-eligible-session relative volume are all shown. Volume units and normalization change the question; a volume/RV level effect is not moderation. Relative volume loses its first20eligible days. VWAP is omitted because repaired VWAP is null.

Raw 30m and 5m volume contrasts are positive while relative volume is negative, and all H−L intervals cross zero. Normalization changes the feature meaning; the sign difference cannot justify choosing whichever scale looks favorable. Relative volume ranges to 7.90× and has 20 warmup days.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15:00–15:30 volume | 1495 | 17/24 | -4.98 to 6.64 | 3.55 | [-5.66, 11.8] | -0.696 | 2.85 | EXPLORATORY_BLOCK_PERCENTILE | 3.47 |
| 15:25–15:30 volume | 1495 | 18/24 | -10.2 to 7.51 | 3.93 | [-3.22, 13.1] | 0.045 | 3.97 | EXPLORATORY_BLOCK_PERCENTILE | 4.14 |
| Late volume / prior 20 eligible mean | 1475 | 19/24 | -12.2 to 6.62 | -2.53 | [-13.5, 8.05] | -0.569 | -3.1 | EXPLORATORY_BLOCK_PERCENTILE | -2.53 |

Rating **INCONCLUSIVE**; fixed exclusion same-sign 2/2; temporal display-level 0/1.

### B3

One/five/20-session returns end at the previous completed full-session close. The lag calendar skips scheduled half-days, but retains full sessions with missing opening data. Missing full-close anchors invalidate windows; price returns are not dividend-adjusted total returns.

The one-session primary contrast is small relative to daily Y noise and its interval crosses zero; five-session evidence is also weak, while the 20-session estimate points negative with an interval crossing zero. These differing horizons provide no coherent moderation signal.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Prior 1-full-session return | 1494 | 15/24 | -10.9 to 9.53 | 0.642 | [-7.85, 11.3] | 2.72 | 3.36 | EXPLORATORY_BLOCK_PERCENTILE | 0.632 |
| Prior 5-full-session return | 1490 | 15/24 | -7.71 to 5.53 | 1.44 | [-10.7, 12.8] | -1.06 | 0.381 | EXPLORATORY_BLOCK_PERCENTILE | 1.59 |
| Prior 20-full-session return | 1475 | 16/24 | -9.37 to 7.96 | -4.65 | [-12.3, 3.86] | 4.63 | -0.0129 | EXPLORATORY_BLOCK_PERCENTILE | -4.65 |

Rating **LOW_PRIORITY**; fixed exclusion same-sign 3/3; temporal display-level 1/1.

### C1

The fixed, unoptimized sign(W) continuation rule is displayed versus |W|; no policy is learned. Entry at C15:29/exit at C15:59 assumes immediate availability and fills. Cost0/2/5/10bp is hypothetical; bid/ask, latency and slippage are absent. TRADING_NOT_ESTABLISHED.

The all-day fixed-rule gross mean is 0.833 bp, with an exploratory interval spanning zero. Hypothetical net means at 2/5/10 bp costs are −1.14/−4.09/−9.01bp; implied gross break-even is only 0.846 bp per active day. Zero-signal days (23) stay flat. These assumptions are not executable alpha evidence.

| panel | n | supported_curve_cells | displayed_mean_range | D_HL | interval | low_increment | high_increment | status | D_HL_common_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /W/; fixed sign(W) continuation | 1495 | 17/24 | -8.28 to 8.27 | 2.27 | [-9.42, 13.3] | 3.96 | 6.23 | EXPLORATORY_BLOCK_PERCENTILE | 2.04 |

Rating **MODEL_DEPENDENT / DEFER**; fixed exclusion same-sign 2/2; temporal display-level 1/1.

## Additional diagnostics

B1 event prevalence, event-bearing groups and clustering; B2 relative-volume tails/warmup; B3 lag warmup and early-session mappings; A6 state cross-occupancy; C1 scenario means and break-even values are recorded in `registries/feature_and_state_diagnostics.json` and `registries/illustrative_cost_scenarios.csv`. Source1 terminal-repair dependence on 2019-08-12/13 and unverified community upstream redistribution rights/adjustment remain prior-source qualifications. No source fidelity, raw-shape theorem, causal, predictive or trading superiority claim follows.

## QA, resource use and reproduction

Seven independent real-date scalar checks cover DST transition, half-day skip, native repair, crisis day and2021 gap context. Checks include endpoints, disjoint acceleration, all 30RV increments, volume sums, strictly prior20volume and lagged close equations. Focused deterministic tests cover current-day exclusion, missing interior anchors, timestamp endpoints, return units, bootstrap joint cells and degenerate/support abstention. Manifest records output reads, preservation hashes, PNG/gallery QA and actual software versions. See mandatory session report for commands/failures and visual inspection.

Run `python -B scripts/b_initial_audit.py run` then `python -B scripts/b_initial_audit.py qa` in the existing environment. Fresh setup: install the project and pinned requirements-stage2B.lock.txt, supply matching authorized canonical sources via EBM_DATA_ROOT, then use the already frozen protocol. No credentials/API are accessed. Scope is offline SPY/B only.

Numerical/plot run resource measurements are in the final manifest; statistics elapsed before publication=90.08s. All44figurepaths have exact manifest hashes; new-feature schema/bytes are registered. No user files moved/deleted; no prior results overwritten.

## Handoff

Human-review the standalone gallery before nominating another experiment. A6 is a comparison of two measured states, A3 extends late returns, A5/B1 illustrate support constraints, and C1 lacks execution evidence. Any later model stage needs a separately approved frozen predictor/state/contrast and matched simple baselines, multiplicity/selection plan and honest future evaluation. The original A1/A2 inconclusive developmental closeout remains unchanged.
