# Experiment B Stage2A — detailed coding-session audit

## 1. Session identification and verdict

**PASS WITH QUALIFICATIONS — implementation/QA, not scientific success.** Completed all requested C1/C2/S1 E/L fits, untrimmed/stress/Huber/source comparisons, standard appropriate diagnostics/inference, matched fixed and chronological quarterly validation,8figures, machine audit and handoff. No EBM, new provider/history/indicator, trading or sealed outcome work. A remains on hold.

User execution prompt: attachment456cf46c-6dc6-4d66-96de-67b635f7a11a/Pasted text.txt, “Codex execution prompt — Experiment B Stage2A”. Source-inspection time recorded2026-10-16 21:34:59UTC/17:34:59EDT after orientation; final report2026-10-16T18:02:42.891692-04:00, America/New_York UTC−04. Agent Codex, exact backend model identifier unavailable. Starting/ending branchmain, commit64794f0ee2846784aeab5c96460b16b82f6097a2. Starting tracked tree clean, one preexisting untracked user document preserved. No commit/stage/push/reset/branch or modification of preexisting tracked files.

Verified actual metadata2680full/2675eligible, training1495,validation497,sealed683. All57Stage1 coefficient/lag rows and21matched-original trio rows reproduce; principal maxdifference4.44e−16. Five March18 original anchors/manual return/RV checks match exactly; midday14minute gap outside inputs, not a reason to delete.

10successful state specifications (C1/C2 E/L plus optional lateW moderation, S1dimensions4/6×E/L),3OLS references,2naive rules.40fixed deletion/source fits+8Huber points;104quarterly refits;44temporal fits;65candidate-influence refits. Registry286entries=274new regression/refit/influence/temporal fits+10legacy verification fits+2rules. No candidate fit/rank failures. Scientific contrasts:501COMPUTED,350supportABSTAIN, distinct from fitted-model status.

**Scientific finding:** no convincing incremental mean/prediction benefit. Sixpredeclared training moderation/curvature questions all Holm p≥0.817. Best primaryquarterC1-E RMSE30.329bp,C1-L30.363 versusN0zero30.307. Paired gainsC1-E−1.348bp² CI[−10.745,8.049],C1-L−3.383 CI[−16.064,9.297]. Splines≈31.43–31.49bp worse; FULL remains primary despite some improved trimmed/Huber fixed-L scores. HighRVX0 has22E/15L rows, so raw anchored four-point claims ABSTAIN. Negative/inconclusive science is retained. Future separately authorized EBM comparison is ready against strong same-date references, not a promised improvement.

## 2. Exact file inventory and preservation

| Action | Repository-relative path | Why / contents / functions-schema | Consumers | Recovery |
| --- | --- | --- | --- | --- |
| CREATED | artifacts/B/stage2A/01_joint_support.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/02_state_slopes.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/03_varying_coefficients.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/04_supported_anchored_contrasts.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/05_residual_and_qq.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/06_variance_and_time.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/07_validation_predictions_calibration.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | artifacts/B/stage2A/08_validation_error_by_state.png | Compact registered machine table or one of8 scientific figures. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | config/B_stage2A_linear_spline_protocol.json | Final pre-fit v2 input hashes/menu/preprocessing/cadence/support/inference/selection settings. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | config/B_stage2A_linear_spline_protocol_v1_pre_fit.json | Preserved pre-fit first draft; validation-cutoff wording clarification versioned before outcomes/fits. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_coefficients.csv | Compact registered machine table or one of8 scientific figures. Shape (3283, 21). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_inference.csv | Compact registered machine table or one of8 scientific figures. Shape (851, 30). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_manifest.json | Input/output/code/config/software/source hashes, fit chronology and resources, recommendations. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_model_diagnostics.csv | Compact registered machine table or one of8 scientific figures. Shape (1961, 41). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_models.csv | Compact registered machine table or one of8 scientific figures. Shape (286, 32). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_paired_loss_tests.csv | Compact registered machine table or one of8 scientific figures. Shape (58, 17). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_sensitivity.csv | Compact registered machine table or one of8 scientific figures. Shape (90, 21). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_support.csv | Compact registered machine table or one of8 scientific figures. Shape (72, 11). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | data/registry/B_stage2A_validation_metrics.csv | Compact registered machine table or one of8 scientific figures. Shape (93, 24). | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | docs/experiment_B_stage2A_methods_and_model_registry.md | Exact equations/columns/knots/units/tails/df/selection/support/reproduction, linked to numeric results. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | reports/B/stage2A_state_linear_and_spline_results.md | Complete substantive scientific results, diagnostics, uncertainty, negative findings, sensitivity and EBM handoff. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | src/ebm_research/experiment_b/stage2a.py | Offline frozen protocol/source/baseline/sensitivity/inference/prediction/registry CLI. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | src/ebm_research/experiment_b/stage2a_diagnostics.py | Adapted Stage1.5 diagnostics, influence, White applicability, spline geometry and calibration. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | src/ebm_research/experiment_b/stage2a_report.py | Eight reviewed plots plus standalone science and exact-method reports. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | src/ebm_research/experiment_b/state_models.py | Core natural spline/state designs, training-only basis, fit and covariance/contrast math. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | tests/test_b_stage2a.py | Four tiny deterministic scientific-math, information, nesting, extrapolation and pairing tests. | CLI/report/manifest or review | Rebuild same stage-owned artifact from pinned inputs; preserve sources. |
| CREATED | reports/sessions/20261016_1802_B_stage2A_state_linear_spline_session.md | Mandatory unique session audit | Review/handoff | Preserve historical report. |
| CREATED (ignored) | data/derived/B/B_stage2A_validation_predictions.parquet | One38766row×18column long validation prediction file;78series×497dates, source/info/mode/variant/fit-asof/history/actual/forecast/loss/state/paired differences | Manifest, validation and future EBM comparisons | Offline CLI rebuild; no per-model/year/fold files. |
| CREATED (ignored) | data/derived/B/B_stage2A_march18_anchor_check.json | Five private original prices plus independent scalar returns/RV; hash in protocol | Source integrity | Rebuild from existing2020source; do not publish raw prices. |
| CREATED (ignored) | logs/stage2A_matplotlib/fontlist-v3.11.0.json | Standard289954byte font cache, no research rows | MatplotlibAgg | Rebuilds automatically. |
| MOVED stage-created | config/B_stage2A_linear_spline_protocol.json → config/B_stage2A_linear_spline_protocol_v1_pre_fit.json | Preserve initial draft, original path recreated asv2 before any model fit/validationY | Protocol audit | Both versions retained. |
| INSPECTED/PRESERVED preexisting untracked | docs/specs/experiment_B_stage1_5_detailed_diagnosis_exact.md | Existing user artifact unchanged SHA9aa7b547de674df736c30d28fe92565b92bb4bee62515f2af7e393a412b0ec42 | User review, not new authority inferred | No overwrite/move/deletion/staging. |

