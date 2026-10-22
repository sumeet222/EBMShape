# Experiment C / C1R — source, state and protocol readiness

**Stage: READY_FOR_C2R_DEV. Implementation QA: PASS WITH QUALIFICATIONS.** The verified existing P0 dataset supports a separately authorized **development-only** C2R using Z0 on the already explored 2016–2021 cohort. No modeling or scientific hypothesis test was executed. H2's return-sign branch and the volume branch remain blocked on explicit policies. Full-horizon eligibility, official split dates, new source acquisition and C evaluation are pending; this report does not release them.

Task `C1R_SOURCE_STATE_PROTOCOL_v1_1`, executed 22 October 2026, America/New_York. Starting branch `main`, commit `f05f23a27e7bd5133b3ba055afd1fae160dfd7c6`; preexisting dirty state consisted of untracked `docs/specs/C/`. Those user-supplied files were preserved. No commit, staging, push, deletion of preexisting material, network call or download occurred.

## Authority and change control

Both approved v1.1 documents and original C v1.0 are present; no required authority is missing. Root AGENTS was read in full, including its mandatory session-report rule. The current executable C1R request overrides obsolete prompt-writing instructions inside the older handoffs. Original v1.0 remains the R1–R6 literature ledger; no external paper was downloaded or independently reverified here.

| Authority / evidence | SHA256 |
|---|---|
| docs/specs/C/experiment_C_revised_complete_research_design_v1_1.md | d402d316e5bf37c43169091cf7377c5bc170a0c74626f51135ac51350cf8c57b |
| docs/specs/C/experiment_C_revised_transition_and_next_stage_handoff_v1_1.md | 072871e0bdacd28324afa4ac4d8d73389b383e2e8c448477059ac94b9dd66ce7 |
| docs/specs/experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md | 5fa9fc0dba2d4dd31c6be6fa7ce226b27ffedf395f252a7116a30bf0fce3fd3e |
| docs/specs/experiment_C_P0_supplied_handoff_v1_1.md | 78e941c0e6fb42480e77a7f32f20f58164698f63393a9d755b5deca69f68261c |
| AGENTS.md | 6727aa17db8369d915d1a85a61b9c1ad1b6b1f9117aef9bc59f807ef72f12455 |
| data/registry/C_preliminary_RV_profile_v1_1.json | a31c8c4349acc62222aba210f7fdc1d9134496082ac64000406eb86f1ed67adb |
| artifacts/C/preliminary_RV_profile_v1_1/source_manifest.json | a63fe1d6314054240d8b2ac488922a8021f85d55434bfd49001298f5d5e4ff99 |
| config/C_preliminary_RV_profile_v1.json | b8021e9235b75733c6d53c46963b5879a49d689174bcc31e0b2cbb1f73f6a57f |
| artifacts/C/preliminary_RV_profile_v1_1/daily_profiles.npz | 2aa2554accde6cfeaadeb5b539b52931f76c1470cdb3a435eefef2e804de0c27 |


The v1.1 §11 change log retires a redundant C0/P0, preserves full-C MID/CLOSE windows, and labels the post-P0 15:00–15:30 window exploratory. Historical P0's narrower windows and WEAK scientific verdict remain intact. v1.1 §4 and the current request control reserved-date access; original v1.0 §4.1's broader statement that B's test segment had been examined is not permission to open it. B's actual closeout identifies 2022–2023 developmental return work and a reserved 2024–September 2026 segment. No claim of globally virgin dates is made.

## Correct source and response

The reference graph is:

```text
B_alpaca_sip_SPY_1m_split_D2_v1 (91 selected minute starts/day)
    + C_spy_1m_p0_v1_1_missing_keys (72 disjoint monthly partitions)
    -> transient full-session source view (keys checked, prices spot-checked)
    -> existing preliminary_RV_profile_v1_1/daily_profiles.npz
```

The B daily return table and its 39-row Hugging Face repair overlay do not enter this graph. No alternative feed was joined. Source files were verified against the original P0 registry/config/source manifest: **6 annual B references + 72 C supplements**, plus the existing derived NPZ. All 79 file size/hash identities pass. The supplement remains **10,318,012 bytes**, 448,173 rows; 136,337 reused D2 rows yield 584,510 distinct source keys. Full key/time-grid checks on the development sources find zero within-source duplicates and zero D2/supplement overlaps. Overlap would fail the join. Saved P0 acquisition overlap OHLC comparisons reported zero discrepancies; no new acquisition comparison was attempted.

