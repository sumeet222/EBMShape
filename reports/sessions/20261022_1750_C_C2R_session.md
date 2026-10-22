# Experiment C / C2R — detailed coding-session audit

## 9.1 Session identification and verdict

Session `20261022_1750_C_C2R_session`; report time **2026-10-22T17:50:15.046045-04:00**, America/New_York (EDT, UTC−04). Baseline captured **2026-10-22T17:09:06.354911-04:00** after initial discovery during this same turn. Agent Codex; exact runtime model identifier not exposed. Experiment **C**, task **C2R_DEVELOPMENT_v1_1**, user attachment `4c2fc699-34c6-4e69-9de5-6db3ffea1a5a/Pasted text.txt` (“CODEX EXECUTION TASK — Experiment C, Stage C2R (v1.1)”). No subagents. Starting/ending branch **main**, commit **f05f23a27e7bd5133b3ba055afd1fae160dfd7c6**. Starting dirty state: prior C1R untracked code/protocol/reports/artifacts and supplied specs; exact status in protected_input_baseline.json. All **417 preexisting files,96,583,509 bytes hashed** are unchanged; original78minute sources and C1R state hash also match. No commit/stage/push/deploy/reset/branch/history/data deletion.

**Implementation/QA PASS. Stage PASS_WITH_QUALIFICATIONS.** C2R completed: source/state alignment; pre-fit freeze;12 contexts × 14 candidates = 60 scalar + 108 profile fits; matched past-only2020/2021 backchecks; requested scalar/profile diagnostics/influence/calibration/environment/sensitivity/uncertainty;14 reviewed figures; full reports and hashes. Final **22/22 tests pass**. P0closing H1 reproduces **2.004981434pp** (delta -2.78e-15pp). Conditional scalar slope evidence survives the fixed family, piecewise/quadratic additions do not. Pooled profile MSE favors M0; primaryM4 is1.6635% worse. ScalarL1closing MSE is2.4332% lower than intercept. This is exploratory development, not materiality/near-invariance certification, independent confirmation, exactsource replication orEBM evidence.

Not done by design: H2/Zret,Zvol,addedZchg,VIX/FOMC,EBM,C5certifiedinference,C6test,trading,2022–2026Cscientificvalues,full-Cofficialsplit,network/downloads/purchases. Existing C1R full-study draft remains unlocked/pending. No scientific redesign or new authorization was inferred.


## 9.2 Exact file inventory

All final repository changes are CREATED C2R files. No preexisting user file was modified/deleted/moved. Session-owned drafts/plots were replaced during the documented repairs. Sizes below are at composition; final exact bytes/hashes are in files_manifest.json.

