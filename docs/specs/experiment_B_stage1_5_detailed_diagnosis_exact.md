# Experiment B — Stage 1.5: Detailed Diagnosis

## 1. Main conclusion

**The regression diagnostics reveal substantial statistical problems with the simple linear models, but they do not establish that those problems caused the failure to reproduce the historical intraday momentum relationship.**

The most important findings are:

1. **Extremely heavy-tailed residuals:** A small number of unusually large market moves dominate parts of the regression.
2. **Strong heteroskedasticity:** Prediction errors become substantially larger during high-volatility market conditions.
3. **Serial dependence and volatility clustering:** Errors are not independent across trading days.
4. **Influential observations:** Several March 2020 observations substantially affect the estimated coefficients.
5. **Temporal instability:** The relationship appears different across market periods, particularly in 2021.
6. **Possible functional-form misspecification:** There is some evidence that simple linear models fail to capture aspects of the relationship.

However, **no consistent positive intraday momentum relationship emerges after the robustness checks**.

Importantly, the implementation appears sound. Codex reproduced all 57 Stage 1 coefficient and inference entries to numerical precision and independently checked return calculations, volatility, timestamps, and session boundaries. The 2022–2023 validation and 2024–2026 sealed test periods remain untouched. fileciteturn8file0L1-L15

The evidence therefore points toward an unstable or weak modern relationship, complicated by market volatility and extreme observations, rather than an identified coding error.

---

## 2. The linear relationship is extremely weak

The primary model is

\[
Y_t=\alpha+\beta X_t+\varepsilon_t,
\]

where \(X_t\) is the previous-close-to-10:00 return and \(Y_t\) is the final-half-hour return, both expressed in basis points.

The three frozen regressions produced:

| Model | Main coefficients | HAC p-values | \(R^2\) |
|---|---|---|---|
| OLS1: \(Y\sim X\) | \(\beta_X=-0.0130\) | 0.671 | 0.000712 |
| OLS2: \(Y\sim W\) | \(\beta_W=-0.0385\) | 0.774 | 0.000522 |
| OLS3: \(Y\sim X+W\) | \(\beta_X=-0.0128,\ \beta_W=-0.0377\) | 0.676, 0.776 | 0.001213 |

Even OLS3 explains only **approximately 0.12% of the training variation** in the final-half-hour return.

This is apparent in your third figure: the regression lines are almost horizontal, while the observations have enormous vertical dispersion.

The data have standard deviations of approximately 68.7 bp for \(X\), 19.9 bp for \(W\), and 33.5 bp for \(Y\).

For OLS1, the HAC 95% confidence interval for \(\beta_X\) is

\[
[-0.0730,\ 0.0470].
\]

Therefore, a 100 bp increase in \(X\) corresponds to an estimated fitted difference of −1.30 bp in \(Y\), with a confidence interval spanning approximately −7.30 to +4.70 bp.

**Interpretation:** We have neither evidence of a reliable positive momentum coefficient nor sufficient precision to rule out every economically meaningful relationship. fileciteturn8file0L17-L52

## 3. Residual normality: a very substantial departure

Your first figure contains three normal QQ plots.

Under normally distributed residuals, observations should fall approximately along the reference line.

Instead, all three models show:

- A relatively compressed central distribution.
- An extremely heavy positive tail.
- A substantial negative tail, though less extreme.
- Several observations many standard deviations away from the center.

The diagnostics quantify this.

| Statistic | OLS1 | OLS2 | OLS3 | Gaussian reference |
|---|---:|---:|---:|---:|
| Skewness | 2.66 | 2.70 | 2.66 | 0 |
| Pearson kurtosis | 51.85 | 51.38 | 51.67 | 3 |
| Jarque–Bera p-value | ≈0 | ≈0 | ≈0 | — |

The kurtosis is extraordinary. A value around 52 indicates far more extreme observations than expected under a normal distribution.

This also explains why the QQ plots are nearly identical: **all three regressions leave almost the same variation unexplained**.

### Does this invalidate OLS?

Not automatically.

OLS does not require normally distributed errors to estimate linear projection coefficients. Nor does HAC inference require exact residual normality.

However, such extreme tails make coefficient estimates sensitive to unusual observations and can weaken finite-sample approximations, particularly when combined with time dependence.

