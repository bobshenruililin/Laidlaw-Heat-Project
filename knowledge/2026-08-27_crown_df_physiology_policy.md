# Crown among 5, 6, and 8 — identification, physiology, and social-impact routing

**Mode:** Explore + Ship.  
**Date:** 27 August 2026.  
**Audience:** Bishai first; Bob if he wants to walk it.  
**Provenance:** every count ratio is `HA_APPROVED_AGGREGATE` from `outputs/tables/cvd_trend_depletion_sensitivity.csv` or a named sibling table. No new health model. Physiology is labelled **hypothesis**. Policy is labelled **routing**.  
**Rails:** Gate 3 remains open. All twelve Model 1 Benjamini–Hochberg *q*-values exceed 0.19 (minimum 0.192). Admission cause is absent. Stroke is not delivered. Daily coefficient recovery failed. Table 2 remains Model 1 (4-df spline). Form 2a is unchanged.

Scoring script: [`scripts/67_crown_spline_df_score.py`](../scripts/67_crown_spline_df_score.py).  
Table: [`reports/crown_df_physiology_2026-08-27/spline_df_joint_score.csv`](../reports/crown_df_physiology_2026-08-27/spline_df_joint_score.csv).  
Figure: [`reports/crown_df_physiology_2026-08-27/figure_joint_headline_vs_trend_df.png`](../reports/crown_df_physiology_2026-08-27/figure_joint_headline_vs_trend_df.png).  
What to say: [`reports/crown_df_physiology_2026-08-27/TALKING_POINTS.md`](../reports/crown_df_physiology_2026-08-27/TALKING_POINTS.md).

This memo revises one sentence in the 27 August mapping note. That note said “do not crown df 6” because 6-df must not replace Table 2. Bishai then asked to crown one of 5, 6, and 8. The crown below is **robustness among more-flexible splines**. It is not a new primary model.

---

## 0. The sentence

**Among 5, 6, and 8, crown 6 — and name the object.** Six is the time-trend spline with 6 degrees of freedom. It is the only specification more flexible than Model 1 that still keeps both exploratory headlines away from 1. Five is not a spline. Five is the reporting scale already in Table 2, `I(count/5)`. Eight is the flexible end that opens the stronger residual — heart-failure cold days — onto 1.

Table 2 stays Model 1 (4 df). All twelve *q*-values still exceed 0.19. Physiology does not put a cliff at day 6. Social impact that is fair is night-time heat for first CHD events and winter cold for first HF events in a diabetes/hypertension population. It is not a validated warning trigger, and it is not admissions averted.

---

## 1. Three objects, not one ladder

Bishai’s “df 5, 6, 8” is still the Figure 3 fusion. Score each object separately. Do not collapse them.

| Number | What it is in this analysis | What it is not |
|:--|:--|:--|
| **5** | Model 1 reporting scale: official day counts divided by five, so the count ratio is per five additional such days in the month. Also, in other literatures: Wang and colleagues’ ≥5 consecutive very-hot-days / hot-nights *mortality* convention, and the Dutch meteorological heatwave (≥5 summer days). | A 5-df spline. There is no 5-df spline in this panel. Model 1 is **4 df**. Sensitivities are **3, 6, 8**. Not a consecutive-day warning identified from 132 months. |
| **6** | Time-trend spline **6 df**, a sensitivity to Model 1’s 4-df natural cubic spline of calendar time. | A 6-day heatwave. A physiological duration. A confirmatory primary. |
| **8** | Time-trend spline **8 df**. | An 8-day heatwave. A better “more significant” model. |

The pre-specified paper specification is already crowned: **4 df**. That is not on Bishai’s list. The forced choice among 5 / 6 / 8 is therefore: **6 as robustness**, **5 as the scale already used to report Table 2**, **8 as the bound that must not be crowned**.

---

## 2. Joint-score analysis

Source: `outputs/tables/cvd_trend_depletion_sensitivity.csv`, Newey–West lag 6, 132 months unless noted. Headlines: CHD × official hot nights / 5 days, and HF × official cold days / 5 days. “Joint preservation” means **both** of those intervals exclude 1.

