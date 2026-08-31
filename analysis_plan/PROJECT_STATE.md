# Project state & living context — Laidlaw Heat Project

**Last updated:** 2026-08-31
**Purpose:** Recover what is true now — science, people, tone, meeting notes — so context compounds.

Also read: `README.md`, `AGENTS.md`, `analysis_plan/human_agent_collaboration.md`.

---

## 0p. Canonical update — Stage 3 to Horizons (31 August)

- Professor Bishai circled **satisfactory**, wrote comments, signed, and dated **31 August 2026**. Keep his wording. Do not tidy it. Do not commit the signed form PDF.
- Bob sends form + essay to `laidlaw@hku.hk` today. Poster may go with that mail (file due 15 September). Pack: [`send_pack_2026-08-31/`](send_pack_2026-08-31/). Durable: [`../knowledge/2026-08-31_stage3_horizons_submit.md`](../knowledge/2026-08-31_stage3_horizons_submit.md).
- Horizons object is the **22 August** essay/poster Bob uploaded with the form (`c083d4096a0924b1` / `0ef58e0951bb2ffd`), matching the 23 August student date. Do not attach `Heat_CVD_Manuscript_20260824_hogan.pdf`. Do not swap in the 24 August rebuild on `main` unless he said he examined that PDF.
- F1000Research showcasing is not implied by this form. Gate 3 still open. Science unchanged: all twelve Model 1 *q* > 0.19.

## 0n. Canonical update — print Hogan PDF for Bishai (27 August)

- Bob is printing the 24 August live manuscript for Bishai’s review. Circulation banner removed. Tables 1–3 each stay on one page; figures and major IMRD sections start new pages. 21 A4 pages. SHA prefix `436fb4ff1b278ec8`.
- Science unchanged: Model 1 only in Table 2; all twelve *q* > 0.19; Hogan HKO sentences verbatim; `UW XX-XXX`; Acknowledgements `None.` Gate 3 still open.
- Form 2a still uses the Stage 3 essay, not this file. Print: `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.pdf`. Review: `manuscript/live_collaborative/PRINT_REVIEW_2026-08-27.md`. Durable: [`knowledge/2026-08-27_hogan_print_for_bishai.md`](../knowledge/2026-08-27_hogan_print_for_bishai.md).

## 0m. Canonical update — Stage 3 Hogan alignment for Bishai (24 August)

- Hogan’s 24 August comments asked for nested Model 1 / Model 2 / Model 3, not “core panel.” The 22 August programme essay still used twelve-model panel language. Bob authorised a Stage 3 rebuild. Science unchanged: all twelve Model 1 *q* > 0.19. Model 2/3 specified, not fitted. No invented health coefficients.
- Programme essay and A0 poster rebuilt. Essay SHA prefix `605cd8db43072cb5`; poster `a972206e61932650`. Introduction–Conclusion 2,773 words. Fable GO / Sol GO. Email A pack: [`send_pack_2026-08-24/`](send_pack_2026-08-24/). Do not attach the live manuscript. Form 2a supervisor block stays blank. Optional Hogan one-liner after the Bishai mail; paste remains human.
- Durable: [`knowledge/2026-08-24_stage3_hogan_align.md`](../knowledge/2026-08-24_stage3_hogan_align.md). Gate 3 still open.

## 0l. Canonical update — Hogan Methods rewrite (24 August)

- Commented PDF `Commented_Heat_CVD_Manuscript_20260824.pdf` read via `pdftotext` (no Acrobat balloons). Inventory: `manuscript/live_collaborative/hogan_20260824_comment_inventory.md`.
- Committee (Fable 5, Opus 5, Grok 4.6, Sol 5.6): **PR 69 base + PR 70 grafts**. Verdict: `manuscript/live_collaborative/COMMITTEE_VERDICT_PR69_vs_PR70.md`. Hogan-facing files: `Heat_CVD_Manuscript_20260824_hogan.docx` / `.pdf`.
- Live Methods: Hogan’s order; nested **Model 1 / Model 2 / Model 3**; equation **(1)** with every symbol named; present-tense Model 2/3; Table 2 = Model 1. No “core panel”. No Results in Methods. Acknowledgements `None.`
- **Model 1** = twelve thermal fits (Table 2). **Model 2** = Model 1 + monthly mean RH + monthly total rainfall ([21] humidity, both tails, modest; [22] Chan 2013 rainfall as attendance hypothesis). **Model 3** = leave-one-year-out same-calendar-day warmer/cooler **mean** counts (15 July 2018 example). Max/min counts are sensitivities. Model 2/3 health coefficients are **not** invented.
- Hogan’s HKO weather paragraph kept verbatim, including the averaging sentence. Rainfall-as-total is a Word comment, not a body overwrite. `UW XX-XXX` stays at the start of Methods.
- Data availability: GitHub URL; counts not posted; no invented data-sharing agreement. Contract tests: `tests/test_hogan_methods_rewrite.py`. Gate 3 still open. Programme Stage 3 PDFs live on the 24 August Hogan-align rebuild (`605cd8db43072cb5` / `a972206e61932650`); this track owns the live-manuscript paste pack only.

