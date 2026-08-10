---
title: "Aggregation-Aware Inference for Monthly Thermal Associations with First Hospitalisation after CHD or HF Diagnosis in Hong Kong, 2013–2023"
author:
  - Bob Shen Ruililin
affiliation:
  - "Laidlaw Scholars Programme, The University of Hong Kong, Hong Kong SAR, China"
bibliography: literature/references.bib
reference-section-title: References
link-citations: true
geometry: margin=1in
fontsize: 11pt
colorlinks: true
mainfont: DejaVu Serif
sansfont: DejaVu Sans
monofont: DejaVu Sans Mono
---

<!--
Authorship-order note (not part of the scientific body):
Author order remains human-owned. See
manuscript/authorship_and_governance_decisions.md. Collaborative outcome
construction was led by the outcome co-investigator. Weather definition
guidance was provided by the weather co-investigator. Population-health
supervision was provided by the supervising investigator. Diagnosis-record
construction was assisted by a clinical collaborator. Full co-author names,
order, and any co-first designation will be finalised before external
submission. No final author order is asserted here.
-->

*Laidlaw Scholars Programme, The University of Hong Kong, Hong Kong SAR, China*

Collaborative contributions are credited in the Acknowledgements. Author order
is recorded separately and is not finalised in this repository version.

## Abstract

**Background.** Monthly ecological analyses of thermal burden and cardiovascular hospitalisation must confront correlated exposure definitions, serial dependence, and the limits of recovering daily effects from monthly sums. In subtropical Hong Kong, hot nights and cold days both remain common.

**Methods.** We analysed territory-month counts of the first recorded hospitalisation after a first coronary heart disease (CHD) or heart failure (HF) diagnosis record among people diagnosed with type 2 diabetes and/or hypertension during January 2013–December 2023 (132 months; 156,156 CHD events; 29,681 HF events). Admission cause was not recorded. Exposures were monthly mean temperature, mean maximum and minimum temperature, and official extreme-day counts (hot nights, cold days, and very hot days). Separate negative-binomial models adjusted for calendar month and a natural spline of time (4 df). The analysis-of-record offset was days in month. Uncertainty was reported as a Model / HC1 / Newey–West lag-3 / Newey–West lag-6 ladder; Newey–West lag 6 was retained as continuity analysis of record, not because an interval excluded the null. Benjamini–Hochberg q-values covered the twelve core contrasts. A constrained monthly-outcome / daily-exposure (M|D) estimator was evaluated under synthetic calibration only. The reported model set was specified after the outcome series were available and is exploratory.

**Results.** Continuity Newey–West lag-6 count ratios included CHD hot nights 1.022 (1.002–1.042) and HF cold days 1.073 (1.006–1.144); both had q = 0.192. Across the Model–HC1–NW3–NW6 ladder, the CHD hot-night intervals were 0.995–1.049, 0.997–1.047, 1.0003–1.0439, and 1.002–1.042; the HF cold-day intervals were 1.023–1.125, 1.011–1.138, 1.007–1.143, and 1.006–1.144. All twelve core q-values exceeded 0.19. CHD Pearson residual autocorrelation at lag 1 was approximately 0.51; HF was approximately 0.15. Joint entry of correlated heat metrics inflated the CHD hot-night coefficient relative to the separate model. Synthetic M|D calibration failed under strict worst-cell gates (null Type I 0.048–0.150; minimum coverage 0.840; maximum non-null relative bias 32.77; maximum moderate false-sign 0.808; stress coverage 0.842). No real daily-exposure coefficient was admitted.

**Conclusions.** The current data do not support a protected differential thermal claim for CHD versus HF. The HF cold-day association is concordant across standard-error methods but unprotected by multiplicity (q = 0.192). The CHD hot-night association is sensitive to standard-error construction. Monthly first-hospitalisation associations in this series remain ecological count ratios under a first-event construction without recorded admission cause.

## Introduction

Cardiovascular disease remains a leading cause of hospital care in ageing subtropical cities. Temperature can alter blood pressure, vascular tone, fluid balance, and cardiac demand [@ye2012; @bhaskaran2013]. Hot nights and very hot days have become more frequent in Hong Kong, yet cold days continue to occur [@hko2013; @hko2021]. Warming therefore changes the balance of thermal hazards rather than removing cold risk.

