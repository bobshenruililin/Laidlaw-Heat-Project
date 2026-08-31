# Ship: Hogan send-ready manuscript (one session, then stop)

Paste this entire file as the user message. Do not add “paste into the shared live document” as a remaining Bob task.

## Done when (all must hold)

1. **Attachable files only** (no README that tells Bob to paste):
   - `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.docx`
   - `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.pdf`
2. Rebuild with `python3 scripts/64_hogan_20260824_manuscript_docx.py` so Word and PDF match the live Discussion (short night/CHD and HF/cold **hypotheses**; WHO/HK HHAP **mapping**, not evaluation).
3. **Same graphs:** Figure 1 `figure_B_first_event_depletion.png`; Figure 2 `figure_A_cold_day_identification.png`; Figure 3 `figure_D_trend_depletion_sensitivity.png` (portrait official-count forest). Not release figure 4. S6 stays supplement.
4. **Same page contract:** A4; circulation banner absent; Tables 1–3 each on one page; Figure 3 on its own page; Hogan HKO sentences verbatim (`HOGAN_OPEN`, `HOGAN_AVG`); Table 2 = Model 1 numbers unchanged; `housing` absent; `medication` count 0; no Gate 3 / pipeline / “core panel” in the scientific body.
5. **No “paste” / “circulate” / “shared live document”** in PDF body text **or** Word comments. Rewrite the Table 2 comment so it does not say “paste Model 2”.
6. Print `sha256` prefixes and page count. Run `tests/test_hogan_methods_rewrite.py`, `tests/test_storm_physio_hhap.py`, `tests/test_hogan_exceeds_20260824_snapshot.py`, `python3 scripts/71_objective_audit_tripwires.py`.
7. Optional: one **email body** in `analysis_plan/send_pack_* /to_hogan.md` that Bob sends himself. Agents do not send Outlook.

## Stop (do not spend the hour on these)

- Inventing `UW XX-XXX`, Author 2–4 names, ICD lists, Model 2/3 health coefficients, stroke results, or a Gate 3 freeze.
- Rebuilding Stage 3 essay/poster unless Bob names them.
- Overwriting Hogan’s weather paragraph.
- A second parallel manuscript.

## Success sentence

Bob can attach the PDF (and Word if Hogan prefers) in one email. No further in-repo hour is required for **this** draft. Remaining holes are human-owned (IRB number, authorship, Roro ICD, team Gate 3).