| Specification | CHD hot nights | HF cold days | Both headlines? | Exclusions among 12 | CHD lag-1 ACF |
|:--|:--|:--|:--|--:|--:|
| Time-trend spline, 3 df | 1.011 (0.990–1.032) includes 1 | 1.066 (1.005–1.131) excludes | no | 1 | 0.595 |
| **Model 1, 4 df** | **1.022 (1.002–1.042) excludes** | **1.073 (1.006–1.144) excludes** | **yes** | 2 (exactly the two headlines) | 0.508 |
| **Time-trend spline, 6 df** | **1.024 (1.005–1.044) excludes** | **1.072 (1.005–1.143) excludes** | **yes** | 2 (exactly the two headlines) | 0.444 |
| Time-trend spline, 8 df | 1.023 (1.005–1.042) excludes | 1.062 (0.994–1.135) **includes 1** | no | 2 (CHD hot nights **and** HF mean Tmin below 1) | 0.437 |
| Year indicators | 1.025 (0.9998–1.050) includes 1 | 1.061 (0.997–1.129) includes 1 | no | 3 (HF mean T / Tmax / Tmin inverse only) | 0.373 |

Rule, written before looking at a favourite number: among specifications **more flexible than Model 1**, crown the unique spline that still preserves **both** headlines. That rule returns **6 df** and only 6 df. The script [`scripts/67_crown_spline_df_score.py`](../scripts/67_crown_spline_df_score.py) fails if any other more-flexible spec also preserves both, or if 6 df does not.

AIC by spline df cannot be computed here. The governed analysis panel is not in this workspace, and the original trend-sensitivity table did not store AIC. Model 1 4-df AIC exists only for the locked core fits (`outputs/tables/cvd_core_model_fit.csv`; CHD hot-nights days-offset AIC 1617.99). Do not invent missing AIC.

---

## 3. Why 6 is “really good” — and the limits of that sentence

What 6-df actually does, on this table:

1. It is the only spline **more flexible than Model 1** that still carries both residuals.
2. The points barely move: CHD hot nights 1.022 → 1.024; HF cold days 1.073 → 1.072.
3. CHD lag-1 residual autocorrelation falls from 0.508 to 0.444. Serial dependence is part of the CHD inferential problem; a drop in ACF is a reason to take 6-df seriously as a robustness check, not a reason to call the CHD residual confirmatory.
4. The two exclusions among twelve contrasts remain **exactly the two headlines**. The specification does not buy the headlines by lighting up the other ten cells.

What 6-df does **not** do:

- It does not create multiplicity protection. *q* is still > 0.19 on Model 1; no new *q* was computed inside the sensitivity grid.
- It does not repair CHD standard-error discordance. Model-based and HC1 intervals for CHD hot nights still include 1 on Model 1.
- It does not repair the pre-2020 CHD hot-night interval, which includes 1 (1.011, 0.991–1.032).
- It does not identify consecutive nights, a warning threshold, or a physiological duration.
- It does not replace the pre-specified 4-df spline in Table 2.

The identification reading, already in the live Discussion, is unchanged: first-event counts fall by about half while official hot nights rise from 10 (2013) to 61 (2021) and 56 (2023). The same time smooth absorbs both. CHD hot nights are sensitive at the **stiff** end (3 df opens that interval onto 1). HF cold days are sensitive at the **flexible** end (8 df opens that interval onto 1). Six df sits in the band where both residuals still exclude 1. That is a property of the nuisance smooth, not of myocardium.

---

## 4. Why not 8, not 3, not year indicators, not 5-as-spline

**Do not crown 8.** It is the flexible bound that opens the more coherent residual. HF cold days are concordant across all four Model 1 standard-error constructions; CHD hot nights are not. A specification that keeps the SE-sensitive residual and gives up the SE-concordant residual is the wrong robustness winner.

**Do not crown 3.** It is the stiff bound that opens CHD hot nights onto 1. CHD lag-1 ACF is worst there (0.595).

**Do not crown year indicators for the headlines.** They produce the highest CHD hot-night point (1.025) and include 1 for **both** headlines. They also produce three inverse continuous-temperature exclusions for HF. That is a different pattern, and it is not the paper’s two residuals.

