# Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023

Bob Ruililin Shen^1^, Author 2^1^, Author 3^1^, Author 4^1^, David Makram Bishai^1^

^1^ School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong, Hong Kong SAR, China

*Author order after the first and last positions remains to be confirmed with the supervising investigator. Scientific roles are recorded in the Acknowledgements.*

## Abstract

**Background.** Hong Kong records more hot nights and very hot days than it did a decade ago, and cold days have not disappeared. Earlier local studies of daily cardiac admissions emphasised cold. Whether that pattern also describes recent monthly counts of first hospitalisation among people with diabetes or hypertension is a separate question.

**Methods.** We analysed 132 territory-months (January 2013–December 2023) of governed monthly aggregate counts of the first recorded hospitalisation after a first diagnosis of coronary heart disease (CHD) or heart failure (HF) among people diagnosed with type 2 diabetes and/or hypertension (156,156 CHD events; 29,681 HF events). Admission cause was not recorded. Exposures were monthly mean temperature, the monthly means of daily maximum and minimum temperature, and official counts of hot nights, very hot days, and cold days. Each exposure entered a separate negative-binomial model with calendar-month indicators, a natural cubic spline of time (4 df), and a days-in-month offset. Intervals were reported as a ladder of model-based, HC1, Newey–West lag-3, and Newey–West lag-6 constructions. Benjamini–Hochberg *q*-values covered the twelve core contrasts. The model set was specified after the outcome series were available and is exploratory. A method for recovering daily exposure coefficients from monthly sums was tested in simulation and was not applied to the health series.

**Results.** Under Newey–West lag-6 reporting, the count ratio was 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF. Both had *q* = 0.192, and all twelve core *q*-values exceeded 0.19. For CHD hot nights, model-based and HC1 intervals included 1, while both Newey–West intervals excluded 1 on the unrounded scale. For HF cold days, all four interval constructions excluded 1. Official cold days fell almost entirely in December–February (141 of 145 days), so the cold-day contrast is identified from differences between winters. Pearson residual autocorrelation at lag 1 was 0.508 for the CHD hot-night model and 0.146 for the HF cold-day model.

**Conclusions.** The data do not support a multiplicity-protected differential thermal claim. The HF cold-day association is concordant across standard-error methods but is not protected by its *q*-value. The CHD hot-night association depends on how uncertainty is computed. All estimates are ecological monthly count ratios for a first-event outcome without recorded admission cause.

**Keywords:** hot nights; cold days; coronary heart disease; heart failure; Hong Kong; monthly time series

## Introduction

Temperature-related cardiovascular morbidity remains a concern in subtropical cities, where intense humid heat coexists with episodic cold [9]. Hong Kong is a dense, ageing city whose thermal profile has shifted within a single decade. At the Hong Kong Observatory (HKO), hot nights increased from 10 in 2013 to 61 in 2021, and very hot days from 17 to 54 in the same comparison [2,4]. Cold days persisted across the period (14 in 2013, 13 in 2021, and 14 in 2023) [2,4,6]. A contemporary local analysis therefore has to hold heat and cold in one design.

Local evidence on cardiac admissions is daily, diagnosis-specific, and drawn from earlier decades. Using data from 2000–2009, Goggins et al. reported that a 1 °C decrease below an estimated 24 °C threshold was associated with a 3.7% increase in acute myocardial infarction admissions, and found no statistically significant heat association in Hong Kong, Taipei, or Kaohsiung [1]. Same-day nitrogen dioxide was the strongest pollutant predictor in that study [1]. An analysis of public-hospital stroke admissions during 1999–2006 found an inverse association of haemorrhagic stroke with temperature and a weaker ischaemic-stroke association below about 22 °C [11]. Closest to the present outcomes, Goggins and Chan analysed daily public-hospital heart-failure admissions and deaths during 2002–2011 and reported a cumulative relative risk of 2.63 (2.43–2.84) for admissions comparing 11 °C with 25 °C over lags extending to 23 days [21]. These studies fix the local historical pattern. They estimate daily risk for cause-coded admissions, so their coefficients do not transfer to monthly counts of first hospitalisation.

