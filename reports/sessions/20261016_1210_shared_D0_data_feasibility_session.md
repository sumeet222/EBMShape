# D0 shared data feasibility — coding-session audit

## 9.1 Session identification and verdict

Session `20261016_1210_shared_D0_data_feasibility_session`, 2026-10-16T12:10:26.216129-04:00, America/New_York (EDT, UTC−04). Agent: Codex / GPT-6 family; exact runtime model not exposed. Scope **SHARED**, user task “Establish the data sources and canonical storage architecture … limited authenticated feasibility checks … small diagnostic samples.”

Starting/ending branch `main`, commit `24de8d01a115d1e4435d82e1091f8c772b6923aa`. Starting tracked tree clean; ignored `.env` preexisted. Four `ResearchSpec/` files appeared after initial inspection and user clarification; these user files are preserved. No commits, staging, branch changes, purchases or full acquisitions.

**D0 implementation/QA: PASS WITH QUALIFICATIONS. A: BLOCKED on WRDS authentication/entitlement. B: PASS for the explicitly limited feasibility checks, not research-ready continuous coverage.** Scientific effects: NOT TESTED. Historical source replication: NOT EXECUTED. Specifications were unavailable at first inspection; user supplied the location while diagnostic work continued. No canonical transformation or scientific change preceded their inspection. Both specs' source/timing/data sections and relevant starter instructions were then read. No approved spec was fabricated or altered.

Completed: repository/credential/disk inspection, bounded authenticated Alpaca/Massive requests, public HF/Kaggle metadata, partial HTTP range test, shared layout/docs, provenance/hash manifest, offline QA, this report. Incomplete: WRDS schema/rows, continuous-coverage audit, SPY-specific HF row extraction, archive licensing verification, daily-price/count reconciliation, canonical datasets, all modeling. These limits are explicit in the stage report.

## 9.2 Exact file inventory

All files below are new Codex artifacts unless marked INSPECTED. No original user file was modified, moved, renamed or deleted. During this session only newly generated provider registry JSONs were operationally rewritten to relocate licensed response rows into ignored raw JSON; their final content is references/hashes only. No extra original full-response copy is retained.

