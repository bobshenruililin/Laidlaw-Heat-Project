# Hot/cold month exposure build

- Built at: 2026-08-10 09:48:08.189538
- **Reference period:** PROVISIONAL study window 2013-2023; registry reference_period still null
- Hogan-locked: FALSE
- Daily file: NA
- Source-locked spillover file: /workspace/data_processed/exposures_spillover_monthly_2013_2023.csv
- Output: `/workspace/data_processed/hm_cm_month_flags_2013_2023.csv`

## Selected-month counts

| ID | n_selected | status |
|---|---|---|
| HM08 | 14 | provisional_study_window |
| HM15 | 7 | provisional_study_window |
| HM17 | 14 | provisional_study_window |
| HM19 | 14 | provisional_study_window |
| HM27 | 23 | spell_presence_proxy |
| HM32 | 38 | 2d3n_presence_proxy |
| CM03 | 14 | provisional_study_window |
| CM08 | 7 | provisional_study_window |
| CM15 | 15 | provisional_study_window |
| CM05 | 0 | mean_tmin_proxy_not_daily_CM05 |
| CM30 | 21 | spell_length_proxy |
| HM23 | 7 | source_locked_Li_daily_events_Hogan_monthly_tail_NOT_locked |

These flags are **provisional**. Gate 3 must not treat HM23 as locked until Playbook 01 closes.