No preexisting user/raw/canonical/spec/report file deleted or overwritten. Existing dataset read by actual manifest path, not guessed/copied. Only move is our new protocolv1 draft; v2 supersedes it before fitting/validation labels with a documented clarification.

Consequential INSPECTED inputs: AGENTS.md,README,.gitignore,requirements-stage1_5.lock.txt; approvedBv1 applicable§§2,4–8 and companion stages; frozenStage1selection/daily/coefficient/state/coverage/QA/source crosswalk/main report and calculation code; Stage1.5main report/summary/manifest/influence; D2original/D2.1cnative39row manifest. Existing daily/benchmarks/linear_diagnostics/stage1/pilot/acquisition code reused unchanged. Stage1execution6module hashes and Stage1.5helpercode remain verified. .env never read/printed. Source use is bounded: this stage independently reads only the2020annual source filtered toMarch17/18 for anchors, not a new multi-year source audit; D2.1c source definition/hash read, not an alternate feed assembled.

Transientfiles: config/B_stage2A_linear_spline_protocol.json.tmp(v1/v2), data/derived/B/B_stage2A_march18_anchor_check.json.tmp, B_stage2A_validation_predictions.parquet.tmp and registry/B_stage2A_manifest.json.tmp were stage-created→atomically MOVED to final; no remnants. Three successful publications reused/replaced only their newly created Stage2A outputs. Tests automatically created/deleted four tiny files in three tempdirs: ebm_stage1_smoke_*/daily.parquet, ebm_d1_smoke_*/smoke.parquet, ebm_d2_smoke_*/tiny.txt and requests.json. Recreate via tests. No preexisting deletion. Standard matplotlib transient lock/cache internals not separately instrumented; finalfontcache listed. No dependency installation or environment rebuild.

## 3. Critical functions/classes and variables

