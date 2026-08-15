# Context bootstrap — read first in every new chat

**Canon date:** 15 August 2026. Read [`PROJECT_STATE.md`](../analysis_plan/PROJECT_STATE.md), [`2026-08-15_cns_paper_team.md`](2026-08-15_cns_paper_team.md), and [`2026-08-10_cns_final_reanalysis.md`](2026-08-10_cns_final_reanalysis.md) for living detail. Update this file whenever a human gate changes.

## Scientific contract

This project now has two distinct tracks. The runnable paper uses governed
territory-month **CHD and HF first-hospitalisation counts** among people
diagnosed with T2D and/or HTN during January 2013–December 2023 (132 months).
Admission cause is absent; the event is first recorded hospitalisation after
first CHD/HF diagnosis. The continuity estimand is an ecological monthly count
ratio from separate negative-binomial models with calendar-month/trend controls
and a days-in-month offset. It is not cohort incidence, principal-diagnosis
CHD/HF, AMI, individual causality, daily DLNM triggering, a mortality
attributable fraction, or an excess-death model.

Stroke remains a future track: it was named but not attached. No real stroke
coefficient exists. Never invent HA rows, field meanings, subtype availability,
suppression rules, event timing, or findings. Only approved aggregate outputs
may leave governance.

## People and ownership

- **Hogan:** weather/climate co-investigator; Goggins framing; Li-HW count-by-month → upper-tail adaptation; age 65–69/70–74 visibility proposal; academic-writing mentorship. He wrote the live manuscript’s weather Methods and commented on its Introduction. His live weather section is primary; do not overwrite it with repository prose.
- **Zhenyuan Liu (“Roro”):** governed HA outcome construction and transfer,
  regression mentorship, and health-data Methods. He delivered CHD/HF
  first-event aggregates on 6–7 August; stroke remains missing.
- **Professor David Bishai:** supervisor, concept/multi-method direction, PI/governance decisions, and team Gate 3.
- **Bob:** reproducible exposure/analysis preparation, pollution/flu
  integration, writing, and durable decision records. The final integrated
  report and journal-facing repository draft are complete. A CHD/HF
  collaborative draft for Hogan’s live file is in
  [`manuscript/live_collaborative/`](../manuscript/live_collaborative/); paste
  remains a human step.
- **Jingwen Liu (“Jasmine”):** first author of the confirmed mortality paper; do not confuse her with Roro.

The manuscript now has one authority: the live file shared by Hogan with Bob and Roro. The canonical Stage 3 essay is reusable source material, not a parallel manuscript. See [`2026-08-02_hogan_live_manuscript.md`](2026-08-02_hogan_live_manuscript.md).

## Evidence spine

