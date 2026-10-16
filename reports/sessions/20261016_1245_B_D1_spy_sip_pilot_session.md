# Experiment B / D1 coding-session audit

## 9.1 Session identification and verdict

Session `20261016_1245_B_D1_spy_sip_pilot_session`, report timestamp **2026-10-16T12:45:11.983630-04:00**, America/New_York, EDT (UTC−04). Agent: Codex; exact runtime model not exposed. Scope **B only**, stage **D1 — Alpaca SIP split-adjusted acquisition pilot and candle-quality audit**. User prompt: attached `3debd64e-9fde-4f3a-8f95-e865b03a7b5d/Pasted text.txt`.

Start/end branch **main**, commit **c971e184c06a0590b3db0c51ae3873de251de285**. Starting `git status --short` empty: clean workspace. The user committed D0 before this session. Existing ignored .env and D0 responses preserved. No commit, staging, push, branch mutation, purchase or user-data deletion.

**Gate: PASS WITH QUALIFICATIONS. Scientific effects: NOT EXECUTED.** All mandatory sampled candle QA passed. Remaining qualifications: daily/minute price/count differences, small cross-provider OHLC differences, actual split event not tested, continuous history not verified. A stayed on hold with no A queries/processing/modeling. D2 needs a separate prompt; no full acquisition/model fit occurred.

Completed: authoritative orientation; verified event/calendar; 11 full-session requests including one half-day plus 3 prior anchors; single compressed canonical store; per-date/window/gap/aggregate QA; ex-dividend/raw/dividend and split-adjusted Massive comparisons; daily reconciliation; source/hash manifests; two focused tests, independent one-day RV/anchor check, zero-network cached reruns, evidence-based docs and reports. Not completed by scope: multi-year/source-era coverage, actual split correction at an event, trade-level discrepancy attribution, any modeling/scientific hypothesis/performance analysis.

## 9.2 Exact file inventory