## 0k. Canonical update — roundtable fold-back before Email A (22 August, night)

- Independent Fable + Sol specs, then a merge: numbered limitations, Methods “How to read the estimates” gloss, Bishai paragraph moved to Acknowledgements, data-provider confirmation restored, Implications heading inside Discussion, Table 1/2/A1 caption-body glue, poster pre-2020 + human footer + unequal HF/CHD callouts. REFERENCES strip kept. Robotic “machine-validated” / “privacy-protected” footer lines not restored.
- New SHA prefixes: essay `c083d4096a0924b1`, poster `0ef58e0951bb2ffd`. Introduction–Conclusion 2,575 words. Fable GO / Sol GO. Durable: `knowledge/2026-08-22_stage3_foldback.md`. Form 2a still Email A. Gate 3 still open.

## 0j. Canonical update — A0 poster REFERENCES strip (22 August, evening)

- Bob asked for a compact reference section on the Stage 3 poster. Fable chose six numbered entries at the bottom, four in-text superscripts, and no citations in Results or the conclusion box.
- Poster SHA-256 prefix `82c077d69c414d18`. Still one-page ISO A0. Essay unchanged (`8b71157e5178b589`). Durable: `knowledge/2026-08-22_stage3_poster_refs.md`. Form 2a still Email A. Gate 3 still open.

## 0i. Canonical update — Word-pathway Stage 3 cut (22 August, second pass)

- Bob asked for stronger Bishai credit, a Table 1 that stays on the page, a hard 3,000-word cut, and the 15 August collab `.docx` as a **format** model. The live manuscript is still not the attachment.
- Essay rebuilt: IMRD + structured Abstract (excluded from the count), numbered citations, footnotes, appendix ladder. Introduction–Conclusion ≈ 2,670 words. Supervisor line + Introduction + Acknowledgements name Professor David Makram Bishai.
- Table 1 is four columns plus a note (no overflowing event-definition column). PDF is XeLaTeX. A Word copy is `outputs/ShenRuililin_Laidlaw_Stage3Report.docx` for opening in Microsoft Word; do not send the 15 August collab draft.
- New PDF SHA-256 prefix `8b71157e5178b589`. Poster later gained a REFERENCES strip (`82c077d69c414d18`; see 0j). Durable: `knowledge/2026-08-22_stage3_word_pathway.md`. Form 2a still Email A. Gate 3 still open.

## 0h. Canonical update — send the accessible essay, not the live manuscript (22 August evening)

- Fable and Sol: **SEND AFTER HUMAN BLANKS**. Do not attach Hogan’s live file or the 15 August collab Word. Keep the slightly more accessible research essay.
- A later same-day rebuild (0i) cut words and added Bishai credit on Bob’s instruction. Do not attach the live manuscript.
- Supervisor one-pager remains optional. Default Email A is essay PDF + form 2a.
- Durable: `knowledge/2026-08-22_stage3_essay_vs_manuscript.md`. Gate 3 still open.

## 0g. Canonical update — Stage 3 report and poster rebuilt (22 August)

- Bob authorised a replacement of the 12 August Sol PDFs. New submission names: `outputs/ShenRuililin_Laidlaw_Stage3Report.pdf` and `outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf` (SHA-256 prefixes `b8b4c63ca9d32dd3` / `b3f16ff27f76ea9b`).
- Poster change is surgical: the self-referential footer is deleted; only `shenrll@connect.hku.hk` remains. Layout, figures, and conclusion box are otherwise unchanged. Still one-page A0 portrait.
- Report: TeX Gyre Termes, no contents list, about 3,175 main-text words, formal article layout. Honesty aligned with the live manuscript (unrounded NW3, pre-2020 CHD interval, ACF 0.508, no “most elevated”). Not a journal clone. Fable and Sol both GO on the PDFs; 0h confirms send-the-essay, not the live file.
- Durable: `knowledge/2026-08-22_stage3_rebuild.md`. Form 2a is still Email A to Bishai. Gate 3 still open.

