# Comparison: Goggins-era daily studies vs this monthly CHD/HF first-event panel

**Updated:** 13 August 2026. The third column is the **delivered** live-manuscript contract, not the July AMI/stroke proposal.

| Dimension | Goggins AMI (2013) | Goggins stroke (2012) | This study (live manuscript) |
|---|---|---|---|
| Study period | 2000–2009 | 1999–2006 | 2013–2023 |
| City / population | Hong Kong (+ Taiwan cities for AMI) | Hong Kong public hospitals, age 35+ | Hong Kong; people diagnosed with T2D and/or HTN during 2013–2023 |
| Outcome | AMI admissions | Haemorrhagic and ischaemic stroke separately | First recorded hospitalisation after first CHD diagnosis; first recorded hospitalisation after first HF diagnosis. Admission cause not recorded. Stroke named but not delivered |
| Coding / construction | ICD-based AMI | ICD stroke subtypes | Field-level ICD lists remain with the outcome co-investigator. Delivered columns labelled `chd_inpatient`, `hf_inpatient` |
| Temporal resolution | **Daily** | **Daily** | **Monthly** (132 territory-months) |
| Temperature metric | Mean temperature (smooth / threshold) | Mean temperature | Monthly mean T, mean Tmax, mean Tmin, and official extreme-day counts (hot nights, very hot days, cold days), the last three per five days |
| Threshold | ~24 °C for cold effect (HK AMI) | IS below ~22 °C; HS linear across range | Hot night Tmin ≥ 28 °C; very hot day Tmax ≥ 33 °C; cold day Tmin ≤ 12 °C (HKO climatological flags) |
| Lag structure | Multi-day averages (e.g. 0–13) | HS lags 0–4; IS lags 0–13 | Same-month continuity; lag-1/2 month as labelled sensitivity, not a recovered daily lag |
| Pollutants | NO2 important for AMI | Pollutants NS for stroke | Assembled; staged archive models exist; **not** continuity-adjusted versions of the twelve-contrast panel |
| Seasonality / trend | Controlled in GAM | Controlled in GAM | Calendar-month indicators + natural cubic spline of time (4 df) |
| Age groups | Reported in related work | Stronger HS effects in older adults | Territory totals only. Ages 65–69 and 70–74 were requested and not delivered |
| Denominator | Daily admissions | Daily admissions | Days-in-month offset. C&SD 35+ population is a sensitivity only. No T2D/HTN still-at-risk person-time |
| Effect measure | % change per 1 °C | % change per 1 °C | Count ratio per 1 °C or per five extreme days |
| Primary finding | Cold-dominant AMI; little heat | Cold-related HS and threshold IS | Exploratory panel: all twelve core *q* > 0.19. HF cold days SE-concordant; CHD hot nights SE-sensitive. Not a protected confirmatory claim |
| Comparability | Daily DL/GAM ≠ monthly extreme-count ratios; different decades and exposures | Same | Do **not** compare coefficients directly or call this a replication |

## Why coefficients are not directly comparable

1. **Temporal aggregation.** Daily distributed-lag effects capture acute triggering. Monthly counts capture a coarser residual after calendar month and trend.
2. **Exposure scaling.** Per 1 °C mean temperature is not per five hot nights or cold days.
3. **Outcome.** AMI or stroke *admissions* are not first CHD/HF hospitalisation after first diagnosis in a diabetes/hypertension cohort without recorded admission cause.
4. **Risk set.** Goggins analysed daily hospital series. This panel has no still-at-risk cohort person-time; estimates are count ratios.
5. **Period.** Pollution mix, age structure, warning systems, and care-seeking differ across decades, including COVID-era months.

**Appropriate use of Goggins et al.:** local historical direction (cold-emphasised cardiac risk; later concern about nighttime heat is a separate literature). Not a numeric “has heat replaced cold?” test.

## Goggins and Chan 2017 (HF) — closer historical motivation for the HF arm

Goggins WB, Chan EYY. *Int J Cardiol*. 2017;228:537–542. doi:10.1016/j.ijcard.2016.11.106. Daily public-hospital HF admissions and HF deaths, Hong Kong, 2002–2011. Cumulative RR for admissions comparing 11 °C with 25 °C over lags to 23 days: **2.63 (2.43–2.84)**. Stronger in older groups and for new than recurrent hospitalisations. This is the outcome-aligned local daily HF study. It is still not the live-manuscript estimand: daily diagnosis-specific admissions ≠ monthly first hospitalisation after first HF diagnosis without recorded admission cause. Do not compare 2.63 with the monthly count ratio 1.073 per five official cold days.