**Diagnosis:** Classical Gaussian regression assumptions are inappropriate here. But nonnormality alone does not explain why the estimated momentum coefficient is negative.

## 4. Heteroskedasticity: the strongest reason to retain volatility conditioning

Your fourth figure is particularly informative.

Look at the two right-hand plots, showing squared residuals against opening realized volatility.

There is a clear upward relationship:

\[
\text{Opening RV}\uparrow
\quad\Longrightarrow\quad
\text{Residual magnitude tends to increase}.
\]

The Spearman correlation between absolute residuals and opening RV is approximately:

\[
\rho_s(|\widehat\varepsilon_t|,RV_t)\approx 0.405
\]

for OLS1, with similar values for OLS2 and OLS3.

The formal diagnostics reinforce this:

| Test | OLS1 p-value | OLS2 p-value | OLS3 p-value |
|---|---:|---:|---:|
| Breusch–Pagan (Koenker) | 0.0043 | 0.451 | 0.0271 |
| White | \(3.37\times10^{-67}\) | \(1.32\times10^{-62}\) | \(8.14\times10^{-126}\) |
| ARCH LM | \(3.29\times10^{-123}\) | \(8.42\times10^{-122}\) | \(2.50\times10^{-119}\) |

The differing Breusch–Pagan and White results are worth noting. The tests consider different variance alternatives, and their usual reference distributions are not fully reliable with dependent financial observations.

Nevertheless, the plots, correlation estimates, and diagnostics strongly support **state-dependent conditional variability**. fileciteturn8file0L217-L299

### Why this matters for our EBM project

There is an important mathematical distinction:

\[
\boxed{\mathbb E[Y\mid X,Z]}
\qquad\text{versus}\qquad
\boxed{\operatorname{Var}(Y\mid X,Z)}.
\]

Our primary EBM project investigates the conditional mean, especially whether the relationship between \(X\) and \(Y\) changes with volatility state \(Z\).

But these diagnostics primarily show that **the conditional variance changes with volatility**.

This makes volatility conditioning scientifically relevant, but it does not yet demonstrate that volatility changes the expected return.

For example, it is possible that

\[
\mathbb E[Y\mid X,Z]\approx 0
\]

while

\[
\operatorname{Var}(Y\mid X,Z)
\]

changes substantially across states.

In that situation, a sufficiently flexible EBM could learn features of changing variability indirectly, but might not improve predictions of the conditional mean.

**This is an important limitation for our original hypothesis.**

---

## 5. Autocorrelation and volatility clustering

The residuals also show statistically detectable dependence across trading days.

For OLS1:

| Diagnostic | Value |
|---|---:|
| Residual ACF, lag 1 | 0.1013 |
| Residual ACF, lag 5 | 0.1108 |
| Durbin–Watson | 1.797 |
| Ljung–Box, lag 5 p-value | \(9.42\times10^{-12}\) |
| ARCH LM, lag 5 p-value | \(3.29\times10^{-123}\) |

Similar results occur in the other models.

There are two distinct phenomena.

**Mean dependence:** Residual autocorrelations around 0.10 indicate some persistence in forecast errors.

**Variance dependence:** The extremely strong dependence in squared residuals indicates pronounced volatility clustering.

The temporal plot makes this concrete. Residual volatility changes sharply around 2020 and subsequently declines.

### Implication for inference

Using Newey–West/HAC standard errors in Stage 1 was appropriate because ordinary homoskedastic standard errors would be misleading.

For example, OLS1's opening-return coefficient has:

| Standard-error method | SE |
|---|---:|
| Ordinary OLS | 0.0126 |
| HAC5 | 0.0306 |
| HC3 | 0.0439 |

The ordinary standard error substantially understates uncertainty relative to both robust alternatives.

However, HAC is not a complete solution. With extreme observations, volatility clustering, and potential changing regimes, its finite-sample reliability remains qualified.

For Stage 2, dependence-aware validation and paired comparisons will be essential.

---

## 6. The 2020 crisis has a substantial influence

This is arguably the most important diagnosis for the weak regression coefficient.

The largest influence comes from **March 18, 2020**.

On that day:

| Variable | Value |
|---|---:|
| Opening return \(X\) | −456.7 bp |
| Preclosing return \(W\) | −137.8 bp |
| Final-half-hour return \(Y\) | +395.1 bp |
| Cook's distance, OLS1 | 2.23 |
| Cook's distance, OLS3 | 3.10 |