Source function register (all new important functions; significant input/output/cutoff/exception semantics follow):
| Path:function(signature) | Purpose / key algorithm | External caller / semantics |
| --- | --- | --- |
| src/ebm_research/experiment_b/state_models.py:specifications() | Bounded E/L candidates, including labeled late W-moderation sensitivities. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:guard_history(frame, asof) | Require unique ordered development dates with completed targets before asof. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:raw_rcs(z, knots) | Restricted cubic curvature terms with linear tails, scaled by knot range². | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:fit_preprocessing(frame, asof) | Fit predictor-only cutoffs, centering and natural spline transforms on past. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:curvature(z, pre, dimension) | Apply training-frozen, centered/scaled natural curvature at any finite Z. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:design(frame, spec, pre) | Explicit E/L matrix; E never reads W, and C2 is literally nested in S1. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:fit_model(frame, spec, pre, asof, robust=False) | Guard then SVD OLS or point-only Huber; reject rank loss explicitly. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:covariance(fit, kind=5) | Bartlett HAC with n/(n-k), normal reference; OLS and HC3 comparators. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:evaluate_linear(fit, vector, lag=5) | Covariance propagation for one fixed linear contrast, not CI subtraction. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:vector_at(fit, x, z, w=0) | Whole response design row at one named state, including all intercept terms. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:slope_vector(fit, z, w=0) | Full-row difference at X=1 and X=0, valid since these models are linear in X. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:wald(fit, columns, lag=5) | Independent coefficient restrictions; withhold singular covariance p-values. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/state_models.py:preprocessing_hash(pre) | Portable identity of predictor-only preprocessing, including quarterly fits. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:training_inputs(root) | Verify frozen daily/source lineage and read training plus date metadata only. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:march18_check(root, train) | Independently verify five original price anchors before influence interpretation. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:choose_support(train, pre) | Predictor-only X/W anchors and coarse cells, fixed before curves/outcomes. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:freeze_protocol(root, path) | First-run predictor-only protocol freeze; never overwrite a previous protocol. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:support_rows(frame, pre, protocol, cohort='train') | Coarse empirical support with explicit low-count/block abstention. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:cell_supported(support, info, state, x, protocol) | CLI entry/formatting helper; see source and module semantics below. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:fit_metadata(fit, fit_id, variant, mode, frame, elapsed, pre, asof) | Every attempted successful fit has a dataset/date/preprocessing identity. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:coefficient_rows(fit, fit_id, kinds=None) | CLI entry/formatting helper; see source and module semantics below. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:inference_rows(fit, fit_id, protocol, support) | Whole-response/slope contrasts and correctly nested joint covariance tests. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:paired_arrays(candidate, comparator) | Exact date-paired comparator loss minus model loss; reject mismatched keys. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:metric_row(frame, forecast, n1, **keys) | Matched descriptive/OOS bp metrics, with named causal N1 denominator. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:load_validation(root, protocol, with_outcome=True) | Read eligible 2022–2023 rows only; sealed scientific columns never requested. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:run(root, protocol_path) | Execute the bounded frozen train→sensitivity→validation workflow offline. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:sensitivity_row(fit, frame, protocol, kind, robust=False, support=None) | Fixed-design fitted state slopes; distinguish parameter projections from raw cells. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:predictor_audit(validation, pre, protocol) | Validation feature occupancy/range only, performed before validation Y read. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:paired_tests(predictions, metrics, protocol) | Date-paired validation loss inference and the predeclared recommendation rule. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:publish(root, protocol_path, protocol, baseline, registry, coefficients, inferences, diagnostics, support, metrics, paired, sensitivity, predictions, preprocessing, feature_audit, recommendations, fits, train, validation, wall, cpu, free) | Write compact registries, one prediction file, figures/report and hash manifest. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a.py:main() | CLI entry/formatting helper; see source and module semantics below. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a_diagnostics.py:full_diagnostics(frame, fit, fit_id, stage1, protocol, refit=None) | Reuse the tested Stage1.5 residual battery, tailoring df and spline interpretation. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a_diagnostics.py:prediction_diagnostics(frame, predictions, model_id, mode) | Coarse supported calibration, state/error magnitude checks on validation only. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a_report.py:table(rows, columns) | CLI entry/formatting helper; see source and module semantics below. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a_report.py:make_figures(train, validation, fits, protocol, predictions, metrics, inferences, diagnostics) | Training fixed-basis shapes plus explicitly labeled2022–23 validation. | CLI/helpers/tests; module I/O and exceptions below |
| src/ebm_research/experiment_b/stage2a_report.py:write_report(manifest, protocol, registry, metrics, inferences, diagnostics, support, sensitivity, paired, coefficients=None) | Standalone results and compact exact-method register, all linked to machine rows. | CLI/helpers/tests; module I/O and exceptions below |
| tests/test_b_stage2a.py:StateModelTests | Four deterministic tests +100row small predictor fixture | unittest; no simulation framework/network |

**state_models I/O and algorithms.** Inputs: ordered eligible development DataFrames(date,X/W/Ybp,raw/logRV), explicit candidate spec, JSON-frozen preprocessing/asof. Outputs: rank-checked matrices, statsmodels results, covariance/contrast/Wald dictionaries. guard_history rejects duplicate/unsorted/outside2016-01-05…2023-12-31 or targetdate≥exclusiveforecastcutoff, and cutoffs>2024-01-01 before fit-data access. Edesign neverreadsW.

Natural restricted cubic raw_rcs uses K4/6knots and K−2curvature terms:
h_j=[(z−k_j)+³−(kK−k_j)/(kK−k(K−1))·(z−k(K−1))+³+(k(K−1)−k_j)/(kK−k(K−1))·(z−kK)+³]/range².
Span includes1,Z,linear tails. Predictor-only curvature projected off1,Zc by training least squares, centered0 at medianZ, scaled by training residualSD; invertible span-preserving transform aids conditioning. EveryS1 design literally includes C2's1,X,Zc,XZc; dimensions4/6 yield E8/12,L9/13. Tests verify nesting/rank/natural-tail second finite differences. No silently dropped variables.

fit_model uses SVD/pseudoinverse OLS, stops rank<p or condition>1e12. HuberT1.345/MAD/maxiter200/tol1e−8 only point estimates/differentloss, no OLS/HAC scientific inference. covariance ordinary/HC3/Bartlett5/10/20,n/(n−k),use_tFalse,normal95%. evaluate_linear vβ and vΣv′, not separate endpoint subtraction; wald checks restrictioncovariance rank, abstains ifsingular.

**stage2a I/O/chronology.** training_inputs verifies immutable files and reads full date metadata only plus filtered training; march18_check only original2020Mar17/18+private5anchor scalar audit. freeze_protocol records predictor-only menu/state/knots/grid/support/schedules/selection before fitting/validation labels. support_rows state×X×L-Wband counts disjoint5eligible-row blocks. Local attempt registers each fit/influence/refit/purpose/error with exactparameters/preprocessinghash/rank/condition/cost/library/formula/asof/sample; no failures occurred.

