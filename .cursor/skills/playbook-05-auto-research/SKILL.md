---
name: playbook-05-auto-research
description: Run the Jin-adapted auto-research lab on the heat–CHD/HF project after an explicit command. Audits and prepares; does not invent findings or freeze Gate 3.
disable-model-invocation: true
---

# Playbook 05 — Auto-research lab

## Trigger phrases

- `/playbook-05-auto-research`
- “Run playbook 05.”
- “Run the auto-research lab.”

## Preconditions

- [ ] CONTEXT_BOOTSTRAP and the live claim ledger have been read.
- [ ] `heat_lab_prompt.txt` and `approach_registry.yml` have been read.
- [ ] Gate 3 is treated as open. This command does not close it.
- [ ] No new undelivered HA file is being silently modelled.

## Execution

Read [`analysis_plan/playbooks/05_auto_research_lab.md`](../../../analysis_plan/playbooks/05_auto_research_lab.md) first and follow it exactly. Use [`analysis_plan/auto_research/heat_lab_prompt.txt`](../../../analysis_plan/auto_research/heat_lab_prompt.txt) as the lab contract. Keep approach families from [`approach_registry.yml`](../../../analysis_plan/auto_research/approach_registry.yml) incompatible on purpose. Run `python3 scripts/50_audit_live_claim_ledger.py` before declaring the live file audited. Do not tell an independent adversary the favoured identification thesis until after its first unaided read. Do not paste into Hogan’s live file.

## Done when

- A dated `lab_run_YYYY-MM-DD.md` exists.
- The machine auditor has been run.
- Remaining gaps are human-owned and named.
- Hogan weather is unchanged.
- Stage 3 PDF and A0 poster were not rebuilt.

## Claim boundaries

This command audits and prepares. It does not freeze Gate 3, lock Hogan weather definitions, invent stroke or person-time rows, or promote a core contrast to a primary result. Do not assume a complete affirmative health proof exists.
