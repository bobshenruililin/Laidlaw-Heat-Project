# Window dependence of first-hospitalisation counts after first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension, Hong Kong, 2013–2023: official-day ratios as a ruling-out exhibit

*Running title:* Window dependence of first-event counts: official-day exhibit

*Candidate article. Estimates are the parked Model 1 and nested-window checks. A confirmatory freeze has not been declared. The thesis is the analysis window, not a new thermal discovery.*

Bob Ruililin Shen^1^, Author 2^1^, Author 3^1^, Author 4^1^, David Makram Bishai^1^

^1^ School of Public Health, Li Ka Shing Faculty of Medicine, The University of Hong Kong, Hong Kong SAR, China

## Abstract

**Background.** Among people with type 2 diabetes and/or hypertension in Hong Kong, the counted event is the first recorded hospitalisation after a first diagnosis of coronary heart disease (CHD) or heart failure (HF). Admission cause was not recorded. Monthly first-event counts fell by about half between 2013 and 2023. Most of that decline was already in place by 2019. 2020 was a trough. 2023 returned toward 2019, not toward 2013. Neighbouring Hong Kong series report fewer public hospitalisations and more cardiovascular deaths in 2020; those papers describe the trough, not the 2013–2019 path. This paper reports two objects from one extract: the path of those first-event counts, and Model 1 official-day count ratios on the full 132 months and on the nested 84 months to December 2019, carried as a ruling-out exhibit.

**Methods.** We analysed 132 territory-months (January 2013–December 2023) of monthly counts of first hospitalisation after a first diagnosis of coronary heart disease (CHD; 156,156 events) or heart failure (HF; 29,681 events) among people with type 2 diabetes and/or hypertension. Admission cause was not recorded. The first object is that count path. The ruling-out exhibit is the Model 1 official-day count ratio on the full 132 months and on the nested 84 months from January 2013 to December 2019. Those 84 months are contained in the 132. The nested specification is an overlapping-sample refit, not a period contrast. Model 1 is a separate negative-binomial model for each of three continuous temperature measures and the official counts of hot nights, very hot days, and cold days, with calendar-month indicators, a 4-df time spline, and an offset for the number of days in the month. Official-day exposures use \(I(\mathrm{count}/5)\) as a reporting scale, read per five additional such days in a month. Intervals used model-based, HC1, and Newey–West lag-3 and lag-6 constructions. Displayed official-day intervals in the text use the lag-6 construction as a display convention, not because that interval excludes 1. Benjamini–Hochberg *q*-values were computed from the twelve full-window Newey–West lag-6 Wald *p* values only. Nested-window intervals have no multiplicity control. No 48-month post-2020 Model 1 table is reported.

**Results.** Annual first-event totals about halved from 2013 to 2023 (CHD 23,830 to 12,323; HF 4,336 to 2,296). Most of that decline was already present by 2019 (CHD 12,396; HF 2,344). 2020 was a trough (CHD 10,237; HF 1,964); 2023 returned toward 2019. The Census and Statistics Department population aged 35 years or older rose by 17% and is not the still-at-risk set. Official-day count-ratio point estimates moved with the window. The HF cold-day ratio per five days was 1.113 (1.053–1.176) in the nested 84 months and 1.073 (1.006–1.144) in the full 132; the CHD cold-day ratio was 1.036 (1.007–1.067) nested and 0.995 (0.949–1.043) full. Those cold-day points moved toward 1 when the later years were added. The CHD hot-night ratio was 1.011 (0.991–1.032) in the nested window and 1.022 (1.002–1.042) in the full window; the larger full-window point appears only when the later years are included. For that full-window CHD hot-night contrast, the model-based interval 1.022 (0.995–1.049) and the HC1 interval 1.022 (0.997–1.047) include 1; the displayed lag-6 interval does not. Nested-window intervals have no multiplicity control and are not a test of a window difference. Continuous mean temperature was inverse in the nested window for both outcomes (CHD 0.980, 0.970–0.990; HF 0.945, 0.927–0.963). Official day counts and monthly means are not interchangeable encodings. All twelve full-window *q*-values exceeded 0.19; the two full-window official-day rows above have *q* = 0.192.

**Conclusions.** First-event counts and official-day count ratios in this extract depend on the window analysed. Official thermal extremes are insufficient to account for that dependence. They remain part of the exposure record. The decline in first events is not a measure of physiological improvement. Estimates remain ecological monthly count ratios for a first-event outcome without recorded admission cause.

**Keywords:** analysis window; first hospitalisation; coronary heart disease; heart failure; Hong Kong; cold days; hot nights

