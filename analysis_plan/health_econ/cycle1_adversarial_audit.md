# Cycle 1 adversarial health-economics audit

**Mode:** Explore
**Date:** 14 August 2026
**Provenance:** `SYNTHETIC_THEORY`
**Status:** No findings. No Gate 3 freeze. No monetisation. No stroke coefficients.

This is a hostile referee report on HE-01–HE-12. “Kill” means that the
economic claim, as currently formulated, is not identified by the available
design. It does not mean that the underlying biological or institutional
story is false. “Survive-to-escalation” means only that a base simulation or
refit could be informative; it earns no claim until it passes the specified
adversarial stress tests. “Park-confirmed” means that there is no credible
single-territory identification design to run now.

## Attack frame

The record is 132 territory-months, with separate negative-binomial models,
calendar-month fixed effects, `ns(time, 4)`, and a days-in-month offset. The
outcome is a first recorded CHD or HF hospitalisation after first diagnosis in
a T2D/HTN cohort. Admission cause is absent. The observed series halves from
2013 to 2023, while the available 35+ denominator rises. The influential
months are 2020-02 and 2022-02; 141 of 145 cold days occur in DJF. All core
q-values exceed 0.19; HF cold days per five is 1.073 (1.006–1.144), and CHD
hot nights per five is 1.022 but SE-sensitive. The M|D daily-recovery
calibration failed 500 synthetic replicates. These are design facts, not
health-economic findings.

Every escalation below is mandatory if the base test fails to kill a
hypothesis:

1. **Missingness:** delete months under MCAR, MAR, and MNAR mechanisms, with
   missingness depending on `Y_t`, on exposure extremes, and on both. Refit
   the exact analysis of record and record estimand-specific coverage, bias,
   and rejection rates.
2. **Correlated macro shock:** add an unobserved shock that is correlated with
   both `T_t` and `Y_t`, with smooth, seasonal, pandemic-like, and
   exposure-extreme versions. A COVID dummy is not an adequate substitute for
   this stress.
3. **Severe selection:** impose an absorbing first-event state and a
   heat-dependent observation/admission threshold. Allow the threshold to
   move with capacity, access, and latent severity. A simulation without
   these features is not a stress test of this dataset.

For any simulation, the parent must report the data-generating parameters,
the estimand used as “truth”, the exact missingness and selection rules, and
coverage—not only whether the fitted coefficient has the expected sign.

## Executive kill board

| Rank | Hypothesis | Verdict | Reason for attack |
|---:|---|---|---|
| 1 | HE-06 | `PARK-CONFIRMED` | Fiscal preference parameters and a within-year budget cycle are not identified in one territory with month fixed effects. |
| 2 | HE-11 | `PARK-CONFIRMED` | There is no spatial or household dimension with which to identify adaptation capital. |
| 3 | HE-03 | `KILL` | A daily capacity censoring operator and an unobserved shadow price cannot be recovered from monthly first events. |
| 4 | HE-04 | `KILL` | EVPI is arbitrary without an agreed utility, prior, decision-maker, and deadline; the claim-set point is governance, not an estimated economic parameter. |
| 5 | HE-12 | `KILL` | Calendar composition is neither a defensible exclusion restriction nor a strong first-stage instrument here. |
| 6 | HE-09 | `KILL` | Public-only counts cannot support a territory-wide total-utilisation claim without a private-sector series. |
| 7 | HE-01 | `KILL` | The stock and inflow are unobserved; a trend spline cannot identify a finite-risk-pool valuation. |
| 8 | HE-02 | `KILL` | The observed count is the product of latent need and conversion; no current variable shifts conversion alone. |
| 9 | HE-05 | `KILL` | First-event data cannot reveal whether an event was brought forward from a later event that is structurally absent. |
| 10 | HE-08 | `SURVIVE-TO-ESCALATION` | Regime heterogeneity is a live transportability threat, but a pre-specified cross-regime test can still be run. |
| 11 | HE-07 | `SURVIVE-TO-ESCALATION` | Selection into admission is central and unresolved; an auxiliary morbidity series could narrow, but not automatically solve, it. |
| 12 | HE-10 | `SURVIVE-TO-ESCALATION` | Aggregation distortion is testable with public weather data, but any conclusion is conditional on the imposed daily response. |

