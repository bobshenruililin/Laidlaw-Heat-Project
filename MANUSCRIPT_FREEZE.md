# Manuscript editorial evidence freeze

**Anchor:** PR #103, commit `7060606fbe44b14b6b2893929781ac477cea1d46`, Git tree `fe1c2560d9367483df8d4d327cff3d26e61e1ae6`. The local equivalent has the same tree. **Authority:** Bob selected this evidence set and requested an editorial finalisation. This record does not register a study, freeze a confirmatory primary, close Gate 3, verify the extraction query or grant dissemination/submission approval.

## Central contribution

Recorded first hospitalisation counts after CHD or HF diagnosis declined before 2020, fell further in 2020 and recovered towards 2019 levels by 2023. The temporal description is arithmetic, not a counterfactual pandemic-effect estimate. Weather models test the stability of associated interpretations, not the mechanisms generating the trajectory.

## Permitted empirical claims

The supplied T2D and/or HTN population yields two 132-month territory series, January 2013–December 2023. The endpoint is the first recorded hospitalisation after first relevant CHD/HF diagnosis; admission cause is absent. The total recorded events are 156,156 CHD-associated stays and 29,681 HF-associated stays, not a unique combined patient count.

All 22 annual totals and disjoint period means may be described. Relative to 2019, 2020 totals are 17.4%/16.2% lower and 2023 totals 0.6%/2.0% lower. These are unadjusted comparisons. “Recovery” refers only to recorded counts towards the late pre-pandemic level.

The complete twelve-model full-series NB family, with days-in-month offset, calendar-month indicators and four-degree-of-freedom natural spline, is exploratory. Its lag-six BH q-values all exceed 0.19 (minimum 0.192239059851566). Retain model/HC1/NW3/NW6 intervals and all declared existing calendar sensitivities. Near-null rounding must not change interpretation.

Pre-2020 84-month fits are nested in the full 132 months, with recalculated spline bases. They may be presented as analysis-window sensitivity. No independent 48-month later-era coefficient, direct interaction, joint window-difference test or weather standardisation exists in the frozen evidence.

## Measurement and inference limits

Source extraction implementation, diagnostic codes, look-back, first-event/same-day rules, entry/exit, eligible person-time and death linkage remain unverified or unavailable. Do not call the stays cause-coded cardiovascular admissions, incident disease, first-ever disease, a closed cohort or evidence of a necessarily depleted risk set. No laboratory, treatment, infection/vaccination or individual care-contact trajectory is available here.

No claim of physiological improvement, causal COVID effect, protective cold, changed thermal susceptibility, weather exclusion, mediation or external validation is permitted. Null and discordant results remain visible. External clinical literature is contextual evidence, with abstract-only and unchecked-supplement status retained; it cannot substitute for measurements in this extract.

## Allowed editorial operations

Rewrite and reorder prose; relocate duplicate tables; plot all frozen estimates; add source-bound labels, arithmetic checks and accessibility improvements; verify citations; and conduct hostile review. Do not fit new outcomes, select new calendars/subgroups, simulate new empirical support or change source estimates. A source defect is a freeze issue to record and resolve separately, not an invitation to reanalyse.

The prepared interaction runner remains prospective and unexecuted/uncalibrated here. It is excluded from the completed-manuscript reproduction path. Human ethics, authorship, dissemination and venue decisions remain distinct from writing quality.

## Source binding

Machine-readable hashes and baseline-document references are in [frozen_evidence_manifest.json](manuscript/covid_period/frozen_evidence_manifest.json). Immutable source files must match these hashes at every final audit. Baseline manuscript hashes identify the starting revision; prose, ledger and export hashes are expected to change during this authorised writing pass.

- `outputs/tables/cvd_descriptive_annual_totals.csv` — SHA-256 `2d4997276d77e28761083117e292f438506d07db639deba5bc17c1843e4862e8`.
- `outputs/tables/cvd_descriptive_covid_era_means.csv` — SHA-256 `338b3a0b426238013f9d11e37e8225d42c2a1f4279eb80a825e3e5407b4fe84c`.
- `outputs/tables/cvd_core_robust_estimates.csv` — SHA-256 `6acfc6f5082780c681c05c48b5953579ad7095d379429dc6125230c8c0824dd4`.
- `outputs/tables/cvd_trend_depletion_sensitivity.csv` — SHA-256 `061158111bbc79478b8cb54f27687447c213fd1bfc13efe9cf3309996f348e5e`.
- `outputs/tables/cvd_core_model_fit.csv` — SHA-256 `a486c75264f15fca2e71afed6b0132d49fa301aeae04ae9bb8747a64f76de124`.
- `reports/data_receipt_2026-08-07.md` — SHA-256 `bc54ade4d974a3400692fd5500e68c4f557c75f7af0b33de17b96263e4206497`.
- `literature/covid_novelty_sources_2026-10-02.json` — SHA-256 `5e18f2ddf12d63338accc143e132c78d4998242309b462540cd527e4fce679de`.
- `literature/covid_novelty_audit_2026-10-02.md` — SHA-256 `c2c6a3c0b9fdc9b56fc8c520f7a7aff4f43503bb7d1fa1a92dc787c9efbc44c9`.
- `literature/covid_physiology_evidence_2026-10-02.md` — SHA-256 `10ffcb962e64fe81c9fa3181fceeef6e4772b73153bd5e53dd079d60184246be`.