| Action | Repository-relative path | Why / what changed | Size / shape | Consumers | Recovery |
|---|---|---|---|---|---|
| CREATED | artifacts/C/C2R_development_v1_1/block_intervals.csv | Reused matching P0block5/10 intervals and new fixed-label block20 window/TV sensitivity | 2,575 bytes; 17x8 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/chronological_predictions.npz | 9x489x78 profile and5x489 scalar forecasts, date/source-slot keys; no target Q/actual copy | 896,859 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/cohort_by_year.csv | Six-row Q1491/Z01472 population flow | 98 bytes; 6x3 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/completion.log | Final no-refit completion output, empty-bin and chronology guards applied | 790 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/completion_first.log | Retained first-completion empty-bin warning evidence | 1,704 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/contrasts_and_materiality.csv | Full/sensitivity whole-fit same-row window/TV contrasts, support/materiality labels | 118,040 bytes; 658x13 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/daily_design_index.csv | 1472unique keys/source slots/Z0/closing share/currentRcontext and declared exclusion flags; no minute or Q table | 135,590 bytes; 1472x8 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/descriptive_predictions.npz | 9x1472x78 profile and5x1472 scalar descriptive predictions, source-slot/date keys; no Q/actual copy | 2,666,487 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/direct_profiles.csv | P0historical/origin-training conditional78bin means andcounts | 171,886 bytes; 3042x6 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/direct_window_summaries.csv | Six named daily Q-share means/SD by historical state, not ratio of group RV totals | 1,340 bytes; 18x7 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/environment_TV.csv | Marginal and supported same-early-training-quintile environment comparisons, otherwise ABSTAIN | 716 bytes; 12x6 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/environment_residual_discrepancy.csv | Same-coarse-cell residual half-L1 environmental shifts under shared D_FULL fits, not probability TV/causal drift | 4,506 bytes; 30x8 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/environment_versions.json | 33installed package names/versions, no credentials or pathful pip URLs | 822 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/feature_collinearity.csv | Nonconstant-term VIF and feature correlations; intercept VIF omitted | 6,969 bytes; 102x7 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figure_data_extra.npz | Small plotted environmental/variance summary arrays | 520 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/01_direct_three_state_profiles.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 298,786 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/02_closing_share_scatter_and_state_OLS.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 213,924 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/03_OLS_estimates_and_interaction_tests.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 146,062 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/04_scalar_OLS_residual_and_QQ.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 255,511 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/05_scalar_OLS_residual_time_ACF_and_variance.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 262,297 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/06_influence_and_robustness.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 208,308 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/07_M0_M1_M2_profile_fit.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 245,220 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/08_state_dependent_profile_OLS.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 327,709 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/09_M4_continuous_state_heatmap.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 245,400 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/10_raw_vs_spline_scientific_fidelity.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 181,204 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/11_development_chronological_model_scorecard.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 227,709 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/12_environment_support_and_composition.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 182,584 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/13_normalization_residuals_and_last_bin.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 247,786 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/14_scalar_calibration_period_means_and_PACF.png | Generated C2R principal scientific image; source/hash/dimensions in plots_manifest.json | 294,257 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/figures/contact_sheet.png | Composite visual review of14newC2Rfigures; no copied P0figures | 899,455 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/fit_hashes.csv | 168 per-fit SHA256 signatures over coefficients, transform, train/forecast hashes and frozen protocol | 17,797 bytes; 168x4 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/model_fidelity_by_state_bin.csv | Raw vswhole-fit observed same-cell means for P0terciles and5trainquantilecells | 611,321 bytes; 5616x9 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/model_parameters.json | All168coefficient/basis/transform/date records; no source rows or original Q | 2,409,006 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/model_registry.csv | 168 unique context/model rows, kind/rank/edf/condition/datehashes/counts/extrapolation/fallback | 52,898 bytes; 168x20 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/model_scores.csv | All model train/2020/2021/pooled scores on matched keys, raw half-L1/TVvalid counts/closing errors | 54,513 bytes; 350x13 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/model_train_eval_gaps.csv | Explicit origin train-versus-development-year error/bias gaps | 1,826 bytes; 28x6 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/origin_state_inventory.csv | Train/eval numeric ranges/cuts/quantiles/out-of-training-range counts | 1,290 bytes; 6x13 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/paired_loss_sensitivities.csv | Per-year/pooled fixedforecast paired profile/closing loss differences; HAC/shared blocks5/10/20,B1000 | 31,926 bytes; 108x15 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/plot_data.npz | Aggregated raw/fitted H-L/D/grids/heatmap/serial and fixedlastbin/14:00diagnostics, not daily Q | 78,214 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/plots_manifest.json | 14principal PNG hashes/dimensions/source references and independent numeric/image QA | 6,707 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/prepare.log | Successful pre-fit source gate/protocol freeze; no scientific fit | 810 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/profile_bin_residuals.csv | 78bin residual mean/variance/RMSE/MAE/skew/tails/state covariance per core profile fit/part | 613,461 bytes; 3510x11 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/profile_daily_errors.csv | 37512model/date scalar vector-error summaries and state keys, no duplicated Q matrix | 7,844,028 bytes; 37512x14 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/profile_diagnostics.csv | Core-context train/eval vector losses, raw normalization/negativity/range, window/edge/roughness/covariance metrics | 45,171 bytes; 45x56 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/profile_errors_by_state.csv | Aggregated date/state profile errors and vector norms from saved daily diagnostics | 18,224 bytes; 135x10 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/protected_input_baseline.json | 417existing relative file hashes/sizes and start Git/time state | 72,701 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/provenance_and_QA.json | Source/config/code/fit/chronology/network/test/plot/preservation/result-status evidence | 29,956 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/report.log | Initial13figures/report/84scorechecks and permitted temporary fontcache environment messages | 1,276 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/residual_covariance.npz | Nine D_FULL78x78 empirical residual covariance matrices, not78independenttests | 296,475 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/residual_eigenvalues.npz | Core-context/part residual covariance spectra and closure/null-direction diagnostic | 38,929 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/run.log | Bounded numerical-run output and statsmodels future-return-object warnings, no API/secrets | 224,919 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_calibration.csv | 75fixed fitted-quintile calibration rows with explicit empty-bin ABSTAIN masks | 6,362 bytes; 75x8 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_conditional_means_and_hac.csv | 180fitted group-mean intervals conditional on design/cuts, not individual prediction intervals | 36,497 bytes; 180x10 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_contrasts_and_HAC.csv | Whole-fit origin-S0 closing H-L estimates/ordinary andHACintervals inpp | 13,383 bytes; 60x14 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_ols_models_and_hac.csv | Ordinary/HAC5/10/20 coefficients, SE/CI/p and piecewise state slopes for three core training contexts | 44,896 bytes; 216x14 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_residual_influence.csv | Actual dated residual/leverage/internal/external studentization/Cook/DFFITS/DFBETAs/flags, never bin-row inference | 5,769,910 bytes; 18395x24 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_residual_period_means.csv | Year/scheduled-five-slot residual means/SD for actual OLSfits | 315,614 bytes; 3850x7 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_specification_tests.csv | Joint level/slope/curvature Wald, RESET/F, rawH1nulls, six-family Holm and explicit skips | 7,426 bytes; 64x10 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/scalar_summary.csv | 15dailyOLS summaries: n/df/rank/condition, R2/adjustedR2/SSE/MSE/GaussianAIC/BIC, residual moments/tails, White/BP/Koenker/JB | 9,735 bytes; 15x34 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/sensitivity_models.csv | All declared exclusions and LOYO model scores/contrasts with non-walk-forward labels | 25,386 bytes; 126x17 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/serial_diagnostics.csv | Daily OLS and profileclose/PC1/norm ACF/PACF/Ljung-Box/squared/ARCH lags5/10/20 with heuristic-reference caveats | 132,766 bytes; 450x15 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/support_and_environment.csv | Distinct-date/five-session-group counts, gates/ranges/masks for origin/state/environment/query | 37,166 bytes; 184x14 | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/tests.log | Final22/22tests afterreportingrepairs | 3,037 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | artifacts/C/C2R_development_v1_1/tests_pre_fit.log | 20/20 full-family synthetic tests before real fits | 2,791 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | config/C_C2R_development_protocol_v1_1.json | Separate pre-fit exploratory freeze, exact source/cohort/code/environment/formulas/bases/lags/blocks/support/release gates | 52,668 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | reports/C/C2R_OLS_state_dependent_splines_full_diagnostics.md | Substantive scientific report, formulas/tables/negative results/support/inference/next gates | 54,775 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | reports/C/C2R_scientific_visual_gallery.md | 14embedded principal plots and concrete scientific interpretation | 8,244 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | reports/C/C2R_theory_applicability_and_limitations.md | Algebra/conditional inference/adapted descriptive/deferred theory ledger, no raw pointwise certification | 4,221 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | scripts/c2r_development_models.py | Installed-package prepare/run/report CLI | 163 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | src/ebm_research/experiment_c/c2r_completion.py | No-refit conditional means, calibration/period/environment residual audits and reporting/figure repairs | 16,103 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | src/ebm_research/experiment_c/c2r_development.py | Offline source gate, pre-fit C2R freeze, twelve contexts, 168 fits, sensitivities, compact predictions/tables | 38,811 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | src/ebm_research/experiment_c/c2r_diagnostics.py | Daily OLS HAC/specification/tails/heteroskedasticity/influence and vector covariance/serial diagnostics; joint blocks and Holm | 13,976 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | src/ebm_research/experiment_c/c2r_models.py | Fixed daily OLS/profile models, exact time/state bases, rank guards, losses and calendar-score HAC | 10,299 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | src/ebm_research/experiment_c/c2r_reporting.py | Independent saved-coefficient/source checks, first13figures and substantive scientific/gallery/theory reports | 51,793 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | tests/test_c2r_models.py | Ten focused C2R synthetic/statistical/regression tests, plus twelve unchanged prior tests in combined suite | 6,679 bytes | C2R report/QA; laterstage only ifauthorized | Regenerate stage-owned outputs; preserve audit snapshots |
| CREATED | reports/sessions/20261022_1750_C_C2R_session.md | Detailed coding-session report in both required locations | This report; final size in filesmanifest | User/nextagent | Never overwrite earlier audit |
| CREATED | reports/C/C2R_coding_session_20261022.md | Detailed coding-session report in both required locations | This report; final size in filesmanifest | User/nextagent | Never overwrite earlier audit |
| CREATED | artifacts/C/C2R_development_v1_1/files_manifest.json | Final exact all-new-file hashes/sizes/totals | Written afterthisreport | Restore/review | Regenerate metadata after authorized changes |
| CREATED | artifacts/C/C2R_development_v1_1/session_paths.json | Two requested report locations | Small JSON | Audit handoff | Regenerate report references |


