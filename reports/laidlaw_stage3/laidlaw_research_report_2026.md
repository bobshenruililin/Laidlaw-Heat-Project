---
title: "Heat, cold and first hospitalisation after cardiovascular diagnosis in Hong Kong"
subtitle: "An exploratory monthly study among people with diabetes or hypertension, 2013–2023"
author: "Bob Shen Ruililin"
date: "Laidlaw Scholars Programme · The University of Hong Kong · Summer 2026"
bibliography: literature/references.bib
citeproc: true
reference-section-title: References
link-citations: true
toc: true
toc-depth: 2
geometry: margin=24mm
papersize: a4
fontsize: 11pt
linestretch: 1.08
colorlinks: true
mainfont: DejaVu Serif
sansfont: DejaVu Sans
monofont: DejaVu Sans Mono
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup{font=small,labelfont=bf}
---

# Summary

Hong Kong is becoming hotter, especially at night, but cold winter days have
not disappeared. Both heat and cold can place additional stress on the
cardiovascular system. This matters particularly for people living with type 2
diabetes or hypertension, who already face a high risk of coronary heart
disease and heart failure.

This project examined whether monthly temperature patterns were associated
with monthly counts of a carefully defined hospital event. The available
Hospital Authority data counted each person's first recorded hospitalisation
after their first diagnosis record for coronary heart disease (CHD) or heart
failure (HF). They did not record the reason for admission. The study therefore
does not claim that every admission was caused by CHD or HF, and it does not
estimate individual risk. Its question is narrower: in months with more heat
or cold, did the governed territory-wide count of these first hospitalisations
also differ?

The analysis covered January 2013 to December 2023, giving 132 monthly
observations. Six temperature measures were examined separately for each
outcome: monthly mean temperature, mean daily maximum temperature, mean daily
minimum temperature, hot nights, cold days, and very hot days. This produced a
panel of twelve comparisons. Models accounted for season, long-term change,
and the different number of days in each month. Four approaches to uncertainty
were shown, and the twelve comparisons were corrected for multiple testing.

Two associations stood out before that correction. Five additional hot nights
in a month corresponded to a CHD count ratio of 1.022 (95% confidence interval
1.002–1.042 using Newey–West lag 6). Five additional cold
days corresponded to an HF count ratio of 1.073 (1.006–1.144). These are
approximately 2.2% and 7.3% higher monthly counts, respectively. However, both
multiple-testing-adjusted *q*-values were 0.192, and all twelve *q*-values
exceeded 0.19. The CHD hot-night interval also included no association under
two of the four uncertainty methods. The findings are therefore exploratory,
not confirmatory.

The main contribution is not a claim that one weather measure has been proved
to cause one disease. It is a reproducible framework that reports the complete
panel, makes uncertainty visible, and refuses claims that the available data
cannot support. Better daily outcome data, a denominator for the cohort still
at risk, and a recorded cause of admission would be needed for stronger
inference.

# 1. Introduction

## 1.1 A city facing heat and cold

Climate change does not replace one thermal hazard with another. In Hong Kong,
hot nights have become more frequent, while cold days still return each winter.
At Hong Kong Observatory Headquarters, the number of hot nights rose from 10
in 2013 to a peak of 61 in 2021. Cold-day counts fluctuated substantially but
remained present throughout the study period. The city must therefore plan for
a changing mixture of overnight heat, very hot days, and episodic cold rather
than assuming that warming makes cold irrelevant.

Temperature can affect cardiovascular health through several pathways. Heat
can promote dehydration, disturb sleep and overnight recovery, and increase
cardiac demand. Cold can raise blood pressure and vascular resistance.
Responses may be stronger in people whose cardiovascular regulation is already
compromised by diabetes or hypertension. These mechanisms make both sides of
the temperature distribution relevant, but they do not establish what will be
visible in a particular dataset.