## Introduction

The 2013–2023 window in Hong Kong is not a homogeneous decade for a hospital count. The counted event is the first recorded hospitalisation after a first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension. Admission cause was not recorded. Annual totals about halved from 2013 to 2023, but most of that decline was already in place by 2019. 2020 was a trough on that lower base. 2023 returned toward 2019, not toward 2013. Type 2 diabetes and hypertension diagnoses still enter through 2023, so the interval is not a closed 2013 cohort; early-year counts can include first-in-window events without a specified washout. Any monthly count of those first events therefore mixes weather, care-seeking, and a shrinking set still able to contribute a first recorded stay. A thermal coefficient estimated on the whole window inherits that mixture.

Hong Kong studies of 2020 describe fewer cardiovascular admissions, not fewer cardiovascular events. Xin et al. reported fewer public hospitalisations in 2020, including cardiovascular admissions, together with additional deaths, particularly cardiovascular deaths and deaths outside public hospitals [1]. That composite is not a CHD–HF–stroke MACE from this extract, and stroke was not attached. Wai et al. found fewer emergency-department visits in January–August 2020 than in the same months of 2019, and higher 28-day mortality among those who did attend [2]. A later Wai et al. cohort of non-COVID deaths likewise paired fewer emergency visits with higher 28-day mortality [3]. Hung et al. documented self-reported avoidance of consultation in a public survey [4]. Tam et al. reported longer delays to ST-elevation myocardial infarction care in a Hong Kong service in early 2020 [5,6]. Those papers are utilisation and delay series from 2020. They are not this type 2 diabetes and/or hypertension first-event construction, they are not AMI or STEMI, and their counts are not imported into the tables below. They can speak to the 2020 trough. They cannot speak to the 2013–2019 decline, and they do not cover February 2022.

Local thermal evidence answers a different question. Goggins et al. analysed daily cause-coded acute myocardial infarction admissions in 2000–2009 [7]. This extract is not AMI and has no admission cause. Goggins and Chan analysed daily public-hospital heart-failure admissions and deaths, allowing repeats, during 2002–2011 [8]. Guo et al. analysed daily unplanned emergency hospitalisations in the hot seasons of 2000–2019 [9]. After adjustment for multi-day mean temperature, the official hot-night indicator showed no overall association with non-cancer, non-external hospitalisation over lags 0–4 days, while an hourly nighttime excess-heat metric did [9]. Those studies estimate daily risk for cause-coded or unplanned admissions. This extract is year-round monthly first events through 2023, without admission cause. Their coefficients do not transfer to monthly counts of first hospitalisation after a first CHD or HF diagnosis. After calendar-month indicators, official cold days here are a between-year winter residual (141 of 145 days in December–February; 29 of 132 months carry any), not a within-season daily temperature slope. They do not identify why a 2013–2019 count ratio would differ from a 2013–2023 fit.

The Observatory record for the same years is unambiguous as climatology. Hot nights at Headquarters rose from 10 in 2013 to 61 in 2021 and 56 in 2023 [10,11,12]. Very hot days rose from 17 to 54 over the 2013–2021 comparison and were 54 in 2023 [11,12]. Cold days were 14 in 2013 and 14 in 2023, with 1 in 2019 and 13 in 2021 [10,11,12]. Air pollution also moved: at general monitoring stations, mean nitrogen dioxide declined from 53.7 µg m^−3^ in 2013 to 32.1 µg m^−3^ in 2023, and fine particulate matter (PM2.5) from 30.8 to 14.6 µg m^−3^, while ozone rose from 42.6 to 58.3 µg m^−3^ [13]. Those series describe the window. They do not, by themselves, explain a first-event count ratio.

This study therefore reports two objects from one extract. The first is the path of the monthly first-hospitalisation counts. The second is the Model 1 count ratio for official hot nights, very hot days, and cold days, shown for the full 132 months and for the nested 84 months that stop at December 2019. Those 84 months are contained in the 132; the nested fit is an overlapping-sample refit, not a period contrast. The official-day ratios are carried as a ruling-out exhibit for the first object. Nested containment means that a constant thermal coefficient need not be invariant once utilisation or depletion after 2019 is present, so stability of the ratios is a weak falsifier. What can be shown is whether official-day point estimates move in the same direction, and whether monthly mean temperature tells the same story as the official day counts. All twelve full-window Model 1 fits are reported so that the exhibit is not a selected pair of rows.

## Methods

