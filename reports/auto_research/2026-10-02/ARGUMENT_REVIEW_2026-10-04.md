# Scientific argument review: frozen manuscript

**Date:** 4 October 2026. **Role:** independent scientific-editorial critic; the manuscript author retains editing responsibility. **Revision reviewed:** manuscript SHA-256 `de0d9dac038b5449b7dc7bf12feb71f60ce23b4f852d8fbd6847f44c6716a045`; supplementary source SHA-256 `9a8f7f90ac3150418a060a86637e3c173402c7a6d9bfdacd28d37802efcdf926`. **Authority:** `MANUSCRIPT_FREEZE.md`, anchored to PR #103 at `7060606fbe44b14b6b2893929781ac477cea1d46`. This review introduces no new analysis or substantive empirical claim and does not reopen the freeze or close a human approval gate.

Applied Hamming Research stages 8–9 and the Laidlaw adapter, repository CNS-writing rules, and relevant Nature-writing argument guidance. Routing: manuscript; research; title/abstract/introduction/discussion; English; Nature-family register without importing flagship journal requirements.

## Assessment

The strongest supported contribution is a description of the recorded trajectory: a substantial decline already occurred before 2020, a further fall occurred in 2020, and counts approached 2019 levels by 2023. The paper cannot explain that trajectory causally or establish a change in disease incidence. Its secondary contribution is model criticism showing why earlier thermal interpretations require restraint. The frozen estimates support both statements; they do not supply a mechanism-discriminating study.

No new blocking contradiction in the frozen evidence was identified in this argument review. The consequential editorial weakness is allocation: weather modelling occupies most of Results, while external mechanisms occupy much of Discussion. Readers can consequently mistake the interpretive qualifications for a second, better-identified empirical story. The remedy is a shorter, explicit question–evidence chain, not stronger claims.

## Priority revisions

| ID | Finding | Authorized improvement | Boundary to retain |
|:--|:--|:--|:--|
| A1 | The Introduction first poses the broad problem of what lower hospital use means, then spends a sentence disclaiming novelty. The actual answerable descriptive question arrives less directly. | State the temporal question explicitly: how did 2020–2023 recorded counts compare with their preceding trajectory? Name related clinical studies fairly, then define this paper's different, narrower task. Delete the self-evaluative sentence about a longer series being insufficient novelty. | Do not claim the paper determines whether health improved, care deteriorated or recording changed. Do not assert that a question has never been studied without evidence. |
| A2 | The count trajectory is central, but its Results include a redundant paragraph of disjoint monthly means already fully reported in S2; most remaining text concerns weather. | Keep annual totals, 2019 comparisons, the 2021/2022 fluctuation and the pre-trend boundary in the primary subsection. Leave the complete disjoint means in S2. Frame the weather question as the stability of fitted associations under existing checks. | Retain all twelve baseline models and consequential calendar/covariance disagreements. Do not imply that these models quantify or exclude weather's contribution to the annual trajectory. |
| A3 | Results repeatedly describe whether intervals cross one. The calendar heading says interpretation is altered without distinguishing a changed coefficient from a changed uncertainty estimate. | Describe coefficient movement and precision first, then use interval inclusion as a concise qualification. State directly that covariance comparisons leave the coefficient unchanged. Route the extended score-autocovariance explanation to Methods or SI if the remaining paragraph still preserves the reason residual correlation alone does not invalidate a narrower HAC interval. | Neither changing interval inclusion nor overlap tests a difference between models. No equivalence claim follows from non-rejection. No unperformed calibration can be implied. |
| A4 | Five Discussion paragraphs partly recreate a literature inventory and compete with the central finding. | Group clinical evidence by its inferential role: reduced use can coexist with adverse outcomes; measured physiological changes are discordant and selected; respiratory suppression is plausible but unmeasured. Keep the continuity study's attendance/survival selection boundary and retain contrary findings. | Preserve specific caveats that materially prevent transfer of findings, including the Hong Kong primary-care sampling dates, the continuity study's landmark selection and the impossibility of vaccination explaining the 2020 dip. No new clinical explanation should be promoted. |
| A5 | The abstract repeats the primary trajectory and then lists several technical details whose full explanation belongs in Methods. | Give the count trajectory and its scale most of the abstract. Retain the complete-family adjusted null result and a single sentence about specification dependence and nested windows. Conclude once with the measurement limit. Use COVID-19 consistently in title and prose, where outside protected text. | The abstract must still identify first stays after diagnosis, missing admission cause/person-time, exploratory weather modelling and the distinction from physiological or causal conclusions. |

## Compact argument and terminology

**Argument:** In the supplied Hong Kong first-hospitalisation series, the 2020 decline followed a longer pre-2020 decline and counts returned towards 2019 values by 2023; exploratory weather fits do not determine why those counts changed.

| Canonical term | Meaning and use |
|:--|:--|
| First recorded hospitalisation after CHD or HF diagnosis | Supplied recorded endpoint; not a cause-coded cardiovascular admission or first-ever disease event. |
| Recorded count | Monthly or annual event total, with eligible person-time unavailable. |
| Count ratio | Conditional ecological association from the stated model; never an incidence ratio. |
| Analysis-window sensitivity | Comparison of nested 84-month and full 132-month fits; never an independent pre/post contrast. |
| Recovery towards 2019 counts | Descriptive return towards a recorded level, without implying improved health. “Rose towards 2019 levels” is an equally clear alternative. |

## Suggested local prose

For the final Introduction paragraph, an evidence-bound opening would be:

