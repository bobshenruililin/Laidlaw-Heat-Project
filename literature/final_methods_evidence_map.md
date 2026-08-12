# Final methods / evidence map — integrated report & manuscript

**Purpose:** One place that maps each essential source to a verified claim, its exact role in the final integrated report / journal-facing CHD–HF manuscript, and the misuse it must not support.  
**Verification date:** 2026-08-10 (Crossref / DOI content negotiation).  
**Authority files:** `literature/references.bib`, `literature/evidence_matrix.csv`, `literature/pathway_evidence_memo.md`, `literature/jasmine_liu2020_confirmed.md`, `literature/roro_revised_manuscript_audit_2026-08-10.md`, and the Stage-3 / final-protocol prose that will feed Hogan’s live manuscript.  
**Not references:** raw emails, Slack, and private PDF transfers are internal provenance only.

---

## Estimand firewall (read first)

| Claim class | What it is | What it is not |
|---|---|---|
| **Daily mortality AFs** | Population attributable fractions from a daily DLNM / quasi-Poisson mortality model (Jasmine 2020; Gasparrini multicountry framing) | Stroke, CHD, or HF monthly count ratios; “discoveries” from p-value counts |
| **Modeled excess deaths** | RR-transport / scenario excess mortality under named heatwave definitions (Roro medRxiv 2026) | New daily death–temperature regressions; Laidlaw hospitalisation results |
| **Monthly morbidity count ratios** | \(\exp(\beta)\) from monthly negative-binomial (or related) models of governed first-hospitalisation aggregates with a days (or days×population) offset | Incidence-rate ratios in a fully observed risk set; principal-diagnosis AMI; daily triggering RRs |
| **M\|D method-validation** | Basagaña–Ballester aggregated likelihood / constrained daily-exposure feasibility under synthetic calibration gates | Confirmatory daily DLNM at \(n=132\); automatic admission of real daily coefficients |

These four classes must never be collapsed into one coefficient sentence.

---

## Provenance that is not citable

| Internal item | Role | Manuscript rule |
|---|---|---|
| Covering emails from Roro / Bob / Hogan | Transfer provenance, date stamps, attachment inventory | Do not list in References |
| Private revised Roro PDF (`revised manuscript_clean.pdf` and byte-identical copies) | Internal methods audit only (`roro_revised_manuscript_audit_2026-08-10.md`) | Cite **medRxiv** DOI `10.64898/2026.03.05.26347683` (v1) for the public record; do not cite the private file in place of the preprint |
| Synthetic calibration CSVs / pilot failure notes | Methods feasibility evidence under `SYNTHETIC_CALIBRATION` | Label provenance; never report as HA findings |

---

## Evidence map

Columns: **source** | **verified claim** | **exact use in final report/manuscript** | **misuse warning**

