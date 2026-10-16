# Experiment B / D2 full acquisition — detailed coding-session audit

## 9.1 Session identification and verdict

Session **20261016_1349_B_D2_spy_full_acquisition_session**, completed report at **2026-10-16T14:10:04.900108-04:00**, America/New_York (EDT, UTC−04). Agent Codex; exact runtime model identifier not exposed. Task **B_D2_FULL_ALPACA_SIP_HISTORY_AND_CANDLE_QA** from attachment `8f9692cc-9e8e-4227-9783-1733fbbbb8e6/Pasted text.txt`. Scope B only; A remained on hold.

Starting and ending branch **main**, commit **79a7099573c595adfd93d0b0a34c230259ab6b01**. Starting `git status --short` empty (clean). Existing ignored .env, D0/D1 data, previous reports and dependency environment preserved. No commit/stage/push/reset/branch mutation, user-data deletion, subscription or account change.

**Implementation/QA gate: PASS WITH QUALIFICATIONS. Stage 1 is permitted as a separate future task using documented eligible days. Scientific effects: NOT EXECUTED.** Full requested-history network retrieval completed; exact gap/eligibility counts reconcile. No model, production return/RV table, relationship test, state quantile, sealed-outcome selection, trading, source-era backfill, new provider or A work.

Objective achieved: available 2016-01-04–2026-09-30 SPY/SIP/split history acquired and fully audited; one 91-window source frozen; annual resume/checksums and complete QA/gap/coverage registries; human report and portable restore documentation. Qualifications: 104 real absent candles, seven ineligible full days, unavailable optional leading anchor, strict half-day full-anchor rule, unknown causes of gaps, D1 price/count differences, actual split-event handling untested. No result was adjusted to manufacture suitability.

## 9.2 Exact file inventory

