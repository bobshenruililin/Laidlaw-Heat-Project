# CHD/HF real-release validation

- Checked: 2026-08-10 11:28:00.723556
- Release directory: `/workspace/outputs/release_chd_hf`
- Passed: 27 / 27

| Check | Status | Detail |
|---|---|---|
| chd_estimate_provenance | PASS | HA_APPROVED_AGGREGATE |
| chd_estimate_month_bound | PASS | range=84-132 |
| chd_diagnostics_real_only | PASS | n_range=132-132; synthetic=FALSE; status=HA_APPROVED_AGGREGATE |
| hf_estimate_provenance | PASS | HA_APPROVED_AGGREGATE |
| hf_estimate_month_bound | PASS | range=84-132 |
| hf_diagnostics_real_only | PASS | n_range=132-132; synthetic=FALSE; status=HA_APPROVED_AGGREGATE |
| no_ambiguous_generic_outputs | PASS | none |
| governed_inputs_gitignored | PASS | source aggregates and merged panels |
| governed_inputs_not_tracked | PASS | no governed inputs tracked |
| release_directory_populated | PASS | /workspace/outputs/release_chd_hf |
| table2_claim_ledger_identity | PASS | 12 rows; rr/CI/p/q/se/provenance identical |
| claim_text_rounding | PASS | claim_text matches 3-dp rounding |
| bh_q_recompute | PASS | BH q values match p.adjust(..., method='BH') |
| claim_ledger_ha_not_real | PASS | HA_APPROVED_AGGREGATE |
| claim_ledger_v2_columns | PASS | tier/post-outcome/multiplicity/SE present |
| claim_ledger_v2_no_extra_real_claims | PASS | v1=12 v2=12 |
| claim_ledger_v2_no_synthetic | PASS | HA_APPROVED_AGGREGATE |
| uncertainty_ladder_12x4 | PASS | 48 HA_APPROVED_AGGREGATE ladder rows (12x4) |
| uncertainty_ladder_ha_provenance | PASS | HA_APPROVED_AGGREGATE |
| weather_source_validation_all_pass | PASS | n=5; all_pass=TRUE; file=/workspace/outputs/release_chd_hf/supplement/methods_feasibility/weather_definition_source_validation.csv |
| synthetic_calibration_path_policy | PASS | synthetic path policy OK; allowed=README.md;RELEASE_INDEX.md;supplement/methods_feasibility/figure_calibration_coverage_by_outcome_kernel.svg;supplement/methods_feasibility/figure_calibration_gate_passfail.svg;supplement/methods_feasibility/figure_calibration_type1_by_outcome_kernel.svg;supplement/methods_feasibility/md_calibration_f1_2_decision_report.md;supplement/methods_feasibility/md_calibration_gate_summary.csv;supplement/methods_feasibility/md_calibration_summary.csv;supplement/methods_feasibility/md_pilot_f1_0_failure_note.md;supplement/methods_feasibility/md_pilot_f1_0_gate_summary.csv;supplement/methods_feasibility/methods_feasibility_manifest.csv;supplement/methods_feasibility/README.md |
| no_synthetic_on_main_claim_surfaces | PASS | none |
| no_raw_monthly_count_descriptives | PASS | no raw monthly-count descriptives |
| analysis_availability_schema | PASS | schema OK |
| blocker_statuses_non_fail_facts | PASS | blocker_rows=6; disposition_ok=TRUE |
| blockers_not_fake_completed_analyses | PASS | no fake completions |
| preserved_tables1to3_figures1to4 | PASS | present |

**RELEASE VALIDATED.**
