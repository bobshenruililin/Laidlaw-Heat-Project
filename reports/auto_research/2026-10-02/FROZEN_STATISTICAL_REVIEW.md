# Independent hostile statistical review — frozen manuscript

**Date:** 2 October 2026. **Role:** statistical adversary, independent of manuscript and figure authors. **Evidence anchor:** PR #103, commit `7060606fbe44b14b6b2893929781ac477cea1d46`. **Disposition:** no blocking statistical claim or transcription error identified in the source-bound revision below. This is an editorial review of released summaries, not primary-data replication, design certification or submission approval.

## Revision binding

- `manuscript/covid_period/Manuscript_covid_period_draft.md` — SHA-256 `420ddf1bdc0b14b3b57eed5fdfa3452e3e59853a2d87c9e72f006846627d7366`.
- `manuscript/covid_period/Supplement_covid_period.md` — SHA-256 `8c5b793570a346f9f49f6bcf3f5b22e1db05eae08fe8524d4bb2ea271152e15d`.
- `figures/covid_period/frozen_publication/annual_counts_source.csv` — SHA-256 `ebe38735ff9f5bc038175b9bf45c85b898cc1dce2991bbc88f9135f399a180b4`.
- `figures/covid_period/frozen_publication/complete_weather_source.csv` — SHA-256 `e9e4c09482c020bbac20e52037024b32cd8d7723ac15b837f87c152adcf2ab7e`.
- `figures/covid_period/frozen_publication/model_criticism_source.csv` — SHA-256 `e189f1c1b615300307898702359a29737b6236e3739cf0adc80688a9e9402884`.

All nine immutable source hashes in `frozen_evidence_manifest.json` matched at review. Baseline source scripts were inspected to verify days-only specification, single-exposure models, natural-spline reconstruction, covariance settings and interval construction. Governed monthly files were not read; no model, simulation, new subgroup or alternative calendar was run.

## Independent numerical audit

A separate CSV/Markdown parser, without using the manuscript builder's audit implementation, verified:

- All 22 annual totals, both cumulative totals (156,156 and 29,681), six disjoint-period means and the four rounded percentage comparisons with 2019. Both annual series decline throughout 2013–2019; 2020 is the minimum annual total; the 2021/2022/2023 rise/fall/rise description is correct.
- Every estimate, confidence interval, p-value and q-value in the twelve-model full-window panel. Recomputing BH across these twelve Wald p-values matched the released q-values to approximately 1e-15; the minimum is 0.192239059851566.
- All twelve official-day nested/full estimates and intervals; all 42 official-day alternative-calendar entries; all 48 baseline uncertainty intervals; all twelve released diagnostic rows.
- The 48 baseline interval identities `exp(beta ± 1.96 SE)` and point-estimate identities `exp(beta)` to maximum absolute discrepancy 4.9e-15. The frozen source uses 1.96 rather than a higher-precision normal quantile; preserving these released values is appropriate.
- The near-null HF mean-minimum-temperature lag-six upper bound is 1.00004966372439 and its Wald p-value is 0.0504136413025569. The supplement explicitly states that the interval includes one; rounded 1.000/1.0000 values do not turn this into a nominal finding.

## Attacks and disposition

| Attack | Severity if omitted | Disposition in reviewed revision |
|:--|:--|:--|
| Treat a days-in-month offset as eligible cohort person-time | Major | Resolved: count-ratio estimand is explicit; population incidence is not claimed. |
| Subtract nested pre-2020 and full-window coefficients as a period effect | Major | Resolved: overlap, rebuilt spline bases and absence of an independent later-era fit/interaction are explicit. |
| Select nominal positive thermal findings while dropping the rest of the panel | Major | Resolved: complete twelve-model family, all q-values and null outcomes are retained. |
| Interpret non-rejection as no weather contribution or equivalence | Major | Resolved: text expressly rejects both inferences. |
| Describe HAC as automatically inflating uncertainty or proving valid coverage | Major | Resolved: coefficient-specific covariance differences, score-autocovariance explanation and uncalibrated finite-sample status are explicit. |
| Use interval crossing/overlap as a formal difference test | Major | Resolved: main caption and Methods reject this use. |
| Hide alternate calendar/start-window or phase-intercept results | Major | Resolved for article's official-day sensitivity family: all seven alternatives are in S5; phase adjustment is visible in Results. |
| Change the interpretation of rounded near-null intervals | Major | Resolved: exact HF Tmin caveat and four-decimal uncertainty table are visible. |
| Treat the 2020 comparison with 2019 as a pandemic counterfactual | Major | Resolved: comparisons are unadjusted arithmetic within a longer declining series. |

## Residual scientific risks

1. **Event/risk-set validity remains unverified.** Without query verification, first-event eligibility, look-back, deaths and eligible person-time, even perfectly reproduced count models cannot establish clinical incidence or physiological improvement. No prose repair resolves this design limit.
2. **Nominal uncertainty is not certified.** The released CHD baseline residual ACF1 values are approximately 0.51–0.53, with small Ljung–Box p-values. Newey–West lag-six covariance is a fixed display convention, not demonstrated finite-sample coverage. The manuscript describes this limitation correctly. Small or large residual ACF alone does not determine score-covariance validity.
3. **Exploratory multiplicity persists beyond the twelve-model family.** BH q-values apply only to that family and inherit the validity and dependence assumptions of the underlying tests. Calendar/window and alternative-covariance comparisons are exploratory and are not protected by those q-values. No confirmatory interpretation is approved.
4. **The diagnostic examples are historically selected.** HF cold days and CHD hot nights earn their display as model criticism, not as newly selected confirmatory endpoints. All twelve baseline contrasts remain visible.
5. **Full frozen-source retention is necessary.** The source CSV contains 108 calendar/window rows. Forty-two continuous-exposure alternative-calendar estimates are not expanded into article tables; they must remain in the unchanged released-source reproducibility package. That is an editorial space choice, not deletion of negative knowledge.

No defect requiring new scientific analysis was identified. Numerical agreement with summary files does not verify the extraction implementation, original fit environment or patient-level construction. Material changes to the bound text or source snapshots require an affected review; frozen-source changes require a separately recorded freeze issue.
