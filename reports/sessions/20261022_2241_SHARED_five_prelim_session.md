# Five preliminary screens — execution session

## 1. Identification and verdict

- Session ID: `20261022_2241_SHARED_five_prelim`; local closeout date2026-10-22, America/New_York (EDT, UTC−04:00). Automated inventory recorded2026-10-23T01:12:59UTC /2026-10-22 21:12:59EDT; inspection began before that checkpoint. Agent: Codex, GPT-6 family; exact backend model not exposed.
- Scope: **SHARED / five new preliminary experiments**, separate from A/B/C. User requested actual autonomous execution, not a proposed plan. Instructions: `docs/ebm_five_preliminary_experiments_codex_execution_prompt_v1.md`; controlling science: `docs/ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md`; repository AGENTS.md.
- Starting/ending branch: `main`; commit unchanged: `3e9c2447064fb67d1c558d000a05ff93b6ddf987`. No commit, staging, push, branch change, package installation, EBM/ML training or trading backtest.
- Preexisting dirty files: the two design/execution documents above; `reports/C/C3_one_state_EBM_figures_for_human_review.pdf`; `reports/C/experiment_C_final_development_closeout_report_v1_0.md`. Preserved. `initial_state.json` was recorded after the new runner namespace had begun, so its Git listing also includes this session's early new files; it is not a claim those files predated the session.
- Implementation/QA verdict: **PASS WITH QUALIFICATIONS**. Stages0–4 executed, shared sources audited/acquired once, all five screens executed or explicitly held, figures generated and inspected, review ZIP produced, required corruption/storage/time/math checks passed. Scientific verdicts are distinct from implementation success.

| Experiment | Principal matched days/events | Outcome | Qualifications/blockers |
| --- | ---: | --- | --- |
| P01_INTRADAY_BETA | 248dates;86,904stock-bars | NO-GO for pooled mean-beta materiality screen | Late−early beta−0.04760,95% block interval[−0.09162,−0.01277], below frozen0.10materiality. Cross-stock dispersion comparison held:0balanced dates across all ten; HCA/KLAC have6eligible dates each. This does not disprove dispersion compression. |
| P02_SIGNED_RV | 1,454SPY dates | DATA HOLD for fixed-q shape | Low/middle/high states10/1,439/5dates; minimum30perstate; reference common logRV support empty. Raw semivariance and lag-controlled references retained separately, without promoting the held shape. |
| P03_TREASURY_HEDGE | 664dates | WEAK | High−low beta−0.04431,[−0.12623,0.03449]; later377dates all in low-spread state, so later full contrast unavailable. Current-vintage FRED lag qualification. |
| P04_VOLUME_REVERSAL | 220dates;2,200stock-days | WEAK | High−low slope0.01401,[−0.12674,0.25061]; temporal sign reversal and extreme-date sensitivity. Split-only price returns, survivorship-selected ten stocks. |
| P05_FOMC_RESPONSE | 47events | DATA HOLD | Negative11/positive36, minimum15per sign. Seven nonstandard/unverified time rows excluded. Unresolved workbook/chart discrepancy for2019-07-31; no substituted shocks. |

No GO recommendation was manufactured. Curvature was not tested. All examined dates are exploratory, not an untouched confirmatory sample. No future EBM stage launched.

## 2. Exact file inventory and recovery

Abbreviations below: `R=artifacts/five_state_shape_prelim_v1`, `D=data/shared/five_state_shape_prelim_v1`. The **complete path-by-path inventory, hashes, byte sizes, and Parquet schemas/counts** is `R/manifests/artifact_inventory.csv`. It includes ignored inputs, figures, logs and caches; grouped rows below are explicit globs, not omitted files. Mutable final-verification/storage logs and the inventory itself are identified as closeout snapshots rather than a recursive self-hash guarantee.

