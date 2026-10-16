# Experiment B Stage2A methods and exact model registry

Numerical results: [scientific report](../reports/B/stage2A_state_linear_and_spline_results.md). Exact numeric preprocessing and schedules: [protocol](../config/B_stage2A_linear_spline_protocol.json). All chronological fit/preprocessing/attempt identities: manifest/modelCSV.

| model_id | family | info | parameters | rank | columns | role | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1_E | C1 | E | 6 | 6 | ["intercept", "X", "DM", "X_DM", "DH", "X_DH"] | primary | PASS |
| C2_E | C2 | E | 4 | 4 | ["intercept", "X", "Zc", "X_Zc"] | primary | PASS |
| S4_E | S4 | E | 8 | 8 | ["intercept", "X", "Zc", "X_Zc", "H1", "X_H1", "H2", "X_H2"] | primary | PASS |
| S6_E | S6 | E | 12 | 12 | ["intercept", "X", "Zc", "X_Zc", "H1", "X_H1", "H2", "X_H2", "H3", "X_H3", "H4", "X_H4"] | higher_df_sensitivity | PASS |
| C1_L | C1 | L | 7 | 7 | ["intercept", "X", "DM", "X_DM", "DH", "X_DH", "W"] | primary | PASS |
| C2_L | C2 | L | 5 | 5 | ["intercept", "X", "Zc", "X_Zc", "W"] | primary | PASS |
| S4_L | S4 | L | 9 | 9 | ["intercept", "X", "Zc", "X_Zc", "H1", "X_H1", "H2", "X_H2", "W"] | primary | PASS |
| S6_L | S6 | L | 13 | 13 | ["intercept", "X", "Zc", "X_Zc", "H1", "X_H1", "H2", "X_H2", "H3", "X_H3", "H4", "X_H4", "W"] | higher_df_sensitivity | PASS |
| C1_L_Wmod | C1 | L | 9 | 9 | ["intercept", "X", "DM", "X_DM", "DH", "X_DH", "W", "W_DM", "W_DH"] | optional_W_moderation | PASS |
| C2_L_Wmod | C2 | L | 6 | 6 | ["intercept", "X", "Zc", "X_Zc", "W", "W_Zc"] | optional_W_moderation | PASS |
| OLS1_E | OLS1 | E | 2 | 2 | ["intercept", "X"] | reference | PASS |
| OLS3_L | OLS3 | L | 3 | 3 | ["intercept", "X", "W"] | reference | PASS |
| OLS2_L | OLS2 | L | 2 | 2 | ["intercept", "W"] | reference | PASS |

## Basis, units and nesting

For K=4/6 training Z knots, j=1…K−2:

h_j(z)=[(z−k_j)_+³−(kK−k_j)/(kK−k(K−1))·(z−k(K−1))_+³+(k(K−1)−k_j)/(kK−k(K−1))·(z−kK)_+³]/(kK−k1)².

Restricted/natural cubic: linear in both tails and span includes1,Z. Curvature projected off1,Zc by predictor-only training least squares, centered0 at Zref and divided by training residual SD. The invertible span transform aids conditioning. Matrices contain literal1,X,Zc,XZc plusH_j,XH_j; E2K parameters,L2K+1 withcommonW. Zero nonlinear blocks exactly nestsC2; testdf=2(K−2). Pureg curvature onlyXH; g nonconstant includesXZc. Full design/restriction covariance rank checked; no silent original-column dropping.

Y/X/W are simple-return bp, Z dimensionless logRV; coefficients on intercept/state main terms inbp, X/W slope and interaction coefficients scaled per stated basis unit. C1 low-reference indicators use exact raw RV cuts, equality lower bin. E does not readW; optional L-W moderation separate from primaryX question.

Zref=-6.257012700074515; cutoffs=[0.001558374721607106, 0.0024281183976187152].

| dimension | quantiles | knots | boundaries |
| --- | --- | --- | --- |
| 4 | [0.05, 0.35, 0.65, 0.95] | [-6.913921705700965, -6.44522266085524, -6.043074190631212, -5.250196473329516] | [-6.913921705700965, -5.250196473329516] |
| 6 | [0.05, 0.23, 0.41, 0.59, 0.77, 0.95] | [-6.913921705700965, -6.587387522943726, -6.368600549458324, -6.136290421575377, -5.843060079784792, -5.250196473329516] | [-6.913921705700965, -5.250196473329516] |

Linear tails outside boundary knots, no clipping/future bounds; validation boundary/observed-range counts recorded before labels. Fixed deletion fits preserve full training preprocessing. Quarterly original categorical cuts unchanged; spline knots/Zref/scales fitted only on prior history. Basis inference conditions on these transforms and does not incorporate post-validation model-selection uncertainty.

## Estimation, uncertainty, choices

OLS stable SVD, full rank; ordinary/HC3/BartlettHAC5 primary10/20 sensitivity,n/(n−k),normal95%. vΣv′ for whole fitted contrasts; restrictioncovariance rank checked for jointWald. Six primarymoderation/curvature tests withHolm; everything else exploratory. Whiteauxiliary products may be algebraically redundant; actualSVD rank−1df. RESET used onlylinear/C1/C2, nestedcurvature forS1. No Gaussian/independence/exogeneity guarantee from residual tests.

FULL includesall1,495. DROP_TOP1/5 use priorOLS1keys,EXCLUDE_2020 distinct,MATCHED_SOURCE removesAug12/13; originalbasisfixed. Huberpoint-onlydifferentloss,noHAC. Everycandidate/refit/failure/influence attempt is inmodelsCSV; internalvariance/RESET auxiliaryregressions are diagnostic tests, not extraforecast candidates. Temporal2016–19/2020/2021 and leaveyearC2/S4 comparefixedbasis; no breakpointsearch.

Quarter starts ['2022-01-01', '2022-04-01', '2022-07-01', '2022-10-01', '2023-01-01', '2023-04-01', '2023-07-01', '2023-10-01']. Fit targetdate <forecastcutoff/date. N1 initializedtrainingmean, expandsdailyonlypreviousY; firsttrainforecast0. Samefixed/quarterlynaivecomparison. Rank sixprimaryFULL candidates byquarterlyMSE withinE/L; retainbestdescriptively, requirepositivepairedHAC5gainCI vsstrongestnaive/OLS forconvincingimprovement. FULL neverreplacedbytrimmedvariant. Higherdf/Wmod sensitivities notautomaticprimaryreplacements. Validationselectioninferenceexploratory andperiodreusedforfutureEBM; testsealed.

## Support, plots and reproduce

Xgrid±10.0bp,x0=0; coarseboundaries±5. LrequiresWoriginalcentral80%bandaround0. Cellminimum50/20nonoverlapfive-rowblocks,100/30strong, practicalnotformal. HighstateX0fails: anchoredhigh-lowscientificcontrastABSTAIN. Projectioncoefficientsare distinctfromrawconditionalmeans.

Existingrequirements-stage1_5.lock.txt+editablepackage, then python -B -m ebm_research.experiment_b.stage2a (optional --data-root PATH). Restoreauthorizedmatchingdaily/sourcefilesbyhash, noAPIcredentials/networkneeded. No newdependency/modelbinary/fulldatareplica/EBM. Protocolpreserved andstage-owned outputsregenerate.
