# Hogan live-manuscript handoff

**Date:** 2 August 2026  
**Question:** Can the current Introduction and Methods in `reports/laidlaw_stage3/essay_lit_methods.md` be used?

## Reusable answer

| Component | YES / NO | Governing source now | Bob’s action |
|---|---|---|---|
| Introduction | **YES, as a substrate** | The live manuscript and Hogan’s comments | Edit the live text against every comment. Reuse the essay’s scientific spine, not its wording by default. |
| Weather Methods from the essay | **NO, not as manuscript text** | Hogan’s weather Methods in the live manuscript | Do not overwrite or silently reconcile Hogan’s section. Use the essay only to check consistency, omissions and cross-references. |
| Remaining Methods due 5 August | **YES, adapt from the essay** | Live manuscript structure, with the essay as source material | Draft Study design, Pollution, Population denominators, Statistical analysis, and the panel discipline for hot/cold months. Coordinate the thermal-month cross-reference with Hogan’s weather section. |
| Detailed health-outcome Methods | **NO, not for Bob to pre-empt** | Roro’s governed data and Methods contribution | Add only a short handoff paragraph containing the already agreed marker principle. Do not infer fields, counts, strata, suppression rules or timing details. |

The authority order is now: **live manuscript and visible comments → explicit team decisions → repository essay**. The essay is a strong source document, but it is no longer a parallel manuscript.

## Introduction strategy

Use the essay Introduction because it already contains the right scientific sequence: clinical importance, Hong Kong setting, the monthly estimand, definition uncertainty, and cold–heat balance. Rebuild that sequence in the live file around Hogan’s comments.

Hogan’s actual comments are not available in this repository. The following are therefore **likely review categories, not reconstructions of what he wrote**:

| Likely comment type | Risk in the current framing | Revision response |
|---|---|---|
| Estimand clarity | “Temperature and stroke” can sound like a daily triggering or causal study. | State early that the estimand is the association between monthly thermal burden and monthly stroke-event aggregates during 2013–2023. Distinguish it from daily lag effects, mortality attributable fractions and excess-death modelling. |
| Cold/heat symmetry | Climate-warming language can make cold appear obsolete; strict rhetorical symmetry can imply equal effects before analysis. | Motivate parallel, pre-specified assessment of heat and cold without asserting equal magnitude or importance. Retain the local evidence that cold remains relevant. |
| Novelty relative to Goggins | A broad novelty claim could erase earlier Hong Kong stroke–weather work. | Credit Goggins et al. directly. Define the contribution as a later period, a monthly governed stroke-event estimand, and a definition-robust thermal panel—not the first Hong Kong study and not a replacement for daily models. |
| Length | Literature detail can obscure the question. | Keep only evidence that changes the design. Move thresholds, event operators, lag mechanics and pollutant-processing details to Methods. Aim for approximately 600–800 words unless the live manuscript has a stricter limit. |
| Jargon | “Estimand”, “DLNM”, “event morphology”, “panel”, and internal labels can slow the reader. | Use plain language first; retain a technical term only when it adds precision. Remove internal pathway codes, Gate language and collaborator-process notes from manuscript prose. |

### Revision checklist before the comments are available in-repo

- [ ] Work directly in the shared file; do not create an offline competing manuscript.
- [ ] Read every Hogan comment before revising individual sentences so local edits do not conflict with his larger argument.
- [ ] Open with the scientific problem, then reach the monthly stroke estimand within the first three paragraphs.
- [ ] Define the unit of analysis, period and target association once.
- [ ] Keep heat and cold in parallel without predicting which will dominate.
- [ ] Credit Goggins et al. as the local stroke foundation and state the difference in time scale and estimand.
- [ ] Present exposure-definition uncertainty as a design problem, not a search for the largest coefficient.
- [ ] Keep mortality attributable fractions and modelled excess deaths out of the stroke claim.
- [ ] Remove thresholds and operational weather rules that belong in Hogan’s Methods.
- [ ] Replace ornate or abstract phrases with short, concrete sentences.
- [ ] Check that every novelty sentence names a precise difference rather than claiming priority.
- [ ] Reply to each live comment with the edit or a concise rationale; do not invent the reviewer’s intent.
- [ ] Re-read the revised Introduction beside Hogan’s weather Methods so terminology and section promises match.

