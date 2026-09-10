# Analysis-window sensitivity of first coronary and heart-failure hospitalisation counts across pandemic-era disruption in Hong Kong, 2013–2023

*Running title:* Window sensitivity of first CHD/HF hospitalisation

Bob Ruililin Shen^1^, Author 2^1^, Author 3^1^, Author 4^1^, David Makram Bishai^1^

^1^ School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong, Hong Kong SAR, China

## Abstract

**Background.** Monthly counts of first hospitalisation can change across analysis windows when the population still at risk, care-seeking, and environmental conditions also change. Hong Kong’s 2013–2023 series spans both a secular decline in first coronary and heart-failure events and pandemic-era disruption. We examined the count trajectory and the sensitivity of thermal count ratios to a nested pre-2020 window.

**Methods.** We analysed 132 territory-months (January 2013–December 2023) of monthly counts of first hospitalisation after a first diagnosis of coronary heart disease (CHD; 156,156 events) or heart failure (HF; 29,681 events) among people with type 2 diabetes and/or hypertension. Admission cause was not recorded. Model 1 is a separate negative-binomial model for each of three continuous temperature measures and the official counts of hot nights, very hot days, and cold days, with calendar-month indicators, a 4-df time spline, and an offset for the number of days in the month. Official-day exposures use \(I(\mathrm{count}/5)\) as a reporting scale, read per five additional such days in a month. A pre-2020 specification repeats Model 1 on January 2013–December 2019 (84 months). Intervals used model-based, HC1, and Newey–West lag-3 and lag-6 constructions. Benjamini–Hochberg *q*-values were computed across the twelve full-window Model 1 fits.

**Results.** Annual first-event totals about halved from 2013 to 2023 (CHD 23,830 to 12,323; HF 4,336 to 2,296), with a further dip in 2020 (CHD 10,237; HF 1,964), while the Census and Statistics Department population aged 35 years or older rose by 17%. Under Newey–West lag-6 reporting, the HF cold-day count ratio per five days was 1.113 (1.053–1.176) before 2020 and 1.073 (1.006–1.144) in 2013–2023. The CHD cold-day ratio was 1.036 (1.007–1.067) before 2020 and 0.995 (0.949–1.043) in the full window. The 84 pre-2020 months are contained in the full window, so these estimates are not independent and interval overlap is not a test of a window difference. No separate 2020–2023 estimate is reported. The CHD hot-night ratio was compatible with 1 before 2020 (1.011, 0.991–1.032) and was 1.022 (1.002–1.042) in the full window. Both full-window estimates have *q* = 0.192. All twelve full-window *q*-values exceeded 0.19. Later years were hotter, whereas monthly cold-day frequency was similar.

**Conclusions.** The first-event trajectory and thermal point estimates were sensitive to the analysis window. The nested fits do not estimate a pre/post effect. Observed thermal encodings do not supply a complete explanation for the count trajectory. The decline in first events cannot be read as physiological improvement.

**Keywords:** analysis window; first hospitalisation; coronary heart disease; heart failure; Hong Kong; cold days; hot nights

## Introduction

The analysis window is part of the question when an outcome is a monthly count
of first events. The 2013–2023 Hong Kong series spans a secular decline, the
2020 disruption of hospital use, and later reopening. It also spans a closed
diagnosis interval in which people leave the still-at-risk population after
their first event. Care-seeking, depletion, and environmental change can
therefore produce similar movements in the observed counts.

Hong Kong studies of 2020 describe fewer cardiovascular admissions, not fewer cardiovascular events. Xin et al. reported fewer public hospitalisations in 2020, including cardiovascular admissions, together with additional deaths, particularly cardiovascular deaths and deaths outside public hospitals [34]. Wai et al. found fewer emergency-department visits in January–August 2020 than in the same months of 2019, and higher 28-day mortality among those who did attend [35]. A later Wai et al. cohort of non-COVID deaths likewise paired fewer emergency visits with higher 28-day mortality [36]. Hung et al. documented self-reported avoidance of consultation in a public survey [37]. Tam et al. reported longer delays to ST-elevation myocardial infarction care in Hong Kong in early 2020 [38,39]. Those papers are utilisation and delay series. They are not this diabetes-or-hypertension first-event construction, and their counts are not imported into the tables below.

