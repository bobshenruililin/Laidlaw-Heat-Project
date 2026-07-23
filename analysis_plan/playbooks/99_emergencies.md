# Playbook 99 — Emergencies and scope shocks

## Trigger

Run when new data, source documents, collaborator decisions, governance constraints, or provenance failures invalidate the expected workflow.

## Preconditions

- Stop the affected analysis or write-up at the first uncertain boundary.
- Preserve the original input, output, registry, and source version.
- Identify the human owner: Hogan for weather definitions; Roro for outcome/source truth; Bishai for PI/governance and headline scope; Bob for implementation and records.
- Do not turn urgency into permission to invent a field, parameter, decision, or finding.

## Steps

1. **More years or strata than expected.** Inventory and quarantine additions from the 2013–2023 core. Confirm governance, dictionary, denominator compatibility, suppression, and scientific role. Treat later years as a labelled extension and additional strata as exploratory until the team amends the plan. Never delay or silently redefine the core.
2. **Hogan proposes a new definition mid-flight.** Record the exact rule and rationale. Before Gate 3, add it to the catalogue/registry with a new ID and regenerate exposure-only audits. After Gate 3, preserve the frozen primary, create a dated amendment and new ID, and label the new rule secondary unless the team formally reopens the gate.
3. **Influenza gap becomes material.** Preserve missing months as `NA`; never fill them with zero. Report the known 121/132 coverage, inspect the missingness pattern, and obtain a team decision on complete-case analysis, defensible imputation, or dropping the sensitivity. Keep the base thermal model separate.
4. **COVID-era results look unusual.** Verify raw counts, service disruption, coding/revision dates, duplicates, offsets, residuals, and influence before interpretation. Run the pre-specified period sensitivity. Describe utilisation disruption as an alternative explanation; do not infer thermal adaptation or biology from a COVID contrast.
5. **Definitions conflict.** Build a comparison table separating the published source rule, project translation, collaborator wording, registry implementation, and observed code. Do not average or silently choose operators. Return source questions to Roro and weather-role questions to Hogan; assign a versioned ID to each legitimately distinct estimand.
6. **Roro’s revised PDF differs from medRxiv v1.** Preserve both versions and produce a definition/equation/table/claim diff. Update the Roro source manifest and canon with explicit version labels. Do not overwrite v1 history or transport revised mortality RRs as stroke coefficients. Any changed monthly sibling requires team review and a registry amendment.
7. **Jasmine’s full PDF changes the MMT or reconstructed method.** Treat the primary PDF/supplement as source truth. Correct the source manifest, citation notes, and any derived definition; record what changed and which artifacts are affected. Do not retrofit old selected months or results silently. Use a new definition version/ID and re-run only after the team decides its role. Preserve the confirmed headline AFs only if the source still supports them.
8. **Disk/path or HA governance conflict.** Stop copying, reading, transforming, or syncing the affected file. Leave the original where received; do not move it into the repository, cloud storage, or an unapproved temp path. Record only non-sensitive metadata permitted by governance. Ask the PI/Roro for the approved path and resume from a documented decision. Never commit HA data.
9. **Synthetic data leak into a manuscript artifact.** Halt export and distribution. Quarantine affected tables, figures, prose, and cached intermediates; trace the leak using `data_status` and input manifests. Audit the worktree and outputs for `SYNTHETIC`, rebuild from the approved real source, and re-verify every number. If an artifact left the workspace, Bob and the PI own correction/notification. Never relabel synthetic output as real.
10. Create a dated incident/amendment note with trigger, affected artifacts, decisions, owner, corrective action, re-run evidence, and unresolved risks. Update the state and bootstrap so a new chat cannot revive the superseded version.

## Done when

- The uncertain or contaminated workflow is stopped and bounded.
- Original versions and provenance are preserved.
- The human owner has made each required decision.
- Registries, source manifests, outputs, manuscript, state, and knowledge identify the corrected version consistently.
- A clean re-run or explicit no-run decision is documented.

## Failure modes

- Quietly absorbing extra years, strata, or definitions into the primary analysis.
- Overwriting a frozen ID or source version.
- Filling influenza, suppression, or unknown fields with zero.
- Calling COVID anomalies adaptation.
- Treating revised mortality parameters as stroke effects.
- Moving HA data to solve a path error without governance approval.
- Fixing a synthetic leak by changing labels rather than rebuilding.

## Which files to update

- A dated `reports/incident_YYYY-MM-DD.md`, source diff, or amendment note
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `analysis_plan/pathway_registry.yml`
- `analysis_plan/hot_cold_month_registry.yml`
- `analysis_plan/statistical_analysis_protocol.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/open_questions_log.md`
- `knowledge/canon_weather_definitions.md` or literature source manifests when affected
- `knowledge/CONTEXT_BOOTSTRAP.md`
- The affected outputs and manuscript only after correction

## Claim boundaries

An emergency response may establish provenance, invalidate an artifact, or justify a new sensitivity. It does not create scientific evidence. Revised sources retain their original estimands; governance fixes do not validate unknown fields; anomaly checks do not establish biology; and synthetic outputs remain non-findings under every label.
