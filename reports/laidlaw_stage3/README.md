# Laidlaw Stage 3 workspace

Summer 2026 deliverables (HKU Laidlaw):

| Deliverable | Status in repo |
|---|---|
| Research essay (accessible academic paper; 2,000–3,000 words) | **Submission copy:** [`ShenRuililin_Laidlaw_Stage3Report.pdf`](ShenRuililin_Laidlaw_Stage3Report.pdf) · source [`laidlaw_research_report_2026.md`](laidlaw_research_report_2026.md) · [`../../outputs/ShenRuililin_Laidlaw_Stage3Report.pdf`](../../outputs/ShenRuililin_Laidlaw_Stage3Report.pdf). Main text ≈2,900 words. SHA-256 prefix `b8b4c63ca9d32dd3`. |
| Pathway × literature map (multimedia) | [`pathway_literature_map.md`](pathway_literature_map.md) |
| A0 portrait poster 841×1189 mm | [`../poster/ShenRuililin_Laidlaw_Stage3Poster.pdf`](../poster/ShenRuililin_Laidlaw_Stage3Poster.pdf) · [TeX](../poster/Laidlaw_Stage3_A0_portrait.tex) · [`../../outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf`](../../outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf). SHA-256 prefix `b3f16ff27f76ea9b`. GEST landscape is legacy only. |
| HKU report form + supervisor endorsement | **Email A ready.** Official form is Bob’s local copy. Current pack: [`../../analysis_plan/send_pack_2026-08-22/`](../../analysis_plan/send_pack_2026-08-22/). Supervisor block stays blank. Due 31 Aug 2026. |
| Spreadsheet columns Q, R | Bob pastes from [`../../analysis_plan/send_pack_2026-08-20/spreadsheet_QR_paste.md`](../../analysis_plan/send_pack_2026-08-20/spreadsheet_QR_paste.md) after reading the sheet headers. |

Submission sequence: [`submission_checklist.md`](submission_checklist.md). Routing: [`ARTEFACT_MAP.md`](ARTEFACT_MAP.md). Rebuild lock: [`../../knowledge/2026-08-22_stage3_rebuild.md`](../../knowledge/2026-08-22_stage3_rebuild.md).

**Scientific roles:** Hogan (weather exposures), Zhenyuan Liu (Hospital Authority outcomes), and David Makram Bishai (supervision).

## Build the submission-facing report

Run from the repository root:

```bash
pandoc reports/laidlaw_stage3/laidlaw_research_report_2026.md \
  --citeproc --pdf-engine=xelatex --resource-path="$PWD" \
  -H reports/laidlaw_stage3/report_preamble.tex \
  -o reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf
cp reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf \
  outputs/ShenRuililin_Laidlaw_Stage3Report.pdf
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
