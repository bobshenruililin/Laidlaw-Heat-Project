# Statistical reporting audit — 4 October 2026

This is a new, read-only review of the current COVID manuscript, independent of its authoring role. It applies the Nature Statistics reporting checklist to the fixed evidence selected by `MANUSCRIPT_FREEZE.md` (PR #103, `7060606fbe44b14b6b2893929781ac477cea1d46`). It does not certify the original extraction, replicate primary-data models, establish calibrated coverage, or close a scientific or submission gate.

## Revision reviewed

- Manuscript SHA-256: `de0d9dac038b5449b7dc7bf12feb71f60ce23b4f852d8fbd6847f44c6716a045`.
- Supplement SHA-256: `9a8f7f90ac3150418a060a86637e3c173402c7a6d9bfdacd28d37802efcdf926`.
- All nine immutable evidence hashes matched the freeze.
- Read: both sources; the five frozen numeric summary tables; main-figure source CSVs; original model-summary generators 31 and 32; descriptive generator 27; historical non-sensitive coverage summaries. No governed monthly health file was accessed. No fit, calendar search, simulation or new hypothesis test was run.

## Design and inference readout

The analysis concerns two territory-level monthly count series, with available windows of 132 months (2013–2023) and 84 nested months (2013–2019). Months are temporally dependent observations, not independent participants or biological replicates. The 156,156 CHD and 29,681 HF recorded stays are outcome-specific counts, not a combined count of unique people. The recorded event follows the first relevant diagnosis; cause-specific admission and incident disease are not established.

The days offset adjusts calendar duration, not the eligible population. Baseline weather models use one exposure per model, calendar-month indicators and a four-degree-of-freedom time spline. There are twelve full-window outcome–exposure combinations. Benjamini–Hochberg adjustment applies to their lag-six Wald p-values alone. Model, HC1, NW3 and NW6 intervals are alternative uncertainty constructions on the same coefficient. Calendar/window sensitivities remain exploratory. Nested fits reconstruct their time-spline bases and cannot be subtracted as a period effect.

## Independent numerical verification

A separate CSV/Markdown parser, without calling the manuscript builder's audit, checked all nine physical supplementary tables:

- All 22 annual totals, both cumulative totals, six period means and the four percentage comparisons with 2019. The unrounded falls were 17.41690868% and 16.21160410% in 2020, and 0.58889965% and 2.04778157% in 2023. The rounded text is correct. Both series decrease in each year through 2019; 2020 is the annual minimum; the later rise/fall/rise description is correct.
- All twelve baseline estimates, intervals, p-values and q-values; twelve nested/full official-day estimates; 42 official-day alternative-calendar estimates; 48 baseline uncertainty intervals; and twelve released diagnostic rows.
- Recomputed BH adjustment across the twelve released p-values: maximum absolute discrepancy `9.99e-16`; minimum q `0.192239059851566`.
- Checked all 48 baseline and 108 calendar/window point-estimate and interval identities against `exp(beta)` and `exp(beta ± 1.96 SE)`: maximum absolute discrepancy `4.89e-15`. Two-sided standard-normal baseline Wald p-values agreed within `1.46e-15`. These are arithmetic checks of released summaries, not new model fitting.
- Verified the twelve complete-weather and 22 model-criticism source rows against the frozen numeric tables.
- Confirmed the HF mean-minimum-temperature NW6 upper bound `1.00004966372439`, with p `0.0504136413025569`: the interval includes one. Existing near-null rounding caveats are correct.

No numerical transcription or claim-blocking statistical error was found in the reviewed revision. No frozen-source change is recommended.

## Consequential reporting changes

| Priority | Location | Finding and recommended revision |
|:--|:--|:--|
| P1 | Methods, “Uncertainty and model criticism”; Fig. 2; Table S3 | State that Wald tests are **two-sided with a standard-normal reference**, and that the displayed **nominal pointwise 95% intervals are not multiplicity-adjusted**. Scripts 31 and 32 explicitly use `2 * pnorm(abs(beta/SE), lower.tail=FALSE)` and `exp(beta ± 1.96 SE)`. BH adjusts the twelve p-values; it does not turn the intervals into simultaneous intervals or certify FDR control when the input tests are uncalibrated. |
| P1 | Methods sample-size/missingness reporting; human completion checklist | Released `n_months` is populated from `nrow(dat)`, not `nobs(model)`, in both original model-summary generators. It establishes the available window size but does not independently certify the observations retained after model-frame missing-value handling. Report window sizes accurately and retain fitted sample size/missing-value handling as a factual verification item. **There is no evidence here that months actually were omitted.** Do not replace this uncertainty with an assertion of missing data or silently change the reported window. |
| P2 | Fig. 3 legend; Table S5 | Call S5 the “complete **official-day** calendar panel”, not the complete calendar panel without qualification. The 42 continuous-exposure alternative-calendar values are retained in the unchanged source CSV and reconstruction package, not expanded in S5. |
| P2 | Figs. 2–3 and S2, Table S5 legends | Make the available window explicit where useful: baseline 132 months; nested 84; first-12/first-24 omission windows 120/108. Label these as time-series observations/windows, not independent sample sizes. Avoid claiming verified fitted `n` until the preceding item is resolved. |
| P2 | Model-criticism Results | Describe the magnitude as well as interval crossing. HF cold-day baseline is 1.073 (1.006–1.144), the eight-df spline 1.062 (0.994–1.135), and the first-24-month omission 1.043 (0.965–1.127). This shows modest point-estimate changes with uncertain precision rather than turning threshold crossing into evidence of different effects. No difference test is available. |

Ready-to-paste uncertainty wording, subject to editorial integration:

> Wald tests used two-sided standard-normal reference probabilities. Nominal pointwise 95% confidence intervals were calculated as exp(β ± 1.96 SE) and were not adjusted for multiple comparisons. Benjamini–Hochberg adjustment covered the twelve full-window lag-six p-values jointly; the alternative covariance, window and calendar comparisons remained exploratory.

## Missingness verification boundary

Historical `chd_qc_summary.csv` and `hf_qc_summary.csv` report 132 rows, no absent calendar months and no suppression flags. `cvd_descriptive_temp_correlations.csv` reports 132 complete outcome–temperature pairs for each continuous exposure; descriptive script 27 computes that field with `complete.cases`. These provide useful support for available outcome and continuous-temperature coverage. They do **not** independently establish complete official-day exposure/control model frames, the active R `na.action`, or actual fitted `nobs`. They are contextual checks, not added empirical findings or a change to the freeze. Original R/package versions are also not supplied by the frozen model summaries.

`AUTHOR_INPUT_NEEDED`: verify actual fitted observations, any omissions/imputation and the original R/package versions from the approved run log or model objects. Confirm the extraction definition and eligible risk set as already required by `SUBMISSION_COMPLETION.md`. This is a submission-completion item; the current descriptive totals remain source-consistent.

## Residual reviewer risk

The largest limitation remains event/risk-set validity, not mathematical transcription. The paper cannot identify physiological improvement, a causal pandemic effect, changed thermal susceptibility, or weather exclusion. CHD residual dependence and uncalibrated nominal uncertainty limit thermal inference; q-values inherit those input-test limitations. The historically selected HF cold-day/CHD hot-night examples are justified only as diagnostics. Preserve the complete family and source CSVs. None of these limitations can be repaired by stronger prose or a different significance threshold.

Affected statistical wording and figures should receive a final check after editing; the revision hashes above identify the starting audit, not automatic approval of later changes.

## Affected-check closure — 4 October 2026

The revised manuscript and supplement were reviewed after the authoring pass. Final text bindings for this check:

- Manuscript SHA-256: `b888668495a3bf70615c3284c98d4576c3b558e4f82c9dba0a35c24ccebb44fe`.
- Supplement SHA-256: `35595709a25d9927b26e18a20b81e936152a7c9368b227e96df961b5afdf0b03`.

All recommended statistical reporting changes were incorporated: nominal pointwise normal-reference intervals, two-sided zero-coefficient Wald tests, explicit non-adjustment of interval endpoints, the defined twelve-test BH family, dependent months, calendar-window versus verified fitted-observation counts, and the official-day scope of the expanded sensitivity table. The new HF cold-day prose values, 1.062 (0.994–1.135) for the eight-df spline and 1.043 (0.965–1.127) after the first-24-month omission, match frozen sources. All supplementary table cells remain identical to the previously checked values. All nine frozen scientific/context hashes remain unchanged.

The revised text keeps missing-value handling unresolved without asserting that data were missing. It also retains the absence of a separate later-era model/interaction and rejects weather exclusion. No remaining blocking statistical reporting defect was identified in these text revisions. Actual fitted observations, original software versions, extraction validity and uncalibrated coverage remain the human/run-record verification items described above. This closure covers statistical text, numerical source consistency and caption meaning; rendered-page and figure-layout inspection belong to the separate production review.

## Final wording and supplement proof check — 4 October 2026

The final abbreviation and precision pass was read, including the restored lag-six specification in the abstract, the absence of a direct period comparison, and expanded CI, HC1 and HAC terms. These do not change the statistical conclusions. The manuscript now binds to SHA-256 `191c33f104c0a6ee7a0a7dbf5bbe0a1087be1f66689d8a1e6a0d435982335cd4`; the supplement source remains `35595709a25d9927b26e18a20b81e936152a7c9368b227e96df961b5afdf0b03`. All nine immutable source hashes were rechecked and remained unchanged.

All six supplement page images in `.research-build/oct4_supp/` were individually inspected using the original-resolution image viewer. Tables were readable, complete and uncropped; no rows or numerical intervals broke across pages. S6 continued between its CHD and HF blocks, with the HF label and column headings intact. The source paragraph continued from page 4 to page 5 without loss. Both supplementary figures and their captions were coherent: S1 marked the observation process as conceptual; S2 visibly warned that the windows overlap and supply no independent later-period estimate or difference test. No consequential visual defect was found.

The reviewed renderer PDF was `.research-build/oct4_supp/Supplement_covid_period.pdf`, SHA-256 `2d29997e0fdf88e4189729083c62f72fbd98c3b356eede1af5add24cb780d353`. This is the rendered proof reviewed here; the production step must copy this version to the canonical deliverable. Exact inspected PNG bindings:

| Page | SHA-256 |
|:--|:--|
| 1 | `72beb7d9aac8dae53a12e66a96765ac2173824182d716ebc6114af4bb1e4b380` |
| 2 | `78cfcb5cbe13235f5a74045f1a103f4e394a45c7ccb968d1e3807eb7d99c02fe` |
| 3 | `64d49720681b4bbea3dc1da80045c1ab90f0bf9e790e6468b00065c6e7d56b45` |
| 4 | `6b9b705c568241c65b3a0980f0032591c2489961f0a90ddcccf82805869a885a` |
| 5 | `0eb359a94cd914a813619b9567a273c303584119bdba2ce647878f3a2782a9a0` |
| 6 | `9469787f50a73b633a2ee79515cc0dae580ca02bb27129ecca966f37ba08acea` |

This final addition extends the statistical review to the six rendered supplement pages. It does not claim inspection of the main manuscript pages or of standalone main-figure exports, which have separate production-review ownership.