| Action | Repository-relative path | Why | What changed (functions/config/data/schema) | Critical dependencies/consumers | Recovery note |
|---|---|---|---|---|---|
| CREATED | `config/D2_spy_source.json` | D2 required implementation/evidence | Frozen operational source/dates/retention/calendar/rates/retries/splits/license/spec reference; 1,529 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `scripts/d2_spy_acquire.py` | D2 required implementation/evidence | Thin entry to installed B acquisition.main; 157 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `src/ebm_research/experiment_b/acquisition.py` | D2 required implementation/evidence | D2 runner, D1 transport/QA reuse, pagination, monthly audit, annual freeze/resume, quality publication; 31,622 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `tests/test_d2_acquisition.py` | D2 required implementation/evidence | Two focused tests: whole-day gap; hash/append-prefix/LF-CRLF/page conflict; 3,280 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_candle_gap_clusters.csv` | D2 required implementation/evidence | 9 maximal within-session absent runs, ET/UTC/endpoints/windows/reason; 1,611 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_candle_qa_sessions.csv` | D2 required implementation/evidence | 2,701 calendar-session QA rows; presence/validity/gaps/windows/eligibility/reasons; no returns/prices; 1,056,070 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_candle_qa_summary.json` | D2 required implementation/evidence | Actual global/time/window/stratum/gap/run/split totals and Stage 1 gate; 149,231 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_coverage_month.csv` | D2 required implementation/evidence | 129 month coverage rows; zero-loss months retained; 5,389 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_coverage_quarter.csv` | D2 required implementation/evidence | 43 quarter coverage rows; 2,082 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_coverage_year.csv` | D2 required implementation/evidence | 11 year coverage rows with real denominators; 706 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_exception_log.json` | D2 required implementation/evidence | One documented post-freeze operational resume correction; no provider failure or changed data; 706 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_invalid_candles.csv` | D2 required implementation/evidence | Header-only invalid/conflicting instant registry; zero real cases; 32 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_missing_candles.csv` | D2 required implementation/evidence | 104 absent minute starts, ET/UTC/windows/reason; 11,854 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/registry/D2_spy_source_manifest.json` | D2 required implementation/evidence | Dataset/provider/config/spec/code/versions/partition/QA/ledger identities, status and freeze/maintenance records; 13,550 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D2_v1/requests.json` | D2 required implementation/evidence | 271 sanitized request records, response hashes/bytes/status/time; no source bodies/headers; 162,322 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `reports/shared/D2_full_spy_sip_acquisition_and_candle_quality.md` | D2 required implementation/evidence | Full required human-readable coverage/gap/eligibility/provenance/resource/restore/gate report; 19,570 bytes before final note | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED | `reports/sessions/20261016_1349_B_D2_spy_full_acquisition_session.md` | D2 required implementation/evidence | This session inventory and reproduction/recovery trail; draft created during acquisition, completed now; completed Markdown report (self-size omitted) | CLI / QA / report / Stage 1 handoff | New session-owned file; metadata reproducible from verified checkpoints; licensed ledger stays ignored |
| CREATED (11 partitions) | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year={2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026}.parquet` | Sole full-history source | 243,804 rows x 12 columns, 8,975,163 bytes; every exact path/size/SHA-256/row count in D2 source manifest blocks | Scientific input availability; future Stage 1 | Ignored licensed data; preserve immutable checksums; restore authorized backup or new data root |
| CREATED (11 QA blocks) | `data/registry/D2_blocks/{2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026}.json` | Annual resume | 7,144,002 bytes total; per-session flags/counts/gaps plus batch retrieval details, no price rows; exact paths/hashes in manifest | Resume and consolidated QA | Reuse saved QA; no full-source re-scan for documentation |
| CREATED → MOVED (temporary group, 11) | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D2_v1/year=*.parquet.tmp` → matching `.parquet` | Atomic first writes | Generated intermediate renamed only after complete audit; no orphan left | partition_write | No user artifact moved; partial/orphan would block resume rather than overwrite |
| CREATED → MOVED (temporary metadata group) | `data/registry/D2_*.json.tmp`, `data/registry/D2_blocks/*.json.tmp`, `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D2_v1/requests.json.tmp` | Atomic generated metadata | Same final paths as inventory; ledger replaced per request; no temporary JSON retained | write_json | No original input overwritten; partial year stays unknown until registered |
| CREATED / AUTO-CLEANED (test group) | OS temporary `ebm_d1_smoke_*/smoke.parquet` (4 suite invocations), `ebm_d2_smoke_*/tiny.txt` (3 D2 suites), `ebm_d2_smoke_*/requests.json` (2 later suites) | Proportional tests | Tiny synthetic I/O/hash/prefix fixtures only | unittest | Automatically removed generated temp directories; no user file deletion |
| MODIFIED | `docs/data_source_registry.md` | Verified new D2 facts | Append actual D2 dates, source/coverage/gaps/eligible split counts/cost/limits; A on hold | Data users / next stage | Original version in starting Git commit; no scientific protocol changed |
| MODIFIED | `docs/canonical_data_layout.md` | Verified new D2 facts | Append authoritative D2 physical schema, retention, annual checkpoint/ledger/restore semantics; D1 diagnostic only | Data users / next stage | Original version in starting Git commit; no scientific protocol changed |
| MODIFIED | `data/README.md` | Verified new D2 facts | Add authoritative D2 status and portable dry-run/restore/resume/verify instructions; old D0/D1 historical text preserved | Data users / next stage | Original version in starting Git commit; no scientific protocol changed |
| INSPECTED | `AGENTS.md; README.md; .gitignore` | Authority, scope, storage/testing/safety/report rules and existing ignore protection | No change | D2 authority / reuse | Preserved |
| INSPECTED | `docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md` | Active B source/timing/state/date/gap/QA gates; no scientific redesign | No change | D2 authority / reuse | Preserved |
| INSPECTED | `docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md` | Stage discipline, portability and exception/reporting requirements | No change | D2 authority / reuse | Preserved |
| INSPECTED | `reports/shared/D0_data_source_feasibility.md; reports/shared/D1_spy_sip_pilot_and_candle_audit.md` | Prior sparse-access/pilot evidence, not full-history certification | No change | D2 authority / reuse | Preserved |
| INSPECTED | `reports/sessions/20261016_1245_B_D1_spy_sip_pilot_session.md` | Prior functions/config/commands/errors and qualified gate | No change | D2 authority / reuse | Preserved |
| INSPECTED | `data/registry/D1_spy_source_manifest.json; config/D1_spy_source.json` | D1 identity/mode/hash/operational precedent | No change | D2 authority / reuse | Preserved |
| INSPECTED | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet` | Actually present and SHA-256 verified; not copied/promoted/overwritten | No change | D2 authority / reuse | Preserved |
| INSPECTED | `src/ebm_research/experiment_b/pilot.py; scripts/d1_spy_pilot.py; tests/test_d1_candles.py` | Reuse calendar, transport, valid_bar, audit_session and gap/aggregate logic; D1 cap/code unchanged | No change | D2 authority / reuse | Preserved |
| INSPECTED | `pyproject.toml; requirements-d1.lock.txt; existing .venv` | Installed editable package/dependencies reused, no install/update | No change | D2 authority / reuse | Preserved |
| INSPECTED | `.env` | Names/presence only; private process-environment loader for authorized headers | No change | D2 authority / reuse | Preserved |
| INSPECTED | `user attachment 8f9692cc-9e8e-4227-9783-1733fbbbb8e6/Pasted text.txt` | Exact execution task, read only | No change | D2 authority / reuse | Preserved |

