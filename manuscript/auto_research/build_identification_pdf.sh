#!/usr/bin/env bash
# Compile the live identification article as a standalone PDF for the auto-research pack.
# Wording authority remains the live Markdown. This does not replace Hogan's shared file.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
mkdir -p outputs/auto_research
pandoc manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md \
  --pdf-engine=xelatex \
  --resource-path="$ROOT" \
  -V geometry:margin=2.4cm \
  -H manuscript/auto_research/preamble.tex \
  -o outputs/auto_research/identification_article_2026-09-02.pdf
echo "built identification article PDF"
ls -la outputs/auto_research/identification_article_2026-09-02.pdf