Hong Kong evidence on temperature and cardiovascular outcomes has largely used daily admissions or mortality with distributed-lag models [@goggins2012stroke; @goggins2013; @chan2013bullwho; @gasparrini2010]. Jingwen Liu et al. (2020) estimated cause-specific mortality attributable to non-optimal temperature during 2006–2016 and reported cold attributable fraction 4.72% versus heat 0.16%, with moderate non-optimum temperatures accounting for more burden than extremes [@liu2020jasmine; @gasparrini2015]. Zhenyuan Liu et al. (2026) transported local relative risks under four heatwave scenarios and reported 1,455–3,238 model-based excess deaths across definitions for 2014–2023 [@liu2026roro]. Those quantities are daily mortality attributable fractions and modelled excess deaths. They are not monthly morbidity count ratios under a different outcome construction.

Exposure definition remains a scientific problem. Continuous monthly temperatures, official extreme-day counts, prolonged spells, and heat-month indicators answer different questions and can select different months [@wang2019ehwe; @li2025heatwaves; @guo2017ehp; @guo2024hotnights]. Correlated heat metrics entered jointly can redistribute effects across coefficients. When outcomes are available only as monthly sums, recovering daily thermal coefficients is a separate methods question [@basagana2024md; @basagana2026md]. It is not automatic.

The present study analyses monthly first recorded hospitalisations after a first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension. The extract does not record the reason for each admission. The estimand is an ecological association between monthly thermal burden and monthly first-event counts under that cohort restriction. It is not a principal-diagnosis CHD or HF admission analysis, not an acute myocardial infarction series from general Hospital Authority extracts without admission reasons, and not a stroke analysis. A stroke series was not delivered.

The manuscript thesis is aggregation-aware inference and thermal-definition uncertainty. Exploratory CHD hot-night and HF cold-day signals are reported inside a complete panel with multiplicity, residual dependence, and standard-error discordance. They are not promoted to confirmatory primary discoveries.

### Scientific framing of aggregation

When health outcomes are released only as monthly sums, two inferential tasks are often confused. The first is to estimate associations between monthly thermal burden and monthly counts. The second is to recover daily exposure coefficients from those sums. The first task is available under the present data contract. The second is a methods question that requires calibration [@basagana2024md; @basagana2026md]. Treating a monthly count ratio as if it were a daily trigger estimate would overstate temporal resolution. Treating a failed calibration as a minor software issue would understate the limit.

Thermal definition multiplies the problem. A month can be labelled hot because its mean temperature is high, because it contains many official hot nights, because it contains a long spell, or because it falls in the upper tail of an atmospheric event-count distribution [@wang2019ehwe; @li2025heatwaves; @guo2017ehp]. These encodings are related but non-interchangeable. Reporting one favourite definition without the others converts definition uncertainty into apparent discovery.

## Methods

### Design and estimand

The study is an ecological territory-month time series covering January 2013 through December 2023 (132 months). For each separate single-exposure model in the continuity panel, the target quantity is a count ratio for monthly first-hospitalisation counts associated with a one-unit or five-day exposure contrast, conditional on seasonality and long-term trend. Because the diabetes or hypertension cohort still at risk of a first event was unavailable, the analysis-of-record offset was days in month. Estimates are therefore monthly count ratios, not cohort incidence-rate ratios [@greenland1989ecological]. The reported model set was specified after the outcome series were available and is exploratory rather than prospectively confirmatory.

### Outcome data

Governed monthly aggregates were supplied by the outcome co-investigator. The cohort universe comprised people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each outcome, the event was the first recorded hospitalisation after the patient’s first diagnosis record for CHD or HF. The delivered monthly columns were labelled `chd_inpatient` and `hf_inpatient`. Inpatient-only semantics are inferred from those labels and remain subject to confirmation by the outcome co-investigator. Diagnosis-record construction was assisted by a clinical collaborator. Admission cause was not recorded. Counts were available at territory × calendar month grain only. Age–sex strata and stroke counts were not included in the delivered files. Provenance for analysis rows was labelled `HA_APPROVED_AGGREGATE`. External dissemination still requires confirmation from the outcome and supervising investigators.

### Exposures

