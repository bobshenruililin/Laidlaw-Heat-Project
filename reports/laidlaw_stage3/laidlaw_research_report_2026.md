---
title: "Heat, cold and first hospitalisation after cardiovascular diagnosis in Hong Kong"
subtitle: "An exploratory monthly study among people with diabetes or hypertension, 2013–2023"
author: "Shen Ruililin"
date: "Laidlaw Scholars Programme · The University of Hong Kong · August 2026"

bibliography: literature/references.bib
csl: literature/vancouver.csl
citeproc: true
reference-section-title: References
link-citations: true
lang: en-GB

documentclass: article
classoption: oneside
papersize: a4
fontsize: 11pt
toc: false
indent: false
linestretch: 1.15
numbersections: false
fig-pos: H

geometry:
  - left=25mm
  - right=25mm
  - top=22mm
  - bottom=22mm
  - includeheadfoot
  - headheight=14pt
  - headsep=6mm
  - footskip=10mm

mainfont: "TeX Gyre Termes"
sansfont: "TeX Gyre Heros"
monofont: "DejaVu Sans Mono"
mainfontoptions:
  - Ligatures=TeX

colorlinks: true
linkcolor: black
citecolor: black
urlcolor: black
filecolor: black
---

**Affiliation.** School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong, Hong Kong SAR, China.

**Supervisor.** Professor David Makram Bishai, School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong.

# Abstract

**Background.** Hong Kong is recording more hot nights than a decade ago, while cold days persist. People with type 2 diabetes or hypertension already face high risk of coronary heart disease (CHD) and heart failure (HF). Whether monthly temperature patterns are associated with monthly first-hospitalisation counts in this group is untested.

**Methods.** Governed Hospital Authority aggregates supplied monthly counts of first hospitalisation after a first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension, January 2013–December 2023 (132 months). Admission cause was not recorded. Model 1 is a separate negative-binomial fit for each of six thermal measures and each outcome: monthly mean, mean maximum and mean minimum temperature, and official counts of hot nights, very hot days and cold days, with calendar-month indicators, a smooth long-term trend, and a days-in-month offset. Model 2 adds monthly mean relative humidity and monthly total rainfall. Model 3 replaces official extreme-day counts with days warmer or cooler than the historical same-calendar-day mean. Reported estimates are from Model 1. Intervals used model-based, HC1, and Newey–West lag-3 and lag-6 constructions. Benjamini–Hochberg *q*-values covered the twelve Model 1 comparisons.

**Results.** Under Newey–West lag 6, five additional hot nights corresponded to a CHD count ratio of 1.022 (1.002–1.042) and five additional cold days to an HF count ratio of 1.073 (1.006–1.144), both with *q* = 0.192; all twelve *q*-values exceeded 0.19. For CHD hot nights, model-based and HC1 intervals included 1, as did the pre-2020 estimate (1.011, 0.991–1.032). For HF cold days, all four constructions excluded 1, and the pre-2020 estimate was stronger (1.113, 1.053–1.176). Official cold days fell almost entirely in December–February (141 of 145).

**Conclusions.** The data do not support a multiplicity-protected thermal claim. The HF association is concordant across standard-error methods; the CHD association depends on the construction and on including 2020–2023. Estimates are ecological monthly count ratios for a first-event outcome without recorded admission cause.

**Keywords:** hot nights; cold days; coronary heart disease; heart failure; Hong Kong; monthly time series

# Introduction

Hong Kong is becoming hotter, especially at night, while cold winter days persist. Both heat and cold can place additional stress on the cardiovascular system. This matters particularly for people living with type 2 diabetes or hypertension, who already face a high risk of coronary heart disease (CHD) and heart failure (HF).

At Hong Kong Observatory Headquarters, official hot nights rose from 10 in 2013 to a peak of 61 in 2021 [@hko2013; @hko2021]. Cold days persisted across the same decade. A contemporary local analysis therefore has to hold heat and cold in one design.

Temperature can affect cardiovascular health through several pathways. Heat can promote dehydration, disturb sleep and overnight recovery, and increase cardiac demand. Cold can raise blood pressure and vascular resistance. Responses may be stronger in people whose cardiovascular regulation is already compromised by diabetes or hypertension [@ye2012]. These mechanisms make both sides of the temperature distribution relevant.

