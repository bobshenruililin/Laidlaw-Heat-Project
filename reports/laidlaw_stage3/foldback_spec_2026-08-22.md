# LOCKED IMPLEMENTATION SPEC — Stage 3 fold-back (22 August 2026, pre-Email-A)

> **Round 2 verdict (Fable, 22 Aug 2026 evening): GO.** All four fold-back items verified in source and renders; honesty checks pass (pre-2020 shown on both callouts with includes/excludes-1 labels; unequal visual weight now favours the more coherent HF signal; Goggins 2013 cited as AMI evidence, never equated with the present CHD outcome). Accepted merged deviations from Round 1: "How to read the estimates" gloss in Methods rather than Results; "Implications and next study" as a subsection inside Discussion (word count 2,575, within band); unequal callout widths. Non-blocking nits logged in the review reply only. Implementer completes GO item 10 (SHA lock note + pointer updates).

**Mode:** Decide → Ship. Roundtable verdict implemented as edits to the FINAL report and CURRENT poster.
Gate 3 open. No refits. No new numbers. Live manuscript not attached, not edited.
Baseline artefacts: report PDF SHA `8b71157e5178b589`, poster PDF SHA `82c077d69c414d18`.
Superseded draft (source of numbered-limitations wording only): `origin/cursor/auto-research-lab-b75b:reports/laidlaw_stage3/laidlaw_research_report_2026.md`. Do not restore its "most elevated", "continuity" jargon, TOC, or Implications heading.

---

## 1. REPORT — `reports/laidlaw_stage3/laidlaw_research_report_2026.md`

### YAML / front matter

- No changes. Keep `toc: false` (decision: **no TOC**. A 9–10-page unnumbered-section essay inside a 3,000-word ceiling gains nothing from a contents page; there is no Laidlaw formatting requirement for one). Keep `author: "Shen Ruililin"`.
- Change `fig-pos: htbp` → `fig-pos: H` (float fix, see below).

### Introduction

- **DELETE** paragraph 2 in full ("This Laidlaw Scholars project was supervised by Professor David Makram Bishai … complementary modelled heatwave-mortality work [@liu2026roro]."). Frees 119 counted words. `@liu2026roro` remains cited in Introduction paragraph 4 and Discussion, so References are unchanged.
- No other Introduction edits.

### Methods → Health data

- **INSERT** after "Admission cause was not recorded." (before "Age–sex strata were not included."):

  > Delivered columns are labelled inpatient; the final event semantics require confirmation from the data provider.

  This restores the caveat already on the poster Methods and closes fold-back item 4.

### Results → Core panel

- **INSERT** the single accessibility gloss as a new paragraph after the sentence ending "…(1.006–1.144; *p* = 0.031)." and before "After correction, both had *q* = 0.192…":

  > In plain terms, these ratios correspond to about 2.2% more CHD first hospitalisations in a month with five additional hot nights, and about 7.3% more HF first hospitalisations in a month with five additional cold days. Both statements describe modelled monthly counts, not any individual's risk.

  Exactly one gloss. The `[^cr]` and `[^q]` footnotes already gloss count ratio and *q*; do not add more.

### Results → Uncertainty and robustness

- No changes. Keep unrounded NW3 1.0003–1.0439, ACF 0.508, pre-2020 1.011 (0.991–1.032) and 1.113 (1.053–1.176), "narrower than the model-based interval … reason for caution".

### Discussion

