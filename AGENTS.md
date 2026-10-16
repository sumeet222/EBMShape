# AGENTS.md — State-Dependent EBM Research (Experiments A + B)

> **Scope:** Repository-wide instructions for Codex and other coding assistants working on the shared research repository. This is a **CV / academic research project**, not a production trading service. Prioritize scientific validity, reproducibility, simplicity, efficient storage, and a complete record of every coding session.
>
> **Role:** Codex is an **implementation assistant and auditor of specified work**, not an unreviewed scientific experiment designer. Follow the user's current stage prompt and the approved experiment-specific research specifications. Do not silently redesign a hypothesis, sample, target, state variable, evaluation, or source-replication claim.

## 1. Instruction authority, scope, and work discipline

1. Follow, in order: the user's explicit current instructions and approved decisions; the **authoritative scientific specification for the active experiment**; the accepted stage prompt/protocol; this `AGENTS.md`; then existing repository conventions. If two binding scientific instructions conflict, **stop that part**, describe the conflict and options, and request a scientific decision. Do not infer approval from silence.
2. Read the relevant specification, protocol, and existing code **before** implementing. Inspect first; make the smallest coherent changes. Use established functions/files instead of creating parallel implementations.
3. Work only on the requested stage or task. No unsolicited large data downloads, model sweeps, backtests, feature searches, package overhauls, repository refactors, or cross-experiment migrations. A useful observation can be documented as a proposed follow-up without implementing it.
4. Do not optimize for a positive financial finding. Preserve negative results, inconclusive intervals, data-access blockers, and stronger simple-model baselines. A data-quality failure is a reason to fix or stop, not to adjust the hypothesis or test period.
5. **Autonomy boundary:** Resolve minor engineering details (paths, safe schema adaptations, retries, small test fixtures, compatible package pins) within the stage scope and record them. Get explicit approval for scientific redesign, major resource costs, licensing/subscriptions, destructive actions, or materially larger data collection.
6. **User mode:** If a request begins with `learning mode:`, prioritize a clear walkthrough of the actual relevant files, functions, variables, execution flow, and likely error points. Explain before changing code unless the user also asks for an implementation.

### Binding scientific separation

| Boundary | Experiment A — monthly stock turnover | Experiment B — SPY intraday volatility |
|---|---|---|
| Unit of observation | Historical **security × formation month**, with monthly date clusters | **SPY × eligible trading day** |
| Scientific outcome | **Next-calendar-month total simple stock return** | **15:30–16:00 ET SPY price return** |
| Main predictor | **Immediately preceding month** total stock return | Previous regular-session close to **10:00 ET** return (includes overnight) |
| State | Previous-month **share volume / historical shares outstanding**, then approved log / categories | **Opening 09:30–10:00 realized volatility from SPY one-minute returns**, then approved log / categories |
| Key data | Historic security identity, exits/delists, historical shares, distributions, market cap, exchanges | Complete eligible SPY minute sessions, correct ET timestamps/price adjustments, previous close |
| Sealed final test | **2023-01-01 through 2026-09-30** | **2024-01-01 through 2026-09-30** |
| Source benchmark | Medhat–Schmeling Table I/IV with exact/source-qualified conditions | Gao and Limkriangkrai source-era regressions and volatility-state comparisons |

The project may **share infrastructure and source files**, but must **never** pool these populations, apply the wrong state or target, inherit one experiment's split, or label adapted analyses as exact paper replication. The user intends substantive Experiment A work in a **separate chat**; common infrastructure and shared-data decisions can be implemented from this repository's coordinated setup, while the present implementation chat remains principally for B.

Place the authoritative source documents under `docs/specs/` **if provided in the local repository**. Preserve their versions; do not fabricate missing files. Recommended names include `experiment_A_turnover_conditioned_momentum_ebm_research_spec_v1.md`, `experiment_B_intraday_volatility_ebm_research_spec_v1.md`, and their respective new-chat instructions. File-name suffixes introduced on download may be normalized in the repo with a documented copy/move after confirming identity. This `AGENTS.md` does not override their scientific decisions.

