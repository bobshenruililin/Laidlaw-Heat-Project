# The missing denominator is the finding

**Post-audit (14 Aug):** SURVIVES-IN-REDUCED-FORM. `A48` as identification and the person-time falsifier stand. “Primarily an artifact,” the 0.109 common-amplitude inversion, and the blanket ban on the word “null” are eliminated. See `knowledge/crucible_adversarial_audit.md` and `reports/identification_crucible_2026-08-14.md`.


**Agent Beta · identification crucible · 14 August 2026 · Mode: Explore**
**Constraints:** no new health model, no governed monthly count read, no HA
microdata, no web search.
**Sibling positions:** `crucible_agent_alpha_aggregation.md` (aggregation
grain), `crucible_agent_gamma_overcontrol.md` (calendar-month overcontrol),
`crucible_agent_delta_decision_rule.md` (multiplicity). This memo argues none of
those three. Its subject is the denominator, and it contests Alpha and Delta on
one point only: whether attenuation toward \(1\) may be read as absence.

## 1. Thesis

The apparent null in the CHD/HF panel — all twelve core \(q>0.19\), count
ratios within a few percent of \(1\) — is primarily an artifact of an absorbing
first-event risk set whose size and composition are omitted from the mean
function, not evidence that thermal association is absent. Without the monthly
still-at-risk T2D/HTN denominator, the residual count ratio has no fixed target:
its sign and magnitude depend on how the depleting trend is represented, on
which months are retained, and on unmeasured pandemic care-seeking. Gate 3 may
therefore freeze Option A as a **reporting rule** — no confirmatory primary —
but must not freeze it as a **scientific conclusion**. The honest freeze is
*estimand incomplete*. Roro's monthly cohort person-time is the falsifier.

Two licensed moves follow. Do not interpret residual count ratios as incidence.
Do not treat attenuation toward \(1\) as a null finding.

## 2. Provenance and paid facts

1. `[HA_APPROVED_AGGREGATE]` The outcome is the territory-month count of the
   first recorded hospitalisation after a first CHD or HF diagnosis among people
   diagnosed with T2D and/or HTN during 2013–2023. Admission cause is absent.
   Once a person has the event, that person leaves the risk set permanently.
2. `[HA_APPROVED_AGGREGATE]` Annual first-event totals
   (`cvd_descriptive_annual_totals.csv`): CHD \(23{,}830\) (2013), \(12{,}396\)
   (2019), \(10{,}237\) (2020), \(12{,}323\) (2023); HF \(4{,}336\),
   \(2{,}344\), \(1{,}964\), \(2{,}296\). Combined 2013:2023 ratio \(1.927\).
   `[REAL C&SD]` The broad population aged \(35+\) rose from \(4.43\)M to
   \(5.19\)M across the same window.
3. `[A48]` The main analysis offsets \(\log(\text{days in month})\), not cohort
   person-time. `[HA_APPROVED_AGGREGATE]` C&SD population \(\times\) days and no
   offset are sensitivities. Neither is the T2D/HTN risk set.
4. `[REAL]` Hot nights rose \(10\) (2013) \(\to 61\) (2021) \(\to 56\) (2023);
   very hot days \(17\to54\). Cold days did not trend: \(14, 21, 7, 21, 9, 21,
   1, 11, 13, 13, 14\).
5. `[REAL]` After calendar-month indicators and \(ns(\text{time},4)\), residual
   SD is \(1.73\) cold days, \(2.70\) hot nights, and \(0.90^\circ\)C of mean
   temperature. Cold days total \(145\), \(97.2\%\) in DJF, \(29\) nonzero
   months.
6. Local labels: `[REAL]` public HKO climate or C&SD population;
   `[HA_APPROVED_AGGREGATE]` approved totals and released coefficients;
   `[DESIGN_DERIVED]` algebra on those artifacts; `[ILLUSTRATIVE_ALGEBRA]` a
   monotone shape used only to evaluate a projection, asserting no cohort size,
   inflow rate, HA row count, or field meaning.
