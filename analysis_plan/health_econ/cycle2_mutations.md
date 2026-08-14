# Health-economics mutation portfolio — Cycle 2

**Mode:** Explore. **Date:** 14 August 2026. **Provenance of every object below:** `SYNTHETIC_THEORY`.

This document mutates the Cycle 1 layer along two axes that Cycle 1 held fixed: dynamic
time-inconsistency, and a supply side with market power. It contains **no findings**, no
coefficients, no currency, and no input to Gate 3. `monetisation_permitted: false` holds
throughout, and is enforced below by construction rather than by warning: the objects
defined here are constraints on any future costing, not costings.

Sources: [`cycle1_hypotheses.md`](cycle1_hypotheses.md) (HE-01–HE-12) and
[`cycle1_adversarial_audit.md`](cycle1_adversarial_audit.md) (the hostile referee report
that killed seven, park-confirmed two, and escalated three).

## What a mutation is, and what it is not

A mutation takes a Cycle 1 object, changes one structural assumption of the environment,
and asks whether a **different** economic object becomes definable. It creates a new
paradigm ID with a new kill test.

It does **not** overturn a Cycle 1 verdict. HE-01, HE-02, HE-03, HE-04, HE-05, HE-09 and
HE-12 remain `KILL` as formulated. HE-06 and HE-11 remain `PARK-CONFIRMED`. Nothing in
this document may be cited as a rescue of those claims. Where a mutation inherits the
same fatal object as its parent — an unobserved stock, an unobserved capacity, an
elicited prior — it inherits the kill with it, and that is stated in each entry.

The reason to mutate a killed object at all is that the kill was a statement about
*identification of a particular parameter*, not about the emptiness of the surrounding
economics. A stock that cannot be valued may still impose a sign restriction on any
valuation. A conversion probability that cannot be separated from need under a demand
model may have a second-moment signature under a rationing model. That is the whole of
the Cycle 2 method.

## Scope contract, carried forward unchanged

- Estimand of record: ecological monthly count ratios for first hospitalisation after
  first CHD or HF diagnosis in a T2D/HTN cohort, Hong Kong, 132 territory-months,
  January 2013 – December 2023. Admission cause is **absent**.
- Analysis of record: separate negative-binomial exposures, calendar-month indicators,
  `ns(time, 4)`, days-in-month offset, Model/HC1/NW3/NW6 uncertainty ladder.
- All twelve core BH q-values exceed **0.19**. HF cold days per 5: **1.073 (1.006–1.144)**.
  CHD hot nights per 5: **1.022 (1.002–1.042)**, SE-sensitive. **Gate 3 is open.**
- First-event totals halve (CHD **23,830 → 12,323**, HF **4,336 → 2,296**, 2013 → 2023)
  against a rising C&SD 35+ denominator. The offset is **not** T2D/HTN person-time.
- Influence leaders are **2020-02** and **2022-02**; **141 of 145** cold days fall in DJF.
- M|D daily recovery **failed** 500-replicate calibration; no daily coefficient exists.
  The stroke file was never delivered; no stroke coefficient exists.

Every other numeric symbol in this document is `SYNTHETIC` or theoretical and exists to
make a structure legible. No HA row count, field meaning, stroke coefficient, capacity
figure, budget, or unit cost is asserted, implied, or estimated.

## The two mutation axes

**Axis A — dynamic time-inconsistency.** Cycle 1 implicitly assumed exponential
discounting and a static environment. Replace it with quasi-hyperbolic `(β, δ)`
preferences held simultaneously by three agents with different horizons: the **household**
deciding whether to invest in monitoring and adaptation and when to present; the
**Hospital Authority manager** deciding between recurrent spending and capital that pays
off over decades; and the **scholar** deciding when to submit against a Laidlaw calendar.
The interesting consequences are never the value of `β` — which is not in these data and
must never be "estimated" from them — but the *wedges*, *reversals*, and *reflexivity*
that `β < 1` introduces into objects that would otherwise be stationary.

**Axis B — supply-side market power.** Cycle 1 modelled demand. Replace the price-taking,
infinitely elastic provider with a monopsonist that rations: a single public Authority
with a binding **daily** capacity, an elective buffer that is cancelled first, and an
admission threshold set to clear a queue rather than to reflect a household's willingness
to seek care. Under Axis B, several quantities Cycle 1 treated as demand objects become
allocation rules, and their econometric character changes from "product of two latent
channels" to "censoring at an unobserved, endogenous, time-varying boundary".

The two axes interact. A present-biased manager under-provides the capacity that
determines where the censoring boundary sits; the boundary then determines what the
household's present bias is even allowed to express. Where that interaction generates a
distinct object, it is stated in the entry.

## Inheritance map

| Cycle 1 object | Verdict | Axis | Cycle 2 object | What is inherited | What is genuinely new |
|---|---|---|---|---|---|
| HE-01 | `KILL` | A | HE-C2-01 | Unobserved stock `S_t`, unobserved inflow | The rent's *growth condition* and its sign, not its level |
| HE-02 | `KILL` | B | HE-C2-02 | No shifter of conversion alone | Second-moment detection of a censoring regime |
| HE-04 | `KILL` | A | HE-C2-04 | No prior, no agreed utility | Prior-free preference-reversal set and revocability |
| HE-07 | `SURVIVE-TO-ESCALATION` | A | HE-C2-07 | Unobserved severity threshold `s*` | `s*` responds to the policy being evaluated |
| HE-08 | `SURVIVE-TO-ESCALATION` | A | HE-C2-08 | Regime-weighted pooled coefficient | Regime as a *decaying, non-stationary* state with two rates |
| HE-10 | `SURVIVE-TO-ESCALATION` | A+B | HE-C2-10 | Nonlinear daily response, monthly aggregation | Composition with daily top-truncation; **signed**, possibly cancelling |
| HE-03 + HE-06 + HE-11 | `KILL` + 2 × `PARK-CONFIRMED` | B | HE-C2-PORT | Absence of any cross-section | The three die of the *same* absence, so they are one request |

---

## HE-C2-01 Hotelling scarcity rent on a depleting first-event stock under present-biased prevention

- **paradigm_id:** HE-C2-01
- **mutates:** HE-01 (`KILL` — stock and inflow unobserved)
- **mutation_axis:** A (dynamic time-inconsistency)
- **theoretical_space:** Exhaustible-resource pricing with quasi-hyperbolic extraction
- **claim_type:** costing constraint (a restriction on any future costing, not a costing)
- **economic_object:** The **growth condition** on the shadow price `μ_t` of leaving one
  member of the diagnosed pool unhospitalised, and the wedge that `β < 1` opens in it.
  Not the level of `μ_t`, which HE-01 already died for.
- **structural_sketch:** Recast the depleting pool as an exhaustible resource in which
  extraction is the bad. Let `R_t` be the diagnosed-but-not-yet-hospitalised stock and let
  a planner choose prevention effort `a_t` that lowers the extraction hazard
  `h(T_t, a_t)`. Under exponential discounting the interior optimum satisfies a Hotelling
  arbitrage condition: the rent must grow at the augmented interest rate,
  `μ_{t+1} / μ_t = 1 + r + m_t`, where `m_t` is the competing-risk rate at which a member
  leaves the pool for reasons that destroy the option — death, emigration, permanent
  routing to the private sector. Inflow `I_t` of newly diagnosed members makes the
  resource partially renewable and damps the growth rate; the exhaustibility premium is
  increasing in `(1 − ρ)` with `ρ = I_t / Y_t`. Cycle 1's observation that both series
  halve while the 35+ denominator rises is *consistent with* `ρ < 1` and does not measure
  it; that remains true here. Now impose `(β, δ)`. The current self discounts the next
  period by `βδ` and all later steps by `δ`, so the *perceived* one-step rent growth is
  `(1 + r + m_t) / β`, strictly above the true rate. Prevention today therefore looks
  relatively expensive against a benefit the planner believes will still be there
  tomorrow. A naive planner re-plans each period and never invests; a sophisticated one
  seeks commitment technology, which is exactly the object of HE-C2-04. The wedge is
  `Δ_β,t = (1 − β) μ_t`, and because `μ_t` rises as the stock depletes, **myopia and
  scarcity compound**: under-provision is worst late in the depletion path, which is where
  the observed series actually is. The single structural consequence that matters for this
  project is a *veto*, not a number: any future projection that multiplies a count ratio
  by a constant unit value has assumed a constant `μ`, and the constant-`μ` assumption is
  inconsistent with the depletion the record already displays. The error it induces has a
  known direction — early periods over-weighted, late periods under-weighted — even though
  its magnitude is not identified.
