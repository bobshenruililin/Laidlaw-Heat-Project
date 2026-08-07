# Project state & living context — Laidlaw Heat Project

**Last updated:** 2026-08-07
**Purpose:** Recover what is true now — science, people, tone, meeting notes — so context compounds.

Also read: `README.md`, `AGENTS.md`, `analysis_plan/human_agent_collaboration.md`.

---

## 1. People and roles

| Person | Contribution | Note |
|---|---|---|
| **Hogan** | Weather / heat framing; Goggins challenge; 65–69 & 70–74; climate X file; hot-month (heatwave counts → upper-tail months); Atmos Res pointer; **author of the live manuscript’s weather Methods and reviewer of its Introduction**; academic-writing guidance | His live weather section is primary; credit openly; do not overwrite it with repository prose |
| **Roro (Zhenyuan Liu)** | HA stroke aggregates; timing rule; dictionary; transfer; **health-data Methods due 7 Aug**; **excess heat-mortality baseline** (medRxiv 2026; uses Jasmine RRs); proposed to guide Bob’s regression work | Cleaned monthly stroke data due 7 Aug; first GOPC stroke mention = marker; true event earlier; ignore later mentions; revised Mac PDF still pending ingest |
| **Prof. David Bishai** | Dec 2025 plan; multi-method; teamwork (“go far together”); Jasmine null-pattern / extend-to-2023; ~10°C discussion prompt; concept lead on Roro excess-mortality paper | Jasmine identity resolved (Jingwen Liu 2020 SCS) |
| **Bob Shen** | Analysis plumbing, pollution assembly, writing; Introduction revisions and non-weather Methods due 5 Aug | Work directly in the live manuscript; preserve Hogan’s weather section and Roro’s health-data ownership |

---

## 2. Outcome semantics (working understanding)

- General HA file: **no admission reasons** → AMI out of scope from that file.
- Stroke aggregates: use **first GOPC mention of stroke as a marker**; hospitalisation/actual stroke generally **precedes** that mention; **do not use second mentions** for incident identification; recover true event month for aggregation.
- Confirm field-level algorithm with Roro before locking methods text.

---

## 3. Scientific state

- Estimand: monthly thermal exposures × stroke aggregates, 2013–2023.
- Public layers ready: HKO climate/extremes/spells, EPD pollution, C&SD denominators, CHP flu (121/132).
- Pathway panel P01–P18 (P13 off until subtype); headline proposal P02+P04 after Gate 3 **with team**.
- **Hot/cold month catalogue:** HM01–HM50 / CM01–CM48 + pathways H01–H12 / C01–C12 (`analysis_plan/hot_cold_month_catalogue.md`; starters in `hot_cold_month_registry.yml`; next-week sheet `hot_cold_next_week_runsheet.md`).
- **Jasmine is confirmed:** Jingwen Liu et al. (2020), *Sustainable Cities and Society* 57:102131, DOI `10.1016/j.scs.2020.102131`; Hong Kong daily mortality 2006–2016; DLNM + quasi-Poisson; reversed J; cold AF 4.72% vs heat AF 0.16%; moderate AF 4.25% vs extreme AF 0.63%. Full PDF/supplement extraction remains pending (`literature/jasmine_liu2020_confirmed.md`; protocol in `jasmine_extension_protocol.md`).
- **Roro medRxiv baseline:** Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika and David Bishai, DOI `10.64898/2026.03.05.26347683`; model-based multi-definition heatwave excess mortality, 2014–2023. It uses RRs from Jasmine and Wang/Ren. MedRxiv v1 deep-read is in `literature/roro_manuscript_deep_read.md`; the Mac `revised manuscript_clean.pdf` has not yet been ingested.
- **Family science baseline:** Jasmine daily mortality AF/RR → Roro absolute heat excess-death scenarios → our monthly stroke morbidity panel. These are complementary estimands (`literature/jasmine_roro_family_map.md`; `literature/exceed_jasmine_and_roro_baseline.md`).
- **Gene/~10°C:** discussion hypothesis only, not a biological threshold or result.
- **No stroke coefficients.** Synthetic ≠ findings.

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

### Friday 7 August — HA CHD/HF arrival and full panel

- Roro delivered monthly CHD and HF first-hospitalisation counts (T2D/HTN cohort; first hosp after first CVD diagnosis; Dr Zhou assisted). Stroke mentioned in email but **not attached**.
- Playbooks 02–03 executed for CHD+HF: QC, merge, P01–P18, provisional HM/CM, descriptives, offset/period sensitivities, forests.
- Gate 1 conditional / Gate 2 closed for CHD+HF; Gate 3 packet ready but **open**.
- Temperature share for Roro: `outputs/share_for_roro/`.
- Results write-up: `reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md` (panel report; not a solo headline claim).
- HA month-level counts remain gitignored under `data_raw/ha_secure_placeholder/` and `data_processed/*_aggregates_normalized.csv` / `*_analysis_panel.csv`.

### Sunday 2 August — live manuscript handoff

- Hogan created and shared a live manuscript with Bob and Roro, commented on the Introduction, and wrote the weather component of Methods.
- The shared file is now the manuscript authority. Work in it directly; stop exchanging parallel manuscript versions.
- Bob owns the Introduction response and the remainder of Methods by **5 August**. He should adapt the canonical essay for design, pollution, population denominators, statistical analysis and thermal-panel discipline, without replacing Hogan’s weather text.
- Roro owns cleaned monthly stroke data and the health-data Methods by **7 August**. Bob’s outcome text is only a brief bridge using the already agreed GOPC-marker principle.
- Hogan will review each contribution after completion. His specific Introduction comments are not in this repository and must not be invented.
- Working set: [`hogan_live_manuscript_handoff.md`](hogan_live_manuscript_handoff.md), [`methods_remainder_bob_aug5.md`](../manuscript/methods_remainder_bob_aug5.md), [`introduction_revision_notes.md`](../manuscript/introduction_revision_notes.md), and [`2026-08-02_hogan_live_manuscript.md`](../knowledge/2026-08-02_hogan_live_manuscript.md).

---

## 5. Laidlaw Stage 3

- Essay 2000–3000 words — canonical publication-register literature-and-methods essay: `reports/laidlaw_stage3/essay_lit_methods.md` + `reports/laidlaw_stage3/Essay_Lit_Methods.pdf` (no stroke results claimed).
- Pathway map: `reports/laidlaw_stage3/pathway_literature_map.md`.
- Poster: A0 **portrait** 841×1189 mm (GEST landscape is wrong orientation + stale AMI aim).
- HKU report form + supervisor endorsement; spreadsheet Q/R — Bob.

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
5. **Bob live-file sync:** fold CHD/HF estimand + Methods into Hogan’s live manuscript without overwriting weather Methods
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
