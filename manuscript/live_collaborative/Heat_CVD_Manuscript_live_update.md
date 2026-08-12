# Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023

Bob Ruililin Shen^1^, Author 2^1^, Author 3^1^, Author 4^1^, David Makram Bishai^1^

^1^ School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong, Hong Kong SAR, China

*Author order after the first and last positions remains to be confirmed with the supervising investigator. Scientific roles are recorded in the Acknowledgements.*

## Abstract

**Background.** Hong Kong now records more hot nights and very hot days than a decade ago, while cold days continue. Local daily studies of cardiac admissions emphasised cold. Whether that pattern describes contemporary monthly first-hospitalisation counts among people with diabetes or hypertension is a different question.

**Methods.** We analysed 132 territory-months (January 2013–December 2023) of governed counts of the first recorded hospitalisation after a first coronary heart disease (CHD) or heart failure (HF) diagnosis among people diagnosed with type 2 diabetes and/or hypertension (156,156 CHD events; 29,681 HF events). Admission cause was not recorded. Exposures were monthly mean temperature, mean daily maximum and minimum temperature, and official extreme-day counts (hot nights, very hot days, cold days). Separate negative-binomial models included calendar-month indicators and a natural cubic spline of time (4 df), with a days-in-month offset. Uncertainty was reported as a Model / HC1 / Newey–West lag-3 / Newey–West lag-6 ladder. Benjamini–Hochberg *q*-values covered the twelve core contrasts. The model set was specified after the outcome series were available and is exploratory. A method that attempts to recover daily exposure coefficients from monthly sums was tested in simulation and not applied to the health series.

**Results.** Continuity Newey–West lag-6 count ratios included CHD hot nights per five days 1.022 (1.002–1.042) and HF cold days per five days 1.073 (1.006–1.144); both had *q* = 0.192. All twelve core *q*-values exceeded 0.19. For CHD hot nights, Model and HC1 intervals included 1; Newey–West intervals excluded 1 on the unrounded scale. For HF cold days, all four interval constructions excluded 1. CHD Pearson residual autocorrelation at lag 1 was 0.51–0.53; HF 0.13–0.18.

**Conclusions.** The data do not support a multiplicity-protected differential thermal claim. The HF cold-day association is concordant across standard-error methods but unprotected by *q*-values. The CHD hot-night association is sensitive to how uncertainty is computed. Estimates are ecological monthly count ratios under a first-event construction without recorded admission cause.

**Keywords:** hot nights; cold days; coronary heart disease; heart failure; Hong Kong; monthly time series

## Introduction

Temperature-related cardiovascular morbidity remains a concern in subtropical cities, where intense humid heat coexists with episodic cold [9,10]. Hong Kong is a dense, ageing city in which hot nights and very hot days have become more frequent while cold days have not disappeared [2,4].

Earlier Hong Kong evidence emphasised cold-related cardiac risk. Using daily data from 2000–2009, Goggins et al. reported that decreases in temperature below an estimated 24 °C threshold were associated with increased acute myocardial infarction (AMI) admissions, while no statistically significant heat effect was observed [1]. The same study identified nitrogen dioxide as an important predictor of AMI admissions. A related daily analysis of stroke admissions during 1999–2006 likewise found stronger cold than heat associations [11]. Those studies establish the local historical pattern. They do not estimate monthly first-hospitalisation counts under a later data contract.

Hong Kong’s thermal environment has changed since those study periods. At the Hong Kong Observatory (HKO), hot nights increased from 10 in 2013 to 61 in 2021, and very hot days from 17 to 54 in the same selected-year comparison [2,4]. Cold days continued to occur (14 in 2013, 13 in 2021, and 14 in 2023). Contemporary analysis therefore has to keep heat and cold in view together.

Air pollution also changed during the present study window. At general monitoring stations, mean nitrogen dioxide declined from 53.7 µg m^−3^ in 2013 to 32.1 µg m^−3^ in 2023, fine particulate matter (PM2.5) from 30.8 to 14.6 µg m^−3^, and ozone rose from 42.6 to 58.3 µg m^−3^ [7]. Temperature and pollutants are not interchangeable covariates. Ozone in particular may confound or lie on the pathway of hot, sunny conditions, so pollution adjustment, when used, is staged rather than screened for attenuation.