No original user artifacts were deleted, renamed or moved. Temporary renames above are only generated first-write intermediates. D1 safety code, source manifest, pilot and old reports are unchanged. New annual QA JSON and consolidated CSV duplicate only inexpensive **audit metadata**, not input candles; both are retained for safe resume and direct review. No full-day/raw JSON, second window store, copied folds/train/test files, model snapshot or scientific daily table exists. The original session draft was created while acquisition ran and completed in this same unique report, not substituted for a historical session.

Canonical shape/schema: **243,804 x 12**, 11 annual Parquets, **8,975,163 bytes**; `symbol:string`, `timestamp_utc:timestamp[us,UTC]`, `session_et:date32`, OHLC/volume/trade_count/vwap float64, `source_batch:string`, `role:string`. Native numeric scale retained without integer truncation. Explicit primary key `(symbol,timestamp_utc)` sorted/unique; zero source duplicates/conflicts. All paths/hashes/row counts are in source manifest, so ignored binary products are fully inventoried without pasting 11 long digests here.

## 9.3 Critical functions, classes and variables

New code is `src/ebm_research/experiment_b/acquisition.py`; the thin wrapper and two tests are the only other executable additions. Inputs never pool A/B populations. D1 helpers were imported unchanged rather than copying an acquisition/QA module or weakening its <=15-session limit.

| Function/class | Signature / CLI | Purpose; input → output | Algorithm, caller, timing and exceptions |
|---|---|---|---|
| `IntegrityError` | RuntimeError subclass | Explicit source/checkpoint/page conflict | Inspection required, never silent overwrite; tested with changed checkpoint/ledger/page overlap |
| `record` | `(bar,batch,role='required_window')` | Native SPY dict → canonical record | Genuine aware UTC start, ET date, source batch, float numeric scales; used only after whole-session QA |
| `from_record` | `(row)` | One verified canonical prior anchor → native bar form | Restore exact previous full close across annual resume; not a synthetic/default price |
| `verify_files` | `(data_root,references)` | Path/bytes/SHA refs → success or IntegrityError | Cheap immutable canonical/QA checkpoint verification; no row rescan |
| `file_ref` | `(path,data_root)` | Small file → portable relative path/bytes/SHA | Manifest/QA/ledger refs; no local absolute path committed |
| `verify_request_ledger` | `(data_root,manifest)` | Current JSON ledger + saved record count/hash → verified committed prefix | Appended incomplete-year requests allowed; changed/truncated committed prefix rejected; supports LF/CRLF writers; resume/verify-only caller |
| `HistoryClient.__init__` | `(raw_dir,config)` | D1 Client + existing ledger → bounded D2 client | Restores chronological lineage, no source-body cache |
| `HistoryClient.get` | `(name,endpoint,params,headers,retain=False)` | HTTP JSON or failure; append sanitized record | Reuses D1 byte/timeout/pacing/hash transport; no bodies retained; transient statuses/network errors get at most two retries, global cap6; entitlement failures stop; changed repeated incomplete-block body is flagged |
| `fetch_pages` | `(client,name,start,end,headers,timeframe='1Min')` | Explicit SPY/SIP/split interval → complete bar list | Inclusive endpoints, ascend/page boundary/token checks, max8 pages; malformed/overlap/cap raises IntegrityError, never converts API error to missing bars |
| `audit_day` | `(day,bars,prior_anchor,cal,config,daily_count)` | One complete retrieved regular session → QA row/gaps/absent/invalid instants | Calls D1 audit_session; adds exact session bounds, raw/field/count/retrieval/91-start/prior-span flags; absence vs invalidity separate; no imputation |
| `partition_write` | `(destination,rows)` | Audited retained windows → sole Zstd annual Parquet | Sort stable key, count/remove identical duplicates, reject conflicting duplicates/orphan/tmp; atomic first write; no existing source replacement |
| `coverage_rows` | `(rows,frequency)` | Actual QA rows → year/month/quarter denominator table | No unknown periods counted as candle loss; used in publish/reporting |
| `publish` | `(data_root,manifest,config,cal,all_days)` | Saved annual QA blocks → consolidated CSV/summary/gate | No source-data reread; unknown/uncommitted dates get null candle counts; exact cluster/stratum/window/run/split accounting and quality-only gate |
| `main` | `scripts/d2_spy_acquire.py --source-config ... --data-root ... --dry-run --max-years N --resume --verify-only` | Frozen config/environment → monthly retrieval, annual checkpoints, final freeze | Source/dates fixed; measured first year then verified resume; completed immutable blocks skipped; no stage1/models; zero-network verify-only |
| `scripts/d2_spy_acquire.py` | thin `main()` entry | Installed package invocation | No sys.path hack or duplicate pipeline |
| `D2Tests.test_successfully_empty_full_day_is_one_390_minute_gap` | unittest | Tiny complete-empty-response fixture → 390-minute single gap | Retrieval COMPLETE differs from unknown HTTP failure; exact ET first/last, missing-sum, primary invalidation |
| `D2Tests.test_resume_hash_conflict_and_page_overlap_abort` | unittest | Tiny temp files/JSON/two-page stub → integrity/resume assertions | Changed immutable hash, legitimate ledger append, changed prefix, LF/CRLF, overlapping page; no mock API platform |

