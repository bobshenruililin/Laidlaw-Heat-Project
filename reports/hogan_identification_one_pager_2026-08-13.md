# Identification one-pager for Hogan — 13 August 2026

**Use:** meeting card, not a live-file paste and not a new Table 2.  
**Provenance:** `HA_APPROVED_AGGREGATE` / `REAL` tables already in the repo. Weather Methods remain yours. Reference period for HM/CM remains unlocked.

---

## What the live paper’s cold-day contrast is actually identified from

Official cold days 2013–2023: **145 total; 141 in December–February** (Dec 40, Jan 54, Feb 47; Mar 4). After calendar-month indicators, remaining variation is **between-year winter**, not summer versus winter. Figure 2 in the paste pack is this heatmap.

A winter-only restriction is a labelled sensitivity, not a remedy.

## What the live paper’s hot-night contrast is actually identified from

Official hot nights: **10 (2013) → 61 (2021) → 56 (2023)** (`REAL` HKO; 2013 was about seven days below the 1981–2010 normal). First-event CHD counts: **23,830 → 12,323** over the same years, while C&SD population 35+ rose ~17%. Both the exposure and the outcome trend; both lean on the same 4-df time spline.

Under that encoding, the CHD hot-night count ratio is compatible with 1 **before 2020** and under COVID-phase adjustment (`cvd_trend_depletion_sensitivity.csv`, Newey–West lag-6):

| Window | Count ratio (95% CI) |
|---|---|
| Pre-2020 (84 months) | **1.011 (0.991–1.032)** |
| COVID-phase adjusted (132 months) | **1.013 (0.994–1.033)** |
| Analysis of record (132 months, NW6) | **1.022 (1.002–1.042)** |

The association is confined to specifications that include 2020–2023. That is a fact about official monthly counts, not a reason to swap in hourly excess heat unless you rewrite weather.

## Why Newey–West is not “the wider, safer interval” here

CHD hot nights, analysis of record (`table4_uncertainty_ladder.csv`):

| Model | HC1 | NW3 | NW6 |
|---|---|---|---|
| 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.0003–1.0439) | 1.022 (1.002–1.042) |

The robust intervals **narrow**. Residual ACF1 is 0.508, so serial dependence is real; the usual “HAC widens” expectation fails for this contrast. HF cold days do widen (Model 1.023–1.125 → NW6 1.006–1.144). The live Discussion now states the CHD direction as caution, not confirmation.

If the shared file is crowded, demote the residual-ACF figure and use `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png` instead. It shows the pre-2020 CHD interval including 1.

## Guo 2024 vs our encoding (open question W10)

Guo et al. (daily hot-season emergency hospitalisation, 2000–2019): official `HNday28` **null** after mean-temperature adjustment (−0.2%, −1.2% to 0.7%); hourly nighttime excess heat associated (+3.1% at the extreme). Our live exposure is still **monthly official counts**. They are coarser by construction. They are not a test of `HNe`. Reconstructing hourly intensity in Bob’s processing paragraph would overwrite your Methods.

## Provisional HM/CM (study-window only — your lock)

HF cold-tail months cohere with the official cold-day residual (`CM08` 1.173, 1.049–1.312; `CM03` 1.122, 1.023–1.230). `HM23` (Li daily event → monthly tail) is currently null. `CM05` (≤10 °C) flags **zero** months. None of these belong in the live paper until the reference period is written down.

## What we are not asking you to approve tonight

A confirmatory primary. A stroke coefficient. A rebuilt Laidlaw PDF. Author order.
