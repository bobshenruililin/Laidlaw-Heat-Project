# Agent collaboration protocol — Laidlaw Heat Project

This file is for **future agents** (and for Bob when briefing them).  
It encodes how this project compounds: scientific honesty, durable context, and permission to explore without turning exploration into fake findings.

Humans: start at [`README.md`](README.md). Living state (science + people + tone): [`analysis_plan/PROJECT_STATE.md`](analysis_plan/PROJECT_STATE.md). Assumptions: [`analysis_plan/assumption_ledger.md`](analysis_plan/assumption_ledger.md).

---

## 1. What success looks like here

Not maximal commits. **Compound readiness**: each session leaves the next session smarter.

A good session ends with at least one of:

1. a decision written down (ledger / gates / meeting note),
2. a reproducible artifact (script, table, figure, schema),
3. a dead end marked as dead (so nobody re-walks it),
4. an open question that is sharper than before.

A bad session: impressive prose that vanishes when the chat ends, or synthetic coefficients dressed up as results.

---

## 2. Non-negotiable scientific rules

- Label provenance: `REAL`, `SYNTHETIC`, `HA_APPROVED_AGGREGATE`, placeholders.
- Never invent HA row counts, field meanings, or coefficients for undelivered files.
- Monthly stroke-aggregate burden ≠ daily DLNM ≠ heatwave excess-death mortality.
- No AMI / principal-dx claims from general HA without admission reasons.
- Never commit HA microdata.
- Panel reporting (pathway IDs), not ten independent “discoveries.”
- Gate 3 headline freeze before primary manuscript claims.

---

## 3. Context is the product (not only the code)

Cursor chat memory helps **one** run. The repo helps **every** run.

Prefer writing into:

| Kind of knowledge | Where it should live |
|---|---|
| What the project is now | `README.md` (short) |
| Working assumptions | `analysis_plan/assumption_ledger.md` |
| Decision gates | `analysis_plan/decision_gates.md` |
| Pathway definitions | `analysis_plan/pathway_catalogue.md` + `pathway_registry.yml` |
| Meeting substance | `reports/meeting_debrief_YYYY-MM-DD.md` |
| Lit → method map | `literature/pathway_evidence_memo.md` |
| How Bob + agents work | **this file** + `analysis_plan/human_agent_collaboration.md` |
| Open questions / rabbit holes | `analysis_plan/context_compound_log.md` |

If you learned something important in chat and did not write it down, the project did not keep it.

---

## 4. Lab meetings are context engines

Treat meetings as **inputs to the ledger**, not only as slides for the room.

After any lab / supervisor meeting, an agent (or Bob) should leave:

1. **What changed** (table: before → after),
2. **What is now out of scope**,
3. **What became newly allowed** (e.g. multi-method panel),
4. **Open questions owned by humans** (data, governance, definitions),
5. **Next executable step** that does not invent missing data.

Template precedent: `reports/meeting_debrief_2026-07-17.md`.

---

## 5. Productive wandering is allowed

Human scientists stray. So may agents — **inside a named mode**.

| Mode | Intent | Must leave behind |
|---|---|---|
| **Ship** | Produce a named artifact | The artifact + short note of limits |
| **Explore** | Follow a curiosity / side path | Entry in `context_compound_log.md` (insight or dead end) |
| **Teach** | Explain for Bob’s growth | Short explanation in-repo or in the reply; no fake certainty |
| **Decide** | Force a fork to close | Ledger / gate update |

Exploration without a write-back is tourism. Exploration with a write-back is research.

Do **not** confuse wandering with claiming. A new pathway idea is a registry draft; a coefficient on synthetic data is never a finding.

---

## 6. What Bob can do that agents cannot

Agents cannot replace:

- PI / governance decisions,
- HA data transfer and dictionary truth,
- taste about what the Laidlaw Scholar wants to become known for,
- relationships in the lab (Roro, Hogan, Chao Ren line, etc.).

The highest-leverage human moves are listed in `analysis_plan/human_agent_collaboration.md`.

---

## 7. Default operating posture for agents on this repo

1. Read README + this file + latest meeting debrief before large work.
2. Prefer extending the pathway panel / ledger over inventing parallel pipelines.
3. When blocked on HA data, improve readiness (QC, schema, lit map, figures) — do not invent outcomes.
4. When Bob asks for “highest quality” without a done-definition, propose one in the first reply and proceed.
5. When something surprising appears while exploring, log it; only promote it to a pathway/SAP after a human nod or an explicit Explore-mode brief.

---

## 8. Anti-patterns

- Rebuilding Week-1 AMI framing after the 17 July recalibration.
- Treating synthetic dry-runs as manuscript results.
- Ten methods as ten press releases.
- Long memos that duplicate the README.
- Asking Bob to re-paste context that already lives in `reports/` or `analysis_plan/`.