Local thermal studies answer a different question. Earlier daily analyses
reported cold-related elevations in acute myocardial infarction and
heart-failure admissions [1,21]. A later hot-season study distinguished the
official hot-night flag from hourly nighttime excess heat [17]. Those designs
estimate daily risk for cause-coded or unplanned admissions. Their coefficients
do not transfer to monthly counts of first hospitalisation after a first CHD or
HF diagnosis.

The later period was hotter, but it was not free of cold days. Monthly mean
temperature rose from 23.83 °C in 2013–2019 to 24.30 °C in 2020–2022. Mean
monthly hot nights rose from 2.74 to 4.53, whereas mean monthly cold days were
similar (1.12 and 1.03). Pollution and influenza also changed across the study
period [7,40]. These co-moving series prevent a single thermal encoding from
being read as an explanation of the hospital-count trajectory.

We describe the first-event trajectory and compare thermal count-ratio point
estimates from the full 132 months with the nested 84-month window ending in
December 2019. The comparison is an analysis-window sensitivity, not a fitted
pre/post effect. The complete twelve-fit Model 1 panel remains visible so that
the window comparison is not presented as a selected thermal finding.

## Methods

The study is an ecological territory-month time series for January 2013 through December 2023 (132 months). It cannot show effects for individual people, the cause of any admission, or day-level triggering [14]. In line with ethical requirements, the study was approved by the Institutional Review Board (IRB) of the HKU/Hospital Authority HK West Cluster (IRB reference number: UW XX-XXX).

### Data sources

#### Health data

The dependent variable is the monthly count of first hospitalisations after a first diagnosis of coronary heart disease (CHD), and separately of heart failure (HF), among people with type 2 diabetes and/or hypertension in Hong Kong. The cohort is people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. For each person, the event is the first recorded hospitalisation after that person’s first CHD diagnosis or first HF diagnosis. Admission cause was not recorded. Monthly counts were supplied from Hospital Authority records. Age and sex strata were not included. Laboratory measurements were not in the transfer and are not analysed.

Monthly influenza activity from November 2013 through December 2023 was obtained from Centre for Health Protection Flu Express summaries. January–October 2013 had no influenza values. Those months were left missing and were not coded as zero. Influenza was therefore not entered in Model 1; it is a sensitivity on the 121 months with data.

#### Weather and pollutants data

Meteorological data was obtained from the HKO. The monthly variables included: temperature (mean, minimum, maximum), relative humidity, total rainfall, the number of hot nights (T~min~ ≥ 28°C), the number of very hot days (T~max~ ≥ 33°C), the number of extremely hot days (T~max~ ≥ 35°C), and the number of cold days (T~min~ ≤ 12°C). Monthly mean pollutant levels for nitrogen dioxide (NO~2~), sulfur dioxide (SO~2~), and ozone (O~3~) were obtained from the Hong Kong Environmental Protection Department (EPD). All monthly data were derived by taking the average of daily data in each calendar month.

A station-month entered a pollutant mean only when at least 75% of expected observations were present. Missing measurements were not coded as zero. Territory-wide monthly pollutant concentrations are unweighted means of general EPD stations. Roadside monitors were not used for those means. Fine particulate matter (PM~2.5~) from the same general stations was assembled for sensitivity analysis only.

#### Population

Mid-year age- and sex-specific population estimates from the Census and Statistics Department (Table 110-01001) were interpolated to month mid-points [8]. Those figures describe the general population, not the diabetes or hypertension group still at risk of a first CHD or HF hospitalisation. Model 1 therefore uses the number of days in the month as the offset and is read as a monthly count ratio, not as a cohort incidence rate [14]. A population × days offset is a sensitivity only. It does not turn the estimate into cohort incidence.

### Statistical analysis

Let \(Y_t\) be the hospital count in month \(t\). Model 1 is a negative-binomial regression [10]:

\[
\log \mathrm{E}(Y_t) = \log(d_t) + \alpha + \beta X_t + \sum_{m=2}^{12} \gamma_m I(\mathrm{month}_t = m) + s(t; 4~\mathrm{df}). \tag{1}
\]

Here \(d_t\) is the number of days in month \(t\); \(\alpha\) is the intercept; \(X_t\) is one weather variable; \(\beta\) is the coefficient for that weather variable; \(I(\mathrm{month}_t = m)\) is 1 if month \(t\) is calendar month \(m\) and 0 otherwise (January is the reference month); \(\gamma_m\) is how much higher or lower month \(m\) is than January; and \(s(t; 4~\mathrm{df})\) is a smooth curve of time with four degrees of freedom, used to capture slow change over the eleven years. In words, the left side is the log of the expected hospital count. The estimate we report is \(\mathrm{e}^{\beta}\), the ratio of expected monthly counts for a 1 °C change in a temperature variable or a five-day change in an official day count.

