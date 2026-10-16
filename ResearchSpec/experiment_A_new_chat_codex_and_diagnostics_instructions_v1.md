# Experiment A — Instructions for the New Implementation / Codex / Results-Diagnostics Chat
## Companion to `experiment_A_turnover_conditioned_momentum_ebm_research_spec_v1.md` | v1.0 | 14 October 2026

**Purpose:** This file governs the **separate** chat that implements and interprets **Experiment A**: published U.S. **monthly turnover-conditioned short-term reversal/momentum**, reproduced and extended with state-dependent Explainable Boosting Machines. The companion research specification freezes the scientific objects and analysis standards; **this file explains how the receiving chat should organize Codex, diagnose execution evidence, handle small exceptions, and return conclusions**. Do not conflate Experiment A with Experiment B (SPY 30-minute closing return/realized volatility).

**First response of new chat:** confirm reading both A `.md` files; restate the one-sentence aim and primary sampling unit; state that **data entitlement/history is the main feasibility gate**; then prepare a tightly scoped **Stage A0** Codex prompt. Do **not** start by training a model or producing one enormous multi-stage Codex prompt.

---

## 1. Responsibilities and authority boundaries

The new chat must:

1. **Treat the scientific specification as authoritative.** Use the Medhat–Schmeling (2022) U.S. monthly source definitions, source Table I/IV benchmarks, post-publication modern test, and exact turnover state. Appendix qualifications in the accepted manuscript and the two `.md` files outrank guesswork.
2. **Break work into short, sequential Codex prompts**, each with explicit filesystem assumptions, deliverables, tests, validation criteria and disk budget. Create the **next prompt only after inspecting actual Codex outputs for the preceding stage** (unless explicitly requested to draft a plan only).
3. **Perform basic but intellectually serious diagnostics** of real results: original-source match, sample/universe integrity, return/share scaling, missing exits, regression inference, support, model baselines, selection, modern OOS and trading costs. Mark what is **proven / suggested / invalid / not executed**.
4. **Use the state-dependent EBM theory correctly.** Distinguish raw scientific conditional means, conditional portfolio sorts, regression projection targets, discretized/continuous turnover, and the current fitted EBM display. Do not transfer source theorems to an incompatible stock panel or native InterpretML bagged path.
5. **Let Codex inspect the user's repository and data if given authority**, without inventing local folders, data entitlements, or completed tests. Never report a research result from an unseen Codex log or fabricated CSV.
6. **Apply approved minor fixes independently** with a logged provenance trail; flag genuine scientific changes for user/design-thread approval.
7. **Return a concise scientific report to the EBM Theory/design chat**, plus a reproducible full report and small artifacts. Scientific negativity and uncertainty are acceptable outcomes. Do not claim trading profitability merely because published historical spreads were positive.

The user deliberately separated the experiment chats from the EBM Theory chat so theoretical discussion can resume without implementation noise. **This chat owns A only**. References to Experiment B are contextual comparisons, not instructions to reuse B's volatility input or target.

---

## 2. Mandatory orientation before writing a Codex prompt

**Read:**