7. No new health model was fitted for this memo. No governed monthly count was
   read. Rebuild: `python3 scripts/49_depletion_crucible.py` then
   `python3 scripts/test_49_depletion_crucible.py`.

## 3. The absorbing-state counting process

1. Let person \(i\) enter the risk set at first T2D/HTN diagnosis and let
   \(T_i\) be the calendar time of the first CHD (or HF) hospitalisation. Define
   the at-risk indicator \(N_i(u)=\mathbf 1\{\text{entered by }u,\ T_i\ge u\}\).
   `[DESIGN_DERIVED]` The state is absorbing: \(N_i(u)=0\) for all \(u>T_i\).
2. Give person \(i\) the multiplicative daily intensity

   \[
   \lambda_i(u)=N_i(u)\,\alpha_i\,
   \exp\!\big(s(u)+f(u)+\beta x(u)\big),
   \]

   with \(\alpha_i>0\) an individual frailty, \(s\) a seasonal term, \(f\) a
   secular term, and \(x\) the thermal exposure.
3. Aggregating to month \(t\) with \(D_t\) days,

   \[
   \mathbb E[Y_t\mid \mathcal F]=\int_{t}\sum_i\lambda_i(u)\,du
   \;\approx\;
   D_t\,R_t\,\bar\alpha_t\,\exp\!\big(s_{m(t)}+f(t)+\beta x_t\big),
   \]

   where \(R_t=\frac{1}{D_t}\int_t\sum_iN_i(u)\,du\) is the mean number still at
   risk and \(\bar\alpha_t=\mathbb E[\alpha_i\mid N_i=1 \text{ in } t]\) is the
   frailty of the survivors. On the log scale,

   \[
   \log\mathbb E[Y_t]
   =\underbrace{\log D_t}_{\text{offset used}}
   +\underbrace{\log R_t+\log\bar\alpha_t}_{\text{omitted}}
   +s_{m(t)}+f(t)+\beta x_t .
   \tag{3.1}
   \]

4. `[DESIGN_DERIVED]` The fitted model supplies \(\log D_t\), calendar-month
   indicators, and \(ns(\text{time},4)\). It supplies nothing for
   \(g_t\equiv\log R_t+\log\bar\alpha_t\). Write \(C\) for the control matrix and
   \(\tilde v=v-C(C^\top C)^{-1}C^\top v\) for the residual of any series.
   The exposure coefficient then converges not to \(\beta\) but to

   \[
   \hat\beta\;\to\;\beta+
   \frac{\operatorname{Cov}(\tilde x,\tilde g)}{\operatorname{Var}(\tilde x)} .
   \tag{3.2}
   \]

   This is the confounding claim in one line: with \(R_t\) omitted and only
   \(D_t\) offset, the coefficient is the thermal association **plus** whatever
   of the risk-set path is correlated with residual weather.
5. `[DESIGN_DERIVED]` The offset choice is not cosmetic. Equation (3.1) says the
   correct exposure is \(D_tR_t\), i.e. person-time. Offsetting \(D_t\) alone
   imposes \(R_t\) constant and forces every movement of the risk set to be
   represented by the seasonal and secular controls, which were specified for
   climate and secular medicine, not for a denominator.
6. `[DESIGN_DERIVED]` Absorption also moves \(\bar\alpha_t\). In any mixed-hazard
   model, conditioning on not yet having had the event selects lower frailty:
   \(\partial_t\mathbb E[\alpha\mid T>t]\le0\) with equality only under
   degenerate \(\alpha\). If thermal susceptibility is a component of
   \(\alpha\) — the ordinary assumption behind susceptible subpopulations — then
   the true slope itself declines along the depletion gradient,
   \(\beta_t=\beta_0+\delta\,d_t\) with \(\delta<0\) and \(d_t\) cumulative
   depletion. This is cohort selection over eleven years. It is **not** daily
   mortality displacement or harvesting, which this design cannot address at
   all.
