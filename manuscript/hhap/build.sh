#!/usr/bin/env bash
# Build the HHAP companion PDF/Word. Does not rebuild Stage 3. Does not freeze Gate 3.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
mkdir -p outputs/auto_research manuscript/hhap
pandoc manuscript/hhap/who2026_hong_kong_instrument_map.md \
  --citeproc \
  --bibliography=literature/references.bib \
  --csl=literature/vancouver.csl \
  --pdf-engine=xelatex \
  --resource-path="$ROOT" \
  -H manuscript/hhap/preamble.tex \
  -o manuscript/hhap/who2026_hong_kong_instrument_map.pdf
cp manuscript/hhap/who2026_hong_kong_instrument_map.pdf \
  outputs/auto_research/who2026_hong_kong_instrument_map.pdf
pandoc manuscript/hhap/who2026_hong_kong_instrument_map.md \
  --citeproc \
  --bibliography=literature/references.bib \
  --csl=literature/vancouver.csl \
  -o manuscript/hhap/who2026_hong_kong_instrument_map.docx
echo "built HHAP companion"
ls -la manuscript/hhap/who2026_hong_kong_instrument_map.pdf \
       outputs/auto_research/who2026_hong_kong_instrument_map.pdf
