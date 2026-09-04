# Adversarial audit of the four crucible theses

**Date:** 14 August 2026
**Mode:** Decide (adversarial audit; no new health model; no governed monthly count read; no HA microdata; no web search)
**Branch:** `cursor/identification-crucible-1fd0`
**Not touched:** Hogan weather prose, Stage 3 PDFs, live paste files. **Gate 3 is not closed here.**

**Standing instruction obeyed:** a thesis is eliminated only on a concrete counterexample or a fatal logical flaw. Where an attack failed, it is recorded as failed in §5 rather than softened into a shared point.

**Rebuild:** `python3 scripts/50_adversarial_audit_checks.py` → `outputs/adversarial_audit/adversarial_audit_checks.json`. Every number below is either a projection of the `REAL` HKO climate design matrix or arithmetic on coefficients the project has already paid for. No health coefficient is created.

---

## 0. What counts as elimination

Three failure modes were treated as fatal:

1. **Straw-man dependence.** A uniqueness claim that only holds against a rival position nobody defends.
2. **Circularity.** An inversion whose output is fixed by the assumption used to perform it.
3. **Historical falsity.** A charge that the lab failed to ask a question the repository shows it already asked and already wrote down.

A thesis whose load-bearing evidence fails but whose narrower rule holds is recorded as SURVIVES-IN-REDUCED-FORM, with the reduced form stated exactly. That is not a compromise; the reduced form is what remains after the counterexample.

---

## 1. Verdicts

### 1.1 Alpha — "aggregation is the estimand, so Option A is the only licensed freeze"

**Verdict: SURVIVES-IN-REDUCED-FORM. The uniqueness claim is ELIMINATED.**

**Counterexample 1 — the Option B that Alpha defeats is not the Option B on the table.** Alpha §8.2 defines the rival as Option B "used to headline the two nominal contrasts", which "would silently promote that object into daily thermal triggering and differential CHD-versus-HF mechanism". The repository's Option B is: "Exploratory panel summary without discovery framing… Still not a confirmatory primary" (`reports/bishai_integrated_report/integrated_project_report.md` §10). Delta's Option B-lite lists "calling RR 1.073 a discovery" and "calling either contrast a mechanism" among its own forbidden promotions. Neither rival asserts daily triggering. Alpha's aggregation null-space algebra constrains **semantics** — no daily allocation, no individual contrast, no admission cause — and every rival on the table already concedes those bounds. An argument that eliminates only positions nobody holds cannot establish uniqueness.

**Counterexample 2 — a licensed sentence that is not a mechanism claim and is not Alpha's Option A.** The following is licensed under Option A *and* under repository Option B *and* under Delta's B-lite, and Alpha's algebra forbids nothing in it:

> At the frozen baseline specification, one of the twelve core contrasts — heart failure, cold days per five days, 1.073 — has intervals excluding 1 under all four displayed uncertainty methods and carries BH *q* = 0.192; under four of the nine already-paid trend and window scenarios its interval includes 1.

It makes no daily, individual, cause-specific, incidence, or cross-outcome claim; it displays all four SE methods rather than selecting one, satisfying `A54`; and it is not a confirmatory primary. Since Option A itself instructs "Report CVD-01 to CVD-12 with q-values and the full SE ladder", a freeze narrow enough to forbid that sentence would forbid Option A as written.

**Fatal logical flaw — category error.** Alpha §8.1 states that Option A "is the direct consequence of the identified object". The identified object determines what the numbers *mean*. It does not select among governance wordings that all accept those meanings. The step from a semantic constraint to a unique freeze choice is a non sequitur, and it is the whole of Alpha's Gate 3 conclusion.

**Second straw-man.** Alpha §6.1 rebuts "month fixed effects kill all thermal variation". Gamma cites the same 45.8% cold-day retention that Alpha uses as the rebuttal. Nobody in the crucible holds the position being refuted.

