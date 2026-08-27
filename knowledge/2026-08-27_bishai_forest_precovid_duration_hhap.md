# Bishai comments on Figure 3 — pre-COVID, spline df, 5-day rule, heat-health planning

**Mode:** Explore + Teach + Ship.  
**Date:** 27 August 2026.  
**Audience:** Bob, then Bishai if Bob wants to walk it.  
**Provenance:** every count ratio below is `HA_APPROVED_AGGREGATE` from `outputs/tables/cvd_trend_depletion_sensitivity.csv` or named sibling tables. No new health model. Physiology is labelled **hypothesis**. Policy is labelled **routing**.  
**Rails:** Gate 3 remains open. All twelve Model 1 Benjamini–Hochberg *q*-values exceed 0.19 (minimum 0.192). Admission cause is absent. Stroke is not delivered. Daily coefficient recovery failed. This memo does not freeze a headline and does not change form 2a.

Peer audit (this session): Fable 5 (claim kill-list), Opus 5 (physiology register), Sol 5.6 (HHAP routing). Condensed in [`reports/bishai_forest_hhap_2026-08-27/peer_briefs.md`](../reports/bishai_forest_hhap_2026-08-27/peer_briefs.md).

---

## 1. Which forest he was looking at

He was looking at **live-manuscript Figure 3**, not the twelve-contrast core forest.

| Document | Name of this graph | Filename |
|:--|:--|:--|
| Live / Hogan PDF (the print copy) | Figure 3 | `figures/live_identification/figure_D_trend_depletion_sensitivity.png` |
| Validated release | figure 4 | `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.svg` |
| Integrated Bishai report | Figure 4 | same release file; that report’s Figure 3 is the core forest |

Y-axis labels on that graph: **Spline df 8**, **Spline df 6**, **Spline df 3**, **Pre-COVID**, **Baseline: spline df 4**.  
Panel titles: **Hot nights, per 5 days** and **Cold days, per 5 days**.

Those two facts explain the comment. “8 / 6 / 5 days splits” is a fusion of spline **degrees of freedom** 8 / 6 / 3 with the **per 5 days** reporting unit printed on every extreme-day panel. “6 spline above count ratio 1” is the 6-df time-trend sensitivity, not a six-day heatwave.

A relabelled teaching read (same numbers, new axis language) is [`reports/bishai_forest_hhap_2026-08-27/figure_teaching_spline_df_not_duration.png`](../reports/bishai_forest_hhap_2026-08-27/figure_teaching_spline_df_not_duration.png). It is an Explore figure. It does not replace Hogan’s live Figure 3.

---

## 2. What “pre-COVID” is, and why one interval does not include 1

**Definition (Methods).** Pre-COVID here is the **pre-2020 window**: January 2013–December 2019, **84 months**. It is one of nine trend/window/COVID-phase specifications. COVID-phase adjustment on the full 132 months uses five labelled phases (through January 2020; February 2020–December 2021; January–April 2022; May–December 2022; from January 2023). Neither is a causal COVID analysis. No multiplicity control was computed inside the 84-month window. No pre-2020 estimate is promoted beyond a sensitivity.

**The interval that does not include 1** on the panel he was almost certainly pointing at is **HF × official cold days**, not CHD × hot nights.

| Contrast | Full window (132 months, Model 1, NW6) | Pre-2020 (84 months, NW6) | Interval vs 1 |
|:--|:--|:--|:--|
| CHD · hot nights / 5 days | 1.022 (1.002–1.042) | 1.011 (0.991–1.032) | pre-2020 **includes 1** |
| HF · cold days / 5 days | 1.073 (1.006–1.144) | 1.113 (1.053–1.176) | pre-2020 **excludes 1** |

If the comment was “pre-COVID does not include 1 at all,” the honest referent is **1.113 (1.053–1.176)** for heart failure and cold days. That is a **winter / cold** residual, not a heat residual. CHD hot nights are weaker before 2020 and compatible with 1.

The same 84-month window moves more than those two cells. **Nine of twelve** Newey–West lag-6 intervals exclude 1, including inverse associations for all six continuous temperature contrasts (Supplementary Table S2). HF hot nights in that window are 0.965 (0.937–0.994): excludes 1 **below** 1. Do not over-read a post-hoc subwindow.

**Why the HF cold-day interval sits away from 1 before 2020 (fair, not proven).**

