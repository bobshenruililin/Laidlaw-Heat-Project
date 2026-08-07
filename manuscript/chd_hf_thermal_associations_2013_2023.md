# Monthly Thermal Exposures and First Hospitalisations for Coronary Heart Disease and Heart Failure among Adults with Diabetes or Hypertension in Hong Kong, 2013–2023

## Authors and affiliations

**Bob Shen Ruililin**^1^

^1^ Laidlaw Scholars Programme, The University of Hong Kong, Hong Kong SAR, China

Collaborative outcome construction was led by the outcome co-investigator. Weather definition guidance was provided by the weather co-investigator. Population-health supervision was provided by the supervising investigator. Full names and institutional details for co-authors will be finalised before external submission.

## Abstract

**Background.** Hot nights and cold days both remain common in subtropical Hong Kong. Monthly associations between thermal burden and first cardiovascular hospitalisations among people with type 2 diabetes or hypertension are poorly characterised.

**Methods.** We analysed territory-month counts of first inpatient hospitalisation after a first coronary heart disease (CHD) or heart failure (HF) diagnosis record among people diagnosed with type 2 diabetes and/or hypertension during January 2013–December 2023 (132 months; 156,156 CHD events; 29,681 HF events). Exposures were monthly mean temperature, mean maximum and minimum temperature, and official extreme-day counts (hot nights, cold days, and very hot days). Separate negative-binomial models adjusted for calendar month and a natural spline of time (4 degrees of freedom). The primary offset was days in month. Inference used Newey–West standard errors with lag 6. Joint multi-exposure models, alternative offsets, trend and first-event-depletion sensitivities, lag models, and residual diagnostics were retained as labelled robustness analyses.

**Results.** In separate exposure models, CHD first hospitalisations were higher in months with more hot nights (count ratio per five hot nights 1.022, 95% CI 1.002–1.042). HF first hospitalisations were higher in months with more cold days (count ratio per five cold days 1.073, 95% CI 1.006–1.144). Continuous temperature associations were near null for CHD and weakly inverse for HF. Benjamini–Hochberg q-values for the twelve exploratory core contrasts were all greater than 0.19. Joint models that entered correlated heat metrics together inflated the CHD hot-night coefficient relative to the separate model. CHD residuals remained serially correlated under the baseline spline; Newey–West intervals and count-series sensitivities were therefore retained.

**Conclusions.** In this governed monthly series, CHD first hospitalisations tracked hot-night burden and HF first hospitalisations tracked cold-day burden more closely than mean temperature. The associations are ecological monthly count ratios under a first-event construction without recorded admission cause. They are not principal-diagnosis attack rates, daily triggering effects, or mortality attributable fractions.

## Introduction

Cardiovascular disease remains a leading cause of hospital care in ageing subtropical cities. Temperature can alter blood pressure, vascular tone, fluid balance, and cardiac demand. Hot nights and very hot days have become more frequent in Hong Kong, yet cold days continue to occur. Warming therefore changes the balance of thermal hazards rather than removing cold risk.

Hong Kong evidence on temperature and cardiovascular outcomes has largely used daily admissions or mortality with distributed-lag models. Goggins and colleagues reported cold-dominant associations for stroke and acute myocardial infarction in earlier periods. Later mortality work quantified non-optimal temperature and heatwave burden using attributable fractions and transported relative risks. Those quantities are not interchangeable with monthly morbidity associations under a different outcome construction.

The present study analyses monthly first hospitalisations after a first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension. The extract does not record the reason for each admission. The estimand is therefore an ecological association between monthly thermal burden and monthly first-event counts under that cohort restriction. It is not a principal-diagnosis CHD or HF admission analysis, not an acute myocardial infarction series from general Hospital Authority extracts without admission reasons, and not a stroke analysis. Stroke aggregates named in the covering correspondence were not available for this release.

Exposure definition remains a scientific problem. Continuous monthly temperatures, official extreme-day counts, and heat-month indicators answer different questions and can select different months. Correlated heat metrics entered jointly can redistribute effects across coefficients. The analysis therefore reports separate single-exposure models as the amended core panel and retains joint models as collinearity diagnostics.

## Methods

### Design and estimand

The study is an ecological territory-month time series covering January 2013 through December 2023 (132 months). The target quantity for each amended core model is a count ratio for monthly first-hospitalisation counts associated with a one-unit or five-day exposure contrast, conditional on seasonality and long-term trend.

