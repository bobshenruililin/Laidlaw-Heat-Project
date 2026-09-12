# Window dependence of first coronary and heart-failure hospitalisations among people with diabetes or hypertension in Hong Kong, 2013–2023

*Running title:* Window dependence of first CHD/HF hospitalisation

*Candidate article. Confirmatory freeze has not been declared. Estimates are the same parked Model 1 and window checks; the thesis is the analysis window, not a new thermal discovery.*

Bob Ruililin Shen^1^, Author 2^1^, Author 3^1^, Author 4^1^, David Makram Bishai^1^

^1^ School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong, Hong Kong SAR, China

## Abstract

**Background.** Monthly counts of first coronary and heart-failure hospitalisation in Hong Kong fell by about half between 2013 and 2023, and fell further in 2020. Neighbouring Hong Kong series report fewer public hospitalisations and more cardiovascular deaths in that year. Whether a thermal count ratio estimated on such a window is stable across the window is untested. This paper asks two questions of one extract: what path the first-event counts followed, and whether official thermal extremes are sufficient to account for the dependence of the estimates on the window analysed.

**Methods.** We analysed 132 territory-months (January 2013–December 2023) of monthly counts of first hospitalisation after a first diagnosis of coronary heart disease (CHD; 156,156 events) or heart failure (HF; 29,681 events) among people with type 2 diabetes and/or hypertension. Admission cause was not recorded. Model 1 is a separate negative-binomial model for each of three continuous temperature measures and the official counts of hot nights, very hot days, and cold days, with calendar-month indicators, a 4-df time spline, and an offset for the number of days in the month. Official-day exposures use \(I(\mathrm{count}/5)\) as a reporting scale, read per five additional such days in a month. A nested specification repeats Model 1 on the 84 months from January 2013 to December 2019, which are contained in the full window. Intervals used model-based, HC1, and Newey–West lag-3 and lag-6 constructions. Benjamini–Hochberg *q*-values were computed across the twelve full-window Model 1 fits.

**Results.** Annual first-event totals about halved from 2013 to 2023 (CHD 23,830 to 12,323; HF 4,336 to 2,296), with a further dip in 2020 (CHD 10,237; HF 1,964), while the Census and Statistics Department population aged 35 years or older rose by 17%. Under Newey–West lag-6 reporting, the HF cold-day count ratio per five days was 1.113 (1.053–1.176) in the nested 84 months and 1.073 (1.006–1.144) in the full 132. The CHD cold-day ratio excluded 1 only in the nested window (1.036, 1.007–1.067 versus 0.995, 0.949–1.043). The CHD hot-night ratio was compatible with 1 in the nested window (1.011, 0.991–1.032) and was 1.022 (1.002–1.042) in the full window. Both full-window estimates have *q* = 0.192. All twelve full-window *q*-values exceeded 0.19. Continuous mean temperature was inverse in the nested window for both outcomes (CHD 0.980, 0.970–0.990; HF 0.945, 0.927–0.963), so official day counts and monthly means are not interchangeable encodings.

**Conclusions.** First-event counts and official-day count ratios in this extract depend on the window analysed. Official thermal extremes are insufficient to account for that dependence. They remain part of the exposure record. The decline in first events is not a measure of physiological improvement. Estimates remain ecological monthly count ratios for a first-event outcome without recorded admission cause.

**Keywords:** analysis window; first hospitalisation; coronary heart disease; heart failure; Hong Kong; cold days; hot nights

## Introduction

The 2013–2023 window in Hong Kong is not a homogeneous decade for a hospital count. It contains a 2020 collapse in public-hospital use and a rebound that did not restore early-decade first-event totals. It also spans a closed diagnosis interval, so the set of people still able to contribute a first event shrinks over time. Any monthly count of first coronary or heart-failure hospitalisation in that window therefore mixes weather, care-seeking, and depletion of the risk set. A thermal coefficient estimated on the whole window inherits that mixture.

Hong Kong studies of 2020 describe fewer cardiovascular admissions, not fewer cardiovascular events. Xin et al. reported fewer public hospitalisations in 2020, including cardiovascular admissions, together with additional deaths, particularly cardiovascular deaths and deaths outside public hospitals [1]. Wai et al. found fewer emergency-department visits in January–August 2020 than in the same months of 2019, and higher 28-day mortality among those who did attend [2]. A later Wai et al. cohort of non-COVID deaths likewise paired fewer emergency visits with higher 28-day mortality [3]. Hung et al. documented self-reported avoidance of consultation in a public survey [4]. Tam et al. reported longer delays to ST-elevation myocardial infarction care in Hong Kong in early 2020 [5,6]. Those papers are utilisation and delay series. They are not this diabetes-or-hypertension first-event construction, and their counts are not imported into the tables below.

