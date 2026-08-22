---
title: "Heat, cold and first hospitalisation after cardiovascular diagnosis in Hong Kong"
subtitle: "An exploratory monthly study among people with diabetes or hypertension, 2013–2023"
author: "Shen Ruililin"
date: "Laidlaw Scholars Programme · The University of Hong Kong · August 2026"

bibliography: literature/references.bib
citeproc: true
reference-section-title: References
link-citations: true
lang: en-GB

documentclass: article
classoption: oneside
papersize: a4
fontsize: 11pt
toc: false
indent: true
linestretch: 1.15

geometry:
  - left=27mm
  - right=27mm
  - top=25mm
  - bottom=25mm
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

# Summary

Hong Kong is becoming hotter, especially at night, while cold winter days
persist. Both heat and cold can place additional stress on the cardiovascular
system. This matters particularly for people living with type 2 diabetes or
hypertension, who already face a high risk of coronary heart disease (CHD) and
heart failure (HF).

This study asked whether monthly temperature patterns were associated with
monthly counts of a precisely defined hospital event. In the governed Hospital
Authority data, the event was each person's first recorded hospitalisation
after a first diagnosis record for CHD or HF. The reason for admission was not
recorded. The study therefore does not claim that any admission was caused by
CHD or HF, and it does not estimate individual risk. Its question is narrower:
in months with more heat or cold, did the territory-wide count of these first
hospitalisations differ?

The analysis covered January 2013 to December 2023, giving 132 monthly
observations. Six temperature measures were examined separately for each
outcome: monthly mean temperature, mean daily maximum, mean daily minimum, hot
nights, cold days, and very hot days. This produced a panel of twelve
comparisons. Models accounted for season, long-term change, and the number of
days in each month. Uncertainty was reported under four standard-error methods,
and the twelve comparisons were corrected for multiple testing.

Two estimates were larger than the rest. Five additional hot nights in a month
corresponded to a CHD count ratio of 1.022 (95% confidence interval
1.002–1.042); five additional cold days to an HF count ratio of 1.073
(1.006–1.144). Neither survived correction: both adjusted *q*-values were
0.192, and all twelve exceeded 0.19. The HF estimate held under all four
uncertainty methods and strengthened when the pandemic years were removed. The
CHD interval included 1 under two of the four methods and was not
evident before 2020. The findings are exploratory, not confirmatory.

The contribution is the complete panel itself: every comparison reported,
uncertainty shown under four methods, and no claim beyond what monthly counts
can support. Stronger inference would require daily outcomes, a denominator for
the cohort still at risk, and a recorded cause of admission.

# 1. Introduction

## 1.1 A city facing heat and cold

Climate change does not replace one thermal hazard with another. In Hong Kong,
hot nights have become more frequent, while cold days still return each winter.
At Hong Kong Observatory Headquarters, the number of hot nights rose from 10
in 2013 to a peak of 61 in 2021. The city therefore faces overnight heat, very
hot days, and episodic cold together.

Temperature can affect cardiovascular health through several pathways. Heat
can promote dehydration, disturb sleep and overnight recovery, and increase
cardiac demand. Cold can raise blood pressure and vascular resistance.
Responses may be stronger in people whose cardiovascular regulation is already
compromised by diabetes or hypertension. These mechanisms make both sides of
the temperature distribution relevant.

Hong Kong already has important evidence on daily temperature and health.
Earlier studies examined daily stroke or acute myocardial infarction
admissions and reported substantial cold-related patterns
[@goggins2012stroke; @goggins2013]. Liu and colleagues estimated mortality
attributable to non-optimal temperature and found a larger fraction associated
with cold than heat during 2006–2016 [@liu2020jasmine]. More recent work
modelled heat-related excess deaths under several heatwave definitions
[@liu2026roro]. A daily mortality attributable fraction, a modelled number of
excess deaths, and a monthly hospitalisation count ratio cannot be substituted
for one another.

## 1.2 Why monthly data require a different question

Health data are often released in aggregate form to protect privacy. In this
project, the governed outcomes were available only as territory-wide monthly
counts. That resolution can support a study of monthly burden, but it cannot
reveal whether a particular hot day triggered a hospitalisation several days
later. It also cannot show which individual experienced which temperature.