7. `[DESIGN_DERIVED]` A single fitted \(\beta\) then returns a weighted average.
   Using the Fisher weight \(Q_t=\theta\mu_t/(\theta+\mu_t)\) of the NB2 score
   (the object named in Alpha §3.4),

   \[
   \hat\beta\;\to\;
   \frac{\sum_tQ_t\tilde x_t^2\,\beta_t}{\sum_tQ_t\tilde x_t^2},
   \qquad Q_t \text{ increasing in } \mu_t \propto R_t .
   \tag{3.3}
   \]

   Fat-risk-set months carry more weight. `[HA_APPROVED_AGGREGATE]` The mean
   monthly approved count in 2013 is \(1.93\) times that of 2023 for CHD and
   \(1.89\) times for HF, so the early window carries roughly twice the weight
   per month of the late window.
8. `[DESIGN_DERIVED]` Equations (3.2) and (3.3) are different failures.
   (3.2) is bias from an omitted level. (3.3) is a target that shifts with the
   composition of the estimation window. A spline can address the first. Nothing
   in the current mean function addresses the second.
9. `[DESIGN_DERIVED]` The naming consequence is exact. \(\exp(\beta)\) equals an
   incidence-rate ratio only if \(\tilde R\perp\tilde x\). That is a testable
   orthogonality condition, and it is currently untested because \(R_t\) does not
   exist in the repository. "Count ratio, not incidence" is therefore an
   identification statement, not a labelling courtesy.

## 4. Why \(ns(\text{time},4)\) does not repair this

1. **Concession first.** A \(4\)-df spline absorbs a *smooth* depletion path
   almost perfectly. `[ILLUSTRATIVE_ALGEBRA]` Normalising four monotone shapes
   to the constant-hazard reading of the observed halving
   (\(\Delta\log=0.656\)), the share of the path removed by month effects plus
   \(ns(\text{time},4)\) is \(1.0000\) for a linear path — the spline's first
   column is linear, so this is by construction — \(0.9998\) front-loaded, and
   \(0.9999\) for a closed-pool accounting shape. The resulting additive bias in
   (3.2) is negligible: every reporting-step multiplier lies within \(0.002\) of
   \(1\). Alpha's "the spline absorbs most of this" is correct for this channel,
   and this memo does not rest on it.
2. **First failure: the path is not smooth.** `[ILLUSTRATIVE_ALGEBRA]` Add a
   non-smooth care-seeking dip of \(0.10\) log-units in February–May 2020 and
   February–May 2022. Month effects plus \(ns(\text{time},4)\) remove only
   \(24.4\%\) of it; \(75.6\%\) survives. Because (3.2) is linear in the path,
   the surviving component transfers a fixed amount per \(0.10\) log-units of
   dip: \(+0.00750\) to hot nights per \(5\) days (\(\times1.0075\)),
   \(-0.00423\) to cold days per \(5\) days (\(\times0.9958\)), and
   \(+0.00358\) per \(^\circ\)C of mean temperature. Heat is pushed up and cold
   is pushed down by the same shock.
3. `[HA_APPROVED_AGGREGATE + ILLUSTRATIVE_ALGEBRA]` That transfer can be closed
   against a paid coefficient. Inverting the released `covid_phase_adjusted`
   shift through the transfer coefficients recovers a latent dip amplitude of
   \(0.109, 0.112, 0.100, 0.113, 0.111\) log-units from CHD mean temperature,
   mean Tmax, mean Tmin, hot nights, and very hot days respectively: mean
   \(0.1089\), SD \(0.0053\), from transfer coefficients that themselves differ
   by a factor of \(2.9\). Five contrasts with different sensitivities recover
   one common amplitude of about a \(10\%\) count shortfall. That coherence is
   what a single omitted non-smooth risk-set factor predicts and what five
   independent thermal effects would not produce. `[HA_APPROVED_AGGREGATE]` The
   influence diagnostics agree on where it sits: 2020-02 and 2022-02 dominate
   Cook's distance for both outcomes.
   The two exceptions are the cold-day contrasts, and they cut the right way for
   this memo rather than against it. CHD cold days inverts to \(-0.096\), the
   wrong sign, and HF cold days to only \(0.020\). Cold-day burden is the one
   exposure whose identifying variance sits mostly in the fat pre-pandemic
   window (§5.4), so it is the contrast least exposed to a 2020/2022 shock.
   `[DESIGN_DERIVED]` A common latent factor should be recoverable from the
   contrasts that overlap it and not from the one that does not.
