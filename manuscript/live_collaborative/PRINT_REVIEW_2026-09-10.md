# Print review — 10 September analysis-window package

## Files

| Object | Pages | Bytes | SHA-256 prefix |
|:--|--:|--:|:--|
| `Heat_CVD_Manuscript_20260910_hogan.docx` | — | 789,283 | `73973d670d5e1730` |
| `Heat_CVD_Manuscript_20260910_hogan.pdf` | 21 | 844,336 | `4f19c70f456ae8c9` |
| `Heat_CVD_Supplement_20260910_hogan.docx` | — | 1,215,672 | `24563b5b04d11b62` |
| `Heat_CVD_Supplement_20260910_hogan.pdf` | 18 | 1,205,575 | `992e1ac0b1069bda` |

Builder: `scripts/77_hogan_20260910_live_docx.py`.

## Main PDF page map

| Object | Page |
|:--|--:|
| Table 1 | 7 |
| Figure 1 | 8 |
| Figure 2 | 10 |
| Table 2 | 13 |
| Figure 3 | 14 |
| Table 3 | 16 |
| References | 20–21 |

Each main table and figure occupies a separate page. Table headers repeat in
Word. No table, caption, or figure is clipped. The page contract is A4, 2.54 cm
margins, Times New Roman, single spacing, and the running header with a page
field.

The Word file contains three tables, three images, and nine comments. Comments
cover authorship, nested-window interpretation, IRB, outcome semantics, Hogan
weather wording, Model 2/3 status, laboratory scope, and Table 2. They contain
no paste, circulation, shared-file, pipeline, Gate, core-panel, or R-script
instruction.

## Supplement

The 18-page supplement contains Supplementary Figures S1–S4 and S6, Tables
S1–S10, and Supplementary Note S1. Figure S5 is unassigned so the established
continuous-temperature display retains S6. Table S9 (archive pollution
models) is on page 15; Table S10 (period weather summaries) is on page 16;
Note S1 is on page 17.
Archive influenza and pollution estimates remain labelled as non-core.
Daily-recovery calibration remains `SYNTHETIC_CALIBRATION`, not a health
finding.

## Checks

- Live claim-ledger audit: 206 checks passed.
- Current package + archived thermal contract: 37 tests passed.
- Full repository: 200 passed; five pre-existing Stage 3/form-2a tests remain
  red. The pre-change commit reproduces the same five failures (193 passed)
  after excluding its collection-broken historical Opus harness.
- Manual browser review: title/Abstract, Hogan weather, Tables 2–3, Figures
  1 and 3, references, Supplementary Tables S9–S10, and Note S1 were legible.
  No clipping, overlap, blank page, or broken character was observed.
- Table 3 text extraction and rendered-page review confirm the third row is
  “HF mean minimum temperature / 1 °C.”

## Locked limits

Hogan’s weather paragraph is verbatim. The scientific body contains no Gate
jargon. Author 2–4 and `UW XX-XXX` remain human-owned. The package has not been
sent or pasted by an agent. Stage 3 files were not rebuilt.
