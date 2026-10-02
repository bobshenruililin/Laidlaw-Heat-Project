# Verification and inspection limits

Pinned main: `b103e96c6761f3409fab6f116c6675b43fdb2ee3`. No governed outcome panel was opened and no health model was fitted.

- Recomputed Benjamini–Hochberg arithmetic from all 12 released p-values: maximum q error 9.99e-16; minimum q 0.192239059852. This checks arithmetic, not p-value validity or identification.
- Matched all 12 baseline ratios and bounds against the sensitivity CSV: maximum absolute difference 0.
- Traced the six nested/full rows displayed in the memo and briefing directly to scenario/outcome/exposure keys.
- Checked annual endpoint/trough totals and sums: CHD 156,156; HF 29,681. Annual summaries are already public; no monthly series reconstructed.
- Reproduced script50 on the COVID ledger: one-check pass. Its `claims` loop does not inspect the `numerals` schema.
- Ran script79 with the pinned base and explicit private output: 232 checks pass; 1 failure: `page map could not be recomputed: No module named 'pymupdf'`. The page-map check is unverified in this environment; this is not a scientific failure or a fully green audit. No existing checker was modified.
- Read checker semantics: string/source/layout and preservation checks do not establish per-value numerical correctness, mechanisms or causal identification.
- 101 PR metadata records screened; 15 selected, with inspection depth recorded. Public issue comments are not a complete inventory of review threads/private exchanges.
- Primary-source inspection levels are recorded for seven citation/method sources. No borrowed effect estimates enter this project's results. Xin bibliographic mismatch is reported, not silently repaired.

The briefing is derived from the memo/register. Its editable chart uses released annual totals indexed to 2013=100; this is descriptive arithmetic, not a new model. Final presentation validation and visual inspection are recorded below after export.

## Briefing validation

- Exactly ten slides, three native editable tables, one native editable chart and ten source-note parts. Package integrity, geometry/font policy and first-party import passed. The chart cache and embedded workbook values/ranges passed structural comparison. Table arithmetic validator skipped ratio/CI strings; those values were checked directly against the public CSVs above.
- All ten initial slides inspected individually; visual QA also performed by a separate reviewer as required by the presentation skill. A long title and date/body spacing were repaired and re-rendered. The final chart axis was made explicit for consistent PDF/PPTX scale.
- PDF exported with the bundled office renderer: ten pages. Exported PDF and imported final PPTX renders were inspected. PowerPoint and Google Slides application editing were not tested; package checks establish native object structure, not all application behaviour.
- PPTX SHA-256: `a888bd42962f9ea5e301be806d65b17e0f81d7b06cdab6d8569a3b8ebca1019a`.