| source | verified claim | exact use in final report/manuscript | misuse warning |
|---|---|---|---|
| Jingwen Liu et al. 2020 (`liu2020jasmine`; DOI 10.1016/j.scs.2020.102131) | HK daily mortality 2006–2016; DLNM + quasi-Poisson; reversed-J; cold AF **4.72%** vs heat **0.16%**; moderate AF **4.25%** vs extreme **0.63%** (headline AFs verified from locked secondary sources pending full-PDF transcription of MMT/splines) | Literature baseline for **daily mortality AFs**; motivates cold–hot symmetry and moderate-vs-extreme burden language; definition-harmonisation only where operators are source-locked | Do not treat AFs as stroke/CHD/HF effects, monthly count ratios, or evidence that heat “has more nulls.” Do not invent MMT, knots, or lag df before the full PDF/supplement is transcribed. |
| Zhenyuan Liu et al. 2026 medRxiv v1 (`liu2026roro`; DOI 10.64898/2026.03.05.26347683) **PREPRINT** | Model-based excess mortality 2014–2023 under four heatwave scenarios using transported local RRs; reported range **1,455–3,238** excess deaths across definitions | Named **modeled excess-death** companion / mortality-baseline family; motivates multi-definition sensitivity and absolute-burden communication | Not peer reviewed. Do not import RRs or death totals into monthly morbidity models. Do not cite the private revised PDF instead of medRxiv. Where revised text conflicts with Wang/Liu primaries, lock to primaries. |
| Wang et al. 2019 (`wang2019ehwe`; DOI 10.1016/j.scitotenv.2019.07.039) | EHWE morphology: VHD `Tmax≥33°C`, HN `Tmin≥28°C`, ≥5 consecutive VHD/HN spells, combined 2D3N/`NDNDN`; mortality associations in HK 2006–2015 | Exposure-definition spine for spell / compound monthly burdens (P05–P06; HM15/HM17/HM19 family); primary lock for Roro `HWD_Tmax/Tmin/Tcombined` operators | Mortality study. Spell operators must come from this paper, not from inconsistent secondary manuscript wording. |
| Li et al. 2025 (`li2025heatwaves`; DOI 10.1016/j.atmosres.2024.107845) | Atmospheric HK heatwaves: May–Sep; Tmax above calendar-day 90th percentile from a 15-day moving window; ≥3 consecutive days; merge nearby events (interval ≤2 days / ≤1 intervening non-hot day) | Motivates Hogan monthly adaptation (**count event starts → upper-tail month**, HM23); source-lock checklist before real association fitting | Atmospheric paper, not a health estimand. Monthly upper-tail counts are an adaptation, not a replication of the published event calendar. |
| Basagaña & Ballester 2024 (`basagana2024md`; DOI 10.1016/S2542-5196(24)00212-2) | Derives / evaluates aggregated-outcome likelihoods including **M\|D** (monthly outcome \| daily exposure) for temperature–mortality; weekly models track daily closely; monthly recovery is unbiased only with sufficient data and can show substantially higher variance | Cite for **M\|D method-validation** framing and clean-room equation inspiration; justifies attempting constrained daily-exposure recovery from monthly sums under calibration gates | Do not claim unqualified monthly unbiasedness. Their public code is unlicensed and must not be copied. Passing their mortality simulations ≠ automatic pass of this project’s CHD/HF calibration gates. Not a morbidity finding. |
| Basagaña & Ballester 2026 (`basagana2026md`; DOI 10.1097/EDE.0000000000001923) | Generalizes temporally aggregated-outcome estimation beyond the 2024 mortality setting | Cite for broader M\|D / aggregation methods scope in Methods | Methods paper only; does not validate any real Laidlaw coefficient. Crossref issued date-parts include 2025-10-02 while journal volume is 2026—use DOI + volume/issue. |
| Gasparrini et al. 2010 (`gasparrini2010`; DOI 10.1002/sim.3940) | Foundational DLNM methodology | Methods citation when discussing Jasmine’s daily DLNM architecture and why a full rich DLNM is prohibited at \(n=132\) months | Do not imply the monthly analysis is a DLNM. |
| Dunsmuir & Scott 2015 (`dunsmuir2015glarma`; DOI 10.18637/jss.v067.i07) | Observation-driven GLARMA models for count time series; `glarma` software | Cite for **negative-binomial GLARMA** serial-dependence ensemble (AR/MA orders frozen) | GLARMA is a robustness/serial-dependence model, not a second primary estimand or a causal claim. |
| Zhu 2011 (`zhu2011nbingarch`; DOI 10.1111/j.1467-9892.2010.00684.x) | Negative-binomial integer-valued GARCH (NB-INGARCH) for overdispersed counts | Cite only if NB-INGARCH / related count dependence is discussed as methodological context for overdispersed serial counts | Not interchangeable with GLARMA; do not claim NB-INGARCH was fitted unless it actually appears in the frozen registry. |
| Lazarus et al. 2018 (`lazarus2018har`; DOI 10.1080/07350015.2018.1506926) | Practical recommendations for HAR / HAC inference | Cite for reporting HC / Newey–West-style intervals alongside model-based SEs without p-hunting on interval choice | Do not select the interval that excludes the null. |
| Politis & Romano 1994 (`politis1994bootstrap`; DOI 10.1080/01621459.1994.10476870) | Stationary bootstrap for dependent data | Cite for serial-dependence-preserving null / max-statistic calibration on the specification curve | Ordinary i.i.d. bootstrap is inadequate for the monthly residual dependence setting. |
| Simonsohn et al. 2020 (`simonsohn2020speccurve`; DOI 10.1038/s41562-020-0912-z) | Specification-curve analysis | Cite for frozen specification-curve reporting (median, IQR, sign stability; no counting of “significant” models) | The curve is descriptive of a predeclared universe; it is not a discovery engine. |
| Tashman 2000 (`tashman2000rolling`; DOI 10.1016/S0169-2070(00)00065-0) | Rolling-origin / out-of-sample forecast evaluation review | Cite for **rolling-origin** predictive protocol (with LOYO) using log-score / deviance / MAE | Predictive log-score gains are not causal evidence. |
| Greenland & Morgenstern 1989 (`greenland1989ecological`; DOI 10.1093/ije/18.1.269) | Ecological bias, confounding, and effect modification in aggregate data | Cite in Limitations for ecological / aggregate association limits | Does not license individual-level causal claims from monthly aggregates. |
| Goggins et al. 2012 (`goggins2012stroke`; DOI 10.1007/s00484-011-0491-9) | Daily HK stroke admissions 1999–2006; HS inverse-T; IS weaker / threshold ~22°C | Historical **daily stroke morbidity** baseline; motivates cold co-primary and subtype/sex questions **if** data exist | Daily coefficients ≠ monthly count ratios. Current CHD/HF file is not stroke. |
| Goggins and Chan 2017 (`goggins2017hf`; DOI 10.1016/j.ijcard.2016.11.106) | Daily HK public-hospital HF admissions and deaths 2002–2011; cumulative RR 2.63 (2.43–2.84) for 11 °C vs 25 °C over lags to 23 days | Historical **daily HF** motivation for retaining cold in the HF arm | Daily cumulative RR ≠ monthly count ratio per five official cold days. Present event has no recorded admission cause. |
| Chan / Goggins et al. 2013 (`chan2013bullwho`; DOI 10.2471/BLT.12.113035) | HK admissions rise with heat above ~29°C and with cold | Supports continuous temperature pathways as first-class | Earlier decade; not CHD/HF monthly first-event aggregates. |
| Guo et al. 2017 (`guo2017ehp`; DOI 10.1289/EHP1026) | Multicountry heatwave–mortality estimates vary across percentile × duration grids | Motivates multi-definition heatwave-month panel (P07) | Definition multiplicity is methodological, not a licence for ten press releases. |
| Guo et al. 2024 (`guo2024hotnights`; DOI 10.1016/j.lanwpc.2024.101168) | Hot-night *excess* associated with hospitalisation; official binary HNday28 often null | Retain official HN counts while examining intensity/persistence separately | Broad hospitalisation, not diagnosis-specific monthly first events. |
| Guo et al. 2025 (`guo2025temppollution`; DOI 10.1021/acs.est.5c10594) | Pollution can amplify temperature–hospitalisation associations in HK | Staged pollution adjustment (NO₂/PM then O₃ last) | Do not dump all pollutants at once into \(n=132\) models. |
| Yang / Chong et al. 2025 (`yang2025coldflu`; DOI 10.1007/s00484-025-02870-2) | Weekly cold + influenza associated with stroke admissions (long HK series) | Pre-specified influenza sensitivity for cold models | Weekly pooled stroke ≠ monthly CHD/HF first-hospitalisation count ratios. |
| Gasparrini et al. 2015 (`gasparrini2015`; DOI 10.1016/S0140-6736(14)62114-0) | Globally, most attributable mortality from moderate non-optimum temperature; cold > heat | Framing companion to Jasmine’s moderate-vs-extreme AF contrast | Multicountry mortality AFs are not local morbidity effects. |
| Lam et al. 2018 (`lam2018amiDiabetes`; DOI 10.1371/journal.pmed.1002612) | Temperature–AMI associations modified by diabetes status (daily) | Optional effect-modification precedent if comorbidity strata exist | Not currently an analysis-of-record claim for the governed aggregates. |
| Bhaskaran et al. 2013 (`bhaskaran2013`; DOI 10.1093/ije/dyt092) | Tutorial on time-series regression in environmental epidemiology | Methods pedagogy / design citation | Tutorial ≠ project-specific result. |
| Ye et al. 2012 (`ye2012`; DOI 10.1289/ehp.1003198) | Review distinguishing temperature–morbidity from mortality evidence | Supports morbidity-vs-mortality wording in Introduction/Discussion | Review-level only. |
| HKO Year’s Weather notes (`hko2013`, `hko2021`) | Official annual extreme-day counts | Context for official VHD/HN/cold-day indicators | Yearbooks are not epidemiologic effect estimates. |