## 2. Recommended repository structure (adapt to what actually exists)

Use one repository and **one shared physical data store**. A and B are separately versioned experiments; they do not require separate copies of vendor extracts, model tables, or utilities. Treat this as a **recommended layout**, not an instruction to create every empty directory immediately.

```text
state_dependent_ebm_research/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example                 # names only; no credentials
├── pyproject.toml               # or one small pinned requirements file
├── docs/
│   ├── specs/                   # read-only approved research specifications
│   ├── data_sources.md          # entitlement, coverage, licenses, provenance
│   └── decisions.md             # approvals / scientific-protocol decisions
├── config/
│   ├── common.yaml              # shared operational settings only
│   ├── experiment_A_protocol_v1.yaml
│   └── experiment_B_protocol_v1.yaml
├── src/ebm_research/
│   ├── common/                   # paths, I/O, calendars, metrics, HAC, QA, plots
│   ├── experiment_a/             # A-specific monthly panel, source sorts, models
│   └── experiment_b/             # B-specific SPY minute RV, source OLS, models
├── scripts/                      # thin CLI entry points, not duplicate pipelines
├── data/
│   ├── README.md                # schema and data retrieval instructions (tracked)
│   ├── registry/                # manifests, dataset IDs, versions, hashes (tracked small files)
│   ├── raw/                     # one immutable source per provider/version (gitignored)
│   ├── canonical/               # one authoritative normalized table per physical dataset (gitignored)
│   │   ├── stocks_monthly/      # eligible A security-month source/canonical view
│   │   └── spy_minute/          # eligible B one-minute SPY source/canonical view
│   └── derived/                 # *small*, explicitly versioned reusable transforms
│       ├── A/                  # e.g., one canonical model-ready monthly table
│       └── B/                  # e.g., one canonical eligible SPY daily table
├── experiments/
│   ├── A/                        # A-only small configs, run IDs, analysis notebooks
│   └── B/                        # B-only small configs, run IDs, analysis notebooks
├── artifacts/
│   ├── A/                        # small predictions, model summaries, figures
│   └── B/
├── reports/
│   ├── A/                        # A-stage results / limitations
│   ├── B/                        # B-stage results / limitations
│   └── sessions/                # mandatory reports for **every** Codex session
├── tests/                        # a few focused synthetic/unit/smoke tests
└── logs/                         # bounded execution logs; secrets scrubbed
```

**Implementation notes:**
- Use Python package imports from `src/ebm_research` and a thin CLI, rather than copying identical code into A and B. Only put a function in `common/` if its semantics genuinely match; different return definitions, weighting, lookahead rules, and clustering belong in experiment-specific modules or explicit options.
- Prefer `python -m ...` / `pip install -e .` to ad hoc `sys.path` changes. Names can be adjusted to an existing repository with a session report documenting the change.
- Git-track small configuration, documentation, code, tests, manifests, and compact human-readable results. Do **not** Git-track raw licensed datasets, huge Parquet files, downloaded archives, credentials, large cached folds, or binary model grids by default.

## 3. Data acquisition: reuse first, one canonical copy, no silent duplication

**Before obtaining data or materializing a new table:**

