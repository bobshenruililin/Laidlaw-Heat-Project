# Project state & living context — Laidlaw Heat Project

**Last updated:** 2026-07-23  
**Purpose:** One place for humans and future agents to recover *what is true now* — science, people, tone, and open wounds — so context compounds.

Start here after `README.md`. Machine rules: `AGENTS.md`. Collaboration habits: `analysis_plan/human_agent_collaboration.md`. Detours: `analysis_plan/context_compound_log.md`.

---

## 1. People and roles

| Person | Role | Email / handle (as used) | Current relationship note |
|---|---|---|---|
| **Bob Shen Ruililin** | Laidlaw Scholar; analysis lead | `shenrll@connect.hku.hk` | Must rebuild trust after unilateral HKO work |
| **Prof. David Bishai** | Supervisor / PI | `dbishai@hku.hk` | Emphasized teamwork (Jul 2026): *go far together*; listening earns trust |
| **Hogan** | Environment / weather co-author track | `hkfwai@connect.hku.hk` | Felt sidelined; still offers methods + manuscript advice |
| **Roro (Zhenyuan Liu)** | HA / aggregates / secure access | `roroliu@hku.hk` | Stroke aggregates pending; Hogan wrote *her* about hot-month defs |

Original Bishai plan (Dec 2025): Step 1 Bob lit review → Step 2 Roro Y file → **Step 3 Hogan prepares monthly X climate file** → Step 4 secure server → Step 5 Bob models.

---

## 2. Scientific state (facts, not findings)

### Estimand (post–17 July 2026 lab meeting)
- Ecological **monthly** associations, Jan 2013–Dec 2023 (`N = 132`).
- Outcome: **stroke admission aggregates** (grain TBD when file arrives).
- **Not** from general HA file: AMI / principal-dx CVD (no reasons for admission).
- Complementary to lab **daily heatwave–mortality** work (Liu/Ren/Bishai) — different estimand.
- Strategy: labelled multi-pathway panel (~10+); headline freeze at Gate 3 (proposal **P02 + P04**).

### Public layers — REAL
- HKO Headquarters climate + extremes + Ren/Wang spell / 2D3N constructs.
- Lag-1 temperature (Dec 2012 joined); HW-month p90/p95/p975; daily diurnal-range TV.
- C&SD age–sex denominators (Table 110-01001).
- EPD EPIC general-station NO₂, O₃, PM₂.₅, PM₁₀ (placeholder removed). Early→late: NO₂/PM down; O₃ up ~+32%.
- CHP Flu Express monthly positivity for P14 (**121/132** months; early-2013 gap).

### Pipeline — READY (plumbing)
- `PATHWAY_MODE=dev|real` via `scripts/run_pathway_pipeline.R`.
- Pathways P01–P18; P13 disabled until subtype; dry-run **17 OK** on **SYNTHETIC** stroke only.
- SAP, schema, diagnostics, forest, manuscript table shells exist.
- **No real outcome coefficients. Synthetic ≠ findings.**

### Still pending (human-owned)
- Stroke aggregate CSV + dictionary + governance path.
- Gate 3 headline freeze after real descriptives.
- **Hogan alignment** on heatwave / “hot month” operationalisation (see §3).

---

## 3. Team dynamics — July 2026 (specific)

### What went wrong (shared reading)
1. Jan 2026: long email thread on novelty vs Goggins; Hogan agreed points, suggested 65–69 / 70–74, offered to prepare climate file; Bob said he was keen to proceed *using files Hogan offered*.
2. Then Bob went quiet (travel / return disruption; also communication failure).
3. Bob built HKO files himself without discussing with Hogan.
4. Hogan interpreted that as “Bob works alone,” and **held back on purpose**.
5. Hogan later emailed **Roro** (not Bob) offering co-author advice and a hot-month recipe (heatwave definition → count per month → top 90/95% months or count threshold; cited Atmos. Res. 2024 `10.1016/j.atmosres.2024.107845`).
6. Bishai emailed Bob on **Teamwork**: geography may have hindered relations; *if you want to go fast go alone, to go far go together*; listening earns trust.

### Repair posture (agreed drafting line)
- Sincere apology to Hogan; do not inventory the repo at him.
- Invite concrete co-author lead on weather definitions / hot-month / environmental interpretation.
- Reply to Bishai acknowledging travel **and** owning silence + unilateral HKO step; commit to go farther with the team.
- Emails should sound human, short, not “AI brief.”

### Implication for Week 2 *sharing*
Do **not** frame Week 2 as solo triumph (“manuscript-ready; wait only for the file”).  
Do frame: meeting recalibrated science; public layers advanced; **weather definitions remain open for Hogan**; outcomes need Roro; teamwork is part of the work product.

---

## 4. Stylistic preferences (Bob) — also for presentations

- **Title / first slide:** only title + Bob’s identity (name, programme, lab, date). No taglines, no READY/PENDING strips, no status clusters.
- Progress decks after interpersonal events should emphasize **shared judgment**, not solo readiness as triumph.
- Prefer storytelling + talking points over dashboard clutter.
- Emails: sincere, short, human; apology without repo inventory; no synthetic “results.”
- Compound context in-repo after meetings **and** interpersonal events.

---

## 5. Key file map

| Need | Path |
|---|---|
| Orientation | `README.md` |
| Agent protocol | `AGENTS.md` |
| This living state | `analysis_plan/PROJECT_STATE.md` (this file) |
| Human–agent habits | `analysis_plan/human_agent_collaboration.md` |
| Detours log | `analysis_plan/context_compound_log.md` |
| Meeting recalibration | `reports/meeting_debrief_2026-07-17.md` |
| Pathways | `analysis_plan/pathway_catalogue.md`, `pathway_registry.yml` |
| SAP | `analysis_plan/statistical_analysis_protocol.md` |
| Week 2 deck / brief | `reports/Week2_Progress_Deck.pdf`, `Week2_Progress_Brief.pdf` |
| Lit → pathways | `literature/pathway_evidence_memo.md` |

---

## 6. Open decisions (owners)

| Decision | Default | Owner |
|---|---|---|
| Stroke file + dictionary | Schema min: `month_id`, `n_events` | Roro / Bob |
| Grain | Prefer age×sex if present | On inspection |
| Subtype IS/HS | Enable P13 only if present | On inspection |
| Hot-month / heatwave ops | Include Hogan Atmos.Res.–style count→percentile as named pathway candidate | Hogan + Bob |
| Headline pair | Proposal P02 + P04 | Team @ Gate 3 |
| Governance | PI path | Bishai |

---

## 7. Agent briefing seed (copy)

```text
Read README.md, AGENTS.md, analysis_plan/PROJECT_STATE.md, latest meeting debrief.
Science: monthly stroke aggregates; no AMI from general HA; synthetic ≠ findings.
People: repair/maintain Hogan trust; weather defs not closed without him; Roro owns aggregates.
Bob style: spare title slides; sincere short emails; write durable context after interpersonal events.
```