### Outcome data

Governed monthly aggregates were supplied by the outcome co-investigator. The cohort universe comprised people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each outcome, the event was the first inpatient hospitalisation after the patient’s first diagnosis record for CHD or HF. Diagnosis-record construction was assisted by a clinical collaborator. Admission cause was not recorded. Counts were available at territory × calendar month grain only. Age–sex strata and stroke counts were not included in the delivered files. Provenance for analysis rows was labelled `HA_APPROVED_AGGREGATE`.

### Exposures

Daily Hong Kong Observatory Headquarters observations were aggregated to calendar months. Continuous exposures were monthly mean temperature and the monthly means of daily maximum and minimum temperature. Official extreme-day counts were hot nights (daily minimum temperature ≥28 °C), very hot days (daily maximum temperature ≥33 °C), and cold days (daily minimum temperature ≤12 °C). Extreme-day exposures were scaled per five days. Lag-one and lag-two month values were created for sensitivity models. Provisional hot-month and cold-month indicators were retained only in the supplement because weather reference rules remain unlocked.

### Denominator and offset

Census and Statistics Department population aged 35 years and older × days in month is available as an ecological person-time offset. It is not person-time among members of the diabetes or hypertension cohort still at risk of a first CHD or HF hospitalisation. Because the release does not provide that cohort denominator, amended core models used `log(days in month)` and are interpreted as monthly count ratios. Population × days and no-offset models were retained as sensitivities.

### Statistical models

Amended core models (pathway IDs P01A, P02A, P02B, P04A, P04B, and P04C) entered one exposure at a time. Each model used a negative-binomial likelihood, a calendar-month factor, and a natural cubic spline of month index with four degrees of freedom. Primary inference used Newey–West standard errors with lag 6. Model-based, HC1, and Newey–West lag-3 intervals were retained. Quasi-Poisson models were fitted as a family sensitivity.

The complete pathway panel retained joint exploratory models that entered maximum and minimum temperature together, or the three official extreme-day counts together, and nested heat-month indicators. Those joint structures are reported for comparison with the separate models and are not designated as confirmatory contrasts. Heat-month percentile indicators were also fitted one definition at a time in separate models.

Robustness analyses comprised alternative trend smooths (3, 6, and 8 degrees of freedom), year fixed effects, exclusion of the first 12 or 24 months, a pre-2020 window, COVID-phase adjustment, lag-0/1/2 exposure models, exclusion of the highest Cook’s-distance month, and negative-binomial INGARCH(1,1) count-series models without an offset. Residual autocorrelation, Ljung–Box tests, and exposure correlations after month and trend residualisation were inspected. Benjamini–Hochberg q-values were computed across the twelve amended core contrasts.

### Provenance and disclosure

Source monthly count files and merged health panels were retained outside version control. Manuscript tables and figures report disclosure-minimised model summaries and indexed series. External submission still requires confirmation from the outcome and supervising investigators.

## Results

### Outcome series

CHD contributed 156,156 first hospitalisations over 132 months (mean 1,183.0 per month). HF contributed 29,681 (mean 224.9 per month). Both series declined over calendar time on an indexed scale (Figure 1). Seasonal profiles differed by outcome (Figure 2).

### Amended core associations

Table 2 and Figure 3 summarise the twelve separate-exposure count ratios under days-in-month offset and Newey–West lag-6 intervals.

For CHD, hot nights were associated with higher monthly first-hospitalisation counts (count ratio per five hot nights 1.022, 95% CI 1.002–1.042; p = 0.032; q = 0.192). Mean temperature, mean maximum temperature, mean minimum temperature, cold days, and very hot days were near null.

For HF, cold days were associated with higher monthly first-hospitalisation counts (count ratio per five cold days 1.073, 95% CI 1.006–1.144; p = 0.031; q = 0.192). Mean minimum temperature was weakly inverse (0.973, 95% CI 0.947–1.000). Hot nights and very hot days were near null.

No amended core contrast had a Benjamini–Hochberg q-value below 0.19. The two unadjusted associations that crossed the conventional 0.05 threshold therefore remain exploratory panel results rather than multiplicity-protected primary claims.

### Joint models and collinearity

After month and trend residualisation, maximum and minimum temperature retained a variance inflation factor of 4.66 when entered jointly. Hot nights and very hot days retained variance inflation factors near 1.96. In the joint extreme-day model with days-in-month offset and Newey–West lag-6 intervals, the CHD hot-night count ratio rose to 1.045 (95% CI 1.015–1.075), whereas the separate hot-night model gave 1.022. The HF cold-day coefficient was similar in joint and separate models (about 1.073). Joint coefficients are therefore retained as diagnostic comparisons, not as preferred effect estimates.

