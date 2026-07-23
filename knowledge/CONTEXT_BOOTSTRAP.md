# Context bootstrap — read first in every new chat

**Canon date:** 23 July 2026. Read [`PROJECT_STATE.md`](../analysis_plan/PROJECT_STATE.md) for living detail and update this file whenever a human gate changes.

## Scientific contract

This is Bob Shen Ruililin’s Laidlaw Hong Kong thermal–stroke project. The estimand is the ecological association between **monthly thermal exposures** and **governed monthly stroke-event aggregates** during January 2013–December 2023 (132 months), expressed as rate ratios from count models with a `population × days_in_month` offset and specified season/trend controls. Daily HKO observations create monthly means, official extreme-day counts, spells, combined day–night events, and lag-one-month exposures. This is not individual causality, a daily DLNM trigger analysis, a mortality attributable fraction, or an excess-death model.

No real stroke coefficients exist yet. Synthetic runs test plumbing only. Never invent HA rows, fields, subtype availability, suppression rules, event timing, or findings. The general HA file lacks admission reasons, so AMI/principal-diagnosis claims are out of scope. The planned stroke rule uses the first GOPC mention as a marker for an earlier event and reconstructs the true event month; Roro must still provide the field-level algorithm. Only approved aggregates may leave governance.

## People and ownership

- **Hogan:** weather/climate co-investigator; Goggins framing; Li-HW count-by-month → upper-tail adaptation; age 65–69/70–74 visibility proposal; academic-writing mentorship. Lock weather definitions with him and credit the project adaptation.
- **Zhenyuan Liu (“Roro”):** governed HA stroke aggregates, dictionary, true-event-month construction, suppression/transfer truth, and regression mentorship.
- **Professor David Bishai:** supervisor, concept/multi-method direction, PI/governance decisions, and team Gate 3.
- **Bob:** reproducible exposure/analysis preparation, pollution/flu integration, writing, and durable decision records.
- **Jingwen Liu (“Jasmine”):** first author of the confirmed mortality paper; do not confuse her with Roro.

## Evidence spine

Jingwen Liu et al. (2020), *Sustainable Cities and Society* 57:102131, DOI [`10.1016/j.scs.2020.102131`](https://doi.org/10.1016/j.scs.2020.102131): Hong Kong daily mortality, 2006–2016; DLNM + quasi-Poisson; reversed J; reported cold AF **4.72%** versus heat **0.16%**, and moderate-temperature AF **4.25%** versus extreme **0.63%**. Exact MMT, cutoffs, spline/lag details, and full test universe await the full PDF/supplement. These are mortality AFs, not stroke effects.

Zhenyuan Liu et al. (2026), medRxiv v1, DOI [`10.64898/2026.03.05.26347683`](https://doi.org/10.64898/2026.03.05.26347683): model-based 2014–2023 excess mortality using transported local RRs under `HWD_Tavg`, `HWD_Tmax`, `HWD_Tmin`, and `HWD_Tcombined`. It reports 1,455–3,238 excess deaths across definitions. The revised PDF has not been ingested; v1 operator ambiguities remain. Its RRs and deaths are not stroke coefficients.

The family is cumulative: Jasmine daily mortality AF/RR → Roro multi-definition modelled heat deaths → this project’s monthly stroke morbidity associations.

## Analysis architecture

The executable pathway panel is `P01–P18`: continuous temperature/lag; official extremes; Wang/Ren spells and 2D3N; heat/cold months; age/sex; COVID; staged pollution; humidity; flu; variability; pre-COVID; and subtype. Seventeen pathways are enabled in synthetic dry-run; `P13` stays off until subtype is explicitly delivered. `P02 + P04` is a proposal, not a frozen headline.

The definition catalogue contains `HM01–HM50` and `CM01–CM48`. Core starters are `HM23`, `HM08`, `HM15`, `HM17`, `HM19`, `CM03`, `CM08`, and `CM15`; first-wave sensitivities are `HM27`, `HM32`, `CM05`, and `CM30`. `HM23` translates Li et al.’s event into Hogan’s monthly count-tail design; reference period, percentiles/ties, gaps, missingness, and month assignment remain pending Hogan. Flu covers 121/132 months and is never zero-filled.

## Human gates and next sequence

1. **Hogan Tuesday lock:** listen first; record exact `HM23` and starter roles; update registry/catalogue/debrief. Run [Playbook 01](../analysis_plan/playbooks/01_hogan_definition_lock.md).
2. **HA arrival:** governance → dictionary/schema → QC → merge → real provenance. Run [Playbook 02](../analysis_plan/playbooks/02_ha_data_arrival.md).
3. **Analysis:** run the complete pathway and HM/CM panels; freeze Gate 3 **with the team** before primary claims; no cherry-picking. Run [Playbook 03](../analysis_plan/playbooks/03_full_analysis_run.md).
4. **Write-up:** only verified real estimates enter Results/Discussion. Engage the [CNS-writing skill](../.cursor/skills/cns-writing/SKILL.md) and [Playbook 04](../analysis_plan/playbooks/04_final_writeup.md).

For shocks, use [Playbook 99](../analysis_plan/playbooks/99_emergencies.md). The prose exemplar is [`essay_lit_methods.md`](../reports/laidlaw_stage3/essay_lit_methods.md); the voice standard is [`writing_standards_hogan.md`](../analysis_plan/writing_standards_hogan.md). Update durable context, not only chat.
