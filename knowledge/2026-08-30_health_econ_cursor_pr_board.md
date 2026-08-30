# Cursor health-econ rails and PR board (30 August 2026)

**Mode:** Ship / Decide. Not a Gate 3 freeze. Not a Model 2/3 health fit. Not a QALY finding.

## Why this entry exists

Bob asked to automate prior scientific-honesty advice (objective audit, Gate 3 still open, Model 2/3 drop-in only) **and** to take care of ~18 open PRs, while adapting a generic “Cursor + Grok 4.6 for a health-econ PhD” checklist to this repository. Named Fable/Sol Max subagents remain unavailable; inherit auditors and tripwire scripts substitute.

## What is confirmed

1. This extract’s identification is ecological monthly negative-binomial count ratios with a Newey–West ladder, not staggered DiD. Generic TWFE / Callaway / Medicaid / QALY defaults would be a category error in the live Methods.
2. DUA zero-ingestion is now in `.cursorignore` (governed `*_analysis_panel.csv`, HA placeholder, `*.dta`). Pipeline mocking uses `data_processed/samples/SYNTHETIC_chd_hf_schema.csv` (8 rows, `data_status = SYNTHETIC`).
3. Playbook 07 + `scripts/69_pr_board.py` classify open PRs. Close rule: policy `CLOSE_SUPERSEDED` **and** zero unique files versus `origin/cursor/model23-gate3-b75b`. Living science PR is **#82**. Closed this session (not merged): #81, #79, #78, #77, #69 (already in `main` via #71). Open stack is 13.
4. Playbook 08 + DAG sketch + identification prompt revive the *idea* of closed PR 54 without dumping Monte Carlo into the journal track.
5. `/objective-audit` + `scripts/71_objective_audit_tripwires.py` encode WORSE-allowed inherit audit. Forbidden Discussion phrases remain absent (`can inform four`, `sits with official`).
6. Gate 3 is still OPEN. Table 2 numbers are unchanged. Governed panels remain absent.

## What remains open

- Human merge of PR #82 (this branch).
- Port-or-keep for unique CONFLICTING PRs: 75, 74, 73, 68, 67, 66, 62, 61, 58, 53, 46, and MERGEABLE unique #80 (Fukuda).
- Hogan weather lock, Roro stroke/person-time/ICD, Bishai Gate 3, Model 2/3 fit after drop-in.
- Named Max seats if quota returns; not required for Playbook 07/08.

## Claim boundary

Cursor rules are workflow constraints. They are not a causal design for Hong Kong hospitalisations and not a health-technology assessment of HHAP.