run FULL→fixed-original-preprocessing stress/source/Huber→temporal/influence then validationpredictors→validationlabels. Fixed forecasts train2016–21; quarterly only earlier completed labels, original categoricalthresholds, past-only spline/centering. N1 expandsdaily from strictly priorY. Everyforecast recordslastobservedtargetdate<forecast/asof. paired_arrays rejects unmatched/duplicate dates; paired_tests meancomparator squaredloss−candidate squaredloss with HACmeanCI. metric_row matchedbpRMSE/MAE/MSE,bias,p95error,correlation,direction, namedN0/causalN1R². Undefinedconstantcorrelation withheld; retrospective-majoritybaseline explicitlydescriptive.

**diagnostics/report.** Reuses Stage1.5residual/influence functions, tailoring settings/Whiteauxrank/RESET/VIF andcopying pandasreadonly arrays. FULLrankforecastmodels remain identifiable while algebraicallysingular expandedWhiteauxproducts areNOT_APPLICABLE(noinvalidp). Addsstate/periodresidualmoments,Zbins,conditionalvariance, fixed-gridcurvewiggles and5exactfixed-basis influence refits/model. New Cookrankings diagnostic only, never choose deletions. Calibrationn/support explicit; constantN0deciles/correlation NA. RichS1RESET replaced by nestedcurvatureWald. Figures show conditionalfixed-basispointwiseHAC5 only supportedregions; modelprojections never equated to rawconditionalmeans. Report numbers from machinefiles/protocol/manifest.

Critical exact variables/defaults:
- dataset_id=B_SPY_daily_split_source1_stage1_v1; primaryD2AlpacaSIP/SPY/split plus exactlyD2.1c39native-price missing-minute patch. No D2.1b union. Source rights/provenance/native adjustment/one-sided closing caveats retained. No new data/http. Original source/daily hashes unchanged.
- X=10000(P10/Pprev−1),W=10000(P1530/P15−1),Y=10000(P16/P1530−1),bp; anchors09:59/14:59/15:29/15:59barstartcloses, previouspermissiblefull15:59, skiphalfdaysonly, nevermissingordinaryfallback. RVsqrt30openinglog-increment squares(firstclose/open), Zlog(RV+1e−8). E10:00X/Zonly,L15:30addsW,Yafter16:00; barUTC/sessionETZoneInfoDST.
- train2016-01-05–2021-12-31 n1495,validation2022–2023 n497, sealed2024–2026-09-30 n683metadataonly. Aonhold. preproc originalRVcuts[0.001558374721607106, 0.0024281183976187152],equalitylowerbin,Zref=-6.257012700074515; representativeZwithin-tercilemedians[-6.673927481801225, -6.256791269350911, -5.709473991823623]. Exactlogcuts/knots/transformscales in protocol;8historicalpreprocessing identities inmanifest.
- S4quantileknots.05/.35/.65/.95(primary),S6.05/.23/.41/.59/.77/.95(sensitivity); cubicdegree3, natural linear tailsoutsideinnerboundaries, no clipping/futurebounds. Centering/scales originalFULLforstress; quarterly recalibratedonlypastpredictors, categoricalcuts stayoriginaltrainingthroughvalidation.
- Modelmenu13: C1_E/C1_L/C1_L_Wmod,C2_E/C2_L/C2_L_Wmod,S4_E/L,S6_E/L,OLS1_E/OLS3_L/OLS2_L;2sharednaives. Sixprimary C1/C2/S4 E/L; higherdf/optionalW notautomaticreplacement. No extraWspline/penalization needed for bounded menu/support; no EBM.
- x0=0,x_magnitude10bp,9pointxgrid±10,coarsexbins−5/+5; L W0=0 band[-16.620280276007815, 18.84402635020036]. Minimum50observations/20nonoverlap5rowblocks(exploratory),100/30strong. HighRVX0n22E/15L fails; no widening afterdiscovery. These screens not formalrawpointidentification.
- DROP_TOP1=2020-03-18; DROP_TOP5 priorOLS1ranking2020-03-18/03-13/02-28/03-27/03-24;EXCLUDE_2020all248eligible2020trainingdays;MATCHED_SOURCEonly2019-08-12/13. FULLn1495,drop1n1494,drop5n1490,no2020n1247,matched1493,Huber1495; same497validationallvariants. Huberpoint-only; no sensitivityreplacesFULLby p/sign/score.
- HAC5primary10/20sensitivity,Bartlett,n/(n−k),normal95%. Sixquestions C1Xstatejoint2df,C2XZ1df,S4combinedcurvature4df eachE/L,Holm6;S6curvature8df/overall/g/W/lag/stress/temporal/selectedvalidation extraexploratory.
- ACF1/5/10/20,LBresidual/squared5/10/20model_df0,ARCH5ddofOLSparameters,BPKoenkerrobustTrue,Whiteexpandedauxrank,RESETfittedsquarelinear/C1/C2only,10binsmin20,Cooktop5/internalstudentization,varianceRV correlations. Temporal2016–19/2020/2021,LOYO2016…2021C2/S4E/L, fixedparsimoniousC2intercept+X2020interactioncontrollingstate/W; no breakpointsearch.
- quarterlyJan/Apr/Jul/Oct2022/23,FULLexpandingonly; historytargetstrictlybeforeforecast. N1initialtrainmeanforday1validationthenprioronlyupdates; trainingfirst0thenprioronly. SamecausalN1 comparatorbothmodes.
- SelectionminimumquarterlyMSEsixprimaryFULLwithininfo; convincinggainneedspositivepairedHAC5CIvsstrongestnaive/OLS(notmet). SecondaryMAE/tail/complexity/sensitivitydisclosed; no p/sign-trimselection. ValidationreusedlaterEBMnotindependentconfirmation.
- random_seed=None,deterministic; no permutation/bootstrap/tradingcost/EBM declarations relevant. execution_data_budget_bytes100000000,finalregisteredproducts5247787. EBM_DATA_ROOT/--data-root,ROOTfrompackagepath; no machinepaths.

