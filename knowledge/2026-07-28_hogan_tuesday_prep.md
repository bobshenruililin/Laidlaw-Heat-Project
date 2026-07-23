# Hogan Tuesday preparation — 28 July 2026

## Why this entry exists

Hogan offered to meet, and Bob is free on Tuesday 28 July 2026. The meeting is the human gate for the weather side of the Laidlaw Hong Kong thermal–stroke project. Its purpose is to listen to Hogan, place the current options under his scientific lead, and leave with written exposure decisions made together.

This is preparation, not a meeting outcome. Blank decisions remain blank until Hogan speaks.

## People and ownership

- **Hogan:** leads weather/heat framing, the Goggins challenge, climate \(X\), hot-month construction, and the proposed visibility of ages 65–69 and 70–74. He pointed the team to Li et al., *Atmospheric Research* 315 (2025) 107845, DOI `10.1016/j.atmosres.2024.107845`, and proposed the project-level sequence: define heatwaves → count events by month → identify upper-tail months.
- **Roro (Zhenyuan Liu):** leads the governed Hospital Authority stroke aggregates and outcome timing. First GOPC stroke mention is a marker; the true stroke event generally occurred earlier and must be assigned to its true month. Later mentions are not incident events.
- **David Bishai:** leads the broader multi-method and Jasmine-extension question.
- **Bob:** brings definition options, exposure-only audits, reproducible implementation, and notes. Tuesday is not a presentation of a finished weather answer.

## Relationship context to protect

After silence following the January discussion, Bob built HKO climate files unilaterally. Hogan felt sidelined. Repair is ongoing. The technical work does not erase that experience.

Practical implications for Tuesday:

- start by asking Hogan how he frames the weather question now;
- acknowledge that weather is his lead;
- credit his Atmos Res count-to-upper-tail adaptation specifically;
- offer genuine choices rather than asking him to approve a finished specification;
- do not recite repository inventory or effort;
- write his wording down and read it back before leaving.

Hogan has also offered academic-writing guidance. Project prose should be less flowery and easier to digest.

## Confirmed Jasmine identity

“Jasmine” is **Jingwen Liu et al. (2020)**:

> Liu J, Hansen A, Varghese B, et al. “Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016.” *Sustainable Cities and Society*. 2020;57:102131. DOI `10.1016/j.scs.2020.102131`.

Confirmed source facts:

- Hong Kong daily mortality, 2006–2016;
- DLNM integrated with quasi-Poisson regression;
- reversed J-shaped temperature–mortality association;
- reported cold attributable fraction **4.72%** versus heat **0.16%**;
- reported moderate-temperature AF **4.25%** versus extreme-temperature AF **0.63%**.

The full PDF and supplement still need exact methods extraction. These mortality AFs are not stroke coefficients and do not establish the recalled hot-versus-cold p-value pattern.

## Roro baseline

Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika, and David Bishai, “Modelling the Excess Mortality Associated with Heat Waves in Hong Kong: 2014–2023,” medRxiv v1 (2026), DOI `10.64898/2026.03.05.26347683`.

Roro's manuscript transports local mortality RRs from Jasmine and Wang/Ren into model-based excess heat-death scenarios under four definitions:

- `HWD_Tavg`
- `HWD_Tmax`
- `HWD_Tmin`
- `HWD_Tcombined`

The definitions vary in temperature metric, persistence, and lag handling. Their final executable operators must follow the final source manifest because medRxiv v1 contains wording ambiguities. Their mortality RRs must not be used as monthly stroke coefficients. Roro's revised manuscript PDF remains pending comparison with medRxiv v1.

## Complementary evidence spine and estimand

1. Jasmine estimates daily mortality temperature relationships and attributable fractions.
2. Roro estimates model-based excess heat deaths under multiple 2014–2023 definitions.
3. The current project will estimate associations between pre-specified monthly thermal exposures and true-event-month stroke aggregates in 2013–2023.

The layers are complementary, not competing. There are no stroke findings yet.

## HM/CM catalogue and Tuesday starters

The full exposure catalogue contains `HM01–HM50` and `CM01–CM48`.

### Core starters

| Code | Working definition |
|---|---|
| `HM23` | Monthly Li-HW starts at or above the frozen May–September p90 |
| `HM08` | Monthly mean temperature at or above frozen p90 |
| `HM15` | Month touches at least five consecutive `Tmax ≥33°C` days |
| `HM17` | Month touches at least five consecutive `Tmin ≥28°C` nights |
| `HM19` | Month touches a Wang/Ren-style 2D3N window |
| `CM03` | At least five days with `Tmin ≤12°C` |
| `CM08` | Monthly mean temperature at or below frozen p05 |
| `CM15` | Month touches at least three consecutive `Tmin ≤12°C` days |

### First-wave additions

| Code | Working definition |
|---|---|
| `HM27` | Night heat-degree burden above 28°C at or above frozen warm-season p75 |
| `HM32` | `HM08` plus upper-quartile warm-season ozone |
| `CM05` | At least one day with `Tmin ≤10°C`; severe-cold sensitivity only |
| `CM30` | Lower-decile cold month plus upper-quartile influenza activity |

## Decisions still open for Hogan

1. **Li-HW / HM23:** season (May–September?); exact calendar-day p90 reference and percentile method; 15-day moving window; at least three consecutive days; gap joining; missing-day tolerance; monthly assignment by event start, event touch, or burden; upper-tail tie handling.
2. **Gate 3 pair:** one hot and one cold co-primary.
3. **Roro siblings:** whether the four `HWD_*` definitions become named monthly exposure siblings, separate from mortality RR transport.
4. **Reference period:** 2013–2019, full 2013–2023, or a defensible pre-study/external climatology.
5. **CM05 status:** retain ~10°C as a labelled sensitivity, not a biological or genetic threshold.
6. **Age visibility:** retain 65–69 and 70–74 if Roro's approved schema and disclosure controls permit.

## Pack contents

The complete meeting-pack index is at
[`reports/hogan_tuesday/README.md`](../reports/hogan_tuesday/README.md).

## Tuesday artifacts

- [Briefing](../analysis_plan/hogan_tuesday_briefing.md)
- [Decision sheet](../analysis_plan/hogan_tuesday_decision_sheet.md)
- [Agenda](../analysis_plan/hogan_tuesday_agenda.md)
- [Email draft](../analysis_plan/hogan_tuesday_email_draft.md)
- [Printable one-pager](../reports/latex/hogan_tuesday_one_pager.tex)
- [Full HM/CM catalogue](../analysis_plan/hot_cold_month_catalogue.md)
- [Roro deep-read](../literature/roro_manuscript_deep_read.md)

## After the meeting

Record Hogan's exact decisions without retrofitting them to current code. Update the registry and exposure-only selected-month audit only after the written lock. Circulate the short record to Hogan and Roro for correction before Gate 3.
