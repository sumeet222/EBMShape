# Experiment B Stage 2B coding-session report

## 1. Identification, authority, objective and verdict

Session ID: 20261016_1820_B_stage2B; began 2026-10-16 approximately18:20 America/New_York (EDT, UTC−04). Codex primary implementation/audit agent; no subagents. Current request: attachment `8d2df561-4981-490b-accc-ec14c424f810/Pasted text.txt`, task B_STAGE2B_EBM_LADDER_SHAPE_FIDELITY_AND_INFERENCE_V1. Scope B only; A remains on hold. Starting branch main, HEAD ebca8fe7c7b0b3ceea36f9fd71942693e42e3cf3, `git status --short` empty. Prior Stage2A work was committed before this session. No preexisting uncommitted work was reset, overwritten or removed. No staging, commit or push authorized/performed.

Objective: complete native InterpretML state-blind/additive/categorical-interaction/continuous-interaction/late-W-state ladder, bounded training-only complexity selection, seed/outlier/time-window diagnostics, matched fixed and quarterly development forecasts, cautious full-surface scientific contrasts and actual theory-assumption audit. No new source acquisition, A3–A6, new indicator/target, sealed statistics or trading.

Implementation verdict and exact resources are finalized in §8–10 below. Scientific raw E shape is INCONCLUSIVE, L ABSTAIN; an implementation pass never establishes financial benefit or theorem validity. Read the scientific report separately: [Stage2B scientific results](../B/stage2B_EBM_ladder_scientific_results.md) and [theory audit](../B/stage2B_theory_applicability_and_implementation.md).

## 2. Consequential inspected inputs and source boundaries

Read root AGENTS.md, README.md, .gitignore; approved Bspecv1 and companion under docs/specs; Stage1 report/selection/daily/QA/state/coefficient manifests; Stage1.5 report/settings/influence/diagnostics manifest; Stage2A scientific report/methods/protocol, all registry files (hash-verified) and forecasts; D2 and exactlyD2.1c source manifest/repair provenance. Targeted prior support figure04 was visually inspected. Stage2A's existing scientific conclusion/diagnostic restrictions were carried forward, not relabeled as evidence for EBMs. `rg --files` inventory included ResearchSpec and found no project-original theorem/consolidation/Task10B–25 reports. No other private project location/access was assumed. Needed exact missing theory files are listed in theory report. Only Bspec/companion/AGENTS/current prompt theory assumptions were applied; original theorem statements were not claimed read.

Dataset B_SPY_daily_split_source1_stage1_v1, daily SHA256 2aa3e2df1cab897abd679ed9cbeff8f6fcb004ecc01a7b32c5938aa6c23b5c2f. 2680 daily rows,2675eligible, train1495/validation497/sealed683. Initial verification used prior training_inputs/load_training and immutable Stage1 source hashes, date-only whole-table projection, then narrow eligible Arrow train or2022–23 predicates. No 2024–2026 scientific column was returned to research functions. Whole-file hash reads are byte integrity checks, not outcome analytics. Scientific source remains D2AlpacaSIPsplit plus exactly39D2.1c native missing-key repairs; no D2.1b overlap or new filling. Original March18 five-price validation is inherited from hash-verified Stage2A; no new minute-data scan or price correction. Source licensing/community adjustment limitations remain. No new credentials accessed or displayed, no market-data/API request.

## 3. Frozen operational/scientific design and critical variables

| exact key / variable | location | meaning, units, default and consumers |
| --- | --- | --- |
| `dataset_id`, `daily`, `counts` | config/B_stage2B_EBM_protocol_v1.json | One canonical daily ID/hash,2680/2675/1495/497/683; all runners/QA |
| `train`, `validation`, `sealed` | same | 2016-01-05..2021-12-31;2022..2023;2024..2026-09-30; guarded reads/refits |
| `X`, `W`, `Y`, `Z`, `symbol`, `timezone`, `adjustment` | same | SPY; ET; SIPsplit/nativepatch; priorclose→10 signedbp;15:00→15:30bp L-only;15:30→16 signedbp; log one-minuteRV+1e−8 |
| `cutoffs_raw` | same | [0.001558374721607106,0.0024281183976187152], equality lower; fixed2016–21 for every variant/refit |
| `z_representatives` | same | Original training within-tercile median logRV; fixed scientific display coordinates |
| `models` / `specifications()` | protocol / ebm_models.py | 11 fixed E/L families; SB/A0c/A0d no edges;A1d X×S;A1c X×Z;A2c_L X×Z+W×Z; nominal S |
| `settings`, `selection` | protocol | Two maxbins32/64, interactionbins8/16, leaf25/10,lr.025;fit2016–20,development2021minMSE,tie lower;seed42/fourbags;one setting/family |
| `effective_base`, `final_bags`, `seeds` | protocol | Native objective rmse;1000rounds,early50,tolerance1e−5;15% stochastic past-only internal holdout;cyclic greedy0,smoothing100/50;8finalbags;42/123/2025/7/314159;n_jobs1;all other effective params explicit |
| `quarterly_schedule`, `asof`, `history_last` | protocol / single prediction table | Jan/Apr/Jul/Oct2022–23, completed target date strictly before cutoff and prediction;initial Jan reuses fixed fit |
| `variants`, `learning_rate_sensitivity` | protocol | FixedMarch18/top5,EXCLUDE_2020,MATCHED_SOURCE Aug12/13;lr.05 single sensitivity;seed42;same497validationdays |
| `temporal_periods`, `leave_year_out` | protocol | All11families2016–19/2020/2021;A1cE/Lleave2016..2021;descriptive, no optimized break |
| `support`, `contrast_grid`, `sparse_plot` | protocol and contrast_grid.json | Ordered ±10/20/30/50,h5/10/15,h<a; W0 thentrainmedian,width5/10/20;50dates/20blocks minimum;100/30 strong;Echosen±20/h15 broadterciles,Lnone;local sparse plotting masks |
| `D_F`, `increment_low`, `increment_high` | shape_contrasts.csv | Four whole predictions, highXincrement minus low;not isolated software component;additivezero tolerance1e−9;no X0 anchor |
| `paired_inference`, `primary_comparisons` | protocol | Comparatorloss−candidateloss bp²;HAC5/10/20,n/(n−1),normal95%;Holm onlyquarterly42A1cvsA0cE/L;500fixed-lossbootstrap5/20 fourcomparisons |
| `materiality` | protocol | Shape±1bp needs justified interval inside tolerance;R²increment≥.0025 plus positiveCI vsstrongstateawaresimple andstrongnaive;not selectedRMSE alone |
| `resource` | protocol | ≤3600sfitloop,100MBnewretainedresearchproducts,60ssinglefit;componentplan562;v1total662mis-sum retained/disclosed |
| `PROTOCOL`, `ROOT`, `EBM_DATA_ROOT` | stage2b.py / existingpilot | Relative portable project root/default shareddata;optional externaldata envroot;no machine paths in new source/config |
| `state`, `identity`, `checkpoint`, `primary` | stage2b.py | Hash-bound successful-fit checkpoint;selected settings;11reusable seed42objects;no input replicas |