The outcome definition requires equal care. The delivered data count the first
recorded hospitalisation after a first CHD or HF diagnosis record among people
with type 2 diabetes and/or hypertension. Admission cause is absent. Calling
these events “heart attacks caused by temperature,” or even
“principal-diagnosis CHD admissions,” would go beyond the data.

## 1.3 Objectives

The primary objective was to estimate monthly associations between thermal
burden and first-hospitalisation counts for CHD and HF during 2013–2023. Three
secondary objectives were to:

1. compare continuous temperature measures with official extreme-day counts;
2. show how conclusions change across defensible uncertainty methods; and
3. determine whether the available monthly outcomes could reliably support a
   more ambitious estimate using daily exposure information.

# 2. Methods

## 2.1 Study design and data

The study used an ecological monthly time-series design. Each observation was
one calendar month for Hong Kong, from January 2013 through December 2023. The
final panel contained 132 months.

Daily weather observations came from Hong Kong Observatory Headquarters.
Public weather series were checked against annual Observatory summaries before
analysis. Population data came from the Census and Statistics Department, and
air-pollution series were assembled from Environmental Protection Department
general monitoring stations for the broader project. The core models reported
here focus on thermal exposures and do not claim that pollution or influenza
confounding has been fully resolved.

Governed Hospital Authority aggregates supplied the two outcomes. The cohort
comprised people recorded with type 2 diabetes and/or hypertension during the
study period. For each outcome, the monthly series counted the first recorded
hospitalisation after the person's first CHD or HF diagnosis record. The
analysis used aggregate counts only; source monthly health files and merged
health panels were not placed in public version control.

## 2.2 Temperature measures

No single number fully represents thermal burden. A warm monthly average can
arise from consistently mild conditions, several intense days, or unusually
warm nights. These patterns may matter differently for health. Six measures
were therefore evaluated:

- monthly mean temperature;
- monthly mean of daily maximum temperature;
- monthly mean of daily minimum temperature;
- number of hot nights, defined as minimum temperature at least 28 °C;
- number of very hot days, defined as maximum temperature at least 33 °C; and
- number of cold days, defined as minimum temperature at most 12 °C.

The continuous measures were interpreted per 1 °C. Extreme-day counts were
interpreted per five additional days in a month. More complex heatwave
definitions exist [@wang2019ehwe; @li2025heatwaves]; the six measures give the
clearest common comparison.

![Official hot nights, very hot days and cold days at Hong Kong Observatory Headquarters, 2013–2023. These are environmental descriptors, not health findings.](figures/exposure_aging/fig01_annual_extremes_coexistence.png){width=92%}

## 2.3 Statistical analysis

Separate negative-binomial regression models were fitted for each outcome and
each exposure: two outcomes multiplied by six exposures produced twelve core
comparisons. Negative-binomial models allow monthly counts to vary more than a
simple Poisson model would permit. Each model controlled for calendar month,
which captures recurring seasonal patterns, and a smooth long-term trend. The
number of days in the month was included as an offset so that February was not
treated as providing the same observation time as a 31-day month.

The reported effect measure is a **count ratio**. A ratio of 1 means that the
model estimates no difference in the monthly count for the stated exposure
change. A ratio of 1.05 means an estimated 5% higher count; a ratio of 0.95
means an estimated 5% lower count. Because the number of people in the cohort
who remained eligible for a first event was unavailable for each month, these
are count ratios rather than individual incidence-rate ratios.

Monthly observations close together in time may remain correlated after
season and trend are modelled. To avoid hiding this choice, uncertainty was
reported four ways: model-based, heteroskedasticity-consistent (HC1), and
Newey–West methods with lags of three and six months. The main results use the
six-month Newey–West interval, but all four were displayed. No method was
chosen because it made a confidence interval exclude 1.

Twelve comparisons also create more opportunities for a small *p*-value to
occur by chance. Benjamini–Hochberg *q*-values were therefore calculated
across the complete twelve-comparison panel. A *q*-value limits the expected
proportion of false discoveries across the set of comparisons.

## 2.4 Robustness and the attempted daily-exposure extension

