# Initial exploration note

**Date:** 2026-07-10  
**Purpose:** Time-boxed Phase-1 assessment of public data access, literature baseline, and analytical refinements before the first-stage exploratory report.

## 1. Source-access findings

### Weather — accessible and built

HKO daily climate extracts (`dailyExtract_YYYY.xml`, JSON content) for 2012–2024 were downloaded successfully from:

`https://www.hko.gov.hk/cis/dailyExtract/dailyExtract_{year}.xml`

Fields include mean pressure, Tmax/Tmean/Tmin, dew point, relative humidity, cloud, rainfall, sunshine, and wind. Official thresholds applied:

| Metric | Definition |
|---|---|
| Hot night | Tmin ≥ 28°C |
| Very hot day | Tmax ≥ 33°C |
| Extremely hot day | Tmax ≥ 35°C |
| Cold day | Tmin ≤ 12°C |

Open-data API companions (`CLMTEMP`, `CLMMAXT`, `CLMMINT`) also downloaded for audit. RH/rainfall are **not** exposed via those open-data `dataType` codes; dailyExtract is the practical source.

**Primary station:** HKO Headquarters (matches official annual extreme series).

**Processed output:** `data_processed/climate_monthly_2013_2023.csv` (132 months).

### Pollution — portal confirmed; bulk API not automated

EPD EPIC portal supports historical downloads but is interactive (chunked date ranges). No automated bulk endpoint was used in this pass. Pipeline includes:

- manual download instructions in `data_raw/epd/README_manual_download.md`
- PLACEHOLDER monthly series labeled `PLACEHOLDER_NOT_FOR_INFERENCE` for code testing only

Hogan should replace placeholders with general-station EPIC extracts (≥75% completeness rule; roadside separate).

### Population — API requires interactive `param`

C&SD Table 110-01002 is the preferred source, but the GET API requires an encrypted `param` generated from the web table UI. Pipeline includes import path for a user-supplied CSV and a clearly labeled `SYNTHETIC_DENOMINATOR` scaffold for workflow testing.

Bob should download mid-year age-sex counts (2012–2024) and drop CSV into `data_raw/csd_population/`.

### HA outcomes — blocked

No Hospital Authority extract is present. All outcome modeling uses SYNTHETIC data only.

## 2. Preliminary thermal-extreme pattern (real HKO data)

Derived annual counts at HKO Headquarters (matches published yearly summaries for hot nights / VHD / cold days):

| Year | Hot nights | Very hot days | Extremely hot days | Cold days |
|---:|---:|---:|---:|---:|
| 2013 | 10 | 17 | 0 | 14 |
| 2014 | 34 | 33 | 0 | 21 |
| 2015 | 37 | 28 | 1 | 7 |
| 2016 | 36 | 38 | 6 | 21 |
| 2017 | 41 | 29 | 1 | 9 |
| 2018 | 26 | 36 | 5 | 21 |
| 2019 | 46 | 33 | 2 | 1 |
| 2020 | 50 | 47 | 3 | 11 |
| 2021 | 61 | 54 | 4 | 13 |
| 2022 | 52 | 52 | 15 | 13 |
| 2023 | 56 | 54 | 4 | 14 |

Descriptive averages:

- **2013–2018:** ~30.7 hot nights, ~30.2 very hot days, ~15.5 cold days/year
- **2019–2023:** ~53.0 hot nights, ~48.0 very hot days, ~10.4 cold days/year

This supports including hot nights as the primary heat metric. Cold-day counts remain variable (not monotonically declining). These are descriptive only — not formal trend tests.

### 2024 extension

Daily extract for 2024 was downloaded. HKO reported 2024 as Hong Kong’s warmest year on record. Recommend requesting 2024 HA data as optional extension without delaying 2013–2023 analysis.

## 3. Literature baseline (summary)

See `memos/literature_baseline.md` for citations. Key points:

- Earlier Goggins AMI work (2000–2009): cold-dominant; little heat effect; NO2 important.
- Subtropical winter-excess CVD morbidity/mortality is well documented in Hong Kong.
- Monthly studies can detect broad seasonal patterns but blunt short-lag heat effects.
- Hot-night / consecutive-extreme metrics are policy- and biology-relevant.
- O3 should be staged cautiously (possible pathway variable).

**Outstanding:** verify exact earlier Goggins stroke admissions citation before manuscript use.

## 4. Analytical refinements adopted in pipeline

1. Primary heat model: **hot nights + cold days** (not all heat metrics together).
2. Alternative heat model: very hot days + cold days.
3. Spell metrics: within-month runs + full spells touching month.
4. Completeness: extremes set to NA if <90% daily completeness.
5. Offset: `log(population × days_in_month)`.
6. COVID phases as in `config.yml`.
7. Two-way clustered SE scaffold for shared monthly exposure.
8. Synthetic outcomes always labeled `data_status = "SYNTHETIC"`.

## 5. Immediate next steps for human team

1. Send `memos/data_request_roro.md` to Roro.
2. Send `memos/environmental_data_request_hogan.md` to Hogan.
3. Bob: download C&SD age-sex population CSV into `data_raw/csd_population/`.
4. Hogan: deposit EPD general-station files into `data_raw/epd/`.
5. Confirm assumption ledger checklist items.
6. Proceed to first-stage exploratory report (now that public weather pipeline is executable).