| Action | Repository-relative path | Why | What changed (functions/config/data/schema) | Critical dependencies/consumers | Recovery note |
|---|---|---|---|---|---|
| CREATED | `pyproject.toml` | D1 implementation or report | Installable src package; calendar/Parquet direct pins | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `requirements-d1.lock.txt` | D1 implementation or report | 10 exact runtime package pins; no machine location | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `config/D1_spy_source.json` | D1 implementation or report | 11 exact sessions/rationale, events, source and bounded controls | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `scripts/d1_spy_pilot.py` | D1 implementation or report | Thin installed-package entry point | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `src/ebm_research/__init__.py` | D1 implementation or report | Package marker | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `src/ebm_research/experiment_b/__init__.py` | D1 implementation or report | B-only package marker | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `src/ebm_research/experiment_b/pilot.py` | D1 implementation or report | Calendar, candle QA, bounded/cache acquisition, comparisons/manifest | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `tests/test_d1_candles.py` | D1 implementation or report | Two focused unittest fixtures including Parquet smoke | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `data/registry/D1_spy_actual_checks.json` | Tracked small QA/provenance | One-day actual anchor/equation/independent RV PASS; no numerical outcomes | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_candle_gap_clusters.csv` | Tracked small QA/provenance | Header only; zero runs | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_candle_qa_sessions.csv` | Tracked small QA/provenance | 11 session rows; grid/gap/OHLC/window/eligibility/reasons | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_candle_qa_summary.json` | Tracked small QA/provenance | Daily/window/year/month/time-of-day totals/runs | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_failure.json` | Tracked small QA/provenance | Sandbox failure now explicitly RECOVERED | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_missing_candles.csv` | Tracked small QA/provenance | Header only; zero absent minutes | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_source_manifest.json` | Tracked small QA/provenance | Dataset/config/spec/code/canonical/auxiliary hashes, versions, cache evidence | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/registry/D1_spy_storage_projection.json` | Tracked small QA/provenance | In-memory compression + calendar-only D2 projection | Report / next stage | Rebuild QA from verified source; retain original provenance |
| CREATED | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet` | Sole primary candle store | 4,113 rows x 13 columns; UTC bar starts, SIP/split, full/anchor roles; 152,721 bytes | QA and future source reference | Ignored; hash in D1 manifest; preserve conflicting identity |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/actual_anchor_check.json` | Lineage or separate auxiliary diagnostic | 448 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/comparison_results.json` | Lineage or separate auxiliary diagnostic | 10292 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/daily_2024-03-08_p0.json` | Lineage or separate auxiliary diagnostic | 861 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/daily_2024-11-27_p0.json` | Lineage or separate auxiliary diagnostic | 861 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/daily_2024-12-02_p0.json` | Lineage or separate auxiliary diagnostic | 653 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/daily_2026-09-14_p0.json` | Lineage or separate auxiliary diagnostic | 1681 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/ex_2026-09-17_dividend_p0.json` | Lineage or separate auxiliary diagnostic | 650 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/ex_2026-09-17_raw_p0.json` | Lineage or separate auxiliary diagnostic | 649 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/ex_2026-09-18_dividend_p0.json` | Lineage or separate auxiliary diagnostic | 1465 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/ex_2026-09-18_raw_p0.json` | Lineage or separate auxiliary diagnostic | 1460 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/ex_2026-09-21_dividend_p0.json` | Lineage or separate auxiliary diagnostic | 1468 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/ex_2026-09-21_raw_p0.json` | Lineage or separate auxiliary diagnostic | 1463 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/massive_split_overlap.json` | Lineage or separate auxiliary diagnostic | 77751 bytes; JSON price/count diagnostics or derived comparison; never primary source | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/requests.json` | Lineage or separate auxiliary diagnostic | 14190 bytes; 25 request endpoint/params/status/body-hash records; no candle payloads | Manifest auxiliary hashes / comparisons | Ignored; preserve source/hash; do not redistribute |
| CREATED | `reports/shared/D1_spy_sip_pilot_and_candle_audit.md` | D1 implementation or report | Required data/scientific QA report and qualified gate | CLI / review / D2 | New file; no user artifact overwritten |
| CREATED | `reports/sessions/20261016_1245_B_D1_spy_sip_pilot_session.md` | D1 implementation or report | This session audit | CLI / review / D2 | New file; no user artifact overwritten |
| MODIFIED | `docs/data_source_registry.md` | New evidence | Appended D1 dates/event/license evidence and observed adjustment/cross-feed/daily differences; D0 entries preserved | Data users / next stage | Original in starting Git commit |
| MODIFIED | `docs/canonical_data_layout.md` | New evidence | D0-as-of wording plus actual D1 schema/path/cache and measured size plan | Data users / next stage | Original in starting Git commit |
| MODIFIED | `data/README.md` | New evidence | Corrected stale no-canonical statement; linked D1 restore/report; D0 commands retained | Data users / next stage | Original in starting Git commit |
| CREATED (generated group) | `.venv/**` — 7,017 regular files, about 243,160,799 bytes | Isolated required dependencies | Package/version manifest `requirements-d1.lock.txt`; Python/pip/runtime libraries | Installed package/tests | Ignored; rebuild from lock and editable install |
| CREATED (generated group) | `src/ebm_research.egg-info/*` — 5 files: PKG-INFO, SOURCES.txt, dependency_links.txt, requires.txt, top_level.txt | Editable installation | Build metadata, about 608 bytes | pip | Ignored; rebuild by pip install -e . |
| CREATED → MOVED (temporary) | `data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet.tmp` → `pilot.parquet` | Atomic write | Sole generated Parquet moved into registered location | Acquisition | No partial file remains; no user file moved |
| CREATED → MOVED (temporary group) | `data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/*.json.tmp` (14 distinct names matching retained JSON inventory); `data/registry/D1_*.json.tmp` (JSON targets above) | Atomic metadata | Stage-owned output only; ledger updated per request | write_json | No temporary JSON remains; no original input overwritten |
| CREATED / auto-cleaned (temporary group) | OS temp `ebm_d1_smoke_*/smoke.parquet` (3 suite executions), pip build/env/ephemeral-wheel directories | I/O smoke / editable build | Tiny smoke Parquet and build dependencies; no licensed data | unittest / pip | Automatically cleaned; no user deletion |
| INSPECTED | `AGENTS.md` | Scope, authority, storage/testing/session rules | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `README.md; .gitignore` | Existing definitions, layout and ignores | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md` | Frozen source/timing/state/date/QA rules | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md` | Workflow and operational exceptions | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `reports/shared/D0_data_source_feasibility.md` | Sparse authenticated feasibility evidence | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `data/registry/d0_*.json (8 files)` | D0 manifests/request/QA evidence | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `data/raw/diagnostics/*.json (15 files)` | Existing ignored source hashes verified; no promotion or copy | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `scripts/d0_probe.py` | Inspected existing helper; fixed 390-day audit not suitable for D1 half-days | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `.env` | Names/presence only; privately loaded into process environment | No changes | D1 authority/evidence | Preserved |
| INSPECTED | `user attachment 3debd64e-9fde-4f3a-8f95-e865b03a7b5d/Pasted text.txt` | Exact D1 task | No changes | D1 authority/evidence | Preserved |

