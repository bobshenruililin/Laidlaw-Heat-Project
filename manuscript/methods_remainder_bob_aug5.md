# Methods remainder for Bob — 5 August draft

**Scope:** Paste these sections into the live manuscript and conform the headings to its structure. They deliberately exclude weather-data processing and operational heatwave rules, which remain in Hogan’s weather Methods. The Outcome paragraph is only a bridge to Roro’s health-data Methods.

## Study design

We will conduct an ecological monthly time-series study of Hong Kong from January 2013 through December 2023. The primary series will contain 132 territory-month observations. Where the governed outcome aggregates support compatible age and sex strata, stratified panels will be analysed using the corresponding population denominators. The target estimand is the rate ratio for monthly stroke-event counts associated with a specified monthly thermal-exposure contrast, conditional on seasonality, long-term trend and the stated adjustment set. The monthly estimand does not identify individual effects or daily triggering.

Exposure definitions and outcome-construction procedures will be specified before substantive association estimates are interpreted. Operational construction of all weather variables is described in the Weather section.

## Pollution

Monthly nitrogen dioxide, ozone, fine particulate matter (PM2.5) and respirable particulate matter (PM10) will be obtained from the Hong Kong Environmental Protection Department EPIC portal. The main analysis will use general monitoring stations. Roadside stations represent a distinct near-road environment and will be reserved for sensitivity analysis.

Completeness will be assessed for each pollutant–station–month against the expected number of observations. A station-month will contribute only when at least 75% of expected observations are available. Values below this threshold will be treated as missing before aggregation; missing measurements will not be coded as zero. Territory-wide monthly concentrations will be calculated as unweighted means across eligible general stations.

Pollution adjustment will be introduced in stages. Nitrogen dioxide and particulate matter will enter before ozone. Ozone will enter last because its seasonal and meteorological coupling with hot, sunny conditions may make simultaneous estimates difficult to interpret. Single- and multi-pollutant models will be treated as distinct adjustment sets rather than screened for favourable attenuation.

## Population denominators

Age- and sex-specific population estimates will be obtained from the Hong Kong Census and Statistics Department Table 110-01001. Mid-year estimates will be interpolated to calendar months. Count models will include the offset

\[
\log(\mathrm{population}\times \mathrm{days\ in\ month}).
\]

This offset accounts for changes in the population at risk and unequal month length. Age bands will remain separate only when the governed outcome aggregates and population series are compatible. Any broader grouping required by the released aggregate structure will be applied identically to outcomes and denominators.

## Statistical analysis

Monthly stroke-event counts will be analysed using negative-binomial regression when the variance exceeds the Poisson mean. Quasi-Poisson regression will provide an alternative mean–variance specification. Models will include calendar-month indicators for seasonality and a pre-specified smooth function of calendar time for long-term trend. Stratified models will use the population-by-days offset for the corresponding cell.

The analysis will retain the thermal exposures and contrasts defined in the Weather section. Continuous measures, official extreme-day counts, spell or event measures, and hot- or cold-month indicators will be treated as different exposure questions rather than interchangeable encodings. Same-month and lagged terms will be labelled separately. Nested thresholds will be fitted in separate models unless a contrast has been specified in advance.

Pollutants will be added through the staged adjustment sequence described above. Period-restricted or period-indicator models will assess sensitivity to COVID-19-related changes in health-care use. Additional adjustment and subgroup analyses will be conducted only when their data sources and aggregate structure support them.

Effect estimates will be reported as rate ratios with confidence intervals. Exposure prevalence, missingness and model diagnostics will be reported with the estimates. Diagnostics will assess overdispersion, residual autocorrelation, influential months and collinearity. The full pre-specified model panel will be presented jointly. Heat–cold comparisons will rely on planned contrasts and consistency across definitions, not on counts of nominally significant results.

## Definition of hot and cold months

Hot- and cold-month indicators will be organised as parallel, pre-specified definition families. The operational daily thresholds, percentile-based events, spell rules, combined day–night events and their monthly mapping are defined in the Weather section. This section does not modify those rules.

Before outcome associations are interpreted, each monthly definition will specify its source or rationale, reference period, percentile algorithm where relevant, treatment of ties, seasonal denominator, missing-day tolerance, cross-month assignment and event-overlap rule. Exposure-only summaries will report how often each definition occurs and which months it selects. Continuous event-day or intensity measures will accompany binary indicators where the Weather section specifies them.

No definition will be promoted because it produces the largest association. Confirmatory contrasts and sensitivity analyses will be labelled in advance, and the complete definition panel will remain visible in reporting. Final selection of the headline hot and cold specifications will be made by the study team after outcome-data quality control and descriptive review.

## Outcome

The outcome will comprise governed monthly aggregates of reconstructed stroke events. **As specified by the outcome co-investigator**, the first General Out-patient Clinic mention of stroke serves as a marker for case identification rather than as the presumed event date; the event is assigned to its reconstructed event month, and later mentions are not treated as new initial events. The health-data Methods will specify the governed source, event reconstruction, temporal aggregation and release procedures. No source fields, event counts, subtype availability or stratum structure are assumed here.