| Action | Repository-relative path | Why | What changed (functions/config/data/schema) | Critical dependencies/consumers | Recovery note |
|---|---|---|---|---|---|
| CREATED | `.env.example` | D0 implementation/documentation | Credential names only; no values | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `scripts/d0_probe.py` | D0 implementation/documentation | credentials, request, audit, main; bounded stdlib CLI | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `scripts/d0_verify.py` | D0 implementation/documentation | main; offline hashes/date grids/overlap/smoke | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `data/README.md` | D0 implementation/documentation | Restore and diagnostic CLI instructions | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_SPY_2016-01-05_sip_raw.json` | Bounded licensed diagnostic response | 42413 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_SPY_2019-07-15_sip_raw.json` | Bounded licensed diagnostic response | 42118 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_SPY_2023-07-17_sip_raw.json` | Bounded licensed diagnostic response | 42470 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_SPY_2024-07-15_sip_raw.json` | Bounded licensed diagnostic response | 42289 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_SPY_2026-09-15_sip_raw.json` | Bounded licensed diagnostic response | 42257 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_response_5.json` | Bounded licensed diagnostic response | 596 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_response_6.json` | Bounded licensed diagnostic response | 596 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_response_7.json` | Bounded licensed diagnostic response | 571 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_alpaca_response_8.json` | Bounded licensed diagnostic response | 571 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1201_massive_response_0.json` | Bounded licensed diagnostic response | 89738 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1208_anchors_response_0.json` | Bounded licensed diagnostic response | 264 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1208_anchors_response_1.json` | Bounded licensed diagnostic response | 268 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1208_anchors_response_2.json` | Bounded licensed diagnostic response | 267 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1208_anchors_response_3.json` | Bounded licensed diagnostic response | 268 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/raw/diagnostics/d0_20261016_1208_anchors_response_4.json` | Bounded licensed diagnostic response | 266 bytes; original provider JSON; SHA-256 in manifest | Offline QA; provider registry | Ignored; requery only with authorization/new ID; vendor bytes may change |
| CREATED | `data/registry/d0_20261016_1201_alpaca.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_20261016_1201_massive.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_20261016_1201_public.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_20261016_1208_anchors.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_20261016_1208_details.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_20261016_1215_hf-range.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_file_manifest.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `data/registry/d0_verification.json` | Reproducible access/metadata/QA evidence | Sanitized JSON; no licensed rows; sample paths/hash/size where relevant | D0 report and verifier | Keep evidence; offline QA/manifest regenerable, API snapshots are dated |
| CREATED | `docs/canonical_data_layout.md` | D0 implementation/documentation | Portable shared root, separate A/B schemas and dataset IDs | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `docs/data_source_registry.md` | D0 implementation/documentation | Verified access, metadata, licensing limits and WRDS prerequisites | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `docs/specs/experiment_A_new_chat_codex_and_diagnostics_instructions_v1.md` | Archive supplied v1 document | Byte-identical copy from ResearchSpec/experiment_A_new_chat_codex_and_diagnostics_instructions_v1.md | Scientific authority for A/B | Original preserved; hash-verify copy |
| CREATED | `docs/specs/experiment_A_turnover_conditioned_momentum_ebm_research_spec_v1.md` | Archive supplied v1 document | Byte-identical copy from ResearchSpec/experiment_A_turnover_conditioned_momentum_ebm_research_spec_v1.md | Scientific authority for A/B | Original preserved; hash-verify copy |
| CREATED | `docs/specs/experiment_B_intraday_volatility_ebm_research_spec_v1.md` | Archive supplied v1 document | Byte-identical copy from ResearchSpec/experiment_B_intraday_volatility_ebm_research_spec_v1.md | Scientific authority for A/B | Original preserved; hash-verify copy |
| CREATED | `docs/specs/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md` | Archive supplied v1 document | Byte-identical copy from ResearchSpec/experiment_B_new_chat_codex_and_diagnostics_instructions_v1.md | Scientific authority for A/B | Original preserved; hash-verify copy |
| CREATED | `reports/shared/D0_data_source_feasibility.md` | D0 implementation/documentation | Stage verdict, exact coverage, storage and next action | User and next stage | New file only; no preexisting user content replaced |
| CREATED | `reports/sessions/20261016_1210_shared_D0_data_feasibility_session.md` | D0 implementation/documentation | This detailed session audit | User and next stage | New file only; no preexisting user content replaced |
| INSPECTED | `AGENTS.md` | Repository instructions, authority and session checklist | No changes | D0 scope | Preserved |
| INSPECTED | `README.md` | Existing project definitions/layout | No changes | D0 scope | Preserved |
| INSPECTED | `.gitignore` | Already ignores credentials and raw/canonical/derived data | No changes | D0 scope | Preserved |
| INSPECTED | `.env` | Credential names/presence only; values loaded privately for authorized headers | No changes | D0 scope | Preserved |
| INSPECTED | `ResearchSpec/*.md (4 files; exact names mirrored in docs/specs above)` | User-supplied research specifications/starters; read active-stage definitions and boundaries | No changes | D0 scope | Preserved |

Created empty local directories `data/canonical/stocks_monthly/`, `data/canonical/spy_minute/`; these are ignored, contain zero bytes and require `mkdir` on a fresh clone. Temporary smoke directories: one per verifier execution under the OS temporary root matching `ebm_d0_smoke_*/smoke.json` (3 executions before this report), automatically removed by TemporaryDirectory. No user intermediates deleted. No binary/Parquet/model file generated. All 15 diagnostic JSON schemas and sizes are in the inventory/manifest; response arrays contain Alpaca bar fields `t,o,h,l,c,v,n,vw` or Massive epoch-ms equivalents.

## 9.3 Critical code/function/variable register