Daily mortality studies in Hong Kong answer a further, distinct question. Liu et al. (2020) reported a cold-dominant attributable fraction for cause-specific mortality during 2006–2016 (cold 4.72% versus heat 0.16%), with moderate non-optimum temperatures accounting for more burden than extremes [12]. Liu et al. (2026) estimated heatwave-related excess deaths under several local definitions for 2014–2023 [13]. Attributable fractions and modelled excess deaths are not monthly morbidity count ratios.

This study estimates the association between specified monthly thermal-exposure contrasts and monthly counts of first hospitalisation after first CHD diagnosis, and after first HF diagnosis, among people with type 2 diabetes and/or hypertension in Hong Kong from January 2013 through December 2023, keeping heat and cold in parallel and reporting definition and uncertainty discordance rather than a single protected claim.

## Methods

### Study design

The design is an ecological territory-month time series covering January 2013 through December 2023 (132 months). For each separate single-exposure model, the target quantity is a count ratio associated with a 1 °C or five-day exposure contrast, conditional on calendar month and a smooth function of time. Individual causal effects, principal-diagnosis CHD or HF, AMI, and daily triggering are not identified [14]. Because the diabetes or hypertension cohort still at risk of a first event was unavailable, the analysis-of-record offset is days in month. Estimates are therefore monthly count ratios, not cohort incidence-rate ratios [14]. The twelve-contrast model set was specified after the outcome series were available and is exploratory.

### Health data

Governed monthly aggregates were constructed and released by the outcome co-investigator. The cohort comprised people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each outcome, the event was the first recorded hospitalisation after the patient’s first diagnosis record for CHD or HF. Diagnosis-record construction was assisted by a clinical collaborator. Admission cause was not recorded. Delivered columns were labelled `chd_inpatient` and `hf_inpatient` at territory × calendar month grain. Inpatient-only semantics are inferred from those labels and remain subject to confirmation. Age–sex strata were not included. A stroke series was named in correspondence but was not attached; no stroke analysis is reported. Field-level ICD lists and the executable timing rule remain with the outcome co-investigator and should replace this paragraph where they differ from it.

### Weather and pollutants data

Meteorological data was obtained from the HKO. The variables included: daily temperature (mean, minimum, maximum), daily relative humidity, daily total rainfall, the number of hot nights (T~min~ ≥ 28°C), the number of very hot days (T~max~ ≥ 33°C), the number of extremely hot days (T~max~ ≥ 35°C), and the number of cold days (T~min~ ≤ 12°C). Daily mean pollutant levels for nitrogen dioxide (NO~2~), sulfur dioxide (SO~2~), and ozone (O~3~) were obtained from the Hong Kong Environmental Protection Department (EPD).

Daily Headquarters series were aggregated to calendar months for analysis. Continuity exposures were monthly mean temperature, the monthly means of daily maximum and minimum temperature, and official counts of hot nights, very hot days, and cold days, the last three scaled per five days so that coefficients correspond to a five-day contrast rather than a single extreme day. Official cold days were concentrated in December–February (141 of 145 days across 2013–2023; four days fell in March). With calendar-month indicators in the model, remaining cold-day variation is between-year differences within winter months. A winter-only restriction is a labelled sensitivity, not a remedy for that identification. Extremely hot days, relative humidity, rainfall, and sulfur dioxide were assembled with the weather series but were not entered in the twelve-contrast continuity panel. Fine particulate matter (PM2.5) from general EPD stations was assembled for staged pollution sensitivities. A station-month contributed to a pollutant mean only when at least 75% of expected observations were available; missing measurements were not coded as zero. Territory-wide monthly concentrations were unweighted means across eligible general stations. Roadside stations were reserved. Nitrogen dioxide and particulate matter were specified to enter before ozone, because ozone is coupled with hot, sunny conditions. Staged pollution models exist in the archive; they are not adjusted versions of the separate continuity panel and were not used to claim that confounding is resolved. Operational heatwave-spell and hot-month rules beyond the official daily thresholds remain with the weather co-investigator; provisional monthly-tail indicators were not used as confirmatory exposures.

### Influenza

Monthly influenza activity was obtained from Centre for Health Protection Flu Express summaries. Coverage was 121 of 132 months, with the gap in early 2013. Missing influenza months were left missing and were never coded as zero. Influenza was not entered in the twelve-contrast continuity panel.

### Population denominators and offsets

