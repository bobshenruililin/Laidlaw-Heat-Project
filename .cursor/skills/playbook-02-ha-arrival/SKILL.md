---
name: playbook-02-ha-arrival
description: Execute governed Hospital Authority aggregate receipt, schema mapping, QC, and real-panel preparation when a release arrives.
disable-model-invocation: true
---

# Playbook 02 — HA data arrival

## Trigger phrases

- `/playbook-02-ha-arrival`
- “Run playbook 02.”

## Preconditions

- [ ] The PI/governance-approved route and permitted use are documented.
- [ ] Received files are approved aggregates, not microdata.
- [ ] Their storage path is approved.
- [ ] Roro or the sender can resolve dictionary, timing, suppression, and release questions.
- [ ] The aggregate schema, decision gates, and scientist runbook have been read.

## Execution

Read [`analysis_plan/playbooks/02_ha_data_arrival.md`](../../../analysis_plan/playbooks/02_ha_data_arrival.md) first and follow it exactly. Preserve originals and never commit HA data. Execute receipt, inventory, source-to-schema mapping, QC, merge checks, and gates in order. Stop on undocumented field meaning, event-month semantics, grain, suppression, governance, or major coverage gaps.

## Done when

- The original release is preserved at the approved, untracked path.
- Field meanings, grain, timing, coverage, subtype, suppression, and population universe are documented.
- Gates 1–2 have an evidence-backed close or explicit stop.
- The merged panel reconciles to aggregates and denominators.
- Real mode contains no synthetic outcome.

## Claim boundaries

QC is not an association result. Report release details only within disclosure rules. Never infer admission reasons, subtype, event timing, zeroes, or unsuppressed values from undocumented fields. Do not publish coefficients before Gate 3.

## Files to update

- `outputs/reports/stroke_data_qc_receipt.md`
- `outputs/tables/stroke_qc_summary.csv`
- `schemas/ha_stroke_aggregate.schema.json` and `schemas/README.md` when warranted
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/open_questions_log.md`
- `knowledge/CONTEXT_BOOTSTRAP.md`
- A dated `reports/data_receipt_YYYY-MM-DD.md` or meeting/QC debrief
