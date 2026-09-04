# What the monthly panel can license — identification crucible

**Date:** 14 August 2026  
**Mode:** Explore then Decide. Not a Gate 3 freeze. No new health model. No governed monthly counts read.  
**Branch:** `cursor/identification-crucible-1fd0`

Four mutually exclusive theses were pushed to extremes and then attacked. This note is the remainder: what still stands after concrete counterexamples, and what must not be said.

Rebuild:

```bash
python3 scripts/48_identification_crucible.py
python3 scripts/49_depletion_crucible.py
python3 scripts/50_adversarial_audit_checks.py
python3 scripts/test_48_identification_crucible.py
python3 scripts/test_49_depletion_crucible.py
python3 scripts/test_50_adversarial_audit_checks.py
```

Agent memos (pre-audit): `knowledge/crucible_agent_alpha_aggregation.md`, `crucible_agent_beta_depletion.md`, `crucible_agent_gamma_overcontrol.md`, `crucible_agent_delta_decision_rule.md`.  
Audit: `knowledge/crucible_adversarial_audit.md`.

GLM-5.3 Max was not in the available model list; Agent Delta ran as Grok 4.5 High.

---

## 1. Axioms (ground truths of *this* design)

1. `[HA_APPROVED_AGGREGATE]` Outcomes are territory-month counts of the first recorded hospitalisation after first CHD or HF diagnosis in a T2D/HTN cohort, 132 months, January 2013–December 2023. Admission cause is absent. Stroke was not delivered.
2. `[DESIGN]` The analysis of record is separate-exposure negative binomial, calendar-month indicators, `ns(time, 4)`, days-in-month offset, Newey–West lag-6 display, with Model/HC1/NW3 shown beside it (`A54`). Control rank ≈ 16; residual df ≈ 116.
3. `[REAL]` After those controls, monthly mean temperature retains 3.6% of its variance (remaining SD 0.90°C; raw SD 4.70°C). Hot nights retain 25%; cold days retain 46%. July hot nights range 1–25. Of 145 cold days, 97.2% fall in December–February; 29 months are nonzero.
4. `[SYNTHETIC_CALIBRATION]` A clean-room monthly-outcome / daily-exposure recovery failed F1.2: Type I to 0.150, coverage to 0.840, relative bias 32.77, false-sign 0.808, while every core cell converged. No real daily coefficient is admitted.
5. `[HA_APPROVED_AGGREGATE]` All twelve core Benjamini–Hochberg *q* exceed 0.19. Rank 1 at *q* < 0.05 would need *p* ≤ 0.004167. The smallest observed *p* is 0.0310 (7.43 times that threshold).
6. `[A48]` The T2D/HTN still-at-risk denominator is absent. `exp(β)` is a count ratio. It is an incidence-rate ratio only if residual person-time is orthogonal to residual weather, which cannot be tested here.
7. `[A58]` Separate CHD and HF coefficients do not estimate a CHD-heat versus HF-cold contrast.

These axioms are not findings. They are the measurement contract.

---

## 2. What each path claimed, and what killed it

| Path | Extreme claim | Verdict | Concrete kill |
|---|---|---|---|
| Alpha (aggregation) | Daily triggering is unidentified, therefore Option A is the *only* licensed freeze | **Reduced.** Estimand and M\|D failure stand. Uniqueness of freeze wording dies. | Repository Option B already forbids discovery framing and is still “not a confirmatory primary.” Semantics do not pick a unique governance sentence. |
| Beta (depletion) | The *q* > 0.19 panel is *primarily* an absorbing-risk-set artifact; attenuation toward 1 is uninterpretable | **Reduced.** A48-as-identification stands. “Primarily” dies. | Smooth `log R` is absorbed by `ns(time,4)` (R² ≈ 0.9998). The 0.10 COVID-kink inversion spans only 36.7% of the released phase operator; the “common 0.109 amplitude” fails inside HF (0.092–0.212, CV 33%). `covid_phase_adjusted` moves HF cold days 1.0728 → 1.0737. Sign of any remaining bias is unknown. |
| Gamma (overcontrol) | Month FE delete the question nobody asked; the continuous-T “null” is mechanical | **Eliminated** as stated. Labelling rule already project law. | The live manuscript already states the anomaly question. Flu retains 48.8% of its variance in the same control space and is 1.673 (1.249–2.243), *p* = 5.7×10⁻⁴ for CHD. The CHD per-°C interval (−0.024 to +0.010) contains the crude January–September gradient (−0.020). |
| Delta (decision rule) | *q* > 0.19 is a BH *and power* tax; Option B-lite is the honest freeze | **Reduced.** BH arithmetic stands. Power inversion dies. B-lite is not a rival freeze. | observed/detectable = *z*/2.8 (max gap 1.4×10⁻⁵): a restatement of *p*. The range 1.043–1.113 hides four rungs whose intervals include 1 (`ns8`, year FE, drop-12, drop-24). Option A already requires the full panel, *q*, and the SE ladder. |