Nighttime heat can be encoded in more than one way. Guo et al. analysed daily unplanned emergency hospitalisations in Hong Kong during the hot seasons of 2000–2019 [17]. After adjustment for multi-day mean temperature, the official hot-night indicator (minimum temperature ≥ 28 °C) showed no overall association with non-cancer, non-external hospitalisation over lags 0–4 days (excess relative risk −0.2%, 95% CI −1.2% to 0.7%) [17]. An hourly excess-heat metric for 20:00–07:59 was associated with higher hospitalisation, including a 3.1% (1.5–4.8%) increase at its extreme value [17]. Official monthly counts of hot nights are, by construction, a coarser encoding than nighttime intensity. They remain an interpretable public climatological series, and they are not a test of the hourly metric. Guo et al. did not study first CHD or HF hospitalisation in a diabetes or hypertension cohort [17].

Air pollution also changed during the present study window. At general monitoring stations, mean nitrogen dioxide declined from 53.7 µg m^−3^ in 2013 to 32.1 µg m^−3^ in 2023, and fine particulate matter (PM2.5) from 30.8 to 14.6 µg m^−3^, while ozone rose from 42.6 to 58.3 µg m^−3^ [7]. Temperature and pollutants are not interchangeable covariates. Ozone is coupled with hot, sunny conditions and may confound the thermal association or lie on its pathway.

Daily mortality studies in Hong Kong answer a further, distinct question. Liu et al. (2020) reported a cold-dominant attributable fraction for cause-specific mortality during 2006–2016 (4.72% for cold versus 0.16% for heat), and a larger fraction for moderate non-optimum temperatures than for extremes (4.25% versus 0.63%) [12]. Liu et al. (2026) estimated 1,455 to 3,238 model-based excess heat deaths for 2014–2023, the range reflecting which local heatwave definition was applied [13]. Attributable fractions and modelled excess deaths are mortality burden quantities. They cannot be rescaled into monthly morbidity count ratios.

This study estimates the association between specified monthly thermal-exposure contrasts and monthly counts of first hospitalisation after first CHD diagnosis, and after first HF diagnosis, among people with type 2 diabetes and/or hypertension in Hong Kong from January 2013 through December 2023. Heat and cold exposures are carried in parallel, and discordance between definitions and between uncertainty constructions is reported in place of a single protected claim.

## Methods

### Study design

The design is an ecological territory-month time series covering January 2013 through December 2023 (132 months). For each separate single-exposure model, the target quantity is a count ratio associated with a 1 °C or five-day exposure contrast, conditional on calendar month and a smooth function of time. Individual causal effects, principal-diagnosis CHD or HF, AMI, and daily triggering are not identified [14]. Because the diabetes or hypertension cohort still at risk of a first event was unavailable, the analysis-of-record offset is days in month. Estimates are therefore monthly count ratios, not cohort incidence-rate ratios [14]. The twelve-contrast model set was specified after the outcome series were available and is exploratory. We refer to the twelve separate single-exposure models as the core panel.

### Health data

Governed monthly aggregates were constructed and released by the outcome co-investigator. The cohort comprised people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each outcome, the event was the first recorded hospitalisation after the patient’s first diagnosis record for CHD or HF. Diagnosis-record construction was assisted by a clinical collaborator. Admission cause was not recorded. Delivered columns were labelled `chd_inpatient` and `hf_inpatient` at territory × calendar month grain. Inpatient-only semantics are inferred from those labels and remain subject to confirmation. Age–sex strata were not included. A stroke series was named in correspondence but was not attached; no stroke analysis is reported. Field-level ICD lists and the executable timing rule remain with the outcome co-investigator and should replace this paragraph where they differ from it.

### Weather and pollutants data

Meteorological data was obtained from the HKO. The variables included: daily temperature (mean, minimum, maximum), daily relative humidity, daily total rainfall, the number of hot nights (T~min~ ≥ 28°C), the number of very hot days (T~max~ ≥ 33°C), the number of extremely hot days (T~max~ ≥ 35°C), and the number of cold days (T~min~ ≤ 12°C). Daily mean pollutant levels for nitrogen dioxide (NO~2~), sulfur dioxide (SO~2~), and ozone (O~3~) were obtained from the Hong Kong Environmental Protection Department (EPD).