| Action | Repository-relative path | Why / what changed | Critical consumers | Recovery |
| --- | --- | --- | --- | --- |
| CREATED | `src/ebm_research/five_prelim/{__init__,core,run,sources,features,statistics,reporting}.py` —7files | New isolated workflow only: frozen contracts, bounded acquisition, observed features, OLS/date blocks, reporting/QA | Thin CLI and new tests | Restore from this change; no existing module overwritten |
| CREATED | `scripts/five_prelim.py` | Thin import/CLI entry | All phases | Rebuild from package main; no sys.path hack |
| CREATED | `tests/test_five_prelim.py` |19deterministic synthetic checks, including intentional mismatches | unittest | Rerun exact command below |
| CREATED | `D/.gitignore`, `D/README.md`, `R/.gitignore` | Ignore private inputs/caches/ZIP; document authorized data restore and portability | Fresh-clone users/Git | Recreate from this change; old `.gitignore` untouched |
| CREATED | `R/configs/*.json` —6files | Five distinct immutable scientific configs plus pre-screen analysis-completion declaration | Every screen/figure preflight | Never edit frozen scientific configs; new scientific version requires approval |
| CREATED | `R/manifests/*` | Source registry, frozen hashes, input identities/schemas, permission metadata, union/budget,124source+derived hash checks, QA/counts/environment/code snapshots; exact list in inventory | All pipeline stages/review bundle | Restore exact hashes; no first-glob or similarly named source fallback |
| CREATED | `R/manifests/remote_metadata/*` | Original source cards/listings/licenses, API revisions and primary-document metadata | Stage0freeze and provenance | Small published metadata; do not infer independent vendor-rights certification |
| CREATED | `R/checkpoints/{hf_months.jsonl,current_stage.json}` | One-pass monthly and final stage checkpoints | Safe resume | Verify retained output hash/counts before skipping; no second validated acquisition |
| CREATED | `D/market_1m/2019-{01..12}.parquet` —12files | Eight missing stocks only; genuine selected RTH OHLCV, UTC minute starts, source revision/validity flags; no new SPY/BAC/KO copy | Shared RV/5-minute features | Restore exact files; do not redownload completed months merely to rerun experiments |
| CREATED | `D/derived/*.parquet` —6files | Daily RV/semivariance2,699rows;5-minute returns104,760rows; stock daily/volume2,470rows; SPY/IEF returns664rows; ETF controls1,099rows; FOMC54rows | Five screens | Hash-verified read-only checkpoint; rebuild only through authorized version/repair, not silent overwrite |
| CREATED | `D/etf_daily/*` —4files | Two pinned small Parquets and receipts; entire published objects retained once, only required symbols/dates decoded for analysis | P03/P04 | Local private research source; not in ZIP/Git |
| CREATED | `D/fred_rates/*` —4files | DGS2/DGS10CSV and two receipts | Prior-available spread | Current vintage; no historical revision claim |
| CREATED | `D/fed_surprises/*` —120files | Workbook+chart-unitsCSV and receipts;5historical-calendarHTML+receipts;53official statementHTML+receipts | P05published shocks/time exclusions | Source workbook immutable; chart is QA only, no substitution |
| CREATED | `R/scratch/*.source.parquet.receipt.json` —12files | Upstream URL/LFS SHA/ETag/bytes retained after raw cleanup | Single-pass evidence | Keep receipts; raw source no longer needed |
| CREATED then DELETED | `R/scratch/2019-{01..12}.source.parquet` —12generated raw temporaries | Required one-month-at-a-time acquisition; each deleted only after selected output validation | No final consumer | Exact original paths/bytes/reasons in `logs/cleanup.jsonl`; recompute features from retained selected files, not redownload raw |
| CREATED | `R/reports/figures/*.png` —13figures; paired `*.meta.json` —13 | Five summaries, overview, three supported support/contrast pairs, P01scatter | Consolidated/per-experiment reports | Rerender from verified figures data and immutable configs; no old plots used |
| CREATED | `R/reports/figure_data/*.csv` —13 | Exact plotted x/y/CI/counts, including held support graphics | Figure verifier/ChatGPT review | Reconstruct from the exact shared inputs; hashes in sidecars |
| CREATED | `R/experiments/<ID>/{results,diagnostics,plots}/*`, five `report.md` | Separate summary/completion JSON, finite-bin tables, OLS diagnostics, per-stock betas, event LOO, figure references without image duplication | Per-ID review and consolidated report | Completed screens skip only if frozen config/input fingerprint match |
| CREATED | `R/reports/{shared_data_inventory,shared_download_integrity,shared_features_QA,experiment_input_contract_matrix}.md` | Human-readable sources/contracts/coverage/feature qualification | Audit/reproduction | Preserve actual failed support, no merged-q substitution |
| CREATED | `R/reports/five_experiment_prelim_closeout_v1.md` | Principal five-experiment scientific report with verified relative embedded images | EBM Theory review | Review with the six image attachments/ZIP |
| CREATED | `R/reports/five_experiment_execution_integrity_v1.md` | Commands, tests, hashes, storage, anomalies, per-ID QA | Scientific/reproducibility audit | Final local verification JSON is authoritative for last byte counts/ZIP SHA |
| CREATED | `R/reports/five_experiment_prelim_review_bundle_v1.zip` | Portable report/images/plotdata/configs/QA, no raw Parquet/XLSX | ChatGPT review | ZIP CRC, exact report bytes and image hashes checked; ZIP itself ignored by Git |
| CREATED | `R/logs/*` | Five stage reports, bounded phase/error/test logs, per-chunk storage trace, network/cleanup ledgers | Recovery/session evidence | Exact log list/size/hash in inventory; meaningful failed attempts retained |
| CREATED | `R/cache/matplotlib/*` —1font cache | Attributable cache contained under budget root | Renderer | Recomputable; not source evidence |
| CREATED | `reports/sessions/20261022_2241_SHARED_five_prelim_session.md` | Mandatory session record | Next session/reviewer | New unique report; no earlier session overwritten |
| INSPECTED ONLY | Two controlling `docs/ebm_five_*_v1.md`, `AGENTS.md`, `pyproject.toml`, old source registries/manifests under `data/registry/` and `artifacts/C/preliminary_RV_profile_v1_1/` | Instructions, dependency/source compatibility, exact immutable SPY graph | New source freeze |843protected preexisting files rehashed unchanged |
| INSPECTED ONLY | Existing six SPY annual+72supplement files; external99-stock raw/metadata roster and ten selected30mfiles; external LSTM permission/revision/completion manifests and12observed2019partitions | Reuse by reference, no copying | New shared derivative source graph | External roots via `PRELIM_SAE_ROOT` / `PRELIM_LSTM_ROOT`; exact paths in manifests |
| INSPECTED/RUN ONLY | `tests/test_c1r_readiness.py`, `tests/test_c2r_models.py` |14existing synthetic timing/OLS regression checks | Scoped verification | Existing code/results untouched; no EBM tests executed |