We fitted Model 1 twelve times: six weather variables × two diagnoses. The six weather variables are monthly mean temperature, monthly mean daily maximum temperature, monthly mean daily minimum temperature, hot nights, very hot days, and cold days. Extreme-day counts were divided by 5 so that each estimate is the change associated with five extra such days in that month, rather than with one extra day. Five days is a convenient scale, not a new weather threshold and not a consecutive-duration rule. The official count of extremely hot days (T~max~ ≥ 35°C) was obtained with the other monthly weather variables and was not used as a temperature variable in Model 1. Each Model 1 fit contains one temperature variable. Temperature terms are not entered together in Model 1. We used a negative-binomial model because monthly counts can vary more than a Poisson model permits. A quasi-Poisson model is a sensitivity.

We report 95% confidence intervals in four ways: the model’s own standard errors, HC1, Newey–West with a lag of 3 months, and Newey–West with a lag of 6 months [19]. The main reported interval is Newey–West with lag 6. Monthly hospital counts can be correlated from one month to the next; Newey–West intervals allow for that. A *q*-value is a *p*-value adjusted for testing the twelve Model 1 fits together [20]. Multiplicity-adjusted *q*-values were computed on the full 132-month window only.

The pre-2020 specification repeats equation (1) on January 2013–December 2019 (84 months). It is a labelled window check, not a 48-month post-2020 primary and not a confirmatory re-fit. COVID-period indicators on the full sample (through January 2020; February 2020–December 2021; January–April 2022; May–December 2022; and from January 2023) are a further labelled specification. They do not replace Model 1, and they do not create a post-only table.

Model 2 additionally adds monthly mean relative humidity [21] and monthly total rainfall [22] to Model 1. Model 3 counts, for each month, the days whose daily mean temperature was above or below the historical average for that day of the year. Model 2 and Model 3 are specified and are not reported as headline estimates. No Model 3 health coefficients are reported.

### Sensitivity analysis

Official day-count estimates from Model 1 can also be read per 3 days or per 1 day without fitting a new model. If the count ratio per five days is *R*, the count ratio per three days is *R*^(3/5) and the count ratio per one day is *R*^(1/5). Those are the same coefficient on a different scale, not a new model.

Other checks were the time-trend spline (3, 6, or 8 degrees of freedom in place of the Model 1 4-df spline, or year indicators in place of that spline). Those checks change the control for slow calendar time, not the length of a heatwave. Further checks were dropping the first 12 or 24 months; weather one or two months earlier; and dropping the most influential month. Cold-day models restricted to November–March are a labelled sensitivity.

Further checks used general-population × days as the offset (this is still a count ratio, not cohort incidence); maximum and minimum temperature in one model, or the three official extreme-day counts in one model; influenza on the 121 months with data; and nitrogen dioxide or PM2.5. Models that added pollution or influenza are extra checks. They are not replacements for Model 1.

Residual correlation was inspected with Pearson autocorrelation and Ljung–Box tests at lags 6 and 12.

Separately, we tested a published method for estimating daily temperature effects from monthly outcomes using simulated Hong Kong weather [15,16]. We did not apply that method to the hospital counts.

### Software

Analyses were conducted in R 4.3.3 (2024-02-29). Negative-binomial models used `MASS::glm.nb` (MASS 7.3-60.0.1). Newey–West and HC1 standard errors used `sandwich` 3.1.3. Natural cubic splines used `splines::ns`.

## Results

### Outcome series

CHD contributed 156,156 first recorded hospitalisations over 132 months, a
mean of 1,183.0 per month. HF contributed 29,681, a mean of 224.9 per month
(Table 1). Annual totals fell by about half from 2013 to 2023 (CHD 23,830 to
12,323; HF 4,336 to 2,296), with a further dip in 2020 (CHD 10,237; HF 1,964).
Over the same years, the interpolated Census and Statistics Department
population aged 35 years or older rose by 17%. Most of the count decline
preceded 2020: 2019 totals were 12,396 for CHD and 2,344 for HF. Figure 1
therefore shows a secular decline with a pandemic-era trough, rather than a
post-2020 health recovery. The series cannot distinguish depletion from
changes in care-seeking without monthly still-at-risk person-time.