Unchanged D1 critical callers reused: `calendar`, `grid`, `prior_full`, `timestamp`, `valid_bar`, `indexed`, `usable`, `audit_session`, `aggregate`, `window_flags`, `csv_write`, `write_json`, `credentials`, `Client`. No D1 `anchor_check` or production scientific-return/RV calculation was called on D2 data. D1's two focused calendar/missingness/math fixtures were reused.

Critical names/config values → file → meaning/units/default → consumers:

- `dataset_id=B_alpaca_sip_SPY_1m_split_D2_v1`, `task_id=B_D2_FULL_ALPACA_SIP_HISTORY_AND_CANDLE_QA` → D2 config → one full-history source/extract identity; main/manifest paths.
- `symbol=SPY`, `feed=sip`, `adjustment=split`, `timeframe=1Min` → config/each request → consolidated split-only minute source; no raw/dividend/all or feed merge. Daily diagnostics also explicitly SIP/split, timeframe1Day.
- `start=2016-01-04`, `end=2026-09-30` → config/guard → exact authorized inclusive modern-history scope. Optional prior full anchor only2015-12-31 15:59; unavailable, not fabricated.
- `calendar=XNYS`, `timezone=America/New_York`, `storage_timezone=UTC`, `bar_label=start` → config and D1 helpers → IANA-aware ET session grids and genuine UTC starts; side=left, early closes/holidays/DST handled by calendar.
- `retention.full_session=['09:30-09:59','14:59','15:00-15:59']`, `retention.early_close=none` → config → precisely91 full-session starts; audit every regular minute first. Initial anchor retained once only if it exists.
- `batch=calendar_month`, `checkpoint=calendar_year` → config → bounded memory, contiguous requests,11 immutable blocks. Monthly spans include known extended-hours rows, discarded by calendar before QA.
- `max_pages_per_request=8`, `request_spacing_seconds=0.5`, `retry_backoff_seconds=[5,15]`, `max_transient_retries_total=6` → config/client → modest request load; actual retries0. D1 inherited per-response cap2,000,000bytes, timeout30s, limit10000; no source JSON archive.
- `warn_retained_bytes=1,000,000,000`, `stop_retained_bytes=2,000,000,000` → config/resource gate → runner stops at unexpected1GB before2GB; actual source/QA17.53MB.
- `manual_extreme_range_fraction=0.05`, `manual_extreme_close_jump_fraction=0.05` → config/D1 audit → review flags only, fixed before data; no clipping/selection. All flags0.
- `opening_rv_loss_stop_fraction=0.02` → config/publish → strict >2% stop; actual train0.200535%, validation0.200803%, sealed0%, overall0.149421%. Separate all-full-day loss counts also reported.
- `splits.train=[2016-01-04,2021-12-31]`, `validation=[2022-01-01,2023-12-31]`, `sealed_test=[2024-01-01,2026-09-30]` → config → **quality-count masks only**, no copied data splits/threshold/model fitting.
- `SCHEMA` → acquisition module →12 canonical columns/types above; numeric float64 avoids fractional-volume truncation. `GAP_FIELDS`, `MISSING_FIELDS` define portable ET/UTC/reason CSV schemas.
- `identity.config_sha256`, `identity.scientific_spec_sha256` → manifest → source/config/spec bind, mismatches stop. Source has no immutable vendor revision ID, so request times/response hashes define snapshot provenance.
- `blocks`, `active_year`, `last_full_session`, `request_ledger`, `requests_total` → manifest → resume state; prior full anchor is read from last verified annual partition only; uncommitted year unknown, never a zero-bar day.
- `eligible_r1/r12/r13/rv/primary`, `has_all_91_required_window_starts`, `prior_full_anchor_elapsed_calendar_days`, `preceding_session_was_early_close` → QA rows → timing-safe input availability, not numerical scientific features. Missing ordinary full close has no older fallback; half-day skip is the explicitly approved separate rule.
- B v1 science unchanged: P10=C09:59, P15=C14:59, P1530=C15:29, P16=C15:59, Pprev=preceding permissible full-session close; opening RV first log(C09:30/O09:30)+29 close ratios, sqrt(sum q²), log guard1e-8. D2 did not compute the production returns/RV.
- `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY` → private environment → headers only; existing .env loaded privately by session launcher. No values/headers logged. No other provider contacted.
- `EBM_DATA_ROOT`, `--data-root` → CLI → physical data root; explicit CLI overrides environment, default repo data/. No hardcoded machine path or symlink requirement.
- Model seeds, interactions, statistical/trading materiality/costs → **not applicable/unchanged**; no model fit or scientific test. Dataset schemas/IDs are operational acquisition versions, not rewritten scientific protocols.