**Do not crown a 5-df spline.** None exists. Inventing one in conversation is how 5, 6, and 8 got fused on Figure 3.

---

## 5. What “5” can honestly mean

Three different fives. Keep them apart.

### 5a. Reporting scale (already in Table 2)

Official counts are entered as `I(count/5)`. If the five-day count ratio is *R*, the same coefficient per three days is *R*^(3/5) and per one day is *R*^(1/5). For Model 1 CHD hot nights: per five nights 1.022 (1.002–1.042); per three nights 1.013 (1.001–1.025); per one night 1.004 (1.000–1.008). Jingjing’s KW15 question is answered by that rescaling. It is not a duration rule.

### 5b. Consecutive-night mortality convention in Hong Kong (not this panel)

Wang, Lau, Ren and colleagues analysed daily all-cause mortality in Hong Kong, 2006–2015 (Wang et al., *Sci Total Environ* 2019;690:923-931). A single hot night was associated with +2.43% (0.75–4.14%) mortality. Five or more consecutive very hot days: +3.99% (0.56–7.53%). Five or more consecutive hot nights: +6.66% (3.45–9.96%). Among day–night combinations, **2D3N** was strongest at +5.32% (1.83–8.93%) and lagged about five days. They named 5 very-hot-days, 5 hot-nights, and 2D3N as representative extremely hot weather events. That is **daily mortality**, not monthly first CHD/HF hospitalisation in a diabetes/hypertension cohort.

Ho, Lau, Ren and Ng characterised prolonged heat in the same city (Ho et al., *Int J Biometeorol* 2017;61:1935-1944). After **five consecutive hot nights**, all-cause mortality was +7.99% (7.64–8.35%) and cardiovascular mortality +7.74% (6.93–8.55%). Consecutive hot *days* were not significantly associated. Non-consecutive heat was associated at lag 0–1. Again: mortality, not this estimand.

Those papers are the local reason a scientist would **watch** ≥5 consecutive nights. They are not a trigger this monthly panel validated.

### 5c. The 2018 exhibit that monthly 5 ≠ consecutive 5

In 2018 Hong Kong recorded **26 official hot nights** and **zero days** inside a ≥5 consecutive-night spell (`outputs/tables/exposure_aging/annual_extremes_and_spell_burden.csv`). Across 2013–2023, 449 hot nights, 195 (43.4%) sat inside ≥5-night spells; 421 very hot days, 183 (43.5%) inside ≥5-day spells. A month can be heavy in official hot nights without a five-night run.

Explore-only duration proxies, not Table 2, not Hogan-locked:

| Object | CHD | HF | Limit |
|:--|:--|:--|:--|
| P05 days in ≥5 hot-night spells (per spell-day; population × days offset) | 1.005 (1.001–1.009) | 0.997 (0.991–1.003) includes 1 | Different offset from Model 1; not a warning rule |
| P05 days in ≥5 very-hot-day spells | 0.996 (0.991–1.000) | 1.000 (0.994–1.006) | Near null |
| HM15 (month touches a ≥5 very-hot-day spell) | 1.035 (0.960–1.116) | 1.004 (0.893–1.129) | **Seven months** only |

P05 CHD hot-night-spell days excluding 1 is motivation for **daily cause-recorded data**, not a crowned Table 2 contrast.

---

## 6. Physiology literature — nights, not a 6-day cliff

The biological question that would make a duration rule worth testing is overnight recovery, not spline df.

**Sleep onset is coupled to a nighttime fall in core temperature.** Chevance, Minor, Vielma and colleagues’ systematic review of ambient heat and sleep (Chevance et al., *Sleep Med Rev* 2024;75:101915) collects the evidence that hotter nights shorten sleep, fragment it, and disturb architecture. That review is about sleep, not hospitalisation.

