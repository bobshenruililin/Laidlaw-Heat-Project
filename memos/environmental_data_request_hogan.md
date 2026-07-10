# Environmental data request — Hogan

**To:** Hogan  
**From:** Project analysis team (Bob / supporting AI pipeline)  
**Subject:** Climate and pollution variables for Hong Kong cardiovascular admissions project  
**Date:** 2026-07-10  

Dear Hogan,

For the 2013–2023 Hong Kong thermal-extremes and cardiovascular admissions project, please prepare daily source files and monthly analysis files for weather and air pollution. A separate **2024 extension** would be useful if readily available, but it should **not delay** the core period.

## Weather

Please use official HKO data where possible. Proposed primary reference: **Hong Kong Observatory Headquarters (HKO)**, with a multi-station sensitivity dataset if feasible.

### Official HKO thresholds (required)

| Metric | Definition |
|---|---|
| Hot night | Daily minimum temperature ≥ **28°C** |
| Very hot day | Daily maximum temperature ≥ **33°C** |
| Extremely hot day | Daily maximum temperature ≥ **35°C** |
| Cold day | Daily minimum temperature ≤ **12°C** |

### Required daily variables

- date
- station
- daily mean temperature
- daily minimum temperature
- daily maximum temperature
- daily mean relative humidity
- daily rainfall
- mean dew point (if available)
- data-completeness or quality flags

### Required monthly variables

```text
month_id
mean_temp
mean_tmin
mean_tmax
relative_humidity
rainfall
hot_nights
very_hot_days
extremely_hot_days
cold_days
longest_hot_night_run
longest_very_hot_run
```

### Additional spell / wet-heat metrics (if possible)

- Number of days belonging to hot-night spells of ≥3 consecutive nights
- Number of days belonging to very-hot-day spells of ≥2 consecutive days
- Maximum **full** spell length touching each month (including spells crossing month boundaries)
- Wet-bulb temperature, or components needed to derive it
- Heat index only if temperature and humidity are temporally aligned
- Typhoon signal days

Please **flag months with incomplete daily observations** rather than treating missing days as non-extreme days. Suggested rule: investigate / set extremes to NA when observed days / days-in-month < 0.90.

### Current pipeline note

The repository already downloads HKO `dailyExtract_YYYY.xml` files (JSON content) for 2012–2024 and builds monthly extremes from them. Please review station choice, completeness handling, and spell-boundary logic before finalizing the exposure file.

## Pollution

### Requested pollutants

- NO2
- O3
- PM2.5
- PM10
- SO2 (optional)

Use **general monitoring stations** for the primary exposure; keep **roadside stations separate**.

### Preferred construction

1. Station-month valid when ≥75% of expected observations are available
2. Monthly territory-wide mean across valid general stations
3. Balanced-station-panel sensitivity (stations operating throughout 2013–2023)
4. Roadside-station sensitivity analysis
5. Retain station-level monthly file for audit

### O3 metrics

Please provide:

1. Ordinary monthly mean O3
2. If possible, monthly mean of daily maximum 8-hour O3 (MDA8) or another EPD peak-oriented metric

Ozone may be correlated with, interact with, or partly mediate hot sunny conditions; we will stage O3 adjustment rather than dump it into the primary thermal model.

## Documentation requested

- Station names and types (general vs roadside)
- Opening and closing dates
- Units and averaging conventions
- Missing-value codes
- Data-revision / validation status
- Source files and download dates
- Known instrument or method changes

## Proposed processed outputs

```text
data_processed/climate_monthly_2013_2023.csv
data_processed/pollution_monthly_2013_2023.csv
```

plus station-level supporting files and a variable dictionary.

Thank you.

Best regards,  
Bob / analysis team
