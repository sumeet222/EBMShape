# P02_SIGNED_RV preliminary screen

## P02_SIGNED_RV — results and limitations

**DATA HOLD**; 1454 independent dates; 1,454 matched rows.

![P02_SIGNED_RV measured summary](../../reports/figures/P02_SIGNED_RV_summary.png)

**NO VALID RESULT for the intended state shape.** Insufficient state counts and/or common predictor support. State event/date counts: {'high': 5, 'low': 10, 'middle': 1439}. No supported response curve or shape-contrast image is presented.

The fixed q tail states have10low and5high SPY days (minimum30); reference-only common logRV support is empty. No bins were merged. Continuous q support is shown in the summary. The separate raw-RV reference remains descriptive: negative coefficient 1.95, positive -1.09, lagRV 0.408; negative-minus-positive95% interval {'estimate': 3.03979058189282, 'lo': 0.7949252646071433, 'hi': 5.532162429285212}. No-state current/lag logRV MSE 0.346; state model 0.345. The held state-slope contrast and any rank-deficient bootstrap draws are not treated as evidence.

| sample | dates | rows | status |
| --- | --- | --- | --- |
| STOCKS_POOLED | 238 | 929 | DATA HOLD |

All dates shown are exploratory. State-bin means are finite-interval averages, not a raw singleton conditional-mean function. B=500 intervals are conditional date-block sensitivity, without multiplicity correction or confirmatory coverage guarantees. SPY2016–2021 is principal; ten-stock2019 is reported separately and must not be pooled with SPY as independent confirmation. RV uses389 adjacent observed closes, excludes overnight and the opening O-C return. Strict prior/next scheduled-session joins discard gaps. Fixed q bins can have weak tail support. Lag logRV is controlled. The raw semivariance regression includes lag RV; it is a separate estimand.

Exact definitions: Y=`next_session_log_RV_389`; X=`current_log_RV_389`; Z=`current_q_down_fixed_thirds`.

Config SHA-256 `57db40d2fc8b9dfab52282abd07b8e663ae959a2cec832c0dc863c635d995eee`; input fingerprint `877717c8fddd79652f725482ac9bf43ba198f67111dad377c6176ce3f1df8909`; source manifest SHA-256 `5aeef79b565d833bceb832004b638ada449eb6075838ea869b89201cae4256f5`.

Reproduction: from repository root, `.venv/bin/python -B scripts/five_prelim.py screen` (verified completed screens are skipped), then `report` and `verify`. Config and source identities are frozen.
