# Five-experiment execution integrity v1

As of 2026-10-23T02:52:27.905410+00:00. Source/legacy/month/config audit: **PASS**; protected preexisting files 843; changed0; unique validated months12/12; remaining raw monthly archives0.

## Actual execution and reproducibility

Working directory: repository root. CLI sequence below uses `.venv/bin/python -B scripts/five_prelim.py <phase>`; every phase log is retained under `../logs`.

1. inventory
2. metadata
3. freeze
4. acquire
5. acquire (small-source recovery; twelve validated months skipped)
6. derive (timestamp-unit failure interrupted)
7. derive (strict-universe audit failure)
8. derive (corrected RTH/cache adaptation; PASS)
9. screen
10. report
11. verify

No packages installed; Python/dependency/code snapshots: `../manifests/runtime_environment.json`. New tests: `.venv/bin/python -B -m unittest discover -s tests -p test_five_prelim.py -v`; scoped existing pure-data/OLS tests recorded in test evidence, excluding EBM training. Synthetic tests do not certify every raw observation.

{
  "at": "2026-10-23T02:50:14.151953+00:00",
  "suites": [
    {
      "command": ".venv/bin/python -B -m unittest discover -s tests -p 'test_five_prelim.py' -v",
      "exit_status": 0,
      "tests": 19,
      "seconds": 2.938,
      "status": "PASS",
      "log": "logs/tests_final.log",
      "sha256": "5d70761cca36c5b3ae9c02b6e83c6c98028d18af853100ede4c51e23b96d903d",
      "test_names": [
        "test_OLS_hand_calculation_and_trusted_regression",
        "test_actual_ETF_identity_and_same_OC_return_window",
        "test_calendar_next_target_does_not_skip_missing_session",
        "test_duplicates_conflicts_no_silent_preference",
        "test_extended_hours_do_not_invalidate_RTH_cached_fixture",
        "test_fed_raw_shock_sign_bp_and_official_event_join",
        "test_fred_prior_availability_not_future",
        "test_hash_tamper_and_atomic_json",
        "test_microsecond_calendar_regression_and_5m_alignment",
        "test_month_checkpoint_verified_resume_and_tamper",
        "test_semivariance_closure_zero_returns_and_missing_minutes",
        "test_sidecar_wrong_ID_target_and_broken_image_link",
        "test_source_hash_and_allowed_readonly_shared_reference",
        "test_stale_frozen_config_rejected_before_source_access",
        "test_storage_cap_prevents_next_write",
        "test_timezone_DST_and_half_day",
        "test_treasury_identity_and_wrong_sources_targets_rejected",
        "test_volume20_excludes_current_and_future"
      ]
    },
    {
      "command": ".venv/bin/python -B -c 'import unittest; loader=unittest.TestLoader(); suite=unittest.TestSuite(loader.discover(\"tests\",pattern=p) for p in [\"test_c1r_readiness.py\",\"test_c2r_models.py\"]); result=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(not result.wasSuccessful())'",
      "exit_status": 0,
      "tests": 14,
      "seconds": 0.234,
      "status": "PASS",
      "log": "logs/tests_existing_scoped.log",
      "sha256": "b7723539c918c1ebe5c6a11577398505fce7a89cf0b5e05d6fb47710082044e3",
      "test_names": [
        "test_source_path_firewall_and_windows",
        "test_split_integer_chronology_withheld_and_temporary_smoke",
        "test_strict_two_predecessors_and_positive_guard",
        "test_train_only_cutpoints_and_fixed_validation",
        "test_analytic_influence_against_trusted_deletions",
        "test_basis_partition_endpoints_and_linear_extrapolation",
        "test_calibration_constant_fit_marks_empty_bins",
        "test_hac_against_statsmodels_and_calendar_gaps",
        "test_joint_date_block_weights_and_temporary_predictions",
        "test_multivariate_OLS_coefficients_and_closure",
        "test_numeric_block_keys_are_chronological",
        "test_rank_failure_and_invalid_TV",
        "test_tensor_fit_matches_explicit_small_design",
        "test_training_transform_unaffected_by_targets_and_future_extremes"
      ]
    }
  ],
  "total_passed": 33,
  "failed": 0,
  "skipped": "Full-suite discovery deliberately excluded B-stage2B/C3 EBM-training tests; no EBM/ML authorized. Synthetic fixtures and scoped C1R/C2R OLS tests do not certify all data."
}

