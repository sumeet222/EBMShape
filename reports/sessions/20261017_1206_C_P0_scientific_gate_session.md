# Experiment C P0 - scientific gate checkpoint

## 1. Session identity and verdict

Session `20261017_1206_C_P0_scientific_gate_session`, 17 October2026, America/New_York / EDT (UTC-04:00). Agent: Codex/GPT-6 family; exact serving revision not exposed. Active task `C-P0-RV-PROFILE-v1.1`, from user attachment ending `21051240-fdc9-4eb4-bfed-a332b2d9a9cd/Pasted text.txt`.

**Implementation status: BLOCKED_SCIENTIFIC_DECISION; draft preparation only.** Six independent numerical/calendar tests pass. No full P0 scientific result, QA verdict, GO/WEAK/NO_GO recommendation, real-data profile or figure exists. Acquisition has not started; downloaded response bytes0. The1GB download permission is recognized and does not need reconfirmation.

The new C specification was initially absent in `docs/`/`ResearchSpec/`, then appeared before protocol freeze alongside its transition prompt. The draft freeze function correctly refused to continue under C_SPEC_NOT_ACCESSIBLE. Reading the actual specification revealed different MID/CLOSE scientific windows from the handoff. The user attachment explicitly requires stopping and asking on scientific conflict; the asynchronous user question remains pending. No scientific approval inferred from silence.

Start/end branch `main`; HEAD `8683ee30ff3edb62f89f9c58e8a68496e61431f3`. Initially dirty/untracked: previous PDF directory `artifacts/figures/`, its exporter `scripts/export_visual_gallery_pdf.py`, and PDF session report `reports/sessions/20261016_1953_B_visual_gallery_pdf_session.md`. Preserved. The two C-spec files appeared as additional user-owned untracked files during the task, not files created by this agent. No Git stage/commit/push/reset occurred. Existing B scientific outputs and sealed data were not modified.

## 2. Exact inventory

| Action | Repository-relative path | Why / changed contents | Consumers | Recovery |
| --- | --- | --- | --- | --- |
| CREATED | `src/ebm_research/experiment_c/__init__.py` | C package marker | Draft C module | Retain for continuation |
| CREATED | `src/ebm_research/experiment_c/preliminary.py` | Draft source client, guarded freeze/acquire/check CLI, independent RV/grid/group/bootstrap kernels | Thin CLI/tests; **not a finished pipeline** | Reconcile spec/windows before approving freeze/acquire; implement remaining analysis/reporting |
| CREATED | `scripts/c_preliminary_RV_profile.py` | Thin entry point | `check`, guarded `freeze`/`acquire` | No duplicated scientific computation |
| CREATED | `tests/test_c_preliminary_RV_profile.py` | Six focused deterministic tests, no network mocks or predictive fits | unittest | Re-run command below |
| CREATED | `artifacts/C/preliminary_RV_profile_v1_1/scientific_conflict_gate.json` | Explicit pending definitions, source status, spec hashes, clock, byte count0 | Handoff/resume | Preserve as checkpoint; do not report a scientific PASS |
| CREATED | `artifacts/C/preliminary_RV_profile_v1_1/download_budget.jsonl` | Empty ledger,0requests/0response bytes | Future cumulative transfer accounting | Append every actual future response/retry; never reset to hide transfers |
| CREATED | `artifacts/C/preliminary_RV_profile_v1_1/gate_tests.log` | Final six-test stdout/stderr | Test evidence | Unit command below |
| CREATED | `reports/C/C_P0_scientific_conflict.md` | Exact scientific mismatch and pending choices | User/design review | Read before resuming |
| CREATED | `reports/sessions/20261017_1206_C_P0_scientific_gate_session.md` | This mandatory session record | Audit/handoff | Preserve |
| INSPECTED, UNCHANGED | `AGENTS.md`, `.gitignore`, `docs/canonical_data_layout.md`, `.env.example` | Project instructions, portable source retention, credential names only | Draft design | No root configuration changes |
| INSPECTED, UNCHANGED | User attachment, both newly appeared `docs/specs/experiment_C_*_v1.md` documents | Binding C definitions and conflict rule | Scientific gate | These are user source files; never overwrite |
| INSPECTED, UNCHANGED | `data/registry/D2_spy_source_manifest.json`, `D2_1c_hf_repair_manifest.json`, `D1_spy_source_manifest.json`; `config/D2_spy_source.json`; prior D1 report | Source provenance/retention/time-label evidence | Coverage/source planning | No HF overlay acquisition or B patch use |
| INSPECTED, UNCHANGED | `src/ebm_research/experiment_b/pilot.py`, `scripts/d0_probe.py` | Existing calendar/hash/credential conventions | Reused functions, not old unbounded HTTP client | B source untouched |
| INSPECTED, UNCHANGED | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year=2016.parquet` | Project session/timestamp only: observed max91rows/day | Local coverage gate | No scientific Y/RV computation |
| INSPECTED, UNCHANGED | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet` | Date-predicated session-key read before2022:0rows | Local coverage gate | No2022–2026scientific fields read |
| INSPECTED, HASH ONLY | D2 `year=2016.parquet` through `year=2021.parquet` | Verify six immutable refs during aborted freeze before C-spec guard | Source preparation | Hashes matched; no transformations or copies |

