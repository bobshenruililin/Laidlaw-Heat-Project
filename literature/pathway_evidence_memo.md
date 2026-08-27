# Pathway evidence memo — literature → analysis pathways

**Purpose:** Tie each pathway to published evidence so the multi-method panel is scientifically motivated, not ad hoc.  
**Scope:** Hong Kong and closely related subtropical / methodological work.  
**Honesty:** Daily DLNM coefficients and monthly burden coefficients are **not interchangeable**.  
**Updated:** 2026-08-27 (consecutive-night physiology addendum; see `knowledge/2026-08-27_crown_df_physiology_policy.md`). Prior spine 2026-08-10.

---

## 1. Foundational Hong Kong temperature–CVD / stroke admissions

| Paper | Design | What it adds | Pathway impact |
|---|---|---|---|
| Goggins et al. 2012 (*Int J Biometeorol*) | Daily HS vs IS separately | HS strong inverse T (lags 0–4); IS weaker / threshold ~22°C; stronger in older & females for HS | Prefer subtype split (P13) **if** available; sex interaction (P17); cold co-primary (P08/P18) |
| Goggins et al. 2013 (*Int J Cardiol*) | Daily AMI + weather/pollution | Cold-dominant AMI; NO₂ important | Stage NO₂ (P11); do not assume heat replaced cold |
| Chan/Goggins et al. 2013 (*Bull WHO*) | Daily admissions vs temperature | Heat above ~29°C and cold both raise admissions | Continuous T pathways remain first-class (P01–P03) |
| Lam et al. 2018 (*PLoS Med*) | Daily AMI × diabetes | Effect modification thinking | Future if comorbidity available |

## 2. Hot nights, intensity, and official binary metrics

| Paper | Design | What it adds | Pathway impact |
|---|---|---|---|
| Guo et al. 2024 (*Lancet Reg Health West Pac*) | Daily hot-season hospitalizations | Official HNday28 often null; hot-night *excess* associated | P04 official counts necessary but not sufficient; spell/intensity-like monthly proxies (P05/P06) matter |
| Wang et al. 2019 (*Sci Total Environ*; Ren corresponding) | Daily EHWE mortality | VHD/HN spells; 2D3N combined | Direct motivation for P05–P06 |
| Liu, Ren, …, Bishai (medRxiv 2026) | Daily multi-definition heatwave excess deaths 2014–2023 | No single heatwave definition; definitions change burden | Motivates P07 multi-definition heatwave-month panel; complementary estimand |

## 3. Heatwave definition multiplicity (methods)

| Paper | Lesson | Pathway impact |
|---|---|---|
| Guo et al. 2017 (*Environ Health Perspect*) multicountry heatwaves | Relative percentiles (90/92.5/95/97.5) × duration (2/3/4 d) grid | P07 monthly collapse: p90/p95/p975 month indicators + spell proxies |
| Gasparrini et al. 2015 (*Lancet*) | Most attributable mortality from moderate non-optimum T; cold > heat globally | Continuous T pathways (P01–P03) remain first-class |
| Xu et al. meta-analyses on HW definitions | Definitions drive effect magnitude | Report panel; freeze headline after Gate 3 |

## 4. Pollution × temperature

| Paper | Lesson | Pathway impact |
|---|---|---|
| Guo et al. 2025 (*ES&T*) | PM₂.₅ / pollution can amplify temperature–hospitalization associations | P11 staged pollution (none → single → multi); avoid dumping all pollutants at once |
| Ozone caution | O₃ correlates with hot sunny weather | P11 enters O₃ last; interpret attenuation carefully |

## 5. Cold, influenza, and stroke burden

| Paper | Lesson | Pathway impact |
|---|---|---|
| Yang/Wei/Chong et al. 2025 (*Int J Biometeorol*) | Weekly cold + ILI+ associated with stroke admissions (1998–2019; ~1.17M admissions); ARR≈1.11 at 5th pct temperature | P08 cold; P14 flu; P18 cold-month |
| Sipilä / Lorking (warm-climate winter stroke) | Winter excess plausible outside temperate heat narratives | Supports cold co-primary framing |

