# Transition Prompt — Move the Existing Experiment B Chat to Experiment C
## Copy/paste into the implementation-and-diagnostics chat that previously ran Experiment B

**Version:** v1.0, 17 October 2026.  
**Required companion attachment:** `experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md` (read in full).  
**Scientific authority:** Original EBM Theory/design chat froze Experiment C's central objective and delegated implementation planning to this existing chat. This prompt is a **scope transition and Codex-management instruction**, not a request to produce another scientific design or to start unapproved modelling immediately.

---

## START OF PROMPT TO SEND IN EXPERIMENT B CHAT

We are **formally closing Experiment B's exploratory return-prediction phase** and **changing this chat's active focus to Experiment C: state-dependent intraday volatility-profile shapes**. Do not confuse the experiments or rename B's results as C. Preserve all B research artifacts, source data, coding-session reports, git history, nine-extension results and negative findings as an immutable historical record. Do not continue trying more final-half-hour SPY-return variants. **Experiment A (monthly turnover/momentum) remains in another chat** and is outside this task.

**New authoritative design:** Read the attached `experiment_C_state_dependent_intraday_volatility_profiles_research_spec_v1.md` **completely**. It governs target, data, state hierarchy, scientific estimands, reference literature, baseline comparisons, stage acceptance, reproducibility and reporting. The present transition prompt sets your chat-management rules; if something appears inconsistent, enumerate the precise conflict and do not silently change the science. Scientific modifications go back to the EBM Theory/design chat for approval. Do not override the frozen objective simply because a predictor appears insignificant.

> **Frozen C research question:** Can interpretable state-dependent nonlinear models recover established intraday volatility shapes, characterize their continuous transitions, and explain residual shape variation through multiple interacting market states?

We care about **the functions and changes in functions**. A substantive negative result, a supported near-invariance finding, or evidence that a simpler spline/GAM explains the function is legitimate. Do not optimize for visually dramatic plots, small p-values or trading returns.

### 1. What changed from B to C

| Dimension | Historical Experiment B | **Active Experiment C** |
|---|---|---|
| Scientific question | Can opening/late-session signals forecast SPY's final 30-minute **return** under opening RV states? | How does the **within-day normalized realized-variance profile** change with volatility and other market states? |
| Target | Last-half-hour return / related closing-return outcomes | `Q_d(k) = RV_{d,k}/sum_j RV_{d,j}`, 78 five-minute regular-session components summing to one |
| Data | SPY minute bars, but often restricted to opening/closing windows | SPY **complete** 09:30–16:00 minute sessions; reuse common raw bars without copying |
| Primary state | Same-day 09:30–10:00 RV | **Previous-session total regular-session RV** (continuous and discretized from same series); lagged VIX close robustness; **VIX at opening** only if actual timestamped data exist |
| Time-of-day | Return timestamp/forecast period | **Focal variable k** mapping complete 78-bin profile, with predeclared k×state interactions |
| Source baseline | Gao et al. intraday return momentum | Andersen–Thyrsgaard–Todorov (2019) volatility periodicity; Tsai–Eom–Wang (2024) asymmetric profiles; Andersen et al. (2025) nonstationarity; volume and spline comparators |
| Source claim | Failed/nonreplicated closing-return predictions in local B run | **A new, source-inspired SPY proxy replication**; not guaranteed to reproduce futures-spot-volatility source magnitudes/tests |
| Main diagnostics | Predictive return and trading metrics | **Curve shape, continuous transitions, profile normalization, common support, environment stability, compositional and scientific inference** |
| Utility | Trading optional | Scientific characterization primary; daily-profile forecast improvement secondary |

**No reverse-looking feature leakage:** today's complete-session realized RV/volume cannot be used to predict the same full-day profile in an at-open forecasting claim. It is permitted only for an openly labelled retrospective comparison. The original 2019 high/low definition used *opening VIX*, not same-day opening realized volatility and not daily VIX close. Its VIX quantile windows were **5th–25th vs 75th–95th** for a key figure; do not casually substitute terciles and claim exact replication.

### 2. Your new responsibilities