- **why_not_already_explored:** Cycle 1's HE-01 asked for a liability *level*
  `L_t = Σ_k δ^k c E[Y_{t+k} | S_t]` and was correctly killed because `S_t` is not
  observed. No document has asked whether the depletion imposes a restriction on the
  *time path* of any admissible unit value, which is a weaker and structurally different
  question. **Anti-convergence guard:** this must not become simple cost of illness with a
  trend term bolted on. If the output is "the coefficient survives a depletion-shaped
  trend", the object has collapsed back into P10/P16 and must be discarded.
- **identification_threats:**
  - `R_t`, `I_t`, `ρ`, `m_t` and `μ_t` are all unobserved. The Cycle 1 kill is inherited
    in full: no level, no liability, no rent may be reported.
  - The one observable implication — a declining exposure modulation `θ_t` as the residual
    pool is selected toward low-hazard members — is observationally equivalent to
    household adaptation (HE-11), to regime drift (HE-C2-08), and to plain misfit of
    `ns(time, 4)`.
  - Left truncation at 2013 mixes incident and long-prevalent members, so frailty
    selection is confounded with the composition drift of the initial stock.
  - `m_t` includes private-sector routing, which is the unobserved public share of the
    killed HE-09. Two unidentified objects appear inside one condition.
- **what_would_kill_it:** A **DGP-discrimination** Monte Carlo, which is a different test
  from Cycle 1's size calculation. Construct three synthetic worlds, each calibrated to
  reproduce the observed halving of first-event totals against a rising 35+ denominator:
  (i) Hotelling depletion with present-biased extraction and frailty selection of the
  residual pool; (ii) a constant stock with a rising household adaptation capital that
  attenuates `θ` over the window; (iii) no structural change at all, with the decline
  generated by diagnosis ascertainment drift and `ns(time, 4)` misfit. Fit the analysis of
  record augmented with an exposure × time interaction, apply the three mandatory
  escalation stresses from the Cycle 1 audit (MNAR deletion keyed to `Y_t` and extremes; a
  continuous macro shock correlated with both `T` and `Y`; absorbing first events with a
  heat-dependent threshold), and report the **confusion matrix of DGP recovery** with
  pairwise AUC. If pairwise AUC is below a pre-registered threshold — 0.6 is the proposed
  `SYNTHETIC` value, to be fixed before running — the rent path is not even *qualitatively*
  identified. HE-C2-01 then dies as an empirical object and survives only as the costing
  veto stated above, which is a discussion-section sentence and not a research strand.
  The expected outcome is exactly that.
- **data_required:** *HAS* — monthly first-event counts, real daily and monthly HKO
  exposure, C&SD 35+ population, the fitted specification. *LACKS* — still-at-risk
  person-time, cohort entry dates, inflow `I_t`, competing-risk exits, any prevention
  activity series, any unit value.
- **status_proposal:** likely_fail
- **provenance:** SYNTHETIC_THEORY

---

## HE-C2-02 Conversion as a queue-clearing rule: censoring, not a demand channel

- **paradigm_id:** HE-C2-02
- **mutates:** HE-02 (`KILL` — need and conversion not separable)
- **mutation_axis:** B (monopsonistic Authority with binding daily capacity)
- **theoretical_space:** Rationed allocation with an unobserved, endogenous censoring boundary
- **claim_type:** identification (detection, not valuation)
- **economic_object:** Whether a **rationing regime is detectable at all** in the second
  moment of the monthly counts — and, if it is, the recognition that the elasticity of
  record is then an elasticity of *allocation* rather than of demand, with a different
  welfare sign convention.
- **structural_sketch:** Under HE-02, `E[Y_t] = N_t · π_t` with `π` a household
  care-seeking probability, and the kill was that nothing shifts `π` alone. Under Axis B,
  `π` is not a household object. The Authority sets an admission threshold `s*_t` to clear
  the queue subject to daily capacity `K_d`, cancelling electives first, so realised daily
  admissions are `A_d = min(D_d, K_d)` and the monthly count is `Y_t = Σ_d A_d`. The
  system is no longer two simultaneous equations in a latent product; it is a **censored
  count process at an unobserved, endogenous, time-varying boundary**. This changes the
  econometric character, and with it the informative moment. Mild daily truncation removes
  only the extreme upper days, so its effect on the monthly **mean** is second-order —
  which is precisely why HE-03 died. But truncation removes the largest deviations, so its
  effect on the monthly **variance** is proportionally larger, and under approximate daily
  independence the variance of a sum of truncated variables scales with `n` rather than
  cancelling. The observable implication is therefore a **dispersion profile**: under
  queue clearing, the negative-binomial dispersion should *decline* in the fitted mean,
  because high-load months are exactly the months where the boundary bites. Under a pure
  demand world with a correctly specified negative-binomial law, the dispersion profile
  should be flat. The welfare consequence is a sign convention, and it is severe: a
  positive `θ` under rationing means the queue released, not that need rose; and a null
  `θ` is fully compatible with a large need shock absorbed entirely by threshold movement
  and elective displacement. Under Axis B, "no association" is not "no burden".
- **why_not_already_explored:** Every Cycle 1 hypothesis, and every pathway in P01–P18,
  interrogates the conditional **mean**. Nothing in the repository has asked what the
  conditional **variance** of the monthly counts is evidence for, and the negative-binomial
  dispersion parameter is currently a nuisance term estimated and discarded.
  **Anti-convergence guard:** this is not HE-03 revived. HE-C2-02 makes no attempt to
  recover `λ_t`, `K_d`, occupancy, or a shadow price, and produces no valuation. It asks
  only whether the *presence* of a censoring regime leaves a signature. If any output
  reports a bed shadow price, a capacity figure, or a cost, the object has collapsed into
  the killed HE-03 and must be discarded. It is also not simple COI: there is no
  multiplication anywhere in it.
- **identification_threats:**
  - Serial dependence of daily demand adds covariance terms to the monthly variance and
    can mimic or mask dispersion compression. Weather is strongly autocorrelated, so this
    threat is not hypothetical.
  - `K_d` is unobserved, endogenous to anticipated seasonal demand, and probably itself
    seasonal — so the boundary moves with the exposure whose effect is being estimated.
  - The first-event restriction and the depleting stock (HE-C2-01) both change the mean
    path over the window, and the dispersion profile is estimated conditional on that
    fitted mean.
  - Overdispersion has many sources — unmodelled heterogeneity, coding batches, reporting
    delay — and a declining dispersion profile is not uniquely a rationing signature.
  - Detection is not identification. Even a clean positive result would say only that some
    censoring regime is present, never how much welfare it hides.