Daily Hong Kong Observatory Headquarters observations were aggregated to calendar months. Continuous exposures were monthly mean temperature and the monthly means of daily maximum and minimum temperature. Official extreme-day counts were hot nights (daily minimum temperature ≥28 °C), very hot days (daily maximum temperature ≥33 °C), and cold days (daily minimum temperature ≤12 °C) [@hko2013; @wang2019ehwe]. Extreme-day exposures were scaled per five days. Lag-one and lag-two month values were created for sensitivity models.

Source-locked atmospheric and spell morphologies were validated for the final
exposure audit against published counts: Li et al. (2025) warm-season
heatwave events 1980–2023 (57/57), and Wang et al. (2019) very hot days, hot
nights, and ≥5-day spell event-days for 2006–2015 (204/204, 230/230, 48/48,
and 56/56) [@li2025heatwaves; @wang2019ehwe]. These post-outcome source checks
did not revise the core association estimates. Provisional hot-month and
cold-month indicators remained unlocked and were retained only in the
Supplement.

### Statistical models

Continuity panel models entered one exposure at a time for each outcome: mean temperature, mean maximum temperature, mean minimum temperature, hot nights, cold days, and very hot days. Each model used a negative-binomial likelihood, a calendar-month factor, and a natural cubic spline of month index with four degrees of freedom [@bhaskaran2013]. Continuity analysis-of-record intervals used Newey–West standard errors with lag 6, reported together with model-based, HC1, and Newey–West lag-3 intervals [@lazarus2018har]. No interval was selected because it excluded the null. Quasi-Poisson models were fitted as a family sensitivity.

Joint exploratory models that entered maximum and minimum temperature together, or the three official extreme-day counts together, were retained as collinearity diagnostics. Heat-month percentile indicators were fitted one definition at a time in separate supplementary models.

Robustness analyses comprised alternative trend smooths (3, 6, and 8 degrees of freedom), year fixed effects, exclusion of the first 12 or 24 months, a pre-2020 window, COVID-phase adjustment, lag-0/1/2 exposure models, and exclusion of the highest Cook’s-distance month. Negative-binomial INGARCH(1,1) models without an offset were fitted as residual-dependence diagnostics only; they are not directly comparable with the days-offset continuity estimates [@zhu2011nbingarch]. Residual autocorrelation and Ljung–Box tests were inspected. Benjamini–Hochberg q-values were computed across the twelve continuity-panel contrasts.

Existing pollution, absolute-humidity, and influenza model paths in the broader pathway archive were legacy or joint structures from earlier panel scaffolding. They are not adjusted versions of the present separate single-exposure continuity models and were not used to claim resolution of confounding.

### Multiplicity and uncertainty display

The twelve outcome–exposure contrasts form one family for false-discovery control. Continuity intervals use Newey–West lag 6 because residual serial dependence is expected in monthly counts and is material for CHD. Model-based, HC1, and Newey–West lag-3 intervals are shown in parallel [@lazarus2018har]. The analysis does not choose an interval after inspecting whether it excludes the null. That display rule is part of the estimand discipline: uncertainty construction is reported, not optimised for significance.

### Constrained monthly-outcome / daily-exposure method

A constrained aggregated-outcome likelihood with daily exposure (M|D) was evaluated as methods feasibility following the Basagaña–Ballester aggregation framework [@basagana2024md; @basagana2026md]. Implementation was clean-room from the published equation. Public code without a repository licence was not copied. Synthetic calibration used real Hong Kong Observatory weather with synthetic daily outcomes matched to disclosure-minimised seasonality, scale, overdispersion, and residual dependence. Admission of any real daily-exposure coefficient required all frozen calibration gates to pass. A full rich daily distributed-lag non-linear model was prohibited at n = 132 months [@gasparrini2010].

### Provenance and disclosure

Source monthly count files and merged health panels were retained outside version control. Manuscript tables and figures report disclosure-minimised model summaries and indexed series. Quantitative claims CVD-01 to CVD-12 map one-to-one to the release claim ledger.

## Results

### Outcome series

CHD contributed 156,156 first recorded hospitalisations over 132 months (mean 1,183.0 per month). HF contributed 29,681 (mean 224.9 per month) (Table 1). Both series declined over calendar time on an indexed scale (Figure 1). Seasonal profiles differed by outcome (Figure 2).