Provider Alpaca SIP, SPY, 1Min, split-only prices; UTC minute-start timestamps, DST-aware America/New_York sessions under XNYS. Base sources additionally contain trade-count/VWAP/role metadata; supplement columns are symbol, timestamp_utc, session_et, open/high/low/close/volume. The NPZ contains 1,511 scheduled slots (including auxiliary 2016-01-04), `rv,q` 1,511×78, remaining 1,511×72, scalar RV/state arrays and retrospective labels. Its content hash is recorded above. This is one retained Q product, referenced without a new copy.

For an ordinary complete day: r0=log(C09:30/O09:30); subsequent rj=log(Cj/Cj−1), j=1…389. Every increment belongs to exactly one of 78 groups of five. v is the sum of squared minute logs; R=sum(v)>0; Q=v/R. There is no overnight term, missing-bar fill, half-day placeholder or dividend total-return substitution. All 1,491 main complete profiles pass nonnegativity, finite positive R, rv/R consistency and closure; max |sum(Q)−1| = **5.55e-16**. The unit is a full SPY session, not 78 independent observations.

**Actual main dates: 2016-01-05–2021-12-31. Q/OPEN: 1,491; strict PREV/Z0: 1,472; Zchg: 1,454.** These match historical QA. Twelve early closes and seven incomplete ordinary days remain excluded. Missing dates/minutes: 2016-02-02/9; 2019-08-12/30; 2020-03-09/14; 2020-03-12/14; 2020-03-16/14; 2020-03-18/14; 2021-05-05/5: total 100. Four March 2020 crisis exclusions limit stress-period generalization; their cause is not established. The exact early-close list is in `source_identity_qa.json` and the unchanged P0 exclusions CSV.

Six predetermined chronological checks independently use scalar logarithms and summation on original source references, comparing v, R, Q and all six window shares. RV tolerance is atol 1e−18 / rtol 1e−12; Q/windows atol 1e−10, rtol 0. All pass. Price identity uses exact source-file hashes; no cross-vendor price tolerance or fabricated price agreement is claimed.

| Calendar-selected date | Rows | max absolute Q error | R absolute error |
|---|---|---|---|
| 2016-01-05 | 390 | 1.39e-17 | 1.36e-20 |
| 2018-01-02 | 390 | 1.39e-17 | 0 |
| 2019-01-02 | 390 | 6.94e-18 | 0 |
| 2019-03-11 | 390 | 1.39e-17 | 3.39e-21 |
| 2020-01-02 | 390 | 2.78e-17 | 0 |
| 2021-01-04 | 390 | 1.39e-17 | 1.36e-20 |


The six immutable half-open windows are OPEN30 [0:6], MID_C [24:48], CLOSE_C [66:78], MID_P0 [30:42], CLOSE_P0 [72:78], PRE_CLOSE_DIAG [66:72]. CLOSE_C/MID_C are full-C primary, P0 windows secondary, and PRE_CLOSE_DIAG post-P0 exploratory. A share is a daily Q sum. R1 remains **SOURCE_INSPIRED_PROXY**: SPY/lagged RV/minute-square allocation differ from E-mini/open VIX/latent periodicity. This audit supplies no new effect estimate, significance, materiality or forecasting result.

## Future physical coverage and access

The C specs require chronological fractions after full-C eligibility but do not explicitly fix exact full-C start/end dates. The **proposed feasibility horizon** here follows the actual local D2 span, 2016-01-05–2026-09-30; it is not an approved full-C analysis horizon. The 2016 source count below includes the valid auxiliary January 4 profile, while the Q count excludes it.