- **what_would_kill_it:** A **moment-power** Monte Carlo, runnable with no governed health
  data. Simulate two families of daily processes on the real HKO exposure path, matched so
  that the fitted monthly **mean** paths are indistinguishable: a demand-only family with
  negative-binomial daily counts, and a queue-clearing family applying `min(D_d, K_d)` at
  utilisation levels `K/E[D] ∈ {0.7, 0.85, 0.95, 1.05}` (`SYNTHETIC`), with both flat and
  seasonal capacity. Aggregate to months, fit the exact analysis of record, and compute a
  pre-registered dispersion-profile statistic — the slope of squared Pearson residuals on
  the fitted mean, or estimated dispersion in the top versus bottom tercile of fitted
  values. Apply all three mandatory escalation stresses, and add daily serial dependence
  calibrated to the real exposure autocorrelation as a fourth. Report power at `n = 132`.
  If power to separate the two families is below a pre-registered level — 0.5 is the
  proposed `SYNTHETIC` value — then rationing and demand are observationally equivalent in
  **both** moments at this resolution, HE-C2-02 dies, and the surviving residue is a
  written statement that the sign convention of the estimand is not established. If power
  is adequate, the deliverable is still not a finding: it is a pre-specified sensitivity
  whose result would qualify the interpretation of `θ`, never monetise it.
- **data_required:** *HAS* — monthly counts, real daily and monthly HKO exposure, the
  fitted specification, the existing dispersion estimates. *LACKS* — bed-day capacity,
  occupancy, elective cancellation counts, A&E process data, waiting times, length of
  stay, any cluster breakdown.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-C2-04 Commitment technology, not option value: the prior-free reversal set

- **paradigm_id:** HE-C2-04
- **mutates:** HE-04 (`KILL` — EVPI arbitrary without prior, utility, decision-maker, deadline)
- **mutation_axis:** A (dynamic time-inconsistency)
- **theoretical_space:** Commitment under quasi-hyperbolic preferences
- **claim_type:** governance structure (explicitly **not** an estimated economic parameter)
- **economic_object:** The **preference-reversal set** — the set of horizons at which the
  ranking of "wait for the stroke file or person-time" against "proceed" flips between the
  planning date and the decision date — together with the **revocability audit** of the
  repository's own written rules as candidate commitment devices.
- **structural_sketch:** The Cycle 1 audit killed EVPI because it requires a prior over
  the missing quantity, a utility over claims and delay, a decision set, a named
  decision-maker, and a deadline; none of these exist in the record, and eliciting them
  would make the "result" a restatement of its own inputs. The mutation abandons the level
  entirely. Under `(β, δ)`, the object that survives without a prior is a property of the
  *ordering*, not of the magnitudes: a preference reversal exists if and only if the sign
  of the perceived utility gap between waiting and proceeding changes as the horizon
  shrinks, and that is determined by the *shape* of the payoff profile against the
  `(β, δ)` discount sequence. If the payoff to waiting is back-loaded relative to the
  payoff to proceeding, then a `β < 1` agent who plans to wait at distance `k` will
  proceed at distance zero, for every prior consistent with the ordering. This is
  prior-free in the exact sense the audit demanded: it needs the ranking, not the level.
  Second, the mutation asks the question that follows a reversal: a sophisticated agent
  buys commitment. The repository already contains candidate devices — the Gate 3 rule,
  the pre-specification discipline in Playbook 03, the SAP, the claim ledger. A written
  rule is a commitment device only if it satisfies three conditions: **written before the
  information arrives**, **observable to a third party** (the PI and co-authors), and
  **costly to revoke**. A rule that fails any one is cheap talk, and its commitment value
  is zero by construction. The deliverable is therefore a two-column audit of existing
  rules against those three conditions, plus the identification of which of the three is
  missing where. The self-referential case is included on purpose: the scholar's own
  submission clock is one of the three `(β, δ)` agents in this cycle, and pretending
  otherwise would be the least honest thing in the document.
- **why_not_already_explored:** The repository treats missing files as governance blockers
  and Cycle 1 tried to treat them as priced options. Neither asked whether the *structure*
  of the waiting decision is time-consistent, which is the one question about it that does
  not require inventing a prior. **Anti-convergence guard:** if any output contains a
  numeric EVPI, an expected value of sample information, a "cost of delay" in currency, or
  an assumed volatility for a real-options calculation, the object has collapsed back into
  the killed HE-04 and must be discarded. This produces a memo, and a memo is not a result.
- **identification_threats:**
  - The payoff ordering is itself asserted, not observed. If waiting and proceeding are
    not comparable at all — different papers, different claims — the reversal set is not
    merely empty, it is undefined.
  - The decision-maker is plural. Under a PI, co-authors, and a scholar with different
    loss functions, the operative object is a bargaining outcome and `β` is not even a
    property of a single agent. The common-agency structure is deferred to Cycle 3.
  - No external deadline structure is written down anywhere in the repository. Cycle 1
    listed this under *LACKS* and it is still missing; an invented deadline would
    manufacture the very back-loading that generates a reversal.
  - "Costly to revoke" is a social fact about this team, owned by humans. An agent can
    audit whether a rule is written and observable; it cannot price the cost of breaking it.
- **what_would_kill_it:** Two prior-free checks, in order. **(1) Reversal-set
  nonemptiness.** Enumerate the admissible payoff orderings — there are few, because the
  action set is small — and determine whether any `β ∈ (0, 1]` produces a different
  preferred action at distance zero than at distance `k`. If the preferred action is
  invariant to the horizon under every admissible ordering, there is no time-inconsistency
  problem here, the entire commitment framing dies, and it dies without any prior having
  been elicited. **(2) Revocability audit.** Score each candidate device on written-first,
  third-party-observable, costly-to-revoke. If no candidate satisfies all three, the
  commitment premium is zero by construction and HE-C2-04 dies as governance theatre —
  which is a genuinely useful thing to have established cheaply. Neither check may be
  reported as an economic estimate, and neither may be used to advance, delay, or
  otherwise touch Gate 3, which is a team decision that this cycle does not participate in.
- **data_required:** *HAS* — the written rules themselves, the Gate 3 packet, the SAP, the
  playbooks, the offset-sensitivity table, the action set. *LACKS* — any written deadline
  structure, a named single decision-maker, an agreed loss function, and any legitimate
  basis for a prior over the undelivered stroke file.
- **status_proposal:** candidate (output is a governance memo, human-owned, never an estimate)
- **provenance:** SYNTHETIC_THEORY

---

## HE-C2-07 Endogenous visibility: `ω(T, P)` when the severity threshold is a household investment

- **paradigm_id:** HE-C2-07
- **mutates:** HE-07 (`SURVIVE-TO-ESCALATION` — report the selection-envelope width, SEW)
- **mutation_axis:** A (dynamic time-inconsistency), interacting with B
- **theoretical_space:** Reflexive selection — the observed outcome responds to the policy being evaluated
- **claim_type:** welfare (an evaluation-design veto)
- **economic_object:** The **policy-reflexivity wedge**: the share of any post-policy change
  in recorded admissions that is a movement in visibility rather than in health, and the
  probability that it reverses the sign of the inferred health effect.
- **structural_sketch:** HE-07 wrote `ε_Y = ε_M + d log ω / d log T` with
  `ω(T) = 1 − F(s* | T)`, and the audit's surviving objection was that `s*` is unobserved
  and heat-dependent. The mutation makes `s*` an *investment*. A household chooses
  monitoring and adaptation — a blood-pressure cuff used or not, a fan or air conditioner
  run or not, an early clinic visit taken or deferred — with immediate costs and delayed
  benefits. Under `(β, δ)` the household under-invests, so `s*` sits systematically above
  the socially optimal threshold, and the shortfall is largest exactly where the benefit is
  most delayed. That predicts a *differential*: slow-onset decompensation, which is the
  HF pathway, should carry a wider selection envelope than acute presentation, which is
  closer to the CHD pathway. Write the envelope difference as
  `DSEW(Γ) = SEW_HF(Γ) − SEW_CHD(Γ)`; because both outcomes share the same exposure,
  missingness and macro-shock stresses, part of the nuisance cancels in the difference.
  The sharper consequence is reflexivity. Write `ω(T; P)` where `P` indexes any policy that
  changes detection or presentation. Then
  `d log Y / dP = d log M / dP + d log ω / dP`, and a policy that works — one that lowers
  latent morbidity `M` while also raising detection `ω` — can **raise** the recorded
  admission count. An evaluation that reads admissions as health therefore has a
  sign-reversal region, and its width is a property of the design rather than of the
  intervention. Under Axis B the reflexivity is doubled: the Authority also moves `s*` to
  clear its queue, so the threshold has both a household and an institutional component
  moving for unrelated reasons.
