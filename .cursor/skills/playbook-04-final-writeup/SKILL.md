---
name: playbook-04-final-writeup
description: Execute final manuscript or Stage 3 writing after verified real results, diagnostics, Gate 3 approval, and disclosure clearance.
disable-model-invocation: true
---

# Playbook 04 — Final write-up

## Trigger phrases

- `/playbook-04-final-writeup`
- “Run playbook 04.”

## Preconditions

- [ ] Outputs carry `REAL` or `HA_APPROVED_AGGREGATE` provenance and no synthetic rows.
- [ ] Gates 1–3 are closed for the proposed claims.
- [ ] Complete pathway and HM/CM results, diagnostics, and sample accounting are checked.
- [ ] Tables are disclosure-cleared.

## Execution

Read [`analysis_plan/playbooks/04_final_writeup.md`](../../../analysis_plan/playbooks/04_final_writeup.md) first and follow it exactly. Also engage and follow the [`cns-writing`](../cns-writing/SKILL.md) skill. Build the claim ledger before prose, reconcile every value to machine-readable outputs and the Gate 3 note, represent the full panel fairly, then run the CNS checklist and contradiction audit.

## Done when

- Results and Discussion use only verified real estimates.
- Every quantitative claim traces to a cleared output with the correct contrast and sample.
- Completed-study prose replaces planning and draft language.
- Null and discordant evidence is represented fairly.
- The prose passes the CNS-writing checklist and Hogan register.

## Claim boundaries

Report bounded ecological monthly stroke-aggregate associations only. Do not imply individual causality, daily lag-response effects, mortality attributable fractions, or excess deaths. Keep literature estimates tied to their source population, period, outcome, and model.

## Files to update

- `reports/laidlaw_stage3/essay_lit_methods.md`
- The PDF/export only after Markdown is final
- Manuscript tables and figure legends under `outputs/`
- `analysis_plan/PROJECT_STATE.md`
- `analysis_plan/assumption_ledger.md` and the SAP amendment log if methods changed
- `knowledge/CONTEXT_BOOTSTRAP.md`
- `knowledge/INDEX.md`
- A dated publication-register knowledge entry