Protocol SHA256 eb0de45412b5952d0012dc44f74e7ca859b2bb4981df49d54377a6caa401169d froze before both pilot and full fitting. Training-only predictor support chosen before fitted shapes/validationY. V1 component total arithmetic typo662 versus actual22+55+385+44+33+12+11=562 did not change a scientific branch, grid, seed or sensitivity. No in-use scientific protocol overwritten or target-driven revision. Native training subset binning updates on perturbations; scientific categories/coordinates fixed. This is a learner perturbation, not Stage2A's fixed-basis deletion. Internal2021screen uses original full-training predictor-only category cuts and is developmental, not an honest live2021forecast. External validation never selects settings or future-quarter hyperparameters.

## 4. Function / class / script register

Inputs across new research modules: guarded eligible SPY DataFrames with session_et(date), x_open_bp/w_preclose_bp/y_last30_bp(float bp), rv_open_raw/log(float); protocol dict; explicit model spec; no sealed labels. Outputs: native estimators, float forecasts/losses, record lists, compact registries/figures/manifests. Runner and publication are thin composition around prior paths/hashes/metrics/guards and actual InterpretML. No custom substitute learner. Exceptions stop affected processing; successful checkpoint is retained. Function-specific contracts follow (signatures are exact source AST; purpose from actual docstrings):


### src/ebm_research/experiment_b/ebm_models.py

| function / signature | purpose / algorithm | inputs → outputs; callers and limits |
| --- | --- | --- |
| `specifications()` | Exactly eleven families; names and interaction edges are scientifically fixed. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `groups(frame, protocol)` | Original training terciles; equality belongs to lower category. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `features(frame, spec, protocol)` | Explicit E/L projection; E does not access W and S is nominal text. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `assert_graph(model, spec)` | Check actual native edges and feature types, including nominal S. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `fit_native(frame, spec, protocol, setting, seed, asof, bags=8)` | Past-only actual EBM, explicit parameters, warnings and algorithmic bag metadata. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `cell_mask(frame, protocol, candidate, state, endpoint)` | Local nonzero X window × RV tercile, additionally fixed W band for L. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `candidate_rows(frame, protocol, candidate, cohort)` | Four local cells with distinct fixed five-row blocks and predictor ranges. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `support_screen(train, protocol)` | Deterministic predictor-only ordered candidates; no fit or outcome input. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `query_frame(x, z, w)` | Full feature rows at training-defined coordinates, without outcomes. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `contrast(model, spec, protocol, grid)` | Four total predictions; not an isolated centered software interaction. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `metrics(frame, pred, n1, **keys)` | Reuse Stage2A matched metrics and add named nonlinear diagnostics. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `residual_diagnostics(frame, pred, protocol, **keys)` | Nonlinear residual battery; classical references disclosed, no OLS pseudo-inference. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `paired_hac(loss_gain, lag=5)` | Fixed paired daily losses, Bartlett HAC n/(n-1), normal asymptotic 95%. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `paired_losses(candidate, comparator)` | Match session keys and identical outcomes before constructing loss gains. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `block_interval(values, block=5, repetitions=500, seed=42)` | Circular moving-block percentile sensitivity, fixed forecasts, no learner refit. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |
| `add(name, value=None, p_value=None, status='DESCRIPTIVE', **extra)` | Internal small helper; see enclosing public contract. | Native/scientific helpers called by runner/results/tests; frame+spec+protocol → estimator/records/arrays; guards support and native type/edge mismatches; inferential caveats in each row. |

### src/ebm_research/experiment_b/stage2b.py

| function / signature | purpose / algorithm | inputs → outputs; callers and limits |
| --- | --- | --- |
| `data_root()` | Portable default shared store; external EBM_DATA_ROOT is optional. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `read_development(path, start, end, columns=None)` | Reject forbidden windows before Arrow scientific projection, including sealed dates. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `freeze(root)` | Write once before pilot/model fit; grids use only training predictors. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `verify(root, p)` | Verify immutable input identities before fitting/resuming. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `pilot(root, p)` | Small actual training fit with no external validation or sealed rows. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `run(root, p)` | Checkpoint the bounded fixed design; quarterly fits never select using future labels. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `main()` | Internal small helper; see enclosing public contract. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |
| `perform(frame, spec, setting_idx, seed, variant, mode, asof, evaluation, cohort='validation', bags=8, lr=None)` | Internal small helper; see enclosing public contract. | CLI freeze/pilot/run/publish and nested perform; protocol+shared data → checkpoint/native objects; strict date/hash/budget errors; no sealed access. |