- **why_not_already_explored:** HE-07 treated `s*` as an unknown but *exogenous* parameter,
  and the live Introduction treats sub-threshold morbidity as unmeasured motivation.
  Neither treats the threshold as an object that responds to the evaluation itself, which
  is the Lucas critique relocated from the macro system to the household.
  **Anti-convergence guard:** this is emphatically **not** a behavioural-nudge hypothesis,
  which the registry rejected and which remains rejected. No message, warning, or reminder
  is being proposed, evaluated, or claimed to work; there is no individual-level exposure
  to any message in these data and there never will be. The claim is the reverse in
  direction: that *any* visibility-affecting policy makes an admissions-based evaluation
  non-invariant, which is a critique of evaluation design. If any output describes the
  effect of a warning system, it has collapsed into the rejected nudge paradigm and the
  already-rejected territory-wide DiD, and must be discarded.
- **identification_threats:**
  - `s*` is unobserved, and both of its components — household and institutional — move
    with heat in the same direction, so the wedge is not signed a priori.
  - The DSEW differential is not scale-free: CHD counts are several times HF counts, so
    precision differs and the difference must be normalised before it means anything.
  - The two outcomes also differ in clinical urgency, coding practice, and pathway to
    admission, so a non-zero DSEW is compatible with explanations that have nothing to do
    with present bias.
  - Bounding `Γ_P`, the admissible movement of `s*` under a policy, requires an auxiliary
    morbidity series whose own threshold is *less* policy-sensitive than the admission
    threshold. Whether such a series exists is unverified, and Cycle 1's outpatient
    proposal is not obviously it: outpatient attendance is plausibly *more* policy-elastic,
    not less.
  - The first-event restriction truncates severity again, interacting with the depleting
    stock of HE-C2-01.
- **what_would_kill_it:** A **sign-reversal probability** under a pre-registered
  reflexivity envelope. Fix a bound `Γ_P` on how far a policy may move `s*`, simulate the
  full stress ensemble from the Cycle 1 audit with both household and institutional
  threshold components, and report
  `SRP(Γ_P) = Pr[ sign(d log M / dP) ≠ sign(d log Y / dP) | Γ_P ]`, alongside the
  normalised `DSEW(Γ)`. If `SRP` is negligible across the entire admissible range of
  `Γ_P`, reflexivity is cosmetic and HE-C2-07 dies, leaving HE-07's SEW as the whole of
  the selection story. If `SRP` is non-negligible for any admissible `Γ_P`, the result is a
  design veto: recorded admissions cannot evaluate any policy that also changes detection,
  and that sentence belongs in a limitations section rather than in a result. The empirical
  bound on `Γ_P` remains blocked on a governed auxiliary series that has not been verified
  to exist; the envelope simulation itself is runnable without it, conditional on an
  assumed `Γ_P` and reported as such.
- **data_required:** *HAS* — the admission series, the fitted specification, the CHD/HF
  pair needed for a differential. *LACKS* — any non-hospital morbidity series, outpatient
  attendance as an outcome, sick-leave or labour data, sleep or blood-pressure series, and
  any observed policy switch.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-C2-08 The regime does not sit still: fading caution, ratcheted protocol, and the weights inside `θ̄`

- **paradigm_id:** HE-C2-08
- **mutates:** HE-08 (`SURVIVE-TO-ESCALATION` — report the regime transportability envelope, RTE)
- **mutation_axis:** A (dynamic time-inconsistency)
- **theoretical_space:** Non-stationary regime weights; Lucas critique with a decay rate
- **claim_type:** identification (a transportability bound, not an estimate)
- **economic_object:** The **half-life of the regime weight** — and the resulting statement
  that the pooled `θ̄` is an average over weights that were still moving at the end of the
  sample, so no month in the series is "regime-normal".
- **structural_sketch:** HE-08 wrote `θ̄ = Σ_R w_R θ_R` with weights the analyst does not
  choose, and proposed a pre-specified cross-regime test. The audit's surviving objection
  was that the real regime is continuous, endogenous, and correlated with extremes. The
  mutation takes that seriously and gives the regime a *dynamic*. Post-shock caution is not
  a state but a decaying quantity, and it decays at **two different rates**. Household
  caution `c_H,t` fades fast: under `(β, δ)`, salience-driven precaution is exactly the kind
  of delayed-benefit behaviour that a present-biased agent abandons as soon as the threat
  stops being vivid, so `c_H` falls steeply and then flattens rather than decaying
  exponentially. Institutional protocol `c_I,t` ratchets: triage rules, infection-control
  procedures, and referral pathways persist long after the households that prompted them
  have reverted, because changing a written procedure has its own cost. Write
  `R_t(ρ_H, ρ_I) = φ_H exp(−ρ_H (t − t_0)^+) + φ_I exp(−ρ_I (t − t_0)^+)` with
  `ρ_I < ρ_H` (`SYNTHETIC` structure). Two consequences follow that HE-08 did not contain.
  First, if `ρ_I` is small, the institutional component is still present in the final
  months, so a "pre-2020 versus post-2022" comparison is **not** a clean pre/post — the
  post period is a partially-treated period, and the RTE computed from a binary split is
  therefore biased toward invariance. Second, extrapolating `θ̄` to a future winter
  implicitly assumes either `ρ = ∞` (instant reversion, so the pandemic months are simply
  discardable) or `ρ = 0` (permanent change, so they are the new normal). Neither is
  defensible, and the honest object is a bound over the admissible `(ρ_H, ρ_I)` set rather
  than a point. Call it the **reversion-adjusted transport bound**,
  `RATB = max over admissible (ρ_H, ρ_I) of | β_transported(ρ) − β_pooled |`. Note the
  self-reference without dwelling on it: this project's own protocol ratchets — a frozen
  SAP, a claim ledger, a Stage 3 PDF lock — are the same phenomenon operating on the
  research process, and they are ratchets for good reasons.
- **why_not_already_explored:** P10 and P16 control for or exclude COVID; HE-08 asked
  whether the parameter is regime-specific; nothing has asked whether the regime *itself*
  has a time constant, which is the difference between a nuisance and a non-stationarity.
  **Anti-convergence guard:** a COVID dummy, an influence-month exclusion, or a pre-2020
  split is **not** this object. If the output is a robustness table showing that direction
  is unchanged, HE-C2-08 has collapsed into P10/P16 and must be discarded. The deliverable
  is an envelope with a stated identifiability failure, not a sensitivity check that passes.
- **identification_threats:**
  - One shock episode gives one decay curve. `ρ_H`, `ρ_I`, `φ_H`, `φ_I` and the onset date
    `t_0` are five quantities to be recovered from 132 months that already carry twelve
    month indicators and a four-degree-of-freedom trend spline.
  - `t_0` is genuinely ambiguous — January 2020, February 2020, or one of several later
    waves — and profiling over both `t_0` and `ρ` at this sample size is hopeless in a way
    that should be stated rather than hidden behind a fitted value.
  - The decay index is smooth and monotone after onset, so it competes directly with
    `ns(time, 4)` for the same variation.
  - Cold-day identification is concentrated in DJF and the influence leaders are both
    Februaries, so the months that carry the regime signal are the months that carry the
    coefficient.
  - Any household/institutional decomposition is an assumption about mechanism, not a
    measured split; the two components are not separately observed anywhere in these data.