## 9.4 Ordered execution and reproducibility trail

Working directory: repository root (`.`). Input task attachment was read only; no prompt/source/spec fabricated.

1. `cat <attachment>/Pasted text.txt`; `git status --short`; `git branch --show-current`; `git rev-parse HEAD`; `rg --files -g 'AGENTS.md' -g 'config/**' -g 'src/**' -g 'tests/**' -g 'scripts/**' -g '*D2*' -g 'reports/shared/**' -g 'reports/sessions/**'`: exit 0, clean main at starting commit.
2. Read AGENTS/README/.gitignore, pyproject/lock/config, D1 implementation/tests/manifest, D0/D1 reports/session audit, shared docs/layout. Targeted B spec reads `sed -n '121,193p'` and `'330,345p'`, starter `'115,147p'`; D1 Client `'207,274p'` and audit sections read explicitly after some large batched output truncation. No claim of reading unavailable theory papers/source archives.
3. Inline Python: `shutil.disk_usage('.')` (initial64,307,200,000free bytes), actual D1 Parquet existence and SHA match, credential names/nonempty flags without values, environment presence flags. `.venv/bin/python --version` reports3.14.6. Reused dependency lock/environment, no pip install.
4. `.venv/bin/python -B -m unittest discover -s tests -p 'test_d1_candles.py' -q`:2/2 PASS,1.029s; known Arrow sandbox CPU-cache sysctl warnings nonfatal. Public Alpaca bars/terms pages checked; no provider data beyond the authorized source.
5. Added D2config/module/wrapper; added exactly2new regression functions. `.venv/bin/python -B scripts/d2_spy_acquire.py --dry-run`:exit 0;2,701sessions,2,680full,21early,1,049,610expected candles; initial optional2015-12-31anchor;~10MBretained and120–300MBtransfer estimate. Calendar counts derived rather than asserted.
6. `.venv/bin/python -B -m unittest discover -s tests -p 'test_d*_*.py' -v`:4/4 PASS,1.945s before acquisition. No live requests in tests.
7. Ran the authorized first-year acquisition with explicit approved network escalation (D0/D1 had established the network sandbox restriction). Actual launcher was:

```sh
.venv/bin/python -B - <<'PY'
import os, runpy, sys
from pathlib import Path
for line in Path('.env').read_text().splitlines():
    s = line.strip()
    if s and not s.startswith('#') and '=' in s:
        k, v = s.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip(chr(34) + chr(39)))
sys.argv = ['d2_spy_acquire', '--max-years', '1']
runpy.run_module('ebm_research.experiment_b.acquisition', run_name='__main__')
PY
```

Exit0. Optional pre-sample request HTTP 200empty. 2016 first checkpoint22,841rows/785,927bytes,9other-window absent minutes,250/251eligible full days.26HTTP 200requests/19,670,613response bytes/88.888s. January measured1,729retained rows/61,429Zstdbytes in memory,8,664,758bytefull-source projection. No second measurement artifact retained.

