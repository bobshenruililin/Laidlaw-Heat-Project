# Final exploratory reanalysis protocol — CHD/HF monthly aggregates

**Version:** F1.0  
**Frozen:** 10 August 2026, before fitting any analyses introduced below  
**Status:** Post-outcome exploratory protocol; not a confirmatory preregistration  
**Study window:** January 2013–December 2023 (132 territory-months)  
**Outcomes:** CHD and HF first-hospitalisation aggregates supplied by the
outcome co-investigator  
**Companion registry:** `analysis_plan/final_model_registry.yml`

## 1. Purpose and inferential status

This protocol freezes the finite model universe for the final integrated
report and journal-facing CHD/HF manuscript. It was written after the outcome
series and SAP Amendment A1 estimates were visible. No analysis in this
protocol may be described as prospectively confirmatory.

The work has two aims:

1. estimate and stress-test ecological monthly associations between thermal
   exposures and first-hospitalisation counts; and
2. test whether daily weather can support a constrained daily-exposure model
   when health outcomes are available only as monthly sums.

The second aim is a methods-feasibility exercise. It cannot be used to promote
a daily triggering claim unless its synthetic calibration gates pass.

## 2. Source contract

### 2.1 Outcome

The governed files contain territory-month counts among people diagnosed with
type 2 diabetes and/or hypertension during 2013–2023:

- first hospitalisation after the first CHD diagnosis record; and
- first hospitalisation after the first HF diagnosis record.

The patient-level source does not record the cause of admission. The outcomes
are therefore not principal-diagnosis CHD or HF admissions, acute myocardial
infarctions, or disease-specific attack rates. The term `inpatient` is inferred
from the delivered column names and still requires confirmation from the
outcome co-investigator. Stroke was named in the covering email but was not
attached.

### 2.2 Exposure and covariates

- HKO Headquarters daily temperature is the primary weather series.
- Official indicators are hot night (`Tmin >= 28 C`), very hot day
  (`Tmax >= 33 C`), and cold day (`Tmin <= 12 C`).
- Li-style heatwave and Wang-style spell/compound definitions are allowed only
  after the exact operators are source-locked.
- Monthly pollution uses EPD general-station means under the existing
  completeness rule.
- Absolute humidity, influenza, COVID phases, holidays, and population are
  sensitivity covariates, not an unrestricted adjustment pool.

### 2.3 Provenance

Real health analyses require every input row to carry
`HA_APPROVED_AGGREGATE`. Simulation outputs carry
`SYNTHETIC_CALIBRATION`. The labels may never be combined in one result table
without an explicit `result_class` column.

Source monthly counts and merged panels remain gitignored. Aggregation does not
grant external-publication authority; written Roro/Bishai confirmation remains
required.

## 3. Estimands

### 3.1 Analysis-of-record monthly estimand

For outcome \(o\), month \(t\), and one exposure \(X_t\):

\[
Y_{o,t} \sim \mathrm{NB}(\mu_{o,t}, \theta_o),
\]

\[
\log(\mu_{o,t}) =
\alpha_{o,m(t)} + ns(t,4) + \beta_o X_t + \log(D_t),
\]

where \(D_t\) is days in month. The reported quantity is
\(\exp(\beta_o)\), a monthly **count ratio** for the stated contrast.

It is not an incidence-rate ratio because the T2D/HTN cohort still at risk of a
first event is unavailable. A population-times-days offset is retained only as
an ecological sensitivity.

### 3.2 Within-season/anomaly estimand

For continuous temperature and official extreme-day counts, an anomaly is the
observed monthly value minus its calendar-month mean. Warm-season heat and
cold-season cold analyses estimate associations within source-locked seasons.
Season cut-points will not be searched after fitting.

### 3.3 Cross-outcome contrast

A single stacked model will test whether the hot-versus-cold contrast differs
between CHD and HF:

\[
\Delta =
(\beta_{H,CHD} - \beta_{C,CHD})
-
(\beta_{H,HF} - \beta_{C,HF}).
\]

