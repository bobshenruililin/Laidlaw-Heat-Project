# Draft — status report to Professor Bishai (Stage 3 + science)

**To:** Professor David Bishai  
**Subject:** Laidlaw Stage 3 status, current analysis, and three decisions  
**Attach:** `outputs/Laidlaw_Stage3_Research_Report_Shen.pdf`  
**Optional if he asks:** `reports/gate3_decision_packet_2026-08-07.md` (internal; not the Laidlaw submission)

Do not attach HA source files, release CSVs, or the poster unless he requests the poster.

---

Dear Professor Bishai,

I am writing with a Stage 3 status note and three decisions that only you can close. The research report is attached.

**Where the analysis is.** Roro released monthly CHD and HF first-hospitalisation counts for the 2013–2023 T2D/HTN cohort (first hospitalisation after first diagnosis; admission cause not recorded). Stroke was named in that email but not attached. We completed the pre-specified monthly panel: 132 months, separate negative-binomial models, calendar-month and trend controls, days-in-month offset. After multiplicity correction, all twelve core q-values exceed 0.19. Two residual patterns are visible and exploratory: HF with cold days, CHD with hot nights. The CHD result is sensitive to the uncertainty method. I am not asking you to freeze a confirmatory headline.

A method that tries to recover daily effects from monthly outcomes failed its simulation gate, so we are not reporting daily coefficients. That matches the data we actually have.

**What the counts themselves show, before any thermal model.** First-event totals fall by about half from 2013 to 2023 (CHD 23,830 → 12,323; HF 4,336 → 2,296), with a further dip in 2020. That is the expected shape of a first-hospitalisation construction, plus pandemic care-seeking. The C&SD age-35+ offset is ecological, not T2D/HTN person-time still at risk. I would rather keep calling these count ratios than incidence rates unless a cohort denominator can be released.

**Stage 3.** The accessible research report and A0 portrait poster are built. I still need the official HKU report form, your comments/endorsement, and written confirmation that these disclosure-minimised aggregate results may be used in the Laidlaw submission. I will not complete supervisor fields myself.

**Three decisions I would value:**

1. **Dissemination / IRB.** Roro asked in July whether additional HA aggregate work needed a protocol update. May the attached report go to `laidlaw@hku.hk` after your endorsement?

2. **Stroke this month.** If a monthly stroke file can arrive in the next two weeks, the same pipeline can run it. If it cannot, I will submit Stage 3 on CHD/HF and keep stroke as a named pending layer. Waiting without a file would only freeze the report.

3. **Highest-leverage extra aggregate, if any.** Patient-level covariates from the July Table 1 list (medications, BMI) are not in the released month totals. Two monthly aggregates would change the paper more than another thermal definition: (a) still-at-risk cohort person-time by month; (b) age bands 65–69 / 70–74 / 75+, which Hogan has asked to make visible. I can ask Roro if you agree those are worth a request.

Hogan and I are meeting on the weather Methods and the live manuscript. I will not overwrite his weather section.

Thank you for the supervision this summer.

Best,  
Bob

---

## Internal crib (do not paste)

- Gate 3 recommendation remains Option A (no confirmatory primary). Human freeze only.
- Flu and NO₂ are strong co-predictors in the original pathway table; they are competing explanations, not new thermal discoveries.
- July Table 1 (age, sex, meds, BMI) is still unpaid as patient-level adjustment. Be honest: aggregates cannot do it.
- If he wants numbers: HF cold days 1.073 (1.006–1.144), q = 0.192, SE-concordant; CHD hot nights 1.022, q = 0.192, Model/HC1 include 1.