No preexisting user file was deleted/moved. Temporary paths above were generated write intermediates, not user artifacts. No licensed full-session duplicate, separate 91-window file, fold/seed/model input copy, or scientific daily table exists. D0 immutable sources and manifests were preserved. The old D0 manifest retains the historical hash of its data README revision; that document was intentionally updated for D1 and the old manifest was not rewritten.

Canonical schema/shape: **4,113 x 13**, 152,721 bytes; `symbol:string`, `timestamp_utc:timestamp[us, UTC]`, `session_et:date32`, `requested_session`, `request_role`, `source_request` strings; OHLC/vwap float64; observed volume/trade_count int64. Future fractional volumes must remain numeric without truncation. Artifact/14 auxiliary sizes/hashes are in D1 source manifest.

## 9.3 Critical function/class/variable register

All implementation functions below are in `src/ebm_research/experiment_b/pilot.py`; external consumers are its CLI main, the thin wrapper and focused tests. Inputs are SPY bar dictionaries, aware times, calendar/config; outputs are named below. No common A/B scientific calculation was introduced.

| Function/class | Signature | Purpose / inputs → outputs | Algorithm, information cutoff, assumptions and limits |
|---|---|---|---|
| `sha` | `(path)` | Small file → SHA-256 | Manifest/cache identity; no repeated input copies |
| `write_json` | `(path,value)` | Stage metadata → atomic JSON | Own .json.tmp then replace; no credentials |
| `timestamp` | `(value:str)` | Source time → UTC-aware exact minute | Reject naive/misaligned timestamp, ValueError |
| `calendar` | `(start,end)` | ISO dates → XNYS calendar | 20-day prior-anchor buffer; side=left; no weekday-only calendar |
| `grid` | `(cal,day)` | Calendar session → minute starts | Actual full/early close/holiday schedule |
| `prior_full` | `(cal,day)` | Current date → preceding permissible full date | Explicit D1 skip-half-day rule; never invent 16:00/13:00 anchor |
| `window_flags` | `(aware_time)` | Time → overlapping named windows | Opening, anchors, late, final target, other |
| `valid_bar` | `(bar)` | Native OHLCV/count → bool | Finite positive consistent OHLC; supplied volume/count finite nonnegative; no clipping |
| `indexed` | `(bars)` | Native list → time→all values + parse/order counts | Keeps duplicates; ordering checked before sorting |
| `usable` | `(values)` | Same-timestamp records → usability | Every bar valid and identical; conflicting duplicate fails |
| `audit_session` | `(day,bars,all_bars,cal,config)` | One whole session → QA row, gap clusters, absent minutes | Missing=absent timestamp; invalid/conflicting separate; expected=present+missing; maximal contiguous gaps; exact prior/window eligibility; no fill |
| `_same_time` | `(value,t)` | Safe exact UTC equality | Prior-anchor lookup; parse failure false |
| `anchor_check` | `(day,all_bars,cal)` | One actual sample → 5 anchors, returns, RV/log | Simple-return endpoints, first open→close +29 close ratios, sqrt(sum q²); ignored numeric QA only, no predictive analysis |
| `credentials` | `()` | Environment → private headers | APCA vars required; prints names only if missing; no dotenv read inside engine |
| `Client` | `(raw_dir,config)` | Small request engine + lineage | Rate spacing, timeout/byte/page caps; no worker or automatic retry |
| `Client.get` | `(name,endpoint,params,headers,retain=False)` | HTTP or verified auxiliary cache → JSON | Body hashes/status/time/size ledger; keys only in headers; full-session bodies not retained twice; sanitized errors abort |
| `Client.alpaca` | `(name,start,end,headers,timeframe='1Min',adjustment='split',retain=False)` | SPY/SIP bounded interval → bars | Explicit modes/endpoints; inspect next_page_token; max 3 pages |
| `csv_write` | `(path,rows,fields)` | Small rows → audit CSV | LF endings; zero-gap headers without fabricated gaps |
| `runs_of_sessions` | `(days,cal)` | Eligible/affected dates → contiguous exchange-session runs | Unsampled/ineligible sessions break runs; no calendar-day adjacency assumption |
| `aggregate` | `(rows,clusters,missing,cal)` | QA → actual total/stratified/runs summary | Year/month/session/window/time-of-day denominators; one day is one cluster; no extrapolation |
| `comparisons` | `(client,config,all_bars,cal,headers,days)` | Bounded auxiliary queries → ignored diagnostics | Split daily and Massive; raw/dividend event modes separate; no primary feed splicing or TAQ equivalence |
| `main` | CLI with --source-config, --data-root, --start/--end, --dry-run | Config/credentials → sole Parquet, QA, manifest | <=15 sessions; cache binds config/date/hash and makes zero HTTP; conflicting identity aborts; full D2 not silently enabled |
| `scripts/d1_spy_pilot.py` | `main()` | Thin CLI → installed package | No sys.path patch/copy of pipeline |
| `tests/...:bars_for` | `(cal,day)` | Constant-price fixture | Test-only bars, never vendor/default data |
| `CandleAuditTests.test_missing_clusters_and_critical_endpoints` | unittest | Missing opening/15:29 + duplicate/order → gap/eligibility assertions | One fixture; 3 absent bars, 2 maximal runs, RV/r12/r13 invalidated |
| `CandleAuditTests.test_calendar_prior_close_formula_and_smoke` | unittest | DST/holiday/half-day/prior/full/math + temporary Parquet | Second fixture; zero-gap null timestamps and portable I/O |