The study is an ecological territory-month time series for January 2013 through December 2023 (132 months). It cannot show effects for individual people, the cause of any admission, or day-level triggering [14]. The study was approved by the Institutional Review Board (IRB) of the HKU/Hospital Authority HK West Cluster (IRB reference number: UW XX-XXX).

### Data sources

#### Health data

The dependent variable is the monthly count of first hospitalisations after a first diagnosis of coronary heart disease (CHD), and separately of heart failure (HF), among people with type 2 diabetes and/or hypertension in Hong Kong during 2013–2023. For each person, the event is the first recorded hospitalisation after that person’s first CHD or HF diagnosis. Admission cause was not recorded. The monthly transfer does not specify a look-back or washout, whether the index stay is the diagnosis episode or a later any-cause stay, the ICD list, or whether the count includes day-procedure or emergency-department records. Age and sex strata were not included. Laboratory measurements were not in the transfer and are not analysed.

Monthly influenza activity from November 2013 through December 2023 was obtained from Centre for Health Protection Flu Express summaries. January–October 2013 had no influenza values. Those months were left missing and were not coded as zero. Influenza was therefore not entered in Model 1; it is a sensitivity on the 121 months with data.

#### Weather and pollutants data

Meteorological data was obtained from the HKO. The monthly variables included: temperature (mean, minimum, maximum), relative humidity, total rainfall, the number of hot nights (T~min~ ≥ 28°C), the number of very hot days (T~max~ ≥ 33°C), the number of extremely hot days (T~max~ ≥ 35°C), and the number of cold days (T~min~ ≤ 12°C). Monthly mean pollutant levels for nitrogen dioxide (NO~2~), sulfur dioxide (SO~2~), and ozone (O~3~) were obtained from the Hong Kong Environmental Protection Department (EPD). All monthly data were derived by taking the average of daily data in each calendar month.

A station-month entered a pollutant mean only when at least 75% of expected observations were present. Missing measurements were not coded as zero. Territory-wide monthly pollutant concentrations are unweighted means of general EPD stations. Roadside monitors were not used for those means. Fine particulate matter (PM~2.5~) from the same general stations was assembled for sensitivity analysis only.

#### Population

Mid-year age- and sex-specific population estimates from the Census and Statistics Department (Table 110-01001) were interpolated to month mid-points [15]. Those figures describe the general population, not the type 2 diabetes and/or hypertension group still at risk of a first CHD or HF hospitalisation. Model 1 therefore uses the number of days in the month as the offset and is read as a monthly count ratio, not as a cohort incidence rate [14]. A population × days offset is a sensitivity only. It does not turn the estimate into cohort incidence.

### Statistical analysis

Let \(Y_t\) be the hospital count in month \(t\). Model 1 is a negative-binomial regression [16]:

\[
\log \mathrm{E}(Y_t) = \log(d_t) + \alpha + \beta X_t + \sum_{m=2}^{12} \gamma_m I(\mathrm{month}_t = m) + s(t; 4~\mathrm{df}). \tag{1}
\]

Here \(d_t\) is the number of days in month \(t\); \(\alpha\) is the intercept; \(X_t\) is one weather variable; \(\beta\) is the coefficient for that weather variable; \(I(\mathrm{month}_t = m)\) is 1 if month \(t\) is calendar month \(m\) and 0 otherwise (January is the reference month); \(\gamma_m\) is the calendar-month coefficient relative to January; and \(s(t; 4~\mathrm{df})\) is a 4-df time smooth. The estimate we report is \(\mathrm{e}^{\beta}\), the ratio of expected monthly counts for a 1 °C change in a temperature variable or a five-day change in an official day count.

We fitted Model 1 twelve times: six weather variables × two diagnoses. The six weather variables are monthly mean temperature, monthly mean daily maximum temperature, monthly mean daily minimum temperature, hot nights, very hot days, and cold days. Extreme-day counts were divided by 5 so that each estimate is the change associated with five extra such days in that month, rather than with one extra day. Five days is a convenient scale, not a new weather threshold and not a consecutive-duration rule. The official count of extremely hot days (T~max~ ≥ 35°C) was obtained with the other monthly weather variables and was not used as a temperature variable in Model 1. Each Model 1 fit contains one temperature variable. Temperature terms are not entered together in Model 1. We used a negative-binomial model because monthly counts can vary more than a Poisson model permits. A quasi-Poisson model is a sensitivity.

