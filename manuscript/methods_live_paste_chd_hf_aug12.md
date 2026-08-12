# Methods remainder for live manuscript — CHD/HF (12 August 2026)

**Use:** Paste into Hogan’s live shared manuscript. Conform headings to the live file.  
**Do not paste:** results, Gate language, pathway IDs, or journal ambitions.  
**Do not overwrite:** Hogan’s Weather Methods.  
**Outcome detail:** Roro owns health-data construction; this file keeps only a bridge.

This supersedes the stroke-framed 5 August draft for live-file use.

## Study design

We conduct an ecological monthly time-series study of Hong Kong from January 2013 through December 2023 (132 territory-month observations). The target estimand is the count ratio for monthly first-hospitalisation events associated with a specified monthly thermal-exposure contrast, conditional on seasonality, long-term trend and the stated adjustment set. The monthly estimand does not identify individual causal effects, admission cause beyond the governed construction, or daily triggering.

Governed outcomes currently available for analysis are monthly counts of first hospitalisation after first coronary heart disease (CHD) diagnosis and first hospitalisation after first heart-failure (HF) diagnosis among people diagnosed with type 2 diabetes and/or hypertension during the study window. Stroke-specific aggregates remain pending; stroke Methods wording will be added when that series is delivered. Exposure definitions and outcome-construction procedures are specified before substantive association estimates are interpreted. Operational construction of weather variables is described in the Weather section.

## Pollution

Monthly nitrogen dioxide, ozone and fine particulate matter (PM2.5) are obtained from the Hong Kong Environmental Protection Department EPIC portal. The main analysis uses general monitoring stations. Roadside stations represent a distinct near-road environment and are reserved for sensitivity analysis.

Completeness is assessed for each pollutant–station–month against the expected number of observations. A station-month contributes only when at least 75% of expected observations are available. Values below this threshold are treated as missing before aggregation; missing measurements are not coded as zero. Territory-wide monthly concentrations are calculated as unweighted means across eligible general stations.

Pollution adjustment, when used, is introduced in stages. Nitrogen dioxide and particulate matter enter before ozone. Ozone enters last because its seasonal and meteorological coupling with hot, sunny conditions can make simultaneous estimates difficult to interpret. Single- and multi-pollutant models are treated as distinct adjustment sets rather than screened for favourable attenuation.

## Population denominators and offsets

Individual-level person-time for the T2D/HTN cohort is not available in the released aggregates. Models therefore do not claim cohort incidence rates. The primary analysis uses a days-in-month offset to account for unequal month length. Broader Census and Statistics Department population series, where used, are ecological context only and are not treated as the cohort at risk. Any age or sex stratification will be applied only when governed outcome aggregates and denominators are compatible.

## Statistical analysis

Monthly event counts are analysed with negative-binomial regression when the variance exceeds the Poisson mean. Quasi-Poisson regression provides an alternative mean–variance specification. Models include calendar-month indicators for seasonality and a smooth function of calendar time for long-term trend.

Thermal exposures and contrasts follow the Weather section. Continuous temperature measures and official extreme-day counts are treated as different exposure questions rather than interchangeable encodings. Same-month and lagged terms are labelled separately. Nested thresholds are fitted in separate models unless a contrast has been specified in advance.

Pollutants may be added through the staged adjustment sequence above. Period-restricted or period-indicator models assess sensitivity to COVID-19-related changes in health-care use. Additional adjustment and subgroup analyses are conducted only when their data sources and aggregate structure support them.

Effect estimates are reported as count ratios with confidence intervals. Exposure prevalence, missingness and model diagnostics accompany the estimates. Diagnostics assess overdispersion, residual autocorrelation, influential months and collinearity. The complete model panel remains visible in reporting. Heat–cold comparisons rely on planned contrasts and consistency across definitions, not on counts of nominally significant results.

## Definition of hot and cold months

Hot- and cold-month indicators are organised as parallel definition families. The operational daily thresholds, percentile-based events, spell rules, combined day–night events and their monthly mapping are defined in the Weather section. This section does not modify those rules.

Before outcome associations are interpreted, each monthly definition specifies its source or rationale, reference period, percentile algorithm where relevant, treatment of ties, seasonal denominator, missing-day tolerance, cross-month assignment and event-overlap rule. Exposure-only summaries report how often each definition occurs and which months it selects.

No definition is promoted because it produces the largest association. Confirmatory contrasts and sensitivity analyses are labelled in advance, and the complete definition panel remains visible in reporting. Final selection of any headline hot and cold specifications is made by the study team after outcome-data quality control and descriptive review.

## Outcome

The outcomes comprise governed monthly aggregates of first hospitalisation after first CHD diagnosis and first hospitalisation after first HF diagnosis in the T2D/HTN cohort, as constructed and released by the outcome co-investigator. Admission cause beyond that construction is not available. The health-data Methods will specify the governed source, case identification, temporal aggregation and release procedures. No source fields, event counts, subtype availability or stratum structure are assumed here beyond what the outcome co-investigator documents. Stroke remains outside the present Methods text until a governed stroke series is delivered.