Critical names → location → units/default/use:

- `ROOT`, `ET`, `UTC`, `FIELDS` → module → portable root from file parents, ZoneInfo America/New_York, UTC, native-to-canonical OHLCV/n/vw mapping. Genuine bar-start semantics preserved; no machine-specific path or fixed UTC-offset logic.
- `dataset_id` → config → `B_alpaca_sip_SPY_1m_split_D1_v1`, one canonical/extract identity. `symbol=SPY`, `feed=sip`, `adjustment=split`, `calendar=XNYS`; raw/dividend never merged with canonical.
- `sessions` → config → 11 dates/rationales fixed before data: 2024-03-08/11, 2024-11-27/29, 2024-12-02, 2026-09-14/15/16/17/18/21. No date replaced after QA. Anchor-only dates 2024-03-07, 2024-11-26, 2026-09-11.
- `ex_date=2026-09-18`, `ex_date_evidence` → config → issuer URLs/version/page/record/pay/distribution facts. `massive_overlap=2026-09-15`; `split_boundary_status=NOT TESTED` on an actual event.
- `max_sessions=15`, `max_pages_per_request=3`, `request_spacing_seconds=0.25` → config → bounded resource controls. Engine timeout 30s, max 2,000,000 response bytes; Alpaca limit 10000, Massive limit 1000.
- `price_tolerance_usd=0.000001` → config → diagnostic OHLC equality threshold, not tick/cost assumption. `manual_extreme_range_fraction=0.05`, `manual_extreme_close_jump_fraction=0.05` → flags only, never clipping; fixed before data.
- `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`, optional `MASSIVE_API_KEY` → exported environment → auth only. Launcher privately loaded original .env. No values/headers/query keys logged.
- `EBM_DATA_ROOT`, `--data-root` → main → shared physical root; CLI overrides environment, repository data/ default. All source paths relative to selected root; no required symlink.
- `--start/--end` → main → paired date range, <=15 sessions, matching event/overlap config required for acquisition. Dry-run validates/plans only, no HTTP/writes.
- `prior_full_session`, `eligible_r1/r12/r13/rv/primary`, `valid_required_window` → QA → exact permissible anchors/window validity; 2024-12-02 uses 2024-11-27 full-session 15:59, explicitly skipping half-day.
- `expected`, `observed_unique`, `valid_unique`, `missing`, `gap_clusters`, `max_gap_length`, `eligible_day_clusters` → summary → actual requested 11-session denominators, not anchor-only rows or minute-IID statistical inflation.
- B v1/`anchor_check`: `Pprev`, `P10=C09:59`, `P15=C14:59`, `P1530=C15:29`, `P16=C15:59`; simple `r1/r12/r13`; RV first open→close then29 close ratios, `sqrt(sum q²)`, log guard `1e-8`. One actual numerical QA example only.
- `>0.02` → gate → strict opening-RV loss stop among full pilot days; actual 0/10; critical closing/prior/structural failures also block.
- B scientific train/validation/test boundaries remain unchanged: preapproved 2016–2021 fallback, 2022–2023 validation, sealed 2024-01-01–2026-09-30. Source-era access UNKNOWN. Seeds/models/interactions/materiality/trading costs unused and unchanged. No scientific protocol rewritten.

