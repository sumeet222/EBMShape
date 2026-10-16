# Experiment B — initial visual audit of nine remaining directions: coding session

## 1. Identification, authorization and verdict

Session ID: **20261016_1938_B_initial_audit_nine_experiments**. Date: 16 October 2026, America/New_York (EDT, UTC−04:00). Persistent clock anchor: **19:24:42 EDT / 23:24:42 UTC**, the preservation snapshot after initial orientation; report finalization 19:41:51 EDT. The earliest orientation tool call was not separately clock-logged. Agent: Codex, GPT-6 family; exact serving revision not exposed.

Task: `B_INITIAL_AUDIT_NINE_REMAINING_EXPERIMENTS_V1`, supplied in the attachment ending `2de7c8a5-449c-4a4e-9ca0-bb5d4232e5e7/Pasted text.txt`. Its instructions authorize this training-only extension after the completed A1/A2 closeout. Earlier data-acquisition requests are historical context, not authorization to fetch data in this session.

**Implementation / QA: PASS_WITH_QUALIFICATIONS.** Nine sections, 36 mandatory and eight additional robustness figures, a standalone gallery, one feature-only table, support/contrast registries and technical report are complete. Eight focused tests pass. All 44 image links resolve. **265 preexisting files, including prior results and canonical sources, verify unchanged.** There were no network requests, predictive fits, permutations, subscriptions, credential reads, commits or pushes.

**Scientific conclusion: NO_CLEAR_WINNER.** A2/A3/A4/A5/A6/B1/B2 are INCONCLUSIVE; B3 is LOW_PRIORITY under the frozen first-panel rubric; C1 is MODEL_DEPENDENT / DEFER and TRADING_NOT_ESTABLISHED. These are descriptive research triage decisions, not hypothesis tests or predictive findings. Five of 72 FULL band contrasts abstain; 241 of 576 contrasts abstain across all eight masks. There are no input-blocked directions. Supported wide intervals remain inconclusive rather than evidence of invariance.

Starting and ending branch: `main`; commit: `6e6ed1150a0fd7fa38afe5c044712600eabbfdbc`. **Initial Git status was clean.** The prior conversational summary referred to an older dirty state; actual fresh Git inspection superseded it. No existing user changes were overwritten. The snapshot's status includes this session's newly created module/script/artifact directory because it was taken after writing the initial implementation, before reading any response for exploration.

Principal deliverables:

- [Image-rich visual review](../../artifacts/B/initial_audit/NINE_EXPERIMENTS_VISUAL_REVIEW.md)
- [Technical scientific report](../B/initial_audit_nine_experiments_feasibility.md)
- [Checked manifest](../../artifacts/B/initial_audit/registries/initial_audit_manifest.json)
- [Final integrity checks](../../artifacts/B/initial_audit/registries/final_integrity.json)

## 2. Exact file inventory and recovery

Every path below is repository-relative unless explicitly described as an OS temporary path. CREATED means new in this session, even when its generated contents were subsequently republished. There were **no modifications, deletions, renames or moves of preexisting repository/user artifacts**. No new raw dataset was retained.