Additional analyses varied the long-term trend, removed early years,
restricted the series to the pre-2020 period, adjusted for pandemic phases,
examined exposure lags, and excluded the most influential month. Joint models
were used only to diagnose what happens when correlated heat measures compete
in the same equation.

The project also evaluated a constrained method that combines monthly outcomes
with daily exposures [@basagana2024md]. Before it could be used on real health
outcomes, it had to recover known effects in simulations designed around Hong
Kong weather and the observed monthly setting. The method failed the
predefined error, coverage, bias and sign-recovery requirements. No daily
health coefficient was therefore produced. Greater mathematical complexity
does not create temporal information that the data cannot supply.

# 3. Results

## 3.1 Environmental and outcome patterns

The weather record shows a clear rise in hot nights and very hot days across
the decade, with year-to-year variation. Cold days were less common than hot
nights in recent years but remained recurrent.

The governed outcome series contained 156,156 CHD first-hospitalisation events
and 29,681 HF events across 132 months. The corresponding monthly means were
1,183.0 and 224.9. Both outcomes displayed seasonality, with a stronger winter
peak for HF.

```{=latex}
\begin{table}[ht]
\centering
\caption{Outcome summary.}
\label{tab:outcome-summary}
\begin{tabular}{lrrr p{0.42\textwidth}}
\toprule
Outcome & Months & Total events & Mean per month & Event definition \\
\midrule
Coronary heart disease & 132 & 156,156 & 1,183.0 & First hospitalisation after first recorded CHD diagnosis \\
Heart failure & 132 & 29,681 & 224.9 & First hospitalisation after first recorded HF diagnosis \\
\bottomrule
\end{tabular}
\end{table}
```

## 3.2 The twelve-comparison panel

![Count ratios and 95% confidence intervals for the twelve core monthly models. The dashed line at 1 indicates no estimated difference. All twelve Benjamini–Hochberg *q*-values exceeded 0.19.](outputs/release_chd_hf/figures/figure3_core_forest.png){width=100%}

Most core estimates were close to a count ratio of 1. For CHD, monthly mean,
maximum and minimum temperatures produced count ratios of approximately
0.993–0.994 per 1 °C. Cold days and very hot days were also near 1. The
largest CHD estimate was for hot nights: 1.022 per five additional hot nights
(95% confidence interval 1.002–1.042 using Newey–West lag 6; *p* = 0.032).

For HF, the continuous temperature estimates were modestly below 1. The
minimum-temperature estimate was 0.973 per 1 °C (0.947–1.000). Hot nights and
very hot days were near 1. The largest HF estimate was for cold days: 1.073
per five additional cold days (1.006–1.144; *p* = 0.031).

These estimates concern modelled monthly counts, not an individual's
probability of hospitalisation. After correction across all twelve
comparisons, the two leading estimates each had *q* = 0.192, and every
*q*-value exceeded 0.19. The panel provides no confirmed association.

## 3.3 What the uncertainty comparison changed

![The two leading exploratory estimates under four approaches to standard errors. The CHD hot-night interval crosses 1 under two methods; the HF cold-day interval does not.](reports/poster/figures/fig_poster_uncertainty.png){width=72%}

The CHD hot-night point estimate was 1.022 under all four standard-error
methods, because the fitted model did not change. The interval did change:
0.995–1.049 with model-based uncertainty, 0.997–1.047 with HC1, 1.0003–1.0439
with Newey–West lag 3, and 1.002–1.042 with Newey–West lag 6. The first two
intervals include 1; the two Newey–West intervals exclude it, at lag 3 only
just. Residual autocorrelation at lag 1 was 0.508 in this model, so how serial
dependence is handled matters for the CHD series; that is why four methods are
shown rather than one. The Newey–West intervals were also narrower than the
model-based interval, which is unusual when residuals are positively
correlated. The exclusion of 1 therefore rests on the smaller robust variance
estimate, which is a reason for caution rather than confirmation.

The HF cold-day point estimate was 1.073. Its four intervals were 1.023–1.125,
1.011–1.138, 1.007–1.143, and 1.006–1.144. All excluded 1, so this estimate
was stable across uncertainty methods. Stability across standard-error methods
does not create protection against multiple testing: the *q*-value remained
0.192.

