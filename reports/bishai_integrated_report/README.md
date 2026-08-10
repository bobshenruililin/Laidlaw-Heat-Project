# Bishai integrated report — artifact map and compile notes

**Purpose.** Supervisor-facing scientific package for the CHD/HF monthly thermal analysis (Hong Kong, 2013–2023).
**Authority date.** 10 August 2026 release artifacts under `outputs/release_chd_hf/`.
**Voice.** Hogan / CNS sparse academic English. Internal Gate language is allowed in the integrated report only.

## Files in this folder

| File | Role |
|---|---|
| [`integrated_project_report.md`](integrated_project_report.md) | Complete supervisor-facing report |
| `README.md` | This map |

## Linked manuscript package

| File | Role |
|---|---|
| [`manuscript/chd_hf_thermal_associations_2013_2023.md`](../../manuscript/chd_hf_thermal_associations_2013_2023.md) | Journal-facing manuscript (no Gate/process jargon in scientific body) |
| [`manuscript/chd_hf_supplement.md`](../../manuscript/chd_hf_supplement.md) | Full supplement |
| [`manuscript/authorship_and_governance_decisions.md`](../../manuscript/authorship_and_governance_decisions.md) | Proposed roles vs open human decisions; no invented author order |

## Release data and figures (cite these paths)

### Tables

| Artifact | Path |
|---|---|
| Outcome summary | `outputs/release_chd_hf/tables/table1_outcome_summary.csv` |
| Twelve core models | `outputs/release_chd_hf/tables/table2_core_models.csv` |
| Robustness summary | `outputs/release_chd_hf/tables/table3_robustness_summary.csv` |
| Uncertainty ladder | `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` |
| Claim ledger v2 | `outputs/release_chd_hf/tables/claim_ledger_v2.csv` |
| Analysis availability | `outputs/release_chd_hf/tables/analysis_availability.csv` |

### Main figures (PNG)

| Figure | Path |
|---|---|
| 1 Indexed series | `outputs/release_chd_hf/figures/figure1_indexed_outcome_series.png` |
| 2 Seasonal pattern | `outputs/release_chd_hf/figures/figure2_seasonal_pattern.png` |
| 3 Core forest | `outputs/release_chd_hf/figures/figure3_core_forest.png` |
| 4 Trend/depletion | `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png` |
| 5 SE ladder | `outputs/release_chd_hf/figures/figure5_se_method_ladder.png` |

### Method-validation figures (synthetic calibration; not health findings)

| Figure | Path |
|---|---|
| Type I by outcome/kernel | `outputs/release_chd_hf/supplement/methods_feasibility/figure_calibration_type1_by_outcome_kernel.png` |
| Coverage by outcome/kernel | `outputs/release_chd_hf/supplement/methods_feasibility/figure_calibration_coverage_by_outcome_kernel.png` |
| Gate pass/fail | `outputs/release_chd_hf/supplement/methods_feasibility/figure_calibration_gate_passfail.png` |
| Spillover event counts | `outputs/release_chd_hf/supplement/methods_feasibility/figure_spillover_event_counts.png` |

Also: `outputs/release_chd_hf/supplement/chd_core_residual_acf_pacf.png`, `outputs/release_chd_hf/supplement/hf_core_residual_acf_pacf.png`, `outputs/release_chd_hf/supplement/figureS1_exposure_correlation.png`, `outputs/release_chd_hf/supplement/figureS2_provisional_hm_cm_calendar.png`.

## Supporting canon (read-only inputs for this draft)

- `knowledge/2026-08-10_correspondence_scientific_contract.md`
- `reports/data_receipt_2026-08-07.md`
- `reports/gate2_qc_close_2026-08-07.md`
- `analysis_plan/final_reanalysis_protocol_2026-08-10.md`
- `analysis_plan/final_claim_tiers.yml`
- `analysis_plan/writing_standards_hogan.md`
- `literature/final_methods_evidence_map.md`
- `literature/references.bib`
- `outputs/calibration_md/md_calibration_f1_2_decision_report.md`
- `outputs/reports/cvd_real_release_validation.md`
- `outputs/release_chd_hf/RELEASE_INDEX.md`

## How to compile (PDF and HTML)

Drafts use Pandoc citations `[@bibtexkey]` and YAML `bibliography` metadata. Run from the repository root. Committed PNGs are embedded via relative paths in the Markdown.

### Integrated report

```bash
pandoc reports/bishai_integrated_report/integrated_project_report.md \
  --from markdown \
  --citeproc \
  --resource-path=.:reports/bishai_integrated_report \
  --pdf-engine=xelatex \
  -o reports/bishai_integrated_report/integrated_project_report.pdf

pandoc reports/bishai_integrated_report/integrated_project_report.md \
  --from markdown \
  --citeproc \
  --resource-path=.:reports/bishai_integrated_report \
  -o /tmp/integrated_project_report.html
```

### Journal manuscript

```bash
pandoc manuscript/chd_hf_thermal_associations_2013_2023.md \
  --from markdown \
  --citeproc \
  --resource-path=.:manuscript \
  --pdf-engine=xelatex \
  -o manuscript/chd_hf_thermal_associations_2013_2023.pdf

pandoc manuscript/chd_hf_thermal_associations_2013_2023.md \
  --from markdown \
  --citeproc \
  --resource-path=.:manuscript \
  -o /tmp/chd_hf_manuscript.html
```

### Supplement

```bash
pandoc manuscript/chd_hf_supplement.md \
  --from markdown \
  --citeproc \
  --resource-path=.:manuscript \
  --pdf-engine=xelatex \
  -o manuscript/chd_hf_supplement.pdf

pandoc manuscript/chd_hf_supplement.md \
  --from markdown \
  --citeproc \
  --resource-path=.:manuscript \
  -o /tmp/chd_hf_supplement.html
```

If `bibliography` in YAML is not resolved, add `--bibliography=literature/references.bib` explicitly.

## Reproducibility commands (completed checks)

```bash
Rscript scripts/35_build_spillover_exposures.R
Rscript scripts/38_cns_final_release_artifacts.R
Rscript scripts/45_recompute_md_calibration_gates.R
Rscript scripts/34_cvd_real_release_checks.R
```

Governed full rerun (local HA files required; do not commit microdata):

```bash
PATHWAY_MODE=real OUTCOMES=chd,hf Rscript scripts/run_cvd_full_analysis.R
```

## Notes

1. HTML comments `<!-- claim:CVD-XX -->` in the manuscript are for claim-ledger checks; they should not render.
2. Authorship order is unresolved; see `manuscript/authorship_and_governance_decisions.md` before external submission.
3. Gate 3 remains open. The integrated report may name it and recommends Option A; the journal manuscript scientific body must not use Gate language.
4. Method-validation (synthetic calibration) figures must keep an explicit non-health caption if embedded.

## Provenance firewall (one screen)

| Allowed on main claim surfaces | Quarantined / literature-only |
|---|---|
| `HA_APPROVED_AGGREGATE` CHD/HF estimates | `SYNTHETIC_CALIBRATION` M\|D metrics |
| `REAL_PUBLIC_HKO` weather validation counts | Daily mortality AFs; modelled excess deaths as morbidity effects |
| Disclosure-minimised tables/figures | Source HA xlsx; merged panels; raw emails |
