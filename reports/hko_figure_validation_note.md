# HKO annual extremes figure — validation note

**Date:** 10 July 2026  
**Station:** Hong Kong Observatory Headquarters (`HKO`)  
**Source file:** `data_processed/climate_monthly_2013_2023.csv`  
**Figure:** `figures/hko_annual_extremes_2013_2023.pdf` / `.png`

## Quality checks

| Check | Result |
|---|---|
| Unique months 2013-01–2023-12 | 132 |
| Months per year | 12 for each year |
| Duplicate month records | 0 |
| Missing extreme counts | 0 |
| Counts within 0–days_in_month | Pass |
| Station field | `HKO` |
| Thresholds | Hot night Tmin≥28; VHD Tmax≥33; cold Tmin≤12 |

## Official comparison

Pipeline annual totals were compared with HKO *The Year's Weather* pages for 2013–2023.

**Result: 33/33 MATCH** (hot nights, very hot days, and cold days × 11 years).

No mismatches were found. Pipeline values were **not** altered to force agreement.

| Year | Hot nights | Very hot days | Cold days |
|---:|---:|---:|---:|
| 2013 | 10 | 17 | 14 |
| 2014 | 34 | 33 | 21 |
| 2015 | 37 | 28 | 7 |
| 2016 | 36 | 38 | 21 |
| 2017 | 41 | 29 | 9 |
| 2018 | 26 | 36 | 21 |
| 2019 | 46 | 33 | 1 |
| 2020 | 50 | 47 | 11 |
| 2021 | 61 | 54 | 13 |
| 2022 | 52 | 52 | 13 |
| 2023 | 56 | 54 | 14 |

Full row-level validation: `outputs/tables/hko_annual_extremes_validation.csv`.

## Caption requirement

The figure caption states that these are **environmental exposure descriptors and not health-outcome results**.

## Script

`scripts/14_hko_annual_extremes_figure.R`