**Reduced form that survives, undamaged.** The NB2 nuisance-adjusted score derivation and the precise estimand name (§3.5); the aggregation null space — any daily perturbation with $\sum_{d\in m} v_d = 0$ is invisible to monthly sums, so more people inside the same monthly cells cannot recover daily timing; the F1.2 distinction between convergence and calibration (convergence 1.000 and maximum median Hessian condition $1.82\times10^3$, against Type I to 0.150, coverage to 0.840, maximum absolute relative bias 32.77, and false-sign probability to 0.808 — a power story cannot produce that combination); `A58`'s refusal of the CHD-heat/HF-cold contrast; and the observation that even a multiplicity-protected coefficient would still be the anomaly-association estimand.

### 1.2 Beta — "the null is a depletion artifact; the honest freeze is estimand incomplete"

**Verdict: SURVIVES-IN-REDUCED-FORM. The strong claim — that attenuation toward 1 is *primarily* an artifact of the absorbing risk set, and that attenuation is therefore not interpretable at all — is ELIMINATED.**

After Beta's own §4.1 concession that `ns(time,4)` removes 99.98% of a smooth depletion path and leaves every reporting-step multiplier within 0.002 of 1, the thesis rests on the covid-kink inversion (§4.3), the interaction channel (3.3), and the fatness ladder (§5). The first fails three ways.

**Counterexample 1 — the inversion is not an inversion of the same object.** The released `covid_phase_adjusted` scenario adds `covid_phase_f`, a five-level factor (four dummies) spanning 2020-02 to 2023-12 (`config.yml` `covid_phases`; `scripts/32_cvd_trend_depletion_lag.R`). Beta divides the resulting coefficient shift by the transfer coefficient of a stipulated eight-month, 0.10 log-unit dip in 2020-02–2020-05 and 2022-02–2022-05 (`scripts/49_depletion_crucible.py`, `depletion_paths`). Regressing the residualised stipulated dip on the residualised released phase dummies returns $R^2 = 0.367$: nearly two-thirds of the shape being inverted is not in the operator that produced the shift. The "recovered latent amplitude" is the ratio of two different projections and is defined only up to two arbitrary shape choices, neither observed.

**Counterexample 2 — the coherence fails on the only replication in Beta's own table.** The claim is within-outcome: same months, same risk set, five exposures whose transfer coefficients differ by a factor of 2.9 recovering one amplitude. For CHD they do: 0.0997, 0.1089, 0.1111, 0.1117, 0.1129 (mean 0.1089, coefficient of variation 4.9%). For HF, from the same file, the same five recover 0.0921, 0.1256, 0.2076, 0.2105, 0.2122 — mean 0.1696, coefficient of variation 33.4%, a 2.3-fold spread. Beta's memo quotes the CHD five, names "the two exceptions" as "the cold-day contrasts", and never reports the HF non-cold five — so the memo asserts by omission the very coherence its own file refutes; `scripts/test_49_depletion_crucible.py` binds only the CHD figure. Outcome-specific risk sets do not repair this, because the failure is *inside* HF, where a single latent monthly factor must give one amplitude. And HF carries the four contrasts Beta itself designates as describable in §8.3.

**Counterexample 3 — even if sound, the inversion does not evidence the denominator, and the release already answers it.** A 2020/2022 care-seeking dip in admissions is an ascertainment and intensity shock. It is not a change in the still-at-risk pool $R_t$, which is what §3 needs. Meanwhile the paid adjustment for exactly that shock moves Beta's own headline contrast by nothing: HF cold days per five days goes from 1.073 (1.006–1.144), *p* = 0.0310, to 1.074 (1.006–1.145), *p* = 0.0311. The channel Beta advances as its decisive evidence leaves untouched the contrast Beta most wants to protect.

**Fatal logical flaw — "primarily" is asserted without a magnitude or a sign.** With the smooth channel conceded as negligible and the kink channel closed for the defended contrasts, the only survivor is (3.3), a Fisher-weighted average over a drifting $\beta_t$. Beta supplies no bound on its size, and §7.4 concedes that if new T2D/HTN diagnoses balance first-event exits the risk set may be flat or rising and the bias sign reverses. A claim that an observed attenuation is *primarily* caused by a mechanism requires a dominance argument. Beta's own text withholds both sign and magnitude, then states that the bias "cannot currently be signed" as the load-bearing claim. Those two sentences cannot both be the thesis.

