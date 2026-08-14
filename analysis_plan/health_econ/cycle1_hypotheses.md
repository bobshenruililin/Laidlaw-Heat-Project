# Health-economics hypothesis portfolio — Cycle 1

**Mode:** Explore. **Date:** 14 August 2026. **Provenance of every hypothesis:** `SYNTHETIC_THEORY`.

This document opens a health-economics layer that the repository does not currently
have. It contains **no findings**. It contains candidate economic objects, structural
sketches, and decisive tests. Nothing here is a Gate 3 input, a manuscript claim, or a
licence to attach a dollar figure to an existing coefficient.

## Scope contract

Reproduced from the record so that every hypothesis below is disciplined by it:

- Estimand of record: **ecological monthly count ratios** for first hospitalisation
  after first CHD or HF diagnosis in a T2D/HTN cohort, Hong Kong, 132 territory-months,
  January 2013 – December 2023. Admission cause is **absent**.
- Analysis of record: separate negative-binomial exposures, calendar-month indicators,
  `ns(time, 4)`, days-in-month offset, Model/HC1/NW3/NW6 uncertainty ladder.
- All twelve core BH q-values exceed **0.19**. HF cold days per 5: **1.073 (1.006–1.144)**,
  q = 0.192, SE-concordant. CHD hot nights per 5: **1.022 (1.002–1.042)**, SE-sensitive
  (Model and HC1 include 1). **Gate 3 is open**; lead recommendation is Option A, no
  confirmatory primary.
- First-event totals halve: CHD **23,830 → 12,323**, HF **4,336 → 2,296** (2013 → 2023),
  while the C&SD 35+ denominator rises. The offset is **not** T2D/HTN person-time.
- Influence leaders are **2020-02** and **2022-02**. Cold-day support is concentrated in
  DJF (**141 of 145** cold days).
- Daily monthly-to-daily (M|D) recovery **failed** 500-replicate calibration. No real
  daily coefficient exists. Stroke was named but **not delivered**; no stroke coefficient
  exists.

Every numeric value introduced *by this document* that is not in the list above is
labelled `SYNTHETIC` or `theoretical` and exists only to make a structure legible.

## What this document is not

It is not a costing. It is not a burden estimate. It does not multiply any ratio above by
any unit cost. The single most likely failure mode of a health-economics layer bolted onto
this project is exactly that multiplication, and it is catalogued below as a rejected
paradigm, not a survivor.

---

## HE-01 Depletion as an exhaustible stock, not a renewable flow

- **paradigm_id:** HE-01
- **theoretical_space:** Stock-flow / finite risk pool
- **claim_type:** costing (with an identification rider)
- **economic_object:** The expected discounted remaining admission liability of the
  still-unhospitalised diagnosed pool — a stock valuation, not a per-period flow.
- **structural_sketch:** Let `S_t` be the number of diagnosed T2D/HTN individuals who have
  a CHD or HF diagnosis but have not yet had their first hospitalisation, with `S_0` the
  January 2013 stock. Monthly events are `E[Y_t] = S_t · h(T_t) · d_t`, where `h` is the
  per-person-month hazard, `T_t` the thermal exposure, and `d_t` days in month. The stock
  evolves as `S_{t+1} = S_t − Y_t + I_t`, where `I_t` is inflow from newly diagnosed
  members. Define the replacement ratio `ρ = I_t / Y_t`; the observed halving of both
  series against a rising 35+ population is what `ρ < 1` looks like inside a closed
  2013–2023 diagnosis window. The fitted `ns(time, 4)` is a smooth proxy for `log S_t`, so
  the estimated thermal parameter `θ` is a modulation of `h` conditional on that proxy. The
  economic object is then `L_t = Σ_k δ^k · c · E[Y_{t+k} | S_t]`, a liability that is
  bounded above by `c · S_t` regardless of `θ`. Any projection that applies `θ` to a
  counterfactual future event count implicitly sets `ρ = 1` and prices a flow the stock
  cannot sustain.
- **why_not_already_explored:** P01–P18 treat depletion as a nuisance to be absorbed by
  the trend spline; no pathway asks what the depleting stock does to the *valuation*
  object, and the cost-of-illness trap assumes a renewable flow by construction.
- **identification_threats:**
  - `ns(time, 4)` and the true `log S_t` path are not the same function; residual
    curvature in the stock leaks into any exposure whose own trend is secular (hot nights
    rose from 10 to 56 over the window).
  - `S_t` is unobserved and `ρ` is unidentified without the T2D/HTN person-time denominator
    that Roro has not supplied.
  - Left truncation at 2013 means `S_0` mixes incident and long-prevalent members with
    very different hazards; the mixture drifts mechanically over the window.
- **what_would_kill_it:** Monte Carlo on the real HKO exposure series with a synthetic
  stock path. Generate counts under `θ = 0` with depletion whose curvature is deliberately
  adversarial to `ns(time, 4)`, fit the analysis of record, and measure the empirical size
  of the test on `θ`. If size stays at nominal across plausible depletion shapes, the
  stock-flow objection is bookkeeping only: `θ` survives as an identified hazard modulation
  and HE-01 collapses to a costing caveat rather than an identification problem. That is
  still a publishable caveat, but it is a much smaller claim.
- **data_required:** *HAS* — monthly first-event counts, real daily and monthly HKO
  exposure, C&SD 35+ population. *LACKS* — monthly still-at-risk person-time, cohort entry
  dates, `I_t`, any per-case cost.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-02 Two-equation utilisation: need and conversion are separately unidentified

- **paradigm_id:** HE-02
- **theoretical_space:** Two-equation utilisation
- **claim_type:** identification (with a welfare corollary)
- **economic_object:** The elasticity of *realised utilisation* with respect to
  temperature, which is the sum of a pathophysiological elasticity and a care-seeking
  conversion elasticity and is therefore not a welfare parameter.
