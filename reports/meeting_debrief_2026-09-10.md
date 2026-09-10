# Meeting debrief — Hogan, 10 September 2026

**Mode:** Decide. **Not** Playbook 01. Hogan did not lock a weather operator. He redirected the **candidate journal angle**.

**His words (email after the chat):** pre-COVID and post-COVID findings are much more interesting because, contrary to expectation, cold weather days have actually “improved” CHD and HF admissions. Change the angle of the paper to focus on that instead of thermal extremes. Use thermal extremes to say this is not the reason for the pre–post difference. Next: (1) check other metadata, especially lab tests with the admissions panel; (2) a quick literature search for physiological evidence of health improvements pre- vs post-COVID — not necessarily CHD/HF.

**This note:** Bob / agents. Do not send the archive or the COVID-period skeleton as a Hogan briefing. His last Hogan-facing object remains the mechanism bullets unless Bob writes a new short reply.

---

## What changed (before → after)

| Before | After |
|---|---|
| Journal-track live file treats Table 2 thermal residuals as the identification article (CHD hot nights; HF cold days). Gate 3 still open. | Hogan **proposes** the pre- vs post-COVID contrast as the angle. Thermal extremes become a ruling-out exhibit. Team freeze of that headline has **not** happened. |
| COVID window was a sensitivity (P16 / Figure 3). | Candidate **primary exhibit**: window dependence of count ratios. |
| Labs not in the ranked Roro ask list. | Hogan asked whether labs came with the panel. Answer: they did not. |

## What is now out of scope (until the team reopens)

- Thermal extremes as the **headline** of the next journal draft.
- Writing “cold days improved health” or “physiology improved after COVID.”
- Inferring adaptation or biology from a COVID contrast (Playbook 99 case 4).
- Treating a 48-month post-only Model 1 as if it already exists.
- Opening governed panels to hunt for labs that were never transferred.

## What became newly allowed

- A parked copy of the thermal live pack under `manuscript/archive/thermal_extremes_2026-08/`.
- A new track `manuscript/covid_period/` that does not overwrite Hogan’s shared Word.
- Playbook 08 Explore on **synthetic** schemas for utilisation-shock Monte Carlo. Not TWFE. Not the live file.
- A Sol/Astra prompt for later: `analysis_plan/prompts/GOAL_covid_period_sol_astra.md`.

## Hogan’s sentence versus the file

Hogan’s “improved” is **his language**. The file supports **window dependence**, not a health-gain coefficient.

- HF cold days / 5 days: full sample **1.073 (1.006–1.144)**; pre-2020 **1.113 (1.053–1.176)**. The cold association is **stronger before 2020**. Including 2020–2023 **attenuates** it toward 1. It does not go below 1.
- CHD cold days / 5 days: pre-2020 **1.036 (1.007–1.067)** excludes 1; full sample **0.995 (0.949–1.043)** includes 1.
- CHD hot nights / 5 days: pre-2020 **1.011 (0.991–1.032)** includes 1; full sample **1.022 (1.002–1.042)** needs 2020–2023.
- First-event **counts** halved 2013→2023 (CHD 23,830→12,323; HF 4,336→2,296) with a 2020 dip, while C&SD 35+ rose ~17%. That is depletion + care-seeking in the live Results, not incidence and not “health improved.”
- There is **no** standalone post-COVID 48-month Model 1 table. Pre-2020 = January 2013–December 2019 (84 months).

**Correction for Bob to confirm with Hogan if needed:** if he meant the **raw admission totals** fell, that is already Figure 1 and is compatible with avoidance and a closed diagnosis window. If he meant the **cold-day count ratio** got smaller after 2019, that is the Figure 3 / P16 contrast. Those are different objects.

## Metadata (labs)

The delivered HA package is `year`, `month`, `chd_inpatient` / `hf_inpatient`. Lab tests (HbA1c, lipids, BNP, creatinine, troponin, …) were **never promised, never delivered, and are not on the ranked ask list**. CDARS can carry labs in *other* HKU papers; that would be a **new governed extract** (Roro / Bishai), not a forgotten column. Ranked asks stay: stroke, still-at-risk person-time, age bands, ICD/inpatient note. Default: **do not ask for labs** until Bishai agrees a new extract. Inventory: [`analysis_plan/covid_period/ha_metadata_inventory.md`](../analysis_plan/covid_period/ha_metadata_inventory.md).

## Literature (quick)

Local evidence is **utilisation down, mortality up**, not physiological improvement. Spine: [`literature/covid_period_mechanism_memo.md`](../literature/covid_period_mechanism_memo.md). Do not paste Xin’s hospitalisation reduction into Table 2.

## Open questions still human-owned

| Question | Owner |
|---|---|
| May the journal paper abandon thermal as primary after Stage 3 already submitted a thermal essay? | Bishai |
| Does “improved” mean CR attenuation, count decline, or physiology? | Hogan |
| New extract (labs / person-time)? | Roro / Bishai |
| Paste a new Word into Hogan’s live file? | Bob |
| Gate 3 freeze of the new headline | Hogan / Roro / Bishai / Bob |

## Next executable step that does not invent data

Bob sends a short reply: we heard the angle; labs did not come with the panel; the file shows **attenuation of cold-day count ratios** and a **halving of first-event counts**, which is not the same as health improvement; thermal stays as a ruling-out exhibit; we will not cut his live Word until he asks. Draft: [`send_pack_2026-09-10/reply_to_hogan.md`](../send_pack_2026-09-10/reply_to_hogan.md).

## Weather lock

Locked something? **No.**