**Also eliminated — the blanket prohibition.** §8.2 instructs that "null", "no association", and "no evidence of an effect" must not appear "anywhere in the manuscript". Beta's own arithmetic supplies a bias budget for two of three channels. A bounded statement about the residual anomaly association, qualified by an unsigned risk-set term, is interpretable and is what the design supports. Silence is not the honest form; qualification is.

**Reduced form that survives.** `A48` restated as identification rather than courtesy: $\exp(\beta)$ is an incidence-rate ratio only if $\tilde R \perp \tilde x$, and that orthogonality is untested because $R_t$ does not exist in the repository. The offset-inertness rebuttal (my attack on it failed — §5.3). Trend-control sensitivity: six of twelve contrasts have a spread exceeding their own point estimate, and CHD hot nights ranges 1.0109–1.0246 with *p* from 0.315 to 0.0144 when only the secular control changes. The monthly cohort person-time falsifier and its four kill conditions, which are the most useful thing in the memo. "Estimand incomplete" as an `A48` amendment rather than a new gate.

**One figure is now forbidden.** §4.7's chance of 1/495 treats the four coinciding contrasts as four draws. Their residual correlations are 0.886 to 0.978 among HF mean temperature, mean Tmax and mean Tmin (`residual_exposure_correlations.csv`), so the set is approximately two independent contrasts, not four. Beta hedges correctly ("this is coherence, not a test"), so this does not kill; the 1/495 must not be quoted.

### 1.3 Gamma — "calendar-month fixed effects are overcontrol of a question nobody asked"

**Verdict: ELIMINATED as stated. The labelling rule survives, and is already project law.**

**Counterexample 1 — the charge is historically false.** Gamma §7: "Nobody in the lab asked that question." The live manuscript already contains, in Results: "After calendar-month indicators, remaining thermal estimates ask whether a given January or July differs from a typical January or July, not whether winter counts exceed summer counts" (`manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`). `knowledge/2026-08-12_existing_data_insights.md` §3 says the same and names it "a weaker, more honest question than 'is winter bad for HF?'". Hogan's own design contribution is the Li-HW count-by-month to upper-tail adaptation translation — an anomaly question by construction (`knowledge/CONTEXT_BOOTSTRAP.md`). Gamma's §6.1 self-falsification condition — "if the estimand of interest is adaptation-scale… this memo reduces to a labelling request" — is met by the record. Gamma wrote its own elimination and did not check whether the condition had already fired.

**Counterexample 2 — the null is not mechanical, and Gamma's own number proves it.** `P14` is fitted in exactly the control space Gamma calls annihilation: `month_f` plus `splines::ns(time_index, df = 4)` (`scripts/20_fit_pathway_panel.R`). The flu series retains **48.8%** of its variance after those controls — comparable to cold days at 45.8% and thirteen times mean temperature's 3.6% — and CHD flu is **1.673 (1.249–2.243), *p* = 5.7×10⁻⁴** on 121 months. A winter-concentrated exposure with genuine year-to-year within-month variation is detected at *p* < 0.001 inside month fixed effects. The dummies remove the eleven-year calendar-month mean of whatever series is fed to them; whether the remainder is informative is a property of the exposure, not a refusal by the design. Gamma imports 1.673 as an argument *for* a seasonal-contrast model without noticing it was produced *by* month fixed effects.

**Counterexample 3 — over-import.** That 1.673 is `original_panel` under a `population_x_days` offset with a model-based standard error, not the amended days-only Newey–West core. For the outcome that carries the cold association, HF flu is **1.407 (0.958–2.067), *p* = 0.081**. The "nameable, measurable confounder" argument does not hold for HF at all.

**Fatal logical flaw — the circularity charge is symmetric.** §5.1 argues that when the exposure *is* the seasonal cycle, conditioning on calendar month deletes it. True, and beside the point, because the chosen estimand is the anomaly. For the anomaly contrast, calendar month adjusts for everything with a fixed calendar pattern, including the 51.2% of flu's own variance that calendar month and trend absorb, holidays, Lunar New Year on average, and seasonal care patterns. Gamma's alternative identifies the winter thermal contrast only under an exhaustive-seasonal-confounder assumption that Gamma concedes is unverifiable — "anything seasonal and unmeasured contaminates it; that is the price". Preferring a differently identified estimand is a choice, not a counterexample to the current one.

