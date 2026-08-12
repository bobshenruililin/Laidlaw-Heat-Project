# Project state & living context — Laidlaw Heat Project

**Last updated:** 2026-08-12
**Purpose:** Recover what is true now — science, people, tone, meeting notes — so context compounds.

Also read: `README.md`, `AGENTS.md`, `analysis_plan/human_agent_collaboration.md`.

---

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
- Drafts for Bob to send (no coefficients in the Hogan note): [`hogan_live_ms_review_request.md`](hogan_live_ms_review_request.md), [`roro_health_methods_request.md`](roro_health_methods_request.md).

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
- HKU report form: pending an accessible copy of the official template plus
  supervisor endorsement; spreadsheet Q/R — Bob.

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
5. **Bob live-file paste:** collaborative draft is ready in `manuscript/live_collaborative/`; paste into Hogan’s shared file only with his permission; do not overwrite weather Methods
6. Jasmine full PDF; Roro revised mortality manuscript diff
7. PI governance confirmation for current aggregate use

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
