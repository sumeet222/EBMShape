State-Dependent EBMs: Experiments A + B
A reproducible, CV/research-grade investigation of state-dependent nonlinear financial relationships with Explainable Boosting Machines (EBMs), anchored in published results and compared against strong simple statistical models. This is not a production trading system. Negative replications and inconclusive findings are valid research outcomes.
The repository holds two scientifically separate experiments with shared data management and lightweight reusable tools. This implementation thread coordinates initial shared infrastructure and data acquisition, then focuses on Experiment B. Experiment A's substantive modeling and evaluation are managed separately.
Studies at a glance
	Experiment A — monthly turnover	Experiment B — intraday volatility
Market	Historical U.S. ordinary nonfinancial equities	SPY ETF
Observation	One security–formation month	One eligible SPY trading day
Predictor	Formation month's total stock return	Prior session close → 10:00 ET SPY return
State	Formation month's share turnover: shares traded / historical shares outstanding	Opening 09:30–10:00 ET realized volatility from one-minute SPY returns
Response	Next month's total simple stock return	15:30–16:00 ET SPY price return
Sealed final test	2023-01-01 through 2026-09-30	2024-01-01 through 2026-09-30
Main literature	Medhat & Schmeling (2022); Yue, Li & Ruan (2023)	Gao et al. (2018); Limkriangkrai et al. (2023)


Do not substitute A's turnover for volatility, B's intraday price return for total monthly return, or mix the samples, units, source benchmarks, protocols, and test dates. An EBM is a scientific extension, not the original papers' estimator. The canonical study definitions and permitted fallbacks reside in versioned specifications under docs/specs/ once added.
Proposed repository layout
.
├── AGENTS.md                 # Required instructions for Codex
├── README.md
├── .gitignore
├── .env.example              # Credential variable names only; add if needed
├── pyproject.toml            # Lightweight dependencies; add when implementation begins
├── docs/
│   ├── specs/                # Frozen A and B specifications and handoffs
│   ├── data_sources.md       # Provider/license/coverage decisions
│   └── decisions.md          # Approved scientific and data decisions
├── config/
│   ├── common.yaml           # Shared operational settings
│   ├── experiment_A_protocol_v1.yaml
│   └── experiment_B_protocol_v1.yaml
├── src/ebm_research/
│   ├── common/               # Shared I/O, calendars, validation, metrics if useful
│   ├── experiment_a/         # A-only monthly features and source benchmarks
│   └── experiment_b/         # B-only SPY minute features and source benchmarks
├── scripts/                  # Thin entry points
├── data/
│   ├── README.md             # Download/rebuild instructions (tracked)
│   ├── registry/             # Small provenance/manifests (tracked)
│   ├── raw/                  # Immutable vendor extracts (ignored)
│   ├── canonical/            # ONE authoritative table per underlying dataset (ignored)
│   │   ├── stocks_monthly/
│   │   └── spy_minute/
│   └── derived/
│       ├── A/                # One reusable model-ready security-month table
│       └── B/                # One reusable model-ready SPY daily table
├── experiments/A/            # A-only run configs/notebooks
├── experiments/B/            # B-only run configs/notebooks
├── artifacts/A/              # Small A result files and figures
├── artifacts/B/              # Small B result files and figures
├── reports/
│   ├── A/                    # A-stage reports
│   ├── B/                    # B-stage reports
│   └── sessions/             # Mandatory detailed Codex-session reports
├── tests/                    # Focused scientific-risk tests (not production test suite)
└── logs/                     # Transient logs (ignored)
The tree is a plan, not a request to create empty directories immediately. The root AGENTS.md governs all agents. Each approved stage should make only the directories and files it needs.
Data: acquire once, reference many times
- A: Prefer authorized WRDS/CRSP historical security data (including historical share counts, distributions, stable IDs and delistings); assess Compustat only for source-style controls. Validate legitimate alternatives before using them. Modern surviving-stock OHLCV is not equivalent to the historical CRSP universe.
- B: Evaluate SPY one-minute bar availability, provenance and timestamp completeness from Alpaca, Hugging Face, Kaggle, existing Massive free entitlement and Schwab. None is considered validated or downloaded merely by appearing in this list.
- Shared vendors can live under data/raw/ once, with one canonical representation and small manifests. Experiments read that data rather than copying it per run, seed or fold. Keep any permitted references to preexisting datasets read-only and provenance-checked.
- Do not commit raw data or licensed vendor extracts. The tracked data/README.md and data/registry/ should describe exactly how an authorized user can reconstruct the dataset. Never place credential values in Git.
- Before materializing a new dataset, check whether a compatible canonical version already exists. Prefer minimal columns, reasonable compression, small derived tables and compact model/prediction outputs. Record storage growth; no uncontrolled large folders.
Workflow
1. Set up Git and AGENTS.md; add the authoritative source documents under docs/specs/.
2. Audit provider access and licensing without bulk downloading. Verify source dates/fields and select viable honest research tiers for A and B.
3. Acquire only approved minimal raw data and create canonical datasets with targeted timestamp, return, turnover and leakage QA.
4. Implement source replications, then small predeclared simple baselines and EBMs, then scientific shape/support checks, sealed walk-forward inference and economic evaluation within each experiment's separate protocol.
5. Keep final scientific reports distinct, while reusing shared code only when the calculations and assumptions match.
Reproducibility and portability
Use relative paths anchored to a project root, environment variables for API credentials and configurable external data locations, a documented Python version and pinned dependencies, explicit random seeds and machine-readable protocols. Another machine should be able to clone the repository, install dependencies and rebuild authorized data from documented sources. The data themselves may require independent entitlement and are intentionally not distributed in Git. Do not assume a specific Mac directory, existing SAE repository or a preinstalled virtual environment.
Testing standard
Spend engineering and compute effort in proportion to scientific risk. Small tests for source calculations, time alignment, leakage, splits, corporate-action/share-unit handling, deterministic repeatability and essential inference are valuable. Avoid extensive synthetic-model test batteries, production orchestration, unnecessary abstraction, redundant model sweeps or heavy test infrastructure. Record test outcomes and explicitly preserve unresolved limitations.
Mandatory report after every Codex session
Save a detailed Markdown report in reports/sessions/, even on error or partial completion. Include the task/stage, Git state and commands, all files created/changed/moved/deleted (with purposes), critical functions and variables/parameters, data inputs and outputs, hashes/versions where relevant, tests and exact results, errors and attempted fixes, resource/disk changes, scientific deviations, and concrete instructions to reproduce or resume. See AGENTS.md for the binding checklist.
Status
Initial repository setup / pre-data acquisition. No data entitlements, downloads, model fits, historical replication, modern predictive results or trading performance are claimed by this README. Start with an access-and-coverage feasibility audit, not a large download.