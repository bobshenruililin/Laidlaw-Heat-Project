# Revised Roro/Bishai heatwave-mortality manuscript — source audit

**Reviewed:** 10 August 2026  
**Title:** *Modelling the Excess Mortality Associated with Heat Waves in Hong
Kong: 2014–2023*  
**Authors:** Zhenyuan Liu, Chao Ren, Jingwen Liu, Kawasaki Yurika, David Makram
Bishai  
**Source status:** Unpublished/revised team manuscript supplied privately by
Bob; do not redistribute.

The two supplied PDFs were byte-identical
(`sha256 c4817d0fe81bfbc807a3d2082c02c4268d289e313b7b35bc6513ee17a5f73e56`).
The PDFs are not committed.

## Estimand firewall

The manuscript transports published local mortality relative risks into
modelled excess deaths under four heatwave scenarios. It does not estimate a
new association between observed 2014–2023 daily deaths and temperature.

The Laidlaw CHD/HF study estimates associations with governed monthly
first-hospitalisation counts. The two studies share weather definitions and
policy context, but not outcomes, coefficients, attributable fractions, or
causal claims.

## Four stated exposure definitions

| Label | Intended construction | Source |
|---|---|---|
| `HWD_Tavg` | Daily mean temperature threshold 30.60 C; manuscript describes a 20-day block and RR phases day 0, days 1–5, days 6–21 | Jingwen Liu et al. (2020) |
| `HWD_Tmax` | Prolonged VHD spell, intended `Tmax >= 33 C` and 5+ consecutive days | Wang et al. (2019) |
| `HWD_Tmin` | Prolonged HN spell, `Tmin >= 28 C` and 5+ consecutive nights | Wang et al. (2019) |
| `HWD_Tcombined` | Two consecutive VHDs with three corresponding hot nights (`NDNDN`/2D3N), with a five-day post-event phase | Wang et al. (2019) |

The exact operators must come from the primary papers, not this manuscript
where the text is inconsistent.

## Definition and calculation issues to resolve privately

1. **Tmax table error.** Table 1 describes HWD_Tmax using minimum temperature,
   a 28 C threshold, and VHN terminology. The intended source definition is
   Tmax at least 33 C.
2. **Spell operator.** “Longer than five” conflicts with the published
   shorthand 5VHD/5HN and the Wang source's “five or more.” Code must use the
   primary source.
3. **2D3N alignment.** A generic five-day window containing any two VHDs and
   three HNs is not equivalent to Wang's three nights surrounding two
   consecutive VHDs (`NDNDN`).
4. **Window arithmetic.** Day 0 plus days 1–5 plus days 6–21 spans 22 days,
   while the manuscript calls HWD_Tavg a 20-day period.
5. **Event independence.** The reference point for a 20-day gap between
   threshold events is not executable from the manuscript wording alone.
6. **Excess-death aggregation.** The text alternates between calculating EHD
   for each event and multiplying an EHD by event counts. The code is needed
   to exclude double multiplication.
7. **Uncertainty.** The simulation appears to vary imported RRs but not
   thresholds, event calendars, baseline deaths, population, transport, or
   model choice. Some intervals are implausibly narrow, including
   3,238 (3,234–3,242).
8. **Age-sex synthesis.** Combining marginal age and sex RRs assumes
   multiplicative independence and is not a measured interaction.
9. **Table integrity.** Annual Table 2 cells are visually misaligned. Table 3
   contains at least one unordered confidence interval in the earlier
   extraction. Numeric reuse requires regenerated source output.
10. **Causal/ranking language.** “Preventable,” “independent risk factor,” and
    treating heat as a mutually exclusive leading cause comparable with
    diabetes exceed what an RR-transport simulation identifies.

These points are an internal methods audit. The Laidlaw manuscript will not
publicly criticise the companion team paper.

## What may inform the Laidlaw analysis

- official daytime and nighttime threshold morphology;
- persistent hot-day and hot-night spells;
- exact 2D3N compound events;
- calendar-boundary affected-day windows;
- the need to expose definition sensitivity;
- the distinction between relative association and absolute burden; and
- policy context concerning heat action planning.

## What may not be transported

- mortality RRs or lag weights as CHD/HF admission coefficients;
- 1,455–3,238 modelled deaths as Laidlaw results;
- age/sex mortality effects as admission effect modification;
- the diabetes/top-ten comparison;
- the excess-death equation applied to monthly hospital counts; or
- claims that the monthly HA series reproduces a daily mortality DLNM.

## Source locks required before coding

1. **Li et al. (2025), DOI 10.1016/j.atmosres.2024.107845:** May–September,
   daily Tmax above a calendar-day 90th percentile from a 15-day moving
   window over 1980–2023, at least three consecutive days, and merging events
   separated by two or fewer days.
2. **Wang et al. (2019), DOI 10.1016/j.scitotenv.2019.07.039:** VHD
   `Tmax >= 33 C`; HN `Tmin >= 28 C`; five or more consecutive VHDs/HNs;
   exact 2D3N `NDNDN`; five-day lag evidence.
3. **Jingwen Liu et al. (2020), DOI 10.1016/j.scs.2020.102131:** threshold
   derivation, event independence, and exact lag-phase endpoints.

Until each operator is confirmed, the corresponding exposure is
`SOURCE_LOCK_PENDING` and cannot enter the final real-data model family.
