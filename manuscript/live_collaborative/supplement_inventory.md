# Live-pack supplement inventory

**Authority for Hogan paste:** `Heat_CVD_Manuscript_live_update.md`.  
**Not** the 10 August `manuscript/chd_hf_supplement.pdf` (do not rebuild).  
**Not** Hogan’s shared Word/Google file (Bob pastes; agents do not).

The live body cites three supplementary objects. Those citations resolve here.

| Live-body citation | Object | Path | Provenance |
|---|---|---|---|
| **Supplementary Figure S1** | Residual ACF for the CHD hot-night and HF cold-day models | `figures/live_identification/figure_C_residual_acf.png` | `HA_APPROVED_AGGREGATE` residuals |
| **Supplementary Table S7** | Archive influenza co-exposure (P14; 121 months); CHD 1.673 (1.249–2.243) stays in the supplement | `outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv` | `HA_APPROVED_AGGREGATE`; **not** core-adjusted |
| **Supplementary Table S9** | Archive pollution-staged models (P11; joint Tmax/Tmin; population×days offset) | same file, P11 rows | `HA_APPROVED_AGGREGATE`; **not** core-adjusted |

Filename collisions that must not override this list:

- `outputs/release_chd_hf/supplement/figureS1_exposure_correlation.png` is an **exposure-correlation heatmap**. Live-pack display number is not S1. Map it as Supplementary Figure S4 if assembled.
- `manuscript/chd_hf_supplement.md` uses **section** numbers S7 (M\|D calibration) and S9 (reproducibility) as well as **Tables** S7 and S9 in section S12. The live body means the tables in S12.
- `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` is **manuscript Table 3**, not a supplementary table numbered 4.

Uncited supplement displays (core forest, SE ladder, heatmap) may be assembled later. They do not steal S1, S7, or S9 from the live body.