No preexisting user artifact was deleted, moved or renamed. Only the twelve new raw-month temporaries were deleted as explicitly required by the execution prompt. The review ZIP duplicates derived review artifacts only, not market inputs.

## 3. Critical code/function and variable register

All functions below are new. Config keys `target`, `predictor`, `frequency` are the runner’s explicit aliases for response, focal_predictor and input_frequency; this minor schema naming choice preserves the exact scientific contracts. Shared context: ROOT is resolved from package location, R/D are new namespaces, market input refs are read-only and SHA-bound; no credentials passed/logged. Failures identify the contract/source/hash operation and stop the affected computation. Trivial formatting helpers are omitted.

| Path:function / signature | Purpose, inputs → outputs / algorithm | Callers, timing and limitations |
| --- | --- | --- |
| `core.py:sha(path)`, `reference(path,root='repo')`, `path_for(ref)` | Streaming SHA-256; portable root/path/hash/byte identity; hash-verified path resolution | All phases; unknown/unsafe/changed refs fail, no fallback. External root env overrides supported. |
| `core.py:write_json(path,value,exclusive=False)`, `append_json(path,value)` | Atomic small JSON/checkpoints; bounded audit ledgers; convert nonfinite diagnostics to JSONnull | All stages. Exclusive creation protects frozen files. Null is unavailable, never zero. |
| `core.py:Budget(run=RUN,data=DATA,cap=10000000000).used/check(reserve=0,operation=...)` | Count R/D/new code/tests/session/cache; check physical free space and used+next reservation; append measured peak trace | Before downloads, chunks, features, reports/ZIP/final checks. Fails closed at cap; test simulates small cap. |
| `core.py:download(url,path,max_bytes,expected_sha=None,headers=None,budget=None)` | Bounded1MiB chunks into controlled `.part`; expected size/LFS SHA; atomic commit+URL/ETag/byte receipt | Stage1only. Valid receipt reuses exact file. Unreceipted existing/partial data do not silently overwrite. No global HF cache. |
| `core.py:contract(config,experiment_id,source_registry=None)`, `load_config(id)` | Assert distinct X/Y/Z/source/frequency/universe/output namespace, frozen config/design hashes | Before every screen/render. Reject P04same-day target, SPY/IEF role swap, missing shocks and aliases. |
| `run.py:inventory()`, `metadata()`, `freeze()` | Inspect local source graph/roster/permissions; small remote cards/listings only; freeze union and5configs before response fits | Initial stage0, immutable guards prevent overwrite. Universe chosen by coverage/sector, not response. |
| `run.py:main()` / `scripts/five_prelim.py <phase>` | Staged CLI: inventory,metadata,freeze,acquire,derive,screen,report,verify | No EBM/ML command exists in this runner. |
| `sources.py:utc_timestamps(values)`, `reconcile(frame)` | Documented epoch units/UTC parse; exact OHLCV duplicate collapse, exclude every conflicting key, validity/genuine flags | Source extraction/derivation. No arbitrary feed preference or imputation. |
| `sources.py:extract_month(raw,month,symbols,output)` | PyArrow65,536-row batches, frozen8-symbol union and RTH filter, OHLCV/key/month validation, zstd selected partition | Stage1one monthly object at a time. Entire monthly Pandas decode is never used. |
| `sources.py:validated_month_output(entry,month,output,revision=HF_REV)` | Source/month/revision/SHA/row-count/symbol-count verification → safe no-network skip | Acquisition resume/final integrity/tests. Hash/count mismatches reject. |
| `sources.py:read_xlsx(path)` | Read-only ZIP/XML values, shared strings and sheet relations → published workbook sheets/rows | Source/schema and event parser; no workbook authored or edited. |
| `sources.py:acquire_all()` | Frozen12-month union once, then independent ETF/FRED/workbook/official-time branches; capped downloads/receipts and raw cleanup | Stage1only.2021 historical-calendar404 handled by published workbook dates→official statements. |
| `features.py:minute_summary(frame,source_id)` | Genuine full390-minute XNYS sessions → RV/RS/q/event data,72five-minute stock/market returns and per-session quality | Derive; UTC ns normalization avoids us/ns false rejection. Only RTH; no overnight or filled price. Incomplete/half sessions excluded. |
| `features.py:next_session(day)`, `previous_session(day)`, `label_daily(frame)` | Exact exchange-calendar neighbors; same-symbol lag/next RV joins and log transforms | Derive, tests. Never leap across a missing/half-day next target. |
| `features.py:volume_lookback(values)` | logVtoday−rolling mean(logV prior20eligible sessions), current excluded | P04 stock aggregation; nonpositive volumes unavailable, no guessed share denominator. |
| `features.py:stock_daily(registry)` |10original observed30mOHLCV+metadata → full13-bar O/C/volume, split-only CC/current/next returns and volume state | Derive. Metadata schema2/hash/adjustment checked; source is not the filled indicator layer. |
| `features.py:lag_rates(rates,returns)` | DGS10−DGS2pp; next US-federal-business-day17:00ET availability; strict backward join before ETF09:30open | P03; conservative assumption and current-vintage limitation, not ALFRED reconstruction. |
| `features.py:etf_rates(acquired)` | SPY/IEF actual ETF identities, same O-C bp log return, daily key/OHLC checks, prior-available rates/control table | P03/P04; not total returns, not yield changes. Missing instrument/invalid bounds reject. |
| `features.py:parse_events(workbook,official)` | Updated FOMC raw MPS rate-pp×100→bp; unique published dates and both workbook/official14:00 flags | P05. No MPS_ORTH substitution; nonstandard/unverified releases excluded. |
| `features.py:derive()` | Shared one-source traversal for RV/5m/event prices, native30m and macro/event joins →6small shared Parquets+schema/fingerprints | Stage2; validated existing checkpoint verifies/returns read-only. No new acquisition. |
| `statistics.py:block_weights(dates,length,B,seed,event=False)` | Circular blocks on scheduled-session slots, preserving gaps; event-pair option | OLS/bin CIs; shared date weights across all stocks. Fixed5-session exploratory sensitivity, not robust coverage theorem. |
| `statistics.py:design(frame,states,controls=(),fixed_assets=False)` | State intercepts + state×X slopes + declared lag/market control and optional stock fixed effects | OLS references; targetY and X units remain experiment specific. |
| `statistics.py:fit_daily(frame,states,controls=(),fixed_assets=False,B=500,seed=20261022,event=False,extra_contrasts=None)` | OLS least squares; per-date XX/XY; weighted normal equations bootstrap; percentile slope/contrast CIs, rank counts and residual moments | All state models/per-stock/reference regressions. Singular bootstrap draws reported, not fake zeros. |
| `statistics.py:fit_point(frame,states,controls=(),fixed_assets=False)` | Declared OLS contrast on temporal/outlier sensitivity subsets → slope difference or NaN | Missing states/rank deficiency → unavailable; not silently merged. |
| `statistics.py:bin_curves(frame,states,cfg)` | Reference-X5–95% common overlap,7fixed bins, finite-bin raw means, joint date-block CIs/count masks | Three informative plots; P02no common support. No smoothed/extrapolated missing tails. |
| `statistics.py:terciles(values,reference_mask)` | Reference-period33/67% cuts, unchanged outside reference | P03macro, P04per-stock volume. No Y/validation refit. |
| `statistics.py:preflight(id)`, `load_frame(id,cfg,inputs)` | Config/source/derived hash assertions, print ID/X/Y/Z/unit/period/fingerprints, exact target/state construction and eligibility | Before each screen; source mismatch/absent definition → explicit DATA HOLD, no best-effort substitute. |
| `statistics.py:analyse(frame,states,controls,cfg,label)`, `screen()` | OLS/conditional means plus declared halves/top1% |X| date stress; materiality/support/stability verdict; separate per-ID receipt/results | Stage3. P02SPY principal, stocks separate; P05minimum15/sign abstention with signed benchmark/LOO only. |
| `reporting.py:provenance(id,result)`, `check_sidecar(meta,expected,figure=None,data=None)` | Bind IDs/X/Y/Z/config/source/input/time and figure/data hashes | Before embedding and verify; wrong ID/target fixtures rejected. |
| `reporting.py:check_png(path)`, `check_links(path)`, `publish(fig,id,suffix,table,result,...)` | Actual PNG decode/size/nonblank/text bounds, exact CSV numeric roundtrip, semantic sidecar and relative image validation | Every figure. Off-axis undrawn Matplotlib ticks excluded from clipping test; true drawn text checked. |
| `reporting.py:figures(id,result)`, `beta_scatter(result,inputs)`, `overview(results)` | Measured response/support/contrast PNGs; P01deterministic strided raw scatter; truthful HOLD diagnostics; six-image contact sheet | Stage4. Scatter thinning only for display, all observations retained in primary fits/bins. |
| `reporting.py:validate_statistics(id,result,inputs)` | Independent OLS reconstruction, regenerate all conditional coordinates/intervals/counts, direct source means; held counts verified | Before embedding. Percentile CI center deviations flagged rather than coerced. |
| `reporting.py:integrity_audit()`, `resources()` | Legacy/source/config/metadata/month/temp checks, unique12network transfers, measured/reserved storage | Reporting/finalverify. No mirror or12-month second pass accepted. |
| `reporting.py:write_reports(results,qa,integrity)`, `bundle()`, `report()`, `verify()` | Consolidated and5per-ID reports, provenance/runtime snapshots, raw-free reviewZIP, CRC/image/report identity, final receipt/checkpoint | Stage4. ZIP receipt/inventory excluded from ZIP self-hash recursion; final local verification records actual ZIP SHA. |

