# Temperature / exposure panel for Roro

Prepared 7 August 2026; dictionary expanded 12 August 2026.

**Provenance:** `REAL` public Hong Kong Observatory / EPD / CHP-derived project layers.  
**Not included:** Hospital Authority health outcomes, coefficients, or any merged HA columns.

**Join key:** `month_id` (`YYYY-MM`), January 2013–December 2023 (**132** months).

| File | Role |
|---|---|
| `temperature_monthly_panel_2013_2023.csv` | Canonical HKO Headquarters monthly means and official extreme-day counts |
| `analysis_exposures_monthly_2013_2023.csv` | Analysis-ready companion: lags, pollution, flu, COVID phase |

The sendable human file is `HKO_temperature_panel_2013_2023.pdf` (rebuild from `reports/latex/hko_temperature_panel_note.tex`). Do not email this README or `NOTE.md`.

---

## 1. `temperature_monthly_panel_2013_2023.csv`

| Column | Definition |
|---|---|
| `month_id` | Calendar month `YYYY-MM` |
| `year`, `month` | Integer year and month |
| `mean_temp` | Monthly mean of daily mean temperature (°C), HKO Headquarters |
| `mean_tmin` | Monthly mean of daily minimum temperature (°C) |
| `mean_tmax` | Monthly mean of daily maximum temperature (°C) |
| `hot_nights` | Count of days with daily `Tmin ≥ 28°C` (HKO hot night) |
| `cold_days` | Count of days with daily `Tmin ≤ 12°C` (HKO cold day) |
| `very_hot_days` | Count of days with daily `Tmax ≥ 33°C` (HKO very hot day) |
| `extremely_hot_days` | Count of days with daily `Tmax ≥ 35°C` (HKO extremely hot day) |
| `days_in_2d3n_window` | Count of calendar days belonging to a Wang/Ren-style 2D3N window: two consecutive very hot days with the three corresponding hot nights (`VHD[i:i+1]` and `HN[i:i+2]`); overlapping starts mark their days |
| `station` | Always `HKO` (Headquarters) in this share |

Absolute daily thresholds follow HKO climatological conventions. Monthly counts are project exposures, not new HKO definitions. Cross-month spell assignment for manuscript weather Methods remains Hogan-owned where contested.

---

## 2. `analysis_exposures_monthly_2013_2023.csv`

| Column | Definition |
|---|---|
| `month_id` | Same join key as the temperature panel |
| `mean_temp`, `mean_tmax`, `mean_tmin` | Same HKO monthly means as above |
| `lag1_mean_temp`, `lag1_mean_tmax`, `lag1_mean_tmin` | Previous calendar month’s means. January 2013 uses December 2012 HKO values (not missing) |
| `hot_nights`, `cold_days`, `very_hot_days` | Same HKO monthly counts as above (`extremely_hot_days` and `days_in_2d3n_window` are only in the temperature panel) |
| `NO2`, `O3`, `PM25` | Territory monthly means from EPD general stations (°C not applicable; µg/m³-class concentrations as processed in the project pollution layer). Completeness and aggregation rules follow the project pollution Methods |
| `flu_indicator` | CHP Flu Express–derived monthly influenza positivity indicator. **121/132** months non-missing; early-2013 gap is left missing (never zero-filled) |
| `covid_phase` | Project period label (see below) |

### COVID phase labels (`config.yml`)

| Label | Inclusive months |
|---|---|
| `pre_covid` | 2013-01 – 2020-01 |
| `early_covid` | 2020-02 – 2021-12 |
| `fifth_wave` | 2022-01 – 2022-04 |
| `late_2022` | 2022-05 – 2022-12 |
| `post_reopening` | 2023-01 – 2023-12 |

These cut-points are project conventions for sensitivity adjustment, not clinical case definitions.

---

## 3. Safe-use rules

1. Prefer `temperature_monthly_panel_2013_2023.csv` when only temperature / extreme-day counts are needed.
2. Use `analysis_exposures_monthly_2013_2023.csv` when merging to the analysis key with lags, pollution, flu, or COVID phase.
3. Do not treat pollution, flu, or COVID columns as temperature data.
4. Do not append HA outcome counts to this share folder or redistributed copies.
5. If a column’s manuscript wording differs from Hogan’s live Weather Methods, Hogan’s live section governs operational weather prose.

## 4. Generation note

Built from the project’s public climate / confounder pipeline for the 2013–2023 monthly panel. Scripts live under `scripts/` in the repository; this folder is the human-facing share pack only.