- **structural_sketch:** Let latent biological need be `N_t = N_0 · exp(α_T · T_t + α_X X_t)`
  and let the probability that a person with need converts it into a recorded first
  hospitalisation be `π_t = Λ(γ_0 + γ_T T_t + γ_A A_t)`, where `A_t` indexes access:
  ambulance availability, A&E queue, pandemic advisories, household caregiver presence.
  Observed counts satisfy `E[Y_t] = N_t · π_t`, so `log E[Y_t] = log N_t + log π_t` and the
  regression recovers only `α_T + γ_T`. Expenditure is `c · Y_t` and rises with either
  channel. Welfare does not: if `α_T = 0` and `γ_T > 0`, heat converts previously unmet
  need into met need, spending rises, and consumer surplus rises. The sign of `dW/dT` is
  therefore not identified by the count ratio even when the count ratio is estimated
  perfectly. A hospital cost is an accounting object attached to `π`, and only the `α`
  channel carries a health loss.
- **why_not_already_explored:** P10 and P16 treat care-seeking as a *nuisance* to be
  controlled or excluded by period; no pathway treats it as a second structural equation
  whose parameter is the thing an economist would actually want, and the cost-of-illness
  trap silently assumes `γ_T = 0`.
- **identification_threats:**
  - No instrument in the current data moves `π` without moving `N`; temperature enters both
    equations by hypothesis.
  - Monthly aggregation destroys the sharpest conversion variation, which is
    day-of-week and hour-of-day.
  - `A_t` is partly the pandemic regime, which is itself the influence-month problem
    (2020-02, 2022-02) and therefore not an exogenous shifter.
- **what_would_kill_it:** Find or fail to find one exclusion restriction that shifts `π`
  and is orthogonal to `T`. The cheapest live candidate is HE-12's calendar composition
  (rest-day and public-holiday counts, which vary 4-versus-5 across months and are
  uncorrelated with temperature). If a conversion shifter is added and both the point
  estimate and the interval on `θ` are unchanged, then `γ_T ≈ 0` empirically and the
  count ratio may be read as a need elasticity. If no admissible shifter exists, HE-02 is a
  permanent limitation and must be written as one rather than solved.
- **data_required:** *HAS* — monthly counts, calendar structure, COVID phase indicators,
  flu and pollution series. *LACKS* — A&E attendance, ambulance call volume, waiting
  times, any documented and dated access or fee shock.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-03 The shadow price of a bed, and why 132 months cannot see it

- **paradigm_id:** HE-03
- **theoretical_space:** Hospital Authority as capacity-constrained supply
- **claim_type:** identification
- **economic_object:** The Lagrange multiplier `λ_t` on the bed-day capacity constraint —
  the shadow price of admitting one more patient, paid in cancelled electives rather than
  in money.
- **structural_sketch:** The Hospital Authority is a single public provider with capacity
  `K_t` bed-days per month and an elective buffer `E_t` that can be cancelled. Latent
  demand `D_t` is realised as `Y_t = D_t` when `D_t + Ē_t ≤ K_t` and as a rationed quantity
  otherwise, with electives displaced first. The economically interesting quantity is
  `λ_t = ∂W/∂K_t`, which is strictly positive only when the constraint binds. Under
  rationing, the estimated thermal coefficient `θ̂` is attenuated toward zero *precisely in
  the periods where the true effect is largest*, so `θ̂` is a censored-demand elasticity and
  a lower bound on `θ`. The critical structural fact is the time scale: capacity binds on
  *days*, and a month in which three days exceed capacity can still show mean occupancy
  below `K`. Aggregating a daily min-operator to a monthly sum therefore washes out most of
  the censoring, so `λ_t` is not recoverable at the resolution we have.
- **why_not_already_explored:** No pathway models supply at all; P01–P18 are demand-side
  exposure–response specifications, and the cost-of-illness trap treats hospital capacity
  as infinitely elastic at a constant unit price.
- **identification_threats:**
  - Monthly aggregation of a daily censoring operator; the bias is second-order at our
    resolution and is confounded with negative-binomial overdispersion.
  - `K_t` is not observed; HA capacity is a policy variable that itself responds to
    anticipated seasonal demand, making it endogenous to `T`.
  - Elective displacement is the true margin and is entirely outside our outcome
    definition, which is first hospitalisation after first CHD/HF diagnosis.
- **what_would_kill_it:** A Monte Carlo with daily capacity censoring aggregated to
  months. Simulate daily admissions from a synthetic dose-response, apply
  `min(D_d, K)` at plausible utilisation levels, aggregate, and fit the analysis of record.
  If the relative attenuation of the monthly `θ̂` is below, say, 2 percent (`SYNTHETIC`
  threshold, to be set before running) across the plausible range of `K`, then the shadow
  price cannot be spoken about from this dataset and HE-03 is discussion-section material
  only.
- **data_required:** *HAS* — monthly counts and real exposure for the simulation harness.
  *LACKS* — bed-day capacity, occupancy, elective cancellation counts, cluster-level
  breakdown, length of stay.
- **status_proposal:** likely_fail
- **provenance:** SYNTHETIC_THEORY

---

## HE-04 Value of information when the posterior does not move but the claim set does

- **paradigm_id:** HE-04
- **theoretical_space:** Value of information
- **claim_type:** VoI
- **economic_object:** The expected value of the missing stroke file and the missing
  person-time denominator, measured in units of the decisions they would change — and the
  finding that for one of them the value is almost entirely in the *admissible claim set*
  rather than in the posterior.
