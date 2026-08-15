# Things to edit in Hogan’s live document

This is the **journal-track** shared file, not the Laidlaw Stage 3 report. Do not paste Laidlaw-essay language into it. Do not overwrite Hogan’s weather paragraph.

**Paste source (15 August protocol pass on the 14 August CNS draft):** `Heat_CVD_Manuscript_live_update.md`  
The 13 August Word copy (`Heat_CVD_Manuscript_20260813_collab_draft.docx`) is behind this markdown. Paste from the markdown. Do not email a parallel Word copy.

If Hogan has already edited weather, paste from `methods_remainder_paste.md` around his paragraph instead.

## Do not touch

| Place | Why |
|---|---|
| Hogan’s *Weather and pollutants data* paragraph, including “Meteorological data was obtained” | His Methods. Copy only if the 28 July text is still there unchanged. |
| Author 2–4 placeholders | Bishai/Hogan decision |
| Any stroke coefficients or ICD lists | Roro has not delivered them |

## Paste / replace (in order)

1. **Title.** Replace the 28 July AMI/stroke title with: *Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis among people with type 2 diabetes or hypertension in Hong Kong, 2013–2023*. Keep the italic working-title note under affiliations (Hogan comment 0).
2. **Abstract.** Replace the yellow “work in progress” with the draft Abstract. Keep exploratory language (all twelve *q* > 0.19). The Abstract states DJF cold-day concentration, June–September hot-night intensity (July 2013, 1 night; July 2022, 25), and the two lag-1 ACF values.
3. **Introduction.** Replace the 28 July text. This answers his comment threads and adds two literature upgrades: Goggins and Chan (2017) as the local daily HF admissions anchor [21]; Guo et al. (2024) used for the official hot-night flag versus hourly excess-heat distinction [17], not as a replication. Goggins AMI remains history, not our endpoint. Reply on each comment using `hogan_comment_responses.md`.
4. **Health data.** Paste the bridge paragraph. Leave a visible note that Roro should replace ICD, timing, and inpatient versus DAE.
5. **Weather.** Leave his paragraph. Paste the **processing** paragraph immediately after it (Headquarters aggregation, five-day scaling, cold-day winter concentration 141/145 in December–February, pollution completeness, hot-month rules remain his).
6. **Influenza, denominators, statistical analysis, daily-recovery, software, ethics.** Paste in full from the draft. These are Bob’s remainder.
7. **Results.** Replace “work in progress” with Tables 1–3, Figures 1–4, and the surrounding prose. Figure 3 is the hot-night twin of Figure 2. Hogan may demote Figure 3 to a supplement; do not drop the July 1 vs 25 sentence if he does.
8. **Figures (insert as images, then delete the markdown path lines if any remain).**
   - Figure 1 — first-event depletion vs C&SD 35+: `figures/live_identification/figure_B_first_event_depletion.png`
   - Figure 2 — cold-day year × month heatmap: `figures/live_identification/figure_A_cold_day_identification.png`
   - Figure 3 — hot-night year × month heatmap (ggplot, vmax 25): `figures/live_identification/figure_D_hot_night_identification.png`
   - Figure 4 — residual ACF: `figures/live_identification/figure_C_residual_acf.png` (numbers already in the Abstract and Results; Fable recommends demoting this to a supplement if the live file is crowded).
   - Preferred extra if a third identification figure is wanted: `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png` (CHD hot-night interval includes 1 before 2020; HF cold-day interval strengthens). Caption: “Core count ratios across trend and first-event sensitivities (Newey–West lag-6 intervals).”
   - Optional extras from `outputs/release_chd_hf/figures/` if he wants a forest or SE-ladder graphic in addition to Tables 2–3: `figure3_core_forest.svg`, `figure5_se_method_ladder.svg`.
