---
name: playbook-07-pr-board
description: Classify open PRs, close only superseded zero-unique science PRs, leave unique work open. Does not merge or freeze Gate 3.
disable-model-invocation: true
---

# Playbook 07 — PR board

## Trigger phrases

- `/playbook-07-pr-board`
- “Run playbook 07.”
- “Tidy the pull requests.”
- “Take care of the lots of PRs.”

## Preconditions

- [ ] `analysis_plan/pr_board_policy.yml` has been read.
- [ ] Living science PR is the policy `living_science_pr` (do not open a parallel science PR).
- [ ] Gate 3 is treated as open. This command does not close it.
- [ ] Unique files versus the living tip have been counted before any close.

## Execution

Read [`analysis_plan/playbooks/07_pr_board.md`](../../../analysis_plan/playbooks/07_pr_board.md) first and follow it exactly. Run `python3 scripts/69_pr_board.py --json`. Close a PR only when the policy action is `CLOSE_SUPERSEDED` **and** unique files vs `living_science_ref` are empty. Post a comment naming the successor. Do not merge. Do not close PR 68, 80, 75, 74, 73, 67, 66, 62, 61, 58, 53, or 46 unless a later policy revision and a unique-file check both say so.

## Done when

- `reports/pr_board_latest.md` exists.
- Close-ready PRs are closed or the board explains why not.
- Unique PRs remain open.
- Gate 3 is still OPEN.

## Claim boundaries

GitHub hygiene is not a scientific result. Do not freeze Gate 3, fit Model 2/3, or invent HA rows.
