# Cycle 1 structural equations — implementable DGP

**Mode:** Explore. **Provenance:** `SYNTHETIC_THEORY`. **Monetisation:** forbidden.  
**Gate 3:** not an input. **Stroke coefficients:** none. **Daily coefficients:** none.

This note writes the estimating equation and the Monte Carlo data-generating processes
that `scripts/48_health_econ_monte_carlo.R` implements. Full adversarial critique is in
[`cycle1_adversarial_audit.md`](cycle1_adversarial_audit.md). Notation is shared.

## Analysis of record (AOR)

\[
\begin{aligned}
Y_t &\sim \mathrm{NB2}(\mu_t,\kappa),\\
\log\mu_t &= \log d_t + \alpha + \theta X_t + \lambda_{m(t)} + B_4(q_t)^\top\zeta.
\end{aligned}
\]

`SYNTHETIC` Monte Carlo defaults: \(n=132\), \(\kappa=0.02\) (MASS `theta` \(=50\)),
CHD-like baseline mean \(1100\), HF-like \(220\),
\(\theta\in\{0,\log 1.02,\log 1.07\}\), \(400\) size/power reps unless
`HE_MC_REPS` overrides. Count magnitudes are inspired by published annual totals and
are **not** monthly means from HA microdata.

Existing exploratory interval widths used only as ADR/CATD denominators
(`EXISTING_EXPLORATORY_INTERVAL`, Gate 3 open, not a freeze):

- HF cold days /5: \(\log 1.144-\log 1.006\)
- CHD hot nights /5: \(\log 1.042-\log 1.002\)

## HE-01 stock-flow

\[
E[Y_t\mid S_t]\approx S_t h_0\exp(\theta X_t)\,d_t,\quad
S_{t+1}=S_t-Y_t+I_t,\quad I_t\sim\mathrm{Poisson}(\rho S_t p_t).
\]

Kill test: empirical size of \(H_0:\theta=0\) under adversarial depletion
(\(\rho\in\{0.6,0.8,1.0\}\) and a 2020 inflow freeze). If size stays near \(0.05\),
the objection is a costing caveat, not an identification failure. Adversary still
kills the *liability level* because \(S_t\) is unobserved.

## HE-03 daily capacity (likely_fail)

\[
Q_{tj}=\min(D_{tj},K),\qquad Y_t=\sum_{j=1}^{d_t}Q_{tj}.
\]

Kill test: relative attenuation of monthly \(\hat\theta\) versus uncensored demand
at utilisation \(u\in\{0.85,0.95,0.99\}\).

## HE-05 harvesting

\[
\log\mu_t=\log d_t+\alpha+\beta_0 X_t+\beta_1 X_{t-1}+\beta_2 X_{t-2}+\lambda_{m(t)}+B_4^\top\zeta,
\quad \sum_{k=0}^{2}\beta_k=(1-\phi)\beta_0.
\]

Kill test: power at \(n=132\) to reject \(\phi=0\) when \(\phi=0.6\).

## HE-07 visibility (survivor → SEW)

\[
\varepsilon_Y=\varepsilon_M+\frac{\partial\log\omega}{\partial X},\qquad
\omega=1-\Phi(c_0-\mu_s+(c_T-b_T)X).
\]

Statistic: selection-envelope width
\(\mathrm{SEW}(\Gamma)=Q_{0.975}(\varepsilon_M-\varepsilon_Y)-Q_{0.025}(\varepsilon_M-\varepsilon_Y)\)
over a pre-specified grid \(\Gamma\) of threshold movement, plus sign-stability
\(\mathrm{SS}=\Pr(\varepsilon_M>0)\). Lower-bound reading fails unless
\(\mathrm{SS}\ge 0.95\) and SEW is inside tolerance.

## HE-08 regime mix (survivor → RTE)

\[
\bar\theta \approx w_0\theta_0+w_1\theta_1,\qquad
w_r=\frac{\sum_{R_t=r}\widetilde X_t^2}{\sum_t\widetilde X_t^2}.
\]

Statistic: regime transportability envelope
\(\mathrm{RTE}=\max_{r,r'}|\beta_r-\beta_{r'}|\). Pass only if the upper limit sits
below a pre-specified transport tolerance (default `SYNTHETIC` \(\log 1.05\)).

## HE-10 unit-value aggregation (survivor → ADR)

Daily mean \(g(T)\) is **imposed**, never recovered (distinct from failed M|D):

\[
\log g(T)=a+b_c(26-T)_+^2+b_h(T-26)_+^2.
\]

\[
\mathrm{ADR}(g)=\frac{|\beta_{\mathrm{month}}(g)-\beta_{\mathrm{target}}(g)|}{0.5\cdot\mathrm{CI}_{\mathrm{existing}}}.
\]

Cosmetic only if the 95th-percentile ADR \(<1\) and coverage holds under
MCAR/MAR/MNAR, macro shock, and selection.

## Escalation operators (mandatory on survivors)

Missingness after the latent panel exists:

\[
\mathrm{logit}\Pr(O_t=1)=a_0+a_X|X_t|+a_Y\mathrm{std}\{\log(1+Y_t^*)\}.
\]

Macro factor with February impulses:

\[
U_t=\xi_{20}\mathbf{1}\{t=\mathrm{2020\text{-}02}\}+\xi_{22}\mathbf{1}\{t=\mathrm{2022\text{-}02}\}+e_t,\quad e_t=0.4 e_{t-1}+\nu_t.
\]

Threshold selection: keep each latent event with probability \(\Phi(-c_0-c_T X_t)\).

## Naive cost-of-illness is not a model

\(C_{\mathrm{naive}}=c\sum_t(\hat\mu_t(X_t)-\hat\mu_t(X^{\mathrm{ref}}))\) silently
imposes \(\rho=1\), \(\gamma_T=0\), \(\phi=0\), \(\omega(T)=\omega_0\). HE-01, HE-02,
HE-05, and HE-07 each kill one equality. No currency may be attached.

## Cycle 2 composition (HE-C2-10)

Signed composite after daily top-truncation then monthly aggregation:

\[
\mathrm{CATD}=\frac{\beta_{\mathrm{month}}-\beta_{\mathrm{target}}}{0.5\cdot\mathrm{CI}_{\mathrm{existing}}}.
\]

Report median and 5th/95th percentiles **by contrast**. A cancellation region where
\(|\mathrm{CATD}|\) is small because two biases offset is a calibration coincidence,
not validity.

DAGs for the laboratory UI: [`dags.json`](dags.json).
