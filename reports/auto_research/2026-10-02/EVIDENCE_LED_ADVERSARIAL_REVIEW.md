# Evidence-led manuscript: adversarial scientific and visual review

**Review date:** 2 October 2026. **Scientific disposition:** no additional must-fix overclaim or critical numerical mismatch identified in the reviewed revision. **Document disposition:** final main pages 6–11 and unchanged supplement pages 1–3 visually inspected; no actionable layout defect identified. This review does not establish submission readiness, verified extraction semantics, clinical identification or leading-journal suitability.

The reviewer prepared the competitor audit and supplied bibliographic checks, but did not write the main manuscript, supplement, analysis runner or figures. This is an independent implementation review, not a blinded replication or an independent primary-data analysis.

## Scope and version binding

Reviewed the full current Markdown main article and supplement, the evidence-led protocol, the common-basis R runner statically, all four new figure captions/source descriptions, and the released source tables. The reviewer did not read governed monthly health files, execute R models, retrieve an extraction query, or obtain laboratory/individual records.

Reviewed SHA-256 values:

- Main Markdown: `8bab6dc9868f5104d594cf23b0a287fbc04df026faf560f55ed2aba9d50efe0c`.
- Supplement Markdown: `26a04d776634a6bcd8e212f41b78cd37a5a23b7302d85c957ec9298615dfdeed`.
- Evidence-led protocol: `06b89a19704821539160a8573a974594ec201027f6278bbe393054498d2167a4`.
- Common-basis runner: `a2e6be74b43ae8a0d8715e5bb3e7809a8d271c7d0e447d945cc3498ca9c763e3`.

Later edits require affected claims and pages to be rechecked. Prior Phase 2 document QA is not treated as verification of these new renders.

## Scientific attacks and outcomes

**Nested-window difference misread as period effect:** rejected by the current text. Main Methods lines 63–65, Table 2/caption, Results and Supplementary Figure S1 consistently state that 84 months are contained within 132 and that the spline basis is recalculated. No independent later-period slope, subtraction test or protection-by-CI-overlap is reported.

**Admissions misread as incidence or physiological benefit:** rejected by the current framing. Methods lines 33–37 and 61 distinguish the supplied first post-diagnosis stay from principal-diagnosis admissions and outcome-specific eligible person-time. The diagnosis interval is not asserted to prove a closed cohort. The early maximum and later rebound are not treated as proofs of particular extraction artefacts.

**External study substituted for evidence in this population:** no such substitution identified. Main Discussion lines 136–154 separates externally plausible mechanisms from the current counts. Youn/Hu qualitative descriptions stay within the checked abstracts. The inconsistent Youn aggregate sample and Korea interval are not imported. Yau's revised paragraph distinguishes CHD/HF/kidney findings from less conclusive stroke/mortality and recognises the attendance, survival and future-infection selection. Its supplemental code lists remain unchecked, as recorded separately.

**Null result converted to absence of weather or physiological change:** rejected. All twelve full-window q-values are reported, with no weather-exclusion inference. Wong's clinical null is described as no evidence of overall adjusted improvement, not equivalence. Sparse support, calendar sensitivity and nominal uncertainty remain acknowledged. Main Figure 3 displays historically discussed diagnostic contrasts, explicitly directing the reader to the complete panels.

**Novelty rescued by feature accumulation:** rejected by the revised Introduction and limitations. The paper does not claim that adding laboratories, care records or later years is inherently novel. The proposed expanded measurement/observation study remains conditional; neither global uniqueness nor causal decomposition is asserted.

**Prepared runner presented as a result:** rejected by the protocol. It states NOT RUN and distinguishes common-basis direct association contrasts from causal COVID effects. Static inspection confirms whole-series spline construction, direct interaction terms, joint later-slope covariance, declared sensitivity scenarios, complete twelve-slot families and explicit failure rows. This is a source-code assessment; numerical execution and coverage calibration remain unverified. Schema verification, clinical-target choice, primary-design freeze and validation remain prospective requirements.

## Numerical verification against released aggregates

Annual source totals reproduce **156,156 CHD** and **29,681 HF** recorded events. Arithmetic 2020-versus-2019 changes round to **−17.4% / −16.2%**; 2023-versus-2019 changes round to **−0.6% / −2.0%**. Source rows show the preceding decline and the 2021/2022/2023 rise/fall/rise without a pandemic counterfactual.

The baseline primary family is identified in `cvd_core_robust_estimates.csv` by `manuscript_role=amended_core_candidate` and `se_method=NeweyWest_lag6`. This yields twelve rows with minimum BH q **0.192239059851566**. A broad single-exposure/days-only filter also includes alternative fits and is not the primary family; those rows were not mixed into this check.

The cold-day baseline ratios/bounds match the main article: CHD **0.994631216608471 (0.948784429293951–1.04269339431323)** and HF **1.07280014928024 (1.00645431800469–1.14351952165835)**. The nested source gives CHD **1.03638701985241 (1.00650546105469–1.0671557149755)** and HF **1.11283089052394 (1.05303734075742–1.17601963669547)**. Rounded displayed values agree.

The unrounded HF minimum-temperature upper bound **1.00004966372439**, p **0.0504136413025569**, verifies the supplement's explicit inclusion of one. The CHD hot-night residual lag-one correlation in the plot source is **0.507802854196383**, agreeing with 0.508. An HAC interval being narrower is not diagnosed as invalid from this residual statistic alone.

Independent exact field comparisons matched every annual figure source row (**22**), every nested-window figure source row (**12**) and every selected-calendar figure source row (**14**) to a unique released table row. These checks verify transcription and plotting source selection; they do not reproduce the governed original analysis. The conceptual figure contains no invented numerical cohort flow.

## Visual inspection and actionable residue

Viewed original-resolution final PNGs from `.research-build/evidence-main-final/page-6.png` through `page-11.png`, after the final abstract and equation-layout revisions, and `.research-build/evidence-supp-render/page-1.png` through `page-3.png`. The supplement source hash is unchanged. Separately inspected original standalone observation-process and annual-count PNGs. All four figure functions were inspected either standalone or embedded in the reviewed pages. No plot-label clipping, table overflow, text overlap or unreadable intervals were identified in these pages. Supplementary Figure S1 preserves its shared ratio scale and overlapping-window warning. Calendar panels have visibly different scales; their captions correctly restrict interpretation to within-panel sensitivity.

**Cleared visual false alarm:** the final page 11 footer is centred and reads `11`, matching the document numbering. The root reviewer also independently confirmed the original footer at original resolution and a single Word section. The earlier report of a right-aligned solitary `1` was an inspection error; no repair is required. The root reviewer separately owns main pages 1–5; this report does not claim those pages were visually checked by this reviewer.

**Remaining scientific limits:** the source extraction specification is unavailable; eligible person-time and laboratory measurements are absent; no direct interaction has been executed; external validation is unconfirmed; decisive competitor supplements remain unchecked. These are boundaries on publication claims, not defects that additional prose or figures can resolve.