We report 95% confidence intervals in four ways: the model’s own standard errors, HC1, Newey–West with a lag of 3 months, and Newey–West with a lag of 6 months [17]. Displayed official-day intervals in the text and in Table 2 use the lag-6 construction as a display convention, not because that interval excludes 1. The four-construction ladder is always shown for CHD hot nights and HF cold days (Table 5). No interval is chosen because it excludes 1. Multiplicity-adjusted *q*-values were computed from the twelve full-window Newey–West lag-6 Wald *p* values only, not from model-based *p* [18]. Nested-window, COVID-phase, spline-df, influence-month, and joint-model fits are outside that family.

The nested specification repeats equation (1) on January 2013–December 2019 (84 months contained in the 132). This is an overlapping-sample refit: month factors and the 4-df spline are re-estimated, with knots on the subset. The difference is not a fitted pre/post effect. No exposure × period interaction was fitted, and no 48-month post-2020 Model 1 table is reported. COVID-period indicators on the full sample (through January 2020; February 2020–December 2021; January–April 2022; May–December 2022; from January 2023) are five intercept levels, a full-sample adjustment rather than a third window. They do not replace Model 1.

Model 2 additionally adds monthly mean relative humidity [8] and monthly total rainfall [19] to Model 1. Model 3 counts, for each month, the days whose daily mean temperature was above or below the historical average for that day of the year. Model 2 and Model 3 are specified and are not reported as headline estimates. No Model 3 health coefficients are reported.

### Sensitivity analysis

Official day-count estimates from Model 1 can also be read per 3 days or per 1 day without fitting a new model. If the count ratio per five days is *R*, the count ratio per three days is *R*^(3/5) and the count ratio per one day is *R*^(1/5). Those are the same coefficient on a different scale, not a new model.

Other checks were the time-trend spline (3, 6, or 8 degrees of freedom in place of the Model 1 4-df spline, or year indicators in place of that spline); dropping the first 12 or 24 months; weather one or two months earlier; and dropping the most influential month. Those checks change the control for slow calendar time, not the length of a heatwave. Cold-day models restricted to November–March are a labelled sensitivity. Further checks used general-population × days as the offset (still a count ratio, not cohort incidence); maximum and minimum temperature in one model, or the three official extreme-day counts in one model; influenza on the 121 months with data; and nitrogen dioxide or PM2.5. Models that added pollution or influenza are extra checks, not replacements for Model 1.

Residual correlation was inspected with Pearson autocorrelation and Ljung–Box tests at lags 6 and 12.

Separately, we tested a published method for estimating daily temperature effects from monthly outcomes using simulated Hong Kong weather [20,21]. We did not apply that method to the hospital counts.

A labelled synthetic exercise on a 132-month count process, not on Hospital Authority rows, asked whether a constant thermal coefficient can look attenuated in a full-window fit when utilisation falls after month 84, when influenza-like co-circulation is zeroed after month 84, or when both occur. Those files are a methods warning. They are not Hong Kong count ratios and are not quoted as estimates.

### Software

Analyses were conducted in R 4.3.3 (2024-02-29). Negative-binomial models used `MASS::glm.nb` (MASS 7.3-60.0.1). Newey–West and HC1 standard errors used `sandwich` 3.1.3. Natural cubic splines used `splines::ns`.

## Results

### Outcome series

CHD contributed 156,156 first recorded hospitalisations over 132 months, a mean of 1,183.0 per month. HF contributed 29,681, a mean of 224.9 per month (Table 1).

**Table 1. Outcome summary.**

| Outcome | Period | Months | Total events | Mean per month | Event construction |
|:--|:--|---:|---:|---:|:--|
| Coronary heart disease | 2013–2023 | 132 | 156,156 | 1,183.0 | First recorded hospitalisation after first CHD diagnosis; admission cause not recorded; not principal diagnosis; not AMI |
| Heart failure | 2013–2023 | 132 | 29,681 | 224.9 | First recorded hospitalisation after first HF diagnosis; admission cause not recorded; not principal diagnosis; not AMI |

Annual totals were highest in 2013 (CHD 23,830; HF 4,336), already near half by 2019 (CHD 12,396; HF 2,344), lowest in 2020 (CHD 10,237; HF 1,964), and in 2023 had returned toward 2019 (CHD 12,323; HF 2,296). Over the same years, the interpolated Census and Statistics Department population aged 35 years or older rose by 17%. That series is not the type 2 diabetes or hypertension group still at risk of a first event, and Figure 1 is not an incidence series. Figure 1 indexes both hospital series and the general-population series to 2013. The decline in first-event counts is not a measure of physiological improvement. It does not quantify depletion without monthly still-at-risk person-time. Mean monthly HF counts were highest in January (287) and lowest in September (196). CHD showed a milder winter elevation (January 1,386; September 1,097). After calendar-month indicators, the thermal estimates ask whether a given January or July differs from a typical January or July. They do not ask whether winter counts exceed summer counts.

