# Pathway × literature map (multimedia handout)

**Purpose:** Show how the labelled analysis panel is anchored—not invented.  
**Credit:** Weather/heat framing and hot-month thinking — **Hogan**; outcome construction — **Roro**; multi-method plan — **Dr Bishai**.  
**Honesty:** Enabled pathways can be dry-run on synthetic outcomes; coefficients are not findings.

| ID | Title | Exposures (short) | Anchor | One-line rationale |
|---|---|---|---|---|
| P01 | Continuous Tmean | `mean_temp` | Goggins; Gasparrini 2015 | Classical continuous temperature–health series |
| P02 | Tmax + Tmin (headline proposal) | `mean_tmax`, `mean_tmin` | Bishai monthly merge; Chan/Goggins | Day/night separation for monthly burden |
| P03 | Lag-1 temperature | lag1 Tmax/Tmin | Bishai original lag note | Prior-month heat/cold may still shape monthly counts |
| P04 | Official extreme counts (headline proposal) | hot nights, VHD, cold days | HKO; Guo 2024 | Policy metrics necessary; binary alone may be weak |
| P05 | Spell burden | days in HN/VHD spells | Wang/Ren 2019 | Sustained extremes ≠ isolated extreme days |
| P06 | 2D3N burden | days in 2D3N window | Wang/Ren 2019 | Combined day–night event morphology |
| P07 | Heatwave-month multi-def | p90/p95/p975 + spells | Guo/Gasparrini 2017; **Hogan** hot-month | No universal HW definition; count→tail months welcome |
| P08 | Cold-primary | cold days, cold spells | Goggins 2012; Yang/Chong 2025 | HK stroke literature is cold-relevant |
| P09 | Age 65+ interaction | Tmax/Tmin × age band | **Hogan** 65–69/70–74; Goggins | Ageing person-time and effect modification |
| P10 | COVID / holidays | P02 + covid/holidays | Care-seeking shocks (methods) | Sensitivity, not centrepiece |
| P11 | Pollution-staged | P02 + NO₂/PM/O₃ stages | Goggins 2013; Guo 2025 | Stage pollutants; O₃ last |
| P12 | Absolute humidity | P02 + AH | Yang/Chong AH preference | Prefer AH over RH entangled with T |
| P13 | IS vs HS | subtype strata | Goggins 2012 | **Disabled** until subtype exists |
| P14 | Flu co-exposure | T + cold + flu | Yang/Chong 2025 | Cold–infection confounding/mediation |
| P15 | Temperature variability | mean diurnal range | Tian/Qiu 2023 | TV linked to circulatory admissions |
| P16 | Pre-COVID window | P02, year<2020 | Methods sensitivity | Test COVID-era care-seeking |
| P17 | Sex interaction | T × sex | Goggins 2012 | Sex patterns in HS especially |
| P18 | Cold-month (p05) | cold month + cold days | Yang/Chong 5th pct | Complements day-count cold metrics |

## Expanded hot/cold month pathways

These families expand `P07` and `P18`; they do not replace the `P01`–`P18` panel. Full operational rules are in [`../../analysis_plan/hot_cold_month_catalogue.md`](../../analysis_plan/hot_cold_month_catalogue.md).

| ID | Definition family | Main anchor / rationale |
|---|---|---|
| H01 | Official absolute hot months | HKO hot-night, very-hot-day and warning metrics |
| H02 | Monthly percentile heat | P07; relative monthly temperature tails |
| H03 | Day/night spell heat | Wang/Ren persistence forms |
| H04 | Combined day–night heat | Wang/Ren 2D3N form |
| H05 | Atmospheric event count-to-tail | Li et al. event rule; monthly adaptation credited to **Hogan** |
| H06 | Percentile × duration grid | Guo et al. 2017 specification diversity |
| H07 | Heat intensity | Degree-day, peak and event-intensity alternatives |
| H08 | Heat compound exposures | Heat–ozone and heat–humidity, with component main effects |
| H09 | Seasonal and anomaly heat | Separates climatological anomaly from calendar season |
| H10 | Persistence and onset | Two-month persistence and thermal transitions |
| H11 | Jasmine-definition heat extension | Exact source rule required; current candidates remain provisional |
| H12 | Frozen hot co-primary | One team-frozen H05/H11 member; remaining definitions are sensitivities |
| C01 | Official cold-day months | HKO ≤12°C counts |
| C02 | Bishai ~10°C sensitivity | Discussion-motivated cutoff, not a biological threshold |
| C03 | Monthly percentile cold | P18 lower-tail monthly temperature |
| C04 | Cold spells | Persistent HKO-threshold cold events |
| C05 | Cold event count-to-tail | Symmetric event-count and day-burden family |
| C06 | Cold intensity | Cold degree-days and peak severity |
| C07 | Cooling transitions | Rapid cooling and cold-period onset |
| C08 | Cold–influenza compound | Yang/Chong rationale; explicit missingness |
| C09 | Cold–humidity/pollution compound | Staged covariates with component main effects |
| C10 | Season, anomaly and persistence | Separates winter, anomaly and sustained cold |
| C11 | Jasmine-definition cold extension | Exact source rule required; current candidates remain provisional |
| C12 | Frozen cold co-primary | One team-frozen C01/C03/C04 member; remaining definitions are sensitivities |
| Jasmine extension | Definition-harmonised extension through 2023 | Confirm source first; preserve its definition/reference period; distinguish daily mortality from monthly stroke burden; see [`jasmine_extension_protocol.md`](../../analysis_plan/jasmine_extension_protocol.md) |

**Gate 3 proposal (team freeze):** P02 + P04.  
**Show with:** `reports/laidlaw_stage3/essay_lit_methods.md`
