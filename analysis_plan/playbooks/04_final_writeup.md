# Playbook 04 — Final write-up

## Trigger

Run when verified real estimates, diagnostics, a team-approved Gate 3 freeze, and disclosure-cleared tables are available for the Stage 3 essay or manuscript.

## Preconditions

- Outputs contain `REAL` or `HA_APPROVED_AGGREGATE` provenance and no synthetic rows.
- Gates 1–3 are closed for the claims to be written.
- The complete pathway panel, HM/CM results, diagnostics, and sample accounting have been checked.
- The canonical essay is [`reports/laidlaw_stage3/essay_lit_methods.md`](../../reports/laidlaw_stage3/essay_lit_methods.md).

## Steps

1. Engage the [`cns-writing`](../../.cursor/skills/cns-writing/SKILL.md) skill. Read [`writing_standards_hogan.md`](../writing_standards_hogan.md) and the current canonical essay before editing.
2. Build a claim ledger from verified outputs. For every proposed sentence, record the outcome, exposure contrast, pathway/definition ID, estimate, confidence interval, sample, provenance, diagnostic caveat, and source table.
3. Reconcile all reported values against the machine-readable result tables and Gate 3 note. Stop on discrepancies; do not choose whichever version reads better.
4. Update the title, Abstract, Aims, and Methods only where the completed analysis differs from the planned text. Preserve the monthly ecological estimand and exact exposure/outcome definitions.
5. Add a `Results` section only after Step 3. Report cohort/panel coverage, missingness, exposure prevalence, primary estimates with confidence intervals, diagnostics, and the pre-specified sensitivity panel. Include null and discordant results without significance-count rhetoric.
6. Add a `Discussion` section that begins with the principal bounded result, then situates it against Jingwen Liu et al. (2020), Zhenyuan Liu et al. (2026), Goggins, and the definition literature without equating their estimands.
7. Update limitations for monthly aggregation, ecological exposure, governed aggregate resolution, residual confounding, model information limits, COVID-era utilisation, suppression, and definition uncertainty actually encountered.
8. Credit scientific contributions by role in the body where they determine methods or outcome construction. Use formal citations for published work and full names in acknowledgements when appropriate.
9. Remove all draft markers, future tense for completed work, internal gate/process language, synthetic references, and administrative logistics from the scientific body. Do not write “results forthcoming” or preserve planned language after results exist.
10. Audit tables, figure legends, supplement references, title/abstract numbers, citations, and acknowledgements against the claim ledger. Apply disclosure rules before export.
11. Run the CNS-writing checklist and a final contradiction search across the essay, Project State, Gate 3 note, and outputs. Update the dated knowledge entry and project state only after the manuscript facts agree.

## Done when

- The canonical essay contains complete Results and Discussion based only on verified real estimates.
- Every quantitative claim traces to a disclosure-cleared output and matches its contrast and sample.
- Planned-procedure and draft language has been replaced by completed-study prose.
- The whole panel, including null and discordant evidence, is represented fairly.
- The prose meets the CNS-writing checklist and Hogan’s spare register.

## Failure modes

- Writing Results from exposure-only graphs, synthetic runs, or unverified intermediate tables.
- Updating the Abstract but leaving contradictory planned language in Methods or Limitations.
- Calling monthly stroke associations a replication of daily mortality work.
- Reporting only favourable definitions, adjustment stages, periods, or subgroups.
- Using internal nicknames or collaborator names in place of formal citations.
- Hiding governance or disclosure limits behind vague prose.

## Which files to update

- `reports/laidlaw_stage3/essay_lit_methods.md`
- The corresponding PDF/export only after the Markdown is final
- Manuscript tables and figure legends under `outputs/`
- `analysis_plan/PROJECT_STATE.md`
- `analysis_plan/assumption_ledger.md` and SAP amendment log if methods changed
- `knowledge/CONTEXT_BOOTSTRAP.md`
- `knowledge/INDEX.md` and a dated publication-register entry

## Claim boundaries

Results are ecological monthly stroke-aggregate associations under the frozen specifications. They are not individual causal effects, daily lag-response estimates, mortality attributable fractions, or modelled excess deaths. Literature findings remain attributed to their source populations, periods, outcomes, and models.