| Path:function | Signature / usage | Purpose, input and output | Algorithm / timing / limitations |
|---|---|---|---|
| `scripts/d0_probe.py:credentials` | `credentials()` | Read environment and simple local `.env` key=value into private mapping | Existing environment wins; simple parser, not a full dotenv implementation; never emits values |
| `scripts/d0_probe.py:request` | `request(url, params=None, headers=None)` | One bounded HTTP request; sanitized status/bytes/body or error | 2,000,000-byte cap; 20s timeout; no retries; never emits credential URLs; HTTP errors store status only |
| `scripts/d0_probe.py:audit` | `audit(bars, day)` | List of bar dictionaries, expected ISO date -> minute/schema/OHLCV QA dict | Expected exact ET-date 390-minute grid; UTC conversion with ZoneInfo; opening count 30; no exchange-calendar generalization |
| `scripts/d0_probe.py:main` | `python3 -B scripts/d0_probe.py PROVIDER --id UNIQUE_ID` | `alpaca`, `massive`, `anchors`, `public`, `details`, `hf-range`; creates dated evidence and ignored licensed samples | Fixed small requests; no pagination/full history; output-exclusive writes; `FileExistsError` protects old evidence. Not a production acquisition/cache layer |
| `scripts/d0_verify.py:main` | `python3 -B scripts/d0_verify.py [--id UNIQUE_ID]` | Read local evidence/raw refs; create small verification and file manifest JSON | Assert hash/size, exact-date grids, OHLCV, prior-close availability; compare 390 minute closes; wrong-date guard; temp I/O. No requests, research features, threshold fitting or inference. Missing raw rows fail intentionally |

Both scripts anchor paths with `Path(__file__).resolve().parents[1]`; no machine path. Verifier is the only code caller of `audit`; probe CLI also uses it. `main` functions are CLI entry points; no package/model consumer exists yet. Standard-library-only Python 3.14.6; no pandas/pyarrow/requests/dotenv/wrds/psycopg2 installed or required for D0.

Critical variables/constants:

- `ROOT` -> both scripts -> portable repository root, path type.
- `ET` -> probe -> `ZoneInfo('America/New_York')`; storage response timestamps UTC, interpretation ET bar start.
- `DATES` -> probe -> `2016-01-05`, `2019-07-15`, `2023-07-17`, `2024-07-15`, `2026-09-15`; fixed representative full sessions, SPY only.
- `MAX_BYTES` -> probe -> 2,000,000 bytes per response, not whole-dataset permission.
- `timeframe=1Min`, `feed=sip`, `adjustment=raw`, `limit=10000`, `sort=asc` -> full Alpaca diagnostics; 09:30–15:59:59 ET endpoints. These raw samples are not approved canonical split-adjusted inputs.
- Adjustment diagnostic -> raw/split/dividend/all on 2024-07-15 09:30–09:34:59 ET, limit 10; future B canonical convention is `split`, matching spec's split-only `adjusted=true`.
- Massive -> SPY 2026-09-15 only, `adjusted=false`, limit 2000; Basic/plan identity is UNKNOWN.
- Prior anchor dates -> probe -> 2016-01-04, 2019-07-12, 2023-07-14, 2024-07-12, 2026-09-14; 15:59 and 16:00 bar starts. Intended previous full-session close uses 15:59, never the 16:00-start bar.
- `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`, `MASSIVE_API_KEY` -> `.env.example` / environment -> secret authentication; values excluded everywhere. `POLYGON_API_KEY` is a supported alias, not configured here.
- `EBM_DATA_ROOT` -> `.env.example`/layout -> future configurable shared data root; **not wired into diagnostic scripts**, which stay in repository data/.
- Dataset/extract IDs -> provider JSON filenames -> diagnostic identities with UTC request timestamps and sample hashes. Full dataset ID proposals are unmaterialized; see layout. Scientific source schema version remains pending.
- A variables/dates -> copied A v1 -> historical security × formation month, monthly total-return predictor/next-month label, contemporaneous volume/historical shares; sealed target-month test 2023-01–2026-09. No transforms run.
- B variables/dates -> copied B v1 -> prior full-session close to 10:00 predictor; sqrt(sum of 30 within-opening log increments squared) state, log guard `1e-8`; target 15:30–16:00 price return; sealed test 2024-01–2026-09. Approved 2016-start fallback: 2016–2021 train, 2022–2023 validation. No research feature/return computed.
- Seeds, model interactions, fit thresholds, trading-cost/materiality parameters: not used or changed; no model initialized. Storage target <1 GB new retained, flag before 2 GB.