1. The full window includes pandemic-era care-seeking and service shocks. The months with largest Cook’s distance are February 2020 (CHD) and February 2022 (HF cold days).
2. Official cold days remain a winter exposure (141 of 145 days in December–February across 2013–2023). The contrast is identified **between winters**, not summer versus winter. Removing 2020–2023 does not create a summer comparison; it compares a shorter run of winters.
3. Residual autocorrelation is lower in the 84-month CHD hot-night fit (lag-1 ACF 0.171 versus 0.508 in the full window), so intervals can tighten for mechanical reasons as well as scientific ones.
4. The pre-2020 and full-period HF cold-day intervals **overlap**. The honest sentence is: the cold–HF residual does not depend on 2020–2023 for its sign. It is still unprotected by *q*, still ecological, and still a sensitivity.

---

## 3. Why 8 / 6 / 5 show different separation

They are not three duration encodings. They are **two axes on one figure**. Spline df is a time-trend control, not a heatwave duration.

| What the eye sees | What it is | What it is not |
|:--|:--|:--|
| Spline df 8 / 6 / 3 | Flexibility of the **calendar-time nuisance spline** (sensitivities to Model 1’s 4 df) | 8-day / 6-day / 3-day heatwaves |
| “per 5 days” in the panel title | Linear **reporting scale**: five additional official extreme days in a month. If the five-day count ratio is *R*, per three days is *R*^(3/5) and per one day is *R*^(1/5) | Consecutive duration; a 5-day warning rule |
| “6 spline above 1” | The 6-df **trend-control** refit of the **same** monthly hot-night or cold-day count | Evidence that six-day heat is uniquely toxic |

**CHD · hot nights / 5 days (NW6)**

| Specification | Count ratio | vs 1 | Lag-1 residual ACF |
|:--|--:|:--|--:|
| Time-trend spline, 3 df | 1.011 (0.990–1.032) | includes 1 | 0.595 |
| Model 1 (4 df) | 1.022 (1.002–1.042) | excludes 1 | 0.508 |
| Time-trend spline, 6 df | 1.024 (1.005–1.044) | excludes 1 | 0.444 |
| Time-trend spline, 8 df | 1.023 (1.005–1.042) | excludes 1 | 0.437 |
| Year fixed effects | 1.025 (0.9998–1.050) | includes 1 | 0.373 |
| Pre-2020 | 1.011 (0.991–1.032) | includes 1 | 0.171 |

Among spline-df scenarios, 6 df is the highest point estimate. Year fixed effects are slightly higher (1.0246 versus 1.0242) and the interval includes 1. Do not crown df 6.

**HF · cold days / 5 days (NW6)**

| Specification | Count ratio | vs 1 |
|:--|--:|:--|
| Time-trend spline, 3 df | 1.066 (1.005–1.131) | excludes 1 |
| Model 1 (4 df) | 1.073 (1.006–1.144) | excludes 1 |
| Time-trend spline, 6 df | 1.072 (1.005–1.143) | excludes 1 |
| Time-trend spline, 8 df | 1.062 (0.994–1.135) | **includes 1** |
| Year fixed effects | 1.061 (0.997–1.129) | includes 1 |
| Pre-2020 | 1.113 (1.053–1.176) | excludes 1 |

**Mechanical reading (identified as identification, not physiology).** First-event counts fall across 2013–2023 while official hot nights rise (10 in 2013, 61 in 2021, 56 in 2023; `REAL` HKO). Both lean on the same time smooth. A stiff 3-df spline leaves more of that shared decline in the residual, so the CHD hot-night coefficient shrinks toward 1. Once the trend has 4–8 df the estimate sits near 1.02 under Newey–West lag 6. At the other end, year fixed effects and the 8-df spline can absorb winter-to-winter variation that the HF cold-day contrast also uses; the HF interval then opens onto 1. Headline: the CHD hot-night residual is **trend-sensitive at the stiff end**; the HF cold-day residual is **trend-sensitive at the flexible end**. Neither pattern is a duration–response.

Same coefficient, other reporting scales (CHD hot nights, Model 1): per 1 day 1.004 (1.000–1.008); per 3 days 1.013 (1.001–1.025). Jingjing’s “why five not three?” question (KW15) is this rescaling. It is not a new model and not a 5-day rule.

---

## 4. Physiology — nights and consecutive strain, not spline df

**[IDENTIFIED]** Physiology cannot explain why a 6-df time spline sits above 1. That movement is a control-function diagnostic.

**[IDENTIFIED]** In the locked Model 1 panel, monthly **very hot day** counts sit at the null for both outcomes (CHD 0.999, 0.974–1.025; HF 0.995, 0.963–1.028). The heat residual that exists at all is **hot nights** for CHD, and it is SE-sensitive: model-based 1.022 (0.995–1.049) and HC1 1.022 (0.997–1.047) include 1; Newey–West lag 3 and lag 6 exclude 1 on the unrounded scale. Lag-1 residual ACF is 0.508. All twelve *q* > 0.19.