## 0f. Canonical update — obtain form 2a (22 August)

- Remaining Stage 3 job is Bishai’s endorsement. Programme PDFs were rebuilt the same day on Bob’s instruction (see 0g). Fable/Sol evening check: send the accessible essay, not the live manuscript (see 0h).
- Hogan reviewing the live file does **not** gate form 2a. He does not sign it. Do not put the form on his Outlook thread.
- Dual path: Email A tonight/Sunday (`send_pack_2026-08-22/`); printed form at Thursday 27 August if unsigned; last comfortable remote date Friday 28 August; submit to `laidlaw@hku.hk` on 31 August after signature.
- Default packet is essay + form 2a. The supervisor one-pager is an optional Thursday print sheet; it now matches the rebuilt conclusion.
- Durable: `knowledge/2026-08-22_stage3_endorsement.md`. Gate 3 still open.

## 0e. Canonical update — Email A to Bishai (20 August)

- **Send now:** new programme note to Professor Bishai with form 2a + locked essay. Ask for the supervisor block by Friday 28 August. Report due 31 August; poster file 15 September (printed on the form). Optional poster attachment is for information only.
- Hogan’s note that he is going through Bob’s work and will add “the TV” to the temperature data panel is weather-panel work. It does **not** delay Email A. Do not put the form on that thread.
- Locked PDFs re-verified against the 20 August uploads (prefixes `6136e85a654502a0` / `4f7c1e408ae2d31f`). Do not rebuild.
- Pack: [`send_pack_2026-08-20/`](send_pack_2026-08-20/). Decide note: [`../knowledge/2026-08-20_bishai_form2a.md`](../knowledge/2026-08-20_bishai_form2a.md). Surfaces: [`../knowledge/2026-08-20_stage3_vs_manuscripts.md`](../knowledge/2026-08-20_stage3_vs_manuscripts.md).
- Agents draft; Bob fills, signs, and sends. Gate 3 still open.

## 0d. Canonical update — intern ceiling note (18 August)

- Printable intern note for Hogan and Bishai, cut to a two-page meeting object (three questions: Hogan exposure family; Bishai identification-focused paper without a confirmatory primary; Roro yes/no on definitions/stroke/person-time/age, not a same-day extract). Public-file search remains a separate log. Form A/B and EHPDCL remain PI paths. Factual inversion in the long note (pre-2020 nine of twelve **exclude** 1) is corrected. CHD hot-night 1.022 is per five nights and SE-sensitive. MDE from the existing ladder is intern-owned identification, not a primary.
- Public-file search was executed, not asserted: HA throughput JSON, DH 2023 ICD-chapter CSV, CKAN (one quarterly throughput table; zero disease-group packages), public HKO daily temperature. Guo 2024 admissions remain licensed. Form A/B and EHPDCL are PI paths.
- Files: `reports/ceiling_card_hogan_bishai_2026-08-18.md` (one page) and `reports/ceiling_note_hogan_bishai_2026-08-18.md` (two-page meeting note). Long working justification: `reports/ceiling_note_hogan_bishai_2026-08-18_long.md`. Search: `reports/public_data_ceiling_search_2026-08-18.md`. Durable: `knowledge/2026-08-18_intern_ceiling_note.md`. Gate 3 still open. Do not paste the note into the live manuscript.

## 0c. Canonical update — raise-and-stop (18 August)

- Frozen 1–10 bar locked before Fable 5 / Sol 5.6 scored. Ceiling remains 6–7. No 8 without new governed data or a multiplicity-protected claim.
- Intersection implemented: Results sentence for the pre-2020 nine-of-twelve (Abstract unchanged); live-track SI `manuscript/live_collaborative/supplement_live_track.md`. Cover letter not drafted (does not land).
- Stop-round: Fable **7.0**, Sol **6.5**. Both: further agent-owned work cannot move either number. Loop closed.
- Bob re-pastes from `REPASTE_2026-08-18.md` into Hogan’s file. Hogan-before-Bishai. Gate 3 still open.

## 0b. Canonical update — auto-research lab (16 August)


- Jin-adapted lab (Playbook 05): branching families, adversarial audit, machine claim ledger. Stop rule is “identification article survives checking,” not “assume a thermal proof exists.”
- First run residue: `analysis_plan/auto_research/`. Independent adversary recorded no kills. Hogan-lock readiness and stroke/person-time idle checklists are packets, not locks or coefficients. Supplementary numbering (S1/S7/S9) is a named Bob-owned gap, not a new result.
- Durable: `knowledge/2026-08-16_auto_research_lab.md`.

