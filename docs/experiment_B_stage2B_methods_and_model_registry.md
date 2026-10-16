# Experiment B Stage 2B methods and model registry

Protocol [v1](../config/B_stage2B_EBM_protocol_v1.json) froze before all pilot/full fits. Dataset B_SPY_daily_split_source1_stage1_v1, SHA256 2aa3e2df1cab897abd679ed9cbeff8f6fcb004ecc01a7b32c5938aa6c23b5c2f. One daily table; all prior Stage2A forecasts referenced without copying their input histories. Original SIP/split source plus exactly39 D2.1c native missing-key repairs; source rights/adjustment qualifications unchanged.

| model_id | features | edges | info |
| --- | --- | --- | --- |
| SB_E | ["X"] | [] | E |
| A0c_E | ["X", "Z"] | [] | E |
| A0d_E | ["X", "S"] | [] | E |
| A1d_E | ["X", "S"] | [["X", "S"]] | E |
| A1c_E | ["X", "Z"] | [["X", "Z"]] | E |
| SB_L | ["X", "W"] | [] | L |
| A0c_L | ["X", "W", "Z"] | [] | L |
| A0d_L | ["X", "W", "S"] | [] | L |
| A1d_L | ["X", "W", "S"] | [["X", "S"]] | L |
| A1c_L | ["X", "W", "Z"] | [["X", "Z"]] | L |
| A2c_L | ["X", "W", "Z"] | [["X", "Z"], ["W", "Z"]] | L |

X is overnight-inclusive prior full close→10:00; Z=log(one-minute opening RV+1e−8); S is nominal text from original training terciles [0.001558374721607106, 0.0024281183976187152], equality lower. W15:00–15:30 is available only to L15:30. Y is signed15:30–16:00 price return in bp. E10:00 never reads W. No financial target or feature changes; A is on hold.

Actual InterpretML core 0.7.3 ExplainableBoostingRegressor, objective rmse; declared edges are runtime-index verified, no mining. Two settings: [{'max_bins': 32, 'max_interaction_bins': 8, 'min_samples_leaf': 25, 'learning_rate': 0.025}, {'max_bins': 64, 'max_interaction_bins': 16, 'min_samples_leaf': 10, 'learning_rate': 0.025}]. All defaults used are explicitly pinned in effective_base. Four bags for screening, eight final; primary seed42, confirmation seeds123/2025/7/314159. No clipping. Max1000rounds, early50, stochastic15% internal validation within available history only. Internal bagging shuffles past rows and is algorithmic; no bag interval is a scientific CI. Native greedy_ratio=0 uses cyclic boosting; native leaf dictionary/bag path is not the project's idealized learner.

Each family's candidate fits use2016–2020 targets and select minimum2021 MSE (ties first setting); settings chosen once before2022–23 evaluation, never reselect at future quarters. State coding retains original2016–2021 predictor-derived cuts even in training-era development; that internal screen is developmental rather than an honest live2021 forecast. Final fixed fits train1495days through2021. Quarterly Jan/Apr/Jul/Oct2022–23 histories use strictly completed targets, selected setting/seed frozen, original terciles unchanged. Jan2022 fixed fit is reused. All55 family/seed FULL models receive fixed and complete497date quarterly evaluation. No2024–2026 outcome read; date metadata/hash only.

All11 families seed42 receive DROP_TOP1 (2020-03-18), fixed Stage1.5 TOP5, EXCLUDE_2020, MATCHED_SOURCE (2019-08-12/13), one learning_rate=.05 sensitivity, and2016–19/2020/2021 fits. A1c E/L additionally leave each training year out. Native learner bins update on changed histories; frozen scientific cutoffs/coordinates remain fixed. These are learning-pipeline perturbations, not a literal fixed-linear-basis deletion. No variant replaces FULL based on better results.

Support screen: endpoints ±a, a10/20/30/50; local halfwidth5/10/15 with h<a; ordered candidates; late W0 then training median with halfwidth5/10/20. Minimum50dates/20 distinct disjoint5row blocks, strong100/30. Broad RV tercile neighborhoods are not pointwise Z support. E accepted ±20bp/h15; L no candidate, ABSTAIN. Exact cell counts/ranges/year mix in support registry. Sparse curves independently mask local cells below thresholds; continuous heatmap uses local Z±.2. No anchoredX0 contrast. Full D_F uses four total predictions at original low/high state medians. Additive D_F must be zero within1e−9. E model-output contrast remains EXPLORATORY/NOT_CERTIFIED; broad cell means estimate a different band functional. L model extrapolations may remain in audit tables labeled ABSTAIN but are not drawn as supported discoveries.

Paired loss comparator−candidate is positive for improvement. Bartlett HAC5 with n/(n−1), normal95%; lags10/20 sensitivity. Primary Holm family comprises quarterlyseed42 A1c_E−A0c_E and A1c_L−A0c_L comparisons only; other comparisons exploratory. Fixed-forecast circular block5/20 percentile bootstrap500 for four declared comparisons, not learner/post-selection bootstrap. Heavy tails, moments, weak-dependence and approximate stationarity matter. Scientific±1bp materiality never established by nonsignificance; predictive gain requires≥.0025 R² over stronger state-aware simple and interval excludingzero, also stronger naive comparison. State composition and within-state loss decomposition are descriptive, not covariate-shift correction.

Selected parameters/bins/terms: data/registry/B_stage2B_ebm_selected_parameters.json. All562 fits, including22screen/55FULL/385additionalquarter/44deletion/33subperiod/12leaveyear/11rate, registered; v1 total_planned662 was a conservative arithmetic typo, component counts unchanged and fully executed. Eleven primary seed42 native artifacts are ignored under artifacts/B/checkpoints/stage2B; no hundreds of serialized exploratory models. Single shared predictionParquet stores development/train/FULL/sensitivity/quarterly predictions, no sealed rows or input replicas.

Reproduce with authorized existing canonical data and matching Stage2A manifests: install requirements-stage2B.lock.txt, editable package, then python -B -m ebm_research.experiment_b.stage2b run (resume matching checkpoint) or publish (publication checkpoint). On a fresh authorized rebuild remove no existing user artifacts; use a fresh checkout, run freeze then pilot then run. Frozen protocol input hashes must match. EBM_DATA_ROOT may point to a portable shared store. No provider credentials/API needed for this offline stage. See session report for exact commands, recovery, errors and versions.

Native API consulted: [official regressor documentation](https://interpret.ml/docs/python/api/ExplainableBoostingRegressor.html); installed0.7.3 signature/source governs actual parameters. Original project theorem/task/consolidation files were absent from repository/ResearchSpec. Only explicit Bspec/AGENTS/current-prompt assumptions were applied; see theory audit for missing material.