Consequential existing sources follow. Exact source identities/read ledger and all417baseline members are machine-enumerated; grouped repeated files are explicit.

| INSPECTED path | What/why | Consumers | Recovery |
|---|---|---|---|
| AGENTS.md | Complete root instructions including mandatory9.1–9.7 | Allwork | Baselinehashpreserved |
| docs/specs/C/experiment_C_revised_complete_research_design_v1_1.md; experiment_C_revised_transition_and_next_stage_handoff_v1_1.md | Approveddesign/handoff, fullreads inthisconversation reconciled againstcurrentpins; currentactive sections read | Windows/state/modes/modelscopes | Pinnedhashesmatch; unchanged |
| docs/specs/experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md; experiment_C_P0_supplied_handoff_v1_1.md | Fulloriginal/P0authority read previously and currentexacthashesverified; retainunchangedscientificparts | R1–R6/P0/math/interpretation | Unchanged; no theoremtextfabricated |
| reports/C/C1R_protocol_and_coverage.md; reports/sessions/20261022_1652_C_C1R_session.md; config/C_full_protocol_v1_1.yaml | Actualexecutionandpendingdraft, notofficialfreeze | Currentstageauthorization/provenance | Preserved |
| artifacts/C/C1R/C1R_execution_QA.json; source_identity_qa.json; state_ledger.csv; protected_input_baseline.json | Actualschemakeys/statehash/source QA | State/provenancegate | Preserved |
| data/registry/C_preliminary_RV_profile_v1_1.json; config/C_preliminary_RV_profile_v1.json; P0source_manifest.json / outputs_manifest.json / qa_results.json | Originalexecutedsource/target/rank/intervalidentities | AllC2Rfits | Preserved |
| artifacts/C/preliminary_RV_profile_v1_1/daily_profiles.npz | 1511scheduledslots, only2016-01-04…2021-12-31 q/rv/RV_prev/dates/labels; Jan4auxiliary | OriginalQbyreference | SHA2aa2554accde6cfeaadeb5b539b52931f76c1470cdb3a435eefef2e804de0c27 |
| data/derived/C/c_development_states_v1_1.parquet | Onlydate_et/predecessor_et/Z0/Z0_reason columns;1491rows/1472validZ0 | At-open state | SHA53c00dd9d7b8b499f6b00ebabe0955f34bea95ef009c4e81cd3b995a021b7238 |
| data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year=201[6-9].parquet plus year=202[01].parquet (6files) | Digest/size only,no minute decode | Parent source | Exactrefs in P0/C2Rmanifest; unchanged |
| data/source_cache/C_spy_1m_p0_v1_1/2016-01.parquet through2021-12.parquet (72monthlyfiles) | Digest/size only, originalsupplementdisjointkeys | Parent source | Exact72hashrefs/source_manifest; unchanged |
| artifacts/C/preliminary_RV_profile_v1_1/window_shares_by_state.csv; reports/C/C_spec_window_preliminary_visual_review.md and verifiedCspecsummaries | Matchinghistoricaldescriptivewindows/intervals | H1reproduction,reuseblock5/10 | No oldbootstrap/figurererun |
| ExperimentB D2source/protectedregister; src/ebm_research/experiment_c/readiness.py; originalCtests/profilecode; pyproject.toml | Provenance/calendar/train-onlytransform reuse andinstalledstack | NewC2Rcode/tests | No Bdailyreturn/forecast/sciencevalues used |


