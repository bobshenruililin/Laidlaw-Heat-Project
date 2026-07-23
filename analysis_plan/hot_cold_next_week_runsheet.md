# Next week: hot/cold month run sheet

## Goal

Identify hot and cold months several defensible ways across 2013–2023. Deliver the 12 exposure-only flags below, selected-month lists and missingness checks before outcomes. In parallel, ingest the confirmed Jasmine paper’s full PDF/supplement and lock its exact source definitions.

## Starter 12

| Tier | ID | Operational rule | Weather lock |
|---|---|---|---|
| Core | HM23 | Li-HW starts/month ≥ frozen May–September p90 | Hogan |
| Core | HM08 | Mean monthly temperature ≥ frozen p90 | Hogan |
| Core | HM15 | Touches ≥5 consecutive Tmax ≥33°C days | Hogan |
| Core | HM17 | Touches ≥5 consecutive Tmin ≥28°C nights | Hogan |
| Core | HM19 | Month touches a Wang/Ren-style 2D3N window | Hogan |
| Core | CM03 | ≥5 Tmin ≤12°C days/month | Hogan |
| Core | CM08 | Mean monthly temperature ≤ frozen p05 | Hogan |
| Core | CM15 | Touches ≥3 consecutive Tmin ≤12°C days | Hogan |
| First wave | HM27 | Monthly `Σ max(0, Tmin−28°C)` ≥ frozen May–October p75 | Hogan |
| First wave | HM32 | HM08 plus May–October ozone ≥ frozen p75 | Hogan |
| First wave | CM05 | ≥1 Tmin ≤10°C day/month | Hogan |
| First wave | CM30 | CM09 plus monthly influenza activity ≥ available-series p75 | Hogan |

## Decisions needed

**Bishai — Jasmine source table:** Jasmine is confirmed as Jingwen Liu et al. (2020), DOI `10.1016/j.scs.2020.102131`. Please provide the full PDF/supplement or source slide and identify the relevant hot/cold figure/table. Confirm the test universe and whether the team wants a same-outcome reproduction, definition transport to stroke, or both.

**Hogan — Li-HW freeze:** Freeze Tmax calendar-day p90; 15-day window; ≥3 consecutive days; May–September; gaps ≤2 days; event-start assignment; monthly-count p90; reference period; percentile/tie method; missing-day tolerance.

## Do not claim yet

- No stroke association, hot–cold contrast, coefficient or causal compound effect.
- Jasmine identity is confirmed; the recalled p-value pattern and exact source specification are not. No replication claim until methods match.
- 10°C remains a discussion cutoff, not a biological threshold.

## Working files

- [Catalogue](hot_cold_month_catalogue.md)
- [Registry](hot_cold_month_registry.yml)
- [Jasmine extension protocol](jasmine_extension_protocol.md)
- [Jasmine paper candidates](../literature/jasmine_paper_candidates.md)