- **structural_sketch:** Let the decision be `d ∈ {A, B}`: submit the exploratory CHD/HF
  paper now under Option A, or wait. Let `δ_S` be the unknown stroke thermal effect with
  prior `p(δ_S)`, and let `U(d, δ_S)` include claim strength, scoop hazard `κ`, and
  timeline depreciation `ν` from the Laidlaw calendar. Then
  `EVPI = E_δ[max_d U] − max_d E_δ[U]`. Two structural features of *this* project drive the
  answer. First, the lead recommendation is already Option A with **no confirmatory
  primary**, so information that would only change *which* contrast is designated primary
  has zero value under a decision rule that designates none: `EVPI ≈ 0` for that use.
  Second, the offset sensitivity already in the record shows that switching from days-only
  to population-by-days moves CHD hot nights across 1.022 / 1.021 / 1.022 and HF cold days
  across 1.073 / 1.073 / 1.075. The person-time denominator therefore has near-zero
  posterior value and substantial *constraint-set* value: it is what converts "ecological
  monthly count ratio" into "incidence rate ratio". That is information whose entire worth
  lies in the sentence it licenses, which is a real and unusual VoI object.
- **why_not_already_explored:** The repository frames the missing files as governance
  blockers, never as priced options; no existing document asks what decision the stroke
  file would change, which is the only question that gives information value.
- **identification_threats:**
  - The prior on `δ_S` is elicited, not estimated; every number in the decision tree will
    be `SYNTHETIC` and the ranking may be prior-driven.
  - Utility over "claim strength" is not commensurable with utility over timeline in any
    non-arbitrary way.
  - The decision-maker is not a single agent: PI, co-authors, and scholar have different
    loss functions, so `max_d` is a bargaining outcome, not an optimisation.
- **what_would_kill_it:** Build the decision tree explicitly with elicited `SYNTHETIC`
  priors and compute EVPI under the full plausible range of `δ_S`. If EVPI for the stroke
  file is below the cost of delay under *every* prior in that range, then waiting is a
  revealed preference rather than an optimal policy, and HE-04 resolves into a one-line
  recommendation instead of a research strand. Symmetrically, if person-time EVPI is
  non-trivial once the claim label is priced, the ask to Roro should be re-ranked above the
  stroke ask.
- **data_required:** *HAS* — the full offset-sensitivity table, the Gate 3 packet, the
  decision structure. *LACKS* — an elicited prior on stroke effects, an agreed loss
  function, any external deadline structure written down.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-05 Economic harvesting: shifted hospital spending versus new hospital spending

- **paradigm_id:** HE-05
- **theoretical_space:** Intertemporal cost shifting
- **claim_type:** welfare
- **economic_object:** The displacement fraction `φ` — the share of heat- or
  cold-attributed admissions that were merely brought forward from a later month, whose
  welfare cost is only the discount differential plus any severity or unit-cost difference,
  not the full episode cost.
- **structural_sketch:** Write the monthly response as a finite distributed lag,
  `log E[Y_t] = base_t + β_0 X_t + β_1 X_{t−1} + β_2 X_{t−2}`, where `X` is the thermal
  exposure. Pure displacement implies a positive `β_0` offset by negative subsequent
  coefficients with `Σ_k β_k = (1 − φ) β_0`; pure new burden implies `Σ_k β_k = β_0`. The
  economic content is that a cost-of-illness figure computed from `β_0` alone overstates
  the true resource cost by a factor of roughly `1 / (1 − φ)` when `φ > 0`. This is *not*
  mortality displacement: nobody has to die for a hospital day to move in time, and the
  welfare arithmetic is different because a shifted admission is still consumed, just
  earlier. The record complicates the story usefully: HF cold days at lag 1 is
  **1.073 (1.014–1.135)**, positive rather than negative, which is the opposite of a
  displacement signature — but persistence `ψ`, seasonal clustering `ω`, and delayed
  decompensation are observationally equivalent to it at monthly resolution.
- **why_not_already_explored:** P03 and the lag sensitivities treat lag-1 as a robustness
  check on a single coefficient; no existing analysis imposes the summability restriction
  that turns a lag panel into a statement about `φ`, and the mortality-displacement
  literature the project already cites is about deaths, not resource timing.
- **identification_threats:**
  - Calendar-month indicators plus `ns(time, 4)` on 132 observations leave thin residual
    variation for a multi-month lag structure; `φ` and `ψ` are close to collinear.
  - Cold exposure is concentrated in DJF (141 of 145 cold days), so the "next month" of a
    January cold shock is February, which is also cold — displacement and persistence share
    the same months.
  - The outcome is a *first* event, which mechanically forbids the within-person
    repeat-admission pattern that displacement models usually exploit.
- **what_would_kill_it:** Monte Carlo using the real HKO monthly exposure series. Simulate
  counts with known `φ ∈ {0, 0.3, 0.6}` (`SYNTHETIC`), fit the analysis of record with lags
  0–2, and compare the sampling distributions of `Σ_k β̂_k`. If power to reject `φ = 0`
  when the truth is `φ = 0.5` is below 0.5 at `n = 132`, then `φ` is not identified here
  and HE-05 must be reported as an unresolvable bound on any cost claim rather than as an
  estimate. That bound is still worth having, because it is the honest interval a referee
  should demand around any monetisation.
- **data_required:** *HAS* — monthly counts, real exposure, existing lag-sensitivity table.
  *LACKS* — length of stay, readmission linkage, per-episode cost, daily resolution.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-06 Present-biased budgeting and the fiscal cycle hidden inside the month dummies

- **paradigm_id:** HE-06
- **theoretical_space:** Time-inconsistent public budgeting
- **claim_type:** mechanism (normative, with an empirical rider)
- **economic_object:** The adaptation-capital wedge `Δ = A* − A^β` between the social
  planner's optimal climate-adaptation stock and the stock chosen by a present-biased
  manager on an annual budget cycle.