1. Inspect `data/registry/`, the existing repository, and any authorized external datasets supplied by the user. Identify existing coverage, ticker/security IDs, source versions, adjustment policy, timestamp convention, and whether the exact required fields are already available. Do not presume the old SAE project's files are accessible or contain SPY. An old dataset may be referenced read-only **only after its provenance and compatibility are checked**.
2. Query only fields/symbols/date ranges needed for the active stage. Request metadata or sample days first. Check provider entitlement/terms and credible provenance, especially for community-hosted Kaggle/Hugging Face archives. Never claim to have access to a provider or local path without verifying it.
3. Keep at most **one authoritative copy of each distinct raw source extract**, plus the minimum genuinely useful normalized/derived versions. Reuse these across experiments and across seeds/folds/reruns; store run metadata and predictions, not another copy of the input rows. No full-data copies in `experiments/`, `artifacts/`, notebooks, `runs/`, or each cross-validation folder.
4. Dataset identity must include at least `provider`, `dataset/symbol or universe`, `coverage`, `frequency`, `adjusted/unadjusted definition`, `timezone`, `schema version`, and `content hash` (where feasible). **Never merge two feeds simply because they share ticker and timestamp.** Record corrections/transforms; raw remains immutable.
5. Prefer references, configured filesystem paths, manifests, column selection, partition pruning, and streamed/chunked processing over physical copying. A path reference must not assume one user's Mac location. Symlinks may be a local convenience, never the only portable way to run the project.
6. Existing external licensed data stay external when licenses disallow redistribution. Keep a portable `data/README.md` explaining approved ways to retrieve or point to them; do not falsely promise that a public Git clone includes licensed inputs. Repository reproducibility is **code/protocol portability plus a documented data acquisition/restore procedure**, not unauthorized data redistribution.
7. Prefer compressed columnar storage when useful, and write only columns required for a stable canonical table. Recompute cheap derived features from shared canonical sources when less costly than storing numerous variants. Avoid materializing identical train/validation/test Parquets for each seed or configuration; use **row keys/date masks** and in-memory filtering. Cache an expensive transform only if repeated measured use warrants it and cache provenance is recorded.
8. Before large writes, estimate output size and inspect current disk use. **Default target: <1 GB of newly retained experiment material; flag before 2 GB** unless a stage prompt authorizes otherwise. These are warnings/targets, not scientifically mandated truncation of a legitimate dataset. Stop before unexpected large downloads or duplication.
9. Never overwrite or delete the user's original data. For generated intermediates, deletion is allowed only if their recomputation path is established and the change is within the approved task; list every deleted path in the session report. Obtain permission before deleting preexisting user files or substantial material.

**Candidate data-source register (not approvals):** WRDS/CRSP and optional Compustat for A; Alpaca, historical SPY data from Hugging Face or Kaggle subject to provenance/rights/completeness, Massive free-plan data, and Schwab Trader API for B. Yahoo Finance may be a cross-check but is not automatically adequate for either core target. Verify actual account entitlements, depth, licensing, and data quality; do not infer these from a vendor's advertised archive.

**Data isolation and keys:** A canonical A row must retain an as-of **stable security identifier + formation month** and a next-month label; a canonical B row must retain **SPY + ET trading session** and correct minute/bar anchors. Do not unify them into an ambiguous `returns.parquet` or allow experiment B's 30-minute return convention to overwrite A's total-return conventions. Different source-derived frequency or adjustment policies require explicit dataset IDs.

## 4. Portable, reproducible code