### src/ebm_research/experiment_b/stage2b_results.py

| function / signature | purpose / algorithm | inputs → outputs; callers and limits |
| --- | --- | --- |
| `export_csv(root, name, rows)` | Small trackable numeric registry; nested native metadata encoded as JSON. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |
| `make_predictions(state, train, val)` | Exactly one long prediction table; quarter-one reuses the identical fixed fit. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |
| `paired_comparisons(root, p, pred, val)` | Matched E/L comparators by reference; developmental HAC and compact block sensitivity. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |
| `empirical_bands(train, val, p, pred)` | Predetermined broad-cell estimand, dependence-conscious diagnostic; never raw point inference. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |
| `theory_ledger()` | Explicitly audit source availability and assumptions, applying feasible diagnostics. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |
| `publish(root, p, state, primary, train, val, n1train, n1val)` | Publish complete fitting inventory and all matched comparisons without new EBM fits. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |
| `publish_cached(root, p)` | Resume publication from bounded private checkpoint; no additional EBM fitting. | Publication consumes completed hash-bound checkpoint/native primary models and permitted rows → one prediction file+CSV/JSON; fails on incomplete fits, dates, actualY mismatch, or cap; no new EBM fitting. |

### src/ebm_research/experiment_b/stage2b_report.py

| function / signature | purpose / algorithm | inputs → outputs; callers and limits |
| --- | --- | --- |
| `figures(root, p, train, val, pred, vm, shapes, surfaces, heat, stability, diag, composition, primary)` | Eleven reproducible figures; population shape claims always support masked. | Publication consumes compact outputs/canonical permitted rows/native11objects → readablePNG/Markdown; masks scientific support; no scientific tuning. |
| `markdown(frame, columns)` | Dependency-free short table of exact saved numeric results. | Publication consumes compact outputs/canonical permitted rows/native11objects → readablePNG/Markdown; masks scientific support; no scientific tuning. |
| `write_reports(root, p, m, vm, shapes, paired, multi, stability)` | Scientific verdict from the complete matched results; no winner-only filtering. | Publication consumes compact outputs/canonical permitted rows/native11objects → readablePNG/Markdown; masks scientific support; no scientific tuning. |
| `save(fig, name, title)` | Internal small helper; see enclosing public contract. | Publication consumes compact outputs/canonical permitted rows/native11objects → readablePNG/Markdown; masks scientific support; no scientific tuning. |
| `axes_grid()` | Internal small helper; see enclosing public contract. | Publication consumes compact outputs/canonical permitted rows/native11objects → readablePNG/Markdown; masks scientific support; no scientific tuning. |
| `selected(frame, info=None)` | Internal small helper; see enclosing public contract. | Publication consumes compact outputs/canonical permitted rows/native11objects → readablePNG/Markdown; masks scientific support; no scientific tuning. |

Critical math: whole D_F=[F(x+,w,zH)−F(x−,w,zH)]−[F(x+,w,zL)−F(x−,w,zL)]; standard additive terms cancel, checked in real/synthetic fits. Fixed paired d=(Y−Fcomp)²−(Y−Fcand)²; intercept-only OLS HAC uses n/(n−1), Bartlett lag; independent direct-meat fixture verifies its SE. Circular block intervals resample daily loss pairs only and do not refit/tune; raw band resampling resamples complete day indices for fixed cells. Neither is exact selection-adjusted pointwise population inference. Ordinary EBM OLS df/leverage/Cook/DFBETA/Wald/RESET are NOT_APPLICABLE. Diagnostic small1+standardizedX+Z variance regressions have explicit IID-reference limitations.

## 5. Execution and reproducibility trail (cwd repository root)

Commands in execution order, with bounded outputs retained where applicable:

1. `pwd`; `git status --short`; `git branch --show-current`; `git rev-parse HEAD`; read supplied prompt, `cat AGENTS.md`, `cat README.md`, `cat .gitignore`; exit0. Subsequent `rg --files`/`rg -n` and `sed -n` reads inspected Bspec/companion, Stage1/1.5/2A reports, configs, source modules and fixtures. Large text was read in targeted sections to avoid indiscriminate theory archive consumption. No files modified by inspections.
2. Python metadata preflight: Python3.14.6, interpret absent, diskfree63,488,000,000bytes coarse counter; existingenvironment detected. Official InterpretML regressor/custominteraction docs searched once via browser tool; local installed API signature is authoritative. Documentation link in methods registry. No market-data browsing/pulls.
3. `.venv/bin/python -m pip install 'interpret-core==0.7.3'` exit0. Actual native learner provided by interpret-core; no unnecessary dashboard/metapackage extras. Installed five distributions listed in resource/inventory appendix; no existing package upgraded. Wheel download interpret16.6MB; other wheels cached. No vendorcredentials or paidsubscription used.
4. `.venv/bin/python -B` metadata/API/schema inspection (`inspect.signature(ExplainableBoostingRegressor)` and `.fit`; protocol/manifest/registry columns). Exit0; exact parameter objects are in selected_parameters.json/models.csv.
5. `.venv/bin/python -B -m ebm_research.experiment_b.stage2b freeze` then `... pilot`; exit0. Freeze verified sources/counts and predictor-only support. Pilot100actual2016rows,4bags,A1c_L;0.307116s nativefit, conservative20× projection4066s exceededhour, triggering full-train timing rather than an unbounded launch.
6. Short `.venv/bin/python -B` full-training timing using `fit_native` on1495trainingrows/A2c_L/setting1/seed42/8bags;0.314718snative, projection208.343sfit or833.372swith4×I/O/diagnosticfactor, within3600s. Native timing fit discarded; full_timing.json records it. No externalvalidationYused for timing/choice.
7. `.venv/bin/python -B -m unittest discover -s tests -p test_b_stage2b.py -v` initially3PASS/1ERROR (nominal pandasStringDtype). Initial `... stage2b run > logs/stage2B_run.log 2>&1` had already launched numericSBfits; Ctrl-C through managed session stopped it (exit130), preserving35successful numericfits. No dependent categorical result trusted.
8. Engineering fix S.astype(object) for pandas3/InterpretML0.7.3; ARCHresult_object=False explicit. Focused test rerun4PASS0.499s. Checkpoint recovery script recorded old/new codehashes and reason, retained35numericruns and removed no successful outputs. Originalfeatures for preservednumericruns unchanged; model scientific questions/parameters/protocol unchanged. Incomplete interruptedfit retried deterministically. `.venv/bin/python -B -m ebm_research.experiment_b.stage2b run > logs/stage2B_run_resumed.log 2>&1` performs rest of complete ladder and publication; final status below.
9. `.venv/bin/python -B -m unittest discover -s tests -v > logs/stage2B_tests.log 2>&1` exit0;22tests3.391s. `git diff --check` exit0. Tests coverprior14+Stage2A4+Stage2B4, not genericproductionframework.
10. Added optionalpyproject stage2b pins; `.venv/bin/python -m pip freeze > requirements-stage2B.lock.txt`, exit0 with pipcache-permissionwarning. A shortPython replacement normalized editableprojectline to`-e .` (no self-recloningrepository). No other dependencysetting changed. Lock includes exact installedPythonlibrary versions; Pythonversion separatelyrecorded.
11. Bounded `tail`/PythonJSON status checks during job, registry/schema/sourcehash inspections, sourceAST inventory generation, and final results/QA/publication commands are listed in closing appendix. A `ps -axo ... | rg ...` diagnostic failed with sandbox`operation not permitted`; process control succeeded via existingmanagedsessionCtrl-C, so no escalation/unrestricted processinventory was needed or requested.

Fresh clone portability: Pythonmatching3.14.6 recommended for exact librarywheels; createvenv, `python -m pip install -r requirements-stage2B.lock.txt` (includes-e.); obtain authorized existing source/canonicaldaily and matchingStage1/2Aregistries/forecastfile via data/README.md/restoredmatchingdatasetID, optionallysetEBM_DATA_ROOT. No credentialsrequired for Stage2Boffline analytics. Verifyfilehashes. Frozenprotocolrecords originalsource/Stage2Ainputhashes,env andruntimeconfig; codehashes in manifest/runtimecheckpoint. Existingfrozenprotocol: run`python -B -m ebm_research.experiment_b.stage2b pilot`, then`... run`; no `freeze`overwrite. Cleanfreshstagewithoutprotocol: `freeze`, `pilot`, `run`. `publish`reusescompletedcheckpointand11nativeobjects withoutre-fitting; exactprivatecheckpointretention/recovery below. Nofullrawfiles suppliedinGit; do not promise dataredistribution.

## 6. Errors, anomalies, decisions and recovery

| when / command | symptom and cause | action, affected files, retest | unresolved / safe next step |
| --- | --- | --- | --- |
| focused nativegraph test | TypeError pandas.StringDtype not supported in InterpretML_clean_x.py1065; pandas3 inferred nominaltextdtype | explicit objectdtype in ebm_models.features; protocolcoding unchanged; all4newtests and22suitePASS | resolved; do not switch S to numericalordinal |
| initialrun aftertestfailure | Concurrent numericfits had started; KeyboardInterrupt in native.generate_seed when stopped | exit130;35successcheckpointentries preserved, pending fit rerun; no fittedresult falselyclaimed complete | allfinished successfulrun below |
| checkpointcodeidentity afterdtypefix | expected protectivehashmismatch because helperchanged | explicit engineering_recovery old/newSHA recorded; savednumericfeatures/forecasts unaffected; no silentinvalidation bypass | futureunexplainedidentitymismatch muststopandinspect |
| fullprotocolplanning | total_planned662versuscomponentactual562, arithmeticbug | V1unchanged; independentlysum frozencomponentcounts, executeallsevenbranches; discloseinmanifest/methods/report | no100fitsmissing, samegrid/seed/sensitivities |
| pilotprojection | conservative100row20×estimated4066s abovehour | fulltrain8bagtimingmeasured0.315s;833soverheadprojection justifiedlaunch | actualjobbounded/countersbelow |
| initialnumericdiagnostics | statsmodelsARCH futuretupleAPIwarning | explicitresult_object=False, sameactualtuple/null, nochangeintestmath | resolved; oldinitiallogpreserved |
| Arrow import/read | sysctlcache/NEONmetadata PermissionDeniedwarnings under sandbox | columnarreads/calculationssucceed; nosecret/sourceerror; noescalation | benigncapabilitywarning, notdatafailure |
| pipfreeze | userpipcachedirnotwritable warning | cacheunneededforfreeze; exit0, portableeditableline | noactionneeded |
| processinventoryattempt | ps sandbox operationnotpermitted | managedsessionCtrl-C stoppedownjob safely | noorphanworker; noexternalprocessclaim |
| originaltheoryfilesmissing | repository/ResearchSpecinventorylacksfullstatements | implementfeasiblespecdiagnostics and explicitassumptionledger, listneededmaterials | exacttheory-specificcertificationBLOCKED, modelstagecontinues |