4. **Second failure: the interaction is never absorbed.** `[DESIGN_DERIVED]`
   \(ns(\text{time},4)\) spans functions of \(t\). A slope that varies along the
   depletion gradient contributes \(\delta\,d_t x_t\), a *product*, which lies
   in that span only if \(x_t\) does. `[ILLUSTRATIVE_ALGEBRA]` Regressing the
   front-loaded path times residual cold days on the same controls leaves
   \(83.1\%\) of its variance; times residual hot nights, \(93.7\%\); the raw
   product form leaves \(52.4\%\) and \(32.8\%\). The contrast is the whole
   argument: the control space removes \(99.98\%\) of the depletion path and
   \(16.9\%\) of that path multiplied by the cold-day anomaly.
5. **Third failure: depletion and the heat trend run in opposite directions over
   the same eleven years.** `[REAL × HA_APPROVED_AGGREGATE]` At annual
   resolution the correlation between exposure and approved CHD event totals is
   \(-0.818\) for hot nights (\(-0.811\) against log events), \(-0.781\) for very
   hot days, and \(-0.765\) for mean Tmax, but \(+0.205\) for cold days. Every
   trending heat metric is roughly \(0.8\) collinear with the depleting count
   series; the one non-trending exposure is not. Whatever the spline does with
   the secular component, it is doing it to a series that is nearly collinear
   with heat and nearly orthogonal to cold.
6. **Fourth failure: the coefficient is a function of the trend control.**
   `[HA_APPROVED_AGGREGATE]` Holding exposure, months, and offset fixed and
   varying only the secular control across `ns3`, `ns4`, `ns6`, `ns8`, and year
   fixed effects, CHD hot nights per \(5\) ranges \(1.0109\) to \(1.0246\) with
   \(p\) from \(0.315\) to \(0.0144\). The spread is \(63\%\) of the baseline
   \(\log\) RR. Six of the twelve core contrasts have a spread that exceeds
   their own point estimate. A quantity that moves this much when only the
   depletion proxy changes is not a measurement of the atmosphere.
7. `[DESIGN_DERIVED]` Two independently defined criteria select exactly the same
   four contrasts out of twelve: spread under \(30\%\) of the point estimate
   across trend controls, and a perfect rank association between window
   risk-set fatness and \(|\log \text{RR}|\) (§5.1). Both sets are
   \(\{\)HF mean temp, HF mean Tmax, HF mean Tmin, HF cold days\(\}\). One
   arbitrary \(4\)-subset of \(12\) matching another has chance \(1/495\); the
   contrasts are correlated so this is coherence, not a test. Robustness to the
   depletion proxy and sensitivity to the risk set are tracking the same latent
   object.

## 5. Sample composition, not residual weather, moves the coefficient

1. `[HA_APPROVED_AGGREGATE]` Place each already-paid window scenario against the
   mean monthly approved count of the months it uses — a risk-set fatness axis:

   | Scenario | Months | Mean monthly HF events | HF cold days /5 | \(p\) (NW6) |
   |---|---:|---:|---|---:|
   | Drop first 24 months | 108 | 200.6 | 1.043 (0.965–1.127) | 0.288 |
   | Drop first 12 months | 120 | 211.2 | 1.067 (0.995–1.143) | 0.069 |
   | Full window | 132 | 224.9 | 1.073 (1.006–1.144) | 0.031 |
   | Pre-COVID | 84 | 252.0 | 1.113 (1.053–1.176) | 0.000148 |

   The two coordinates increase together without exception; the rank
   correlation is \(+1.000\). Across all twelve core contrasts, seven have a
   rank correlation of at least \(0.8\) between fatness and \(|\log\text{RR}|\),
   three are negative, and the mean is \(+0.483\). The twelve share one climate
   series, so this is a description, not a test.
