#!/usr/bin/env bash
# Stage 3 report: Word pathway (docx for Microsoft Word) + XeLaTeX PDF (submission).
# LibreOffice PDF export collapses pandoc tables; do not use it for the official PDF.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
python3 reports/laidlaw_stage3/make_reference_docx.py
pandoc reports/laidlaw_stage3/laidlaw_research_report_2026.md \
  --citeproc \
  --csl=literature/vancouver.csl \
  --resource-path="$ROOT" \
  --reference-doc=reports/laidlaw_stage3/stage3_reference.docx \
  -o reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.docx
python3 reports/laidlaw_stage3/fix_docx_tables.py
cp reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.docx \
  outputs/ShenRuililin_Laidlaw_Stage3Report.docx

pandoc reports/laidlaw_stage3/laidlaw_research_report_2026.md \
  --citeproc \
  --csl=literature/vancouver.csl \
  --pdf-engine=xelatex \
  --resource-path="$ROOT" \
  -H reports/laidlaw_stage3/report_preamble.tex \
  -o reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf
cp reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf \
  outputs/ShenRuililin_Laidlaw_Stage3Report.pdf
cp reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf \
  reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf
cp outputs/ShenRuililin_Laidlaw_Stage3Report.pdf \
  outputs/Laidlaw_Stage3_Research_Report_Shen.pdf
echo "built:"
ls -la reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.docx \
       reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf \
       outputs/ShenRuililin_Laidlaw_Stage3Report.pdf \
       outputs/ShenRuililin_Laidlaw_Stage3Report.docx