Local thermal evidence answers a different question. Using 2000–2009 data, Goggins et al. associated a 1 °C decrease below an estimated 24 °C threshold with a 3.7% increase in acute myocardial infarction admissions, and found no statistically significant heat association in Hong Kong, Taipei, or Kaohsiung [7]. Closest to the present heart-failure outcome, Goggins and Chan analysed daily public-hospital heart-failure admissions and deaths during 2002–2011 and reported a cumulative relative risk of 2.63 (2.43–2.84) for admissions comparing 11 °C with 25 °C over lags to 23 days [8]. Guo et al. analysed daily unplanned emergency hospitalisations in the hot seasons of 2000–2019: after adjustment for multi-day mean temperature, the official hot-night indicator showed no overall association with non-cancer, non-external hospitalisation over lags 0–4 days, while an hourly nighttime excess-heat metric did [9]. Those studies estimate daily risk for cause-coded or unplanned admissions. Their coefficients do not transfer to monthly counts of first hospitalisation after a first CHD or HF diagnosis, and they do not identify why a 2013–2019 count ratio would differ from a 2013–2023 fit.

The Observatory record for the same years is unambiguous as climatology. Hot nights at Headquarters rose from 10 in 2013 to 61 in 2021 and 56 in 2023 [10,11,12]. Very hot days rose from 17 to 54 over the 2013–2021 comparison and were 54 in 2023 [11,12]. Cold days were 14 in 2013 and 14 in 2023, with 1 in 2019 and 13 in 2021 [10,11,12]. Air pollution also moved: at general monitoring stations, mean nitrogen dioxide declined from 53.7 µg m^−3^ in 2013 to 32.1 µg m^−3^ in 2023, and fine particulate matter (PM2.5) from 30.8 to 14.6 µg m^−3^, while ozone rose from 42.6 to 58.3 µg m^−3^ [13]. Those series describe the window. They do not, by themselves, explain a first-event count ratio.

This study therefore reports two objects from one extract. The first is the path of the monthly first-hospitalisation counts. The second is the Model 1 count ratio for official hot nights, very hot days, and cold days, shown for the full 132 months and for the nested 84 months that stop at December 2019. The official-day ratios are carried as a ruling-out exhibit for the first object: if official thermal extremes were a sufficient account of the window dependence, those ratios would be stable across the two windows, and continuous temperature would tell the same story as the official day counts. All twelve full-window Model 1 fits are reported so that the exhibit is not a selected pair of rows.

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

Mid-year age- and sex-specific population estimates from the Census and Statistics Department (Table 110-01001) were interpolated to month mid-points [15]. Those figures describe the general population, not the diabetes or hypertension group still at risk of a first CHD or HF hospitalisation. Model 1 therefore uses the number of days in the month as the offset and is read as a monthly count ratio, not as a cohort incidence rate [14]. A population × days offset is a sensitivity only. It does not turn the estimate into cohort incidence.

### Statistical analysis

Let \(Y_t\) be the hospital count in month \(t\). Model 1 is a negative-binomial regression [16]:

\[
\log \mathrm{E}(Y_t) = \log(d_t) + \alpha + \beta X_t + \sum_{m=2}^{12} \gamma_m I(\mathrm{month}_t = m) + s(t; 4~\mathrm{df}). \tag{1}
\]

Here \(d_t\) is the number of days in month \(t\); \(\alpha\) is the intercept; \(X_t\) is one weather variable; \(\beta\) is the coefficient for that weather variable; \(I(\mathrm{month}_t = m)\) is 1 if month \(t\) is calendar month \(m\) and 0 otherwise (January is the reference month); \(\gamma_m\) is how much higher or lower month \(m\) is than January; and \(s(t; 4~\mathrm{df})\) is a smooth curve of time with four degrees of freedom, used to capture slow change over the eleven years. In words, the left side is the log of the expected hospital count. The estimate we report is \(\mathrm{e}^{\beta}\), the ratio of expected monthly counts for a 1 °C change in a temperature variable or a five-day change in an official day count.