Age- and sex-specific mid-year population estimates from the Census and Statistics Department (Table 110-01001) were linearly interpolated to calendar-month midpoints [8]. Those denominators describe the general population, not the diabetes or hypertension cohort still at risk of a first CHD or HF hospitalisation. Continuity models therefore used a days-in-month offset, \(\log(d_t)\), and are interpreted as monthly count ratios [14]. A general-population × days offset was retained only as a sensitivity. It does not convert the estimand into cohort incidence.

### Statistical analysis

Let \(Y_t\) be the monthly count in month \(t\). Continuity models used a negative-binomial likelihood [10],

\[
\log \mathrm{E}(Y_t) = \log(d_t) + \alpha + \beta X_t + \sum_{m=2}^{12} \gamma_m I(\mathrm{month}_t = m) + s(t; 4~\mathrm{df}),
\]

where \(d_t\) is days in month, \(X_t\) is a single exposure, and \(s(t; 4~\mathrm{df})\) is a natural cubic spline of month index. Each continuity model entered one exposure at a time: mean temperature, mean maximum temperature, mean minimum temperature, hot nights, cold days, or very hot days, for CHD and for HF (twelve contrasts). Quasi-Poisson models were a family sensitivity. Negative binomial was preferred because monthly counts were overdispersed relative to Poisson.

Continuity intervals used Newey–West standard errors with lag 6 [19], reported together with model-based, HC1, and Newey–West lag-3 intervals. Lag 6 was the continuity reporting choice because residual serial dependence is expected in monthly counts and is material for CHD. No interval was selected because it excluded 1.

Joint models that entered maximum and minimum temperature together, or the three official extreme-day counts together, were retained as collinearity diagnostics. Variance inflation factors were computed after residualising on calendar month and the trend spline.

Robustness analyses comprised alternative trend smooths (3, 6, and 8 df), year fixed effects, exclusion of the first 12 or 24 months, a pre-2020 window (January 2013–December 2019; 84 months), COVID-phase adjustment, lag-0/1/2 month exposures, and exclusion of the month with largest Cook’s distance. COVID phases were pre-COVID (through January 2020), early COVID (February 2020–December 2021), fifth wave (January–April 2022), late 2022 (May–December 2022), and post-reopening (from January 2023). Pearson residual autocorrelation and Ljung–Box tests at lags 6 and 12 were inspected. Benjamini–Hochberg *q*-values were computed across the twelve continuity contrasts [20].

Archive models that entered pollution, humidity, or influenza are not adjusted versions of the separate continuity panel. They were not used to claim that confounding is resolved.

### Constrained daily-exposure recovery

A constrained method for recovering daily exposure coefficients from monthly sums was evaluated in simulation against Hong Kong weather, following the Basagaña–Ballester aggregation framework [15,16]. Implementation was from the published estimating equation. Public code without a repository licence was not copied. Synthetic daily outcomes were matched to disclosure-minimised seasonality, scale, overdispersion, and residual dependence of the monthly series. Admission of any real daily coefficient required all frozen calibration gates to pass, including Type I error, coverage, relative bias, and sign recovery. A 500-replicate calibration against Hong Kong weather failed those requirements. A subsequent worst-cell re-summary of the same fits did not reverse that decision. No daily health coefficient was produced. This is a project-specific calibration result. It does not show that the Basagaña–Ballester method fails in general. A full daily distributed-lag non-linear model is not identified from 132 monthly sums.

### Software

Analyses were conducted in R 4.3.3 (2024-02-29). Negative-binomial models used `MASS::glm.nb` (MASS 7.3-60.0.1). Newey–West and HC1 standard errors used `sandwich` 3.1.3. Natural cubic splines used `splines::ns`.

### Ethics and governance

Analyses used governed Hospital Authority monthly aggregates supplied under existing collaborative arrangements. Source monthly counts and merged panels are not redistributed. Aggregation reduces re-identification risk but does not grant external-publication authority. Written confirmation from the outcome and supervising investigators remains required before journal submission. Whether the institutional review protocol requires amendment for this work remains a decision for the supervising investigator.

## Results

### Outcome series

CHD contributed 156,156 first recorded hospitalisations over 132 months (mean 1,183.0 per month). HF contributed 29,681 (mean 224.9 per month) (Table 1). Annual totals declined by about half from 2013 to 2023 (CHD 23,830 to 12,323; HF 4,336 to 2,296), with a further dip in 2020 (CHD 10,237; HF 1,964). That shape is expected under a first-event construction in a 2013–2023 diagnosis window, together with pandemic changes in care-seeking. Mean monthly HF counts were highest in January (287) and lowest in September (196); CHD showed a milder winter elevation (January 1,386; September 1,097). After calendar-month indicators, remaining thermal estimates ask whether a given January or July differs from a typical January or July, not whether winter counts exceed summer counts.