Failed attacks (do not re-run): treating HF cold as “a few winters” (eight of twelve winter groups for 80% of residual identifying variance); treating offset inertness as a test of `R_t`; treating Beta’s CHD amplitude coherence as generic (it is not).

---

## 3. The identified object

After calendar-month indicators and a 4-df time spline, the negative-binomial score for an extreme-day count (scaled per five days) is a weighted covariance between residual first-event monthly counts and residual within-calendar-month weather-anomaly burden. The reported `exp(β)` is the expected monthly count ratio for five extra hot nights or cold days of that kind.

That object is identified. July 1 versus 25 hot nights, and January 0 versus 11 cold days, are inside the residual variation. What is *not* identified, from this grain, is:

- daily allocation or lag kernels (aggregation null space; F1.2 failed);
- individual causality or admission-cause effects (outcome construction);
- cohort incidence (missing `R_t`);
- the winter-versus-summer contrast after confounder adjustment (absorbed into month intercepts, by choice);
- a CHD-versus-HF thermal difference (`A58`).

Month FE are not a sample-size failure (116 residual df remain). They are a choice of estimand. The lab already wrote that choice down.

---

## 4. What the paid panel then says, without promotion

At the frozen baseline, one of twelve core contrasts — heart failure, cold days per five days, 1.073 — has intervals excluding 1 under Model, HC1, NW3, and NW6, and carries BH *q* = 0.192. Under four of nine already-paid trend and window scenarios (`trend_ns8`, year FE, drop first 12 months, drop first 24 months) that same interval includes 1. Pre-COVID it is 1.113 (1.053–1.176). Those rungs are reported together. They are Delta’s robustness reading and Beta’s composition reading; neither interpretation is established.

CHD hot nights per five days, 1.022, exclude 1 only under NW3/NW6. Model 0.995–1.049 and HC1 0.997–1.047 include 1. Pre-2020: 1.011 (0.991–1.032), *p* = 0.289. Residual ACF(1) ≈ 0.51. This contrast is SE-sensitive at baseline and is not a second “signal.”

Continuous-temperature ratios hug 1 because leftover thermal SD is about 0.9°C, not because the design refuses to estimate. Flu, which keeps 49% of its variance after the same controls, is detected. The continuous-temperature intervals do not exclude a slope as large as the crude seasonal gradient.

---

## 5. Licensed paragraph (survived the audit)

> Across twelve core contrasts fitted separately by outcome and exposure, the estimand is a within-calendar-month, year-to-year weather-anomaly count ratio for first recorded hospitalisation after first diagnosis, conditional on a four-degree-of-freedom secular trend and a days-in-month offset, with the still-at-risk cohort denominator absent. No contrast clears Benjamini–Hochberg control: rank one would require *p* ≤ 0.004167 and the smallest observed *p* is 0.031. At the frozen baseline one contrast, heart failure and cold days per five days at 1.073, excludes 1 under all four displayed uncertainty methods; under four of nine paid trend and window scenarios it does not. The panel licenses no confirmatory primary, no daily, individual, cause-specific or cross-outcome claim, and no statement that thermal association is absent.

That is a reporting rule, not a finding. Gate 3 remains a human decision. Option A as already written — no confirmatory primary; report CVD-01 to CVD-12 with *q* and the SE ladder — is compatible with this paragraph. Narrating *q* > 0.19 as “no association” is not.

---

## 6. Human-owned next (unchanged by this crucible)

1. Gate 3 freeze (Option A / B / C) by Hogan / Roro / Bishai / Bob.
2. Roro: monthly T2D/HTN still-at-risk person-time, split by entries and exits (`D10`).
3. Hogan: weather / HM-CM lock (Playbook 01). This note does not drop month FE.
4. Stroke file, ICD lists, inpatient semantics, dissemination, IRB.

A seasonal-contrast model (winter indicator or harmonic plus flu) remains a *different* estimand. It is parked for Hogan. It is not run here.

---

## 7. Forbidden promotions (audit §3, condensed)

Do not say: Option A is the only logically licensed freeze; Option B implies daily triggering; the null is primarily a missing-denominator artifact; five contrasts recover one 0.109 latent dip; month FE refuse to estimate; only official extremes can show signals; CHD continuous-T results are precise nulls; effects sit at 77% of detectable size; HF cold is “robust 1.043–1.113” without the four rungs that include 1; HF cold is a headline or discovery; any causal, incidence, stroke, or daily-coefficient claim.