Hong Kong already has important evidence on daily temperature and health. Earlier studies examined daily stroke or acute myocardial infarction admissions and reported substantial cold-related patterns [@goggins2012stroke; @goggins2013]. Closest to the present outcomes, Goggins and Chan analysed daily public-hospital heart-failure admissions and deaths during 2002–2011 and reported a strong cold association [@goggins2017hf]. Liu and colleagues estimated mortality attributable to non-optimal temperature and found a larger fraction associated with cold than heat during 2006–2016 [@liu2020jasmine]. More recent work modelled heat-related excess deaths under several heatwave definitions [@liu2026roro]. A daily mortality attributable fraction, a modelled number of excess deaths, and a monthly hospitalisation count ratio cannot be substituted for one another.

Nighttime heat can be encoded in more than one way. Guo et al. analysed daily unplanned emergency hospitalisations in Hong Kong during the hot seasons of 2000–2019 [@guo2024hotnights]. After adjustment for multi-day mean temperature, the official hot-night indicator showed no overall association with non-cancer hospitalisation, whereas an hourly nighttime excess-heat metric did. Official monthly counts of hot nights are a coarser encoding than that hourly metric. They remain an interpretable public climatological series, and they are not a test of it.

Health data are often released in aggregate form to protect privacy. In this project, the governed outcomes were available only as territory-wide monthly counts of each person's first recorded hospitalisation after a first diagnosis record for CHD or HF, among people with type 2 diabetes and/or hypertension. Admission cause is absent. That resolution can support a study of monthly burden, but it cannot reveal whether a particular hot day triggered a hospitalisation several days later, and it cannot support a claim of principal-diagnosis CHD or acute myocardial infarction.

The objective was to estimate monthly associations between specified thermal-exposure contrasts and these first-hospitalisation counts from January 2013 through December 2023, carrying heat and cold in parallel, reporting the complete Model 1 panel of twelve comparisons, and testing whether monthly outcomes could support a more ambitious daily-exposure extension.

# Methods

## Study design

The design is an ecological territory-month time series covering January 2013 through December 2023 (132 months). For each single-exposure model, the target quantity is a count ratio associated with a 1 °C or five-day exposure contrast, conditional on calendar month and a smooth function of time. Individual causal effects, principal-diagnosis CHD or HF, acute myocardial infarction, and daily triggering are not identified [@greenland1989ecological; @bhaskaran2013].

## Health data

Governed Hospital Authority aggregates supplied the two outcomes. The cohort comprised people recorded with type 2 diabetes and/or hypertension during the study period. For each outcome, the monthly series counted the first recorded hospitalisation after the person's first CHD or HF diagnosis record. Diagnosis-record construction was assisted by a clinical collaborator. Admission cause was not recorded. Delivered columns are labelled inpatient; the inpatient inclusion rule and event-timing semantics require data-provider confirmation. Age–sex strata were not included. A stroke series was named in correspondence but was not attached, and no stroke analysis is reported. Source monthly health files and merged health panels were not placed in public version control.

## Temperature measures

Daily weather observations came from Hong Kong Observatory Headquarters and were checked against annual Observatory summaries before analysis. Six Model 1 measures were evaluated: monthly mean temperature; the monthly means of daily maximum and minimum temperature; hot nights (minimum temperature at least 28 °C); very hot days (maximum temperature at least 33 °C); and cold days (minimum temperature at most 12 °C). Continuous measures were interpreted per 1 °C. Extreme-day counts were interpreted per five additional days in a month. Monthly mean relative humidity and monthly total rainfall were assembled for Model 2; they are not in the Model 1 estimates below. More complex heatwave definitions exist [@wang2019ehwe; @li2025heatwaves]; the six measures give the clearest common comparison. Air-pollution and influenza series were assembled for the broader project; Model 1 does not claim that confounding by those factors has been resolved.

## Statistical analysis

Model 1 comprises separate negative-binomial fits for each outcome and each thermal exposure, giving twelve comparisons [@bhaskaran2013]. Each fit included calendar-month indicators, a natural cubic spline of month index with 4 degrees of freedom, and a days-in-month offset. Model 2 adds monthly mean relative humidity and monthly total rainfall to that specification. Model 3 keeps the Model 1 structure but replaces official extreme-day counts with counts of days whose daily mean temperature was above or below the leave-one-year-out mean for that calendar day; maximum- and minimum-temperature versions of those counts are sensitivities. Model 2 and Model 3 are specified; they have not been fitted to the governed health panel in this report, and no health coefficients are invented for them. Uncertainty for Model 1 was reported four ways: model-based, HC1, and Newey–West with lags of three and six months.[^se] The main results use the six-month Newey–West interval; all four are displayed. No method was chosen because it made a confidence interval exclude 1. Benjamini–Hochberg *q*-values were calculated across the twelve Model 1 comparisons.