### Critical frozen variables/config keys

| Exact name → file | Meaning/units/default → consumers |
| --- | --- |
| `IDS`, `CONTRACTS` → `core.py` | Five exact source/X/Y/Z/frequency/unit declarations; all preflights/tests/sidecars |
| `STOCKS` → `core.py` and5configs | BAC,KO,HON,ORCL,DHR,KLAC,LOW,HCA,SLB,IP. Ten verified99-roster members; no post-result substitutions. CAT/JNJ absent roster. |
| `HF_REV` → `core.py` | `776328445b7ac6e7815ef3a483e9c8ded1eb6d56`; only mito0o852/OHLCV-1m,2019-01…12; new8stocks, existingSPY/BAC/KO referenced |
| `coverage` → five configJSON | P01:2019; P02:2016-01-04…2021-12-31 (stocks2019only); P03:2021-05-12…2023-12-29; P04:2024-09-26…2025-09-25; P05:2016–2021. Actual complete cases recorded separately. |
| `session_timezone`, `storage_timezone` | America/New_York /UTC; minute/30m timestamps are bar starts; DST via calendar/zone data |
| `minute_RV_definition`, `p02_q_bins` |389close-to-close intervals; no overnight/opening OC term, epsilon0/positiveRV; q fixed[0,1/3,2/3,1] |
| `p02_lag_control` | Immediately preceding scheduled session logRV; next scientific target immediately next scheduled session logRV |
| `reference_period_end` | P01:2019-06-30; P02:2019-12-31; P03:2022-06-30; P04:2025-03-31; P05:2018-12-31. Cuts/edges reference-only; halves are sensitivity, not held-out validation. |
| `p04_volume_definition`, `p04_market_control` | Own logV−previous20eligible logV mean; per-stock reference terciles; same-day SPY O-C control; stock CC price target remains next-session |
| `adjusted_returns` / raw metadata | Price log returns, not total returns; stock30m split-only/not dividend adjusted. ETF primary O-C avoids unsupported total-return claim. |
| `bootstrap` | B500, seed20261022,5scheduled-session circular blocks; all rows per date together. Event-pairs method declared, but P05shape held before unreliable bands. No InterpretML errors used. |
| `support` | State minimum30dates; bin minimum10dates; P05minimum15events/sign and6/bin. These rules were frozen before fits; never changed to obtain curves. |
| `bins`, `x_anchors` |7common bins. Anchors P01[−10,10]bp (outside sharedsupport→withheld), P02[−11,−9]logRV (no support), P03/P04[−100,0]bp, P05[0,10]shockbp. Whole-linear-surface D=Δslope×ΔX only on common support. |
| `materiality` | Slopes: P01/P02/P03:0.10; P04:0.02; P05:1bp/bp. GO requires material size, interval excluding0, supported bins/states, stable sign across declared sensitivity subsets. NO-GO is sample-specific small contrast, not population equivalence. |
| `p05_zero_tolerance_bp`, `p05_event_window` |0.01bp excluded nearzero; rawMPS×100to bp; SPY C14:29/C13:59 for14–14:30; preQA C13:59/C13:54 for13:55–14. No alternate-time shifting. |
| `source_registry_sha256`, `scientific_design_sha256`, `input_fingerprint`, `output_dir` | Frozen exact source/design/derived identity and per-ID namespace; configs listed in `frozen_configs.json`. No model interaction declaration exists: only state-interaction OLS, EBM/ML prohibited. No trading costs/P&L assumed. |

