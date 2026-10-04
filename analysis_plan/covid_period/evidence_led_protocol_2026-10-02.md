# Evidence-led study protocol — 2 October 2026

**Status: prospective readiness specification, not a registered or frozen primary analysis.** No new HA transfer, laboratory extract or separate approved later-period model output has arrived. Previously inspected count patterns and thermal estimates remain exploratory. This protocol replaces neither source definitions nor human scientific/dissemination decisions.

## The decision this study should resolve

When recorded hospitalisations fall, distinguish changes in health, care contact, observation and eligible population. A recorded first hospitalisation after a diagnosis is an observation process, not a validated incident cardiovascular endpoint. Multiple explanations may coexist. New fields and additional years alone do not establish novelty: Yau et al. (2026; DOI [10.1111/dom.70984](https://doi.org/10.1111/dom.70984)) already examines continuity of care, CHD/HF, clinical covariates and competing mortality with follow-up into 2024. The separately maintained novelty audit must identify a question and discriminating design beyond that work before an expanded paper is advertised as original.

## Measurement audit and required reconciliation

The 7 August receipt documents territory-month counts (`year`, `month`, `chd_inpatient` or `hf_inpatient`), January 2013–December 2023; the cohort universe is recorded T2D and/or HTN during that interval, and the event is the first recorded hospitalisation after the first relevant CHD/HF diagnosis. Admission cause is absent. The receipt's early general-population offset is historical: the current association analysis uses days in month only. Neither offset supplies eligible cohort person-time.

**Source extraction query not located:** a tracked-file search for SQL/query/extraction records found no executable source query or verified extraction specification. The receipt describes the intended construction; it does not verify its implementation. Request a non-sensitive specification or analyst attestation, not a copy of patient rows. Do not infer a closed cohort or inevitable depletion from the diagnosis interval or declining counts.

Reconcile, before incidence analysis:

- T2D/HTN entry rule and date; prevalent versus newly recorded disease; eligibility before each cardiovascular event; whether eligibility uses diagnoses occurring after an event; any look-ahead selection.
- CHD/HF code lists, diagnosis setting, historical look-back and observable history; first-ever versus first-observed event; prevalent cardiovascular disease handling; whether diagnosis and hospitalisation on the same date qualify.
- Event linkage/order, inpatient/day-case/ED inclusion, admission date versus discharge date, recurrent admissions, transfers and deduplication; available principal/secondary diagnosis definitions and validation evidence. Existing counts cannot be relabelled cause-specific.
- Outcome-specific risk sets and departures at event, death, migration/loss of observable follow-up or study end; re-entry rules and cohort refresh; death linkage completeness. First CHD and first HF risk sets need not be identical.
- Coding/system changes, missingness, observation coverage and suppression rules, including whether suppressed cells are distinguishable from true zeros.

The audit's deliverable is a signed or otherwise traceable semantic specification, an annotated query/version identifier where permissible, and aggregate reconciliation checks. A person identifier or detailed clinical record must not enter this repository.

## Separate targets and boundaries

**Recorded burden:** monthly counts of the supplied first-recorded construction; describe period patterns with calendar duration. No cohort incidence or physiological improvement follows.

**Eligible-population incidence:** only after a validated event definition and outcome-specific eligible person-time exist. Analyse entry/exit and competing mortality. A cause-specific hazard, subdistribution quantity and cumulative incidence answer different questions; choose based on the clinical target before fitting. An improved survivor mean cannot establish improved health in the original population. Infection-related death or loss of attendance is not ignorable censoring by default.

**Weather association change:** a direct difference in conditional monthly exposure slopes across a calendar split, using one full-series calendar basis. It is neither an identified effect of COVID nor a test that weather caused the burden decline. No subtraction of nested/full-window estimates is allowed.

**Mechanism:** repeated measurements, care utilisation and infections can test discriminating predictions. Adjustment-induced coefficient changes are not mediation evidence. Conditioning on infection, vaccination, attendance or survival may select patients or block a pathway; draw and justify the relevant causal graph before choosing an adjustment set.

## Rival predictions: observations capable of weakening the explanation

1. **Physiological improvement.** Predicts clinically coherent within-person improvements, measured before the outcome, beyond changes in treatment and measurement/attendance composition. Worsening or precisely null trajectories across adequately observed representative eligible patients weaken a broad improvement explanation. Survivor/attender-only improvements do not discriminate it from selection. Specify meaningful clinical differences from clinical evidence and blinded baseline information, not observed p-values; report uncertainty and coverage before concluding a test was severe.
2. **Care disruption.** Predicts contact/testing reductions, delayed presentations, altered severity or deaths despite fewer recorded admissions. Stable contact/observation coverage with a precise decline in validated incidence and no adverse mortality pattern weakens a disruption-only explanation. Reduced contacts could accompany better health; correlation between contacts and events alone is not decisive. Mortality must be comparably defined and its ascertainment checked.
3. **Risk-set or recording change.** Predicts changes aligned with eligibility, cohort replenishment, coding, look-back or linkage. Stable audited definitions and eligible person-time, with persistent standardised event changes, weaken a recording/risk-set-only account. Agreement between two outputs from the same flawed extraction is not independent validation.
4. **Respiratory suppression.** Predicts calendar/co-circulation alignment and stronger change where infection-triggered pathways are plausible. A stable association through respiratory circulation changes, with adequate precision and comparable support, weakens the specific prediction. Ecological influenza is an imperfect proxy for individual exposure; broad non-pharmaceutical interventions also change behaviour. Missing influenza months are not zero activity.
5. **Changing thermal susceptibility.** Predicts directly estimated period differences under common support and plausible calendar/co-exposure controls. Precisely small interactions weaken a substantial change; wide intervals or sparse cold-positive months are inconclusive. Neither a null nor a changed weather slope rules out weather as one contributor to burden.
6. **Model/calendar artefact.** Predicts consequential instability under declared temporal flexibility, influential observations or dependence handling. Reproducible direction and precision across justified alternatives weaken this account but cannot repair outcome measurement. No specification earns priority by preserving a preferred interval.

For each proposed test record target population, expected adverse observation, smallest meaningful detectable difference, design assumptions, exposure/measurement support, and achieved precision. Simulation is labelled SYNTHETIC and evaluates error detection, coverage and calibration; it is never manuscript evidence about Hong Kong. Do not equate non-significance with equivalence. A progressive research move adds a distinctive prediction or resolves a measurement problem; specification hunting that protects a preferred conclusion is degenerative.

## Prepared common-basis analysis

The explicit-input runner is `scripts/83_covid_common_basis_interactions.R`. It performs separate negative-binomial fits for CHD/HF crossed with mean temperature, Tmax, Tmin, hot nights, cold days and very hot days. Continuous contrasts are per 1 degree Celsius; official-day contrasts are per five days, not consecutive spells.

Baseline formula: `n_events ~ exposure_scaled * later + factor(month) + splines::ns(time_index, df=4) + offset(log(days_in_month))`, using the whole 132-month series. `later` initially denotes January 2020 onward; February 2020 is the declared timing sensitivity. Trend df6 and df8 are fixed sensitivity scenarios, never elected by significance. Each scenario's basis is constructed once on the complete series and shared by the two period slopes. Year fixed effects, alternative influenza/co-exposure controls, influence diagnostics and eligible-person-time models are subsequent declared criticisms, not silently substituted models in this runner.

Report pre slope, later slope and direct interaction using full coefficient covariance: Var(beta+gamma)=Var(beta)+Var(gamma)+2Cov(beta,gamma). Export the joint two-slope covariance as well as the interaction uncertainty. Display model, HC1, NW3 and NW6 uncertainty; NW6 uses prewhite=FALSE and adjust=TRUE. No silent quasi-Poisson, alternate trend or model-SE fallback is permitted. Complete all twelve interaction slots for each split/trend/SE method; failed/unsupported fits retain missing results and a reason. BH adjustment covers twelve tests within each declared scenario/method, including failed slots. Only January/df4/NW6 is the continuity display; other scenarios are sensitivities, not independent discoveries. This is an exploratory extension until human design lock, not retrospective preregistration.

Export exposure support by calendar month and period, overlap/zero support, Pearson residual and regression-score autocorrelations. Small support cells describe design limitations, not a numerical gate invented to suppress inconvenient results. Nominal normal intervals/HAC estimates need finite-sample calibration; the prepared runner does not certify calibrated coverage. Coefficients must not be promoted to findings until analyst execution, diagnostics, calibration and output approval occur.

A schema demonstration may use `Rscript scripts/83_covid_common_basis_interactions.R --chd /absolute/analyst/chd.csv --hf /absolute/analyst/hf.csv --output /absolute/analyst/new_empty_run --approval-receipt /absolute/analyst/execution_receipt.json`. These are illustrative paths, not known files. The output parent must exist. Synthetic fixtures require `--synthetic-calibration` and compatible synthetic provenance instead of an execution receipt. Run the synthetic interface test with `Rscript tests/test_covid_common_basis_interactions.R`; it does not open governed data.

**Execution status on 2 October: NOT RUN on real or synthetic panels.** An R runtime was not available in the development environment. A supplied synthetic R test exercises known contrasts, joint covariance, complete families and invalid input rejection when a runtime and dependencies are available. Passing contract/static checks does not verify numeric model execution.

## Governed analyst handoff and stop/go decisions

1. Submit the draft request separately for review; obtain scope and access decisions through the appropriate human process. No message has been sent.
2. Receive only a non-sensitive schema/dictionary/semantic receipt here. The analyst executes row-level construction and linked analyses inside the approved environment; identifiers, exact clinical dates and patient measurements stay there.
3. Analyst validates eligibility/events/deaths and emits approved aggregation or approved estimates. Counts are not automatically safe because they are aggregate. Document small-cell handling, export authority and version/hash lineage.
4. For the monthly runner provide explicit CHD/HF CSV paths and a human-approved execution receipt matching their SHA-256 hashes. No automatic secure-directory discovery or remote access occurs. Outputs initially have status AWAITING_DISCLOSURE_REVIEW and remain outside the repository; the receipt permits execution, not public dissemination.
5. Verify schema and event semantics, resolve novelty, then lock the prospective linked-data SAP and validation definitions before inspecting new associations. Existing results are labelled exploratory. Plan registration is not asserted by a local draft.
6. **Go** to linked clinical evaluation when the fields and measurement process can distinguish at least two plausible explanations and the novel comparison is supported. **Stop/redirect** if event/risk-set semantics cannot be established or the proposed contribution duplicates existing studies. Retain the bounded count paper and adjust venue; do not add uninformative models as a substitute.
7. An independent governed population with harmonised definitions is external validation. Hospital-cluster holdout is internal validation. Public mortality patterns are triangulation. Keep external results reserved until the primary plan is locked; explain transportability and differences, not just direction agreement.

## Current residue

Produced a measurement reconciliation checklist, an unsent governed-data request, an executable-input contract and a prepared direct-interaction runner. No new coefficients, clinical measurements, ethics facts, authorship decisions, external validation or publication approval were created.
