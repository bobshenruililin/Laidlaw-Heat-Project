# Methods (revised draft)

**Working title:** Thermal extremes and cardiovascular hospital burden in an aging Hong Kong, 2013–2023  

*Publication-style draft for internal review. Unresolved items are tagged `[TO CONFIRM: ...]`. Ecological associations only.*

---

## Study design and setting

We will conduct a retrospective ecological time-series study of monthly cardiovascular hospital admissions among Hong Kong residents aged 35 years or older. The planned core study window is January 2013 through December 2023. `[TO CONFIRM: whether 2024 is included as an optional extension without delaying the core analysis]` The unit of analysis will be the month × age group × sex × diagnosis stratum. Associations will be interpreted at the population level and will not be presented as individual-level causal effects.

Hong Kong is a dense subtropical city with operational heat and cold warnings issued by the Hong Kong Observatory (HKO). The study is motivated by contemporary warming, population aging, changing air-pollution profiles, and COVID-period disruption of hospital utilization, and by earlier local evidence of cold-related cardiovascular burden.

## Outcomes

Aggregate monthly counts will be obtained from the Hospital Authority (HA). `[TO CONFIRM: secure access route, output-vetting rules, and whether aggregates may leave the secure environment]`

**Recommended primary outcome:** monthly emergency or unplanned inpatient admissions with acute myocardial infarction (AMI), ischemic stroke, or hemorrhagic stroke recorded as the principal diagnosis. `[TO CONFIRM: principal diagnosis availability]` `[TO CONFIRM: emergency/unplanned admission-type field]`

**Secondary outcomes (if available):** ED attendances; ED-only events not followed by admission; unique patients; in-hospital deaths; bed-days; and all-cause emergency admissions/ED attendances by age and sex for COVID-context description.

**Episode definition:** `[TO CONFIRM: episode definition]` Recommended default: combine inter-hospital or specialty transfers into one episode where feasible; retain true readmissions as separate events; assign events to the month of admission or ED presentation rather than discharge.

**ED versus inpatient:** ED and inpatient series will be analyzed separately unless mutually exclusive ED-only records are available. `[TO CONFIRM: ED/inpatient double-counting rules]`

### Diagnosis coding

`[TO CONFIRM: HA coding system]` Coding may be ICD-9-CM, ICD-10, or mixed across 2013–2023. Provisional working definitions:

**If ICD-9-CM**

- AMI: `410.x` (exclude old MI `412`)
- Hemorrhagic stroke: `430`, `431`, provisionally `432.x` (sensitivity: `430–431` only)
- Ischemic stroke: `433.x1`, `434.x1`, `436` (sensitivity: with/without `436`)
- Exclude TIA `435.x` and stroke sequelae `438.x`

**If ICD-10**

- AMI: `I21–I22`
- Hemorrhagic stroke: `I60–I62`
- Ischemic stroke: `I63`
- Unspecified stroke `I64` only in sensitivity
- Exclude TIA `G45`

Small-cell suppression will not be coded as zero. `[TO CONFIRM: suppression threshold and complementary suppression]`

## Age groups and population denominators

Preferred age groups:

```text
35–39, 40–44, 45–49, 50–54, 55–59, 60–64,
65–69, 70–74, 75–79, 80–84, 85+
```

`[TO CONFIRM: age-group availability, especially separation of 65–69 and 70–74]`

Age-sex-specific population estimates will be obtained from the Census and Statistics Department. `[TO CONFIRM: population universe alignment with HA residency/eligibility; whether foreign domestic helpers should be excluded in sensitivity]` Monthly denominators will be estimated by linear interpolation between mid-year estimates. The preferred model offset is:

```text
log(age-sex-specific population × days in month)
```

## Environmental exposures

### Weather

Daily HKO observations will be aggregated to calendar months. `[TO CONFIRM: HKO station]` Recommended default: Hong Kong Observatory Headquarters as primary series, with multi-station sensitivity if feasible.

Official definitions:

- hot night: daily minimum temperature ≥ 28°C;
- very hot day: daily maximum temperature ≥ 33°C;
- extremely hot day: daily maximum temperature ≥ 35°C;
- cold day: daily minimum temperature ≤ 12°C.

**Primary heat exposure:** monthly number of hot nights.  
**Co-primary cold exposure:** monthly number of cold days.  
**Alternative exposures:** very hot days; extremely hot days; mean temperature; mean daily minimum temperature; spell-length metrics.

Highly collinear heat metrics will not enter the same default model. Months with insufficient daily completeness (proposed <90%) will be flagged and extreme counts set to missing rather than treating unobserved days as non-extreme.

### Air pollution

Monthly NO₂, O₃, PM2.5, and PM10 will be constructed from Environmental Protection Department monitoring data. `[TO CONFIRM: pollution station set]` Recommended default: general stations for primary exposure; roadside stations for sensitivity only. Station-months with <75% expected observations will be treated as invalid. Ozone will be staged carefully because it may correlate with, modify, or partly mediate hot sunny conditions. `[TO CONFIRM: availability of peak-oriented O₃ metric such as MDA8]`

## Covariates

Models will include calendar-month fixed effects, a smooth long-term time trend, and COVID-period indicators. `[TO CONFIRM: COVID phases]` Working phases:

- pre-COVID: Jan 2013–Jan 2020  
- early COVID: Feb 2020–Dec 2021  
- fifth wave: Jan–Apr 2022  
- late 2022: May–Dec 2022  
- post-reopening: 2023  

Influenza activity from Centre for Health Protection surveillance is proposed for sensitivity analyses initially. `[TO CONFIRM: influenza in primary vs sensitivity model]` Public-holiday counts and a Chinese New Year indicator will be included after an official calendar is finalized. Typhoon-signal days may be examined exploratorily.

## Statistical analysis

### Descriptive analysis

We will describe trends in thermal extremes, pollution, and age-sex population structure; assess missingness; and, once HA data are available, summarize admission rates by age, sex, diagnosis, and COVID period.

### Main model

Negative Binomial regression will be the default because monthly admission counts may be overdispersed. Poisson and quasi-Poisson specifications will be compared. The basic mean model is:

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

Rate ratios will be reported per 5 additional hot nights, per 5 additional very hot days, per 5 additional cold days, and per 1°C higher mean or mean-minimum temperature.

Although the analysis panel may contain thousands of age-sex-diagnosis rows, territory-wide weather exposures vary over only 132 months in the core window. Variance estimation will therefore account for shared monthly exposure and within-stratum correlation (e.g., clustered covariance; GEE or related models as sensitivity analyses).

### Effect modification

Interactions will be fitted separately rather than simultaneously, prioritizing hot nights × age, cold days × age, hot/cold × diagnosis, and O₃ × hot nights.

### Pollution staging

1. No pollutant adjustment (total thermal association)  
2. NO₂ only  
3. PM2.5 only  
4. O₃ only  
5. O₃ × hot nights  
6. Multi-pollutant sensitivity only  

### COVID sensitivities

At minimum: full-period model with COVID adjustment; pre-COVID analysis; exclusion of 2020–2022; focused attention to the 2022 fifth wave.

### Historical comparison

Comparisons with earlier Goggins-era daily studies will initially be qualitative because periods, temporal resolution, lag structures, and estimands differ. Direct coefficient comparison will be avoided unless methods are harmonized.

### Missing data and disclosure

Suppressed HA cells will not be treated as zero. Incomplete environmental months will be flagged using prespecified completeness rules. All development datasets used before HA access are labeled synthetic or placeholder and are not substantive findings.

## Software and reproducibility

Analyses will be conducted in R using a scripted pipeline (`scripts/00_setup.R` through `scripts/13_make_report_outputs.R`), with preserved raw public files, processed analysis files, session information, and an assumption ledger. Real HA modeling will use parallel scripts that accept an approved aggregate extract inside the permitted environment.