## 4. Execution and reproducibility trail

Working directory for every command: repository root. Main recorded sequence:

```text
git status --short
git branch --show-current
git rev-parse HEAD
cat AGENTS.md
cat docs/ebm_five_preliminary_experiments_design_and_shared_data_plan_v1.md
cat docs/ebm_five_preliminary_experiments_codex_execution_prompt_v1.md
.venv/bin/python -B scripts/five_prelim.py inventory
.venv/bin/python -B scripts/five_prelim.py metadata
.venv/bin/python -B scripts/five_prelim.py freeze
.venv/bin/python -B scripts/five_prelim.py acquire
.venv/bin/python -B scripts/five_prelim.py acquire > artifacts/five_state_shape_prelim_v1/logs/acquire_resume.log 2>&1
.venv/bin/python -B scripts/five_prelim.py derive > artifacts/five_state_shape_prelim_v1/logs/derive.log 2>&1
.venv/bin/python -B scripts/five_prelim.py derive > artifacts/five_state_shape_prelim_v1/logs/derive_corrected.log 2>&1
.venv/bin/python -B scripts/five_prelim.py derive > artifacts/five_state_shape_prelim_v1/logs/derive_final.log 2>&1
.venv/bin/python -B scripts/five_prelim.py screen > artifacts/five_state_shape_prelim_v1/logs/screen.log 2>&1
.venv/bin/python -B -m unittest discover -s tests -p 'test_five_prelim.py' -v > artifacts/five_state_shape_prelim_v1/logs/tests_final.log 2>&1
.venv/bin/python -B scripts/five_prelim.py screen > artifacts/five_state_shape_prelim_v1/logs/screen_resume.log 2>&1
.venv/bin/python -B scripts/five_prelim.py report > artifacts/five_state_shape_prelim_v1/logs/report_verified_release.log 2>&1
.venv/bin/python -B scripts/five_prelim.py verify > artifacts/five_state_shape_prelim_v1/logs/verify_final.log 2>&1
git diff --check
```