Jingwen Liu et al. (2020), *Sustainable Cities and Society* 57:102131, DOI [`10.1016/j.scs.2020.102131`](https://doi.org/10.1016/j.scs.2020.102131): Hong Kong daily mortality, 2006–2016; DLNM + quasi-Poisson; reversed J; reported cold AF **4.72%** versus heat **0.16%**, and moderate-temperature AF **4.25%** versus extreme **0.63%**. Exact MMT, cutoffs, spline/lag details, and full test universe await the full PDF/supplement. These are mortality AFs, not stroke effects.

Zhenyuan Liu et al. (2026), medRxiv v1, DOI [`10.64898/2026.03.05.26347683`](https://doi.org/10.64898/2026.03.05.26347683): model-based 2014–2023 excess mortality using transported local RRs under `HWD_Tavg`, `HWD_Tmax`, `HWD_Tmin`, and `HWD_Tcombined`. It reports 1,455–3,238 excess deaths across definitions. The private revised PDF was audited on 10 August; primary Wang/Li/Liu operators govern where its wording is inconsistent. Its RRs and deaths are not CHD/HF or stroke coefficients.

The family is cumulative: Jasmine daily mortality AF/RR → Roro
multi-definition modelled heat deaths → this project's monthly CHD/HF
first-hospitalisation associations. Stroke remains a future morbidity layer.

## Analysis architecture

The analysis of record is a twelve-contrast, separate-exposure
negative-binomial panel (CHD/HF × mean temperature, mean Tmax, mean Tmin, hot
nights, cold days, very hot days) with a days offset and full Model/HC1/NW3/NW6
uncertainty ladder. All core q-values exceed 0.19. HF cold days are
SE-concordant but q-unprotected; CHD hot nights are SE-sensitive. Gate 3 is
open.

Exact Wang/Li weather morphology now reproduces five source anchors. A
clean-room monthly-outcome/daily-exposure method failed 500-replicate F1.2
calibration and no real daily coefficient is admitted. See
[`2026-08-10_cns_final_reanalysis.md`](2026-08-10_cns_final_reanalysis.md).

The definition catalogue contains `HM01–HM50` and `CM01–CM48`. Core starters are `HM23`, `HM08`, `HM15`, `HM17`, `HM19`, `CM03`, `CM08`, and `CM15`; first-wave sensitivities are `HM27`, `HM32`, `CM05`, and `CM30`. `HM23` translates Li et al.’s event into Hogan’s monthly count-tail design; reference period, percentiles/ties, gaps, missingness, and month assignment remain pending Hogan. Flu covers 121/132 months and is never zero-filled.

## Human gates and next sequence

1. **HA CHD/HF (7 Aug 2026):** Gate 1 conditional + Gate 2 closed. Full real pathway/HM-CM panel complete. See [`data_receipt_2026-08-07.md`](../reports/data_receipt_2026-08-07.md), [`gate3_decision_packet_2026-08-07.md`](../reports/gate3_decision_packet_2026-08-07.md), [`results_panel_chd_hf_2026-08-07.md`](../reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md).
2. **Stroke file still missing** — re-request from Roro; do not invent stroke rows.
3. **Gate 3:** lead recommendation is explicit no confirmatory primary
   (Option A); freeze with the team only.
4. **Hogan weather lock:** provisional HM/CM reference period is study-window only. Run [Playbook 01](../analysis_plan/playbooks/01_hogan_definition_lock.md) when locked.
5. **Live manuscript:** 15 August CNS-register paste pack is in [`manuscript/live_collaborative/`](../manuscript/live_collaborative/). Shen Ruililin pastes from [`LIVE_DOC_EDITS.md`](../manuscript/live_collaborative/LIVE_DOC_EDITS.md) into Hogan’s shared file (do not email a parallel Word copy). Reply to his seven 28 July threads from [`hogan_comment_paste_replies.md`](../manuscript/live_collaborative/hogan_comment_paste_replies.md); do not resolve them until he has read the replies. Weather paragraph remains Hogan’s. Roro still owns health-data expansion. Figure 3 is trend/depletion sensitivity. Three surfaces: [`2026-08-13_three_manuscript_surfaces.md`](2026-08-13_three_manuscript_surfaces.md). Team merge: [`2026-08-15_cns_paper_team.md`](2026-08-15_cns_paper_team.md). Comment map: [`2026-08-15_hogan_live_comments.md`](2026-08-15_hogan_live_comments.md). [Playbook 04](../analysis_plan/playbooks/04_final_writeup.md) prose only — Gate 3 remains open.
6. **Submission gates:** written dissemination authority, PI IRB decision,
   ICD/inpatient semantics, authorship/order, and cohort risk-set decision.
7. **Final packet:** integrated report in
   [`reports/bishai_integrated_report/`](../reports/bishai_integrated_report/);
   manuscript and supplement in [`manuscript/`](../manuscript/); validated
   release in [`outputs/release_chd_hf/`](../outputs/release_chd_hf/).

Use the explicit slash skills `/playbook-01-hogan-lock`, `/playbook-02-ha-arrival`, `/playbook-03-full-analysis`, `/playbook-04-final-writeup`, or `/playbook-99-emergencies`; `/playbook` asks which one. Each skill reads the canonical playbook and cannot replace human evidence or gate ownership. See the [command contract](2026-07-26_commands_and_blog_auto.md).

For shocks, use [Playbook 99](../analysis_plan/playbooks/99_emergencies.md). The prose exemplar is [`essay_lit_methods.md`](../reports/laidlaw_stage3/essay_lit_methods.md); the voice standard is [`writing_standards_hogan.md`](../analysis_plan/writing_standards_hogan.md). Update durable context, not only chat.

For public Laidlaw website writing, use `/laidlaw-blog` or `/blog-from-deck`, the separate MIT Admissions-style canon in [`2026-07-26_laidlaw_blog_canon.md`](2026-07-26_laidlaw_blog_canon.md), and drafts in [`reports/blog/`](../reports/blog/). A deck can trigger a draft offer; Bob edits and publishes.

For the **Laidlaw Scholar Network (LSN)** research-project summary and interactive companion, use [`reports/lsn/research_project_summary.md`](../reports/lsn/research_project_summary.md) and [`docs/lsn/`](../docs/lsn/). Exposure-only public page; CHD/HF first-event framing as of 13 August; Bob edits before posting.