**Table 1. Outcome summary.**

| Outcome | Period | Months | Total events | Mean per month | Event construction |
|---|---|---:|---:|---:|---|
| Coronary heart disease | 2013–2023 | 132 | 156,156 | 1,183.0 | First recorded hospitalisation after first CHD diagnosis record |
| Heart failure | 2013–2023 | 132 | 29,681 | 224.9 | First recorded hospitalisation after first HF diagnosis record |

![Indexed monthly first-hospitalisation series for CHD and HF, January 2013–December 2023. Each outcome's 2013 monthly mean equals 100; absolute monthly counts are not shown.](../outputs/release_chd_hf/figures/figure1_indexed_outcome_series.png){width=100%}

![Calendar-month seasonal profiles of indexed CHD and HF first-hospitalisation counts.](../outputs/release_chd_hf/figures/figure2_seasonal_pattern.png){width=100%}

### Complete continuity panel

Table 2 and Figure 3 summarise the twelve separate-exposure count ratios under days-in-month offset. Continuity analysis-of-record intervals are Newey–West lag 6. The full uncertainty ladder is Table 4 and Figure 5.

**Table 2. Complete continuity panel: separate negative-binomial models with
days-in-month offset and Newey–West lag-6 intervals.**

| Outcome | Exposure contrast | Count ratio (95% CI) | p | BH q |
|---|---|---:|---:|---:|
| CHD | Mean temperature / 1 °C | 0.993 (0.976–1.010) | 0.424 | 0.726 |
| CHD | Mean maximum temperature / 1 °C | 0.993 (0.979–1.007) | 0.321 | 0.642 |
| CHD | Mean minimum temperature / 1 °C | 0.994 (0.977–1.012) | 0.509 | 0.764 |
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 0.032 | 0.192 |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 0.823 | 0.900 |
| CHD | Very hot days / 5 days | 0.999 (0.974–1.025) | 0.962 | 0.962 |
| HF | Mean temperature / 1 °C | 0.974 (0.947–1.002) | 0.069 | 0.207 |
| HF | Mean maximum temperature / 1 °C | 0.981 (0.958–1.005) | 0.113 | 0.272 |
| HF | Mean minimum temperature / 1 °C | 0.973 (0.947–1.000) | 0.050 | 0.202 |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.825 | 0.900 |
| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 0.031 | 0.192 |
| HF | Very hot days / 5 days | 0.995 (0.963–1.028) | 0.764 | 0.900 |

![Forest plot of the twelve continuity-panel count ratios under days-in-month offset and Newey–West lag-6 intervals. Point estimates and intervals correspond to Table 2. Benjamini–Hochberg q-values for all twelve contrasts exceeded 0.19.](../outputs/release_chd_hf/figures/figure3_core_forest.png){width=100%}

<!-- claim:CVD-01 -->
<!-- CHD mean temperature per 1 °C: 0.993 (0.976–1.010); q = 0.726. -->

<!-- claim:CVD-02 -->
<!-- CHD mean maximum temperature per 1 °C: 0.993 (0.979–1.007); q = 0.642. -->

<!-- claim:CVD-03 -->
<!-- CHD mean minimum temperature per 1 °C: 0.994 (0.977–1.012); q = 0.764. -->

<!-- claim:CVD-04 -->
<!-- CHD hot nights per five days: 1.022 (1.002–1.042); p = 0.032; q = 0.192. -->

<!-- claim:CVD-05 -->
<!-- CHD cold days per five days: 0.995 (0.949–1.043); q = 0.900. -->

<!-- claim:CVD-06 -->
<!-- CHD very hot days per five days: 0.999 (0.974–1.025); q = 0.962. -->

<!-- claim:CVD-07 -->
<!-- HF mean temperature per 1 °C: 0.974 (0.947–1.002); q = 0.207. -->

<!-- claim:CVD-08 -->
<!-- HF mean maximum temperature per 1 °C: 0.981 (0.958–1.005); q = 0.272. -->

<!-- claim:CVD-09 -->
<!-- HF mean minimum temperature per 1 °C: 0.973 (0.947–1.000); q = 0.202. -->

<!-- claim:CVD-10 -->
<!-- HF hot nights per five days: 1.003 (0.976–1.031); q = 0.900. -->

<!-- claim:CVD-11 -->
<!-- HF cold days per five days: 1.073 (1.006–1.144); p = 0.031; q = 0.192. -->

<!-- claim:CVD-12 -->
<!-- HF very hot days per five days: 0.995 (0.963–1.028); q = 0.900. -->

All twelve continuity-panel Benjamini–Hochberg q-values exceeded 0.19. No contrast therefore meets a multiplicity-protected confirmatory threshold in this exploratory panel.

For CHD, continuous monthly mean temperatures were near null (count ratios 0.993–0.994), whereas the official hot-night count association was larger under continuity Newey–West lag-6 reporting. These encodings are non-interchangeable descriptions of monthly thermal burden; the contrast does not imply that a causal hot-night effect was missed by the means. For HF, continuous temperature associations were weakly inverse and the cold-day count association was positive. That pattern remains exploratory under multiplicity control.

### Standard-error discordance for the leading exploratory contrasts

**Table 4. Uncertainty ladder for the two leading exploratory contrasts.**

| Outcome and exposure | Model | HC1 | NW3 | NW6 |
|---|---|---|---|---|
| CHD hot nights / 5 days | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.0003–1.0439) | 1.022 (1.002–1.042) |
| HF cold days / 5 days | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