## 9.4 Exact execution and reproducibility trail

Working directory throughout: repository root `.`. Substantial commands/statuses in order:

1. `cat <user attachment>/Pasted text.txt`; `git status --short`; `git branch --show-current`; `git rev-parse HEAD`; `rg --files -g 'AGENTS.md' -g '*D1*' -g 'scripts/**' -g 'config/**' -g 'src/**' -g 'tests/**' -g 'data/registry/**'`: exit 0; clean main and commit above.
2. `cat .gitignore`, shared layout/source docs/D0 report and README/AGENTS; `sed -n '1,180p' scripts/d0_probe.py`; `ls -la`. Targeted B spec reads: 1–35, 121–220, 220–320, 320–415, 415–455 lines; B starter first70. Batched output sometimes truncated, active source/timing/QA sections read separately. No unseen paper/theory archive claimed read.
3. Inline Python presence-only credentials; Python/importlib availability; `shutil.disk_usage('.')`. Python3.14.6; initial free **64,307,200,000 bytes**. No venv/pandas/pyarrow/calendar/numpy installed. .env names present but not exported; 15 D0 raw responses exist.
4. Public primary sources inspected via web: issuer distribution listing/schedule page3, NYSE early-close announcement, Alpaca bars/aggregation/disclosures/terms, Massive documentation/terms, PyPI metadata. Links in config/docs/stage report. Historical XLSX and subscriber-agreement link returned browser errors and are not claimed inspected. No bulk source data/download.
5. `python3 -m venv .venv`; `.venv/bin/python -m pip --version`: exit0.
6. `.venv/bin/python -m pip install --no-cache-dir 'exchange-calendars==4.13.2' 'pyarrow==23.0.1'`: exit0; about50.8MB package transfer, runtime pinned in lock.
7. Created package/config/tests. `.venv/bin/python -m pip install --no-build-isolation -e .`: exit2, build backend absent in fresh venv. `.venv/bin/python -m pip install --no-cache-dir -e .`: exit0 with isolated build dependencies. No system environment modified.
8. `.venv/bin/python -B -m unittest discover -s tests -p 'test_d1_candles.py' -v`: initial 2/2 PASS (~1.31s). `.venv/bin/python -B scripts/d1_spy_pilot.py --dry-run`: exit0; 4,110 expected session minutes +3 anchors; about411KB pre-compression projection; no HTTP/writes.
9. Acquisition ran this private environment loader (first sandboxed, then same command approved outside sandbox after URLError):

```sh
.venv/bin/python -B - <<'PY'
import os, runpy
from pathlib import Path
for line in Path('.env').read_text().splitlines():
    s = line.strip()
    if s and not s.startswith('#') and '=' in s:
        k, v = s.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip(chr(34) + chr(39)))
runpy.run_module('ebm_research.experiment_b.pilot', run_name='__main__')
PY
```