**Table 1. Outcome summary.**

| Outcome | Period | Months | Total events | Mean per month | Event construction |
|:--|:--|---:|---:|---:|:--|
| Coronary heart disease | 2013–2023 | 132 | 156,156 | 1,183.0 | First recorded hospitalisation after first CHD diagnosis |
| Heart failure | 2013–2023 | 132 | 29,681 | 224.9 | First recorded hospitalisation after first HF diagnosis |

### Exposure context

At HKO Headquarters, hot nights rose from 10 in 2013 to 61 in 2021 and 56 in 2023. Very hot days rose from 17 to 54 over the same 2013–2021 comparison and were 54 in 2023. Cold days were 14 in 2013 and 14 in 2023 (1 in 2019; 13 in 2021). These are exposure counts, not health effects.

### Continuity panel

Table 2 reports the twelve separate-exposure count ratios under the days-in-month offset and Newey–West lag-6 intervals.

**Table 2. Separate negative-binomial models with days-in-month offset and Newey–West lag-6 intervals.**

| Outcome | Exposure contrast | Count ratio (95% CI) | *p* | BH *q* |
|:--|:--|--:|--:|--:|
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

All twelve *q*-values exceeded 0.19. No contrast meets a multiplicity-protected confirmatory threshold in this exploratory panel. The HF mean-minimum-temperature interval included 1 at the fourth decimal place (unrounded upper bound 1.00005).

For CHD, continuous monthly temperatures were near null (0.993–0.994), whereas the official hot-night count association was larger under Newey–West lag-6 reporting. These encodings describe different monthly thermal questions; the contrast does not imply that a causal hot-night effect was missed by the means. For HF, continuous temperature associations were weakly inverse and the cold-day count association was positive.

### Uncertainty ladder

**Table 3. Uncertainty ladder for the two leading exploratory contrasts.**

| Outcome and exposure | Model | HC1 | NW3 | NW6 |
|:--|:--|:--|:--|:--|
| CHD hot nights / 5 days | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.0003–1.0439) | 1.022 (1.002–1.042) |
| HF cold days / 5 days | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

For CHD hot nights, Model and HC1 intervals included 1; NW3 and NW6 excluded 1 on the unrounded scale (NW3 1.000253–1.043860). For HF cold days, all four constructions excluded 1, but *q* remained 0.192. Concordance across standard-error methods does not create multiplicity protection.

### Joint models, residuals, and robustness

After month and trend residualisation, maximum and minimum temperature retained a variance inflation factor of 4.66 when entered jointly. Hot nights and very hot days retained variance inflation factors near 1.96. In the joint extreme-day model, the CHD hot-night count ratio rose to 1.045 (1.015–1.075) from 1.022 in the separate model. The HF cold-day coefficient was similar in joint and separate models (1.073). Joint coefficients are diagnostics, not preferred estimates.

Pearson residual autocorrelation at lag 1 was 0.51–0.53 for CHD continuity models and 0.13–0.18 for HF. For the two leading contrasts it was 0.508 (CHD hot nights) and 0.146 (HF cold days). Ljung–Box tests at lag 6 rejected residual white noise for CHD (*p* < 10^−8^) and not for HF (*p* > 0.3). Serial dependence is part of the inferential problem for CHD. It is why Newey–West intervals are shown rather than model-based intervals alone.

Offset choice changed continuity count ratios only trivially. Across trend and early-period specifications, the CHD hot-night ratio ranged from 1.011 to 1.025 and the HF cold-day ratio from 1.043 to 1.113. The HF cold-day association was stronger before 2020 (1.113, 1.053–1.176). Lag-1 month models attenuated the CHD hot-night association toward 1 (1.010, 0.979–1.042). The HF cold-day association remained elevated at lag 1 (1.073, 1.014–1.135) and was weaker at lag 2 (1.053, 0.985–1.127). Lag-one month is a labelled sensitivity; it is not a daily lag curve. The months with largest Cook’s distance were February 2020 (CHD) and February 2022 (HF cold days). Excluding the worst month left both exploratory directions unchanged (CHD hot nights 1.021, 1.001–1.040; HF cold days 1.088, 1.034–1.144).