Hong Kong already has important evidence on daily temperature and health.
Earlier studies examined daily stroke or acute myocardial infarction
admissions and reported substantial cold-related patterns
[@goggins2012stroke; @goggins2013]. Liu and colleagues estimated mortality
attributable to non-optimal temperature and found a larger fraction associated
with cold than heat during 2006–2016 [@liu2020jasmine]. More recent work
modelled heat-related excess deaths under several heatwave definitions
[@liu2026roro]. Those studies answer valuable but different questions. A daily
mortality attributable fraction, a modelled number of excess deaths, and a
monthly hospitalisation count ratio cannot be substituted for one another.

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
“principal-diagnosis CHD admissions,” would go beyond the data. The report
uses the longer but accurate description because precision about the outcome
is part of the science.

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
interpreted per five additional days in a month. More complex spell and
heatwave definitions were developed and source-checked elsewhere in the
project [@wang2019ehwe; @li2025heatwaves], but the six-measure panel provides
the clearest common comparison for this report.

Cold-day identification used between-year variation within the same calendar
month and was concentrated in December–February. A winter-only restriction is
a future sensitivity analysis, not a cure for identification.

![Official hot nights, very hot days and cold days at Hong Kong Observatory Headquarters, 2013–2023. These are environmental descriptors, not health findings.](figures/exposure_aging/fig01_annual_extremes_coexistence.png){width=92%}

## 2.3 Statistical analysis

Separate negative-binomial regression models were fitted for each outcome and
each exposure: two outcomes multiplied by six exposures produced twelve core
comparisons. Negative-binomial models allow monthly counts to vary more than a
simple Poisson model would permit. Each model controlled for calendar month,
which captures recurring seasonal patterns, and a natural spline of time with
four degrees of freedom (`ns(time, 4)`). The number of days in the month was
included as an offset so that February was not treated as providing the same
observation time as a 31-day month.

The reported effect measure is a **count ratio**. A ratio of 1 means that the
model estimates no difference in the monthly count for the stated exposure
change. A ratio of 1.05 means an estimated 5% higher count; a ratio of 0.95
means an estimated 5% lower count. Because the number of people in the cohort
who remained eligible for a first event was unavailable for each month, these
are count ratios rather than individual incidence-rate ratios.

Monthly observations close together in time may remain correlated after
season and trend are modelled. To avoid hiding this choice, uncertainty was
reported four ways: model-based, heteroskedasticity-consistent (HC1), and
Newey–West methods with lags of three and six months. The continuity analysis
used the six-month Newey–West interval, but all four were displayed. No method
was chosen because it made a confidence interval exclude 1.

In the leading models, Pearson residual autocorrelation at lag 1 was 0.508 for
CHD hot nights and 0.146 for HF cold days.

Twelve comparisons also create more opportunities for a small *p*-value to
occur by chance. Benjamini–Hochberg *q*-values were therefore calculated
across the complete twelve-comparison panel. A *q*-value is not the probability
that a result is true or false. It is a tool for limiting the expected
proportion of false discoveries when a set of comparisons is considered
together.

## 2.4 Robustness and the attempted daily-exposure extension

Additional analyses varied the long-term trend, removed early years, restricted
the series to the pre-2020 period, examined exposure lags, and excluded the
most influential month. These checks ask whether a result depends on a narrow
modelling choice or one observation. Joint models were used only to diagnose
what happens when correlated heat measures compete in the same equation.

The project also evaluated a constrained method that combines monthly outcomes
with daily exposures [@basagana2024md]. Before it could be used on real health
outcomes, it had to recover known effects in simulations designed around Hong
Kong weather and the observed monthly setting. The F1.1 500-replicate run
failed its admission criteria. After that run, F1.2 re-summarised the existing
fits against unchanged numerical thresholds using worst-cell rules; admission
remained fail. No daily health coefficient was therefore produced. This
project-specific result does not show that the Basagaña–Ballester method fails
generally.

# 3. Results

## 3.1 Environmental and outcome patterns

The weather record shows a clear rise in hot nights and very hot days across
the decade, with year-to-year variation. Cold days were less common than hot
nights in recent years but remained recurrent. This coexistence supports
examining heat and cold together rather than treating one as a historical
concern.

The governed outcome series contained 156,156 CHD first-hospitalisation events
and 29,681 HF events across 132 months. The corresponding monthly means were
1,183.0 and 224.9. Both outcomes displayed seasonality, with a stronger winter
peak for HF. These totals describe the study series; they do not establish an
effect of weather.

**Table 1. Outcome summary**

| Outcome | Months | Total events | Mean per month | Event definition |
|:--|--:|--:|--:|:--|
| Coronary heart disease | 132 | 156,156 | 1,183.0 | First hospitalisation after first recorded CHD diagnosis |
| Heart failure | 132 | 29,681 | 224.9 | First hospitalisation after first recorded HF diagnosis |

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