- **what_would_kill_it:** A **profile-identifiability** Monte Carlo. Simulate counts on the
  real exposure path with a known two-rate decay index across a grid of `(ρ_H, ρ_I, t_0)`,
  fit the analysis of record interacted with `R_t(ρ)`, and profile the likelihood in `ρ`.
  Report the width of the 95% profile interval on the implied half-life. If that interval
  is effectively unbounded — the proposed pre-registered failure condition is that it
  covers everything from about three months to infinity — then `ρ` is not identified,
  the two-rate structure cannot be fitted, and the only admissible output is the RATB
  reported as an **envelope over the whole admissible `ρ` set**, with the binary-split RTE
  flagged as biased toward invariance. That envelope is the deliverable and it is a
  limitation, not a result. If instead the profile is informative, that would be
  surprising, and the correct response is to suspect the simulation before believing it.
- **data_required:** *HAS* — the full monthly series, real exposure, COVID phase
  indicators, influence diagnostics, the existing pre-2020 split. *LACKS* — an external
  utilisation series to calibrate caution, any measure of protocol persistence, more than
  one shock episode, and enough pandemic winters to estimate an interaction.
- **status_proposal:** candidate
- **provenance:** SYNTHETIC_THEORY

---

## HE-C2-10 Truncation composed with aggregation: a signed, possibly cancelling monthly distortion

- **paradigm_id:** HE-C2-10
- **mutates:** HE-10 (`SURVIVE-TO-ESCALATION` — report the aggregation distortion ratio, ADR)
- **mutation_axis:** A + B (capacity set by a present-biased manager; distortion evaluated at monthly scale)
- **theoretical_space:** Composition of two bias operators — index-number aggregation and capacity censoring
- **claim_type:** costing constraint (a projection-validity gate)
- **economic_object:** The **signed composite distortion** in the monthly coefficient when a
  concave daily truncation operator is applied before a nonlinear aggregation, and the
  **cancellation region** in which the two biases offset by coincidence rather than by design.
- **structural_sketch:** HE-10 took the true daily response `g(T_d)` and showed that
  `Σ_d g(T_d) ≈ n [ g(T̄) + ½ g''(T̄) s² ]`, so a monthly regression on `T̄` estimates a
  mixture of the slope and a curvature term weighted by the variance gradient
  `ς = ∂s² / ∂T̄`, which in a subtropical climate is expected to be negative. That is one
  operator. Axis B supplies a second: realised daily admissions are `min(D_d, K_d)`, a
  **concave** operator that bites hardest on the highest-demand days. The composition is
  the point. Truncation removes precisely the tail days that carry the convexity generating
  the Jensen term, so on the curvature channel the two operators act in **opposite**
  directions; on the slope channel, both attenuate the response at high load, so they act
  in the **same** direction. The composite sign is therefore not determined analytically.
  It depends on four things: the curvature class of `g`; the variance gradient `ς`, which
  is a property of the real daily HKO series and is measurable today without any governed
  health data; the utilisation level `K / E[D]`; and — critically — whether `K` is itself
  seasonal. If the Authority plans winter surge capacity, then `K_d` is correlated with the
  exposure whose coefficient is being estimated, and the truncation operator's bite is
  season-dependent. That opens the sharpest consequence in this document: **the distortion
  can differ in sign between the CHD hot-night contrast and the HF cold-day contrast**, so
  a single distortion statistic for the panel is not sufficient and one must be reported
  per contrast and per season. Under Axis A, `K` is set by a present-biased manager who
  under-provides capacity, which makes the truncation channel larger than a
  social-planner benchmark would suggest — the two axes multiply here rather than merely
  coexisting. The final new object is the **cancellation region**: the set of
  (curvature, `ς`, utilisation) combinations where the two biases offset to within
  tolerance. It matters because inside that region a *passing* distortion test is a
  coincidence of the calibration and not a property of the design, so the Cycle 1 pass
  criterion is unsafe wherever the region is non-trivial.
- **why_not_already_explored:** HE-10 evaluated one operator and reported the ADR in
  **absolute value**. The mutation is that once a second operator is present, the sign is
  the whole content: `|ADR|` cannot distinguish "no distortion" from "two distortions that
  happened to cancel". Nothing in the repository, and nothing in Cycle 1, composes the two.
  **Anti-convergence guard, stated twice because this object is closest to the cliff:**
  this never estimates, recovers, reports, or implies a daily coefficient. The M|D
  daily-recovery paradigm failed its 500-replicate calibration and is closed. HE-C2-10
  *imposes* a synthetic daily response and asks what the monthly estimator does to it; it
  never runs the arrow in the other direction. If any output is described as recovering a
  daily effect, it has collapsed into the failed M|D paradigm and must be discarded. It is
  also not a DLNM attributable-fraction costing: no attributable fraction is computed, and
  no fraction is multiplied by anything.
- **identification_threats:**
  - The true `g` is unknown, so every distortion figure is conditional on an imposed
    curvature class and is illustrative rather than definitive.
  - Extreme-count exposures — hot nights, cold days — are already tail statistics, so the
    Taylor argument in the monthly mean is not even the right object for them, and the two
    exposure families need separate treatment throughout.
  - `K_d` is unobserved and its seasonality is an assumption; the sign result is
    conditional on that assumption, which cannot be verified from these data.
  - Real within-month variance is itself trending across the window, so `ς` is not a
    constant and the distortion is not stationary.
  - Daily serial dependence violates the independence used in the simple variance
    argument, and weather is strongly autocorrelated.
  - The cancellation region is defined relative to a tolerance that must be pre-registered;
    choosing it after seeing results would make the whole exercise circular.
- **what_would_kill_it:** The highest-value simulation in this cycle, and it requires no
  governed health data at all. Build a full factorial Monte Carlo on the **real** daily HKO
  series: curvature class `g ∈ {linear, reversed-J with heat-tail convexity, threshold
  count}`; the real measured variance gradient `ς` plus perturbations of it; utilisation
  `K / E[D] ∈ {0.7, 0.85, 0.95, 1.05}` (`SYNTHETIC`); and capacity both flat and seasonal.
  Apply the three mandatory escalation stresses — MNAR deletion aimed at the months where
  the Jensen term is largest, a continuous macro shock correlated with both the daily
  exposure distribution and monthly admissions, and absorbing first events with a
  heat-dependent threshold — and add daily serial dependence as a fourth. Aggregate,
  fit the exact analysis of record, and report the **signed** composite statistic
  `CATD = [ β_month − β_target ] / (0.5 × CI_width_existing)`, with median and 5th/95th
  percentiles, **separately for each contrast and each exposure family**, together with
  the mapped extent of the cancellation region. The pre-registered pass condition is
  strictly harder than Cycle 1's: composition is cosmetic only if the 90% interval of
  signed `CATD` contains zero **and** has width below one **across the entire factorial**,
  with coverage maintained under every stress family. If the sign flips anywhere in the
  factorial, or if the cancellation region is non-trivial, then no monthly-coefficient
  scenario projection is admissible without stating the utilisation and curvature it
  assumes — and since utilisation is unobserved, the practical consequence is a
  **projection veto**, which is a cheap, self-contained, and genuinely useful result to
  have in hand before anyone proposes a costing.
- **data_required:** *HAS* — real daily HKO exposure, real monthly exposure, the exact
  fitted specification, the existing interval widths. `ς` is computable today from public
  climate data with no governance. *LACKS* — nothing for the simulation; the true `g`, real
  capacity, and real utilisation are unobservable and are supplied synthetically by
  construction, which is the reason the output is a bound and not an estimate.
- **status_proposal:** candidate — **highest simulation priority in Cycle 2**
- **provenance:** SYNTHETIC_THEORY

---

## HE-C2-PORT One request, not three: the cluster-level data ask as a portfolio

