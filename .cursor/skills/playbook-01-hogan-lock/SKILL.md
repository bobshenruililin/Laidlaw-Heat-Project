---
name: playbook-01-hogan-lock
description: Execute the post-Hogan-meeting weather-definition lock after actual notes or written corrections are available.
disable-model-invocation: true
---

# Playbook 01 — Hogan definition lock

## Trigger phrases

- `/playbook-01-hogan-lock`
- “Run playbook 01.”

## Preconditions

- [ ] Actual Hogan meeting notes, a completed decision sheet, or written corrections exist.
- [ ] Hogan’s words, team decisions, proposals, and unresolved questions can be distinguished.
- [ ] The current registry, catalogue, and weather-definition canon have been read.
- [ ] A blank decision sheet is not being treated as evidence.

## Execution

Read [`analysis_plan/playbooks/01_hogan_definition_lock.md`](../../../analysis_plan/playbooks/01_hogan_definition_lock.md) first and follow it exactly. Execute its steps in order. Do not fill missing decisions from defaults. If a precondition fails, stop at that boundary, name the missing evidence and owner, and record the unresolved item where the playbook requires.

## Done when

- A dated debrief separates decisions, proposals, and open questions.
- `HM23` is fully executable or explicitly pending.
- Registry, catalogue, canon, ledger, gates, state, and knowledge agree.
- The selected-month audit is reproducible.
- Hogan and Roro have a correction-friendly record.

## Claim boundaries

This command locks exposure definitions; it creates no health finding. Exposure prevalence, selected months, and event counts are not stroke associations. Do not infer thresholds, adaptation, or stroke effects.

## Files to update

- `reports/meeting_debrief_YYYY-MM-DD.md`
- `analysis_plan/hot_cold_month_registry.yml`
- `analysis_plan/hot_cold_month_catalogue.md`
- `knowledge/canon_weather_definitions.md`
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `knowledge/open_questions_log.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/CONTEXT_BOOTSTRAP.md`
- `knowledge/INDEX.md`
