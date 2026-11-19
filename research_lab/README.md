# Reproducing the Hong Kong hospitalisation study

The lab compares annual recorded first-stay counts with public hospital service activity, tests three historical benchmarks and measures how much weather variation remains after calendar adjustment. The analyses are retrospective. The [protocol](protocol.json) specifies the inputs, units and comparisons.

## Run from the repository root

```bash
python3 -m pip install -r research_lab/requirements.txt
python3 -m research_lab check
python3 -m research_lab run --out /tmp/laidlaw-study
python3 -m unittest discover -s research_lab/tests -v
```

Python 3.10 or later and NumPy are sufficient for the numerical work. The check rebuilds the tables and an example question, verifies source fingerprints and compares against the committed outputs. The run command writes a complete result directory. Repeating an identical run is safe. A different result requires a new destination. [Evidence manifest](results/manifest.json) · [Figure and manuscript build](../manuscript/covid_period/november/README.md)

| Read the evidence | What each row represents |
|---|---|
| [Annual hospital activity](results/service_context.csv) | Eleven calendar years, two first-stay series and three service comparators. Each index uses its own 2019 base. [Official table cells and editions](sources/HK_INPATIENT.md) |
| [Annual changes and denominator thresholds](results/annual_changes.csv) | Within-series changes and the eligible person-time ratio giving equal recorded-event rates relative to 2019 |
| [Historical forecasts](results/hindcast.csv) | Two outcomes, four target years and three rules. Each rule only sees years before its target. All 24 comparisons are retained. |
| [Weather design](results/weather_design.csv) | Six exposures, three calendar windows and the four-df time spline. The smallest number of months accounting for half the squared residuals describes concentration in time. |
| [Daily weather agreement](results/weather_source_agreement.json) | Two encodings from the same HKO station over 4,017 dates. Three daily means differ by 0.1°C. All 396 monthly threshold counts agree. |
| [Archived weather estimates](results/weather_models.csv) | Twelve full-window contrasts and all four uncertainty constructions. The lag-six BH adjustment is recomputed across all twelve. |

## Run a different weather question

Copy the [example card](questions/later_weather_support.json) and state the question and criterion before evaluating it. The example runs with:

```bash
python3 -m research_lab challenge research_lab/questions/later_weather_support.json --out /tmp/laidlaw-questions
```

Every requested calendar setting returns all six exposures and all three windows. The chosen exposure family and window define which cells must meet the criterion. The included card asks whether six months are needed to supply half the adjusted variation for every threshold-day exposure in 2020–2023. Zero of twelve cells met that illustrative criterion. All 72 computed cells are saved. [Example result](questions/later_weather_support/verdict.json) · [Complete grid](questions/later_weather_support/all_designs.csv)

| Field | Accepted settings |
|---|---|
| `spline_df` | Increasing subset of 3, 4, 6, 8 |
| `window` | `2013-2023`, `2013-2019`, `2020-2023` |
| `family` | `all_six`, `temperatures`, `threshold_days` |
| `metric` | `residual_share`, `largest_month_share`, `months_for_half_ss` |
| `comparison`, `threshold` | `at_least` or `at_most`, with a fraction in [0,1] or a whole number of months |

Each card records its question, code, inputs and outputs under a content-derived run ID. An unmet scientific criterion is retained. A source or computational error exits nonzero. The separate command `python3 -m research_lab.history_design` tests observation-history logic using invented counts. [What an original health-model refit would require](measurement.md)