**Figure 1. First-event counts fell while the general population aged 35 years or older rose.** Index = 1 in 2013. CHD 23,830 (2013) → 12,396 (2019) → 10,237 (2020) → 12,323 (2023); HF 4,336 → 2,344 → 1,964 → 2,296. Source: governed Hospital Authority aggregate annual totals; Census and Statistics Department mid-year population aged 35 years or older. The Census series is not the still-at-risk set. The figure does not measure consecutive hot or cold spells, and it is not a physiological series.

![Figure 1](../../figures/live_identification/figure_B_first_event_depletion.png)

### Exposure context

At HKO Headquarters, hot nights rose from 10 in 2013 to 61 in 2021 and 56 in 2023 [12]. The 2013 count was about seven days below the 1981–2010 normal [10]. The 2021 count was the highest annual number of hot nights in the Observatory record at that time [11]. Very hot days rose from 17 to 54 over the same 2013–2021 comparison, and were 54 in 2023 [12]. Cold days were 14 in 2013 and 14 in 2023, with 1 in 2019 and 13 in 2021 [12]. These are exposure counts, and not health effects. Mean official hot nights were 2.7 per month in 2013–2019 and 4.5 per month in 2020–2022. Figure 2 shows official cold days by year and month. Of 145 cold days in 2013–2023, 141 fell in December–February (December 40, January 54, February 47), and 4 fell in March. Twenty-nine of 132 months carried at least one official cold day. The year 2019 contributed a single cold day. After calendar-month indicators, the remaining cold-day variation is between-year winter variation, and not a summer-versus-winter contrast.

**Figure 2. Official cold days by year and month, Hong Kong Observatory Headquarters, 2013–2023.** Source: Hong Kong Observatory official daily cold-day flags (T~min~ ≤ 12 °C), aggregated to calendar months. Identification is between winters, not a consecutive-duration spell, and not a physiological mechanism.

![Figure 2](../../figures/live_identification/figure_A_cold_day_identification.png)

### Nested-window official-day panel

Table 2 reports the official-day Model 1 count ratios, per five additional such days in the month, for the full 132 months and for the nested 84 months. The 84 months are contained in the 132. The nested specification is an overlapping-sample refit: calendar-month factors and the 4-df spline are re-estimated, and spline knots follow the subset. The two columns are not independent periods, and their difference is not a fitted pre/post effect. Interval overlap between the two columns is not a test of a window difference, and discordance of whether 1 is excluded is not such a test. Figure 3 is the ruling-out exhibit for official-day encodings across trend-spline, window, and COVID-phase specifications. Figure 1 is the count-path object.

Point estimates moved. The HF cold-day ratio was 1.113 (1.053–1.176) in the nested window and 1.073 (1.006–1.144) over the full window. The CHD cold-day ratio was 1.036 (1.007–1.067) in the nested window and 0.995 (0.949–1.043) in the full window. The CHD hot-night ratio was 1.011 (0.991–1.032) in the nested window and 1.022 (1.002–1.042) in the full window. Cold-day points moved toward 1 when the later years were added; the CHD hot-night point was larger only in the full window. HF hot nights moved from 0.965 (0.937–0.994) in the nested window to 1.003 (0.976–1.031) in the full window, the opposite of CHD hot nights. Displayed lag-6 intervals are a convention, not a window test. For full-window CHD hot nights the lag-6 interval is 1.022 (1.002–1.042) and excludes 1, while the model-based 1.022 (0.995–1.049) and HC1 1.022 (0.997–1.047) intervals include 1 (Table 5). Both full-window official-day rows in Table 2 have *q* = 0.192. Nested-window intervals have no multiplicity control. COVID-phase intercepts on the full sample, an adjustment rather than a third window, moved the CHD hot-night ratio to 1.013 (0.994–1.033) and left the HF cold-day ratio at 1.074 (1.006–1.145). Extra time steps can absorb a slow hot-night trend; that is overcontrol, not a period effect. There is no 48-month post-2020 Model 1 table. Movement of a monthly count-ratio point estimate is not a measure of physiological improvement.

The exhibit that can be read from Table 2 and Table 3 is that official-day point estimates are not invariant to the window, that cold-day and CHD hot-night points move in opposite directions, and that nested-window mean temperature is not the same contrast as official day counts. That is not a formal test of a window difference. Attenuation of the HF cold-day point toward 1 is predicted if utilisation falls after month 84 while a thermal coefficient is constant, so that movement is not a disproof of weather. Official thermal extremes are therefore insufficient to explain why the fits depend on the window, and they are not thereby irrelevant to the fits.