**[HYPOTHESIS]** Overnight heat is a different physiological object from a hot afternoon. A night with Tmin ≥ 28 °C truncates the usual nocturnal fall in blood pressure and fragments sleep, so the next day starts without full cardiovascular recovery. Unreplaced overnight fluid loss leaves a volume-contracted, haemoconcentrated morning. In people with type 2 diabetes and hypertension — this extract’s risk set — autonomic dysfunction and reduced coronary flow reserve shrink the margin between myocardial oxygen supply and demand. Under that account the damaging quantity is **unrecovered consecutive strain**, not a count of isolated hot nights. A monthly sum cannot tell five consecutive hot nights from five scattered ones, so a true consecutive-night effect would be attenuated. That is a reason the monthly very-hot-day counts can look flat even if daytime heat still matters in daily designs.

**[HYPOTHESIS]** There is no unique biological cliff at day 5 versus day 6 versus day 8. Thermoregulatory and sleep-recovery reserve depletes continuously. “About five days” is a **convention** for accumulated unrecovered strain, not a threshold the myocardium counts. Wang et al. (2019) operationalised ≥5 consecutive official very hot days or hot nights (and a 2-day/3-night compound) for Hong Kong **mortality**. Li et al. (2025) used ≥3 consecutive days above a calendar-day 90th percentile as an **atmospheric** heatwave. Chau and Pun (2025) reported CVD admission associations after **three** consecutive very hot days in people aged ≥65 (case-crossover; not this estimand). Guo et al. (2024) found official binary hot-night days often null for daily hospitalisation after mean-temperature adjustment, while a hot-night **excess** metric was associated. Those papers motivate watching **nights** and **runs**, not a claim that this monthly panel has identified a 5-day rule.

**[HYPOTHESIS]** Cold and heart failure are a different mechanism. Cold raises systemic vascular resistance and afterload; a ventricle without reserve decompensates. Goggins and Chan (2017) reported a daily cumulative RR of 2.63 (2.43–2.84) for 11 °C versus 25 °C over lags to 23 days in Hong Kong public-hospital HF. That magnitude is not transferable to 1.073 per five official cold days. Table 2 does not adjust for influenza. Official cold days sit in the same months as winter infection and winter behaviour. Describe the residual as **winter-clustered**, not as a thermal effect net of flu.

**[IDENTIFIED, Explore only]** Days inside ≥5-night hot-night spells (pathway P05, population×days offset, not Table 2) give CHD 1.005 (1.001–1.009) per spell-day. The 5VHD-month touch indicator `HM15` is 1.035 (0.960–1.116) with **seven** flagged months and is not Hogan-locked. Neither number validates a warning trigger.

---

## 5. Three meanings of a “5-day rule”

| Meaning | Status here | Policy consequence |
|:--|:--|:--|
| **Reporting scale** | Locked. Official counts enter Model 1 as `I(count/5)`. | Communicates a five-day contrast. Says nothing about whether the days are adjacent. |
| **Consecutive duration (Wang ≥5 VHD/HN; some European HHWS)** | Not identified. Monthly sums cannot test it. M\|D daily recovery failed. P05/HM15/HM17 are Explore. | Cannot license “N consecutive hot nights activates outreach” from this paper. |
| **Forecast logistics (WHO/WMO HHWS often 3–10 day lead; many systems 3–5 day outlook)** | Outside the extract. | A duration trigger is as much an operations parameter as a physiological one. |

Hong Kong’s own instruments are mostly **not** a numbered consecutive-day rule. The Very Hot Weather Warning is issued when the territory is expected to be generally threatened by very hot weather and is cancelled when that threat ends. While it is in force, HKO may add a **“Prolonged Heat”** special alert when “a few days” of very hot days or hot nights occur, and an **“Extremely Hot Weather”** tip near 35 °C (HKO educational article, December 2023). The Labour Department Heat Stress at Work Warning is a same-day Hong Kong Heat Index band. Department of Health heat-stroke advice already names heart disease and high blood pressure.

WHO/WMO warning-system guidance treats heatwaves as multi-day events (often at least two to three days) and records that some national systems use explicit consecutive-day rules. The Netherlands example in that guidance (>25 °C on five consecutive days) is a meteorological convention cited as precedent, not a finding from these hospital counts.

**Fair answer to Bishai.** There may be scientific truth in a **multi-day overnight** rule, because recovery fails across consecutive hot nights. This extract cannot say that the right number is 5 rather than 3 or 8, and it cannot say that Hong Kong should change the Very Hot Weather Warning. What it can say is that **night-time heat is the heat metric that moves in this panel**, daytime very-hot-day **monthly counts do not**, and **cold-season heart failure** is the more coherent residual.

---

## 6. Implications for heat-health planning (routing, not an evaluation)

