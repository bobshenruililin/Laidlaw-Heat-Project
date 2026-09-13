# Independent review — August thermal paper, the 10 September rewrite, and the covid_period draft

**Date:** 12 September 2026. **Mode:** review (diagnosis only). **No new findings.** No Hospital Authority
coefficient, row count, or lab field is created here. Gate 3 stays open. Hogan's HKO paragraph is not
rewritten anywhere in this review.

**Objects compared**

| Label | File | Status |
|---|---|---|
| August | [`../archive/thermal_extremes_2026-08/live_collaborative_snapshot/Heat_CVD_Manuscript_live_update.md`](../archive/thermal_extremes_2026-08/live_collaborative_snapshot/Heat_CVD_Manuscript_live_update.md) | Parked heritage; byte-locked |
| 10 September rewrite | [`../live_collaborative/Heat_CVD_Manuscript_live_update.md`](../live_collaborative/Heat_CVD_Manuscript_live_update.md) | Hogan paste target; not edited by this review |
| covid_period draft | [`Manuscript_covid_period_draft.md`](Manuscript_covid_period_draft.md) | Development authority; repaired in this branch |

The three files share one licensed extract: 132 territory-months of first CHD and first HF hospitalisation
counts among people with type 2 diabetes and/or hypertension, January 2013 to December 2023, with admission
cause absent and stroke undelivered.

## 1. August was one paper

The parked thermal article asks a single question and answers it in a spine a stranger can follow:
Outcome series → Exposure context → Model 1 → Uncertainty ladder → Joint models and residual diagnostics →
Sensitivity analyses. The title, the Abstract, and the last Introduction paragraph name the same object.
The Discussion reads the tables it printed: twelve *q*-values above 0.19, a four-construction standard-error
ladder, and the analysis window carried as a sensitivity rather than as a headline.

August is the structural template for the repair. It is not a numerical template: its numerals are the same
parked Model 1 estimates, and the repair does not move them.

## 2. The 10 September change was a glue job, not Hogan's request

Hogan asked for a different angle: read the window contrast as the primary object and use thermal extremes to
argue that weather is not why the period difference appears. The Playbook 99 record of that decision
([`../../reports/incident_2026-09-10_scientific_angle_covid.md`](../../reports/incident_2026-09-10_scientific_angle_covid.md))
says to park thermal, open `manuscript/covid_period/`, and **not** rewrite `manuscript/live_collaborative/` in
place. The live folder was then rewritten in place anyway. Two consequences follow, and both are structural
rather than scientific.

**Two authorities.** `live_collaborative/` and `covid_period/` now both claim to be the current wording. The
covid_period README even describes itself as the predecessor of the live rewrite, which inverts the Playbook 99
instruction.

**One confused article.** The live file carries a window-dependence title and Abstract on top of August thermal
Methods, a Results order that leads with the count collapse and then leaves the thermal panel behind as a
residue, and a Discussion that argues utilisation, depletion, and weather entanglement as an essay rather than
as a reading of its own Table 2. A reader cannot tell which of the two objects is the paper.

## 3. The covid_period draft is the better scientific start

The development draft already states the licensed objects more cleanly than the live file: the first-event count
path, and the official-day count ratio shown for the full window and for the nested 84-month specification as a
ruling-out exhibit. It keeps the refusals that matter — no physiological improvement, nested windows are not a
pre/post effect, no post-only 48-month Model 1 table, `I(count/5)` as a reporting scale.

It was still not an August-quality paper before this branch. Three defects:

- The official-day section was headed "Period-split official-day panel", which invites the pre/post reading the
  design does not license.
- Results ran to seven sections, with continuous temperature and joint models presented at the same level as
  the two headline objects.
- The Discussion continued past the three labelled rivals into sleep physiology, cold-afterload physiology, and
  a heat–health-action-plan mapping that the monthly counts cannot address.

## 4. References are a thermal list with COVID papers taped on

Measured across the three files (in-text `[n]` markers against the numbered reference list):

| File | Entries listed | Distinct entries cited | Uncited entries | Numbered in order of appearance |
|---|---:|---:|---|---|
| August | 33 | 31 | 3, 5 | No (first appearances run 9, 2, 4, 6, 1, 11, 21, 17, …) |
| 10 September rewrite | 42 | 21 | 2–6, 9, 11–13, 18, 23–33 | No (body opens at [34]–[39], then jumps back to [1], [21], [17]) |
| covid_period draft (before repair) | 39 | 28 | 3, 5, 9, 11, 18, 23–26, 29, 32 | No (body opens at [34]–[39]) |

The pattern is append-only editing: the COVID papers were added as [34]–[42] instead of being renumbered into
the sequence, and the August physiology, sleep, stroke, and heat–health-action-plan entries were left in the
list after the paragraphs that cited them were cut. No entry is a fabricated citation; every uncited entry is a
real paper that the current body no longer reads.