Daily Headquarters series were aggregated to calendar months for analysis. Core exposures were monthly mean temperature, the monthly means of daily maximum and minimum temperature, and official counts of hot nights, very hot days, and cold days, the last three scaled per five days so that coefficients correspond to a five-day contrast rather than a single extreme day. Official cold days were concentrated in December–February (141 of 145 days across 2013–2023; four days fell in March). With calendar-month indicators in the model, remaining cold-day variation is between-year differences within winter months. A winter-only restriction is a labelled sensitivity, not a remedy for that identification. Extremely hot days, relative humidity, rainfall, and sulfur dioxide were assembled with the weather series but were not entered in the twelve-contrast core panel. Fine particulate matter (PM2.5) from general EPD stations was assembled for staged pollution sensitivities. A station-month contributed to a pollutant mean only when at least 75% of expected observations were available; missing measurements were not coded as zero. Territory-wide monthly concentrations were unweighted means across eligible general stations. Roadside stations were reserved. Nitrogen dioxide and particulate matter were specified to enter before ozone, because ozone is coupled with hot, sunny conditions. Staged pollution models exist in the archive; they are not adjusted versions of the separate core panel and were not used to claim that confounding is resolved. Operational heatwave-spell and hot-month rules beyond the official daily thresholds remain with the weather co-investigator; provisional monthly-tail indicators were not used as confirmatory exposures.

### Influenza

Monthly influenza activity was obtained from Centre for Health Protection Flu Express summaries. Coverage was 121 of 132 months, with the gap in early 2013. Missing influenza months were left missing and were never coded as zero. Influenza was not entered in the twelve-contrast core panel.

### Population denominators and offsets

Age- and sex-specific mid-year population estimates from the Census and Statistics Department (Table 110-01001) were linearly interpolated to calendar-month midpoints [8]. Those denominators describe the general population, not the diabetes or hypertension cohort still at risk of a first CHD or HF hospitalisation. Core models therefore used a days-in-month offset, \(\log(d_t)\), and are interpreted as monthly count ratios [14]. A general-population × days offset was retained only as a sensitivity. It does not convert the estimand into cohort incidence.

### Statistical analysis

Let \(Y_t\) be the monthly count in month \(t\). Core models used a negative-binomial likelihood [10],

\[
\log \mathrm{E}(Y_t) = \log(d_t) + \alpha + \beta X_t + \sum_{m=2}^{12} \gamma_m I(\mathrm{month}_t = m) + s(t; 4~\mathrm{df}),
\]

where \(d_t\) is days in month, \(X_t\) is a single exposure, and \(s(t; 4~\mathrm{df})\) is a natural cubic spline of month index. Each core model entered one exposure at a time: mean temperature, mean maximum temperature, mean minimum temperature, hot nights, cold days, or very hot days, for CHD and for HF (twelve contrasts). Quasi-Poisson models were a family sensitivity. Negative binomial was preferred because monthly counts were overdispersed relative to Poisson.

Core intervals used Newey–West standard errors with lag 6 [19], reported together with model-based, HC1, and Newey–West lag-3 intervals. Lag 6 was the core reporting choice because residual serial dependence is expected in monthly counts and is material for CHD. Robust intervals are not automatically wider than model-based intervals; the four-construction ladder is reported for that reason. No interval was selected because it excluded 1.

Joint models that entered maximum and minimum temperature together, or the three official extreme-day counts together, were retained as collinearity diagnostics. Variance inflation factors were computed after residualising on calendar month and the trend spline.

Robustness analyses comprised alternative trend smooths (3, 6, and 8 df), year fixed effects, exclusion of the first 12 or 24 months, a pre-2020 window (January 2013–December 2019; 84 months), COVID-phase adjustment, lag-0/1/2 month exposures, and exclusion of the month with largest Cook’s distance. COVID phases were pre-COVID (through January 2020), early COVID (February 2020–December 2021), fifth wave (January–April 2022), late 2022 (May–December 2022), and post-reopening (from January 2023). Pearson residual autocorrelation and Ljung–Box tests at lags 6 and 12 were inspected. Benjamini–Hochberg *q*-values were computed across the twelve core contrasts [20].

Archive models that entered pollution, humidity, or influenza are not adjusted versions of the separate core panel. They were not used to claim that confounding is resolved.

### Constrained daily-exposure recovery

A constrained method for recovering daily exposure coefficients from monthly sums was evaluated in simulation against Hong Kong weather, following the Basagaña–Ballester aggregation framework [15,16]. Implementation was from the published estimating equation. Public code without a repository licence was not copied. Synthetic daily outcomes were matched to disclosure-minimised seasonality, scale, overdispersion, and residual dependence of the monthly series. Admission of any real daily coefficient required all frozen calibration gates to pass, including Type I error, coverage, relative bias, and sign recovery. A 500-replicate calibration against Hong Kong weather failed those requirements. A subsequent worst-cell re-summary of the same fits did not reverse that decision. No daily health coefficient was produced. This is a project-specific calibration result. It does not show that the Basagaña–Ballester method fails in general. A full daily distributed-lag non-linear model is not identified from 132 monthly sums.

