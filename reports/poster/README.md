# Posters

## Laidlaw Stage 3 submission (current)

```bash
cd reports/poster
pdflatex -interaction=nonstopmode Laidlaw_Stage3_A0_portrait.tex
```

- Primary TeX: `Laidlaw_Stage3_A0_portrait.tex`
- Output: `Laidlaw_Stage3_A0_portrait.pdf` (ISO **A0 portrait**, 841 × 1189 mm, single page)
- Submission copy: `outputs/Laidlaw_Stage3_Poster_Shen.pdf`

### Layout

Full-width header (title, author, exploratory-panel badges), then two equal
portrait column shells filling the page, then a collaborator/provenance footer.
Left column: motivation and scope boundaries; data/cohort/estimand; three
figures (annual extremes, monthly extremes, seasonal pattern); literature map.
Right column: 12-contrast methods panel; key exploratory results with the two
validated signals; 12-contrast core table; forest plot; SE-method ladder;
M|D feasibility note (negative methods result); limitations; pointers; take-home.

### Content sources and provenance

- REAL HKO extremes (`figures/exposure_aging/fig01`, `fig02`) — environmental descriptors only
- `HA_APPROVED_AGGREGATE` seasonal pattern + panel results (`outputs/release_chd_hf/figures/figure2`, `figure3`, `figure5`)
- Validated numbers only from `reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md`
- Gate 3 is OPEN: every health association on the poster is labelled exploratory;
  no confirmatory headline; no stroke; no principal-diagnosis AMI.

## GEST-2026 poster (legacy — landscape, not the Stage 3 submission)

`GEST2026_poster.tex` / `GEST2026_poster.pdf` (ISO A0 **landscape**, 1189 × 841 mm).
Kept for the GEST-2026 record; wrong orientation for the Laidlaw Stage 3 call —
do not submit it as the Stage 3 poster. Its submission copy was
`outputs/GEST-2026_Poster_Shen.pdf`.

```bash
cd reports/poster
pdflatex -interaction=nonstopmode GEST2026_poster.tex
```

## Author

Shen Ruililin* — BASc (Global Health and Development), School of Public Health, The University of Hong Kong