Hong Kong does not publish a single WHO-branded municipal Heat–Health Action Plan as one document in the European-city sense. It has a **bundle**: VHWW, Hot Weather Special Advisory, Prolonged Heat / Extremely Hot Weather tips, HKHI, workplace warnings, DH/CHP advice, Home Affairs temporary heat shelters, and a separate Cold Weather Warning. This paper did not evaluate that bundle.

**Can inform (hypothesis-generating).**

1. Overnight heat deserves to stand beside daytime metrics in any review of heat-health messages for people with diabetes or hypertension. Official monthly very-hot-day counts were null here; hot nights were the only heat residual, and even that residual is SE- and period-sensitive.
2. A heat-only plan would miss the stronger residual in this extract: HF × official cold days, winter-identified, stronger before 2020. Cold Weather Warning and winter HF preparedness are the matching instruments.
3. The extract specifies what a **daily**, cause-recorded series would need to test duration triggers: consecutive versus scattered hot nights; hot-night excess versus binary HNday28 (Guo 2024); influenza-adjusted winter HF.

**Cannot inform.** Warning thresholds, a 5-day consecutive trigger, lead times, admissions averted, cooling-centre effects, cost-effectiveness, or a claim that existing warnings work or fail. All twelve *q* > 0.19. Gate 3 is open. Admission cause is absent.

**Three untested policy hypotheses (for Hogan / HKO / DH, not for the live Table 2).**

1. Cumulative hot nights add short-term health information beyond very-hot-day counts, VHWW status, or HKHI.
2. Additional outreach during **sustained hot nights** (HKO’s qualitative “Prolonged Heat” idea) may matter more for this cardiometabolic population than an extra daytime very-hot-day count.
3. Linked heat **and** cold activation pathways, with prospective winter HF surveillance, may fit Hong Kong better than a summer-only heat plan.

**Stage 3 / form 2a / Gate 3.** No change. This memo is commentary on a figure Bishai already has. It is not new evidence for endorsement and not a Gate 3 freeze.

---

## 7. What Bob can say aloud

> The rows that look like 8-, 6-, and 5-day splits are statistical controls — how flexible we let the long-term time trend be — and the “per 5 days” in the title is the reporting unit, five extra official hot nights or cold days in a month. There is no 6-day heatwave in that figure. The CHD hot-night estimate sits near 1.02 once the trend is flexible enough, but it is compatible with 1 with a stiff trend or in 2013–2019, and none of the twelve estimates survives multiplicity control. The interval that sits entirely away from 1 is heart failure and cold days before 2020: 1.113 (1.053–1.176). That is a cold result, not a heat one. A monthly panel cannot test a daily 5-day warning rule. The physiology that *would* motivate a multi-day night rule is failed overnight recovery, which is a hypothesis, not something these 132 months identify. For heat-health planning, the defensible message is that night-time heat and winter heart failure deserve attention in existing HKO/DH instruments, not that any threshold is validated.

Paste-ready short version: [`reports/bishai_forest_hhap_2026-08-27/TALKING_POINTS.md`](../reports/bishai_forest_hhap_2026-08-27/TALKING_POINTS.md).

---

## 8. Kill list (Fable)

Do not say: the 6-df spline is a 6-day heat effect; the figure compares 8/6/5-day heatwave definitions; this validates a 5-day warning; pre-COVID confirms the CHD hot-night effect; physiology explains df 6; pre-2020 is “the true effect”; Jasmine AFs or Roro excess deaths are these count ratios; Gate 3 is closed; Hong Kong has one named HHAP that this paper evaluated.

---

## 9. Sources (no new coefficients)

- Live Figure 3 caption and Methods: `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`
- Estimates: `outputs/tables/cvd_trend_depletion_sensitivity.csv`; Table 2 `outputs/release_chd_hf/tables/table2_core_models.csv`; S2 `manuscript/live_collaborative/supplement_live_track.md`
- Official extremes: `outputs/tables/exposure_aging/annual_extremes_and_spell_burden.csv` (`REAL` HKO)
- P05 / HM15: `outputs/tables/chd_pathway_panel_estimates.csv`; `outputs/tables/chd_hm_cm_panel_estimates.csv` (Explore; not Hogan-locked)
- Wang et al. 2019; Li et al. 2025; Guo et al. 2024; Goggins and Chan 2017; Chau/Pun 2025 — see `literature/final_methods_evidence_map.md`
- HKO: <https://www.hko.gov.hk/en/education/weather/hot-and-cold-weather/00706-Beware-of-Health-Effects-of-Extremely-Hot-Weather.html>
- WMO/WHO, *Heatwaves and Health: Guidance on Warning-System Development*
- WHO Europe HHAP guidance (2008; 2026 second-edition launch announced)
