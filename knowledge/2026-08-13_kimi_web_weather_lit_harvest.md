# Kimi K3 web harvest — HKO yearbooks, EPD air quality, and literature verification

**Date:** 13 August 2026
**Mode:** Explore / Ship (public-source verification for the live manuscript)
**Provenance rule:** every number below is labelled `REAL` (public HKO/EPD/press source) or `cited paper`. No HA numbers appear in this memo. Nothing here touches `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`, Hogan's weather paragraph, or Laidlaw PDFs.

Sources were read on 13 August 2026 via HKO Year's Weather pages, info.gov.hk press releases, the EPD/AQHI annual report annex, publisher pages, PubMed E-utilities, Semantic Scholar, and medRxiv.

---

## 1. Yearbook and EPD tables versus our tables

### 1a. HKO annual extremes versus `outputs/tables/hko_annual_extremes_2013_2023.csv`

| Year | Hot nights (Tmin ≥ 28 °C) | Very hot days (Tmax ≥ 33 °C) | Cold days (Tmin ≤ 12 °C) | Status |
|---|---|---|---|---|
| 2013 | 10 (repo 10) | 17 (repo 17) | 14 (repo 14) | **Match** [REAL] |
| 2017 | 41 (repo 41) | 29 (repo 29) | 9 (repo 9) | **Match** [REAL] |
| 2019 | 46 (repo 46) | 33 (repo 33) | 1 (repo 1) | **Match** [REAL] |
| 2021 | 61 (repo 61) | 54 (repo 54) | 13 (repo 13) | **Match** [REAL] |
| 2023 | 56 (repo 56) | 54 (repo 54) | 14 (repo 14) | **Match** [REAL] |
| 2024 | 50 | 52 | 11 | **New public row** (outside our 2013–2023 window) [REAL] |

Sources: HKO Year's Weather 2013 (`/en/wxinfo/pastwx/ywx2013.htm`), 2017, 2019, 2021, 2023, 2024 (`/en/wxinfo/pastwx/YYYY/ywxYYYY.htm`), cross-checked against info.gov.hk press releases of 8 Jan 2020 (2019), 7 Jan 2022 (2021), 8 Jan 2024 (2023), 13 Jan 2025 (2024).

Additional verified colour [REAL]:

- 2021 was the warmest year on record at the time (annual mean 24.6 °C); 61 hot nights and 54 very hot days were both the highest on record. This anchors the claim-ledger line "2021 hot nights highest in-window: 61".
- 2019 was the warmest year on record at the time (24.5 °C); its single cold day is the fewest annual cold days since 1884, and its absolute minimum (11.4 °C on 1 Jan) is the highest annual minimum on record.
- 2023 was one of the second warmest years (24.5 °C); 56 hot nights ranked second highest; 4 extremely hot days (matches repo EHD = 4).
- 2024 became the warmest year on record (24.8 °C, 1.3 °C above the 1991–2020 normal) with 52 very hot days, 50 hot nights, 2 extremely hot days, 11 cold days. Note for framing: 2024 was warmest by **mean temperature** but its hot-night count (50) sat below 2021 (61), 2023 (56), and 2022 (52) — mean warmth and extremes counts are not interchangeable.
- 2013 (our window's first year) was a near-normal year: annual mean 23.3 °C, hot nights about seven days **below** the 1981–2010 normal. The in-window rise 10 → 61 hot nights (2013 → 2021) therefore starts from an unusually cool-hot baseline, not a typical year.

**Internal consistency check (ran today):** the monthly panel `outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv` sums exactly to the annual CSV for all four metrics in all 11 years. No internal discrepancy.

**Unresolved (minor):** the extremely-hot-days column (Tmax ≥ 35 °C) is not stated in the Year's Weather prose for most years (2013–2022). Repo values are consistent with each year's stated annual maximum (e.g. 2013 max 34.9 °C → 0 EHD; 2017 max 36.6 °C → 1 EHD), and 2023's prose confirms 4. If an EHD count is ever quoted in the live paper, verify against HKO daily data first.

### 1b. HKO definitions and trend pages

Verified from HKO "Climate Change in Hong Kong" pages [REAL]:

- Definitions: hot night = daily minimum ≥ 28.0 °C; very hot day = daily maximum ≥ 33.0 °C; cold day = daily minimum ≤ 12.0 °C. Identical wording appears in the Year's Weather footnotes and on the extreme-weather page. These match the project's exposure construction.
- Trend direction: "Over the last hundred years or so, the numbers of hot nights … and very hot days … have increased while the number of cold days … has decreased" (HKO extreme-weather page).
- Warming rate: annual mean temperature at HKO Headquarters rose 0.14 °C per decade over 1885–2025 and 0.35 °C per decade over 1996–2025 (both statistically significant at 5%; HKO temperature page).
- Older quantified extremes trend (HKO reprint r832, Wong & Mok): over 1885–2008, cold days fell 1.2 days per decade and hot nights rose 1.5 nights per decade (both significant at 5%); very hot days showed no significant trend over that full period.

### 1c. EPD general-station pollution versus `outputs/tables/pollution_annual_means_general_2013_2023.csv`

Comparison against the EPD annex "2011 to 2023 Annual Average Concentrations of Major Air Pollutants in Hong Kong" (info.gov.hk, 7 Feb 2024; 2023 values preliminary) and the AQHI "Air Quality in Hong Kong 2023" report [REAL]:

| Pollutant (general stations) | 2013 EPD / repo | 2023 EPD / repo | Endpoint status |
|---|---|---|---|
| NO₂ (µg/m³) | 54 / 53.72 | 32 / 32.08 | **Match** (EPD rounds to integers) |
| PM2.5 (µg/m³) | 31 / 30.83 | 15 / 14.56 | **Match** |
| PM10 (µg/m³) | 47 / 47.09 | 25 / 24.71 | **Match** |
| O₃ (µg/m³) | 43 / 42.61 | 58 / 58.31 | **Match** |

- The live claim-ledger line "NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3" is consistent with EPD's published general-station averages at both endpoints. 2013→2023 changes: NO₂ −40%, PM2.5 −53%, O₃ +37% [REAL, computed from repo table].
- **Mismatch (mid-series, explained):** EPD's per-year network averages differ from repo values in 2015–2016 (NO₂: EPD 49/47 vs repo 46.41/43.84; O₃: EPD 42/39 vs repo 44.38/41.31). PM2.5 and PM10 match EPD in every year. The likely cause is station composition: EPD averages all general stations operating in each year (Tseung Kwan O joined in 2016, North later), while the repo table appears to use a fixed panel. This does **not** affect any live-paper number, which quotes only endpoints; it would matter only if mid-series annual values are quoted.
- EPD's own framing for 2023: ambient PM10, PM2.5, NO₂ and SO₂ annual averages fell 40–69% from their 2011 peaks; ozone "gradually turned steady" after rising. Air quality in 2023 was the second best since 1997.

---

## 2. Literature facts the live Introduction/Discussion MAY say

All entries below were re-verified today against the publisher page, PubMed abstract, or preprint server. Paste-ready sentences; provenance = cited paper.

### Guo et al. 2024, *Lancet Reg Health West Pac* 51:101168 — DOI 10.1016/j.lanwpc.2024.101168 (live [17])

Verified against the full text (Table 3, Table 4, Results). The say-map numbers are all correct:

- "Guo et al. analysed 5,002,114 non-cancer, non-external emergency hospitalisations over 3,680 hot-season (May–October) days in Hong Kong, 2000–2019." (cited paper; abstract count)
- "The official binary hot-night indicator (daily minimum ≥ 28 °C; 499 days, 13.6%) showed no overall adjusted association with hospitalisation over lags 0–4 days (excess relative risk −0.2%, 95% CI −1.2% to 0.7%)." (cited paper, Table 3)
- "Each 10 °C·h of hot-night excess was associated with 1.9% (0.2% to 3.5%) higher hospitalisation; the 99th percentile of HNe (28.9 °C·h versus zero) with 3.1% (1.5% to 4.8%)." (cited paper, Table 3)
- "Circulatory hospitalisation rose 4.3% (1.8% to 6.9%) per 10 °C·h of HNe; the respiratory estimate was not significant." (cited paper, Table 3)
- "HNday90th (HNe ≥ 17.7 °C·h; 187 days, 5.1%) was associated with 1.9% (0.7% to 3.0%) higher hospitalisation." (cited paper, Table 4)
- New verified detail available if wanted: associations were stronger in people aged ≥ 65 (5.3%, 3.2% to 7.4%, at 99th-percentile HNe) and in the low-SES group (5.3%, 2.8% to 8.0%); HNe sums hourly degrees above 28 °C from 20:00 to 07:59. (cited paper)

### Goggins et al. 2013, *Int J Cardiol* 168:243–249 — DOI 10.1016/j.ijcard.2012.09.087 (live [1])

Verified against PubMed abstract (PMID 23041014). Say-map numbers correct:

- "In Hong Kong during 2000–2009, a 1 °C decrease below an estimated 24 °C threshold was associated with a 3.7% increase in AMI admissions (mean temperature, lags 0–13 days); no significant heat association was observed." (cited paper)
- "Same-day NO₂ was the strongest pollutant predictor in all three cities; a 10 µg/m³ increase was associated with a 1.1% rise in AMI admissions in Hong Kong." (cited paper)

### Goggins et al. 2012, *Int J Biometeorol* 56:865–872 — DOI 10.1007/s00484-011-0491-9 (live [11])

Verified against PubMed abstract (PMID 21915799). Say-map numbers correct; CIs now confirmed if the live text wants them:

- "During 1999–2006, haemorrhagic stroke admissions (n = 23,457) fell monotonically with temperature across 8.2–31.8 °C: a 1 °C lower mean over lags 0–4 days was associated with a 2.7% (95% CI 2.0% to 3.4%) higher admission rate." (cited paper)
- "The ischaemic association (n = 107,505) was weaker and apparent only below about 22 °C: 1.6% (1.0% to 2.2%) per 1 °C lower mean over lags 0–13 days. Pollutants were not associated with either subtype." (cited paper)

### Goggins and Chan 2017, *Int J Cardiol* 228:537–542 — DOI 10.1016/j.ijcard.2016.11.106

Verified against PubMed abstract (PMID 27875731). Say-map numbers correct; one additional verified sentence available:

- "During 2002–2011, the cumulative relative risk of HF admission comparing an 11 °C with a 25 °C day was 2.63 (2.43 to 2.84) over lags to 23 days; the corresponding HF mortality relative risk was 3.13 (1.90 to 5.16) over lags to 42 days." (cited paper)
- "Associations were stronger in older age groups and for new than recurrent hospitalisations; co-morbidities did not modify the association." (cited paper)

### Liu et al. 2020, *Sustain Cities Soc* 57:102131 — DOI 10.1016/j.scs.2020.102131 (live [12])

Verified against the published abstract (ScienceDirect blocked direct fetch; abstract obtained via Semantic Scholar). Confirmed AFs only:

- "During 2006–2016, cold accounted for a mortality attributable fraction of 4.72% versus 0.16% for heat; moderate non-optimum temperatures accounted for 4.25% versus 0.63% for extremes." (cited paper)
- "The temperature–mortality relation was reversed J-shaped; the largest relative risks appeared at extreme cold, led by injuries (RR 2.18, 95% CI 1.03 to 4.62), then respiratory and circulatory causes, over lags 0–21 days." (cited paper; new verified detail)
- MMT, cut-offs, knots, and full lag specification remain unverified — full PDF still not in hand.

### Liu et al. 2026, *medRxiv* — DOI 10.64898/2026.03.05.26347683 (live [13], preprint)

Verified against the medRxiv v1 page (posted 6 March 2026):

- "Model-based excess heat deaths in Hong Kong during 2014–2023 ranged from 1,455 (95% CI 1,098 to 1,812) to 3,238 (3,234 to 3,242) across four heatwave definitions; in 2023 the annualised excess death rate ranged from 2.95 (2.41 to 3.50) to 5.09 (5.07 to 5.12) per 100,000." (cited preprint)
- "Males and people aged 65 or older were disproportionately affected." (cited preprint)
- The preprint's own conclusion calls heat waves "among the top ten causes of death in Hong Kong … comparable to diabetes." Treat as preprint rhetoric; do not import into the live paper (see §3).

### Newly found local papers the project has not cited (2024–2026 window, plus one older anchor)

1. **Chau/Pun et al. 2025, *J Gerontol A* 80(4):glaf002 — DOI 10.1093/gerona/glaf002** (online 7 Jan 2025). Territory-wide hospitalisations 2012–2018, age ≥ 65, time-stratified case-crossover, HKO very-hot-day/hot-night definitions. Three consecutive very hot days were associated with cardiovascular admissions in community-dwelling older people (RR 1.09, 95% CI 1.03 to 1.14, lag 4); in old-age-home residents the association was larger and later (RR 1.28, 1.05 to 1.54, lag 18). Currently appears only inside Roro's medRxiv reference list; not in our evidence matrix. Directly relevant to the Introduction's heat–morbidity chain and to a Discussion sentence on frailty and delayed onset. (cited paper)
2. **EcoEnv 2025, *Ecotoxicol Environ Saf* — DOI 10.1016/j.ecoenv.2025.117827 (PMID 39904255).** HA emergency circulatory admissions 2004–2019 (1,276,632 EHAs): temperature-related AF 7.98% (5.24% to 10.58%) for admission counts and 13.09% (6.80% to 18.28%) for length of stay, with the lower-quartile cold range explaining over half. Uncited; a strong, recent, local cold–circulatory-hospitalisation burden anchor that complements Jasmine's mortality AFs. (cited paper)
3. **Tian, Qiu, Sun, Lin 2016, *Circ Cardiovasc Qual Outcomes* 9:135–142 — DOI 10.1161/circoutcomes.115.002410.** Older than the requested window but outcome-aligned and uncited: emergency circulatory admissions 2005–2012; optimum temperature 23.0 °C; cumulative RR 1.69 (1.56 to 1.82) for extreme cold and 1.22 (1.15 to 1.29) for moderate cold over lags 0–21; cold AF 6.33% (moderate) + 0.82% (extreme); no apparent heat effect. (cited paper)
4. Peripheral: *Urban Climate* 2024 asthma EHA/LOS (DOI 10.1016/j.uclim.2024.102240) — respiratory, not cardiac; list only if a respiratory contrast sentence is ever needed.
5. Already cited, not new: Guo et al. 2025 *Environ Sci Technol* 59:27107–27117 (DOI 10.1021/acs.est.5c10594) is in `literature/evidence_matrix.csv` and `references.bib`; Frontiers in Public Health 2024 TLOS (DOI 10.3389/fpubh.2024.1411137) is in `literature/pathway_evidence_memo.md`.

---

## 3. Facts the live paper MUST NOT say

Reinforces the say-map; each item verified against source today.

1. Do not quote Guo et al.'s per-10 °C·h CI as anything other than (0.2%, 3.5%) from Table 3 — and note the paper's own Results prose prints (0.2%, 3.6%). If a reviewer asks, cite Table 3. Do not average the two.
2. Do not mix Guo's 3.1% overall extreme-HNe estimate with the 4.3% circulatory per-10 °C·h estimate; different contrasts, different units.
3. Do not cite Guo's NCNE total inconsistently: the abstract says 5,002,114, the Results text says 5,002,144 (source typo). Use the abstract.
4. Do not call 2024 "the hottest year by hot-night count": 2024 was warmest by annual **mean** (24.8 °C) but had fewer hot nights (50) than 2021 (61), 2023 (56), and 2022 (52). Mean warmth ≠ extremes count.
5. Do not convert EPD endpoint changes (NO₂ −40%, PM2.5 −53%, O₃ +37%, 2013→2023) into claims about within-window year-by-year trends from our table; mid-series repo values differ from EPD network averages by station composition (§1c).
6. Do not import the medRxiv preprint's "top ten causes of death / comparable to diabetes" framing into the journal paper; it is unreviewed rhetoric, and its excess-death totals are model-transported, not observed.
7. Do not quote Jasmine's MMT, moderate/extreme cut-offs, or spline settings; only the four AFs and the reversed-J shape are verified. The injuries-first RR ordering (2.18, 1.03–4.62) is verified from the abstract but is not a circulatory estimate.
8. Do not present the J Gerontol A 2025 case-crossover RRs (1.09; 1.28) as comparable to our monthly count ratios; different design, age restriction (≥ 65), and lag structure.
9. Do not use the EcoEnv 2025 or Circ Outcomes 2016 circulatory AFs (7.98%; 6.33% + 0.82%) as if they were first-hospitalisation or T2D/HTN-cohort quantities; both are all-age emergency-admission attributable fractions from earlier periods.
10. Standing rules unchanged: no stroke coefficients, no AMI/principal-diagnosis framing for our outcome, no daily DLNM claims for our series, no mechanism claims (sleep, blood pressure, vasoconstriction) as results.

---

## 4. Public-data upgrades we could crawl next (proposals only — none implemented)

1. **Hourly HKO temperature for an HNe-style intensity metric.** Guo et al. show the official binary flag is null while hourly excess heat is not; an hourly crawl (HKO regional weather / API history) would let Hogan's locked definitions add an intensity column. This is Hogan's weather lock to give — proposed, not built.
2. **Extend the annual extremes table to 2024–2025.** 2024 verified today (50 HN, 52 VHD, 11 CD, 2 EHD; warmest year on record by mean). One-row extension of `hko_annual_extremes_2013_2023.csv` is trivial once the team wants post-window context; 2025's Year's Weather page should be checked when final.
3. **EPD EPIC by-station yearly CSVs.** A documented fixed-station panel (with the station list recorded in the schema) would explain the 2015–2016 NO₂/O₃ differences against EPD network averages and future-proof the pollution table.
4. **HKO warming-rate citation for the Introduction.** 0.35 °C per decade over 1996–2025 (HKO temperature page) is a cleaner local-warming sentence than a generic global preamble, if Hogan wants one.
5. **CHP / Centre for Health Protection cold- and heat-related public surveillance summaries** (e.g. weekly influenza-like-illness and heat-stroke reports) as contextual time series — only if a future pathway needs them; flu already covers 121/132 months.

## 5. Dead ends (do not re-walk)

- **PubMed web UI** blocks scripted fetch (cookie wall). Use NCBI E-utilities (`esearch`/`efetch`) — worked first try.
- **ScienceDirect DOI landing for SCS 102131** returns 406 to scripted fetch. Semantic Scholar's abstract sufficed for the four AFs; the full PDF (MMT, cut-offs, splines) remains unobtained — do not invent.
- **Guo et al. internal inconsistencies** (NCNE total 5,002,114 vs 5,002,144; per-10 °C·h CI 3.5% vs 3.6%): resolved by citing abstract/Table 3. Not worth an erratum hunt tonight.
- **EPD mid-year reconciliation**: the 2015–2016 NO₂/O₃ gaps are station-composition artefacts, not a data error; chasing exact per-station reproduction is low value until someone quotes mid-series years.
- **EHD counts for 2013–2022** are not in Year's Weather prose; only daily data would confirm. Not needed by the live paper.
- **HKO long-term extremes trend quantification** newer than Wong & Mok (1885–2008) was not found in citable prose form tonight; the direction statement on the HKO climate page plus the 0.35 °C/decade warming rate is sufficient for framing.

---

## 6. Rows for `analysis_plan/context_compound_log.md`

| Date | Mode | Spur / question | What we tried or noticed | Keep / drop / park | Promoted to? |
|---|---|---|---|---|---|
| 2026-08-13 | Explore | Do HKO yearbooks agree with our annual extremes table? | All six checked years (2013/2017/2019/2021/2023) match exactly; 2024 adds a verified public row (50 HN / 52 VHD / 11 CD); monthly panel sums to annual CSV 11/11 years | Keep | this memo; claim-ledger weather lines now yearbook-anchored |
| 2026-08-13 | Explore | Do EPD published averages agree with our pollution table? | Endpoints match EPD Annex 1 exactly (NO₂ 54→32, PM2.5 31→15, O₃ 43→58); 2015–16 NO₂/O₃ differ by station composition — not an error, but only endpoints should be quoted | Keep | this memo §1c |
| 2026-08-13 | Explore | Are the say-map literature numbers source-true? | Guo Table 3/Table 4, Goggins 2013/2012/2017 abstracts, Liu 2020 abstract, Liu 2026 medRxiv all re-verified; only wrinkle is Guo's internal 3.5% (Table 3) vs 3.6% (prose) CI — cite Table 3 | Keep | this memo §2; feeds say-map precision |
| 2026-08-13 | Explore | Any uncited 2024–2026 HK hot-night/cold-day hospitalisation papers? | Found two: J Gerontol A 2025 glaf002 (EHWE, 65+, CVD RR 1.09 lag 4; OAH 1.28 lag 18) and EcoEnv 2025 117827 (cold AF 7.98% circulatory EHA 2004–2019); plus older uncited Circ Outcomes 2016 cold-circulatory AF anchor | Keep | this memo §2; candidate Introduction/Discussion adds for the team |
| 2026-08-13 | Explore | Can we quantify the long-term HKO extremes trend for framing? | Direction confirmed on HKO climate page; warming 0.35 °C/decade 1996–2025; newer per-decade extremes rates not found in citable prose tonight | Park | this memo §5 |
| 2026-08-13 | Explore | Guo NCNE total and per-10 CI internally inconsistent | Abstract 5,002,114 vs Results 5,002,144; Table 3 CI 3.5% vs prose 3.6% — cite abstract/Table 3, do not blend | Drop (resolved) | this memo §3 |