| Year | Ordinary / early close | Full local coverage | Q / Z0 verified | Missing full-day coverage |
|---|---|---|---|---|
| 2016 | 251 / 1 | 250 | 249 / 247 | 1 |
| 2017 | 249 / 2 | 249 | 249 / 247 | 0 |
| 2018 | 248 / 3 | 248 | 248 / 245 | 0 |
| 2019 | 249 / 3 | 248 | 248 / 244 | 1 |
| 2020 | 251 / 2 | 247 | 247 / 241 | 4 |
| 2021 | 251 / 1 | 250 | 250 / 248 | 1 |
| 2022 | 250 / 1 | 0 | UNVERIFIED | 250 |
| 2023 | 248 / 2 | 0 | UNVERIFIED | 248 |
| 2024 | 249 / 3 | 4 | UNVERIFIED | 245 |
| 2025 | 247 / 3 | 0 | UNVERIFIED | 247 |
| 2026 | 187 / 0 | 6 | UNVERIFIED | 181 |


Later D2 annual files physically retain only 09:30–09:59, 14:59, and 15:00–15:59 starts. Historical D2 QA audited full vendor replies before discarding other minutes; its old full-day completeness numbers do not mean those 390 prices are retained. Existing D1 pilot metadata separately reports ten complete ordinary sessions: 2024-03-08, 2024-03-11, 2024-11-27, 2024-12-02, and 2026-09-14/15/16/17/18/21. Their prices were not read, hashes were not recomputed, and they are **not admitted** into the C/P0 union. Combining D1 and D2 would need an explicit source-version/overlap decision. Metadata evidence is a coverage aid, not validated C numeric eligibility.

`coverage_by_period.csv` records each year and references; `future_session_coverage.csv` records all **1,181 ordinary future dates**, immediate scheduled predecessor/ordinary flags, physical coverage and withheld status. Of these, 1,171 lack full local source coverage even crediting D1's ten manifest-reported days. Without admitting D1, plan for **all 1,181** days. In both cases the 57 monthly periods 2022-01…2026-09 need source planning. 2023-06-05 also has a four-minute original D2 gap. Its old B alternative repair is excluded from C. All future target/RV/predecessor numeric validity remains **FUTURE_ELIGIBILITY_METADATA_UNKNOWN**. No future Q, R, return, CLOSE_C or state was read or calculated.

Prospective acquisition proposal, **NOT AUTHORIZED / zero bytes spent**: if the user approves the horizon and source, query existing-account Alpaca SIP split SPY 1Min in those 57 months, with a conservative request for **150,000,000 cumulative response-body bytes** including retries (stop before the cap), and **15,000,000 retained supplemental bytes**. Scaling the actual P0 response/retention per ordinary day to 1,171 gaps gives about **93,488,892 transferred / 8,060,304 retained bytes**; excluding D1 credit increases the point estimate to ~94.3 MB / 8.13 MB for 1,181 days. These estimates include P0-style extended-hours response overhead and are not a promise of current entitlement, missing-bar repair, identical provider revisions or licensing. Entitlement/terms must be checked in the separately approved acquisition stage. Reuse D2 only after snapshot overlap QA; retain only missing keys. Fetching future source and deriving future C science require distinct approval gates. Do not use this proposal as permission, and do not reuse P0's historic 1 GB ceiling.

Z0 needs the immediate scheduled predecessor, Zchg its predecessor as well. Half-day predecessors remain invalid for primary Z0 even if a 15:59 anchor exists elsewhere. A later Jan 2022 state may legitimately use Dec 2021 only in an approved later stage; this audit created no 2022 state/lookback. Volume would need 20 older admissible sessions under an approved rule, not a silent cross-boundary lookup.

## State readiness

