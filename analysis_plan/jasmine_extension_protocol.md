# Jasmine definition-harmonised extension protocol

**Target window:** January 2013–December 2023

**Project outcome:** Monthly Hong Kong stroke-event aggregates, subject to Roro's timing and governance rules

**Status:** Protocol only. “Jasmine's paper” has not been identified, and no source-paper coefficient or new stroke coefficient is reproduced or claimed.

---

## 1. Aim and naming rule

The immediate aim is to preserve the earlier paper's thermal definitions and ask whether the pattern Dr Bishai recalls remains visible in a later window ending in 2023. Dr Bishai remembers more non-significant (“null”) p-values on the hotter side and fewer on the colder side.

Use the word **replication** only if the team has the exact source and can match its outcome, exposure, time unit, population, lag and model closely enough to reproduce its target estimand. If the earlier paper used daily mortality and the present project uses monthly stroke aggregates, call the work a **definition-harmonised extension** or **transport of the exposure definition**, not an exact replication.

---

## 2. Paper identity: stop/go gate

### Leads, all explicitly unconfirmed

1. **Wang, Ren et al. (2019):** Hong Kong daily all-cause mortality and extremely hot weather events, 2006–2015; DOI `10.1016/j.scitotenv.2019.07.039`. This matches the approximate end year and supplies 5VHD, 5HN and 2D3N definitions. Public metadata reviewed so far do not explain the “Jasmine” label.
2. **Meeting-note lead:** “Liu et al. 2020, South China cold/hot attributable fraction, 2006–2016, *Sustainable Cities and Society*.” The exact title, authors and DOI have not been verified. Do not cite this string as a confirmed paper.
3. **Adjacent verified lead, not presumed to be Jasmine's:** Sida Liu et al. (2020), Hong Kong high/low-temperature mortality, 2007–2015, *IJERPH*, DOI `10.3390/ijerph17197326`.

### What Bob should confirm with Dr Bishai

Ask for the PDF, DOI or full citation and then confirm:

- What does “Jasmine” refer to: author, student, analyst, file name or presentation?
- Which figure/table/supplement contains the recalled hotter-versus-colder null pattern?
- Does “month” mean calendar-month strata, monthly observations, seasonal groups, or temperature bins?
- What was the outcome: all-cause mortality, cause-specific mortality, stroke, admissions, excess deaths or attributable fraction?
- What geography and population were analysed?
- What were the exact study dates and analysis time unit?
- Which temperature variable, thresholds, reference period, season and event-gap rule were used?
- Were heat and cold defined absolutely, by percentile, relative to minimum-mortality temperature, or by a spline?
- What lag window, model family, seasonality control, long-term trend and covariates were used?
- What fixed collection of tests generated the p-values Dr Bishai remembers?
- Does Dr Bishai want same-outcome reproduction, exposure-definition transport to stroke, or both?

**Stop rule:** do not code a “Jasmine” model or quote a cold/heat contrast until these points are resolved. Generic catalogue definitions may proceed under their own IDs.

---

## 3. Source-definition extraction

Once the paper is confirmed, create a versioned source manifest containing:

| Field | Required transcription |
|---|---|
| Citation | Full authors, title, journal, year, DOI |
| Population/outcome | Exact numerator, denominator and exclusions |
| Time unit/window | Daily, weekly or monthly; first and last date |
| Exposure series | Station/grid, temperature variable and aggregation |
| Hot definition | Threshold, percentile, duration and season |
| Cold definition | Threshold, percentile, duration and season |
| Reference | Comparison temperature/category and threshold reference period |
| Event assignment | Start, touch, end or event-day burden across months |
| Lag | Same day/month and all lag terms |
| Model | Family, link, offset, seasonality, trend and covariates |
| Test universe | Every outcome × month/season × exposure × lag contrast |
| Reported output | Effect measure, interval and p-value location |

Two people should independently check the manifest against the methods and supplement. Record unresolved ambiguities rather than filling them by convention.

---

## 4. Exposure reconstruction and overlap check

1. Acquire the HKO series needed by the source rule. Retain raw dates and quality flags.
2. Implement the source rule exactly, including its original reference period and percentile algorithm. Do not recalculate thresholds on 2013–2023 for the primary extension.
3. Preserve daily runs across month/year boundaries. Record how events spanning two months are assigned.
4. Unit-test known edge cases: threshold equality, one-day gaps, permitted two-day gaps if applicable, missing days, February, and events crossing 31 December.
5. Produce an exposure-only audit table by month: hot/cold flag, component counts, event starts, event days, intensity and missingness.
6. Use the project's overlap with the source window—provisionally 2013–2015 for the Wang/Ren lead, or 2013–2016 if the second lead is confirmed—to compare exposure coding with any published or author-supplied event list.

If source outcomes are unavailable, the overlap step validates **exposure coding only**. It cannot validate or reproduce the paper's health coefficients.

---

## 5. Extension through 2023

Apply the locked source definition unchanged from January 2013 through December 2023. Retain:

- `source_definition_primary`: original threshold/reference construction;
- `contemporary_threshold_sensitivity`: threshold recalculated on a pre-declared later climatology, if the team wants it;
- exposed-month count and complete selected-month list for both;
- explicit flags for COVID-era months and missing exposure/covariate data.

The contemporary-threshold result answers a different question and must not silently replace the source-definition extension.

### Outcome alignment

Roro should supply aggregates assigned to the true stroke-event month. First GOPC mention is a marker, not automatically the event date. Do not infer unavailable HA field meanings, include AMI without admission reasons, or expose small cells.

If only monthly stroke aggregates are available, aggregate source-defined daily event metrics to month before joining. State plainly that this changes both outcome and temporal estimand relative to a daily mortality paper.

---

## 6. Statistical model and staged comparison

Use the existing P01–P18 framework. For count outcomes, begin with a pre-specified negative-binomial or quasi-Poisson model, subject to diagnostics, with:

- population × days-in-month offset where appropriate;
- calendar-month seasonality;
- a pre-specified smooth long-term trend;
- source-matched meteorological controls where available;
- staged pollution, absolute-humidity and influenza sensitivities rather than automatic inclusion; and
- the same stroke definition in every hot/cold comparison.

Run in this order:

1. **Exposure audit:** no outcomes; verify prevalence, overlap and missingness.
2. **Source-definition primary:** unchanged thermal rule and pre-specified model.
3. **Definition sensitivity:** one alternative at a time, labelled by HM/CM code.
4. **Covariate sensitivity:** add pre-labelled covariate sets without changing the exposure rule.
5. **Period sensitivity:** pre-COVID and full-window comparisons, without treating a difference in significance as evidence of effect modification.

Never select the reported definition because it yields the smallest p-value.

---

## 7. Month-stratified null-pattern design

### 7.1 First resolve what “month-stratified” meant

The source may have used:

- twelve calendar-month-specific estimates;
- broad hot- and cold-season strata;
- monthly time-series observations grouped by thermal definition; or
- several temperature bins/definitions that were described informally as months.

Replicate the actual structure once confirmed. The following is a fallback design, not a claim about Jasmine's methods.

### 7.2 Pre-specify a fixed test universe

Before fitting outcomes, freeze:

- one stroke outcome definition;
- one lag rule;
- matched hot and cold definition pairs;
- the hot/cold calendar grouping if required by the source;
- the covariate set;
- all subgroup contrasts; and
- the multiplicity family.

If no source grouping exists, a provisional seasonal contrast can use May–September versus November–March, leaving April and October as shoulder months. The team must approve this before outcome inspection.

### 7.3 Primary inference

Avoid twelve isolated regressions: 2013–2023 supplies only 11 repeats of each calendar month. Fit a pooled model with planned exposure-by-season or exposure-by-calendar-month interactions. Use:

1. a global Wald or likelihood-ratio test for interaction/heterogeneity; and
2. a pre-specified linear contrast between the average hot-side and cold-side coefficients, with the weighting rule frozen in advance.

Report each estimate with its confidence interval. A p-value is not an effect size, and p ≥ 0.05 is not evidence of no effect.

### 7.4 Secondary reproduction of the recalled “null” pattern

For the fixed test universe only, define a result as “non-significant at 0.05” exactly as the source did, then report:

- number of tests in each hot/cold family;
- number and proportion with p ≥ 0.05;
- raw and multiplicity-adjusted p-values;
- coefficient signs, magnitudes and confidence intervals; and
- the hot-minus-cold difference in non-significant proportions.

Because models share months, outcomes and definitions, ordinary binomial tests falsely assume independence. If uncertainty around the proportion difference is required, refit the complete fixed panel in a **year-block bootstrap**, preserving all months within a sampled year. With only 11 years, label this uncertainty analysis exploratory and inspect stability. Do not add tests after seeing which family appears less null.

If the source's p-value set cannot be reconstructed, do not claim confirmation or refutation of Dr Bishai's recollection.

---

## 8. Interpretation guardrails

The idea that populations in South China might be relatively resistant to heat mortality yet vulnerable near approximately 10°C cold is a **discussion hypothesis only**. The present ecological time series cannot identify genes, ancestry effects or causal adaptation. Heat acclimatisation, housing, air conditioning, behaviour, occupation, age structure, health care and selective survival are plausible non-genetic explanations.

Treat 10°C as a candidate exposure cutoff (`CM05`/`CM17`), not a biological threshold. Even if cold estimates are less often non-significant than heat estimates, that pattern alone cannot establish adaptation, genetics, mechanism or causality.

---

## 9. Minimum reporting package

- Confirmed source citation and locked extraction manifest.
- Exposure-code version and threshold/reference metadata.
- Monthly hot/cold audit table through December 2023.
- Overlap validation result, explicitly limited to exposure coding if outcomes are unavailable.
- Model specification and complete fixed test universe.
- Estimates, confidence intervals, exposed-month counts and multiplicity information.
- A paragraph distinguishing exact replication, definition extension and new monthly stroke analysis.
- An honesty statement: no genetic inference; no invented source or stroke coefficients; synthetic runs are not findings.