### Robustness

Offset choice changed amended core count ratios only trivially. Across trend and first-event-depletion scenarios, the CHD hot-night ratio ranged from 1.011 to 1.025, and the HF cold-day ratio ranged from 1.043 to 1.113. The HF cold-day association was stronger in the pre-2020 window (1.113, 95% CI 1.053–1.176). Lag-1 and lag-2 models attenuated the CHD hot-night association toward the null. The HF cold-day association remained elevated at lag 1 (1.073, 95% CI 1.014–1.135) and was weaker at lag 2. Exclusion of the highest Cook’s-distance month left both signals in the same direction.

Pearson residual autocorrelation at lag 1 was about 0.51 for CHD baseline models and about 0.15 for HF. Ljung–Box tests rejected residual white noise for CHD but not for HF. Negative-binomial INGARCH(1,1) models reduced residual autocorrelation and retained positive CHD hot-night and HF cold-day associations. Newey–West lag-6 intervals remain the primary reported uncertainty for the amended core table because the baseline generalised linear models do not remove serial dependence.

## Discussion

Two qualitative patterns emerge from the amended panel. CHD first hospitalisations among people with diabetes or hypertension tracked official hot-night burden more closely than mean temperature or cold days. HF first hospitalisations tracked cold-day burden more closely than hot nights. That pattern is consistent with local historical emphasis on cold for cardiac admissions and with contemporary concern about nighttime heat, but it should not be over-interpreted as a causal partition of heat and cold pathways.

The methodological corrections matter for interpretation. Joint entry of correlated heat metrics inflated the CHD hot-night coefficient relative to the separate model. Nested heat-month percentile indicators in a single equation estimate incremental contrasts rather than stand-alone definition effects. Residual autocorrelation in the CHD series makes model-based intervals too narrow; Newey–West and count-series sensitivities are therefore part of the result, not optional extras. Declining first-event counts over the decade raise the possibility of cohort depletion or changing coding and care patterns; trend and early-period sensitivities bound that concern but cannot eliminate it without cohort denominators.

These monthly count ratios are not daily distributed-lag triggering estimates. They are not mortality attributable fractions. They are not principal-diagnosis CHD or HF admission rates. They are not acute myocardial infarction findings from general Hospital Authority extracts without admission reasons. Stroke remains outside the present release.

## Limitations

1. Admission cause was not recorded; the event is first hospitalisation after a first CHD or HF diagnosis record.
2. The cohort still at risk of a first event was unavailable, so rates are not true cohort incidence rates.
3. The analysis is ecological and monthly; within-month timing and individual temperature exposure are unobserved.
4. Age, sex, and subtype strata were not delivered.
5. CHD residual serial correlation remains material under the baseline spline.
6. Multiplicity-adjusted q-values for the exploratory core family do not support a protected primary claim.
7. Weather hot-month and cold-month reference rules remain unlocked; those indicators stay supplementary.
8. External dissemination still requires confirmation from the outcome and supervising investigators.

## Data and code

Disclosure-minimised tables, claim ledger, and figures are archived under `outputs/release_chd_hf/`. Source monthly health counts and merged panels are governed and not redistributed through the public repository. Analysis code is available in the project scripts directory. External submission requires team confirmation.

## Acknowledgements

We thank the outcome co-investigator for constructing and releasing the governed monthly aggregates, the weather co-investigator for guidance on thermal definitions and scientific writing, the supervising investigator for population-health oversight, and the clinical collaborator who assisted diagnosis-record construction.

## Tables and figures

- **Table 1.** Outcome summary (`outputs/release_chd_hf/tables/table1_outcome_summary.csv`).
- **Table 2.** Amended core single-exposure models (`table2_core_models.csv`).
- **Table 3.** Robustness ranges (`table3_robustness_summary.csv`).
- **Figure 1.** Indexed monthly first-hospitalisation series.
- **Figure 2.** Seasonal profile.
- **Figure 3.** Core forest plot.
- **Figure 4.** Trend and first-event sensitivity forest.

Claim identifiers CVD-01 to CVD-12 in `outputs/release_chd_hf/tables/claim_ledger.csv` map one-to-one to Table 2 rows.
