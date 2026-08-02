---
name: playbook-03-full-analysis
description: Execute the complete real-data pathway analysis after Gates 1–2 close and the governed merged panel is ready.
disable-model-invocation: true
---

# Playbook 03 — Full analysis

## Trigger phrases

- `/playbook-03-full-analysis`
- “Run playbook 03.”

## Preconditions

- [ ] Gates 1–2 document schema, governance, QC, coverage, merge integrity, and denominators.
- [ ] Outcome rows have verified real-data provenance and no synthetic outcomes.
- [ ] Weather-definition implementation status matches the registry.
- [ ] `HM23` is not called locked unless Playbook 01 is complete.
- [ ] The team is available to own Gate 3.

## Execution

Read [`analysis_plan/playbooks/03_full_analysis_run.md`](../../../analysis_plan/playbooks/03_full_analysis_run.md) first and follow it exactly. Run the versioned, registry-driven pathway and HM/CM panels; validate diagnostics and sample accounting; prepare the complete Gate 3 packet; and preserve null, discordant, skipped, and failed specifications. An agent cannot close Gate 3 alone.

## Done when

- Real pathway and HM/CM panels reproduce from versioned registries.
- Every estimate has an ID, provenance, contrast, sample size, and diagnostic status.
- Gate 3 is team-approved or explicitly open.
- Manuscript tables match frozen IDs and retain the auditable panel.
- No synthetic output appears in real results.

## Claim boundaries

These are ecological monthly associations, not individual causal effects, daily triggers, attributable fractions, or excess deaths. Never choose headline definitions by p-value or magnitude. “Robust” requires pre-specified consistency and acceptable diagnostics.

## Files to update

- `analysis_plan/pathway_registry.yml`
- `analysis_plan/hot_cold_month_registry.yml`
- `analysis_plan/statistical_analysis_protocol.md`
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/open_questions_log.md`
- `knowledge/CONTEXT_BOOTSTRAP.md`
- `outputs/reports/pathway_panel_summary.md`
- `outputs/tables/pathway_panel_estimates.csv`
- `outputs/tables/manuscript_pathway_panel_table.csv`
- A dated Gate 3 freeze and analysis-run note