The complete 48-row ladder is Supplementary Table S1.

For CHD hot nights, the point estimate was 1.022 under all four standard-error methods. The 95% intervals were Model 0.995–1.049, HC1 0.997–1.047, Newey–West lag 3 1.0003–1.0439, and Newey–West lag 6 1.002–1.042. Model-based and HC1 intervals included the null; NW3 and NW6 excluded it on the unrounded scale. No interval was used to designate a primary claim.

For HF cold days, the point estimate was 1.073. The 95% intervals were Model 1.023–1.125, HC1 1.011–1.138, Newey–West lag 3 1.007–1.143, and Newey–West lag 6 1.006–1.144. All four intervals excluded the null for this contrast, but the corresponding q-value remained 0.192. Concordance across standard-error methods therefore does not by itself create multiplicity protection.

### Joint models and collinearity

After month and trend residualisation, maximum and minimum temperature retained a variance inflation factor of 4.66 when entered jointly. Hot nights and very hot days retained variance inflation factors near 1.96. In the joint extreme-day model with days-in-month offset and Newey–West lag-6 intervals, the CHD hot-night count ratio rose to 1.045 (1.015–1.075), whereas the separate hot-night model gave 1.022. The HF cold-day coefficient was similar in joint and separate models (about 1.073). Joint coefficients are diagnostic comparisons, not preferred effect estimates.

### Residual dependence

Pearson residual autocorrelation at lag 1 was approximately 0.51 for CHD baseline models (range 0.508–0.534 across the six continuity-panel exposures) and approximately 0.15 for HF (range 0.131–0.179). Ljung–Box tests rejected residual white noise for CHD but not for HF. Negative-binomial INGARCH(1,1) models without an offset reduced residual autocorrelation and retained positive CHD hot-night and HF cold-day associations; those unoffset diagnostics are not directly comparable with the days-offset continuity estimates. Serial dependence is therefore part of the inferential problem, not an optional diagnostic footnote.

### Robustness

**Table 3. Point-estimate ranges across trend/depletion, offset, lag, and
influence analyses.**