**Counterexample 4 — the localisation claim is false on the paid table.** §4 asserts that the extreme-day counts "are the only exposures that carry variance past the month dummies", so nominal signals "can only appear at P04A/P04B". BH ranks 3 and 4 of twelve are continuous-temperature HF contrasts: mean Tmin *p* = 0.0504, mean temperature *p* = 0.0692. HF mean Tmin excludes 1 under three of four SE methods and HF mean temperature under two (`se_method_discordance.csv`). At lag 1, HF mean Tmin is *p* = 0.003, smaller than any extreme-day contrast. Gamma concedes this in §6.3 and then restates the localisation claim in §7.

**Counterexample 5 — "precise null" is wrong on Gamma's own scale.** §3 calls the CHD continuous-temperature results precise anomaly nulls. The NW6 per-degree interval for CHD mean temperature is −0.0240 to +0.0101 in log counts. The crude between-season gradient implied by the paid seasonality table — January 1,386.3 versus September 1,097.1 events across 17.10 °C versus 28.63 °C — is −0.0203 per °C, **inside** that interval. For HF the crude gradient is −0.0329 and the interval is −0.0541 to +0.0020, also containing it. Under a linear reading the anomaly design does not exclude a slope equal to the entire seasonal gradient. This defeats "the null is the mechanical consequence of R²(month) ≈ 0.96" and independently supports the single Gamma rule worth keeping.

**Reduced form that survives.** Do not narrate 0.993 or 0.974 as "temperature is unrelated to monthly first-event counts". Do not narrate the P04 concentration as biology preferring official thresholds. State the projection identity (4.70 °C → 0.90 °C, R²(month) = 0.958). All three are already in force in the live file and in `A48`/`A54` practice. Gamma supplies emphasis, not a new licence.

### 1.4 Delta — "*q* > 0.19 is a BH and power tax; the honest freeze is Option B-lite"

**Verdict: SURVIVES-IN-REDUCED-FORM. §3 is ELIMINATED and the surviving sentence must be rewritten.**

**Counterexample 1 — the power inversion is the p-value in costume.** observed/detectable $= |\hat\beta|/(2.8\,\mathrm{SE}) = z/2.8$, a strictly monotone function of *p* alone. Recomputed for all twelve contrasts, the maximum absolute gap between $z/2.8$ and the reported ratio is $1.4\times10^{-5}$. "77% of the 80%-power detectable size" is therefore an invertible restatement of "*p* = 0.031", and any contrast with *p* just above 0.05 returns roughly 0.70. This is observed (post-hoc) power, which adds nothing to the p-value, and it is computed on the two smallest p-values in a family of twelve after inspection, so the ratio is high *because* they were selected. §3 must be struck. Its conclusion does not need it: Benjamini–Hochberg controls the false-discovery rate, not power, and §2's verified arithmetic — rank 1 requires *p* ≤ 0.004167, the smallest observed *p* is 7.43 times that, and rank 1 is pulled down to rank 2's 0.1922 — carries the point unaided.

**Counterexample 2 — asymmetric robustness, an offence this repository has already ruled on.** §4 compresses HF cold days into "trend/depletion range: 1.043–1.113" and then quotes intervals only for the strengthening rungs. Four of the nine paid scenarios have intervals including 1: `trend_ns8` 1.062 (0.994–1.135), *p* = 0.073; `year_fixed_effects` 1.061 (0.997–1.129), *p* = 0.064; `drop_first_12_months` 1.067 (0.995–1.143), *p* = 0.069; `drop_first_24_months` 1.043 (0.965–1.127), *p* = 0.288. This is precisely the practice the 13 August critique made mandatory to stop — the CHD hot-night 1.011 hidden inside "1.011 to 1.025" (`knowledge/2026-08-13_fable_live_doc_critique.md`) — reproduced with the outcomes exchanged. The consequence for wording is exact: **SE-concordance is a property of the frozen baseline specification, not of the contrast.** Replace `ns4` with `ns8` and the Newey–West interval includes 1.

