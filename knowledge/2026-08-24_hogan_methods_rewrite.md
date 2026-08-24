# 24 August 2026 — Hogan Methods rewrite

**Mode:** Ship. **Not** a Gate 3 freeze. **Not** a Stage 3 PDF rebuild.

## What was read

`Commented_Heat_CVD_Manuscript_20260824.pdf` (16 pp, Word export, author Hogan). No Acrobat annotation objects. All balloons recovered with `pdftotext -layout` as `Commented [H1]–[H6]`, `[H21]`, `[KW7]–[KW20]`. Inventory: [`../manuscript/live_collaborative/hogan_20260824_comment_inventory.md`](../manuscript/live_collaborative/hogan_20260824_comment_inventory.md).

Same-day email: simplify Methods; numbered models a high-school reader can follow; no Results in Methods; section order; no WIP ethics in the body; RH and rainfall in the models; no TV-day counts; day-of-year historical averages instead.

## Numbering lock

Nested **Model 1 / Model 2 / Model 3**, not Models 1–12 as primary names.

- **Model 1:** twelve thermal fits already in Table 2 (no RH/rain in the equation). Table 2 reports Model 1.
- **Model 2:** Model 1 + monthly total rainfall + monthly mean RH. Cite [21] for humidity only. Rainfall is in the model because Hogan listed it, not because Goggins and Chan 2017 used rainfall. Not fitted here (governed panel absent).
- **Model 3:** replace official extreme-day counts with leave-one-year-out same-calendar-day warmer/cooler counts of mean, max, and min temperature (six monthly series). Specified; not fitted.

KW15 is a rescaling of the Model 1 extreme-day coefficient (*R*^(3/5), *R*^(1/5)), not a fourth model.

## What changed

Live wording: [`../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`](../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md).

Final paste files: [`Heat_CVD_Manuscript_20260824_hogan.docx`](../manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.docx) and [`.pdf`](../manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.pdf). Builder: `scripts/64_hogan_20260824_manuscript_docx.py`.

Weather-only climatology counts (132 months): [`../data_processed/hogan_abnormal_day_counts_2013_2023.csv`](../data_processed/hogan_abnormal_day_counts_2013_2023.csv). Script: `scripts/52_hogan_abnormal_day_counts.py`.

Contract tests: `tests/test_hogan_methods_rewrite.py`.

## What remains human

- Paste the Word file into the shared live document (do not email a competing copy unless Hogan asks).
- @Roro: IRB number; ICD/timing if they differ.
- Fit Model 2 on the governed panel: `Rscript scripts/53_hogan_models_rh_rain.R`. **Not done here.** Do not invent coefficients.
- Hogan’s HKO paragraph stays his. Averaging-vs-total rainfall is a Word comment, not a body overwrite.
- Model 3 is specified weather; it does not winter-peak like Hogan’s TV series.

Gate 3 remains open. No AMI, stroke result, or confirmatory thermal headline. Stage 3 PDFs remain byte-locked (`c083d4096a0924b1` / `0ef58e0951bb2ffd`).
