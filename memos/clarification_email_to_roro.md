# Clarification email to Roro

**From:** Bob Shen  
**To:** Roro  
**Cc:** Professor David Bishai; Hogan  
**Subject:** Follow-up after your 12 July note — a few definitions before the first HA descriptive report  
**Date:** (send after / around the 17 July lab meeting, or before if Roro prefers async)

---

Dear Roro,

Thank you again for the 12 July clarifications. They were very helpful: ICD-9, patient-level admission information, separate 65–69 and 70–74 bands, and the confirmation that ED-to-inpatient episodes are not in this extract. I have updated the 17 July lab deck accordingly and credited your note.

I am preparing the first **validated HA descriptive report** (counts, missingness, episode definitions, age-specific rates, and Table 1). Before I touch the extract on HPC, I would be grateful for a short confirmation on the following definitional points. These are follow-ups, not a reopening of what you already answered.

## 1. DAE and row / episode definition

You noted that DAE records are included. I do **not** want to guess the expansion. Could you please confirm what “DAE” refers to in this ICD-9 extract, and whether each row is one admission episode?

## 2. Principal diagnosis, admission route, transfers, and recurrence

For the first descriptive pass, my working proposal is:

- primary counts based on **principal diagnosis** if the field is available;
- clarify whether elective inpatient admissions are in scope given that ED-to-inpatient episodes are excluded;
- ask how transfers and same-patient recurrence should be handled so we do not double-count episodes.

I would appreciate your preferred rules, or the fields I should use to implement them.

## 3. Admissions-only dataset versus defined at-risk cohort

This determines the analysis design:

- **Admissions-only + C&SD person-time** → monthly admission-rate (Negative Binomial) design — my proposed default;
- **Defined cohort with non-event follow-up / patient-months** → patient-month risk design.

Could you confirm which of these the extract supports? Until the denominator is clear, I will describe outcomes as monthly admission counts/rates rather than “patient-level risk.”

## 4. Medication / BMI timing (and IRB)

Professor Bishai asked that Table 1 include age, sex, diuretics, beta blockers, metformin, SGLT2 inhibitors, and BMI. I will include these **descriptively** as requested.

For modelling, I need to know:

- whether these fields are already on the approved extract;
- whether medication dates and BMI measurement dates are available;
- whether measurements can be shown to precede the admission event.

Separately, you raised whether the IRB protocol should be updated. I will follow whatever Professor Bishai decides as PI; I am not seeking to change governance myself.

## Access

Hogan and I will complete the wet-ink signatures as arranged. Once that is done, I would be grateful for onboarding to the HPC environment so I can produce the descriptive report without causal claims.

Happy to take this by email or briefly after the lab meeting — whichever is easiest for you.

Best regards,  
Bob Shen  
Laidlaw Scholar  
The University of Hong Kong