## 5. Blank pages are the builder, not Word

[`../../scripts/77_hogan_20260910_live_docx.py`](../../scripts/77_hogan_20260910_live_docx.py) forces
`doc.add_page_break()` after every table and after every figure, sets `page_break_before` on any caption that is
not already at the top of a page, and sets `page_break_before` on the Introduction, Results, Discussion,
Strengths, and References headings. In August that print craft cost little because the article was shorter and
the floats were larger relative to the prose. In the longer rewrite it strands most of the Results.

Measured fill of the text column (lowest text-block baseline divided by page height) in the built PDFs:

| PDF | Pages | Pages at ≤ 0.30 fill | Worst pages |
|---|---:|---:|---|
| `Heat_CVD_Manuscript_20260910_hogan.pdf` | 21 | 12 | p8 0.15, p10 0.15, p11 0.10, p14 0.19 |
| `Heat_CVD_Manuscript_20260824_hogan.pdf` (August) | 22 | 4 | p7 0.21, p13 0.20, p12 0.24, p9 0.29 |

Pages 5 to 17 of the live PDF are the Results, and eleven of those thirteen pages are less than a third full.
That is a layout contract, not a scientific problem, and it is fixable without touching a numeral.

## 6. What this review does not conclude

- It does not rank the two candidate angles. Whether the window contrast replaces thermal extremes as the
  journal primary is Bishai's decision.
- It does not read Hogan's "improved" for him. Whether he meant point-estimate attenuation, the count
  trajectory, or physiology is still a human question.
- It does not freeze Gate 3, promote any *q* > 0.19 estimate, or claim that health improved.
- It does not compare caliber scores. The ceiling note
  ([`../../knowledge/2026-09-10_highest_reachable_live_paper.md`](../../knowledge/2026-09-10_highest_reachable_live_paper.md))
  already records that scientific strength cannot be raised by prose.

## 7. Repair carried out in this branch

Scope is `manuscript/covid_period/` plus new scripts. `live_collaborative/` and
`archive/thermal_extremes_2026-08/` are untouched.

1. One question in the title, Abstract, and last Introduction paragraph: the first-event count path, and
   nested-window official-day count ratios as a ruling-out exhibit.
2. Results restored to five scannable sections in August order, with continuous temperature, joint models, and
   diagnostics demoted into one checks section.
3. Discussion stops after utilisation, depletion, and weather entanglement, with one refusal sentence for
   physiology and heat–health action plans.
4. References renumbered in Vancouver order of appearance, with the uncited August leftovers dropped from the
   main list and the Methods citations kept.
5. A covid_period print builder ([`../../scripts/78_covid_period_manuscript_docx.py`](../../scripts/78_covid_period_manuscript_docx.py))
   that places a float on its own page only when it will not fit, and a recorded page map.
6. Rails checks ([`../../scripts/79_covid_period_rails_checks.py`](../../scripts/79_covid_period_rails_checks.py)):
   claim-ledger numerals, citation order, Hogan weather verbatim, forbidden phrases, and page-map fill.

No numeral changed. The parked Model 1 estimates in [`claim_ledger.yml`](claim_ledger.yml) are quoted as they
already stood.

## 8. Hostile-read pass (13 September 2026)

The 12 September rebuild was one IMRD, not the 10 September glue job. It still carried thermal-paper residue that a hostile read would mark FIX. This pass applied those FIXes. Numerals were not moved. No governed field was invented.

Applied:

- Abstract Methods now names the nested 84 ⊂ 132 official-day ratios as the ruling-out exhibit, not as an afterthought to a thermal primary.
- Newey–West lag-6 is a display convention matching the parked tables. It is not called the main reported interval. Table 5 is the Model / HC1 / NW3 / NW6 ladder.
- Table 3 is the encoding contrast (mean temperature versus official days in both windows), inside the nested-window section. Table 4 is the twelve-fit thermal exhibit. The sixth Results heading is gone.
- "Nine of the twelve" significance-count is cut. Inverse nested-window continuous-temperature fits remain.
- Daily-recovery Type I error numbers are cut from Results. Methods still records that the method was not applied to the hospital counts.
- Discussion stops after the three rivals plus one refusal for daily neighbours, Liu mortality, physiology, and heat–health action plans. It does not point at a missing supplement. Influenza and pollution moved to limitations.
- Strengths and limitations precede Conclusion.

Human-owned leftovers: IRB `UW XX-XXX`; Author 2–4; Acknowledgements `None.`; still-at-risk person-time; stroke file; whether this angle replaces the parked thermal paper. Gate 3 stays open.
