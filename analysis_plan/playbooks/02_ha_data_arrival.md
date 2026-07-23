# Playbook 02 — HA data arrival

## Trigger

Run when governed Hospital Authority stroke aggregate files, a dictionary, or a revised aggregate release arrive.

## Preconditions

- The PI/governance-approved route and permitted use are documented.
- Files are approved aggregates, not microdata, and can be stored at the approved path.
- The sender or Roro can answer dictionary, timing, suppression, and release questions.
- [`ha_stroke_aggregate.schema.json`](../../schemas/ha_stroke_aggregate.schema.json), [`decision_gates.md`](../decision_gates.md), and [`scientist_runbook.md`](../scientist_runbook.md) have been read.

## Steps

1. Keep the received files unchanged. Place approved CSVs only in `data_raw/ha_secure_placeholder/` when that path is governance-approved. Record receipt date, source, original filename, file hash, transfer authority, and permitted use in a governed receipt note. Do not commit the data.
2. Inventory every file, sheet, column, type, code value, period, and apparent grain before renaming anything. Never assign a field meaning from its name alone.
3. Map documented source fields to the schema. Require explicit definitions for `month_id`, `n_events`, outcome universe, true-event-month construction, age, sex, subtype, suppression, missing values, revisions, and population eligibility. If a required meaning is unknown, stop and ask Roro; do not let a script supply a convenient default.
4. If the release contains more years, strata, outcomes, or fields than expected, quarantine the extras from the core analysis. Preserve the 2013–2023 stroke estimand, inventory the additions, and request a team decision before extending scope. Update the schema only from documented meanings.
5. Run QC before fitting:

   ```bash
   PATHWAY_MODE=real Rscript scripts/08c_qc_stroke_aggregates.R
   ```

   Review the source-to-schema mapping and `outputs/reports/stroke_data_qc_receipt.md`. Add checks for duplicates at the declared grain, month coverage, impossible counts, revisions, suppression codes, subtype totals, and stratum completeness.
6. **Small cells:** treat suppressed or disclosure-controlled cells as missing/suppressed, never zero. Do not reverse-engineer complementary suppression. Collapse strata only with an authorised rule and document the information loss.
7. **Subtype surprise:** if explicit ischaemic and haemorrhagic subtypes arrive, verify coding, mutual exclusivity, unspecified stroke handling, and reconciliation with pooled totals. Keep `P13` disabled until the subtype field and reporting permission are confirmed; pooled stroke remains the default until the team changes it.
8. Build and inspect the merge:

   ```bash
   Rscript scripts/19_build_analysis_exposures.R
   PATHWAY_MODE=real Rscript scripts/08d_merge_stroke_panel.R
   ```

   Check one-to-one or expected one-to-many joins, denominator compatibility, `population × days_in_month` offsets, missing exposures, duplicate cells, and exact study-window coverage.
9. Write a Gate 1–2 data-receipt/QC note. Record every deviation and its disposition. Do not proceed when event-month semantics, aggregate grain, denominator universe, suppression, or major gaps remain unexplained.
10. Only after Gates 1–2 close, set `PATHWAY_MODE=real` for the full run:

    ```bash
    PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R
    ```

    Verify every output carries `HA_APPROVED_AGGREGATE` or another documented real-data provenance label and no `SYNTHETIC` status.
11. Update project state, gates, ledger, schema documentation, and knowledge with what the delivered file actually supports. Do not add unavailable subtype, age, sex, clinical, or admission-reason claims.

## Done when

- The original release is preserved under the approved path and is not tracked by Git.
- Field meanings, grain, event month, coverage, subtype status, suppression, and population universe are documented.
- Gates 1–2 have an evidence-backed close or an explicit stop.
- The merged panel reconciles to the approved aggregates and denominators.
- Real mode refuses or contains no synthetic outcome.

## Failure modes

- Letting the ingest script silently create `data_status`, `stroke_type`, age, or sex semantics that the source did not provide.
- Choosing the first matching CSV when multiple revisions exist.
- Treating missing or suppressed cells as zero.
- Expanding to extra years or outcomes before completing the 2013–2023 core.
- Enabling subtype pathways because a label exists without validating its coding.
- Running models before unexplained month gaps or duplicate grains are resolved.

## Which files to update

- `outputs/reports/stroke_data_qc_receipt.md`
- `outputs/tables/stroke_qc_summary.csv`
- `schemas/ha_stroke_aggregate.schema.json` and `schemas/README.md` when documented fields require a contract change
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/open_questions_log.md`
- `knowledge/CONTEXT_BOOTSTRAP.md`
- A dated `reports/data_receipt_YYYY-MM-DD.md` or meeting/QC debrief

## Claim boundaries

Receipt, row counts, field availability, and descriptives may be reported only from the delivered governed release and within its disclosure rules. QC is not an association result. Do not infer AMI, admission reasons, subtype, event timing, or unsuppressed values from undocumented fields. Do not publish coefficients before Gate 3 permits primary claims.