The simulated daily-recovery method failed its worst-cell gates (null Type I error 0.048–0.150; minimum coverage 0.840; maximum non-null relative bias 32.8; maximum moderate false-sign rate 0.808). No real daily coefficient is reported. That refusal is specific to this monthly series and this implementation.

## Discussion

The current data do not support a protected differential thermal claim for CHD versus HF. Under continuity Newey–West lag-6 reporting, CHD first-hospitalisation counts were more closely associated with official hot-night burden than with mean temperature or cold days, and HF counts were more closely associated with cold-day burden than with hot nights. Those patterns sit inside multiplicity adjustment that leaves all twelve *q*-values above 0.19. The HF cold-day association is the more coherent residual signal: it is concordant across standard-error methods, survives exclusion of the most influential pandemic month, and is not an artefact of entering correlated heat metrics jointly. It remains *q*-unprotected. Because official cold days fall almost entirely in December–February, that residual is a between-year winter contrast, not a summer-versus-winter contrast. The CHD hot-night association is smaller and depends on the uncertainty method.

That partition is consistent with local historical emphasis on cold for cardiac admissions [1] and with later concern about nighttime heat [17]. It is not a causal allocation of heat and cold pathways. Goggins et al. analysed daily AMI admissions with a temperature threshold and pollution covariates [1]. The present series is monthly, first-event, without admission cause, and without a still-at-risk cohort denominator. Agreement in direction with a cold-HF residual is therefore a bounded comparison, not a replication.

Liu et al. (2020, 2026) remain complementary mortality baselines [12,13]. Their attributable fractions and excess-death totals cannot be rescaled into the present count ratios. The failed daily-recovery calibration is the corresponding methods limit: monthly sums do not automatically yield daily trigger estimates [15,16].

Pollution and influenza are scientifically motivated in this setting [1,18]. Archive models in which they enter are not continuity-adjusted thermal estimates. On the 121 months with influenza data, an archive model that entered a flu indicator associated influenza with higher CHD counts (1.673, 1.249–2.243). That coefficient is not an adjusted version of Table 2. Confounding by infection, ozone, or nitrogen dioxide is therefore not resolved. Absent cohort person-time, even a stable count ratio remains a count ratio.

A protected primary claim would have required a predeclared confirmatory contrast, multiplicity control that survives the twelve-contrast family, uncertainty constructions that are not chosen for null exclusion, and residual diagnostics that do not leave substantial CHD serial correlation unaddressed. This release does not meet that bar. We report the complete panel and the refusals.

## Conclusion

Between 2013 and 2023, Hong Kong experienced a large increase in hot nights while cold days persisted. In governed monthly data for people with diabetes and/or hypertension, CHD first-hospitalisation counts were most elevated in relation to hot nights, and HF counts in relation to cold days. Neither pattern survived correction across twelve comparisons, and the CHD result was sensitive to the treatment of uncertainty. The study therefore offers hypotheses and an aggregation-aware reporting standard, not proof of thermal effects on disease-caused admission.

## Strengths and limitations

Strengths include a complete twelve-contrast panel, an explicit standard-error ladder, source-documented official extreme-day thresholds, and a refused daily-recovery analysis.

Limitations. Admission cause was not recorded. Inpatient-only semantics remain unconfirmed. Cohort person-time still at risk of a first event was unavailable. The analysis is ecological and monthly [14]. Age, sex, and subtype strata were not delivered. CHD residual serial correlation remains material. Official cold-day counts are winter-concentrated, so the HF cold-day residual is identified from between-year winter differences. Weather hot-month and cold-month reference rules remain unlocked. Pollution, humidity, and influenza confounding is unresolved in the continuity panel. External dissemination of the governed aggregates still requires confirmation from the outcome and supervising investigators.

## Declaration on the use of AI

AI-assisted tools were used for code scaffolding, methodological brainstorming, and review of potential data and modelling issues. Scientific claims, numerical results, and collaborator-owned Methods text were checked against governed outputs and the live weather paragraph.

## Declaration of competing interest

The authors declare no competing interests.

## Acknowledgements

We thank the weather co-investigator for the live weather Methods, thermal-definition guidance, and comments on the Introduction; Zhenyuan Liu for constructing and releasing the governed Hospital Authority aggregates and for regression mentorship; Professor David Bishai for supervision; and Dr Jingjing Zhou for assistance with diagnosis-record construction. Author order and any co-first designation remain to be confirmed.