Ignored binary outputs contain predictions/covariances/aggregate plot arrays, never another input Q. Chronological profiles are9x489x78/scalars5x489; descriptive profiles9x1472x78/scalars5x1472. Nine78x78residual covariances and spectra are diagnostics, not independent observations. Existing NPZ/log ignore policy applies; no .gitignore change. Licensed sources remain external/local subject to account/exchange terms; a public clone does not ship them.

Temporary files: /private/tmp/c2r_start.json, c2r_tests_pre_fit.log, c2r_prepare.log (audit copies retained in artifacts), /private/tmp/c2r_write_session.py (this report writer), and /private/tmp/c2r_mpl_cache (~289,954bytes). Initial Matplotlib also created OS-temp matplotlib-hxnwy8n1. All contain small metadata/logs/fontcache, no credentials orrawdata. Five new-suite runs automatically created/removed five c2r_smoke_* tiny synthetic-NPZ directories. Three combined runs additionally created/removed six C1R path/split fixture directories and three P0 NPZ fixture directories. Random tempfile names were not retained; prefixes/counts/reproduction identify generated-only effects. No preexisting artifact was deleted or orphan download retained.


## 9.3 Critical code/function/variable register

| Path:function/class | Signature | Line | Purpose |
|---|---|---|---|
| src/ebm_research/experiment_c/c2r_completion.py:calibration_rows | fitted, residual, context, model | 20 | Fixed quintiles with explicit empty-bin status when fitted values tie. |
| src/ebm_research/experiment_c/c2r_completion.py:chronological_periods | frame | 35 | Sort numeric period keys as time indices, never lexicographically. |
| src/ebm_research/experiment_c/c2r_completion.py:complete |  | 40 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:clean | value | 36 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:write_json | path, value | 44 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:no_network |  | 50 | Reject attempted socket connections during local C2R execution. |
| src/ebm_research/experiment_c/c2r_development.py:load_inputs |  | 62 | Hash references, then load only the pinned 2016–2021 Q and state table. |
| src/ebm_research/experiment_c/c2r_development.py:prepare |  | 123 | Write the C2R-only pre-fit protocol, never mutate the full-C draft. |
| src/ebm_research/experiment_c/c2r_development.py:save_csv | name, rows | 189 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:support_row | context, group, mask, d, labels, origin | 193 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:metrics | q, pred, name, context, part, kind | 204 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:run |  | 218 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_development.py:main |  | 471 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_diagnostics.py:distribution | values | 17 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_diagnostics.py:influence_arrays | fit | 25 | Exact OLS deletion identities, avoiding N repeated leave-one-out fits. |
| src/ebm_research/experiment_c/c2r_diagnostics.py:linear_contrast | beta, cov, contrast, null=0.0, one_sided=False | 41 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_diagnostics.py:wald | beta, cov, indices | 51 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_diagnostics.py:series_diagnostics | values, name, context, model, ddof=0 | 59 | Eligible-date ordered scalar serial diagnostics, never bin-row IID tests. |
| src/ebm_research/experiment_c/c2r_diagnostics.py:scalar_diagnostics | model, transform, dates, z, q, slots, context | 80 | OLS coefficients/HAC, design, tails, heteroskedasticity and influence. |
| src/ebm_research/experiment_c/c2r_diagnostics.py:profile_diagnostics | q, pred, dates, z, labels, model, context, part, slots | 163 | 78-vector residual distribution/covariance, scores and calibration. |
| src/ebm_research/experiment_c/c2r_diagnostics.py:block_weights | slots, length, B, seed | 207 | Shared circular draws over scheduled slots; no filling missing responses. |
| src/ebm_research/experiment_c/c2r_diagnostics.py:holm_family | rows, context='D_FULL' | 218 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_models.py:date_hash | dates | 21 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_models.py:check_design | x, max_condition=10000000000.0 | 25 | Reject unidentifiable fits rather than manufacture coefficient tests. |
| src/ebm_research/experiment_c/c2r_models.py:time_basis | df | 34 | Clamped cubic B splines on k=0..77, uniform fixed knots, row sum one. |
| src/ebm_research/experiment_c/c2r_models.py:natural_basis | values, knots | 46 | Four-knot natural cardinal cubic basis, with linear continuation outside. |
| src/ebm_research/experiment_c/c2r_models.py:scalar_design | zs, labels, model | 65 | Fixed column order for scalar closing-share OLS; intercept always first. |
| src/ebm_research/experiment_c/c2r_models.py:Model | dataclass/unittest | 79 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_models.py:fit_models | dates, z, q, slots | 110 | Fit the frozen five scalar/nine profile candidates, one small origin. |
| src/ebm_research/experiment_c/c2r_models.py:profile_losses | q, pred | 177 | Daily vector scores; TV is defined only for numerically simplex output. |
| src/ebm_research/experiment_c/c2r_models.py:calendar_hac | x, resid, slots, lag | 186 | Bartlett Newey–West score covariance with scheduled-session gaps. |
| src/ebm_research/experiment_c/c2r_reporting.py:table | frame, columns=None, limit=None | 17 | CLI or focused test |
| src/ebm_research/experiment_c/c2r_reporting.py:render |  | 26 | CLI or focused test |
| tests/test_c2r_models.py:fixture | n=90 | 19 | CLI or focused test |
| tests/test_c2r_models.py:C2RTests | dataclass/unittest | 28 | CLI or focused test |


`Model.predict(z, transform)` reconstructs the exact stored map from origin-specific mean, SD, categories and knots. Inputs are ordered ET dates, finite Z0, an N×78 float64 response and original scheduled-session indices. Outputs are scalar closing shares or complete profiles. Only deterministic time and ex-ante Z0/S0 enter models. Current-day R is used only for context and the retrospective top-1% sensitivity. The bounded runner and synthetic tests call `fit_models`; reporting reads its saved coefficients.

