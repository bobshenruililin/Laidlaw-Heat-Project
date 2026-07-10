# C&SD population denominators — import instructions

Preferred source: Census and Statistics Department Table 110-01002
(Population by sex and age), or 110-01001 / single-year age tables that can
construct 65–69 and 70–74 separately.

## How to obtain

1. Open https://www.censtatd.gov.hk/en/web_table.html?id=110-01002
2. Customise to mid-year (or half-yearly) population by sex and age for 2012–2024.
3. Use the page API button to copy the GET URL (includes encrypted `param`), OR download CSV/XLSX.
4. Save into this folder as `csd_population_age_sex.csv` with columns such as:
   year, sex, age, population   OR   year, sex, age_group, population
5. Re-run this script.

Alternative table excluding foreign domestic helpers: 110-01002A — useful as sensitivity
if HA residency definitions suggest FDH exclusion.

API docs: https://www.censtatd.gov.hk/datagovhk/WT_data_dict_en.pdf