**Table 2. Official-day count ratios in the full 132-month window and in the nested 84-month overlapping refit (Newey–West lag-6 display).** Each estimate is the Model 1 count ratio per five additional official days in the month. The nested 84 months are contained in the 132; the columns are not a period contrast. Benjamini–Hochberg *q*-values apply to the twelve full-window Newey–West lag-6 Wald *p* values only.

| Outcome | Exposure contrast | Full 132 months | Nested 84 ⊂ 132 (not a period effect) |
|:--|:--|--:|--:|
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042), *q* = 0.192 | 1.011 (0.991–1.032) |
| CHD | Very hot days / 5 days | 0.999 (0.974–1.025) | 0.997 (0.982–1.012) |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 1.036 (1.007–1.067) |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.965 (0.937–0.994) |
| HF | Very hot days / 5 days | 0.995 (0.963–1.028) | 0.990 (0.960–1.021) |
| HF | Cold days / 5 days | 1.073 (1.006–1.144), *q* = 0.192 | 1.113 (1.053–1.176) |

**Figure 3. Model 1 count ratios for official day counts across time-trend, window, and COVID-period specifications (Newey–West lag-6 intervals).** The exposure is the monthly official day count divided by five, so each estimate is the count ratio per five additional such days in that month. Rows labelled 3, 6, or 8 df replace the 4-df time-trend spline of Model 1. Neither the five-day scale nor the spline degrees of freedom refers to consecutive days. The nested window is January 2013–December 2019 (84 months), an overlapping-sample refit, not a period contrast. Continuous-temperature fits for the same specifications are a labelled check, not a physiology panel.

![Figure 3](../../figures/live_identification/figure_D_trend_depletion_sensitivity.png)

Table 3 places mean temperature beside the official-day headlines in the same two windows. In the nested window, mean temperature was inversely associated with both outcomes (CHD 0.980, 0.970–0.990; HF 0.945, 0.927–0.963). In the same 84 months, official cold days were positively associated with both outcomes, and official hot nights were compatible with 1 for CHD and inverse for HF. COVID-phase intercept adjustments on the full sample moved mean temperature to 0.989 (0.975–1.003) for CHD and 0.967 (0.944–0.991) for HF. Continuous monthly temperature and official day counts are therefore not interchangeable encodings of the same contrast. All six continuous-temperature contrasts were inverse in the nested window. No multiplicity control was computed within that window. No nested-window estimate is promoted beyond a labelled specification.

**Table 3. Mean temperature versus official-day encodings (Newey–West lag-6 display).** COVID-phase values are intercept adjustments on the full 132 months, not a third window.

| Outcome | Encoding | Full 132 months | Nested 84 ⊂ 132 | Full-sample COVID-phase adjustment |
|:--|:--|--:|--:|--:|
| CHD | Mean temperature / 1 °C | 0.993 (0.976–1.010) | 0.980 (0.970–0.990) | 0.989 (0.975–1.003) |
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 1.011 (0.991–1.032) | 1.013 (0.994–1.033) |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 1.036 (1.007–1.067) | 0.991 (0.943–1.041) |
| HF | Mean temperature / 1 °C | 0.974 (0.947–1.002) | 0.945 (0.927–0.963) | 0.967 (0.944–0.991) |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.965 (0.937–0.994) | 0.994 (0.972–1.016) |
| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 1.113 (1.053–1.176) | 1.074 (1.006–1.145) |

Across trend, window, and COVID-phase specifications, the CHD hot-night point estimate ranged from 1.011 to 1.025, and the HF cold-day point estimate from 1.043 to 1.113 (Figure 3). That range of points is not robustness of exclusion of 1: under an 8-df spline, year indicators, or dropping the first 12 or 24 months, the displayed lag-6 interval for HF cold days includes 1. No trend specification is preferred over the 4-df spline in Model 1. The months with largest Cook’s distance were February 2020 for CHD and February 2022 for HF cold days. Excluding the most influential month left both exploratory directions unchanged (CHD hot nights 1.021 (1.001–1.040); HF cold days 1.088 (1.034–1.144)). Lag-one month is a labelled sensitivity. It is not a daily lag curve.

### Twelve-fit thermal exhibit

Table 4 reports the twelve separate-exposure count ratios under the offset for the number of days in the month and Newey–West lag-6 intervals. It is the thermal exhibit, not the headline of this article.

**Table 4. Model 1 thermal exhibit on the full 132-month window (days-in-month offset; Newey–West lag-6 intervals).** Benjamini–Hochberg *q* is `p.adjust` of the twelve Newey–West lag-6 Wald *p* values, not model-based *p*.

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