This ranking is about how quickly the *claim* can be killed, not about how
important the underlying mechanism might be.

## HE-01 — depletion stock-flow

### 1. Fatal identification objection

`S_t`, the still-at-risk diagnosed stock, and `I_t`, the inflow of newly
diagnosed people, are both unobserved. The observed count is compatible with
an exhaustible stock, changing diagnosis ascertainment, changing cohort
composition, changing coding, or some combination. A four-degree-of-freedom
time spline is not a measurement of `log(S_t)`, and the 35+ denominator is not
the T2D/HTN diagnosed person-time denominator. Therefore neither replacement
ratio `rho = I_t/Y_t` nor a finite liability is identified.

### 2. Observational equivalence

The same declining count path can be generated by: (i) true depletion; (ii)
falling diagnosis incidence or referral; (iii) a changing risk-set definition;
(iv) public-sector routing changes; (v) an unobserved macro shock; or (vi)
selection into the first recorded event. The thermal coefficient can be the
same under all six constructions after the spline and month effects are
fitted.

### 3. Why the proposed kill-test is insufficient

A Monte Carlo that supplies the parent with a known synthetic stock path and
then recovers nominal size only establishes that the chosen spline handles
that chosen path. It does not show that the real stock is observed, that
inflow is stable, or that left truncation is harmless. The test can pass while
the economic valuation remains unidentified because the missing stock is the
object being valued.

### 4. Escalation stress

- Missingness must depend on high counts, extreme temperatures, and the
  depletion state, not only on random month deletion.
- The unobserved macro shock must jointly move diagnosis/inflow and thermal
  exposure, with curvature that resembles but is not equal to `ns(time, 4)`.
- Selection must make the first-event absorbing state and the admission
  threshold heat-dependent, so that the observed decline can arise without
  true stock depletion.

### 5. Verdict: `KILL`

The finite-stock economic object cannot be recovered from these aggregates.
The observed decline may motivate a limitation statement, but it cannot
license a stock valuation or a future event-flow projection.

## HE-02 — need versus conversion

### 1. Fatal identification objection

With latent biological need `N_t` and conversion probability `pi_t`,

`E[Y_t] = N_t * pi_t`,

so the count equation observes only `log(N_t) + log(pi_t)`. Temperature is
allowed to enter both terms. There is no current variable that shifts
conversion while leaving need unchanged, and no admission-reason or A&E
process is available to construct one. The thermal count ratio is not a
welfare or pathophysiological elasticity.

### 2. Observational equivalence

A positive count ratio can mean more biological deterioration, easier access,
more caregiver availability, less avoidance of hospitals, queue release, or
some mixture. A null can mean no biological effect, offsetting conversion,
capacity rationing, or outcome depletion. Each produces the same reduced-form
monthly coefficient.

### 3. Why the proposed kill-test is insufficient

Adding holiday or rest-day counts and observing an unchanged `theta` does not
prove `gamma_T = 0`. A weak instrument can leave the coefficient unchanged
because it has no first-stage power. The exclusion can also fail through
activity, diet, caregiver behaviour, or Lunar New Year timing. A Monte Carlo
with a valid, strong, truly exogenous instrument can pass while the real
calendar variable is endogenous.

### 4. Escalation stress

- Make missingness depend on conversion difficulty, observed `Y_t`, and
  exposure extremes; otherwise the first-stage and second-stage checks are
  too clean.
- Add an unobserved access shock that moves both temperature exposure patterns
  and observed admissions, rather than controlling for it with a binary
  pandemic dummy.
- Make the admission threshold heat-dependent and first events absorbing;
  under rationing, `pi_t` becomes a queue-clearing rule rather than a care-
  seeking probability.

### 5. Verdict: `KILL`

The current data identify realised public first hospitalisation counts only.
They do not separate need from conversion, and HE-12 does not supply a
credible exclusion restriction.

## HE-03 — bed shadow price

### 1. Fatal identification objection

