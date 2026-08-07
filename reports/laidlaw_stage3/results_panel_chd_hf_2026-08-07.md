# Monthly thermal exposures and first cardiovascular hospitalisations among adults with diabetes or hypertension in Hong Kong, 2013–2023: a complete multi-specification panel

**Bob Shen Ruililin** · Laidlaw Scholars Programme, The University of Hong Kong  
**Analysis date:** 7 August 2026  
**Provenance:** `HA_APPROVED_AGGREGATE` monthly counts supplied by Zhenyuan Liu; weather and confounders from public HKO, EPD, C&SD, and CHP series.  
**Authority note:** The live shared manuscript remains the collaborative manuscript file. This repository report documents the completed real-data panel for CHD and HF. Stroke aggregates were not in the 7 August upload. Team Gate 3 freeze is still required before any single specification is treated as the primary claim.

## Abstract

We analysed monthly associations between thermal exposures and first inpatient hospitalisations for coronary heart disease (CHD) and heart failure (HF) among people with type 2 diabetes and/or hypertension in Hong Kong from January 2013 through December 2023. Outcome counts were constructed by the outcome co-investigator as the first hospitalisation after the first diagnosis record for each condition. Negative-binomial models with month indicators and a flexible time trend produced a pre-specified pathway panel and provisional hot- and cold-month definitions. For CHD, each additional five hot nights was associated with a rate ratio of 1.044 (95% CI 1.012–1.077). For HF, each additional five cold days was associated with a rate ratio of 1.073 (1.011–1.138), and each 1 °C higher monthly mean minimum temperature with 0.958 (0.919–0.998). Continuous same-month mean temperatures were weakly associated with CHD. Extreme heat-month percentile indicators were internally discordant. Person-time used Census and Statistics Department population aged 35 years and older and is not the diabetes–hypertension cohort still at risk of a first event. Stroke counts were not delivered. No specification is frozen as primary until the investigative team closes the analysis-plan freeze.

## Introduction (estimand update)

Earlier project framing targeted monthly stroke-event aggregates. On 7 August 2026 the outcome co-investigator released monthly CHD and HF first-hospitalisation counts for the diabetes and/or hypertension cohort and clarified that admission causes are not recorded in the underlying patient extract. The operative estimand for the present panel is therefore the ecological association between monthly thermal burden and monthly first CHD or HF hospitalisations in that cohort. Stroke remains intended but unanalysed until the file arrives.

## Methods (outcome and analysis)

**Design.** Ecological monthly time series, 132 territory-months, January 2013–December 2023.

**Outcomes.** CHD inpatient first events after first CHD diagnosis; HF inpatient first events after first HF diagnosis; cohort restricted to type 2 diabetes and/or hypertension diagnoses during 2013–2023. Territory-month grain only.

**Exposures.** Hong Kong Observatory Headquarters continuous temperatures, official extreme-day counts, spell and combined day–night metrics, lag-one-month temperatures, and provisional hot/cold-month flags built from the project registry under a study-window reference period.

**Offset.** log(population aged ≥35 × days in month). A days-only offset sensitivity was also fit.

**Models.** Negative binomial regression with month factors and a natural spline of time index (4 degrees of freedom). Heteroskedasticity-consistent standard errors. Pathway identifiers follow `pathway_registry.yml`. Hot/cold-month models use provisional registry flags and are labelled not weather-locked.

## Results

### Descriptive pattern

CHD contributed 156,156 first hospitalisations (mean 1,183 per month). HF contributed 29,681 (mean 225 per month). Both series declined substantially from 2013 to 2023, consistent with a first-event construction in a finite at-risk pool and with care-seeking shocks. Seasonal structure and temperature correlations are summarised in `outputs/tables/cvd_descriptive_*.csv`. HF counts correlated more strongly and negatively with monthly mean temperature than CHD counts.

### Pathway panel — CHD