No deleted/moved files, downloaded bodies, raw-cache partitions, normalized arrays, plots or generated temporary dataset. No config/C protocol, copied handoff, start snapshot or source manifest was written: freeze failed before those operations. The draft module contains code for these future operations, not proof they occurred. No source-cache directory was materialized.

## 3. Important functions / variables

All functions below are in `src/ebm_research/experiment_c/preliminary.py`, unless noted.

| Function / signature | Purpose, I/O and algorithm | Timing / callers / limitations |
| --- | --- | --- |
| `local_env()` / `data_root()` | Read established key names locally, resolve EBM_DATA_ROOT/defaultdata | Values never printed; no account entitlement claim |
| `freeze(handoff)` | Verify old source refs, search actual C spec, then planned protocol/snapshot | **Actual call raised C_SPEC_FOUND before writes**; fallback branch must be reconciled, not bypassed |
| `BudgetClient.__init__(p)` | Planned cumulative-ledger client; existing Alpaca credentials | Not invoked; credentials/entitlements not authenticated |
| `BudgetClient.body(response,limit)` | Bounded streamed chunks, Content-Length precheck, reject partial response at cap | Not yet tested against live source; not a completed budget QA claim |
| `BudgetClient.get(params,tag)` | Planned endpoint request, count error/retry bodies, sanitized JSONL ledger, capped backoff | Not invoked; no requests/keys logged; exception on entitlement or size failure |
| `source_frame(data,p,year)` | Verify/read explicit2016–2021 B columns only | Draft acquisition helper, not invoked |
| `acquire()` | Planned monthly SPY SIP/split pagination, overlap OHLC equality, retain only missing keys | Not invoked; no cache/supplement exists; no fallback/public source attempt needed before scientific decision |
| `profile_day(frame,day,cal)` | Exact390minute grid; first log(C0930/O0930),389adjacent closes; reshape78×5 and sum squares | Synthetic tests only; rejects half/missing/duplicate/out-of-order/end-label/invalid/zero-RV days; no overnight/fill |
| `rank_groups(values,dates)` | Stable(value,date) sorting; floor(3rank/N), independent three groups | Synthetic ties tested; records split ties and boundaries; no actual state labels formed |
| `strict_previous(dates,rv_day,cal)` | Immediate prior scheduled exchange date lookup; unavailable prior staysNaN | Half-day predecessor test; does not use B prior_full helper or leap backwards |
| `block_indices(n,length,rng)` | Joint circular consecutive trading-date-slot indices | Tiny fixture tests5/10length, seed42; no actual1000-draw run |
| `bootstrap_means(q,labels,indices)` | Shared-date sampled group means across all78bins | Labels fixed; invalid label-1excluded, no per-bin/group shuffling; synthetic fixture only |
| `main()` | CLI `check`, `freeze --handoff PATH`, `acquire` | Check reports scientific pending; no approved config means acquire refuses |
| `tests:synthetic()` / `CProfileTests` |390bar deterministic fixture and six tests | Existing dependencies; no elaborate framework |