## Configs and experiment QA

| ID | config_sha256 | QA | result |
| --- | --- | --- | --- |
| P01_INTRADAY_BETA | 197c769732e27298df2ff9a02b290ef2f9d5406404a74db3b7928895155faa3b | PASS | NO-GO |
| P02_SIGNED_RV | 57db40d2fc8b9dfab52282abd07b8e663ae959a2cec832c0dc863c635d995eee | PASS | DATA HOLD |
| P03_TREASURY_HEDGE | fe4a1b73a08bc527b80297ddd0e269375ef290494b75ac5df37c868e0ef9a13b | PASS | WEAK |
| P04_VOLUME_REVERSAL | b12c6d0c70a4dbb13d4de5db64716ca690739c9458e1a817b0716903d187cd37 | PASS | WEAK |
| P05_FOMC_RESPONSE | ab17d8d6d9f1948ab6d62e1bce34cbb96877059f83d180e77c29d991388f095a | PASS | DATA HOLD |

Input fingerprint `877717c8fddd79652f725482ac9bf43ba198f67111dad377c6176ce3f1df8909`; source manifest `5aeef79b565d833bceb832004b638ada449eb6075838ea869b89201cae4256f5`. Original and derived source SHA-256s rechecked before statistics/rendering/final verification. Wrong-ID/target/hash/stale-config fixtures reject; no frozen science changed to work around results.

## Storage and one-pass evidence

{
  "hard_cap_bytes": 10000000000,
  "measured_peak_bytes": 297766292,
  "largest_reserved_envelope_bytes": 397708076,
  "current_incremental_bytes": 26744179,
  "baseline": {
    "hard_cap_bytes": 10000000000,
    "soft_replan_bytes": 8000000000,
    "baseline_repo_bytes": 838104304,
    "physical_free_bytes": 59392000000,
    "monthly_raw_max_bytes": 290814381,
    "retained_new_minute_budget_bytes": 100000000,
    "derivatives_bytes": 100000000,
    "small_sources_bytes": 30000000,
    "plots_reports_logs_bundle_bytes": 80000000,
    "cache_bytes": 20000000,
    "conservative_incremental_peak_forecast_bytes": 620814381,
    "safety_margin_bytes": 9379185619,
    "used_after_inventory": 193152,
    "physical_workspace_total_cap": "No stricter imposed cap discovered; 10GB is explicitly incremental; free space separately checked"
  },
  "new_data_bytes": 19213917,
  "run_bytes": 7263168
}

Exact monthly ledger `../checkpoints/hf_months.jsonl`, network receipts `../logs/network.jsonl`, controlled deletion paths `../logs/cleanup.jsonl`, storage samples including each1MiB download chunk `../logs/storage.jsonl`. Private sources are read only and not redistributed in the ZIP.

## Exceptions and recovery

Sandbox DNS initially failed; approved network execution succeeded.2021 Fed historical-calendar404 was resolved with direct official statements from published dates; non14:00events remain excluded. A microsecond/nanosecond calendar comparison originally rejected valid SPY sessions; the job was interrupted before derivative output/statistical fits, units normalized and regression-tested. Reused BAC/KO files include extended hours; applying the frozen RTH filter restored eligible sessions. The subsequent complete derivation passed; invalid attempts are preserved in separate logs and never used for results. PyArrow emits sandbox CPU-cache/sysctl warnings without affecting returned data or checks. Publisher chart and workbook vintage differences are documented, not repaired by substituting shocks.

## Statistical/visual QA