**A few consecutive hot nights can leave core temperature high into the recovery period.** Ioannou, Tsoutsoubi, Mantzios and colleagues confined seven young healthy men for ten days (Ioannou et al., *Appl Physiol Nutr Metab* 2024;49:1394-1408). Nights 4–6 were 26.3 °C; nights before and after were 22.3 °C. Mean nocturnal core temperature was 0.2 °C higher during **and after** the three hot nights than before them, more so in the first two hours of sleep (+0.3 °C). Total sleep time fell by 14 minutes per 0.1 °C rise in overnight core temperature. This is not T2D/HTN, not Hong Kong, not hospitalisation, and not a 5-versus-6-versus-8 comparison. It is laboratory support for *non-recovery across consecutive nights*.

**Bedroom heat in older adults is associated with autonomic strain.** O’Connor, Bach, Forbes and colleagues monitored 47 community-dwelling adults aged ≥65 years in southeast Queensland across one summer (O’Connor et al., *BMC Med* 2025;23:703). Relative to nights <24 °C, bedroom temperatures of 24–26 °C, 26–28 °C, and 28–32 °C had odds ratios 1.4 (1.2–1.6), 2.0 (1.8–2.3), and 2.9 (2.5–3.4) for a clinically relevant drop in lnRMSSD, with higher heart rate and a shift toward sympathetic dominance. Hong Kong’s official hot night is Tmin ≥ 28 °C outdoors. That is not the same as a 24 °C bedroom. The paper is observational, Australian, and not a first-event CHD series. It is a reason to take **indoor night temperature** seriously as a hypothesis, including in a city whose official hot-night count rose from 10 to 61 in a decade.

**The sleep–CVD mediating literature is thin and mixed.** Ashe, Wozniak, Conner and colleagues’ scoping review of extreme heat, sleep, and cardiovascular measures found **three** eligible studies (Ashe et al., *Syst Rev* 2025; DOI 10.1186/s13643-024-02742-7). Blood pressure did not move in one direction: some analyses showed lower diastolic pressure in the heat, others a short-term systolic rise. No study demonstrated that sleep mediates a heat–hospitalisation path. Do not tell a clean “hot nights abolish nocturnal dipping, therefore CHD admissions” story from this panel or from that review.

**Local hospitalisation evidence already in the live paper remains the right neighbour, not a replication.** Guo, Chan, Qiu, Wong and Ho found that after adjustment for multi-day mean temperature, the official hot-night *flag* was null for non-cancer, non-external emergency hospitalisation in Hong Kong, 2000–2019, while hourly nighttime excess heat was associated, including +3.1% (1.5–4.8%) at its extreme and +3.4% (0.2–6.8%) for circulatory admissions (Guo et al., *Lancet Reg Health West Pac* 2024;51:101168). Official monthly counts are coarser than that hourly metric. Goggins and Chan’s daily heart-failure relative risk of 2.63 (2.43–2.84) comparing 11 °C with 25 °C is a different estimand from 1.073 per five official cold days (Goggins and Chan, *Int J Cardiol* 2017;228:537-542).

**There is no myocardial threshold at 5 versus 6 versus 8 days.** Wang’s five is an empirical mortality convention in this city. Ho’s five is the same city’s consecutive-night mortality contrast. The Dutch meteorological heatwave is ≥5 consecutive summer days ≥25 °C of which ≥3 are ≥30 °C, identified *after the fact*. The Dutch National Heatwave Plan is activated on *forecast*, often from **four** days with Tmax >27 °C, and it also uses night temperature and humidity (RIVM). Operations chose 4 because a 5-day meteorological definition is too late for carers. That is the opposite of discovering a biological cliff at 6.

Physiology therefore supports: (i) nights rather than monthly very-hot-day counts; (ii) consecutive nights as a **hypothesis** for failed overnight recovery; (iii) indoor temperature as a plausible exposure the outdoor official count only proxies. Physiology does **not** support crowning spline df 6, and it does not support adopting a 5-day HKO trigger from 132 monthly counts.

---

## 7. Policy and social impact that this panel can lend

Hong Kong already has a **bundle**, not one WHO-branded municipal Heat–Health Action Plan evaluated here: Very Hot Weather Warning (not a fixed consecutive-day rule), Hot Weather Special Advisory, a “Prolonged Heat” educational tip when “a few days” of very hot days or hot nights occur, Extremely Hot Weather around 35 °C, Hong Kong Heat Index / Labour same-day action, Department of Health advice that already names heart disease and hypertension, and a separate Cold Weather Warning.