- **Implications: keep inside Discussion** (paragraph 4 already carries the next-study content). Do not restore the draft's "Implications and next study" heading — it invites re-expansion past the ceiling and adds nothing at this length.
- Keep the "**Strengths.**" run-in unchanged.
- **REPLACE** the "**Limitations.**" run-in paragraph (110 words) with a lead line plus numbered list — the draft's seven items updated to final wording, plus the two honesty items the draft missed (pre-2020 CHD; NW narrower than model), with the draft's serial-dependence/multiplicity item split to hold them cleanly:

  > **Limitations.** Nine limitations determine how these results should be read:
  >
  > 1. **Outcome meaning.** Admission cause was not recorded, and event semantics await data-provider confirmation (Methods); an event is a first hospitalisation after a first CHD or HF diagnosis, not a demonstrated cardiac-caused admission.
  > 2. **Ecological resolution.** Each observation describes Hong Kong for one month; individual exposure and within-month timing are unknown [@greenland1989ecological].
  > 3. **Denominator.** Monthly counts of cohort members still at risk of a first event were unavailable, so the estimates are count ratios rather than incidence-rate ratios.
  > 4. **Confounding.** Adjustment for pollution, humidity and influenza is unresolved in the core panel.
  > 5. **Exposure measurement.** Headquarters weather is a territory-level proxy for neighbourhood, indoor and personal exposure.
  > 6. **Serial dependence.** CHD residual autocorrelation remained material (0.508 at lag 1), and the Newey–West intervals were narrower than the model-based interval, so their exclusion of 1 is a reason for caution rather than confirmation.
  > 7. **Multiplicity.** No comparison survived Benjamini–Hochberg correction across the twelve contrasts; every *q*-value exceeded 0.19.
  > 8. **Period and season structure.** The CHD hot-night estimate is compatible with 1 before 2020 (1.011, 0.991–1.032), whereas the HF cold-day estimate is stronger before 2020 (1.113, 1.053–1.176); official cold days are concentrated in December–February (141 of 145), so the HF contrast is identified between winters.
  > 9. **Available outcomes.** Age, sex and disease-subtype strata were not delivered; a stroke series was not delivered, and no stroke result is reported.

### Conclusion

- No changes. It already reads "more closely associated … than the other thermal measures" — "most elevated" stays dead.

### Acknowledgements

- **REPLACE** paragraph 1 with the merged supervisor paragraph (Introduction content folded in; no citation bracket in Acknowledgements — the medRxiv work is cited in the body):

  > I am especially grateful to Professor David Makram Bishai, who supervised this Laidlaw Scholars project. He set its scientific direction: a complete comparison of heat and cold encodings in one Hong Kong panel rather than a search for a single confirmatory association, with every comparison reported, uncertainty shown under more than one standard-error method, and the limits of monthly aggregates stated in the same document as the estimates. He advised on population-health interpretation of monthly counts and guided what may honestly be reported from governed Hospital Authority aggregates. The study sits within a School of Public Health programme he leads on temperature and health in Hong Kong, which also includes complementary modelled heatwave-mortality work. This report is submitted for the Laidlaw Stage 3 requirement under his supervision. Journal writing continues separately with the weather and health-data co-investigators. Remaining errors are mine.

- Keep paragraph 2 (Hogan, Zhenyuan Liu, Dr Jingjing Zhou, dissemination sentence) unchanged.

### Appendix

- Content unchanged. Formatting only (below).

### Figure/table float fixes (LaTeX)

1. `report_preamble.tex`: add `\usepackage{float}` and force in-place figures regardless of template defaults:
   `\makeatletter\renewcommand\fps@figure{H}\makeatother`
   With `[H]`, Figure 1 sits with the Table 1/Results text and Figure 2 can no longer break Table 2's longtable across pages (caption p4 / body p6 disappears).
2. Markdown: insert a raw `\newpage` line immediately before `# Appendix`, so Table A1 starts atop a fresh page and cannot split. Pandoc passes raw LaTeX to the PDF and drops it in the docx pathway.
3. Table A1 cell wrap: replace the ordinary space between each point estimate and its opening parenthesis with a non-breaking space (U+00A0) in all eight data cells (e.g. `1.022 (1.0003–1.0439)`), so a CI can never wrap under the wrong column. Fallback only if a wrap survives rebuild: wrap the A1 table in raw `\begingroup\footnotesize` … `\endgroup` lines.

### Word-count target