1. **No hardcoded machine paths** (`/Users/...`, absolute home directories), user names, tokens, provider account IDs, or local volume names in code/config. Locate the project root robustly (e.g. `Path(__file__).resolve()` where appropriate), use relative repository paths and optional environment variables such as `EBM_DATA_ROOT`, `EBM_CACHE_ROOT`. Resolve paths with `pathlib`; provide sensible defaults that work from a clean checkout.
2. Keep data outside Git where appropriate, but implement a **simple documented setup**: Python version, `pip install -e .` or a pinned requirements install, copy `.env.example` to local `.env`, configure authorized provider secrets, point to/download data, run a smoke test, and reproduce a documented example. Prefer a small, cross-platform Python stack; add dependencies only when they solve a real need.
3. Pin or record exact **Python and major library versions** for final/reported runs, especially `interpret`, pandas/NumPy, timezone/calendar packages, and statistical packages. Save `python --version`, dependency snapshot (e.g. `pip freeze`), CLI arguments, seeds, configuration/code revision, source-data identity, time range, and outputs. Avoid unnecessary environment managers or containerization unless genuinely needed.
4. Use `zoneinfo.ZoneInfo('America/New_York')` and timezone-aware timestamps for market-session logic; explicitly declare storage timezone and whether bar timestamps mark **bar start or end**. Do not infer ET by adding a fixed UTC offset (DST). Use a real trading calendar for market days/half-days when relevant.
5. Make randomness explicit (NumPy/Python/sklearn/InterpretML seeds as applicable). Identical code/data/config/software should give materially reproducible results; where exact bitwise equality is impossible, document nondeterministic sources and an appropriate tolerance.
6. Commands should work on supported Mac/Linux/Windows systems where dependencies and credentials exist. Do not depend on shell-only GNU utilities or GPU availability for essential functionality. Where a shell command is platform-specific, provide a Python equivalent or clear alternative. No blanket claim that private data are shipped with the repository.
7. Make all pipeline functions **idempotent when practical**: reuse a verified input/cache by dataset ID; avoid appending duplicate rows or duplicating files after reruns. Write outputs safely (unique run IDs / atomic replace for small approved generated outputs), with stable keys and assertions against duplicate records.
8. Use readable functions with short docstrings describing inputs, outputs, assumptions, and information timing; comment **non-obvious** variables, loops and financial/statistical transformations. Avoid excessive comments on trivial Python. Keep a single source of truth for thresholds, targets, date splits, feature names, and model hyperparameters in version-controlled configs.
9. Failure should be diagnosable: raise informative exceptions naming **operation, dataset/config identifier, offending column/date/key where safe, expected vs actual behavior**, and practical next step. Do not swallow exceptions, produce fake default data, or continue after an integrity failure. Use concise bounded logs and never log secrets or licensed raw row dumps.

## 5. Scientific protocol, data integrity, and correct evaluation

- Freeze the relevant `experiment_A_protocol_v1.yaml` or `experiment_B_protocol_v1.yaml` **before** sealed final evaluation. Record intentional versioned changes and rerun affected stages. Minor operational fixes can be logged without changing the science; **scientific changes require approval** and, if warranted, a new protocol version. Never use the sealed test to choose a new target, threshold, model or hyperparameter.
- Keep **source-era replication**, **modern held-out validation**, and **new EBM shape analysis** separately labeled. Be candid about missing historical coverage, incomplete vendor fields and adaptations to the original paper.
- Build features only from information available at prediction/formation time. Check chronology at all joins, rolling calculations, winsorization, categorical thresholds, training/validation/test splits, refit windows, and trading decisions. Do not train or internally early-stop on shuffled rows across future dates.
- **A:** monthly total return and delisting treatment; historical share counts, volume units, identity, NYSE source breakpoints, as-of market capitalization, month-cluster inference. No current shares outstanding substituted into history; no month-`t` Fama–MacBeth fitted slope used to forecast the already realized month `t`.
- **B:** overnight-inclusive prior-close-to-10:00 predictor; actual one-minute opening realized volatility; 15:00–15:30 late predictor only at its permissible decision time; correct 15:30–16:00 scientific target. Thirty-minute bars alone are insufficient to reconstruct the required one-minute volatility state.
- Compare exactly matched observations and an honest simple **state-aware linear interaction / spline or GAM** baseline before claiming an EBM increment. Keep source-model comparators, predictive metrics, scientific shape contrasts, and trading P&L separate.
- Model-output four-point contrasts must be calculated from the **whole fitted prediction surface**, not a single interaction-term chart. Discrete/bin mean, fitted/projection target, raw conditional mean, and economic decision values are different objects. Check joint support and dependence; do not call InterpretML term/bag errors rigorous confidence intervals for raw selected scientific shapes.
- Match inference to the **sampling unit**: A generally uses calendar-month cluster/block reasoning; B has one SPY session per day and may have daily serial dependence. State HAC/bootstrap/null assumptions rather than treating cross-section rows or permuted datasets as automatically IID/exchangeable. Full-process permutations require rebuilding the promised selection steps; shuffled saved forecasts are not a substitute.
- Trading evaluation must use executable **information and execution times**, explicit transaction costs, appropriately constrained baselines, and separate gross/net metrics. Neither a significant association nor a historical source coefficient proves profitability. Do not invent missing spreads, fills, delisting payments, or permissions.

