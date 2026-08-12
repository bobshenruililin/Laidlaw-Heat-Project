# Laidlaw Stage 3 submission packet

## Submit these files

### Send to Prof. David Bishai now

Attach only:

- [`../../outputs/Laidlaw_Stage3_Research_Report_Shen.pdf`](../../outputs/Laidlaw_Stage3_Research_Report_Shen.pdf)

Use [`../../analysis_plan/bishai_stage3_endorsement_request.md`](../../analysis_plan/bishai_stage3_endorsement_request.md).

The official HKU report form is not present in the workspace. Do not invent it,
its fields, supervisor comments or signatures.

### Final HKU submission after endorsement

Submit:

1. `outputs/Laidlaw_Stage3_Research_Report_Shen.pdf`
2. the completed and endorsed official `2a. Laidlaw - Report Form (HKU).docx`

The currently recorded recipient is `laidlaw@hku.hk`; Bob must verify the
address and attachment requirements against the official 2026 instructions.

### Poster showcase

Use:

- [`../../outputs/Laidlaw_Stage3_Poster_Shen.pdf`](../../outputs/Laidlaw_Stage3_Poster_Shen.pdf)

Do not attach the poster to the Bishai review request or final HKU email unless
the official instructions explicitly require it.

## Current status

| Item | Status |
|---|---|
| CHD/HF scientific content | **READY** — exploratory, all core BH *q* > 0.19 |
| Stroke | Not delivered; no result reported |
| Research-report source | **READY** after the designated compliance trim |
| Research-report PDF | **READY** (rebuilt after trim) |
| A0 portrait poster | **READY** — one page, 841 × 1189 mm |
| Official HKU form | **MISSING FROM WORKSPACE** |
| External-result authorization | **HUMAN GATE** |
| Event-wording confirmation | **HUMAN GATE** |
| Bishai endorsement | **HUMAN GATE** |
| Final transmission | **BOB ONLY** |

The complete sequence is in
[`submission_checklist.md`](submission_checklist.md). The reusable publishing
pattern is in
[`../../knowledge/2026-08-12_laidlaw_publish_pattern.md`](../../knowledge/2026-08-12_laidlaw_publish_pattern.md).

## Rebuild the report after the trim

Run from the repository root:

```bash
pandoc reports/laidlaw_stage3/laidlaw_research_report_2026.md \
  --citeproc --pdf-engine=xelatex --resource-path="$PWD" \
  -o reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf

cp reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf \
  outputs/Laidlaw_Stage3_Research_Report_Shen.pdf
```

Verify the post-trim main text is no more than 3,000 words and that all figures
and references render.

## Poster source

The Stage 3 poster source is
[`../poster/Laidlaw_Stage3_A0_portrait.tex`](../poster/Laidlaw_Stage3_A0_portrait.tex).
Rebuild it only if authorized wording changes.

## Keep internal

Do not submit:

- `laidlaw_research_report_2026.md`
- `results_panel_chd_hf_2026-08-07.md`
- `pathway_literature_map.md`
- `essay_lit_methods.md` or its drafts
- `outputs/release_chd_hf/`
- `reports/bishai_integrated_report/`
- `manuscript/`
- the legacy `GEST2026_poster.*`
- governed source aggregates or merged health panels

The July literature-and-methods essay is source material only. It is not the
2026 submission report.
