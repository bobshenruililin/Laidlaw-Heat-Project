# Hogan lock card — HM23 is not yet executable

**Date:** 14 August 2026.  
**Audience:** Hogan (weather lock). Not a Bishai object. Not Gate 3.  
**Playbook:** [01](../analysis_plan/playbooks/01_hogan_definition_lock.md). A blank sheet is not a lock. This card does not fill the blanks.

The catalogue already names the event family (Li et al. *Atmospheric Research* 315:107845) and Hogan’s count-to-tail adaptation. Rank 3.92 on the first-wave file does **not** replace the parameter lock. Registry `threshold_policy.reference_period` is still `null`. The study-window 2013–2023 cut used in `outputs/reports/hm_cm_exposure_build.md` is provisional.

Tick one box per row. Leave it blank if it is still open. Bob implements only what is ticked.

| Parameter | Working option now (not locked) | Tick | If ticked, what changes | If left blank |
|---|---|---|---|---|
| Calendar-day percentile **reference period** | Provisional: study window 2013–2023 | [ ] 2013–2019 [ ] 2013–2023 [ ] other: ______ | All relative HM/CM flags rebuild from that climatology | Keep `null`; do not call the file locked |
| Daily p90 **method / ties** | Unspecified in the registry | [ ] type-7 [ ] type-8 [ ] other: ______ | Event starts can differ on tied days | Event operator is not executable |
| Daily comparison | Registry draft: `>` p90 | [ ] `>` [ ] `≥` | Inclusive nights enter Li-HW | Leave as draft |
| Season | Registry draft: May–September | [ ] MJJAS [ ] other: ______ | Eligible months for event search | Leave as draft |
| Duration | Registry draft: ≥3 consecutive days | [ ] 3 [ ] other: ______ | Spell definition | Leave as draft |
| Gap join | Registry draft: join if gap ≤2 days | [ ] ≤2 [ ] no join [ ] other: ______ | Event counts, not intensity | Leave as draft |
| Missing-day tolerance | `threshold_policy.missing_day_tolerance: null` | [ ] drop day [ ] require complete window [ ] other: ______ | How incomplete HKO days are treated | Leave as draft |
| Month assignment | Registry draft: `event_start` | [ ] start [ ] touch [ ] start primary + touch sensitivity | Which month receives a cross-month spell | HM15/HM17 still “ready after cross-month assignment check” |
| Monthly count percentile | Registry draft: p90 of May–Sep monthly event starts | [ ] p90 MJJAS [ ] other: ______ | Which months become HM23 | Leave as draft |
| Monthly discrete ties | Unspecified | [ ] include all tied months [ ] other: ______ | How many months flag in a tied year | Leave as draft |

One Methods sentence changes only when the reference period and the percentile/tie rule are both ticked: “provisional, study-window reference” becomes a locked rule with Hogan as owner.

**Do not:** treat this card as Playbook 01 done; overwrite Hogan’s live weather paragraph; freeze Gate 3; fit more catalogue IDs because rank is 3.92.

Open question W03 remains open until Hogan’s wording is on the Tuesday sheet and in `hot_cold_month_registry.yml`.
