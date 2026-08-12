# Things to edit in Hogan’s live document

This is the **journal-track** shared file, not the Laidlaw Stage 3 report. Do not paste Laidlaw-essay language into it. Do not overwrite Hogan’s weather paragraph.

**Paste source (13 August end-game):** `Heat_CVD_Manuscript_20260813_collab_draft.docx`  
Markdown: `Heat_CVD_Manuscript_live_update.md`  
If Hogan has already edited weather, paste from `methods_remainder_paste.md` around his paragraph instead.

## Do not touch

| Place | Why |
|---|---|
| Hogan’s *Weather and pollutants data* paragraph, including “Meteorological data was obtained” | His Methods. Copy only if the 28 July text is still there unchanged. |
| Author 2–4 placeholders | Bishai/Hogan decision |
| Any stroke coefficients or ICD lists | Roro has not delivered them |

## Paste / replace (in order)

1. **Title.** Replace the 28 July AMI/stroke title with: *Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023*.
2. **Abstract.** Replace the yellow “work in progress” with the draft Abstract. Keep exploratory language (all twelve *q* > 0.19). The Abstract now also states DJF cold-day concentration and the two lag-1 ACF values.
3. **Introduction.** Replace the 28 July text. This answers his comment threads and adds two literature upgrades: Goggins and Chan (2017) as the local daily HF admissions anchor [21]; Guo et al. (2024) used for the official hot-night flag versus hourly excess-heat distinction [17], not as a replication. Goggins AMI remains history, not our endpoint. Reply on each comment using `hogan_comment_responses.md`.
4. **Health data.** Paste the bridge paragraph. Leave a visible note that Roro should replace ICD, timing, and inpatient versus DAE.
5. **Weather.** Leave his paragraph. Paste the **processing** paragraph immediately after it (Headquarters aggregation, five-day scaling, cold-day winter concentration 141/145 in December–February, pollution completeness, hot-month rules remain his).
6. **Influenza, denominators, statistical analysis, daily-recovery, software, ethics.** Paste in full from the draft. These are Bob’s remainder.
7. **Results.** Replace “work in progress” with Tables 1–3, Figures 1–3, and the surrounding prose.
8. **Figures (insert as images, then delete the markdown path lines if any remain).**
   - Figure 1 — first-event depletion vs C&SD 35+: `figures/live_identification/figure_B_first_event_depletion.png`
   - Figure 2 — cold-day year × month heatmap: `figures/live_identification/figure_A_cold_day_identification.png`
   - Figure 3 — residual ACF: `figures/live_identification/figure_C_residual_acf.png`
   - Optional extras from `outputs/release_chd_hf/figures/` if he wants a forest or SE-ladder graphic in addition to Tables 2–3: `figure3_core_forest.svg`, `figure5_se_method_ladder.svg`.
9. **Discussion / Conclusion / limitations.** Replace “work in progress.” Keep the refusal of a protected primary claim. Bounded comparisons only: HF–cold with Goggins and Chan (2017); hot nights with Guo et al. (2024) metric distinction. Do not paste HM/CM coefficients or archive flu/NO₂ as adjusted Table 2.
10. **References.** Keep his 1–8 (C&SD repaired as 8). Add 9–21 from the draft. Do not drop Yang CY. New overnight addition is [21] Goggins and Chan 2017.

## Honesty taken from later drafts (approved for *this* file only)

| Taken | Why |
|---|---|
| NW3 CHD hot nights as 1.0003–1.0439 (unrounded 1.000253–1.043860) | Display honesty; Model/HC1 still include 1 |
| Leading-contrast ACF 0.508 / 0.146, now also Figure 3 | Why Newey–West is shown |
| Cold days 141/145 in DJF; remaining variation is between-year winter; Figure 2 | Identification, not a new model |
| First-event depletion vs rising 35+ population; Figure 1 | Bishai’s Table 1 instinct assumed a stable risk set we do not have |
| 500-replicate failure, then worst-cell re-summary; not a general indictment of Basagaña–Ballester | Methods limit without protocol jargon |
| Count ratios, not incidence, without cohort person-time | Estimand |
| Guo official-flag null vs hourly excess heat | Stops the paper from treating monthly official hot-night counts as intensity |
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

## After paste

This list is for you to edit in Hogan’s shared file. Do not email him a parallel Word copy; he asked the group to work in the live file.

The 12 August Outlook reply only tells him you are editing now. It does not replace this paste.