Publication-preflight fixes made before affected code execution: pandasDataFrame.info/asof method-name collisions changed to bracketcolumn access; tableformatter JSON-encodeslistcells beforepd.isna; resourceimport optional onWindows. These are engineering-only outputcompatibility improvements, not changes to fits, nulls, features or decisions. No Pylance/editor/Pyrightstate is claimed inspected; actualimport/unittestcommands are evidence. Unsupportedrawshapes/negativeforecastperformance are scientific limitations, not bugs to fix.

## 7. Tests, QA and scientific integrity

Newtests exactlyfour: information-time/read/historyguards with forbiddenwindow failingbeforeI/O andEprojectionwithoutW; actualnative11graphs andnominalS withfour-wholeprediction/additivezero checks; exactlocalnonzerosupport andfive-rowblock/nearzeroabstentionfixture; paireddate/Ymatching and independentlyhand-computedHACmeat variance plusdeterministicblockinterval. No syntheticmarketecosystem or genericpipelineframework. Fullsuite22PASS. Syntheticpasses do not certifywholeactualdataset; actualaudits belowprovide narrowerreal-dataevidence.

Important preservedboundaries: A/Bseparate; sameSPYrows/target/state/source/times; nofuturequartertargetentershistory; source/dayhashesremainfixed; categoricalcutoffsconstant; no2024–2026label/predictionstatistics; noX0scientificanchor; fullsurfaceDnotrawsoftwareterm; noselectedfavorableoutlierbranchreplacesFULL; noOLS-onlyinferenceforEBMs; noseedSD/bagSDaspopulationCI; noexactnoveltheoremclaim. Eacceptedbroadbandsarenotcontinuity/pointwisebiascoverageproof;LfailsandABSTAINS. ValidationbandrawfidelitymayABSTAINwith31lowstatedates; noforcedcellmeanCI.


## 8. Final results and independent QA

**PASS WITH QUALIFICATIONS — STAGE2B_MODEL_LADDER_COMPLETE; SEAL_INTACT.** All 11 families and 55 selected FULL family/seed fits succeeded. The seven frozen branches contain 22 screen, 55 FULL, 385 additional quarterly, 44 fixed-exclusion, 33 subperiod, 12 leave-year-out and 11 learning-rate fits: **562 successful fits**. The protocol's total662 field was an arithmetic error, not an omitted branch. One incomplete native attempt was interrupted and rerun; no unresolved fit failure remains. All 210 complete validation forecast series contain identical 497 dates. One shared prediction Parquet contains 192,117 rows. E raw scientific shape is INCONCLUSIVE; L scientific shape ABSTAIN; both primary A1c prediction decisions are NO_CREDIBLE_INCREMENT.

Final real audit command: `.venv/bin/python -B logs/stage2B_real_audit.py > logs/stage2B_real_audit_final.log 2>&1`, exit0. This retained audit script is a bounded actual-output verification, not a new test framework. Evidence:

```json
{
  "status": "PASS",
  "prediction_rows": 192117,
  "matched497_series": 210,
  "model_fits": 562,
  "model_artifacts_reloaded": 11,
  "reconstructed_primary_train_validation_rows": 21912,
  "max_primary_prediction_error_bp": 0.0,
  "independently_recomputed_HAC_rows": 618,
  "max_paired_mean_error": 9.947598300641403e-14,
  "max_paired_se_error": 2.842170943040401e-14,
  "E_support_cells": [
    {
      "state": 0,
      "x": -20.0,
      "n": 116,
      "blocks": 90
    },
    {
      "state": 0,
      "x": 20.0,
      "n": 189,
      "blocks": 122
    },
    {
      "state": 2,
      "x": -20.0,
      "n": 72,
      "blocks": 60
    },
    {
      "state": 2,
      "x": 20.0,
      "n": 67,
      "blocks": 52
    }
  ],
  "all_registered_hashes_verified": true,
  "source_hash_unchanged": true,
  "seal_intact": true,
  "scientific_rows_exposed_after_2023": 0,
  "wall_seconds": 4.948050166014582
}
```

The four accepted E cells contain n/block pairs116/90,189/122,72/60,67/52. They satisfy exploratory50/20, but not all satisfy strong100/30. Broad-cell support does not certify continuous-point identification or bias/dependence coverage. Late candidates all failed. All 618 HAC rows match independent centered-meat calculations; all 11 actual saved models exactly reconstruct 21,912 primary train/validation predictions (max0bp). Runtime metadata graphs/types match all562fits and actual reloaded objects. All input/output hashes, dates, actualY, losses and additive-zero contrasts passed. All source/canonical and prior Stage2A files remain unchanged.

Primary quarterly A1c_E RMSE30.600168bp versus N030.306832; A1c_L30.278808. Continuous interaction versus additive mean squared-loss gains: E−12.323251bp², HAC5CI[−27.147548,2.501046], Holm.206502; L−.946834, CI[−11.394802,9.501133], Holm.859022. Versus C1: E−16.518340([−49.580188,16.543508]); L+5.081365([−34.303635,44.466365]). No convincing beneficial increment. Fitted E D_F=.526240bp remains a model-output contrast without certified population CI or ±1bp equivalence.

All12PNG figures were inspected as a contact sheet. Final full-resolution figure02 shows low/middle/high E/L total slices, simple comparators and explicit late-high ABSTAIN; figure10 shows all seeds and perturbations as points with a FULL42 reference, so small differences remain visible. Full tail/crisis residual ranges are retained. No population shape bands are drawn.

Publication/recovery commands and resolved issues:

- Resumed `stage2b run` completed all562fits, then exited1 at publication because forecast uniqueness omitted screening setting. Both settings legitimately share dates; no forecast or fit was invalid. Added setting to key, plus smallest regression assertion inside existing fourth new test.
- `stage2b publish > logs/stage2B_publish.log 2>&1`: exit0, no EBM fitting. Independent review found individual-quarter metrics mixed with full497date summaries; fixed labels to validation_quarter and filtered human summary to497dates.
- `stage2b publish > logs/stage2B_publish_final.log 2>&1`: exit0, no EBM fitting. Final labels separate385partial-fit rows; full validation rows alln497. Output forecasts/loss comparisons unchanged.
- `.venv/bin/python -B -m unittest discover -s tests -v > logs/stage2B_tests_final.log 2>&1`: **22PASS,3.017s**, including the screening-key regression. Still only four new test methods.
- Added compressed-checkpoint fallback to publish_cached after publication; round-trip SHA and562receipts verified before deleting plaintext. Source hash entry refreshed and real audit rerun. No fit formula, threshold, target, setting, seed, date or decision changed.
- Clarified optional null cost in theory report: retaining the actual two-family, five-seed discovery path requires(2screen+5seeds×8fits)×2families×100=8400fits, conservative projection~10,575s above3600cap. A cheaper primary-seed conditional shortcut needs a separately frozen scope/interpretation. No counterfeit nullp-value.
- Initial final-report generator failed with `SyntaxError: unterminated string literal` at inline line49, before any statements/file changes. This smaller retained generator replaces it. No successful scientific artifact affected.

## 9. Exact file inventory, resources and Git

The table lists every reviewable created/modified path; ignored data/models/logs follow separately. No preexisting user artifact was deleted or moved. All report/registry creation is from the frozen run; schemas and hashes are in the manifest.

| Action | repository-relative path | why / what changed | dependencies / consumers | recovery |
| --- | --- | --- | --- | --- |
| MODIFIED | `pyproject.toml` | 576bytes; optional stage2b pins only, existing options preserved | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/01_ebm_input_support.png` | 127779bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/02_ebm_model_ladder_shapes.png` | 273219bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/03_ebm_continuous_heatmap.png` | 90413bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/04_supported_nonzero_contrasts.png` | 57222bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/05_ebm_discrete_continuous_comparison.png` | 157768bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/06_ebm_residual_qq.png` | 97054bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/07_ebm_variance_time.png` | 266992bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/08_ebm_validation_calibration.png` | 166072bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/09_ebm_validation_error_by_state.png` | 84763bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/10_ebm_seed_outlier_stability.png` | 114612bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/11_ebm_state_composition_fidelity.png` | 69310bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `artifacts/B/stage2B/12_ebm_native_components.png` | 134333bytes; labeled scientific/support/diagnostic figure | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `config/B_stage2B_EBM_protocol_v1.json` | 28100bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_continuous_grid.csv` | 5928bytes;90rows×9columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_contrast_grid.json` | 15684bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_decisions.csv` | 869bytes;2rows×15columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_diagnostics.csv` | 32793499bytes;121479rows×29columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_discretization.csv` | 3028bytes;12rows×11columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_empirical_bands.csv` | 5280bytes;28rows×13columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_empirical_cells.csv` | 5699bytes;16rows×25columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_final_qa.json` | 913bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_finite_differences.csv` | 3025834bytes;13488rows×11columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_full_timing.json` | 315bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_interaction_and_multiplicity.csv` | 73263bytes;206rows×21columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_manifest.json` | 16642bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_models.csv` | 2083783bytes;562rows×31columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_paired_loss_tests.csv` | 212710bytes;626rows×20columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_pilot.json` | 5337bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_selected_parameters.json` | 48681bytes; protocol, provenance, QA, selected configuration or output manifest | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_shape_contrasts.csv` | 132599bytes;570rows×20columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_software_components.csv` | 71705bytes;544rows×6columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_stability.csv` | 38649bytes;155rows×16columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_state_composition.csv` | 1700bytes;8rows×12columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_support.csv` | 62165bytes;280rows×18columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_surfaces.csv` | 2154538bytes;15174rows×16columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_term_importance.csv` | 233710bytes;1642rows×14columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_theory_method_ledger.csv` | 5174bytes;11rows×9columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_training_metrics.csv` | 328085bytes;562rows×33columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `data/registry/B_stage2B_ebm_validation_metrics.csv` | 2312634bytes;4187rows×35columns; numeric registry | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `docs/experiment_B_stage2B_methods_and_model_registry.md` | 6482bytes; methods/scientific/theory/session Markdown audit | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `reports/B/stage2B_EBM_ladder_scientific_results.md` | 23683bytes; methods/scientific/theory/session Markdown audit | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `reports/B/stage2B_theory_applicability_and_implementation.md` | 7191bytes; methods/scientific/theory/session Markdown audit | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `reports/sessions/20261016_1820_B_stage2B_ebm_models.md` | 29408bytes; methods/scientific/theory/session Markdown audit | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `requirements-stage2B.lock.txt` | 561bytes; exact portable dependency snapshot, editable project-e. | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `src/ebm_research/experiment_b/ebm_models.py` | 15256bytes; research implementation or four focused test methods; function register§4 | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `src/ebm_research/experiment_b/stage2b.py` | 19744bytes; research implementation or four focused test methods; function register§4 | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `src/ebm_research/experiment_b/stage2b_report.py` | 36684bytes; research implementation or four focused test methods; function register§4 | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `src/ebm_research/experiment_b/stage2b_results.py` | 34726bytes; research implementation or four focused test methods; function register§4 | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED | `tests/test_b_stage2b.py` | 4707bytes; research implementation or four focused test methods; function register§4 | Stage2B offline fit/publication/review | Reproduce from frozen inputs; preserve original files |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/SB_E.joblib` | 5392bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A0c_E.joblib` | 10000bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A0d_E.joblib` | 5330bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A1d_E.joblib` | 7285bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A1c_E.joblib` | 21638bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/SB_L.joblib` | 8049bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A0c_L.joblib` | 7871bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A0d_L.joblib` | 8143bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A1d_L.joblib` | 10233bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A1c_L.joblib` | 10233bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `artifacts/B/checkpoints/stage2B/A2c_L.joblib` | 11518bytes; selected FULL seed42 native estimator, terms/bins/bags/scores | Exact surface/forecast reconstruction | Refit frozen selected setting with exact inputs/InterpretML |
| CREATED (ignored) | `data/derived/B/B_stage2B_ebm_predictions_v1.parquet` | 192117rows×16columns;3458354bytes;forecast,actual,loss,dates,model,setting,seed,variant,mode,cohort,state,asof/history | Shared forecasts; no sealed rows or cloned predictor histories | Reproduce stage or publication cache |
| CREATED (ignored) | `logs/stage2B_checkpoint.json.gz` | 16956015bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_checkpoint_archive.json` | 609bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_figures_contact.png` | 663964bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_finish_report.py` | 15632bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_matplotlib/fontlist-v3.11.0.json` | 289954bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_publish.log` | 853bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_publish_final.log` | 790bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_real_audit.log` | 1430bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_real_audit.py` | 6775bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_real_audit_final.log` | 1430bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_run.log` | 38026bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_run_resumed.log` | 3101bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_tests.log` | 3739bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED (ignored) | `logs/stage2B_tests_final.log` | 3739bytes; bounded execution/test/audit log or source, QA contact sheet, archive/cache metadata | Session diagnosis/recovery | Recompute with recorded commands; gzip holds publication receipts |
| CREATED then DELETED (ignored) | `logs/stage2B_checkpoint.json` | Agent-generated130,385,592byteplaintext metadata/forecast cache, replaced by verified16,956,015bytegzip | Publication resume | Decompress logs/stage2B_checkpoint.json.gz; SHA50d88c62f79d0d32ebe3fd16788aa8ac5e9dc4f6e56724a2eed88014100e837c |
| CREATED then MOVED (transient) | `config/B_stage2B_EBM_protocol_v1.json.tmp`; `data/registry/B_stage2B_ebm_*.json.tmp`; `logs/stage2B_checkpoint.json.tmp`; `logs/stage2B_checkpoint_archive.json.tmp` | Existingwrite_json atomic staging names, renamed to same destination without.tmp; checkpoint staging reused after each fit; no residual temporary file | Atomic publication/checkpoint | Noncanonical intermediates, regenerate from destination or run; never original user files |
| INSPECTED | Root AGENTS.md,README.md,.gitignore; docs/specs/experiment_B_*v1.md; Stage1/1.5/2A reports/configs/methods and machine registries; D2/D2.1c source/repair manifests | Binding source/protocol/result evidence, preserved | Scientific definitions and baselines | Verify frozen input hashes |
| INSPECTED | `data/derived/B/B_SPY_daily_split_source1_stage1_v1.parquet`; `data/derived/B/B_stage2A_validation_predictions.parquet`; Stage2A support figure04; existing daily/benchmark/linear/state-model utilities | Canonical daily data with guarded projection and prior forecasts by reference | No source/history copies or baseline re-fitting | Authorized source restore per data/README.md |