All twelve *q*-values exceeded 0.19, with a minimum of 0.192. No model meets a multiplicity-protected confirmatory threshold. The two smallest lag-6 *p* values (HF cold days 0.031; CHD hot nights 0.032) are pulled to the same *q* = 0.192 by the Benjamini–Hochberg step-up. Model-based *p* for those rows are 0.004 and 0.112. The HF mean-minimum-temperature interval narrowly included 1, with an unrounded upper bound of 1.00005. For CHD, the continuous monthly temperature estimates were near null, between 0.993 and 0.994, whereas the official hot-night count estimate was larger under the displayed lag-6 construction. These encodings describe different monthly thermal questions. The contrast does not imply that a hot-night effect was missed by the means. It is not a test of hourly nighttime excess heat [9]. For HF, the continuous temperature estimates were weakly inverse, and the cold-day count estimate was positive.

After month and trend residualisation, maximum and minimum temperature retained a variance inflation factor of 4.66 when entered jointly. Hot nights and very hot days retained variance inflation factors near 1.96. In the joint extreme-day model, the CHD hot-night count ratio was 1.045 (1.015–1.075), compared with 1.022 in the separate model. The HF cold-day estimate was the same in the joint and separate models, at 1.073. Joint coefficients are diagnostics, and not preferred estimates.

### Uncertainty ladder

**Table 5. Uncertainty ladder for CHD hot nights and HF cold days on the full 132-month window.**

| Outcome and exposure | Model | HC1 | NW3 | NW6 |
|:--|:--|:--|:--|:--|
| CHD hot nights / 5 days | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.0003–1.0439) | 1.022 (1.002–1.042) |
| HF cold days / 5 days | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

For CHD hot nights, the model-based and HC1 intervals included 1, while both Newey–West intervals excluded 1 on the unrounded scale (lag 3: 1.000253 to 1.043860). The lag-6 interval is narrower than the model-based interval while Pearson residual autocorrelation at lag 1 is 0.508. Positive serial correlation should inflate a HAC variance; a narrower Newey–West interval here is a finite-sample HAC warning, not a more precise discovery. On the nested 84-month refit the same CHD hot-night lag-1 autocorrelation was 0.171, and the HF cold-day autocorrelation was −0.046 against 0.146 on the full window. For HF cold days, all four constructions excluded 1 at the Model 1 baseline, and *q* remained 0.192. Concordance across standard-error methods does not create multiplicity protection. No interval was chosen because it excluded 1.

Pearson residual autocorrelation at lag 1 was 0.508 in the CHD hot-night model and 0.146 in the HF cold-day model. Ljung–Box tests at lag 6 gave *p* < 10^−7^ for every CHD Model 1 fit and *p* > 0.3 for every HF Model 1 fit (lag 6 only). Serial dependence is part of the inferential problem for CHD. That is why the four-construction ladder is shown rather than a single interval.

## Discussion

The extract shows window dependence, not a protected thermal discovery. First-event counts fell while the general population aged 35 years or older rose. Official-day count-ratio point estimates moved with the window, in opposite directions for cold days and for CHD hot nights. All twelve full-window Model 1 *q*-values exceeded 0.19. Neither exploratory contrast is a confirmatory primary.

Three labelled rivals can produce that pattern. They are not mixed into one mechanism paragraph.

**Utilisation.** Neighbouring Hong Kong studies from 2020 do not share this first-event construction, and their counts are not imported into the tables. Xin et al. reported fewer public hospitalisations in 2020, including cardiovascular admissions, together with additional deaths, particularly cardiovascular deaths and deaths outside public hospitals [1]. Those out-of-hospital deaths can remove a first hospitalisation from this series without implying fewer cardiac events. Wai et al. found fewer emergency-department visits and higher 28-day mortality among attenders [2,3]; attender fatality does not change this monthly count. Hung et al. documented self-reported avoidance of consultation in a public survey [4]. Tam et al. reported longer delays to ST-elevation myocardial infarction care in a Hong Kong service in early 2020 [5,6]; this extract has no ACS marker. Those papers can speak to the 2020 trough. They end in 2020. They do not cover February 2022, the HF cold-day influence month, and they do not explain the 2013–2019 decline. Non-presentation and death before arrival can reduce the monthly count; delay can move a count across months; attender-selection and survey avoidance do not identify Table 1. They do not license reading the count drop as recovered health.