The target `lambda_t` is a supply-side multiplier on an unobserved daily
capacity constraint. Neither bed-day capacity nor occupancy, elective
displacement, length of stay, nor cluster is observed. Monthly sums do not
invert a daily `min(D_d, K_d)` operator. Even the sign of attenuation is not
reliably known when capacity, elective cancellations, and referral routing
respond to anticipated weather.

### 2. Observational equivalence

Attenuation of a thermal association can arise from capacity rationing,
depletion, macro demand destruction, exposure measurement error, or ordinary
negative-binomial overdispersion. A stable monthly count ratio can arise under
binding capacity if electives are displaced first, or under no capacity
constraint if latent need is weak.

### 3. Why the proposed kill-test is insufficient

A daily censoring Monte Carlo with a selected utilisation range and a known
`K_d` can show less than a synthetic two-percent attenuation. That is a
calibration result for an assumed operator, not evidence that `lambda_t` is
identified. The simulation can pass because it omits endogenous capacity,
elective substitution, hospital heterogeneity, and first-event selection.

### 4. Escalation stress

- Delete months when capacity records would be most likely to be missing:
  high `Y_t`, extremes, and high latent occupancy.
- Correlate the unobserved capacity/planning shock with both thermal exposure
  and admissions; do not replace it with a pandemic dummy.
- Apply severe daily rationing with an absorbing first-event state and a
  heat-dependent threshold, including elective displacement before acute
  displacement.

### 5. Verdict: `KILL`

The bed shadow price is not a recoverable parameter at this grain. It is a
discussion limitation, not a Cycle 1 estimand.

## HE-04 — value of information

### 1. Fatal identification objection

EVPI is not identified by the data. It requires a prior over the missing
quantity, a utility function over claims and delay, a decision set, a
decision-maker, and a deadline. Here the stroke file is absent, person-time
would change the admissible wording more than the point estimate, and the
decision rule is a team governance choice. A numerical VoI is therefore an
elicited policy calculation, not an empirical result.

### 2. Observational equivalence

The same existing posterior can imply zero, large, or negative “value” for
the missing file depending on the prior, scoop loss, publication utility,
co-author loss function, or deadline. No reduced form distinguishes those
utilities.

### 3. Why the proposed kill-test is insufficient

A decision tree can show EVPI below delay cost for a selected family of
priors and still be false as a team recommendation. The Monte Carlo may pass
because it treats the prior and utility as data. Sensitivity over a narrow
elicited range is not a defence when the range itself is the unsupported
assumption. Calling person-time “near-zero posterior value” also does not
make its claim-set value a measured economic quantity.

### 4. Escalation stress

- Let missingness of the stroke file depend on expected effect size, extremes,
  and the outcome itself; compare decisions under informative arrival.
- Add an unobserved macro shock correlated with both the expected new evidence
  and current `T`–`Y` results.
- Let severe first-event selection change which decision would be made after
  the missing file arrives.

### 5. Verdict: `KILL`

Do not report a numeric EVPI. If the team wants a decision memo, report the
assumptions and a qualitative ordering of data requests; that is governance,
not an identified health-economic parameter.

## HE-05 — harvesting and displacement fraction `phi`

### 1. Fatal identification objection

The proposed displacement test needs later admissions from the same risk set
to reveal events brought forward. The outcome is a first event. After that
event the person disappears from the risk set, so the counterfactual later
event that would identify `phi` is structurally unobserved. Monthly lag
coefficients cannot distinguish intertemporal displacement from persistent
need, delayed decompensation, seasonal clustering, or stock depletion.

### 2. Observational equivalence

Positive lag-0 and negative lag-1 terms can be displacement, a temporary
biological response, exposure persistence, weather autocorrelation, or
pandemic timing. Positive lag-1 HF cold-day association is compatible with
delayed decompensation and does not identify either mechanism. A zero sum can
also be produced by cancellation between unrelated lag processes.

### 3. Why the proposed kill-test is insufficient

Power to distinguish `phi = 0` from a synthetic `phi = 0.5` under a known
finite distributed lag only answers whether that simulated lag design is
recoverable. It can pass while the real first-event process has no repeat
event counterfactual. With 132 months, lag terms are also entangled with DJF
clustering, month effects, and the trend spline.

### 4. Escalation stress