The virtual environment is ignored. Newly installed packages are grouped by their exact distribution RECORD manifests, which enumerate every mechanically installed path (rather than listing thousands of library files):

| distribution | version | files present from RECORD | installed bytes | path / recovery |
| --- | --- | --- | --- | --- |
| interpret-core | 0.7.3 | 182 | 75446527 | `.venv/lib/python3.14/site-packages/` package and matching `.dist-info/RECORD`; reinstall lock |
| scikit-learn | 1.9.1 | 1679 | 46287823 | `.venv/lib/python3.14/site-packages/` package and matching `.dist-info/RECORD`; reinstall lock |
| joblib | 1.6.0 | 213 | 1973472 | `.venv/lib/python3.14/site-packages/` package and matching `.dist-info/RECORD`; reinstall lock |
| cloudpickle | 3.1.2 | 11 | 126759 | `.venv/lib/python3.14/site-packages/` package and matching `.dist-info/RECORD`; reinstall lock |
| threadpoolctl | 3.7.0 | 7 | 167912 | `.venv/lib/python3.14/site-packages/` package and matching `.dist-info/RECORD`; reinstall lock |

Resources: registered scientific products/figures/native models/reports 48,778,307bytes (~48.8MB). Private compressed recovery cache16,956,015bytes, fontcache289,954bytes, plus bounded logs/code/session; approximately67,034,606new retained research bytes before this final report append (~67MB). New package files separately124,002,493bytes (~124MB). Both research outputs and environment together remain under1GB; research outputs remain under frozen100MB. No input dataset/history/seed/fold replicas, no downloads of financial data. One published Stage2B long predictionParquet; private compressed forecast/metadata receipts are an explicit recovery cache, not another canonical input or Parquet.

Resumed loop wall600.869992s / CPU544.215382s includes527remaining fits and checkpoint/diagnostic work. The35preserved initial successes have native timings in models.csv, but full interrupted-process CPU/wall was not captured. Actual native fit_seconds sum across562successes 122.161154s. Final publication wall35.622315s; earlier successful publication also ran, neither required new EBM fitting. Final publication process high-water RSS 637,321,216bytes; this does not measure earlier fit-process peak. Per-fit score_bytes measures native arrays only, not total memory. Compression11.700s verified round-trip SHA before deleting only the generated plaintext.

