# Crucible Agent Gamma — calendar-month fixed effects are overcontrol

**Post-audit (14 Aug):** ELIMINATED as stated. The labelling rule (do not narrate anomaly nulls as “temperature is unrelated”) survives and was already project law. The live manuscript already asks the anomaly question; flu is detected inside month FE. See `knowledge/crucible_adversarial_audit.md` and `reports/identification_crucible_2026-08-14.md`.


**Date:** 2026-08-14  
**Mode:** Explore (proof memo; no new health models; no HA microdata; no web search)  
**Agent:** Gamma (Fable 5)  
**Branch:** `cursor/identification-crucible-1fd0`  
**Thesis (extreme):** Calendar-month fixed effects do not adjust the seasonal thermal question — they delete it. They absorb 95.8% of mean-temperature variance into 11 intercepts and leave the continuous-temperature coefficient a within-calendar-month anomaly slope on a 0.90°C-SD residual. The "null" on continuous temperature is the mechanical consequence of R²(month)≈0.96, not evidence that temperature is unrelated to monthly first-event counts. Extreme-day counts are the only nominal signals because they are the only exposures that carry variance past the month dummies. Gate 3 should not freeze Option A on the overcontrolled specification as if it had tested the seasonal question.

**Not this memo:** daily-kernel identification (Alpha), missing person-time (Beta), BH/power arithmetic (Delta). Delta accepts the month-FE estimand and reads its residuals; Gamma argues the estimand itself is the weaker question. The two are orthogonal and can both be true.

---

## 1. Provenance

| Object | Status | Source |
|---|---|---|
| Residual variation after month FE / month+ns4 | `REAL` HKO monthly | `outputs/identification_crucible/exposure_residual_variation.csv` |
| Calendar support (cold days, hot nights by month) | `REAL` | `outputs/identification_crucible/calendar_month_support.csv`; `identification_summary.json` |
| Residualised exposure correlations | `REAL` | `outputs/identification_crucible/residual_exposure_correlations.csv` |
| Projection-identity check (demeaning by calendar month) | `REAL`, recomputed this session from `data_processed/climate_monthly_2013_2023.csv` | numbers in §2 |
| Core 12 count ratios, p, q | `HA_APPROVED_AGGREGATE` | `outputs/release_chd_hf/tables/table2_core_models.csv` via `bh_detectability.csv` |
| Crude seasonality and crude Pearson r | `HA_APPROVED_AGGREGATE` | `knowledge/2026-08-12_existing_data_insights.md` §3 (`cvd_descriptive_seasonality_by_month.csv`, `cvd_descriptive_temp_correlations.csv`) |
| Flu co-predictor, influence months | `HA_APPROVED_AGGREGATE` | same memo §6, §9 (`combined_pathway_panel_estimates.csv`, influence tables) |

No governed counts were read. Hogan weather prose, Stage 3 PDFs, and live paste files untouched.

---

## 2. The projection identity — what month dummies actually do to temperature

By Frisch–Waugh–Lovell, the coefficient on `mean_temp` in a model with calendar-month indicators is the slope of (residualised) counts on the residual of temperature after projection onto the month dummies. With 12 calendar cells × 11 years, that projection replaces each observation by its 11-year calendar-month mean, so the identifying regressor is exactly the anomaly \(T_{y,m} - \bar T_m\).

Verified this session on the `REAL` climate file:

- Raw SD of monthly mean temperature: **4.70°C**. SD of \(T_{y,m}-\bar T_m\): **0.965°C** (79.5% collapse). After adding `ns(time,4)`: **0.897°C ≈ 0.90°C** — an **~81% SD collapse**, matching `exposure_residual_variation.csv` (R²(month)=0.958; R²(full)=0.964; remaining variance share 3.6%).
- The absorbed axis is the entire climate of Hong Kong: calendar-month means run from **17.1°C (January) to 29.5°C (July)**, a 12.4°C range; DJF mean 17.6°C vs JJA 29.1°C. The largest anomaly ever shown to the model is **2.83°C**. The design offers the coefficient roughly one-fifth of the thermal SD and less than a quarter of the thermal range.
- The trend spline is innocent: R²(ns4 only)=**0.012** for mean_temp. The month dummies do essentially all of the annihilation.
- Residual df after full controls is **116** with control rank 16. This is not a degrees-of-freedom shortage; 116 df remain. What was removed is the signal axis, not the sample.

