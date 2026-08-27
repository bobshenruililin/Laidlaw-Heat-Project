# Live Figure 3 rebuilt for the manuscript (27 August 2026)

**Why this entry exists.** Bishai’s comments were on live-manuscript Figure 3. A matplotlib teaching forest in `reports/` was rejected. The same mapping (spline df ≠ duration; pre-2020 away from 1 is HF cold days; no 5-day warning rule from this panel) is now in the paper figure, caption, Results, and Discussion.

## What changed

- Live Figure 3 is no longer a copy of release `figure4_trend_depletion_sensitivity` (15 × 8 in). Script `scripts/66_live_figure3_relabel.py` writes a portrait 6.2 × 7.35 in forest to `figures/live_identification/figure_D_trend_depletion_sensitivity.png`.
- Layout: 2 rows (CHD, HF) × 3 official-count columns. Y-axis: “Time-trend spline, N df”, “Pre-2020 (Jan 2013–Dec 2019)”, Model 1 shaded. Strips: “per 5 more official hot nights / very hot days / cold days”, not bare “per 5 days”.
- Teal = 95% CI excludes 1; grey = includes 1. No new health model. Release figure 4 is untouched.
- Continuous-temperature columns moved to Supplementary Figure S6 (`figure_E_continuous_temperature_sensitivity.png`) so the pre-2020 inverse-T pattern is not hidden.
- Caption still starts “Figure 3. Model 1 count ratios”. Five-day scale and spline df are named against consecutive days. Abstract, Table 2, and Hogan’s HKO weather paragraph are unchanged.

## Locked numerals (unchanged)

CHD hot nights / 5 days **1.022 (1.002–1.042)**; HF cold days / 5 days **1.073 (1.006–1.144)**; all twelve Model 1 *q* > 0.19. Pre-2020 HF cold **1.113 (1.053–1.176)** excludes 1; CHD hot nights pre-2020 **includes 1**. Year-indicator CHD hot nights **1.025 (0.9998–1.050)** includes 1; do not crown df 6.

## What this is not

Not a Gate 3 freeze. Not an evaluated municipal heat-health action plan. Not a consecutive-day warning rule. Stage 3 hashes remain `605cd8db43072cb5` / `a972206e61932650`. Form 2a still uses the essay.

Paste file: rebuild with `python3 scripts/64_hogan_20260824_manuscript_docx.py`. Current Hogan PDF SHA-256 prefix `fb01f23fe3d908c4` (22 A4 pages; Figure 3 on p. 15).