## Data and code availability

A disclosure-minimised release of tables, figures, and machine-readable checks accompanies the analysis. Source monthly health counts and merged panels are governed and are not redistributed. External submission requires team confirmation.

## References

1. Goggins WB, Chan EYY, Yang CY. Weather, pollution, and acute myocardial infarction in Hong Kong and Taiwan. *Int J Cardiol*. 2013;168(1):243-249. doi:10.1016/j.ijcard.2012.09.087
2. Hong Kong Observatory. The Year's Weather — 2013. https://www.hko.gov.hk/en/wxinfo/pastwx/ywx2013.htm
3. Hong Kong Observatory. The Year's Weather — 2017. https://www.hko.gov.hk/en/wxinfo/pastwx/2017/ywx2017.htm
4. Hong Kong Observatory. The Year's Weather — 2021. https://www.hko.gov.hk/en/wxinfo/pastwx/2021/ywx2021.htm
5. Hong Kong Observatory. The Year's Weather — 2024. https://www.hko.gov.hk/en/wxinfo/pastwx/2024/ywx2024.htm
6. Hong Kong Observatory. Hong Kong Observatory Open Data. https://www.hko.gov.hk/en/abouthko/opendata_intro.htm
7. Environmental Protection Department. Environmental Protection Interactive Centre: Air Quality Data. https://cd.epic.epd.gov.hk/EPICDI/air/station/?lang=en
8. Census and Statistics Department. Population by Sex and Age Group (Table 110-01001). https://data.gov.hk/en-data/dataset/hk-censtatd-tablechart-110-01001
9. Ye X, Wolff R, Yu W, Vaneckova P, Pan X, Tong S. Ambient temperature and morbidity: a review of epidemiological evidence. *Environ Health Perspect*. 2012;120(1):19-28. doi:10.1289/ehp.1003198
10. Bhaskaran K, Gasparrini A, Hajat S, Smeeth L, Armstrong B. Time series regression studies in environmental epidemiology. *Int J Epidemiol*. 2013;42(4):1187-1195. doi:10.1093/ije/dyt092
11. Goggins WB, Woo J, Ho S, Chan EYY, Chau PH. Weather, season, and daily stroke admissions in Hong Kong. *Int J Biometeorol*. 2012;56(5):865-872. doi:10.1007/s00484-011-0491-9
12. Liu J, Hansen A, Varghese B, et al. Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016. *Sustain Cities Soc*. 2020;57:102131. doi:10.1016/j.scs.2020.102131
13. Liu Z, Ren C, Liu J, Kawasaki Y, Bishai DM. Modelling the excess mortality associated with heat waves in Hong Kong: 2014–2023. medRxiv. 2026. doi:10.64898/2026.03.05.26347683
14. Greenland S, Morgenstern H. Ecological bias, confounding, and effect modification. *Int J Epidemiol*. 1989;18(1):269-274. doi:10.1093/ije/18.1.269
15. Basagaña X, Ballester J. Unbiased temperature-related mortality estimates using weekly and monthly health data: a new method for environmental epidemiology and climate impact studies. *Lancet Planet Health*. 2024;8(10):e766-e777. doi:10.1016/S2542-5196(24)00212-2
16. Basagaña X, Ballester J. Unbiased estimates using temporally aggregated outcome data in time series analysis: generalization to different outcomes, exposures, and types of aggregation. *Epidemiology*. 2026;37(1):16-20. doi:10.1097/EDE.0000000000001923
17. Guo YT, Chan KH, Qiu H, Wong ELY, Ho KF. The risk of hospitalization associated with hot nights and excess nighttime heat in a subtropical metropolis: a time-series study in Hong Kong, 2000–2019. *Lancet Reg Health West Pac*. 2024;51:101168. doi:10.1016/j.lanwpc.2024.101168
18. Yang Z, Wei Y, Jiang X, et al. Association of cold weather and influenza infection with stroke: a 22-year time-series analysis. *Int J Biometeorol*. 2025;69(5):963-973. doi:10.1007/s00484-025-02870-2
19. Newey WK, West KD. A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*. 1987;55(3):703-708. doi:10.2307/1913610
20. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J R Stat Soc Series B*. 1995;57(1):289-300. doi:10.1111/j.2517-6161.1995.tb02031.x