## 9.4 Execution and reproducibility trail

Working directory throughout: repository root (`.`). Initial commands (in order):

1. `pwd`; `git status --short`; `git branch --show-current`; `git rev-parse HEAD`; `rg --files -g 'AGENTS.md' -g 'README.md' -g '.gitignore' -g '*spec*' -g '*protocol*' -g 'pyproject.toml' -g '*requirements*' -g 'data/registry/**' -g 'docs/**'`.
2. `cat AGENTS.md README.md .gitignore`; `rg --files --hidden -g '!.git/**' -g '!.env' -g '!.venv/**'`; `ls -la`; `sed -n '100,230p' AGENTS.md`.
3. Inline Python presence-only checks of `.env` key names, matching environment key names, `sys.version`, `shutil.disk_usage('.')`, importlib availability for requests/pandas/pyarrow/dotenv/wrds/psycopg2 and existence of `~/.pgpass`, `~/.pg_service.conf`, `~/.kaggle/kaggle.json`, `~/.netrc`. No values printed. Repeated short check because large prior output was truncated.
4. Inline `urllib.request.urlopen('https://huggingface.co/api/datasets/mito0o852/OHLCV-1m', timeout=15)` network smoke: DNS failed under sandbox; no output retained.
5. `mkdir -p scripts data/registry data/raw/diagnostics data/canonical/stocks_monthly data/canonical/spy_minute reports/shared reports/sessions docs`; `date '+%Y-%m-%d %H:%M:%S %Z'`.
6. Created probe via apply_patch. Network requests then explicitly escalated after sandbox failure; approvals granted. No secret was interpolated into shell commands.

Actual network reproduction commands, in dispatch order (exit 0 each):

```sh
python3 scripts/d0_probe.py alpaca --id d0_20261016_1201
python3 scripts/d0_probe.py massive --id d0_20261016_1201
python3 scripts/d0_probe.py public --id d0_20261016_1201
python3 scripts/d0_probe.py details --id d0_20261016_1208
python3 scripts/d0_probe.py anchors --id d0_20261016_1208
python3 scripts/d0_probe.py hf-range --id d0_20261016_1215
```

Do **not** rerun these exact IDs into existing evidence. Fresh reconstruction uses one new ID and `d0_verify.py --id NEW_ID`; details in `data/README.md`. API URLs/parameters are preserved in public evidence or the script. The per-provider wall times were Alpaca 1.599s, Massive 0.167s, public 0.501s, details 21.135s (includes timeout), anchors 0.735s, HF range 0.460s, excluding tool approval/wait time. There were **27 provider HTTP requests: 26 successful and one 20-second timeout**, plus the initial sandbox DNS-failing smoke. No background task remains.

Inspections after user clarification: `rg --files --hidden -g '!.git/**' -g '!.env'`; `ls -la ResearchSpec`; `rg -n` heading/data/timing matches in both research specs; `sed -n '1,150p'` on both starters; `sed -n '1,245p'` A spec; `sed -n '1,220p'` B spec; targeted `sed -n '160,185p'` and `'185,305p'` A and `'1,55p'` B starter. Some batched tool output was truncated; targeted subsequent reads recovered the active data sections. No inaccessible paper/theory file is claimed read.

