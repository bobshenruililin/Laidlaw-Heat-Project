# Intern ceiling note for Hogan and Bishai — 18 August 2026

**Mode:** Ship (meeting file) + Teach (why intern hours cannot mint a primary).
**Audience:** Professor Bishai and Hogan, via a printable note Bob can hand them. Not an Outlook dump. Not a live-manuscript paste.
**Does not:** freeze Gate 3, overwrite weather, invent stroke/daily/person-time, mention scoring loops or agent names in the meeting file.

## Why the entry exists

Bob asked for a hard intern justification: this is the peak of what intern-owned work can do on the delivered monthly CHD/HF file; diminishing returns thereafter; how to break the ceiling; what Hogan, Roro, and Bishai can actually open. The intern was required to search public sources in depth and demonstrate the search, not shrug.

## What is confirmed

Public Hong Kong files cannot replace the governed 132-month first-hospitalisation series among people with T2D and/or HTN.

Demonstrated on 18 August 2026 UTC by `scripts/52_public_outcome_ceiling_search.py`:

- HA `ipdpdd-en.json`: 809 rows, financial year × hospital, no month, no ICD.
- DH 2023 disease-class CSV: one year, ICD-10 chapters, episode basis including day inpatients; I00–I99 = 162,691 (7.20%).
- CKAN inpatient search: one package (C&SD Table 930-92087, quarterly throughput). Disease-group search: zero packages. Guessed HA disease-group JSON paths returned HTTP 200 wrapping HTML 404.
- HKO daily mean temperature for 2013: 365 complete public days. Weather is not the missing object. `HHOT` is tides, not hourly air temperature.
- HA Central Panel Form A (~HK$15,000+) / Form B (~HK$60,000+), local PI, Undertaking (HK storage, destroy within 12 months). Form A ICD-9-CM dimension is all-inpatient episode aggregates, not our cohort first-event rule.
- EHPDCL: CRADLE forbids output; DARE/EXPERT need institutional agreement, ethics, fees.
- Guo et al. 2024: HA emergency admissions used under licence, not publicly available.

Meeting objects: one-page card [`reports/ceiling_card_hogan_bishai_2026-08-18.md`](../reports/ceiling_card_hogan_bishai_2026-08-18.md) and short note [`reports/ceiling_note_hogan_bishai_2026-08-18.md`](../reports/ceiling_note_hogan_bishai_2026-08-18.md) (about two pages; three questions only). Public-file audit: [`reports/public_data_ceiling_search_2026-08-18.md`](../reports/public_data_ceiling_search_2026-08-18.md). Intern working justification retained at [`reports/ceiling_note_hogan_bishai_2026-08-18_long.md`](../reports/ceiling_note_hogan_bishai_2026-08-18_long.md); do not hand that to the room.

## What remains open

Unchanged human doors: Hogan weather lock; Roro stroke / ICD / person-time / age bands; Bishai headline, dissemination, IRB, authorship, whether to open Form B or EHPDCL. Gate 3 still open. No 8 on the frozen bar.

## Owners

Hogan writes weather. Roro writes health-data semantics and any new governed file. Bishai is PI. Bob pastes into the live file and does not send a parallel Word manuscript.

## Estimand boundary

The intern note restates the live paper: monthly ecological count ratios, not incidence, not principal diagnosis, not daily DLNM, not mortality AF. Public annual episode chapters are a different object.

## Files that own the detail

- Meeting note (intern voice): `reports/ceiling_note_hogan_bishai_2026-08-18.md`
- PDF: `reports/ceiling_note_hogan_bishai_2026-08-18.pdf`
- Search log: `reports/public_data_ceiling_search_2026-08-18.md`
- Machine JSON: `outputs/auto_research/public_outcome_ceiling_search.json`
- Script: `scripts/52_public_outcome_ceiling_search.py`
