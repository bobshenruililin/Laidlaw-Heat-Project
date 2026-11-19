# What it would take to reproduce the original health fits

The public analysis reconstructs the 22 annual first-stay totals from the released summary, compares them with public service statistics and checks the published weather-model displays. Annual episode totals do not distinguish first stays after diagnosis from subsequent stays.

| Calculation | Minimum input |
|---|---|
| Refit the monthly weather models | One count for each of 132 calendar months per outcome from January 2013 through December 2023, plus the definition of a qualifying first recorded stay. An official download or table number would allow verification of the source and coverage. |
| Estimate how recorded-event rates changed | Eligible person-time in the same calendar month for each outcome, including entry and exit from eligibility. |
| Test sensitivity to available history | Paired counts in identical candidate populations and calendar months, built with fixed prior history and with all available history. Compare the overlaps and differences. |

First reconcile each monthly series to its eleven annual totals. Check the diagnosis setting, same-day admission rule and available prior history. Without measured person-time one can still calculate the change required for equal rates. In 2023 versus 2019 the break-even ratio of eligible person-time is 12,323/12,396 for CHD and 2,296/2,344 for HF. The actual ratios are unknown. [Annual calculations](results/annual_changes.csv)

The synthetic exercise demonstrates how different first-event histories can yield identical recorded counts. Run it with `python3 -m research_lab.history_design`. [Paired comparison design](history_design.py)

Hong Kong’s public tables report episodes ending in discharge or death, including day inpatients. The endpoint in this study is the first recorded hospitalisation after a relevant diagnosis among people with diabetes and/or hypertension. [Hospital Authority statistics](https://www3.ha.org.hk/data/HAStatistics/MajorReport) · [Department of Health inpatient statistics](https://data.gov.hk/en-data/dataset/hk-dh-dh_ncddhss-ncdd-dataset-10)
