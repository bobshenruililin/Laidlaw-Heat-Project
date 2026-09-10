# Context bootstrap — read first in every new chat

**Canon date:** 10 September 2026. Read [`PROJECT_STATE.md`](../analysis_plan/PROJECT_STATE.md), [`2026-08-16_auto_research_lab.md`](2026-08-16_auto_research_lab.md), [`2026-08-15_cns_paper_team.md`](2026-08-15_cns_paper_team.md), and [`2026-08-10_cns_final_reanalysis.md`](2026-08-10_cns_final_reanalysis.md) for living detail. Update this file whenever a human gate changes.

## Scientific contract

**10 September 2026:** Hogan proposed redirecting the **candidate journal angle** from thermal extremes to the pre- vs post-COVID contrast, using thermal extremes as a ruling-out exhibit. That is **not** a Gate 3 freeze. The thermal live pack is parked at [`manuscript/archive/thermal_extremes_2026-08/`](../manuscript/archive/thermal_extremes_2026-08/). The new draft lives in [`manuscript/covid_period/`](../manuscript/covid_period/). Do not overwrite Hogan’s shared Word in place. Do not write “health improved.” Labs were never in the HA monthly transfer. Debrief: [`reports/meeting_debrief_2026-09-10.md`](../reports/meeting_debrief_2026-09-10.md).

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

The manuscript now has one authority: the live file shared by Hogan with Bob and Roro. Stage 3 submits the accessible programme essay (`outputs/ShenRuililin_Laidlaw_Stage3Report.pdf`), not that live file. Same-day Word-pathway cut: [`2026-08-22_stage3_word_pathway.md`](2026-08-22_stage3_word_pathway.md).

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
5. **Live manuscript:** Hogan Word+PDF now exceed the 24 August Desktop snapshot (`b172ed31659d6cd6`, 14 pages). Current PDF `96b69b7b7ba38513` (22 A4); Word `852702ded2c4e968`. Short night/CHD and HF/cold hypotheses + instruments-only WHO/HK map remain. Table 2 = Model 1; Hogan HKO paragraph untouched. Word comments no longer say paste/pipeline. Model 2/3 still need a governed-panel fit. Roro still owns ICD/timing and the IRB number. Gate 3 remains open. Scorecard: [`../reports/hogan_exceeds_20260824_snapshot.md`](../reports/hogan_exceeds_20260824_snapshot.md). Durable: [`2026-08-31_hogan_exceeds_snapshot.md`](2026-08-31_hogan_exceeds_snapshot.md).
6. **Stage 3 programme (30 Aug 2026 send pack):** [`ShenRuililin_Laidlaw_Stage3Report.pdf`](../outputs/ShenRuililin_Laidlaw_Stage3Report.pdf) SHA prefix `1200082a9e7c9caa`. Send pack: [`send_pack_2026-08-30/`](../analysis_plan/send_pack_2026-08-30/). Same science as the live Discussion; Appendix Table A2 is instruments-only. Reported estimates remain Model 1; Models 2–3 specified, not fitted. Poster optional (`a972206e61932650`). Form 2a signed 31 Aug against the 22 Aug foldback — hashes: [`2026-08-31_bishai_form2a_signed.md`](2026-08-31_bishai_form2a_signed.md). Do not attach the live manuscript. Gate 3 remains open.
7. **Submission gates (journal):** PI IRB decision, ICD/inpatient semantics, authorship/order, and cohort risk-set decision. Gate 3 remains open.
8. **Final packet:** integrated report in
   [`reports/bishai_integrated_report/`](../reports/bishai_integrated_report/);
   manuscript and supplement in [`manuscript/`](../manuscript/); validated
   release in [`outputs/release_chd_hf/`](../outputs/release_chd_hf/).
9. **Bishai Figure 3 comments (27 Aug):** pre-COVID away from 1 is HF cold days, not CHD hot nights. “8/6/5 days” on that graph are spline df plus the per-5-day reporting scale. Mapping: [`2026-08-27_bishai_forest_precovid_duration_hhap.md`](2026-08-27_bishai_forest_precovid_duration_hhap.md). Live Figure 3 rebuilt (portrait official-count forest; S6 for continuous T): [`2026-08-27_live_figure3_relabel.md`](2026-08-27_live_figure3_relabel.md). **Same night, forced crown among 5/6/8:** 6-df is the named robustness check (only more-flexible spline that keeps both headlines); Table 2 stays 4 df; 5 is not a spline; 8 opens HF cold days onto 1. [`2026-08-27_crown_df_physiology_policy.md`](2026-08-27_crown_df_physiology_policy.md). Gate 3 remains open.

Use the explicit slash skills `/playbook-01-hogan-lock`, `/playbook-02-ha-arrival`, `/playbook-03-full-analysis`, `/playbook-04-final-writeup`, `/playbook-05-auto-research`, `/playbook-06-scientific-search`, `/playbook-07-pr-board`, `/playbook-08-health-econ-lab`, `/objective-audit`, or `/playbook-99-emergencies`; `/playbook` asks which one. Playbook 06 is [`06_scientific_search.md`](../analysis_plan/playbooks/06_scientific_search.md). Generic TWFE/Callaway/QALY advice is Playbook 08 only, never the live file. DUA: `.cursorignore`. Open-PR board: [`reports/pr_board_latest.md`](../reports/pr_board_latest.md) (living tip `origin/main`; 0 open as of 4 Sep 2026). Each skill reads the canonical playbook and cannot replace human evidence or gate ownership. See the [command contract](2026-07-26_commands_and_blog_auto.md). Auto-research lab: [`analysis_plan/playbooks/05_auto_research_lab.md`](../analysis_plan/playbooks/05_auto_research_lab.md) and [`2026-08-16_auto_research_lab.md`](2026-08-16_auto_research_lab.md).

For shocks, use [Playbook 99](../analysis_plan/playbooks/99_emergencies.md). The prose exemplar is [`essay_lit_methods.md`](../reports/laidlaw_stage3/essay_lit_methods.md); the voice standard is [`writing_standards_hogan.md`](../analysis_plan/writing_standards_hogan.md). Update durable context, not only chat.

For public Laidlaw website writing, use `/laidlaw-blog` or `/blog-from-deck`, the separate MIT Admissions-style canon in [`2026-07-26_laidlaw_blog_canon.md`](2026-07-26_laidlaw_blog_canon.md), and drafts in [`reports/blog/`](../reports/blog/). A deck can trigger a draft offer; Bob edits and publishes.

For the **Laidlaw Scholar Network (LSN)** research-project summary and interactive companion, use [`reports/lsn/research_project_summary.md`](../reports/lsn/research_project_summary.md) and [`docs/lsn/`](../docs/lsn/). Exposure-only public page; CHD/HF first-event framing as of 13 August; Bob edits before posting.