The time basis is a clamped cubic partition of unity with 8 primary or 12 sensitivity columns. The four-column natural state basis uses training minimum, terciles and maximum, with linear continuation outside. Factorized M4 least squares equals the explicit balanced tensor design. Constants in both spans avoid redundant intercepts. P-OLS-Z verifies the sums of intercepts/slopes are one/zero. The centered additive ablation uses the same bases without a tensor and is not native EBM M3. Rank or condition failures stop the affected fit before p-values.

Scalar designs have the exact frozen intercept, z_s, category and interaction columns. OLS sample sizes and degrees of freedom count days. Calendar HAC embeds estimating scores in scheduled slots, with zero scores for missing observations and n/(n−p) correction; it does not impute returns. Tests match trusted statsmodels calculations for HAC and analytic influence measures. Circular block weights jointly resample dates across all bins/states/losses. Labels and saved forecasts remain fixed; no learner is refitted in those draws.

The four original fitting/diagnostic/runner/reporter files were frozen before fitting and remain unchanged. The later completion module adds diagnostics already requested by the task and repairs presentation. It does not alter coefficients, cutpoints, bases, forecasts or scientific selection. Its separate code hash and before/after coefficient/forecast equality are recorded.

| Critical variable/key → file | Meaning / units / default | Consumers / cutoff |
|---|---|---|
| ROOT/OUT/CONFIG → c2r_development | Relativeinstalledprojectroot/C2Rartifacts/separateprefitJSON | Portablepathlib; no machinepath |
| EBM_DATA_ROOT → load_inputs | Optionalexport, defaultROOT/data; symlink/traversalrefsrefused | No .env/secrets/API |
| PINS → c2r_development | Five actual supplied spec/NPZ/source-manifest hashes | Gatebeforefit |
| dates,q,z,slots → load_inputs | 1472ISOETkeys,Nx78fractions,logpriorR,scheduledindex | Matchbydate, notBtable |
| n_Q/n_Z0/date_range → protocol | 1491/1472;2016-01-05…2021-12-31;Jan4priorauxiliary | Allstatecomparisonsmatched1472 |
| origins → protocol | 2016–19train→2020(983→241);2016–20train→2021(1224→248) | Past-only,489pooled,alreadyexplored |
| mean/sd,S0,state_knots_standardized → transforms | TrainpopulationSD(ddof0),linearquantileterciles/tiesupper,naturalmin/tercile/maxknots | Fixedineval; refitwhen trainingpopulationchanges |
| quintile_cuts,quantiles → transforms | 5trainingdisplaybins;.1/.25/.5/.75/.9querygrid | Coarse means/support; notpointwise identification |
| WINDOWS/k0 → readiness/protocol | CLOSE66:78primary,MID24:48,OPEN0:6;P0MID30:42/CLOSE72:78secondary;PRE_CLOSE66:72exploratory;k0=30 | Whole-daydenominator;ETbarstart |
| SCALAR_IDS/PROFILE_IDS → c2r_models | 5scalar+9profilemaps,12contexts | 168fits;noEBM/search/seedgrid |
| degree/df/penalty/max_condition → modelmetadata/protocol | Cubic;time8/12,state4;penalty0;limit1e10 | No adaptive expansion |
| support gates → protocol | Display30dates/10groups,basic50/20,strong100/30 | Originalslot//5groups not independentclusterproof;M1M0fallback |
| lags/blocks/B/seed → protocol | 5/10/20;B1000;seed42;paired42+length | Conditional/asymptotic/descriptive only |
| six-familyHAC10 → protocol | L1slope,L2levels,L3slopeinteractions,L4curvature,rawH1>0,rawH1>0.02 | Holm not P0selectioncorrection |
| top1/top5/drop_rules → runner/QA | 15highestcurrentR;5D_FULLL1Cookdates;exclude2020;LOYO2016..21 | D-onlysharedkeys,FULLprimary,LOYO non-walk-forward |
| materiality → protocol | 2ppclosing,.05globalTV | NOT_CERTIFIED; no point-estimate invariance |
| full_C/deferred → protocol | Officialdatesnull,splitpopulationpending;Zret/Zvoldeferred;Zchginventory;VIX/FOMCabsent | No reserved release |
| source_identities/read_ledger/network_attempts → QA | 84authority/state/sourceidentityrecords,2016–2021readscope,0connectattempts | No2022+scientificdata/API/download |
| fit_sha256 → fit_hashes.csv | Coefficients+transform+date/protocol hash per168fits | No modelupload |


## 9.4 Execution and reproducibility trail

Workingdirectory `.`; shellzsh; Python **3.14.6**; exactmajorversions **{'numpy': '2.5.4', 'pandas': '3.0.6', 'scipy': '1.18.1', 'statsmodels': '0.15.0', 'patsy': '1.0.3', 'matplotlib': '3.11.2', 'pillow': '12.3.0', 'exchange-calendars': '4.13.2'}**;33package snapshot in environment_versions.json. No install/update. SourceSPY/AlpacaSIP/1Min/splitonly,UTCstarts/ETXNYS. ParentNPZSHA2aa2554accde6cfeaadeb5b539b52931f76c1470cdb3a435eefef2e804de0c27; source-manifestSHAa63fe1d6314054240d8b2ac488922a8021f85d55434bfd49001298f5d5e4ff99. C2RprotocolSHA **24ef4122ce069df7f7e228ecfc1f05b48983005273c1e84da10cfb03cdb14bca**. Code/config/source/environment/fit/prediction hashes areactualfileidentities; currentGitcommit is provenance only, not falsely claimed tocontainuncommittedcode.