---

## How each claim class appears in the final write-up

1. **Daily mortality AFs** — Introduction / evidence spine only (Jasmine; Gasparrini 2015). Numbers stay labelled as mortality AFs.
2. **Modeled excess deaths** — Companion baseline paragraph (Roro medRxiv). Range illustrates definition sensitivity; labelled model-based / RR-transport.
3. **Monthly morbidity count ratios** — Results tables for CHD/HF amended-core and robustness/GLARMA ensemble. Report \(\exp(\beta)\) with multiplicity discipline; Gate 3 freezes headlines.
4. **M\|D method-validation** — Methods and (if gates fail) a documented feasibility failure; real daily-exposure coefficients enter Results only after Section-8 calibration gates in `final_reanalysis_protocol_2026-08-10.md`.

---

## Deduplication notes (this pass)

| Issue | Resolution |
|---|---|
| `wang2014hotspell` vs `wang2019ehwe` (same PMID 31302556) | Keep **`wang2019ehwe`** only |
| `wang2025coldflu` key but Yang first author | Canonical key **`yang2025coldflu`**; thin `.bib` alias `wang2025coldflu` kept for existing `\citep{wang2025coldflu}` call sites |
| Incomplete `cho2024` / `liu2025` matrix stubs | Replaced with verified `cho2024korea` / `liu2025tianjin` |
| Roro author Crossref inversion (`Yurika, Kawasaki`) | BibTeX uses **`Kawasaki, Yurika`** with explicit note |
| Private revised manuscript vs medRxiv | Public cite = medRxiv v1 only |

---

## Still uncertain / pending human or PDF locks

| Item | Status |
|---|---|
| Jasmine full PDF: exact MMT, moderate/extreme cutoffs, spline/lag df, full cause tables, derivation of 30.60°C and lag-phase RRs used by Roro | **Pending full-PDF transcription**; headline AFs above remain usable with that caveat |
| Roro revised PDF vs medRxiv v1 numeric/operator deltas | Audited privately; **do not cite private PDF**; operators locked to Wang/Liu/Li primaries where conflict |
| Basagaña 2026 “year” | Journal volume **2026**; Crossref issued date-parts include **2025-10-02** |
| Zhu 2011 “year” | Journal volume **2011**; Crossref issued date-parts include **2010-09-02** |
| Tian/Qiu 2023 TV and Frontiers 2024 TLOS rows in older pathway memo | Used in pathway motivation; **not** re-verified in this essential-spine pass—add to `.bib` only after a dedicated Crossref check if cited in the final manuscript |
| Outcome column meaning (`inpatient` inference) and stroke-file absence | Human/governance facts, not bibliographic |
