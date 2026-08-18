# Independent Round A — methods and causal-inference audit

**Role:** scientific and methods lead  
**Date:** 15 August 2026  
**Status:** static audit of the named manuscript, dictionary, and disclosure-minimised release outputs  
**Provenance:** health estimates are `HA_APPROVED_AGGREGATE`; `data_processed/variable_dictionary.csv` describes a `SYNTHETIC` development panel and is not a governed HA data dictionary.

This review did not receive or assume a preferred thesis. The monthly health
analysis panels and HA microdata are absent (`PARKED_NO_PANEL`), so no model was
re-fitted and no monthly health series was reconstructed. The audit can assess
the reported models and released tables, but it cannot verify undisclosed
field-level outcome rules or source-data missingness.

## Population, exposure, comparator, outcomes, design, estimand

### Population

The statistical population is not all Hong Kong residents and not a stable
closed cohort. It is the monthly aggregate of people described as diagnosed
with type 2 diabetes and/or hypertension during 2013–2023 who could contribute
a first recorded hospitalisation after a first CHD or HF diagnosis record.
The number still at risk of a first event in each month is unavailable.
Eligibility, entry, survival, prior-event exclusion, and the executable timing
rule cannot be audited from the release.

### Exposure

Each model uses one territory-month exposure from HKO Headquarters:

- monthly mean of daily mean, maximum, or minimum temperature, reported per
  1 °C;
- monthly count of official hot nights (daily minimum temperature at least
  28 °C), very hot days (daily maximum temperature at least 33 °C), or cold
  days (daily minimum temperature at most 12 °C), reported per five days.

These are ambient station-based monthly proxies. They do not measure personal
temperature, indoor temperature, nighttime heat intensity, or daily exposure
immediately before an event.

### Comparator

The comparator is model-based rather than a physical intervention: a
territory-month with an exposure value one reporting unit higher than another
month at the same calendar-month category and fitted time-spline value, with
days in month held through the offset. For extreme-day counts, the reporting
unit is five days. Different ways of producing the same monthly mean or count
are treated as equivalent even though their daily sequence, intensity,
humidity, and co-exposures may differ.

### Outcomes

The outcomes are monthly counts labelled as the first recorded
hospitalisation after the first CHD diagnosis record and after the first HF
diagnosis record. Admission cause was not delivered. They are therefore not
principal-diagnosis CHD/HF admissions, AMI admissions, recurrent events,
mortality, or daily triggered events. Inpatient-only semantics are inferred
from released column labels and remain unconfirmed. Age, sex, and disease
subtype strata were not released.

### Design

This is an ecological territory-month time series with 132 months from January
2013 through December 2023. The twelve exposure–outcome models were specified
after the outcome series were available and are exploratory. The core design
does not contain individual linkage between exposure, covariates, and outcome.

### Estimand

Let \(Y_t\) be an outcome count, \(X_t\) one scaled exposure, \(d_t\) days in
month, and \(C_t\) the calendar-month indicators and fitted time spline. The
reported model implies

\[
\frac{E(Y_t\mid X_t=x+1,C_t,d_t)}
     {E(Y_t\mid X_t=x,C_t,d_t)}
=\exp(\beta).
\]

Thus the estimand of record is a **model-conditional ecological monthly
expected-count ratio** per reporting-unit contrast. It is not an incidence-rate
ratio because cohort person-time is absent. It is not an individual,
daily-triggering, controlled direct, total, or other causal effect. There is no
identified causal target estimand in the available design: an intervention on
“one additional degree” or “five additional threshold days” is not uniquely
defined, and exchangeability, temporal ordering, and the risk set are not
established.

## DAG-style assumption list (text, not a figure file)

The following text DAG makes the necessary distinctions. Arrows denote
plausible data-generating relations, not relations established by this
dataset.

1. **Season and long-term time:** calendar season and secular time
   \(\rightarrow\) temperature; pollution; influenza; cohort size and
   composition; diagnosis and admission practice; health-care access; and
   monthly CHD/HF counts. Month indicators and a smooth time term block only
   the forms of these common causes represented by the fitted functions.
2. **Weather system:** synoptic conditions, humidity, rainfall, solar
   radiation, and atmospheric stagnation \(\rightarrow\) measured temperature
   and pollutant concentrations; these factors may also \(\rightarrow\)
   hospitalisation counts. Humidity and rainfall were assembled but not in the
   core models; solar radiation and stagnation are not in the inspected
   dictionary.