Inspection also used `rg --files`, `rg`, `cat`/`sed`/`tail` on the specific source/manifests/code/tests named in the inventory; read-only bounded PyArrow/pandas probes; web primary-source verification for source cards/FRED/Fed release conventions and Bauer–Swanson ED4 units; read-only spreadsheet skill instructions for the SF Fed workbook. No spreadsheet was authored/edited. The pipeline uses stdlib ZIP/XML because openpyxl is absent; no extra package was installed. Source URL/query/ETag/hash/actual-byte execution trail is `logs/network.jsonl`; no secret values appear.

The two derive failures are **not** successful data products: first INT-stopped at PID62660 after zero complete SPY days from unit mismatch; second exited1at strict-universe check because reused BAC/KOextended hours were not yet filtered. `derive_final.log` exits0and is the trusted derivation. Reporting development attempts are preserved in `report*.log`: first clipping false positive, then absent optional `interpret` distribution metadata; repaired as noted below. Subsequent cosmetic/QA additions rerendered small figures only, without recomputing frozen scientific screens or downloading inputs. Exact log list/timestamps/approximate log-wall-time evidence is `manifests/execution_timing_estimates.json`.

Environment: Python3.14.6; NumPy2.5.4, pandas3.0.6, PyArrow23.0.1, SciPy1.18.1, statsmodels0.15.0, matplotlib3.11.2, Pillow12.3.0, exchange-calendars4.13.2. Full installed-distribution and code hashes: `runtime_environment.json`. Optional `interpret` metapackage absent; `interpret-core` recorded but unused. Source design SHA `519a2bca9ec060d0c3552926d2103e99c825d59e8c2905ce535fd8795f02ac14`; execution prompt SHA `6ac2ea3550f9d9cbfb4f0f02505814e189eda44ad97602bec5ce65ea5f8566c1`; input fingerprint `877717c8fddd79652f725482ac9bf43ba198f67111dad377c6176ce3f1df8909`. All five config hashes and source-file hashes are in the immutable manifests, not inferred from names.

### Fresh clone / portable restore

Create a suitable Python environment and install `pip install -e '.[stage1_5]'` with the exact recorded dependency versions for a matching run. A public clone does not include licensed/private source extracts. Obtain authorized hash-matching SPY base/supplements, the original selected30m files and observed BAC/KO2019partitions; set `PRELIM_SAE_ROOT` / `PRELIM_LSTM_ROOT` if external locations differ. Use `D/README.md`, the resolved path map and manifests to restore files; do not fabricate data or replace filled layers with observed ones by relabeling. Small upstream sources remain subject to their documented research/redistribution terms.

Smallest checks: run the19new synthetic tests, then `python -B scripts/five_prelim.py verify` on a restored completed run. `screen` validates/skips completed receipts. `derive` verifies/skips the immutable shared checkpoint. Do not invoke `inventory`/`freeze` over this existing run; do not delete a validated month to force reacquisition. If an essential exact source cannot be restored, report DATA HOLD. No provider tokens are required for these new public small downloads; authorization for existing private datasets is still necessary.

