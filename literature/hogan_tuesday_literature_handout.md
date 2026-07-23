# Hogan Tuesday literature card

**Meeting:** 28 July 2026

**Question:** Which weather definitions should the 2013–2023 monthly stroke project freeze before Gate 3?

The papers below are a connected evidence family, not interchangeable estimates. They move from earlier daily admissions, to daily mortality and heatwave definitions, to Roro’s modeled excess-mortality scenarios. Our proposed layer is different again: monthly thermal exposures associated with true-event-month stroke aggregates.

## Jasmine — locked identity and cold–heat burden

**Liu J, Hansen A, Varghese B, et al. (2020).** “Cause-specific mortality attributable to cold and hot ambient temperatures in Hong Kong: a time-series study, 2006–2016.” *Sustainable Cities and Society* 57:102131. DOI [`10.1016/j.scs.2020.102131`](https://doi.org/10.1016/j.scs.2020.102131).

- Hong Kong daily mortality; DLNM integrated with quasi-Poisson regression.
- Reported overall attributable fractions: **4.72% cold vs 0.16% heat**; **4.25% moderate vs 0.63% extreme** temperature.
- The paper identity and headline AFs are locked. Exact minimum-mortality temperature (MMT), moderate/extreme cutoffs, spline and lag choices still require the full PDF and supplement.

**Why it matters Tuesday:** Jasmine supports a genuine cold co-primary and a moderate-temperature perspective, but her mortality AFs cannot be transported as monthly stroke coefficients.

## Wang/Ren — local event and combined day–night family

**Wang D, Lau KKL, Ren C, Goggins WB, et al. (2019).** “The impact of extremely hot weather events on all-cause mortality in a highly urbanized and densely populated subtropical city: A 10-year time-series study (2006–2015).” *Science of the Total Environment* 690:923–931. DOI [`10.1016/j.scitotenv.2019.07.039`](https://doi.org/10.1016/j.scitotenv.2019.07.039).

- Defines a very hot day as `Tmax ≥33°C` and a hot night as `Tmin ≥28°C`.
- Develops representative 5-VHD, 5-HN and combined 2D3N event families.
- This is an all-cause mortality study at daily resolution.

**Why it matters Tuesday:** It gives the local persistence and day–night structures behind `HM15`, `HM17` and `HM19`, while leaving us to specify transparently how each event is collapsed to months.

## Li, *Atmospheric Research* — Hogan’s weather lead

**Li C, Wei W, Chan PW, Huang J (2025; accepted 2024).** “Heatwaves in Hong Kong and their influence on pollution and extreme precipitation.” *Atmospheric Research* 315:107845. DOI [`10.1016/j.atmosres.2024.107845`](https://doi.org/10.1016/j.atmosres.2024.107845).

- May–September heatwave: daily `Tmax` exceeds its calendar-day p90 for at least three consecutive days.
- The published construction uses a 15-day moving calendar window and joins events separated by no more than two days.
- **Credit split:** Li et al. provide the atmospheric event rule; **Hogan proposed counting those events by month and flagging upper-tail event-count months for this project**.

**Why it matters Tuesday:** It supplies the source event for Hogan’s `HM23` family, whose reference period, monthly assignment and upper-tail/tie rules should now be locked with him.

## Goggins 2012/2013 — foundation and comparability challenge

**Goggins WB, Woo J, Ho S, Chan EYY, Chau PH (2012).** “Weather, season, and daily stroke admissions in Hong Kong.” *International Journal of Biometeorology* 56:865–872. DOI [`10.1007/s00484-011-0491-9`](https://doi.org/10.1007/s00484-011-0491-9).

**Goggins WB, Chan EYY, Yang CY (2013).** “Weather, pollution, and acute myocardial infarction in Hong Kong and Taiwan.” *International Journal of Cardiology* 168:243–249. DOI [`10.1016/j.ijcard.2012.09.087`](https://doi.org/10.1016/j.ijcard.2012.09.087).

- The stroke paper separated haemorrhagic and ischaemic admissions and found cold-relevant daily associations with different shapes and lag windows.
- The AMI paper likewise provides an earlier cold-dominant Hong Kong comparison and highlights pollution, including NO₂.
- Their daily admissions designs are not coefficient-comparable with a monthly aggregate panel.

**Why it matters Tuesday:** Hogan’s Goggins framing asks whether the later period is still best treated as a careful time-change comparison—older population, later heat extremes and changed pollution—without claiming a proven regime shift.

## Guo 2024 — hot-night intensity, not only a binary flag

**Guo YT, Chan KH, Qiu H, Wong ELY, Ho KF (2024).** “The risk of hospitalization associated with hot nights and excess nighttime heat in a subtropical metropolis: a time-series study in Hong Kong, 2000–2019.” *The Lancet Regional Health – Western Pacific* 51:101168. DOI [`10.1016/j.lanwpc.2024.101168`](https://doi.org/10.1016/j.lanwpc.2024.101168).

- Compares the official `Tmin ≥28°C` hot-night indicator with nighttime heat-intensity measures.
- Reports that nighttime heat excess was associated with hospitalization while the official binary hot-night measure alone was not associated with excess risk in that analysis.
- Outcomes are broad hospitalizations, including circulatory admissions—not this project’s stroke outcome.

**Why it matters Tuesday:** It argues for keeping an intensity measure such as `HM27` beside official hot-night counts rather than deciding that a binary null would close the nighttime-heat question.

## Yang/Chong 2025 — cold, influenza and stroke

**Yang Z, Wei Y, Jiang X, Li C, Lin G, Wang Y, Chong KC (2025).** “Association of cold weather and influenza infection with stroke: a 22-year time-series analysis.” *International Journal of Biometeorology* 69:963–973. DOI [`10.1007/s00484-025-02870-2`](https://doi.org/10.1007/s00484-025-02870-2).

- Uses weekly Hong Kong stroke admissions from 1998–2019 with a quasi-Poisson GAM and DLNM.
- Reports cold temperature and influenza activity as stroke-admission risk factors.
- Weekly exposure–lag estimates are not monthly coefficients.

**Why it matters Tuesday:** It supports a pre-specified cold–influenza sensitivity (`CM30`) while keeping the base cold definition interpretable and avoiding an unestimated claim that influenza modifies temperature.

## Roro — four-definition excess-mortality baseline

**Liu Z, Ren C, Liu J, Kawasaki Yurika, Bishai DM (2026).** “Modelling the Excess Mortality Associated with Heat Waves in Hong Kong: 2014–2023.” *medRxiv* v1. DOI [`10.64898/2026.03.05.26347683`](https://doi.org/10.64898/2026.03.05.26347683). **Preprint; not peer reviewed.**

- Applies published local mortality RRs from Jasmine and Wang/Ren to four scenarios: `HWD_Tavg`, `HWD_Tmax`, `HWD_Tmin`, and `HWD_Tcombined`.
- Estimates model-based attributable excess deaths rather than fitting a new stroke model.
- MedRxiv v1 has executable wording ambiguities; Roro’s revised manuscript remains pending comparison.

**Why it matters Tuesday:** The four `HWD_*` definitions can become named monthly exposure siblings beside other families—never replacements and never imported mortality RRs—once the final source manifest is settled.

## Tuesday claim boundary

No paper above supplies a finding for the project’s undelivered monthly stroke series. Tuesday should freeze exposure definitions and reporting roles, not select a definition because of a health coefficient.