| Action | Path | Why / contents changed | Dependencies / consumers | Recovery |
| --- | --- | --- | --- | --- |
| CREATED | `src/ebm_research/experiment_b/initial_audit.py` | One reusable offline module: protocol freeze, training projection, features, raw bins/bootstrap/support, 44 figures, publication and QA | Existing pilot/daily/repair/acquisition helpers; script below | Source control/review this new file; no other research modules were edited |
| CREATED | `scripts/b_initial_audit.py` | Thin `freeze / run / publish / qa` CLI | Imports the module | Restore this small file; no scientific logic duplicated |
| CREATED | `tests/test_b_initial_audit.py` | Eight deterministic math/time/lag/bootstrap/smoke checks | Existing environment, protocol, tiny temporary fixtures | Run unittest command below |
| CREATED | `artifacts/B/initial_audit/.gitignore` | Ignore local matplotlib font cache only | Root `.gitignore` already excludes Parquet/logs | No root ignore rules changed |
| CREATED | `artifacts/B/initial_audit/README.md` | Index, scope, lineage and reproduction | Gallery / registries | `run` or `publish` |
| CREATED | `artifacts/B/initial_audit/NINE_EXPERIMENTS_VISUAL_REVIEW.md` | Main nine-section gallery, all 44 actual embedded PNGs, all variants, common-date contrasts, limitations/rankings | Fixed numerical CSVs and figures | `publish`; prose-only final edit reused numerical products |
| CREATED | `artifacts/B/initial_audit/config/initial_audit_protocol_v1.json` | Frozen nine definitions, bins, masks, seeds, costs, candidate/rating rules and input hashes | All audit computation | Preserve; `freeze` refuses overwrite. Fresh checkout already containing it should use `run`, not refreeze |
| CREATED | `artifacts/B/initial_audit/config/matplotlib_cache/fontlist-v3.11.0.json` | Local generated font inventory, 289,954 bytes; ignored / machine-specific cache | Matplotlib only | Regenerated by plotting; not a portable protocol/input |
| CREATED | `artifacts/B/initial_audit/derived/initial_audit_new_features.parquet` | Single ignored feature-only table, **1,495 × 19**, **246,685 bytes**, Zstandard compressed | All nine views join by session key | `run`; requires matching authorized canonical sources, no new API calls |
| CREATED | `artifacts/B/initial_audit/registries/start_snapshot.json` | 265 preexisting path/byte/hash references, branch/commit/status/free disk | Preservation QA | Preserve initial evidence; do not recreate it over an old session |
| CREATED | `artifacts/B/initial_audit/registries/predictor_only_design.json` | Numeric bins, display limits, candidate neighborhoods/counts, selected candidate, recent cuts and exact effective dates, written before Y read | Every statistic/plot | `run` verifies equality on rerun; mismatches stop |
| CREATED | `artifacts/B/initial_audit/registries/feature_definitions.csv` | Formulas, source fields, units, windows/cutoffs, missingness/warmup and n | Gallery/report/feature audit | `run` |
| CREATED | `artifacts/B/initial_audit/registries/empirical_bins_and_support.csv` | **6,216** raw cell rows: FULL/sensitivities, heatmap and coarse5 bins, means/rates, n/groups/events, uncertainty/status; **2,344** valid interval rows | All figure curves/heatmaps | `run`; publication preserves byte hash |
| CREATED | `artifacts/B/initial_audit/registries/empirical_state_contrasts.csv` | **576** supported/abstained band comparisons; six endpoint cells, fixed masks, pairwise state increments and exploratory intervals | Fig4, triage and common-date comparison | `run`; missing scientific estimates remain blank, not zero |
| CREATED | `artifacts/B/initial_audit/registries/experiment_feasibility_summary.csv` | Exactly nine rows, frozen rubric indicators/ratings, n, effect/noise and stability counts | Gallery/technical report | `run`; not recomputed from validation |
| CREATED | `artifacts/B/initial_audit/registries/illustrative_cost_scenarios.csv` | 16 state/all × cost0/2/5/10 rows; hypothetical means/intervals and gross break-even | C1 figure4/report | `run`; no observed execution claims |
| CREATED | `artifacts/B/initial_audit/registries/feature_and_state_diagnostics.json` | Event prevalence/clustering, RV-state cross-occupancy, relative-volume tails and lag warmups | Scientific interpretation | `run` |
| CREATED | `artifacts/B/initial_audit/registries/feature_QA.json` | Seven real-date scalar checks, chronology, source/minute counts, exclusions and mask dates/counts | QA/report | `run` |
| CREATED | `artifacts/B/initial_audit/registries/output_QA.json` | All 44 image dimensions/hashes/links, feature schema/rows, support/draw counts, preserved-file count | Checked manifest | `qa` |
| CREATED | `artifacts/B/initial_audit/registries/final_integrity.json` | Final training-predicate, no-fit AST, frozen/numerical-hash, link, whitespace and test checks | Final handoff | Repeat small checks described below; do not substitute for source-data QA |
| CREATED | `artifacts/B/initial_audit/registries/initial_audit_manifest.json` | Source/code/output hashes, exact read trace, software, resource counters, publication history and session linkage | Restore/reproduction | Rebuilt by `run`; publication refreshes derived product references; final metadata refresh includes this report |
| CREATED | `artifacts/B/initial_audit/registries/execution.log` | Initial numerical/plot run stdout/stderr, 2,087 bytes | Debugging | Original completed run log retained |
| CREATED | `artifacts/B/initial_audit/registries/publication.log` | First formatting-only republication | Debugging / resource trail | Retained, ignored log |
| CREATED | `artifacts/B/initial_audit/registries/publication_final.log` | Second formatting-only republication after visual margin correction | Debugging / resource trail | Retained, ignored log |
| CREATED | `artifacts/B/initial_audit/registries/final_QA.log` | Standalone output/preservation QA command | Debugging | `qa` (its logged test count predates the final eighth test; authoritative final count is tests.log/final_integrity) |
| CREATED | `artifacts/B/initial_audit/registries/tests.log` | Final eight-test stdout/stderr, including benign Arrow hardware warnings | Test evidence | Unittest command below |
| CREATED | `artifacts/B/initial_audit/registries/visual_review_contact_sheet.png` | One **2,250 × 3,150** QA contact sheet of all44 scientific figures, **2,022,226 bytes**; not a45th scientific figure | Manual structural review | Recreate thumbnails from the 44 final PNGs; no original prices copied |
| CREATED | `artifacts/B/initial_audit/figures/A2/0[1-5]_*.png` | Exactly five named figures; 1 panel per main view | Gallery | `publish`; paths/hashes individually enumerated in manifest |
| CREATED | `artifacts/B/initial_audit/figures/A3/0[1-5]_*.png` | Exactly five figures; all4 late-return/acceleration variants | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/A4/0[1-5]_*.png` | Exactly five figures; gap and morning variants | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/A5/0[1-5]_*.png` | Exactly five figures; signed/magnitude/squares/both signs (6panels) | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/A6/0[1-5]_*.png` | Exactly five figures; recent principal/opening comparison on identical dates | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/B1/0[1-5]_*.png` | Exactly five figures; X-early and W-late adverse-event rates | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/B2/0[1-5]_*.png` | Exactly five figures; raw30/raw5/relative-volume variants | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/B3/0[1-5]_*.png` | Exactly five figures; lag1/5/20 variants | Gallery | Same |
| CREATED | `artifacts/B/initial_audit/figures/C1/0[1-4]_*.png` | Exactly four illustrative feasibility figures; costs are separate scenario panels | Gallery | Same; no fake fifth/learned-policy figure |
| CREATED | `reports/B/initial_audit_nine_experiments_feasibility.md` | Separate methods/results/limitations/reproduction report | Human review | `run`/`publish` |
| CREATED | `reports/sessions/20261016_1938_B_initial_audit_nine_experiments.md` | This mandatory new session record | Handoff | Preserve as audit evidence |
| CREATED → REMOVED | OS temporary `EBMShape_initial_audit_smoke_*/feature_fixture.parquet`, `smoke.json` | One-row feature fixture and tiny JSON output during smoke test; TemporaryDirectory removes both and its directory | Test only | Regenerated by test; no user data deleted |
| CREATED → ATOMICALLY RENAMED | This audit's `*.json.tmp` siblings for protocol/snapshot/design/feature-QA/state-diagnostics/output-QA/manifest/final-integrity | Existing `pilot.write_json` atomic metadata writes; no retained large intermediate | Above JSON products | Re-run affected metadata operation; no `.tmp` remains |