> We asked how recorded first-hospitalisation counts during 2020–2023 compared with their preceding trajectory. We examined two territory-wide monthly series after CHD or HF diagnosis among people diagnosed with type 2 diabetes and/or hypertension during 2013–2023. As a secondary question, we assessed the stability of existing weather associations across the complete model family and its calendar and uncertainty checks. These analyses describe recorded burden and the dependence of fitted associations on specification; they do not identify the processes responsible for changing counts.

This preserves a descriptive, exploratory design. It does not turn the question into a prospective hypothesis or imply a new statistical comparison.

## Remaining scientific decisions

The event extraction, diagnostic timing, admission cause, same-day eligibility, look-back, risk-set entry/exit, person-time and death linkage remain unverified or unavailable. These determine whether the descriptive record can be accepted as a publishable measure, not merely how it should be worded. The current frozen summaries cannot resolve them. The paper also lacks direct period-interaction estimates, calibrated finite-sample uncertainty and validation evidence. No stronger novelty or venue claim is justified by editorial improvement alone.

The protected HKO paragraph must remain verbatim with its aggregation clarification. Human confirmation of ethics, authorship, dissemination and submission facts remains separate. This review has not inspected primary health data or independently replicated the models.

## Author handoff

The manuscript author is implementing A1–A5 as a bounded editorial pass. Recheck the revised argument for any loss of contrary findings, endpoint precision or model boundaries before final rendering. Numerical reporting and figure geometry have separate audit owners; this review is not a substitute for either.

## Recheck of the revised argument

Reviewed on 4 October 2026 after the author's compression and statistical-reporting pass:

- Manuscript SHA-256 `b888668495a3bf70615c3284c98d4576c3b558e4f82c9dba0a35c24ccebb44fe`.
- Supplement SHA-256 `35595709a25d9927b26e18a20b81e936152a7c9368b227e96df961b5afdf0b03`.
- Abstract: 200 whitespace-delimited words. Discussion: seven paragraphs.

The revised Introduction poses the temporal question explicitly and assigns the weather models a secondary specification-stability question. Results answer them in that order. The numerical disjoint-period repetition is removed while S2 retains its complete contents. The complete twelve-model family, the nested-window limitation, interval-method disagreement and calendar sensitivity remain visible. The Discussion now moves from the trajectory to the recording process, care evidence, discordant clinical measurements, respiratory context, weather interpretation and the resulting limits. This is a coherent reduction rather than a new explanatory claim.

The favourable Taiwan findings, adverse Tokyo and survivor findings, inconclusive Hong Kong primary-care findings, landmark selection and less-conclusive stroke/mortality results in the continuity study, and temporal limitation on vaccination remain represented. All seventeen reference entries are unchanged; the protected HKO paragraph is identical to the preceding reviewed source. The supplementary edits clarify nominal pointwise uncertainty, the adjusted test family and the distinction between calendar length and verified fitted sample size; they do not change any numerical table entry. No new causal, incidence, physiological or thermal-susceptibility claim was introduced by compression.

Two small wording repairs were recommended to the author before export: replace “Overlapping analysis windows did not identify a change in thermal response” with “Overlapping analysis windows did not permit a direct period comparison”, to avoid sounding like a performed null test; restore “small” before the Tokyo cohort's adverse changes, consistent with the frozen literature memo. Neither recommendation requires reanalysis or a changed empirical claim.

**Final source recheck:** both precision repairs are present in manuscript SHA-256 `191c33f104c0a6ee7a0a7dbf5bbe0a1087be1f66689d8a1e6a0d435982335cd4`. The abstract remains 200 whitespace-delimited words and now identifies the lag-six adjusted family. Confidence interval, HC1 and HAC expansions improve first-use clarity without changing the estimates. The supplement remains SHA-256 `35595709a25d9927b26e18a20b81e936152a7c9368b227e96df961b5afdf0b03`.

**Disposition:** argument revisions satisfy A1–A5; no material remaining claim–evidence mismatch was found in these sources. Numerical audit, figure audit, rendered-document inspection and human approval facts remain separate checks.

## Rendered-proof inspection: main manuscript pages 6–9

Inspected each full-page PNG at original resolution from the final main-document render, rather than relying on extracted text. PDF SHA-256: `35dfe2bf4b13b2ef92354ab2d5ce9a2bd02e212dbce68d4b0bafb5fc5478a68c`.

| Page | Inspected material | Visual finding | PNG SHA-256 |
|:--|:--|:--|:--|
| 6 | Endpoint Methods, protected weather paragraph, aggregation clarification, descriptive comparisons and start of model specification | Body and headings remain readable with consistent spacing; temperature thresholds and chemical subscripts render correctly; heading at the page bottom has accompanying body text. No clipping or overlap. | `ad096d45c6ad1b7866d20c4c6fea3861538c394204a7c2e24335060b5a4059db` |
| 7 | Model equation, symbol definitions, uncertainty/criticism Methods and Data availability | Equation and its right-hand number are legible; subscripts and summation limits are visible; paragraph flow and numbered citations are intact. Footer is separate from text. | `aaf7c0bc2ae1e8da70b6238e2a803b7476c0377e74b8b4986376687e4264c049` |
| 8 | Code availability and references 1–14 | Repository address, bibliographic entries and DOI strings fit within the text area. Reference 14 is complete before the footer. No collision or truncation. | `1382cfac364c79fb0aaf8cab669cc108d4845c011a23741c395ec408f69963df` |
| 9 | References 15–17 and final footer | All three entries are complete and legible. The remaining whitespace is the natural end of the reference list; there is no detached continuation or missing text. | `ae97341b8b28ffffb73239ee099ca5c12d1e66b2c0e544e568590b5521167174` |

**Visual disposition:** no consequential typography, equation, flow, citation-layout or footer defect found on pages 6–9. Main pages 1–5, supplementary pages and figure files have separate inspection owners. This proof inspection is not bibliographic full-text verification or primary-data replication.
