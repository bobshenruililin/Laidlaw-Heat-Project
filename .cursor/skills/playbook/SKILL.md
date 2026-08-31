---
name: playbook
description: Route an explicit playbook command to the correct Laidlaw gate or emergency workflow.
disable-model-invocation: true
---

# Playbook router

## Trigger phrase

- `/playbook`

If Bob supplies no number or workflow, ask which playbook to run. Do not infer a gate from partial context.

| Command | Use when |
|---|---|
| `/playbook-01-hogan-lock` | Actual Hogan meeting notes or corrections are ready for the weather-definition lock. |
| `/playbook-02-ha-arrival` | A governed HA aggregate release, dictionary, or revision arrives. |
| `/playbook-03-full-analysis` | Gates 1–2 are closed and the real merged panel is ready. |
| `/playbook-04-final-writeup` | Gate 3, verified real results, diagnostics, and cleared tables are ready. |
| `/playbook-05-auto-research` | Jin-adapted lab: adversarial audit and readiness packets; does not invent findings or freeze Gate 3. |
| `/playbook-07-pr-board` | Classify open PRs; close only superseded zero-unique science PRs. Does not merge. |
| `/playbook-08-health-econ-lab` | Explore identification/HTA lab on synthetic schemas. Never writes CEA into the live file. |
| `/objective-audit` | Inherit-only BETTER/WORSE/MIXED audit. WORSE is allowed. |
| `/playbook-99-emergencies` | Source, scope, governance, definition, or provenance shocks interrupt normal work. |

Playbook **06** (scientific-search harness) lives on PR #68 and is not on this branch. Do not reuse the number 06 here.

After Bob chooses, open the named skill and its linked playbook. Check preconditions before execution, preserve human-owned gates, and stop at the first unmet scientific or governance boundary.

## Claim boundary

Routing a command does not prove its preconditions or authorize a human-owned decision. Never select a workflow merely to bypass a blocked gate.
