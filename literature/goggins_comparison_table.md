# Comparison: Goggins-era daily studies vs proposed monthly study

| Dimension | Goggins AMI (2013) | Goggins stroke (2012) | Proposed current study |
|---|---|---|---|
| Study period | 2000–2009 | 1999–2006 | 2013–2023 (core) |
| City/population | Hong Kong (+ Taiwan cities for AMI) | Hong Kong public hospitals, age 35+ | Hong Kong residents age 35+ |
| Outcome | AMI admissions | Hemorrhagic and ischemic stroke separately | AMI; ischemic stroke; hemorrhagic stroke |
| Coding system | ICD-based AMI | ICD stroke subtypes | [TO CONFIRM: ICD-9-CM / ICD-10 / mixed] |
| Temporal resolution | **Daily** | **Daily** | **Monthly** |
| Temperature metric | Mean temperature (smooth/threshold) | Mean temperature | Official extreme-day counts (hot nights, cold days) + alternatives |
| Threshold | ~24°C for cold effect (HK AMI) | IS below ~22°C; HS linear across range | Hot night Tmin≥28°C; cold day Tmin≤12°C |
| Lag structure | Multi-day averages (e.g. 0–13) | HS lags 0–4; IS lags 0–13 | Same-month (lag-1 sensitivity) |
| Pollutants | NO2 important for AMI | Pollutants NS for stroke | Staged NO2/O3/PM; O3 cautious |
| Seasonality / trend | Controlled in GAM | Controlled in GAM | Month FE + smooth time trend |
| Age groups | Reported in related work | Stronger HS effects in older adults | Prefer 5-year bands; separate 65–69 & 70–74 |
| Effect measure | % change per 1°C | % change per 1°C | RR per 5 extreme days/nights |
| Primary finding | Cold-dominant AMI; little heat | Cold-related HS and threshold IS | Not yet estimated (HA pending) |
| Comparability limitation | Daily DL/GAM estimands ≠ monthly extreme-count RRs; different decades and exposure definitions | Same | Do **not** compare coefficients directly |

## Why coefficients are not directly comparable

1. **Temporal aggregation:** Daily distributed-lag effects capture acute triggering; monthly counts capture broader burden and may attenuate short-lag heat.
2. **Exposure scaling:** Per 1°C mean temperature ≠ per 5 hot nights or cold days.
3. **Period and context:** Pollution mix, population age structure, warning systems, and care-seeking differ across decades.
4. **Outcome packaging:** Diagnosis algorithms, emergency vs elective mix, and COVID disruption differ.

**Appropriate use of historical findings:** qualitative direction and scientific motivation; not numeric “shift” tests unless methods are harmonized.