- Ledger: 2,670 (pdftotext, Introduction–Conclusion) − 119 (Bishai paragraph out) + ≈50 (gloss) + ≈20 (Methods caveat) + ≈100 (numbered limitations net of deleted run-in) ≈ **2,720**.
- Target band **2,700–2,750**; hard bounds 2,000–3,000. Abstract, Acknowledgements, Appendix and References stay outside the count. If over 3,000 after build, trim Discussion paragraph 4 — never the limitations, gloss, or caveat.
- Rebuild with `bash reports/laidlaw_stage3/build_stage3_report.sh` (XeLaTeX PDF official; docx Word-only).

---

## 2. POSTER — `reports/poster/Laidlaw_Stage3_A0_portrait.tex`

### Author line (header)

- `\textbf{Bob Shen Ruililin}` → `\textbf{Shen Ruililin}`. Matches the report. Everything else in the header stays.

### Results lead sentence

- Replace "…specified after the outcome series was available --- two contrasts stand out."
  with "…specified after the outcome series was available --- two contrasts stand out, with unequal robustness."

### Callouts (pre-2020 fold-in; the honesty fix for equal visual weight)

Keep 1.022 and 1.073 as the 50 pt NW6 headline numerals. Inside each callout's right minipage, after the CI line, add one Slate line at 19/24:

- CHD (HeatTint):
  `\vspace{1.5mm}`
  `{\fontsize{19}{24}\selectfont\color{Slate}2013--2019 only: 1.011 (0.991--1.032) --- includes 1\par}`
- HF (ColdTint):
  `\vspace{1.5mm}`
  `{\fontsize{19}{24}\selectfont\color{Slate}2013--2019 only: 1.113 (1.053--1.176) --- excludes 1\par}`

Both callouts grow identically (~8 mm); the asymmetry is carried by the words, not by unequal boxes.

### Results bullets

- CHD bullet tail: "--- but the interval \emph{includes 1} under two of four standard-error methods and before 2020, so the signal is uncertainty- and period-sensitive."
- HF bullet tail: "--- the interval excludes 1 under all four methods, and the association is stronger before 2020."
- Third bullet (all q > 0.19) unchanged.

### Interpretation bullet 2

- Replace with: "The CHD hot-night estimate is \textbf{sensitive to how uncertainty is computed} and is not evident before 2020; the HF cold-day estimate is stable across methods and stronger before 2020."
  (Left column is shorter than the Conclusion column; this wraps without raising the band.)

### Footer (exact, one line, human English)

Replace the email-only line with:

```
{\fontsize{17.5}{22}\selectfont\color{Slate}Collaborators: Hogan (weather definitions)~\textperiodcentered~ Zhenyuan Liu (Hospital Authority aggregates)~\textperiodcentered~ Supervisor: Prof.~David Bishai\hfill shenrll@connect.hku.hk\par}
```

Update the comment above it to: `% Footer: human credits + contact. Do not restore the machine-validated metadata block.`
Banned from the footer (robotic): "Reproducible, machine-validated analysis and release package"; "Outcomes: privacy-protected Hospital Authority monthly aggregate counts"; "Laidlaw Stage 3 Research Poster · ISO A0 portrait"; "Weather: Hong Kong Observatory daily records (public)". (The privacy-protected phrase stays where it belongs, in the Methods bullet.)

### What NOT to shrink or change

- The six-item REFERENCES strip: all entries, sizes, and its position after the bottom band. Reviewers have not seen it; it stays.
- The 50 pt callout numerals 1.022 / 1.073 (NW6) and their CI/p/q lines.
- The forest and ladder figures and captions, including unrounded NW3 1.0003–1.0439.
- Methods bullets, including the inpatient/"require data-provider confirmation" caveat and the event counts 156,156 / 29,681.
- The Objective box, title, subtitle, Definitions block, Conclusion takeaway box.

### Space plan (must remain exactly 1 page, 2383.94 × 3370.39 pt)