**How to read the estimates.** A count ratio of 1 means no estimated difference in the monthly count; 1.05 means a 5% higher count for the stated exposure change. Because monthly counts of cohort members still at risk of a first event were unavailable, these are count ratios rather than incidence-rate ratios. A *q*-value limits the expected proportion of false discoveries when all twelve comparisons are considered together; it is not the probability that a result is true.

[^se]: Residual serial dependence is expected in monthly counts and is material for CHD (Results). Robust intervals are not automatically wider than model-based intervals, which is why the four-construction ladder is reported.

Robustness analyses varied the long-term trend, removed early years, restricted the series to 2013–2019, adjusted for pandemic phases, examined lag-0 to lag-2 month exposures, and excluded the most influential month. Joint models were used only as collinearity diagnostics.

A constrained method that combines monthly outcomes with daily exposures was evaluated in simulation against Hong Kong weather before any application to real health counts [@basagana2024md; @basagana2026md]. The method failed predefined error, coverage, bias and sign-recovery requirements (Appendix). No daily health coefficient was produced.

Analyses used R 4.3.3. Governed aggregates were analysed under existing collaborative arrangements; aggregation does not by itself confer external-publication authority.

# Results

## Outcome and exposure series

The governed series contained 156,156 CHD first-hospitalisation events and 29,681 HF events across 132 months (Table 1). Monthly means were 1,183.0 and 224.9. Both series showed seasonality, with a stronger winter peak for HF. Official hot nights and very hot days rose across the decade, with year-to-year variation; cold days remained recurrent (Figure 1). Of 145 official cold days in 2013–2023, 141 fell in December–February, and 29 of 132 months carried at least one.

```{=latex}
\Needspace{8\baselineskip}
```

**Table 1.** Outcome summary, Hong Kong, 2013–2023.

| Outcome                | Months | Total events | Mean per month |
|:-----------------------|------:|-------------:|---------------:|
| Coronary heart disease |    132 |      156,156 |        1,183.0 |
| Heart failure          |    132 |       29,681 |          224.9 |

*Note.* The event is the first recorded hospitalisation after the first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension. Admission cause was not recorded.

![Official hot nights, very hot days and cold days at Hong Kong Observatory Headquarters, 2013–2023. These are environmental descriptors, not health findings.](figures/exposure_aging/fig01_annual_extremes_coexistence.png){width=82% fig-pos=H}

## Model 1

Table 2 reports the twelve separate-exposure Model 1 count ratios under Newey–West lag-6 intervals. Most estimates were close to 1. The largest CHD estimate was for hot nights: 1.022 per five additional hot nights (1.002–1.042; *p* = 0.032). The largest HF estimate was for cold days: 1.073 per five additional cold days (1.006–1.144; *p* = 0.031). After correction, both had *q* = 0.192, and every *q*-value exceeded 0.19. The panel provides no confirmed association. Figure 2 displays the same twelve intervals.

```{=latex}
\Needspace{18\baselineskip}
```

**Table 2.** Model 1: separate negative-binomial models with a days-in-month offset and Newey–West lag-6 intervals. Thermal exposures only.

| Outcome | Exposure contrast                | Count ratio (95% CI) | *q*   |
|:--------|:---------------------------------|---------------------:|------:|
| CHD     | Mean temperature / 1 °C          | 0.993 (0.976–1.010)  | 0.726 |
| CHD     | Mean maximum temperature / 1 °C  | 0.993 (0.979–1.007)  | 0.642 |
| CHD     | Mean minimum temperature / 1 °C  | 0.994 (0.977–1.012)  | 0.764 |
| CHD     | Hot nights / 5 days              | 1.022 (1.002–1.042)  | 0.192 |
| CHD     | Cold days / 5 days               | 0.995 (0.949–1.043)  | 0.900 |
| CHD     | Very hot days / 5 days           | 0.999 (0.974–1.025)  | 0.962 |
| HF      | Mean temperature / 1 °C          | 0.974 (0.947–1.002)  | 0.207 |
| HF      | Mean maximum temperature / 1 °C  | 0.981 (0.958–1.005)  | 0.272 |
| HF      | Mean minimum temperature / 1 °C  | 0.973 (0.947–1.000)  | 0.202 |
| HF      | Hot nights / 5 days              | 1.003 (0.976–1.031)  | 0.900 |
| HF      | Cold days / 5 days               | 1.073 (1.006–1.144)  | 0.192 |
| HF      | Very hot days / 5 days           | 0.995 (0.963–1.028)  | 0.900 |