We fitted Model 1 twelve times: six weather variables × two diagnoses. The six weather variables are monthly mean temperature, monthly mean daily maximum temperature, monthly mean daily minimum temperature, hot nights, very hot days, and cold days. Extreme-day counts were divided by 5 so that each estimate is the change associated with five extra such days in that month, rather than with one extra day. Five days is a convenient scale, not a new weather threshold and not a consecutive-duration rule. The official count of extremely hot days (T~max~ ≥ 35°C) was obtained with the other monthly weather variables and was not used as a temperature variable in Model 1. Each Model 1 fit contains one temperature variable. Temperature terms are not entered together in Model 1. We used a negative-binomial model because monthly counts can vary more than a Poisson model permits. A quasi-Poisson model is a sensitivity.

We report 95% confidence intervals in four ways: the model’s own standard errors, HC1, Newey–West with a lag of 3 months, and Newey–West with a lag of 6 months [17]. The main reported interval is Newey–West with lag 6. Monthly hospital counts can be correlated from one month to the next; Newey–West intervals allow for that. A *q*-value is a *p*-value adjusted for testing the twelve Model 1 fits together [18]. Multiplicity-adjusted *q*-values were computed on the full 132-month window only.

The nested specification repeats equation (1) on January 2013–December 2019 (84 months). Those 84 months are contained in the 132; the two fits are therefore not independent periods, and their difference is not a fitted pre/post effect. No interaction between exposure and period was fitted, and no 48-month post-2020 window is reported as a Model 1 table. COVID-period indicators on the full sample (through January 2020; February 2020–December 2021; January–April 2022; May–December 2022; and from January 2023) are a further labelled specification. They do not replace Model 1.

Model 2 additionally adds monthly mean relative humidity [8] and monthly total rainfall [19] to Model 1. Model 3 counts, for each month, the days whose daily mean temperature was above or below the historical average for that day of the year. Model 2 and Model 3 are specified and are not reported as headline estimates. No Model 3 health coefficients are reported.

### Sensitivity analysis

Official day-count estimates from Model 1 can also be read per 3 days or per 1 day without fitting a new model. If the count ratio per five days is *R*, the count ratio per three days is *R*^(3/5) and the count ratio per one day is *R*^(1/5). Those are the same coefficient on a different scale, not a new model.

Other checks were the time-trend spline (3, 6, or 8 degrees of freedom in place of the Model 1 4-df spline, or year indicators in place of that spline). Those checks change the control for slow calendar time, not the length of a heatwave. Further checks were dropping the first 12 or 24 months; weather one or two months earlier; and dropping the most influential month. Cold-day models restricted to November–March are a labelled sensitivity.

Further checks used general-population × days as the offset (this is still a count ratio, not cohort incidence); maximum and minimum temperature in one model, or the three official extreme-day counts in one model; influenza on the 121 months with data; and nitrogen dioxide or PM2.5. Models that added pollution or influenza are extra checks. They are not replacements for Model 1.

Residual correlation was inspected with Pearson autocorrelation and Ljung–Box tests at lags 6 and 12.

Separately, we tested a published method for estimating daily temperature effects from monthly outcomes using simulated Hong Kong weather [20,21]. We did not apply that method to the hospital counts.

A labelled synthetic exercise on a 132-month count process, not on Hospital Authority rows, asked whether a constant thermal coefficient can look attenuated in a full-window fit when utilisation falls after month 84, when influenza-like co-circulation is zeroed after month 84, or when both occur. Those files are a methods warning. They are not Hong Kong count ratios and are not quoted as estimates.

### Software

Analyses were conducted in R 4.3.3 (2024-02-29). Negative-binomial models used `MASS::glm.nb` (MASS 7.3-60.0.1). Newey–West and HC1 standard errors used `sandwich` 3.1.3. Natural cubic splines used `splines::ns`.

## Results

### Outcome series

CHD contributed 156,156 first recorded hospitalisations over 132 months, a mean of 1,183.0 per month. HF contributed 29,681, a mean of 224.9 per month (Table 1). Annual totals fell by about half from 2013 to 2023 (CHD 23,830 to 12,323; HF 4,336 to 2,296), with a further dip in 2020 (CHD 10,237; HF 1,964). Over the same years, the interpolated Census and Statistics Department population aged 35 years or older rose by 17%. Mean monthly first-event counts were 1,315 for CHD and 252 for HF in 2013–2019, against 926 and 173 in 2020–2022. Figure 1 indexes both hospital series and the general-population series to 2013. The decline in first-event counts is compatible with depletion of the at-risk set in a 2013–2023 diagnosis window, together with pandemic changes in care-seeking. It is not a measure of physiological improvement. It does not quantify the share attributable to depletion without monthly still-at-risk person-time. Mean monthly HF counts were highest in January (287) and lowest in September (196). CHD showed a milder winter elevation (January 1,386; September 1,097). After calendar-month indicators, the thermal estimates ask whether a given January or July differs from a typical January or July, and not whether winter counts exceed summer counts.

