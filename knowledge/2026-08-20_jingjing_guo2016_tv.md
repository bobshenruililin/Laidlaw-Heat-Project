# Jingjing 20 August 2026 — Guo 2016 temperature variability on the climate panel

**Mode:** Ship. **Not** a Gate 3 freeze. **Not** a health-model run.

## The email (verbatim job)

Jingjing asked the group to add **Temperature Variability (TV)** to the temperature data panel, and said “the number of TV dates in a month may be helpful,” citing [PMID 27258598](https://pubmed.ncbi.nlm.nih.gov/27258598/).

That paper is Guo Y, Gasparrini A, Armstrong BG, et al. 2016. Temperature variability and mortality: a multi-country study. *Environ Health Perspect* 124:1554–1559. DOI 10.1289/EHP149.

## Was this already in our manuscripts and outputs?

**Related, not the same, and not on the share panel.**

| Surface | Status before 20 August 2026 |
|---|---|
| Roro temperature panel (12 August share) | No TV columns. Means + official extreme-day counts only. |
| Live Hogan manuscript | Weather paragraph is HKO-only. TV is not a core exposure. |
| Locked Stage 3 essay / poster | Not featured. An older methods list named TV as a planned sensitivity. Do not rebuild Stage 3 for this. |
| Pathway P15 | Ran as `temp_variability_mean_range` = monthly **mean diurnal range** (Tmax − Tmin), motivated by Tian/Qiu 2023 JoGH, **not** Guo 2016. Archive only; not in the twelve-contrast core. Do not quote those numbers in the Jingjing reply. |
| `scripts/19_build_analysis_exposures.R` | Also builds `temp_variability_sd_tmean` (within-month SD of daily mean T). Still not Guo’s min/max SD. |

Guo 2016 does **not** define a “TV date.” TV is a continuous daily SD. Jingjing’s phrasing is a reasonable monthly summary request, not a second paper.

Hogan owns the weather panel and the live weather paragraph. Building TV from public HKO does not take that away from him. The p90 “TV date” count is a convenience column for him to keep, move, or drop.

## What we shipped

Script: `scripts/65_guo2016_tv_temperature_panel.py`.

Living panel: `outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv`.

Thread pack: `analysis_plan/send_pack_2026-08-21_tv/` (CSV + `to_thread.md`). Bob sends from the existing Outlook thread; agents do not send.

New columns: `tv_guo2016_0_1_mean`, `tv_guo2016_0_7_mean`, `tv_guo2016_0_1_days`, `high_tv_guo2016_0_1_days` (p90 convenience, Hogan-owned), `dtr_mean`.

Hand check: 2013-01-02 TV0–1 = 3.672 °C (sample SD of Tmin/Tmax 14.9/19.3 on 2 Jan and 10.8/17.4 on 1 Jan). Study-period p90 of daily TV0–1 = 3.772 °C (403 / 4017 days). Official `cold_days` total remains 145; `hot_nights` 449.

## What we did not do

- Did not fit TV against CHD/HF.
- Did not paste TV into Hogan’s weather paragraph.
- Did not rebuild Stage 3 PDFs.
- Did not treat P15 diurnal-range IRRs as Guo 2016 findings.