The executed loader used the equivalent literal quote-strip expression; no secret was interpolated into shell text or output. First request failed URLError under network sandbox; no candle response/partial source retained. Escalation explicitly approved; then **25 HTTP200 calls, 491,773 response bytes, 10.471s** including throttling, exit0. No automatic retries or workers remain.

Exact successful request parameters/time/hash/status are in ignored `requests.json`, referenced by source manifest:

- **11** SPY/SIP/split 1Min whole sessions, calendar open through close−1s; early day ends12:59:59 ET; all one page.
- **3** SPY/SIP/split anchor-only15:59:00–15:59:59 on2024-03-07,2024-11-26,2026-09-11; others reused.
- **4** SPY/SIP/split 1Day groups:2024-03-08–11,2024-11-27–29,2024-12-02,2026-09-14–21; midnight ET through final23:59:59; no years-between download.
- **6** raw/dividend diagnostic windows:2026-09-17 15:59;09-18 09:30–09:34;09-21 09:30–09:34, two modes each. Split reused from canonical.
- **1** Massive adjusted=true regular interval2026-09-15, millisecond boundaries, limit1000, key only in bearer header.

10. Local JSON/CSV inspection: zero gaps,10 eligible full days; daily/OHLC differences retained. No date replaced based on outcomes. Added cache-auxiliary hash/preflight/code/spec fingerprints/summary maxima as operational corrections only.
11. `.venv/bin/python -B scripts/d1_spy_pilot.py`: **three cached reruns**,0HTTP each, unchanged artifact; ~6.5–6.9s each. Latest manifest network_calls_this_run=0 refers to validation; original25-call ledger preserved.
12. Focused suite repeated after changes; **three invocations total,2/2 each**, final0.992s. No expanded test platform.
13. `.venv/bin/python -B scripts/d1_spy_pilot.py --start 2026-09-14 --end 2026-09-21 --dry-run`: six full sessions,2,340 minutes +1anchor; no writes/network or identity overwrite.
14. Independent one-day check: read Parquet2024-03-08; assert five anchors/simple equations; NumPy `sqrt(sum(diff(log([O09:30,C09:30,...,C09:59]))**2))` agrees (atol1e-14,rtol1e-10). Saved boolean evidence; numerical check remains ignored.
15. In-memory Parquet measurement:943 selected-window/anchor rows→37,674 bytes; no second retained file. Calendar-only projection and runtime dependency lock generated. pip freeze inspected; editable machine path not committed.
16. Added report/docs; inline AST/hash/secret/CSV reviews; `git diff --no-index --check /dev/null <each authored file>` initially flagged CSV CRLF; corrected LF, cached re-audit and2tests PASS.
17. `git diff --check`; `git diff --stat`; `git status --short`; `git check-ignore .env data/canonical/spy_minute/B_alpaca_sip_SPY_1m_split_D1_v1/pilot.parquet data/raw/alpaca/B_alpaca_sip_SPY_1m_split_D1_v1/requests.json .venv/pyvenv.cfg`; all expected protected paths ignored. Initial session-report generation shell command had heredoc delimiter collision and zsh unmatched-backtick parse error, created no report/file; corrected unique delimiter for this report. No acquisition code/data affected.

Environment **Python3.14.6**, exchange-calendars4.13.2, pandas3.0.6, NumPy2.5.4, pyarrow23.0.1, tzdata2026.5;10 exact runtime pins in lock. No random seed used. Config SHA256 `087740cdc02e097ed236f59b7b7461ab03dbc6f8cafbbfff1091aa4f47fc9bbb`; canonical SHA256 `065ab7a800749ab73cf62e4afc854891a30f2eb30fdfed513aa3e131411e4cf8`. Code/spec/auxiliary hashes in manifest. Logs are bounded sanitized request ledger plus tool diagnostics, no secret/full candle stdout dumps.

Fresh clone: create venv; install requirements-d1.lock.txt, then `pip install -e .`; run two-test suite/dry-run; privately export authorized keys; run bounded pilot only. Windows uses .venv/Scripts/python. A clone has manifests but not ignored licensed inputs: reconstruct into a **new --data-root** if old manifests lack source files; preserve original identity and dated evidence, do not bypass conflicting hashes. Vendors may revise bytes; re-download does not guarantee historical identical hashes. No new account/subscription or vendor entitlement implied.

