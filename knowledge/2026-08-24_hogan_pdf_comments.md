# Hogan / Jingjing comments on `Commented_Heat_CVD_Manuscript_20260824.pdf`

**Read method.** The PDF has no popup `/Annot` comments. Word flattened bubbles into the page as `Commented [H1]`–`[H6]`, `[KW7]`–`[KW20]`, and `[H21]`. Those strings, plus Hogan’s 24 August email, are the complete comment set used here. If a bubble exists only in Hogan’s live Word file and was not exported, it is not in this PDF.

**Author tags.** H = Hogan. KW = Jingjing (comments in the file).

| ID | Place | Ask | What we did |
|---|---|---|---|
| H1 | Running title | Amend once results exist | Running title already names first CHD/HF hospitalisation. Leave unless Hogan wants a new one. |
| H2 | Authors | Decide with Dr Bishai | Placeholders kept. Not a Methods issue. |
| H3 | Intro AMI/stroke | Remove; scope has changed | Live Introduction no longer treats AMI/stroke as this paper’s endpoints. **Paste the live Introduction over the PDF’s old AMI/stroke 35+ paragraph.** |
| H4 | Housing, behaviour | Cite or drop; do not name unmeasured housing; medication instead | Live Introduction does not name housing or behaviour. Medication is also unmeasured, so it is not named either. |
| H5 | “Environmental context has evolved” | Sounds like pollution changed after Goggins 2009; prove or rewrite | Live Introduction reports 2013–2023 EPD means and says they are not Goggins 2000–2009. **Paste that paragraph.** |
| H6 | Thesis | One sentence; leave until Results, then amend | Live closing Introduction paragraph is already one sentence. |
| KW7 | Study design | Use “dependent variable” | Methods now opens Health data with that term. |
| KW8 | Offset | Say “number of days in a month” | Equation defines \(d_t\) that way. |
| KW9 | “Specified after outcomes available” | Remove now that outcomes exist | Sentence removed. |
| KW10 | Ethics | One sentence that the study has approval | One IRB sentence. No process text. |
| KW11 | IRB number | Roro to insert UW number | No `UW XX-XXX` in the body. Comment for Roro in `LIVE_DOC_EDITS.md`. |
| KW12 | Influenza | Health data, not a tangent | Influenza sits under Health data. |
| KW13 | Influenza missingness | Brief reason | Flu Express had no usable series for Jan–Oct 2013; not coded as zero. |
| KW14 | “Include this data as well” | Use the rainfall/RH already listed | Model 2 includes monthly rainfall and mean relative humidity. |
| KW15 | Why five days not three? | Sensitivity | Model 1 also repeated per 3 days and per 1 day. |
| KW16 | Cold days in DJF | Results, not Methods | That observation is not in Methods. Winter-only fit is a labelled sensitivity. Hogan’s email: the interpretation is fine as a limitation. |
| KW17 | “Reserved” stations | Unclear | “Roadside monitors were not used.” |
| KW18 | Table 1 | Good | Unchanged. |
| KW19 | Acknowledgements | Do not thank co-authors | Section is now “None.” |
| KW20 | Data/code | GitHub for code; check IRB/Roro for data | Code URL given. Health counts not posted. |
| H21 | Yang C-Y → Yang CY | Done | Reference 1 already uses Yang CY. |

**Email (Hogan → Bob, with note to Jingjing).**

| Ask | What we did |
|---|---|
| Methods too complex; rewrite remaining subsections | Methods order is now data sources → equation → sensitivity. |
| Drop “core panel / twelve core contrasts”; use Model 1, 2, 3 | Done. |
| High-school readable | Short sentences; every symbol in the equation is named. |
| No Results in Methods | DJF cold-day concentration, Type I rates, and “material for CHD” removed from Methods. |
| No work-in-progress in the manuscript | Fake IRB number, “written confirmation remains required”, and “protocol may need amendment” removed from the body. |
| Cold-day series: interpretation OK as a limitation | Stays in Results/limitations only. |
| Add monthly rainfall and RH (Goggins and Chan 2017) | Model 2. We cite [21] as a local HF study that treated rainfall as a meteorological covariate. We do **not** quote an unverified rainfall–attendance coefficient. |
| Do not threshold a TV index | Model 3 uses leave-one-year-out same-calendar-day climatology. Series: `data_processed/hogan_climatology_day_counts_2013_2023.csv`. Mean warmer days/month 16.7; cooler 13.6 (slightly more warm days, as expected in a warming decade). |

**Not fitted on this machine.** Governed CHD/HF panels are gitignored and are not in this workspace. Model 2 and Model 3 are specified in Methods. Table 2 remains Model 1 until Bob runs `scripts/62_fit_hogan_model2_model3.R` on the machine that holds `data_processed/chd_analysis_panel.csv`. Do not invent those coefficients.
