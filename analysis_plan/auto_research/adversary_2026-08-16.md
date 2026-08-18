# Independent adversary — 16 August 2026

**Subagent:** `bc-c760d429` (Fable). **Thesis withheld** until after the first unaided read of the live Markdown. Kill only with a table contradiction or a forbidden-claim hit.

## Kills

None.

- **Table 2:** live file matches `outputs/release_chd_hf/tables/table2_core_models.csv` on `rr`, bounds, *p*, and BH *q*. CHD hot nights 1.02182 (1.00185–1.04219), *p* 0.03204; HF cold days 1.07280 (1.00645–1.14352), *p* 0.03096; both *q* 0.192239; minimum *q* 0.192239 > 0.19. HF Tmin unrounded upper bound 1.00004966 → “1.00005”.
- **Ladder:** `table4_uncertainty_ladder.csv`. CHD hot nights: model and HC1 include 1; NW3 1.000253 and NW6 1.00185 exclude 1. Widths 0.05441 → 0.04957 → 0.04361 → 0.04034. HF cold days: all four `rr_low` > 1.
- **Sensitivities:** `cvd_trend_depletion_sensitivity.csv`. CHD/P04A 1.01088–1.02465 → “1.011 to 1.025”; HF/P04B 1.04289–1.11283 → “1.043 to 1.113”. Pre-2020 and COVID-phase sentences match. ACF1 0.5078 / 0.14554 → 0.508 / 0.146.
- **Cold days:** 132 `REAL` rows of `cold_days_by_month_year.csv`: Dec 40 + Jan 54 + Feb 47 = 141; March 4; total 145; 29 months ≥1; 2019 = 1.
- **Forbidden claims:** no AMI/principal-dx from this extract; no daily health coefficient; no stroke analysis; no Gate 3 freeze in the Markdown body; 2.63 and 3.1% explicitly not equated to 1.073 / 1.022; no sleep/BP; no health-econ.

## Near-kills

1. Joint vs separate HF cold days equal only at 3-dp (1.07278552 vs 1.07280015).
2. Ljung–Box “*p* > 0.3 for every HF core model” is lag-6 (min 0.318984). Lag-12 for HF/P02A is 0.0991; the claim does not extend there.
3. Ozone 42.6 → 58.3 are 2013/2023 endpoints; 2019 O₃ was 59.37.
4. Joint CHD very-hot-days HC1 interval excludes 1; the body demotes all joint coefficients to collinearity diagnostics.
5. Supplementary Figure S1 double assignment; S7/S9 section-vs-table overlap; manuscript Table 3 sourced from file `table4_*`.

## Hogan weather

Verbatim. Live paragraph MD5 `a5db1c6b0fd3fcc0f1ac8cbd79bd2b9c` matches `HOGAN_WEATHER_VERBATIM`. After `T~min~` normalisation, 504/504 bytes match `scripts/49_build_live_collab_docx.py`.

## Did not invent

No daily coefficient, stroke/AMI/principal-dx estimate, cohort incidence, pollution-adjusted Table 2, multiplicity-protected finding, or 2.63/3.1%/1.073/1.022 equivalence. No models fitted. Live Word file not touched.