Critical names: `OUT` → `artifacts/C/preliminary_RV_profile_v1_1`; `CONFIG` → **unwritten** `config/C_preliminary_RV_profile_v1.json`; `WINDOWS` → draft P0 mapping OPEN0:6/MID30:42/CLOSE72:78, **pending explicit decision**, not an approved frozen protocol; `ET/UTC` imported from existing calendar helper; `COLORS/NAMES` planned consistent state display. In the unreachable fallback freeze draft: provisional2016-01-05–2021-12-31, source auxiliary start2016-01-04, SPY/SIP/1Min/split, decimal cap1e9, request bound8e6bytes, limit10000rows, two retries,30second timeout, fixed seed42/B1000/blocks5and10, top_fraction.01. These choices are not reported as executed or finally approved. No C forecasting split or model declaration exists.

## 4. Execution trail and reproduction

Working directory: repo root. Existing `.venv` Python3.14.6 / NumPy / pandas / PyArrow / exchange-calendars used. No dependency installation or environment change in this session. No network APIs reached.

Commands/operations, in order (repeated narrow read-only variants grouped):

1. `cat '<user attachment>/Pasted text.txt'`; `git status --short; git branch --show-current; git rev-parse HEAD; cat AGENTS.md`. Long combined displays truncated; narrower reads followed.
2. `sed -n '105,240p' '<attachment>'`; repository `rg --files --hidden` filtering C/spec/source names; `.gitignore`; pilot source reads. Initial recursive C-spec search returned nofiles.
3. `sed -n '65,110p' '<attachment>'`; inventory parquet/metadata paths underdata/ResearchSpec/docs; read source registration/layout and existing bounded-client functions. No whole multiyear dataset loaded to countdates.
4. Narrow `sed` reads of `pilot.credentials`, `Client`, existing `.env.example` names and D0 credential parser. InlinePython lists local Parquet file paths/sizes, reads D2 metadata, and reports free disk65,945,600,000bytes. No secrets printed.
5. InlinePython D1 date-only predicate `<2022-01-01` →0rows; D2year2016 `session_et,timestamp_utc` projection →max91rows/session. Optional local environment values were read by `data_root()` but not printed.
6. `apply_patch` created draft C module/package and thin CLI.
7. `.venv/bin/python -B -c 'from ebm_research.experiment_c.preliminary import freeze; freeze("<user attachment>/Pasted text.txt")'` → **exit1,C_SPEC_FOUND**, six old-source refs hash verified before guard. No protocol/source/API writes.
8. `rg --files docs ResearchSpec` Cfilter and `cat` actual Cspec; narrow `sed -n '148,220p'` and transition prompt reads. User-owned newCspec/transition files now present. §2.1 window mismatch identified; no numerical result yet.
9. Asynchronous user-question tool requests P0-vs-Cspec window decision, offering explicit supplementary/exception options. Permission for1GB is not questioned.
10. Add six independent mathematical/calendar tests; `.venv/bin/python -B -m unittest discover -s tests -p 'test_c_preliminary_RV_profile.py' -v` → **exit0,6PASS,0.196s test-body**, approximately1.60s process wall.
11. Add guarded `main()`; inlinePython write machine scientific gate and empty download ledger; `.venv/bin/python -B scripts/c_preliminary_RV_profile.py check` →exit0,SCIENTIFIC_DECISION_PENDING,0networkbytes.
12. `.venv/bin/python -B -m unittest discover -s tests -p 'test_c_preliminary_RV_profile.py' -v > artifacts/C/preliminary_RV_profile_v1_1/gate_tests.log 2>&1`; `git diff --check`; ending status. All pass. Write these reports and final small whitespace/Git/storage checks.

Small reproducible current check:

```text
python -B scripts/c_preliminary_RV_profile.py check
python -B -m unittest discover -s tests -p test_c_preliminary_RV_profile.py -v
```

