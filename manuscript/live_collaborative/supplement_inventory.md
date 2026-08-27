# Live-pack supplement inventory

**Authority for Hogan paste:** `Heat_CVD_Manuscript_live_update.md`.  
**Assembled SI (18 August):** [`supplement_live_track.md`](supplement_live_track.md). Rebuild with `python3 scripts/51_build_live_track_supplement.py`.  
**Not** the 10 August `manuscript/chd_hf_supplement.pdf` (do not rebuild).  
**Not** Hogan’s shared Word/Google file (Bob pastes; agents do not).

The live body cites these supplementary objects. They resolve in `supplement_live_track.md`.

| Live-body citation | Object | Path | Provenance |
|---|---|---|---|
| **Supplementary Figure S1** | Residual ACF for the CHD hot-night and HF cold-day models | `figures/live_identification/figure_C_residual_acf.png` | `HA_APPROVED_AGGREGATE` residuals |
| **Supplementary Table S1** | Twelve-contrast uncertainty ladder | `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` | `HA_APPROVED_AGGREGATE` |
| **Supplementary Table S2** | Pre-2020 twelve-contrast NW6 panel (nine of twelve exclude 1) | `outputs/release_chd_hf/supplement/cvd_trend_depletion_sensitivity.csv` `pre_covid` | `HA_APPROVED_AGGREGATE` |
| **Supplementary Figure S2** | SE-method ladder plot | `outputs/release_chd_hf/figures/figure5_se_method_ladder.png` | `HA_APPROVED_AGGREGATE` |
| **Supplementary Figure S3** | Core forest | `outputs/release_chd_hf/figures/figure3_core_forest.png` | `HA_APPROVED_AGGREGATE` |
| **Supplementary Figure S4** | Exposure-correlation heatmap | `outputs/release_chd_hf/supplement/figureS1_exposure_correlation.png` | `REAL` exposures; **not** live S1 |
| **Supplementary Figure S6** | Continuous-temperature trend/window forest (same nine specs as Figure 3) | `figures/live_identification/figure_E_continuous_temperature_sensitivity.png` | `HA_APPROVED_AGGREGATE`; not a copy of release figure 4 |
| **Supplementary Tables S3–S6** | Lag, influence, VIF/joint, residual diagnostics | release supplement CSVs | `HA_APPROVED_AGGREGATE` |
| **Supplementary Table S7** | Archive influenza co-exposure (P14; 121 months); CHD 1.673 (1.249–2.243) stays in the supplement | `outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv` | `HA_APPROVED_AGGREGATE`; **not** core-adjusted |
| **Supplementary Table S8** | Daily-recovery calibration gates | `outputs/release_chd_hf/supplement/methods_feasibility/md_calibration_gate_summary.csv` | `SYNTHETIC_CALIBRATION`; not a health finding |
| **Supplementary Table S9** | Archive pollution-staged models (P11; joint Tmax/Tmin; population×days offset) | same file, P11 rows | `HA_APPROVED_AGGREGATE`; **not** core-adjusted |

Filename collisions that must not override this list:

- `outputs/release_chd_hf/supplement/figureS1_exposure_correlation.png` is an **exposure-correlation heatmap**. Live-pack display number is **S4**.
- `manuscript/chd_hf_supplement.md` uses **section** numbers S7 (M\|D calibration) and S9 (reproducibility) as well as **Tables** S7 and S9 in section S12. The live body means the tables in the live-track SI.
- `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` is Supplementary Table **S1** in the live-track SI; manuscript Table 3 remains the two-contrast ladder.

Uncited HM/CM calendar plots remain provisional and are not given a live-pack display number.
