---
name: blog-from-deck
description: Offer and prepare a Bob-reviewed Laidlaw blog draft when a progress deck changes or Bob asks for a blog from a deck.
disable-model-invocation: false
paths:
  - "reports/latex/week*_*.tex"
  - "reports/latex/**/Week*_*.tex"
  - "reports/**/Week*_Progress_Deck.*"
  - "reports/hogan_tuesday/**"
---

# Blog from a progress deck

## Triggers

- A matching progress deck is created or updated.
- `/blog-from-deck`
- “Blog from this deck.”

For a path-triggered change, offer this workflow when appropriate; do not silently publish or claim that Bob has approved the draft.

## Preconditions

- [ ] The source deck and week identity can be located.
- [ ] Deck content and speaker notes, when present, have been read.
- [ ] Scientific provenance is distinguishable from plans, published context, and findings.

## Execution

1. Read [`knowledge/2026-07-26_laidlaw_blog_canon.md`](../../../knowledge/2026-07-26_laidlaw_blog_canon.md) and [`reports/blog/STYLE_NOTES.md`](../../../reports/blog/STYLE_NOTES.md).
2. Extract the week identity, story arc, collaborators, and shifts in anticipation from the deck and speaker notes. Do not infer private feelings or dialogue.
3. Choose a concise slug and draft `reports/blog/weekN_<slug>.md` in Bob’s first person and the MIT Admissions register. Never use CNS voice.
4. Separate project plans, published context, environmental descriptives, and verified project findings.
5. Add the draft to `reports/blog/README.md`.
6. Append one dated Ship row to `analysis_plan/context_compound_log.md`, naming the deck and draft.
7. Stop before publication. Ask Bob for a creative, privacy, length, and voice pass.

## Done when

- The deck’s real arc and collaborator roles are recognisable.
- No biography, findings, data fields, dialogue, or emotions are invented.
- Draft, index, and compound-log row agree on week and source.
- The status is ready for Bob’s edit, not published.

## Files to update

- `reports/blog/weekN_<slug>.md`
- `reports/blog/README.md`
- `analysis_plan/context_compound_log.md`