**Table 1. Outcome summary.**

| Outcome | Period | Months | Total events | Mean per month | Event construction |
|:--|:--|---:|---:|---:|:--|
| Coronary heart disease | 2013–2023 | 132 | 156,156 | 1,183.0 | First recorded hospitalisation after first CHD diagnosis |
| Heart failure | 2013–2023 | 132 | 29,681 | 224.9 | First recorded hospitalisation after first HF diagnosis |

**Figure 1. First-event counts fell while the general population aged 35 years or older rose.** Index = 1 in 2013. CHD 23,830 → 12,323; HF 4,336 → 2,296. Source: governed Hospital Authority aggregate annual totals; Census and Statistics Department mid-year population aged 35 years or older. The figure does not measure consecutive hot or cold spells, and it is not a physiological series.

![Figure 1](../../figures/live_identification/figure_B_first_event_depletion.png)

### Exposure context

At HKO Headquarters, hot nights rose from 10 in 2013 to 61 in 2021 and 56 in 2023 [12]. The 2013 count was about seven days below the 1981–2010 normal [10]. The 2021 count was the highest annual number of hot nights in the Observatory record at that time [11]. Very hot days rose from 17 to 54 over the same 2013–2021 comparison, and were 54 in 2023 [12]. Cold days were 14 in 2013 and 14 in 2023, with 1 in 2019 and 13 in 2021 [12]. These are exposure counts, and not health effects. Mean official hot nights were 2.7 per month in 2013–2019 and 4.5 per month in 2020–2022. Figure 2 shows official cold days by year and month. Of 145 cold days in 2013–2023, 141 fell in December–February (December 40, January 54, February 47), and 4 fell in March. Twenty-nine of 132 months carried at least one official cold day. The year 2019 contributed a single cold day. After calendar-month indicators, the remaining cold-day variation is between-year winter variation, and not a summer-versus-winter contrast.

**Figure 2. Official cold days by year and month, Hong Kong Observatory Headquarters, 2013–2023.** Source: Hong Kong Observatory official daily cold-day flags (T~min~ ≤ 12 °C), aggregated to calendar months. Identification is between winters, not a consecutive-duration spell, and not a physiological mechanism.

![Figure 2](../../figures/live_identification/figure_A_cold_day_identification.png)

### Nested-window official-day panel

Table 2 reports the official-day Model 1 count ratios, per five additional such days in the month, for the full 132 months and for the nested 84 months. The 84 months are contained in the 132, so the two columns are not independent periods and their difference is not a fitted pre/post effect. Interval overlap between the two columns is not a test of a window difference. Figure 3 is the main identification display for this article, including trend-spline and COVID-phase rows.

The HF cold-day ratio was 1.113 (1.053–1.176) in the nested window and 1.073 (1.006–1.144) over the full window. Both intervals exclude 1 under Newey–West lag-6 reporting. The full-window estimate has *q* = 0.192. The CHD cold-day ratio excluded 1 only in the nested window (1.036, 1.007–1.067). In the full window it was 0.995 (0.949–1.043). The CHD hot-night ratio was 1.011 (0.991–1.032) in the nested window, an interval that includes 1, and 1.022 (1.002–1.042) in the full window (*q* = 0.192). COVID-phase indicators on the full sample moved the CHD hot-night ratio to 1.013 (0.994–1.033) and left the HF cold-day ratio at 1.074 (1.006–1.145). There is no 48-month post-2020 Model 1 table. Attenuation of a cold-day count ratio toward 1, or a hot-night ratio that appears only when the later years are included, is a change in a monthly count model. It is not a measure of physiological improvement.

Read as the ruling-out exhibit, the panel does not behave as a sufficient account of the window dependence would require. The cold-day ratios move in one direction between the windows, and the CHD hot-night ratio moves in the other. Official thermal extremes are therefore insufficient to explain why the fits depend on the window, and they are not thereby irrelevant to the fits.

**Table 2. Official-day count ratios in the full window and in the nested January 2013–December 2019 window (Newey–West lag-6).** Each estimate is the Model 1 count ratio per five additional official days in the month. The 84 nested months are contained in the 132. Benjamini–Hochberg *q*-values apply to the twelve full-window Model 1 fits only.

