# Playbook 05 — Auto-research lab

## Trigger

Run when Bob (or an agent under an explicit `/playbook-05-auto-research` command) wants a Jin-shaped multi-agent research institute applied to the heat–CHD/HF project: branching approach families, adversarial audit, open provenance, and a stop rule that forbids “best effort” science.

Do **not** run this playbook as a search for a protected thermal finding.

## Preconditions

- [`knowledge/CONTEXT_BOOTSTRAP.md`](../../knowledge/CONTEXT_BOOTSTRAP.md) and [`manuscript/live_collaborative/claim_ledger.md`](../../manuscript/live_collaborative/claim_ledger.md) have been read.
- [`analysis_plan/auto_research/heat_lab_prompt.txt`](../auto_research/heat_lab_prompt.txt) and [`approach_registry.yml`](../auto_research/approach_registry.yml) have been read.
- The live wording authority is [`manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`](../../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md). Hogan’s weather paragraph is already in that file.
- Gate 3 is **open**. Playbook 04’s freeze precondition is not met. This lab does not close it.
- No new HA microdata, stroke file, or still-at-risk person-time is required to start. If those files arrive, stop this playbook and run Playbook 02.

## Adapted stop rule

Return only when all three hold:

1. The identification article’s quantitative sentences survive adversarial audit against frozen tables (machine auditor green, or every red item has a named source-file contradiction).
2. Every remaining hole is labelled **human-owned** with an owner (Hogan / Roro / Bishai / Bob).
3. No agent has filled a hole by invention (no stroke coefficients, no daily DLNM, no Gate 3 freeze, no Hogan weather rewrite, no health-econ in the paper body).

Partial scientific progress is allowed only as a **named gap**, never as a coefficient. Do not copy Jin’s “assume a complete affirmative proof exists.”

## Steps

1. Read the lab prompt and the approach-family registry. Keep the six families alive in parallel. Do not tell an independent adversary the favoured identification thesis until after its first read of the live file.
2. Run `python3 scripts/50_audit_live_claim_ledger.py` against the live Markdown and `manuscript/live_collaborative/claim_ledger.yml`. A red auditor is a stop, not a prompt to invent a matching number.
3. Launch named subagents by family, not by wording. Root agent synthesises, challenges, and redirects. An adversary may kill a family only with a **table contradiction** or a **forbidden-claim hit**.
4. Write `analysis_plan/auto_research/lab_run_YYYY-MM-DD.md`: families tried, killed, still alive; auditor result; exact remaining human gaps.
5. If weather definitions remain unlocked, refresh the Hogan-lock **readiness** pack only: pending vs already in the registry. Do not execute Playbook 01. A blank decision sheet is not a lock.
6. If stroke or person-time is still missing, refresh the idle-state checklist (schema, QC, first hour after a file arrives). Do not invent rows.
7. Deposit residue: knowledge entry, `context_compound_log.md` row, and pointers in CONTEXT_BOOTSTRAP / INDEX. Do not start a parallel manuscript. Do not paste into Hogan’s live file. Do not email the Outlook thread.

## Done when

- A dated lab-run note exists.
- The machine auditor has been run and its log is in the lab-run note or `outputs/`.
- Remaining gaps are human-owned and named.
- Hogan weather is unchanged.
- Stage 3 PDF and A0 poster were not rebuilt.

## Failure modes

- Treating this playbook as a 16-hour search for a Nature finding or a confirmatory primary.
- Isolating agents from Goggins, Guo, both Liu papers, or Hogan’s weather paragraph (those are the spine, not contamination).
- Killing an inconvenient sensitivity because it is inconvenient, rather than because a table contradicts it.
- Filling Gate 3, authorship, IRB, ICD/inpatient semantics, or weather-lock blanks from defaults.
- Writing health-econ Monte Carlo or `SYNTHETIC_THEORY` into the journal-track live file.
- Overwriting “Meteorological data was obtained from the HKO.”

## Which files to update

- `analysis_plan/auto_research/lab_run_YYYY-MM-DD.md`
- `analysis_plan/auto_research/hogan_lock_readiness.md` when the registry status changes
- `analysis_plan/auto_research/stroke_person_time_idle_checklist.md` when receipt rules change
- `analysis_plan/context_compound_log.md`
- `knowledge/CONTEXT_BOOTSTRAP.md`, `knowledge/INDEX.md`, and a dated knowledge entry
- `manuscript/live_collaborative/claim_ledger.yml` only when a verified numeral or source path changes

## Claim boundaries

This playbook audits and prepares. It does not freeze Gate 3, lock Hogan weather definitions, invent undelivered HA fields, or promote any core contrast to a primary result. The live collaborative pack remains the journal-track authority; paste remains a human step.
