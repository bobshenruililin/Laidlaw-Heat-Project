# Things to edit in Hogan’s live document

This is the **journal-track** shared file, not the Laidlaw Stage 3 report. Do not email him a parallel Word copy. Continue in the shared document.

**Wording authority:** Markdown `Heat_CVD_Manuscript_live_update.md`.  
**24 August 2026:** Hogan’s commented PDF is `Commented_Heat_CVD_Manuscript_20260824.pdf`. Comment table: `hogan_20260824_comment_inventory.md`. Paste replies: `hogan_20260824_paste_replies.md`. Methods paste around his weather paragraph: `methods_remainder_paste.md`.

## 24 August — do this first

1. Leave Hogan’s *Weather and pollutants data* HKO paragraph as he rewrote it (including “All monthly data were derived by taking the average of daily data in each calendar month.”). Paste around it from `methods_remainder_paste.md`. Do **not** paste model specification or the December–February cold-day sentence under Weather.
2. Replace the rest of Methods from the live_update: Data sources (health, weather processing, population) → Statistical analysis (Model 1 equation **without** RH/rain, then Model 2, then Model 3) → Sensitivity analysis → Software. Keep his ethics sentence with `UW XX-XXX`. Author-order confirmation is a comment, not body text. Acknowledgements = `None.`
3. In Hogan’s **Abstract Methods**, name Model 1 / Model 2 / Model 3 and keep **Table 2 reports Model 1**. Delete any sentence about the simulated daily-recovery method failing calibration. That result stays in Results only.
4. Reply in the KW balloons from `hogan_20260824_paste_replies.md`. Do not resolve until he has read them.
5. Put the Table 2 **and Abstract** Word comments from that replies file on those objects. On a machine **with** the governed panel, run `Rscript scripts/53_hogan_models_rh_rain.R` and add **Model 2** beside Table 2. This checkout cannot fit Model 2 (panel absent; blocker in `outputs/tables/hogan_models_rh_rain_blocker.csv`). Do not invent coefficients.
6. Day-of-year warmer/cooler counts are **Model 3** (`scripts/52_hogan_abnormal_day_counts.py`), not a replacement for official HKO hot nights / cold days in Table 2, and not Jingjing TV-day counts.

**Word/PDF to paste:** `Heat_CVD_Manuscript_20260824_hogan.docx` and `.pdf`, built by `python3 scripts/64_hogan_20260824_manuscript_docx.py`. Prefer pasting that file over reconstructing from markdown. Do not email a competing copy unless Hogan asks for the file.

## Do not touch

| Place | Why |
|---|---|
| Hogan’s HKO weather paragraph, including “Meteorological data was obtained from the HKO.” | His Methods (24 Aug rewrite). |
| Author 2–4 placeholders | Bishai/Hogan decision |
| Any stroke coefficients or ICD lists | Roro has not delivered them |
| Table 2 numbers until the RH/rainfall refit | Would mix two specifications |

When copying from the 15 August Word file, **skip** Methods **and** the Abstract Methods sentence about daily-recovery failure. Use the 24 August `Heat_CVD_Manuscript_live_update.md` instead.

## Comment bubbles first (28 July threads)


Copy each block from `hogan_comment_paste_replies.md` into the matching thread. Do not invent further comments.

| ID | Hogan’s ask | What is now in the draft |
|---|---|---|
| 0 | Amend the running title once results exist | Running title: *Thermal extremes and first CHD/HF hospitalisation* |
| 1 | Author 2–4 after discussion with Dr Bishai | Placeholders retained |
| 3 | Remove “AMI and stroke may respond differently” now that the scope has changed? | Removed as our endpoint. Goggins AMI stays as local daily history [1]; Goggins and Chan 2017 is the closer daily HF paper [21] |
| 4 | Cite the factors; drop housing/behaviour if unmeasured; consider medication | Housing, behaviour, air-conditioning, and medication are all out (medication is also unmeasured). Citations attach to season, trend, pollution, or Ye et al. [9] |
| 8 | “Environmental context has also evolved” sounds like pollutants changed after Goggins 2009 | Rewritten as 2013–2023 EPD general-station means; explicit that this is not a reconstruction of 2000–2009 [1] |
| 9 | Combine the thesis into one sentence after Results | Last Introduction paragraph is now one sentence |
| 54 | Yang C-Y → Yang CY | Kept |

**Flag, not a comment reply:** references [3] and [5] (HKO Year’s Weather 2017 and 2024) are uncited in the body. They are in his 1–8 block, so do not delete them. Ask him to prune or attach.

## Paste / replace (in order)

**If Hogan’s file already has the 15 August paste:** do **not** re-paste the whole 15 August pack. Do the **24 August — do this first** block, or replace the shared file from `Heat_CVD_Manuscript_20260824_hogan.docx`. Rename Results “Core panel” / “Models 1–12” → “Model 1”. Leave his HKO weather paragraph.

**If the live file is still the 28 July skeleton:** paste in this order from `Heat_CVD_Manuscript_live_update.md` / `methods_remainder_paste.md`.