| Outcome | Exposure contrast | 2013–2023 (132 months) | Nested 2013–2019 (84 months) |
|:--|:--|--:|--:|
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042), *q* = 0.192 | 1.011 (0.991–1.032) |
| CHD | Very hot days / 5 days | 0.999 (0.974–1.025) | 0.997 (0.982–1.012) |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 1.036 (1.007–1.067) |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.965 (0.937–0.994) |
| HF | Very hot days / 5 days | 0.995 (0.963–1.028) | 0.990 (0.960–1.021) |
| HF | Cold days / 5 days | 1.073 (1.006–1.144), *q* = 0.192 | 1.113 (1.053–1.176) |

**Figure 3. Model 1 count ratios for official day counts across time-trend, window, and COVID-period specifications (Newey–West lag-6 intervals).** The exposure is the monthly official day count divided by five, so each estimate is the count ratio per five additional such days in that month. Rows labelled 3, 6, or 8 df replace the 4-df time-trend spline of Model 1. Neither the five-day scale nor the spline degrees of freedom refers to consecutive days. The nested window is January 2013–December 2019 (84 months). Continuous-temperature fits for the same specifications are a supplement, not a physiology panel.

![Figure 3](../../figures/live_identification/figure_D_trend_depletion_sensitivity.png)

### Twelve-fit thermal exhibit

Table 3 reports the twelve separate-exposure count ratios under the offset for the number of days in the month and Newey–West lag-6 intervals. It is the thermal exhibit, not the headline of this article.

**Table 3. Model 1: negative-binomial models with an offset for the number of days in the month and Newey–West lag-6 intervals.**

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

All twelve *q*-values exceeded 0.19, with a minimum of 0.192. No model meets a multiplicity-protected confirmatory threshold. The HF mean-minimum-temperature interval narrowly included 1, with an unrounded upper bound of 1.00005. For CHD, the continuous monthly temperature estimates were near null, between 0.993 and 0.994, whereas the official hot-night count estimate was larger under Newey–West lag-6 reporting. These encodings describe different monthly thermal questions. The contrast does not imply that a hot-night effect was missed by the means, and it is not a test of hourly nighttime excess heat [9]. For HF, the continuous temperature estimates were weakly inverse, and the cold-day count estimate was positive.

### Uncertainty ladder

**Table 4. Uncertainty ladder for the two leading exploratory contrasts.**

| Outcome and exposure | Model | HC1 | NW3 | NW6 |
|:--|:--|:--|:--|:--|
| CHD hot nights / 5 days | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.0003–1.0439) | 1.022 (1.002–1.042) |
| HF cold days / 5 days | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

For CHD hot nights, the model-based and HC1 intervals included 1, while both Newey–West intervals excluded 1 on the unrounded scale (lag 3: 1.000253 to 1.043860). The ladder narrowed from the model-based interval to the Newey–West intervals for that contrast. Robust intervals are not automatically wider, and the direction of that change is itself informative. For HF cold days, all four constructions excluded 1, and *q* remained 0.192. Concordance across standard-error methods does not create multiplicity protection. No interval was chosen because it excluded 1.

### Specification and diagnostic checks

Table 5 places mean temperature beside the official-day headlines in the same two windows. In the nested window, mean temperature was inversely associated with both outcomes (CHD 0.980, 0.970–0.990; HF 0.945, 0.927–0.963). In the same 84 months, official cold days were positively associated with both outcomes, and official hot nights were compatible with 1 for CHD and inverse for HF. COVID-phase indicators on the full sample moved mean temperature to 0.989 (0.975–1.003) for CHD and 0.967 (0.944–0.991) for HF. Continuous monthly temperature and official day counts are therefore not interchangeable encodings of the same contrast. Nine of the twelve Newey–West lag-6 intervals excluded 1 in the nested window, including inverse associations for all six continuous temperature contrasts. No multiplicity control was computed within that window, and no nested-window estimate is promoted beyond a labelled specification.

**Table 5. Mean temperature versus official-day encodings (Newey–West lag-6).**

| Outcome | Encoding | 2013–2023 | Nested 2013–2019 | COVID-phase indicators |
|:--|:--|--:|--:|--:|
| CHD | Mean temperature / 1 °C | 0.993 (0.976–1.010) | 0.980 (0.970–0.990) | 0.989 (0.975–1.003) |
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 1.011 (0.991–1.032) | 1.013 (0.994–1.033) |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 1.036 (1.007–1.067) | 0.991 (0.943–1.041) |
| HF | Mean temperature / 1 °C | 0.974 (0.947–1.002) | 0.945 (0.927–0.963) | 0.967 (0.944–0.991) |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.965 (0.937–0.994) | 0.994 (0.972–1.016) |
| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 1.113 (1.053–1.176) | 1.074 (1.006–1.145) |