## 0a. Canonical update — CNS-register live paper (15 August)

- Fable / Opus / Sol team produced the strongest honest paper the monthly panel can support: an identification article, not a discovery headline.
- Live paste pack: `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md` and `Heat_CVD_Manuscript_20260815_collab_draft.docx`. Hogan weather paragraph unchanged. His seven 28 July comments are answered in `hogan_comment_paste_replies.md`. Figure 3 is now trend/depletion sensitivity; ACF is supplement. Abstract carries the pre-2020 CHD hot-night null. Twenty-nine of 132 months carry ≥1 official cold day.
- CNS *register* applied; CNS *venue* not claimed. First journal target after human blockers: Environmental Research (EHP reach). Gate 3 still open. Stage 3 PDFs still byte-locked.
- Durable: `knowledge/2026-08-15_cns_paper_team.md`; `manuscript/cns_team/00_parent_synthesis.md`.

## 0. Canonical update — final integrated reanalysis (10 August)

- Current runnable outcomes: CHD and HF first recorded hospitalisation after
  first diagnosis among a T2D/HTN cohort, 132 territory-months. Admission cause
  is absent; stroke was not delivered.
- Analysis of record: separate negative-binomial exposures, calendar-month +
  `ns(time,4)`, days offset, full Model/HC1/NW3/NW6 ladder.
- All twelve core q-values exceed 0.19. HF cold days are SE-concordant but
  q-unprotected; CHD hot nights are SE-sensitive. No protected differential
  thermal claim.
- Exact Wang/Li weather engine passes five source-count reproductions.
- Clean-room M|D daily-recovery method failed 500-replicate F1.2 gates; no
  real daily coefficient is admitted.
- Final packet:
  `reports/bishai_integrated_report/integrated_project_report.pdf`,
  `manuscript/chd_hf_thermal_associations_2013_2023.pdf`,
  `manuscript/chd_hf_supplement.pdf`, and `outputs/release_chd_hf/` (29/29).
- Lead scientific recommendation: Gate 3 Option A — explicit no confirmatory
  primary; methods-focused exploratory paper. Human approval remains open.
- Durable handoff: `knowledge/2026-08-10_cns_final_reanalysis.md`.

---

## 1. People and roles

| Person | Contribution | Note |
|---|---|---|
| **Hogan** | Weather / heat framing; Goggins challenge; 65–69 & 70–74; climate X file; hot-month (heatwave counts → upper-tail months); Atmos Res pointer; **author of the live manuscript’s weather Methods and reviewer of its Introduction**; academic-writing guidance | His live weather section is primary; credit openly; do not overwrite it with repository prose |
| **Roro (Zhenyuan Liu)** | Governed HA outcome construction/transfer; regression mentorship; health-data Methods; excess heat-mortality baseline (medRxiv 2026) | Delivered CHD/HF first-event aggregates 6–7 Aug; stroke still missing; revised mortality PDF audited 10 Aug |
| **Prof. David Bishai** | Dec 2025 plan; multi-method; teamwork (“go far together”); Jasmine null-pattern / extend-to-2023; ~10°C discussion prompt; concept lead on Roro excess-mortality paper | Jasmine identity resolved (Jingwen Liu 2020 SCS) |
| **Bob Shen** | Analysis plumbing, pollution assembly, writing; Introduction revisions and non-weather Methods due 5 Aug | Work directly in the live manuscript; preserve Hogan’s weather section and Roro’s health-data ownership |

---

## 2. Outcome semantics (working understanding)

- General HA file: **no admission reasons** → AMI out of scope from that file.
- Stroke aggregates: use **first GOPC mention of stroke as a marker**; hospitalisation/actual stroke generally **precedes** that mention; **do not use second mentions** for incident identification; recover true event month for aggregation.
- Confirm field-level algorithm with Roro before locking methods text.

---

## 3. Scientific state

- Current estimand: monthly thermal exposures × CHD/HF first-hospitalisation
  counts under a days offset; monthly count ratios, not incidence. Future
  stroke estimand remains blocked by the missing file.