2. `[HA_APPROVED_AGGREGATE]` The pre-COVID window is the decisive case because
   it moves the wrong way for a power story. It uses \(84\) of \(132\) months
   and \(71.3\%\) of HF events, yet HF mean temperature goes from
   \(0.974\) (\(p=0.069\)) to \(0.9446\) (\(0.9269\)–\(0.9626\),
   \(p=3.3\times10^{-9}\)), HF mean Tmin from \(0.973\) (\(p=0.050\)) to
   \(0.9439\) (\(p=5.5\times10^{-10}\)), and HF cold days from \(1.073\)
   (\(p=0.031\)) to \(1.113\) (\(p=1.5\times10^{-4}\)). `[DESIGN_DERIVED]`
   Discarding a third of the months cannot systematically enlarge an effect and
   reduce \(p\) by seven orders of magnitude under a homogeneous slope with
   sampling noise only. Either the slope differs by risk-set regime, or the
   excluded months contribute variance unrelated to weather. Both are
   composition. Neither is absence of association.
3. `[HA_APPROVED_AGGREGATE]` The same axis read from the other end. Dropping the
   first \(24\) months removes \(18\%\) of the months but \(27.0\%\) of HF
   events — the fattest part of the risk set — and HF cold days falls to
   \(1.043\) (\(0.965\)–\(1.127\), \(p=0.288\)). Retaining only the fat early
   window strengthens the estimate; deleting the fat early window weakens it.
   These are two independent cuts of one composition axis moving the same way.
4. `[REAL × HA_APPROVED_AGGREGATE]` Weighting makes the asymmetry sharper than
   raw month counts suggest. Weighting residual exposure variance by the
   approved-count scale that drives \(Q_t\), the 2013–2018 share of identifying
   information is \(63.2\%\) for cold days against HF but \(49.9\%\) for hot
   nights against CHD. For cold days, count weighting raises the early share
   above the unweighted \(55.3\%\); for hot nights it does not.
5. `[REAL]` The counter-case is CHD hot nights, and it must be stated. Its
   fatness rank correlation is \(-0.2\), and pre-COVID it attenuates to
   \(1.011\) (\(0.991\)–\(1.032\), \(p=0.289\)). The reason is support
   migration: hot-night burden is concentrated in the depleted era. The
   \(48\) months after 2019 are \(36.4\%\) of the panel but hold \(52.7\%\) of
   residual hot-night variance, a \(1.45\)-fold over-concentration, whereas cold
   days hold \(34.3\%\), a factor of \(0.94\). Restricting to pre-COVID removes
   more than half the hot-night identifying variance, so the weight channel and
   the support channel pull in opposite directions for heat.
6. `[DESIGN_DERIVED]` The conclusion from §5.5 is not that heat is null. It is
   that no subsample of these \(132\) months estimates a stable heat
   coefficient, because the design cannot separate the depletion gradient from
   the climate trend. That is a statement about the panel, not about the
   cardiovascular system.

## 6. Counterexamples to "depletion is already absorbed by the spline"

1. **"\(ns(\text{time},4)\) removes the depletion."** It removes \(99.98\%\) of
   a *smooth* path (§4.1) and \(24.4\%\) of a pandemic kink (§4.2). Absorption
   is a property of the assumed shape. The observed series is not smooth: the
   CHD total falls \(25.5\%\) in the first year and then by single-digit
   percentages, and `[HA_APPROVED_AGGREGATE]` two pandemic months dominate the
   influence diagnostics for both outcomes.
2. **"Absorbing the level is enough."** It is not, because a depletion-varying
   slope enters as a product. \(83\%\) to \(94\%\) of the interaction survives
   the full control space (§4.4). Additive control cannot remove a
   multiplicative term.
