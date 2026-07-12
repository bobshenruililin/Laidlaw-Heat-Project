# Post-meeting next steps — 17 July 2026 lab meeting

**Purpose:** Capture decisions and actions immediately after the meeting so the project can move without waiting on informal memory.  
**Status:** Template with placeholders — fill in after the meeting. Do not invent decisions.

---

## 1. Decisions made

| Topic | Decision | Source (who / when) | Notes |
|---|---|---|---|
| Analysis unit / denominator | _[TBD — admissions-only monthly rates vs patient-month cohort]_ | | |
| Primary exposure / lag sequence | _[TBD — same-month primary with lag-1 sensitivity?]_ | | |
| Diagnosis position | _[TBD — principal vs any-position]_ | | |
| Transfer / recurrence rule | _[TBD]_ | | |
| Medication / BMI role | _[TBD — descriptive only for now?]_ | | |
| IRB amendment needed? | _[TBD — PI decision]_ | | |
| Next lab deliverable date | _[TBD]_ | | |

---

## 2. Decisions still open

| Topic | Why still open | Blocker | Owner | Target date |
|---|---|---|---|---|
| Full meaning of DAE | Not expandable from current note | Needs Roro / data dictionary | Roro | _[TBD]_ |
| Exact row / episode unit | Schema not yet shared | Dictionary or masked mock | Roro | _[TBD]_ |
| Admission route fields | Not confirmed | Schema | Roro | _[TBD]_ |
| Meds / BMI field presence and dates | Not confirmed | Schema + governance | Roro / Bishai | _[TBD]_ |
| HPC access timing | Wet-ink pending | Signatures + onboarding | Bob / Hogan / Roro | _[TBD]_ |
| Small-cell suppression rules | Needed before releasing tables | Roro / HPC policy | Roro | _[TBD]_ |

---

## 3. Action register

| Action | Owner | Deadline | Depends on | Done? |
|---|---|---|---|---|
| Complete wet-ink signatures | Bob, Hogan | _[TBD]_ | — | |
| Onboard Bob to HPC | Roro | _[TBD]_ | Wet-ink | |
| Provide data dictionary or masked/mock schema | Roro | _[TBD]_ | — | |
| Clarify DAE, row unit, diagnosis position, admission route, transfers | Roro | _[TBD]_ | Dictionary preferred | |
| Confirm admissions-only vs defined cohort | Roro / Bishai | _[TBD]_ | Schema | |
| IRB determination | Professor Bishai | _[TBD]_ | Roro’s governance note | |
| Extend weather build to December 2012 | Bob | _[TBD]_ | — | |
| Prepare HA QC / descriptive scripts | Bob | _[TBD]_ | Mock schema helpful | |
| Draft Table 1 Panel B shell | Bob | _[TBD]_ | Agreed denominator | |
| Update assumption ledger after meeting | Bob | _[TBD]_ | Meeting notes | |
| Update `decision_gates.md` exit criteria | Bob | _[TBD]_ | Meeting notes | |

---

## 4. What Bob can do immediately

- Finish wet-ink paperwork.
- Extend processed HKO monthly file to include December 2012 (raw daily data already present).
- Keep merge / descriptive pipeline ready (`08b_merge_real_ha_panel.R` and related scripts).
- Draft blank Table 1 Panel B and QC checklist shells.
- Send concise clarification email requesting dictionary / masked schema (no patient data by ordinary email).
- Update the assumption ledger and decision gates with meeting outcomes.

---

## 5. What waits for HPC access

- Any touch of real HA outcomes.
- Row counts, uniqueness, missingness, and episode QC on the real extract.
- Descriptive admission counts, age-specific rates, and completed Table 1 Panel B.
- Any temperature–admission association estimate.

---

## 6. Branching paths after schema confirmation

### If the file is admissions-only

- Proceed with the **monthly admission-rate** default.
- Define valid episodes → aggregate by month × age × sex × diagnosis.
- Merge HKO exposures + C&SD person-time (mid-year MDT; monthly interpolated).
- Offset: `log(population × days_in_month)`.
- Describe meds/BMI in Table 1; do **not** treat them as automatic pre-exposure confounders until timing is known.
- Analysis-plan amendment: lock estimand as stratum-specific monthly admission rates (not patient-month risk).

### If a defined cohort with non-event follow-up exists

- Switch to a **patient-month risk** design (or hybrid, if advised).
- Confirm at-risk start/stop rules, censoring, and how non-event months are represented.
- Revisit medication/BMI timing relative to risk intervals.
- Analysis-plan amendment: replace population-rate offset with individual person-time; revise Table 1 denominator language.

---

## 7. Analysis-plan amendments required

After the meeting, update:

1. `analysis_plan/assumption_ledger.md` — close or re-open A03–A08, A27, A30, A37–A39 as decided.
2. `analysis_plan/decision_gates.md` — mark Gate 1 items resolved or blocked.
3. Methods draft estimand language — “monthly admission rates” vs “patient-month risk.”
4. Primary exposure / lag freeze note (Gate 3) once Bishai confirms.

Do **not** amend the plan to claim unconfirmed future extensions (pollution, district, 2024) as selected near-term work.

---

## 8. Next lab deliverable

**Target (after access + schema confirmation):**

Validated HA data dictionary and QC report; descriptive admission counts and age-specific rates; completed Table 1.

**Explicitly not the next deliverable:** causal or semi-causal regression results.

Regression begins only after the outcome definition and descriptive QC are approved (Gate 2 → Gate 3 → Gate 4).

---

## 9. Meeting-note capture (fill in live)

- Date/time: 17 July 2026
- Attendees: _[TBD]_
- Key quotes / rulings: _[TBD]_
- Follow-up email sent?: _[Y/N]_
- Ledger updated?: _[Y/N]_
