# Laidlaw Stage 3 workspace

Summer 2026 deliverables (HKU Laidlaw):

| Deliverable | Status in repo |
|---|---|
| Research essay (accessible academic paper; **ca.** 2,000–3,000 words) | **Submission copy:** [`ShenRuililin_Laidlaw_Stage3Report.pdf`](ShenRuililin_Laidlaw_Stage3Report.pdf) · Word working copy [`ShenRuililin_Laidlaw_Stage3Report.docx`](ShenRuililin_Laidlaw_Stage3Report.docx) · source [`laidlaw_research_report_2026.md`](laidlaw_research_report_2026.md). Abstract excluded from the count; Introduction–Conclusion 2,575 words. SHA-256 prefix `c083d4096a0924b1`. Do not substitute the live manuscript or the 15 August collab draft. |
| Pathway × literature map (multimedia) | [`pathway_literature_map.md`](pathway_literature_map.md) |
| A0 portrait poster 841×1189 mm | [`../poster/ShenRuililin_Laidlaw_Stage3Poster.pdf`](../poster/ShenRuililin_Laidlaw_Stage3Poster.pdf) · [TeX](../poster/Laidlaw_Stage3_A0_portrait.tex) · [`../../outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf`](../../outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf). SHA-256 prefix `0ef58e0951bb2ffd`. Compact REFERENCES strip, pre-2020 callouts, human footer. GEST landscape is legacy only. |
| HKU report form + supervisor endorsement | **Human action this week.** Official form is Bob’s local copy. Current pack: [`../../analysis_plan/send_pack_2026-08-22/`](../../analysis_plan/send_pack_2026-08-22/). Hogan review does not gate it. Due 31 Aug 2026. |
| Spreadsheet columns Q, R | Bob pastes from [`../../analysis_plan/send_pack_2026-08-20/spreadsheet_QR_paste.md`](../../analysis_plan/send_pack_2026-08-20/spreadsheet_QR_paste.md) after reading the sheet headers. |

Submission sequence: [`submission_checklist.md`](submission_checklist.md). Routing: [`ARTEFACT_MAP.md`](ARTEFACT_MAP.md). Rebuild lock: [`../../knowledge/2026-08-22_stage3_rebuild.md`](../../knowledge/2026-08-22_stage3_rebuild.md).

**Scientific roles:** Hogan (weather exposures), Zhenyuan Liu (Hospital Authority outcomes), and David Makram Bishai (supervision).

## Build the submission-facing report

Word working copy plus XeLaTeX PDF (do not use LibreOffice to make the official PDF):

```bash
bash reports/laidlaw_stage3/build_stage3_report.sh
```

Poster:

```bash
cd reports/poster
pdflatex -interaction=nonstopmode Laidlaw_Stage3_A0_portrait.tex
cp Laidlaw_Stage3_A0_portrait.pdf ShenRuililin_Laidlaw_Stage3Poster.pdf
cp Laidlaw_Stage3_A0_portrait.pdf ../../outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf
```

## Superseded source document

The July literature-and-methods essay
([`essay_lit_methods.md`](essay_lit_methods.md) /
[`Essay_Lit_Methods.pdf`](Essay_Lit_Methods.pdf)) remains a writing and
literature source. It is **not** the 2026 submission copy.

The current submission report and poster make no stroke claim.