Commands/operations in actual order (large read-only Python inspection heredocs summarized by exact inputs/fields; persistent source/manifests replace ephemeral tooloutput for reproduction):

1. cat suppliedC2Rattachment; git status --short; git branch --show-current; git rev-parse HEAD; rg --files forAGENTS/C1R/C2R/requirements/locks. Read rootrules, reviseddesign/handoff, original/P0authority/currenthashes, actualC1Rreport/config/session/registries, Cspecsupplement/sourcecode; boundedcat/sed whenlargeoutputtruncated.
2. .venv/bin/python -B - preservation/pin heredoc: five supplied hashesPASS;417existing relativepathhash/size records withGit/time state to /private/tmp/c2r_start.json; installedpackageversions; no credentialvalues. Schema/manifest/window heredoc: actualfourstatecolumns, JSONkeys, matchingoldwindowrows, sourcecachecount/bytes.
3. apply_patch introduced coremodules/CLI/tests/reporter. First .venv/bin/python -B -m unittest discover -s tests -p 'test_c2r*.py' -v →7PASS/1FAIL on exactendpointfloat. Fixedtesttolerance only. Second samecommand →8/8PASS,0.096s. One multi-filepatch contextmismatch failedatomically; reapplied exactpatch, ASTvalidated.
4. .venv/bin/python -B -m unittest discover -s tests -p 'test_c*.py' -v > /private/tmp/c2r_tests_pre_fit.log 2>&1 →20/20PASS,0.511s. ASTparsePASS. .venv/bin/python -B scripts/c2r_development_models.py prepare > /private/tmp/c2r_prepare.log 2>&1 →exit0,1472dates,pre-fitfreezeSHAabove,NOscientificmodel fit.
5. mkdir -p artifacts/C/C2R_development_v1_1; .venv/bin/python -B scripts/c2r_development_models.py run > artifacts/C/C2R_development_v1_1/run.log 2>&1 →exit0,7.479871s,60scalar/108profilefits; all12contexts. Source/chronology/closure/window/H1checks beforefit. No expansion afterscore. Statsmodelsfuturetuplewarningsrecorded; currentversionoutputsvalid.
6. Readcompactmodelscore/family/normalization/supporttables. .venv/bin/python -B scripts/c2r_development_models.py report > artifacts/C/C2R_development_v1_1/report.log 2>&1 →exit0,29.11s,13figures,84coretrain/evalscorechecks +pooled/cellchecks. DefaultMatplotlibhomecacheunwritable, permittedautotempcache used. Contactsheet inspected withimage tooling.
7. Added reporting-only c2r_completion, no newfit. MPLCONFIGDIR=/private/tmp/c2r_mpl_cache .venv/bin/python -B -m ebm_research.experiment_c.c2r_completion > artifacts/C/C2R_development_v1_1/completion.log 2>&1 →exit0with emptycalibrationbinwarnings. Preserved firstlog ascompletion_first.log; explicitemptyABSTAINguard/regressiontest; samecompletioncommand again; combinedsuite21PASS. Coefficients/forecastsunchanged.
8. Individualfigure14visualreview detected lexicographicnumericblocksorting. Addednumericperiodsort+regression; QQaxisfractionlabel clarified. Samecompletioncommand again →exit0,14figures,norefit. .venv/bin/python -B -m unittest discover -s tests -p 'test_c*.py' -v > artifacts/C/C2R_development_v1_1/tests.log 2>&1 →22/22PASS,0.613s. Re-viewed correctedfigure14.
9. Finalpythonheredoc:417baselinehashes, originalsource/statehashes, source-slot/datepointers/noQcopy,168registry/datehashkeys, bothpast-onlyorigins, calibrationcounts/emptyflags,14PNGhash/decode/dimensions, sourcecache72/10,318,012bytes, AST/whitespace/diffchecks. Wrotefit_hashes/baseline/environment/logsnapshots/finalprovenance. Narrative-onlyresultclarification, nofit.
10. Initialinline session-reportwriter failed NameError fromunescapedliteral braces in an f-string beforewriting anyreport. Replacedwiththissavedliteral-safe reportwriter /private/tmp/c2r_write_session.py; no scientificfileaffected. Wrote synchronizeddetailedreportsinbothrequiredpaths, thensealedfinalfilemanifest/exactbytes/Gitstatus.

Numericrun7.479871s andinitialrender29.11s areinstrumented; completionpasseswereseconds-scale/norefit, notseparatelytimed. PeakRSS notmeasured. NoGPU/multiprocessworker/API/remotejob. run.log~225KB, otherlogs small; source/credentials neverdumped.

Freshclone: restore matchingauthorizedP0NPZ+78sources+C1Rstate frommanifests, or exportEBM_DATA_ROOT. Codeclone doesnotshiplicensedinputs/ignoredNPZs. UsematchingPython/packageversions; existing setup python -m pip install -e ".[stage1_5]" is a documented futuremachine setup, NOTexecutedunderthezero-networktask. WithversionedC2Rfreezealready present run:

```sh
python -B -m unittest discover -s tests -p 'test_c*.py' -v
python -B scripts/c2r_development_models.py run
python -B scripts/c2r_development_models.py report
python -B -m ebm_research.experiment_c.c2r_completion
```

prepare isonlyforanabsentreviewedfreeze andneveroverwritesit. OptionalwritableMPLCONFIGDIR avoidstempfontcachewarning. No vendorcredentials/networkrequired. NeverrunP0acquire/run/verify torestoreabsentinputsunderC2R; missing/mismatchedinputstopsBLOCKED_SOURCE_IDENTITY. Originalfourfrozenfilesarecheckedbyrun; completionseparatehashregistered. Matcharraysat1e−10acrossBLAS/platforms; notuniversalbitwiseequality. Narratives/finalsessionaudit areversionedreviewrecords, regeneratedwithdocumentedcompletion/manualaudit ratherthananunapprovedscientificrerun.