In plain language, the two leading estimates correspond to approximately 2.2%
more CHD first-hospitalisation events per five additional hot nights and 7.3%
more HF first-hospitalisation events per five additional cold days. These
descriptions concern modelled monthly counts, not an individual's probability
of hospitalisation.

After correction across all twelve comparisons, the two leading estimates each
had *q* = 0.192. Every core *q*-value exceeded 0.19. The complete panel
therefore provides no multiplicity-protected confirmatory association.

## 3.3 What the uncertainty comparison changed

![The two leading exploratory estimates under four approaches to standard errors. The CHD hot-night interval crosses 1 under two methods; the HF cold-day interval does not.](reports/poster/figures/fig_poster_uncertainty.png){width=72%}

The CHD hot-night point estimate was 1.022 under all four standard-error
methods. The intervals were 0.995–1.049 using model-based uncertainty,
0.997–1.047 using HC1, 1.0003–1.0439 using Newey–West lag 3, and 1.002–1.042
using Newey–West lag 6. Model-based and HC1 intervals included 1; NW3 excluded
1 only on the unrounded scale, and NW6 excluded 1. No method was selected
because its interval excluded the null.

The HF cold-day point estimate was 1.073. Its four intervals were
1.023–1.125, 1.011–1.138, 1.007–1.143, and 1.006–1.144. All excluded 1, so
this association was more stable across uncertainty methods. That stability
does not overcome the multiple-testing result: its *q*-value remained 0.192.

## 3.4 Robustness and calibration

Across alternative trend and early-period specifications, the CHD hot-night
count ratio ranged from 1.011 to 1.025, and the HF cold-day ratio ranged from
1.043 to 1.113. Removing the most influential month preserved both directions.
Later monthly lags weakened the CHD hot-night estimate. HF cold days remained
elevated at a one-month lag and weakened at two months. These checks reduce
concern that one coding choice or observation created the pattern, but they do
not establish a daily lag sequence.

The attempted monthly-outcome/daily-exposure estimator passed its numerical
convergence checks but failed its substantive calibration requirements.
In the post-run F1.2 worst-cell re-summary, false-positive rates reached 0.150,
confidence-interval coverage fell to 0.840, and sign recovery was poor for
moderate effects. The method was not applied to produce a real daily
coefficient.

# 4. Interpretation

## 4.1 What the study suggests

The results suggest that the way thermal burden is defined matters. Monthly
average temperature and counts of official extremes did not produce the same
patterns. In the CHD series, hot nights stood out more than mean temperature
or very hot days. In the HF series, cold days stood out more than hot nights.
This is scientifically plausible: nighttime heat may limit physiological
recovery, while cold may increase circulatory strain. It is also compatible
with Hong Kong research that has retained cold as an important cardiovascular
hazard while drawing increasing attention to nighttime heat
[@goggins2013; @guo2024hotnights].

Compatibility is not confirmation. The twelve models were specified after the
outcome series was available, and no association survived correction across
the panel. The CHD hot-night interval changed its null-crossing status across
uncertainty methods. Correlated heat measures also redistributed the CHD
coefficient when entered together. The defensible conclusion is therefore
that the panel contains two hypotheses worth testing with better data, not two
causal discoveries.

## 4.2 Why the result still matters

Null or uncertain findings can be useful when they close off weak claims. This
project establishes that monthly governed data can support a transparent
comparison of thermal-burden measures. It also shows where that design stops.
The data cannot identify within-month timing, individual exposure, or the cause
of admission. The failed daily-exposure calibration provides an empirical
reason not to present a daily coefficient, rather than relying only on a
general warning about aggregation.

The distinction has practical consequences. A health-protection message based
on confirmed daily triggering would require different evidence from an
exploratory monthly burden pattern. The present findings do not justify
disease-specific warning thresholds. They do support continued attention to
both overnight heat and winter cold, and they motivate a governed design that
links daily weather to dated, cause-recorded admissions.

## 4.3 Strengths

The project has five main strengths. First, it uses an eleven-year public
weather record and governed health aggregates. Second, weather definitions
were source-checked rather than reconstructed from memory. Third, all twelve
core comparisons are reported as one panel, reducing selective emphasis on the
smallest *p*-values. Fourth, four uncertainty methods are displayed rather
than selecting the one that gives the most attractive interval. Fifth, tables,
figures and claim text are linked to machine-readable outputs and automated
release checks.

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
   over time, and no core comparison survived correction for twelve tests.