| State | Availability / prepared dates | Information time / mode | Minimum outstanding requirement |
|---|---|---|---|
| Z0 | AVAILABLE_VERIFIED; 1472 | before date_et 09:30 ET; <bound method Series.mode of state                                                                  Z0
availability                                           AVAILABLE_VERIFIED
prepared_valid_dates                                                 1472
information_time                                  before date_et 09:30 ET
mode                                                            F_ALLOWED
minimum_needed          Existing P0 RV_prev with strict calendar mappi...
Name: 0, dtype: object> | Existing P0 RV_prev with strict calendar mapping; log stored once here |
| S0 | PARTIAL_TRANSFORM_VERIFIED_CUTS_UNFITTED; 0 | before date_et 09:30 ET; <bound method Series.mode of state                                                                  S0
availability                     PARTIAL_TRANSFORM_VERIFIED_CUTS_UNFITTED
prepared_valid_dates                                                    0
information_time                                  before date_et 09:30 ET
mode                                                            F_ALLOWED
minimum_needed          Approved training date cohort, then fit two Z0...
Name: 1, dtype: object> | Approved training date cohort, then fit two Z0 quantiles; no new source |
| Zret | BLOCKED_DEFINITION; 0 | before open; previous completed closes only; <bound method Series.mode of state                                                                Zret
availability                                           BLOCKED_DEFINITION
prepared_valid_dates                                                    0
information_time              before open; previous completed closes only
mode                                              F_ALLOWED_WHEN_VERIFIED
minimum_needed          Approved previous-two-close anchor and early-c...
Name: 2, dtype: object> | Approved previous-two-close anchor and early-close/missing policy; matching existing split-only closes |
| Zchg | AVAILABLE_VERIFIED_WITH_PER_STATE_MASK; 1454 | before open; <bound method Series.mode of state                                                              Zchg
availability                     AVAILABLE_VERIFIED_WITH_PER_STATE_MASK
prepared_valid_dates                                               1454
information_time                                            before open
mode                                                          F_ALLOWED
minimum_needed          Two immediate prior valid ordinary P0 RV values
Name: 3, dtype: object> | Two immediate prior valid ordinary P0 RV values |
| Zvol | BLOCKED_DEFINITION; 0 | before open; <bound method Series.mode of state                                                                Zvol
availability                                           BLOCKED_DEFINITION
prepared_valid_dates                                                    0
information_time                                              before open
mode                                              F_ALLOWED_WHEN_VERIFIED
minimum_needed          Approved older-eligible vs strict-chain policy...
Name: 4, dtype: object> | Approved older-eligible vs strict-chain policy, epsilon, split-volume units/revisions and complete historical volume totals |
| ZV | ABSENT; 0 | published previous close as-of audit required; <bound method Series.mode of state                                                                  ZV
availability                                                       ABSENT
prepared_valid_dates                                                    0
information_time            published previous close as-of audit required
mode                                              F_ALLOWED_WHEN_VERIFIED
minimum_needed          Authorized daily VIX source, previous-close as...
Name: 5, dtype: object> | Authorized daily VIX source, previous-close as-of timestamps/calendar |
| Zopen | ABSENT; 0 | no later than 09:30 ET; <bound method Series.mode of state                                                               Zopen
availability                                                       ABSENT
prepared_valid_dates                                                    0
information_time                                   no later than 09:30 ET
mode                                              F_ALLOWED_WHEN_VERIFIED
minimum_needed          Authorized timestamped VIX observations availa...
Name: 6, dtype: object> | Authorized timestamped VIX observations available by 09:30 ET |
| Zfomc | ABSENT; 0 | known schedule before open; <bound method Series.mode of state                                                               Zfomc
availability                                                       ABSENT
prepared_valid_dates                                                    0
information_time                               known schedule before open
mode                                              F_ALLOWED_WHEN_VERIFIED
minimum_needed          Authentic dated historical announcement schedu...
Name: 7, dtype: object> | Authentic dated historical announcement schedule with release time and emergency flags |
| ZopenRV | AVAILABLE_VERIFIED_P0; 1491 | 10:00 ET; <bound method Series.mode of state                                                            ZopenRV
availability                                       AVAILABLE_VERIFIED_P0
prepared_valid_dates                                                1491
information_time                                                10:00 ET
mode                                                 D_ONLY_FOR_FULL_DAY
minimum_needed          Existing P0 RV_open; D only for full-day profile
Name: 8, dtype: object> | Existing P0 RV_open; D only for full-day profile |
| Zd | AVAILABLE_VERIFIED_P0; 1491 | after close; <bound method Series.mode of state                                           Zd
availability                 AVAILABLE_VERIFIED_P0
prepared_valid_dates                          1491
information_time                       after close
mode                                        D_ONLY
minimum_needed          Existing P0 RV_day; D only
Name: 9, dtype: object> | Existing P0 RV_day; D only |
| Vsame | PARTIAL_SOURCE_COLUMNS_ONLY; 0 | after close; <bound method Series.mode of state                                                       Vsame
availability                          PARTIAL_SOURCE_COLUMNS_ONLY
prepared_valid_dates                                            0
information_time                                      after close
mode                                                       D_ONLY
minimum_needed          Source volume totals not prepared; D only
Name: 10, dtype: object> | Source volume totals not prepared; D only |


