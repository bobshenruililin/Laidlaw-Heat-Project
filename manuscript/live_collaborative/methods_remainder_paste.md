# Methods remainder — paste around Hogan’s weather paragraph

**Do not replace Hogan’s *Weather and pollutants data* paragraph.** If that paragraph is unchanged from 28 July 2026, it is already reproduced verbatim in `Heat_CVD_Manuscript_live_update.md`. If he has edited it, paste the blocks below around his current text.

Paste order in the live file:

1. **Study design** (new; before Health data)
2. **Health data** (bridge; Roro should expand)
3. Hogan’s **Weather and pollutants data** paragraph — leave in place
4. **Processing paragraph** (immediately after his paragraph, same subsection)
5. **Influenza**
6. **Population denominators and offsets**
7. **Statistical analysis** through **Ethics and governance**

---

### Study design

The design is an ecological territory-month time series covering January 2013 through December 2023 (132 months). For each separate single-exposure model, the target quantity is a count ratio associated with a 1 °C or five-day exposure contrast, conditional on calendar month and a smooth function of time. Individual causal effects, principal-diagnosis CHD or HF, AMI, and daily triggering are not identified. Because the diabetes or hypertension cohort still at risk of a first event was unavailable, the analysis-of-record offset is days in month. Estimates are therefore monthly count ratios, not cohort incidence-rate ratios. The twelve-contrast model set was specified after the outcome series were available and is exploratory. We refer to the twelve separate single-exposure models as the core panel.

### Health data

Governed monthly aggregates were constructed and released by the outcome co-investigator. The cohort comprised people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each outcome, the event was the first recorded hospitalisation after the patient’s first diagnosis record for CHD or HF. Diagnosis-record construction was assisted by a clinical collaborator. Admission cause was not recorded. Delivered columns were labelled `chd_inpatient` and `hf_inpatient` at territory × calendar month grain. Inpatient-only semantics are inferred from those labels and remain subject to confirmation. Age–sex strata were not included. A stroke series was named in correspondence but was not attached; no stroke analysis is reported. Field-level ICD lists and the executable timing rule remain with the outcome co-investigator and should replace this paragraph where they differ from it.

### Weather and pollutants data — processing only (after Hogan’s paragraph)

Daily Headquarters series were aggregated to calendar months for analysis. Core exposures were monthly mean temperature, the monthly means of daily maximum and minimum temperature, and official counts of hot nights, very hot days, and cold days, the last three scaled per five days so that coefficients correspond to a five-day contrast rather than a single extreme day. Official cold days were concentrated in December–February (Results, Figure 2), so with calendar-month indicators in the model the remaining cold-day variation is a difference between years within winter months. A winter-only restriction is a labelled sensitivity, not a remedy for that identification. Extremely hot days, relative humidity, rainfall, and sulfur dioxide were assembled with the weather series but were not entered in the twelve-contrast core panel. Fine particulate matter (PM2.5) from general EPD stations was assembled for staged pollution sensitivities. A station-month contributed to a pollutant mean only when at least 75% of expected observations were available; missing measurements were not coded as zero. Territory-wide monthly concentrations were unweighted means across eligible general stations. Roadside stations were reserved. Nitrogen dioxide and particulate matter were specified to enter before ozone, because ozone is coupled with hot, sunny conditions. Staged pollution models exist in the archive; they are not adjusted versions of the separate core panel and were not used to claim that confounding is resolved. Operational heatwave-spell and hot-month rules beyond the official daily thresholds remain with the weather co-investigator; provisional monthly-tail indicators were not used as confirmatory exposures.

### Influenza

Monthly influenza activity was obtained from Centre for Health Protection Flu Express summaries. Coverage was 121 of 132 months, with the gap in early 2013. Missing influenza months were left missing and were never coded as zero. Influenza was not entered in the twelve-contrast core panel.

### Population denominators and offsets

Age- and sex-specific mid-year population estimates from the Census and Statistics Department (Table 110-01001) were linearly interpolated to calendar-month midpoints. Those denominators describe the general population, not the diabetes or hypertension cohort still at risk of a first CHD or HF hospitalisation. Core models therefore used a days-in-month offset and are interpreted as monthly count ratios. A general-population × days offset was retained only as a sensitivity. It does not convert the estimand into cohort incidence.

### Statistical analysis

Core models used a negative-binomial likelihood. The linear predictor included a days-in-month offset, one exposure, calendar-month indicators, and a natural cubic spline of month index with four degrees of freedom. Each model entered one exposure at a time: mean temperature, mean maximum temperature, mean minimum temperature, hot nights, cold days, or very hot days, for CHD and for HF (twelve contrasts). Quasi-Poisson models were a family sensitivity.

Core intervals used Newey–West standard errors with lag 6, reported together with model-based, HC1, and Newey–West lag-3 intervals. Lag 6 was the core reporting choice because residual serial dependence is expected in monthly counts and is material for CHD. Robust intervals are not automatically wider than model-based intervals; the four-construction ladder is reported for that reason. No interval was selected because it excluded 1.

Joint models that entered maximum and minimum temperature together, or the three official extreme-day counts together, were retained as collinearity diagnostics.

Robustness analyses comprised alternative trend smooths (3, 6, and 8 df), year fixed effects, exclusion of the first 12 or 24 months, a pre-2020 window (January 2013–December 2019; 84 months), COVID-phase adjustment, lag-0/1/2 month exposures, and exclusion of the month with largest Cook’s distance. COVID phases were pre-COVID (through January 2020), early COVID (February 2020–December 2021), fifth wave (January–April 2022), late 2022 (May–December 2022), and post-reopening (from January 2023). Pearson residual autocorrelation and Ljung–Box tests at lags 6 and 12 were inspected. Benjamini–Hochberg *q*-values were computed across the twelve core contrasts.

Archive models that entered pollution, humidity, or influenza are not adjusted versions of the separate core panel.

### Constrained daily-exposure recovery

A constrained method for recovering daily exposure coefficients from monthly sums was evaluated in simulation against Hong Kong weather. A 500-replicate calibration failed Type I, coverage, bias, and sign-recovery requirements. A subsequent worst-cell re-summary of the same fits did not reverse that decision. No daily health coefficient was produced. This is a project-specific result; it does not show that the Basagaña–Ballester method fails in general.

### Software

Analyses were conducted in R 4.3.3. Negative-binomial models used `MASS::glm.nb`. Newey–West and HC1 standard errors used `sandwich`. Natural cubic splines used `splines::ns`.

### Ethics and governance

Analyses used governed Hospital Authority monthly aggregates supplied under existing collaborative arrangements. Source monthly counts are not redistributed. Written confirmation from the outcome and supervising investigators remains required before journal submission.
