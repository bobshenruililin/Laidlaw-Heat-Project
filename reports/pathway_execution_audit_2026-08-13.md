# Pathway execution audit — CHD/HF, 13 August 2026

**Question:** Bishai asked for roughly ten methods, then a hot/cold-month catalogue. Have they all been executed?  
**Answer:** The **enabled monthly panel has been run** on the delivered CHD and HF first-event aggregates. Three registry pathways never ran because the file cannot support them. Ninety-eight catalogue recipes were **listed**, not fitted. Fitting the rest would be diminishing returns.

**Provenance:** `HA_APPROVED_AGGREGATE` status files and estimate tables dated 7–10 August 2026. No new health model was fitted for this note. Gate 3 remains open. Stroke was not delivered.

---

## 1. Two layers (do not mix)

| Layer | What it is | Offset | Role now |
|---|---|---|---|
| **Original pathway panel** (`combined_pathway_panel_estimates.csv`, 124 rows) | P01–P18 as registered, both outcomes | Mostly `population_x_days` | Archive / specification diversity. Not the live paper’s Table 2. |
| **Analysis of record** (`outputs/release_chd_hf/tables/table2_core_models.csv`) | Twelve separate single-exposure models (CHD/HF × mean T, Tmax, Tmin, hot nights, cold days, very hot days) | `days_only` | Live manuscript core panel. Newey–West lag-6 display. All twelve BH *q* > 0.19. |

The original P04 CHD hot-night ratio under the population×days joint-ish panel (1.044, 1.012–1.077) is **not** the analysis-of-record 1.022 (1.002–1.042). Quote Table 2 for the paper.

---

## 2. Registry P01–P18 — executed or not

Source: `chd_pathway_panel_status.csv` and `hf_pathway_panel_status.csv` (identical).

| ID | Family | Status | Why |
|---|---|---|---|
| P01 / P01A | Mean temperature | **ok** | Ran, both outcomes |
| P02 / P02A / P02B | Tmax / Tmin | **ok** | Ran |
| P03 | Lag-1 temperature | **ok** | Ran; labelled monthly lag, not a daily DLNM |
| P04 / P04A–C | Official extreme counts | **ok** | Ran; this family became the live core |
| P05 | Hot-night spell days (≥5) | **ok** | Ran |
| P06 | Combined day–night (2D3N window) | **ok** | Ran; later weather engine replaced the approximate 2D3N proxy with Wang’s exact pattern for *exposure construction*, not a new health headline |
| P07 / P07A–D | Heatwave-month multi-def | **ok** | Ran; nested percentile coefficients are not confirmatory |
| P08 | Cold-primary | **ok** | Ran |
| P09 | Age-stratified | **skipped_no_age_sex** | Delivered grain is territory-month, not age bands |
| P10 | COVID / holidays | **ok** | Ran |
| P11 | Pollution-staged (5 stages) | **ok** | Ran; archive, not an adjusted Table 2 |
| P12 | Humidity | **ok** | Ran |
| P13 | Ischaemic vs haemorrhagic split | **disabled** | Needs a stroke subtype file. None exists. |
| P14 | Flu co-exposure | **ok** | Ran on 121/132 months; flu indicator CHD 1.673 (1.249–2.243) is a co-predictor, not a thermal finding |
| P15 | Temperature variability | **ok** | Ran |
| P16 | Pre-COVID window | **ok** | Ran (84 months) |
| P17 | Sex interaction | **skipped_no_age_sex** | Same grain limit as P09 |
| P18 | Cold-month (p05) | **ok** | Ran |

**Count:** 25 enabled IDs in the YAML (including lettered splits). **22 ok** on both CHD and HF. **2 skipped** for missing age/sex. **1 disabled** for missing stroke subtypes.

Bishai’s “~10 methods” request is therefore **met and exceeded** on the data we actually have. The holes are data grain, not unrun code.

---

## 3. Hot/cold-month catalogue — listed vs fitted