**Table 1. Outcome summary.**

| Outcome | Period | Months | Total events | Mean per month | Event construction |
|:--|:--|---:|---:|---:|:--|
| Coronary heart disease | 2013–2023 | 132 | 156,156 | 1,183.0 | First recorded hospitalisation after first CHD diagnosis |
| Heart failure | 2013–2023 | 132 | 29,681 | 224.9 | First recorded hospitalisation after first HF diagnosis |

**Figure 1. First-event counts fell while the general population aged 35 years or older rose.** Index = 1 in 2013. CHD 23,830 → 12,323; HF 4,336 → 2,296. Source: governed Hospital Authority aggregate annual totals; Census and Statistics Department mid-year population aged 35 years or older. The figure does not measure consecutive hot or cold spells, and it is not a physiological series.

![Figure 1](../../figures/live_identification/figure_B_first_event_depletion.png)

### Exposure context

Mean temperature, hot nights, and very hot days were higher in 2020–2022 than in 2013–2019, whereas monthly cold-day frequency was similar (Supplementary Table S10). These are exposure summaries, not health effects. Of 145 cold days in 2013–2023, 141 fell in December–February. Twenty-nine of 132 months carried at least one official cold day (Figure 2). After calendar-month indicators, the remaining cold-day variation is between-year winter variation, not a summer-versus-winter contrast.

**Figure 2. Official cold days by year and month, Hong Kong Observatory Headquarters, 2013–2023.** Source: Hong Kong Observatory official daily cold-day flags (T~min~ ≤ 12 °C), aggregated to calendar months. Identification is between winters, not a consecutive-duration spell, and not a physiological mechanism.

![Figure 2](../../figures/live_identification/figure_A_cold_day_identification.png)

### Nested-window official-day panel

Table 2 reports the official-day Model 1 count ratios, per five additional such days in the month, for the full 132 months and for the labelled 84-month specification. Figure 3 is the main identification display for this article, including trend-spline and COVID-phase rows.

The HF cold-day point estimate was 1.113 (1.053–1.176) before 2020 and 1.073 (1.006–1.144) over 2013–2023. The CHD cold-day estimate was 1.036 (1.007–1.067) before 2020 and 0.995 (0.949–1.043) in the full window. The 84 pre-2020 months are contained in the full window, so the estimates are not independent and interval overlap is not a test of a window difference. The CHD hot-night estimate was compatible with 1 before 2020 (1.011, 0.991–1.032) and was 1.022 (1.002–1.042) in the full window. Both displayed full-window estimates have *q* = 0.192. COVID-phase indicators on the full sample moved the CHD hot-night ratio to 1.013 (0.994–1.033) and left the HF cold-day ratio at 1.074 (1.006–1.145). These are nested-window sensitivity estimates. No interaction between thermal exposure and period was fitted, and no separate 2020–2023 Model 1 estimate is reported.

**Table 2. Official-day count ratios in the full window and in January 2013–December 2019 (Newey–West lag-6).** Each estimate is the Model 1 count ratio per five additional official days in the month. Pre-2020 is a labelled specification (84 months). Benjamini–Hochberg *q*-values apply to the twelve full-window Model 1 fits only.

| Outcome | Exposure contrast | 2013–2023 (132 months) | Pre-2020 (84 months) |
|:--|:--|--:|--:|
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042), *q* = 0.192 | 1.011 (0.991–1.032) |
| CHD | Very hot days / 5 days | 0.999 (0.974–1.025) | 0.997 (0.982–1.012) |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 1.036 (1.007–1.067) |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.965 (0.937–0.994) |
| HF | Very hot days / 5 days | 0.995 (0.963–1.028) | 0.990 (0.960–1.021) |
| HF | Cold days / 5 days | 1.073 (1.006–1.144), *q* = 0.192 | 1.113 (1.053–1.176) |

**Figure 3. Model 1 count ratios for official day counts across time-trend, window, and COVID-period specifications (Newey–West lag-6 intervals).** The exposure is the monthly official day count divided by five, so each estimate is the count ratio per five additional such days in that month. Rows labelled 3, 6, or 8 df replace the 4-df time-trend spline of Model 1. Neither the five-day scale nor the spline degrees of freedom refers to consecutive days. Pre-2020 is January 2013–December 2019 (84 months). Continuous-temperature fits for the same specifications are a supplement, not a physiology panel.