One-off local scripts read provider JSON, print sanitized row/status/schema/count summaries, compare September close values, relocate newly generated provider `data` payloads into `data/raw/diagnostics/<id>_<provider>_response_<index>.json`, update sample references/hashes, copy each `ResearchSpec/*.md` byte-for-byte to `docs/specs/` with existence protection and hash equality. Final probe now implements the same ignored-payload separation. Docs, .env.example and this report were created exclusively; no overwrite of prior user artifacts. No retained temporary scripts or logs outside the inventory.

Browser research used public source pages, not credentials: Alpaca historical bars/minute aggregation/disclosures, Massive custom bars/terms, WRDS CRSP overview, Hugging Face dataset card, Kaggle search/candidate pages. Source links and machine-response snapshots are in `docs/data_source_registry.md`; no web claims are promoted to authenticated access.

Final verification commands:

```sh
python3 -B scripts/d0_verify.py
python3 -B scripts/d0_probe.py --help
git diff --check
git status --short
```

Additional inline checks: `ast.parse` on each script; compare configured nonempty secret bytes privately against every authored/archived/registry/report text (counts only); run `git diff --no-index --check /dev/null <file>` per new authored text; `git check-ignore .env data/raw/diagnostics/d0_20261016_1201_alpaca_SPY_2016-01-05_sip_raw.json`; presence-only PostgreSQL/WRDS environment checks; aggregate file sizes with Path.stat. Exact substantial algorithms are in the two retained scripts; hashes and source identity are in the manifest. No pip install or external dependency snapshot was needed (stdlib only).

From a fresh authorized clone: use Python >=3.10 with timezone data; privately configure the three keys via environment or local `.env` based on `.env.example`; create registry/raw parents; run the six bounded CLI commands with a new shared ID; run verifier selecting that ID. Public metadata and vendor data can change, so new observations need new hashes. No WRDS access is implied. Offline verification of the original run requires the original ignored raw files with matching SHA-256.

## 9.5 Tests, quality checks and scientific integrity

- Offline verifier PASS on three executions: 15 sample file SHA-256/byte checks, five exact-date grids (390 unique sorted rows each; 30 opening rows; zero OHLCV/missing/extra errors), Massive 390 regular minutes, five prior-close pairs, exact 390 close overlap (max absolute difference 0), wrong-date regression guard, temporary I/O smoke.
- CLI help and AST syntax PASS. No modeling smoke was relevant: no package/model pipeline exists or changed.
- `git diff --check` PASS for tracked changes (none). New authored-file whitespace PASS (7 files before this report). Immutable source copies contain original Markdown hard-break trailing spaces; broader whitespace check reported those, intentionally preserved rather than altering scientific source files.
- Secret scan PASS, zero configured secret matches in 22 text/evidence files before this report. `.env` and raw samples confirmed ignored. Registry/docs/scripts remain trackable. No credential values printed.
- Duplicate store prevention: no existing input data found; one raw object per distinct request; no train/test/fold/seed/model copies or canonical duplicate created. A/B identities remain separate.
- Not tested: continuous archive coverage, all exchange sessions, DST-transition/half-day logic, corporate-action/ex-dividend correctness, daily-versus-minute close/count reconciliation, source TAQ comparability, WRDS field permissions, fitting/selection/support/inference, costs. Sample QA is not a full scientific data gate.
- Sealed-period observations were accessed solely for authorized timestamp/schema/coverage QA; no target returns, RV states, coefficients, models or performance comparisons were produced. All scientific definitions/dates preserved. No scientific result invalidated because none was generated.

## 9.6 Errors, anomalies, decisions and recovery

