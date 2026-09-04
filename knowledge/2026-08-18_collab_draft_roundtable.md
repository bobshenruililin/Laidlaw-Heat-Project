# 18 August 2026 — roundtable on `Heat_CVD_Manuscript_20260815_collab_draft`

**Mode:** Decide. **Not a Gate 3 freeze. Live file not rewritten.**

Bob asked for a caliber-and-strength evaluation of the 15 August collaborative draft, with a roundtable of Kimi K3, Sol 5.6, Fable 5, and Opus 5.

## Who sat

| Seat | Model in this environment | Job |
|---|---|---|
| Fable 5 | Claude Fable 5 (highest thinking) | Senior-scientist identification critique |
| Opus 5 | Claude Opus 5 (highest thinking) | Hogan / CNS-register prose critique |
| Sol 5.6 | GPT-5.6 Sol (highest) | Venue, contribution test, submission readiness |
| Kimi K3 | **Not available** | Skipped. No substitute model was launched. Parent verified contested numerals against frozen tables instead of a new web harvest. The 13 August Kimi harvest already locked HKO/EPD/Guo/Goggins/Liu public numbers. |
| Parent | Grok 4.6 | Adjudicate, score, write the decision |

Canonical text: [`manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`](../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md) (5,963 words). The Word file is the same scientific body plus a paste header and embedded Figures 1–3.

## Decision

The 15 August draft is a **high-caliber specialty manuscript built on a weakly identified ecological series**. Prose is near the best environmental-epidemiology papers. Scientific strength is modest. The paper is the strongest honest article these monthly aggregates can support. It is not a discovery paper, not a CNS-venue paper, and not submission-ready.

**Hogan paste:** ship the 15 August pack. Do not rewrite the weather paragraph. Flag one Conclusion sentence (below) as a human optional rewrite at paste time.

**Journal submission:** not yet. Human blockers and one construction-choice display still sit in front of any editor.

Gate 3 remains open. Stage 3 PDF and A0 poster remain frozen.

## Scores

Calibration used by all seats: 10 = Cell/Nature/Science main text; 8 = best EHP/IJE papers; 6 = competent specialty journal; 4 = student draft.

| Seat | Caliber | Scientific strength |
|---|---:|---:|
| Fable 5 | 8 | 5 |
| Opus 5 | 8 | 6 |
| Sol 5.6 | 6 | 5 |
| **Parent call** | **8 as Hogan-register prose; 6 as a submission object** | **5** |

Sol’s lower caliber score is about submission incompleteness (placeholders, unassembled supplement, collaborator instructions in Methods), not about sentence quality. Fable and Opus judged the sentences. Parent keeps both numbers.

## What the paper is

An exploratory twelve-contrast report of ecological monthly count ratios for first hospitalisation after first CHD or HF diagnosis, with explicit refusals: no multiplicity-protected primary, no daily coefficient, no cohort incidence, no admission-cause claim. The 1.022 / 1.073 pair is a worked example, not a finding.

“Identification article” is useful internally and slightly overbranded externally. The paper shows where monthly variation comes from. It does not identify a thermal effect. Sol’s phrase is the publishable one: **aggregation-aware exploratory case study**.

## What it is not

Not evidence of a thermal effect on cardiac hospitalisation. Not a replication or refutation of Guo et al. or Goggins and Chan. Not a methods paper that generalises the Basagaña–Ballester failure. Not Environmental Health Perspectives / IJE / Lancet Planetary Health / Nature Communications material on present evidence.

## What is genuinely excellent

- Complete twelve-contrast panel with all *q* > 0.19 stated in the Abstract.
- Four-construction ladder that admits Newey–West *narrowed* for CHD hot nights.
- Figure 2: 141 of 145 official cold days in December–February; 29 of 132 months informative.
- Figure 1: first-event decline versus rising C&SD 35+ population, named as depletion rather than falling incidence.
- Failed daily-recovery calibration reported as a refusal, scoped to this series.
- Guo paragraph: official hot-night flag is not the hourly intensity metric.
- Machine claim ledger: `python3 scripts/50_audit_live_claim_ledger.py` passed (154 checks) on this evaluation day.