### Software

Analyses were conducted in R 4.3.3 (2024-02-29). Negative-binomial models used `MASS::glm.nb` (MASS 7.3-60.0.1). Newey–West and HC1 standard errors used `sandwich` 3.1.3. Natural cubic splines used `splines::ns`.

### Ethics and governance

Analyses used governed Hospital Authority monthly aggregates supplied under existing collaborative arrangements. Source monthly counts and merged panels are not redistributed. Aggregation reduces re-identification risk but does not grant external-publication authority. Written confirmation from the outcome and supervising investigators remains required before journal submission. Whether the institutional review protocol requires amendment for this work remains a decision for the supervising investigator.

## Results

### Outcome series

CHD contributed 156,156 first recorded hospitalisations over 132 months (mean 1,183.0 per month). HF contributed 29,681 (mean 224.9 per month) (Table 1). Annual totals declined by about half from 2013 to 2023 (CHD 23,830 to 12,323; HF 4,336 to 2,296), with a further dip in 2020 (CHD 10,237; HF 1,964). Over the same years the interpolated Census and Statistics Department population aged 35 years or older rose by 17%. Figure 1 indexes those series to 2013. The decline in first-event counts is compatible with risk-set depletion in a 2013–2023 diagnosis window, together with pandemic changes in care-seeking. It is not a measure of falling incidence in the territory, and it does not quantify the share of depletion without monthly still-at-risk person-time. Mean monthly HF counts were highest in January (287) and lowest in September (196); CHD showed a milder winter elevation (January 1,386; September 1,097). After calendar-month indicators, remaining thermal estimates ask whether a given January or July differs from a typical January or July, not whether winter counts exceed summer counts.

**Table 1. Outcome summary.**

| Outcome | Period | Months | Total events | Mean per month | Event construction |
|:--|:--|---:|---:|---:|:--|
| Coronary heart disease | 2013–2023 | 132 | 156,156 | 1,183.0 | First recorded hospitalisation after first CHD diagnosis |
| Heart failure | 2013–2023 | 132 | 29,681 | 224.9 | First recorded hospitalisation after first HF diagnosis |

**Figure 1. First-event counts fell while the general population aged 35+ rose.** Index = 1 in 2013. CHD 23,830 → 12,323; HF 4,336 → 2,296. Provenance: HA_APPROVED_AGGREGATE annual totals; REAL C&SD mid-year population aged 35+.

![Figure 1](../../figures/live_identification/figure_B_first_event_depletion.png)

### Exposure context

At HKO Headquarters, hot nights rose from 10 in 2013 to 61 in 2021 and 56 in 2023 [6]. The 2013 count was about seven days below the 1981–2010 normal [2]. The 2021 total was the highest annual number of hot nights in the Observatory record through the study window. Very hot days rose from 17 to 54 over the same 2013–2021 comparison and were 54 in 2023. Cold days were 14 in 2013 and 14 in 2023 (1 in 2019; 13 in 2021). These are exposure counts, not health effects. Figure 2 shows official cold days by year and month. Of 145 cold days in 2013–2023, 141 fell in December–February (December 40, January 54, February 47) and 4 fell in March. The year 2019 contributed a single cold day. After calendar-month indicators, remaining cold-day variation is between-year winter, not a summer-versus-winter contrast.

**Figure 2. Official cold days by year and month, Hong Kong Observatory Headquarters, 2013–2023.** Provenance: REAL HKO official flags (Tmin ≤ 12 °C) rolled to calendar months.

![Figure 2](../../figures/live_identification/figure_A_cold_day_identification.png)

### Core panel

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

For CHD, continuous monthly temperatures were near null (0.993–0.994), whereas the official hot-night count association was larger under Newey–West lag-6 reporting. These encodings describe different monthly thermal questions. The contrast does not imply that a causal hot-night effect was missed by the means, and it is not a test of hourly nighttime excess heat [17]. For HF, continuous temperature associations were weakly inverse and the cold-day count association was positive.

### Uncertainty ladder

**Table 3. Uncertainty ladder for the two leading exploratory contrasts.**

| Outcome and exposure | Model | HC1 | NW3 | NW6 |
|:--|:--|:--|:--|:--|
| CHD hot nights / 5 days | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.0003–1.0439) | 1.022 (1.002–1.042) |
| HF cold days / 5 days | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