**Counterexample 3 — the ladder cannot be evidence for both readings.** Delta reads the window rungs as robustness; Beta reads the identical rungs as a monotone risk-set composition axis with Spearman +1.000. Neither may cite the ladder as unqualified support without stating that the same rungs carry the rival reading.

**Fatal for the wording, not the substance.** Delta's audit-surviving sentence pairs "retains an SE-concordant exploratory residual" with "the expected Benjamini–Hochberg outcome for effects at ~77% of the 80%-power detectable size, not a demonstration of absence". That presupposes an effect and then supplies an excuse for its non-detection. It reads as a discovery with an apology attached. Replacement wording is §4.

**Reduced form that survives.** The BH arithmetic and the rank-1/rank-2 pull-down. *q* > 0.19 is not a demonstration of absence. The CHD/HF separation stated strictly as an uncertainty-display fact: CHD hot nights 1.022 with Model 0.995–1.049 and HC1 0.997–1.047 including 1, pre-2020 1.011 (0.991–1.032), *p* = 0.289, and residual ACF(1) ≈ 0.51 with the NW6 interval *narrower* than the model interval. Option A as a reporting rule.

**And one structural finding.** "Option B-lite" is not a rival freeze. Repository Option A already instructs "Report CVD-01 to CVD-12 with q-values and the full SE ladder; refuse a single headline differential thermal claim". Delta's B-lite is Option A plus a prohibition on null narration. The crucible's apparent four-way disagreement about *which freeze* is in fact a one-way disagreement about *narration*, and on narration Beta, Gamma and Delta agree while Alpha is silent rather than opposed.

---

## 2. What is now uneliminated

The parent proof must carry all of the following, and may carry nothing that contradicts them.

1. **The estimand.** An outcome-specific, separate-exposure, nuisance-adjusted NB2 pseudo-true log count-ratio for a year-to-year within-calendar-month change in monthly extreme-day burden, conditional on a 4-df secular trend and normalised by days in month. Ecological; not incidence, not principal diagnosis, not an individual contrast, not a daily effect. (Alpha §3; uncontested.)
2. **The aggregation null space.** Daily allocation and lag timing are not recoverable from monthly sums without additional structural restrictions, and the restriction set that was tried failed calibration on Type I error, coverage, bias, and sign while converging cleanly. (Alpha §4; uncontested.)
3. **The denominator gap.** The still-at-risk T2D/HTN cohort person-time is absent; $\exp(\beta)$ is a count ratio and would be an incidence-rate ratio only under an orthogonality condition that cannot currently be tested. The sign of the resulting bias is unknown, including the possibility that the risk set is flat or rising. (Beta §3, §7.4; `A48`.)
4. **The estimand is the anomaly contrast, and the lab already said so.** The between-season contrast is absorbed into the eleven month intercepts and is not estimated with confounder adjustment. The live manuscript already states this. (Gamma §2–§3, corrected by §1.3 above.)
5. **Month fixed effects retain power for exposures with real within-month variation.** Flu retains 48.8% of its variance in the same control space and is estimated at 1.673 (1.249–2.243) for CHD. The near-1 continuous-temperature ratios reflect how little temperature varies within calendar month, not a design that refuses to estimate.
6. **The continuous-temperature intervals do not exclude the crude seasonal gradient.** CHD −0.0240 to +0.0101 per °C against a crude −0.0203; HF −0.0541 to +0.0020 against −0.0329. Neither a null nor a seasonal finding may be read from them.
7. **Multiplicity.** All twelve core BH *q* exceed 0.19; rank 1 requires *p* ≤ 0.004167; the smallest observed *p* is 0.0310, 7.43 times the threshold. BH controls the false-discovery rate, not power, and under the positive dependence induced by one shared climate series it is likely conservative — which favours the "tax, not absence" reading. (Delta §2.)
8. **The one SE-concordant contrast, correctly bounded.** HF cold days per five days, 1.073, is the only core contrast whose interval excludes 1 under all four displayed methods, **at the frozen baseline**. Under `trend_ns8`, `year_fixed_effects`, `drop_first_12_months` and `drop_first_24_months` its interval includes 1. Both halves travel together, always.
9. **The window ladder is contested evidence.** The same four rungs are Delta's robustness and Beta's composition axis. Report the rungs; do not report either interpretation as established.
10. **Sparsity is not the objection to HF cold.** Residual cold-day identifying variance is spread across winters: the largest winter-year group holds 15.7%, the largest single month 10.3%, and eight of twelve groups are needed to reach 80%. Hot nights are more concentrated (six groups). Any synthesis that dismisses HF cold as "a few winters" is wrong.
11. **`A58` stands.** No cross-outcome CHD-heat/HF-cold claim without the stacked interaction and a released estimate of $\Delta$ with calibrated uncertainty.
12. **`A54` stands, and extends.** No SE method may be selected because its interval excludes 1. This now explicitly includes selecting a rung of the SE ladder by the multiplicity result it would produce: Newey–West lag 6 is the frozen inferential display and BH is computed on it alone.
13. **The freeze disagreement is narration, not governance.** Option A already mandates full panel reporting with q-values and the SE ladder. No agent produced a licensed sentence that Option A forbids.

