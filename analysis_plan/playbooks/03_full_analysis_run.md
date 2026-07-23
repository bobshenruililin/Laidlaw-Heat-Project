# Playbook 03 — Full analysis run

## Trigger

Run after the approved stroke aggregates have passed Gates 1–2 and the real merged panel is ready for the pre-specified pathway analysis.

## Preconditions

- Gate 1 documents schema, outcome definition, true-event-month rule, grain, governance, and suppression.
- Gate 2 documents coverage, missingness, plausibility, merge integrity, and denominator compatibility.
- The outcome rows carry verified real-data provenance; no synthetic outcome is present.
- Weather definitions have the status claimed in the registry. `HM23` is not run as “locked” unless Playbook 01 is complete.
- The team, not an agent alone, is available to close Gate 3.

## Steps

1. Snapshot the versions of [`pathway_registry.yml`](../pathway_registry.yml), [`hot_cold_month_registry.yml`](../hot_cold_month_registry.yml), the SAP, input manifest, and code commit or worktree state. Record any approved departures before looking for a preferred estimate.
2. Confirm that code consumes the frozen HM/CM registry:

   ```bash
   rg "hot_cold_month_registry" scripts analysis_plan
   ```

   If no executable builder consumes it, stop and implement a versioned registry-driven exposure build and selected-month audit. Do not hand-code starter flags in a notebook.
3. Rebuild the real panel and run all enabled `P01–P18` pathways:

   ```bash
   PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R
   ```

   Preserve statuses for successful, disabled, skipped, and failed pathways.
4. Validate `data_status`, model convergence, offsets, sample sizes, month coverage, residual diagnostics, autocorrelation, overdispersion, influential months, and exposure collinearity. Reconcile pathway-specific sample changes, especially the 121/132-month influenza series.
5. Run the frozen HM/CM starter panel through its registry-driven builder and model layer. Export each definition’s parameters, selected-month list, exposure prevalence, missingness, and estimate. Keep absolute thresholds, relative months, spells, combined events, and compound sensitivities as distinct estimands.
6. Prepare a Gate 3 decision packet containing the QC/descriptive evidence, scientific rationale, exposure prevalence, model feasibility, and the complete pre-specified panel. Do not rank candidate definitions by p-value or effect magnitude.
7. Freeze Gate 3 **with Hogan, Roro, Bishai, and Bob as applicable**. Record the primary outcome; hot and cold co-primary definitions; pathway IDs; denominator; seasonality/trend; adjustment ladder; COVID role; subtype role; and sensitivity set. If the team defers, all estimates remain a panel without a headline claim.
8. Date and version the Gate 3 note. Any later scientific change requires a documented amendment and a new pathway/definition ID when the estimand changes; never silently redefine an existing ID.
9. Regenerate manuscript tables:

   ```bash
   Rscript scripts/22_make_pathway_manuscript_tables.R
   Rscript scripts/23_pathway_diagnostics.R
   Rscript scripts/24_pathway_forest_figure.R
   Rscript scripts/15b_pathway_smoke_checks.R
   ```

   Update the exporter if the frozen headline IDs differ from its configured subset. Verify the tables label real provenance and match the Gate 3 note.
10. Report the complete panel, including null, discordant, skipped, and non-convergent specifications. Explain sample changes and definition sensitivity. Do not select a favourable adjustment stage or subgroup after seeing results.
11. Update the SAP amendment log, ledger, gates, project state, knowledge, and analysis run record with exact versions and output paths.

## Done when

- The real pathway and HM/CM panels are reproducible from versioned registries.
- Every estimate has an ID, provenance, exposure contrast, sample size, and diagnostic status.
- Gate 3 is signed off with the team or is explicitly still open.
- Manuscript tables match the frozen IDs and include the complete panel needed to audit selection.
- No synthetic output appears in the real result set.

## Failure modes

- Running an HM/CM label that no code derives from the registry.
- Choosing the headline pair because it is largest or nominally significant.
- Hiding failed, null, or discordant pathways.
- Treating a subtype, age, sex, pollution, or influenza sensitivity as confirmatory without the frozen role.
- Allowing a hard-coded `P02 + P04` table to mislabel a different Gate 3 decision.
- Comparing monthly rate ratios directly with daily DLNM RRs, attributable fractions, or modelled excess deaths.

## Which files to update

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

## Claim boundaries

The models estimate ecological monthly associations in governed stroke aggregates. They do not estimate individual causality, daily triggering, mortality attributable fractions, or excess deaths. “Robust” means consistent under the pre-specified panel with acceptable diagnostics; it does not mean that only favourable specifications were retained.
