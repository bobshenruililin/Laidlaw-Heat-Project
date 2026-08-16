# Hogan-lock readiness — not a lock

**Date:** 16 August 2026  
**Playbook:** 01 runs only after actual Hogan notes or a completed decision sheet. This file is a readiness packet. A blank [`hogan_tuesday_decision_sheet.md`](../hogan_tuesday_decision_sheet.md) is **not** evidence of a lock.

Official daily counts already in the live paper (hot nights Tmin ≥ 28°C, very hot days Tmax ≥ 33°C, cold days Tmin ≤ 12°C) are Hogan’s 28 July weather paragraph. They are not `HM23` / `CM05`. Do not overwrite that paragraph.

| Decision-sheet item | Registry now | Status |
|---|---|---|
| Li-HW / `HM23` season | `definitions.HM23.parameters.event_season_months: [5,6,7,8,9]` | **Proposal in registry, not Hogan-written.** `implementation_status: requires threshold reference-period freeze` |
| `HM23` calendar-day p90, 15-day window, 3 consecutive days, join gaps ≤2, monthly assignment `event_start`, monthly p90 | same `parameters` block | **Working option.** Not locked. |
| `HM23` missing-day tolerance | `threshold_policy.missing_day_tolerance: null` | **Pending Hogan** |
| `HM23` cross-month mapping | `threshold_policy.cross_month_event_assignment: null`; HM23 uses `event_start` | **Pending Hogan** (start vs touch vs both) |
| Hot Gate 3 co-primary | starters include HM23, HM08, HM15, HM17, HM19 | **Pending Hogan / team.** Live paper uses official hot-night *counts*, not HM23 |
| Cold Gate 3 co-primary | `CM03` ready (five days Tmin ≤ 12°C); `CM08` needs reference-period freeze; `CM15` needs cross-month check | **Pending Hogan / team.** Live paper uses official cold-day *counts* |
| Roro `HWD_Tavg/Tmax/Tmin/Tcombined` as monthly siblings | not in this registry as HM/CM IDs | **Pending Hogan.** Mortality RRs must not be transported as CHD/HF coefficients |
| Threshold reference period | `threshold_policy.reference_period: null` | **Pending Hogan.** Provisional project practice is study-window only; that is not his lock |
| Percentile / tie method | `threshold_policy.percentile_method: null` | **Pending Hogan** |
| `CM05` (any day Tmin ≤ 10°C) | `implementation_status: ready`; `tier: first_wave`; source “Bishai discussion threshold; hypothesis sensitivity only” | **Code-ready, Hogan confirmation pending.** Not a biological discovery. Zero-month risk if the threshold is rare — do not invent a coefficient if a future run has no events |
| Age bands 65–69 and 70–74 | not in delivered CHD/HF territory-month file | **Pending Roro schema + Hogan visibility.** Territory-total paper until then |

**Already executable without Playbook 01**

- Official HKO daily flags aggregated to months (live weather paragraph + processing paragraph).
- `CM03` absolute five-cold-day month (registry `ready`), still not a live-paper confirmatory exposure.

**Must not do with this packet**

- Fill Hogan-says blanks from registry defaults.
- Call a weather nomination the Gate 3 headline freeze.
- Promote provisional `CM08` 1.173 / `CM03` 1.122 / `HM23` null as confirmatory (Explore only; unlocked).
- Run Playbook 01 until written Hogan words exist.

**Owner:** Hogan writes; Bob records; agents update registry only after a debrief that distinguishes his words from proposals.