## 9.5 Tests, QA and scientific integrity

- **PASS2/2**, three suite invocations. Small missing-run/duplicate/order and calendar/prior/formula/Parquet fixtures only; temporary outputs cleaned. Final suite0.992s.
- **Real audit PASS:**11 session grids; **4,110 expected=observed=valid**,missing0,gaps0,longest0/null. All duplicates/conflicts/ordering/parse/invalid/zero-volume/zero-count/extra/extreme counts0. Three valid prior-anchor rows separately identified.
- Ten full sessions have all30 opening bars, all91 scientific-window starts, allanchors and both30-minute late/target windows. Opening strict loss0/10; complete full days/required windows100%; combined eligible day clusters10. Half-day210expected, no fake missing180bars; excluded HALF_DAY. No fill/clipping/outcome-based deletion.
- Actual eligible runs2,1,1,6; maximum6. Missingness-run maximum0. Exact year/month/session/window/time-of-day denominators in summary. These purposeful sampled conditions do not prove random missingness or full-history completeness.
- One actual-sample equation/independent RV validation PASS; no predictor-target association, threshold fit, model/test metric or trading study. Numeric results ignored; no research daily table.
- Cache/identity PASS:3reruns0HTTP, unchanged source; canonical/14auxiliary/code/spec hashes checked. D0 immutable inputs/manifests preserved. Updated data README is the explicit documentation exception to old historical document hash.
- Credential protection: no configured-secret values in authored code/docs/manifests/reports; .env/source/venv ignores checked. No keys/headers/query secrets logged. No licensed rows committed.
- **Qualified comparisons:**390 Massive matching timestamps;2opens differ max.013USD,1high max.000046USD,low/close exact. Daily close−lastminute −.045 to+.100USD; counts differ, all11>=500. No forced equality or independent-feed/TAQ claim. Ex-date raw/split identical in11diagnostic candles; prior dividend close lower1.89USD, subsequent windows unchanged. Actual split NOT TESTED.
- Python syntax and tracked/new-text whitespace PASS after LF correction. Some Arrow sysctl capability warnings nonfatal; no pipeline/model path exists to test.
- Untested: continuous provider dates, actual split correction, original-era source fidelity, trade-level daily discrepancy attribution, full calendar/provider behavior over all years, modeling/inference/trading. Frozen Btarget/state/sealed dates retained; A untouched.

## 9.6 Errors, exceptions and recovery

| When / operation | Symptom / cause | Fix, affected files, rerun | Remaining / next safe step |
|---|---|---|---|
| Editable --no-build-isolation install | BackendUnavailable, cannot import setuptools.build_meta; confirmed backend absent | Normal isolated editable install succeeds; package imports/tests PASS | Resolved; use standard documented install |
| First Client.get acquisition request | Sandbox network URLError; no response | Failure record + approved escalation;25HTTP200; record RECOVERED; no partial source | Resolved; no automatic retry/background work |
| Arrow I/O under sandbox | sysctlbyname hw.l1/l2/l3cache/neon Operation not permitted | All Parquet writes/reads and3test suites pass | Nonfatal capability warning; no data corruption observed |
| pip freeze inspection | Pip cache permissions warning, cache disabled | Used importlib.metadata exact lock; no private editable location committed | No permissions workaround needed |
| Historical issuer XLSX/subscriber link | Browser Internal Error | Accessible issuer listing/schedule and public terms used instead | Account-specific rights not certified; no redistribution |
| Cross-source/daily discrepancies | OHLC or daily/minute not identical | Preserved/quantified; canonical SIPsplit unchanged; no clipping or target substitution | Exact trade-level causes unresolved, carried as qualifications |
| Default CSV writer | CRLF triggers no-index whitespace check | LF writer, regenerate own small QA from cache,2tests PASS | Resolved; Parquet unchanged |
| Cache/range review | Need preflight and auxiliary hashes | Added bounded event-config/range guard and hash checks;0HTTP cache passes | Intentional D1bound remains, no D2full range supported |
| Session report shell generation | Nested heredoc delimiter collision → zsh unmatched backtick | Verified no new session file; unique delimiter retry | Resolved; no data/code affected |
| Data documentation | Old no-canonical wording stale after acquisition | Minimal README/layout status correction, registry evidence append | D0 historical manifest unchanged |