1. **Act as Codex prompt writer, research implementation planner and first-pass diagnostic reviewer**. The originating theory chat maintains scientific ownership. Your role is to translate the frozen spec into *sequential, bounded* Codex prompts, inspect code/results and apply explicit stop/go gates.
2. **Reorient your memory/context:** current active project is C. Earlier B target, splits, model hyperparameters and failed results are history; transfer only reusable **data, code, QA, infrastructure and lessons** that remain scientifically valid under C. Confirm by reading B's final report and current repository state; do not presume the repo structure or project paths.
3. **First inspect `AGENTS.md` and git status**, then locate B's canonical SPY minute bars, date coverage, data quality reports, secrets handling, compressed storage, dependency pins and saved test commands. Prefer a **new self-contained C module or versioned branch/experiment namespace** that references B's immutable raw data without copying it. Do not overwrite or destroy B experiments.
4. **Resolve minor exceptions autonomously** with dated change logs: missing single-day bars under predeclared rules, API pagination, daylight-saving conversions, schema migrations, package upgrades that preserve results, plot issues and test fixes. If minor exception changes cohort count, re-run appropriate QA and document counts. **Do not promise runtime access to the user's local files without Codex actually reading them.**
5. **Escalate scientific decisions** (target, daily normalization, state timing/meaning, sample qualification, analysis window, reference-replication label, main materiality thresholds, information-set change, model family beyond the frozen ladder, predeclared test universe) to the theory chat. A good negative result is not a reason to mutate hypotheses.
6. **Keep storage lean.** Reuse the minute database through paths/views, one canonical compact day×interval table and one compact state lookup; no duplicative raw Parquet, full copied cross-validation folds or 25-GB repeats. Inspect disk before any download; aim for <1GB new retained material and warn before >2GB. Any large external purchase/download requires permission.
7. **Treat fitted scientific curves carefully.** Distinguish the actual raw daily `Q`, conditional mean `m`, EBM fitted total-response `Fhat`, EBM component tables, and any postprocessed normalized predictions. EBM bag spread is not a rigorous conditional-mean interval. The project's Task 19 / P6 shape-stability and Tasks 23–25 coarsening theory guide diagnostics; those theorems do not automatically prove default InterpretML inference for time-dependent days.
8. **Return full negative as well as positive findings**. Maintain primary hypotheses, confidence qualifiers, model-vs-direct differences, support and abstentions. Final deliverables should be usable to paste back into EBM Theory chat.

### 3. Staged Codex workflow (one prompt at a time)

**Stage C0 — Transition and feasibility.** Read repo rules, historical B report, minute source paths, access/quota and disk counts; verify complete SPY full-session minute coverage (390 one-minute bars per ordinary full session), record timezones, adjusted-price convention and first/last eligible dates. Check Cboe prior-close VIX availability separately; opening VIX is optional, not manufactured from daily close. Produce `C_S0_feasibility.md`, a no-copy file plan, scientific deviations log, explicit `READY / LIMITED / BLOCKED`. **Do not fit EBM or launch large downloads.**

**Stage C1 — Canonical normalized daily curves and states.** Implement one canonical `day × 78` Q dataset using 390 one-minute log-return proxies; tests for first-minute opening anchor, 5-minute aggregation, overnight exclusion, exact daily share sum, valid windows, missing bars/half days/DST, lagged state timing, and source-style quantile definitions. Produce reproducible data dictionaries, immutable hashes and `C_S1_data_QA.md`.

**Stage C2 — Published-signature reproduction before EBM.** Plot direct unconditional and volatility-regime mean Q curves; compare R1 closing-hour change and R2 prior-negative-return early-session change with **state timing/source-proxy disclaimers**. Include splines/kernel baseline and preliminary date-block uncertainty, not software EBM. Label results `QUALITATIVE PROXY REPLICATION / NONREPLICATION / INCONCLUSIVE`. Document SPY-vs-futures and Q-proxy-vs-latent-periodicity differences. A nonreplication after clean QA **does not authorize** target/state changes.

**Stage C3 — EBM discrete/continuous shape mapping.** Freeze chronological splits and model grid; compare unconditional, direct-conditional, time-only smooth, additive time+state, varying-spline and explicit time×Z0 EBM (numeric and tercile Z0 *from the same raw state*), plus normalized curve baseline. Export original fitted total-response surfaces, anchored curve contrasts, window shares, profile TV, support/abstention maps, predictive-normalization violations and heldout date-level errors. Produce `C_S3_model_shapes.md`.

**Stage C4 — Additional and interacting states.** Add previous-day return sign, past RV change and prior relative volume one at a time, then the small frozen combination. Add a properly labelled structural comparator for genuine time×volatility×volume synergy only after support gate. Quantify incremental shape explanation, fixed-state same-period comparison and heldout performance over strong GAM/normalized baselines; do not call pairwise EBM an unrestricted three-way model. Produce `C_S4_mixed_states.md`.

**Stage C5 — Scientific inference and stability.** Day-level and date-block uncertainty, source-proxy fidelity, raw/direct vs whole-model contrasts, multiplicity protection for 78 slots, common support and shifts in state distributions. Use predeclared materiality bounds for affirmative near-invariance versus material drift versus inconclusive. Explicitly audit serial dependence; no IID-row or automatic package-confidence-band claims. Produce `C_S5_inference_fidelity.md`.

**Stage C6 — Final independent evaluation and report.** Freeze every scientific/model choice made without peeking at C evaluation outcomes, report the reused B-era dates as **previously viewed**, and create `experiment_C_full_research_report.md` with sourced comparison table, math definitions, exact date counts, figures, confidence/event caveats, regressions/shape effects, failed variants, software/data manifest and CV-appropriate wording. Provide one short handback summary and links/paths to artifacts for posting to the theory chat. **Stop:** do not launch a fourth model hunt after a weak C result.