7. **Available outcomes.** Age, sex and disease subgroups were unavailable.
   A stroke series was not delivered and no stroke result is reported.

# 5. Implications and next study

The next analysis should not simply add more monthly definitions. Its highest
value would come from improving the outcome data contract. A stronger design
would include the dated admission, recorded reason for admission, cohort entry
and follow-up, and the number of people still at risk of a first event. Daily
or weekly outcome resolution would make lag analysis possible. Age, sex,
diagnostic subtype and location would allow assessment of vulnerability and
exposure misclassification. Pollution, humidity and influenza could then be
incorporated in a clearly staged confounding plan.

The two exploratory patterns provide specific hypotheses for that design:
whether repeated hot nights precede CHD-related admissions, and whether cold
days precede HF-related admissions among people with diabetes or hypertension.
Those hypotheses should be declared before fitting the next outcome series.
The analysis should retain both heat and cold measures, use a limited primary
contrast set, and preserve the full uncertainty display.

For public-health practice, the immediate message is deliberately broader.
Hong Kong's changing climate includes more nighttime heat without the
elimination of cold. Cardiovascular adaptation should therefore avoid a
heat-only narrative. This report does not quantify preventable admissions, but
it identifies the evidence needed before burden estimates or disease-specific
recommendations can be defended.

# 6. Conclusion

Between 2013 and 2023, Hong Kong experienced increasing hot-night burden while
cold days persisted. In governed monthly data for people with diabetes and/or
hypertension, CHD first-hospitalisation counts were most elevated in relation
to hot nights, while HF counts were most elevated in relation to cold days.
Neither pattern survived correction across twelve comparisons, and the CHD
hot-night result was sensitive to the treatment of uncertainty.

The study therefore offers hypotheses, not proof of thermal effects. Its more
durable contribution is a reproducible and aggregation-aware framework: define
the event precisely, compare thermal measures as a panel, show uncertainty,
and decline daily or causal claims when the data cannot support them.

# Acknowledgements

I thank Hogan for guidance on weather definitions and academic writing;
Zhenyuan Liu (“Roro”) for constructing and releasing the governed Hospital
Authority aggregates and for regression mentorship; and Professor David
Bishai for supervision and population-health guidance. Diagnosis-record
construction also benefited from clinical collaboration. External
dissemination of governed results remains subject to the appropriate team and
institutional approvals.

# Appendix A. Complete core panel

**Table A1. Separate negative-binomial monthly models with a days-in-month
offset and Newey–West lag-6 confidence intervals.**

| Outcome | Exposure contrast | Count ratio (95% CI) | BH *q* |
|:--|:--|--:|--:|
| CHD | Mean temperature / 1 °C | 0.993 (0.976–1.010) | 0.726 |
| CHD | Mean maximum temperature / 1 °C | 0.993 (0.979–1.007) | 0.642 |
| CHD | Mean minimum temperature / 1 °C | 0.994 (0.977–1.012) | 0.764 |
| CHD | Hot nights / 5 days | 1.022 (1.002–1.042) | 0.192 |
| CHD | Cold days / 5 days | 0.995 (0.949–1.043) | 0.900 |
| CHD | Very hot days / 5 days | 0.999 (0.974–1.025) | 0.962 |
| HF | Mean temperature / 1 °C | 0.974 (0.947–1.002) | 0.207 |
| HF | Mean maximum temperature / 1 °C | 0.981 (0.958–1.005) | 0.272 |
| HF | Mean minimum temperature / 1 °C | 0.973 (0.947–1.000) | 0.202 |
| HF | Hot nights / 5 days | 1.003 (0.976–1.031) | 0.900 |
| HF | Cold days / 5 days | 1.073 (1.006–1.144) | 0.192 |
| HF | Very hot days / 5 days | 0.995 (0.963–1.028) | 0.900 |

# Appendix B. Submission interpretation

This report is an accessible research essay for the Laidlaw Stage 3
submission. It presents current CHD/HF results and supersedes the earlier
literature-and-methods essay as the submission-facing research report. The
journal manuscript and technical supplement contain fuller diagnostics. The
separate HKU report form requires supervisor completion and endorsement.