8. Checked saved2016gap/eligibility/cost/identity and storage. Added **summary-only** cluster/disjoint distributions and execution-history bookkeeping between invocations; no source/QA/retention science change, no re-download of2016. Then ran the same approved private loader with `sys.argv=['d2_spy_acquire','--resume']`, preserving and skipping verified2016. Exit0, remaining10years processed.559.300s. No uncontrolled concurrent requests or background worker.
9. Monthly request pattern on every page: `GET https://data.alpaca.markets/v2/stocks/SPY/bars`, parameters `timeframe=1Min`, `feed=sip`, `adjustment=split`, `sort=asc`, `limit=10000`, calendar first-session open to last-session close−1s inclusive; continuation `page_token` followed until absent. Monotonic page boundary/repeated-token/range checks enforce integrity. Yearly count queries use same endpoint/feed/adjustment with1Day and ETmidnight/final23:59:59. Optional initial anchor is15:59:00–15:59:59 only. Actual ledger has **260minute pages (including anchor) +11daily pages =271**, allHTTP 200, **222,454,942bytes**,0failures/retries. No auth header/token values/full keyed URLs retained. Exact per-request boundaries/hashes/times in ignored ledger.
10. First pass audited every retrieved regular-session minute, then selected required windows; completed years froze canonical and QA together. Progress was attended and reported; no source query/repair selected after inspecting returns. All2,701sessions complete; source freeze **2026-10-16T17:58:00.521428Z (13:58EDT)**.
11. Final aggregate publication reads saved QA only; it does not re-scan/re-download discarded full-day prices. Parquet metadata checks read first/last bounds/counts from11files; one prior-session row subset read at the actual year resume. These are not repeated whole-period candle audits.
12. Static review found a **resume-only bookkeeping defect**: a whole-file hash on the append-only request ledger could reject an interrupted run's legitimate new records. Added `verify_request_ledger` committed-prefix validation, LF/CRLF support, and tiny assertions in the existing D2resume test. No data/QA result changed. First correction suite4/4 PASS1.884s; final portable correction suite4/4 PASS2.724s. Source acquisition fingerprints remain in `execution_history`; current maintenance fingerprints explicitly separate.
13. `.venv/bin/python -B scripts/d2_spy_acquire.py --verify-only`:11years/243,804rows/8,975,163bytes verified, **0network calls**, twice after operational fixes. No second full historical acquisition or source-candle audit.
14. Added explicit schema/provider/split/license descriptors and hashes for9published quality files to final source manifest. These are post-freeze metadata additions, not modified candle files. Logged the operational correction; no observed provider/entitlement/parse/duplicate failure was hidden. Wrote full D2report, appended new facts to3docs, completed this report from its acquisition-progress draft.
15. Final cheap checks: syntax via `ast.parse`; `git diff --check`; no-index whitespace checks for new authored text; configured-secret byte scan (no values output); source/config/spec/QA/published/ledger hashes; annual/month/quarter/cluster/window/split CSV counters; D1source and prior-report preservation; ignored-source protection; final Gitstatus. Final validation note below records actual results.

Exact frozen config SHA-256 **848a8068ea146a4c45edd92e15e3aa57ff7df736815463145015dff6edc14c0c**; Bspec SHA-256 **0e3f0946f4b6c9696c888f86e42669bff709fa56599b6069391e3b5af3e4acfc**. First invocation acquisition code SHA **5ccfae605e1a0965ae3db18f67ab5cb2135f2d514e6a09940ede88c79ce2466b**; resumed acquisition code SHA **27740ea03253176da47330d6d46cf7c7b61a3290ab83b763ea91759a6328602e**. Unchanged D1helper SHA **91d2acf233c4ab897e8e0595e425148f95735ad383642d825e195ca50ffbe67a**. Current resume/metadata maintenance hashes are registered separately; no assertion that original acquisition executed post-freeze code.

Python3.14.6; exchange-calendars4.13.2, pandas3.0.6, numpy2.5.4, pyarrow23.0.1, tzdata2026.5; full runtime pins in unchanged requirements-d1.lock.txt. No seeds, fitting hyperparameters or numerical research outputs applicable. Measured source invocations **648.188s total**; HTTPwall151.3405s, plus pacing and audit/serialization. Human preparation/approvals/report time not included in that measured runtime.

New machine: create venv; install lock then `pip install -e .`; use matching authorized local source/QA backup and `--verify-only`, or **new empty data root** for a separately authorized acquisition. Export only private APCA keys, run dry-run/first block/--resume as above. CLI--data-root overrides EBM_DATA_ROOT; Windows uses .venv/Scripts/python. A public clone contains no licensed Parquets. Vendor revisions may change responses: preserve original frozen identity/hashes, never promise byte-identical re-download or overwrite a changed source. Current source is fully complete, so the smallest reproduction check is verify-only (no credentials/network required); Stage 1 is not part of recovery.

## 9.5 Tests, full QA and scientific integrity

**Tests:** reused D1 two-fixture suite2/2 PASS; then complete4-test suite ran 3 times (1.945s,1.884s,2.724s), all4/4 PASS. Exactly2new functions, tiny complete-empty-day and checkpoint/prefix/pagination regressions; no mocked ecosystem, synthetic decade, model fit or benchmark framework. Temp smoke outputs auto-cleaned. Arrow CPU-cache/neon sysctl warnings are nonfatal; all Parquet/I/O/hash checks pass.