The very negative opening return followed by a very positive closing return strongly pushes the estimated opening-return slope downward.

Another highly influential observation, March 13, 2020, has approximately \(X=+341\) bp and \(Y=+462\) bp, pushing the relationship in the opposite direction.

The result is a regression strongly affected by a small number of extreme days.

### What happens when influential observations are removed?

| OLS1 estimation method | Opening coefficient |
|---|---:|
| Original OLS | −0.0130 |
| Remove most influential day | +0.0134 |
| Remove five most influential days | −0.0173 |
| Huber robust regression | −0.0217 |
| Exclude all of 2020 | −0.0350 |

These results are revealing.

Removing just March 18 changes the coefficient's sign.

However, removing five influential days gives a negative coefficient again. Robust regression also remains negative.

The confidence interval after removing March 18 is

\[
[-0.0568,\ 0.0836],
\]

so the resulting positive point estimate is not statistically convincing.

**Diagnosis:** Outliers destabilize the coefficient, but removing them does not restore a robust positive relationship. fileciteturn8file0L397-L455

One additional data-quality point deserves attention: March 18 also has a known missing midday candle cluster. Those minutes are outside the required scientific windows, so they do not directly invalidate the return inputs. Nevertheless, because this is the single most influential date, I would independently recheck its four price anchors before closing the replication audit.

That is a targeted verification, not a reason to exclude the observation.

---

## 7. Temporal instability: 2021 looks particularly different

The fixed subperiod regressions produced:

| Training period | Days | OLS1 opening coefficient | HAC p-value |
|---|---:|---:|---:|
| 2016–2019 | 996 | −0.0213 | 0.431 |
| 2020 | 248 | +0.0049 | 0.929 |
| 2021 | 251 | **−0.0830** | **0.0149** |
| All 2016–2021 | 1,495 | −0.0130 | 0.671 |
| Excluding 2020 | 1,247 | −0.0350 | 0.124 |

This suggests an interesting possibility.

During 2021, the relationship resembles **intraday mean reversion** rather than momentum: stronger early returns are associated with weaker closing returns.

The 2021 coefficient is reasonably large compared with the full-period coefficient.

For a 100 bp increase in opening return, the fitted closing return changes by approximately

\[
-0.083(100)=-8.3\text{ bp}.
\]

But there are important limitations.

The 2021 result is one exploratory subperiod result among multiple comparisons.

Also, the formal test of the 2020 opening slope against the non-2020 slope gives

\[
p=0.500.
\]

We therefore cannot conclude that a structural break has been formally established.

The evidence supports **period variation in estimated coefficients**, not a confirmed regime-change mechanism. fileciteturn8file0L459-L589

This is relevant for EBM because a model trained on the full 2016–2021 period might average over substantially different conditional relationships.

A more flexible model is not automatically better at handling that instability. It might simply overfit it.

---

## 8. Is there evidence of nonlinear relationships?

**Some evidence of misspecification exists, but it is not yet compelling evidence of a useful nonlinear conditional mean.**

The RESET tests give:

| Model | RESET HAC p-value |
|---|---:|
| OLS1 | 0.0437 |
| OLS3 | 0.000098 |

These tests examine whether adding a squared fitted-value term improves the regression.

The results suggest that the original linear specification may omit some structure.

However, RESET does not tell us what that structure is.

It could reflect nonlinear conditional means, interactions, extreme observations, or other forms of misspecification.

Look at your second figure showing residuals against predictors and fitted values.

The orange bin averages fluctuate somewhat, but they remain relatively close to zero compared with the large vertical dispersion of the observations.

There is no visually obvious, stable nonlinear curve comparable to the strong variance relationship observed against RV.

### My interpretation

The evidence for nonlinear **conditional variance** is strong.

The evidence for nonlinear **conditional mean** is considerably weaker.

This distinction matters when deciding whether to train EBMs.

It provides a legitimate reason to investigate nonlinear models, but not yet a reason to expect a substantial improvement.

---

## 9. Multicollinearity is not the problem

OLS3 uses both \(X\) and \(W\).

Its variance inflation factors are:

\[
\operatorname{VIF}(X)\approx 1.00033,
\qquad
\operatorname{VIF}(W)\approx 1.00033.
\]