![Figure 3](../../figures/live_identification/figure_D_trend_depletion_sensitivity.png)

### Full thermal panel and uncertainty

The complete twelve-fit Model 1 panel, with all four uncertainty constructions,
is reported in Supplementary Table S1. All twelve full-window *q*-values
exceeded 0.19; the minimum was 0.192. No fit meets a
multiplicity-protected confirmatory threshold.

**Table 3. Uncertainty ladder for four diagnostic contrasts.**

| Outcome and exposure | Model | HC1 | NW3 | NW6 |
|:--|:--|:--|:--|:--|
| CHD hot nights / 5 days | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.000–1.044) | 1.022 (1.002–1.042) |
| HF mean temperature / 1 °C | 0.974 (0.956–0.993) | 0.974 (0.949–1.000) | 0.974 (0.949–1.001) | 0.974 (0.947–1.002) |
| HF mean minimum temperature / 1 °C | 0.973 (0.956–0.991) | 0.973 (0.950–0.997) | 0.973 (0.948–0.999) | 0.973 (0.947–1.000) |
| HF cold days / 5 days | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

For CHD hot nights, the model-based and HC1 intervals included 1, while the
Newey–West intervals excluded 1. Those robust intervals were narrower, not
wider, than the model-based interval. For HF mean and minimum temperature, the
model-based intervals excluded 1, whereas the Newey–West lag-6 intervals
included 1. HF cold days excluded 1 under all four constructions. No
construction was selected because it excluded 1, and agreement across
constructions does not create multiplicity protection.

### Analysis-window context

Before 2020, mean temperature was inversely associated with both outcomes (CHD 0.980, 0.970–0.990; HF 0.945, 0.927–0.963). In the same 84 months, the HF hot-night estimate was 0.965 (0.937–0.994), while the HF cold-day estimate was 1.113 (1.053–1.176). Nine of the twelve Newey–West lag-6 intervals excluded 1 in that nested window, including all six continuous-temperature contrasts (Supplementary Table S2; Supplementary Figure S6). No multiplicity control was computed within that window. The panel is not a uniformly null monthly result, and the pre-2020 estimates are not promoted beyond sensitivity analyses.

### Joint models, residuals, and influence

Pearson residual autocorrelation at lag 1 was 0.508 in the CHD hot-night model
and 0.146 in the HF cold-day model. Ljung–Box tests at lag 6 gave *p* <
10^−7^ for every CHD Model 1 fit and *p* > 0.3 for every HF Model 1 fit.
Serial dependence is therefore part of the CHD mean-model problem, not only an
interval problem.

Across trend, window, and COVID-phase specifications, the CHD hot-night point estimate ranged from 1.011 to 1.025, and the HF cold-day estimate from 1.043 to 1.113 (Figure 3). February 2020 had the largest Cook’s distance for CHD; February 2022 did so for HF cold days. Excluding those months left the directions unchanged (CHD hot nights 1.021, 1.001–1.040; HF cold days 1.088, 1.034–1.144). Full lag, influence, collinearity, residual, and daily-recovery diagnostics are reported in Supplementary Tables S3–S8.

## Discussion

The principal result is sensitivity to the analysis window, not a pre/post
effect. First-event counts had already fallen substantially by 2019, followed
by a further trough in 2020. The cold-day point estimates were smaller in the
full window than in the nested pre-2020 window. Because the 84-month window is
contained in the full window, this comparison does not estimate a period
contrast. The CHD hot-night interval excluded 1 only in the full window. No
exposure-by-period interaction was fitted. All twelve full-window *q*-values
exceeded 0.19.

**Utilisation.** Hong Kong studies reported fewer public hospitalisations and
emergency-department visits in 2020, together with more cardiovascular or
out-of-hospital deaths [34–36]. A public survey found avoidance of medical
consultation [37]. Studies of ST-elevation myocardial infarction found delayed
presentation and a worse in-hospital course [38,39]. These are care-seeking
and system-shock patterns, not evidence of improved cardiovascular health.
They cannot determine how much of the present count trajectory reflects
delayed or avoided care.

**First-event depletion.** The outcome can occur only once after a person’s
first CHD or HF diagnosis in the study window. People leave the risk set after
that event. The decline in Figure 1 is therefore compatible with a shrinking
still-at-risk population, but monthly person-time was unavailable [14].
General-population growth does not resolve that denominator problem.