- **paradigm_id:** HE-C2-PORT
- **mutates:** HE-03 (`KILL`), HE-06 (`PARK-CONFIRMED`), HE-11 (`PARK-CONFIRMED`) jointly
- **mutation_axis:** B (supply side), with the governance cost structure from Axis A
- **theoretical_space:** Design of a data request as a portfolio with complementarities
- **claim_type:** VoI machinery applied to identification status, **not** to utility
- **economic_object:** The **identification-gain ledger** of a candidate data request, and
  whether its elements are complements — that is, whether any single element changes any
  parameter's identification status on its own, or only a bundle does.
- **structural_sketch:** Three Cycle 1 objects failed of the *same* cause. HE-03 needed
  capacity and occupancy; HE-06 needed cluster budgets and capital vintage; HE-11 needed a
  geography joined to housing and appliance ownership. In each case the fatal problem was
  that a single territory time series cannot separate stories that are observationally
  equivalent within it — capacity rationing, budget myopia, and household adaptation all
  produce a declining fitted trend and an attenuated hot-season coefficient, and none is
  distinguishable from the others or from spline misfit. A cross-section separates them
  *jointly*, because each hypothesis's confounder is another hypothesis's regressor. That
  is the definition of a complementarity, and it means the right unit of request is one
  bundle rather than three asks. The Cycle 1 audit killed EVPI, so no expected value may be
  computed here; the mutation is to use the machinery without the prior. Build a matrix
  whose rows are currently-unidentified parameters — the bed shadow price `λ`, the
  adaptation-capital wedge `Δ_β`, the household capital gradient `θ_h(K_h)`, the
  cluster-specific variance gradient `ς_c`, the public share `σ` — and whose columns are
  candidate data elements: cluster-level monthly counts, bed-day capacity and occupancy,
  elective cancellation counts, cluster capital and recurrent budgets, catchment housing
  mix, private inpatient volumes. Each cell records whether that element changes that
  parameter from "not identified" to "identified under stated assumptions". This is an
  analytic exercise in identification status, requiring no prior, no utility, and no
  assertion that any element exists. The governance cost is then an **integer**, not a
  currency: each request consumes one unit of finite human attention — the PI's, Roro's,
  the governance process's — and the design problem is to flip the most rows with the
  fewest requests, subject to a feasibility judgment that belongs entirely to humans. The
  expected structure is strict supermodularity: cluster counts alone flip nothing because
  the cluster-level covariates are what make them informative, occupancy alone flips
  nothing without counts to join it to, and the smallest useful bundle is probably a pair.
  The expected *result* is honest and partial: even the full bundle probably leaves `λ`
  unflipped, because capacity is endogenous to anticipated weather at cluster level exactly
  as it is at territory level.
- **why_not_already_explored:** The repository requests data hypothesis by hypothesis;
  Cycle 1 named the portfolio idea in its mutation seeds but did not construct the object.
  Treating identification status rather than expected utility as the currency is what makes
  it survivable after HE-04's kill. **Anti-convergence guard:** if any output attaches a
  number, a utility, or a probability to the value of a request, it has collapsed into the
  killed HE-04 and must be discarded. The output is a matrix of statuses and a bundle
  recommendation, and the decision to ask for anything at all is a human governance move
  that this document does not make.
- **identification_threats:**
  - Clusters are not randomly assigned. Capital vintage, catchment deprivation, and
    capacity all correlate with each other and with the population served, so a
    cross-section identifies these parameters only under stated and strong assumptions.
  - Capacity remains endogenous to anticipated weather within clusters, so `λ` may remain
    unidentified even under the full bundle. The ledger must record that as an expected
    outcome rather than discovering it late.
  - Small-cell suppression rules would apply to cluster-level counts and are unknown; a
    suppressed cross-section may be formally available and practically uninformative.
  - The identification-status entries are analyst judgements about what a design would
    support, and different analysts will fill some cells differently. The matrix must be
    written with its assumptions attached to each cell.
- **what_would_kill_it:** Construct the matrix and inspect its column structure.
  **(1)** If any single element flips any row on its own, the portfolio claim is false for
  that parameter and the correct move is a small, separate, cheap request — which would be
  a useful and immediate correction to the Cycle 1 seed. **(2)** If no single element flips
  any row but a bundle does, supermodularity holds and the deliverable is one governance
  ask with a written justification for its cardinality. **(3)** If even the full bundle
  leaves every row unflipped, then the entire cross-sectional programme is not a solution,
  HE-03, HE-06 and HE-11 stay dead permanently rather than parked hopefully, and three
  research strands are closed for the price of an afternoon's analysis. That third outcome
  is the most valuable one available here, and it is the reason to do this before any human
  spends governance capital.
  **This document does not assert that cluster-level counts, capacity records, budgets,
  housing linkages, or private volumes exist, are obtainable, or would be permitted.** It
  defines what would be asked for if a human opened that door, and nothing more.
- **data_required:** *HAS* — the identification arguments in Cycle 1 and in the audit, the
  fitted specification, the existing governance record. *LACKS* — everything in the column
  set, all of it unverified.
- **status_proposal:** candidate (analytic, runnable now, no data and no governance required)
- **provenance:** SYNTHETIC_THEORY

---

## Cycle 2 portfolio summary

| ID | Mutates | Axis | Claim type | Status | Runnable now without governed health data? |
|---|---|---|---|---|---|
| HE-C2-01 | HE-01 (`KILL`) | A | costing constraint | likely_fail | Yes — DGP-discrimination Monte Carlo |
| HE-C2-02 | HE-02 (`KILL`) | B | identification (detection) | candidate | Yes — moment-power Monte Carlo |
| HE-C2-04 | HE-04 (`KILL`) | A | governance structure | candidate | Yes — algebra and an audit; not an estimate |
| HE-C2-07 | HE-07 (survivor) | A + B | welfare (design veto) | candidate | Envelope yes; empirical bound blocked |
| HE-C2-08 | HE-08 (survivor) | A | identification (bound) | candidate | Yes — profile-identifiability Monte Carlo |
| HE-C2-10 | HE-10 (survivor) | A + B | costing constraint | candidate | Yes — **highest priority**, real HKO daily only |
| HE-C2-PORT | HE-03 + HE-06 + HE-11 | B | VoI machinery on status | candidate | Yes — analytic matrix, no data |

Six candidates and one likely_fail. Five of the seven are decidable with public climate
data and synthetic outcomes alone, which is the property that matters while the stroke file
and the person-time denominator are outstanding.

Recommended order, cheapest decisive test first: **HE-C2-PORT** (an afternoon, and it can
close three strands), **HE-C2-10** (the richest simulation and the only one whose failure
mode is a concrete projection veto), **HE-C2-02** (a genuinely new moment to look at),
**HE-C2-08** (expected to return "unidentified", which is itself the deliverable),
**HE-C2-07** (envelope only until an auxiliary series is verified), **HE-C2-04** (a memo,
human-owned), **HE-C2-01** (run only if a documented dead end is wanted).

## YAML-ready list for `paradigm_registry.yml`

Appending requires a human decision about file structure: the existing registry is keyed
`cycle: 1` at the top level, so this block either converts the registry to a multi-cycle
document or lands in a sibling file. The registry is left untouched here, because
promotion of any paradigm is a human nod under the Explore-mode rule in `AGENTS.md` §5.

