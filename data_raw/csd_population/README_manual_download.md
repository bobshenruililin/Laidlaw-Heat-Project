# C&SD population denominators

**Automated primary source (used by `scripts/05_build_population_denominators.R`):**

C&SD MDT CSV for Table **110-01001** (Population by sex and age group), mid-year (`H=1`).

```text
https://www.censtatd.gov.hk/data/MDT_76_110-01001_POP_Raw_K_1dp_per_n.csv
```

Values in the MDT are in thousands (`'000`); the build script converts to persons.

Single-year ages (Table **110-01002**) are also downloaded for audit:

```text
https://www.censtatd.gov.hk/data/MDT_76_110-01002_POP_Raw_K_1dp_per_n.csv
```

Normalized annual output written by the pipeline:

```text
csd_population_age_sex_annual_normalized.csv
```

Schema: `schemas/csd_population_annual.schema.json`

## Manual alternative

1. Open https://www.censtatd.gov.hk/en/web_table.html?id=110-01001
2. Place a normalized file here named `csd_population_age_sex.csv` with columns:
   `year, sex, age_group, population` (persons, not thousands).
3. Re-run `scripts/05_build_population_denominators.R`.

Sensitivity (exclude foreign domestic helpers): Table 110-01001A / 110-01002A.

Set `pipeline.refresh_csd: true` in `config.yml` to force re-download of MDT files.

API docs: https://www.censtatd.gov.hk/datagovhk/WT_data_dict_en.pdf