## 6. Tests and audit scope: research-grade, not production-grade

**Protect correctness with a few high-value checks. Do not build an elaborate testing platform.**

Required proportional checks for any materially changed research path:

1. **One fast smoke test:** imports, config parsing, path resolution, ability to read one small representative file or synthetic fixture, and creation of a small output in a temporary location.
2. **Focused deterministic synthetic tests for critical math/time logic only:** for example, known simple returns/basis points, A formation→next-month mapping and turnover scaling, B previous close→10:00 and minute-open RV/timestamp endpoints, DST/half-days where implemented, and chronological split/no-leakage behavior.
3. **Cheap real-data audits when data are available:** row-key uniqueness, required-column coverage, relevant min/max dates, market-calendar alignment, missingness and impossible values, selected hand-checked rows. Do not scan billions of rows repeatedly if a cached invariant or small partition sample can establish the local question; run one full integrity pass when a new canonical dataset is first materialized.
4. **A regression sanity check** when changing a statistical method: compare a tiny reproducible example with a direct hand calculation or a trusted independent baseline. Verify uncertainty/baseline implementations where scientifically consequential.
5. On a bug, add the **smallest regression test** reproducing it and rerun directly affected checks. Do not automatically run entire multi-year backtests and dozens of null repetitions for a documentation/path fix.

**Explicitly avoid** property-testing frameworks, mocked API ecosystems, extensive synthetic-market simulators, CI/CD deployment infrastructure, excessive defensive validation, heavyweight MLOps tooling, and benchmark/test suites whose CPU/Codex cost outweighs research value. Test a critical invariant with a 10-row fixture rather than a large synthetic dataset when possible. Escalate testing only when a documented bug, algorithmic sensitivity, or inference risk justifies it.

For every test report actual command, status, scope, and any skipped test with rationale. A `PASS` on a synthetic toy fixture does not claim the entire real dataset is sound. A scientific failure should stop affected inference; a low predictive score or negative return is **not** a test failure.

## 7. CPU, time, storage, and Codex efficiency

- **Plan briefly, then implement.** At task start inspect what exists, identify the smallest reusable change, and say what you will verify. Do not repeatedly reread huge theory archives when only one assumption or protocol section matters.
- Start with a cheap sample/one date/one configuration; verify correctness before full data processing. Cache genuinely expensive invariant input transformations once, and share by reference. Keep seeds, folds, and model runs from cloning input tables.
- Respect the requested bounded model search. Avoid running extensive EBM hyperparameter grids, five-seed expansions, repeated bootstraps/permutations, or historical full downloads before the relevant stage gate and data QA pass.
- Prefer vectorized/streamed/chunked calculations when they materially save resources; do not over-engineer a distributed computation system for a small SPY daily table or modest monthly panel.
- Record basic wall time and retained output sizes for substantial jobs. Before an operation expected to consume large CPU, network quota, or >2 GB incremental disk, explain the cost/alternative and obtain approval if outside the current authorization.
- Do not leave unattended loops, background workers, scheduled tasks, data polling, or automatic large retries unless specifically requested and technically supported. Apply capped retries/backoff to API calls; stop on entitlement errors.

## 8. Git, secrets, and safe changes

