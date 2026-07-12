# Speaker notes — Lab meeting 17 July 2026

**Presenter:** Bob Shen  
**Audience:** Professor Bishai, Roro, Hogan, and the lab  
**Target length:** ~8–10 minutes (main deck only; appendix on request)

Tone: prepared first-time Laidlaw researcher; collaborative; propose defaults; ask seniors to confirm decisions that require their expertise. Do not present synthetic results as findings. Do not invent an expansion for “DAE.”

---

## Title / opening (~30 s)

“Thank you — this is a short progress update. I completed the monthly HKO exposure file and Table 1 Panel A. Today I want to confirm three things: the exposure file, the analysis unit and denominator, and the HA schema / access / governance steps so we leave with a clear path to the first validated HA descriptive report.”

---

## Slide 1 — Purpose (~45 s)

Read the three objectives. Emphasize that this meeting is about locking definitions before real admission analysis, not about causal results.

Bridge: “I’ll start with what is already confirmed.”

---

## Slide 2 — What is now confirmed (~1.5 min)

**Exposure side (I completed):**
- HKO Headquarters, January 2013–December 2023
- 132 months; monthly mean / Tmin / Tmax and extreme counts
- Annual extremes validated 33/33 against HKO *Year’s Weather*

**HA side (credit Roro):**
- ICD-9 confirmed
- Patient-level admission information confirmed
- 65–69 and 70–74 available separately
- No ED-to-inpatient episodes in this extract

**Pending:**
- Wet-ink / HPC access still in progress
- No real admission analysis yet

Say explicitly: “Roro’s clarifications answered the main structural questions. What remains are definitional follow-ups — DAE, denominator, and meds/BMI timing — not gaps in the reply.”

---

## Slide 3 — Temperature visualization (~1 min)

Point to the ribbon: Tmin–Tmax range with monthly mean line.  
State: HKO Headquarters; °C; N = 132 months; ends December 2023; environmental exposure data only.

One sentence: “This is the exposure series we will merge once HA access is live.”

---

## Slide 4 — Table 1 structure (~1.5 min)

**Panel A:** walk the means/SDs briefly; note they are verified from `climate_monthly_2013_2023.csv`.

**Panel B:** list requested fields as pending. Say you will include age, sex, diuretics, beta blockers, metformin, SGLT2 inhibitors, and BMI descriptively as Professor Bishai requested.

Critical line: “Panel A has 132 month-level observations; Panel B will have a patient-, admission-, or patient-month-level denominator. I will not put them under one undifferentiated N.”

On medications/BMI: “Their model role depends on whether we have a true at-risk cohort, whether measurements precede the event, and whether dates are available. I am not rejecting these covariates — I need the information to use them correctly.”

---

## Slide 5 — Analysis design fork (~2 min)

This is the scientific correction slide. Speak slowly.

**Left path (proposed default):**
patient-level HA records → define episodes → aggregate month × age × sex × diagnosis → merge HKO + C&SD person-time → Negative Binomial monthly admission-rate model.

**Right path:**
only if a defined cohort with non-event follow-up exists → patient-month risk model.

Say: “Until the denominator is defined, I will call this monthly admission counts or rates, not patient-level risk.”

Proposed default: “Retain the original monthly population-rate design unless the HA extract contains a defined at-risk cohort. I would appreciate confirmation.”

---

## Slide 6 — Lags and model ladder (~1.5 min)

- Contemporaneous and lag-1 can both be added to the merge.
- Current vs lag-1 Tmax: r ≈ 0.82 (verified; 131 pairs).
- Proposed ladder: same-month primary; lag-1 separate sensitivity; current/previous-month average secondary.
- Do not put mean, Tmin, Tmax, and all lags in one initial model.

On December 2012: “Daily HKO data for December 2012 exist in the raw extracts, but the processed monthly file starts January 2013, so January 2013 lag-1 is currently missing. I recommend extending the weather build to December 2012.”

Close with: “I propose this model ladder and would welcome confirmation.”

---

## Slide 7 — Confirmations and next deliverable (~1.5–2 min)

Group the four headings; do not turn this into an interrogation.

Assign actions briefly:
- **Bob:** wet-ink; Dec 2012 weather extension; descriptive scripts; Table 1 Panel B shell
- **Roro:** DAE / episode / denominator / meds-BMI clarification; onboard after signatures
- **Hogan:** wet-ink; station / pollution timing advice
- **Professor Bishai:** design default, model ladder, covariate role, IRB path

End exactly: “Next deliverable: validated HA descriptive counts, missingness, episode definitions, age-specific rates, and completed Table 1. No causal claims.”

---

## Appendix (only if asked)

| Slide | Use when |
|---|---|
| A1 ICD-9 | Someone asks about diagnosis codes |
| A2 Validation table | Someone challenges annual extremes |
| A3 Detailed questions | Deep dive with Roro |
| A4 Pipeline | Someone asks what is already coded |
| A5 Full Table 1 shell | Someone wants the full covariate list |
| A6 Pollution / district | Someone asks about extensions |

---

## Phrases to use / avoid

**Use:** “I completed…”, “Roro has confirmed…”, “My proposed default is…”, “I would appreciate confirmation…”, “This determines whether…”

**Avoid:** “What does this mean?” without context; “I am unsure what Professor prefers”; “blocked” as the dominant narrative; implying Roro’s reply was inadequate; presenting synthetic results as findings; implying Bob controls IRB/HA governance.