3. **"If the trend control mattered, we would see it."** It is visible.
   Changing only the trend control moves CHD hot nights across \(1.0109\) to
   \(1.0246\) and \(p\) across \(0.315\) to \(0.0144\), and exceeds the point
   estimate in six of twelve contrasts (§4.6).
4. **"We tested the offset and it did not matter."** `[HA_APPROVED_AGGREGATE]`
   `cvd_offset_sensitivity_wide.csv` gives CHD hot nights \(1.022/1.021/1.022\)
   and HF cold days \(1.073/1.073/1.075\) across days-only, population \(\times\)
   days, and no offset. `[DESIGN_DERIVED]` That inertness measures the
   smoothness of the *wrong* denominator: C&SD population aged \(35+\) is a
   near-linear series and is therefore nearly collinear with
   \(ns(\text{time},4)\), so substituting it changes almost nothing. An
   inert wrong denominator is not evidence that the right denominator is inert.
   `[HA_APPROVED_AGGREGATE + REAL]` The counted first-event pool falls by a
   factor of \(1.93\) while the C&SD series rises \(17.1\%\), in the opposite
   direction. Whether the risk set itself moves that way is §7.4, and it is
   exactly what the offset sensitivity does not test.
5. **"A perfectly absorbed \(\log R_t\) would settle it."** It would settle
   (3.2) and not (3.3), and it would still leave \(\exp(\beta)\) a count ratio.
   Incidence requires the denominator in the model, not partialled out of it
   (§3.9).
6. **"Absorption makes the estimate stable, so it is trustworthy."**
   `[DESIGN_DERIVED]` Absorbing \(\log\bar\alpha_t\) into a smooth trend hides a
   drifting target rather than removing a nuisance. Stability under a control
   that also removes the estimand's own heterogeneity is not evidence of
   validity.
7. **"Depletion is real but small."** `[HA_APPROVED_AGGREGATE]` The counts
   halve. `[DESIGN_DERIVED]` For the additive channel the relevant magnitude is
   not the total decline but the non-smooth residual, which the paid
   `covid_phase_adjusted` shift implies is about \(0.11\) log-units and which
   accounts for \(0.0075\) of the \(0.0216\) baseline CHD hot-night \(\log\) RR
   — roughly a third of the point estimate from one omitted care-seeking
   component alone.

## 7. Falsification: the Roro file that would kill this thesis

1. The falsifier is a monthly still-at-risk person-time series for the
   diagnosed cohort, delivered as an approved aggregate. Minimum fields per
   month, separately for the CHD-free and HF-free risk sets because the two
   absorbing states differ: persons at risk at month start; person-days at risk
   within the month; entries from new T2D/HTN diagnosis; exits split by first
   event, death, and other censoring. An age-band breakdown would additionally
   make \(\bar\alpha_t\) drift partly observable and is the natural vehicle for
   Hogan's 65–69 / 70–74 visibility proposal.
2. **Kill condition one.** Refit the core panel with \(\log(\text{person-time})\)
   as the offset. If HF cold days stays near \(1.073\) with comparable
   uncertainty *and* the fatness ladder in §5.1 collapses — that is, the
   pre-COVID, full-window, and drop-24 estimates converge — then the days offset
   was adequate, the ladder was weather and noise, and this memo is wrong.
3. **Kill condition two.** Compute
   \(\operatorname{Corr}(\tilde{\log R},\tilde x)\) after month effects and
   \(ns(\text{time},4)\). If it is near zero for cold days and for hot nights,
   the bias term in (3.2) is empirically absent and §4.2–§4.5 lose their
   mechanism.
4. **Kill condition three, and the most likely way this memo is wrong.** If
   accumulating new T2D/HTN diagnoses roughly balance first-event exits, monthly
   person-time may be flat or rising rather than depleting. Then the halving of
   counts is a falling hazard, not a falling denominator, the sign of the bias in
   (3.2) reverses, and Option A regains footing as a statement about hazard.
   This possibility is the reason the load-bearing claim of §1 is that the bias
   cannot currently be *signed*, which is a stronger and more defensible
   statement than any particular direction.
