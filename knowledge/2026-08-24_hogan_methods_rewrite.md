# 24 August 2026 — Hogan Methods rewrite

**Mode:** Ship. **Not** a Gate 3 freeze. **Not** a Stage 3 PDF rebuild.

## What was read

`Commented_Heat_CVD_Manuscript_20260824.pdf` (16 pp, Word export, author Hogan). No Acrobat annotation objects. All balloons recovered with `pdftotext -layout` as `Commented [H1]–[H6]`, `[H21]`, `[KW7]–[KW20]`. Inventory: [`../manuscript/live_collaborative/hogan_20260824_comment_inventory.md`](../manuscript/live_collaborative/hogan_20260824_comment_inventory.md).

Same-day email: simplify Methods; numbered models; no Results in Methods; section order; no WIP ethics in the body; RH and rainfall in the models; no TV-day counts; day-of-year historical averages instead.

## What changed

Live wording: [`../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`](../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md). Paste: [`LIVE_DOC_EDITS.md`](../manuscript/live_collaborative/LIVE_DOC_EDITS.md). Replies: [`hogan_20260824_paste_replies.md`](../manuscript/live_collaborative/hogan_20260824_paste_replies.md).

Weather-only abnormal-day counts (132 months, RH/rain match `climate_monthly`): [`../data_processed/hogan_abnormal_day_counts_2013_2023.csv`](../data_processed/hogan_abnormal_day_counts_2013_2023.csv). Scripts: `scripts/52_hogan_abnormal_day_counts.py` (this checkout) and `.R` (Bob’s machine).

## What remains human

- Paste into the shared live file (do not email a parallel Word copy).
- @Roro: IRB number; ICD/timing if they differ.
- Refit Table 2 with RH and rainfall on the governed panel: `Rscript scripts/53_hogan_models_rh_rain.R`. **Not done here** (panel absent; `outputs/tables/hogan_models_rh_rain_blocker.csv`). Do not invent coefficients.
- Hogan’s HKO paragraph stays his. Averaging-vs-total rainfall is a live-file comment, not a body overwrite.
- Day-of-year warmer/cooler counts are sensitivity weather only; they do not winter-peak like Hogan’s TV series.

Fable GO / Sol GO on the paste pack. Table 2 refit remains human (governed panel). Gate 3 remains open. No AMI, stroke result, or confirmatory thermal headline.
