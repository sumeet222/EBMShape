# P01_INTRADAY_BETA preliminary screen

## P01_INTRADAY_BETA — results and limitations

**NO-GO**; 248 independent dates; 86,904 matched rows.

![P01_INTRADAY_BETA measured summary](../../reports/figures/P01_INTRADAY_BETA_summary.png)

Primary last-minus-first slope contrast: **-0.0476**, 95% date-block sensitivity interval **[-0.0916, -0.0128]**. Frozen material slope threshold: 0.1.

| state | slope | interval |
| --- | --- | --- |
| early | 1.02 | [0.9899, 1.055] |
| mid | 0.98 | [0.9578, 1.003] |
| late | 0.972 | [0.9441, 0.9994] |

![Whole-surface and slope contrast](../../reports/figures/P01_INTRADAY_BETA_shape_contrast.png)

![Support audit](../../reports/figures/P01_INTRADAY_BETA_support.png)

7 jointly supported common-X bins; 493/500 nonsingular resamples. Reference-half contrast -0.0482, later -0.0425, without top1% absolute-X dates -0.0505. Sign stability: True. These sensitivity results do not replace the primary estimate.

![Synchronous stock-market scatter](../../reports/figures/P01_INTRADAY_BETA_scatter.png)

Early minus late cross-stock beta SD: unavailable; shared-date95% interval None; 0 common dates. Per-stock beta estimates are saved. **Dispersion compression cannot be assessed reliably:** there are fewer than30common dates across all ten stocks; HCA/KLAC each have only6eligible dates. No balanced-panel dispersion bootstrap or literature-dispersion replication claim is made. The NO-GO status applies to the pooled mean-beta contrast only.

The pooled mean beta is slightly lower late than early. This is a mean-slope finding, not evidence of the literature’s cross-stock dispersion compression.

All dates shown are exploratory. State-bin means are finite-interval averages, not a raw singleton conditional-mean function. B=500 intervals are conditional date-block sensitivity, without multiplicity correction or confirmatory coverage guarantees. 2019 only; ten coverage/sector-selected stocks, incomplete minute days excluded without filling. Cross-stock beta dispersion uses common balanced dates and identical resampled dates across stocks. Primary status uses the pooled last-minus-first slope; dispersion is an additional diagnostic. Neither curvature nor a novel intraday effect is asserted.

Exact definitions: Y=`stock_5m_log_return_bp`; X=`spy_synchronous_5m_log_return_bp`; Z=`clock_start_ET_early_mid_late`.

Config SHA-256 `197c769732e27298df2ff9a02b290ef2f9d5406404a74db3b7928895155faa3b`; input fingerprint `877717c8fddd79652f725482ac9bf43ba198f67111dad377c6176ce3f1df8909`; source manifest SHA-256 `5aeef79b565d833bceb832004b638ada449eb6075838ea869b89201cae4256f5`.

Reproduction: from repository root, `.venv/bin/python -B scripts/five_prelim.py screen` (verified completed screens are skipped), then `report` and `verify`. Config and source identities are frozen.
