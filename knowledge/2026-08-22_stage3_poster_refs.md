# Stage 3 poster — compact REFERENCES strip (22 August 2026)

Bob asked for a reference section on the A0 poster, at the bottom, using spare
space. Fable locked the citation set and signed off the render (GO).

## Lock

| File | Bytes | SHA-256 |
|---|---:|---|
| `outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf` | 94,196 | `82c077d69c414d18f412ef4334793e67d7f7153c7709242833067ee2f9e861a5` |

Identical copies: `reports/poster/ShenRuililin_Laidlaw_Stage3Poster.pdf`,
`reports/poster/Laidlaw_Stage3_A0_portrait.pdf`, and the legacy name
`outputs/Laidlaw_Stage3_Poster_Shen.pdf`.

`pdfinfo`: 1 page, 2383.94 × 3370.39 pts (ISO A0). Source:
`reports/poster/Laidlaw_Stage3_A0_portrait.tex`.

The essay is unchanged (`8b71157e5178b589`).

## What changed

- Six numbered Vancouver-style entries in a full-width mist strip under
  Interpretation / Conclusion: HKO yearbooks (2013 and 2021 combined);
  Goggins 2013; Goggins 2017 HF; Liu 2020 (Jasmine, mortality);
  Liu 2026 (Roro, medRxiv preprint `10.64898/2026.03.05.26347683`);
  Greenland & Morgenstern 1989.
- Four in-text superscripts only: intro 10→61 hot nights `[1]`; hospital
  burden `[2,3]` vs mortality burden `[4,5]`; HKO definitions `[1]`;
  no causal / principal-diagnosis claim `[6]`. No citations in Results,
  callouts, captions, or the conclusion box.
- Spare gutters reclaimed (header / after top / after results now 10 mm).
  The previous `\vfill` before the email was sending the strip to page 2;
  the strip now follows the bottom band directly. Contact email only;
  the deleted “machine-validated” footer stays gone.

## Honesty (Fable)

Complementary literature only. Goggins 2013 is not treated as AMI = our CHD
series. Liu 2020 / 2026 are mortality / excess-death papers, not validation of
the hospitalisation estimates. All 12 *q* > 0.19; exploratory framing intact.
Gate 3 still open.

## Rebuild

```bash
cd reports/poster
pdflatex -interaction=nonstopmode Laidlaw_Stage3_A0_portrait.tex
cp Laidlaw_Stage3_A0_portrait.pdf ShenRuililin_Laidlaw_Stage3Poster.pdf
cp Laidlaw_Stage3_A0_portrait.pdf ../../outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf
```
