# Independent editorial review of the frozen manuscript

**Date:** 2 October 2026. **Role:** independent editorial reviewer, not manuscript author or figure producer. **Evidence authority:** `MANUSCRIPT_FREEZE.md`, PR #103 at `7060606fbe44b14b6b2893929781ac477cea1d46`. This review concerns presentation of the frozen evidence, not a new scientific analysis or submission approval.

## Revision examined

- Final `manuscript/covid_period/Manuscript_covid_period_draft.md`: SHA-256 `de0d9dac038b5449b7dc7bf12feb71f60ce23b4f852d8fbd6847f44c6716a045`.
- Final `manuscript/covid_period/Supplement_covid_period.md`: SHA-256 `9a8f7f90ac3150418a060a86637e3c173402c7a6d9bfdacd28d37802efcdf926`.
- Initial review examined manuscript `420ddf1bdc0b14b3b57eed5fdfa3452e3e59853a2d87c9e72f006846627d7366` and supplement `8c5b793570a346f9f49f6bcf3f5b22e1db05eae08fe8524d4bb2ea271152e15d`; the findings below record that repair history.
- Governing style: `.cursor/skills/cns-writing/SKILL.md` and `analysis_plan/writing_standards_hogan.md`.

## Findings requiring editorial repair

| ID | Finding | Consequence | Bounded fix |
|:--|:--|:--|:--|
| E1 | References are numbered by the previous draft's ordering rather than first appearance. The current first-citation sequence is 1, 2, 15, 16, 17, 7, 8, 9, 10, 11, 12, 13, 14, 3, 4, 5, 6. | The numbering is internally traceable, but it does not meet the usual sequential convention of a numbered-reference research article. | Renumber all in-text citations and the reference list consistently by first appearance. Preserve every source and its scientific use. |
| E2 | Figure 2's caption calls Supplementary Table S3 entries “Exact estimates, p-values and q-values”; that table rounds them to three decimal places. | “Exact” overstates the precision supplied in the cited table. | Use “Reported estimates, p-values and q-values”, or locate full precision explicitly in the released source CSV. Do not alter any scientific values. |
| E3 | Main captions use CHD/HF without expanding the acronyms; Figures 2–3 refer to the “full window” without naming its dates. | A figure taken separately from the manuscript is less self-contained than the user's acceptance criterion requires. | Expand coronary heart disease (CHD) and heart failure (HF) in each main caption; identify the full window as January 2013–December 2023. No change to the displays or evidence is needed. |

All three findings were resolved through editorial changes, without changing the frozen evidence. The repaired source was independently checked:

- **E1 resolved:** first-citation order is now 1–17. Removing only the entry numbers, the set of all seventeen bibliographic strings is identical to the frozen starting manuscript. No source was added or removed.
- **E2 resolved:** Figure 2 now says “Reported estimates, p-values and q-values” and separately locates full-precision values in the source CSV.
- **E3 resolved:** all three main captions expand the outcome acronyms and identify 2013–2023; Figures 2–3 specify January 2013–December 2023. Supplementary captions also expand their outcome acronyms and identify relevant windows. Figure 2's axis now displays the degree sign in 1°C. These repairs are present in the reviewed proofs.
- Final source hashes are recorded above. The intermediate revision after E1–E2, before E3, was manuscript `0a3fd7b73bde43fd76c4d9b86c1c4ac056cde4045095e20e1edc8e1430b6961d` with the original supplement hash.

**Final disposition:** no material unresolved editorial claim, organisation, caption or inspected-proof defect remains in this revision. Separate numerical, clinical and human-governance checks retain their own authority; editorial completion is not submission approval.

## Hostile assessment

**Contribution and novelty.** The manuscript claims a descriptive trajectory within a pre-existing decline. It does not present a physiological improvement, a causal pandemic effect or a new explanation of cardiovascular disease. Closest studies are named early rather than hidden. The data offer limited explanatory novelty; improved prose cannot remove this scientific limit. A leading selective venue is not warranted merely by the three-figure presentation.

