# Round B — verification of the Round A methods/causal audit (Sol)

**Date:** 15 August 2026. **Verified against:** `data_processed/variable_dictionary.csv`, `outputs/release_chd_hf/tables/table2_core_models.csv` and `table4_uncertainty_ladder.csv`, fresh greps of `data_processed/` and `outputs/release_chd_hf/`, the committed and current working-tree `Heat_CVD_Manuscript_live_update.md`, the 28 July skeleton, and the comment/decision ledgers. No model re-fitted; no health number added.

## Confirmed Sol claims

1. **Dictionary provenance.** `variable_dictionary.csv` is synthetic development metadata (`n_events` "(SYNTHETIC in this file)"; `data_status` "Must equal SYNTHETIC for the development panel"). Sol's scoping — absence means unavailable to this analysis, not proof about HA source systems — is exactly right.
2. **No medication field.** Fresh case-insensitive searches for medication/prescription/drug/statin/antihypertensive/insulin/ATC find nothing in the dictionary, `data_processed/`, or `outputs/release_chd_hf/`. (Apparent hits elsewhere in `outputs/` are the substring "atc" inside "match".)
3. **Variable inventory.** Humidity (relative, absolute, dew point) and rainfall exist in the dictionary and are stated in Methods as assembled but not core; no solar-radiation or stagnation variable exists — all as Sol stated.
4. **Release tables.** `table2_core_models.csv`: 12 rows, all `n_months` = 132, `offset_policy` = `days_only`, negative binomial, NW6, `HA_APPROVED_AGGREGATE`. `table4_uncertainty_ladder.csv`: all twelve contrasts × four SE methods with identical point estimates to table2 — Sol's "same twelve point estimates appear in the core and uncertainty tables" is correct.
5. **Offset claims.** Core days-only; general-population × days retained as a labelled sensitivity; archive influenza model (P14) on `population_x_days`, not the core offset — all correct and now stated in the live Discussion.
6. **Quotations.** All six "Old" quotes and all four overreach quotes matched the committed live file verbatim. The ozone "confounder, effect modifier, or pathway variable" phrase is in the superseded skeleton only, exactly as Sol attributed it.
7. **Access honesty.** Sol declares `PARKED_NO_PANEL`, no re-fit, and no sight of HA microdata, ICD lists, or the timing rule. No invented variables, rows, or access anywhere in the audit.
8. **CEA rejection: correct.** No intervention or comparator (the exposure contrasts are model-based); no causal effect to feed an economic model (all q > 0.19; ecological count ratios); no costs, utilisation prices, or QALY inputs anywhere in the release (`external_data_feasibility.md`: "No utilisation prices in the HA aggregates. Do not force CEA"). Sol's missing-element list is the standard reference case and none of it is present. Matches approach registry A6 `rejected`. The descriptive burden/resource-use carve-out is properly separated as future linked work.
9. **Multiplicity scope.** BH covers only the twelve declared contrasts; the live Discussion now states the archive flu coefficient lies outside that correction — consistent with Sol's point.
10. **Identification facts.** 141/145 DJF cold days and June–September always ≥1 hot night match the verified project and HKO numbers.

## Rejected or qualified Sol items

1. **The proposed "Unmeasured factors" replacement sentence — rejected as a paste.** Sol's drop-in names medication, disease severity, blood-pressure control, housing, air-conditioning access, and individual behaviour in the paper body. The recorded comment-4 disposition omits housing/behaviour/AC from the **paper body** and rejected even an appendix listing; Sol's sentence re-inserts exactly the dangled factors Hogan struck, offered as a direct replacement with no flag that it reverses a Hogan-owned decision. On the literal reading Hogan's instruction targeted the Introduction ("from the get-go"), so a Limitations mention is arguable — but reversing the recorded body-wide rule is Hogan's call, not an auditor's edit. The underlying analysis (DAG items 6–7) stands as audit content, where naming such factors is the job.
2. **DAG item 16, "changing station composition" for pollutants — qualified.** Plausible and phrased as a potential issue, but no in-repo primary source; it needs an EPD source before it can enter the manuscript.
3. **"No identified causal target estimand" — judgment, not fact.** Defensible and consistent with the paper's own refusals; recorded here as a methods opinion rather than a source-checkable claim.

## The prescription-only Limitations sentence: adequate

The live file now carries: "Monthly prescription fields were not in the released aggregates, so changes in therapy are absorbed by the time spline and are not separable from it."

- It answers the one question any referee of a 2013–2023 T2D/HTN cohort with halving first-event counts will ask, with the technically correct statement (absorbed by the spline, not separable).
- It is factual and correctly scoped to the released aggregates; it does not claim the HA source systems lack medication records — matching Sol's own caution about the synthetic dictionary.
- Housing, AC, and behaviour stay out of the body per comment 4, and their scientific content survives generically in the existing single-station / territory-wide exposure limitation.
- The comment ledger now records the disposition as Limitations-only with the residual that Hogan may prefer total omission — correctly left strikeable.

## False source or offset claims in Sol's audit

**None found.** Sol cites no external literature (nothing to invent), quotes the manuscript and skeleton accurately, attributes the skeleton phrase correctly, and every offset statement matches the release tables.

## Remaining citation/variable defects (current working tree)

1. **Introduction still cites [2,4,6] for the 2023 cold-day value** while the Results exposure paragraph now correctly cites [2,4,22]. Change the Intro anchor to [22]; after that, [6] (HKO Open Data) becomes uncited unless attached where it genuinely belongs — the Methods processing paragraph built on daily open-data flags, which currently carries no citation.
2. **Refs [3] (2017 yearbook) and [5] (2024 yearbook) remain uncited** — Hogan-owned decision still open (drop both; [5] survives only with the optional 2024 climate sentence).
3. **Ref [7] (EPD EPIC portal) still lacks an access date or stable document anchor** (GIA annex) for the 2013→2023 means.
4. **Claim ledger figure rows are stale after the renumbering:** the ledger still maps Figure 3 → residual ACF and Figure 4 → hot-night heatmap, while the live file now has Figure 3 = hot-night heatmap (`figure_D`) and Figure 4 = residual ACF (`figure_C`). One-line swap.
5. **Variable-side trap, not a manuscript defect:** the synthetic dictionary's `offset_log` is `log(population * days_in_month)` while the analysis of record is days-only. Anyone citing `variable_dictionary.csv` as core-model documentation imports the wrong offset; one provenance line in that CSV or its README closes the trap.

Fixed since Round A, no action needed: figure order now sequential; [22] added and attached in Results; Liu 2020 wording now "for mortality"; the four overreach sentences revised; the flu coefficient flagged as outside the twelve-contrast correction; the title now names the T2D/HTN population.
