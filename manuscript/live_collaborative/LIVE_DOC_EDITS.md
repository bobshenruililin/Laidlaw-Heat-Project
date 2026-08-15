# Things to edit in Hogan’s live document

This is the **journal-track** shared file, not the Laidlaw Stage 3 report. Do not paste Laidlaw-essay language into it. Do not overwrite Hogan’s weather paragraph.

**Paste source (15 August, CNS-register team merge):** Markdown `Heat_CVD_Manuscript_live_update.md`.  
The 13 August Word copy (`Heat_CVD_Manuscript_20260813_collab_draft.docx`) is **stale** relative to this Markdown. Paste from Markdown, or rebuild Word locally; do not email Hogan a parallel Word copy.

## Do not touch

| Place | Why |
|---|---|
| Hogan’s *Weather and pollutants data* paragraph, including “Meteorological data was obtained” | His Methods. Copy only if the 28 July text is still there unchanged. |
| Author 2–4 placeholders | Bishai/Hogan decision |
| Any stroke coefficients or ICD lists | Roro has not delivered them |

## Paste / replace (in order)

1. **Title.** Keep: *Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023*. Do not switch to a methods-forward title in this file.
2. **Abstract.** Replace with the 15 August Abstract. It now carries the pre-2020 CHD hot-night null (1.011, 0.991–1.032), the stronger pre-2020 HF cold-day interval, and the simulated daily-recovery refusal. Residual ACF values are no longer in the Abstract.
3. **Introduction.** Replace. Sentence one cites [9] only. [6] is on the 2023 cold-day count. Closing paragraph states the contribution as identification displays, not a discovery.
4. **Health data.** Paste the bridge paragraph. Leave a visible note that Roro should replace ICD, timing, and inpatient versus DAE.
5. **Weather.** Leave his paragraph. Paste the **processing** paragraph immediately after it. New identification sentence: 29 of 132 months carried at least one official cold day (REAL HKO monthly flags).
6. **Influenza, denominators, statistical analysis, daily-recovery, software, ethics.** Paste in full from the draft.
7. **Results.** Replace. Tables 1–3 stay. Figures: 1 depletion, 2 DJF heatmap, **3 trend/depletion sensitivity** (not residual ACF). Ljung–Box lag 6 is now *p* < 10^−7^ for every CHD core model (the live 13 August “*p* < 10^−8^” was false for the hot-night model by a hair).
8. **Figures (insert as images, then delete the markdown path lines if any remain).**
   - Figure 1 — first-event depletion vs C&SD 35+: `figures/live_identification/figure_B_first_event_depletion.png`
   - Figure 2 — cold-day year × month heatmap: `figures/live_identification/figure_A_cold_day_identification.png`
   - Figure 3 — trend / window / COVID-phase sensitivity: `figures/live_identification/figure_D_trend_depletion_sensitivity.png` (copy of `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`)
   - **Supplement only:** residual ACF `figures/live_identification/figure_C_residual_acf.png` (was main Figure 3 on 13 August). Optional extras: `outputs/release_chd_hf/figures/figure3_core_forest.svg`, `figure5_se_method_ladder.svg`.
9. **Discussion / Conclusion / limitations.** Replace. Flu numeral 1.673 is out of the body (direction only; numeral in the release). CHD hot-night window dependence and spline entanglement are explicit. Conclusion remains comparative, not superlative.
10. **References.** Keep 1–21. Flag to Hogan: [3] (2017 yearbook) and [5] (2024 yearbook) are uncited in the body; prune or attach. Do not delete his block unilaterally.

## Honesty taken from the 15 August team pass

| Taken | Why |
|---|---|
| Figure 3 = trend/depletion sensitivity; ACF demoted | Identification work vs two numbers already in Results |
| Pre-2020 CHD hot nights in the Abstract | Stops Abstract-vs-Results asymmetry |
| 29 of 132 months with ≥1 official cold day | Verified REAL count; effective information for the HF cold-day contrast |
| Ljung–Box *p* < 10^−7^ | Largest CHD core lag-6 *p* is 1.17 × 10^−8^ |
| Flu numeral out of Discussion | Largest CI-bearing archive effect; not core-adjusted |
| 2021 hot-night record cited to [4] | “At that time,” not an unsourced full-record superlative |
| Daily-recovery sentence restored to Abstract Methods | Fable must-say; still a refusal, not a coefficient |

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

## After paste

This list is for you to edit in Hogan’s shared file. Do not email him a parallel Word copy; he asked the group to work in the live file.

Venue recommendation (not for the scientific body): Environmental Research as first submission once human blockers close; EHP as one deliberate reach; IJE only if recast and cut; Lancet Planetary Health thematic not editorial; Nature Communications / Nature / Science / Cell not honest on these data. See `manuscript/cns_team/03_sol_journal_target.md` and `manuscript/cns_team/00_parent_synthesis.md`.
