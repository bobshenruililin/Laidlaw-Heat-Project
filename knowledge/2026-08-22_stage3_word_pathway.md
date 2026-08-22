# Stage 3 Word-pathway rebuild — 22 August 2026 (evening, second pass)

**Mode:** Ship. Bob-authorised. Not a Gate 3 freeze. Not a substitution of Hogan’s live file.

Bob asked to acknowledge Professor Bishai more fully, fix Table 1 overflow, cut the report to 3,000 words, and consider the 15 August collab Word draft as a **format** pathway. The live collaborative manuscript is still not the Stage 3 attachment.

## Why the 15 August `.docx` read and formatted better

It was not because that file is the programme report. It is a paste source for Hogan’s live journal file (placeholder authors, Hogan weather paragraph, ~5,500 words). It looked better because of genre and layout:

- Structured **Abstract** (Background / Methods / Results / Conclusions) and unnumbered IMRD, not 1.1 teaching subsections
- Numbered citations
- Word-native tables with autofit and a short Table 1 (event definition as a note, not a fifth overflowing column)
- Affiliation / last-author block that names Professor Bishai
- Paragraph spacing rather than school-report numbering

Stage 3 now borrows that **register and table design**. It does not borrow Author 2–4, Hogan’s weather paragraph, or the live file’s length.

## What we did not do

LibreOffice PDF export of the pandoc `.docx` collapsed tables into a right-hand stack. Microsoft Word is the reader for the `.docx`. The **HKU PDF** is XeLaTeX from the same markdown, so Table 1 stays inside the text block.

Do not email `Heat_CVD_Manuscript_20260815_collab_draft.docx` to Bishai or to `laidlaw@hku.hk`.

## New lock

| File | Bytes | SHA-256 |
|---|---:|---|
| `outputs/ShenRuililin_Laidlaw_Stage3Report.pdf` | 405,448 | `8b71157e5178b589c01f1c8853bc44d00cd2c8319ebd6e91f893c1d9005462da` |
| `outputs/ShenRuililin_Laidlaw_Stage3Report.docx` | 355,772 | `56c09558f35ba1c76741e401bcdb52e9907be8388159647f4d5ef5841b35c5e2` |
| `outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf` | 92,186 | `b3f16ff27f76ea9b244d27919a8319c676326ba47c31a92344892e43701443ac` |

Poster bytes were unchanged at this pass. Later the same evening they gained a REFERENCES strip (`knowledge/2026-08-22_stage3_poster_refs.md`; SHA prefix `82c077d69c414d18`).

## Word count

Form 2a: **ca.** 2,000–3,000. Count used here:

- **Abstract excluded** (journal convention Bob requested)
- Footnotes and appendix excluded
- **Introduction through Conclusion ≈ 2,670 words** (markdown); ≈ 2,730 by `pdftotext`

That is inside the band. Do not pad.

## Bishai credit

- Title-page **Supervisor** line with full name and School of Public Health
- Introduction: scientific direction (complete heat-and-cold panel; four uncertainty methods; limits stated with the estimates; lab programme including complementary mortality work)
- Acknowledgements: first and longest paragraph

He is not listed as a co-author of the programme report. Journal authorship remains the live file.

## Honesty retained

Unrounded NW3 1.0003–1.0439; pre-2020 CHD 1.011 (0.991–1.032) and HF 1.113 (1.053–1.176); ACF 0.508; 141 of 145 cold days in December–February; 29 of 132 months; “more closely associated,” not “most elevated”; twelve models specified after outcomes were available; no stroke result.

Build: `reports/laidlaw_stage3/build_stage3_report.sh`.