After month and trend residualisation, maximum and minimum temperature retained a variance inflation factor of 4.66 when entered jointly. Hot nights and very hot days retained variance inflation factors near 1.96. In the joint extreme-day model, the CHD hot-night count ratio was 1.045 (1.015–1.075), compared with 1.022 in the separate model. The HF cold-day estimate was the same in the joint and separate models, at 1.073. Joint coefficients are diagnostics, and not preferred estimates.

Pearson residual autocorrelation at lag 1 was 0.508 in the CHD hot-night model and 0.146 in the HF cold-day model. Ljung–Box tests at lag 6 gave *p* < 10^−7^ for every CHD Model 1 fit and *p* > 0.3 for every HF Model 1 fit. Serial dependence is part of the inferential problem for CHD, which is why the four-construction ladder is shown rather than a single interval.

Across trend, window, and COVID-phase specifications, the CHD hot-night ratio ranged from 1.011 to 1.025, and the HF cold-day ratio from 1.043 to 1.113 (Figure 3). For CHD hot nights, the 6-df and 8-df intervals exclude 1 (1.024, 1.005–1.044; 1.023, 1.005–1.042). The 3-df interval includes 1 (1.011, 0.990–1.032). The year-indicator interval has the highest point estimate of the trend checks and includes 1 (1.025, 0.9998–1.050). No trend specification is preferred over the 4-df spline in Model 1. For HF cold days, the 8-df interval includes 1 (1.062, 0.994–1.135). Lag-1 month models attenuated the CHD hot-night association toward 1 (1.010, 0.979–1.042). The HF cold-day association remained elevated at lag 1 (1.073, 1.014–1.135) and was weaker at lag 2 (1.053, 0.985–1.127). Lag-one month is a labelled sensitivity, and it is not a daily lag curve. The months with largest Cook’s distance were February 2020 for CHD and February 2022 for HF cold days. Excluding the most influential month left both exploratory directions unchanged (CHD hot nights 1.021, 1.001–1.040; HF cold days 1.088, 1.034–1.144).

The simulated daily-recovery method failed its worst-cell criteria: null Type I error ranged from 0.048 to 0.150, minimum coverage was 0.840, maximum non-null relative bias was 32.8, and the maximum moderate false-sign rate was 0.808. No real daily coefficient is reported.

## Discussion

The extract shows window dependence, not a protected thermal discovery. Annual first events fell by roughly half (CHD 23,830 to 12,323; HF 4,336 to 2,296, with a 2020 dip to 10,237 and 1,964) while the general population aged 35 years or older rose 17%. Cold-day point estimates were larger in the nested 84 months than in the full 132 (HF 1.113 vs 1.073; CHD 1.036 vs 0.995), with overlapping intervals. The CHD hot-night interval excluded 1 only in the full window (1.022, 1.002–1.042; nested: 1.011, 0.991–1.032). All twelve full-window Model 1 *q*-values exceeded 0.19, so neither estimate is a confirmatory primary.

Three labelled rivals can produce that pattern. They are not mixed into one mechanism paragraph.

**Utilisation.** Neighbouring Hong Kong files show fewer hospitalisations and more cardiovascular deaths in 2020 [1–4]. Emergency-department visits fell and 28-day mortality among attenders rose [2,3]. Self-reported avoidance of consultation was common [4]. ST-elevation myocardial infarction care was delayed [5,6]. Those patterns are consistent with reduced care-seeking and system shock. They predict fewer first recorded hospitalisations in a monthly Hospital Authority series without requiring a quieter myocardium. They do not identify how much of Table 1 is delayed presentation. They do not license reading the count drop as recovered health.

**Depletion.** The event is a first hospitalisation after a first CHD or HF diagnosis inside a 2013–2023 diagnosis window. People who have already had that first event cannot contribute another. Absent monthly still-at-risk person-time, the decline in Figure 1 is compatible with a shrinking risk set, with avoided care, or with both [14]. It is not incidence in the territory, and it is not a measure of physiological improvement.

**Weather-entanglement.** Official hot nights were more frequent in the same years in which care-seeking changed (2.7 per month in 2013–2019; 4.5 per month in 2020–2022). The CHD hot-night residual needs those later years. The same 4-df spline that absorbs the first-event decline also absorbs the hot-night trend. That is an identification problem, not evidence that hot nights caused the count drop. Official cold days remain a winter-to-winter contrast (141 of 145 days in December–February; 29 of 132 months carry any). Weather is therefore insufficient as an account of the window dependence, and it is not irrelevant to the fit. Continuous mean temperature in the nested window is inverse for both outcomes and is not a substitute for the official-day encoding (Table 5).