All changes are D1-authorized or allowed operational fixes, logged before scientific evaluation. No scientific redesign/relaxed RV rule, no new licensing/subscription, no user-data destruction. No science result invalidated because none exists. Trusted checkpoint: registered sole Parquet/auxiliary hashes plus cached real QA PASS. On mismatch preserve source and inspect ledger/config; do not overwrite or blindly requery. Structural QA failure stops inference/acquisition expansion with explicit reason/gap evidence.

## 9.7 Resources, Git and next handoff

Retained canonical **152,721bytes**, auxiliary diagnostics/lineage **113,892bytes**, total **266,613bytes** (~0.267MB) source+cross-check material. D1registry ~50KB; authored source/config/test/report text small. Ignored venv **~243.16MB** across7,017regular files; editable metadata~608bytes. Stage growth including environment about**243.6MB**, well below1GB. No full-day+91window duplicate, large archive, fold clone, model artifact, heavy CPU job or pending API worker. Host free-disk API stayed64,307,200,000bytes; direct file sizes quantify actual additions rather than inferring from global usage.

Calendar-only D2plan:2,701sessions (2,680full,21early)2016-01-04–2026-09-30. Measured943selected rows/37,674compressed bytes scales to~**9.74MB** for243,881required-window/leading-anchor rows or~**38.97MB** fullregular retention. Actual first usable date/prior anchor/provider completeness/compression overhead unverified. D2must fetch whole sessions for full-grid QA even if onlyapprovedwindows retained afterward; one source and compact audit/lineage only.

Ending tracked modifications: data/README.md,docs/canonical_data_layout.md,docs/data_source_registry.md. New D1package/config/tests/registry/reports untracked; ignored source,auxiliary,venv/buildmetadata remain local. No Gitcommit/stage/push. Existing AGENTS/rootREADME/.gitignore/.env/D0data unchanged. See final post-report status note below.

Handoff: read [D1pilot and candle audit](../shared/D1_spy_sip_pilot_and_candle_audit.md), source manifest, session QA, updated source/layout docs, Bv1§3–4/§10. A remains on hold. A separate **D2full-acquisition prompt is justified**: split-only SIP primary, explicit full-session prior anchors, consistent minute endpoints, repeat full calendar/candle-gap/window QA on all acquired days, retain strict >2%RVloss stop and leading-anchor limitations, preserve daily/cross-feed qualifications and one compact canonical store. No D2download/modeling is started or implicitly authorized. No new scientific decision is needed for this pilot; carry its qualifications forward.

Final post-report validation: PASS authored-file whitespace/Python syntax, configured-secret scan over 35 files (including all new ignored diagnostic JSON; zero matches), unchanged D0 immutable inputs (intentional data README revision excluded), canonical/14 auxiliary/audit-code/config hashes, header-only gap files. Latest source manifest confirms 4,113 rows / 152,721 bytes and cached network_calls_this_run=0. Branch/commit unchanged. Exact ending Git status:

```text
 M data/README.md
 M docs/canonical_data_layout.md
 M docs/data_source_registry.md
?? config/
?? data/registry/D1_spy_actual_checks.json
?? data/registry/D1_spy_candle_gap_clusters.csv
?? data/registry/D1_spy_candle_qa_sessions.csv
?? data/registry/D1_spy_candle_qa_summary.json
?? data/registry/D1_spy_failure.json
?? data/registry/D1_spy_missing_candles.csv
?? data/registry/D1_spy_source_manifest.json
?? data/registry/D1_spy_storage_projection.json
?? pyproject.toml
?? reports/sessions/20261016_1245_B_D1_spy_sip_pilot_session.md
?? reports/shared/D1_spy_sip_pilot_and_candle_audit.md
?? requirements-d1.lock.txt
?? scripts/d1_spy_pilot.py
?? src/
?? tests/
```