Fifteen of seventeen enabled pathways converged. Age and sex interaction pathways were skipped because strata were absent. Continuous same-month mean temperature (P01) and same-month maximum and minimum temperatures (P02) were compatible with no strong linear association. In the official extreme-day pathway (P04), hot nights scaled per five days had RR 1.044 (1.012–1.077), whereas very hot days scaled per five days had RR 0.971 (0.943–0.999) and cold days were near null. Hot-night spell days (P05) showed a small positive association. Heat-month indicators at the 95th and 97.5th percentiles of monthly mean temperature moved in opposite directions and should not be selectively elevated. Cold-month and cold-day pathways were largely null for CHD. Pre-COVID restriction (P16) did not create a large continuous-temperature signal. Offset choice did not reverse the hot-night direction.

### Pathway panel — HF

The same fifteen pathways converged. Lower monthly mean temperature (P01) and lower mean minimum temperature (P02) were associated with higher HF first-hospitalisation rates (mean_tmin RR 0.958, 0.919–0.998). Cold days in P04 had RR 1.073 (1.011–1.138) per five days; hot nights and very hot days were near null. Lag-one-month mean minimum temperature (P03) was also inverse. The cold-month indicator at the 5th percentile of mean temperature was imprecise, but provisional cold-month flags CM03 and CM08 showed elevated rate ratios. The pre-COVID subset strengthened the mean_tmin association (RR 0.923, 0.882–0.967). Pollution-staged and humidity-adjusted P02 models preserved the qualitative cold signal for HF, although confidence intervals widened when absolute humidity entered with temperature.

### Cross-outcome contrast

Shared headline terms show a provisional heat-night signal for CHD and a provisional cold signal for HF. This contrast is reported as a panel pattern. It is not a test of outcome-specific mechanisms and is not a Gate 3 headline.

### Hot/cold-month provisional panel

Registry-driven flags were built for the starter set. HM23 used a provisional daily calendar-day percentile construction under the study window and is not a weather co-investigator lock. Binary month models for HF suggested higher rates in colder absolute and relative months; CHD associations were weaker and mixed. These estimates remain labelled provisional.

## Discussion

The delivered outcomes change the scientific product from a stroke-only monthly panel to a diabetes–hypertension first-hospitalisation panel for CHD and HF. Within that panel, heat-night burden is more consistently associated with CHD first events, whereas cold burden is more consistently associated with HF first events. Continuous temperature associations are weak for CHD and cold-leaning for HF. Definition choice matters: extreme heat-month percentiles can disagree, which is why the analysis retains a labelled panel rather than a search for the largest coefficient.

Jingwen Liu et al. (2020) reported larger cold than heat attributable fractions for Hong Kong mortality. Zhenyuan Liu et al. (2026) quantified heatwave excess deaths under multiple definitions. Those studies estimate mortality burdens under daily constructions. The present results estimate monthly morbidity associations for first CHD and HF hospitalisations in a high-risk clinical cohort. The estimands are complementary, not interchangeable.

### Limitations

1. Person-time is general-population ecological offset, not diabetes–hypertension cohort at-risk time.
2. First-event counts decline secularly; residual trend misspecification can bias thermal coefficients.
3. Territory-month aggregates omit age, sex, and subtype strata.
4. Stroke counts were not supplied in the 7 August files.
5. Hot/cold-month reference periods are provisional pending weather lock.
6. Ecological monthly designs cannot identify daily triggering or individual causality.
7. Team analysis-plan freeze remains open; the panel is complete, the headline is not.

## Data and code

- Receipt: `reports/data_receipt_2026-08-07.md`
- Gate 2: `reports/gate2_qc_close_2026-08-07.md`
- Gate 3 packet: `reports/gate3_decision_packet_2026-08-07.md`
- Estimates: `outputs/tables/combined_pathway_panel_estimates.csv`
- Temperature share for collaborators: `outputs/share_for_roro/`
- Runner: `PATHWAY_MODE=real OUTCOMES=chd,hf Rscript scripts/run_cvd_full_analysis.R`

Hospital Authority monthly event files remain outside version control.