- Make missingness depend on the latent post-shock counterfactual and on
  extreme months, so deleted months preferentially erase compensating lags.
- Add a macro shock correlated with both thermal persistence and admissions;
  let it have its own lag structure rather than a single dummy.
- Enforce absorbing first events, heat-dependent thresholds, and severe
  selection. The test must show whether an apparent negative lag can be
  manufactured without displacement.

### 5. Verdict: `KILL`

`phi` is not identified from first-event monthly aggregates. Do not turn lag
sensitivities into an economic harvesting estimate or any monetisation.

## HE-06 — present-biased public budgeting

### 1. Fatal identification objection

The preference parameter `beta` belongs to an institutional planner, not to
the monthly admission count. Fiscal-year seasonality and any month-specific
admission threshold are absorbed by the twelve calendar-month indicators in a
single territory. Adaptation capital, recurrent spending, budget history, and
capital depreciation are not observed.

### 2. Observational equivalence

The same seasonal pattern is consistent with present bias, ordinary
administrative scheduling, weather seasonality, staffing cycles, or coding
changes. A smooth decline can be adaptation investment, depletion, diagnosis
change, or the time spline. Counts cannot distinguish these stories.

### 3. Why the proposed kill-test is insufficient

There is no honest base Monte Carlo that can identify an institutional
preference from these data. A synthetic planner model would pass by
construction because `beta` is supplied to the simulation. A null month
interaction would be absorbed by fixed effects and would not kill or support
present bias.

### 4. Escalation stress

- Treat missing budget and count months as MNAR when extremes or fiscal
  pressure are high.
- Add an unobserved fiscal/macro shock correlated with both thermal exposure
  and admissions, not merely an annual or COVID indicator.
- Add first-event selection and a heat-dependent admission threshold so that
  apparent budget responses cannot be attributed to rationing-free demand.

### 5. Verdict: `PARK-CONFIRMED`

Park pending cluster-level counts, capital and recurrent budgets, adaptation
project histories, and documented budget timing. The current territory series
cannot test this mechanism.

## HE-07 — visibility fraction `omega`

### 1. Fatal identification objection

Admission is a selected tail above an unobserved severity and conversion
threshold. Both latent morbidity and the threshold may move with heat,
access, capacity, and household resources. Thus

`epsilon_Y = epsilon_M + d log(omega(T)) / d log(T)`

does not identify total morbidity, and the admission coefficient is not
automatically a lower bound. First-event selection and depletion make the
threshold composition change over time.

### 2. Observational equivalence

A larger admission association can mean more total morbidity, a lower
heat-dependent threshold, public routing, or a more selected high-risk
remaining stock. A null can mean no morbidity effect or exact cancellation
between morbidity and visibility. An outpatient null is not decisive if
outpatient access and coding respond differently.

### 3. Why the proposed kill-test is insufficient

Comparing one outpatient elasticity with one admission elasticity assumes
common exposure, catchment, coding, timing, and selection. Statistical
indistinguishability is not equality of latent welfare loss. A simulation
with a fixed threshold can make `omega` look invariant while the real
threshold is heat-dependent. The test can therefore pass for the wrong
selection process.

### 4. Escalation stress

- Make outpatient or admission months MNAR as a function of `Y_t` and
  exposure extremes; allow the two sources to have different missingness.
- Add an unobserved macro shock that moves both latent morbidity and
  conversion/access, with correlation to temperature.
- Use an absorbing first-event state and a threshold `s*_t` that changes
  with heat, capacity, and access; include severe threshold movement in the
  sensitivity envelope.

### 5. Verdict: `SURVIVE-TO-ESCALATION`

The selection objection survives because a governed auxiliary morbidity
series could narrow it, but no current result supports a lower-bound or
total-burden interpretation.

### 6. Exact statistic to report

Report the **selection-envelope width (SEW)**:

`SEW(Gamma) = Q_0.975[epsilon_M - epsilon_Y | Gamma] -
              Q_0.025[epsilon_M - epsilon_Y | Gamma]`,

where `Gamma` is a pre-specified bound on heat-dependent threshold movement
and the quantiles are over the full missingness, macro-shock, and absorbing-
selection stress ensemble. Also report the sign-stability share