These values are essentially one.

The correlation between \(X\) and \(W\) is only approximately 0.018.

Consequently, multicollinearity cannot explain the weak coefficients or large HAC uncertainties.

Adding \(W\) to the regression also barely changes the estimated coefficient of \(X\).

This suggests the problem is not redundancy between the predictors. Rather, each predictor has very little demonstrated linear association with the closing return.

---

## 10. Why did the historical result fail to replicate?

We can now separate the possible explanations by evidential strength.

| Potential explanation | Assessment |
|---|---|
| Incorrect return calculations | **No evidence** from the checks performed |
| Timestamp/DST errors | No evidence from the verified dates |
| Hugging Face repairs | Negligible effect on results |
| Multicollinearity | Effectively ruled out as an explanation |
| Extreme observations | **Confirmed substantial influence** |
| Heteroskedasticity | **Strongly supported** |
| Residual serial dependence | Supported |
| Period-specific coefficient variation | Observed, but no confirmed structural break |
| Nonlinear conditional mean | Possible, not established |
| Different historical versus modern market behavior | Plausible, not identified |
| Differences in TAQ/Alpaca measurement or source conventions | Unresolved |
| Different opening-RV normalization | Cannot directly explain unconditional OLS1's point estimate |

One additional observation: replacing overnight-inclusive \(X\) with the intraday-only opening return produces a coefficient of approximately −0.0192, with HAC \(p=0.869\).

So the negative result does not disappear under that particular alternative opening-return definition.

The exact historical source construction remains incompletely verified, and we do not have the original 1993–2013 observations.

**We therefore cannot determine whether the original economic relationship disappeared, changed across market regimes, or differs because of measurement and sampling conventions.** fileciteturn8file0L53-L107

---

## 11. What does this mean for our EBM research?

I would separate the conclusions into three levels.

### A. Historical replication

**Current status: Not corroborated in the 2016–2021 training sample.**

The weak result is not adequately explained by a discovered coding mistake.

We should preserve this as a genuine negative or inconclusive modern-period finding.

### B. State-dependent EBM methodology

**Current status: Still scientifically justified for investigation.**

The data clearly exhibit dependence on opening volatility, especially in the conditional variability of returns.

The RESET diagnostics also provide limited motivation to investigate deviations from simple linear conditional means.

However, explaining changing residual variance is not the same as predicting the direction or magnitude of expected returns.

Our EBM investigation must make this distinction explicit.

### C. Trading implications

**Current status: No predictive or economic advantage established.**

The original linear models explain almost none of the return variation.

A nonlinear model faces a difficult problem: its apparent improvement could arise from fitting rare crisis observations or nonstationary patterns rather than learning a stable trading signal.

Consequently, a better in-sample fit would be particularly unconvincing here.

---

## 12. Recommended next steps

**I recommend proceeding with Stage 2, with one minor verification first.**

First, independently verify the March 18, 2020 price anchors because that day is exceptionally influential. This is a small, targeted check rather than another full diagnostic investigation.

Then proceed with the planned **state-aware model comparison**, preserving the original primary dataset and outcomes:

| Model | Research question |
|---|---|
| Constant-mean predictor | Can any model improve on predicting no conditional variation? |
| Original OLS | Does simple intraday momentum predict the close? |
| Linear \(X\times Z\) interaction | Does a volatility-dependent linear slope help? |
| Varying-coefficient spline | Does a smooth nonlinear slope dependence help? |
| State-dependent EBM | Does additional interpretable nonlinear flexibility improve prediction? |

All models should be evaluated on matched observations, with chronological validation, careful complexity control, and comparisons robust to influential dates.

For the EBM, I would pay particular attention to whether apparent nonlinear features persist outside 2020 and outside extreme-support regions.

### Final assessment

**Stage 1.5 has successfully diagnosed why ordinary linear regression is statistically fragile in these data, but not why the historical momentum result changed.**

The strongest finding is that volatility governs the scale of closing-return uncertainty much more clearly than the simple regressors govern its conditional mean.

That is scientifically meaningful, although different from the original objective.

I would now test whether any stable conditional-mean relationship exists beyond linear regression, while keeping the negative replication result intact.

**Stage 2 should be a genuine falsification test of the EBM hypothesis—not an attempt to recover positive results by increasing model flexibility.**