5. **Kill condition four.** If a person-time-offset model reproduces attenuation
   toward \(1\) *within* the fat pre-COVID window, then attenuation is not
   compositional there either, and the residual estimand is closer to a genuine
   near-null than argued here.
6. **What would not falsify it.** A monthly stroke file; a larger or smoother
   general-population offset; more spline degrees of freedom; a different
   standard-error method; a longer calendar window that continues to omit
   \(R_t\). None supplies the denominator. `[HA_APPROVED_AGGREGATE]` The first
   three are already shown to be beside the point: the general-population offset
   is inert (§6.4), extra spline degrees of freedom move the coefficient without
   stabilising it (§4.6), and no standard-error method changes a point estimate.

## 8. Gate 3 consequence

1. Separate the two things Option A is being asked to do. As a **reporting
   rule** — no confirmatory primary contrast, panel reporting by pathway ID, no
   headline — Option A is correct and this memo does not contest it. As a
   **scientific conclusion** — "no association", "null", "no evidence of a
   thermal effect" — Option A is unlicensed, because it reads a coefficient
   whose target is undefined without \(R_t\) as though its target were zero.
2. The freeze this memo supports is *estimand incomplete pending cohort
   person-time*, recorded as an amendment to `A48` rather than as a new gate.
   Operationally: report the count ratios as count ratios with their windows;
   state that neither the magnitude nor the sign of the risk-set bias is
   currently estimable; report the fatness ladder in §5.1 as a limitation rather
   than as robustness; and do not write "null", "no association", or "no
   evidence of an effect" anywhere in the manuscript.
3. `[DESIGN_DERIVED]` The asymmetry in §4.7 gives the team a concrete drafting
   rule. The four HF contrasts that are stable under trend controls and
   monotone in risk-set fatness may be described as coherent residual
   associations under a stated incomplete estimand. The remaining eight,
   including CHD hot nights, should be described as not identified at this
   grain.

## 9. What must not be claimed on the basis of this memo

No HA row count, cohort size, inflow rate, ICD list, admission meaning, or
stroke result is supplied or implied here; the illustrative depletion paths are
projection devices and assert none of these. This memo produces no corrected
coefficient, no incidence rate, no attributable fraction, and no person-time
denominator; the amplitude inversion in §4.3 returns a care-seeking amplitude
implied by a released coefficient shift, not a repaired estimate. Nothing here
supports daily triggering, harvesting or mortality displacement, an individual
causal contrast, a principal-diagnosis or AMI claim, or a CHD-heat versus
HF-cold mechanism. Frailty selection is asserted only as a property of mixed
hazards over eleven cohort years, not as a measured biological finding. The
depletion premise itself remains unverified until §7.1 arrives.

## 10. In-repo proof sources

1. `outputs/depletion_crucible/depletion_summary.json`
2. `outputs/depletion_crucible/depletion_path_absorption.csv`
3. `outputs/depletion_crucible/interaction_absorption.csv`
4. `outputs/depletion_crucible/omitted_logr_bias.csv`
5. `outputs/depletion_crucible/covid_kink_amplitude_inversion.csv`
6. `outputs/depletion_crucible/riskset_fatness_ladder.csv` and
   `riskset_fatness_ladder_stats.csv`
7. `outputs/depletion_crucible/time_control_sensitivity.csv`
8. `outputs/depletion_crucible/count_weighted_information.csv`
9. `outputs/depletion_crucible/annual_trend_collinearity.csv`
10. `outputs/tables/cvd_trend_depletion_sensitivity.csv`,
    `cvd_descriptive_annual_totals.csv`, `cvd_offset_sensitivity_wide.csv`
11. `outputs/identification_crucible/exposure_residual_variation.csv`
12. `knowledge/2026-08-12_existing_data_insights.md` §1 and §8
13. `analysis_plan/assumption_ledger.md` (`A48`)
14. `scripts/49_depletion_crucible.py`, `scripts/test_49_depletion_crucible.py`