{
  "P01_INTRADAY_BETA": {
    "status": "PASS",
    "OLS_reconstructed": true,
    "all_curve_coordinates_reconstructed": true,
    "direct_source_bins": 3,
    "supported_common_bins": 7,
    "bootstrap_valid": 493,
    "CI_center_outside_percentiles": 0,
    "note": "Percentile intervals need not contain original estimates; outside centers flagged, never forced inside. Nonlinear curvature not tested."
  },
  "P02_SIGNED_RV": {
    "status": "PASS",
    "support_counts": {
      "high": 5,
      "low": 10,
      "middle": 1439
    },
    "curves": "no valid state shape presented for DATA HOLD; diagnostic references retained"
  },
  "P03_TREASURY_HEDGE": {
    "status": "PASS",
    "OLS_reconstructed": true,
    "all_curve_coordinates_reconstructed": true,
    "direct_source_bins": 3,
    "supported_common_bins": 4,
    "bootstrap_valid": 500,
    "CI_center_outside_percentiles": 0,
    "note": "Percentile intervals need not contain original estimates; outside centers flagged, never forced inside. Nonlinear curvature not tested."
  },
  "P04_VOLUME_REVERSAL": {
    "status": "PASS",
    "OLS_reconstructed": true,
    "all_curve_coordinates_reconstructed": true,
    "direct_source_bins": 3,
    "supported_common_bins": 7,
    "bootstrap_valid": 500,
    "CI_center_outside_percentiles": 0,
    "note": "Percentile intervals need not contain original estimates; outside centers flagged, never forced inside. Nonlinear curvature not tested."
  },
  "P05_FOMC_RESPONSE": {
    "status": "PASS",
    "support_counts": {
      "negative": 11,
      "positive": 36
    },
    "curves": "no valid state shape presented for DATA HOLD; diagnostic references retained"
  }
}

Actual exported PNGs are decoded and tested for minimum size/nonblank content. Text extents, shared X grids, support masks, coordinate roundtrips, independent source-row means and OLS reconstructions are checked. A manual opening of all six reviewer images is separately recorded in `../manifests/manual_visual_review.json`; until present, subjective visual inspection must not be inferred from automated QA.

Manual review record:

{
  "at": "2026-10-23T02:50:14.146242+00:00",
  "method": "Actual tool view_image openings, final five summaries and overview plus corrected support/contrast exports",
  "verdict": "PASS",
  "final_reviewed_images": {
    "P01_INTRADAY_BETA_summary.png": "1c026d30a89098ae4f11c24806389f211619e479c039eb6e3202eac8ea52b6d6",
    "P02_SIGNED_RV_summary.png": "ce12cca70ff47124961720d13e6bd85efce568b979f342145686c0de3a61fdc8",
    "P03_TREASURY_HEDGE_summary.png": "5f39ff6ef838ee17bfdd4904bba64009bf81f8a9ce056b46c8f6f17366917317",
    "P04_VOLUME_REVERSAL_summary.png": "82d2b6c8978cc774936b0d2e955dd87c9c3adf2a6053472aa62d455b583738e6",
    "P05_FOMC_RESPONSE_summary.png": "f4cb6c514b201587c51915951dbb55c16ea7cd5b36e1ec60931149cd77d162d2",
    "five_experiment_overview.png": "5607b1c3c5c0b1f13b228b83a9de771b007fff9424a8fc01224242e196adf327",
    "P03_TREASURY_HEDGE_support.png": "4fe02370e0b7278a1ff94290b3137e7ae92909bdfd917942ddc905258745d0e2",
    "P04_VOLUME_REVERSAL_support.png": "58033742e57fc6b8c0dab49cddb687acdba747260b225c9217c90785a205a9ba",
    "P03_TREASURY_HEDGE_shape_contrast.png": "62f322d5d9ea7a4cade5143bed82f53e8fd2c63b2878bc04588b83d6a71611eb"
  },
  "additional_earlier_review": "P01 scatter/support/contrast and P04 contrast inspected during development; final automated PNG/data/metadata checks cover all13.",
  "findings": "Readable axes/units/dates/counts and HOLD warnings; no final clipped text. Manual review caught support-chart state-color inconsistency; fixed canonical state order and added rejection fixture before release. No scientific estimates changed."
}