## 9.5 Tests, quality and scientific integrity

| Gate | Actual result/scope |
|---|---|
| Source/stateidentity | PASS fivepins,78minutehashes,statehash; no minutere-extraction/source change |
| Real Q/state/time | PASS1491Q/1472Z0,finitepositiveR,Qclosure/nonnegativity,rv/R,6windows,scheduledordinaryp(d),expZ0≈RV_prev |
| Newstatisticalchecks | PASS10C2Rtests: basis/tails,tensor-explicitOLS,HAC/influencevsstatsmodels,targets-invariantfeatures,rank/TV,blocks/output,calibrationempties,numericperiodsort |
| Existingfixtures | PASS4C1R+8P0:390increments/78bins,firstopen/noovernight,endpoints/DST/holiday/half/missing/duplicate/badprice,strictpriorchain |
| Totaltests | 22passed/0failed final; syntheticPASS nottick-levelmarketqualityproof |
| Chronology/matchedkeys | PASS983→241(2020),1224→248(2021),489pooled; train-onlyscales/cuts/knots,sharedforecastdatehashes |
| P0reproduction | PASS2.00498143427624pp,negligibledelta; reuseold5/10,new20only andfixedforecastpaired5/10/20 |
| Savedfit/plotreconciliation | PASS84coretrain/evalscores,pooledscores,3rawgroups/wholefitcellmeans,observed=fitted+residual;atol1e−10/scores1e−12 |
| Rawcomposition | PASS everychronologicalprofileforecastnonnegative/simplex, maxsumdefect<3e−15; no clipping/M8 |
| Sensitivities | PASSFULLunchanged;15topR/5fixedCook/exclude2020sharedkeys; transformrefitperchangedtrain; LOYOnotwalk-forward; unsupportedscienceABSTAIN |
| Images | PASS14principalPNGs+contact decodednonblank>=1600px; hashes/dimensions/source refs; actualcontact/individualrepairreview |
| Firewall/preservation | PASS417baselines+source hashesunchanged,sourcecachegrowth0,no2022+scientificread/API,0downloadbytes,noC3/officialsplitrelease |
| Scientificscope | QUALIFIEDconditionalassociation,weaknonlinearmoderation,negativeprofileincrement,sparseness/crisismissingness;no populationcertification |


Actual OLS n and degrees of freedom count days, never 78N. HAC/Wald and block intervals require suitable moments, weak dependence/stability and a valid law for the selected complete-session population; those premises are not proved here. White/BP/Koenker use a small fixed auxiliary design, not 78 time dummies. JB, ARCH, Ljung–Box, RESET and F tests have heuristic reference p-values under dependence. ACF/PACF compress eligible-date gaps for descriptive summaries; HAC and resampling preserve scheduled spacing. Scalar Gaussian AIC and adjusted R² are not assigned to generic profile models. Holm addresses only the named finite family under valid marginal p-values; it does not undo P0 selection or certify a raw pointwise mean.

The exact SPY Q response, windows, immediate predecessor and information cutoffs were preserved. P0 labels are retrospective. Origin-specific S0 uses the same numeric state with training-only cuts, including the one disclosed D_FULL boundary difference from rank labels. All 2016–2021 dates were already explored; 2020/2021 backchecks are not untouched validation. Four incomplete March 2020 sessions remain absent. H1 interval lower bounds below 2 pp and TV intervals extending above 0.05 do not certify materiality or near-invariance. Full-C horizon/population, Zret, Zvol and reserved-data decisions remain pending.

## 9.6 Errors, anomalies, decisions and recovery

| When/location | Symptom/cause | Fix/affected files | Recheck/unresolvedscope |
|---|---|---|---|
| Initialbasisendpointtest | Expected1exact,actual0.9999999999999999; confirmedroundoff | 14-decimaltoleranceintestonly, no basis change | 8then20/21/22PASS; beforeanyscientificfit |
| Atomicpatchcontext | paired_scope literalcontextmismatch | Patchfailedwithnoedits; correctedexactpatches | AST/testsPASS |
| Statsmodels0.15ARCH | FutureWarningtupledefault changesin0.16/after2027 | Retainedwarninglog/pinnedversion, no warning-onlyrefit | Currentdiagnosticsvalid; futuremigrationmustretestreturnhandling |
| PyArrowlocalread | sysctlCPUcache/neonOperationnotpermitted | Warningonly,allhash/I/Ocheckswork | No escalation/workaround needed |
| Matplotlibcache | Defaulthomepathunwritable | Permittedautotempfontcache; explicitMPLCONFIGDIRsubsequently | 14figuresvalid; rebuildablecache |
| Firstcompletioncalibration | Emptyfittedquantilebinsfromconstant/categoricalties; Meanofemptyslice | Explicitn0/NaN/ABSTAIN; helper/regression; firstlogretained | 21then22PASS; nofit/forecastchange |
| Visualfigure14 | Numericblockkeyslexicallyordered,invalidconnectedchronology | Numericsort/smallregression; replacedonlysession-ownedfigure14/contact/manifest | Correctedimagevisuallyreviewed; earlierchronologyplotinvalid, underlyingmeans/modelresultsunchanged |
| QQunitclarity | QQrawfractionswhileotherresidualpanelsinpp | Regeneratedfigure04withfractionylabel; manifesthashupdated | Residualvaluesunchanged; imagedecode/hashPASS |
| ExistingC1Rnarrative | Series.modeboundmethodrenderedinstatetable, actualCSVledgercorrect | DocumentedandpreservedC1R; C2Rexplicitcolumns | No source/scienceimpact |
| Firstsessionwriter | NameError source_manifest fromunescapedf-stringliteralbraces, line121 ofinlineheredoc | No reportwaswritten; savedliteral-safe temporarywriter | Detailedreportscreated; no scientificoutputaffected |
| Scientificlimits | Crisisexclusions,sparse2020cells,negativeprofileincrement,weakmoderation | Preservenegative/inconclusiveestimatesandABSTAIN; no window/source/modelrescue | Independent/full-Cclaimsdeferred |


