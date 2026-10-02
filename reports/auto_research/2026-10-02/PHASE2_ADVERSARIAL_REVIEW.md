# Phase 2 independent adversarial review — 2 October 2026

Scope: revised scientific body of `manuscript/covid_period/Manuscript_covid_period_draft.md`; temporary table/reference tokens excluded. This is a review of a completed exploratory manuscript, not a demand for a new transfer, output or formal pre/post finding. No governed files were opened and no outcome models were fitted. Provenance checked: existing `HA_APPROVED_AGGREGATE` descriptive/model summaries, public scripts, and the bounded external-literature memo.

## Verdict

The revised scientific body survives the earlier adversarial objections. **No must-fix scientific inference remains in the reviewed body.** This verdict does not certify the eventual populated tables, reference numbering, graphics or submission declarations. Those require final assembly checks.

The paper now makes a useful bounded distinction: descriptive count decline, pandemic-era trough/rebound, and sensitivity of thermal associations. It does not manufacture a post-only estimate, infer a physiological benefit, or treat an unadjusted comparison as a pandemic effect. Completion does not require new outcome fits.

## Earlier problems resolved

- “The diagnosis interval does not establish a closed cohort or a monotonically declining population at risk.” This repairs the unjustified closed-cohort/depletion assumption.
- “Their difference is not an estimated pre/post effect.” The revised Methods additionally disclose overlapping samples and recalculated spline knots/boundaries. This matches `scripts/32_cvd_trend_depletion_lag.R` and its frozen sensitivity table.
- “Hot-night estimates increased in both outcomes when later years were included: from 1.011 to 1.022 for CHD and from 0.965 to 1.003 for HF.” This repairs the previous erroneous opposite-direction claim.
- “A pandemic-era utilisation shock can change a fitted weather coefficient if its timing is associated with weather after calendar adjustment; a lower overall count does not predict attenuation in every model.” This repairs the unconditional attenuation prediction.
- “The lag-six interval being narrower does not itself show that the covariance estimate is invalid: a sandwich covariance depends on regression score autocovariances, not solely on residual autocorrelation.” This repairs the HAC claim; [sandwich's official documentation](https://sandwich.r-forge.r-project.org/reference/vcovHAC.html) describes estimating-function autocovariances.
- “The thermal panel also cannot exclude weather as an explanation for the count trajectory.” The unjustified ruling-out language is removed.
- “In particular, the early maximum does not prove an artefact of first-in-window recording, and the later rebound does not disprove a changing risk set.” This repairs the previous depletion/ascertainment assertions.

## Numerical spot checks

`outputs/tables/cvd_descriptive_annual_totals.csv` supports 2019/2020/2023 totals of 12,396/10,237/12,323 for CHD and 2,344/1,964/2,296 for HF. Percentage changes versus 2019 are −17.42%/−16.21% in 2020 and −0.59%/−2.05% in 2023; the manuscript's one-decimal values are correct. Both outcomes rise in 2021, fall in 2022, and rise in 2023.

`outputs/tables/cvd_descriptive_covid_era_means.csv` supports the disjoint 84/36/12-month descriptive means. `cvd_trend_depletion_sensitivity.csv` supports the displayed nested/full cold-day ratios and COVID-phase-adjusted ratios. These outputs contain no post-only 48-month thermal coefficient or interaction contrast.

The Wong paragraph's warning about the actual 2020/2021 sampling dates is supported by the [primary Methods, Subject section](https://link.springer.com/article/10.1186/s12875-025-02893-z). Its null adjusted differences do not establish equivalence or physiological recovery. The revised paragraph properly avoids those claims. The other physiological examples were checked against `literature/covid_physiology_evidence_2026-10-02.md`; this review does not replace the separate primary-source/reference audit.

## Optional wording refinements

1. “There were 156,156 CHD-associated and 29,681 HF-associated first hospitalisations.” The Methods supplies the correct meaning, so this is not a finding error; however, “associated” may sound disease-caused in the abstract. Prefer “There were 156,156 first recorded hospitalisations after CHD diagnosis and 29,681 after HF diagnosis.” Apply the same refinement to the corresponding Results sentence.
2. “The most directly relevant local study, by Wong and colleagues, found no overall adjusted improvement in HbA1c or blood pressure among regular primary-care attenders with type 2 diabetes.” Prefer “found no evidence of an overall adjusted improvement” to avoid treating a null test as proof of no change. The following design caveats already limit the interpretation appropriately.
3. “The recovery approached the late pre-pandemic level rather than the much higher 2013 level.” “Counts returned towards the late pre-pandemic level…” would further prevent “recovery” from being read as health recovery. The current context explicitly concerns counts and is defensible.
4. Abstract cold-day intervals could be labelled Newey–West lag-six directly. The body already defines the display convention; this is clarity, not a numerical repair.

## Final assembly boundary

Populate tables and references from the declared sources, keep first-recorded post-diagnosis wording in captions, and check that no export restores the old ruling-out or physiological-improvement language. Ethics, authorship and permission declarations remain human-owned submission items; no approval should be inferred or supplied by this review. No new scientific result is required for this exploratory manuscript.

## Final assembly verdict — populated main and supplement

Reviewed absolute working-clone files:

- `/private/tmp/laidlaw-autoresearch-20261002/manuscript/covid_period/Manuscript_covid_period_draft.md` — SHA-256 at review: `54a9bca2ac2a99331a7712da7ea6b3ca6e7adfb9db71fc9eceaa16596080487f`.
- `/private/tmp/laidlaw-autoresearch-20261002/manuscript/covid_period/Supplement_covid_period.md` — SHA-256 at review: `1562518c8edf77e4621cc27ea8180f2a4eadee14fdac4534633c94a57650845b`.

**Final scientific assembly passes. No must-fix scientific claim or misplaced nested/full column was found.** All four prior optional prose refinements were applied. Outcome definitions and captions preserve first recorded hospitalisation after diagnosis, with unavailable admission cause and no incidence denominator. Main Table 2 labels the pre-2020 84 months separately from the full 132 months and assigns their ratios/intervals correctly. No post-only thermal inference or physiological finding has appeared during assembly.

The supplement retains all twelve baseline tests and their full-window lag-six BH family. Independent string checks against `cvd_core_robust_estimates.csv` verified all twelve baseline ratio/interval and p/q displays (minimum unrounded q `0.192239059851566`) and all 48 uncertainty intervals. Checks against `cvd_trend_depletion_sensitivity.csv` verified all 54 official-day sensitivity ratio/interval strings across main and supplement. These checks supplement, rather than replace, the main/supplement semantic column read. Source files were existing approved summaries; no new fits or monthly health data were used.

All fourteen numbered references are populated, and no temporary table/reference tokens remain. Clinical evidence claims preserve selected populations, observational limitations, the Wong sampling-date caveat, different infection/AMI/HF endpoints, and vaccination conditional on infection. These claims remain hypotheses or external context rather than imported findings from this series. No further literature expansion or new outcome analysis is needed to finish this exploratory paper.

One optional display clarification remains: HF mean-minimum-temperature NW6 upper bound is `1.00004966372439`, displayed as `1.000` in S2 and `1.0000` in S4. A short note that this interval includes one on the unrounded scale, or displaying `1.00005` for that bound, avoids ambiguity. The p-value and current interpretation are correct, so this is not a substantive inference failure. This suggestion was sent to the parent agent before final export.

Document visual QA (reported separately as eight main plus three supplement pages) is outside this text-and-source audit. Ethics, author approvals and external submission permissions retain their human ownership. The assembled manuscript is a completed exploratory draft, not a newly confirmed causal or physiological result.

Final display clarification implemented: the supplement now gives the HF mean-minimum lag-six unrounded upper bound (1.0000496637) and p = 0.0504, explicitly confirming inclusion of one. The direct source auditor checks both values.
