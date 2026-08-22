# Posters

## Laidlaw Stage 3 submission (current)

```bash
cd reports/poster
pdflatex -interaction=nonstopmode Laidlaw_Stage3_A0_portrait.tex
```

- Primary TeX: `Laidlaw_Stage3_A0_portrait.tex`
- Output: `Laidlaw_Stage3_A0_portrait.pdf` (ISO **A0 portrait**, 841 × 1189 mm, single page)
- Submission copy: `outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf` (also copied as `ShenRuililin_Laidlaw_Stage3Poster.pdf` in this folder)

22 August 2026: the self-referential footer was deleted on Bob’s instruction. `\vfill` is retained so the bands do not shift. The only remaining footer line is `shenrll@connect.hku.hk`. Do not restore the “machine-validated” metadata block.

### Layout (readability redesign v2, Aug 2026)

Ground-up redesign after the dense two-column/15-box draft was rejected as
unreadable at 1–2 m; v2 moves to a **band architecture** so the sheet is filled
(~91% of usable height) without stretching whitespace mechanically:

1. Full-width header band (title, subtitle, author/affiliation).
2. Compact top band: INTRODUCTION + annual-extremes context figure (left,
   40%) | OBJECTIVE + METHODS with a horizontal data-flow chain (right, 58%).
3. Dominant full-width RESULTS band (~55% of content area): lead line, two
   key-number callout boxes, panel bullets, then the 12-contrast forest drawn
   as two side-by-side outcome panels (CHD | HF) with the focused
   SE-uncertainty plot beside it.
4. Bottom band: INTERPRETATION / LIMITATIONS | CONCLUSION (+ next-data note).
5. Footer bottom-anchored with `\vfill`; band gutters are fixed (14/30/30 mm)
   so spacing is deliberate, not stretched.

Type scale (actual printed sizes): title 74 pt, subtitle/author 30 pt, section
headings 34 pt (uppercase), results sub-heading 26 pt, body 26 pt, callout
numbers 50 pt, figure labels ≈21–25 pt, captions 18.5 pt, definitions note
20 pt Ink, footer 17.5 pt. Roughly 650 poster words excluding labels, captions
and footer (≈575 excluding the two small notes).

Palette: deep ink/navy + teal on white; warm accent (#B84A2E) for heat, cool
blue (#2F6C9C) for cold. Typographic identity only — no logo assets exist, so
none are faked.

### Figures (poster-specific, reproducible)

```bash
Rscript scripts/46_build_laidlaw_poster_figures.R
```

Draws three figures into `reports/poster/figures/`, sized for the band layout
so labels print at ≈21–25 pt:

- `fig_poster_weather.*` (12.5 × 7.0 in) — annual HKO hot nights vs cold days,
  2013–2023; prints ~317 mm wide in the top band
  (source: `outputs/tables/exposure_aging/annual_extremes_and_spell_burden.csv`)
- `fig_poster_forest12.*` (18 × 11.6 in) — the 12 core count ratios (NW6) as two
  side-by-side outcome panels with an estimate column each; prints ~496 mm wide
  (source: `outputs/release_chd_hf/tables/table2_core_models.csv`)
- `fig_poster_uncertainty.*` (10 × 10.8 in) — the two leading contrasts × 4 SE
  methods; prints ~274 mm wide beside the forest. The CHD hot-night NW3 row is
  shown at 4 decimals — 1.022 (1.0003–1.0439) — because at 3 dp it rounds to
  1.000 and the narrow exclusion of 1 would be invisible
  (source: `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`)

### Content rules honoured

Validated numbers only (CHD series × hot nights 1.022 [1.002–1.042], p = 0.032,
q = 0.192; HF series × cold days 1.073 [1.006–1.144], p = 0.031, q = 0.192; all
12 q > 0.19; 132 months; 156,156 CHD / 29,681 HF events). Wording follows the
validated manuscript: the panel was **specified after the outcome series was
available** (no "pre-specified" claim); outcomes are **first hospitalisation
after a first recorded CHD/HF diagnosis** (inpatient-labelled aggregate columns;
admission cause not recorded; event semantics pending data-provider
confirmation); outcomes wording uses "CHD series / HF series", never
cause-specific admissions. Exploratory framing throughout; no Gate 3 language,
no provenance strings, no file paths, no stroke content, no
principal-diagnosis claim, no raw monthly counts; "governed" replaced with
"privacy-protected ... monthly aggregate counts". Technical detail is
compressed into captions/notes and the footer.

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