![Count ratios and 95% confidence intervals for the twelve Model 1 monthly fits. The dashed line at 1 indicates no estimated difference. All twelve Benjamini–Hochberg *q*-values exceeded 0.19.](outputs/release_chd_hf/figures/figure3_core_forest.png){width=88% fig-pos=H}

## Uncertainty and robustness

The CHD hot-night point estimate was 1.022 under all four standard-error methods. Intervals were 0.995–1.049 (model-based), 0.997–1.047 (HC1), 1.0003–1.0439 (Newey–West lag 3), and 1.002–1.042 (Newey–West lag 6). The first two include 1; the Newey–West intervals exclude it, at lag 3 only just. Residual autocorrelation at lag 1 was 0.508 in this model. The Newey–West intervals were also narrower than the model-based interval, which is unusual when residuals are positively correlated. The exclusion of 1 therefore rests on the smaller robust variance estimate, which is a reason for caution rather than confirmation.

The HF cold-day point estimate was 1.073. Its four intervals were 1.023–1.125, 1.011–1.138, 1.007–1.143, and 1.006–1.144. All excluded 1. Concordance across standard-error methods does not create multiplicity protection: *q* remained 0.192. The full ladder is Table A1.

Restricting the series to 2013–2019, before the pandemic altered hospital use, strengthened the HF cold-day ratio to 1.113 (1.053–1.176) and weakened the CHD hot-night ratio to 1.011 (0.991–1.032). The CHD association is therefore confined to analyses that include 2020–2023; the HF association is not. Across other checks, the CHD ratio ranged from 1.011 to 1.025 and the HF ratio from 1.043 to 1.113. At a one-month lag, the CHD estimate moved toward 1 while the HF estimate remained elevated; none of these checks establishes a daily lag sequence.

The attempted monthly-outcome, daily-exposure estimator passed numerical convergence checks but failed calibration (Appendix). No daily coefficient was applied to the real health series.

# Discussion

These data do not support a multiplicity-protected differential thermal claim. Under Newey–West lag-6 reporting, CHD first-hospitalisation counts were more closely associated with official hot-night burden than with mean temperature or very hot days, and HF counts were more closely associated with cold-day burden than with any heat measure. Both patterns sit inside the twelve Model 1 comparisons, in which every *q*-value exceeds 0.19. The twelve Model 1 fits were specified after the outcome series was available. The complete Model 1 panel is therefore reported, and no contrast is promoted to a primary result.

The HF cold-day association is the more coherent of the two residual signals. It is concordant across all four standard-error constructions, survives exclusion of the most influential month, and is strongest before 2020. It nevertheless remains unprotected by its *q*-value. Because official cold days fall almost entirely in December–February, and because only 29 of 132 months carry any official cold day, the association is identified from differences between winters rather than from a summer-versus-winter contrast. The direction is consistent with earlier daily evidence that lower temperature was associated with higher heart-failure admissions in Hong Kong [@goggins2017hf]. The comparison is between questions, not magnitudes: a cumulative daily relative risk is not a monthly count ratio per five official cold days, and the present event is a first hospitalisation after a first HF diagnosis without recorded admission cause.

The CHD hot-night association is smaller, depends on the uncertainty method, and was not evident before 2020. It should be read against Guo et al. rather than as a replication of that study [@guo2024hotnights]. A difference between monthly mean temperature and monthly official hot-night counts does not identify an hourly nighttime-heat mechanism. Interrupted overnight recovery is one hypothesis for why a hot-night count could differ from monthly mean temperature; the monthly design cannot test it. Five additional official days is a reporting scale, not a consecutive-day trigger. Ambient heat is associated with shorter sleep [@chevance2024sleep]. Three laboratory hot nights left core temperature high into recovery in young men [@ioannou2024heatwave]. Bedroom temperatures above 24 °C were associated with lower heart-rate variability in older adults [@oconnor2025bedroom]. Those papers do not measure first CHD hospitalisation here, and a scoping review found only three extreme-heat–sleep–cardiovascular studies, with mixed blood-pressure findings [@ashe2025ehe]. Cold can raise afterload; heart failure has little reserve against that load [@ikaheimo2018cold; @li2026cold]. None of these pathways is identified in 132 monthly counts. Liu et al. remain complementary mortality baselines [@liu2020jasmine; @liu2026roro]; their attributable fractions and excess-death totals cannot be rescaled into the present count ratios.