## 3.4 Robustness and calibration

The most informative check restricted the series to 2013–2019, before the
pandemic altered hospital use. The HF cold-day ratio strengthened to 1.113
(1.053–1.176). The CHD hot-night ratio weakened to 1.011 (0.991–1.032), an
interval including 1, and weakened similarly under pandemic-phase adjustment.
The CHD association is therefore confined to analyses that include 2020–2023,
the years in which hot nights peaked and hospital use changed; the HF
association does not depend on those years. Across other checks, the CHD ratio
ranged from 1.011 to 1.025 and the HF ratio from 1.043 to 1.113, and removing
the most influential month preserved both directions. At a one-month lag, the
CHD estimate moved toward 1 while the HF estimate remained elevated; none of
these checks establishes a daily lag sequence.

The attempted monthly-outcome, daily-exposure estimator passed its numerical
convergence checks but failed its calibration requirements in simulation. In
the most difficult cells, false-positive rates reached 0.150,
confidence-interval coverage fell to 0.840, and sign recovery was poor for
moderate effects. No daily coefficient was applied to the real health series.

# 4. Interpretation

## 4.1 What the study suggests

The results suggest that the way thermal burden is defined matters. In the CHD
series, hot nights were more closely associated with the monthly counts than
mean temperature or very hot days; in the HF series, cold days more than any
heat measure. Both patterns are plausible — nighttime heat may limit overnight
recovery, while cold increases circulatory strain — and both are compatible
with Hong Kong research that retains cold as a cardiovascular hazard while
drawing increasing attention to nighttime heat
[@goggins2013; @guo2024hotnights].

Compatibility is not confirmation. The twelve models were specified after the
outcome series was available, and none survived correction across the panel.
The HF association rests on a narrow slice of data: official cold days fell
almost entirely in December–February (141 of 145), and only 29 of 132 months
contained any, so the models compare colder winters with milder winters, not
winter with summer. The CHD association depends on the uncertainty method and
appears only in analyses including 2020–2023. The panel therefore contains two
hypotheses worth testing with better data, not two discoveries.

## 4.2 Why the result still matters

Null or uncertain findings can be useful when they close off weak claims. This
project establishes that monthly governed data can support a transparent
comparison of thermal-burden measures. It also shows where that design stops.
The data cannot identify within-month timing, individual exposure, or the cause
of admission. The failed daily-exposure calibration provides an empirical
reason not to present a daily coefficient.

The distinction has practical consequences. A health-protection message based
on confirmed daily triggering would require different evidence from an
exploratory monthly burden pattern. The present findings do not justify
disease-specific warning thresholds. They do support continued attention to
both overnight heat and winter cold, and they motivate a governed design that
links daily weather to dated, cause-recorded admissions.

## 4.3 Strengths

The project has four main strengths. First, it uses an eleven-year public
weather record and governed health aggregates. Second, weather definitions
were source-checked rather than reconstructed from memory. Third, all twelve
core comparisons are reported as one panel, reducing selective emphasis on the
smallest *p*-values. Fourth, four uncertainty methods are displayed rather
than one chosen interval.

## 4.4 Limitations

The limitations determine how the results should be read:

1. **Outcome meaning.** Admission cause was not recorded. The event is the
   first hospitalisation after a recorded CHD or HF diagnosis, not necessarily
   an admission caused by that condition.
2. **Ecological resolution.** Each observation describes Hong Kong for one
   month. Individual exposure and within-month timing are unknown, so
   individual or daily causal inference is unavailable [@greenland1989ecological].
3. **Denominator.** The number of cohort members still eligible for a first
   event in each month was not available. The estimates are count ratios, not
   cohort incidence-rate ratios.
4. **Confounding.** Season and long-term trend were controlled, but the core
   panel does not claim complete adjustment for pollution, humidity,
   influenza, behavioural change, or changes in health care.
5. **Exposure measurement.** Headquarters weather is a territory-level proxy.
   It cannot represent differences between neighbourhoods, indoor
   temperatures, air-conditioning access, or personal activity.