- Public layers ready: HKO climate/extremes/spells, EPD pollution, C&SD denominators, CHP flu (121/132).
- Pathway panel P01–P18 (P13 off until subtype); headline proposal P02+P04 after Gate 3 **with team**.
- **Hot/cold month catalogue:** HM01–HM50 / CM01–CM48 + pathways H01–H12 / C01–C12 (`analysis_plan/hot_cold_month_catalogue.md`; starters in `hot_cold_month_registry.yml`; next-week sheet `hot_cold_next_week_runsheet.md`).
- **Jasmine is confirmed:** Jingwen Liu et al. (2020), *Sustainable Cities and Society* 57:102131, DOI `10.1016/j.scs.2020.102131`; Hong Kong daily mortality 2006–2016; DLNM + quasi-Poisson; reversed J; cold AF 4.72% vs heat AF 0.16%; moderate AF 4.25% vs extreme AF 0.63%. Full PDF/supplement extraction remains pending (`literature/jasmine_liu2020_confirmed.md`; protocol in `jasmine_extension_protocol.md`).
- **Roro medRxiv baseline:** Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika and David Bishai, DOI `10.64898/2026.03.05.26347683`; model-based multi-definition heatwave excess mortality, 2014–2023. It uses RRs from Jasmine and Wang/Ren. MedRxiv v1 deep-read is in `literature/roro_manuscript_deep_read.md`; the private revised PDF was audited in `literature/roro_revised_manuscript_audit_2026-08-10.md` and is not the public citation.
- **Family science baseline:** Jasmine daily mortality AF/RR → Roro absolute heat excess-death scenarios → our monthly stroke morbidity panel. These are complementary estimands (`literature/jasmine_roro_family_map.md`; `literature/exceed_jasmine_and_roro_baseline.md`).
- **Gene/~10°C:** discussion hypothesis only, not a biological threshold or result.
- **No stroke coefficients.** CHD/HF coefficients are exploratory; all core
  q-values exceed 0.19. Synthetic calibration ≠ health findings.

---

## 4. Meeting notes (week of share)

- Writing early (lit + methods) looks like serious research to peers.
- Marmot / health equity as inspiration for who bears thermal risk.
- Peer heat project: district representative Mandy; heat summit; possible LegCo hearing — ambient motivation for HK heat work, not our results.
- Share **deck** (not brief) for lab; bare title slide (identity only).
- Closing nudge to Hogan + Roro + Bishai (Jasmine source table/full PDF, weather lock and outcome timing) with `:)` .
- Next week: spin out hot-month / cold-month definitions (catalogue ready; lock with Hogan).

### Tuesday 28 July — Hogan weather lock

- Hogan offered to meet; Bob is free Tuesday. Start by listening to Hogan's current weather framing and the Goggins challenge.
- Meeting target: written Li-HW / `HM23` parameters; one hot and one cold Gate 3 co-primary; status of Roro's four `HWD_*` definitions; threshold reference period; `CM05` as sensitivity only; and visibility of ages 65–69 / 70–74 if governed aggregates permit.
- Bring definition options and exposure-only graphs. Do not present them as health findings or ask Hogan to approve a finished weather answer.
- Credit split: Li et al. supply the atmospheric event definition; Hogan proposed the project-level count-by-month → upper-tail adaptation. Roro retains ownership of outcome timing.
- Working set: [`reports/hogan_tuesday/README.md`](../reports/hogan_tuesday/README.md) (pack index); briefing / decision sheet / agenda / talking points / email under `analysis_plan/hogan_tuesday_*`; knowledge entry `knowledge/2026-07-28_hogan_tuesday_prep.md`.

### Friday 7 August — HA CHD/HF arrival and amended reanalysis

- Roro delivered monthly CHD and HF first-hospitalisation counts (T2D/HTN cohort; first hosp after first CVD diagnosis; Dr Zhou assisted). Stroke mentioned in email but **not attached**.
- Playbooks 02–03 executed for CHD+HF: QC, merge, full pathway panel, provisional HM/CM, descriptives, offset/period sensitivities, forests.
- **Amendment A1:** real-only diagnostics; separate single-exposure core (days-only offset; Newey–West lag-6); joint P02/P04 retained as collinearity diagnostics only; scripts 31–34 + `outputs/release_chd_hf/` (9/9 validation PASS).
- Amended exploratory pattern (Gate 3 open; all core q > 0.19): CHD hot nights /5 → 1.022 (1.002–1.042); HF cold days /5 → 1.073 (1.006–1.144).
- Separate CHD/HF manuscript draft: `manuscript/chd_hf_thermal_associations_2013_2023.md` (does not overwrite Hogan’s live stroke-oriented weather Methods).
- Gate 1 conditional / Gate 2 closed for CHD+HF; Gate 3 packet ready but **open**.
- Temperature share for Roro: `outputs/share_for_roro/`.
- HA month-level counts remain gitignored under `data_raw/ha_secure_placeholder/` and `data_processed/*_aggregates_normalized.csv` / `*_analysis_panel.csv`.
- Dissemination: aggregates OK for internal draft; Roro/Bishai confirmation still required before external submission.