The model includes outcome-specific month effects and trends and clusters or
bootstraps at calendar month. Separate coefficients do not establish
\(\Delta \ne 0\).

### 3.4 Predictive estimand

Predictive evidence is the held-out log-score difference between a
season-plus-trend baseline and the same model with one frozen thermal exposure.
It is not causal evidence.

### 3.5 Aggregated-outcome/daily-exposure estimand

For latent daily means \(\lambda_d=\exp(X_d\beta)\) and observed monthly count
\(S_m\):

\[
S_m \sim \mathrm{Poisson}\left(
\sum_{d \in m} o_d \exp(X_d\beta)
\right).
\]

This is the Basagana-Ballester aggregated likelihood. It is implemented
clean-room from the published equation. Their public code has no repository
licence and will not be copied.

Daily exposure coefficients are admitted only for a constrained,
low-dimensional model that passes Section 8. Unequal month length is handled
by the daily sum. General-population offsets remain sensitivities because they
do not represent the cohort risk set.

## 4. Frozen exposure families

### 4.1 Amended core

Each exposure is fitted separately:

1. mean temperature per 1 C;
2. mean maximum temperature per 1 C;
3. mean minimum temperature per 1 C;
4. hot nights per 5 days;
5. cold days per 5 days; and
6. very hot days per 5 days.

The twelve outcome-exposure contrasts form one multiplicity family.

### 4.2 Calendar-spillover morphology

Daily events are translated into monthly exposure burdens using:

- event starts in month;
- events overlapping month;
- event days in month;
- same-day affected days;
- days 1–5 after event exposure; and
- days 6–21 after event exposure where the source definition supports it.

Each calendar day belongs to at most one phase for a given event. A phase that
crosses a month boundary is assigned to the month containing the affected day,
not the event-onset month. These variants are an exposure audit. They are not
all fitted as independent discovery tests.

### 4.3 Source lock

Before association fitting:

- Li et al. (2025): confirm warm-season bounds, Tmax percentile operator,
  15-day moving reference window, study reference period, minimum duration,
  and event-merging interval. The source's interval of at most two days is
  implemented as at most one intervening non-hot day.
- Wang et al. (2019): confirm `>=5` VHD/HN spells, exact `NDNDN` 2D3N
  alignment, and five-day post-event interval.
- Jingwen Liu et al. (2020): independently confirm the 30.60 C threshold and
  lag phases before any Liu-style daily kernel is implemented.

The revised excess-mortality manuscript is not authoritative where it conflicts
with its cited primary sources.

## 5. Monthly model ensemble

### 5.1 Analysis of record

- Negative-binomial point estimate.
- Model-based, HC1, Newey-West lag 3, and Newey-West lag 6 intervals shown
  together.
- No interval is selected because it crosses 0.05.

### 5.2 Structural serial-dependence model

A negative-binomial GLARMA model uses the same exposure, season/trend design,
and `log(days)` offset. AR/MA orders are limited to `(1,0)`, `(0,1)`, and
`(1,1)`. Order is selected by a frozen likelihood/diagnostic rule, not the
exposure p-value.

### 5.3 Frozen robustness ladder

For each amended core exposure:

1. baseline month factor plus `ns(time,4)`;
2. `ns(time,3)` and `ns(time,6)`;
3. year fixed effects plus calendar-month effects;
4. calendar-month anomaly exposure;
5. warm-season heat or cold-season cold;
6. COVID-phase adjustment;
7. pre-2020 period;
8. staged absolute humidity;
9. staged NO2, then PM2.5;
10. influenza for cold models;
11. ozone last;
12. exclusion of the maximum-Cook's-distance month; and
13. one- and two-month exposure leads as placebo tests.

No model may contain more than one thermal exposure except the single,
predefined hot-versus-cold cross-outcome model.

### 5.4 Prediction

- Leave one calendar year out.
- Rolling origin with a 12-month horizon where training size permits.
- Compare baseline versus baseline-plus-exposure using log score, deviance,
  and mean absolute error.