3. **Ozone:** meteorology and emissions \(\rightarrow\) ozone; ozone may
   \(\rightarrow\) health. Temperature may also affect ozone formation.
   Consequently, ozone could be a correlated co-exposure, a proxy for shared
   meteorology, or part of a temperature-related causal sequence. The available
   aggregate series do not determine which DAG is correct. Calling ozone a
   “pathway variable” is not licensed.
4. **Other pollution and infection:** nitrogen dioxide, particulate matter,
   and influenza activity may \(\rightarrow\) hospitalisation counts and
   co-vary with season, weather, mobility, and the COVID period. They are absent
   from the core panel. Archive models do not resolve this confounding and, for
   influenza, do not use the core offset.
5. **Risk set and composition:** cohort entry, age, sex, disease severity,
   duration of diabetes or hypertension, prior disease, survival, and prior
   first event \(\rightarrow\) the number at risk and monthly counts. The
   dynamic risk set is unobserved. A days-in-month offset does not block these
   paths.
6. **Medication and care:** medication use, adherence, blood-pressure and
   glycaemic control, preventive care, coding, care seeking, and hospital
   capacity \(\rightarrow\) recorded hospitalisation. These may vary over time
   and during COVID. They are not measured in the inspected dictionary or
   release outputs.
7. **Housing and behaviour:** housing, air-conditioning access, occupation,
   mobility, socioeconomic position, and heat/cold avoidance \(\rightarrow\)
   personal exposure and susceptibility \(\rightarrow\) hospitalisation.
   Headquarters temperature does not block these paths.
8. **Selection:** diagnosis with diabetes or hypertension, receiving a CHD/HF
   diagnosis record, surviving and remaining event-free, and reaching hospital
   determine inclusion in a monthly first-event count. Conditioning on this
   selected and changing cohort can induce selection bias if determinants of
   diagnosis, survival, or care also vary with weather or calendar time.
9. **Exposure measurement:** true personal and neighbourhood exposure
   \(\rightarrow\) Headquarters proxy only imperfectly. Applying one station
   territory-wide creates spatial and personal-exposure error. The station–grid
   comparison reported in the manuscript shows that agreement for monthly mean
   minimum temperature does not validate threshold hot-night classification.
10. **Outcome measurement:** latent clinical event and diagnosis/admission
    processes \(\rightarrow\) released “first hospitalisation after first
    diagnosis” count. Missing admission cause and unverified inpatient/timing
    rules permit outcome misclassification relative to cardiac-cause
    hospitalisation.
11. **Temporal ordering:** same-month exposure and counts do not establish that
    exposure preceded an event. Monthly aggregation also mixes immediate,
    delayed, displacement, and cumulative relations. Month-lag models do not
    recover a daily lag-response function.
12. **Serial dependence:** prior outcome level, omitted persistent causes, and
    cohort depletion may \(\rightarrow\) subsequent counts. Newey–West
    covariance estimates alter standard errors; they do not correct an
    incorrectly specified conditional mean or remove time-varying confounding.
13. **Consistency:** a five-hot-night contrast has multiple versions depending
    on timing, consecutiveness, intensity, humidity, and indoor exposure.
    Consistency for a unique causal intervention is therefore not met.
14. **Positivity:** cold days occur almost entirely in winter and hot nights
    are always present in June–September in this window. Calendar-month
    adjustment leaves limited within-season, between-year support. Positivity
    is weak for broad causal contrasts even though coefficients are numerically
    estimable.
15. **Model form:** the reported ratio assumes a log-linear exposure relation
    within each separate model and sufficient control by month plus a
    four-degree-of-freedom time spline. The release does not establish these as
    correct causal functional forms.
16. **Missingness:** all core rows report 132 fitted months, but the absent
    source panel prevents an audit of suppressed, imputed, or structurally
    missing outcome values. Influenza covers 121 months and was not zero-filled.
    Pollutant station-month eligibility and changing station composition create
    a separate measurement/missingness issue.
17. **Multiplicity and selection:** Benjamini–Hochberg adjustment covers the
    twelve declared core contrasts. It does not protect selection across the
    wider set of lags, trend choices, offsets, joint models, archive covariate
    models, thermal definitions, or post-outcome designation of “leading”
    contrasts. Separate CHD and HF coefficients do not themselves test a
    CHD-versus-HF difference.