### Wednesday 5 August — LSN research summary

- Paste-ready Laidlaw Scholar Network research-project summary: [`reports/lsn/research_project_summary.md`](../reports/lsn/research_project_summary.md).
- Interactive exposure-only companion: [`docs/lsn/`](../docs/lsn/) (REAL HKO monthly climate; no stroke findings). Bob edits before posting to LSN.
- Knowledge note: [`knowledge/2026-08-05_lsn_research_summary.md`](../knowledge/2026-08-05_lsn_research_summary.md).

### Wednesday 12 August — live manuscript (Hogan skeleton → CHD/HF draft)

- Hogan’s 28 July live file is now the paste target: Methods remainder finished; Introduction comments answered; first Results/Discussion written to the delivered CHD/HF first-hospitalisation contract. Weather paragraph copied verbatim. Health data remains Roro’s to expand. Author 2–4 still placeholders.
- Working set: [`manuscript/live_collaborative/`](../manuscript/live_collaborative/). Knowledge: [`2026-08-12_live_manuscript_collab.md`](../knowledge/2026-08-12_live_manuscript_collab.md).
- One reply-all on Hogan’s 12 August thread: [`send_pack_2026-08-12/reply_on_thread.md`](send_pack_2026-08-12/reply_on_thread.md). Attach the temperature CSV and `HKO_temperature_panel_2013_2023.pdf`. Do not attach markdown, a parallel manuscript, or a programme report. Paste list for the live file (Shen Ruililin edits it himself): [`LIVE_DOC_EDITS.md`](../manuscript/live_collaborative/LIVE_DOC_EDITS.md). How the thread works: [`correspondence_working_culture.md`](../knowledge/correspondence_working_culture.md).
- **Sol Stage 3 freeze:** report + A0 poster PDFs are byte-identical to Bob’s uploaded Sol copies. This branch does not rewrite them. See [`2026-08-12_sol_stage3_outputs_lock.md`](../knowledge/2026-08-12_sol_stage3_outputs_lock.md).

### Wednesday–Thursday 12–13 August — end-game live paste pack

- Overnight job finished the Hogan live file as a paste pack, not a third paper. Title, Abstract, Introduction, remaining Methods, Results (Tables 1–3 + Figures 1–3), Discussion, and references 9–21 are written to the CHD/HF first-event contract. Weather paragraph still verbatim. Health data still Roro’s to expand.
- Literature upgrades: Goggins and Chan (2017) as daily HF history; Guo et al. (2024) for official hot-night flag versus hourly excess heat. Identification figures: DJF cold days, first-event depletion vs C&SD 35+, residual ACF.
- Working set: [`manuscript/live_collaborative/`](../manuscript/live_collaborative/) (`LIVE_DOC_EDITS.md`, `Heat_CVD_Manuscript_20260813_collab_draft.docx`). Night memo: [`2026-08-13_live_doc_night_explore.md`](../knowledge/2026-08-13_live_doc_night_explore.md). Three surfaces: [`2026-08-13_three_manuscript_surfaces.md`](../knowledge/2026-08-13_three_manuscript_surfaces.md).
- Do not email the Word copy. Paste into Hogan’s shared file. Laidlaw Stage 3 PDF and A0 poster remain byte-locked.

### Thursday 13 August — research team (Kimi / Fable / Opus / Sol)