| When / operation | Symptom / cause | Action / files / rerun | Unresolved / next safe step |
|---|---|---|---|
| Initial spec inventory | No specs present at first; later user supplied ResearchSpec location | Asked early, continued only expressly authorized access probes, then read relevant documents and hash-copy four files | Resolved; originals preserved |
| Sandbox urllib smoke | `URLError: nodename nor servname provided, or not known`; network sandbox confirmed by successful escalated requests | Requested command escalation; explicit approvals granted; bounded probe scripts succeed | No further workaround or network escalation needed for offline QA |
| HF filter in details probe | `TimeoutError` after ~20s; server/network cause unknown | Recorded null status; no automatic retry or archive download | SPY inclusion/selectivity unverified; rights and row-group investigation needed before acquisition |
| Provider rights/plan checks | Existing account agreements/plan identity not inspectable via returned bars | Stored rows ignored; recommendations conditional on verified diagnostic access only | Do not redistribute; confirm account terms/full range before full acquisition |
| Initial broader whitespace check | Assertion on three existing Markdown hard-break trailing-space lines in copied A source | Preserved source bytes; scoped authored-file check passes | No code error; immutable-source exception documented |
| Environment checks after whitespace assertion | First inline validation terminated before PostgreSQL presence/disk lines | Reran those checks separately; all PGHOST/PGUSER/PGPASSWORD/PGPASSFILE/PGSERVICE/PGSERVICEFILE/WRDS_USERNAME/WRDS_PASSWORD absent | WRDS blocked until secure authorized configuration |
| Portability review | Original offline verifier had no selector for fresh reconstructed evidence alongside archived metadata | Added `--id`, documented restore selection, reran existing offline verifier PASS | No extra network run needed; fresh remote behavior not retested |
| Disk observations | Free space fell from 65.536 GB to 64.3072 GB while own retained additions remained <1 MB | Report measured retained file bytes; unrelated system change suspected, attribution unknown | Recheck disk before larger acquisition; do not attribute global disk movement to D0 |

All deviations were operational fixes within scope: safe standard-library implementation, ignored payload placement, spec archival copies and bounded request IDs. No scientific redesign. Daily/split-adjusted production acquisition remains separate. No quarantined partial dataset or unfinished worker; only failed HF filter status. Last reliable checkpoint: offline D0 verifier PASS and manifest. Resume with stage report and source registry, configure WRDS or propose the small B split/calendar pilot; do not rerun successful network probes unnecessarily.

## 9.7 Resources, Git and handoff

Provider rows **304,952 bytes** retained, 15 ignored files. Public metadata/manifests/QA about 0.34 MB; four spec archival copies **171,800 bytes**; remaining code/docs/report text small. Total Codex-retained material about **0.88 MB** including this report (approximate), canonical/derived data **0 bytes**. User-supplied ResearchSpec originals total 171,800 bytes and are accounted separately from Codex storage growth. No large CPU work, packages, bulk archives, model fits, subscriptions or unattended process. Initial free disk 65.536 GB; later 64.3072 GB, external activity not attributed. Target <1 GB comfortably met.

Ending expected `git status --short`:

```text
?? .env.example
?? ResearchSpec/
?? data/
?? docs/
?? reports/
?? scripts/
```

Tracked diff is empty: all authored outputs are new/untracked; do not blindly add raw data or .env. `.gitignore`, AGENTS.md, README.md and user .env unchanged. No authorized commit/push requested or performed. Supplied ResearchSpec files and their exact archival copies are the only deliberate document duplication; no dataset duplication.

Handoff: read [D0 feasibility](../shared/D0_data_source_feasibility.md), `docs/data_source_registry.md`, `docs/canonical_data_layout.md`, then copied A/B v1 specs. A has no verified provider access; authenticate WRDS/CRSP/optional Compustat for small schema/two-month checks. B has verified sparse 2016–2026 SIP feasibility and one recent Massive overlap, eligible to propose a small split-adjusted calendar/ex-dividend pilot under the already approved 2016-start fallback. Continuous data and research-ready ≥3-year gate remain unproven. No new scientific decision is required for that pilot; absent source-era/rights evidence must retain qualified claim labels. Full acquisition is not started.

Final post-report checks: PASS AST syntax; PASS whitespace on all 8 authored text files; PASS configured-secret scan on 23 text/evidence files; PASS every recorded manifest hash; PASS `git diff --check`. Final Git status matched the six untracked entries above. Measured retained Codex files were 881,644 bytes before this short audit note (about 0.882 MB). Corrected the verifier-execution count in this report to three; no verification result changed.