The principal unsupported causal assumptions are exchangeability, a stable
and correctly denominated risk set, well-defined intervention/consistency,
temporally ordered exposure, valid individual exposure measurement, and
selection-free outcome ascertainment. Regression adjustment cannot recover
these from the released aggregates.

## Recommended regression specification vs what is already fitted

### Already fitted

For each outcome and exposure separately, the analysis of record is

\[
\log E(Y_t)=\log(d_t)+\alpha+\beta X_t+
\text{calendar-month indicators}+ns(t,4).
\]

It uses a negative-binomial mean model, a days-in-month offset, Newey–West
lag-6 reporting, and a full model-based/HC1/Newey–West lag-3/Newey–West lag-6
uncertainty ladder. The same twelve point estimates appear in the core and
uncertainty tables. Benjamini–Hochberg q-values cover the twelve core
contrasts. Joint models are collinearity diagnostics, not preferred estimates.

### Recommendation under `PARKED_NO_PANEL`

No revised regression or re-fit is recommended in this round. Retain the
already-fitted specification only as an **exploratory conditional-association
model**, and report:

- the exact ecological monthly count-ratio estimand;
- the complete twelve-contrast panel and q-values;
- the full uncertainty ladder without selecting a covariance method because
  it excludes the null;
- residual autocorrelation and the unresolved CHD conditional-mean concern;
- the limited seasonal support for the extreme-day contrasts;
- archive pollution and influenza models as different specifications, not
  “adjusted core” estimates.

The existing model is not a defensible causal regression merely by adding
available covariates. Newey–West standard errors address covariance estimation,
not exchangeability, risk-set depletion, exposure error, temporal ordering, or
selection. Likewise, ratios across differently scaled exposures should not be
ranked as evidence that one thermal encoding is “more closely associated” than
another, and separate outcome models do not estimate a differential CHD-versus-
HF effect.

A future causal study would require a newly specified design, not a cosmetic
re-fit of this panel: cohort person-time, verified outcome timing and admission
semantics, a prespecified causal DAG and lag estimand, finer temporal exposure
and outcome alignment, and measured time-varying common causes. Those are data
and design requirements and are outside this parked analysis.

## Sensitivity / falsification / robustness that is already present vs still needed

### Present in the release or manuscript

- Complete twelve-model core panel with one exposure per model.
- Model-based, HC1, Newey–West lag-3, and Newey–West lag-6 uncertainty ladder.
- Benjamini–Hochberg adjustment across the twelve core contrasts; no core
  contrast is multiplicity-protected.
- Alternative trend smooths, year fixed effects, exclusion of the first one or
  two years, pre-COVID restriction, and COVID-phase adjustment.
- Contemporaneous and one- and two-month exposure-lag specifications, correctly
  labelled as month lags rather than a daily lag curve.
- Exclusion of the month with the largest Cook's distance.
- Days-only versus general-population-based offset checks, with explicit
  recognition that the latter is not cohort person-time.
- Negative-binomial versus quasi-Poisson family sensitivity.
- Joint temperature and joint extreme-day models with residualised variance
  inflation factors, retained as collinearity diagnostics.
- Pearson residual autocorrelation and Ljung–Box checks.
- Staged pollution, humidity, and influenza archive models, explicitly not
  treated as adjusted core estimates.
- Exposure-identification checks for winter concentration of cold days, summer
  intensity of hot nights, and single-station versus gridded measurement.
- A simulation gate that rejected daily-effect recovery for this dataset; no
  real daily coefficient was admitted.

### Still needed to support stronger inference, but not executable here

- A source-level audit of outcome completeness, suppression, zero handling,
  cohort entry, prior-event exclusion, and the executable diagnosis-to-
  hospitalisation timing rule.
- Monthly cohort-at-risk person-time and composition, including age, sex,
  disease duration/severity, medication, and survival.
- A prespecified causal DAG assigning pollution, ozone, humidity, influenza,
  COVID disruption, care access, and behavioural adaptation explicit roles.
- A direct formal contrast if the paper wishes to claim differences between
  CHD and HF or between exposure encodings. Current coefficient ranking is not
  such a test.
