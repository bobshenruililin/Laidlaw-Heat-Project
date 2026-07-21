# Pathway registry — stroke × thermal extremes (Hong Kong, 2013–2023)

**Purpose:** Machine- and human-readable catalogue of analysis pathways.  
**Rule:** Every estimate in outputs must carry a `pathway_id`. Present as a **panel**, not ten discoveries.  
**Headline freeze:** Gate 3 names one primary pair (default proposal: `P02` + `P04`).

Implementation: `scripts/20_fit_pathway_panel.R` reads this file.

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
| P03 | Lag-1 temperature | `lag1_mean_tmax` (and/or lag1 Tmean/Tmin) | Same | Delayed burden / prior-month heat-cold |
| P04 | Official extreme counts | `hot_nights`, `cold_days`, `very_hot_days` | Scaled per 5 days | HKO policy metrics; debrief M4 |
| P05 | Spell burden (Ren/Wang) | `days_in_hot_night_spell_ge5`, `days_in_very_hot_spell_ge5` | NB | Wang et al. 2019 EHWE spells |
| P06 | Combined day–night | `days_in_2d3n_window` or `month_has_2d3n_window` | NB | Wang/Ren 2D3N |
| P07 | Heatwave-month indicators | `hw_month_tmean_p95`, `hw_month_tmax33_spell` | Binary / count | Guo EHP multi-def; Liu/Bishai 4 defs (monthly collapse) |
| P08 | Cold-primary | `cold_days`, `days_in_cold` / cold-spell metrics | NB | Goggins 2012 stroke; Yang/Chong 2025 cold+flu |
| P09 | Age-stratified | Preferred exposure from P02/P04 | Stratum or interaction | Aging / 65–69 & 70–74 |
| P10 | Seasonality / COVID / AH | Core + `covid_phase` / AH / holidays | Sensitivity ladder | Guo 2024; COVID care-seeking |
| P11 | Pollution-staged | Core + NO2 / PM25 / O3 staged | Nested models | Goggins NO2; Guo 2025 temp×pollution |
| P12 | Humidity / AH pathway | Core + `absolute_humidity` | Sensitivity | Cold–humidity entanglement |

## Extension pathways (run if data allow)

| ID | Family | Requires | Notes |
|---|---|---|---|
| P13 | IS vs HS split | Subtype in stroke file | Reinstate Goggins-style separation |
| P14 | Flu co-exposure | CHP Flu Express monthly positivity | Yang/Chong 2025 |
| P15 | Temperature variability | Monthly mean diurnal range proxy | HK TV–hospitalisation literature |
| P16 | Pre-COVID only | Drop 2020–2022 | Care-seeking shock sensitivity |
| P17 | Roadside pollution | Roadside EPIC files | Sensitivity only |

---

## Default model form (monthly counts)

For territory-month aggregates:

```text
n_events ~ f(exposure) + month_factor + ns(time_index, df=4) [+ covid_phase]
         + offset(log(population_35plus * days_in_month))
family: negative binomial (MASS::glm.nb) or quasi-Poisson fallback
```

For month × age × sex aggregates: add `age_group + sex` (and interactions only in P09).

Cluster-robust SEs by `month_id` when strata exist.

---

## Reporting products

| Output | Path |
|---|---|
| Pathway coefficient panel | `outputs/tables/pathway_panel_estimates.csv` |
| Model fit diagnostics | `outputs/tables/pathway_panel_fit_stats.csv` |
| Human summary | `outputs/reports/pathway_panel_summary.md` |
| Figure: exposure overlay | `outputs/figures/pathway/` |

---

## YAML machine registry

See `analysis_plan/pathway_registry.yml`.