The exact shared figure basenames are `01_scatter_state_lines.png`, `02_conditional_means_with_intervals.png`, `03_raw_XZ_conditional_response_heatmap.png`, `04_support_and_state_contrasts.png`, and (eight directions) `05_temporal_and_outlier_robustness.png`. All44 final files, dimensions, bytes and hashes are individually listed in `output_QA.json`/manifest. Initial figures were replaced only by this session's formatting republications, never by alternative statistical analyses.

Consequential INSPECTED inputs:

| Action | Paths | Why / consumers / recovery |
| --- | --- | --- |
| INSPECTED | `AGENTS.md`, `README.md`, `.gitignore`, `pyproject.toml` | Binding workflow, storage, environment and Git/secrets rules; unchanged |
| INSPECTED | `docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md`, `docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md` | B science, cutoffs, no-leakage and claim separation; no new A work |
| INSPECTED | `reports/B/stage1_replication_benchmarks.md`, `stage1_5_linear_replication_diagnostics.md`, `stage2A_state_linear_and_spline_results.md`, `stage2B_EBM_ladder_scientific_results.md`, `stage2B_theory_applicability_and_implementation.md`, `stage2C_theorem_method_audit.md`, `stage2C_literature_anchored_A1_A2_closeout.md` | Prior context/qualifications only; prior development scores did not enter new triage |
| INSPECTED | `docs/experiment_B_stage2B_methods_and_model_registry.md`, `config/B_stage1_dataset_selection.json`, `B_stage1_5_diagnostics.json`, `B_stage2A_linear_spline_protocol.json`, `B_stage2B_EBM_protocol_v1.json` | Reuse original cuts/top-five dates and preserve existing model results; qualified negative findings unchanged |
| INSPECTED | `src/ebm_research/experiment_b/{daily,pilot,repair,acquisition,linear_diagnostics,stage2b,stage2c}.py` and existing thin script | Reuse actual calendar/RV/overlay/hash/guard semantics; do not call all-period loaders or fitting routines |
| INSPECTED | `data/registry/{B_stage1_daily_manifest,B_stage1_state_metadata,B_stage2B_ebm_manifest,B_stage2C_closeout_manifest,D2_spy_source_manifest,D2_1c_hf_repair_manifest}.json` | Canonical identities and historical metadata only |
| INSPECTED | `data/derived/B/B_SPY_daily_split_source1_stage1_v1.parquet` | Hash all bytes; project/predicate scientific reads to2016–2021 before transformation; no later outcomes |
| INSPECTED | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year=2016.parquet` through `year=2021.parquet` (6partitions) | Read one shared training projection, unique SPY/UTC-start keys; no new minute copies |
| INSPECTED, HASH ONLY | Same source directory `year=2022.parquet` through `year=2026.parquet` (5partitions); prior checkpoint models/artifacts | Preservation bytes/hashes only; no scientific deserialization/model prediction |
| INSPECTED | `data/patches/B/B_spy_hf_source1_D2_1c_v1.parquet`, `data/registry/D2_spy_missing_candles.csv` | Hash39row native patch, date/project before overlay; missing-key metadata; never use D2.1b |

The snapshot gives the complete preexisting hash inventory; the table need not enumerate every unchanged prior figure/import individually. `.env` and credential values were not read or printed.

## 3. Critical code, algorithms and variables

All new functions below are in `src/ebm_research/experiment_b/initial_audit.py` unless stated otherwise. Small text/selection/formatting helpers (`read_json`, `panel`, `select_rows`, `select_contrasts`, `number`, `markdown`, `plot_setup`, `y_unit`, `figure_title`, `panel_axes`, `save_figure`) perform their named local tasks and do not introduce a model or scientific selector.

| Function / signature | Inputs → outputs / callers | Algorithm, timing, assumptions and limitations |
| --- | --- | --- |
| `directions()` | None → nine fixed direction specs / freeze | All24 panels predeclared, no outcome-favorable variant retention |
| `root_data()` | Optional `EBM_DATA_ROOT` → Path / readers | Portable shared store, default repo/data; no hardcoded user path |
| `freeze()` | Existing configs/manifests/byte refs → protocol + snapshot / CLI | Verify source hashes; import old cuts and exact exclusions; freeze schemes before Y; refuse existing protocol overwrite |
| `read_training(path, columns, eligible=False, start='2016-01-04')` | Parquet → column-projected Arrow predicate result + read trace | End hard-limited2021-12-31; rejects start2022+ before I/O; initial Jan4 only for historical anchors; no all-period scientific load |
| `lagged_closes(close_series, h)` | Chronological scheduled-full P16 → lag returnbp | Shift1 then prior / prior.shift(h), all h+1 prior anchors finite; no current close; missing interior invalidates |
| `prior_volume(volume, lookback=20)` | Eligible full-session late volumes → denominator | `shift(1).rolling(20,min_periods=20).mean()`, excludes current/future, first20 missing |
| `feature_layer(data,p)` | Projected training daily/minutes + sole patch → joined predictor frame, new-only features, cuts, real QA | Original overlay collision/missing-key guards; late bars15:00..15:29 only; historical closes separately shifted; unique session, true XNYS full-session index, availability guards; no Y column read here |
| `real_feature_checks(frame,full,minutes,features,p)` | Seven real dates → scalar QA records | Independent scalar endpoint returns, acceleration,30RV increments, volume, lag returns and prior20mean; raises named date/field mismatch |
| `quantile_edges(x,count)`, `assign_bins(x,edges)` | Predictor values → unique edges / bin index | Pooled8/5quantiles; deterministic ties, equality lower; no response use |
| `panel_mask(frame,spec)` | Required finite feature/state and fixed sign facet → mask | No outcome filtering or imputation |
| `design(frame,p,cuts)` | Predictor frame only → numerical plans + common mask | Fixed candidate quantile bands, first with all6cells50/20; partners marginalized; exact candidates/counts saved before response read; negative sign facet can fail |
| `circular_indices(n,B,length,seed)` | n1495,B300,L5,seed → joint resampled row indices | Circular consecutive eligible-day blocks; same indices for all cells/states/panels |
| `grouped_bootstrap(cell,y,indices,n_cells)` | Joint row membership/outcome → B×cell ratio means/rates | Resample joint records; empty cells NaN, no independent state shuffle; fixed previously causal features/bins |
| `interval(values,support,p)` | Supported resamples → lo/hi/n/status | Require270finite and nondegenerate width; otherwise ABSTAIN; exploratory percentile variability only |
| `masks(frame,p,common)` | Training dates/old exclusions →8fixed masks | Original eligible indices/groups retained; no response-driven exclusions |
| `response(frame,identity,p)` | Frozen training Y/W → Y, adverse event or fixed-rule payoff | B1 threshold−20bp fixed; C1 sign(W)Y, zero flat; outcomes available16:00, never predictors |
| `cell_statistics(...,kind='curve',bin_count=8)` | Fixed bins/joint bootstrap → raw means/rates/n/groups/events/status | Display20/10, interval50/20; B1 separate5events/5nonevents/3eventgroups; coarse5 and continuous6Z bands retained |
| `contrast_statistics(...)` | Fixed predictor-only bands + target/mask →3state-pair differences | (b−a)high−(b−a)low plus M−L/H−M; all needed support checked; B1 outcome support applied AFTER selection without fallback; failed scientific estimates/intervals blank |
| `summarize(frame,plans,bins,contrasts,p)` | First declared panel + support/interval/sensitivity indicators →9ratings | Exact frozen conjunctive rubric; no composite/tuned score; C1 always deferred; no validation metrics |
| `feature_registry(frame,features,p)` | Shared features → formulas/counts/windows/missing rules | Existing X/W/Z referenced, new columns persisted only; event/payoff are labels only |
| `diagnostics(frame,features,cuts,indices,p)` | Training records → compact JSON and16cost rows | B1 class/clustering, A6 cross-state counts, B2tails, B3warmup; C1 cost per active day, no costs on23flat days |
| `draw_curve(...)`, `plots(...)` | Fixed registry values →44PNG | Raw points/empirical means, NaN gaps, actual cell/event counts; quantile-spaced heatmap geometry labeled numerically, no response interpolation; stop if figures exceed50MB |
| `write_reports(...)` | Same fixed results → gallery/index/technical report | Every variant shown; common-date table; source/proxy/selection/execution caveats. Narrative describes this exact hash-frozen dataset and is not used in decisions |
| `qa_outputs(preserve=True)` | Produced files + original snapshot → QA JSON |44PNGs decode/nonempty, links, feature-only schema/date guards, support/event/draw reconciliation,265original hashes |
| `run()` | Frozen matching sources → complete numerical/plot/report products + manifest | Numerical design written before explicit training-Y read; one statistical run; no full-data duplicate |
| `publish()` | Saved numerical CSVs/features + training-projected daily → refreshed plots/prose/manifest | No bootstrap/model rerun; checks four CSV byte hashes unchanged; logs publication resources/history |
| `main()` | `freeze / run / publish / qa` → bounded stage action | `run` errors save last_failure.json and re-raise; no actual run failed / no such file retained |
| `tests/test_b_initial_audit.py:InitialAuditTests` | Tiny deterministic fixtures →8unit/smoke checks | Includes direct hand D_HL5/M_L2/H_M3 example; no market simulator/framework |

Reused critical helpers: `daily.opening_rv` (30valid OHLC bars, first open→close +29close increments), `daily.at`/`guard_training`, `pilot.calendar`/`prior_full`/`write_json`/`sha`, `repair.merge_overlay`, `acquisition.verify_files`/`file_ref`. The existing all-period `repair.load_minutes` and `linear_diagnostics.load_training` were inspected but **not called**, because the current stage needs tighter date and column projection and no unnecessary model imports.

| Exact variable / config key | Location / meaning / units / default | Used by |
| --- | --- | --- |
| `OUT`, `PROTOCOL`, `TRAIN` | Module: audit root, frozen JSON, **2016-01-05–2021-12-31**; Jan4 historical-anchor read exception only | All orchestration/guards |
| `source_id`, `daily`, `data_refs`, `adjustment` | Protocol: daily `B_SPY_daily_split_source1_stage1_v1`, source hash and split/native39row lineage | Freeze/read/reproduction |
| `symbol`, `timezone` | SPY, America/New_York; physical UTC bar starts | Feature/calendar guards |
| `outcome` | Signed10000(C15:59/C15:29−1)bp,16:00availability | All targets; never a predictor |
| `opening_cutoffs_raw` | `[0.001558374721607106,0.0024281183976187152]`, frozen original training RV | Original state |
| `opening_cutoffs_log` | `[-6.46410542902094,-6.02063452513255]` | Original state; equality lower |
| `rv_epsilon`, `new_state` | 1e−8;30one-minute recent increments through15:29 | A6 principal recent state |
| `cutoffs_log.rv_late_log` | Numerical design: `[-7.0040583024795176,-6.413856387887993]`, separate recent-state TRAIN cuts | A6 only; not opening cuts |
| `directions.*.panels`, `cutoff`, `facet` | Fixed24panels, E10:00 or L15:30; ALL/NEGATIVE/NONNEGATIVE | Every plot/stat; no learned interaction declaration |
| `binning.primary/coarse/z_bins` | 8/5/6 pooled predictor-only quantile bins, deterministic ties | Raw cells; coarse sensitivity not ranking selector |
| `binning.display_quantiles` | 0.005/0.995, predictor-only viewing limits; tails retained in estimates | Scatter/curves; heatmaps retain whole bins on labeled quantile-spaced axes |
| `binning.display_min_n/display_min_groups` |20/10 | Descriptive curve/heatmap display, weaker temporal screen |
| `support.min_n/min_groups`, `strong_n/strong_groups` |50/20,100/30, pragmatic—not theorem constants | Intervals/contrasts |
| `support.event_min/nonevent_min/event_groups_min` |5/5/3 | B1 probability cells/contrasts only |
| `contrast_candidates` | `[.10,.30,.70,.90]`, `[.05,.35,.65,.95]`, `[0,.40,.60,1]` quantile bands, ordered | First qualifying endpoint rule before Y |
| `bootstrap.seed/B/length/min_valid/percentile` |20261016 /300 /5eligible rows /270 /[2.5,97.5] | Shared joint circular bootstrap; no stochastic learner |
| `exclusions.DROP_TOP1`, `DROP_TOP5` | Imported exact prior dates:18March2020; five=[18March,13March,28Feb,27March,24March2020] | Fixed sensitivities, never principal exclusions |
| `masks` | FULL, DROP_TOP1, DROP_TOP5, NO_2020, PRE_2020, YEAR_2020, YEAR_2021, COMMON_DATES | Every panel; no cutoff refits |
| `event_threshold_bp` |−20, fixedstrict less-than; −40optional omitted | B1 label |
| `costs_bp`, `rule`, `execution` |0/2/5/10bp, fixedsign(W) continuation, hypothetical C15:29→C15:59 immediate fills | C1 illustration only; no optimized sign/cost/entry |
| `ranking.*` | First-panel rubric; promising requires interval excluding0, materiality max1bp/.10SD or.02probability, all3fixed signs and≥2temporal signs,≥50%cell support; low priority small<.05SD/.01probability or severe instability | Summary, not significance/validation selection |
| `READS` | Projected column lists and Arrow predicates, no values/secrets | Manifest leakage audit |
| `FILENAMES`, `STATES`, `COLORS` | Five fixed names, low/middle/high, consistent blue/green/orange | Figure QA/interpretation |

The new feature table's exact columns are session_et; late_return_5m_bp/10m/15m, late_accel_bp, gap_bp, morning_bp, abs_x_bp, x_squared_bp2, x_centered_squared_bp2, abs_w_bp, rv_late_30/log, late_volume_30m/5m, relative_late_volume, lag_close_1_bp/5_bp/20_bp. There is **no Y, original price anchor, original X/W/opening-RV copy or minute-level row** in it. The manifest supplies content hash/schema identity.

## 4. Execution and reproducibility trail

Working directory throughout: repository root `.`. No dependency installation/environment modification was performed. Existing Python **3.14.6**, NumPy2.5.4, pandas3.0.6, PyArrow23.0.1, Matplotlib3.11.2 and exchange-calendars4.13.2 were used. Exact effective versions are in the manifest; existing `requirements-stage2B.lock.txt` remains unchanged. InterpretML/sklearn were not used for any fit. Randomness is solely the declared NumPy generator for joint descriptive block samples.

Ordered command register (repeated polls/read variants grouped; tool-based `apply_patch` created/edited only the new paths inventoried above):

| Order | Actual command / operation | Result / scope |
| --- | --- | --- |
|1| `pwd; git status --short; rg --files docs/specs config src/ebm_research/experiment_b reports/B` (inventory displayed through `head -100`) |0; actual clean Git state/source inventory |
|2| `cat AGENTS.md; cat README.md; cat .gitignore; cat '<user attachment>/Pasted text.txt'` |0; binding stage request; some long display output truncated, subsequent targeted reads used |
|3| `git branch --show-current; git rev-parse HEAD; git status --short; cat .gitignore; cat pyproject.toml` |0; main/6e6ed11/clean |
|4| `cat docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md; cat docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md` |0; supplemented by targeted `sed` reads below |
|5| `cat config/B_stage1_dataset_selection.json; cat config/B_stage1_5_diagnostics.json; cat config/B_stage2A_linear_spline_protocol.json` |0; repeated once with smaller output budget to inspect exact masks/cuts |
|6| `sed -n '1,240p' src/ebm_research/experiment_b/daily.py; sed -n '1,180p' src/ebm_research/experiment_b/stage2b.py` |0; daily/RV and old reader semantics |
|7| `cat data/registry/D2_1c_hf_repair_manifest.json; head -80 data/registry/D2_spy_source_manifest.json` |0; source1 sole patch |
|8| `cat src/ebm_research/experiment_b/daily.py`; `sed -n '1,150p' .../linear_diagnostics.py`; `sed -n '1,100p' .../stage2c.py`; `sed -n '1,90p' .../pilot.py` |0; existing implementation and hash/calendar helpers |
|9| `sed -n '1,155p' '<user attachment>/Pasted text.txt'` |0; direct reread of stage definitions |
|10| Shell `for f in` the seven prior report paths in §2, `head -38 "$f"`; `cat data/registry/B_stage1_state_metadata.json` |0; orientation, not new validation selection |
|11| `.venv/bin/python -B -` inline schema probe using `json`, `pq.read_schema`, `shutil.disk_usage` |0; inspected three manifest key sets, daily/minute column names, free61,849,600,000bytes; **no scientific row read** |
|12| `sed -n '190,330p' docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md`; `sed -n '1,120p'` B companion; `head -55 docs/experiment_B_stage2B_methods_and_model_registry.md`; `head -50 config/B_stage2B_EBM_protocol_v1.json` |0; feature/inference/protocol sections |
|13| `sed -n '1,160p' .../repair.py; head -75 README.md; ls scripts; rg 'def verify_files\|def merge_overlay\|def file_ref' -n src/ebm_research/experiment_b` |0; reuse and source inventory |
|14| `sed -n '50,80p' .../acquisition.py; sed -n '1,60p' scripts/b_stage1_5_diagnostics.py; sed -n '150,195p'` B spec; `sed -n '1,65p'` companion; `find artifacts/B -maxdepth 2 -type f` displayed with `head -15` |0; return/timing/reuse details |
|15| `.venv/bin/python -B -c 'from ebm_research.experiment_b.initial_audit import freeze; freeze()'` |0;1.57s; protocol frozen before Y;265preserved files; references9,465,699existing bytes |
|16| `rg '^def ' -n src/ebm_research/experiment_b/initial_audit.py; wc -l .../initial_audit.py; git status --short` |0; inspected new reusable function layout |
|17| `.venv/bin/python -B -m unittest discover -s tests -p 'test_b_initial_audit.py' -v` |0; initial6tests pass,1.72s process /0.014s tests |
|18| `.venv/bin/python -B scripts/b_initial_audit.py run > artifacts/B/initial_audit/registries/execution.log 2>&1` |0; only full statistical run,90.084s wall /61.127s CPU,300shared resamples,44figures |
|19| Repeated `tail -N` of execution/publication logs; `find .../figures -name '*.png'` counted with `wc -l`; `du -sh artifacts/B/initial_audit`; `git diff --check`; `ls -lT .../execution.log` |0; bounded progress/storage checks, no data acquisition |
|20| `ps -axo pid,etime,%cpu,rss,command` piped to `rg 'b_initial_audit\|PID'`; then `date; du -sh ...` |ps denied by sandbox; aggregate shell final status0. Optional process listing abandoned; no CPU/RSS claim based on it |
|21| `.venv/bin/python -B -` with pandas projected **generated training-only CSVs** and JSON diagnostics |0; inspected FULL high−low effects, event counts, cross-state matrix, costs and later COMMON_DATES B2/B3 comparisons; no source/validation outcomes |
|22| `tools.view_image` on A2fig2/fig4 and A5fig3 |Identified dense count/heatmap labels; no numerical changes |
|23| One `apply_patch` failed a context match around report narrative |No file changed by failed patch; split into matching patches |
|24| `sed -n '925,1050p' .../initial_audit.py` and successful patches |0; spacing, raw-heatmap coordinate labels, narrative and publication helper |
|25| `.venv/bin/python -B -` source-text replacements for readable prose; unittest command above |0;7tests after temporary-output smoke addition |
|26| `.venv/bin/python -B scripts/b_initial_audit.py publish > .../registries/publication.log 2>&1` |0;25.635s wall /25.089s CPU; same statistical CSV hashes, **zero bootstrap reruns** |
|27| `tail -12 .../publication.log; git diff --check; git status --short; wc -l .../initial_audit.py` |0; source/plot review |
|28| `tools.view_image` A5fig3, A2fig2, B1fig4, C1fig2, A4fig5; `head -38` gallery |Found remaining multirow title/footer/table crowding, corrected physical margins only |
|29| `.venv/bin/python -B -` preserve first publication's existing metadata in publication_history and minor new-prose spacing |0; no source/protocol/numerical edits |
|30| `.venv/bin/python -B scripts/b_initial_audit.py publish > .../registries/publication_final.log 2>&1` |0;26.853s wall /25.956s CPU; hashes of all4numeric CSVs unchanged, no resampling |
|31| `.venv/bin/python -B -` read COMMON_DATES contrasts/resource/feature-QA metadata; `tools.view_image` final B1fig4/C1fig2 |0; final layout readable; common-date comparisons corroborate reported sign qualifications |
|32| `.venv/bin/python -B -` training-only column-projected read + existing feature/CSV joins → `write_reports(...)`; PIL thumbnail contact sheet |0;4.52s process; added every panel's common-date D, prose only; original figures/numerics reused |
|33| `tools.view_image` contact sheet; `.venv/bin/python -B scripts/b_initial_audit.py qa > .../final_QA.log 2>&1`; unittest to tests.log; `git diff --check`; `git check-ignore` derivedParquet/fontcache; `cat .../final_QA.log` |0;44images/links,265original hashes, feature1495×19,72FULL/576total contrasts,5/241abstentions |
|34| `sed -n '330,470p'` B spec; `sed -n '85,190p'` companion; `tail -4 .../tests.log; git status --short; date` |0; closing scientific/economic and workflow safeguards |
|35| Added direct12row hand-calculated cross-state test; final unittest command to tests.log |0;**8tests**,0.069s test-body time; no broad older/model suites |
|36| `.venv/bin/python -B -` final frozen/CSV/read-predicate/no-fit-AST/link/whitespace checks |Initial assertion failed on one trailing space in new technical report; no statistical failure |
|37| Successful `apply_patch` makes report paragraph joins rstrip; inlinePython rstrip of that generated report |0; no scientific text/value change |
|38| Repeat small final-integrity Python checks + `qa_outputs()` |0;final_integrityPASS,8tests,44image links,265immutable files; no resampling |
|39| Final session creation and manifest metadata/hash refresh; `git diff --check`, ending status/resource checks |0 on completion; no Git stage/commit/push |

The inline final checker verified: unchanged protocol/numerical-design/four numeric-CSV hashes; every recorded source read ends2021-12-31; AST contains no `.fit`, `.fit_predict` or `.fit_transform` calls; every local Markdown link exists; new text has no trailing whitespace; tests.log endsOK with8tests; all output/preservation QA passes. It did not claim a generic sandbox/network theorem. Code inspection and actual offline call paths establish no network/model operation for this stage.

### Minimal reproduction / fresh machine

Use a compatible Python and the existing pinned dependency snapshot; install the project editable. Obtain **authorized matching inputs**, not a duplicate input tree: point `EBM_DATA_ROOT` to the canonical shared store with the manifest paths/hashes. These private data are not distributed by a public Git clone. Provider credentials are unnecessary for this offline audit; reconstructing vendor inputs separately requires lawful access and the earlier acquisition instructions.

```text
python -m pip install -r requirements-stage2B.lock.txt
python -m pip install -e .
python -B -m unittest discover -s tests -p test_b_initial_audit.py -v
python -B scripts/b_initial_audit.py run
python -B scripts/b_initial_audit.py qa
```

`freeze` is only for a genuinely new audit directory lacking its protocol; it fails rather than overwriting this approved frozen record. `run` checks existing numeric predictor design equality. `publish` regenerates layout/prose using fixed saved numerical files without a statistical rerun. Restore/recompute the one feature-only table if omitted by Git. No full source download or copied fold datasets are needed.

Protocol SHA256: `da9fbe99f4d64842ec8a76b7f5026f1683e20578361c845c5ca3c13567c3bf96`.
Daily SHA256: `2aa3e2df1cab897abd679ed9cbeff8f6fcb004ecc01a7b32c5938aa6c23b5c2f`.
Native patch SHA256: `398141da0889940fb03dcbe0faea29c5abd50da8fdc7d1e5deec7c0ed6f85172`.
Other source, design, code and final output hashes are in the manifest/snapshot. No secrets occur in these records.

## 5. Tests, scientific integrity and observed results

**Eight focused tests PASS**, including imports/config/read/write smoke in a temporary location; DST and completed-bar cutoffs; exactly30RV increments; past-only volume/current-close exclusion; missing interior lag anchor; reject later start before I/O; joint-cell circular resampling and degenerate abstention; boundary equality lower; direct hand difference-of-increments. The initial6test pass and intermediate7test pass are preserved in this execution trail; final tests.log is authoritative8test evidence. No old model tests/backtests were run because their paths were not changed.

Cheap real checks: seven dates—2016-01-05,2019-03-08,2019-03-11,2019-08-12,2019-12-02,2020-03-18,2021-05-06—agree with independent scalar formulas. Clock conversions show10:00UTC15:00 before spring DST andUTC14:00 after it. The December2prior anchor is2019-11-27, skipping the scheduled early close only. Return/acceleration endpoints exclude the15:30-start bar. The late RV has30increments, not29or a full-day proxy. Missing-opening full sessions remain in historical close indexing, while primary eligibility is unchanged. No current or future volume enters the prior20reference.

One shared training-minute projection contains **136,376 rows**, including the39date-filtered native patch rows. Minute symbol/UTC keys and session-date alignment pass. All1495eligible dates have valid recent RV. The existing canonical/provenance and prior whole-session audit are reused; no new assertion of full390minute storage/completeness was made.

| Direction | Eligible observations / variants | Rating / evidence |
| --- | --- | --- |
|A2|1495|INCONCLUSIVE; W H−L3.33bp, exploratory interval[−6.96,13.36] |
|A3|1495each,4variants|INCONCLUSIVE; last5−5.62bp vs last10+7.63bp; all H−L intervals cross0 |
|A4|1495both|INCONCLUSIVE; gap−19.53bp[−35.78,−5.94] nominal exploratory interval excludes0, fixed exclusions keep sign; only1temporal contrast supported at weaker display level. No two-environment confirmation |
|A5|1495base transforms;668negative /827nonnegative|INCONCLUSIVE; negative-magnitude3state-pair contrasts abstain; magnitude/square rank-bin results identical, not independent evidence |
|A6|1495both states|INCONCLUSIVE; recent H−L2.60bp[−8.69,12.55], opening3.33bp; same-state occupancy61.1% |
|B1|1495both|INCONCLUSIVE;217events (14.5%),140event-bearing five-rowgroups,52adjacent pairs; early H−L/M−L lack enough events, no fallback; late H−L−.0134probability[−.168,.132] |
|B2|1495raw30/raw5;1475relative|INCONCLUSIVE; firstrelative2016-02-03, raw and normalized signs differ with intervals crossing0; common1475date comparison preserves that qualification |
|B3|1494lag1 /1490lag5 /1475lag20|LOW_PRIORITY on firstpanel rubric; primary0.642bp[−7.85,11.28],≈.019SD(Y); effective startsJan6/Jan12/Feb3,2016 |
|C1|1495,23flat signals|MODEL_DEPENDENT /DEFER; gross0.833bp intervalcrosses0, hypothetical net means−1.14/−4.09/−9.01bp at2/5/10bp; gross break-even.846bp/active trade. Execution not established |

Common-date mask: **1475**,2016-02-03–2021-12-31. All variants retain matching common-date contrast rows, also shown in the gallery tables. No comparison ranks bp, probabilities or share volumes on an incommensurate common numeric scale.

Contrast support:50dates/20distinct nonoverlapping five-eligible-row groups in every needed neighborhood, strong100/30. Display20/10 is a separate weaker rule, never passed off as scientific contrast support. B1 additionally needs5events/5nonevents/3event groups. In the72FULL comparisons, **5ABSTAIN**=3negative-sign magnitude +2earlyevent state pairs; across576including fixed masks,241abstain. Blank estimates and intervals remain blank. Every reported interval has≥270finite joint draws and nonzero width. No zero-width fake uncertainty or unsupported gap interpolation was created.

Manual visual review: all44 on contact sheet; full-resolution A2fig2/fig4, A5fig3, B1fig4, C1fig2, A4fig5, and corrected B1/C1 layouts inspected. Label collisions were repaired through formatting-only republications. The final figures show actual data and masks, not placeholders or learned curves. Quantile-spaced heatmaps show numerical bin medians/log-RV ranges; coordinate spacing is not numerical width and no response is interpolated.

The frozen B signedY, overnight-inclusive X, opening RV, calendar and sealed dates remain unchanged. A6 is the **explicitly authorized alternative recent state**, and C1 is the explicitly authorized hypothetical illustration; neither replaces the original primary study. Experiment A remains scientifically separate and untouched. No2022–2023outcome columns or2024–2026scientific rows were read. Earlier reports were read for required historical context, not new validation selection. Prior validation is already developmental, not made fresh by this audit.

These are raw **broad-band, partner-marginal** observational comparisons, not pointwise conditional means, fixed-partner effects, causal estimates, EBM increments, theorem applications or executable alpha. Fixed bins/cuts/bootstrap do not repair nonstationarity, dependent heavy tails, multiple directions, data reuse or sparse recent environments. A high-RV level/variance alone is not moderation. No formal selective/confirmatory p-values or population-equivalence declarations were produced.

## 6. Errors, decisions and recovery

| When / operation | Symptom / cause | Action / affected files / recheck | Remaining issue / recovery |
| --- | --- | --- | --- |
| Long orientation reads | Tool display truncation, not file/parser errors | Used narrower `sed`/`head`/schema reads; no sources altered | No fabricated missing-source claim |
| Training Parquet reads/tests/publication | Arrow emits `IOError: sysctlbyname failed` for cache sizes/optional.neon, errno1 | Confirmed optional sandbox hardware-discovery warnings; reads/QA succeed; no entitlement escalation/dependency change | Warnings retained in bounded logs; not a data I/O failure |
| Optional `ps` progress probe | `operation not permitted: ps` | Did not use process listing; wall/CPU measured with perf_counter/process_time | Peak RSS not measured or claimed; no action needs unsandboxed process access |
| One report-edit apply_patch | Context match failed near `descriptions.append` | Atomic failure changed no files; inspected actual section and split patches | Resolved; no scientific product invalidated |
| First visual review | n/group text crowded around near-zero X; narrow heatmap cells unreadable | Uniform count tables; quantile-spaced labeled heatmap coordinates; republish from fixed CSVs | Numerical/threshold/input hashes unchanged |
| Second visual review | Multirow panel titles/footer collided with figure header/axes | Physical-inch top/bottom margins; count-row spacing; formatting-only republish | Final full images +contact sheet readable; no resampling |
| Manifest review | Active execution.log would change after final stdout, invalidating its in-run digest | Excluded live logs/cache from scientific product references; final immutable diagnostic refs captured after jobs finish | No data error; final manifest hashes audited after logging completes |
| Final whitespace check | Assertion on a trailing space in generated technical report | Strip paragraph-end whitespace in writer and existing generated report; repeat final integrity check | Resolved; values/protocol/figures unchanged |

No package import failure, incomplete acquisition, credential failure, fitted-model failure, missing required feature, leakage error or numerical integrity failure occurred. No scientific redesign was made after response inspection. Engineering choices—8/5bins,6continuousZbands, conservative display/interval/event gates, candidate bands, first-panel rubric and optional-feature omissions—were frozen before response exploration as requested. No unstated unmade scientific decision is required to complete this screen.

Resume from the final checked manifest, not from an old progress log. The numerical CSVs, feature table and44PNG are trustworthy **within the stated descriptive scope**. There are no quarantined partial products or running background jobs. Preserve protocol/design/snapshot. If a canonical hash fails, stop and locate the matching authorized source—do not refetch/replace and silently reuse scientific claims. If a later engineering change only concerns layout, use `publish`, then `qa`; do not rerun a model or use validation. A future scientific model stage needs separate approval and a fresh frozen protocol.

## 7. Resources, Git and handoff

Initial numerical/plot run:90.084s wall,61.127s process CPU. Formatting republications:25.635s/25.089s CPU and26.853s/25.956s CPU. **Combined major computation142.572s wall /112.171s CPU**, plus short tests/QA/prose/contact-sheet work (the prose/contact helper took4.52s). These are command compute times, not total conversational wall time. No peak-RSS measurement; no network bytes/calls; no fits; no unattended workers. No statistical resampling was repeated during the two publication passes.

New logical storage is approximately **14.4MB including source/tests/reports, diagnostics, 44scientific PNGs and the QA contact sheet**. The44figures total **9,678,364bytes**; contact sheet2,022,226bytes; feature-only Parquet246,685bytes; raw-data growth0. The audit root before this final session/manifest update measured14,308,690bytes; final exact bytes are refreshed in the manifest/final handoff. Source refs reuse9.47MB already on disk rather than copying them. Reported free disk before/after is61,849,600,000bytes; APFS/sandbox free reporting remained coarse/unchanged, so logical file sums are the observed incremental-use measure. Budget is comfortably below1GB retained and50MBfigures. No duplicates per direction/fold/model were created. The one small shared feature table and all cheap derived results are reused.

Ending status consists only of new audit paths:

```text
?? artifacts/B/initial_audit/
?? reports/B/initial_audit_nine_experiments_feasibility.md
?? reports/sessions/20261016_1938_B_initial_audit_nine_experiments.md
?? scripts/b_initial_audit.py
?? src/ebm_research/experiment_b/initial_audit.py
?? tests/test_b_initial_audit.py
```

`git diff --check` passes; untracked new-text trailing whitespace was checked explicitly because Git diff alone does not inspect untracked contents. DerivedParquet, logs and local font cache are ignored as intended. No existing tracked file changed, no files staged, no commit/push authorized or made. Prior pyproject, prior reports/configs/models and both canonical source/repair views remain byte-identical to the265file snapshot.

**Handoff:** Read the [standalone gallery](../../artifacts/B/initial_audit/NINE_EXPERIMENTS_VISUAL_REVIEW.md), [technical report](../B/initial_audit_nine_experiments_feasibility.md), protocol and final manifest first. The audit establishes data availability and honest support-limited raw views for all nine directions; it establishes no confirmatory mean-shape/predictive/trading finding. Review A4's nominal gap contrast alongside its absent temporal support, then A6's state reassignment and A5/B1 support abstentions. B3 has little primary moderation evidence; C1 lacks executions and is deferred. The next small safe action is human visual/scientific review and, only if a candidate is nominated, a separate frozen one-question model/comparator/multiplicity protocol. No new acquisition is needed for this completed feasibility screen; no sealed or reserved responses should be opened to rank these plots.
