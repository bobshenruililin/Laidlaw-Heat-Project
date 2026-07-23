# Jasmine definition-harmonised extension protocol

**Target window:** January 2013–December 2023

**Project outcome:** Monthly Hong Kong stroke-event aggregates, subject to Roro's timing and governance rules

**Status:** Protocol only. “Jasmine’s paper” is now confirmed as Jingwen Liu et al. (2020), *Sustainable Cities and Society* 57:102131, DOI `10.1016/j.scs.2020.102131`. Headline findings are locked; the full paper and supplement still need source-definition extraction. No new stroke coefficient is reproduced or claimed.

**Companion reads:** `literature/jasmine_liu2020_confirmed.md`, `literature/roro_manuscript_deep_read.md`, and `literature/exceed_jasmine_and_roro_baseline.md`.

---

## 1. Aim and naming rule

The immediate aim is to preserve Liu et al.’s thermal definitions and ask whether a source-matched pattern remains visible in a later window ending in 2023. Dr Bishai remembers more non-significant (“null”) p-values on the hotter side and fewer on the colder side. That recalled test pattern is **not yet verified from the full text**.

What is already confirmed from the 2020 paper is a cold-dominant mortality burden: cold AF 4.72% versus heat AF 0.16%, and moderate-temperature AF 4.25% versus extreme-temperature AF 0.63%. These AF contrasts motivate the symmetric design but are not stroke coefficients or substitutes for reconstructing the source test universe.

Use the word **replication** only if the team has the exact source and can match its outcome, exposure, time unit, population, lag and model closely enough to reproduce its target estimand. If the earlier paper used daily mortality and the present project uses monthly stroke aggregates, call the work a **definition-harmonised extension** or **transport of the exposure definition**, not an exact replication.

---

## 2. Paper identity: resolved; source extraction remains a gate

### Locked citation

Jingwen Liu, Alana Hansen, Blesson Varghese, Zhidong Liu, Michael Tong, Hong Qiu, Linwei Tian, Kevin Ka-Lun Lau, Edward Ng, Chao Ren and Peng Bi. “Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016.” *Sustainable Cities and Society*. 2020;57:102131. DOI `10.1016/j.scs.2020.102131`.

The paper uses Hong Kong daily mortality, a distributed lag non-linear model integrated with quasi-Poisson regression, and reports a reversed J-shaped relationship. At extreme cold, the highest reported RR is for injury mortality: 2.18 (95% CI 1.03–4.62), lag 0–21.

### What the full PDF and supplement must still resolve

- Which figure/table/supplement contains the recalled hotter-versus-colder null pattern?
- Does “month” mean calendar-month strata, monthly observations, seasonal groups or temperature bins?
- What are the exact minimum-mortality reference, moderate/extreme boundaries and percentile algorithms?
- What are the spline degrees of freedom, knot locations, lag basis, seasonality, trend and covariates?
- What fixed collection of estimates/tests generated the p-values Dr Bishai remembers?
- Which exact RRs and lag phases were subsequently extracted for Roro’s `HWD_Tavg` scenario?
- Does the requested extension include a same-outcome mortality reproduction, definition transport to stroke, or both?

**Stop rule:** generic HM/CM catalogue coding may proceed. Do not label a model “Jasmine-source-matched,” reproduce the recalled p-value pattern, or invent source spline parameters until the full text and supplement are transcribed.

---

## 3. Source-definition extraction

Once the full paper and supplement are ingested, create a versioned source manifest containing:

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
6. Use the project’s **2013–2016** overlap with Liu et al.’s confirmed 2006–2016 window to compare exposure coding with any published or author-supplied event list.

If source outcomes are unavailable, the overlap step validates **exposure coding only**. It cannot validate or reproduce the paper's health coefficients.

---

## 4.1 Roro bridge: team baseline, not a substitute for Jasmine extraction

Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika and David Bishai’s 2026 medRxiv v1 paper transports Liu et al. (2020) heat RRs into a 2014–2023 excess-death model. Its `HWD_Tavg` scenario starts a 20-day window at daily mean temperature around the 99th-percentile threshold of 30.60°C and uses RR phases for day 0, days 1–5 and days 6–21. Roro also applies Wang/Ren daily-maximum, daily-minimum and 2D3N definitions.

These four Roro definitions should be extended/collapsed to monthly exposure metrics through 2023 as a **separately labelled team-baseline family**. They do not reveal every parameter of Jasmine’s DLNM, and Roro’s mortality RRs must not be reused as stroke coefficients.

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

The full source may show:

- twelve calendar-month-specific estimates;
- broad hot- and cold-season strata;
- monthly time-series observations grouped by thermal definition; or
- several temperature bins/definitions that were described informally as months.

Replicate the actual structure once transcribed. The following is a fallback design, not a claim about Jasmine’s methods.

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
