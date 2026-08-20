# Monthly CHD/HF analysis — one card

**Shen Ruililin · 18 August 2026 · print · not a live-file paste**

Hospital Authority–approved monthly first-event CHD/HF counts among people with T2D and/or HTN, 2013–2023. Stroke, daily outcomes, and cohort person-time are not in the file.

## What the extract supports

Ecological monthly count ratios. Not incidence. Not principal diagnosis. Not daily triggering. Twelve predeclared contrasts; all *q* > 0.19. CHD hot nights 1.022 per five hot nights (1.002–1.042) under Newey–West lag 6; other error constructions and the pre-2020 window include 1. Cold days sit almost entirely in December–February. Hogan’s weather paragraph already stands.

Further modelling cannot create missing person-time or a stroke file. A detectable-effect calculation on this covariance ladder is intern work; it does not mint a primary.

## Public substitutes

I downloaded HA financial-year hospital throughput (no month, no ICD), the DH 2023 ICD-chapter episode file, and public HKO daily temperature. They are the wrong grain. Guo et al. (2024) used licensed HA emergency admissions. Full log: `public_data_ceiling_search_2026-08-18.md`.

## Questions for this meeting

1. **Hogan.** Keep official monthly hot-night, very-hot-day, and cold-day counts as the exposure family? If HM23 remains, which reference period and month-assignment rule?
2. **Professor Bishai.** Proceed as an identification-focused paper without a confirmatory primary, once weather and health-data methods are confirmed?
3. **Roro, as a follow-up.** Outcome definitions, and a yes/no on stroke, person-time, and 65–69 / 70–74. Not a same-day extract request.

Short note: `ceiling_note_hogan_bishai_2026-08-18.md`.