## 6. Temperature variability, humidity, and healthcare burden

| Paper | Lesson | Pathway impact |
|---|---|---|
| Tian/Qiu et al. 2023 (*J Glob Health*) | Short-term TV associated with circulatory hospitalisations in HK; older adults more vulnerable | P15 monthly mean diurnal-range (from daily extracts) |
| Absolute humidity vs RH | RH entangled with temperature | Prefer AH (climate file) in P12 |
| Frontiers 2024 TLOS cardiopulmonary HK | Non-optimal T raises total length of stay; cold dominates attributable fraction | Complements admission-count estimand; motivates reporting burden carefully |
| Eco-Environ Saf 2025 cold circulatory costs | Cold attributable risk for emergency circulatory admissions + LOS/costs | Supports cold pathways as co-primary, not afterthought |

## 7. COVID-era care-seeking

HK 2020–2022 utilisation shocks can mimic or mask environmental signals. P10 / P16 treat COVID as sensitivity structure, not as the scientific centrepiece.

## 8. What this project uniquely can claim (if pathways succeed)

A transparent, multi-definition **monthly** assessment of thermal exposures and **stroke admission aggregates** in 2013–2023 Hong Kong, with aging denominators and staged pollution — complementary to daily mortality heatwave work in the same lab — **without** claiming principal-dx AMI from a file that lacks admission reasons.

---

## Bibliography keys (repo)

See `literature/references.bib`, `literature/evidence_matrix.csv`, and especially **`literature/final_methods_evidence_map.md`** (source → verified claim → exact manuscript use → misuse warning). New pathway IDs should cite at least one anchor above when added to `pathway_registry.yml`.

Canonical key notes (2026-08-10):

- Prefer `yang2025coldflu` over the older `wang2025coldflu` alias (alias kept only for legacy cite keys).
- Prefer `wang2019ehwe` (do not revive `wang2014hotspell`).
- Roro public cite = `liu2026roro` (medRxiv preprint), never the private revised PDF.
- Methods spine keys: `basagana2024md`, `basagana2026md`, `gasparrini2010`, `dunsmuir2015glarma`, `zhu2011nbingarch`, `lazarus2018har`, `politis1994bootstrap`, `simonsohn2020speccurve`, `tashman2000rolling`, `greenland1989ecological`, `li2025heatwaves`.

---

## 9. Claim-class firewall (final report)

Keep these estimands separate in prose and tables:

1. **Daily mortality AFs** — Jasmine 2020; Gasparrini 2015 framing.
2. **Modeled excess deaths** — Roro medRxiv 2026 (RR-transport scenarios).
3. **Monthly morbidity count ratios** — this project’s CHD/HF (and any future stroke) NB/GLARMA panel.
4. **M|D method-validation** — Basagaña–Ballester aggregated likelihood under synthetic calibration gates only.

Emails and private PDFs are provenance, not references.

---

## 10. Dry-run / real-panel status

Synthetic plumbing checks and any real CHD/HF panel outputs live under `outputs/`. Coefficients remain labelled by provenance (`SYNTHETIC`, `HA_APPROVED_AGGREGATE`, etc.). See the living state file rather than treating this memo as a results ledger.

## 11. Consecutive nights vs spline df (27 August 2026)

Local **mortality** papers give an empirical reason to watch ≥5 consecutive hot nights (Wang et al. 2019; Ho et al. 2017). Sleep and overnight core-temperature physiology support nights and non-recovery (Chevance et al. 2024; Ioannou et al. 2024; O’Connor et al. 2025). Those sources do **not** identify a 5- vs 6- vs 8-day myocardial threshold, and they are not this project's monthly first-event estimand. Durable: [`knowledge/2026-08-27_crown_df_physiology_policy.md`](../knowledge/2026-08-27_crown_df_physiology_policy.md). P05/HM15 remain Explore motivation for daily data, not Table 2.
