# Correction to two archived CHD/HF sensitivity analyses

**19 November 2026.** The August thermal manuscript and its PDF supplement contain uncertainty estimates that should be withdrawn from interpretation. One error affects the unoffset count time-series models. A second affects fits with the most influential month removed. Corrected real-data intervals require the governed analysis panels or sufficient saved model objects.

## Affected releases

Each file occurs in both `outputs/tables/` and `outputs/release_chd_hf/supplement/`. The two copies of each file have identical bytes. Each contains six exposure specifications for each of CHD and HF. The SHA-256 hashes identify the original exports.

| File | Affected quantities in all 12 rows | Original SHA-256 |
|---|---|---|
| `cvd_count_timeseries_sensitivity.csv` | `std_error`, `rr_low`, `rr_high` | `4fa12d8423f265098ebc3936640d5ec7e25fd7cb1851a772dd6a87668414ab72` |
| `cvd_influence_sensitivity.csv` | `std_error_nw6`, `p_value_nw6`, `rr_low`, `rr_high`, `residual_acf1` | `cf4ddae00f6612e6b889bd6a6461e7d4724c9f0ae099e5e75a1360e73509a594` |

**Unoffset INGARCH fits.** The old script took the inverse of `info.matrix_corrected`, the middle matrix $B$ of the negative-binomial sandwich. The package computes $H^{-1}BH^{-1}$ using `info.matrix` for $H$. The correction calls the fitted model's covariance method. A missing score correction or unusable covariance leaves the interval unavailable. This calculation occurs after fitting, so the stored coefficient and residual series are separate quantities. Their original fitting accuracy has not been independently verified. [Pinned package implementation](https://github.com/cran/tscount/blob/173decbf9ca4d9dfd96e6b8aacb996214d491325/R/vcov.tsglm.R)

**Influential-month deletion.** Eight released rows identify February 2020 and four identify February 2022 as the deleted month. In all twelve fits the original script fed a shortened series to Newey–West and to the lag-one residual calculation. Removing February makes January and March adjacent in the input. When both months are fitted, their Bartlett weight at bandwidth six becomes 6/7, where their calendar separation gives 5/7. The same pair then enters the lag-one residual product. The revised functions use actual month distances and match Cook's distances to the fitted frame. Previously, an additional model omission could have mislabelled the deleted month. The public summaries cannot establish whether such an omission occurred. [Affected original script](https://github.com/bobshenruililin/Laidlaw-Heat-Project/blob/b3380ded3c9c65e47c69be2984d32cf404504a11/scripts/32_cvd_trend_depletion_lag.R)

Both fixes concern uncertainty or diagnostics. The gap calculation alone leaves fitted point estimates unchanged for the same selected sample. Annual event totals and the twelve full-series days-offset baseline models use other calculations. Neither the direction nor the magnitude of an interval correction follows from the published summaries.

## Recompute and review

Run the synthetic regression from the repository root with MASS, sandwich and tscount installed.

```sh
Rscript tests/test_governed_contracts.R
```

In an authorised analysis copy with the two approved panels, the revised sensitivity runner writes tables under `outputs/tables/`. Preserve the original exports separately. Record input and code versions, the R and package versions, the month selected, the actual fitted sample sizes and any unavailable intervals.

```sh
Rscript scripts/32_cvd_trend_depletion_lag.R
```

The responsible analyst can then reconcile each old and new row and return the disclosure-reviewed aggregate comparison. The existing PDFs retain the historical values. Read this correction alongside the thermal manuscript's residual-dependence and robustness sections, supplement sections S5.4–S5.5, and integrated report sections 6.4 and 6.6. No numerical replacement is available from this public audit.
