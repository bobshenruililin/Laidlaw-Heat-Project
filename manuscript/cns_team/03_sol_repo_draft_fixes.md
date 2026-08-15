# Sol cleanup instructions for the repository journal draft

**Target:** `manuscript/chd_hf_thermal_associations_2013_2023.md`

**Authority rule:** Hogan’s live shared manuscript remains the journal authority. The repository draft is a methods-heavy parallel surface. Use it as an archive and source of checked text; do not paste it wholesale into the live file.

## Mandatory wording fixes

Line numbers refer to the pre-edit repository Markdown audited on 15 August 2026.

| Pre-edit line(s) | Section | Required change | Status in this branch |
|---:|---|---|---|
| 39, 41 | Abstract | Replace “continuity analysis of record” with “core reporting choice”; replace “Continuity Newey–West” with “Under Newey–West lag-6 reporting.” | Applied |
| 67 | Design and estimand | Replace “continuity panel” with “core panel” and define it once: “We refer to the twelve separate single-exposure models as the core panel.” | Applied |
| 88, 92, 94, 98 | Statistical models / multiplicity | Replace all “continuity” labels with “core”; retain Newey–West lag 6 as the reporting choice without implying it is validated by null exclusion. | Applied |
| 128, 130, 132, 150, 188, 190 | Core-panel Results | Rename the section, table, forest caption, and prose from “continuity” to “core.” | Applied |
| 213 | Residual dependence | Use “six core-panel exposures” and “days-offset core estimates.” | Applied |
| 235, 237, 239 | Robustness figures and prose | Rename captions and prose to “core panel.” Add the pre-2020 CHD hot-night interval and the COVID-phase-adjusted interval. | Applied |
| 249 | Discussion opening | Replace “Under continuity Newey–West...” with “Under Newey–West lag-6 reporting...” and keep both residual signals inside the unprotected twelve-contrast family. | Applied |
| 259, 276, 278, 279 | Discussion / limitations | Replace the remaining “continuity” labels with “core.” | Applied |

After editing, `rg -i "continuity" manuscript/chd_hf_thermal_associations_2013_2023.md` should return no matches.

## Pre-2020 CHD hot-night transparency

The original repository Results gave the HF pre-2020 estimate with its interval but compressed CHD into a point-estimate range. That is asymmetric reporting.

Add after the HF pre-2020 sentence in Robustness:

> The CHD hot-night association was weaker and compatible with 1 in the pre-2020 window (1.011, 0.991–1.032) and under COVID-phase adjustment (1.013, 0.994–1.033).

Add in the Discussion:

> The CHD hot-night association was not evident in the pre-2020 window.

Sources:

- `manuscript/live_collaborative/claim_ledger.md`
- `outputs/release_chd_hf/supplement/cvd_trend_depletion_sensitivity.csv`
- `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`

These are existing `HA_APPROVED_AGGREGATE` sensitivity results. They do not change Table 2.

## Newey–West ladder-direction honesty

The draft already reports the four intervals but did not explain their direction. For CHD hot nights the ladder narrows:

- Model: 1.022 (0.995–1.049);
- HC1: 1.022 (0.997–1.047);
- NW3: 1.022 (1.0003–1.0439);
- NW6: 1.022 (1.002–1.042).

Add after the CHD hot-night ladder paragraph:

> For this contrast, the ladder narrowed from the model-based to the Newey–West intervals. Robust intervals are not automatically wider, and the direction of that change is itself informative.

Add to the Discussion:

> For CHD hot nights, the Newey–West intervals were narrower than the model-based interval, which is atypical under positive residual autocorrelation. The exclusion of 1 therefore rests on the smaller robust variance estimate and is a reason for caution, not confirmation.

Do not write that the model-based interval is “too narrow.” Do not describe Newey–West as conservative. The observed ladder supports neither statement.

## Conclusion language

The cleaned repository draft should not rank an unprotected panel using “largest,” “strongest,” “most elevated,” or an equivalent superlative. Its current Abstract conclusion is acceptable:

> The current data do not support a protected differential thermal claim for CHD versus HF.

If a separate Conclusion section is restored, use bounded comparative language:

> In governed monthly aggregates for people with type 2 diabetes and/or hypertension, CHD first hospitalisations were more closely associated with hot nights, and HF first hospitalisations with cold days, than with the other thermal encodings examined. Neither association was protected across the twelve comparisons, and the CHD estimate depended on the treatment of uncertainty.

Do not turn that comparison into a headline before the team closes Gate 3.

## Surface-specific rules

1. **Do not paste the repository YAML affiliation into Hogan’s live file.** The YAML lists only `Laidlaw Scholars Programme, The University of Hong Kong`. It is repository metadata, not a team-approved journal affiliation block.
2. Do not overwrite Hogan’s weather Methods with repository prose.
3. Roro retains ownership of the governed health-data paragraph and its ICD, timing, and inpatient semantics.
4. Do not copy provisional HM/CM estimates into the live Results.
5. Do not add stroke, daily-trigger, mortality-burden, or health-economic results.
6. Do not infer dissemination authority from the existence of the disclosure-minimised release.

## Citation and asset checks before any future repository PDF export

- Keep mortality attributable fractions, modelled excess deaths, daily admission risks, and monthly morbidity count ratios attached to their own cited designs.
- Preserve the explicit non-transferability statements around Goggins, Guo, Jingwen Liu et al., and Zhenyuan Liu et al.
- Restore or export the manifest-listed PNGs under `outputs/release_chd_hf/figures/` before rebuilding the repository journal PDF; this checkout currently contains the SVGs but not those PNGs.
- Restore or regenerate the display-only files under `figures/live_identification/` from `scripts/47_live_identification_figures.R` if the repository draft is ever aligned to the live three-figure structure.

## PDF lock

Do **not** rebuild either Stage 3 PDF:

- `reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf`
- `outputs/Laidlaw_Stage3_Research_Report_Shen.pdf`

Do **not** rebuild the A0 poster:

- `reports/poster/Laidlaw_Stage3_A0_portrait.pdf`

The report copies must remain byte-identical with SHA-256 `6136e85a654502a0aff3018918a6b27f16d449b9da65678a238df2f53e9d36c2`. The poster must remain byte-identical with SHA-256 `4f7c1e408ae2d31fd5c316c0b435ea46ed2d6091d156c577fd25cbdd7a68afa2`.

No PDF was rebuilt as part of this cleanup.