---

## 3. Forbidden sentences

No synthesis may utter any of these, in any paraphrase.

1. "Option A is the only logically licensed freeze." (Alpha §1, §8; eliminated in §1.1.)
2. "Option B would promote the panel into daily triggering / a CHD-versus-HF mechanism." Not true of repository Option B or of B-lite.
3. "The null is primarily an artifact of the missing denominator." No sign, no magnitude. (Beta; eliminated in §1.2.)
4. "Five contrasts recover one common latent amplitude of about 0.109." The same table's HF five span 0.092 to 0.212.
5. "The paid `covid_phase_adjusted` shift inverts to the latent risk-set dip." It inverts through a stipulated shape only 36.7% spanned by the operator that produced the shift.
6. Any use of "1/495", or of "two independently defined criteria" as if the four HF contrasts were four independent draws.
7. "Do not write 'null' or 'no association' anywhere." The licensed form is qualified, not absent.
8. "Month fixed effects delete the exposure / nobody asked the anomaly question / the specification refuses to estimate." (Gamma; eliminated in §1.3.)
9. "Only the official extreme-day metrics can show signals." BH ranks 3 and 4 are continuous-temperature HF contrasts.
10. "The CHD continuous-temperature results are precise nulls." Their interval contains the crude seasonal gradient.
11. "Flu is the confounder month fixed effects delete instead of adjusting." Flu was estimated inside month fixed effects at 1.673, *p* = 5.7×10⁻⁴.
12. "Winter kills" / "cold is worse for HF" / any between-season effect size. The seasonal estimand is unestimated with confounder adjustment.
13. "The effects are at 77% of the detectable size, so *q* > 0.19 is expected." This is *p* = 0.031 restated, computed on selected contrasts.
14. "HF cold days is robust across trend and depletion specifications" or any bare range such as "1.043–1.113" without the four rungs whose intervals include 1.
15. "HF cold days is the panel's outstanding residual / headline." A headline verb, however hedged, reads as a discovery.
16. "Under a different SE method the contrast would clear BH." `A54`, extended in §2.12.
17. Any statement that heat or cold caused a hospitalisation, that an individual's exposure triggered an event, that the counts are incidence, attack rates, principal-diagnosis CHD/HF, AMI or stroke, or that a daily coefficient exists.

---

## 4. The strongest remaining licensed paragraph

Everything below survived every attack above. 118 words.

> Across twelve core contrasts fitted separately by outcome and exposure, the estimand is a within-calendar-month, year-to-year weather-anomaly count ratio for first recorded hospitalisation after first diagnosis, conditional on a four-degree-of-freedom secular trend and a days-in-month offset, with the still-at-risk cohort denominator absent. No contrast clears Benjamini–Hochberg control: rank one would require *p* ≤ 0.004167 and the smallest observed *p* is 0.031. At the frozen baseline one contrast, heart failure and cold days per five days at 1.073, excludes 1 under all four displayed uncertainty methods; under four of nine paid trend and window scenarios it does not. The panel licenses no confirmatory primary, no daily, individual, cause-specific or cross-outcome claim, and no statement that thermal association is absent.