## 5. Tests, audits and scientific integrity

| Check / actual command | Result and scope |
| --- | --- |
| `.venv/bin/python -B -m unittest discover -s tests -p 'test_five_prelim.py' -v` | **19PASS**,2.938s at final recorded execution. Covers smoke import/output, config/source/schema isolation, intentional SPY/IEF reversal, wrong P02source/frequency, missing FED_SHOCKS, P04same-day target, stale config, tampered source, allowed shared read-only reference, DST/half-days, us/ns regression, exact5m/event arithmetic, RVsemivariance identity, strict calendar target, prior20volume, ETF O-C identities, FRED availability, rawshock×100/sign/official join, verified month resume/count/hash, cap simulation, OLS hand calculation+statsmodels, wrong sidecar ID/target, broken embedded links. |
| `.venv/bin/python -B -c 'import unittest; loader=unittest.TestLoader(); suite=unittest.TestSuite(loader.discover("tests",pattern=p) for p in ["test_c1r_readiness.py","test_c2r_models.py"]); result=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(not result.wasSuccessful())'` | **14PASS**,0.234s. Existing synthetic timing/path/OLS/HAC/basis/chronology checks only. No existing experiment data/result write. |
| `screen` then `screen` resume | Five distinct preflight identities printed. Second run skipped all5verified receipts without refitting or networking. |
| Native30m real-data audit | **32,320bars** across selected ten-stock/date range: OHLC bounds passed; prior full13bar/day eligibility and native observed volume audited. Exact symbol/date/row counts and limitations saved. |
| `report` reconstruction | All plotted supported finite-bin means/CI/counts regenerated from source; independent direct source means checked per state; cached OLS coefficients reproduced. Held P02/P05counts match source. All13PNGdecoded,≥1200px, nonblank and text-boundary checks pass; shared grids/NaN gaps and correct labels preserved. |
| Image opening | Five summary PNGs and overview actually opened with `view_image`, plus P01support/contrast/scatter and additional contrast figures. Numeric/date/unit/support qualifications inspected; final image hashes recorded in manual review evidence. |
| `verify` |843old files unchanged; original/derived/metadata hashes, five frozen configs, unique12validated monthly objects and12successful transfers; no source mirror; zero raw/partial temp files; ZIPCRC, exact report and image bytes; embedded relative images valid. |
| `git diff --check` and new-file text scan | PASS; tracked diff empty and no trailing whitespace in new code/config/report text checked. New artifacts are untracked/ignored, not staged. |

**Total33tests passed,0failed** in the final recorded suites. Full repository discovery intentionally skipped B-stage2B/C3EBM-training tests because this task prohibits EBM/ML training and changes no such path. Existing exploratory source data are not certified by a toy fixture; actual source/hash/calendar/coverage audits are separately recorded. No untouched test claim, causal inference, profit/novelty assertion or exact-paper replication label. No A/B/Ctarget/state/split was modified or pooled into these new scientific outcomes.

GO/WEAK/NO-GO/DATA HOLD are frozen operational exploratory classifications; they do not measure a theorem or correct for searching across five ideas. Raw bin averages differ from controlled OLS surfaces. Whole-surface four-point contrasts use intercept/control cancellation only for the fitted linear state model, never a single EBM term. P01anchors are withheld outside common support. P02fixed sparse states were not merged; P05alternate events were not shifted to14:00. Weak/negative scientific results are not test failures.

## 6. Errors, exceptions, decisions and recovery