One ignored shared keyed numeric lookup is `data/derived/C/c_development_states_v1_1.parquet`; it contains only 1,491 existing P0 profile dates, Z0/Zchg, predecessor dates, reason masks and provenance/information-time labels. No Q/windows are duplicated. Publicly reviewable `development_state_availability.csv` omits the numeric state values and retains masks, reasons and keys. Optional states never remove primary Q dates: use per-state masks. The 19 Z0 failures cannot skip to older sessions; the extra two-prior failures remain explicit. Existing P0 RV_prev matches exp(Z0) to atol 1e−18/rtol 1e−12.

P0 rank labels were independently reconstructed on their **whole P0 branch cohorts**; they are D-only. The new S0 function fits only provided dated training Z0, uses linear 1/3 and 2/3 quantiles, assigns boundary ties upward and missing states −1, and applies saved cutpoints unchanged. Synthetic tests pass; **no real S0 cutpoints were fitted**. This reusable transform does not settle the official cohort or imply balanced validation groups.

Zret remains unresolved because v1.0 §3.2 says previous regular-session closes while v1.1 §3.2 refers to previous full-session closes/two relevant full-session anchors. Lawful alternatives are immediate scheduled closes including early-close sessions when truly available, or consecutive valid ordinary full-session anchors with gaps masked. Do not substitute RTH open-to-close or silently skip missing anchors. Zvol explicitly mentions older eligible complete sessions but also scheduled-looking d−21:d−2 notation, and no epsilon or volume revision audit is frozen. Proposed policy: require immediate p(d) complete, then use its 20 older complete eligible sessions strictly before p(d), with a documented guard; alternative: strict scheduled chain with any invalid slot blocking. Neither was selected here. No associated response means or predictor search was performed. No VIX/FOMC files were found locally by filename inventory; absence is scoped to this repository.

## Split and exposure ledger

v1.1 §4 says “chronologically ordered eligible full days”; original v1.0 §4.1 says “first 60% eligible days”. Neither explicitly resolves all-Q-first/mask-later versus Z0-modeling-first. **SPLIT_POPULATION_POLICY is PENDING_APPROVAL.** Recommend Z0_ELIGIBLE for primary F matched comparisons, while recording Q coverage separately. This recommendation is not a frozen scientific decision.

| Illustration ONLY | N | 60 / 20 / remainder sizes | Train end | Validation start / end | Illustrative evaluation start | Z0 matched sizes |
|---|---|---|---|---|---|---|
| Q_ELIGIBLE_THEN_MASK_Z0 | 1491 | [894, 298, 299] | 2019-08-05 | ['2019-08-06', '2020-10-19'] | 2020-10-20 | [886, 291, 295] |
| Z0_ELIGIBLE | 1472 | [883, 294, 295] | 2019-07-31 | ['2019-08-01', '2020-10-19'] | 2020-10-20 | [883, 294, 295] |


Every table entry above is **ILLUSTRATIVE_NOT_FULL_C**, on entirely explored P0 data. Q-first produces 894/298/299 calendar rows and 886/291/295 matched Z0 rows; Z0-first produces 883/294/295. The training cutoff shifts from 2019-08-05 to 2019-07-31, illustrating why the choice matters. None of these are official held-out splits. All exact full-C cutoff fields remain null. The CLI sorts unique ISO date keys, uses integer 3N//5 and 4N//5 (mathematically floor 0.6N/0.8N), reports hashes/sizes/ranges and refuses every freeze request in C1R.

Exposure: all 2016–2021 Q and both window sets were viewed in P0; some B signed-return studies examined 2022–2023; 2024–September 2026 remains reserved under B's protocol. A new chronological label cannot make old records blind. No evaluation is released by this audit. Final C evaluation requires explicit approval plus frozen dataset/cohort, shortlist, selection route, cutpoints and tests.

## Draft protocol and next gate

