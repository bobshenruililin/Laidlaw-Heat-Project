# Things to edit in Hogan’s live document

## 24 August 2026 — Hogan PDF + email (do this now)

Commented PDF: repo root `Commented_Heat_CVD_Manuscript_20260824.pdf`. Comment map: `knowledge/2026-08-24_hogan_pdf_comments.md`. Wording authority remains `Heat_CVD_Manuscript_live_update.md`. Methods-only Word: `Heat_CVD_Methods_20260824_paste.docx` (after `python3 scripts/63_hogan_methods_docx.py`).

**Paste Methods in full** from the live Markdown. Hogan already rewrote the weather paragraph in the PDF; the live Markdown copies that paragraph and then says rainfall is a sum and extremes are counts. Do not put the July daily-variables paragraph back.

Also paste, same sitting:

1. Introduction (PDF still has AMI/stroke, age 35, and “environmental context has evolved”).
2. Acknowledgements → `None.`
3. Data/code availability (GitHub for code; no public hospital counts).
4. Bubble replies in `methods_remainder_paste.md`. Do not resolve threads until Hogan has read them.

**Roro comment (do not put in the body):** insert the real HKU/HA West IRB number into the one ethics sentence.

**Do not paste Model 2/3 coefficients.** Governed panels are not on this machine. Climatology day counts are in `data_processed/hogan_climatology_day_counts_2013_2023.csv`. Five-day vs three-day vs one-day official counts are the same Model 1 coefficient rescaled, not new fits.

The 15 August Word file is no longer the Methods paste source.

---

This is the **journal-track** shared file, not the Laidlaw Stage 3 report. Do not paste Laidlaw-essay language into it. Do not email him a parallel Word copy.

**Wording authority:** Markdown `Heat_CVD_Manuscript_live_update.md`.  
**Formatted paste source (15 August):** `Heat_CVD_Manuscript_20260815_collab_draft.docx` (figures embedded; weather paragraph identical to the 28 July text).  
**Comment-bubble replies:** `hogan_comment_paste_replies.md`.  
The 13 August Word copy is **stale**. The 28 July commented original is archived as `Heat_CVD_Manuscript_20260728_hogan_comments.docx` (provenance only; do not paste it back).

Work **in** Hogan’s shared file. His seven unread threads stay on that file. Paste around them, then reply in the bubbles. Do not resolve the threads until he has read the replies.

## Do not touch

| Place | Why |
|---|---|
| Hogan’s *Weather and pollutants data* paragraph, including “Meteorological data was obtained” | His Methods. The 15 August Word file copies it verbatim; leave the live-file paragraph in place rather than duplicating it. |
| Author 2–4 placeholders | Bishai/Hogan decision |
| Any stroke coefficients or ICD lists | Roro has not delivered them |

When copying from the 15 August Word file, **skip** the brown instruction note at the top and the italic weather-lock note under Methods.

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

1. **Title.** Keep: *Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023*. Add the running title under it. Do not switch to a methods-forward title in this file.
2. **Abstract.** Replace with the 15 August Abstract. It now carries the pre-2020 CHD hot-night null (1.011, 0.991–1.032), the stronger pre-2020 HF cold-day interval, and the simulated daily-recovery refusal. Residual ACF values are no longer in the Abstract.
3. **Introduction.** Replace. Sentence one cites [9] only. Housing, behavioural adaptation, air-conditioning, and medication are not mentioned. [6] is on the 2023 cold-day count. Pollution paragraph reports 2013–2023 EPD means and states they are not Goggins 2000–2009. Closing paragraph is one sentence (estimand + reporting).
4. **Health data.** Paste the bridge paragraph. Leave a visible note that Roro should replace ICD, timing, and inpatient versus DAE.
5. **Weather.** Leave his paragraph. Paste the **processing** paragraph immediately after it. New identification sentence: 29 of 132 months carried at least one official cold day (REAL HKO monthly flags).
6. **Influenza, denominators, statistical analysis, daily-recovery, software, ethics.** Paste in full from the draft.
7. **Results.** Replace. Tables 1–3 stay. Figures: 1 depletion, 2 DJF heatmap, **3 trend/depletion sensitivity** (not residual ACF). Ljung–Box lag 6 is now *p* < 10^−7^ for every CHD core model (the live 13 August “*p* < 10^−8^” was false for the hot-night model by a hair).
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
| Daily-recovery sentence restored to Abstract Methods | Fable must-say; still a refusal, not a coefficient |
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

If the 15 August pack is already in Hogan’s file, do not paste it again. Apply only [`REPASTE_2026-08-18.md`](REPASTE_2026-08-18.md) (G3 Results sentence; two Methods/Results SI citations) and attach [`supplement_live_track.md`](supplement_live_track.md). Leave the Abstract and the weather paragraph.
