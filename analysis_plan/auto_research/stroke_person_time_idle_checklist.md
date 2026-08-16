# Stroke / person-time idle checklist

**Date:** 16 August 2026  
**Status:** Stroke file not attached. Still-at-risk person-time not delivered. CHD/HF territory-month first-event counts are in hand (7 August).  
**Do not** invent rows, ICD lists, subtype availability, or coefficients while idle.

This is family F05 in [`approach_registry.yml`](approach_registry.yml). When a governed file arrives, stop Playbook 05 and run [`02_ha_data_arrival.md`](../playbooks/02_ha_data_arrival.md).

## Ranked Roro asks (unchanged)

1. Stroke monthly file (the missing attachment).
2. Still-at-risk person-time by month for the T2D/HTN cohort (people without a first CHD/HF hospitalisation yet).
3. Age bands 65–69, 70–74, 75+ as monthly counts, same event definition.
4. ICD inclusion list + inpatient vs DAE confirmation in writing.

Do not ask for daily outcomes, admission cause, medications, or microdata.

## First hour after a governed file arrives

1. **Do not commit the file.** Place it only on the governance-approved path. Record receipt date, original filename, SHA-256, transfer authority, and permitted use in `reports/data_receipt_YYYY-MM-DD.md`.
2. **Hash and inventory** every sheet, column, type, period, and apparent grain before renaming. Do not assign meaning from a column name.
3. **Map to schema, do not extend it from guesses.**
   - Stroke counts → [`schemas/ha_stroke_aggregate.schema.json`](../../schemas/ha_stroke_aggregate.schema.json) (`month_id`, `n_events` required; age/sex/subtype optional).
   - Person-time or age-banded CHD/HF → new documented fields; do not reuse the AMI/stroke `diagnosis_group` enum in [`schemas/ha_monthly_aggregate.schema.json`](../../schemas/ha_monthly_aggregate.schema.json) as if this extract were AMI.
4. **Grain.** Territory-month vs month × age × sex. Extra years, strata, or outcomes are quarantined until a team decision. Keep 2013–2023 as the core window.
5. **Suppression.** Suppressed or small cells are missing, never zero. Do not reverse-engineer complementary suppression.
6. **Dictionary stops.** If event-month semantics, inpatient vs DAE, ICD lists, or the still-at-risk definition are unknown, stop and ask Roro. Scripts must not supply a convenient default.
7. **QC before models.** For stroke-shaped files, the playbook command is `PATHWAY_MODE=real Rscript scripts/08c_qc_stroke_aggregates.R` only after the mapping is documented. Review duplicates, month coverage, impossible counts, and suppression. For person-time, document eligibility, risk-set entry and exit, first-event removal, and the measurement unit/date; require non-negative monthly counts aligned to 132 months or a stated gap. Do not treat a days-in-month offset as cohort person-time.
8. **No coefficients in hour one.** Descriptives and QC only. Gate 1–2 receipt note before any negative-binomial run. Gate 3 remains open; a new outcome does not freeze a primary.
9. **Update state, not the live paper’s Results.** CONTEXT_BOOTSTRAP, decision gates, open-questions log. Stroke stays out of the Hogan live Results until a real panel exists. Do not paste a parallel manuscript.

## If the file never arrives

Correct idle behaviour: keep stroke named and absent; keep the days-in-month offset; never call CHD/HF count ratios incidence. Incorrect: a synthetic stroke panel, a daily DLNM, or holding Stage 3 for an undelivered attachment (Stage 3 PDFs are already byte-locked on CHD/HF).

**Owner of the file:** Roro. **Owner of the ask:** Bob. **Agents** prepare this checklist and stop at the first unknown field meaning.