`config/C_full_protocol_v1_1.yaml` is a **YAML 1.2 JSON-syntax draft**, parsable with the standard library; no new YAML dependency was added. Status DRAFT_PENDING_COVERAGE_AND_RELEASE, locked=false, evaluation NOT_AUTHORIZED, models NOT_FITTED, grid NOT_FROZEN_YET. It records the authority/source hashes, mathematical response, six windows, states/timing, D/F separation, H1–H5/RQ1–RQ5, stage ladder and explicit pending fields. It preserves the 0.02 closing/opening and 0.05 global/environment-TV references. P0 does not establish an effect exceeding 2 pp.

C2R is planned for direct science and M0/M1/M2/M4 only after its own instruction and stage-specific freeze. C3 adds M3/M5/M6/M8 with ≤2 predeclared EBM settings and ≤3 shortlisted seeds; C4 M7/M9/M10 is conditional; C5 handles inference/fidelity/environment; C6 is released once only. No InterpretML hyperparameters are invented here. Distinct-date support gates 30/10, 50/20, 100/30 dates/five-session groups are operational planning thresholds, not theorem validity. Later 5/10/20-day block sensitivity and ≥1,000 descriptive draws are plans only. All native-vs-raw theorem correspondence is deferred, not presumed by software output.

Required decisions, only before the dependent work:

1. Which full-C date horizon and split population are approved: Q-first/mask-later or Z0-first (recommended for primary F)?
2. Which Zret close-anchor/early-close policy should govern H2? Which Zvol lookback/epsilon and volume provenance policy should govern its later extension?
3. If later data are wanted, is the separately bounded SPY acquisition plan approved? Evaluation still needs a separate explicit release and final freeze.

These do not block Z0-only descriptive development on the verified explored cohort. **Recommendation: permit a separately scoped development-only C2R for Z0 H1/H3 and simple baselines; hold H2, Zvol, full-horizon forecasting/evaluation and acquisition until their gates are settled.** This is a readiness recommendation, not execution of C2R or a C2R prompt.

## QA, resources and reproducibility

The final source audit and focused suite are documented in `C1R_execution_QA.json`; `source_identity_qa.json` is the reference registry and exact read ledger. Twelve tests pass: four new C1R tests and eight unchanged P0 tests. Existing tests run tiny synthetic bootstrap fixtures only; no empirical P0 bootstrap, plot, source extraction or scientific model was rerun. Final audit validates the 2016–2021 keys/grids/identity, scalar spots and saved arrays; it does not revalidate every raw OHLC value or independently reproduce historical inference. Later science values remain withheld. Protected-file baseline checks and Git diff/whitespace checks are recorded in execution QA and the dated session report.

Early execution errors were a missing optional pytest package and two NumPy-string compatibility issues, all resolved without adding dependencies or changing data/science. Use unittest, built-in min/max on string arrays and Python str at calendar boundaries. PyArrow emits sandbox sysctl CPU-cache capability warnings; successful reads and checks are unaffected. These are engineering diagnostics, not failed scientific invariants. No source identity or mathematical QA mismatch occurred.

```sh
python -m venv .venv
# Activate the environment using your platform's normal command.
python -m pip install -e .
python -B -m unittest discover -s tests -p 'test_c*.py' -v
python -B scripts/c1r_readiness.py audit
python -B scripts/c1r_readiness.py split --eligible-manifest APPROVED_DATE_ONLY_MANIFEST.json
```

The existing environment also provides pandas/NumPy; exact installed versions are in `environment_versions.json` (Python 3.14.6, NumPy 2.5.4, pandas 3.0.6, PyArrow 23.0.1, exchange-calendars 4.13.2). For exact reproduction match those versions. On a fresh clone, restore **authorized** matching-hash P0 NPZ and 78 source references using the original source manifest; set EBM_DATA_ROOT if inputs live outside `data/`. No source credentials are needed for this local audit. The clone does not ship licensed data, and C1R must not call a historic acquisition command to fill a missing cache. Missing inputs or hash changes stop the audit.

New material is small text/metadata plus one compact numeric state table, below 50 MB; exact final bytes and the detailed created/inspected inventory are in the session report/execution QA. Zero source network bytes, zero raw copies, zero duplicated Q products, no model artifacts/figures. Existing source and P0/B files are unchanged. Future resource estimates are planning only. Read this report and the candidate protocol first at handoff, then the original authority/P0 manifests; the next authorized stage has not begun.