The catalogue contains **HM01–HM50** and **CM01–CM48** (98 recipes). That is a definition library.

The **first-wave fitted set** is twelve IDs (`chd_hm_cm_panel_status.csv` / `hf_hm_cm_panel_status.csv`):

| ID | Status | Notes (provisional study-window reference; **not Hogan-locked**) |
|---|---|---|
| HM08, HM15, HM17, HM19, HM23, HM27, HM32 | **ok** | `HM23` (Li event → monthly tail) null for CHD (0.996, 0.941–1.054) and HF (0.964, 0.897–1.036) |
| CM03, CM08, CM15, CM30 | **ok** | HF `CM08` 1.173 (1.049–1.312); HF `CM03` 1.122 (1.023–1.230). Meeting material, not live Table 2 |
| CM05 (`Tmin` ≤ 10 °C monthly proxy) | **skipped_no_variation** | Zero months flagged. The ~10 °C discussion prompt is not currently an executable monthly exposure |

Running the other 86 catalogue IDs on the same 132 months would manufacture a shelf of related coefficients. It would not close Hogan’s lock, Roro’s ICD paragraph, or Gate 3.

---

## 4. What ran *after* the pathway script (also executed)

These are not extra “discoveries.” They are the honesty layer on the same counts.

- Uncertainty ladder Model / HC1 / NW3 / NW6 (`table4_uncertainty_ladder.csv`).
- Trend, year FE, drop-early-months, pre-2020, COVID-phase (`cvd_trend_depletion_sensitivity.csv`). CHD hot nights pre-2020: 1.011 (0.991–1.032).
- Lag-0/1/2 month (`cvd_lag_sensitivity.csv`).
- Influence / Cook (`cvd_influence_sensitivity.csv`); leaders are 2020-02 and 2022-02.
- Offset sensitivity (days vs population×days vs none): coefficients barely move; the *sentence* (count ratio vs incidence) does.
- Joint vs separate (`cvd_single_vs_joint_estimates.csv`); VIF (`cvd_exposure_vif.csv`).
- Residual ACF and Ljung–Box.
- Clean-room Basagaña–Ballester daily-recovery: **failed** 500-replicate calibration; no real daily coefficient.
- Identification figures (DJF cold days; first-event depletion vs C&SD 35+; residual ACF).

---

## 5. What has *not* been executed (and should not be forced)

| Missing | Blocker | Correct next step |
|---|---|---|
| P09 / P17 | No age/sex monthly counts | Ask Roro (ranked ask #3). Do not impute bands. |
| P13 | No stroke file, no subtype | Named pending. Do not invent ICD splits. |
| Remaining HM01–50 / CM01–48 | Hogan has not locked reference period | Playbook 01 after written notes. Do not fish. |
| Hourly `HNe` (Guo intensity) | Would rewrite Hogan’s weather Methods | W10; his call. |
| Cohort still-at-risk person-time | Not delivered | Ranked ask #2. Days offset stays honest until then. |
| 2024 health months | After the 132-month window | Optional climate sentence only. |

---

## 6. Diminishing returns

**Already past the useful frontier for new *thermal* models on this file.** Another encoding of the same 132 months will not fix first-event depletion, missing person-time, or *q* > 0.19.

Hours still buy something if they produce **reports, public honesty, or meeting cards**, not new rows in Table 2:

1. This audit (what ran).
2. Public surfaces that still say “waiting for stroke.”
3. Hogan identification (pre-2020 CHD null; NW ladder narrower than Model).
4. Teaching the estimand (count ratio ≠ incidence).

Hours that look like work and are not: refitting P05–P07 under a new spline; rebuilding the frozen Stage 3 PDF; promoting `CM08` into the live paper; reconstructing hourly heat without a weather rewrite.

---

## 7. Core mission this cycle stayed pointed at

Keep the project honest after the data arrived: one exploratory monthly first-event panel, fully reported, no confirmatory freeze, public writing that no longer pretends we are still waiting for the file Roro already sent.