## 4. Ordered execution/reproducibility trail

Working directory repository root(.); authoring patch contents persistent inlistedsource andhashes.
1. cat attachedprompt; git status --short,git branch --show-current,git rev-parse HEAD; rg --files relevantconfig/src/tests/reports/registries. Readapplicableroot/Bspec/protocol/Stage1/1.5/source files withcat/sed/rg; combinedlongoutputs sometimestruncated,followedbytargetedreads. Preexistinguserdocnotadoptedasnewscientificauthority.
2. .venv/bin/python -B inline verify_files/sha, datecounts2680/2675/1495/497/683, sourceids anddisk63,488,000,000freebytes. Stage1sixexecutionmodulehashes,daily/manual/producthashes unchanged; metadataonlysealed. No newpackages(network0).
3. apply_patch authoring: two JavaScriptquotingSyntaxError attempts failedbeforefilesystemmutation; retriedsmallerrawstrings. InitialPythonimportfailed reserved break= keyword in stage2a.py129; renamedbreak_definition beforedata/scienceoutputs.
4. .venv/bin/python -B inline importedfreeze_protocol andcalled ondata/expectedconfigpath: preflightPASS,8rowdesignsmoke+fullpredictorrankPASS,March18anchors/RV/returnsPASS; initialv1SHAe3291500896bb16c90b53af0d2d0790321abd1c42f7a0173c5d567c31cea91c9. Before anycandidatefit/validationY, preservedv1_as_pre_fit andversionedwordingcorrectionv2 tofreezeoriginalcategoricalcuts(allquarterly). Finalv2SHA22b248cfc6f1ed9636b36e272effde0f7d30ff4474773bfab84c89291dd581d0; no outcome-drivenchange.
5. .venv/bin/python -B -m unittest discover -s tests -p 'test_b_stage2a.py' -v:4/4PASS,0.732s. No morethan4newtests.
6. .venv/bin/python -B -m ebm_research.experiment_b.stage2a firstintegration exit1: missingquantileskey in adaptercalltolegacylinear_diagnostics.py163. Addedexistingextremequantileconvention. ExpectedWhiteauxSingularMatrixWarning handled by explicitNOT_APPLICABLE/noinvalidp, forecastdesignrankstillfull. No scientificpublication orvalidationY beforefailure.
7. SameCLI secondintegration exit1: correlationmatrixfill_diagonal usespandas3readonlyto_numpy view(stage2a_diagnostics.py58). Fixedcopy=True. No publishedinference/validationY. Scientificmenu/definitions unchanged.
8. SameCLI initialsuccessfulpublication exit0,42.141381s wall/13.019892sCPU;38766predictions,8figures,allregistries. Reviewednumbers/plots,retainednegatives. Firstmatplotlibfontcachebuiltunderignoredlogs.
9. Completedrequiredper-rowmetadata,quarterpredictor/tailaudit,explicitwigglegeometrydiagnostics andreportinterpretation, withoutmodel/protocol changes. .venv/bin/python -B -m unittest discover -s tests -v:18/18PASS,3.301s. SameCLI successsecondpublication exit0,24.339207s wall/18.898220sCPU; sameallnumericmodel/validation findings.
10. Finalformulas/library/seed/validationavailabilitymetadataadded; sameCLI successfinalpublication exit0,86.405750s wall/40.550338sCPU (observedwallvariation, not claimedscaling). Allsamebenchmark/validationnumbers. Outputcompletenessrerun,notnewhypothesis. Eightfiguresvisuallyreviewed(view_image),axes/titles/units/masksreadable.
11. IndependentPythonQA: registereddata/figure/report/code/protocol/sourceprivateaudithashesPASS; Stage1/1.5helpers/files unchanged. Reconstructed36778nonnaivevalidationforecasts directlyfromsavedparameters/preprocessing/design, maxdifference0bp. All78series exactly497identicaldates; no duplicatekeys,actualYmatchescanonical2022–23,losserror². Everyhistorylastdate<forecast/cutoff; quarter n=1495+earliereligiblevalidationdates, originalcategoricalcutsunchangedall8histories. N1independentcumulativesumsPASS,N0zeros; fixedstressbasisidentitiesalloriginal.
12. Independent58pairedmeanlossestimates maxdifference1.78e−15; oneprimaryC1-EvsN0quarterHAC5SE independentlyfromscalarBartlettscoremeat/n(n−1)=4.794529352340683 matcheslibrary1e−12relative. Shape/status/byteaudit,userfilehashunchanged; git diff --check/status/stat. Initialsession-reportwriter failedIndexError onemptydocstringbeforecreatinganyfile; fixedsafeASTdocfallback inthiswriter. Wrotethisuniquereport; finalhash/link/new-filewhitespace/portability/Gitchecks. No stage/commit/push.

