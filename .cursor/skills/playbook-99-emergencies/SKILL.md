---
name: playbook-99-emergencies
description: Execute the emergency workflow when source, scope, governance, definition, or provenance shocks invalidate normal work.
disable-model-invocation: true
---

# Playbook 99 — Emergencies

## Trigger phrases

- `/playbook-99-emergencies`
- “Run playbook 99.”

## Preconditions

- [ ] The affected analysis or writing has stopped at the uncertain boundary.
- [ ] Original inputs, outputs, registries, and source versions are preserved.
- [ ] The human owner is identified.
- [ ] Urgency is not being used to invent fields, parameters, decisions, or findings.

## Execution

Read [`analysis_plan/playbooks/99_emergencies.md`](../../../analysis_plan/playbooks/99_emergencies.md) first and follow it exactly. Select the matching shock path, preserve and version evidence, return decisions to the named human owner, and create the dated incident or amendment record. Never move HA data to bypass a governance/path problem or fix synthetic contamination by relabelling.

## Done when

- The uncertain or contaminated workflow is stopped and bounded.
- Original versions and provenance are preserved.
- Required human decisions are recorded.
- Registries, manifests, outputs, manuscript, state, and knowledge identify the corrected version.
- A clean re-run or explicit no-run decision is documented.

## Claim boundaries

Emergency work may establish provenance, invalidate an artifact, or justify a sensitivity; it creates no scientific evidence. Governance fixes do not validate unknown fields, anomaly checks do not establish biology, and synthetic outputs remain non-findings.

## Files to update

- A dated `reports/incident_YYYY-MM-DD.md`, source diff, or amendment note
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `analysis_plan/pathway_registry.yml`
- `analysis_plan/hot_cold_month_registry.yml`
- `analysis_plan/statistical_analysis_protocol.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/open_questions_log.md`
- Affected source canons or manifests
- `knowledge/CONTEXT_BOOTSTRAP.md`
- Affected outputs and manuscript only after correction