Three neighbouring literatures bound what these three rivals can be asked to carry. Daily cardiac-admission studies do not rescue a monthly first-event claim: Goggins and Chan's cumulative relative risk comparing 11 °C with 25 °C is not a monthly count ratio per five official cold days, and it is not imported into Table 2 or Table 3 [8]. Guo et al. reported no overall association for the official hot-night flag after adjustment for mean temperature, so a difference between monthly means and monthly official counts does not identify an intensity mechanism [9]. Liu et al. (2020, 2026) remain complementary mortality baselines whose attributable fractions and excess-death totals cannot be rescaled into the present count ratios [22,23]. Physiological accounts of overnight recovery and cold-related afterload, and any mapping onto heat–health action-plan elements, are not identified by 132 monthly counts and are left to the supplement.

Two limits of this extract remain unresolved rather than adjudicated. Influenza covers 121 of 132 months and is a sensitivity, not Model 1; a labelled synthetic count process, not this Hospital Authority panel, shows that a full-window coefficient can look attenuated when utilisation or an influenza-like term collapses after month 84 while the true coefficient is held constant. Pollution declined across the decade [13], and that co-trend is slow rather than a 2020-only switch, so confounding by infection or ozone is unresolved in Model 1.

## Conclusion

In this 2013–2023 first-event extract, monthly CHD and HF counts fell, and cold-day count ratios were stronger in the nested 84 months than in the full window. Official hot nights and cold days do not supply a sufficient account of that window dependence. They remain part of the exposure record. The data do not show that health recovered after 2020, and they do not support a multiplicity-protected differential thermal claim. What the file supports is a window-dependent count ratio for a first hospitalisation after a first diagnosis, without admission cause and without person-time.

## Strengths and limitations

**Strengths.** The analysis window is treated as part of the estimand rather than as a nuisance to be averaged through. Official-day ratios are shown for both the full window and the nested 84-month specification. All twelve full-window Model 1 fits are reported. Uncertainty is shown as a four-construction ladder. Figure 1 and Figure 3 display the two objects the thesis needs: the first-event decline and the dependence of each official-day ratio on the window and the time smooth.

**Limitations.** Admission cause was not recorded, so an event is a first hospitalisation after a first diagnosis and not a cardiac-caused admission. Monthly counts of people still at risk of a first event were unavailable, so the estimates are count ratios rather than incidence-rate ratios [14]. Laboratory series were not delivered. The design is ecological and monthly, so individual-level and daily-triggering interpretations are not identified [14]. Monthly official-day totals cannot identify consecutive duration. Age, sex, and disease-subtype strata were not delivered. Residual serial correlation remains material for CHD, with lag-1 Pearson autocorrelation of 0.508 in the hot-night model. Official cold days are concentrated in December–February, and only 29 of 132 months carry any official cold day. The CHD hot-night estimate is compatible with 1 in the nested window. There is no post-only 48-month Model 1 table. Official hot-night counts are not hourly nighttime excess heat [9]. All exposures were measured at a single Observatory station and applied territory-wide. Influenza is missing for January–October 2013. Confounding by pollution, humidity, rainfall, and influenza is unresolved in Model 1. A corresponding stroke series was not available. Influence months include February 2020 for CHD and February 2022 for HF cold days. Physiological mechanisms are not identified from the 132 months.

## Declaration on the use of AI

AI-assisted tools were used for code scaffolding, methodological brainstorming, and review of potential data and modelling issues. Scientific claims and numerical results were checked against Hospital Authority monthly counts and the live weather paragraph.

## Declaration of competing interest

The authors declare no competing interests.

## Acknowledgements

None.

## Data and code availability

Code is at https://github.com/bobshenruililin/Laidlaw-Heat-Project. Monthly hospital counts are not posted. What may be shared later depends on ethics approval. This file is a candidate article on the COVID-period track. It does not overwrite the parked thermal manuscript.

## References