**Full real-source audit:** **1,049,610expected =1,049,506unique observed/valid +104absent**. All2,701scheduled sessions retrieved, unknown0, whole-empty0. Invalid/corrupt/duplicate/conflicting/order/parse/zero-volume/zero-count/extra/review-extreme totals0. Missing field counts also0. Each session reconciles present+absent=expected; maximal clusters sum exactly104; year/month/quarter/window sums reproduce totals. No duplicates inflate unique counts. No API error classified as candle loss.

**Gaps:**9clusters,8affected sessions, max28minutes on2019-08-12 15:32–15:59ET (one largest tie). Mean11.555556,median14,p95linear22.4; size bins1:0,2–4:2,5–9:2,10–29:5,30+:0. Full list/ET+UTC/reasons and top20 in stage report/CSV/summary; no guessed causal labels. Longest affected-day run1 (8tied dates), longest eligible run250sessions2021-11-29–2022-11-23. Unsampled/uncommitted coverage was null/unknown during first-block stage, then fully resolved; no hidden partial month/year.

**Windows:** disjoint opening46 +14:59anchor0 +late1 +target29 +other28=104. Overlapping critical-anchor flags2 (15:29,15:59, both2019-08-12) not counted twice. Four full-session RV losses; one closing-label loss; all strict loss rates below2% (overall4/2677=.149421%). Full candle-complete2672/2680; all91inputs complete2675/2680; primary2673/2680. These are distinct metrics, not interchangeable.

**Eligibility:** primary full-day counts1493/1499train,497/498validation,683/683sealed. Seven ineligible full dates:2016-01-04missingleadinganchor;2019-08-12closinganchors;2019-08-13missingpriorclose;2020-03-09/12/16 and2023-06-05incompleteopening30.21early closes separately excluded. Six complete calendar years have every full day primary-eligible (2017,2018,2021,2022,2024,2025), exceeding3-year data screen; no statistical power/shape/support guarantee. Firsteligible2016-01-05; last2026-09-30. Daily SIP/split count flags available/>=500 on2701dates, not TAQequivalence or forced minute reconciliation.

**Timing/science:** source always SPY/SIP/split, UTCbarstarts→ETcalendar; no 16:00-start target, no overnight/full-day RV, no price fill or older fallback for ordinary missing full close. Prior permissible full rule spans21early-close boundaries transparently. Sealed data used only for mechanical availability/quality counts, not outcomes/model/state selection. No production r1/r12/r13/RV table, correlations, regressions, EBM, trading or A work. This is modern-only data readiness, not Gao1993–2013replication. Unknown missingness causes/selection and D1daily/cross-feed/split-event qualifications are preserved.

**Freeze/security:** source and annual QA immutable SHA-256 plus committedledger prefix verified; published outputs hashed; current maintenance code separate from executed acquisition hashes. Credentials/source remain ignored; zero configuredsecret matches in authored outputs. No licensed rows committed or redistributed. Source source/QA restore instructions complete, subject to independent entitlement. Existing D1helper/pilot/oldreports unchanged.

## 9.6 Errors, anomalies, decisions and recovery

| When / command / location | Symptom and confirmed vs suspected cause | Fix/actions/files/tests | Remaining and shortest safe next step |
|---|---|---|---|
| Optional2015-12-31anchor | HTTP 200empty, confirmed absent returned anchor; no assertion about entire pre2016archive | Retain explicit unavailable flag; initialday r1ineligible; no invented price or new feed | Qualification carried into Stage 1 |
| Real gap dates |104absent starts/9clusters, causes unknown | Preserve actual rows +absence registry, strict input flags/exclusions; no requery to conceal or fill | Stage 1useseligibledata; no random-missingness assumption |
| Annual checkpoint resume | Clean2016resume successful, but staticreview/fixture exposed growing-ledger whole-file guard defect for interrupted runs | Changed to committedprefix checksum, LF/CRLF safe; existing short resume test expanded,4/4 PASS; no actual acquisition data invalidated | Corrected; immutable files still whole-filechecked; source bytes unchanged |
| Before second source invocation | Needed richer cluster/disjoint summaries and code-history preservation | Summary-only additions; first2016hasheschecked, no reacquisition; both execution fingerprints saved | No scientificchange; originalcountsretained |
| Postfreeze descriptor review | Needed explicit schema/provider/split/quality-hash metadata | Added descriptors/maintenance identity; no source-candle audit/rewrite | Metadata revision documented; freeze time denotes source data |
| Local PyArrowtests/verify |sysctlbyname cache/neon Operationnotpermitted in sandbox, warningonly | I/O/tests/hashchecks pass; no privilege workaround or packagechange | Nonfatal; exact warnings in tool output, no observedcorruption |
| Global disk measurement | Free64.3072GB→63.8976GB while ownsource/QA~17.53MB | Report directfilebytes; unrelated activity not attributed | Recheckbeforefuturelargework; no budgetissue |

