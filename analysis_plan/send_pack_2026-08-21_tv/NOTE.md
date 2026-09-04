# Dictionary addendum — Guo 2016 TV columns

Added 20 August 2026. Source script: `scripts/65_guo2016_tv_temperature_panel.py`.

## Operator (Guo et al. 2016, *EHP*)

Daily TV is the **sample standard deviation** of daily **Tmin and Tmax** over a lag window:

- TV0–1 = SD of four values: Tmin and Tmax on day *d* and day *d*−1.
- TV0–7 = SD of sixteen values: Tmin and Tmax on days *d* through *d*−7.

This is **not** the within-month SD of daily mean temperature, and **not** mean diurnal range (Tmax − Tmin). Those older proxies still exist in the analysis archive as P15 (`temp_variability_mean_range`). They are a different estimand.

Guo 2016 reports TV as a **continuous** daily exposure. The paper does **not** define a “TV date.”

## New monthly columns

| Column | Definition | Provenance |
|---|---|---|
| `tv_guo2016_0_1_mean` | Mean of daily TV0–1 in the month | REAL (HKO daily Tmin/Tmax) |
| `tv_guo2016_0_7_mean` | Mean of daily TV0–7 in the month | REAL (HKO daily Tmin/Tmax) |
| `tv_guo2016_0_1_days` | Count of days in the month with TV0–1 defined | REAL |
| `high_tv_guo2016_0_1_days` | Count of days with TV0–1 ≥ study-period p90 of daily TV0–1 | Convenience threshold, **not** in Guo 2016. p90 = 3.772 °C on 2013–2023 daily TV0–1. Hogan may drop or move this. |
| `dtr_mean` | Mean of Tmax − Tmin in the month | REAL. Same family as archived P15. Labelled so it is not confused with Guo TV. |

January 2013 TV0–1 uses December 2012 Tmin/Tmax for the lag. TV0–1 is defined on all 31 days of January 2013.

Hand check: 2013-01-02 TV0–1 = 3.672 °C from HKO Headquarters Tmin/Tmax 14.9/19.3 (2 Jan) and 10.8/17.4 (1 Jan).

## Unchanged columns

`month_id`, `year`, `month`, `mean_temp`, `mean_tmin`, `mean_tmax`, `hot_nights`, `cold_days`, `very_hot_days`, `extremely_hot_days`, `days_in_2d3n_window`, and `station` are copied through unchanged from the 12 August share file.