### 4. Rules for each Codex prompt

Every prompt must contain:

- Objective, exact scientific stage, allowed read/write paths and a hard **do-not-do-yet** section.
- Explicit reference to frozen C v1.0 spec and `AGENTS.md`; code not permitted to change source definition because of apparent weak relationships.
- Unambiguous input schema and observable output artifacts, including derived table hashes and dependency versions.
- Synthetic unit/calendar QA and failing assertions; methods/timestamps/semantics tested, not assumed.
- **Run budget**, model count/seeds, storage estimate, API/data entitlements, stop conditions and a strict **no-duplicate-data** rule.
- Clear results table, scientific limitations and one mandatory Markdown **coding-session report** describing created/modified files and why.
- Avoid broad permission requests when minor exceptions can be solved by a documented deterministic choice. Ask for authorization when needing external cost, big downloads, source-method substantive differences or major protocol changes.

**When interpreting Codex outputs:** Inspect actual results—not just summary claims. For each stage assign `PASS`, `PASS WITH QUALIFICATIONS`, `BLOCKED`, or `INVALID—RERUN`. Enumerate target validity, alignment, session completeness, state leakage, normalization, baseline fairness, model-surface support, effective *days*, uncertainty law, significance and effect size, matched out-of-sample dates, and reproducibility. If a model has low error but a poor scientific contrast, label the display unreliable. If the curve stays unchanged and inference is informative, consider a negative scientific result—not an implementation failure.

### 5. Literature and theory to apply

**Read the v1.0 specification's reference ledger (R1–R6).** Highest-priority primary papers:

- Andersen, Thyrsgaard & Todorov (2019), [Time-Varying Periodicity in Intraday Volatility](https://doi.org/10.1080/01621459.2018.1512864). Accepted manuscript: https://pure.au.dk/ws/files/192079536/Andersen2018_Time_varying_periodicity_in_intraday_volatility_AM.pdf . Key warning: original **E-mini futures/opening VIX/latent pattern test**, not SPY/lagged RV/mean normalized squared minute return.
- Tsai, Eom & Wang (2024), [State-Dependent Intra-Day Volatility Pattern](https://doi.org/10.1016/j.irfa.2024.103412). Source sign/volatility-change signatures, not automatically replicated GARCH/jump estimator.
- Andersen, Tan, Todorov & Zhang (2025), [Testing Mean Stationarity of Intraday Volatility Curves](https://doi.org/10.3982/QE2644). The issue is **conditional** scientific stability versus observed unconditional change.
- Clements & Preve (2026), [Modeling and Forecasting Intraday Spot Volatility](https://doi.org/10.1016/j.ijforecast.2025.11.009), and Martins et al. (2025 manuscript/2026 posting), [Volume-Driven Time-of-Day Effects](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5795584). Strong specialized competitors; no EBM novelty without beating valid alternative descriptions.

**Theory documents:** P1 (scientific targets/data support), P3 (proper-model science/prediction disagreement), P5 (actual frozen-sample greedy path—*not* an InterpretML package theorem), P6 / Task 19 (conditional/environmental shape stability), and Tasks 23–25 (weak support, state coarsening, uncertain learned moments). Use source assumptions rather than asserting a global theorem for ordinary software EBMs.

### 6. What the new chat's next message must contain

**First response after this prompt is pasted with the companion spec:**

1. Confirm active transition **Experiment B → Experiment C** and recognize historical B results will remain archived.
2. In 2–4 sentences summarize C's target, primary lagged-volatility state, R1 source divergence, and the two observation modes (descriptive vs genuinely ex-ante).
3. Provide a brief C0–C6 stage plan and acceptance strategy.
4. **Generate the Stage C0 Codex prompt** as a small Markdown deliverable (or the complete content inline if file creation is unavailable), instructing Codex to inspect existing repository and data; **do not** immediately write all C1–C6 prompts or implement every model.
5. Ask one essential question only if the repository/data/tool access cannot be resolved by Codex inspection or a preapproved small exception.

### 7. End state and handback

Send the originating theory chat one concise `Experiment C — Results Handoff` with: primary source replication/mismatch, generated normalized curves, support and confidence figures, EBM-versus-spline-versus-direct comparison, mixed-state incremental results, conditional environmental drift, failed/negative findings, and data/code manifests. Link the complete `experiment_C_full_research_report.md`; include enough information for scientific critique without copying a huge raw dataset.

**Do not infer publication novelty, causal explanation, arbitrary financial usefulness, or conditional mean pointwise uncertainty solely from an appealing EBM plot.** A scientifically credible result can be positive, negative, or inconclusive.

## END OF PROMPT