Python3.14.6; numpy=2.5.4, pandas=3.0.6, scipy=1.18.1, statsmodels=0.15.0, pyarrow=23.0.1, matplotlib=3.11.2. Existingrequirements-stage1_5.lock.txt26runtimepins; no InterpretML/newdependency. Freshclone:
~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-stage1_5.lock.txt
.venv/bin/python -m pip install -e .
# Restore matching authorized private sources/daily/registries.
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B -m ebm_research.experiment_b.stage2a --data-root PATH
~~~
Windows.venv/Scripts/python. PublicGit lackslicensedrows; matchingprivatebackupneeded. No providercredentials/networkafterrestore. Existingprotocol reused; --freeze-protocol firstcreationonlyrejectsexistingfile. Do notoverwritev2witholddefaultgenerator; documentedclarification retained. Changedprovideridentityrequiresseparateversionedacquisition,notfakehashes.

## 5. Actual tests, math/time/source checks and scientific integrity

18/18PASS,0failed;fournewcriticaltests:
- trainingguard/linear-tails: rejectsforbiddenhistorybeforepredictoraccess, transformingfuturepointsdoesnotalterknots, secondfinite-difference0outsidebothboundaries.
- categoricalformula/information: lowerbintie, knownformulaoutputs3/8/10,EwithoutW.
- literalC2/S1nesting/ranks8/12,vΣv′ andHACnormal t_testCIagree.
- chronologicalcutoff/datepairreorderingandmissing-keyrejection.
Existing14testscovertime/RV/DST/halfday/priorfullanchors/directHACmath/ParquetI/O/overlayduplicate/hashintegrity. No broadsimulator/seed/grid/nullframework. SourceMarch18sameoriginalSIPpricesverified; noncriticalmiddayabsencenotbad-priceclaim.

AllFULL/stress/quarterdesignsrank=parameters; maxcondition≈73530.47<1e12stop. Huberconverged(noMaxiterqualifications). NamedCIconditionalfixedbasis/state/weakdependence/finite-momentassumptions,notrawpointorcausalclaim. DiagnosticNOT_APPLICABLE16=10singularWhiteaux+4richS1RESET+2constantN0calibration/correlation;allreasonsmachine-readable. Coefficient/pairedp-valuesunadjustedexceptexplicit6Holmfamily; selectedvalidationintervalsnotindependentconfirmation. NormalitynotHACprerequisite; independence/exogeneitynotprovedbyresidualtests.

Source/protocoltarget/timebasis/A-Bseparationpreserved. Validationlabelsnowauthorizedforpredictions/metricsandchronologicalearlier-quarterrefits,neverknotsusingfuturelabels. Sealed2024–2026onlydate/eligibility/hashmetadatacount683; zero scientificrows/metrics/curves/selection. N1notanoraclemean. Fixeddeletionvariantsneverremovevalidationdates; identical497keysall78series. No P&L/executioncosts/technicalindicators/sourcefallback/datafill.

Numericaloutcomes: C1-E/L,C2-E/L moderationp≈.26/.98/.26/.95,S4curvaturep≈.138/.136,HOLM≥.817; nofamilyclaim. QuarterlyRMSE N030.3068,C1E30.3291,C1L30.3626,S4E31.4271,S4L31.4867. FixedC1EvsbestOLS1gain−.340CI[−4.567,3.888];fixedC1LvsN0−12.348CI[−23.579,−1.116],exploratoryafterselection. SomeHuber/deletionlatefixedfitsbetter(e.g.C2Ldrop5RMSE30.0623vsFULL30.6568),retainedassensitivitynotwinner. ResidualvarianceRV Spearman≈.369–.413persists. State-shapehighX0rawABSTAIN350rows; parameterprojectioncoefficients distinct.

Validationpredictorsstatecounts31/151/315;65datesoutsideinnerknots(lineartails),zeroZoutsideobservedtrainingrange,oneWbelowtrainmin. Quarter-specificpredictor/tailauditregistered. No targetmagnitudeclip/trim or modelselectionfromfavorabletrainingp. Scientificnegativescorrectlyqualified,notautomaticstagefailure.

## 6. Errors, decisions and recovery

Meaningfulexceptionsandfixes:
- ToolpatchJSquotingSyntaxError(2): nofilesystemmutation; splitpatches. PreflightreservedPythonbreakkeyword: correctedbreak_definition beforefreeze.
- Adaptermissingquantiles: firstintegrationstopbeforepublication/validation; suppliedpriorconvention. pandas3readonlycorrelationarray: secondstop; copy=True. Bothengineeringfixes,no scientificredesign; finalfullrun/18tests/independentreconstructionverify.
- Whiteauxrankdeficientwarning: algebraicexpandedproducts,notcandidateforecastmatrix; explicitlyNA/noinvalidp, mathematicalreasonlogged. RichS1RESETwithheldinpreferencetonestedcurvature. ConstantN0no meaningfuldecilecorrelationNA.
- Pre-fitprotocolwording: preservev1,clarifyfixedoriginalvalidationcategoriesinv2 beforefitting/labels; allowedimplementationcorrectiontofollowcurrentprompt,notpost-fitcoefficientrescue.
- Arrowcache/NEONsysctlOperationnotpermittedwarnings: nonfatal; actualParquet/hash/testchecksPASS. Noescalatedpermissionsneeded.
- InitialreportbuilderIndexError(emptyfunctiondocstring) beforeoutputfile: safeASTfallback, thissuccessfulreportwriter; no data/artifactchanged.
- HighRVX0supportlack andweakmean/predictionresults: preserveABSTAIN/FULL/negativeoutputs. No target/grid/source/horizonchange. No externalAPIerror/secret/subscription/data-integrityfailure/unresolvedscientific-definitionconflict.
No actualunit-testfailure. Pylance/Pyright/editorwarningstateunavailable/notclaimed; no needlesslint/packageoverhaul.