- Charter: [`knowledge/2026-08-13_research_team_charter.md`](../knowledge/2026-08-13_research_team_charter.md).
- Sol (programme): keep Stage 3 PDF and A0 poster frozen. Living routing index: [`reports/laidlaw_stage3/ARTEFACT_MAP.md`](../reports/laidlaw_stage3/ARTEFACT_MAP.md). Memo: [`2026-08-13_sol_laidlaw_deliverable_system.md`](../knowledge/2026-08-13_sol_laidlaw_deliverable_system.md). LSN 5 August stroke frame is stale; do not post unchanged.
- PI public-data check: HKO Year’s Weather 2013/2019/2021/2023 match the extremes table; EPD GIA general-station NO₂/PM2.5/O₃ match in rounded magnitude. 2024 (50 hot nights, 52 very hot days, 11 cold days) is post-sample only. [`2026-08-13_pi_hko_yearbook_check.md`](../knowledge/2026-08-13_pi_hko_yearbook_check.md).
- Kimi harvest: yearbooks, EPD endpoints, and Guo/Goggins/Liu numbers re-verified at source; no live-paper numeral change. [`2026-08-13_kimi_web_weather_lit_harvest.md`](../knowledge/2026-08-13_kimi_web_weather_lit_harvest.md).
- Fable critique merged: Newey–West CHD hot-night intervals are *narrower* than Model (Discussion now says so); CHD pre-2020 1.011 (0.991–1.032) reported beside the HF pre-2020 interval; “continuity” → “core panel.” [`2026-08-13_fable_live_doc_critique.md`](../knowledge/2026-08-13_fable_live_doc_critique.md). Synthesis: [`2026-08-13_research_team_synthesis.md`](../knowledge/2026-08-13_research_team_synthesis.md).
- Next three weeks (compute vs human gates): [`next_three_weeks_prospect_2026-08-13.md`](next_three_weeks_prospect_2026-08-13.md).
- Cycle 1 (13 Aug): pathway execution audit; Hogan identification one-pager; week-of-data blog draft; LSN rewrite to CHD/HF. [`../reports/researcher_cycle_2026-08-13.md`](../reports/researcher_cycle_2026-08-13.md).

### Wednesday 12 August — Hogan tonight + Bishai Stage 3

- Hogan meeting: listen first; lock weather reference period / `CM05` / live-file paste permission; do not dump coefficients. Sheet: [`hogan_tonight_2026-08-12.md`](hogan_tonight_2026-08-12.md).
- Bishai: Stage 3 report + three decisions (dissemination, stroke wait, person-time/age-band request). Draft: [`bishai_stage3_status_report.md`](bishai_stage3_status_report.md).
- Roro ranked monthly asks: [`roro_missing_data_asks.md`](roro_missing_data_asks.md).
- Unused existing-data read (no new models): [`2026-08-12_existing_data_insights.md`](../knowledge/2026-08-12_existing_data_insights.md).

### Sunday 2 August — live manuscript handoff

- Hogan created and shared a live manuscript with Bob and Roro, commented on the Introduction, and wrote the weather component of Methods.
- The shared file is now the manuscript authority. Work in it directly; stop exchanging parallel manuscript versions.
- Bob owns the Introduction response and the remainder of Methods by **5 August**. He should adapt the canonical essay for design, pollution, population denominators, statistical analysis and thermal-panel discipline, without replacing Hogan’s weather text.
- Roro owns cleaned monthly stroke data and the health-data Methods by **7 August**. Bob’s outcome text is only a brief bridge using the already agreed GOPC-marker principle.
- Hogan will review each contribution after completion. His 28 July Introduction comments are now recorded from the uploaded live file in [`manuscript/live_collaborative/hogan_comment_responses.md`](../manuscript/live_collaborative/hogan_comment_responses.md); do not invent further threads.
- Working set: [`hogan_live_manuscript_handoff.md`](hogan_live_manuscript_handoff.md), [`methods_remainder_bob_aug5.md`](../manuscript/methods_remainder_bob_aug5.md), [`introduction_revision_notes.md`](../manuscript/introduction_revision_notes.md), and [`2026-08-02_hogan_live_manuscript.md`](../knowledge/2026-08-02_hogan_live_manuscript.md).

---

## 5. Laidlaw Stage 3

- Research report — current submission copy:
  `reports/laidlaw_stage3/laidlaw_research_report_2026.md` +
  `reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf`
  (≈3,200 main-text words; accessible CHD/HF report with figures, references,
  and appendices). The July stroke-framed literature-and-methods essay remains
  source material, not the submission copy.
- Pathway map: `reports/laidlaw_stage3/pathway_literature_map.md`.
- Poster: readable A0 **portrait** 841×1189 mm at
  `reports/poster/Laidlaw_Stage3_A0_portrait.pdf`; six required sections,
  26-point body type, reproducible poster-specific figures. The GEST landscape
  poster is legacy only.
- HKU report form: official template is Bob’s local copy. Email A send pack
  [`send_pack_2026-08-20/`](send_pack_2026-08-20/). Supervisor block still
  blank. Spreadsheet Q/R — Bob pastes after reading the sheet headers.

---

## 6. Stylistic preferences

- Title slide: title + Bob identity only (no taglines/status strips).
- Credit Hogan/Roro/Bishai; minimise self-credit.
- Emails: sincere, short, human.
- Multimedia: cut to pathway map + essay PDF during talk.
- **Academic prose:** follow `analysis_plan/writing_standards_hogan.md` — less flowery, easier to digest; Hogan mentors writing + climate.

