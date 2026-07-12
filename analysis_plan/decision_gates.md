# Decision gates — Temperature–CVD project

Working decision gates for moving from the 17 July 2026 lab meeting to the first validated HA descriptive report and, later, the first inferential models.

**Principle:** Do not run analyses that depend on an unconfirmed HA schema. Do not inspect substantive coefficients before Gates 1–3 are closed.

Owners and dates below use placeholders where the meeting has not yet decided.

---

## Gate 1 — Schema and access

**Required before touching real outcomes.**

| Prerequisite | Status | Owner | Stop condition |
|---|---|---|---|
| HPC access (wet-ink complete; onboarding done) | Pending | Bob, Hogan, Roro | No real HA files until access is live |
| Data dictionary or masked/mock schema | Pending | Roro | Do not invent field meanings |
| Row / episode definition (incl. full meaning of DAE) | Open | Roro | Do not aggregate until row unit is known |
| Diagnosis position (principal vs any-position) | Open | Roro / Bishai | Do not lock ICD algorithms without this |
| Admission route / elective–emergency fields | Open | Roro | Do not infer route from ED-to-inpatient absence |
| Transfer and recurrence handling | Open | Roro | Prevent double-counting before descriptives |
| Medication / BMI timestamps | Open | Roro | Descriptive Table 1 only until timing known |
| Ethics / governance determination (IRB amendment?) | Open | **PI (Bishai)** | Bob does not decide IRB scope |

**Exit criterion:** Written confirmation (email, meeting notes, or data dictionary) covering the items above, plus live HPC access for Bob.

---

## Gate 2 — Outcome-data QC

**Required before regression.**

| Check | Purpose | Stop condition |
|---|---|---|
| Row counts and uniqueness | Establish extract size and keys | Unexplained duplicates → pause |
| Missing dates and fields | Bound usable sample | Critical date fields missing → pause |
| Impossible values | Catch coding / extract errors | Resolve with Roro before modelling |
| Duplicate episodes | Apply transfer/recurrence rules | Rules not applied → pause |
| Suppression / output rules | Never treat suppressed cells as zero | Rules unknown → do not release tables |
| Monthly outcome counts | First exposure–outcome merge readiness | Implausible seasonality unexplained → review |
| Age / sex distributions | Align with C&SD strata | Missing 65–69 / 70–74 → escalate |
| Coding discontinuities | Detect ICD or practice shifts | Document before modelling |
| COVID-era anomalies | Care-seeking / capacity shocks | Flag; do not over-interpret |
| Comparison against any available HA totals | External plausibility | Large unexplained gaps → pause |

**Exit criterion:** Validated HA data dictionary + QC report circulated and acknowledged; descriptive admission counts and age-specific rates reviewed; Table 1 Panel B completed under the agreed denominator.

---

## Gate 3 — Analysis-plan freeze

**Lock before inspecting substantive coefficients.**

| Item | Proposed default (pending confirmation) | Owner |
|---|---|---|
| Primary outcome | AMI / ischemic stroke / hemorrhagic stroke as separate endpoints (provisional ICD-9) | Bishai / team |
| Primary denominator | C&SD age–sex person-time (Table 110-01001; mid-year; monthly interpolated), unless a defined cohort exists | Bishai / Roro |
| Diagnosis definitions | Principal diagnosis if available; provisional ICD-9 lists in memo | Roro / Bishai |
| Primary exposure | Same-month Tmax / Tmin (Bishai 12 Jul direction); official extremes secondary | Bishai |
| Primary lag | Same-month initial; lag-1 as separate sensitivity | Bishai |
| Seasonality / trend strategy | Prespecify before coefficient inspection | Team / Bishai |
| Population offset | `log(population × days_in_month)` for admissions-only design | Bob (implement) |
| COVID sensitivity | Phase indicators as sensitivity / secondary; not required for first descriptives | Team / Bishai |
| Interaction hierarchy | Prespecify age / period interactions after core model stable | Team |
| Medication / BMI model role | Descriptive first; model use only if timing and at-risk structure support it | Bishai / Roro |

**Exit criterion:** Short written freeze note (ledger update or methods addendum) signed off by Professor Bishai before any coefficient review.

---

## Gate 4 — First model run

**Run only after Gates 1–3.**

Allowed at this gate:

- Count regression with population offset under the frozen admissions-only design; **or**
- Patient-month risk model **only if** Gate 1 confirmed a defined at-risk cohort with non-event follow-up.

Not allowed before this gate:

- Interpreting temperature coefficients as findings
- Comparing “effects” to historical daily DLNM studies as if methods were identical
- Treating synthetic workflow outputs as results

**Stop condition:** Any Gate 1–3 item reopens (e.g. new episode definition, denominator change) → return to the relevant gate before further modelling.

---

## Gate 5 — Extensions

**Only after the core model is stable.**

Deferred until Gates 1–4 are complete and the primary temperature–admission association is documented:

- Pollution (current file is placeholder)
- Influenza
- Multi-station weather
- District analysis
- 2024 extension
- Comorbidity / medication–BMI pathway extensions (if timing supports)

These are **not** selected as near-term analyses. They become candidates only after the core 2013–2023 temperature pathway is stable.

---

## Immediate work that does **not** wait on HA access

Bob can proceed now:

1. Complete wet-ink authorization.
2. Extend the weather build to include December 2012 for January 2013 lag-1.
3. Prepare HA descriptive / QC scripts against a masked or mock schema once available.
4. Draft Table 1 Panel B shell (blank cells; no invented numbers).
5. Keep the assumption ledger and these decision gates current after the 17 July meeting.

---

## Related documents

- `analysis_plan/assumption_ledger.md`
- `reports/post_meeting_next_steps.md`
- `reports/deck_final_audit.md`
- `memos/clarification_email_to_roro_final.md`