- Growth: callouts +≈8 mm; results bullets +≈11 mm worst case; interpretation bullet +0 (absorbed by taller right column); footer +0 (one line replaces one line).
- Recovery, applied in order until the page closes: (a) `\vspace{10mm}` after header → `7mm`; (b) `\vspace{10mm}` after top band → `7mm`; (c) `\vspace{10mm}` after results band → `7mm`; (d) `\vspace{5mm}` before callouts → `4mm` and the two `\vspace{4mm}` around the results bullets → `3mm`; (e) last resort: drop "and the association is stronger before 2020" from the HF bullet (the callout already carries the number).
- Geometry unchanged. **No `\vfill` before the refs strip** (it ships the strip to page 2). Build with `pdflatex -interaction=nonstopmode` twice; verify `pdfinfo`: Pages 1, size 2383.94 × 3370.39 pts.

---

## 3. DO NOT TOUCH

- **Live manuscript**: Hogan's shared file, `manuscript/live_collaborative/`, `Heat_CVD_Manuscript_20260815_collab_draft.docx`. Not attached to Email A, not edited, not quoted into the essay.
- **Form 2a** (`2a. Laidlaw - Report Form (HKU).docx`): Bob's own fields only; supervisor fields blank; never committed.
- **Hogan's weather paragraph**: lives in the live file, not this essay; do not import or paraphrase it into the report or poster.
- **All coefficients and counts**: Table 2, Table A1, 1.022/1.073, 1.0003–1.0439, 0.508, 1.011 (0.991–1.032), 1.113 (1.053–1.176), 141/145, 29/132, 156,156/29,681. No refits, no re-rounding, no new numbers, no synthetic values.
- **Abstract**: unchanged (pre-2020 asymmetry already stated there).
- **Citations**: Guo "no association for the official hot-night flag" sentence; Goggins 2017 HF-cold framing; Roro cite stays medRxiv `10.64898/2026.03.05.26347683`; Liu 2020/2026 never cited as validating hospitalisation estimates; `references.bib`, `vancouver.csl`.
- **Status**: Gate 3 open — no headline freeze, no "primary result" language anywhere. No stroke, no AMI/principal-diagnosis claims.
- **Build pipeline order** in `build_stage3_report.sh` (reference-docx → docx → table fix → XeLaTeX PDF → copies).

---

## 4. GO CRITERIA FOR ROUND 2

Report (all must pass):

1. `bash reports/laidlaw_stage3/build_stage3_report.sh` exits 0; PDF and docx regenerate.
2. Layout: Figure 1 in place with its text (no near-empty float page); Table 2 caption and all twelve rows on one page; Table A1 whole on one page, no CI wrapped under a wrong column.
3. Word count: Introduction–Conclusion within 2,000–3,000 by the packet's pdftotext method (target ≈2,700–2,750).
4. Present: "require confirmation from the data provider" (Methods); "In plain terms" gloss (once); numbered Limitations 1–9; merged supervisor paragraph in Acknowledgements.
5. Absent: supervisor paragraph in Introduction; "most elevated"; "continuity"; "machine-validated"; "Bob Shen"; any TOC.
6. Numbers diff against the locked `8b71157e` PDF: every numeral identical; only text moved or added.

Poster (all must pass):

7. `pdflatex` ×2 exits 0; `pdfinfo`: Pages 1, size 2383.94 × 3370.39 pts; refs strip with all six entries on page 1.
8. Header author "Shen Ruililin"; footer contains Hogan, Zhenyuan Liu, Prof. David Bishai, and the email; none of the four banned footer phrases; no `\vfill` before the refs strip.
9. "2013--2019 only" lines appear exactly once per callout with digits 1.011 (0.991--1.032) and 1.113 (1.053--1.176); results lead says "with unequal robustness".

Packet:

10. New SHA-256 for both PDFs recorded in a dated knowledge lock note; `WHAT_TO_ATTACH.md` and `CONTEXT_BOOTSTRAP.md` item 6 updated to the new SHAs; Fable prose/citation pass and Sol layout pass both GO; Gate 3 still open; Email A attaches only the report PDF + form 2a (+ optional poster).