That paragraph is a reporting rule, not a finding. It names one contrast and immediately bounds it in the same sentence, which is the only construction that cannot be quoted as a discovery.

---

## 5. Attacks that failed

Recorded so nobody re-runs them.

1. **Genericity of Beta's amplitude inversion.** I predicted the cross-exposure coherence would reproduce under arbitrary pandemic-era shapes, making it uninformative. It does not. Coefficient of variation across the five non-cold exposures: 0.180 for an early-COVID block, 0.147 for the fifth wave, 1.117 for late 2022, 1.098 for post-reopening, 6.087 for a single 2020-02–2023-12 block, and 0.747 for a ramp. None approaches the observed CHD tightness of 0.049. The CHD coherence is a real property of the fitted CHD phase coefficients. The kill in §1.2 is shape mismatch and the HF failure, not genericity. **Dead end.**
2. **HF cold as "a few winters".** Sparsity is not there: top winter-year group 15.7%, top single month 10.3%, eight of twelve groups for 80%; hot nights are the more concentrated series. **Dead end.**
3. **Offset inertness against Beta.** Beta's rebuttal holds. Population × days is near-collinear with `ns(time,4)`, and the no-offset variant removes $\log D_t$, whose 28–31-day swing is itself calendar-month patterned and therefore absorbed by the month dummies. Neither sensitivity tests $R_t$. Attack fails.
4. **Beta's §8.3 selection as self-contradictory.** I checked whether the four HF contrasts Beta calls describable are the *worst* contaminated by Beta's own covid channel. They are not: $|\Delta\log \mathrm{RR}| / |\log \mathrm{RR}|$ is 0.259–0.290 for HF mean temperature, mean Tmax and mean Tmin and 0.012 for HF cold days — the four lowest in the panel. Attack fails.
5. **BH conservativeness against Delta.** Not attacked. Under positive regression dependence BH is conservative, and the twelve contrasts share one climate series, so this helps Delta's reading. No concrete flaw was found and none was invented.

---

## 6. Test results

| Command | Result |
|---|---|
| `python3 scripts/test_48_identification_crucible.py` | **PASS** |
| `python3 scripts/test_49_depletion_crucible.py` | **PASS** (14 memo claims bound to tables) |
| `python3 scripts/50_adversarial_audit_checks.py` | Ran clean; wrote `outputs/adversarial_audit/adversarial_audit_checks.json` |

`test_49` passes while binding only the CHD amplitude ("CHD latent dip amplitude: 0.1089 (SD 0.0053)"). A passing test is not a defence of §1.2 counterexample 2: the test asserts the number Beta reported, and the counterexample is the number Beta did not.

## 7. In-repo proof sources

1. `outputs/adversarial_audit/adversarial_audit_checks.json`, `scripts/50_adversarial_audit_checks.py`
2. `outputs/identification_crucible/` — `identification_summary.json`, `exposure_residual_variation.csv`, `se_method_discordance.csv`, `bh_detectability.csv`, `residual_exposure_correlations.csv`, `calendar_month_support.csv`
3. `outputs/depletion_crucible/` — `covid_kink_amplitude_inversion.csv`, `riskset_fatness_ladder.csv`, `depletion_summary.json`
4. `outputs/tables/` — `cvd_trend_depletion_sensitivity.csv`, `cvd_descriptive_seasonality_by_month.csv`, `combined_pathway_panel_estimates.csv`, `cvd_offset_sensitivity_wide.csv`
5. `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`
6. `reports/bishai_integrated_report/integrated_project_report.md` §10 (Option A / B / C as actually written)
7. `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md` (Results: the anomaly-question sentence)
8. `knowledge/2026-08-12_existing_data_insights.md` §3–§6; `knowledge/2026-08-13_fable_live_doc_critique.md` (symmetric sensitivity reporting)
9. `analysis_plan/assumption_ledger.md` — `A48`, `A54`, `A58`; `reports/gate3_decision_packet_2026-08-07.md`
10. `config.yml` `covid_phases`; `scripts/20_fit_pathway_panel.R`; `scripts/32_cvd_trend_depletion_lag.R`; `scripts/49_depletion_crucible.py`
