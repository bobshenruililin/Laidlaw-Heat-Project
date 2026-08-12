# Laidlaw Stage 3 workspace

Summer 2026 deliverables (HKU Laidlaw):

| Deliverable | Status in repo |
|---|---|
| Research essay (accessible / academic; around 3,000 words) | **Submission copy:** [`laidlaw_research_report_2026.md`](laidlaw_research_report_2026.md) · [`Laidlaw_Research_Report_2026.pdf`](Laidlaw_Research_Report_2026.pdf) · [`../../outputs/Laidlaw_Stage3_Research_Report_Shen.pdf`](../../outputs/Laidlaw_Stage3_Research_Report_Shen.pdf). Main text ≈3,200 words; current CHD/HF results, three figures, references, and appendices. |
| Pathway × literature map (multimedia) | [`pathway_literature_map.md`](pathway_literature_map.md) |
| A0 portrait poster 841×1189 mm | Built: [`../poster/Laidlaw_Stage3_A0_portrait.pdf`](../poster/Laidlaw_Stage3_A0_portrait.pdf) · [TeX](../poster/Laidlaw_Stage3_A0_portrait.tex) · submission copy [`../../outputs/Laidlaw_Stage3_Poster_Shen.pdf`](../../outputs/Laidlaw_Stage3_Poster_Shen.pdf) (GEST landscape kept as legacy only) |
| HKU report form + supervisor endorsement | **Pending.** Complete the official HKU template, then send the essay + form to Prof. Bishai for endorsement and comments before submission to `laidlaw@hku.hk`. The template itself is not yet available inside this repository. |
| Spreadsheet columns Q, R | Bob |

Submission sequence and scientific checks:
[`submission_checklist.md`](submission_checklist.md).
Routing index (which file to edit, which is locked):
[`ARTEFACT_MAP.md`](ARTEFACT_MAP.md).

**Scientific roles:** Hogan (weather exposures), Zhenyuan Liu (Hospital Authority outcomes), and David Makram Bishai (supervision).

## Build the submission-facing report

Run from the repository root:

```bash
pandoc reports/laidlaw_stage3/laidlaw_research_report_2026.md \
  --citeproc --pdf-engine=xelatex --resource-path="$PWD" \
  -o reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf
cp reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf \
  outputs/Laidlaw_Stage3_Research_Report_Shen.pdf
```

## Superseded source document

The July literature-and-methods essay
([`essay_lit_methods.md`](essay_lit_methods.md) /
[`Essay_Lit_Methods.pdf`](Essay_Lit_Methods.pdf)) remains a writing and
literature source. It is **not** the 2026 submission copy: it was framed around
planned stroke research before the governed CHD/HF aggregates arrived.

The current submission report and poster make no stroke claim. Stroke should
be added only if governed aggregates are later delivered and analysed.
