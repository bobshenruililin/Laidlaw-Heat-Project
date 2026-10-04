# Scientific protocol for the next discriminating analysis

The completed exploratory manuscript separates recorded first-hospitalisation burden from weather associations. Its approved aggregate summaries establish a decline before 2020, a further dip in 2020 and return towards 2019 totals by 2023. They do not establish physiological improvement, an independent later-era thermal coefficient or weather exclusion. No new laboratory data or approved outcome fit was available.

## Metadata relevant to interpretation

The documented transfer contains year, month and a first-hospitalisation count for each outcome. Admission cause, eligible person-time, laboratory results, treatment and individual infection histories are absent. First-event timing, diagnostic code inclusion, look-back, deduplication and entry/exit rules are not established by the count columns. A diagnosis interval does not prove a closed cohort or inevitable depletion. General-population denominators cannot supply the missing risk set.

These are measurement limits in the study, not evidence that the underlying health system has no clinical fields. Clinical improvement would require repeated measurements and information about attendance and testing, rather than another coefficient on the existing counts.

## Competing explanations and adverse predictions

- **Physiological improvement:** predicts improved repeated clinical measurements among eligible people, beyond selection into continued care. External evidence is mixed; the local HbA1c/BP study found no evidence of overall adjusted improvement. A benefit in selected subgroups remains possible.
- **Care disruption:** predicts reduced contacts or altered presentation timing without requiring better physiology. Hong Kong admissions/mortality studies make this plausible for 2020, but do not identify the explanation for these events or the preceding decline.
- **Risk-set or event recording:** predicts changes aligned with eligibility, look-back or coding transitions. Neither the early maximum nor later rebound resolves this explanation without extraction rules and eligible population counts.
- **Respiratory suppression:** predicts changes concentrated in winter or respiratory circulation. Reduced influenza exposure could alter cold-day associations without changing the direct effect of cold. Infection among eligible people was not measured.
- **Thermal susceptibility change:** predicts a direct period interaction with adequate exposure support and stable interpretation under plausible calendar/co-exposure controls. Existing nested/full fits do not test it.
- **Calendar/model sensitivity:** is already observed. All twelve full-window q-values exceed 0.19. No spline or uncertainty estimator should be selected for retaining an attractive interval.

## Analysis protocol if suitable data become available

Separate the recorded-count target from the exposure-by-period association and from any causal pandemic effect. For a direct association contrast, use one full-series model with a common calendar basis and exposure-by-period terms. Report pre and later slopes and their direct contrast with joint uncertainty. January 2020 is the initial calendar split consistent with the existing subset; February 2020 is a declared timing sensitivity. Do not subtract full and nested coefficients.

Inspect within-season exposure support, especially cold-positive months, before interpreting an interaction. Diagnose regression-score dependence as well as residual dependence, influential observations and calendar sensitivity. Report an inconclusive contrast when the analysis has little capacity to detect error.

Keep the complete exposure/outcome family. If twelve interaction tests are treated as one confirmatory family, specify its multiplicity procedure before fitting. Do not choose an exposure, spline or cut date from its p-value. For influenza criticism, compare models on the same observed months; early missing influenza months are not zero activity. Covariate-adjustment changes do not automatically identify mechanisms or overcontrol.

Physiological testing additionally requires repeated clinical measurements, treatment and attendance information. Lower values among tested attenders can reflect selection. Relevant measures may include HbA1c, blood pressure, lipids and renal function, with dates, units and testing frequency; selectively ordered troponin or BNP requires its clinical indication. These are proposed measurements, not transferred fields or completed analyses.

Before each test, state the observation that would weaken its explanation and whether the test could detect that observation. A new model is progressive when it produces a distinct prediction or resolves a measurement problem. Repeated specification changes that merely preserve a preferred coefficient are degenerative. Falsification, severe testing, causal reasoning, model criticism and strong inference thus determine the next measurements and contrasts, without manufacturing an affirmative result.

## Publication boundary

The manuscript and source-verification package are complete for scientific review. Submission facts remain in the separate completion checklist. This protocol contains scientific hypotheses and proposed analyses only; it does not assign collaborator responsibilities or disclose internal governance deliberations.