- **structural_sketch:** Model the Hospital Authority planner with quasi-hyperbolic
  preferences `(β, δ)`, choosing between recurrent spending, which pays off within the
  budget year, and adaptation capital `A` — ward cooling, cold-weather outreach, surge
  staffing — which depreciates at `d_A` and pays off over decades. The planner's first-order
  condition under-weights all future periods uniformly by `β < 1`, so the wedge `Δ` is
  increasing in the payoff horizon of `A` and is largest exactly for climate adaptation.
  Our count ratios enter this problem only as one input parameter to the marginal
  productivity of `A`, which is the correct and modest role for them. There is also an
  empirical rider that matters for our own specification: the Hong Kong government
  financial year runs April to March (verify the Authority's own reporting year before
  use), so any end-of-fiscal-year variation in admission thresholds or discretionary
  activity is a *within-year* pattern that is perfectly collinear with the twelve calendar
  month indicators. Our month dummies therefore absorb climatic seasonality and fiscal
  seasonality jointly, and no re-specification on a single territory can separate them.
- **why_not_already_explored:** The repository has no supply-side or budget-side model at
  all; P10's seasonality controls are statistical nuisance terms, and nobody has noted that
  they are also absorbing an institutional budget cycle.
- **identification_threats:**
  - `β` is a preference parameter of an institution, not a quantity estimable from
    admission counts.
  - Fiscal-year seasonality is exactly collinear with calendar-month indicators in a
    single-territory series; the two are not separable in principle here.
  - Adaptation capital may have been installed continuously over 2013–2023, making the
    "wedge" a moving target that `ns(time, 4)` partly absorbs.
- **what_would_kill_it:** Demand a design before doing any work. The only credible source
  of variation is cross-sectional: the Authority's hospital clusters differ in capital
  vintage and budget history. If cluster-level monthly counts and cluster capital spending
  cannot be obtained under governance, there is no test, and HE-06 must be parked as a
  discussion frame rather than pursued. Parking it explicitly is the deliverable.
- **data_required:** *HAS* — nothing directly; the count ratios are at best one input
  parameter. *LACKS* — cluster-level counts, cluster capital and recurrent budgets,
  adaptation-project inventory, any budget-cycle documentation.
- **status_proposal:** park
- **provenance:** SYNTHETIC_THEORY

---

## HE-07 The visible fraction: hospitalisation is a selected tail of the welfare loss

- **paradigm_id:** HE-07
- **theoretical_space:** Selection into observed hospitalisation
- **claim_type:** welfare
- **economic_object:** The visibility fraction `ω(T)` — the share of total heat- and
  cold-attributable welfare loss that ever becomes a recorded first hospitalisation — and
  whether it is constant in temperature.
- **structural_sketch:** Let each cohort member draw a severity `s` from a distribution
  `F(s | T)` that shifts with temperature, and let hospitalisation occur when `s > s*`.
  Then observed counts are proportional to `ω(T) = 1 − F(s* | T)`, and the estimated
  elasticity satisfies `ε_Y = ε_M + d log ω / d log T`, where `ε_M` is the elasticity of
  total morbidity. Everything below `s*` — degraded sleep, elevated resting blood pressure,
  outpatient visits, medication changes, informal care hours, lost work capacity — carries
  real welfare cost and is structurally invisible to our outcome. If `s*` were fixed, `ε_Y`
  would be a clean lower bound on `ε_M` and the paper's burden would be a conservative
  floor. But `s*` is itself the output of the conversion problem in HE-02 and the capacity
  problem in HE-03, so it moves with heat, access, and crowding, and even the lower-bound
  interpretation is not free. The economic reading of the paper's estimand is therefore:
  it prices the tip of the iceberg, in the one currency the Authority happens to record.
- **why_not_already_explored:** The live Introduction already gestures at sleep and blood
  pressure as *unmeasured motivation*; no document treats the unmeasured layer as a
  quantity with a name, a parameter, and a testable invariance condition.
- **identification_threats:**
  - `s*` is unobserved and is plausibly heat-dependent in the same direction as `s`, which
    biases `ε_Y` toward `ε_M` in an unknown amount.
  - The first-event restriction truncates the severity distribution again, in a way that
    interacts with the depleting stock in HE-01.
  - Any outpatient comparison series will have a different catchment and coding regime, so
    a null difference in elasticities is weak evidence of invariance.
- **what_would_kill_it:** Obtain one non-hospital morbidity series on the same 2013–2023
  monthly window — general outpatient clinic attendance for the cohort, or a sentinel
  outpatient series — and estimate the same thermal contrasts on it. If the outpatient
  elasticity is statistically indistinguishable from the admission elasticity, `ω` is
  approximately heat-invariant, the lower-bound reading is defensible, and HE-07 shrinks to
  a scale factor. If the two diverge sharply, the admission-based burden is not a bound in
  any direction and no monetisation of it is defensible.
- **data_required:** *HAS* — the admission series; the institutional fact that first
  outpatient mention was used as a diagnosis-timing marker, which means the outpatient
  layer exists in the source system. *LACKS* — outpatient attendance counts as an outcome,
  sick-leave or labour data, any sleep or blood-pressure series.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-08 The weather-to-spending map is not policy-invariant

- **paradigm_id:** HE-08
- **theoretical_space:** Macro health-system shocks
- **claim_type:** identification
- **economic_object:** The regime-invariance of the mapping from temperature to hospital
  expenditure — that is, whether `θ` is a structural parameter usable for pricing a future
  winter, or a regime-weighted average with weights set by pandemic policy.
- **structural_sketch:** Let utilisation be `u(T; R_t)` where `R_t` indexes the
  care-seeking regime. The pooled estimate is `θ̄ = Σ_R w_R θ_R` with weights `w_R` given by
  each regime's share of identifying variation, which the analyst does not choose. Two
  facts in the record make this concrete rather than abstract. The influence leaders are
  **2020-02** and **2022-02** — both Februaries — and cold-day identification lives almost
  entirely in DJF (**141 of 145**). So the pandemic demand destruction is concentrated in
  the very months that carry the cold-day coefficient. Furthermore, COVID policy affects
  both the seasonal timing of exposure windows and the propensity to attend hospital, so
  conditioning analysis on realised counts has a collider-like flavour rather than a simple
  confounding one. The economic consequence is a Lucas-critique reading: an elasticity
  averaged across a regime that no longer exists cannot price a future winter under a
  different utilisation regime, no matter how tight its interval.