`SS(Gamma) = Pr[epsilon_M > 0 | Gamma]`.

The lower-bound interpretation **passes** only if the pre-registered
selection envelope is sign-stable (`SS(Gamma) >= 0.95`) and its width is
within the pre-specified scientific tolerance `epsilon_tol`. It **fails**
otherwise. A failure is not evidence of zero morbidity; it kills the
lower-bound claim.

## HE-08 — regime invariance

### 1. Fatal identification objection

The pooled coefficient is a regime-weighted average, not necessarily a
structural temperature response. The two influence months are 2020-02 and
2022-02, and cold-day support is concentrated in DJF. Pandemic access,
avoidance, queueing, and coding can change the mapping from temperature to
recorded first events. Three pandemic winters cannot support a precise
regime interaction with the existing trend and month effects.

### 2. Observational equivalence

A pre/post difference can reflect a changed thermal response, a macro shock,
seasonal composition, depletion, exposure measurement, or a changing
threshold. Overlapping intervals can arise under true invariance with low
power or under meaningful non-invariance with noisy estimates.

### 3. Why the proposed kill-test is insufficient

An influence-month exclusion or a binary COVID interaction can leave direction
unchanged while the magnitude is non-transportable. A conventional
non-rejection of equality is especially weak with three pandemic winters.
A Monte Carlo with correctly specified binary regimes and independent shocks
can pass while the real regime is continuous, endogenous, and correlated with
temperature extremes.

### 4. Escalation stress

- Delete months MNAR by regime, `Y_t`, and extremes; allow missingness to
  differ before and during access disruption.
- Add a continuous unobserved macro shock correlated with both temperature
  and admissions, with a February concentration but no binary label.
- Combine regime changes with an absorbing first-event state and a
  heat-dependent threshold; allow the threshold to respond to pandemic
  access and capacity.

### 5. Verdict: `SURVIVE-TO-ESCALATION`

The regime-invariance objection is testable but not resolved by the existing
influence exclusion or pre-2020 split. No pooled coefficient should be
treated as policy-invariant before the escalation test.

### 6. Exact statistic to report

Report the **regime transportability envelope (RTE)** for each estimand:

`RTE(Gamma) = max_{r,r' in R} | beta_r - beta_r' |`,

with confidence limits obtained from the joint refit across regimes and the
three escalation stresses. Report the cold-day contrast explicitly as

`Delta_cold = beta_cold,pre - beta_cold,pandemic`.

Regime invariance **passes** only if the 95% RTE upper limit is below the
pre-specified transport tolerance `epsilon_transport` and empirical
coverage remains at least the pre-specified level under all stress families.
It **fails** if the envelope exceeds that tolerance or coverage collapses.
Failure blocks policy extrapolation; it does not prove a biological regime
change.

## HE-09 — public share versus territory total

### 1. Fatal identification objection

The extract contains public-sector first hospitalisations. It does not
observe private admissions, switching, waiting times, or household prices.
Therefore

`d log(Y_public)/dT = d log(Y_total)/dT + d log(sigma)/dT`

cannot be decomposed. A public count ratio is not a territory-wide
utilisation or fiscal-incidence ratio.

### 2. Observational equivalence

The same public association can be generated by total morbidity, routing from
private to public care, routing from public to private care, changes in
urgency, or a selected public-follow-up cohort. The public share can move
even when total admissions do not.

### 3. Why the proposed kill-test is insufficient

If a private series exists and the public-plus-private pattern matches, that
would be reassuring only if coding, coverage, timing, and cohort definitions
are comparable. If no series exists, the absence of evidence cannot set
`d log(sigma)/dT` to zero. A synthetic dual-sector Monte Carlo with known
share dynamics is not evidence about Hong Kong's unobserved private sector.

### 4. Escalation stress

- Make public or private months MNAR when public counts, temperature
  extremes, or waiting times are high; test differential missingness.
- Add an unobserved macro shock that changes both total need and the public
  share while correlating with temperature.
- Impose absorbing first events and a heat-dependent public/private
  threshold, including severe substitution and queue rationing.

### 5. Verdict: `KILL`