**Weather entanglement.** The later period was hotter, whereas monthly
cold-day frequency was similar. Hot nights rose in the same years in which
care-seeking changed, and the CHD hot-night interval excluded 1 only when
those years were included. Continuous-temperature and official-day estimates
also differed in the nested window. The observed thermal encodings therefore
do not supply a complete explanation for the count trajectory. They are not evidence that weather was irrelevant.

An immune-recovery explanation is not supported by this extract. Studies in
Hong Kong have associated vaccination with lower cardiovascular risk after
documented SARS-CoV-2 infection [42]. That is prevention of post-infection
complications, not improvement in baseline first-event risk. Post-acute
SARS-CoV-2 infection has instead been associated with higher cardiovascular
risk [41]. Infection, vaccination, antibody levels, and laboratory measures
were not in the monthly transfer.

Influenza transmission fell sharply during Hong Kong’s early pandemic
interventions [40]. The archive influenza model covers 121 months and is not
an adjusted Model 1 estimate (Supplementary Table S7). Pollution also
declined across the decade [7]. Archive pollution models use a different
joint-temperature specification and a population × days offset
(Supplementary Table S9). Infection and pollution therefore remain unresolved
co-exposures rather than explanations established by this analysis.

This result bears on a common interpretive failure in coarse first-event
series. A lower observed count can reflect a smaller risk set or less hospital
use. A smaller coefficient in a longer,
nested window is not a period effect. A monthly official-day total also does
not distinguish consecutive days from days scattered through the month.
Five additional official days is a reporting scale, not a duration threshold.

## Strengths and limitations

**Strengths.** The count trajectory and thermal estimates are kept as separate
objects. The full twelve-fit panel is reported, including all null and
discordant estimates. Uncertainty is shown under four constructions. Figures
1–3 show the secular decline, the limited distribution of cold-day exposure,
and sensitivity to the analysis window and time trend.

**Limitations.** Admission cause was not recorded, so an event is a first
hospitalisation after a first diagnosis and not a cardiac-caused admission.
Monthly still-at-risk person-time was unavailable; the estimates are count
ratios rather than incidence-rate ratios [14]. Laboratory, infection,
vaccination, age, sex, and disease-subtype series were not delivered. No
exposure-by-period interaction or post-only Model 1 was fitted. The design is
ecological and monthly, so individual and daily-trigger interpretations are
not identified [14]. CHD residual serial correlation remained material
(lag-1 autocorrelation 0.508). Only 29 of 132 months carried an official cold
day. Exposure was assigned from one Observatory station. Confounding by
pollution, humidity, rainfall, influenza, and changes in hospital use remains
unresolved. Stroke was not available.

## Conclusion

Monthly first CHD and HF hospitalisations declined across 2013–2023, with a
further trough in 2020. Cold-day point estimates were larger in the nested
pre-2020 window than in the full window. No period interaction or separate
post-2020 Model 1 estimate was fitted. Later years were hotter, while cold-day
frequency was similar. The thermal variables do not supply a complete
explanation for the count trajectory. The data show analysis-window
sensitivity and do not show improved cardiovascular health after COVID-19.

## Declaration on the use of AI

AI-assisted tools were used for code scaffolding, methodological brainstorming, and review of potential data and modelling issues. Scientific claims and numerical results were checked against Hospital Authority monthly counts and the live weather paragraph.

## Declaration of competing interest

The authors declare no competing interests.

## Acknowledgements

None.

## Data and code availability

