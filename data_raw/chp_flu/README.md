# CHP Flu Express

Weekly influenza surveillance from the Centre for Health Protection.

- Raw: `flux_data.csv` from https://www.chp.gov.hk/files/misc/flux_data.csv
- Dictionary: https://www.chp.gov.hk/files/pdf/flux_spec_en.pdf
- Monthly aggregate used in models: `flu_monthly_2013_2023.csv` / `flu_for_confounders.csv`
- Primary metric: monthly mean of `AandB_proportion` (influenza A+B positivity among respiratory specimens)

Refresh:

```bash
python3 scripts/21_download_chp_flu.py
Rscript scripts/06_build_confounders.R
Rscript scripts/06b_build_hk_holidays.R
```