**Organisation.** The main headings follow Abstract → Introduction → Results → Discussion → Methods → availability → References. Results lead with the annual burden, then distinguish the complete weather family from selected diagnostic examples. Discussion returns to the meaning of recorded counts, uses discordant clinical literature to limit interpretation and leaves competing explanations open. No future-study programme or internal gate language intrudes into the scientific body.

**Endpoint wording.** The title says hospitalisations *after* diagnosis. The abstract and Methods identify the supplied construction and absence of admission cause and eligible person-time. The paper does not promote these stays to validated cause-coded events or incidence. “CHD-associated” and “HF-associated” are acceptable only with the supplied definition attached; they must not become “CHD/HF admissions” in a shortened title, graphical abstract or press-facing summary.

**Figure necessity.** Figure 1 supplies the contribution directly and retains separate zero-origin scales. Figure 2 preserves the complete twelve-model family, rather than selected nominal findings. Figure 3 explains why the historically discussed associations do not bear a stable mechanistic interpretation. Its selection is explicitly diagnostic. Supplementary Figure S1 clarifies observation processes without inventing a cohort flow; S2 displays dependent, overlapping-window fits without treating them as a direct period contrast. Main figures 2–3 have a bounded critical role and must not be promoted above the recorded-count result.

**Null and inconvenient evidence.** The lag-six adjusted family has no q-value below 0.19; the near-null HF minimum-temperature interval is explicitly treated using its unrounded upper bound. Calendar and uncertainty disagreements remain visible. Clinical literature includes adverse, inconclusive and selection-sensitive findings. The paper does not dismiss this evidence to manufacture coherence.

**Repetition and register.** Some key endpoint and inferential limits recur in the abstract, Results, Discussion, Methods and self-contained captions. Each occurrence serves a different reading context; deleting them indiscriminately would weaken protection against a predictable misreading. The protected HKO paragraph retains its mandated wording and is followed immediately by the clarification of aggregation. There is no material stylistic overstatement or unsupported novelty adjective. Minor tightening could occur during journal-specific copyediting without changing scientific claims.

**Cross-references.** The draft contains three main figures, two supplementary figures and seven numbered supplementary tables. Annual counts, complete weather estimates, nested windows, calendar alternatives, interval constructions and diagnostics are assigned to S1–S7 respectively. All cited objects are present. The selected model-criticism figure does not imply that its examples exhaust the released sensitivity results.

## Boundaries of this review

This is an editorial review with source, caption and rendered-proof inspection. The reviewer inspected the main and supplementary pages across the repair pass and rechecked affected main figure pages 2–4 and supplementary pages 2–5 after the caption and table-width repairs. Labels and intervals are readable, the captions remain with their displays, the native model equation is legible and the fixed supplementary header reads “Outcome” without a mid-word split. No clipping or misleading graphic emphasis was identified in those proofs. The author separately completed all-page and all-vector-figure visual inspection.

Final proof bindings:

- `manuscript/covid_period/Heat_CVD_Manuscript_covid_period.pdf`: 9 pages; SHA-256 `09bad10b6da1d32a4ea8e7fb40b31b177329f5742452302c599b622bd8bbc0ff`.
- `manuscript/covid_period/Supplement_covid_period.pdf`: 5 pages; SHA-256 `56bd147cabf5a3a25a6ec3b2f4e0790948395cf3d46d2ae95b477f07297b3924`.

Numerical transcription and clinical-source verification are assigned to the independent statistical and clinical reviewers. No primary health data were accessed, no model was refitted and no calibration or external validation was performed. Ethics, authorship, extraction-query validation, dissemination and submission facts require human confirmation separately. Unknown admission cause and eligible person-time remain scientific limits, not defects that an editorial revision can remove.