For CHD hot nights, Model and HC1 intervals included 1; NW3 and NW6 excluded 1 on the unrounded scale (NW3 1.000253–1.043860). For that contrast the ladder narrowed from the model-based to the Newey–West intervals; robust intervals are not automatically wider, and the direction of that change is itself informative. For HF cold days, all four constructions excluded 1, but *q* remained 0.192. Concordance across standard-error methods does not create multiplicity protection.

### Joint models, residuals, and robustness

After month and trend residualisation, maximum and minimum temperature retained a variance inflation factor of 4.66 when entered jointly. Hot nights and very hot days retained variance inflation factors near 1.96. In the joint extreme-day model, the CHD hot-night count ratio rose to 1.045 (1.015–1.075) from 1.022 in the separate model. The HF cold-day coefficient was similar in joint and separate models (1.073). Joint coefficients are diagnostics, not preferred estimates.

Pearson residual autocorrelation at lag 1 was 0.51–0.53 for CHD core models and 0.13–0.18 for HF. For the two leading contrasts it was 0.508 (CHD hot nights) and 0.146 (HF cold days) (Figure 3). Ljung–Box tests at lag 6 rejected residual white noise for CHD (*p* < 10^−8^) and not for HF (*p* > 0.3). Serial dependence is part of the inferential problem for CHD, which is why the four-construction ladder is shown rather than a single interval.

**Figure 3. Residual autocorrelation after month and trend.** Lag-1 autocorrelation is 0.508 for the CHD hot-night model and 0.146 for the HF cold-day model. Dashed lines are ±1.96/√132. Provenance: REAL residuals from already-fitted core models.

![Figure 3](../../figures/live_identification/figure_C_residual_acf.png)

Offset choice changed core count ratios only trivially. Across trend and early-period specifications, the CHD hot-night ratio ranged from 1.011 to 1.025 and the HF cold-day ratio from 1.043 to 1.113. The HF cold-day association was stronger before 2020 (1.113, 1.053–1.176). The CHD hot-night association was weaker and compatible with 1 in the pre-2020 window (1.011, 0.991–1.032) and under COVID-phase adjustment (1.013, 0.994–1.033). Lag-1 month models attenuated the CHD hot-night association toward 1 (1.010, 0.979–1.042). The HF cold-day association remained elevated at lag 1 (1.073, 1.014–1.135) and was weaker at lag 2 (1.053, 0.985–1.127). Lag-one month is a labelled sensitivity; it is not a daily lag curve. The months with largest Cook’s distance were February 2020 (CHD) and February 2022 (HF cold days). Excluding the worst month left both exploratory directions unchanged (CHD hot nights 1.021, 1.001–1.040; HF cold days 1.088, 1.034–1.144).

The simulated daily-recovery method failed its worst-cell gates (null Type I error 0.048–0.150; minimum coverage 0.840; maximum non-null relative bias 32.8; maximum moderate false-sign rate 0.808). No real daily coefficient is reported. That refusal is specific to this monthly series and this implementation.

## Discussion

The current data do not support a protected differential thermal claim for CHD relative to HF. Under Newey–West lag-6 reporting for the core panel, CHD first-hospitalisation counts were more closely associated with official hot-night burden than with mean temperature or cold days, and HF counts were more closely associated with cold-day burden than with hot nights. Both patterns sit inside a twelve-contrast family in which every *q*-value exceeds 0.19. The complete panel is therefore reported, and no contrast is promoted to a primary result.

The HF cold-day association is the more coherent of the two residual signals. It is concordant across all four standard-error constructions. It survives exclusion of the most influential pandemic month. It is not produced by entering correlated heat metrics jointly. It nevertheless remains unprotected by its *q*-value. Because official cold days fall almost entirely in December–February, the association is identified from differences between winters rather than from a summer-versus-winter contrast.

The CHD hot-night association is smaller, depends on the uncertainty method, and was not evident in the pre-2020 window. Model-based and HC1 intervals include 1, whereas the Newey–West intervals exclude 1 on the unrounded scale (lag 3: 1.000253 to 1.043860). Pearson residual autocorrelation at lag 1 is 0.508 in that model, so inference for that series depends on how serial dependence is handled. For the hot-night contrast the Newey–West intervals were narrower than the model-based interval, which is atypical under positive residual autocorrelation; the exclusion of 1 therefore rests on the smaller robust variance estimate and is a reason for caution, not confirmation. No interval construction was chosen because it excluded 1.