- **why_not_already_explored:** P10 and P16 handle COVID as a control or an exclusion
  window; neither asks whether the *parameter itself* is regime-specific, which is the
  economic rather than epidemiological framing, and the influence-exclusion check that
  exists establishes robustness of *direction*, not invariance of *magnitude*.
- **identification_threats:**
  - Only three pandemic winters exist; a regime interaction on cold days is estimated off
    roughly three Februaries.
  - Regime and secular time are entangled, so `ns(time, 4)` and `R_t` compete for the same
    variation.
  - "Regime" is not binary; advisories, waves, and public confidence changed continuously
    while the coding of regimes will be coarse.
- **what_would_kill_it:** A formal regime-invariance test rather than an influence
  exclusion. The record already contains the ingredients for the comparison — the pre-2020
  HF cold-day estimate is 1.113 (1.053–1.176) against a pooled 1.073 (1.006–1.144) — and
  the point estimates differ in the direction demand destruction predicts while the
  intervals overlap heavily. The decisive version is a pre-specified test of equality with
  an honest power calculation attached. If power to detect an economically meaningful
  difference is negligible at three winters, HE-08 becomes a stated limitation on
  extrapolation, which is exactly what an economist reading this paper would want written
  down.
- **data_required:** *HAS* — full monthly series, COVID phase indicators, influence
  diagnostics, existing pre-2020 split. *LACKS* — an external utilisation series to
  calibrate the regime, and enough pandemic winters to estimate the interaction.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-09 Public counts are a share, not a total: the dual-sector substitution margin

- **paradigm_id:** HE-09
- **theoretical_space:** *Extra* — dual public/private system and fiscal incidence
- **claim_type:** identification
- **economic_object:** The public-sector share `σ_t` of total territory-wide
  hospitalisation, and the substitution elasticity that determines whether a thermal
  coefficient on public counts reflects morbidity or routing.
- **structural_sketch:** Hong Kong runs a dual system: a near-free public Authority sector
  and a substantial private hospital sector. Our outcome counts only the public arm, so
  `Y_t^public = σ_t · Y_t^total` and
  `d log Y^public / dT = d log Y^total / dT + d log σ_t / dT`. The share `σ_t` depends on
  relative waiting time `w_t`, urgency, and the effective time-and-money price faced by
  the household, with substitution elasticity `η`. Urgent presentations route
  overwhelmingly public; discretionary and deferrable ones are the margin where `η` bites.
  A thermal shock that raises urgency raises `σ_t` mechanically, so even a perfectly
  estimated public-sector `θ` is a composite of a morbidity elasticity and a routing
  elasticity. The fiscal-incidence reading is separate and also unexplored here: at a token
  point-of-service charge, the money cost falls on the public purse while the time,
  transport, and informal-care costs fall on households, so "hospital cost" and "burden on
  Hong Kong" are different objects with different distributional signs.
- **why_not_already_explored:** Every pathway treats the Authority extract as if it were
  the territory; no document in the repository distinguishes the public share from the
  total, and the cost-of-illness trap compounds the error by attaching a public unit cost
  to what is already a selected share.
- **identification_threats:**
  - `σ_t` is unobserved and its trend is entangled with the depletion trend in HE-01.
  - Private-sector data, if it exists at all, is likely annual and differently coded, so
    any share series will be interpolated.
  - The cohort is T2D/HTN patients under public follow-up, which may itself select on low
    private-sector propensity, making `η` small but non-zero and unmeasurable.
- **what_would_kill_it:** Establish whether monthly private inpatient discharge counts
  exist for 2013–2023 — this must be *verified*, not assumed; the repository record
  contains nothing on it. If they exist and the thermal pattern in public-plus-private
  totals matches the public-only pattern, substitution is not driving `θ` and HE-09
  collapses to a framing point. If they do not exist at monthly resolution, HE-09 becomes a
  bounded limitation: the paper measures public utilisation, and should say so in those
  words rather than in the language of territory-wide burden.
- **data_required:** *HAS* — public counts only. *LACKS* — private inpatient volumes,
  waiting-time series, any household out-of-pocket or informal-care measure.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-10 Monthly exposure as a unit-value index: signed aggregation bias in any projection

- **paradigm_id:** HE-10
- **theoretical_space:** *Extra* — aggregation bias as an index-number problem
- **claim_type:** costing
- **economic_object:** What the monthly coefficient *is* as an aggregator of a nonlinear
  daily dose-response, and the sign of the error it induces in scenario-based cost
  projections.
- **structural_sketch:** Suppose the true daily response is `g(T_d)`, nonlinear and
  plausibly reversed-J. A month's expected count is `Σ_d g(T_d) ≈ n·[g(T̄) + ½ g''(T̄)·s²]`,
  where `T̄` is the monthly mean and `s²` the within-month variance. Regressing monthly
  counts on `T̄` therefore estimates a mixture of the slope `g'` and a curvature term
  weighted by the *gradient of within-month variance*, `ς = ∂s²/∂T̄`. In a subtropical
  climate this gradient is not zero and not sign-ambiguous by accident: cold-season months
  carry surges and wide dispersion while hot-season months are more uniform, so `ς < 0` is
  the expected shape and the bias in the monthly slope is signed and computable. This is
  exactly the aggregation problem that index-number theory calls a unit-value bias: the
  "representative day" implied by a monthly mean does not exist, and its non-existence has
  a direction. The costing consequence is the point: a projection that applies a monthly
  `θ` to future monthly means will misprice, because warming changes both `T̄` and `s²`.