- At session start record branch, `git status --short`, current commit (if any), and whether the workspace is already dirty. Preserve preexisting uncommitted changes. Use a focused feature/stage branch if the user/stage requests it. Do **not** reset, force-push, overwrite unrelated changes, rewrite history, delete branches, or commit/push without authorization.
- Make cohesive, reviewable changes. Check `git diff --check` and relevant diffs before finishing. If commits are authorized, use short descriptive commits tied to a stage; never commit secrets or large data. Do not `git add .` blindly.
- Provide `.gitignore` rules for `.env`, keys, caches, notebooks' large transient output, raw/derived datasets, large artifacts and logs while retaining lightweight docs/manifests. Ensure tracked `data/README.md` and small registry files remain trackable despite data-directory ignores.
- API tokens belong only in environment variables or approved local secret stores. Never echo credentials into logs, prompts, reports, stack traces, or Git. Respect WRDS/CRSP/Compustat and other source licenses; do not mirror licensed raw data to public repositories or unauthorized hosting.
- No deleting, overwriting, renaming, or moving preexisting user artifacts outside the authorized scope. Document exact effects and recovery path for any authorized deletion or migration.

## 9. Mandatory detailed Markdown report **after every Codex session**

**Non-negotiable:** Every Codex session—successful, partly successful, blocked, interrupted, or failed—must conclude with a **new, detailed, human-readable Markdown report** under:

`reports/sessions/YYYYMMDD_HHMM_<experiment-or-shared>_<stage-or-task>_session.md`

Use a unique timestamp/ID (timezone specified), never silently overwrite a past report. If errors prevent normal completion, write the best possible **failure/recovery report before stopping**. If the task makes **no code changes**, still record inspections, commands, evidence, conclusions, and next action.

**Report must contain enough information to reproduce the actual work and diagnose an error without guessing what Codex changed.** At minimum include all the following sections:

### 9.1 Session identification and verdict

- Session ID, local date/time/timezone, agent/model if known, experiment `A` / `B` / `SHARED`, exact task/stage, user instruction or prompt file, starting/ending Git branch and commit, preexisting dirty state.
- Objective, initial assumptions, work completed, work not completed, clear `PASS`, `PASS WITH QUALIFICATIONS`, `BLOCKED`, or `INVALID—RERUN` **for the stage's implementation/QA**, separately from any scientific effect conclusion.

### 9.2 Exact file inventory (required even for failed sessions)

Use a table with columns:

`Action (CREATED / MODIFIED / DELETED / MOVED / INSPECTED) | repository-relative path | why | what changed (functions/config/data/schema) | critical dependencies/consumers | recovery note`

- List **every created, modified, deleted, and moved file**, including tests, data products, configs, notebooks, small reports and generated intermediate files; group huge numbers of mechanically created partitions by **explicit glob/count and manifest** rather than silently omit them.
- For deleted files give original paths, deletion reason, whether tracked, and restore/rebuild instructions. For moved files give both old and new paths. For modified code identify major sections or diff references. Distinguish user files from Codex-generated intermediates.
- `INSPECTED` entries need only cover consequential existing files/data sources (not every import/library file). If a produced binary is untracked/ignored, include its exact path, schema/shape/size and creation command.

### 9.3 Critical code/function/variable register

Record, for **each important newly introduced or materially changed function/class/script**:

`path:function or class | signature / CLI usage | purpose | input columns/types and source | output columns/types/artifacts | key algorithm/equations | external callers | assumptions/information cutoff | exceptions/known limitations`

Also list **critical variables/config keys/constants** by `exact name → file → meaning/units → allowed range/default → where used`. Include at least dates, symbol/universe, return and state definitions, timezone, split boundaries, adjustment policy, seed, model interaction declaration, materiality/cost assumptions, and output dataset IDs **when relevant to the session**. Do not document every loop index/local temporary variable. Provide enough detail that a future agent knows what matters and where to look.

### 9.4 Execution and reproducibility trail

- Exact commands executed and their order, working directory (portable repository-relative representation), environment/Python/dependency versions when relevant, CLI arguments, seed(s), config paths/versions/hashes, input provider/dataset ID/date range/schema/identity, and output IDs/paths/hashes when appropriate.
- For a substantial script, give the concise run command needed to reproduce it, and record exit status, wall time, output size, and a bounded path to relevant logs. Include sample subset and whether commands reached external APIs. Never include secret values.
- Explain how to start from **a fresh clone on another machine**: install dependencies, configure secrets/data root, obtain authorized inputs or select matching cached files, and run the smallest verification/reproduction command. If a vendor entitlement is required, say so.