| When / operation | Symptom and confirmed/suspected cause | Fix / affected files / verification / residual issue |
| --- | --- | --- |
| Initial metadata/acquisition network inside sandbox | urllib DNS/host resolution failure; sandbox-related | Retried required network command with approved escalation. No scientific/source substitution, no install. Receipts prove12successful objects, no duplicate validated pass. |
| Stage1Fed2021calendar | Official historical2021page404; five-year historical-page publication lag | Allowed minor endpoint repair: published2021workbook dates→direct official statement URLs. `sources.py`. Twelve already validated months skipped on recovery. Seven nonstandard/unverified source events remain excluded. |
| First derive, `features.minute_summary` | UTC `datetime64[us]` `.asi8` compared with calendar ns; zero eligibleSPYdays despite correct clock | INT-stopped own job before derivative commit/statistics. Normalize both DatetimeIndex resolutions to ns. Small us/ns regression test passes. Failed log preserved; no invalid estimate retained. |
| Second derive / strict universe audit | Reused BAC/KOobserved cache contains pre/post-market bars;390count check rejected every cached day | Apply frozen09:30–16RTH mask before completeness. `features.py`; extended-hours synthetic test. Final derivation exits0,2,699complete RVdays and all11minute symbols present. No missing minute filled. |
| Final manual color/label review | P03/P04support count bars had correct labels/values but colors followed sorted groupby order instead of canonical state order; unavailable later-period text sat on plot edge | Reindex support by canonical states, assert bar heights/colors, freeze sidecar series order/colors and test reversal rejection; add half-row vertical margins. Final corrected supports and six reviewer images opened again. Scientific outputs unchanged. |
| Figure boundary QA | Matplotlib retains tick Text objects outside current axis view that are not drawn; false clipping flag `1.2` | Exclude only out-of-view undrawn tick labels from extents check; keep real visible-text checks. `reporting.py`; actual exported images pass and visually inspected. |
| Environment snapshot | `importlib.metadata.version('interpret')` absent despite installed interpret-core | Optional package absence is recorded, no package installation/training. Python/numeric packages remain unchanged. |
| SF Fed units QA |53/54overlapping workbook×100 values within0.025bp of chart;2019-07-31workbook0.575979vschart5.29bp, discrepancy−4.714021bp | Unit factor independently documented by author paper; source discrepancy cause **unresolved**, possibly vintage/revision. Keep frozen workbook rawMPS; do not substitute chart. Exact comparisons saved. P05already held for11negative events; no valid shape claim. |
| Sparse coverage/support | HCA/KLAC6complete days;0balanced all-stock dates; P02tail states10/5; P05negative11; P03later only low state | Scientific non-results preserved. No universe/year/state/window tuning. Dispersion and unsupported anchors/curves withheld; P03later contrast explicitly “not estimable.” |
| Sandbox PyArrowCPU metadata | sysctl CPU-cache/neon probes denied; data reads still succeed | Benign bounded warnings retained in logs. Tests/math/hash/data invariants pass; no CPU capability assumption used. |

All fixes are allowed minor engineering/schema/endpoint/plot-audit corrections, not a scientific redesign. No newly larger source union, alternate shock, merged qstate, guessed total return or altered cap was authorized or implemented. No approval is currently pending. Data holds need scientific review/new version or genuinely independent adequate data before later modeling; they do not block reviewing completed artifacts.

Trusted checkpoint: `R/checkpoints/current_stage.json` after finalverify (`ALL_GATES_VERIFIED`, next actionSTOP). Trusted inputs: `validated_inputs.json`; frozen science `frozen_configs.json`; final results under each exact ID. Bad derive/report attempts are logs only, not quarantined scientific estimates. Resume with `verify`, or inspect the closeout Markdown and final integrity/storage/visual QA manifests. Do not rerun acquisition to repair a scientific support failure.

## 7. Resource/Git summary and handoff

- Initial repository baseline838,104,304bytes; initial physical free59,392,000,000bytes. TenGB cap is incremental, not total sibling-project size. Forecast620,814,381bytes; all next-step reservations below cap.
- **Measured incremental peak297,766,292bytes**, including staged raw monthly object and attributable logs/code/data/cache. Source downloads totaled3,209,573,881network bytes over12successful monthly objects, but only one raw month existed at a time. Network acquisition timestamps01:50:50.122157–01:52:06.938208UTC (about76.82s); CPU derivation/statistics/rendering use recorded log elapsed estimates. No unattended polling/jobs/schedules remain.
- Before final session/inventory additions, retained shared data19,213,917bytes; run artifacts about7.25MB; code/tests/session add a small remainder. Exact final retained bytes and largest reserved envelope: `R/manifests/final_storage.json` / `final_verification.json`. Rough retained total27MB; well below hard10,000,000,000bytes. Tiny synthetic test tempfiles automatically cleaned; next-step reservations conservatively cover them. No global HF/package cache created; one Matplotlib font cache lives underR/cache.
- Duplicate downloads prevented: existing78SPYsourcefiles,12BAC/KOcachefiles, ten raw30mstockfiles and validated12new filtered months reused by hash; no experiment-level market copies. Review ZIP contains small review outputs only. New source inputs are ignored by namespace `.gitignore`; no raw data staged.
- Final Git status: main/unchanged commit, no tracked modifications; newRnamespace, DREADME/ignore, source package, CLI, test and this session report untracked. The four preexisting dirty files remain untracked and unchanged. Exact final `git status --short`, diffstat/check and new-file text QA are in `R/manifests/git_closeout.json`.

Handoff: read [the consolidated scientific closeout](../../artifacts/five_state_shape_prelim_v1/reports/five_experiment_prelim_closeout_v1.md), then execution integrity, exact analyzed sample counts and final source/storage/visual verification manifests. Review P03/P04asWEAK, P01pooled small beta contrast with unsupported dispersion, P02/P05asDATA HOLD. No unmade scientific decision was silently resolved; source discrepancy/coverage limitations are explicit. The next action is **scientific review only**, using the Markdown+reviewZIP+six summary/overview PNGs in the EBM Theory ChatGPT chat. No EBM sweep, extra archive pass, backtest or new study has been started.
