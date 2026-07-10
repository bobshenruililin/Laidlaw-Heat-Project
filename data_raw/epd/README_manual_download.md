# EPD pollution raw data — manual download instructions

Primary portal: https://cd.epic.epd.gov.hk/EPICDI/air/

## Recommended download steps

1. Open EPIC Air Quality Data Download / Display.
2. Select pollutants: NO2, O3, RSP/PM10, FSP/PM2.5 (SO2 optional).
3. Select **general** stations for the primary extract; download roadside separately.
4. Prefer daily or hourly validated data; monthly aggregates are acceptable if completeness metadata are available.
5. Because monthly requests are limited (e.g. 120 months), download in chunks covering 2013–2023 (and optional 2024).
6. Save files into this folder as CSV, e.g.:
   - `epd_general_daily_2013_2017.csv`
   - `epd_general_daily_2018_2022.csv`
   - `epd_general_daily_2023_2024.csv`
   - `epd_roadside_daily_*.csv`
7. Keep a station metadata file if possible (`stations_metadata.csv`).

## Completeness rule

Station-month valid if ≥75% of expected observations are present.

## Units

Document units as provided by EPD (typically µg/m³ for these pollutants in recent reports).

Do not overwrite raw files after download; append new versions with dates if revised.