TrustcheckpointfinalB_stage2A_manifest.json andhashed8CSVs/onepredParquet/8PNGs/main+methoddocs. Initialincompletein-memorydiagnosticrunsnottrusted/published; finalregenerationchecksvalid. Noorphan.tmp/quarantine/workerleft. Onlaterinterruptioninspecthash/manifestcompletenessbeforeusingoutputs; sameCLIregeneratesstage-ownedoutputsfromsameprotocol/source. NevermutateStage1/D2data/manifests/unsealtesttofixformatting. Anynewscientificmenu/source/target/state/contrastrequiresversionedprotocol/approvalasapplicable. Keepuseruntrackedfilepreserved.

## 7. Resources, exact hashes, Git and handoff

Three successfulpublications total152.886338s wall/72.468450sCPU,excludingpreflight,shortfailedattempts,tests/independentQA/preparation. Individualfinal86.405750/40.550338; wallvariationreportednotexplained. n≤1992,parameters≤13,noheavyunattendedloop/largefuturework.

RegisteredCSV/data/figureproducts5247787bytes;8figures1108972bytes;predictionParquet2076703bytes. Newreviewablefilesbeforethisreport3398698bytes,plusignoredprediction/privateanchorJSON,fontcache289954. Totalnewretainedresearchmaterial~5.5MB,wellunder100MB;default2GBgateneverapproached. No dependencies/API/dataHTTP/acquisitionbytes added. Initial/latestfree63.488GBcoarseglobalobservation;directsizesauthoritative. No duplicatedcanonicaldaily/minute/year/model/seed/foldinputs.

Startingtrackedtreecleanwithonepreexistinguntrackeduserfile;endingexistingtrackeddiffempty. Beforethisreport26stage-createdreviewablefiles+theuserfile;reportaddsone. No Gitstaging/commit/push. git diff --checkPASS; customnew-filecheckscoveruntrackedcontent. Endingstatusbeforethisreport:
~~~text
?? artifacts/B/stage2A/
?? config/B_stage2A_linear_spline_protocol.json
?? config/B_stage2A_linear_spline_protocol_v1_pre_fit.json
?? data/registry/B_stage2A_coefficients.csv
?? data/registry/B_stage2A_inference.csv
?? data/registry/B_stage2A_manifest.json
?? data/registry/B_stage2A_model_diagnostics.csv
?? data/registry/B_stage2A_models.csv
?? data/registry/B_stage2A_paired_loss_tests.csv
?? data/registry/B_stage2A_sensitivity.csv
?? data/registry/B_stage2A_support.csv
?? data/registry/B_stage2A_validation_metrics.csv
?? docs/experiment_B_stage2A_methods_and_model_registry.md
?? docs/specs/experiment_B_stage1_5_detailed_diagnosis_exact.md
?? reports/B/stage2A_state_linear_and_spline_results.md
?? src/ebm_research/experiment_b/stage2a.py
?? src/ebm_research/experiment_b/stage2a_diagnostics.py
?? src/ebm_research/experiment_b/stage2a_report.py
?? src/ebm_research/experiment_b/state_models.py
?? tests/test_b_stage2a.py
?? reports/sessions/20261016_1802_B_stage2A_state_linear_spline_session.md
~~~