- **why_not_already_explored:** This is emphatically **not** the failed M|D recovery. M|D
  attempted to *estimate* daily coefficients from monthly sums and failed its 500-replicate
  calibration; HE-10 makes no attempt to recover `g` and instead characterises what the
  monthly coefficient already estimates and whether it may be used for extrapolation. The
  first is an estimation problem that is closed; the second is a validity-of-costing
  problem that has never been opened.
- **identification_threats:**
  - The true `g` is unknown; any bias calculation is conditional on an assumed curvature
    and is therefore illustrative rather than definitive.
  - Extreme-count exposures (hot nights, cold days) are already tail statistics, so the
    Taylor argument applies to them differently than to mean temperature and the two
    families need separate treatment.
  - Real within-month variance is itself trending over the window, so `ς` is not constant.
- **what_would_kill_it:** A pure Monte Carlo requiring no Hospital Authority data at all.
  Take the **real** daily HKO series, impose a `SYNTHETIC` daily response `g` with known
  curvature, generate daily counts, aggregate to months, fit the exact analysis of record,
  and compare `θ̂` to the truth implied by `g`. If the aggregation bias is small relative to
  the width of the existing confidence intervals across the plausible curvature range, then
  HE-10 is cosmetic and should be dropped in one line. If it is comparable to or larger
  than the interval width, then no monthly-coefficient-based projection may be published
  without this correction — which is a genuinely useful, cheap, and self-contained result.
- **data_required:** *HAS* — real daily HKO exposure, real monthly exposure, the exact
  fitted specification. *LACKS* — nothing; this is runnable today without any governed
  health data, which makes it the cheapest hypothesis in the portfolio.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-11 Adaptation capital in the household: air conditioning, housing, and tariffs

- **paradigm_id:** HE-11
- **theoretical_space:** *Extra* — household production of effective exposure
- **claim_type:** mechanism
- **economic_object:** The distribution of household adaptation capital that turns outdoor
  temperature into effective exposure, and the resulting fact that a territory coefficient
  is a capital-weighted average rather than a structural parameter.
- **structural_sketch:** Households produce effective exposure
  `T_eff = T_out − a(K_h, p_e)`, where `K_h` is air-conditioning and insulation capital and
  `p_e` the electricity tariff that governs its utilisation. The territory coefficient is
  `θ = Σ_h w_h · θ_h(K_h)` with weights `w_h` given by the housing-type distribution:
  public rental estates, private flats, and subdivided units differ enormously in `K_h` and
  in the ability to run it. Two consequences follow. First, `θ` is not transportable: it
  belongs to the 2013–2023 capital distribution, not to Hong Kong as such. Second,
  saturation of `K` over the window generates an endogenous downward drift in `θ_hot` that
  `ns(time, 4)` partly absorbs, so a small estimated hot-night effect is consistent with
  either a weak biological effect or a strong effect that adaptation has been offsetting.
  The record shows hot nights rising from 10 to 56 across the window while the CHD
  hot-night ratio sits at 1.022 with Model and HC1 intervals including 1 — a pattern that
  the territory-level data cannot decompose.
- **why_not_already_explored:** P09 and P17 stratify by person characteristics that we do
  not have; nothing in the panel treats *housing and energy price* as the mediating capital
  stock, which is the standard economic framing of adaptation and is absent from the
  repository entirely.
- **identification_threats:**
  - The outcome file has no geography, no housing type, and no income, so the weights
    `w_h` are unobservable at any level.
  - Tariff changes are territory-wide and therefore perfectly collinear with time.
  - Adaptation and depletion (HE-01) both produce a declining fitted trend and are not
    separable without a cross-section.
- **what_would_kill_it:** The absence of any spatial dimension kills it now. A decisive
  version needs district-level or cluster-level monthly counts joined to Census
  air-conditioning ownership and housing type; without that join there is no test, only a
  story. Park it, and record the exact data join that would revive it, so that a future
  governance request can ask for the right thing in one attempt.
- **data_required:** *HAS* — territory-level counts and exposure only. *LACKS* — district
  or cluster geography, housing type, Census appliance ownership linkage, electricity
  tariff history.
- **status_proposal:** park
- **provenance:** SYNTHETIC_THEORY

---

## HE-12 The time price of an admission: caregiver endowment and calendar composition

- **paradigm_id:** HE-12
- **theoretical_space:** *Extra* — household time endowment as an access price
- **claim_type:** identification
- **economic_object:** The time price `τ_t` of converting need into a recorded admission,
  and the calendar composition of a month as a source of variation in it that is orthogonal
  to temperature.
- **structural_sketch:** An elderly person's first hospitalisation is jointly produced:
  someone must notice deterioration, decide, and provide transport. That someone is a
  family member or a domestic helper, and their availability is not uniform across the days
  of a month. Hong Kong's Employment Ordinance guarantees one rest day in every seven,
  in practice usually Sunday, and public holidays cluster with lunar and Western calendars.
  Write `E[Y_t] = h(T_t) · Σ_d κ(type_d)` where `κ` is a caregiver-availability weight by
  day type. Months contain four or five of any given weekday, and holiday counts vary
  substantially, so the *effective* offset is `Σ_d κ(type_d)`, not `d_t`. The crucial
  property is that rest-day and holiday counts are essentially uncorrelated with monthly
  temperature. That makes calendar composition a rare thing in this dataset: a shifter of
  the conversion equation in HE-02 that does not shift biological need — a candidate
  exclusion restriction, obtainable with no new governed data.
- **why_not_already_explored:** P10 already carries holiday indicators, but strictly as a
  nuisance control on the count equation. The new content is threefold: reading calendar
  composition as a *price* rather than a nuisance, using it as an exclusion restriction to
  separate `α_T` from `γ_T` in HE-02, and recognising that the days-in-month offset is
  misspecified in a way that has an economic interpretation. This is a reuse of an existing
  covariate for a structurally different purpose, and it should be logged as such rather
  than claimed as a new variable.