| Outcome | Exposure | Baseline | Trend/depletion range | Offset range | Lag 0–2 range | After max-Cook exclusion |
|---|---|---:|---:|---:|---:|---:|
| CHD | Mean temperature / 1 °C | 0.993 | 0.980–0.996 | 0.993–0.993 | 0.993–0.999 | 0.995 |
| CHD | Mean maximum temperature / 1 °C | 0.993 | 0.982–0.995 | 0.993–0.993 | 0.993–0.999 | 0.994 |
| CHD | Mean minimum temperature / 1 °C | 0.994 | 0.982–0.998 | 0.994–0.994 | 0.994–0.997 | 0.996 |
| CHD | Hot nights / 5 days | 1.022 | 1.011–1.025 | 1.021–1.022 | 1.010–1.022 | 1.021 |
| CHD | Cold days / 5 days | 0.995 | 0.989–1.036 | 0.995–0.997 | 0.995–1.026 | 0.990 |
| CHD | Very hot days / 5 days | 0.999 | 0.993–1.006 | 0.999–0.999 | 0.999–1.021 | 0.999 |
| HF | Mean temperature / 1 °C | 0.974 | 0.945–0.985 | 0.974–0.974 | 0.973–0.998 | 0.966 |
| HF | Mean maximum temperature / 1 °C | 0.981 | 0.958–0.990 | 0.981–0.981 | 0.981–0.998 | 0.973 |
| HF | Mean minimum temperature / 1 °C | 0.973 | 0.944–0.983 | 0.973–0.973 | 0.970–0.997 | 0.966 |
| HF | Hot nights / 5 days | 1.003 | 0.965–1.007 | 1.003–1.003 | 0.997–1.012 | 1.002 |
| HF | Cold days / 5 days | 1.073 | 1.043–1.113 | 1.073–1.075 | 1.053–1.073 | 1.088 |
| HF | Very hot days / 5 days | 0.995 | 0.988–0.997 | 0.995–0.995 | 0.995–1.018 | 0.994 |

![Trend and first-event-depletion sensitivity forest for continuity-panel exposures. Ranges summarise alternative trend smooths, year fixed effects, early-period exclusions, pre-2020 restriction, and COVID-phase adjustment (Table 3).](../outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png){width=100%}

![Standard-error method ladder for the twelve continuity-panel contrasts. Each exposure shows Model, HC1, Newey–West lag-3, and Newey–West lag-6 intervals around the same point estimate. Intervals were not selected by null exclusion.](../outputs/release_chd_hf/figures/figure5_se_method_ladder.png){width=100%}

Offset choice changed continuity-panel count ratios only trivially (Table 3; Figure 4). Across trend and first-event-depletion scenarios, the CHD hot-night ratio ranged from 1.011 to 1.025, and the HF cold-day ratio ranged from 1.043 to 1.113. The HF cold-day association was stronger in the pre-2020 window (1.113, 1.053–1.176). Lag-1 and lag-2 models attenuated the CHD hot-night association toward the null. The HF cold-day association remained elevated at lag 1 (1.073, 1.014–1.135) and was weaker at lag 2 (1.053, 0.985–1.127). Exclusion of the highest Cook’s-distance month left both signals in the same direction.

Offset triviality and directional stability under influence checks reduce concern that a single coding month drives the exploratory pattern. They do not resolve residual autocorrelation in the CHD series, nor do they convert q-values above 0.19 into protected primary claims. Lag-one and lag-two month models remain labelled sensitivities and do not identify a daily lag curve.

### Methods-feasibility: constrained daily-exposure recovery

Synthetic M|D calibration failed under the frozen F1.2 worst-cell gates. Null Type I error ranged from 0.048 to 0.150. Minimum core coverage was 0.840. Maximum absolute relative bias for non-null effects was 32.77. Maximum moderate-effect false-sign rate was 0.808. Minimum stress-scenario coverage was 0.842. Convergence and Hessian gates passed; Type I, coverage, bias, false-sign, and stress coverage did not. An earlier 100-replicate pilot with harmonic nuisance seasonality had already failed for HF-like null cells (Type I approximately 0.62–0.75); calendar-month nuisance correction (F1.1) and worst-cell gate aggregation (F1.2) were applied before the final decision. The method was rejected for real-data admission. No real daily-exposure coefficient enters the Results as a health finding. Methods-validation figures are confined to the Supplement.

## Discussion

The current data do not support a protected differential thermal claim for CHD versus HF. Under continuity Newey–West lag-6 reporting, CHD first-hospitalisation counts were more closely associated with official hot-night burden than with mean temperature or cold days, and HF counts were more closely associated with cold-day burden than with hot nights. Those exploratory patterns sit inside multiplicity adjustment that leaves all twelve core q-values above 0.19. The HF cold-day association is concordant across Model, HC1, NW3, and NW6 intervals but remains q-unprotected (q = 0.192). The CHD hot-night association is standard-error sensitive: Model and HC1 intervals include the null, whereas NW3 and NW6 exclude it on the unrounded scale.

