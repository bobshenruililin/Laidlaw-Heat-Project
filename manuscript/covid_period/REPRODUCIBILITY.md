# Reproduce the frozen article from released summaries

**Evidence anchor:** PR #103 at `7060606fbe44b14b6b2893929781ac477cea1d46`. **Provenance:** all displayed health values are `HA_APPROVED_AGGREGATE`. This package reconstructs tables, arithmetic comparisons, figures and document exports from already released summaries. It does not reproduce the original governed-data extraction or model fits, establish interval calibration, or grant data-use/publication authority.

## Completed path

1. Verify `frozen_evidence_manifest.json` against `MANUSCRIPT_FREEZE.md`. Nine scientific/context source files are immutable. Baseline manuscript hashes identify the historical starting revision; editorial outputs may change.
2. Use Python with Matplotlib to run `scripts/86_frozen_publication_figures.py` from the repository/package root. It refuses altered numerical source hashes, reads approved summary tables, and writes three PNG/SVG/PDF displays with minimal source CSVs. Observed rendering runtime: Python 3.11.4, Matplotlib 3.11.0, DejaVu Sans. SVG text remains editable; PDF uses embedded TrueType fonts. Fixed SVG identifiers and export metadata permit byte reproduction in that runtime. Captions are in the manuscript sources.
3. With the bundled document Python, run `scripts/81_covid_research_manuscript.py --audit`. It checks 35 source/value, interpretation, contrast-preservation and cross-reference conditions and writes `claim_ledger.yml`. It reads no underlying hospitalisation panel. It imports formatting helpers from script 78 but does not execute that historical builder or its obsolete prose contract.
4. Run script 81 without `--audit` to create both editable Word documents. Observed document runtime: bundled Python 3.12.14, python-docx 1.2.0. Use the packaged document renderer with `--emit_pdf`, then inspect every page before replacing released PDFs. Word/PDF archive metadata need not reproduce byte-for-byte; source content and visible layout must agree. The equation is native editable Word mathematics.

The five unchanged numerical CSVs are annual totals, disjoint-period means, core robust estimates, complete trend/window sensitivity, and baseline fit diagnostics in `outputs/tables/`. **All 108 rows of `cvd_trend_depletion_sensitivity.csv` remain available**, including 42 continuous-exposure alternative-calendar estimates not expanded into the article's tables. None is filtered from this package. All 48 baseline uncertainty constructions and all twelve baseline contrasts remain in the supplement. Older full source CSVs contain other released rows; only the declared NB/days-only/single-exposure family supplies this article's baseline figures and tables.

Supplementary observation and nested-window graphics retain their existing editable SVG, vector PDF and source CSV exports. The observation figure is conceptual, with unobserved pathways and no numerical cohort flow. It is not empirical source data or an identified causal model.

## Historical analyses and unexecuted readiness

Historical completed-summary generators are `scripts/27_cvd_descriptives_real.R`, `scripts/31_cvd_core_robustness.R` and `scripts/32_cvd_trend_depletion_lag.R`. Their governed inputs are absent from this public reconstruction path. Source-to-summary agreement cannot validate those inputs, the clinical extraction rules, the original fit environment or nominal coverage.

`scripts/83_covid_common_basis_interactions.R` is prospective readiness only: **NOT RUN on these outcomes, NOT CALIBRATED, and NOT a source of any article result.** Rscript was unavailable during this editorial run. No simulation, new interaction, separate later-era fit, independent validation or clinical trajectory was generated. Neither that runner nor exploratory synthetic exercises belongs to the completed-results path. The prospective runner is deliberately absent from the reconstruction archive.

## Package and review records

`reproducibility_manifest.json` inventories the reconstruction archive by SHA-256, with runtime versions and completed/unexecuted status. The ZIP mirrors repository-relative paths and includes the five full numerical summaries, frozen source context, figure exports/source tables, manuscript Markdown, ledger and required presentation/audit helpers. It contains no individual or governed monthly health records. Edited Word and reviewed PDF deliverables are distributed separately.

`FROZEN_VERIFICATION.md`, `FROZEN_STATISTICAL_REVIEW.md`, `FROZEN_CLINICAL_REVIEW.md`, `FROZEN_EDITORIAL_REVIEW.md` and `FROZEN_REVIEWER_RISK.md` in `reports/auto_research/2026-10-02/` record the review scope and remaining conditions. The source-access limits of close external studies remain in the frozen novelty register. Human submission facts are tracked in `SUBMISSION_COMPLETION.md`.