- Negative-control outcomes or exposures and a future-exposure lead
  falsification. None is present in the inspected release.
- A prespecified serial-correlation strategy whose adequacy is shown for CHD;
  the current HAC ladder does not remove residual mean dependence.
- Validation of threshold exposures against spatial or population-weighted
  personal exposure. Agreement for monthly mean temperature is insufficient
  validation for hot-night counts.
- A missing-data analysis for the incomplete influenza series and pollutant
  station composition if either is promoted beyond an archive sensitivity.
- Multiplicity accounting for the full analysis universe or, prospectively, a
  frozen primary contrast before seeing outcomes.

These are limitations and future-study requirements, not a request to re-fit
the absent panel.

## Causal vs associational language verdict, with quoted overreach if any

**Verdict:** the current live manuscript is predominantly associational and
contains unusually clear refusals of individual causality, incidence,
principal-diagnosis interpretation, daily triggering, and multiplicity-
protected claims. It does **not** report an identified causal effect. However,
several comparative or mechanistic phrases overreach what the separate,
differently scaled models establish.

Current live-file examples:

1. “CHD first-hospitalisation counts were more closely associated with official
   hot-night burden than with mean temperature or cold days, and HF counts were
   more closely associated with cold-day burden than with hot nights.” This
   ranks coefficients on non-comparable exposure scales and implies
   cross-encoding and cross-outcome comparisons that were not formally tested.
2. “The HF cold-day association is the more coherent of the two residual
   signals.” This is a post-outcome ranking, not a prespecified statistical
   estimand.
3. “It is not produced by entering correlated heat metrics jointly.” Similarity
   in a joint diagnostic does not establish what produced an association.
4. “CHD first hospitalisations were more closely associated with hot nights,
   and HF first hospitalisations with cold days, than with the other thermal
   encodings examined.” The conclusion repeats an unsupported ranking despite
   the q-unprotected panel and incomparable contrasts.

The origin skeleton, which is explicitly superseded, stated that “ozone in
particular may act as a confounder, effect modifier, or pathway variable.”
The live manuscript no longer makes that claim. The removal was warranted:
available ozone measurements and archive regressions do not identify
confounding, interaction, or mediation.

Terms such as “association,” “conditional count ratio,” “compatible with,” and
“unresolved confounding” are appropriate. “Effect,” “impact,” “pathway,”
“explains,” “protective,” or “risk” should be reserved for cited external
studies or explicitly qualified as causal quantities not identified here.

## Medication and other unmeasured factors

Medication does **not** exist in the inspected available dictionary or release
outputs. Searches of `data_processed/variable_dictionary.csv` and
`outputs/release_chd_hf/` found no medication, prescription, drug, statin, or
antihypertensive field. The dictionary is synthetic-development metadata, not
an HA source dictionary; absence therefore means **unavailable to this
analysis**, not proof that the HA's underlying systems contain no medication
records.

Medication cannot be described as adjusted, stratified, balanced, or ruled
out. Depending on the causal question, use and adherence could be prognostic,
time-varying confounders through shared seasonal or care processes, or effect
modifiers. The aggregate release cannot distinguish those roles.

Other unavailable or unresolved factors include age, sex, disease subtype,
disease duration and severity, prior cardiovascular disease, blood-pressure
and glycaemic control, smoking, socioeconomic position, housing,
air-conditioning, occupation, mobility, personal exposure, care seeking,
hospital capacity, coding changes, and the monthly cohort still at risk.
Pollution, humidity, rainfall, influenza, and COVID phase are at least partly
available, but they are not core adjustments and do not resolve the remaining
factors.

## Health-economics feasibility (yes/no and missing elements)

**No.** This dataset does not support a cost-effectiveness analysis. It contains
ecological monthly event counts and exposure associations, not an evaluated
intervention or an economic outcome model. It also does not support a causal
claim that changing a thermal metric would change hospitalisations.

Required CEA elements that are missing include:

- a defined intervention and mutually exclusive comparator;
- intervention coverage, adherence, implementation pathway, and effectiveness;
- a causal effect of the intervention on relevant health outcomes;
- cohort denominators, baseline risks, and transitions among health states;
- recurrent events, mortality, survival, and longer-term consequences;
- resource use and unit costs, including intervention and hospital costs;
- health-state utilities and QALYs, or another stated health outcome;
- analytic perspective, time horizon, cycle length, and discounting;
- model structure and parameter distributions for probabilistic uncertainty;
- equity/subgroup specification and, where relevant, a decision threshold.