- **identification_threats:**
  - The exclusion restriction requires that calendar composition affects need not at all,
    which is arguable: activity patterns and diet differ on holidays.
  - Lunar New Year moves between January and February and is confounded with the coldest
    months, so the largest holiday shock is *not* orthogonal to temperature and may need to
    be excluded from the instrument.
  - Weak-instrument risk is real: the variation is four-versus-five days out of thirty, and
    132 observations is a small first stage.
- **what_would_kill_it:** Add rest-day and non-Lunar-New-Year public-holiday counts to the
  analysis of record, both as covariates and inside the offset. If their coefficients are
  null and `θ` for CHD hot nights and HF cold days is unchanged to three decimals, then the
  time-price channel is empirically inert here, HE-12 dies, and HE-02 loses its only cheap
  instrument — which is itself a decisive and reportable result. The test costs one model
  refit and no governance.
- **data_required:** *HAS* — everything: monthly counts, the Hong Kong public-holiday
  calendar, and the existing specification. *LACKS* — individual caregiver status, day-level
  admission timing, helper-population series by month.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## Portfolio summary

| ID | Space | Claim type | Status | Runnable without new governed data? |
|---|---|---|---|---|
| HE-01 | Stock-flow / finite risk pool | costing | candidate | Yes (Monte Carlo) |
| HE-02 | Two-equation utilisation | identification | candidate | Partly (needs HE-12 instrument) |
| HE-03 | Capacity-constrained supply | identification | likely_fail | Yes (Monte Carlo) |
| HE-04 | Value of information | VoI | candidate | Yes (decision tree) |
| HE-05 | Intertemporal cost shifting | welfare | candidate | Yes (Monte Carlo) |
| HE-06 | Time-inconsistent budgeting | mechanism | park | No (needs cluster data) |
| HE-07 | Selection into hospitalisation | welfare | candidate | No (needs outpatient series) |
| HE-08 | Macro health-system shocks | identification | candidate | Yes (existing series) |
| HE-09 | Dual public/private system | identification | candidate | No (needs private volumes) |
| HE-10 | Aggregation / index-number bias | costing | candidate | Yes (Monte Carlo, cheapest) |
| HE-11 | Household adaptation capital | mechanism | park | No (needs geography) |
| HE-12 | Caregiver time price | identification | candidate | Yes (one refit) |

Nine candidates, one likely_fail, two parked. Five are decidable today with no new governed
data, which is the property that matters while the stroke file and person-time denominator
are outstanding.

## YAML-ready paradigm list

```yaml
# analysis_plan/health_econ/paradigm_registry.yml — Cycle 1
cycle: 1
provenance: SYNTHETIC_THEORY
paradigms:
  - id: HE-01
    title: Depletion as an exhaustible stock, not a renewable flow
    space: stock_flow_finite_risk_pool
    claim_type: costing
    status: candidate
    one_line: First-event counts draw down a bounded pool, so any projection multiplying a ratio by future events prices a flow the stock cannot sustain.
  - id: HE-02
    title: Two-equation utilisation, need versus conversion
    space: two_equation_utilisation
    claim_type: identification
    status: candidate
    one_line: Monthly counts identify only the sum of a pathophysiology elasticity and a care-seeking elasticity, so the sign of the welfare effect is unidentified.
  - id: HE-03
    title: Shadow price of a bed under capacity rationing
    space: capacity_constrained_supply
    claim_type: identification
    status: likely_fail
    one_line: Capacity binds on days and washes out in monthly sums, so the bed shadow price is not recoverable at our resolution.
  - id: HE-04
    title: Value of information with a moving claim set and a static posterior
    space: value_of_information
    claim_type: VoI
    status: candidate
    one_line: The stroke file changes no decision under Option A, while person-time changes the admissible sentence rather than the estimate.
  - id: HE-05
    title: Economic harvesting of hospital spending
    space: intertemporal_cost_shifting
    claim_type: welfare
    status: candidate
    one_line: The displacement fraction separates shifted spending from new spending and bounds any monetisation, but may be unidentified at n=132.
  - id: HE-06
    title: Present-biased budgeting and the fiscal cycle inside the month dummies
    space: time_inconsistent_public_budgeting
    claim_type: mechanism
    status: park
    one_line: Annual budget myopia under-provides adaptation capital, and fiscal seasonality is perfectly collinear with our calendar-month indicators.
  - id: HE-07
    title: The visible fraction of the welfare loss
    space: selection_into_hospitalisation
    claim_type: welfare
    status: candidate
    one_line: Admissions are the tail above a severity threshold that itself moves with heat, so the burden is a selected subset and not a clean lower bound.
  - id: HE-08
    title: The weather-to-spending map is not policy-invariant
    space: macro_health_system_shocks
    claim_type: identification
    status: candidate
    one_line: Pandemic demand destruction is concentrated in the Februaries that carry cold-day identification, making the pooled elasticity a regime-weighted average.
  - id: HE-09
    title: Public counts are a share, not a total
    space: dual_public_private_system
    claim_type: identification
    status: candidate
    one_line: The Authority extract measures the public share, so a thermal coefficient mixes morbidity with routing between public and private sectors.
  - id: HE-10
    title: Monthly exposure as a unit-value index
    space: aggregation_index_number_bias
    claim_type: costing
    status: candidate
    one_line: The monthly coefficient aggregates a nonlinear daily response with variance-gradient weights, giving a signed bias in any scenario costing.
  - id: HE-11
    title: Household adaptation capital, housing and tariffs
    space: household_adaptation_capital
    claim_type: mechanism
    status: park
    one_line: Effective exposure is produced with air-conditioning capital, so a territory coefficient is a capital-weighted average that drifts as saturation rises.
  - id: HE-12
    title: The time price of an admission
    space: household_time_endowment
    claim_type: identification
    status: candidate
    one_line: Rest-day and holiday composition varies across months and is orthogonal to temperature, giving a candidate exclusion restriction for the conversion equation.
```