6. **Serial dependence and multiplicity.** CHD residuals remained correlated
   over time (lag-one correlation 0.508), and no core comparison survived
   correction for twelve tests.
7. **Available outcomes.** Age, sex and disease subgroups were unavailable.
   A stroke series was not delivered and no stroke result is reported.

# 5. Implications and next study

The next analysis should improve the outcome data rather than add more monthly
definitions. A stronger design would include the dated admission, recorded
reason for admission, cohort entry and follow-up, and the number of people
still at risk of a first event. Daily or weekly outcome resolution would make
lag analysis possible. Age, sex, diagnostic subtype and location would allow
assessment of vulnerability and exposure misclassification. Pollution,
humidity and influenza could then be incorporated in a clearly staged
confounding plan.

The two exploratory patterns provide specific hypotheses for that design:
whether repeated hot nights precede CHD-related admissions, and whether cold
days precede HF-related admissions among people with diabetes or hypertension.
Those hypotheses should be declared in advance, with both heat and cold
measures retained and the full uncertainty display preserved.

For public-health practice, the immediate message is deliberately broader.
Hong Kong's changing climate includes more nighttime heat without the
elimination of cold. Cardiovascular adaptation should therefore avoid a
heat-only narrative. The report does not quantify preventable admissions; it
identifies the evidence needed before such estimates can be defended.

# 6. Conclusion

Between 2013 and 2023, Hong Kong experienced increasing hot-night burden while
cold days persisted. In governed monthly data for people with diabetes and/or
hypertension, CHD first-hospitalisation counts were more closely associated
with hot nights, and HF counts with cold days, than with the other thermal
measures examined. Neither association survived correction across twelve
comparisons, and the CHD estimate depended on the uncertainty method and on
including the pandemic years.

The study therefore offers hypotheses, not proof of thermal effects. What it
leaves behind is a precisely defined first-event outcome, a complete
twelve-comparison panel, uncertainty shown under four methods, and a
documented refusal to produce daily coefficients that monthly counts cannot
support.

# Acknowledgements

I thank Hogan for guidance on weather definitions and on academic writing;
Zhenyuan Liu for constructing and releasing the governed Hospital Authority
aggregates and for regression mentorship; and Professor David Bishai for
supervision and population-health guidance. Diagnosis-record construction was
assisted by a clinical collaborator. Dissemination of governed results
requires the approval of the team and the relevant institutions.

```{=latex}
\clearpage
```

# Appendix. Complete core panel

```{=latex}
\renewcommand{\thetable}{A\arabic{table}}
\setcounter{table}{0}
\begin{table}[ht]
\centering
\small
\caption{Separate negative-binomial monthly models with a days-in-month offset and Newey--West lag-6 confidence intervals.}
\label{tab:core-panel}
\begin{tabular}{llcc}
\toprule
Outcome & Exposure contrast & Count ratio (95\% CI) & BH $q$ \\
\midrule
CHD & Mean temperature / 1 °C & 0.993 (0.976--1.010) & 0.726 \\
CHD & Mean maximum temperature / 1 °C & 0.993 (0.979--1.007) & 0.642 \\
CHD & Mean minimum temperature / 1 °C & 0.994 (0.977--1.012) & 0.764 \\
CHD & Hot nights / 5 days & 1.022 (1.002--1.042) & 0.192 \\
CHD & Cold days / 5 days & 0.995 (0.949--1.043) & 0.900 \\
CHD & Very hot days / 5 days & 0.999 (0.974--1.025) & 0.962 \\
HF & Mean temperature / 1 °C & 0.974 (0.947--1.002) & 0.207 \\
HF & Mean maximum temperature / 1 °C & 0.981 (0.958--1.005) & 0.272 \\
HF & Mean minimum temperature / 1 °C & 0.973 (0.947--1.000) & 0.202 \\
HF & Hot nights / 5 days & 1.003 (0.976--1.031) & 0.900 \\
HF & Cold days / 5 days & 1.073 (1.006--1.144) & 0.192 \\
HF & Very hot days / 5 days & 0.995 (0.963--1.028) & 0.900 \\
\bottomrule
\end{tabular}
\end{table}
```