All fixes were routine engineering or reporting corrections. No scientific target, state, window, source, testing rule or candidate setting changed after outcome inspection. FULL remains primary. Completion verifies unchanged coefficient and forecast hashes. No source/math/timing/hash invariant failed. The initial empty-bin presentation and figure14 chronology are superseded by the corrected final files; the earlier screenshot should not be used as a time plot. The underlying block means and model results were unchanged.

The last successful checkpoints are the numerical run, 84 independent score checks, final completion with 14 figures, all 22 tests, and source/baseline/chronology/hash checks. Trust outputs only under their final hashes and stated conditional scope. Restore missing inputs through approved manifests; never overwrite a mismatching source or borrow B's alternative repair. Read the main report, gallery, theory ledger, protocol and fit/provenance registries first. No background process remains. C3 requires a new instruction; no fitting starts automatically.

## 9.7 Resources, Git summary and handoff

At this audit checkpoint, C2R artifacts occupy approximately **27,101,678 bytes**, including **4,236,212 bytes** of figures/contact sheets. Nonfigure artifacts are **22,865,466 bytes**. Code, protocol, tests and reports add modest text overhead; the final `files_manifest.json` records exact file sizes/hashes and totals. Nonfigure retention is below the 100 MB target and 250 MB alert, with total retention far below the repository's 1 GB target and 2 GB flag. New raw/source bytes, source-cache growth and downloaded bytes are all **zero**. The 72-file source supplement remains 10,318,012 bytes. No source table, target Q array or per-fold input Parquet was duplicated.

The largest new nonfigure outputs are daily error summaries (~7.8 MB), scalar influence (~5.8 MB), descriptive predictions (~2.7 MB), coefficient/transform metadata (~2.4 MB) and chronological predictions (~0.9 MB). The preservation sweep covered 96.6 MB of scoped existing artifacts plus about 14.9 MB of authorized minute references, avoiding a broad multi-GB scan. Numeric work took 7.48 seconds, initial rendering 29.11 seconds, and completion passes a few seconds each. Peak RSS was not measured. Temporary audit/font-cache material is under 1 MB and rebuildable. No package install, source purchase, upload, GPU job, model sweep or background worker remains.

Tracked Git diff/stat are empty and `git diff --check` passes. Preexisting untracked C1R work and supplied specs remain unchanged. New C2R files are untracked until separately authorized; NPZs/logs remain ignored. Nothing was staged, committed or pushed. Ending status:

```text
?? artifacts/C/C1R/
?? artifacts/C/C2R_development_v1_1/
?? config/C_C2R_development_protocol_v1_1.json
?? config/C_full_protocol_v1_1.yaml
?? docs/specs/C/
?? reports/C/C1R_protocol_and_coverage.md
?? reports/C/C2R_OLS_state_dependent_splines_full_diagnostics.md
?? reports/C/C2R_coding_session_20261022.md
?? reports/C/C2R_scientific_visual_gallery.md
?? reports/C/C2R_theory_applicability_and_limitations.md
?? reports/sessions/20261022_1652_C_C1R_session.md
?? reports/sessions/20261022_1750_C_C2R_session.md
?? scripts/c1r_readiness.py
?? scripts/c2r_development_models.py
?? src/ebm_research/experiment_c/c2r_completion.py
?? src/ebm_research/experiment_c/c2r_development.py
?? src/ebm_research/experiment_c/c2r_diagnostics.py
?? src/ebm_research/experiment_c/c2r_models.py
?? src/ebm_research/experiment_c/c2r_reporting.py
?? src/ebm_research/experiment_c/readiness.py
?? tests/test_c1r_readiness.py
?? tests/test_c2r_models.py
```

Handoff: **PASS_WITH_QUALIFICATIONS**. The positive raw closing-allocation association reproduces, but neither an effect exceeding 2 pp nor profile near-invariance is certified. The conditional linear slope and 2.43% scalar MSE improvement coexist with no whole-profile forecasting gain: M0 performs best and primary M4 is 1.66% worse. Piecewise/quadratic additions lack fixed-family evidence. Residual tails, year means, state shifts, sparse support and four missing crisis days constrain generalization. Every observed chronological raw profile nevertheless passes closure and nonnegativity.

A bounded C3 design review could compare EBMs with the strong simple baselines and declared smoothers, retaining negative outcomes and approximation limitations. Actual C3 implementation requires a separate user instruction; no C3 code, prompt or fit was started. The pending full-C decisions are the horizon, split population, Zret, Zvol and reserved-data/source authority.

Read first: [main scientific diagnostics](../C/C2R_OLS_state_dependent_splines_full_diagnostics.md), [interpreted figure gallery](../C/C2R_scientific_visual_gallery.md), [theory and limitations](../C/C2R_theory_applicability_and_limitations.md), then the C2R protocol, `model_registry.csv`, `fit_hashes.csv` and `provenance_and_QA.json`. This report is intentionally mirrored at the AGENTS-required session path and the user-requested C path; it duplicates only small documentation, not research inputs.