## Failed on arrival — rejected before entering the portfolio

Logged so the registry never re-walks them.

| Rejected mechanism | Why rejected |
|---|---|
| Simple cost of illness: ratio times events times unit cost | The named trap. Assumes a renewable flow (HE-01), a pure need channel (HE-02), no displacement (HE-05), and an unselected outcome (HE-07). It is a critique target, never a survivor. |
| Behavioural nudges, SMS reminders, heat-warning messaging as the mechanism | Explicitly on the anti-convergence registry. Also unidentifiable here: no individual-level exposure to any message. |
| DLNM-based attributable-fraction costing | Re-runs the daily paradigm already covered by the Jasmine and Roro layers, and no daily coefficient exists after the failed M|D calibration. |
| Re-tuning M\|D daily recovery to obtain daily cost coefficients | Already logged as a dead end on 13 August. Retuning after a failed 500-replicate calibration is the definition of re-walking. |
| VSL-based mortality valuation | Our file has no mortality outcome. Valuing deaths belongs to the mortality layer, not to a first-hospitalisation morbidity file. |
| QALY or DALY burden from admissions | Requires severity, length of stay, and utility weights. We have counts only. |
| Cost-effectiveness of a heat action plan | Requires an effectiveness parameter for an intervention we have never observed being switched on or off. |
| Difference-in-differences on heat warnings | One territory, no control unit, warnings issued territory-wide. There is no untreated group. |
| Synthetic control for Hong Kong | No donor pool combines a comparable single-payer hospital system with comparable subtropical exposure. |
| Price-elasticity or insurance-demand estimation | Point-of-service price in the public system is a token fee with no usable variation over our window. |
| Machine-learning hospital cost prediction, or any dashboard | Prediction without an economic object. Also explicitly out of scope for this cycle. |
| Air-pollution co-benefit monetisation from P11 | Would need concentration-response plus valuation, which routes straight back into the cost-of-illness trap on a co-predictor we already refuse to promote. |
| Any AMI or principal-diagnosis costing | Admission cause is absent. Prohibited by the project contract. |
| Stroke cost per case, or any stroke economic quantity | The stroke file was never delivered. Nothing about stroke may be priced, modelled, or projected. |
| Gazetted ward fees used as if they were costs | Fees are administered prices, not opportunity costs. Worth logging as a common error in Hong Kong health-economics work, not worth pursuing. |
| Mortality displacement relabelled as "economic harvesting" | Only admitted as HE-05 *because* it is about resource timing rather than deaths. The mortality version is a duplicate and is rejected. |
| Productivity-loss transfer using published climate-labour elasticities | Would import elasticities from other settings and apply them without any Hong Kong labour data, producing a number with no local content. |

## Mutation seeds for Cycle 2

The Cycle 1 hypotheses are static. Two mutations should be applied to whatever survives.

**(a) Under dynamic time-inconsistency**

- **HE-01 becomes a Hotelling problem.** If the unhospitalised pool is exhaustible, the
  shadow value of a remaining member rises as the stock depletes, so the correct unit cost
  in any projection is a rising scarcity rent rather than a constant. A present-biased
  planner will under-value the remaining stock and systematically under-invest in
  preventing draw-down. This converts HE-01 from a caveat into a pricing rule.
- **HE-04 becomes a commitment problem.** The naive EVPI computed under exponential
  discounting is the benchmark; under `(β, δ)` preferences a present-biased scholar or
  supervisor will submit too early relative to that benchmark. The interesting Cycle-2
  question is not "what is the option worth" but "what commitment device — a pre-registered
  stroke addendum clause, a written Gate 3 rule — restores the exponential decision".
- **HE-07 becomes endogenous to the policy.** The severity threshold `s*` is the output of a
  household investment problem; if households are present-biased about adaptation, then
  `ω` responds to the very interventions being evaluated, and the evaluation is not
  invariant to its own success.

**(b) Under supply-side rationing or a monopsonistic Authority**

- **HE-02 under rationing.** The conversion probability `π` stops being a demand object and
  becomes a queue-clearing rule, so the identified elasticity is an elasticity of
  *rationing*, not of demand. Every welfare statement flips sign convention.
- **HE-09 under monopsony.** If the Authority is a monopsonist in clinical labour and a
  near-monopolist in acute care, the private sector is a price-rationed safety valve; heat
  shocks then surface as private volume, and the public elasticity understates the total by
  a factor governed by the substitution elasticity. HE-09 and HE-03 stop being independent.
- **HE-10 under capacity.** Daily top-truncation from capacity composes with the Jensen
  aggregation term, giving a doubly biased monthly coefficient whose sign is ambiguous
  analytically. That composition is a clean, self-contained Monte Carlo target and is
  probably the single most informative Cycle-2 simulation.
- **A new cross-sectional seed.** Several parked hypotheses (HE-06, HE-11) and one
  likely_fail (HE-03) revive together if cluster-level or district-level monthly counts ever
  become available under governance. Cycle 2 should price *that* single data request as a
  portfolio, using the HE-04 machinery, rather than requesting each dataset separately.

## What Cycle 1 does not license

- No monetisation of any existing coefficient.
- No stroke economics of any kind.
- No claim that Gate 3 is frozen, or any input to that freeze.
- No new pathway ID, registry entry, or SAP amendment; these are hypotheses, and promotion
  requires a human nod under the Explore-mode rule.
- No assertion that any external dataset named above exists. Private-sector volumes,
  outpatient series, cluster budgets, and Census linkages are all listed as *to be
  verified*, not as available.
