# Stage 1 checkpoint

UTC: 2026-10-23T01:55:09.874482+00:00

One shared acquisition pass and small-source intake executed; see monthly ledger, source receipts, holds and storage trace.

All writes use new five-screen namespaces. No old A/B/C outputs modified.

## Retrospective closeout evidence

Files created/consumed: `checkpoints/hf_months.jsonl,logs/network.jsonl,logs/cleanup.jsonl,acquired_sources.json;12selected monthly outputs`.

12successful unique archive objects,3209573881network bytes; raw monthly files deleted after selected hash/count validation. Resume skipped all12. Small ETF/FRED/workbook sources once;2021Fed404 repaired through official statement URLs. No mirror or global HF cache. Measured peak297766292bytes.

Tests: see `../manifests/test_execution_evidence.json`; source/config gates plus actual stage-specific audits. Failures and recoveries are preserved in bounded phase logs and the mandatory repository session report.

Storage: no baseline data deleted or duplicated; precise retained/temporary/peak bytes in storage/network/cleanup ledgers. Git: main at3e9c244, no tracked changes/commits; new namespaces only; four preexisting dirty files preserved.

Next validated action: Derive shared features.