```yaml
# Cycle 2 mutation block — for analysis_plan/health_econ/paradigm_registry.yml
# Source document: analysis_plan/health_econ/cycle2_mutations.md
# A mutation is a NEW object with a NEW kill test. No Cycle 1 verdict is overturned.
cycle: 2
date: 2026-08-14
mode: explore
provenance: SYNTHETIC_THEORY

scope_contract:
  inherits: cycle_1_scope_contract
  monetisation_permitted: false
  gate3: open
  stroke_file: not_delivered
  daily_coefficient: none_admitted_after_failed_MD_calibration

mutation_axes:
  A_dynamic_time_inconsistency:
    agents: [household, hospital_authority_manager, scholar_submission_clock]
    preferences: quasi_hyperbolic_beta_delta
    rule: beta_is_never_estimated_from_admission_counts
  B_supply_side_market_power:
    provider: single_public_authority_as_rationing_monopsonist
    constraint: binding_daily_capacity_with_elective_buffer_cancelled_first
    rule: no_price_markup_or_lerner_index_is_claimed

paradigms:
  - id: HE-C2-01
    title: Hotelling scarcity rent on a depleting first-event stock under present-biased prevention
    mutates: HE-01
    cycle1_verdict_unchanged: KILL
    axis: A
    space: exhaustible_resource_pricing_with_hyperbolic_extraction
    claim_type: costing_constraint
    status: likely_fail
    runnable_without_new_governed_data: true
    kill_test: dgp_discrimination_confusion_matrix_depletion_vs_adaptation_vs_spline_misfit
    one_line: >-
      The rent on a remaining unhospitalised member must grow along the optimal path, so a
      constant unit value is inconsistent with the observed depletion; the level stays
      unidentified and the residue is a veto on constant-price costing.

  - id: HE-C2-02
    title: Conversion as a queue-clearing rule, not a demand channel
    mutates: HE-02
    cycle1_verdict_unchanged: KILL
    axis: B
    space: rationed_allocation_with_endogenous_censoring_boundary
    claim_type: identification_detection
    status: candidate
    runnable_without_new_governed_data: true
    distinct_from: HE-03_bed_shadow_price_which_stays_killed
    kill_test: moment_power_dispersion_profile_demand_vs_queue_clearing_at_n132
    one_line: >-
      Under rationing the count is censored at an unobserved boundary, so the informative
      moment is the second, not the first; a positive coefficient means queue release and a
      null is compatible with a large absorbed need shock.

  - id: HE-C2-04
    title: Commitment technology, not option value — the prior-free reversal set
    mutates: HE-04
    cycle1_verdict_unchanged: KILL
    axis: A
    space: commitment_under_quasi_hyperbolic_preferences
    claim_type: governance_structure_not_an_economic_parameter
    status: candidate
    runnable_without_new_governed_data: true
    forbidden_output: [numeric_evpi, evsi, cost_of_delay_in_currency, real_option_volatility]
    kill_test: reversal_set_nonemptiness_plus_revocability_audit_written_observable_costly
    one_line: >-
      A preference reversal is a property of the payoff ordering and needs no prior, and a
      written rule is a commitment device only if it is written first, observable to a third
      party, and costly to revoke.

  - id: HE-C2-07
    title: Endogenous visibility when the severity threshold is a household investment
    mutates: HE-07
    cycle1_verdict_unchanged: SURVIVE-TO-ESCALATION
    axis: A_with_B
    space: reflexive_selection_policy_dependent_threshold
    claim_type: welfare_design_veto
    status: candidate
    runnable_without_new_governed_data: envelope_only
    not_a_nudge_hypothesis: true
    kill_test: sign_reversal_probability_under_prespecified_reflexivity_envelope_plus_normalised_DSEW
    one_line: >-
      Present-biased households under-invest in detection, so the admission threshold is a
      policy-responsive investment and a working policy can raise recorded admissions while
      lowering morbidity.

  - id: HE-C2-08
    title: Fading caution and ratcheted protocol — regime weights that never settle
    mutates: HE-08
    cycle1_verdict_unchanged: SURVIVE-TO-ESCALATION
    axis: A
    space: non_stationary_regime_weights_lucas_critique_with_decay
    claim_type: identification_bound
    status: candidate
    runnable_without_new_governed_data: true
    kill_test: profile_identifiability_of_decay_half_life_over_rho_and_onset_grid
    one_line: >-
      Household caution fades fast while institutional protocol ratchets, so the post-period
      is partially treated, a binary split is biased toward invariance, and the honest output
      is a transport envelope over the admissible decay set.

  - id: HE-C2-10
    title: Truncation composed with aggregation — a signed, possibly cancelling monthly distortion
    mutates: HE-10
    cycle1_verdict_unchanged: SURVIVE-TO-ESCALATION
    axis: A_and_B
    space: composition_of_capacity_censoring_and_index_number_aggregation
    claim_type: costing_constraint_projection_validity_gate
    status: candidate
    priority: highest_simulation_target_of_cycle_2
    runnable_without_new_governed_data: true
    never: recovers_or_reports_a_daily_coefficient
    distinct_from: [failed_MD_daily_recovery, dlnm_attributable_fraction_costing]
    kill_test: factorial_signed_CATD_by_contrast_and_season_plus_cancellation_region_mapping
    one_line: >-
      Daily top-truncation removes the tail curvature that generates the Jensen term, so the
      two biases oppose on curvature and agree on slope; the composite sign can differ
      between the hot-night and cold-day contrasts and an absolute-value statistic hides it.

  - id: HE-C2-PORT
    title: One request, not three — the cluster-level data ask as a portfolio
    mutates: [HE-03, HE-06, HE-11]
    cycle1_verdicts_unchanged: [KILL, PARK-CONFIRMED, PARK-CONFIRMED]
    axis: B
    space: data_request_design_with_complementarities
    claim_type: voi_machinery_on_identification_status_not_utility
    status: candidate
    runnable_without_new_governed_data: true
    asserts_data_exists: false
    kill_test: identification_status_matrix_single_column_flip_versus_bundle_supermodularity
    one_line: >-
      Three dead objects died of one absence, and each one's confounder is another's
      regressor, so the unit of request is a bundle priced in integer units of human
      governance attention rather than in utility.

failed_on_arrival_cycle2:
  - estimating_beta_present_bias_of_households_or_ha_from_monthly_counts
  - hyperbolic_rediscounting_of_a_cost_stream_that_does_not_exist
  - ha_as_profit_maximising_cartel_with_a_markup_or_lerner_index
  - bed_auction_or_queue_position_pricing
  - rust_style_dynamic_discrete_choice_of_household_care_seeking
  - estimating_the_hotelling_rent_level_ie_reviving_killed_HE01_under_a_new_label
  - markov_regime_switching_estimation_from_one_pandemic_episode
  - monopsony_wage_or_clinical_labour_market_estimation
  - real_options_valuation_of_waiting_with_an_assumed_volatility
  - treating_the_HE_C2_10_cancellation_region_as_evidence_of_validity
  - evaluating_a_heat_warning_policy_through_HE_C2_07_reflexivity
  - commitment_language_used_to_justify_moving_or_freezing_gate3
  - time_inconsistency_of_the_estimator_presented_as_an_economic_object

cycle3_mutation_seeds:
  stochastic_volatility_of_heat:
    - the variance gradient of HE-C2-10 is itself a stochastic process with clustering, so
      the aggregation distortion has a distribution rather than a value
    - the economic object becomes the price of exposure variance, not of its mean
  endogenous_diagnosis_timing:
    - the outcome is first hospitalisation after first diagnosis, so risk-set entry is a
      health-system output that may itself respond to exposure and to clinic capacity
    - ask whether the estimand is a well-defined contrast before asking what it is worth
  dual_agency_mechanism_design:
    - two principals with different loss functions govern different gates of one submission
      while the agent is present-biased; are the gates substitutes or complements
    - a frame about process design only, never a claim about any colleague's motives
  myopia_gradient_across_agents:
    - household, manager and scholar have different beta; ask whether adaptation aggregates
      weakest-link or best-shot across them
  knightian_ambiguity_rather_than_risk:
    - replace the factorial in HE-C2-10 with a max-min over the curvature and variance-
      gradient class, turning the cancellation region into a robust-decision problem
```

## Failed on arrival — Cycle 2 rejects