Initial coarse free-space counter63,488,000,000bytes; resumed fitting63078400000→61849600000; current61849600000. These coarse counters include unrelated system/APFS/cache/swap activity and cannot be attributed exactly to retained research material. Direct file sizes above are the storage evidence. No unrequested worker, schedule or process remains; no GPU or vendor/API work.

Final Git snapshot (before this final append; branchmain and HEADebca8fe7c7b0b3ceea36f9fd71942693e42e3cf3 unchanged):

```text
 M pyproject.toml
?? artifacts/B/stage2B/
?? config/B_stage2B_EBM_protocol_v1.json
?? data/registry/B_stage2B_ebm_continuous_grid.csv
?? data/registry/B_stage2B_ebm_contrast_grid.json
?? data/registry/B_stage2B_ebm_decisions.csv
?? data/registry/B_stage2B_ebm_diagnostics.csv
?? data/registry/B_stage2B_ebm_discretization.csv
?? data/registry/B_stage2B_ebm_empirical_bands.csv
?? data/registry/B_stage2B_ebm_empirical_cells.csv
?? data/registry/B_stage2B_ebm_final_qa.json
?? data/registry/B_stage2B_ebm_finite_differences.csv
?? data/registry/B_stage2B_ebm_full_timing.json
?? data/registry/B_stage2B_ebm_interaction_and_multiplicity.csv
?? data/registry/B_stage2B_ebm_manifest.json
?? data/registry/B_stage2B_ebm_models.csv
?? data/registry/B_stage2B_ebm_paired_loss_tests.csv
?? data/registry/B_stage2B_ebm_pilot.json
?? data/registry/B_stage2B_ebm_selected_parameters.json
?? data/registry/B_stage2B_ebm_shape_contrasts.csv
?? data/registry/B_stage2B_ebm_software_components.csv
?? data/registry/B_stage2B_ebm_stability.csv
?? data/registry/B_stage2B_ebm_state_composition.csv
?? data/registry/B_stage2B_ebm_support.csv
?? data/registry/B_stage2B_ebm_surfaces.csv
?? data/registry/B_stage2B_ebm_term_importance.csv
?? data/registry/B_stage2B_ebm_theory_method_ledger.csv
?? data/registry/B_stage2B_ebm_training_metrics.csv
?? data/registry/B_stage2B_ebm_validation_metrics.csv
?? docs/experiment_B_stage2B_methods_and_model_registry.md
?? reports/B/stage2B_EBM_ladder_scientific_results.md
?? reports/B/stage2B_theory_applicability_and_implementation.md
?? reports/sessions/20261016_1820_B_stage2B_ebm_models.md
?? requirements-stage2B.lock.txt
?? src/ebm_research/experiment_b/ebm_models.py
?? src/ebm_research/experiment_b/stage2b.py
?? src/ebm_research/experiment_b/stage2b_report.py
?? src/ebm_research/experiment_b/stage2b_results.py
?? tests/test_b_stage2b.py
```

Tracked diff summary:

```text
 pyproject.toml | 1 +
 1 file changed, 1 insertion(+)
```

Only tracked change is optionalstage2b line in pyproject. New source/config/docs/reports/registries/figures await user review. All preexisting work preserved. No staging, commit or push. No deleted preexisting user files.

## 10. Resume/recovery and next handoff

Trusted checkpoint: all562 successful receipts in `logs/stage2B_checkpoint.json.gz`; decompressed SHA above. Published science/tables/predictions/11native objects/finalQA are complete subject to scientific limitations. Initial interrupted fit and publication-only errors were recovered; no invalid partial scientific result is presented as confirmed.

To regenerate publication without fitting, run `python -B -m ebm_research.experiment_b.stage2b publish` with pinned environment and authorized matching inputs; publisher reads gzip when plaintext is absent. It replaces this stage's generated products. Afterwards rerun real audit and refresh QA/session/manifest references. A later `run` without plaintext checkpoint starts a fresh fit execution (~10minutes), so do not use it merely to view figures. If resuming fit processing from an archive, decompress to a separate working copy and inspect recorded code identity; never bypass an unexplained hash mismatch. Manifest previous_code_identity preserves actual fitting hashes; publisher/test source was completed separately without changing fitted mathematical operations. A clean authorized checkout can rerun the frozen protocol instead of adapting a checkpoint.

Read scientific report, theory audit, methods registry, protocol, manifest, decisions and finalQA first. The complete11family additive/discrete/continuous ladder and matched development comparisons are ready for review. Both primary continuous interactions lack credible incremental predictive gain; E continuous-point shape is uncertified and L joint support fails. Exact project theorem materials are still missing; ledger distinguishes adapted diagnostics and blocked theorem claims. No strong source-era replication, novel inferential validity, positive alpha or trading benefit follows from implementation QA.

Proposed next separately reviewed stage: freeze a shortlisted full-pipeline null/permutation scope and dependence assumptions, then separately freeze the sealed walk-forward protocol. Keep2024–September2026sealed until that review/authorization. Execution/cost economics remains later work. No scientific redesign was silently made. Stage2B itself is complete with qualifications; no additional EBM family fitting is pending.

Final audit-trail assembly time: 2026-10-16T18:42:44.909822-04:00.

Final maintenance commands: `.venv/bin/python -B logs/stage2B_finish_report.py` created the closing inventory/resource/recovery sections (exit0,2.331s); this retained ignored generator is listed in the inventory. Atomic staging destination counts: config protocol1, data/registry Stage2B JSON6, logs checkpoint/archive2 unique paths, each renamed to its matching final path; no residual .tmp. No preexisting file was deleted. Final short verifier below parsed all new Python/JSON, checked whitespace and relative Markdown links, verified all registered content hashes including QA/archive, and ran git diff --check; no model/data calculations were repeated.