Exactcreatedreviewableidentities(sessionnotself-hashed):
| Path | Bytes | SHA256 |
| --- | --- | --- |
| artifacts/B/stage2A/01_joint_support.png | 68638 | 9397699c156efee0628a3822a8c1068cb37b234cf3895b518c9e52d8f70cb8ed |
| artifacts/B/stage2A/02_state_slopes.png | 42308 | 9f111acbfc4961059a6a985128b5dbe00cc12455c93787c567cf37fd6a18dde5 |
| artifacts/B/stage2A/03_varying_coefficients.png | 179506 | 04040f9eb7de6a30eea180f7646cdd2c99e1003a6544908eb7975652f5c465a3 |
| artifacts/B/stage2A/04_supported_anchored_contrasts.png | 118120 | 5f41345261b762482eebddb064450c05f7091b52b8fa847b02356a5a10068eca |
| artifacts/B/stage2A/05_residual_and_qq.png | 218159 | 0bad616fbe2fcbddb3a5b4d0e0de1db7f1b8fbd282766c73215a0713b691eef6 |
| artifacts/B/stage2A/06_variance_and_time.png | 215861 | 9116e360bbd1add9b738ec1ce44ab822b07cd3936eed4cf7af957923dce514e5 |
| artifacts/B/stage2A/07_validation_predictions_calibration.png | 161075 | 9494548cea3423909f7f1851a33b9a12969373feb2039a30b9bf18b7e6a3d161 |
| artifacts/B/stage2A/08_validation_error_by_state.png | 105305 | b92b79e1b6ac8f6a792a7d496a7ad03a1190c2406324d44353674f63171eda75 |
| config/B_stage2A_linear_spline_protocol.json | 13734 | 22b248cfc6f1ed9636b36e272effde0f7d30ff4474773bfab84c89291dd581d0 |
| config/B_stage2A_linear_spline_protocol_v1_pre_fit.json | 13186 | e3291500896bb16c90b53af0d2d0790321abd1c42f7a0173c5d567c31cea91c9 |
| data/registry/B_stage2A_coefficients.csv | 990190 | 21f64281efec613ad1c0e8bf60eafcd494c0184dda36f6e57485c4775bbfdce1 |
| data/registry/B_stage2A_inference.csv | 240758 | 0ab7296a558fcf5b4d5ca22dcdbbe5cefef278ffd902d57b28a07bff87fd147d |
| data/registry/B_stage2A_manifest.json | 44713 | 40ec79b8e2ae484464d7acd14b88e7679500c5a78e2abe570e5636bc823e6c65 |
| data/registry/B_stage2A_model_diagnostics.csv | 532797 | a56d4c8647128236f2c3995b59b86003bdffe83cc9a6683701c870969974f678 |
| data/registry/B_stage2A_models.csv | 206113 | 2e6ff4d234cd02d4280fc86ed2ed63dfe232685036c194971c1fb5fb47ce266f |
| data/registry/B_stage2A_paired_loss_tests.csv | 15149 | 44c7341cbcd057c4c2983f8e3e1bf596961ad6bd9c5740ea0f35f82e47e35394 |
| data/registry/B_stage2A_sensitivity.csv | 29374 | 3d63356727065423ba5a23e3baee705bfb52af26c59e8f899214ce898bdf51cf |
| data/registry/B_stage2A_support.csv | 7226 | 659bff205b963e0e190cbc76c3513b1a70fd613ff024a4ed858772d5f73a0fa5 |
| data/registry/B_stage2A_validation_metrics.csv | 40505 | 00ec5031a1006bf2499677f2893467ce16f0ada3d87c4d2efe79dd6784aed007 |
| docs/experiment_B_stage2A_methods_and_model_registry.md | 5917 | 697adc96bbe839d3a27b1b860d359d81881938c96e8c1dfc210a62dbede82cdc |
| reports/B/stage2A_state_linear_and_spline_results.md | 48166 | d2ba440e813803386f894b9a3b5f48530586a4e7dc3bfa8f1a08d64904e798c9 |
| src/ebm_research/experiment_b/stage2a.py | 49412 | 024b19786c68b00769e930545f922af21b656ebecd9e49a0e66a7c90f695ea1b |
| src/ebm_research/experiment_b/stage2a_diagnostics.py | 7747 | 09c6f856f70a6e92b9ba8aaed7f7b1a216c24dd6dbf2097ad8db14b247b3cd71 |
| src/ebm_research/experiment_b/stage2a_report.py | 31984 | 80e83835727ed3a7b114eb6e39f03270914d5b1fee0f37ee683cd0b848b338c6 |
| src/ebm_research/experiment_b/state_models.py | 8931 | 64a9f0a04622bee5f356aae026ae0e95fa4c222e90ff4186d54a7cac1222eb53 |
| tests/test_b_stage2a.py | 3824 | 8e0de6906db90e15645d9c4faa5c3cd6ccb0e10a68fc4b148842d22e0fa98c63 |

DailyinputSHA2aa3e2df1cab897abd679ed9cbeff8f6fcb004ecc01a7b32c5938aa6c23b5c2f. FinalprotocolSHA22b248cfc6f1ed9636b36e272effde0f7d30ff4474773bfab84c89291dd581d0. Entireinput/output/software/code/source/preprocessingSHAmapinmanifest/protocol;eachfitregistry includesparameters/formula/units/dates/library/seed/availability/time/memoryidentity. PrivateMarchanchorSHA0dbaf478c8e239c863d5832b0023ec4b27be5aff5f6a02d2a3ff42eb154a8707;actualpricesremainignored. Source/userfilesunchanged.

**Handoff:** Read [scientificreport](../B/stage2A_state_linear_and_spline_results.md), [exactmethods](../../docs/experiment_B_stage2A_methods_and_model_registry.md),protocol/manifestandvalidation/paired/sensitivityregistries. MatchedFULLC1/C2/S1E/L,naive/state-blindstrongreferences,predictivestatecuts,causalfixed/quarterlyschedules,allstress/source/influenceevidenceandcompactforecastsreadyforfutureseparatelyauthorizedadditive/discrete/continuousEBMs. No convincingstate/splinegain;zeroisstrong. RetainFULLprimary/supportmasks/validationselectioncaveats,sealed2024–2026. UnsupportedhighX0rawcontrastneedscontinuedABSTAINoraseparatelypredeclaredsupportedfuturedesign. NoEBMfitstarted;Aonhold.

Final completion checks: a short `.venv/bin/python -B` read-only verifier rechecked final protocol SHA256, preserved preexisting user-document SHA256, session existence/size, empty `git diff --name-only`, and `git diff --check`; exit 0 (0.136 s). A final `tail -n 42` read of the supplied Stage 2A prompt confirmed final-answer and EBM-handoff requirements; exit 0. This audit-trail append changes only this session report. No further model fitting or data access occurred.
