# D2.1c — First Hugging Face archive: actual download and native-price repair

**PARTIAL — PASS WITH QUALIFICATIONS.** The explicitly requested first archive was downloaded and used to create **39 actual missing-minute repairs**. This new optional view uses `mito0o852/OHLCV-1m` **native prices with factor1**, replacing the earlier scaled-pitrading alternative when explicitly selected. **These are the same39 keys, not39 additional recoveries.** Relative to immutable Alpaca-only D2, missing minutes fall104→65 and primary-eligible full days increase2,673→2,675. Relative to D2.1b, the eligible population is unchanged and the source/price definition differs.

All original Alpaca data and the prior repair are preserved. No full composite copy, model, production daily feature table, scientific regression, target-return selection, state threshold or trading evaluation was created. Experiment A remains on hold.

## Access, limits and source identity

User instruction: **“check the first huggingface dataset with over300mb file download. Use it to fix the data before ending.”** This explicitly authorizes the one332.44MB temporary download, overriding the earlier150MB temporary-file cap for that file. The prior500MB aggregate transfer allowance remains. The maximum occupied temporary allocation was336.59MB; additional sparse range projections occupied less than14.50MB each and were deleted one at a time.

Source: [mito0o852/OHLCV-1m](https://huggingface.co/datasets/mito0o852/OHLCV-1m/tree/776328445b7ac6e7815ef3a483e9c8ded1eb6d56), pinned revision **776328445b7ac6e7815ef3a483e9c8ded1eb6d56**, monthly `data/ohlcv_YYYY-MM.parquet`. The uploader attributes the source to Finnhub; that upstream lineage and redistribution rights are **not independently verified**. No declared license was found in the retained card/file listing. This is explicitly user-directed **private** access/repair, not approval to publish raw data or an exact SIP/source-replication claim. No paywall/gate was bypassed, subscription purchased or token disclosed.

The immutable baseline is `B_alpaca_sip_SPY_1m_split_D2_v1`. The new optional delta is **B_spy_hf_source1_D2_1c_v1**. The prior **B_spy_hf_repair_D2_1b_v1** remains a separate alternative; **never union both**, because their39 keys overlap.

## Full-file download and selective follow-up

June2023 was downloaded in full as requested: **332,444,106 bytes**, HTTP200, SHA256 **fef946f15a7a7159cda0bf59b3f92e244464fa96a976f57d5b43b55b757c5a9b**. It contains **26,538,286 rows in26 groups**, including **16,592 SPY rows** in groups11/12. After exact SPY/context filtering only40 nearby source rows were retained. All four missing June5 opening minutes are also absent from this source; close agreement on neighboring candles does not create missing observations.

That full object was deleted immediately after extraction. The first full read demonstrated actual SPY placement; remaining months then used true selective reads: retrieve footer, read ticker columns to locate actual SPY groups, fetch only those groups' remaining columns, filter exact gap contexts and remove the sparse projection. This avoids pretending byte-range support alone gives ticker pushdown.

| Month | Remote object bytes | Actual new body bytes | Context rows retained | Context bytes | Method |
| --- | ---: | ---: | ---: | ---: | --- |
| 2016-02 | 271,508,411 | 12,738,094 | 49 | 6,234 | Ticker-first ranges |
| 2019-08 | 290,814,381 | 12,956,672 | 82 | 7,019 | Ticker-first ranges |
| 2020-03 | 400,244,796 | 13,950,796 | 160 | 9,589 | Ticker-first ranges |
| 2021-05 | 377,857,860 | 14,067,302 | 40 | 5,904 | Ticker-first ranges |
| 2023-06 | 332,444,106 | 332,444,106 | 40 | 5,976 | Full file |

Retained source contexts total **371 rows /34,722 bytes**, covering the eight original gap dates plus nearby diagnostic observations. They are small ignored source evidence, not a full monthly SPY store. Contexts include some extended-hours observations from the ±20minute selection; these are excluded from regular-session comparisons and never used as a fictitious right neighbor after15:59. Exact required timestamp coverage was checked against the original104-key CSV.

Full June object and all four sparse temporary files/directories are gone. The largest **logical** sparse file was400,244,796 bytes (March2020), but only14,487,552 bytes were allocated for its fetched ranges; no400MB March object was downloaded. No archive clone or datasets cache was created. Complete remote-object SHA256 is claimed only for June; other months have pinned revision, footer and per-range response hashes plus retained-context hashes.

## Local timing, price basis and per-cluster evidence

Actual source timestamps are **aware UTC nanoseconds**, consistent with the card's minute-start convention. Zero-shift prices/returns are compared with ±1minute alternatives using original Alpaca windows and the already-retained76 diagnostic neighbor rows. No extra Alpaca requests were needed. No naive-clock localization, interpolation, additive fit, or fitted price factor was applied. The accepted OHLC values and volume are copied from source1 without scaling.

The original screening limits remain:≥10 overlap closes, median close error≤2bp, p95 close error≤5bp, p95 matched one-minute return error≤8bp. All four OHLC p95 errors also pass5bp. Accepted source rows have positive finite internally valid OHLC and positive finite volume, unique keys and pre2024 dates. Source trade counts/VWAP do not exist; their repair columns remain null. No volume scaling, daily-close substitution or target-outcome-driven choice.

| Cluster ET, bar starts | Original missing | Actual source1 candidates | Accepted | Matched closes | Close median /p95 /max bp | Matched-return p95 bp |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| 2016-02-02 11:19–11:27 | 9 | 9 | 9 | 40 | 0.000 / 0.513 / 2.610 | 0.478 |
| 2019-08-12 15:29–15:30 | 2 | 2 | 2 | 32 | 0.000 / 1.755 / 5.557 | 0.695 |
| 2019-08-12 15:32–15:59 | 28 | 28 | 28 | 29 | 0.003 / 2.224 / 5.557 | 0.695 |
| 2020-03-09 09:35–09:48 | 14 | 0 | 0 | 16 | 0.000 / 2.501 / 4.644 | 3.481 |
| 2020-03-12 09:36–09:49 | 14 | 0 | 0 | 16 | 0.000 / 1.333 / 3.544 | 1.628 |
| 2020-03-16 09:31–09:44 | 14 | 0 | 0 | 16 | 0.000 / 2.425 / 5.359 | 5.864 |
| 2020-03-18 12:57–13:10 | 14 | 0 | 0 | 0 | — / — / — | — |
| 2021-05-05 11:27–11:31 | 5 | 0 | 0 | 0 | — / — / — | — |
| 2023-06-05 09:52–09:55 | 4 | 0 | 0 | 40 | 0.000 / 0.245 / 7.467 | 1.516 |

February2016 has20 pre-gap and20 independent post-gap matches. August2019 has **11 available pre-gap matches**,20 independent matches from14:35–14:54ET and the original15:31ET bar. The source archive lacks some other minutes that Alpaca observed; those original observations remain authoritative and are not removed. The local matched sample for the terminal cluster is smaller because its ±20minute window begins later. No assumption of full source-month completeness follows from any match count.

For February, relative close-ratio SD is0.439bp and median source/Alpaca volume ratio1.000. For the first August cluster the relative ratio SD is1.137bp and median volume ratio0.999745. Raw/native close levels pass without a fitted multiplier. The diagnostic pre-gap ratio is stored but **not applied**.

**One-sided terminal qualification:** There is no same-session right neighbor after15:59. The original15:31 overlap differs by5.557bp at the close, and observed local maxima reach5.904bp high and10.767bp low. These maxima are reported, not hidden; p95 and matched-return screens pass. The first repaired15:32close joined to original15:31 produces a4.167bp log step. Terminal repaired bars have legitimate internal OHLC/positive volume and a nonconstant price path; independent earlier overlaps support a compatible local native basis. All28 terminal rows remain flagged for greater source uncertainty. This is an optional sensitivity repair, not proof of exact consolidated-feed equivalence.

All **65 remaining original missing keys are absent** from the correctly timed source1 extracts. No artificial or shifted row was inserted to fill them. Neighboring close agreement, especially in June2023, can be consistent with shared feed/processing lineage and is **not proof of provider independence**. Absence does not establish market halts or another missingness cause.

## Resulting source view and unchanged baseline

| Quantity | Immutable Alpaca-only D2 | Optional first-source view |
| --- | ---: | ---: |
| Expected regular starts |1,049,610|1,049,610|
| Observed regular minutes from original QA plus accepted keys |1,049,506|1,049,545|
| Missing minutes /clusters /dates |104 /9 /8|65 /6 /6|
| Complete full sessions, out of2,680 |2,672|2,674|
| Complete91-window /opening30 inputs |2,675 /2,676|2,676 /2,676|
| Valid15:29 /15:59 /prior-full close |2,679 /2,679 /2,678|2,680 /2,680 /2,679|
| Primary eligible full days |2,673|2,675|
| Train /validation /sealed eligible |1,493 /497 /683|1,495 /497 /683|
| View rows |243,804|243,843|

New eligible dates relative to original D2: **2019-08-12 and2019-08-13**. February's9 restored midday bars improve full-session completeness, not scientific eligibility. No opening-RV exclusion is recovered. Leading2016-01-04 prior-close exclusion and21 half-day exclusions persist. All683 sealed-test full days and every original Alpaca column remain unchanged.

Remaining clusters:2020-03-09 09:35–09:48;2020-03-12 09:36–09:49;2020-03-16 09:31–09:44;2020-03-18 12:57–13:10 (14minutes each);2021-05-05 11:27–11:31 (5);2023-06-05 09:52–09:55 (4), allET. Largest14minutes, four ties. Full key lists and statuses are tracked. **104=39accepted+65unavailable**, zero invalid/rejected source1 candidate rows and no duplicates.

The new first-source delta and earlier pitrading delta cover exactly the same39 keys. Their repaired closes differ by median0.119bp, p950.520bp, maximum0.708bp. These are data-source differences, not additional repaired days or an evaluated scientific effect. Old repair files remain immutable alternatives; no data copy was made per seed/fold/model.

## Artifacts, usage and checks

New patch: `data/patches/B/B_spy_hf_source1_D2_1c_v1.parquet`, **39×30 columns,22,077 bytes**, SHA256 **398141da0889940fb03dcbe0faea29c5abd50da8fdc7d1e5deec7c0ed6f85172**. It records provider/revision/URI/group, raw-context hash, per-range-manifest hash, native adjustment factor1, UTC timestamp method, source qualification, acceptance status and terminal flag.

[Manifest](../../data/registry/D2_1c_hf_repair_manifest.json), [all original-key decisions](../../data/registry/D2_1c_hf_repair_decisions.csv), [comparisons and timing alternatives](../../data/registry/D2_1c_hf_comparisons.json), [remaining65 keys](../../data/registry/D2_1c_hf_remaining_candles.csv). Shared source/layout documentation now records the new optional version.

```python
from pathlib import Path
from ebm_research.experiment_b.repair import load_minutes
original = load_minutes()  # unchanged Alpaca default
source1_view = load_minutes(repair_manifest=Path('data/registry/D2_1c_hf_repair_manifest.json'))
```

The existing loader enforces original manifest/source/missing-registry and patch hashes, exact original-missing keys, source validity, UTC/pretest dates and strict collision rejection. No new loader or full composite storage was introduced. Default rows remain243,804; explicit first-source view has243,843. Two real loads were identical, all original columns match the original-only view, and all32 registered original files pass hashes. A real key-grid pass independently reproduces2,675 eligible full days. **Seven focused tests pass**,1.914s; no new test framework, model or package.

## Costs and next stage

This session read **386,156,970 HTTP body bytes**, including the requested332.44MB full file. Including prior repair work: **413,874,880 bytes**, below500MB by86,125,120 bytes. There were **136 successful external requests**:1full HTTP200 and135 HTTP206 range reads, no errors/retries. TLS/headers/redirect overhead is unmeasured; body counts are not falsely presented as exact wire traffic. Acquisition/extraction took **62.335s wall /7.282s CPU**; patch publication and real QA took8.814s wall. Existing packages were reused. All five temporary files were deleted.

**56,799 bytes** of new price data remain:34,722 contexts +22,077 delta. Only small code/config/metadata/reports add storage; exact total is in the [session report](../sessions/20261016_1508_B_D2_1c_source1_repair.md). No full monthly or full composite Parquet remains.

**PASS WITH QUALIFICATIONS for the requested download and first-source repair.** Further repairs of the remaining65 minutes are blocked by actual source1 absence, not the former300MB spending cap. Keep original-only and source1-composite views separately auditable. A later Stage1 instruction must predeclare its principal/sensitivity source before financial results; this task does not choose it based on predictions. Source1 licensing/provenance and one-sided closing qualifications remain explicit; do not publish raw data or claim exact paper replication.