Code is at https://github.com/bobshenruililin/Laidlaw-Heat-Project. Monthly
hospital counts are not posted. What may be shared later depends on ethics
approval.

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
22. Chan EYY, Goggins WB, Yue JSK, Lee P. Hospital admissions as a function of temperature, other weather phenomena and pollution levels in an urban setting in China. *Bull World Health Organ*. 2013;91(8):576-584. doi:10.2471/BLT.12.113035
23. Chevance G, Minor K, Vielma C, et al. A systematic review of ambient heat and sleep in a warming climate. *Sleep Med Rev*. 2024;75:101915. doi:10.1016/j.smrv.2024.101915
24. Ioannou LG, Tsoutsoubi L, Mantzios K, et al. Impact of a simulated multiday heatwave on nocturnal physiology, behavior, and sleep: a 10-day confinement study. *Appl Physiol Nutr Metab*. 2024;49:1394-1408. doi:10.1139/apnm-2024-0105
25. O’Connor FK, Bach AJE, Forbes C, et al. Effect of nighttime bedroom temperature on heart rate variability in older adults: an observational study. *BMC Med*. 2025;23:703. doi:10.1186/s12916-025-04513-0
26. Ashe N, Wozniak S, Conner M, et al. Association of extreme heat events with sleep and cardiovascular health: a scoping review. *Syst Rev*. 2025;14:19. doi:10.1186/s13643-024-02742-7
27. Ikäheimo TM. Cardiovascular diseases, cold exposure and exercise. *Temperature (Austin)*. 2018;5(2):123-146. doi:10.1080/23328940.2017.1414014
28. Li Y, Wu J, Xu Y, et al. Cold exposure and the cardiovascular system: from physiological adaptation to pathological risk. *Front Physiol*. 2026;16:1740919. doi:10.3389/fphys.2025.1740919
29. WHO Regional Office for Europe. *Heat–health action plans: guidance*. 2nd ed. Copenhagen: WHO Regional Office for Europe; 2026. ISBN 9789289062930. https://www.who.int/europe/publications/i/item/9789289062930
30. Chong SN, Law HF. Beware of Health Effects of Extremely Hot Weather. Hong Kong Observatory. December 2023. https://www.hko.gov.hk/en/education/weather/hot-and-cold-weather/00706-Beware-of-Health-Effects-of-Extremely-Hot-Weather.html
31. Hong Kong Observatory. Cold and Very Hot Weather Warnings. https://www.hko.gov.hk/en/wservice/warning/coldhot.htm
32. Centre for Health Protection. Beware of Heat Stroke. 11 August 2025. https://www.chp.gov.hk/en/static/90064.html
33. Home Affairs Department. Emergency Relief Services: temporary heat shelters. https://www.had.gov.hk/en/public_services/emergency_services/emergency.htm
34. Xin H, Wu P, Wong JY, et al. Hospitalizations and mortality during the first year of the COVID-19 pandemic in Hong Kong, China: an observational study. *Lancet Reg Health West Pac*. 2023;30:100645. doi:10.1016/j.lanwpc.2022.100645
35. Wai AKC, Wong CKH, Wong JYH, et al. Changes in emergency department visits, diagnostic groups, and 28-day mortality associated with the COVID-19 pandemic. *Ann Emerg Med*. 2022;79(2):148-157. doi:10.1016/j.annemergmed.2021.09.424
36. Wai AKC, Yip TF, Wong YH, et al. The effect of the COVID-19 pandemic on non–COVID-19 deaths: a cohort study. *JMIR Public Health Surveill*. 2024;10:e41792. doi:10.2196/41792
37. Hung KK, Walline JH, Chan EYY, et al. Health service utilization in Hong Kong during the COVID-19 pandemic: a cross-sectional public survey. *Int J Health Policy Manag*. 2022;11(4):508-513. doi:10.34172/ijhpm.2020.183
38. Tam CCF, Cheung KS, Lam S, et al. Impact of coronavirus disease 2019 (COVID-19) outbreak on ST-segment–elevation myocardial infarction care in Hong Kong, China. *Circ Cardiovasc Qual Outcomes*. 2020;13(4):e006631. doi:10.1161/CIRCOUTCOMES.120.006631
39. Tam CCF, Cheung KS, Lam S, et al. Impact of coronavirus disease 2019 (COVID-19) outbreak on outcome of myocardial infarction in Hong Kong, China. *Catheter Cardiovasc Interv*. 2021;97(2):E194-E197. doi:10.1002/ccd.28943
40. Cowling BJ, Ali ST, Ng TWY, et al. Impact assessment of non-pharmaceutical interventions against coronavirus disease 2019 and influenza in Hong Kong: an observational study. *Lancet Public Health*. 2020;5(5):e279-e288. doi:10.1016/S2468-2667(20)30090-6
41. Xie Y, Xu E, Bowe B, Al-Aly Z. Long-term cardiovascular outcomes of COVID-19. *Nat Med*. 2022;28:583-590. doi:10.1038/s41591-022-01689-3
42. Wan EYF, Mathur S, Zhang R, et al. Association between BNT162b2 and CoronaVac vaccination and risk of CVD and mortality after COVID-19 infection: a population-based cohort study. *Cell Rep Med*. 2023;4(10):101195. doi:10.1016/j.xcrm.2023.101195