No HTTP failure, rate-limit/backoff, entitlement stop, incomplete page, parse failure, conflicting duplicate, corrupt/orphan partition, unexpectedly large write or invalid scientific result occurred. The only identified code defect was an operational interrupted-resume guard, fixed and regression-tested without changing candles/QA. All minor changes were within allowed engineering scope; no scientific decisions silently made. No past result invalidation/rerun is needed; no uncompleted segment remains. No quarantined/partial source file or unfinished network task remains.

Recovery checkpoint is the final manifest with11completedyears, retrieval_complete=true, active_year=null, registeredsource/QA/published/ledger identities. **Use `.venv/bin/python -B scripts/d2_spy_acquire.py --verify-only`**. On changed/orphan/partial/corrupt output, preserve exact paths andinspectmanifest/ledger; never overwrite, weakencoverage, or switchprovider. On genuine interrupted future acquisition, registered yearsverified/skipped, uncommittedyearunknown/retriedbounded, repeatedchangedresponseflagged. No automaticunattendedloop.

## 9.7 Resources, Git summary and handoff

Canonical **8,975,163bytes/11files**, request ledger **162,322bytes**, annual QA **7,144,002bytes/11files**, consolidated registries roughly1.24MB; totalretained source/QA~**17.53MB**. Includingnew code/config/tests/docs/reports, net D2 growth is about**17.6MB**. Existing D1 environment reused,0new package installs; no full JSON/alternate-window/fold/model copy. First yearmeasured 0.786 MB, final 8.98 MB. Dataset budget<1GB comfortably met; no2GB escalation.271HTTP 200calls/222.45MBresponse bytes/0errors/retries; measuredsource invocations648.188s. No cloud/warehouse/worker/distributedstack or costly model run.

Starting Git clean, ending tracked modifications only data README/shared source/layout docs; new D2 code/config/tests/registries/reports untracked. Ignored licensed annual Parquets/ledger stay local. D1 data/specs/code/old reports/.env/.gitignore/pyproject/lock preserved. No commit/stage/push. Exact final Git status/diff/security/hash results recorded below after report completion.

Handoff: read [D2 full acquisition/candle-quality report](../shared/D2_full_spy_sip_acquisition_and_candle_quality.md), D2 source manifest, per-session QA, gaps/summary, updated source/layout docs and B v1§3–4/§10. **Stage 1may be separately authorized**: one canonical daily table and source-style OLS on the modern 2016-start branch, using documented eligible pairs, strict opening RV/minute anchors, existing train/validation/sealed boundaries, count-basis and half-day elapsed-time qualifications. No statistical/scientific finding is asserted; noStage 1task is executed. A remains on hold. Missingness causes and actual split-event verification remain limitations rather than scientific redesign decisions.

Final post-report validation: PASS all 32 registered source/annual-QA/published-quality/ledger byte sizes and SHA-256 checks; config/spec and current maintenance-code identities; every per-session present+absent=expected identity; 104 missing-minute rows and summed nine cluster lengths; 11 year/129 month/43 quarter totals; 2,673 primary eligibility flags; no missing price/volume/count fields. D1 source checksum preserved. PASS syntax, authored whitespace and configured-secret scan over 31 text/metadata files (zero matches). All 11 years verified with zero network calls. Final focused suite 4/4 PASS (2.724 seconds); no whole-period candle re-audit after freeze. Net source/QA bytes 17,522,718 before report text. Branch/commit unchanged; no Git staging/commit/push. Exact ending status:

```text
 M data/README.md
 M docs/canonical_data_layout.md
 M docs/data_source_registry.md
?? config/D2_spy_source.json
?? data/registry/D2_blocks/
?? data/registry/D2_spy_candle_gap_clusters.csv
?? data/registry/D2_spy_candle_qa_sessions.csv
?? data/registry/D2_spy_candle_qa_summary.json
?? data/registry/D2_spy_coverage_month.csv
?? data/registry/D2_spy_coverage_quarter.csv
?? data/registry/D2_spy_coverage_year.csv
?? data/registry/D2_spy_exception_log.json
?? data/registry/D2_spy_invalid_candles.csv
?? data/registry/D2_spy_missing_candles.csv
?? data/registry/D2_spy_source_manifest.json
?? reports/sessions/20261016_1349_B_D2_spy_full_acquisition_session.md
?? reports/shared/D2_full_spy_sip_acquisition_and_candle_quality.md
?? scripts/d2_spy_acquire.py
?? src/ebm_research/experiment_b/acquisition.py
?? tests/test_d2_acquisition.py
```