The direction of the HF cold-day residual is consistent with earlier daily evidence that lower temperature was associated with higher heart-failure admissions in Hong Kong [21]. The comparison is between questions, not between magnitudes. A cumulative daily relative risk comparing 11 °C with 25 °C is not a monthly count ratio per five official cold days, and the present event is a first hospitalisation after a first HF diagnosis without recorded admission cause. The CHD hot-night residual should likewise be read against Guo et al. rather than as a replication of it [17]. That study reported no overall association for the official hot-night flag after adjustment for mean temperature, and a positive association for hourly nighttime excess heat [17]. The present analysis uses monthly official counts, a first-event CHD series, and a later decade. A difference between monthly mean temperature and monthly official hot-night counts does not identify an intensity mechanism, and sleep, blood pressure, and personal exposure were not measured.

Liu et al. (2020, 2026) remain complementary mortality baselines [12,13]. Their attributable fractions and excess-death totals cannot be rescaled into the present count ratios. The failed daily-recovery calibration is the corresponding methods limit: monthly sums do not automatically yield daily trigger estimates [15,16]. That refusal is specific to this series, this implementation, and this calibration standard. It is not evidence that recovery of daily effects from aggregated outcomes fails in general.

Pollution and influenza are scientifically motivated in this setting [1,18]. Archive models in which they enter are not adjusted versions of the core panel. On the 121 months with influenza data, an archive model associated influenza activity with higher CHD counts (1.673, 1.249–2.243), and that coefficient does not adjust Table 2. Confounding by infection, ozone, or nitrogen dioxide is therefore unresolved. Absent cohort person-time, even a stable count ratio remains a count ratio [14].

A protected primary claim would have required a predeclared confirmatory contrast, multiplicity control that survives the twelve-contrast family, uncertainty constructions that are not chosen for null exclusion, and residual diagnostics that leave no substantial CHD serial correlation unaddressed. This analysis does not meet that bar. We report the complete panel and the refusals.

## Conclusion

Between 2013 and 2023, hot nights in Hong Kong increased while cold days persisted. In governed monthly aggregates for people with type 2 diabetes and/or hypertension, CHD first hospitalisations were more closely associated with hot nights, and HF first hospitalisations with cold days, than with the other thermal encodings examined. Neither association survived correction across the twelve comparisons, and the CHD estimate depended on the treatment of uncertainty. The contribution of this analysis is a set of hypotheses and an explicit account of what monthly aggregate counts cannot settle. Better-denominated and more finely resolved data are required before a thermal effect on cardiac hospitalisation in this cohort can be estimated.

## Strengths and limitations

**Strengths.** The twelve-contrast panel is reported in full rather than filtered to its largest estimates. Uncertainty is shown as an explicit four-construction ladder rather than as a single interval. Extreme-day exposures use published official thresholds. Identification displays show the sources of cold-day variation and of the first-event decline. The daily-recovery analysis is reported as a refusal rather than as a coefficient.

**Limitations.** Admission cause was not recorded, so an event is a first hospitalisation after a first diagnosis and not a cardiac-caused admission. Inpatient-only semantics are inferred from the delivered column labels and remain to be confirmed. Monthly counts of cohort members still at risk of a first event were unavailable, so the estimates are count ratios rather than incidence-rate ratios [14]. The design is ecological and monthly, so individual-level and daily-triggering interpretations are not identified [14]. Age, sex, and disease-subtype strata were not delivered. Residual serial correlation remains material for CHD, with lag-1 Pearson autocorrelation of 0.508 in the leading model. Official cold days are concentrated in December–February, so the HF cold-day estimate rests on differences between winters. Official hot-night counts are not hourly nighttime excess heat [17]. All exposures were measured at a single Observatory station and applied territory-wide; within-territory exposure variation was not modelled. Reference rules for monthly hot-tail and cold-tail indicators are not yet fixed, and no such indicator was used as a confirmatory exposure. Pollution, humidity, and influenza confounding is unresolved in the core panel. A stroke series was named in correspondence but was not delivered, and no stroke result is reported. External dissemination of the governed aggregates requires confirmation from the outcome and supervising investigators.

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
21. Goggins WB, Chan EYY. A study of the short-term associations between hospital admissions and mortality from heart failure and meteorological variables in Hong Kong. *Int J Cardiol*. 2017;228:537-542. doi:10.1016/j.ijcard.2016.11.106