The same collapse hits all three smooth exposures: mean_tmax remaining SD 1.00°C (R²(month)=0.947), mean_tmin 0.93°C (0.956).

---

## 3. The question swap — the winter question is estimated, then discarded as nuisance

The lab's motivating question is between-season: crude HF January mean **287** vs September **196**; CHD **1,386** vs **1,097**; crude Pearson with mean temperature HF **r=−0.40**, CHD **r=−0.20** (`HA_APPROVED_AGGREGATE`). That contrast lives on the 12.4°C axis of §2.

Under month FE, that entire contrast is absorbed into the 11 month intercepts. The intercepts are estimated — the winter effect is inside the fitted model — and then treated as nuisance, never read. The continuous-temperature coefficient answers only: *is an unusually cold January different from a typical January, by ±0.9°C?* That is a different and strictly weaker question, and it is the only question the specification tests.

The paid results are exactly what this predicts: after month FE the continuous-temperature count ratios hug 1 — CHD 0.993–0.994 (q 0.64–0.76), HF 0.973–0.981 (q 0.20–0.27). For CHD these are *precise* anomaly nulls (per-°C SE ≈ 0.007–0.009). A precise null on 0.90°C anomalies licenses no statement — in either direction — about the 12.4°C seasonal contrast. Reporting it as "temperature shows no association" converts an estimand swap into a scientific conclusion.

---

## 4. Why the extreme-day counts survive — geometry, not biology

The official-definition counts are the only exposures that carry variance past the month dummies:

- **Retained variance share after full controls:** hot nights **25.1%**, very hot days **30.0%**, cold days **45.8%** — versus 3.6–4.3% for the three smooth means. Cold days retain ~12× the share of mean_tmin.
- **Why:** these are zero-truncated, skewed counts with huge within-calendar-month spread that an 11-year cell mean cannot absorb. July hot nights range **1–25** across the 11 years (SD 7.0 around a mean of 13.5); January cold days range **0–11**. Cold days are zero in April–November (103 of 132 months zero; 145 total days, 97.2% in DJF); hot nights are zero November–April.
- **What their coefficients mean after month FE:** a "cold-day effect" is identified almost entirely from *which winters* had more days with Tmin≤12°C — not from winter versus summer.

So when nominal signals appear, they can only appear at P04A/P04B: CHD hot nights 1.022 (p=0.032, q=0.192), HF cold days 1.073 (p=0.031, q=0.192). This localisation is the geometry of retained variance, not evidence that biology responds to threshold counts rather than to temperature. The residualised correlations say the counts are still temperature anomalies in disguise: after month+trend, corr(cold_days, mean_tmin) = **−0.664** and corr(hot_nights, very_hot_days) = **0.700**. The counts measure much the same anomaly as the smooth means; they simply deliver it with 6–12× more surviving variance. "Only the official extreme metrics show signals" is a statement about the projection, and it should never be narrated as a biological threshold finding.

---

## 5. Counterexample — "month FE is required to avoid confounding" (by what?)

The defence of month FE is that it prevents seasonal confounding. Examine it:

1. **If the "confounder" is season itself, the argument is circular.** A confounder is a third variable distinct from the exposure contrast under study. When the scientific exposure *is* the seasonal thermal cycle, conditioning on calendar month does not separate exposure from confounder — it deletes the shared axis, exposure included. That is not adjustment; it is refusal to estimate.
2. **The nameable seasonal confounder is measurable and should be modelled, not deleted.** Influenza is the concrete case: the flu indicator predicts CHD counts at **1.67 (1.25–2.24)** on 121 months (P14, `HA_APPROVED_AGGREGATE`), and flu is winter-peaked. A seasonal-contrast model (winter indicator or annual harmonic as the estimand, flu covariate on its measured 121/132-month values, trend spline) lets the data say how much of the winter excess flu explains — the thermal contrast shrinks when flu enters, or it does not. Month FE forecloses that question: it discards the thermal contrast and the flu contrast together, unread, and within months it cannot separate cold anomalies from flu anomalies anyway.
3. **Month FE does not even deliver the protection invoked for it.** The confounders that actually contaminate this panel move *within* calendar months across years: the two most influential observations are **2020-02 and 2022-02**, pandemic care-seeking shocks that month FE by construction cannot absorb (they are deviations from the February mean) and that had to be handled by influence diagnostics; Lunar New Year is a moveable feast that falls in late January some years and February in others, which fixed calendar-month intercepts cannot represent. So the design deletes the seasonal signal it was supposed to protect and passes through the year-specific shocks it was supposed to block.