## Two table-backed holes the 15 August merge left open

These are already in frozen `HA_APPROVED_AGGREGATE` tables. They are not new models. They are not promoted into the live file in this session.

### 1. Table 3 is one-sided (Opus)

Table 3 shows the ladder only for the two “leading” contrasts. Under model-based intervals, HF mean temperature is 0.974 (0.956–0.993) and HF mean minimum temperature is 0.973 (0.956–0.991). HF Tmin still excludes 1 under HC1 and NW3; NW6 is the construction that lets the upper bound reach 1.00005. Source: `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`.

Newey–West lag 6 as the core reporting choice therefore does two jobs at once: it is the construction that excludes 1 for CHD hot nights, and the construction that includes 1 for HF Tmin. The paper already warns that the CHD hot-night exclusion “rests on the smaller robust variance estimate.” It does not show the inverse case. Extending Table 3, or dropping “leading,” is a submission-stage display decision, not a new analysis.

### 2. Pre-2020 continuity is colder than the narration (Fable)

Figure 3 already shows all twelve contrasts across windows. The body narrates only that CHD hot nights become compatible with 1 before 2020 and that HF cold days strengthen. The same `pre_covid` rows (84 months) also give:

| Contrast | Pre-2020 count ratio (approx. 95% CI) |
|---|---|
| CHD mean temperature / 1 °C | 0.980 (0.970–0.990) |
| HF mean temperature / 1 °C | 0.945 (0.927–0.963) |
| HF hot nights / 5 days | 0.965 (0.937–0.994) — sign inverts |
| HF cold days / 5 days | 1.113 (1.053–1.176) — already quoted |

Source: `outputs/tables/cvd_trend_depletion_sensitivity.csv`. This is continuity with the older cold-dominant local literature. Narrating it as one Discussion sentence would strengthen honesty. Promoting it as a new primary would repeat the selection the paper refuses. Human nod required before any live-file change.

## Paste-time flag (do not silent-edit)

Conclusion: “CHD first hospitalisations were more closely associated with hot nights, and HF first hospitalisations with cold days, than with the other thermal encodings examined.”

No formal contrast between encodings or between outcomes is fitted. The Abstract Conclusions line is the correct version. Optional paste-time rewrite: keep the Abstract wording, or state that no test of difference was fitted. Hogan weather paragraph stays verbatim, including “Meteorological data was obtained.”

## Venue (revised)

The 15 August call put Environmental Research first and EHP as reach. This roundtable is stricter.

| Rank | Venue | Parent note now |
|---|---|---|
| 1 (ambitious, after blockers) | Environmental Research | Still the first ambitious target. Major revision likely. Desk rejection is a real risk (endpoint without admission cause; unresolved confounding). |
| 2 (realistic landing) | *International Journal of Biometeorology* | Sol’s cleanest landing. Not in the 15 August list; added here. |
| 3 | *Science of the Total Environment* | Broad fit; reviewers will press exposure and confounder-adjusted core models. |
| — | EHP | Downgraded from “reach” to unlikely. Fable and Opus: reject / desk-reject. |
| — | IJE | Only if recast as a ~3,000-word aggregated-outcome inference paper. Not as the present original-research article. |
| — | Lancet Planetary Health; Nature Communications; Nature / Science / Cell | Not honest. |

## Human vs manuscript holes

Already named and still open: dissemination authority; PI IRB; ICD / inpatient semantics; authorship; cohort risk-set; Hogan weather lock; Roro health-data paragraph; Gate 3 Option A with the team.

Manuscript-internal, not blockers for Hogan paste: Author 2–4 placeholders; “should replace this paragraph”; unused Hogan references [3] and [5] (flag, do not delete his block); Strengths after Conclusion; cited S1 / S7 / S9 not assembled as a submission supplement.

## Residue

Full seat notes: [`manuscript/cns_team/06_roundtable_2026-08-18.md`](../manuscript/cns_team/06_roundtable_2026-08-18.md). Live file, claim ledger, Hogan weather, and Stage 3 PDFs were not changed.
