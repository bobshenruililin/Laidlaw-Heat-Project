# Speaker notes — Lab meeting 17 July 2026 (final)

**Presenter:** Bob Shen  
**Audience:** Professor Bishai, Roro, Hogan, and the lab  
**Target length:** ~8–10 minutes (main deck only; appendix on request)

Tone: prepared Laidlaw student; collaborative; propose defaults; ask seniors to confirm decisions that require their expertise. Do not present synthetic results as findings. Do not invent an expansion for “DAE.”

---

## Opening (~45 s)

> Following Professor Bishai's email, I completed the part that does not require HA access: the monthly HKO exposure file, its validation, and the environmental portion of Table 1. Roro's reply has also clarified the coding system, age-band availability, and access process. I will briefly show what is ready, one schema question that determines the model, and the first output I can produce once access is active.

Point briefly to the one-line status bar: READY exposure file; PENDING HA/HPC access and schema; TODAY analysis unit, lag plan, next deliverable.

Bridge: “Here is what is ready for the first merge.”

---

## Frame 2 — What is ready for the first merge (~1.5 min)

**Completed (my side):**
- HKO Headquarters, January 2013–December 2023
- 132 months; monthly mean / Tmin / Tmax and extreme counts
- Lag variables constructible; environmental Table 1 done; merge pipeline prepared

**Confirmed by Roro (credit naturally):**
- ICD-9
- Complete admission outcomes at patient level
- 65–69 and 70–74 available separately
- ED-to-inpatient episodes are not included in this extract
- HPC onboarding follows wet-ink authorization

Say the boundary once: “Current boundary: exposure file and merge pipeline are ready; real HA associations await HPC access and row-definition confirmation.”

Do **not** stack separate apology caveats. Keep it as project management.

---

## Frame 3 — Monthly temperature (~1 min)

Point to the ribbon: Tmin–Tmax range with monthly mean line.  
State briefly: HKO Headquarters; °C; N = 132 months; ends December 2023.

Footer already says: environmental exposure data only; no admission outcomes shown.

One sentence: “This is the exposure series we will merge once HA access is live.”

---

## Frame 4 — Table 1 is partly complete (~1.5 min)

**Panel A:** walk the means/SDs briefly; verified from `climate_monthly_2013_2023.csv`; unit = month; N = 132.

**Panel B:** grouped fields — patients/episodes; age/sex; medication fields; BMI. Say you will describe them as Professor Bishai requested.

On-slide sentence: variables can be described as requested; model role depends on at-risk population and pre-event timing.

In notes only: with admissions-only data, meds/BMI measured at or near admission are often not pre-exposure confounders. You are not rejecting these covariates — you need timing and cohort structure to use them correctly.

---

## Frame 5 — One schema question (~2 min)

This is the key design slide. Speak slowly; walk the vertical pathway.

Ask: admissions only, or a defined cohort with non-event follow-up?

**Proposed default (vertical flow):**
admissions-only → define valid episodes → aggregate month × age × sex × diagnosis → merge HKO + C&SD person-time → monthly admission-rate / count model.

**Alternative (small callout):** only if non-event follow-up exists → patient-month risk model.

Say: “Until the denominator is confirmed, I will talk about monthly admission counts or rates, not patient-level risk.”

Also say (notes): you will describe the requested covariates and will use them in models when the data structure and timing make that scientifically valid. The monthly population-rate default does **not** reject Professor Bishai’s requested covariates.

---

## Frame 6 — Temperature variables and lag plan (~1.5 min)

- Analysis file can carry same-month and lag-1 mean, Tmin, and Tmax (carrying ≠ putting all in one model).
- Same-month vs lag-1 Tmax: r ≈ 0.82 (exact 0.822489; 131 pairs).
- Fit temperature specifications separately rather than in one saturated model.
- Proposed sequence: same-month initial; lag-1 sensitivity; current/previous-month average secondary.
- Extend processed weather to December 2012 so January 2013 has valid lag-1.

**Decision for today (say aloud):** primary temperature metric — mean temperature, Tmin/Tmax, or extreme-day counts. Bishai asked to merge monthly max/min and lag; extreme-day counts remain available as secondary / staged options.

Explain briefly: same-month is proposed because historical heat–CVD work often finds short lags, and monthly aggregation already smooths daily timing. This does **not** reproduce a daily distributed-lag model.

---

## Frame 7 — Decisions that unlock the first HA report (~1.5–2 min)

Title softens the ask; group under three headings:

1. **Outcome and episode definition** — DAE; row unit; principal vs any-position; transfers/recurrence; admission route/elective status.
2. **Analysis population** — admissions-only vs defined cohort; medication/BMI dates and non-event follow-up; primary temperature metric.
3. **Access and governance** — wet-ink/HPC timing; IRB amendment (PI decision); output/disclosure review.

Assign actions verbally (not on slide):
- **Bob:** wet-ink; Dec 2012 weather extension; HA descriptive scripts; Table 1 Panel B shell
- **Roro:** data dictionary / masked schema; DAE / episode / denominator / meds-BMI clarification; onboard after signatures
- **Hogan:** wet-ink; station / pollution timing advice if asked
- **Professor Bishai:** design default, primary metric, lag sequence, covariate role, IRB path

---

## Closing (~30–45 s)

> My proposed first analysis remains the monthly admission-rate design: define valid episodes from the patient-level records, aggregate them by month, age, sex, and diagnosis, and merge them with HKO exposure and C&SD person-time. I will include current and lag-1 temperature in the analysis file and fit them as separate specifications. Once the row definition, governance path, and access are confirmed, I will return with the validated HA descriptives and completed Table 1 before fitting substantive models.

End on the deliverable box: validated HA data dictionary/QC report; descriptive counts and age-specific rates; completed Table 1. Regression only after outcome definition and descriptive QC are approved.

---

## Appendix (only if asked)

| Slide | Use when |
|---|---|
| A1 ICD-9 | Someone asks about diagnosis codes |
| A2 Validation table | Someone challenges annual extremes |
| A3 Detailed schema questions | Deep dive with Roro |
| A4 Pipeline | Someone asks what is already coded / C&SD status |
| A5 Full Table 1 shell | Someone wants the full covariate list |
| A6 Pollution / district / 2024 | Someone asks about extensions |

---

## Clarification email timing

Prefer sending `memos/clarification_email_to_roro_final.md` **after** the 17 July meeting so Bishai can reframe items first. If Roro needs advance notice, send only a short schema-item list, not the full memo.

---

## Phrases to use / avoid

**Use:** “I completed…”, “Roro has confirmed…”, “My proposed default is…”, “I would appreciate confirmation…”, “Current boundary…”, “Analysis file can carry…”, “Regression will begin only after…”

**Avoid:** interrogating Roro; “blocked” as the dominant narrative; implying synthetic results are findings; inventing a DAE expansion; implying Bob controls IRB/HA governance; reading every bullet; saying “merge includes” if it sounds like one saturated model.
