---
name: playbook-08-health-econ-lab
description: Explore-only health-econ identification lab on synthetic schemas. Never writes TWFE/CEA into the live manuscript. Does not freeze Gate 3.
disable-model-invocation: true
---

# Playbook 08 — Health-econ identification lab

## Trigger phrases

- `/playbook-08-health-econ-lab`
- “Run playbook 08.”
- “Health-econ PhD workflow.”
- “DAG / IV / RDD / CEA on this repo.”

## Preconditions

- [ ] CONTEXT_BOOTSTRAP and `.cursorrules` have been read.
- [ ] Governed `*_analysis_panel.csv` files will not be opened.
- [ ] Live manuscript will not be edited by this command.
- [ ] Gate 3 is treated as open.

## Execution

Read [`analysis_plan/playbooks/08_health_econ_identification_lab.md`](../../../analysis_plan/playbooks/08_health_econ_identification_lab.md) first. Use [`analysis_plan/health_econ/identification_lab_prompt.txt`](../../../analysis_plan/health_econ/identification_lab_prompt.txt) and [`dag_this_extract.md`](../../../analysis_plan/health_econ/dag_this_extract.md). Bind code to `data_processed/samples/SYNTHETIC_chd_hf_schema.csv`. Do **not** default to TWFE, Callaway & Sant'Anna, Medicaid DiD, or QALY text in the journal track. Named Max seats may be missing; use inherit auditors. Closed PR 54 is prior residue, not a finding.

## Done when

- A dated note exists under `analysis_plan/health_econ/`.
- Outputs are labelled `SYNTHETIC`.
- Live file and Hogan weather paragraph are unchanged.
- Gate 3 remains OPEN.

## Claim boundaries

This command trains identification and DUA hygiene. It produces no CHD/HF coefficient and no Hong Kong QALY.
