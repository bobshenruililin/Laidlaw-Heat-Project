# Hogan / Jingjing comments on `Commented_Heat_CVD_Manuscript_20260824.pdf`

**Read method.** The PDF has no popup `/Annot` comments. Word flattened bubbles into the page as `Commented [H1]`–`[H6]`, `[KW7]`–`[KW20]`, and `[H21]`. Those strings, plus the 24 August email *as stated in the user brief and `PROJECT_STATE.md` §0l* (the Outlook body is not stored in this repo), are the complete comment set used here. If a bubble exists only in Hogan’s live Word file and was not exported, it is not in this PDF.

**Author tags.** H = Hogan. KW = Jingjing.

## Verbatim PDF bubbles

| ID | Verbatim text (from flattened PDF) | What the live manuscript now does |
|---|---|---|
| H1 | “Running title proposed by Bob. Will need to be amended once results have been generated.” | Running title already names first CHD/HF hospitalisation. Leave unless Hogan wants a new one. |
| H2 | “To be determined after discussion with Dr. Bishai.” | Author 2–4 placeholders kept. Not a Methods issue. |
| H3 | “Remove now since the scope of the study has changed?” (on AMI/stroke responding differently) | Live Introduction no longer treats AMI/stroke as this paper’s endpoints. **Paste the live Introduction over the PDF’s old AMI/stroke 35+ paragraph.** |
| H4 | “You need to cite the papers for these factors. In the context of this study, if we don’t have the housing and behavioural adaptation data, I would suggest to not mention it and instead replace it with medication instead. You don’t want to encourage people to think about a possible factor that we did not control for from the get-go.” | Live Introduction does not name housing, behaviour, or medication (medication is also unmeasured). |
| H5 | “The phrasing of “the environmental context has also evolved” makes me think that the level of air pollutants has changed after Goggin’s study in 2009. Is this the case? If not, then we need to remove this or rewrite it.” | Live Introduction reports 2013–2023 EPD means and says they are not Goggins 2000–2009. **Paste that paragraph.** |
| H6 | “I feel like the thesis of the paper can be combined into one statement/sentence. We will leave it as it is for now and amend this after the Results are generated.” | Live closing Introduction paragraph is already one sentence. |
| KW7 | “I would prefer the term "dependent variable."” | Methods opens Health data with that term. |
| KW8 | “Do you mean "the number of days in a month"? This would make it more clear.” | Equation defines \(d_t\) that way. |
| KW9 | “Once the outcome series is available, remove this sentence.” | “Specified after outcomes available” removed. |
| KW10 | “@Bob: You only need one sentence here to indicate that this study has ethics approval. All the other stuff is not required (I deleted it already).” | One IRB sentence. No process text. |
| KW11 | “@Roro: Can you input the IRB reference number here for this study?” | No `UW XX-XXX` in the body. Comment for Roro in `LIVE_DOC_EDITS.md`. |
| KW12 | “As this is considered to be "health" data, I moved it to this section and rewrote it so that it is clearer.” | Influenza sits under Health data. |
| KW13 | “Brief justification needed.” (influenza gap) | Flu Express had no usable series for Jan–Oct 2013; not coded as zero. |
| KW14 | “I would suggest that you include take this data as well.” (on rainfall/RH already listed in Hogan’s weather paragraph) | Model 2 includes monthly total rainfall and mean relative humidity. |
| KW15 | “Why five days and not three days? How do the values differ if you used a single extreme day? Maybe you can do a sensitivity analysis to check?” | Same Model 1 coefficient, rescaled: if the five-day ratio is *R*, the three-day ratio is *R*^(3/5) and the one-day ratio is *R*^(1/5). |
| KW16 | “Remove. This is an observation, meaning it goes in the Results.” (DJF concentration of cold days) | Not in Methods. Winter-only fit is a labelled sensitivity. Hogan’s email: the interpretation is fine as a limitation. |
| KW17 | “What does this mean? Reserved for what?” | “Roadside monitors were not used.” |
| KW18 | “Good.” (Table 1) | Unchanged. |
| KW19 | “You do not include the co-authors here. The acknowledgement section is for acknowledging people whose contribution helped the study but do not qualify as intellectual contribution. … At the moment, I don't think we have anyone to acknowledge.” | Section is `None.` |
| KW20 | “This needs to be rewritten. All you need to say is that the code used to generate the findings can be found on your github page (provide link). For the data, we need to check with Roro and look at the IRB app to see as to what can be publicly shared.” | Code URL given. Health counts not posted. |
| H21 | “Changed from Yang C-Y to Yang CY for consistent formatting.” | Reference 1 already uses Yang CY. |

## Email (Hogan → Bob, with note to Jingjing)

The Outlook body is **not** checked into this repository. The asks executed here are those stated in the 24 August user brief and in `analysis_plan/PROJECT_STATE.md` §0l. No extra email sentences were invented.

| Ask (from that brief) | What we did |
|---|---|
| Methods too complex; rewrite remaining subsections | Methods order is now data sources → equation → sensitivity. |
| Drop “core panel / twelve core contrasts”; use Model 1, 2, 3 | Done in live Methods, Abstract, and Results headings. |
| High-school readable | Short sentences; every symbol in the equation is named. |
| No Results in Methods | DJF cold-day concentration, Type I rates, and “material for CHD” removed from Methods. |
| No work-in-progress in the manuscript | Fake IRB number, protocol-amendment language, and a false “roles are in the Acknowledgements” footnote removed. |
| Cold-day series: interpretation OK as a limitation | Stays in Results/limitations only. |
| Add monthly rainfall and RH (Goggins and Chan 2017) | Model 2. We cite [21] for **humidity**, which that paper used as a meteorological predictor. We do **not** claim Goggins entered rainfall, and we do not quote an unverified rainfall–attendance coefficient. Rainfall is still in Model 2 because Hogan listed it and KW14 asked to use it. |
| Do not threshold a TV index; count days vs leave-one-year-out same-calendar-day climatology | Model 3. Series: `data_processed/hogan_climatology_day_counts_2013_2023.csv`. Mean warmer days/month 16.7; cooler 13.6. |

**Not fitted on this machine.** Governed CHD/HF panels are gitignored and are not in this workspace. Model 2 and Model 3 are specified in Methods. Table 2 remains Model 1 until Bob runs `scripts/62_fit_hogan_model2_model3.py` on the machine that holds `data_processed/chd_analysis_panel.csv`. Do not invent those coefficients.

**Human paste.** Bob pastes the live Methods (and Introduction / Acknowledgements / data-availability) into Hogan’s shared file. Do not email a parallel Word copy. Do not resolve comment bubbles until Hogan has read the replies.
