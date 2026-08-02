# Slash commands and deck-to-blog drafting — 26 July 2026

**Decision:** The project’s five playbooks are explicit Cursor skills, and progress decks can reliably trigger an offer to draft a Laidlaw blog. Automation stops before publication.

## Command surface

| Command | Action | Invocation |
|---|---|---|
| `/playbook` | Ask which numbered workflow Bob intends | Explicit only |
| `/playbook-01-hogan-lock` | Hogan definition lock | Explicit only |
| `/playbook-02-ha-arrival` | Governed HA receipt and QC | Explicit only |
| `/playbook-03-full-analysis` | Complete real-data analysis panel | Explicit only |
| `/playbook-04-final-writeup` | Final write-up plus CNS-writing | Explicit only |
| `/playbook-99-emergencies` | Source/scope/governance/provenance shock | Explicit only |
| `/laidlaw-blog` | Draft or revise a public Laidlaw post | Explicit only |
| `/blog-from-deck` | Draft from a named progress deck | Explicit or deck-change suggestion |

The playbook skills are thin execution contracts. Each requires the agent to read the canonical file under `analysis_plan/playbooks/`, check its preconditions, follow it exactly, and preserve its human-owned gates and claim boundaries. The skill is not a substitute for meeting evidence, governance approval, delivered data, team Gate 3, or disclosure clearance.

## What “automatic” means for blogs

When a matching progress deck is created or updated, `blog-from-deck` may be offered automatically. When invoked, it:

1. reads the deck and speaker notes when present;
2. extracts the week, real story arc, collaborators, and documented shifts in anticipation;
3. reads the Laidlaw blog canon and style notes;
4. drafts `reports/blog/weekN_<slug>.md` in the MIT Admissions register;
5. updates `reports/blog/README.md`;
6. appends a Ship row to `analysis_plan/context_compound_log.md`; and
7. stops and asks Bob for a creative, privacy, length, and voice pass.

## What remains human-gated

- Bob chooses the personal emphasis and decides whether the first-person voice feels true.
- Bob edits biography, privacy, tone, length, and site formatting.
- Bob alone decides whether and when to post.
- The agent does not silently publish, interact with the Laidlaw website, or claim Bob approved a draft.
- The agent never invents biography, dialogue, feelings attributed to collaborators, data fields, coefficients, or findings.

The blog register is public, warm, and process-centred. It is never the CNS register. Scientific boundaries remain unchanged: plans and synthetic dry-runs are not findings; monthly stroke associations are not daily mortality or daily DLNM results.

## Implementation

Skills live in `.cursor/skills/`; classic dual-support command stubs live in `.cursor/commands/`. The canonical blog rules remain `knowledge/2026-07-26_laidlaw_blog_canon.md` and `reports/blog/STYLE_NOTES.md`.
