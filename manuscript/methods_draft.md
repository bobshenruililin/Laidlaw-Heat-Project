# Methods (draft)

**Working title:** Thermal extremes, aging, pollution, and cardiovascular hospital burden in Hong Kong, 2013–2023

*This draft is intended for later adaptation into a manuscript. Associations are ecological and should not be interpreted as individual-level causal effects.*

## Study design and setting

We will conduct a retrospective ecological time-series study of monthly cardiovascular hospital admissions among Hong Kong residents aged 35 years or older from January 2013 through December 2023. An optional 2024 extension may be added if Hospital Authority and environmental data are available without delaying the core analysis. The unit of analysis will be the month × age group × sex × diagnosis stratum. The study setting is Hong Kong, a dense subtropical city experiencing warming, more frequent hot nights and very hot days, population aging, and changing air-pollution profiles.

## Data sources

### Outcomes

Aggregate monthly counts will be requested from the Hospital Authority (HA). The primary outcome will be monthly emergency or unplanned inpatient admissions with acute myocardial infarction (AMI), ischemic stroke, or hemorrhagic stroke recorded as the principal diagnosis. Secondary outcomes, if available, will include ED attendances, ED-only events, unique patients, in-hospital deaths, and bed-days. All-cause emergency admissions and ED attendances by age and sex will be requested to characterize COVID-era utilization disruption.

Diagnosis algorithms will be finalized after confirmation of the HA coding system (ICD-9-CM, ICD-10, or mixed). Provisional ICD-9-CM definitions are AMI `410.x`; hemorrhagic stroke `430`, `431`, and provisionally `432.x`; ischemic stroke `433.x1`, `434.x1`, and `436`; with exclusion of TIA `435.x`, stroke sequelae `438.x`, and old MI `412`. ICD-10 backups are AMI `I21–I22`, hemorrhagic stroke `I60–I62`, and ischemic stroke `I63`, with `I64` reserved for sensitivity analyses. Transfers will be combined into one episode where feasible; true readmissions will remain separate events. ED and inpatient series will be analyzed separately unless mutually exclusive ED-only records are available.

### Weather exposures

Daily meteorological observations from the Hong Kong Observatory (HKO) will be aggregated to calendar months. The primary reference series will be the Hong Kong Observatory Headquarters station, with multi-station sensitivity analyses if available. Official HKO definitions will be used:

- hot night: daily minimum temperature ≥ 28°C;
- very hot day: daily maximum temperature ≥ 33°C;
- extremely hot day: daily maximum temperature ≥ 35°C;
- cold day: daily minimum temperature ≤ 12°C.

The primary heat exposure will be the monthly number of hot nights. Cold days will be treated as a co-primary thermal exposure. Alternative models will examine very hot days, extremely hot days, monthly mean / minimum / maximum temperature, and spell-duration metrics (longest consecutive hot-night run; longest consecutive very-hot-day run; days belonging to multi-day spells). Months with insufficient daily completeness (proposed threshold: <90% of days observed) will be flagged and extreme counts set to missing rather than treating unobserved days as non-extreme.

### Air pollution

Monthly concentrations of NO2, O3, PM2.5, and PM10 will be constructed from Environmental Protection Department (EPD) monitoring data. General stations will define the primary territory-wide exposure; roadside stations will be reserved for sensitivity analyses. A station-month will be considered valid when at least 75% of expected observations are present. The primary monthly exposure will be the unweighted mean across valid general stations, with a balanced-panel sensitivity using stations operating throughout the study period. For ozone, both the monthly mean and a peak-oriented metric (e.g., monthly mean of daily maximum 8-hour O3) will be sought when available.

### Population denominators

Age-sex-specific population estimates will be obtained from the Census and Statistics Department. Preferred age groups are 35–39 through 80–84 in five-year bands, plus 85+. Monthly denominators will be estimated by linear interpolation between mid-year estimates. The model offset will be `log(population × days_in_month)`. Calendar-year assignment of mid-year population will be examined as a sensitivity analysis. The population universe will be aligned, as far as possible, with HA residency/eligibility definitions.

### Other covariates

Models will include calendar-month fixed effects, a smooth long-term time trend, and COVID-period indicators. Proposed COVID phases are: pre-COVID (Jan 2013–Jan 2020); early COVID (Feb 2020–Dec 2021); fifth wave (Jan–Apr 2022); late 2022 (May–Dec 2022); and post-reopening (2023). Public-holiday counts and a Chinese New Year indicator will be constructed. Influenza activity from Centre for Health Protection surveillance may be included in sensitivity models. Typhoon-signal days may be examined exploratorily.

## Statistical analysis

### Descriptive analysis

We will describe trends in thermal extremes, pollution, and age-sex population structure; assess missingness and completeness; and, once HA data are available, summarize admission rates by age, sex, diagnosis, and COVID period.

### Main model

Because monthly admission counts may be overdispersed, Negative Binomial regression will be the default. The basic mean model is:

```text
log(μ_{a,s,d,t}) = α
  + β1 · (hot_nights_t / 5)
  + β2 · (cold_days_t / 5)
  + age_group_a + sex_s + diagnosis_group_d
  + month fixed effects
  + spline(time_index)
  + COVID phase indicators
  + offset[log(population_{a,s,t} × days_in_month_t)]
```

Very hot days will replace, rather than routinely accompany, hot nights in alternative heat models, to limit collinearity. Rate ratios will be reported per 5 additional hot nights, per 5 additional very hot days, per 5 additional cold days, and per 1°C higher mean or mean-minimum temperature.

Because weather is shared across strata within a month, variance estimation will account for common monthly shocks and within-stratum serial correlation (e.g., two-way clustered covariance by month and outcome stratum). GEE or other correlated-count models will be considered as sensitivity analyses.

### Effect modification

Interactions will be tested separately rather than simultaneously, prioritizing:

- hot nights × age group;
- cold days × age group;
- hot nights × diagnosis group;
- cold days × diagnosis group;
- O3 × hot nights.

### Pollution staging

Pollution will be introduced in stages:

1. no pollutant adjustment (total thermal association);
2. NO2 only;
3. PM2.5 only;
4. O3 only;
5. O3 × hot nights interaction;
6. multi-pollutant sensitivity model.

Ozone and influenza will be interpreted cautiously because they may lie partly on heat- or cold-related pathways.

### Sensitivity analyses

Planned sensitivities include Poisson vs Negative Binomial vs quasi-Poisson; exclusion of 2020–2022; pre-COVID-only analysis; lag-1 month exposure; alternative heat and cold metrics; month fixed effects vs harmonic seasonality; with/without pollutants; age-grouping alternatives; diagnosis-specific models; ED-only vs inpatient-only series; and optional 2024 extension.

### Missing data and suppression

Suppressed HA cells will not be treated as zero. Incomplete environmental months will be flagged using prespecified completeness rules and investigated before exclusion or imputation. All synthetic development datasets will be labeled `SYNTHETIC` and will not be reported as substantive findings.

## Software and reproducibility

Analyses will be conducted in R using a scripted pipeline (`scripts/00_setup.R` through `scripts/13_make_report_outputs.R`), with preserved raw data, processed analysis files, session information, and an assumption ledger.