**Strengths.** The twelve Model 1 comparisons are reported in full. Uncertainty is shown as an explicit four-construction ladder. Extreme-day exposures use published official thresholds. Weather definitions were source-checked against Observatory summaries. The daily-recovery analysis is reported as a refusal rather than as a coefficient.

**Limitations.** Nine limitations determine how these results should be read:

1. **Outcome meaning.** Admission cause was not recorded, and event semantics await data-provider confirmation (Methods); an event is a first hospitalisation after a first CHD or HF diagnosis, not a demonstrated cardiac-caused admission.
2. **Ecological resolution.** Each observation describes Hong Kong for one month; individual exposure and within-month timing are unknown [@greenland1989ecological].
3. **Denominator.** Monthly counts of cohort members still at risk of a first event were unavailable, so the estimates are count ratios rather than incidence-rate ratios.
4. **Confounding.** Adjustment for pollution, humidity and influenza is unresolved in Model 1. Model 2 specifies humidity and rainfall but is not fitted here. Model 3 is specified and is likewise unfitted.
5. **Exposure measurement.** Headquarters weather is a territory-level proxy for neighbourhood, indoor and personal exposure.
6. **Serial dependence.** CHD residual autocorrelation remained material (0.508 at lag 1), and the Newey–West intervals were narrower than the model-based interval, so their exclusion of 1 is a reason for caution rather than confirmation.
7. **Multiplicity.** No comparison survived Benjamini–Hochberg correction across the twelve contrasts; every *q*-value exceeded 0.19.
8. **Period and season structure.** The CHD hot-night estimate is compatible with 1 before 2020 (1.011, 0.991–1.032), whereas the HF cold-day estimate is stronger before 2020 (1.113, 1.053–1.176); official cold days are concentrated in December–February (141 of 145), so the HF contrast is identified between winters.
9. **Available outcomes.** Age, sex and disease-subtype strata were not delivered; a stroke series was not delivered, and no stroke result is reported.

## Implications and next study

The data cannot identify within-month timing, individual exposure, or the cause of admission. The failed daily-exposure calibration is an empirical reason not to present a daily coefficient. The present findings do not justify disease-specific warning thresholds, a consecutive-day trigger, or an evaluation of Hong Kong’s existing warnings. They do support continued attention to both overnight heat and winter cold.

WHO heat–health action-plan guidance lists eight core elements [@who2026hhap]. Hong Kong already has a warning, communication and shelter bundle, including a Prolonged Heat Special Alert that names a few days of very hot days or hot nights [@chong2023hko; @hko_vhw]. Department of Health advice already names heart disease and high blood pressure [@chp2025heatstroke]. Appendix Table A2 maps each WHO element to that bundle and to what this panel can and cannot inform. I do not count admissions averted.

The next study needs dated, cause-recorded admissions, cohort person-time, and daily or weekly outcome resolution. Those next hypotheses—whether repeated hot nights precede CHD-related admissions, and whether cold days precede HF-related admissions in this cohort—should be declared in advance, with heat and cold retained and the full uncertainty display preserved.

# Conclusion

Between 2013 and 2023, Hong Kong experienced increasing hot-night burden while cold days persisted. In governed monthly data for people with diabetes and/or hypertension, CHD first-hospitalisation counts were more closely associated with hot nights, and HF counts with cold days, than with the other thermal measures examined. Neither association survived correction across twelve comparisons, and the CHD estimate depended on the uncertainty method and on including the pandemic years.

The study therefore offers hypotheses, not proof of thermal effects. Physiological accounts of overnight recovery and cold-related afterload, and a mapping onto published heat–health action-plan elements, are interpretation, not identification. What it leaves behind is a precisely defined first-event outcome, a complete twelve-comparison Model 1 panel, uncertainty shown under four methods, and a documented refusal to produce daily coefficients that monthly counts cannot support.

# Acknowledgements