9. **Discussion / Conclusion / limitations.** Replace “work in progress.” Keep the refusal of a protected primary claim. Bounded comparisons only: HF–cold with Goggins and Chan (2017); hot nights with Guo et al. (2024) metric distinction. The 14 August pass adds: hot-night identifying variation is summer intensity (Figure 4); ERA5 monthly mean Tmin tracks Headquarters while 28 °C-night counts do not. The 15 August pass states that archive influenza 1.673 used a general-population × days offset, not the core days-in-month offset. Do not paste HM/CM coefficients or archive flu/NO₂ as adjusted Table 2. Do not paste daily Jaccard 0.031, 449 vs 17, or 0.045 as a health attenuation factor.
10. **References.** Keep his 1–8 (C&SD repaired as 8). Add 9–21 from the draft. Do not drop Yang CY. New overnight addition is [21] Goggins and Chan 2017. Do not add Mistry unless Hogan asks. Hogan’s unused yearbooks [3] 2017 and [5] 2024 stay in the list; do not attach 2024 as a health year.
11. **ERA5 limitation (in the markdown already; Hogan can strike).** One sentence after the existing territory-wide limitation. Source: `limitation_station_grid_bridge.md`. Do not overwrite his weather paragraph. Do not treat 0.045 as a health attenuation factor.
12. **Intensive-margin identification (in the markdown already; Hogan can strike Figure 3).** June–September always had ≥1 official hot night; remaining contrast is July intensity (1 vs 25). Source: `limitation_intensive_margin.md`. Different limitation from the station–grid check. Do not paste 95.4% or the 14 overlapping nights.
13. **Still optional, after Hogan has seen the identification-profile card.** One supplementary table (six encodings × identifying share / intensive split / family / instrument). Card: `reports/hogan_identification_profile_2026-08-14.md`. Do not paste identifying-share percentages, the reliability curve, Jaccard 0.031, or the fourteen nights into Methods.
14. **Competing interest.** Do not paste “The authors declare no competing interests.” Paste: “Each author will complete a competing-interest statement before journal submission.”
15. **Introduction pollution paragraph (comment 8).** Keep 2013–2023 EPD means. Include the sentence that this is not a 2000–2009 reconstruction. Do not use “pathway variable.”

## Honesty taken from later drafts (approved for *this* file only)

| Taken | Why |
|---|---|
| NW3 CHD hot nights as 1.0003–1.0439 (unrounded 1.000253–1.043860) | Display honesty; Model/HC1 still include 1 |
| Leading-contrast ACF 0.508 / 0.146, now also Figure 3 | Serial dependence is part of the inferential problem; not a claim that model-based intervals are too narrow |
| CHD hot-night Newey–West ladder narrower than Model | Table 3; Discussion states this as caution, not confirmation |
| CHD hot nights pre-2020 1.011 (0.991–1.032) and COVID-phase 1.013 (0.994–1.033) | Same paid sensitivity table as the HF pre-2020 interval; prose only, not Table 2 |
| Cold days 141/145 in DJF; remaining variation is between-year winter; Figure 2 | Identification, not a new model |
| First-event depletion vs rising 35+ population; Figure 1 | Bishai’s Table 1 instinct assumed a stable risk set we do not have |
| 500-replicate failure, then worst-cell re-summary; not a general indictment of Basagaña–Ballester | Methods limit without protocol jargon |
| Count ratios, not incidence, without cohort person-time | Estimand |
| Guo official-flag null −0.2% (−1.2% to 0.7%) vs hourly excess heat | Stops the paper from treating monthly official hot-night counts as intensity |
| Goggins and Chan 2017 as HF history | Closer local daily HF evidence than AMI or stroke |

| Not taken | Why |
|---|---|
| Trimming the Laidlaw report to 3,000 words | Different document; Sol copy stays |
| Internal F1.1/F1.2 labels | Process language, not journal Methods |
| Gate 3 / Laidlaw admin | Not this file |
| Goggins 2017 RR 2.63 compared with 1.073 | Different estimand; direction only |
| Guo 3.1% compared with 1.022 | Daily hot-season emergency hospitalisation ≠ monthly first-event CHD |
| Sleep / blood-pressure mechanism paragraph | Not measured; Hogan’s rule is not to name factors we lack |
| Provisional HM/CM (`CM08`, `HM23`, `CM05`) | Unlocked definition family; Explore memo only |
| Archive flu 1.673 as an adjusted thermal estimate | Kept in Discussion as why confounding is unresolved |
| 2019 as a health “experiment” | One-cold-day year is exposure natural history only |
| 2024 HKO extremes (50 hot nights, 52 very hot days, 11 cold days) as a health year | After the 132-month window. Optional one-sentence Discussion context only, if Hogan wants post-sample climate. PI-checked: `knowledge/2026-08-13_pi_hko_yearbook_check.md` |
| Chau/Pun 2025, EcoEnv 2025, Tian 2016 as live citations | Parked local papers; different estimands. Human nod required. |

## After paste

This list is for you to edit in Hogan’s shared file. Do not email him a parallel Word copy; he asked the group to work in the live file.

The 12 August Outlook reply only tells him you are editing now. It does not replace this paste.