1. Xin H, Wu P, Wong JY, et al. Hospitalizations and mortality during the first year of the COVID-19 pandemic in Hong Kong, China: a retrospective observational study. *Lancet Reg Health West Pac*. 2022;21:100645. doi:10.1016/j.lanwpc.2022.100645
2. Wai AKC, Wong CKH, Wong JYH, et al. Changes in emergency department visits, diagnostic groups, and 28-day mortality associated with the COVID-19 pandemic. *Ann Emerg Med*. 2022;79(2):148-157. doi:10.1016/j.annemergmed.2021.09.424
3. Wai AKC, Yip TF, Wong YH, et al. The effect of the COVID-19 pandemic on non–COVID-19 deaths: a cohort study. *JMIR Public Health Surveill*. 2024;10:e41792. doi:10.2196/41792
4. Hung KK, Walline JH, Chan EYY, et al. Health service utilization in Hong Kong during the COVID-19 pandemic: a cross-sectional public survey. *Int J Health Policy Manag*. 2022;11(4):508-513. doi:10.34172/ijhpm.2020.183
5. Tam CCF, Cheung KS, Lam S, et al. Impact of coronavirus disease 2019 (COVID-19) outbreak on ST-segment–elevation myocardial infarction care in Hong Kong, China. *Circ Cardiovasc Qual Outcomes*. 2020;13(4):e006631. doi:10.1161/CIRCOUTCOMES.120.006631
6. Tam CCF, Cheung KS, Lam S, et al. Impact of coronavirus disease 2019 (COVID-19) outbreak on outcome of myocardial infarction in Hong Kong, China. *Catheter Cardiovasc Interv*. 2021;97(2):E194-E197. doi:10.1002/ccd.28943
7. Goggins WB, Chan EYY, Yang CY. Weather, pollution, and acute myocardial infarction in Hong Kong and Taiwan. *Int J Cardiol*. 2013;168(1):243-249. doi:10.1016/j.ijcard.2012.09.087
8. Goggins WB, Chan EYY. A study of the short-term associations between hospital admissions and mortality from heart failure and meteorological variables in Hong Kong. *Int J Cardiol*. 2017;228:537-542. doi:10.1016/j.ijcard.2016.11.106
9. Guo YT, Chan KH, Qiu H, Wong ELY, Ho KF. The risk of hospitalization associated with hot nights and excess nighttime heat in a subtropical metropolis: a time-series study in Hong Kong, 2000–2019. *Lancet Reg Health West Pac*. 2024;51:101168. doi:10.1016/j.lanwpc.2024.101168
10. Hong Kong Observatory. The Year's Weather — 2013. https://www.hko.gov.hk/en/wxinfo/pastwx/ywx2013.htm
11. Hong Kong Observatory. The Year's Weather — 2021. https://www.hko.gov.hk/en/wxinfo/pastwx/2021/ywx2021.htm
12. Hong Kong Observatory. Hong Kong Observatory Open Data. https://www.hko.gov.hk/en/abouthko/opendata_intro.htm
13. Environmental Protection Department. Environmental Protection Interactive Centre: Air Quality Data. https://cd.epic.epd.gov.hk/EPICDI/air/station/?lang=en
14. Greenland S, Morgenstern H. Ecological bias, confounding, and effect modification. *Int J Epidemiol*. 1989;18(1):269-274. doi:10.1093/ije/18.1.269
15. Census and Statistics Department. Population by Sex and Age Group (Table 110-01001). https://data.gov.hk/en-data/dataset/hk-censtatd-tablechart-110-01001
16. Bhaskaran K, Gasparrini A, Hajat S, Smeeth L, Armstrong B. Time series regression studies in environmental epidemiology. *Int J Epidemiol*. 2013;42(4):1187-1195. doi:10.1093/ije/dyt092
17. Newey WK, West KD. A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*. 1987;55(3):703-708. doi:10.2307/1913610
18. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J R Stat Soc Series B*. 1995;57(1):289-300. doi:10.1111/j.2517-6161.1995.tb02031.x
19. Chan EYY, Goggins WB, Yue JSK, Lee P. Hospital admissions as a function of temperature, other weather phenomena and pollution levels in an urban setting in China. *Bull World Health Organ*. 2013;91(8):576-584. doi:10.2471/BLT.12.113035
20. Basagaña X, Ballester J. Unbiased temperature-related mortality estimates using weekly and monthly health data: a new method for environmental epidemiology and climate impact studies. *Lancet Planet Health*. 2024;8(10):e766-e777. doi:10.1016/S2542-5196(24)00212-2
21. Basagaña X, Ballester J. Unbiased estimates using temporally aggregated outcome data in time series analysis: generalization to different outcomes, exposures, and types of aggregation. *Epidemiology*. 2026;37(1):16-20. doi:10.1097/EDE.0000000000001923
22. Liu J, Hansen A, Varghese B, et al. Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016. *Sustain Cities Soc*. 2020;57:102131. doi:10.1016/j.scs.2020.102131
23. Liu Z, Ren C, Liu J, Kawasaki Y, Bishai DM. Modelling the excess mortality associated with heat waves in Hong Kong: 2014–2023. medRxiv. 2026. doi:10.64898/2026.03.05.26347683