Conclusion of the counterexample: month FE trades a named, measurable confounder (flu) for wholesale deletion of the estimand, while leaving the real within-month confounders standing. The honest defence of month FE is not "it avoids confounding" — it is "we chose to study anomalies." That choice should be stated, and its cost (§2–§3) priced.

---

## 6. Self-falsification — what would make month FE *not* overcontrol

Gamma's thesis dies, in whole or part, under any of the following:

1. **The lab genuinely asks the anomaly question.** If the estimand of interest is adaptation-scale — "does an unusually hot July differ from a typical July?" — then month FE is exactly the right design and this memo reduces to a labelling request. The overcontrol charge presumes the motivating question is between-season (the crude winter peaks, Hogan's cold–HF framing, the Jasmine cold-dominant mortality spine say it is).
2. **Numerical threshold.** If R²(month) for mean_temp were ≤ ~0.5 — remaining SD ≥ ~3.3°C, ≥50% variance share — month FE would be cheap insurance, not annihilation, and I would withdraw "overcontrol." At remaining SD ≥ ~2°C (≥18% share) I would soften to "expensive but defensible." At the observed **0.90°C / 3.6%**, the extreme reading stands.
3. **Signal survival.** If the anomaly design nevertheless produced SE-concordant continuous-temperature signals, annihilation would be an incomplete story. Partial concession owed: HF continuous residuals sit at p=0.050–0.069 (mean_tmin 0.973, lag-1 p=0.003), direction-consistent with cold harm — the collapse did not fully silence HF. The thesis is strongest for CHD, where the anomaly slope is a precise null.
4. **Confounder dominance.** If, in a seasonal-contrast model with measured covariates, flu (plus trend) absorbed the entire winter excess, the FE and seasonal specifications would agree and the choice would be inert. That is an empirical outcome the current specification cannot reveal — which is itself the point.

---

## 7. Extreme conclusion — what Gate 3 may and may not freeze

Freezing Option A *on the month-FE specification* freezes an answer to the within-calendar-month anomaly question. Nobody in the lab asked that question; the motivating literature (crude winter peaks, Goggins cold–HF, Liu 2020 cold-dominant AFs) asks the between-season one. The specification's continuous-temperature "nulls" must not be narrated as "temperature is unrelated to monthly first-event counts," and the survival of P04A/P04B must not be narrated as biology preferring official thresholds.

**Licensed alternative (human-gated):** pre-specify a seasonal-contrast model — winter indicator or annual harmonic as the exposure of interest, flu covariate, trend spline — as a *different estimand*, labelled as such, with its own confounding limits stated (anything seasonal and unmeasured contaminates it; that is the price of asking the seasonal question at all). Whether to add that estimand, and whether the live paper's identification paragraph should state the 81% SD collapse, are **Hogan / team Gate 3 choices**. No agent freeze.

### Audit-surviving sentence

> The calendar-month fixed-effect design removes 96% of mean-temperature variance (SD 4.70°C → 0.90°C) and with it the winter–summer contrast that motivates the study; its near-1 continuous-temperature count ratios therefore answer "does an anomalously warm month differ from a typical month of the same calendar position," not "is winter worse," and the concentration of nominal signals in the two extreme-day counts (retained residual variance 25–46%, versus 3.6–4.3% for smooth means) follows from that projection geometry rather than from biology preferring official thresholds.

---

## 8. Forbidden claims

- Do **not** tell Bob to drop month FE from the live paper; Hogan owns the weather/identification framing and the team owns Gate 3.
- Do **not** run or report a seasonal-contrast health model before a human nod; this memo licenses a pre-specification, not a result.
- Do **not** claim "winter kills" or any seasonal effect size — the seasonal estimand is currently unestimated with confounder adjustment.
- Do **not** call the anomaly nulls wrong; they correctly answer the anomaly question. The error would be presenting them as the seasonal answer.
- Do **not** invent HA counts, stroke rows, or new coefficients.

**Keep:** the projection identity (4.70 → 0.90°C, ~81%), the question-swap statement, and the geometry explanation for why only P04A/P04B can show signals.  
**Drop:** any Gate 3 wording that reads month-FE continuous-temperature nulls as "no temperature association."  
**Park:** the seasonal-contrast (winter indicator / harmonic + flu) pre-specification, pending Hogan and team Gate 3.
