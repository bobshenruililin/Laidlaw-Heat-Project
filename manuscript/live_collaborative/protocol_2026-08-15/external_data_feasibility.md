# External-data feasibility — 15 August 2026

Protocol §7. Public web may be searched. Nothing here is merged into the primary health model unless authors approve a protocol change.

| Candidate | Source / version | Geography | Time / grain | Role if used | Compatibility | Decision |
|---|---|---|---|---|---|---|
| HKO Headquarters daily T and official flags | HKO open data; yearbooks | One station, applied territory-wide | Daily → month, 2013–2023 | **Primary exposure** (already in) | Matches Hogan weather paragraph | Keep. Live paper stays on Headquarters. |
| HKO Year’s Weather 2013/2017/2021/2024 | Official HTML | Headquarters | Annual | Contextual validation | 2017 unused in body; 2024 after health window | Cite 2013/2021 in body; retain 2017/2024 as Hogan bibliography; do not add 2024 to models |
| EPD EPIC general-station NO₂, SO₂, O₃, PM2.5 | Project crawl + GIA annex check | HK general stations (roadside reserved) | Daily → month | Contextual + staged archive | 2013–2023 only; not a Goggins 2000–2009 reconstruction | Do not silently extend to 2000–2009 |
| C&SD Table 110-01001 | data.gov.hk | HK resident population | Mid-year → linear month | Offset sensitivity / Figure 1 | General population, not T2D/HTN risk set | Already used as sensitivity/context |
| ERA5-Land at Observatory coordinate | Open-Meteo cache, script 48 | Point, not districts | Daily → month | **Limitation / corroboration of means**, not a substitute encoding | Mean Tmin tracks; 28 °C-night counts do not | Already one Limitations sentence. Do not put health on cells. |
| King’s Park / Waglan official flags | HKO open data | Other stations | Daily | Sensitivity of exposure definition | Jaccard vs HQ low | Hogan-first; not in live body |
| WorldPop night weighting | Public raster | Spatial | — | Exposure-only equity description | Not linked to HA outcomes | Stay out of live paper |
| CHP Flu Express | Public summaries | HK | Monthly, 121/132 | Archive covariate | Gap early 2013; never zero-fill | Already documented |
| HA medication / BMI | Not public | Person-level | — | Would change estimand | **Not delivered** | Blocked |
| Hospital costs / QALY sets | Various | — | — | Health economics | No utilisation prices in the HA aggregates | Do not force CEA |
| Guo 2024 hourly HNe | Published paper | HK hot seasons 2000–2019 | Daily hospitalisation | Literature distinction | Different outcome and grain | Cite; do not re-analyse their microdata |

**Access dates.** HKO 2013 yearbook and Guo 2024 PDF Table 3 fetched 15 August 2026 (this session). GIA pollution annex previously PI-checked 13 August 2026.

**Licensing.** HKO and EPD are official public series already in the project. ERA5 via Open-Meteo is public reanalysis; live paper does not treat it as HKO.
