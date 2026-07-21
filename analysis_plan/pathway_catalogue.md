# Pathway registry — stroke × thermal extremes (Hong Kong, 2013–2023)

**Purpose:** Machine- and human-readable catalogue of analysis pathways.  
**Rule:** Every estimate in outputs must carry a `pathway_id`. Present as a **panel**, not ten discoveries.  
**Headline freeze:** Gate 3 names one primary pair (default proposal: `P02` + `P04`).  
**SAP:** `analysis_plan/statistical_analysis_protocol.md`

Implementation: `scripts/20_fit_pathway_panel.R` reads `pathway_registry.yml`.

---

## Scientific posture

1. **Estimand:** monthly hospital-*burden* associations for stroke aggregates — not daily DLNM triggering (Goggins) and not excess-death counts (Liu/Ren/Bishai mortality).
2. **Why many pathways:** no universal heatwave definition (Guo et al. EHP 2017; Wang/Ren 2019; lab multi-definition mortality work). Specification diversity is the design.
3. **Honesty:** label synthetic dry-runs `SYNTHETIC`; never mix estimands across scales.

---

## Core pathways (run by default)

| ID | Family | Primary exposure(s) | Model skeleton | Literature anchor |
|---|---|---|---|---|
| P01 | Continuous Tmean | `mean_temp` | NB + offset + season + trend | Classical temperature–health series |
| P02 | Continuous Tmax/Tmin | `mean_tmax`, `mean_tmin` | NB + offset + season + trend | Bishai 12 Jul merge request |
| P03 | Lag-1 temperature | `lag1_mean_tmax` / `lag1_mean_tmin` | Same | Delayed burden / prior-month heat-cold |
| P04 | Official extreme counts | `hot_nights`, `cold_days`, `very_hot_days` | Scaled per 5 days | HKO policy metrics; Guo 2024 |
| P05 | Spell burden (Ren/Wang) | hot-night / very-hot spell day counts | NB | Wang et al. 2019 EHWE |
| P06 | Combined day–night | `days_in_2d3n_window` | NB | Wang/Ren 2D3N |
| P07 | Heatwave-month multi-def | p90/p95/p975 month + VHD spell | Binary indicators | Guo EHP 2017 grid (monthly collapse) |
| P08 | Cold-primary | `cold_days`, cold-spell touch | NB | Goggins 2012; Yang/Chong 2025 |
| P09 | Age-stratified | Tmax/Tmin × age_band65 | Interaction | Aging / 65+ |
| P10 | Seasonality / COVID / holidays | Core + covid + holidays | Sensitivity ladder | Care-seeking shocks |
| P11 | Pollution-staged | Core + NO₂/PM₂.₅/O₃ stages | Nested models | Goggins NO₂; Guo 2025 |
| P12 | Humidity / AH | Core + absolute humidity | Sensitivity | Cold–humidity entanglement |

## Extension pathways

| ID | Family | Requires | Notes |
|---|---|---|---|
| P13 | IS vs HS split | Subtype in stroke file | Disabled until present |
| P14 | Flu co-exposure | CHP Flu Express | Complete-case (early-2013 gap) |
| P15 | Temperature variability | Daily diurnal-range mean | JoGH 2023 TV–hospitalisation |
| P16 | Pre-COVID only | Drop 2020–2022 | Care-seeking sensitivity |
| P17 | Sex interaction | Age×sex grain | Goggins HS sex pattern |
| P18 | Cold-month (p05) | Built in exposures | Complements P08 |

---

## Default model form (monthly counts)

```text
n_events ~ f(exposure) + month_factor + ns(time_index, df=4) [+ covid_phase]
         + offset(log(population * days_in_month))
family: negative binomial (MASS::glm.nb) or quasi-Poisson fallback
```

Cluster-robust SEs by `month_id` when strata exist.

---

## Reporting products

| Output | Path |
|---|---|
| Pathway coefficient panel | `outputs/tables/pathway_panel_estimates.csv` |
| Model fit diagnostics | `outputs/tables/pathway_panel_fit_stats.csv` |
| Headline residual diagnostics | `outputs/tables/pathway_headline_diagnostics.csv` |
| Forest figure | `outputs/figures/pathway/pathway_panel_forest.png` |
| Human summary | `outputs/reports/pathway_panel_summary.md` |
| Manuscript tables | `outputs/tables/manuscript_pathway_panel_table.csv` |

---

## YAML machine registry

See `analysis_plan/pathway_registry.yml`.
