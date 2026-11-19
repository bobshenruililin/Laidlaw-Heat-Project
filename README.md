# First hospitalisations after cardiovascular diagnosis in Hong Kong

From 2013 to 2019, recorded first hospitalisations after coronary heart disease (CHD) or heart failure (HF) diagnosis fell every year in the two study series. Total inpatient episodes across Hong Kong rose every year. Over the next four annual transitions, the series moved together. This repository contains the paper, annual source tables and executable analyses behind that comparison.

[Read the paper](manuscript/covid_period/november/Manuscript.pdf) · [Editable Word version](manuscript/covid_period/november/Manuscript.docx) · [Read on GitHub](manuscript/covid_period/november/Manuscript.md)

## Reproduce the results

From the repository root with Python 3.10 or later and NumPy installed, run the following commands.

```bash
python3 -m research_lab check
python3 -m unittest discover -s research_lab/tests -v
```

[Installation and commands](research_lab/README.md) · [Protocol](research_lab/protocol.json) · [Numerical tables](research_lab/results/)

| Question | Evidence |
|---|---|
| When did the two study series and wider inpatient activity diverge? | [Eleven annual observations per series](research_lab/results/service_context.csv) and [official source definitions](research_lab/sources/HK_INPATIENT.md) |
| How large was the 2020 departure from earlier years? | [Three benchmarks for each outcome and target year](research_lab/results/hindcast.csv). Every forecast uses only earlier observations. |
| Which months supply the weather comparisons? | [Six exposures across three time windows](research_lab/results/weather_design.csv) and [a question you can change and rerun](research_lab/questions/later_weather_support.json) |
| Which historical estimates need another calculation? | [Time-series uncertainty corrections](reports/legacy_uncertainty_correction_2026-11-19.md) |
| What additional data would distinguish changing first-event risk from changing observation? | [Measurement and replication](research_lab/measurement.md) |

The two outcome series describe people with type 2 diabetes and/or hypertension. Each counts the first recorded hospitalisation after a relevant diagnosis. The two outcomes can overlap. The public episode series include repeat stays and day inpatients. Each of the five series is indexed to its own 2019 total. The comparison describes recorded use.
