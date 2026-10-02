# Current COVID manuscript development track

**2 October 2026 revision:** a complete exploratory paper on recorded first hospitalisation burden before and during the pandemic. Annual counts declined before 2020, dipped further in 2020 and returned towards 2019 levels by 2023. Thermal models are sensitivity analyses. They do not identify physiological improvement or exclude a weather contribution.

Edit `Manuscript_covid_period_draft.md` here. `Heat_CVD_Manuscript_covid_period.docx` and `.pdf` are its review exports. `Supplement_covid_period.md`, `.docx` and `.pdf` report disjoint period means, all twelve baseline models, the complete official-day calendar sensitivity panel and all uncertainty constructions. `claim_ledger.yml` binds their values to approved CSVs and source hashes. `PRINT_PAGE_MAP.md` records the verified exports.

The protected HKO paragraph remains verbatim. The following paragraph clarifies that official days are summed threshold indicators and rainfall is a total. Admission cause and eligible person-time remain unavailable. The nested 84-month and full 132-month fits overlap and use recalculated spline bases. No independent 48-month later-era fit or interaction has arrived. Gate 3 remains open.

The live shared-document paste target in `../live_collaborative/`, the thermal archive, Stage 3 essay and poster are preserved. This revision supersedes the September candidate here; its earlier wording, ledger and export builder remain recoverable in Git. Do not rebuild the current paper with scripts 78/79/80: those enforce September page/prose/figure contracts, including the obsolete ruling-out framing.

## Reproduce this revision

Use the bundled document Python identified by the workspace dependency loader:

```sh
python scripts/81_covid_research_manuscript.py --audit
python scripts/81_covid_research_manuscript.py
```

The audit reads only approved aggregate CSVs. It checks actual table values, not their mere presence, and writes the ledger. Render both Word files with the packaged `documents/render_docx.py --emit_pdf`, using bundled LibreOffice, and inspect every page before replacing the PDF exports. The annual figure is produced by `scripts/82_covid_annual_counts_figure.py` using standard Matplotlib and the already-approved annual totals. No governed monthly health file is read by these operations.

Scientific review and next steps:

- `../../reports/auto_research/2026-10-02/PHASE2_ADVERSARIAL_REVIEW.md`
- `../../reports/auto_research/2026-10-02/PHASE2_DOCUMENT_QA.md`
- `../../reports/auto_research/2026-10-02/PHASE2_RESEARCH_DECISIONS.md`
- `../../literature/covid_physiology_evidence_2026-10-02.md`
- `SUBMISSION_COMPLETION.md`

No new transfer or approved output was available. Human ethics, event-definition, authorship and dissemination confirmations remain separate from completion of the scientific prose. No sending or submission has occurred.