No provider credentials are needed to reproduce these synthetic tests. Full P0 reproduction is not available yet: first resolve scientific windows, record actual specification/hash and the approved P0 deviation, then implement remaining acquisition/analysis. Matching B canonical source refs and working APCA credentials will be needed for the preferred source path. A public clone does not contain licensed minutes.

## 5. QA and scientific integrity

Six tests pass: known390log returns with distinct values, all78five-term sums and total;09:34/09:35 and15:54/15:55 attribution; DST/holiday/half-day calendar; missing/duplicate/reversed/end-labelled grid; invalidprice and zeroRVDAY; strict preceding exchange date including intervening halfday; stable tie-group ranks; reproducible joint5/10date-block fixture. Multiple invariants are covered by individual tests, not an inflated test-count target. No actual bootstrap CI, empirical normalization/plot reconciliation or image QA was performed because scientific computation is pending.

The current graph formulas and390term convention agree with both supplied sources. Scientific mismatch is **window-share target**, not a source entitlement/data defect. The full Cspec future60/20/20 heldout allocation and materiality conventions must not be silently transplanted into or erased by P0; no final split or evaluation was created. Existing B sealed2024–2026scientific fields were not read. Only source file names/hash metadata and pre2022date predicates were used; no B forecasts or outcome tables loaded. A/B populations/targets unchanged. No source fidelity, original VIX replication, descriptive GO/NO_GO or no-effect claim is made.

## 6. Errors / decisions / recovery

| Event | Cause / response | Status / next action |
| --- | --- | --- |
| Long orientation displays truncated | Tool-output budget | Used targeted reads; no fake claim of missing text |
| Arrow sysctl hardware warnings during Parquet probes | Optional cache/NEON introspection denied in sandbox | Actual reads passed; no package/system change |
| Freeze C_SPEC_FOUND | Cspec appeared after initial search | Correct safety stop, not bypassed; no config/download written |
| Main windows differ | P0 MID12–13/CLOSE15:30–16; specMID11:30–13:30/CLOSE15–16 | **NEEDS SCIENTIFIC DECISION**, pending question; no approval inferred |

No entitlement test, HTTP failure, download retry, partial response, rejected real session or raw-cache write occurred. Prepared network functions remain unexercised and must not be treated as verified access. No C_SPEC_NOT_ACCESSIBLE report/config was emitted after the actual spec appeared. No after-results protocol change occurred: there are no scientific results.

Recovery: start at `reports/C/C_P0_scientific_conflict.md` and the actual Cspec §2.1. Record the user's explicit window decision before changing `WINDOWS` or continuing protocol freeze. Update the fallback-only freeze function to reference the real spec and approved exception/supplement; do not simply remove its guard and mislabel the spec missing. Finish authorized bounded acquisition,≥300day source gate, analysis,1000valid joint5/10block draws,12plots, numeric reconciliation and complete reports afterward. Current kernels/tests are trusted only within their small synthetic scope. No partial scientific artifact requires quarantine.

## 7. Resource / Git / handoff

Network response bodies **0bytes**; budget ledger empty and its meaning explicit. New retained material is small draft code/tests/gate/reports (tens of KB); no input dataset or duplicated source. No large CPU job; tests approximately0.2s body time each run, no1000bootstrap job. Initial free space65.95GB. Disk cap untouched, no background process or scheduled work. No dependencies added.

Git ending additions include this session's C files plus all preserved initial user/PDF/Cspec files. No tracked diff or commit; `git diff --check`passes. Original B source refs verified during gate. Agent edits only the newly created C paths inventoried above; the newly supplied Cspec and transition prompt are user artifacts, not agent-authored replacements.

Handoff: the transfer authorization is sufficient, and the missing390minute coverage is expected and solvable in scope. The sole current blocker is the explicitly escalated scientific window mismatch. After the user chooses, continue the same P0 objective end-to-end rather than restarting orientation, expanding to full C models, or asking again about the already authorized1GB. No plot/effect exists yet; no scientific conclusion should be quoted from this checkpoint.