At most, the released counts could motivate a separate descriptive burden or
resource-use study after linkage to validated utilisation and cost data. They
cannot by themselves estimate incremental costs, incremental health effects,
or an incremental cost-effectiveness ratio.

## Proposed methods-sentence replacements (exact old → new; no new numbers)

The replacements below add no numerical result and require no model re-fit.

### Target estimand

**Old:** “For each separate single-exposure model, the target quantity is a
count ratio associated with a 1 °C or five-day exposure contrast, conditional
on calendar month and a smooth function of time.”

**New:** “For each separate single-exposure model, the reported parameter is
the model-implied ratio of expected monthly counts under a higher exposure
value, conditional on calendar month and the fitted time spline; it is a
conditional ecological association, not a causal contrast or an incidence-rate
ratio.”

### Outcome semantics

**Old:** “For each outcome, the event was the first recorded hospitalisation
after the patient’s first diagnosis record for CHD or HF.”

**New:** “For each outcome, the released count was described as the first
recorded hospitalisation after the patient’s first CHD or HF diagnosis record;
admission cause, field-level diagnosis rules, and the executable timing rule
were unavailable for this analysis.”

### Ozone

**Old:** “Nitrogen dioxide and particulate matter were specified to enter
before ozone, because ozone is coupled with hot, sunny conditions. Staged
pollution models exist in the archive; they are not adjusted versions of the
separate core panel and were not used to claim that confounding is resolved.”

**New:** “Pollution covariates were examined only in staged archive models.
Because the causal role of ozone relative to temperature is not established,
these models are alternative associational specifications and do not identify
mediation, a pathway effect, or resolution of confounding.”

### Serial correlation and uncertainty

**Old:** “Core intervals used Newey–West standard errors with lag 6 [19],
reported together with model-based, HC1, and Newey–West lag-3 intervals.”

**New:** “The fitted coefficients are presented with the complete model-based,
HC1, and Newey–West uncertainty ladder. The Newey–West covariance estimates
address residual dependence in standard errors but do not repair
misspecification of the conditional mean or identify a causal effect.”

### Unmeasured factors

**Old:** “Age, sex, and disease-subtype strata were not delivered.”

**New:** “Age, sex, disease-subtype strata, medication use, disease severity,
blood-pressure control, housing, air-conditioning access, and individual
behaviour were not available in the inspected dictionary or release outputs
and were not controlled in the core models.”

### Cross-encoding and cross-outcome comparison

**Old:** “Under Newey–West lag-6 reporting for the core panel, CHD
first-hospitalisation counts were more closely associated with official
hot-night burden than with mean temperature or cold days, and HF counts were
more closely associated with cold-day burden than with hot nights.”

**New:** “The core panel contained a positive CHD–hot-night estimate and a
positive HF–cold-day estimate, but neither was multiplicity-protected. Because
the exposure contrasts differ in scale and no formal contrast compared
coefficients across encodings or outcomes, the panel does not establish that
one outcome is more closely related to one thermal exposure than another.”

### Joint-model diagnostic

**Old:** “It is not produced by entering correlated heat metrics jointly.”

**New:** “Its point estimate was similar in the joint extreme-day diagnostic,
which was not designated as a preferred or causal model.”

### Conclusion

**Old:** “In governed monthly aggregates for people with type 2 diabetes and/or
hypertension, CHD first hospitalisations were more closely associated with hot
nights, and HF first hospitalisations with cold days, than with the other
thermal encodings examined.”

**New:** “In governed monthly aggregates for people with type 2 diabetes and/or
hypertension, the exploratory panel contained positive CHD–hot-night and
HF–cold-day estimates, but neither was multiplicity-protected and no formal
comparison across thermal encodings or outcomes was performed.”

**Old:** “Better-denominated and more finely resolved data are required before
a thermal effect on cardiac hospitalisation in this cohort can be estimated.”

**New:** “Estimating a causal thermal effect on cardiac hospitalisation in this
cohort would require cohort person-time, verified outcome timing and admission
semantics, finer temporal alignment, and a design that addresses measured and
unmeasured common causes.”