That pattern is consistent with local historical emphasis on cold for cardiac admissions and with contemporary concern about nighttime heat [@goggins2013; @guo2024hotnights]. It should not be over-interpreted as a causal partition of heat and cold pathways. Joint entry of correlated heat metrics inflated the CHD hot-night coefficient relative to the separate model. Declining first-event counts over the decade raise the possibility of cohort depletion or changing coding and care patterns; trend and early-period sensitivities bound that concern but cannot eliminate it without cohort denominators.

Daily mortality attributable fractions [@liu2020jasmine] and modelled excess deaths under heatwave scenarios [@liu2026roro] remain complementary literature baselines. They are not interchangeable with the present monthly morbidity count ratios. The failed M|D calibration shows that aggregation-aware inference can reject, not only propose, recovery of daily thermal coefficients from monthly sums [@basagana2024md]. Weekly or daily morbidity designs with governed outcomes would be required before daily lag claims are scientifically available.

### What a protected claim would have required

A protected primary claim would have required, at minimum, a predeclared confirmatory contrast, multiplicity control that survives the twelve-contrast family, standard-error constructions that do not rest on choosing the interval that excludes the null, and residual diagnostics that do not leave substantial CHD serial correlation unaddressed. The present release does not meet that bar. The scientifically stronger move is to report the complete panel and the refusals.

Pollution, influenza, and humidity associations are scientifically motivated in Hong Kong [@guo2025temppollution; @yang2025coldflu]. Existing archive paths for those covariates were legacy or joint structures and are not adjusted versions of the present separate continuity models. Confounding by pollution, humidity, or influenza is therefore not resolved here [@greenland1989ecological]. Absent the still-at-risk cohort denominator, even a perfectly stable count ratio remains a count ratio. Future incidence language requires that denominator, not a change of adjectives in the abstract.

## Strengths and limitations

Strengths include a complete twelve-contrast panel with claim-ledger identity, an explicit standard-error ladder, source-validated weather morphology, disclosure-minimised release validation, and a predeclared refusal to admit uncalibrated daily-exposure estimates.

Limitations:

1. Admission cause was not recorded; the event is the first recorded hospitalisation after a first CHD or HF diagnosis record.
2. Delivered columns were labelled `*_inpatient`; inpatient-only semantics are inferred and remain unconfirmed.
3. The cohort still at risk of a first event was unavailable, so rates are not true cohort incidence rates.
4. The analysis is ecological and monthly; within-month timing and individual temperature exposure are unobserved [@greenland1989ecological].
5. Age, sex, and subtype strata were not delivered.
6. CHD residual serial correlation remains material under the baseline spline.
7. Multiplicity-adjusted q-values for the exploratory continuity family do not support a protected primary claim; HF cold-day SE concordance does not create multiplicity protection, and CHD hot-night inference is SE-sensitive.
8. Weather hot-month and cold-month reference rules remain unlocked; those indicators stay supplementary.
9. Legacy pollution, humidity, and influenza pathway fits were not adjusted versions of the separate continuity panel; confounding by those covariates is unresolved.
10. Negative-binomial INGARCH fits were unoffset diagnostics and are not directly comparable with days-offset continuity estimates.
11. Synthetic calibration used disclosure-minimised seasonality rather than governed daily outcomes; failure blocks real M|D admission but does not itself estimate a health effect.
12. External dissemination still requires confirmation from the outcome and supervising investigators.
13. Author order remains unresolved and is recorded separately.

## Ethics and governance

Analyses used governed Hospital Authority monthly aggregates supplied under existing collaborative arrangements. Source monthly counts and merged panels remain outside public version control. Aggregation reduces re-identification risk but does not grant external-publication authority. Written confirmation from the outcome and supervising investigators remains required before journal submission or public promotion. Whether the IRB protocol requires amendment for this HA work remains a human-owned decision.

## Data and code availability

Disclosure-minimised tables, claim ledger, and figures are archived under `outputs/release_chd_hf/`. Source monthly health counts and merged panels are governed and not redistributed through the public repository. Analysis code is available in the project scripts directory. Exact table and figure paths are listed below. External submission requires team confirmation.

## Acknowledgements

We thank the outcome co-investigator for constructing and releasing the governed monthly aggregates, the weather co-investigator for guidance on thermal definitions and scientific writing, the supervising investigator for population-health oversight, and the clinical collaborator who assisted diagnosis-record construction.