### 9.5 Tests, quality checks, and scientific integrity

- Tests/audits run, exact commands, what was checked and what **was not**, pass/fail counts, relevant warnings. For failed checks show the expected/actual difference with a safe small example or pointer to sanitized logs.
- Note data-leakage/timing checks, row keys, source comparisons, support and chronological split validation **only to the extent applicable**. Explicitly identify results invalidated by an error; don't keep them as confirmed evidence.
- State whether user-specified scientific variables, dates, source protocols, and A/B separation were preserved. Distinguish a passed implementation check from a supported scientific hypothesis.

### 9.6 Errors, anomalies, decisions, and recovery

For every meaningful error or nontrivial exception, record:

`when / command / file+function+line if available / symptoms+error excerpt / suspected or confirmed cause / fixes attempted / files affected / tests rerun / unresolved issue / shortest safe next step`

- Include package/import/Pylance warnings that matter, API failures and permissions, incomplete downloads, temporary directories, partial outputs, dirty-worktree issues, and unexpected disk growth. Mark confirmed versus suspected causes.
- Record any change from the planned task and whether it was **approved**, **allowed minor exception**, or **NEEDS SCIENTIFIC DECISION**. Never silently change a frozen protocol to work around disappointing model results.
- Give explicit **resume/recovery instructions**: last successful command/checkpoint, which outputs can be trusted, which partial outputs are quarantined, and the next command or file to inspect. Do not claim unfinished tests were completed.

### 9.7 Resource and Git summary; next handoff

- New bytes by major data/artifact category (reasonable approximate values OK if labeled), retained vs temporary data, duplicated copies found/prevented, disk budget status, large CPU/API work actually performed, and pending expensive work.
- `git status --short`, diff summary, authorized commits (if any), untracked/ignored files requiring attention. State if any preexisting user changes were preserved.
- **Handoff to the next Codex session or ChatGPT review:** one-paragraph technical summary, validated results, blockers, exact files to read first, unmade scientific decisions, and a small proposed next stage. Link the relevant stage scientific report separately when one exists.

**Use concise tables and practical details, not thousands of lines of pasted logs.** Keep full logs in small local files with paths where warranted, and quote only diagnostic excerpts. The goal is a trustworthy audit trail with **low engineering overhead**—the report describes the work already performed; it is not a request to invent a complicated telemetry framework.

At the end of the Codex chat response, provide the path to the **session report**, principal files changed, test verdict, storage change, and any blockers. Do not omit the report just because the task failed.

## 10. Starting / ending checklist

**Before coding:**
- [ ] Identify active scope: `SHARED`, `A`, or `B`; read the binding scientific spec/protocol and requested stage.
- [ ] Inspect relevant existing code/data; check Git status and existing source/derived files; plan zero-duplication reuse.
- [ ] Check likely data entitlement, storage and CPU impact; avoid unnecessary work.
- [ ] Confirm any unresolved *scientific* ambiguity that would change the experiment; otherwise proceed with safe operational defaults and log them.

**Before ending:**
- [ ] Confirm no A/B target/state/date mix-up, future-data leak, secret exposure, or license breach.
- [ ] Run only the proportionate tests directly relevant to the change; check the diff and report failures accurately.
- [ ] Account for every created/modified/deleted/moved file and important function/config variable.
- [ ] Record exact run/reproduce steps, source/version/seed, data references, outputs and disk growth.
- [ ] Write the mandatory Markdown session report, including failure recovery and scientific caveats if applicable.

---

**Operating principle:** *Build the minimum credible research implementation; audit the parts that can invalidate scientific conclusions; reuse data and code rather than cloning them; leave enough evidence that another machine or coding agent can reproduce, inspect, and repair the work.*