---

## 7. What is done vs still human-gated (as of 2 August 2026)

### Done remotely (do not re-do without new evidence)
- Pathway panel plumbing + HM/CM catalogue (50/48) + starters
- Jasmine identity locked; Roro medRxiv v1 deep-read; exceed-baseline + family map + adjacent crawl
- Week 2 deck / Laidlaw lit-methods draft updated for Jasmine + Roro
- Pollution monthly layer; flu (121/132); holiday scaffold
- Live-manuscript handoff, non-weather Methods draft, Introduction revision draft and acknowledgement email prepared

### Still needs humans / files (cannot fake)
1. **Stroke monthly file** from Roro (referenced but not attached on 7 Aug)
2. **Team Gate 3 freeze** using `reports/gate3_decision_packet_2026-08-07.md`
3. **Hogan weather lock** for HM23 reference period (provisional flags only today)
4. Confirm ICD/inpatient inclusion lists; ideally T2D/HTN cohort denominators
5. **Bob live-file paste:** 13 August end-game pack in `manuscript/live_collaborative/LIVE_DOC_EDITS.md`; paste into Hogan’s shared file only; do not overwrite weather Methods; do not email a parallel Word copy. Send pack: `send_pack_2026-08-12/`
6. Jasmine full PDF; Roro revised mortality manuscript diff
8. **Bob sends Email A** (`send_pack_2026-08-20/`): form 2a + locked essay to Bishai; supervisor block by Friday 28 August. Spreadsheet Q/R paste after reading headers.

### Done remotely (do not re-do without new evidence)
- Pathway panel plumbing + HM/CM catalogue (50/48) + starters
- Jasmine identity locked; Roro medRxiv v1 deep-read; exceed-baseline + family map + adjacent crawl
- Week 2 deck / Laidlaw lit-methods draft updated for Jasmine + Roro
- Pollution monthly layer; flu (121/132); holiday scaffold
- Live-manuscript handoff, non-weather Methods draft, Introduction revision draft and acknowledgement email prepared
- **REAL CHD/HF full pathway + provisional HM/CM panels, descriptives, sensitivities, Gate 2 close, Gate 3 packet, CNS panel Results report**

Until the team freezes Gate 3, panel coefficients are complete analyses but not primary manuscript claims. Stroke remains unanalysed.

---

## 8. Upcoming workflow

1. **Bob’s 5 Aug manuscript contribution:** work in the live file; answer the visible Introduction comments; add design, pollution, denominators, statistical analysis and thermal-panel discipline; leave Hogan’s weather Methods intact.
2. **Roro’s 7 Aug handoff:** receive the cleaned monthly stroke aggregates and health-data Methods without inferring any undisclosed fields or counts.
3. **HA aggregate arrival:** confirm governance and dictionary; inventory without inventing fields; QC schema, timing, suppression, grain, subtype, coverage, and denominator compatibility; merge only after Gate 1. Switch to `PATHWAY_MODE=real` only after Gate 2 closes. Follow [`playbooks/02_ha_data_arrival.md`](playbooks/02_ha_data_arrival.md).
4. **Weather reconciliation:** treat Hogan’s live weather section as primary; transcribe only explicit decisions into the registry and catalogue. A written manuscript rule is not automatically the Gate 3 headline choice. Follow [`playbooks/01_hogan_definition_lock.md`](playbooks/01_hogan_definition_lock.md) where applicable.
5. **Full analysis:** run the complete `P01–P18` and registry-driven HM/CM panels; validate diagnostics; freeze the headline specification at Gate 3 **with the team**; export complete manuscript tables without cherry-picking. Follow [`playbooks/03_full_analysis_run.md`](playbooks/03_full_analysis_run.md).
6. **CNS final write-up:** only verified real estimates enter Results and Discussion. Engage [`.cursor/skills/cns-writing/SKILL.md`](../.cursor/skills/cns-writing/SKILL.md), revise the live manuscript in spare academic prose, and preserve estimand boundaries. Follow [`playbooks/04_final_writeup.md`](playbooks/04_final_writeup.md).

At every transition, refresh [`knowledge/CONTEXT_BOOTSTRAP.md`](../knowledge/CONTEXT_BOOTSTRAP.md). Use [`playbooks/99_emergencies.md`](playbooks/99_emergencies.md) for source, scope, governance, or provenance shocks.