## Methods division for 5 August

Bob should paste and adapt `manuscript/methods_remainder_bob_aug5.md` in the live file, following its existing headings and house style.

1. **Study design:** monthly ecological time series, January 2013–December 2023, with the rate-ratio estimand and conditional interpretation.
2. **Pollution:** EPD EPIC general-station series, completeness rule, monthly aggregation and staged adjustment.
3. **Population denominators:** C&SD source, monthly interpolation and the population-by-days offset.
4. **Statistical analysis:** count-model family, season and trend controls, diagnostics, complete panel reporting and planned contrasts.
5. **Hot/cold months:** explain pre-specification and parallel panel discipline, while pointing operational heatwave and weather rules to Hogan’s section.
6. **Outcome bridge:** leave Roro’s health-data section intact. Include only the team-agreed GOPC-marker principle, explicitly attributed to the outcome co-investigator.

The essay’s weather prose may be used as a private consistency checklist: Are daily measures mapped to months? Are cross-month events handled? Are absolute, relative, spell and combined day–night measures kept conceptually distinct? Any discrepancy should become a live-file question to Hogan, not an unannounced replacement.

> **Thinking box**
>
> - **One manuscript:** edit the shared file, use comments or suggestions for contested changes, and avoid email attachments or local forks as alternative authorities.
> - **Visible ownership:** Hogan leads weather Methods; Roro leads governed outcome construction and health-data Methods; Bob owns the remaining Methods draft due 5 August. Cross-references should connect these sections without absorbing another person’s contribution.
> - **CNS register remains the standard:** short sentences, explicit estimands, no process language, no inflated novelty and no claims beyond the data.
> - **When Roro’s cleaned monthly stroke data arrive on 7 August:** verify schema, month coverage, aggregation, timing, suppression and denominator compatibility before changing the statistical text. Roro’s health-data Methods should replace or expand the brief outcome bridge. Data arrival does not itself create a result.
> - **Gate 3 remains a team decision:** drafting candidate primary and sensitivity models does not freeze the headline specification. The team still closes that choice after governed-data QC and appropriate descriptives.

## Further thinking (2 August)

The live file is not only a logistics upgrade. It changes authorship dynamics. Hogan is no longer commenting on a solo draft after the fact; he has written the weather Methods as a co-author and set the Introduction’s review frame. The repository essay remains valuable because it already solved the hard conceptual problems—monthly estimand, cold–heat symmetry without premature claims, definition multiplicity as design rather than fishing, pollution staging, and the Jasmine/Roro mortality baselines as complementary rather than interchangeable. Those ideas can travel into the live manuscript. The prose often should not: Hogan’s comments will prefer his rhythm and the journal’s house style.

The Aug 5 deadline for Bob’s Methods remainder is realistic if the weather section is left alone. The risky path is “reconciling” Hogan’s weather text with our catalogue IDs (HM23, P02) inside the manuscript. Catalogue IDs belong in the registry; the manuscript should speak in scientific English. Cross-reference Hogan’s section for operators; keep panel discipline in Bob’s statistical text.

When Roro’s cleaned monthly stroke file arrives on 7 August, the temptation will be to run everything immediately. The better sequence is still Playbook 02 (QC → schema → merge → real mode), then Playbook 03. Writing Methods before data is not a problem if the Outcome section stays a governed handoff. Writing Results before QC is.

One more anticipation shift: earlier the project waited for definitions; now definitions are being written into a manuscript while health data are still inbound. That is mature only if every Methods sentence remains procedure, not prediction.