New rejections generated by the two mutation axes. These are additional to the seventeen
Cycle 1 rejects, all of which remain rejected. Logged so no later cycle re-walks them.

| Rejected mechanism | Why rejected |
|---|---|
| Estimating `β` for households or the Authority from monthly admission counts | A preference parameter is not in these data. Any "estimate" would return the simulation's own input, which the Cycle 1 audit already identified as passing by construction. |
| Re-discounting a cost stream with `(β, δ)` to produce a "behaviourally corrected" burden | There is no cost stream, and constructing one is monetisation, which is forbidden this cycle. The hyperbolic wrapper adds sophistication to a prohibited object. |
| Treating the Authority as a profit-maximising cartel and estimating a markup or Lerner index | There are no prices and no marginal costs; the point-of-service charge is a token administered fee. "Cartel" is an analytical device for rationing in this cycle and is never a pricing claim. |
| Auction or queue-position pricing for beds | No observed queue, no waiting-time series, no allocation microdata, and none is expected. |
| Rust-style dynamic discrete choice of household care-seeking | Requires individual state transitions and choice histories. The data are territory-month totals. |
| Estimating the Hotelling rent *level* under a new label | This is the killed HE-01 valuation with different vocabulary. HE-C2-01 is a sign and growth-condition object only, and its own expected verdict is failure. |
| Markov or Hamilton regime-switching estimation of the pandemic regime | One episode in 132 months. The transition matrix is not identified, and the method would import an appearance of rigour that the sample cannot support. |
| Monopsony wage or clinical labour-market estimation | No wage, employment, or staffing data exist in this project, and the outcome file has nothing to do with them. |
| Real-options valuation of waiting for the stroke file | Requires an assumed volatility, which is the same disease that killed HE-04's prior. An invented volatility is an invented prior wearing a finance costume. |
| Reading a null composite distortion inside the cancellation region as evidence of projection validity | The specific self-deception HE-C2-10 exists to expose. A cancelling pair of biases is a property of the calibration, not of the design. |
| Evaluating a heat-warning or outreach policy through HE-C2-07's reflexivity | No policy switch is observed; this would resurrect both the rejected nudge paradigm and the rejected territory-wide difference-in-differences at once. |
| Using commitment-device language to justify moving, freezing, or pre-empting Gate 3 | Gate 3 is a team decision owned by the PI and co-authors. An Explore-mode cycle may model commitment abstractly and may not touch the gate. |
| Presenting time-inconsistency of the *analyst* as an economic result | Adaptive stopping and specification drift are research-conduct matters for pre-specification and governance, not economic objects. |

## Anti-convergence guards for Cycle 2

Each mutation has a specific way of collapsing back into something already rejected. The
guard is stated with the object; they are gathered here so a later reader can check the
whole set quickly.

- **HE-C2-01 → simple cost of illness with a trend.** If the output is "the coefficient
  survives a depletion-shaped trend", it is P10/P16 and it is discarded.
- **HE-C2-02 → the killed HE-03.** If any output reports a bed shadow price, a capacity
  figure, occupancy, or a cost, it has become HE-03 and is discarded. The permitted object
  is detection in the second moment, nothing else.
- **HE-C2-04 → a numeric EVPI.** Any number in currency, utils, or probability attached to
  the value of waiting is the killed HE-04 and is discarded.
- **HE-C2-07 → behavioural nudges.** The rejected paradigm is "messaging is the mechanism".
  The permitted claim is the reverse: that visibility-affecting policies make an
  admissions-based evaluation non-invariant. No message is proposed or evaluated.
- **HE-C2-08 → a COVID dummy.** A pre-2020 split or an influence-month exclusion is a
  robustness check, not a regime object. If the output is a table showing direction is
  unchanged, it is P10/P16 and is discarded.
- **HE-C2-10 → the failed M|D recovery, or a DLNM attributable fraction.** The daily
  response is *imposed*, never recovered, and no attributable fraction is computed or
  multiplied by anything. This is the closest object to the cliff edge in the document.
- **HE-C2-PORT → the killed HE-04.** Attaching a value, a utility, or a probability to a
  data request restores the prior problem. The permitted currency is identification status
  and an integer count of governance requests.

## Cycle 3 mutation seeds

The engine does not stop. Cycle 2 held the estimand fixed and mutated the environment;
Cycle 3 should mutate the estimand and the uncertainty class.

**Stochastic volatility of heat.** HE-C2-10 treats the within-month variance gradient `ς`
as a fixed feature of the climate. It is not: daily temperature variance clusters, trends,
and responds to the same circulation patterns that set the mean. If `ς` is a stochastic
process, then the aggregation distortion is a *distribution* rather than a value, and the
economic object shifts from the mean of exposure to the **price of exposure variance** — a
quantity that connects directly to why a warm month with three extreme days is not a warm
month. This also feeds back into HE-C2-08, because volatility clustering and regime decay
are hard to tell apart at monthly resolution.

**Endogenous diagnosis timing.** The most consequential unexamined assumption in the whole
project is that entry into the risk set is exogenous. The outcome is *first hospitalisation
after first diagnosis*, and the diagnosis date is itself a health-system output: it depends
on clinic attendance, screening capacity, and a household's willingness to be told. Under
present bias, people defer the appointment at which they would be diagnosed, and that
deferral is plausibly weather-sensitive. If exposure moves risk-set entry as well as the
event, the estimand is a composite of two timings, and Cycle 3 should ask whether it is a
well-defined contrast **before** asking what it is worth. This seed touches every object in
both cycles and is the strongest candidate for the next round.

**Dual agency as mechanism design.** Two gates govern one submission: the weather-definition
lock and the team's Gate 3. They are held by different people with different loss functions,
and the agent between them has a submission clock. The formal object is a two-principal,
one-agent common-agency game, and the question is whether the two gates are substitutes or
complements as commitment technology — whether having both makes the process more robust or
merely slower. **This is a frame about process design and must never become a claim about
any colleague's motives or intentions.** The interpersonal rule in `AGENTS.md` §6 governs
anything written under this seed.

**The myopia gradient.** Cycle 2 gives household, manager and scholar the same functional
form and different parameters. Cycle 3 should ask how adaptation aggregates across them:
weakest-link, in which the most myopic agent determines the outcome, or best-shot, in which
one far-sighted agent rescues it. The two aggregators imply opposite policy targets and are
distinguishable in theory long before any data exist.

**Knightian ambiguity instead of risk.** HE-C2-10 runs a factorial over curvature classes
and utilisation levels and takes quantiles, which treats the unknown structure as risk.
It is closer to ambiguity: nobody has a probability distribution over the true daily
response. Replacing the factorial quantile with a max–min over the admissible class turns
the cancellation-region problem into a robust-decision problem and yields a bound that does
not depend on a made-up weighting of the scenarios.

## What Cycle 2 does not license

- No monetisation of any coefficient, and no cost, price, or currency quantity anywhere.
  `monetisation_permitted: false`.
- No claim that any Cycle 1 `KILL` has been overturned. HE-01, HE-02, HE-03, HE-04, HE-05,
  HE-09 and HE-12 remain killed as formulated; HE-06 and HE-11 remain park-confirmed.
- No stroke economics, no stroke coefficient, no stroke row count, and no statement about
  what the undelivered stroke file contains.
- No daily coefficient, no recovery of a daily response, and no attributable fraction.
- No input to Gate 3, no advancement or delay of it, and no use of commitment language to
  influence it.
- No assertion that cluster-level counts, capacity records, budgets, private volumes,
  outpatient series, or housing linkages exist, are obtainable, or would be permitted.
- No new pathway ID, registry promotion, or SAP amendment. These are hypotheses, and
  promotion requires a human nod under the Explore-mode rule in `AGENTS.md` §5.
- No estimate of `β` for any agent, including the scholar, from any admission count.
