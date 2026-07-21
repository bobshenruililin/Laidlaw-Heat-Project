# Pathway evidence memo — literature → analysis pathways

**Purpose:** Tie each pathway to published evidence so the multi-method panel is scientifically motivated, not ad hoc.  
**Scope:** Hong Kong and closely related subtropical / methodological work.  
**Honesty:** Daily DLNM coefficients and monthly burden coefficients are **not interchangeable**.

---

## 1. Foundational Hong Kong temperature–CVD admissions

| Paper | Design | What it adds | Pathway impact |
|---|---|---|---|
| Goggins et al. 2013 (*Int J Cardiol*) | Daily AMI + weather/pollution | Cold-dominant AMI; NO₂ important | Keep cold pathways (P08); stage NO₂ (P11); do not assume heat replaced cold |
| Goggins et al. 2012 (*Int J Biometeorol*) | Daily HS vs IS separately | HS strong inverse T (lags 0–4); IS weaker / threshold | Prefer subtype split (P13) **if** stroke file allows; else pooled stroke with caveat |
| Lam et al. 2018 (*PLoS Med*) | Daily AMI × diabetes | Effect modification thinking | Future extension if comorbidity available |

## 2. Hot nights, intensity, and official binary metrics

| Paper | Design | What it adds | Pathway impact |
|---|---|---|---|
| Guo et al. 2024 (*Lancet Reg Health West Pac*) | Daily hot-season hospitalizations | Official HNday28 often null; hot-night *excess* associated | P04 official counts necessary but not sufficient; spell/intensity-like monthly proxies (P05/P06) matter |
| Wang et al. 2019 (*Sci Total Environ*; Ren corresponding) | Daily EHWE mortality | VHD/HN spells; 2D3N combined | Direct motivation for P05–P06 |
| Liu, Ren, …, Bishai (medRxiv 2026) | Daily multi-definition heatwave excess deaths 2014–2023 | No single heatwave definition; 4 definitions change burden | Motivates P07 multi-definition heatwave-month panel; complementary estimand (mortality ≠ admissions) |

## 3. Heatwave definition multiplicity (methods)

| Paper | Lesson | Pathway impact |
|---|---|---|
| Guo et al. 2017 (*Environ Health Perspect*) multicountry heatwaves | Relative percentiles × duration grid | P07 percentile + spell indicators |
| Gasparrini et al. 2015 (*Lancet*) | Most attributable mortality from moderate non-optimum T, cold > heat globally | Continuous T pathways (P01–P03) remain first-class, not only extremes |
| Xu et al. meta-analyses on HW definitions | Definitions drive effect magnitude | Report panel, freeze headline after Gate 3 |

## 4. Pollution × temperature

| Paper | Lesson | Pathway impact |
|---|---|---|
| Guo et al. 2025 (*ES&T*) | PM₂.₅ / pollution can amplify temperature–hospitalization associations | P11 staged pollution (none → single → multi); avoid dumping all pollutants at once |
| Ozone caution | O₃ correlates with hot sunny weather; possible pathway | P11 enters O₃ last; interpret attenuation carefully |

## 5. Cold, influenza, and stroke burden

| Paper | Lesson | Pathway impact |
|---|---|---|
| Yang/Wei/Chong et al. 2025 (*Int J Biometeorol*) | Weekly cold + ILI+ associated with stroke admissions (1998–2019) | P08 cold; P14 flu when CHP series loaded |
| Sipilä / Lorking (warm-climate winter stroke) | Winter excess plausible outside temperate heat narratives | Supports cold co-primary framing |

## 6. Temperature variability & humidity

| Paper | Lesson | Pathway impact |
|---|---|---|
| TV–hospitalisation Hong Kong studies (e.g. JoGH 2023) | Short-term temperature variability associated with admissions | Optional P15 monthly TV proxy from daily range |
| Absolute humidity vs RH | RH entangled with temperature | Prefer AH (already in climate file) in P12 |

## 7. COVID-era care-seeking

HK 2020–2022 utilisation shocks can mimic or mask environmental signals. P10 / P16 treat COVID as sensitivity structure, not as the scientific centrepiece.

## 8. What this project uniquely can claim (if pathways succeed)

A transparent, multi-definition **monthly** assessment of thermal exposures and **stroke admission aggregates** in 2013–2023 Hong Kong, with aging denominators and staged pollution — complementary to daily mortality heatwave work in the same lab — **without** claiming principal-dx AMI from a file that lacks admission reasons.

---

## Bibliography keys (repo)

See `literature/references.bib` and `literature/evidence_matrix.csv`. New pathway IDs should cite at least one anchor above when added to `pathway_registry.yml`.