Fair routing, if Bishai wants a social-impact sentence:

1. **The population is already the policy population.** First hospitalisation after first CHD or HF diagnosis among people with type 2 diabetes and/or hypertension is closer to a primary-prevention / high-risk-chronic-disease frame than all-cause mortality. DH materials already name heart disease and hypertension. This paper does not need a new named group. It needs not to over-claim.
2. **Night-time heat is the CHD residual; daytime official very-hot-day counts are not.** CHD very hot days: 0.999 (0.974–1.025). CHD hot nights: 1.022 (1.002–1.042) under NW6, *q* = 0.192, SE-sensitive, pre-2020 compatible with 1. The honest policy hypothesis is overnight heat information (including intensity, as in Guo et al.), not a new very-hot-day threshold.
3. **Winter heart failure is the more coherent residual.** 1.073 (1.006–1.144) per five official cold days; pre-2020 1.113 (1.053–1.176); all four SE constructions exclude 1; 141 of 145 official cold days fall in December–February. Heat-only summer planning would miss the stronger signal in this file.
4. **Duration is a hypothesis for daily data, not a knob to turn on this forest.** Wang/Ho give a local mortality reason to test ≥5 consecutive hot nights if a daily cause-recorded series is obtained. 2018 (26 hot nights, zero 5-night spells) is the exhibit that a monthly five-day scale cannot do that test. HKO’s “Prolonged Heat” tip already speaks of “a few days.”
5. **Housing and night cooling are the social lever that physiology actually points to**, via O’Connor et al. (bedroom ≥24 °C) and Guo et al. (hourly excess), not via spline df. This panel cannot measure indoor temperature, air-conditioning, or housing quality.

What must not be said for impact:

- Admissions averted.
- A 5-, 6-, or 8-day warning should be adopted or retired.
- Existing HKO/DH/Labour warnings work or fail.
- Gate 3 is closed.
- 6-df is physiology.
- CHD hot nights are confirmed by pre-2020.

---

## 8. Kill list

| Claim | Status |
|:--|:--|
| 5, 6, and 8 are three heatwave durations | Dead. Spline df + reporting scale. |
| There is a 5-df spline | Dead. |
| Crown 8 because ACF is lowest | Dead. It opens HF cold days onto 1. |
| Crown 6 as Table 2 / confirmatory primary | Dead. Table 2 stays 4 df. *q* > 0.19. |
| Crown 6 because it is a 6-day biological threshold | Dead. |
| Exclude-1 on a sensitivity is truth | Dead. CHD is still SE-sensitive; pre-2020 CHD includes 1. |
| P05 / HM15 belong in Table 2 | Dead. Explore; HM15 has seven months. |
| Wang 2019 / Ho 2017 replicate this CHD/HF panel | Dead. Daily mortality ≠ monthly first events. |
| Guo 2024 is contradicted by monthly official counts | Dead. Different encoding and outcome. |
| This analysis evaluated Hong Kong’s warnings | Dead. |
| Admissions would fall if a 5-night rule were added | Dead. |

---

## 9. What this does not change

- Table 2, Abstract, Hogan’s HKO weather paragraph.
- Stage 3 hashes `605cd8db43072cb5` / `a972206e61932650`.
- Form 2a (still the Stage 3 essay).
- Gate 3 (open; lead recommendation remains Option A).
- Live Figure 3 (already rebuilt; this diagnostic figure is a `reports/` object, not a paper figure).

The live Results may add one sentence that 6-df is the only more-flexible spline preserving both residual intervals. That sentence does not replace “No trend specification is preferred over the 4-df spline in Model 1.”

---

## 10. Next executable step that does not invent missing data

Walk Bishai through [`TALKING_POINTS.md`](../reports/crown_df_physiology_2026-08-27/TALKING_POINTS.md) and the diagnostic figure. Do not refit Model 1. Do not change Stage 3 PDFs. If he accepts 6-df as the named robustness check, paste the optional Results sentence; do not move Table 2. The test of consecutive nights waits on daily cause-recorded data from Roro / HA, which this night cannot produce.