Kill any territory-wide or total-utilisation interpretation. The surviving
descriptive object is public first-hospitalisation utilisation in this
cohort; the public-share decomposition is not identified without verified,
comparable private volumes.

## HE-10 — monthly exposure as a unit-value index

### 1. Fatal identification objection

A monthly mean does not identify the nonlinear daily response. If the daily
response is `g(T_d)`, then monthly aggregation depends on both the mean and
within-month distribution:

`sum_d g(T_d) ~= n * [g(Tbar) + 0.5*g''(Tbar)*s2]`.

The curvature, variance gradient, lag structure, and tail process are not
identified by the monthly outcome. For extreme-count exposures, the
mean-temperature Taylor argument is not even the right object.

### 2. Observational equivalence

The same monthly coefficient can arise from a linear daily response, a
reversed-J response, different within-month variance, threshold counts,
serial dependence, or daily capacity censoring. A scenario projection can
therefore change while fitting the historical monthly coefficient equally
well.

### 3. Why the proposed kill-test is insufficient

A Monte Carlo with a selected known `g` can show small distortion relative to
the existing interval while missing the true curvature class, tail response,
macro shock, or threshold censoring. Passing for smooth mean exposures does
not kill the issue for hot nights or cold days. The test is conditional
illustration, not recovery of `g`—and it must not be relabelled as the failed
M|D daily-recovery problem.

### 4. Escalation stress

- Make missingness depend on daily extremes, monthly `Y_t`, and within-month
  variance; MNAR deletion must target the months where Jensen bias is largest.
- Add an unobserved macro shock correlated with both daily exposure
  distributions and monthly admissions, including nonlinear interactions.
- Apply daily capacity top-truncation, absorbing first events, and a
  heat-dependent threshold before aggregation. Test the composition of
  truncation bias and aggregation bias.

### 5. Verdict: `SURVIVE-TO-ESCALATION`

This is a legitimate, self-contained projection-validity stress, but it
cannot identify a daily health response and cannot produce a monetised
quantity. It earns survival only as a conditional sensitivity analysis.

### 6. Exact statistic to report

Report the **aggregation distortion ratio (ADR)** for each imposed daily
response and exposure family:

`ADR(g) = | beta_month(g) - beta_target(g) | /
          (0.5 * CI_width_existing)`.

Here `beta_month(g)` is the coefficient from the exact monthly analysis of
aggregated synthetic counts, and `beta_target(g)` is the known coefficient
for the pre-specified scenario estimand under the same real HKO exposure
path. Report the median and 95th percentile of `ADR(g)` over the full
stress ensemble, separately for means and extreme counts.

Aggregation is **cosmetic** only if the 95th-percentile ADR is below one
and coverage remains at least the pre-specified level under every stress
family. It **fails** the projection-validity gate if ADR reaches one or
coverage fails. Failure blocks monthly-coefficient scenario extrapolation;
it does not recover a daily coefficient.

## HE-11 — household AC and adaptation capital

### 1. Fatal identification objection

There is no household, district, housing, appliance, tariff, or income
dimension in the outcome file. Outdoor temperature is not effective indoor
exposure, but the transformation cannot be estimated. Territory-wide tariff
changes are collinear with time, while adaptation saturation and depletion
both look like a changing trend.

### 2. Observational equivalence

A small hot-night coefficient can mean strong adaptation, weak biology,
public routing, depletion, measurement error, or a changing threshold.
Territory-level data cannot distinguish these.

### 3. Why the proposed kill-test is insufficient

There is no valid single-territory base test. A synthetic household model
will recover the supplied capital distribution by construction. A trend
interaction cannot identify household adaptation because the required
cross-section is absent.

### 4. Escalation stress

- Make missingness depend on heat, household adaptation, and observed
  admissions, including missing extremes.
- Add an unobserved macro/energy shock correlated with outdoor temperature
  and admissions; a tariff dummy is not enough.
- Combine household-specific thresholds with absorbing first events and
  heat-dependent selection into public hospitalisation.

### 5. Verdict: `PARK-CONFIRMED`

Park until district- or cluster-level counts can be governed and joined to
housing type, appliance ownership, and energy-use measures. Do not infer
adaptation from the territory trend.