1. **Title.** Keep: *Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023*. Add the running title under it. Do not switch to a methods-forward title in this file.
2. **Abstract.** Replace with the 24 August Abstract in the live_update (Model 1 / Model 2 / Model 3; Table 2 reports Model 1; no daily-recovery failure in Abstract Methods; Table 2 numbers unchanged until Model 2 is fitted).
3. **Introduction.** Replace. Sentence one cites [9] only. Housing, behavioural adaptation, air-conditioning, and medication are not mentioned. [6] is on the 2023 cold-day count. Pollution paragraph reports 2013–2023 EPD means and states they are not Goggins 2000–2009. Closing paragraph is one sentence (estimand + reporting).
4. **Health data.** Paste from `methods_remainder_paste.md`. Leave a Word comment that Roro should replace ICD, timing, and inpatient versus DAE. Influenza stays under Health data. Do not put confirmation-WIP in the body.
5. **Weather.** Leave his HKO paragraph. Paste only the **processing** paragraph after it (75% completeness; general stations; roadside not used; PM2.5 for sensitivity). Do not paste model lists or the December–February cold-day observation under Weather.
6. **Statistical analysis, sensitivity, software.** Paste from `methods_remainder_paste.md` / the live_update. One ethics sentence at the top of Methods (already in the opening). No separate Ethics WIP section.
7. **Results.** Replace from the live_update. Heading is **Model 1**, not “Core panel” and not “Models 1–12”. Tables 1–3 stay (Table 2 numbers unchanged until Model 2 is fitted; add the Word comment). Figures: 1 depletion, 2 DJF heatmap, **3 trend/depletion sensitivity** (not residual ACF). Ljung–Box lag 6 is *p* < 10^−7^ for every CHD Model 1 fit.
8. **Figures (insert as images, then delete the markdown path lines if any remain).**
   - Figure 1 — first-event depletion vs C&SD 35+: `figures/live_identification/figure_B_first_event_depletion.png`
   - Figure 2 — cold-day year × month heatmap: `figures/live_identification/figure_A_cold_day_identification.png`
   - Figure 3 — trend / window / COVID-phase sensitivity: `figures/live_identification/figure_D_trend_depletion_sensitivity.png` (copy of `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`)
   - **Supplement only:** residual ACF `figures/live_identification/figure_C_residual_acf.png` — this is **Supplementary Figure S1** in the live body. Bindings: `supplement_inventory.md`. Optional extras: `outputs/release_chd_hf/figures/figure3_core_forest.svg`, `figure5_se_method_ladder.svg`. Do not insert the release heatmap `figureS1_exposure_correlation.png` as S1.
9. **Discussion / Conclusion / limitations.** Replace. Flu numeral 1.673 is out of the body (direction only; numeral in the release). CHD hot-night window dependence and spline entanglement are explicit. Conclusion remains comparative, not superlative.
10. **References.** Keep 1–21. Flag to Hogan: [3] (2017 yearbook) and [5] (2024 yearbook) are uncited in the body; prune or attach. Do not delete his block unilaterally. Yang CY stays.

## Honesty taken from the 15 August team pass

| Taken | Why |
|---|---|
| Figure 3 = trend/depletion sensitivity; ACF demoted | Identification work vs two numbers already in Results |
| Pre-2020 CHD hot nights in the Abstract | Stops Abstract-vs-Results asymmetry |
| 29 of 132 months with ≥1 official cold day | Verified REAL count; effective information for the HF cold-day contrast |
| Ljung–Box *p* < 10^−7^ | Largest CHD core lag-6 *p* is 1.17 × 10^−8^ |
| Flu numeral out of Discussion | Largest CI-bearing archive effect; not core-adjusted |
| 2021 hot-night record cited to [4] | “At that time,” not an unsourced full-record superlative |
| Daily-recovery failure stays in Results, not Abstract Methods | Hogan: no Results in Methods; calibration refusal is a result |
| Running title + one-sentence thesis | Hogan comments 0 and 9 |
| Housing / behaviour / medication omitted | Hogan comment 4; none of those variables is in the monthly aggregates |
| Pollution paragraph scoped to 2013–2023 | Hogan comment 8; not a reconstruction of Goggins 2000–2009 |

| Not taken | Why |
|---|---|
| Methods-forward title T2 | Live file keeps Hogan’s descriptive title |
| Nature / Science / Cell submission framing | CNS *register* ≠ CNS *venue* |
| Health-econ Monte Carlo / ς | `SYNTHETIC_THEORY`; not a health result |
| Gate 3 freeze | Team-owned |
| HM/CM provisional estimates | Unlocked |
| Numerical 2.63-vs-1.073 or 3.1%-vs-1.022 | Different estimands |
| Sleep / blood-pressure mechanism paragraph | Not measured |
| Rebuilding Stage 3 PDF / A0 poster | Byte-locked |
| Naming medication as an uncontrolled factor | Same problem Hogan flagged for housing |

## After paste

This list is for you to edit in Hogan’s shared file. Do not email him a parallel Word copy; he asked the group to work in the live file.

Venue recommendation (not for the scientific body): Environmental Research as first submission once human blockers close; EHP as one deliberate reach; IJE only if recast and cut; Lancet Planetary Health thematic not editorial; Nature Communications / Nature / Science / Cell not honest on these data. See `manuscript/cns_team/03_sol_journal_target.md` and `manuscript/cns_team/00_parent_synthesis.md`.

If the 15 August pack is already in Hogan’s file, do not paste that pack again. Still apply the **24 August — do this first** block (Methods rewrite, Abstract deletion + comment, KW replies, Table 2 comment). Do not stop at [`REPASTE_2026-08-18.md`](REPASTE_2026-08-18.md) alone. Leave the HKO weather paragraph.
