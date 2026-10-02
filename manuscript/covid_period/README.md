# Current COVID manuscript development track

**Evidence-led revision, 2 October 2026:** a complete exploratory paper on recorded first hospitalisation burden before and during the pandemic. Annual counts declined before 2020, dipped further in 2020 and returned towards 2019 levels by 2023. Thermal models are sensitivity analyses. They do not identify physiological improvement or exclude a weather contribution.

Edit `Manuscript_covid_period_draft.md` here. `Heat_CVD_Manuscript_covid_period.docx` and `.pdf` are its review exports. `Supplement_covid_period.md`, `.docx` and `.pdf` report disjoint period means, all twelve baseline models, the complete official-day calendar sensitivity panel and all uncertainty constructions. `claim_ledger.yml` binds their values to approved CSVs and source hashes. `PRINT_PAGE_MAP.md` records the verified exports.

The protected HKO paragraph remains verbatim. The following paragraph clarifies that official days are summed threshold indicators and rainfall is a total. Admission cause and eligible person-time remain unavailable. The nested 84-month and full 132-month fits overlap and use recalculated spline bases. No independent 48-month later-era fit or interaction has arrived. Gate 3 remains open.

The live shared-document paste target in `../live_collaborative/`, the thermal archive, Stage 3 essay and poster are preserved. This revision supersedes the September candidate here; its earlier wording, ledger and export builder remain recoverable in Git. Do not rebuild the current paper with scripts 78/79/80: those enforce September page/prose/figure contracts, including the obsolete ruling-out framing.

## Reproduce this revision

Use the bundled document Python identified by the workspace dependency loader:

```sh
python scripts/81_covid_research_manuscript.py --audit
python scripts/81_covid_research_manuscript.py
```

The audit reads only approved aggregate CSVs. It checks actual table values, not their mere presence, and writes the ledger. Render both Word files with the packaged `documents/render_docx.py --emit_pdf`, using bundled LibreOffice, and inspect every page before replacing the PDF exports. The four source-bound figures are produced by `scripts/84_covid_evidence_figures.py` using standard Matplotlib and already-approved summaries; script 82 delegates to this builder. PDF/SVG vector exports and figure-source CSVs accompany the PNGs. Three figures appear in the main article and one in the supplement. No governed monthly health file is read by these operations.

Scientific review and next steps:

- `../../reports/auto_research/2026-10-02/EVIDENCE_LED_PACKET.md`
- `../../reports/auto_research/2026-10-02/EVIDENCE_LED_ADVERSARIAL_REVIEW.md`
- `../../reports/auto_research/2026-10-02/EVIDENCE_LED_VERIFICATION.md`
- `../../literature/covid_novelty_audit_2026-10-02.md`
- `../../analysis_plan/covid_period/evidence_led_protocol_2026-10-02.md`
- `../../analysis_plan/covid_period/ha_data_request_2026-10-02.md` — DRAFT UNSENT
- `SUBMISSION_COMPLETION.md`

The closest 2025–2026 diabetes, hypertension and continuity-of-care studies are discussed among the seventeen references. Access limitations and unchecked supplements are in the novelty audit. The prepared common-basis runner is unexecuted and uncalibrated here. Earlier Phase 2 review files are historical checks of their earlier exports.
No new transfer or approved output was available. Human ethics, event-definition, authorship and dissemination confirmations remain separate from completion of the scientific prose. No sending or submission has occurred.