- Exposure selection is frozen before prediction.

### 5.5 Specification curve

The specification universe is exactly the cross-product declared in
`final_model_registry.yml`. Results are summarised by median, interquartile
range, sign stability, and a simultaneous max-statistic from a
serial-dependence-preserving null. The report will not count nominally
significant models.

## 6. Multiplicity and selection

1. The twelve amended core contrasts receive BH q-values for continuity.
2. The frozen specification curve receives a family-wise max-statistic
   calibrated under a parametric or stationary-block null.
3. Spillover variants are a separate methods family and cannot rescue a core
   claim.
4. The post-outcome CHD-hot/HF-cold pattern remains exploratory even if one
   robustness model excludes the null.
5. A real daily-exposure fit cannot be called confirmatory because its model
   was introduced after outcomes were seen.

## 7. Synthetic calibration design

Daily latent counts are simulated using the real HKO weather sequence and
outcome-specific nuisance structures matched to:

- observed total-count scale;
- seasonal profile;
- secular first-event decline;
- COVID-era level changes;
- negative-binomial overdispersion; and
- monthly residual dependence.

Core scenarios cross:

- null, small, and moderate thermal effects;
- same-day, 0–5-day, and 0–21-day cumulative kernels;
- CHD-like and HF-like count scales;
- no AR versus outcome-matched AR;
- stable versus depleting risk set; and
- COVID shock absent versus present.

Pilot runs use 100 replicates. Core runs use 500. Cells within Monte Carlo
uncertainty of a decision boundary use 1,000.

Comparators are:

- oracle daily model (simulation only);
- current monthly negative-binomial model;
- constrained aggregated-outcome/daily-exposure likelihood;
- negative-binomial GLARMA with offset; and
- simplified spillover-burden model.

## 8. Admission gates for the daily-exposure method

All criteria must pass before a real daily-exposure estimate enters the
manuscript:

1. convergence rate at least 95%;
2. null type-I error between 3% and 8%;
3. 95% interval coverage at least 90%;
4. absolute relative bias no greater than 20% for non-null effects;
5. false-sign rate no greater than 10% for moderate effects;
6. positive-definite Hessian with condition number below \(10^8\);
7. fewer than 5% divergent or boundary fits; and
8. no coverage below 85% in AR, depletion, or COVID stress scenarios.

The real model is limited to 20 parameters. A full 8-df-per-year,
21-day non-linear DLNM is prohibited for 132 monthly observations.

If any gate fails, the result is a documented methods-feasibility failure and
the monthly model remains the analysis of record.

## 9. Claim tiers

- **Established:** provenance, definitions, totals, period, model diagnostics.
- **Supported:** complete estimates and robustness patterns traceable to real
  release tables.
- **Exploratory:** exposure-outcome signals, cross-outcome differences, and
  all post-outcome model extensions.
- **Hypothesis:** biological mechanisms, differential thermal pathways, and
  care-seeking explanations.
- **Future:** stroke, cohort incidence, age/sex/medication effects, and any
  daily or individual-level causal analysis requiring new governed data.

## 10. Human-owned decisions

Agents cannot close:

1. Gate 3 headline or the decision to declare no confirmatory primary;
2. CHD/HF ICD inclusion lists and inpatient semantics;
3. T2D/HTN cohort-at-risk denominators;
4. stroke delivery and event-construction algorithm;
5. Hogan's weather/HM-CM lock;
6. IRB/governance determination;
7. external dissemination approval;
8. author order or co-first designation; or
9. journal submission.

## 11. Reproducibility and reporting

- Every result must be generated by an orchestrated script.
- Every table row carries `data_status`, `result_class`, model ID, and outcome.
- Failed fits remain in a status table.
- Main claims map one-to-one to a claim ledger.
- Release checks verify table-to-ledger-to-manuscript identity, provenance,
  multiplicity recomputation, and manifest hashes.
- Null, discordant, and failed-calibration results remain visible.
- Raw correspondence, HA source counts, and merged health panels are not
  committed.
