Appendix A — selected original theorem statements supplied for exact audit
The following are source-text excerpts, extracted from the original reports, not paraphrased theorem replacements. For compactness each extract starts at the original ## Theorem/Proposition heading and ends before its proof; some terms rely on the original source setting (FD/FL, D, supplied envelope, real-valued scientific row, physical tree family, etc.). These prerequisite setting assumptions must be recovered from the actual original source if a theorem is to be claimed exactly instantiated. If those setting sections are not available to Codex, record the corresponding assumption as UNVERIFIED, rather than inferring it from this excerpt or from market data. The source-precendence and scope notes below are from the supplied state_dependent_ebm_consolidation_assumptions_and_issues_v1.md (Task 26 strict editorial crosswalk; not a semantic independent proof audit).
A.0 — Mandatory source-setting boundaries (explicitly supplied)
- T10B: Genuine nonsaturated finite multifeature tree spans, actual weights, scientific representers, class-bias restrictions, and separate statistical/standardization models; global null preservation need not preserve local science. Model projection ≠ raw conditional mean.
- T11: One continuous raw feature with fixed finite observed states, local studentization and bounded-response or supplied-regularity simultaneous bands. Fixed-law and uniform adaptive statements differ; local tails/localization bias are material. Its finite-state framework does not automatically cover continuous-valued Z and multifeature X,W native learner.
- T12: Finite Gaussian actual whole-tree winner selection with specified gain path and capped stop; separate known-/unknown-scale constructions. Not an arbitrary native stochastic fit or analyst-selected state/mesh/donor/grid.
- T15: Affirmative almost-stability requires its full-mean confidence events, known/material tolerances and distinct continuum/table observation laws. Nonrejection of difference is not certification of equivalence.
- T16–T18: Idealized proper tree spaces, actual finite greedy histories under fixed/specific heterogeneous designs, and specified correction/feasible covariance. Continuous two-feature local fidelity and approximation/optimization gaps are distinct. These do not certify the bagged native InterpretML tree-building history.
- T19/T21: Separate across-environment and shared-time-panel assumptions; a stable mixture-level error pattern is not stable conditional shapes nor a causal drift decomposition. T19's stand-alone original report is not included in the source statements below; use the scope register for this distinction, not a fabricated T19 theorem quotation.
- T20: Finite growing proper model spaces/query panels and calibrated capacity-risk costs; exact space retention versus dictionary physical cost are different.
- T22: Five separate questions including shape adequacy, prediction gain and trading decision gain. Its package correspondence is a static software audit, not a native fit executed in that theory report.
- T23: Fixed finite support/rare-cell laws with specialized Gaussian known-class or bounded-dependent constructions. Stable fitted rank and global RMS do not protect every raw contrast.
- T24: Continuous-state coarsening, within-bin shape/level/composition identities, and bounded known information for valid bin-to-raw inference. Exact state-affine retained spaces are not equivalent to arbitrary three-tercile EBMs.
- T25: Known or estimated moment/coarsening operator, supplied response family/admissibility class, pilot/label information, and simultaneous uncertainty. Estimated moments are not the same as arbitrary within-tercile empirical histograms; full affine raw inverse theory is not applied by fitting an EBM.
All excerpts below preserve original theorem ID, source filename and original starting line. In the final machine ledger, include specific excerpts' status (KNOWN, PROVED, etc.) and explicitly say which original prerequisites could not be inspected. Avoid treating source crosswalk mapping as mathematical validation of a theorem.
Source: T10B.B1 — state_dependent_ebm_research_task10B_proper_multifeature_theory_results_v0_10B.md, original line 261
Theorem T10B.B1 — Model estimability, scientific identification, and support-specific precision
Status: KNOWN / DERIVED WITH MATCHED ASSUMPTIONS; complete argument given to fix the target.
Let a deterministic table dictionary \(\Psi\) span a declared model, let \(R_n\) evaluate its cells at the sample, and put \(\Phi=R_n\Psi\), \(V=\operatorname{col}\Phi\), \(P_V\) its Euclidean projector. A table contrast \(a\) induces coefficient row \(\ell=\Psi^\top a\).
The model contrast is determined by sample fitted values for every coefficient vector exactly when \(\ell\perp\ker\Phi\). When it is estimable its unique representer in \(V\) is
\[
v=\Phi(\Phi^\top\Phi)^\dagger\ell,\qquad
\|v\|^2=\ell^\top(\Phi^\top\Phi)^\dagger\ell.
\]
If every cell with \(a_c\ne0\) has count \(N_c>0\), define \(u_i=a_{C_i}/N_{C_i}\) on those cells and zero elsewhere. Then
\[
v=P_Vu,\qquad \|v\|^2\le\sum_{c:a_c\ne0}\frac{a_c^2}{N_c}.
\]
Under FD with centered finite error covariance \(C_\varepsilon\), the endpoint statistic \(v^\top Y\) has mean \(v^\top R_n\mu\) and variance \(v^\top C_\varepsilon v\). Its mean is a contrast of an empirical model projection, not generally \(a^\top\mu\). If \(C_\varepsilon=\sigma^2 I\), the variance is \(\sigma^2\|v\|^2\).
For a full positive atomic law, \(a^\top\mu\) is scientifically identified by its required cells, regardless of the model. Without an extension restriction, a nonzero coefficient on a zero-probability cell makes the scientific functional unidentifiable. At exact duplication, the diagonal group is supported, but the specified individual and opposite-sign comparisons are not.
Source: T10B.B2 — state_dependent_ebm_research_task10B_proper_multifeature_theory_results_v0_10B.md, original line 383
Theorem T10B.B2 — Functional preservation, sharp response-class bounds, and dimension requirements
Status: PROVED HERE; representer algebra is classical and was screened in 10A §9.6.
Fix a supported finite table, \(Q\succ0\), \(P=P_{\mathcal S}^Q\), and row \(a\). Put \(r=Q^{-1}a\), \(b=(I-P)r\). Then
\[
a^\top(I-P)v=\langle b,v\rangle_Q
 =\langle b,(I-P)v\rangle_Q.
\]
Consequently:
(i) Exact preservation for all unrestricted tables is equivalent to \(r\in\mathcal S\).
(ii) On an affine response class \(v_0+\mathcal M\), with \(\mathcal M\) linear, exact preservation is equivalent to \(\langle b,v_0\rangle_Q=0\) and \(b\perp_Q\mathcal M\).
(iii) On \(\mathcal F_R=\{v:\|(I-P)v\|_Q\le R\}\),
\[
\sup_{v\in\mathcal F_R}|a^\top(Pv-v)|=R\|b\|_Q.
\]
If \(b\ne0\) and no residual/class bound is imposed, the supremum is infinite.
(iv) For finitely many rows \(a_j\), the smallest linear enlargement of \(\mathcal S\) preserving all of them under this fixed \(Q\) is
\[
\mathcal S+\operatorname{span}\{Q^{-1}a_j\}_j.
\]
Its added dimension is the rank of the residual representers \((I-P)Q^{-1}a_j\). This is a linear-space statement, not automatic realization by a permitted tree family.
(v) If a fixed space must preserve one nonzero \(a\) for every positive diagonal weighting, it must contain each cell indicator \(e_c\) for which \(a_c\ne0\). This condition is also sufficient.
Source: T11.A1 — state_dependent_ebm_research_task11_feasible_raw_point_inference_results_v0_11.md, original line 170
Proposition T11.A1 — Supported raw values, exact mixture covariance, and occupancy
Status: KNOWN PRINCIPLES / DERIVED WITH MATCHED ASSUMPTIONS.
Under (D) and continuous versions, all raw evaluations in (3.5) are identified. Conditional on \(\mathscr C_n\), responses are independent, and the responses in each cell are identically distributed according to \(Y\mid C_n=c\). On occupied requested cells,
\[
 E[\bar Y_c\mid\mathscr C_n]=\mu_{c,n},\quad
 \operatorname{Var}(\bar Y_c\mid\mathscr C_n)=v_{c,n}/N_c,
\tag{4.1}
\]
with conditional cross-cell covariance zero. Moreover
\[
 v_{c,n}=E[\sigma^2(U,Z)\mid C_n=c]
              +\operatorname{Var}(m(U,Z)\mid C_n=c),
\tag{4.2}
\]
where \(\sigma^2(U,Z)=\operatorname{Var}(Y\mid U,Z)\).
For (3.4), under (H), a deterministic bias allowance is
\[
 |d_n-\theta|\le b_n(\theta):=
 \sum_j|c_j|L_{r_j}d_{j,n}^{\,s},\qquad
 d_{j,n}=\sup_{v\in B_{b_n(u_j)}}|v-u_j|\le h.
\tag{4.3}
\]
The supremum can include bin endpoints without changing the bound. In particular, a four-point allowance is at most \(4Lh^s\). Combine coefficients for sampling covariance, but do not replace (4.3) by \(\|a_n\|_1Lh^s\) when distinct raw values fall in the same cell.
For \(M_n=KB_n\),
\[
 P\{\exists c:N_c<n\pi_{c,n}/2\}
 \le KB_n\exp(-nc_0h_n/8).
\tag{4.4}
\]
Thus \(nh_n/\log(KB_n)\to\infty\) gives full occupancy, \(N_{\min}\ge nc_0h_n/2\), and eventually at least two observations per cell with probability tending to one. Only \(nh_n\to\infty\) is needed for growth of a fixed finite list of requested-cell counts.
Source: T11.B2 — state_dependent_ebm_research_task11_feasible_raw_point_inference_results_v0_11.md, original line 577
Theorem T11.B2 — Finite-sample simultaneous bands for the raw mean and every raw state contrast
Status: PROVED WITH A KNOWN RESPONSE RANGE AND A KNOWN HÖLDER CLASS; UNKNOWN VARIANCE IS ALLOWED.
Fix any \(n\), deterministic \(B\ge2\), observed states \(1,\ldots,K\), the full G1 dictionary, and \(0<\alpha<1\). Assume the IID raw experiment, an identified continuous mean on the full rectangle, the known response range, and the supplied global Hölder bound (H). Set
\[
 M=KB,\qquad x=\log(4M/\alpha).
\tag{8.9}
\]
If any cell has fewer than two responses, report \(\mathbb R\) everywhere and do not reject a global null. Otherwise, conditionally on the coarse labels, pair each cell's responses in original input order, compute \(r_c=r_{N_c}(x)\) from B1, and report
\[
 I_{n,t}(u,r)=
 \left[s_{t,b_n(u),r}\ \pm
 \{r_{b_n(u),r}+L_rh^s+\Delta_{n,t}\}\right].
\tag{8.10}
\]
Then, for almost every coarse-label realization,
\[
 \boxed{P\{m(u,r)\in I_{n,t}(u,r)\ 
       \forall u\in[0,1],\ r=1,\ldots,K,\ t\ge0\mid\mathscr C_n\}
       \ge1-\alpha.}
\tag{8.11}
\]
The same unconditional inequality follows. This is finite-sample coverage uniform over the disclosed bounded-response/Hölder class, not conditional on the full raw design.
On the same event, every four-point raw contrast is covered for every iteration. A simple radius around its fitted contrast is
\[
 r_{b,r}+r_{b_0,r}+r_{b,r_0}+r_{b_0,r_0}
       +2(L_r+L_{r_0})h^s+4\Delta_{n,t}.
\tag{8.12}
\]
A sharper valid version combines repeated cell coefficients in the sampling and optimization terms:
\[
 R_{a,n,t}=\sum_c|a_{c,n}|r_c+b_n(\theta)
                              +\|a_n\|_1\Delta_{n,t}.
\tag{8.13}
\]
The raw bias term still uses the original raw evaluations as in (4.3). Structural raw cancellations can receive \(\{0\}\). No further multiplicity penalty is needed for the uncountable collection of raw contrasts obtained from this one simultaneous mean event.
Under (D), \(h_n\to0\), \(nh_n/\log(KB_n)\to\infty\), and either G2 stopping rule, the maximal radius satisfies
\[
 \sup_{u,r}\operatorname{rad}I_{n,t_n}(u,r)
 =O_p\!\left(Lh_n^s+R\sqrt{\frac{\log(KB_n)}{nh_n}}
              +\frac{R\log(KB_n)}{nh_n}+\Delta_{n,t_n}\right).
\tag{8.14}
\]
For fixed \(K\), \(h_n\asymp(\log n/n)^{1/(2s+1)}\) gives the familiar upper order \((\log n/n)^{s/(2s+1)}\). This report proves the upper bound, not a new minimax or optimal-length theorem.
Source: T12.C1 — state_dependent_ebm_research_task12_adaptive_selection_scientific_inference_results_v0_12.md, original line 323
Theorem T12.C1 — Exact known-scale selective law and finite equal-tailed intervals
Status: KNOWN CONDITIONAL-GAUSSIAN PRINCIPLE / COMPLETE SCIENTIFIC-TARGET SPECIALIZATION.
Fix \(k\), let \(a=a_{\varphi(k)}\), and use (5.3). Under (3.3), before selection,
\[
T_a\sim N(\theta,\tau_a^2),\qquad
\theta=a^\top\mu,\quad \tau_a^2=\sigma^2 r_a/n,
\qquad T_a\ \perp\ V_a.
\tag{5.6}
\]
For almost every \(v\) under the distribution of \(V_a\) conditional on \(E_k\), the slice \(S=\mathcal Z_k^a(v)\) has positive normal probability. On such a slice,
\[
\boxed{\mathcal L(T_a\mid E_k,V_a=v)
       =N(\theta,\tau_a^2)\text{ truncated to }S.}
\tag{5.7}
\]
No condition \(\mu\in\mathcal S_{\rm pair}\) is imposed.
For its positive-length disjoint intervals \(S=\bigcup_{b=1}^L(l_b,u_b)\), with endpoint conventions immaterial for normal probabilities, put
\[
 F_{\theta,\tau,S}(t)=
 \frac{\displaystyle\sum_b
 \int_{(l_b,u_b)\cap(-\infty,t]}\tau^{-1}\phi((z-\theta)/\tau)\,dz}
 {\displaystyle\sum_b[\Phi((u_b-\theta)/\tau)-\Phi((l_b-\theta)/\tau)]}.
\tag{5.8}
\]
At the true \(\theta\), (5.8) evaluated at \(T_a\) is conditionally uniform. The equal-tailed two-sided p-value for \(\theta=\theta_0\) is
\[
p_k(\theta_0)=2\min\{F_{\theta_0,\tau_a,S}(T_a),
                       1-F_{\theta_0,\tau_a,S}(T_a)\}.
\tag{5.9}
\]
It is exactly uniform under that selected null. For almost every selected observation, the solutions
\[
F_{L,\tau_a,S}(T_a)=1-\alpha/2,
\qquad F_{U,\tau_a,S}(T_a)=\alpha/2
\tag{5.10}
\]
exist, are unique and finite, satisfy \(L<U\), and give
\[
P_\mu\{a^\top\mu\in[L,U]\mid E_k,V_a\}=1-\alpha.
\tag{5.11}
\]
This is an exact finite-sample identity for every finite mean \(\mu\) and known \(\sigma>0\). Null slices or zero-mass exceptional outputs receive an uninformative set and p-value one.
Source: T15.C1 — state_dependent_ebm_research_task15_almost_stable_certification_results_v0_15.md, original line 264
Theorem T15.C1 — Discrepancy bounds and simultaneous false-affirmation control
Status: INHERITED CONFIDENCE-EVENT TRANSFORMATION / COMPLETE CERTIFICATION COROLLARY. Functional equivalence is established methodology [L1–L2].
Use the experiment, actual fit, and radii in §§3–4. Define
\[
L_t^\Delta=\max\left\{0,\sup_u(|\widehat D_t(u)|-r_t(u))\right\},
\qquad
U_t^\Delta=\sup_u(|\widehat D_t(u)|+r_t(u)).
\tag{5.1}
\]
On insufficient-count samples define \([L_t^\Delta,U_t^\Delta]=[0,\infty)\) and abstain. Then
\[
\boxed{\Pr\{L_t^\Delta\le\Delta_\infty\le U_t^\Delta\ \forall t\ge0
\mid\mathscr C_n\}\ge1-\alpha.}
\tag{5.2}
\]
The following reporting rules have simultaneous false-affirmation probability at most \(\alpha\), conditionally on coarse labels and hence unconditionally:
\[
\begin{array}{ll}
U_t^\Delta<\varepsilon_s:&\texttt{CERTIFIED APPROXIMATELY INVARIANT},\\
L_t^\Delta>\varepsilon_v:&\texttt{CERTIFIED MATERIALLY STATE-VARYING}.
\end{array}
\tag{5.3}
\]
If neither rule holds, report \(\texttt{INCONCLUSIVE}\), not invariance. With a common tolerance the labels cannot both occur on the same sample. The error guarantee includes arbitrary selection of an iteration of this one frozen-sample path and any raw anchors/locations whose contrasts are consequences of the same full raw mean event. It is a marginal/simultaneous guarantee, not exact coverage conditional on the event that a particular label or iteration was selected.
Source: T15.F1 — state_dependent_ebm_research_task15_almost_stable_certification_results_v0_15.md, original line 788
Theorem T15.F1 — A sharp, target-specific adequacy gate in a fixed proper table
Status: INHERITED T10B.B2 / COMPLETE OPERATIONAL COROLLARY. The representer mechanism is classical.
For fixed positive \(Q\), a proper linear space \(\mathcal S\) and its \(Q\)-orthogonal projector \(P\), define
\[
v_a=(I-P)Q^{-1}a,\qquad \kappa_a=\|v_a\|_Q.
\tag{10.1}
\]
Then, for all mean tables,
\[
\boxed{|a^\top(P\mu-\mu)|\le\kappa_a A_{\mathcal S,Q}(\mu).}
\tag{10.2}
\]
The bound is sharp over \(\{\mu:A_{\mathcal S,Q}(\mu)\le r\}\): its supremum is \(r\kappa_a\). If \(\kappa_a=0\), the query is preserved for every table. Otherwise no universal constant smaller than \(\kappa_a\) suffices for this norm and class.
On J1/J2's event, any certified adequacy upper bound \(U_A\) gives a valid population-projection fidelity upper bound \(\kappa_a U_A\). For the actual finite fit,
\[
|a^\top(s_t-\mu)|\le
q_{P^\top a}^{\rm box}+\kappa_a U_A+
\|P Q^{-1}a\|_Q E_t^Q
\tag{10.3}
\]
on the same event. Under J3's ball, replace the first term by \(\rho_{\rm ball}\|P Q^{-1}a\|_Q\). J2's observed direct display-error interval is another valid same-event alternative, often more informative when all atomic means are available.
Source: T16.I2 — state_dependent_ebm_research_task16_joint_scientific_adequacy_greedy_certification_results_v0_16.md, original line 554
Theorem T16.I2 — Two computable scientific-fidelity bounds, with distinct projection links
Status: COMPLETE ERROR ACCOUNTING ON I1'S EVENT; no improvement over the direct bound is asserted.
Let \(P_\pi\) project onto \(\mathcal S_h\) under population cell masses, while \(P_q\) uses observed masses. Put \(D_q=\operatorname{diag}(q)\), \(D_\pi=\operatorname{diag}(\pi)\), and
\[
 \kappa_{\pi,a}=\|(I-P_\pi)D_\pi^{-1}a_h\|_\pi,
 \quad
 U_{A,h}=\operatorname{dist}_\pi(\bar Y,\mathcal S_h)
              +\left(\sum_c\pi_cr_c^2\right)^{1/2}.
 \tag{6.1}
\]
Then a valid same-event bound for a four-point scientific error is the sum of these five numerically available terms:
\[
\begin{split}
 |a(s_t)-a(m)|\le{}&\underbrace{\nu_{q,a}E_t}_{\rm optimization}\\
 &+\underbrace{\sum_c|(P_q^\top a_h)_c|r_c}_{\rm conditional\ response\ sampling}\\
 &+\underbrace{|a_h^\top(P_q-P_\pi)\bar Y|
       +\sum_c|((P_q-P_\pi)^\top a_h)_c|r_c}_{\rm empirical/population\ weighting}\\
 &+\underbrace{\kappa_{\pi,a}U_{A,h}}_{\rm finite\ proper\ projection\ bias}
 +\underbrace{4\beta_h}_{\rm raw\ localization}.
\end{split}
 \tag{6.2}
\]
This finite-bin structural term is not confused with the continuous-class modulus.
A different valid bound uses that modulus. Let \(U_A=\widehat A+\epsilon_2\), and evaluate the explicit representatives of \(P_{\mathcal S}H_h\). Then
\[
\begin{split}
 |a(s_t)-a(m)|\le{}&\nu_{q,a}E_t
 +|a(P_qH_h)-a(P_{\mathcal S}H_h)|\\
 &+22\epsilon_\infty+4\mathcal B(U_A).
\end{split}
 \tag{6.3}
\]
The alignment term is observable, includes finite-bin and empirical-weight discrepancies, and is not set to zero. Computing it as written requires the endpoint \(P_q\bar Y\); an endpoint-free version replaces the first two terms by the directly evaluated \(|a(s_t)-a(P_{\mathcal S}H_h)|\). Neither formulation is advertised as saving that solve while secretly using it.
Source: T18.A1 — state_dependent_ebm_research_task18_heterogeneous_state_composition_persistent_certification_results_v0_18.md, original line 133
Theorem T18.A1 — Conditional-state decomposition of the actual proper projector
Status: PROVED HERE; completion of the square/residualization is classical. This explicit identity supplies the actual-Q geometry needed in the new path proof.
For every positive two-state table define
\[
 w_{ij}=q_{ij,+}+q_{ij,-},\quad
 d_{ij}=\frac{q_{ij,+}-q_{ij,-}}{w_{ij}},\quad
 v_{ij}=w_{ij}(1-d_{ij}^2),\quad \zeta=\sum v_{ij},\quad \widetilde w=v/\zeta. \tag{4.1}
\]
All these weights are positive, \(|d_{ij}|<1\), and \(\zeta>0\). For any response residual \(r\), let
\[
 B=(r_+-r_-)/2,\qquad F=(r_++r_-)/2+dB,
 \qquad b=P_A^{\widetilde w}B,                         \tag{4.2}
\]
where \(P_A^{\widetilde w}\) is the weighted additive-feature projection including constants. Then
\[
 \boxed{(P_Qr)_{ij,z}=F_{ij}+(z-d_{ij})b_{ij},}\qquad
 \|P_Qr\|_Q^2=\|F\|_w^2+\zeta\|b\|_{\widetilde w}^2, \tag{4.3}
\]
\[
 \operatorname{dist}_Q(r,\mathcal S)^2
 =\zeta\|B-P_A^{\widetilde w}B\|_{\widetilde w}^2.       \tag{4.4}
\]
Thus computing the proper endpoint requires only one additive solve with \(B_1+B_2-1\) parameters, plus cell operations, not an unstructured full-dimensional solve.
Source: T18.R1 — state_dependent_ebm_research_task18_heterogeneous_state_composition_persistent_certification_results_v0_18.md, original line 573
Theorem T18.R1 — Empirical factorization discrepancy, occupancy and its actual limit
Status: PROVED HERE using classical multinomial concentration. Let IID atomic labels have positive fixed population masses \(\pi_c\), \(M=2B_1B_2\), and \(\pi_{\min}>0\). Write
\[
 q_c=N_c/n,\quad \widehat p_z=\sum_{ij}q_{ij,z},\quad
 \widehat w_{ij}=\sum_zq_{ij,z},\quad
 \widehat\delta=\max_{ij,z}\left|\frac{q_{ij,z}}
 {\widehat p_z\widehat w_{ij}}-1\right|.                \tag{9.1}
\]
On incomplete samples the robust full-grid procedure abstains or uses a separately proved supported-space method; the missing values are not set to zero.
For \(0<u<1\), the event
\[
 \mathcal D_u=\{ |q_c/\pi_c-1|\le u\quad\forall c\}
\]
satisfies
\[
 P(\mathcal D_u^c)\le2M\exp(-n\pi_{\min}u^2/3).        \tag{9.2}
\]
It implies full occupancy; \(n\pi_{\min}(1-u)\ge2\) is a stronger sufficient condition for at least two observations per cell. Require \(n-M>0\) separately when constructing a saturated Gaussian scale.
If the population factorizes as \(\pi_{ij,z}=p_z w_{ij}\), then
\[
 \widehat\delta\le\phi(u):=\frac{1+u}{(1-u)^2}-1
 =\frac{3u-u^2}{(1-u)^2}\quad\hbox{on }\mathcal D_u.    \tag{9.3}
\]
For a general population define
\[
 \delta_\pi=\max_{ij,z}\left|\frac{\pi_{ij,z}}
 {p_z w_{ij}}-1\right|.
\]
Then
\[
 |\widehat\delta-\delta_\pi|\le(1+\delta_\pi)\phi(u)
 \quad\hbox{on }\mathcal D_u.                          \tag{9.4}
\]
In particular, at fixed dimension, \(\widehat\delta\to\delta_\pi\) in probability, not necessarily zero. In either balanced H-family of §3, \(\delta_\pi=|\theta|\).
Source: T20.I1 — state_dependent_ebm_research_task20_scientific_fidelity_capacity_cost_results_v0_20.md, original line 757
Theorem T20.I1 — One honest Gaussian experiment and separate certification fields
Status: CLASSICAL / MATCHED CONFIDENCE-EVENT INFERENCE; complete calibration and constrained-path consequences.
For each raw atom c, observe \(N_c\ge1\) independent replicates
\[
Y_{c\ell}=\mu_c+\epsilon_{c\ell},\quad
\epsilon_{c\ell}\stackrel{\mathrm{ind}}\sim N(0,\sigma^2),
\quad\sigma>0\text{ unknown},\quad\mu\in\mathbb R^M.
\]
Let \(n=\sum_cN_c>M\), \(q_c=N_c/n\), \(f=n-M\), \(y_c=\bar Y_c\), and
\[
\widehat\sigma^2=\frac1f\sum_c\sum_{\ell=1}^{N_c}(Y_{c\ell}-y_c)^2.
\]
For \(0<\alpha_{\rm err}<1\), put
\[
\rho=\widehat\sigma\sqrt{\frac{M F_{M,f}(1-\alpha_{\rm err})}{n}}.
\]
Then
\[
\boxed{\Pr\{\|y-\mu\|_Q\le\rho\}=1-\alpha_{\rm err}.}              \tag{11.1}
\]
On this one event, all the following bounds hold simultaneously, over every row in any predeclared finite universe and every iterate of (10.4).
Raw scientific information and calibrated rows:
\[
|a^\top y-a^\top\mu|\le\rho\sqrt{a^\top Q^{-1}a},
\qquad a^\top s_t=a^\top y\quad(a\text{ a row of }A_*).              \tag{11.2}
\]
Proper class adequacy: for \(A_Q(\mu)=\operatorname{dist}_Q(\mu,\mathcal S)\),
\[
\bigl(\operatorname{dist}_Q(y,\mathcal S)-\rho\bigr)_+
\le A_Q(\mu)\le \operatorname{dist}_Q(y,\mathcal S)+\rho=:U_A.       \tag{11.3}
\]
An exact distance solve here has a real cost; an independently proved upper/lower envelope may be used instead.
Actual fitted table:
\[
(\|s_t-y\|_Q-\rho)_+\le\|s_t-\mu\|_Q\le\|s_t-y\|_Q+\rho.         \tag{11.4}
\]
Uncalibrated query and all later constrained iterates: define
\[
\nu_{b,T}=\sqrt{b^\top T_QQ^{-1}T_Q^\top b},\qquad
\kappa_{b,T}=\sqrt{b^\top(T_Q-I)Q^{-1}(T_Q-I)^\top b},
\]
\[
C_b(t)=\|P_{\mathcal W}^QQ^{-1}b\|_Q E_t.
\]
Then
\[
\boxed{\sup_{u\ge t}|b^\top(s_u-\mu)|
       \le C_b(t)+\rho\nu_{b,T}+\kappa_{b,T}U_A.}                  \tag{11.5}
\]
For b in the row space of \(A_*\), the optimizer and structural-bias factors vanish and \(\nu_{b,T}=\sqrt{b^\top Q^{-1}b}\). The same-event direct observed-discrepancy bound
\[
|b^\top(s_t-\mu)|\le |b^\top(s_t-y)|+\rho\sqrt{b^\top Q^{-1}b}
\]
is also available for a current iterate; it does not describe all later movement without an added valid path allowance.
Source: T22.A1 — state_dependent_ebm_research_task22_five_question_theoretical_validation_results_v0_22.md, original line 113
Proposition T22.A1 — The invariance hierarchy and its limits
Status: CLASSICAL / INHERITED DISTINCTIONS, COMPLETE ARGUMENT. Assume common support across the compared environments and the required conditional versions and moments.
Conditional-law equality across environments is equivalent to \(Y\perp E\mid X,Z,A=a\), interpreted almost surely under the mixture law. It implies conditional-mean equality. Mean equality implies equality of all supported anchored fixed-state shapes. The latter implies equality of their state-modulation differences. None of the last three implications reverses in general.
Source: T22.D1 — state_dependent_ebm_research_task22_five_question_theoretical_validation_results_v0_22.md, original line 487
Theorem T22.D1 — Exact state-information value for squared loss
Status: CLASSICAL CONDITIONAL-PROJECTION THEOREM; COMPLETE PROOF AND CROSS-QUESTION CONSEQUENCES. Fix one held-out law with \(EY^2<\infty\). Let
\[
 m_{XZ}=E[Y\mid X,Z],\qquad m_X=E[Y\mid X],\qquad
 V_Z=E[(m_{XZ}-m_X)^2].
\]
For every square-integrable state-aware predictor f,
\[
 R(f)=E[(Y-f)^2]=E[\operatorname{Var}(Y\mid X,Z)]+E[(f-m_{XZ})^2],
\]
\[
 \boxed{R(m_X)-R(m_{XZ})=V_Z\ge0.}
 \tag{4.2}
\]
For a predictor learned on an independent training sample, these statements hold conditional on the training output, with f then fixed. In particular,
\[
 R(m_X)-R(\widehat f)=V_Z-E[(\widehat f-m_{XZ})^2\mid\text{training}].
 \tag{4.3}
\]
Source: T22.E1 — state_dependent_ebm_research_task22_five_question_theoretical_validation_results_v0_22.md, original line 579
Theorem T22.E1 — A legitimate prediction or action comparison
Status: CLASSICAL CONDITIONAL EVALUATION AND RANDOMIZATION PRINCIPLES; THE PROTOCOL IS FULLY SPECIFIED. Let \(\mathcal F_{\mathrm{tr}}\) include all discovery, bin/state/feature selection, tuning, fitting, source selection, and action-map choices. Conditional on it, let K resulting comparison rules be fixed. Evaluate them on independent full held-out clusters. For each comparison k, define the paired cluster loss difference
\[
 D_{k,t}=\text{loss of baseline in cluster }t-
                  \text{loss of candidate in cluster }t,
 \qquad G_k=E[D_{k,t}\mid\mathcal F_{\mathrm{tr}}].
\]
Positive G means the candidate is better under this exact held-out law and loss.
With conditional finite second moments and IID held-out clusters, \(\sqrt T(\bar D-G)\) has its full conditional covariance limit. With a conditionally stationary known finite dependence range, the covariance is the long-run sum instead. A correctly calibrated simultaneous event controls all K comparisons. A predeclared meaningful improvement \(\delta_k>0\) is certified only when a valid lower confidence bound for \(G_k\) exceeds \(\delta_k\). Otherwise the result is inconclusive or adverse; a positive point estimate is not enough.
For a finite-sample route, if D belongs to a known interval and the held-out process has a known finite dependence range, apply B1 to independent subsequences, or I2 with U≡1, with error allocation over K. For a separate exact Gaussian route, suppose the held-out mean vector y has known covariance \(\Sigma\) and Gaussian error. Then for fixed f,b and evaluation masses q,
\[
 \widehat G^{\mathrm{pred}}=\sum_c q_c\{2(f_c-b_c)y_c+b_c^2-f_c^2\},
\]
\[
 \operatorname{Var}(\widehat G^{\mathrm{pred}}\mid\mathcal F_{\mathrm{tr}})
 =v^T\Sigma v,\quad v_c=2q_c(f_c-b_c).
 \tag{5.1}
\]
For binary actions from D2,
\[
 \widehat G^{\mathrm{act}}=\sum_c q_c(d_c-d_{b,c})(y_c-\tau),
 \quad\operatorname{Var}(\widehat G^{\mathrm{act}}\mid\mathcal F_{\mathrm{tr}})
 =w^T\Sigma w,\quad w_c=q_c(d_c-d_{b,c}).
 \tag{5.2}
\]
Gaussian intervals are exact conditional on training; a zero coefficient vector gives a deterministic zero difference, not an artificial positive precision claim.
Source: T22.G2 — state_dependent_ebm_research_task22_five_question_theoretical_validation_results_v0_22.md, original line 831
Theorem T22.G2 — Current scientific certification does not require algorithmic equivalence
Status: CLASSICAL CONFIDENCE-SET CONSEQUENCE, WITH A USEFUL ALGORITHM-INDEPENDENT SCOPE. Suppose one event \(\mathcal E\) of probability at least \(1-\alpha\) gives \(|y_c-\mu_c|\le r_c\) for every needed raw cell. Let f be any measurable current prediction table, even fitted or selected using y and not belonging to \(\mathcal S\). Then, simultaneously for every finite supported row q,
\[
 \boxed{|q^T(f-\mu)|\le |q^T(f-y)|+\sum_c|q_c|r_c.}
 \tag{7.3}
\]
For positive normalized Q, let \(r_Q=(\sum_cQ_{cc}r_c^2)^{1/2}\). On the same event,
\[
 \operatorname{dist}_Q(\mu,\mathcal S)
 \in[(\operatorname{dist}_Q(y,\mathcal S)-r_Q)_+,
                   \operatorname{dist}_Q(y,\mathcal S)+r_Q],
\]
\[
 |\|f-\mu\|_Q-\|f-y\|_Q|\le r_Q.
 \tag{7.4}
\]
If f is verified to lie in \(\mathcal S\), additionally
\[
 \boxed{\|f-y\|_Q^2-\|P_Qy-y\|_Q^2=\|f-P_Qy\|_Q^2.}
 \tag{7.5}
\]
Thus a verified excess-loss bound supplies an endpoint-error bound even for a different fitting algorithm.
Source: T23.I2 — state_dependent_ebm_research_task23_changing_support_scientific_fidelity_results_v0_23.md, original line 234
Theorem T23.I2 — No-visit, testing, and honest-width obstructions
Status: MATCHED TASK 21.S2 / TASK 22.I3 MECHANISM, COMPLETE GAUSSIAN VERSION. Consider two P0-G laws with identical labels, common variance, and all cell means equal except \(\mu_*^{(1)}-\mu_*^{(0)}=h\). A raw row with \(a_*\ne0\) changes by \(a_*h\). Extra observations whose laws are identical under the alternatives do not change the following bounds:
\[
 P_0(|\widehat\theta-\theta_0|\ge r)+P_1(|\widehat\theta-\theta_1|\ge r)
 \ge(1-\delta_T)^T,
 \quad 0<r<|a_*h|/2,
\tag{3.8}
\]
\[
 \operatorname{TV}(P_0,P_1)
 \le \min\{1, |h|\sqrt{T\delta_T}/(2\sigma)\}.
\tag{3.9}
\]
For an interval honest at level \(1-\alpha\) under both laws,
\[
 P_0\{\operatorname{diam}C_T\ge|a_*h|\}
 \ge 1-2\alpha-\operatorname{TV}(P_0,P_1).
\tag{3.10}
\]
If law 0 satisfies approximate equivalence and law 1 violates it, any rule whose false-equivalence probability under law 1 is at most \(\alpha\) has power under law 0 at most \(\alpha+\operatorname{TV}(P_0,P_1)\).
Source: T23.G1 — state_dependent_ebm_research_task23_changing_support_scientific_fidelity_results_v0_23.md, original line 733
Theorem T23.G1 — Regular model fitting can converge to incorrect raw science
Status: PROVED HERE — COMPLETE SINGLE-DELETION EXTENSION OF THE LITERAL GREEDY PROJECTION ARGUMENT; NOT A PACKAGE THEOREM. Retain the original twelve trees, fixed \(0<\eta<2\), zero start, exact full-leaf mean updates and earliest-index maximal-gain choice. Fix either Q-RARE or U-RARE with \(\delta_T\to0\). Use the P0-G sampling law, a fixed bounded proper table s, a fixed finite \(\gamma\), and
\[
 \mu_T=s+\gamma e_*.
\tag{9.1}
\]
The conclusions about geometric regularity also hold for any other uniformly bounded finite mean sequence with this same single-deletion design.
With probability tending to one, every core cell is observed and the empirical proper Gram matrix
\[
 \widehat G_T=H^T\widehat Q_TH,\qquad
 \widehat Q_T=\operatorname{diag}(N_c/T)
\]
is positive definite, even if the rare cell has no observations. The unique empirical proper table is
\[
 \widehat s_T=H\widehat\beta_T,\qquad
 \widehat\beta_T=\widehat G_T^{-1}\frac1T\sum_{t=1}^T h_{C_t}Y_t.
\tag{9.2}
\]
Here \(h_c=H_{c,\cdot}^T\). No raw mean is imputed at a missing cell: equation (9.2) fits the observed loss and uses the model's uniquely determined completion.
Let \(\lambda(\widehat Q_T)\) be the exact average-frame minimum of the twelve leaf projectors on \(\mathcal S\), with norm induced by \(\widehat Q_T\). Then there is a neighborhood of the deleted-cell population design and a constant \(\lambda_*>0\) on which
\[
 \lambda(\widehat Q_T)\ge\lambda_*.
\tag{9.3}
\]
This does not require \(T\delta_T\to\infty\). For the actual fit \(s_{T,t}\), write \(e_{T,t}=\widehat s_T-s_{T,t}\). For every realized core-occupied design,
\[
 \|e_{T,t+1}\|_{\widehat Q_T}^2
 =\|e_{T,t}\|_{\widehat Q_T}^2
 -\eta(2-\eta)\max_k\|P_{k,\widehat Q_T}(y-s_{T,t})\|_{\widehat Q_T}^2,
\tag{9.4}
\]
where y contains the observed cell means and arbitrary unused values at empty cells. Both the fitting rule and (9.4) are independent of those unused values. The usual geometric and gain/frame envelopes hold for every future iteration on the same sample.
An exact design-only schedule
\[
 t_T=\left\lceil\frac{(1+\zeta)\log T}{\eta(2-\eta)\lambda(\widehat Q_T)}\right\rceil,\qquad\zeta>0,
\tag{9.5}
\]
or the same schedule with a verified positive lower frame bound that stays bounded below in this neighborhood, has \(t_T=O_p(\log T)\) and
\[
 \max_c|s_{T,t_T,c}-\widehat s_{T,c}|=o_p(T^{-1/2}).
\tag{9.6}
\]
Nevertheless, for the spike in Q-RARE,
\[
 a_I^Ts_{T,t_T}\longrightarrow a_I^Ts,
 \qquad a_I^T\mu_T=a_I^Ts+\gamma.
\tag{9.7}
\]
In particular, with s=0, \(\gamma=1\), and \(0<\varepsilon<1\), a false raw approximate-invariance declaration based on
\[
 |a_I^Ts_{T,t_T}|+z_{1-\alpha/2}\frac{\sigma}{\sqrt T}
       \sqrt{(H^Ta_I)^T\widehat G_T^{-1}(H^Ta_I)}<\varepsilon
\tag{9.8}
\]
has probability tending to one. Formula (9.8) incorrectly interprets a model-noise width as a raw scientific interval. A valid raw interval or a valid bias-retaining display certificate is not contradicted.
Source: T24.E1 — state_dependent_ebm_research_task24_information_preserving_continuous_state_discretization_results_v0_24.md, original line 271
Proposition T24.E1 — Exact within-bin shape, level, and composition decomposition
Status: PROVED HERE; AN EXACT CONDITIONAL-MIXTURE IDENTITY, RELATED TO BUT NOT IDENTICAL WITH TASK 19.M1. Fix a bin and matched feature settings \(x,x_0\). Let \(P_{e,x}=\Pi_{e,k,x}\), \(P_{e,0}=\Pi_{e,k,x_0}\),
\[
 g_e(z)=m_e(x,z)-m_e(x_0,z),\qquad b_e(z)=m_e(x_0,z),
\]
and \(G_e=\int m_e(x,z)dP_{e,x}-\int m_e(x_0,z)dP_{e,0}\). With \(\delta g=g_1-g_0\), \(\delta b=b_1-b_0\), and \(\delta P_x=P_{1,x}-P_{0,x}\), \(\delta P_0=P_{1,0}-P_{0,0}\),
\[
\boxed{
 G_1-G_0
 =P_{0,x}\delta g+(P_{0,x}-P_{0,0})\delta b
 +\delta P_x\,m_1(x,\cdot)-\delta P_0\,m_1(x_0,\cdot).
}
\tag{4.3}
\]
Here \(Pf\) means \(\int f\,dP\). All integrals are assumed finite. If \(\|\delta g\|_\infty\le\varepsilon\), the first term is bounded by \(\varepsilon\), but the second need not be small without a level/kernels restriction.
Source: T24.I1 — state_dependent_ebm_research_task24_information_preserving_continuous_state_discretization_results_v0_24.md, original line 846
Theorem T24.I1 — A bounded-data bin-to-raw and current-output confidence report
Status: CLASSICAL CONCENTRATION AND CONFIDENCE-EVENT TRANSFORMATION; COMPLETE SCOPE-SPECIFIC PROOF. For one predetermined partition, observe T IID full records, and assume a supplied response range \([L_Y,U_Y]\) of length R. Let D predeclared feature/bin/environment cells be required. At an occupied cell use its empirical mean \(y_c\) and
\[
 r_c=R\sqrt{\frac{\log(2D/\alpha)}{2N_c}}.
 \tag{10.1}
\]
Use an uninformative interval for an empty required cell. Then all ordinary coarse means are covered simultaneously with probability at least \(1-\alpha\), conditionally on their coarse labels and hence unconditionally.
For each declared raw scientific query q, let a be its matched coarse row, combine repeated cell coefficients, and suppose a valid supplied deterministic bound satisfies
\[
 |a^T\mu-q(m)|\le\beta_{\mathcal P,q}.
 \tag{10.2}
\]
Then on the same event,
\[
 \boxed{q(m)\in
 [a^Ty\ \pm\{\sum_c|a_c|r_c+\beta_{\mathcal P,q}\}],}
 \tag{10.3}
\]
and for any measurable current prediction table f, including an output selected using these same observations,
\[
 \boxed{|a^Tf-q(m)|\le
 |a^Tf-a^Ty|+\sum_c|a_c|r_c+\beta_{\mathcal P,q}.}
 \tag{10.4}
\]
The table need not belong to \(\mathcal S_K\). A random bias bound from a separate calibrated event adds that event's failure probability; an unknown population bias cannot simply be inserted as though observed.
Source: T25.I1 — state_dependent_ebm_research_task25_estimated_moments_scientific_fidelity_results_v0_25.md, original line 152
Theorem T25.I1 — A simultaneous moment/response event and a class-closure bound
Status: PROVED IN T25 — classical bounded concentration and exact class algebra. Fix a finite family of partitions and environments before inference. For each required cell let \(N_c^M,N_c^Y\) be the respective counts, and let \(\widehat M_c,\widehat\mu_c\) be its observed means when occupied. Suppose the basis on that cell lies in an interval of known length \(R^M_c\) and Y in an interval of known length \(R_Y\). For a cell family of size D and allocated failure probability \(\alpha_M\),
\[
 r_c^M=R_c^M\sqrt{\frac{\log(2D/\alpha_M)}{2N_c^M}}
 \tag{4.1}
\]
provides a simultaneous conditional-on-pilot-labels moment event. The analogous response formula with \(\alpha_Y,R_Y,N_c^Y\) provides its conditional-on-response-labels mean event. Empty cells receive the full supplied range, or an uninformative set if no range is supplied. Then the joint event has probability at least \(1-\alpha_M-\alpha_Y\). A finite union over partitions/environments remains valid without independence between alternative analyses of the same records.
For \(\phi=z\), \(R_c^M=h_k\), not one. This uses the known location of a pilot state inside its bin. Conditioning on exact pilot Z would instead make the pilot estimate deterministic and does not give the sampling statement in (4.1).
Source: T25.I2 — state_dependent_ebm_research_task25_estimated_moments_scientific_fidelity_results_v0_25.md, original line 213
Theorem T25.I2 — Joint inversion, including weak and partial identification
Status: PROVED IN T25 — confidence-region projection, a classical construction. On I1's event let \(\mathcal I_M\) be the moment interval box intersected with any genuinely supplied admissibility restrictions, and \(\mathcal I_Y\) the response-mean box. For a supplied parameter class \(\Theta\), define
\[
 \mathcal C=\{(\theta,M'): \theta\in\Theta,\ M'\in\mathcal I_M,
                         \ T(M')\theta\in\mathcal I_Y\}.
 \tag{5.1}
\]
Then the projection
\[
 C_\ell=\{\ell^T\theta:(\theta,M')\in\mathcal C\}
 \tag{5.2}
\]
contains the true raw query simultaneously for every declared \(\ell\), with at least the joint-event coverage probability. No estimated singular-value threshold or division by an estimated moment gap is required. The convex hull of (5.2) is a valid, potentially more conservative interval.
Source: T25.F1 — state_dependent_ebm_research_task25_estimated_moments_scientific_fidelity_results_v0_25.md, original line 786
Proposition T25.F1 — Joint raw decisions, model adequacy, and current-output fidelity
Status: PROVED IN T25 — deterministic consequences of the correctly specified confidence event. Suppose I2 or I3 provides a joint raw interval \([\widehat q_j\pm R_j]\) for a declared finite scientific family, including the required environmental and curvature rows. Then the true maximum absolute environmental drift lies between
\[
 L_\Delta=\max\{0,\max_j(|\widehat q_j|-R_j)\},\qquad
 U_\Delta=\max_j(|\widehat q_j|+R_j).
 \tag{12.1}
\]
Certify approximate raw stability only if \(U_\Delta<\varepsilon_S\), material drift only if \(L_\Delta>\varepsilon_D\), otherwise report inconclusive. Raw curvature uses its own signed row and its own positive materiality threshold. No inference of nonlinearity from stability is made.
For any observed current coarse prediction table f and its specified comparison row a,
\[
 \boxed{|a^Tf-q(m)|\le|a^Tf-\widehat q|+R_q.}
 \tag{12.2}
\]
This holds simultaneously for every f on the raw event, even if the fit and fitting iteration used the same observations. It does not assert that \(a^Tf\) and \(q(m)\) are the same population functional. It instead audits their actual discrepancy.
End of source extracts / Codex instruction