## HE-12 — holiday exclusion and caregiver time price

### 1. Fatal identification objection

Calendar composition is not guaranteed to affect conversion only. Rest days
and holidays can change activity, diet, exposure, clinic schedules, family
observation, and biological need. Lunar New Year is seasonally entangled with
the coldest months. The four-versus-five weekday variation is small, and
month fixed effects absorb much of the relevant calendar structure. This is
not a credible exclusion restriction merely because the calendar is
pre-determined.

### 2. Observational equivalence

A holiday coefficient can represent caregiver availability, altered
health-seeking, altered exposure, altered need, clinic closure, reporting
delay, or coding. An unchanged thermal coefficient can mean no conversion
channel, a weak first stage, offsetting violations, or an overfit control.

### 3. Why the proposed kill-test is insufficient

Adding rest-day and non-Lunar-New-Year holiday counts and seeing the two
thermal ratios unchanged to three decimals is not an IV test. It does not
establish relevance, exclusion, monotonicity, or adequate power. A
Monte Carlo with an exogenous calendar instrument can pass while the real
calendar changes both need and conversion.

### 4. Escalation stress

- Make missingness depend on holiday periods, high counts, and extreme
  exposures; include MNAR reporting delays.
- Add an unobserved macro/access shock correlated with both temperature and
  holiday composition, rather than treating the calendar as independent.
- Impose a heat-dependent threshold and absorbing first-event state so that
  calendar composition changes selection as well as conversion.

### 5. Verdict: `KILL`

HE-12 does not provide the exclusion needed for HE-02. It may be included
as a transparent calendar sensitivity, but it cannot identify a caregiver
time price or a need elasticity.

## Ranked kill sequence

Run the shortest destructive checks first:

1. **Park immediately:** HE-06 and HE-11 have no current identification
   design. Write the exact data request and stop.
2. **Reject unsupported interpretations:** HE-03, HE-04, HE-09, and HE-12
   fail from missing supply, utility, private-sector, or exclusion
   information. No elaborate simulation rescues them.
3. **Run only if the parent wants a documented dead end:** HE-01, HE-02,
   and HE-05. Their central latent objects are unobserved or structurally
   removed by first-event measurement.
4. **Escalate the three conditional survivors:** HE-07, HE-08, and HE-10.
   These are not findings. They are the only candidates for which a
   pre-specified envelope or public-data simulation can materially narrow a
   live objection.

The parent should stop a line once its fatal object is shown to be absent.
More simulation is not evidence when the parameter is not defined by the
observed data.

## Anti-convergence notes

These hypotheses must not be allowed to disguise old models as new economics:

- **HE-01 → P10/P16 plus a trend story.** Adding a depletion-shaped trend to
  the existing spline is not stock-flow identification. If the output is
  only “the coefficient survives seasonality/COVID sensitivity,” the
  hypothesis collapsed back into P10/P16. It also routes directly into the
  rejected simple cost-of-illness model.
- **HE-02 → P10/P16 or simple COI.** A pandemic control, holiday control, or
  unchanged count ratio does not separate need and conversion. Multiplying
  the ratio by events and a unit cost is the exact prohibited shortcut.
- **HE-03 → no existing P pathway.** A monthly censoring simulation is a
  capacity caveat, not a new demand pathway. If it reports only attenuation
  of a P01–P18 coefficient, it has not identified a bed shadow price.
- **HE-04 → governance memo, not a model.** A decision tree with arbitrary
  priors is not a posterior result. Do not relabel missing-data triage as
  VoI evidence.
- **HE-05 → P03 lag sensitivity.** A lag-1 coefficient or a sum of lag
  coefficients is not `phi` without a repeat-event counterfactual. It must
  not become a cost-of-illness correction factor.
- **HE-06 → P10 month fixed effects.** A fiscal-cycle narrative absorbed by
  month dummies is not an estimated present-bias parameter.
- **HE-07 → P09/P17 selection language.** Age or sex stratification can show
  heterogeneity, not the total welfare loss below the admission threshold.
  An outpatient comparison is a distinct auxiliary outcome, not another
  pathway headline.