I am especially grateful to Professor David Makram Bishai, who supervised this Laidlaw Scholars project. He set its scientific direction: a complete comparison of heat and cold encodings in one Hong Kong panel rather than a search for a single confirmatory association, with every comparison reported, uncertainty shown under more than one standard-error method, and the limits of monthly aggregates stated in the same document as the estimates. He advised on population-health interpretation of monthly counts and guided what may honestly be reported from governed Hospital Authority aggregates. The study sits within a School of Public Health programme he leads on temperature and health in Hong Kong, which also includes complementary modelled heatwave-mortality work. This report is submitted for the Laidlaw Stage 3 requirement under his supervision. Journal writing continues separately with the weather and health-data co-investigators. Remaining errors are mine.

I thank Hogan for guidance on weather definitions and on academic writing, and Zhenyuan Liu for constructing and releasing the governed Hospital Authority aggregates and for regression mentorship. Diagnosis-record construction was assisted by Dr Jingjing Zhou. Dissemination of governed results requires the approval of the team and the relevant institutions.

```{=latex}
\clearpage
\Needspace{14\baselineskip}
```

# Appendix

**Table A1.** Uncertainty ladder for the two leading exploratory contrasts.

| Outcome and exposure    | Uncertainty method | Count ratio |          95% CI |
|:------------------------|:-------------------|------------:|----------------:|
| CHD hot nights / 5 days | Model-based        |       1.022 |     0.995–1.049 |
| CHD hot nights / 5 days | HC1                |       1.022 |     0.997–1.047 |
| CHD hot nights / 5 days | Newey–West lag 3   |       1.022 |   1.0003–1.0439 |
| CHD hot nights / 5 days | Newey–West lag 6   |       1.022 |     1.002–1.042 |
| HF cold days / 5 days   | Model-based        |       1.073 |     1.023–1.125 |
| HF cold days / 5 days   | HC1                |       1.073 |     1.011–1.138 |
| HF cold days / 5 days   | Newey–West lag 3   |       1.073 |     1.007–1.143 |
| HF cold days / 5 days   | Newey–West lag 6   |       1.073 |     1.006–1.144 |

**Daily-exposure calibration.** The constrained monthly-outcome, daily-exposure estimator was evaluated in a 500-replicate simulation matched to Hong Kong weather and to the overdispersion and residual dependence of the monthly series [@basagana2024md; @basagana2026md]. In the most difficult cells, false-positive rates reached 0.150, confidence-interval coverage fell to 0.840, and sign recovery was poor for moderate effects. Admission of any real daily coefficient required all frozen calibration criteria to pass. They did not. This is a project-specific calibration result, not a general indictment of the method. A full daily distributed-lag non-linear model is not identified from 132 monthly sums.

**Table A2.** WHO 2026 heat–health action-plan elements, Hong Kong instruments, and what this panel can inform. This table is a mapping, not an evaluation.

| WHO element | Hong Kong instrument | This panel can inform | This panel cannot inform |
|:--|:--|:--|:--|
| 1. Governance | Multi-agency bundle (HKO, DH/CHP, Labour, HAD) | Heat and cold already have separate warning authorities | Whether coordination is adequate |
| 2. Warning system | VHWW; Hot Weather Special Advisory; Prolonged Heat Special Alert (a few days of very hot days or hot nights); Extremely Hot Weather ~35 °C; HKHI | CHD residual sits with official hot-night counts, not very-hot-day counts; Prolonged Heat already names nights | A new consecutive-day trigger; whether warnings work |
| 3. Populations at increased risk | CHP names heart disease and high blood pressure among at-risk groups | The present T2D/HTN first-event cohort is already inside that named group | A new named group; age or subtype targeting |
| 4. Communication | HKO, CHP, and Labour public advice | Overnight heat and winter cold both deserve continued attention | Message-testing or behaviour change |
| 5. Health-system resilience | Hospital Authority operations (not studied) | Monthly first-event counts are not a surge dashboard | Staffing or ward cooling |
| 6. Reducing heat exposure | Indoor ventilation or air-conditioning advice; HAD temporary heat shelters | Indoor night temperature is a hypothesis from sleep and autonomic studies | Indoor temperature or shelter use in this series |
| 7. Surveillance | No near-real-time first-event CHD/HF feed | Why monthly aggregates cannot guide activation | Event-day surveillance beyond needing dated, cause-recorded admissions |
| 8. Monitoring, evaluation and learning | Not performed here | Honest evaluation would need daily cause-recorded data and a predeclared contrast | This report as an evaluation of warnings |

Cold-weather counterpart (not a WHO heat element): Cold Weather Warning and HAD temporary cold shelters. The more coherent residual here is HF × official cold days.