- `experiment_A_turnover_conditioned_momentum_ebm_research_spec_v1.md` **in full**. If inaccessible, request it; never reconstruct from a short conversation summary.
- This instruction file **in full**.
- Repo `AGENTS.md`, README, requirements/lockfiles, Git status, data/audit scripts, current canonical data index and already-existing EBM/SAE modeling artifacts after legitimate repo access.
- Main publication [Medhat & Schmeling (2022)](https://doi.org/10.1093/rfs/hhab055), especially the available [author-accepted PDF](https://openaccess.city.ac.uk/id/eprint/31278/1/MS_short_term_mom_v27.pdf), printed §2.1–2.2/§2.6, Tables I and IV; [Yue, Li & Ruan (2023)](https://doi.org/10.1016/j.pacfin.2022.101920).
- Internal paper guide `state_dependent_ebm_paper1_experiment_theory_v1.pdf` and relevant P2/P3/P6/P7/P8, plus Tasks 19, 22–25 **only when applying a matching sourced argument**. The monograph is a source-navigation asset, not a theorem overriding each original report.

**Mandatory first audit:**

1. What legitimately accessible source covers historical *NYSE/AMEX/NASDAQ ordinary and nonfinancial* stock-months **including firms later delisted**?
2. Does that source provide **actual historical shares outstanding and share volume in documented units**, total returns/distributions/delist results, stable security ID, exchange/eligibility code, and formation market cap?
3. Is Compustat/accounting data actually accessible for Table IV controls? If not, explicitly make `IV2 NOT EXECUTED`; keep `IV1` as a distinct source-style experiment.
4. Do we have enough *months*, not merely rows, before the sealed **2023–2026-09** test? Can this sample do true conditional 10×10 NYSE-breakpoint sorts without empty portfolios? Which honest tier (`A-FULL`, `A-MODERN-BROAD`, `A-MODERN-RESTRICTED`, `A-SHORT-PILOT`, `A-TOO-SHORT`, `A-NO-TURNOVER`) applies?
5. What storage would the new data query/extract retain? Can SQL/remote selection avoid duplicating huge CRSP history or the previous ~25-GB intraday model outputs?

**Source-era access is not assumed.** NYU Stern [WRDS research-data access instructions](https://research.stern.nyu.edu/services/research-datasets) explain registration/eligibility, but the user must actually be entitled to the relevant products. An account alone is not proof of CRSP licensing. Do **not** purchase new data or send vendor-protected raw tables to an external party without authorization.

**Do not advance to A1** when the only “history” is ~2024–2026 30-minute bars on the curated 99 current equities. That supports code QA, not monthly A's substantive hypothesis.

---

## 3. Six staged Codex prompts and explicit gates

Write one exact, copy-paste-ready Codex prompt at a time, **including the inherited `AGENTS.md` rules**, explicit input/output paths once observed, acceptance tests, failure behavior, comments/docstrings and a required end-of-stage Markdown report. Do not duplicate Python pipeline copies where function reuse suffices. All work stays in a small `experiment_A_monthly_turnover/` root adapted to the repository.

### Stage A0 — Repository, historic data and scientific feasibility (**FIRST**)

**Codex tasks:** Inspect existing directories, environment, access permissions (without printing secrets), CRSP/WRDS/vendor entitlement, historical volume and shares, total/delisting returns, ticker/PERMNO identity, intended source sample, pretest-month count, NYSE breakpoints ability and disk storage. Produce data dictionary, retention proposal, source Table I/IV field crosswalk and `A-FULL / A-MODERN-BROAD / A-MODERN-RESTRICTED / A-SHORT-PILOT / A-TOO-SHORT / A-NO-TURNOVER` tier with evidence.

**Accepted only if:** existence/entitlement shown, earliest/latest usable formation and target month reported; stable identity/volume units, share-count and exit treatment feasible; measured independent calendar months and median names per month; no concealed survivorship and no 10×10 with 99 names; disk plan explicit.

**If blocked:** stop and return `DATA_BLOCKED / REQUIRES APPROVAL`. Permitted prototype: synthetic/time-label unit tests or small reference-to-existing-data QA. **No automatic replacement of turnover by volatility, or monthly by 30-minute returns.**

**Output:** `reports/A0_data_go_nogo.md`, `docs/dataset_entitlement_and_survivorship_audit.md`, planned `experiment_A_protocol_v1.yaml` with proposed scientific defaults, list of approval blockers.

### Stage A1 — Canonical monthly security panel and source-era benchmarks

**Codex tasks:** Build one immutable reference to raw data and one compressed security-month canonical table. Join historical security identity, formation-month return/volume/shares/cap and next-month **total return**, handle dividend/delist consistently, record source-style 1963–2018/available-overlap eligibility. Unit tests for lagging, split/share units, adjusted/unadjusted price pitfalls, stale shares, ticker changes and delisted exits. Implement **NYSE-only return-first conditional 10×10 Table I** when justified, and monthwise market-cap WLS **Table IV** with trimmed/standardized inputs, `IV1` and optionally authentic `IV2`.

**Accepted only if:** source-vs-ours law/period/universe/coding table; sign/units/CI/time series for historical benchmark; 10×10 nonempty-cell audit; monthwise FMB WLS not used to forecast same month; features known by formation month end; actual source sample differences preserved. Apparent expected-source failure => investigate QA, **not** tune to force agreement.

**Outputs:** `reports/A1_source_replication.md`, canonical table path/ref, small signed Table I/IV CSVs and plots, leakage/data audit, input hashes, exceptions.

### Stage A2 — Genuine time-safe simple baselines and EBMs

**Codex tasks:** Freeze machine-readable protocol and source hashes; form **train/val/held-out** monthly splits from the spec; predeclare numeric `Z=log(prior share turnover)` and **training-only terciles**, source and EBM transformed X as separate pipelines. Fit naive zero/average, **past-only predictive** analog of Fama–MacBeth, matched linear interaction, smooth spline, additive EBM, and prescribed `(return,turnover)` interaction EBM in ordinal and numerical state forms. Use time-aware model selection and hard resource budgets.

**Accepted only if:** all models have identical target/security/month data, no future standardization/cutoff/regressor, no random row validation crossing years, package version and exact term definitions documented; source-style FMB slopes not slipped into OOS predictions; reasonable seed/complexity checks completed.

**Outputs:** `reports/A2_state_models.md`, compact prediction table, runs/config hashes, parameters, job timing, memory and disk growth.

### Stage A3 — Scientific shape, support and fitted-display fidelity

**Codex tasks:** Compute **total-prediction** return×turnover surfaces and scientifically declared `S(z)`, `D(x,z_H,z_L)` at fixed return/turnover/controls; produce supported continuous and train-frozen categorical comparisons, return first/turnover conditional source-portfolio overlay **as separate targets**, local-bin scientific checks, joint occupancy by months/securities and bootstrap/seed diagnostics. Curvature/sign transition is **hypothesis**, not a forced output.

**Accepted only if:** all four comparison configurations have supported joint X×Z×controls; use month-block inference or explicitly scoped alternative; no term-purification interpretation as intrinsic; mask/abstain for sparse cells; no model-projection shape relabeled raw scientific truth; no arbitrary selected threshold quoted at nominal p=.05.

**Outputs:** `reports/A3_scientific_shapes_and_support.md`, support map, fixed comparison table with intervals and materiality, fidelity checks, figures.

### Stage A4 — Walk-forward sealed test, dependence-robust inference and full-process nulls

**Codex tasks:** Train/tune only on history; evaluate frozen **2023–2026-09** source-style modern signs, monthly rank IC, OOS loss, paired EBM-vs-strongest-simple model improvement with **calendar-cluster** uncertainty. Carry out full-pipeline null tests in the project’s four-stage framework: in-sample fit; full in-sample null reruns; walk-forward OOS; full walk-forward null reruns. Preserve **same calendar-month outcomes/common shocks** as much as the chosen null supports, and explicitly describe any violated exchangeability assumptions.

**Accepted only if:** no sealed-test refits chosen by its results; source-era vs modern conclusions separated; month/asset common shocks retained in scientific uncertainty; full discovery/selection rerun for each null, Monte Carlo resolution reported; null diagnostics not miscalled exact p-values absent warranted exchangeability.

**Outputs:** `reports/A4_walk_forward_and_nulls.md`, sealed predictions, monthwise loss/rank-IC pairs, block CI calculations, null manifest with N draws and limits.

### Stage A5 — Execution-aware economic comparison and final publication/portfolio report

**Codex tasks:** Construct source-inspired reversal/momentum sign orientations, fixed-turnover and EBM forecast-rank portfolios where feasible, long-only/long-short and matched exposures, actual monthly rebalance timing, 0/10/25/50 bps **one-way per-side** assumptions, borrow/delist constraints and valid time-separated position history. Compare to strongest simple state-aware model, zero/random/buy-and-hold and, if justified, source benchmark. Synthesize all result claims, alternative interpretations, peer-reviewed source match and CV-safe wording.

**Accepted only if:** source `high-minus-low` negative low-turnover return is **not mislabeled** positive momentum; costs and turnover actually applied; no ex-post universe or feature search; negative net results and uncertain/non-reproducible theory claims transparent; all six stages have tests and integrity files.

**Outputs:** `reports/A5_economic_value_and_final_report.md`, `reports/experiment_A_final_research_report.md`, copy-ready summary for EBM Theory thread, final input/output manifest, archived Stage A0–A5 reports.

---

## 4. Small implementation-exception policy

**Allowed without asking, but recorded immediately:** WRDS/CRSP table-name/API schema migration, column aliases after unit tests, pagination/network retries, memory-friendly query chunking, canonical directory changes to match repo, minor empty data artifacts handled under frozen drop/abstention rules, correct leap/month-end calendar handling, code-comment or chart fixes, a pinned compatible InterpretML/WRDS client version, reducing seeds/bags/null draws for actual resource limits, and using the **preapproved** `A-MODERN-BROAD`/`A-MODERN-RESTRICTED`/descriptive-only `A-SHORT-PILOT` claims if source-era entitlement fails.

**For each exception record:** `date/stage → exact scientific or engineering change → rationale/evidence → affected targets → files/config hashes → tests rerun → impact on claimed comparability`. If a bug is found after results, **rerun all affected reports**, not only the one plot that exposed it.

**Requires user/design-thread permission BEFORE implementation:**

- Changed 1-month prediction horizon or a different return target; a future 30-minute return is **Experiment B/another study**, not an authorized A fallback.
- A different primary state (historical/realized volatility, VIX, volume not divided by shares, liquidity spread, industry membership) or converting share turnover to daily normalized volume without a separately named sensitivity.
- Switching true-source 1963–2018 universe to surviving 99 names while keeping historical-source language; dropping delist/share-count integrity or changing total return to raw price return.
- Changing 2023–2026-09 sealed test after studying outcomes, redefining low/high states by significance, changing x anchors/materiality thresholds based on the test, or excluding failed dates to manufacture a source sign.
- Removing the strong simple interaction/spline baseline, model-turnover normalization without disclosure, accepting a native EBM path theorem from a different algorithm, expanding primary interaction search or using source Table IV same-month fitted slopes prospectively.
- Initiating a new data subscription/licensing decision or a storage-heavy download without authorization.

**No scientific rescue rule:** If modern high-turnover momentum vanishes, first audit shares/universe/lag/delist/weights and support. If data are valid, **report decay/transport failure or inconclusive evidence**. Do not move the horizon to a better-looking weekly/daily result or select an ex-post winner threshold.

---

## 5. Diagnostic checklist for returned Codex results

For every returned output maintain a **claim-evidence ledger**:

`claim_ID | source-vs-modern | exact target | formation/target timing | universe/exits | month clusters | weighting | baseline | effect + units | interval/p | support | selection level | source/data law | conclusion | next falsification`.

Mandatory warnings:

1. **Table I vs EBM scientific row:** the source's turnover categories are **conditional within past-return deciles using NYSE breakpoints**. A plot at a fixed turnover log-ratio is a *different scientific comparison*. Do not assert identical targets just because both have "low" and "high" labels.
2. **Table IV vs predictive model:** monthly FMB WLS coefficients are fit on already realized monthly Y. An out-of-sample forecast needs coefficients trained on *previous* months. Source t=9.06 is **not** a model test R² or a live alpha.
3. **State precision:** shares outstanding must be historical and consistent with the observed formation-month share volume. A split or stale current share count can manufacture a spurious nonlinearity.
4. **Universe selection:** published samples contained exits, delistings and a broad universe. The selected present-day 99 equities are *not* an unbiased historical sample. In particular 10×10 double sort is impossible/unstable with 99 names per month.
5. **Common month shocks:** a 100-firm×100-month panel does **not** contain 10,000 IID state/return experiments. Use returns/scores aggregated to dates and appropriate month-based uncertainty.
6. **Source vs modern:** significant source t statistics do not guarantee significance post-2018, and failure in China does not imply U.S. failure. We require a modern U.S. test, not cherry-picked historical confirmation.
7. **Projection ≠ raw:** an EBM low-order projection can display nonzero interaction when supported raw science is additive, or miss genuine local raw contrast. `D_F` from full predicted surface is not automatically `D_m` (P3/Tasks 10C and 23).
8. **Continuous vs discretized same state:** a binned EBM numerical turnover feature is not differentiable as a true smooth functional; category averaging can change the estimand and obscure the transition. Compare supported contrasts, not arbitrary smooth splines of bin tables (P2/Tasks 24–25).
9. **Effective support:** large sample rows do not substitute for occupied return×turnover×size cells across **multiple** independent months. Mask absent crossings; zero population support is different from zero sampled row count.
10. **State/shape vs economics:** negative low-turnover winner–loser spread means reversal; the profitable reversal *orientation*, if any, flips signs. Profit requires feasible execution and costs. Predictive rank gains are not causal evidence or guaranteed action value.
11. **Equivalence claim:** nonrejection of a difference is not affirmative stability. A 95% CI must fit completely inside a prespecified materiality bound; otherwise status `INCONCLUSIVE` (P6/Tasks 15/19/22).
12. **Selection and software:** InterpretML bagged scores are not raw-population selected-inference CIs. Project Task 12's selected-true-atom Gaussian pivot and Tasks 17–18's actual greedy-path certificates are scoped to other literal learners and observation laws.
13. **Null testing:** a within-month shuffle of returns across firms breaks firm dependence and may alter conditional support. It is a negative-control diagnostic unless assumptions justify exchangeability; a visually impressive null p value is not mathematical proof.
14. **Baseline:** outperforming state-blind OLS is **not sufficient** for EBM added value; compare against matched information **linear interaction and varying-coefficient spline** and state-aware trading baselines.
15. **Data leak:** future share counts, next-month cap, post-hoc accounting vintage, test-fitted normalization, same-month FMB slopes in test predictions, pooled train/test randomly bagged validation are **invalid**.

If quality checks fail: label the affected scientific outputs **INVALID**, instruct Codex to repair and version/rerun, and **do not** promote plausible-looking figures as provisional confirmed findings.

---

## 6. Reproducibility, storage and repository behavior in EVERY Codex prompt

- **No data duplication:** use WRDS/Massive authorized **narrow column/date queries**, point to original immutable vendor extracts and existing clean data, make **one compressed monthly security-panel table**, and write only compact per-fold/month predictions, models and statistics. Never copy the full historical database into each experiment or recreate the previous ≈25-GB Parquet proliferation.
- **Disk audit before download or fitting:** list largest project files, anticipated new storage, proposed canonical paths. Report net disk growth per stage; flag if retained generated artifacts may exceed **2 GB**. Never delete user's existing files without permission. Deduplicate *outputs* only after preserving audit and checksums.
- **Protocol integrity:** freeze machine-readable `experiment_A_protocol_v1.yaml` once data tier/split/metrics are chosen and **before final test**. Log scientific-source references, code/data/config hashes, source field schemas, dates, root version, `interpret` version, weights, seeds, EBM interaction tuple indices, bin-cutoffs, calendar treatment, per-run resource counters.
- **Tests:** synthetic month-lag tests, share-unit scaling and split fixtures, security ID and delist-return tests, NYSE conditional breakpoint tests, missing accounting-vintage tests, exact time-safe walk-forward predictions, common-month bootstrap/permutation fixtures, deterministic model comparisons and storage/manifest tests.
- **Code standards:** follow `AGENTS.md` Git rules, comments on functions/loops/important variables, docstrings, type hints, no secret commits, tests with a small fixture without full data, logs for known/warnings/Pylance issues, no silent source changes.
- **Credentials:** use configured environment variable/authorized WRDS login methods; don't paste WRDS passwords, `MASSIVE_API_KEY`, bearer tokens, or sensitive raw vendor data into prompts/GitHub/research PDFs.
- **After each stage:** generate a Markdown session report listing **every created/changed file with purpose**, tests and actual outcomes, exceptions, uncompleted branches, protocol changes, source reproduction status, resource counters, and the exact approval/stage gate decision.
- **No hidden background action:** the new chat cannot promise unattended follow-up unless it really invokes an available scheduling tool. It may produce Codex prompts and review shared returned logs, not invent a completed local implementation.

---

## 7. Stage request naming and conversation interaction

Recommended Codex stage IDs, **not full Codex prompts**:

1. `A0_REPO_WRDS_UNIVERSE_AND_HISTORY_FEASIBILITY`
2. `A1_MONTHLY_PANEL_TABLE_I_IV_REPRODUCTION`
3. `A2_MONTHLY_STATE_LINEAR_SPLINE_EBM_BASELINES`
4. `A3_SUPPORT_SHAPE_FIDELITY_AUDIT`
5. `A4_SEALED_WALK_FORWARD_AND_FULL_NULLS`
6. `A5_MONTHLY_COSTS_TRADING_AND_FINAL_REPORT`

After user returns Codex artifacts respond in a consistent form:

`stage → what was actually inspected → PASS / PARTIAL / BLOCKED / INVALID → source/Table-I/Table-IV status → source/modern differences → supported scientific and prediction claims with uncertainty → key exceptions and disk growth → next staged Codex prompt or escalation`.

**Small-exception policy is permission to fix code and log decisions, not permission to rewrite source definitions.** If the entitlement gate establishes no valid CRSP-style turnover panel, stop and ask about legitimate data access rather than delivering a spurious high-accuracy monthly EBM on the 99-stock two-year dataset.

---

## 8. Return package to the original EBM Theory/design chat

At completion provide a **copy-ready Markdown summary** in exactly this order:

1. **Dataset + scientific provenance:** authorized vendor, source/universe restriction, earliest/latest eligible dates, source-era overlap, formation/target month mapping, calendar cluster count, PERMNO/identity and exits, historical shares/outstanding methodology, old NASDAQ adjustment status, Compustat vintage.
2. **Source reproduction:** Table I return-first conditional double sorts/NYSE breakpoints and low−high signed monthwise spreads; Table IV monthwise FMB estimates (uncontrolled/controlled), source published benchmarks, all deviations and confidence intervals. Explicitly distinguish source-era and post-publication periods.
3. **Baseline and model scorecard:** naive, source-style explanatory FMB, **time-safe** rolling/pooled linear, matched interaction/spline, additive EBM, discrete and continuous EBM, controls when real. Include walk-forward OOS rank IC/R²/RMSE/paired CIs and stronger simple comparator.
4. **Scientific state/shape conclusions:** fixed turnover Z/log units, x anchors in documented cross-sectional return-sd, `S(z)` and `D_m`/`D_F` distinct, joint support across firms/months, raw/bin/model contrast evidence, sign/threshold/nonlinearity and multiple-testing status, affirmative/inconclusive temporal invariance.
5. **Dependence/selection and null tests:** calendar HAC/block settings, full-pipeline in-sample/OOS null reruns and Monte Carlo resolution, source of approximation assumptions, sealed test and any contamination.
6. **Trading/economic implications:** executable month-end strategy protocol, turnover/cost scenarios, short/long orientation, random/market/strong state-aware comparators, gross and net uncertainty, observed exits.
7. **Honest claims and CV:** A-H0a–A-H7 statuses, source-era vs modern, supported/failed/inconclusive/non-executed, strong simple baseline result and exactly what **could** be put on a CV without pretending a profit or publication contribution.
8. **Files and decisions:** final reports, small output objects, hashes, exact future scientific questions for theory papers P2/P3/P6/P8, `GO / HOLD / STOP` recommendation and any required user authorization.

The original theory thread should not have to load the entire repository to understand whether the classic U.S. turnover-conditioned phenomenon was replicated and whether an EBM added **new supported scientific detail**.

---

## 9. Final non-negotiable scope

A convincing Experiment A outcome can be: a successful paper-compatible replication, a signed interaction without reliable new nonlinear shape, an EBM that adds no improvement over spline/linear models, a support-constrained or incomplete result, or a genuine modern U.S. change in the phenomenon. **We are measuring those possibilities, not manufacturing a positive new return law.** Full paper comparability requires historical universe/turnover quality. Explicit insufficient-data/blocked status is a valid outcome.

**Keep this chat and its Codex prompts for Experiment A only.** Experiment B has already been handed off separately. Once both experiment chats are running, the EBM Theory/design thread resumes independent theoretical discussion.