- **HE-08 → P10/P16 influence exclusion.** A pre-COVID split or deletion of
  2020-02/2022-02 is not a regime-invariance test unless it reports the
  cross-regime envelope and its power/coverage.
- **HE-09 → simple COI on public counts.** A public unit cost attached to a
  public-only selected share is not territory-wide burden.
- **HE-10 → failed M|D if mishandled.** It must never estimate or claim a
  daily coefficient. If the simulation is described as “recovering daily
  effects,” it has collapsed into the already failed M|D paradigm.
- **HE-11 → P09/P17 or trend adaptation.** Person-stratum heterogeneity is
  not household capital, and a secular hot-night trend is not AC ownership.
- **HE-12 → P10 holiday sensitivity.** A holiday covariate is not an
  exclusion restriction. If the output is only a robust count ratio, HE-12
  has collapsed into P10.

## Cycle 2 mutation attacks

Any Cycle 1 survivor must be attacked again under both dynamic
time-inconsistency and Hospital Authority rationing or cartel power. A static
survivor is not a structural parameter until it survives these mutations.

### Dynamic time-inconsistency

- **HE-01:** The remaining stock has a rising scarcity value as it is
  depleted. A present-biased planner may underinvest in prevention, but the
  scarcity rent is not identified without stock, inflow, and intervention
  data. Stress-test whether a dynamic planner can generate the same monthly
  path as depletion plus a time spline.
- **HE-04:** Replace exponential discounting with `(beta, delta)` preferences.
  The question becomes whether a written Gate 3 rule or pre-registered
  addendum is a commitment device. The commitment value depends on human
  preferences and cannot be inferred from counts.
- **HE-05:** Dynamic discounting changes the welfare value of timing, while
  first-event measurement still hides the displaced event. A lag pattern
  cannot identify harvesting merely because discounting is non-constant.
- **HE-07:** The threshold `s*_t` becomes endogenous to household and system
  adaptation. An intervention can change visibility and thereby change the
  estimated outcome without changing latent morbidity.
- **HE-08:** A time-inconsistent system may change access rules at predictable
  budget or pandemic horizons. Test continuous regime drift, not only
  pre/post dummies.
- **HE-10:** Warming changes the distribution of daily extremes, while a
  present-biased planner changes capacity or adaptation investment. The
  monthly aggregation distortion is then policy-dependent.

### HA rationing, cartel, or monopsony power

- **HE-02:** Under queue clearing, `pi_t` is not a household conversion
  probability. It is an allocation rule set by a capacity-constrained public
  provider. The observed coefficient may be an elasticity of rationing.
- **HE-03:** A single public provider can exercise institutional market power
  over acute capacity and clinical labour. Bed shadow price, waiting time,
  elective displacement, and admission threshold must be modelled jointly;
  no monthly count alone identifies them.
- **HE-07:** Rationing makes `s*_t` an HA policy variable. A stable admission
  ratio can conceal a changing welfare loss if the threshold moves to clear a
  queue.
- **HE-09:** Private hospitals become a price-rationed safety valve. Public
  counts can fall when total need rises if substitution increases. HE-09 and
  HE-03 are then not independent hypotheses.
- **HE-10:** Daily top-truncation composes with Jensen aggregation. The sign of
  the total monthly distortion is not guaranteed. This is the strongest
  Cycle 2 simulation target, but it remains conditional on a synthetic daily
  response and must not be presented as a recovered daily effect.
- **HE-12:** Calendar composition may alter queue arrival and queue clearing,
  not only caregiver time. Its exclusion restriction becomes even less
  credible under rationing.

The preferred Cycle 2 data request, if a human governance decision opens one,
is a single cluster-level portfolio: monthly outcomes, capacity/occupancy,
elective displacement, and adaptation/budget history. Requesting isolated
variables for each hypothesis would leave the same supply-side
observational-equivalence problem in place.

## Final disposition

Cycle 1 does not produce an economic estimate. It kills eight proposed
claims as currently identified, confirms two as parked, and leaves three
conditional sensitivity objects for escalation. None of these dispositions
changes the CHD/HF analysis of record, promotes a pathway, closes Gate 3,
creates a stroke result, or authorises monetisation.
