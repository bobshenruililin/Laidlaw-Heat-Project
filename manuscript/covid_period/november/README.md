# November manuscript

[Read the paper](Manuscript.pdf) · [Editable Word document](Manuscript.docx) · [Markdown source](Manuscript.md)

The article compares two first-stay series with hospital activity across Hong Kong. The [data tables](../../../research_lab/results/) provide exact values for the annual trajectories, the historical forecasts and the weather design. The [official source notes](../../../research_lab/sources/HK_INPATIENT.md) locate the transcribed cells. The [October supplement](../Supplement_covid_period.md) retains the complete weather model family. The [measurement guide](../../../research_lab/measurement.md) describes the inputs for an independent refit.

## Rebuild the paper

Run these commands from the repository root after reproducing the lab results. The two Markdown tables are generated. To refresh them after a reviewed source change, run the `tables` action. The figures are editable SVGs. The Word export uses the same figures.

```sh
paper=manuscript/covid_period/november
python3 "$paper/build.py" check
python3 "$paper/build.py" figures --rasters /tmp/laidlaw-paper-figures
python3 "$paper/build.py" word --rasters /tmp/laidlaw-paper-figures
python3 "$paper/build.py" pdf
```

The check uses the Python standard library. Figure rendering requires Matplotlib. Word export requires Pandoc and python-docx. PDF export requires LibreOffice available as `soffice`.