**Depletion.** The event is an absorbing first hospitalisation after a first CHD or HF diagnosis among people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. New diagnoses still enter through 2023. Whether “first” is first in the 2013–2023 window (no washout) or incident after look-back is unspecified in the monthly transfer. The 2013 totals are the highest annual counts (CHD 23,830; HF 4,336), the pattern a left-censored first-in-window dump produces. 2020 lies below 2023 (CHD 10,237 vs 12,323; HF 1,964 vs 2,296), which a depletion-only closed cohort after 2013 does not predict. Absent monthly still-at-risk person-time, Figure 1 does not quantify the share due to depletion [14]. It is not incidence in the territory. It is not a measure of physiological improvement.

**Weather-entanglement.** Official hot nights were more frequent in the same years in which care-seeking changed (2.7 per month in 2013–2019; 4.5 per month in 2020–2022). The CHD hot-night residual needs those later years. The same 4-df spline that absorbs the first-event decline also absorbs the hot-night trend. That is an identification problem, not evidence that hot nights caused the count drop. Official cold days remain a winter-to-winter contrast (141 of 145 days in December–February; 29 of 132 months carry any). Weather is therefore insufficient as an account of the window dependence, and it is not irrelevant to the fit. Continuous mean temperature in the nested window is inverse for both outcomes and is not a substitute for the official-day encoding (Table 3).

Daily cardiac-admission studies do not rescue a monthly first-event claim. Goggins and Chan's cumulative relative risk of 2.63 (2.43–2.84) comparing 11 °C with 25 °C is not a monthly count ratio per five official cold days, and it is not imported into Table 2 or Table 4 [8]. Guo et al. reported no overall association for the official hot-night flag after adjustment for mean temperature, so a difference between monthly means and monthly official counts does not identify an intensity mechanism [9]. Jingwen Liu et al. estimated daily mortality attributable fractions in Hong Kong [22]. Zhenyuan Liu et al. modelled heatwave excess deaths under transported local relative risks [23]. Those attributable fractions and excess-death totals cannot be rescaled into the present count ratios. Physiological accounts of overnight recovery and cold-related afterload, and any mapping onto heat–health action-plan elements, are not identified by 132 monthly counts.

## Strengths and limitations

**Strengths.** The analysis window is treated as part of the estimand rather than as a nuisance to be averaged through. Official-day ratios are shown for both the full window and the nested 84-month specification. Mean temperature is placed beside those ratios in the same windows (Table 3). All twelve full-window Model 1 fits are reported. Uncertainty is shown as a four-construction ladder. Figure 1 displays the first-event count path. Figure 3 is the ruling-out exhibit for official-day encodings.

**Limitations.** Admission cause was not recorded, so an event is a first hospitalisation after a first diagnosis and not a cardiac-caused admission. Monthly counts of people still at risk of a first event were unavailable, so the estimates are count ratios rather than incidence-rate ratios [14]. Laboratory measurements were not in the monthly transfer. The design is ecological and monthly, so individual-level and daily-triggering interpretations are not identified [14]. Monthly official-day totals cannot identify consecutive duration. Age, sex, and disease-subtype strata were not delivered. Residual serial correlation remains material for CHD, with lag-1 Pearson autocorrelation of 0.508 in the hot-night model. Official cold days are concentrated in December–February, and only 29 of 132 months carry any official cold day. The CHD hot-night estimate is compatible with 1 in the nested window. There is no post-only 48-month Model 1 table. Official hot-night counts are not hourly nighttime excess heat [9]. All exposures were measured at a single Observatory station and applied territory-wide. Influenza covers 121 of 132 months and is a sensitivity, not Model 1; omitting it from Model 1 is a limitation of a window paper as well as of a thermal fit. A labelled synthetic count process, not this Hospital Authority panel, shows that a full-window coefficient can look attenuated when utilisation or an influenza-like term collapses after month 84 while the true coefficient is held constant. Pollution declined across the decade [13]. That co-trend is slow rather than a 2020-only switch, so confounding by infection or ozone is unresolved in Model 1. A corresponding stroke series was not available. Influence months include February 2020 for CHD and February 2022 for HF cold days. Physiological mechanisms are not identified from the 132 months.

## Conclusion

In this 2013–2023 first-event extract, monthly CHD and HF counts fell. Official-day count-ratio point estimates moved with the window, in opposite directions for cold days and for CHD hot nights. Official thermal extremes are insufficient to account for that dependence. They remain part of the exposure record. The data do not show that health recovered after 2020, and they do not support a multiplicity-protected differential thermal claim. What the file supports is a window-dependent count ratio for a first hospitalisation after a first diagnosis, without admission cause and without person-time.

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
