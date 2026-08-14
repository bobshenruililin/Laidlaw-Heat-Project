# Fable YC / product pass — 14 August 2026

**Mode:** Decide + Ship. Product taste only. No health findings, no HA rows, no freeze-lift. All numbers below already exist in the charter, the atlas, the field laboratory, or the hub. Uncommitted residue for Bob and the parent.

## Demo Day sentence

The same 4,017 Hong Kong nights count as 449 hot, 17 hot, or 1,453 hot depending on the thermometer, and we built the slider that turns that definition fight into a sixty-second demo.

## Natures of the deliverables

| Surface | True job | Current failure mode | 10x if | Kill / keep / freeze |
|---|---|---|---|---|
| Stage 3 essay PDF (`6136e85a654502a0…`) | Prove the research summer to HKU and the Foundation | Finished but unendorsed and unposted; the risk is inaction, not content | It is in Bishai's inbox today and in the University room by 31 August | Freeze (already frozen) |
| A0 poster (`4f7c1e408ae2d31f…`) | Stop a walker at Chi Wah for ten seconds | Logos pending as print overlay | Overlay done before 15 September; nothing else touched | Freeze |
| HKU 2a worksheet | Unblock the one signature agents cannot produce | Waiting behind "the essay already looks done" | Sent to Bishai now with the frozen PDF | Keep (human) |
| Hogan live file | The journal paper | Temptation to grow parallel drafts | Only the paste pack touches it | Keep (live authority) |
| LSN summary + `docs/lsn` | Become the URL HKU reports to the Foundation | Not posted; the ribbon gets confused with the Network room | Posted after Bob's privacy pass, hub linked once | Keep |
| Blog drafts | First-person process in the programme register | Register drift (caught once by Sol; stays caught) | Bob's voice pass plus one link to the hub | Keep as drafts |
| `docs/peers` | "The flag does not travel": 449 / 17 / 1,453 on one grid | The calibration table — the actual product — is buried under a gazetteer of sixteen cities | The triple leads; cities demoted to supporting cast | Keep as a room |
| `docs/geo` | "The territory disagrees with itself" (Waglan 252 vs Headquarters 17) | Reads as a smaller PRD mosaic at a different zoom | Folded in as a zoom level of one field, not a separate front door | Keep, merge |
| `docs/prd` | "The 28 °C night is marine" (~353 marine vs ~12 in the Guangzhou box) | Third restatement of the same insight | Same merge | Keep, merge |
| `docs/field` | The methods room: eight views of one 4,017 × 90 matrix | Eight methods read as eight products; strongest science, weakest story | Demoted to the "how we checked" room behind the demo | Keep, demote |
| `docs/` hub | The front door | Canonical URL 404s; a card menu forces a choice before understanding | Pages enabled; the slider is the hero; rooms sit behind it | Keep, promote |
| "Move the night" demo | The sixty-second version of the whole project | Does not exist yet | Ships as the hub hero under the conditions below | Ship (conditional) |

On the four Leaflet maps: they are **one product with four rooms**, currently shipped as **four unfinished products**. The tell is the disclaimer — every hub card ends with a variant of "not a hospital map." When four pages need the same disclaimer, they are one page. Peers, geo, prd, and field are the same insight at four zooms (city rank, territory, delta, delta through time), each with its own front door, no shared state, and its punchline stated in prose because the interaction cannot state it. The fix is not a fifth map. It is one hallway with one parameter.

## Jobs to be done

- **YC partner:** opens one URL, drags 28 °C to 26 °C, watches 449, 17, 1,453 and the 90-cell field move together, and leaves able to repeat the Demo Day sentence.
- **Hogan:** never opens Leaflet. He takes the static exceedance-and-agreement figure and the calibration table (RMSE 1.97 °C, bias −1.47 °C, Jaccard 0.031) for the weather Methods, with provenance beside every number.
- **Bishai:** uses none of this. His sixty seconds are the 2a request: frozen essay, worksheet, one clear ask for the endorsement block. The demo's only job with him is to stay out of that email.
- **Horizons administrator:** needs name, title, and a Scholars Network University-room URL to report to the Foundation. GitHub Pages does not exist for this person.
- **Laidlaw website reader:** reads one first-person post and clicks one link. They should land on the hub hero, not a menu of four maps. They want the sentence, not the panel.
- **Chi Wah passer-by:** gets ten seconds of frozen A0 poster in the week of 5 October. The poster does that job alone; the maps matter only if a stable URL exists by then.

## Verdict on the parent candidate

**Ship-only-if.** It is the right object: it converts four rooms into one interaction and turns Jaccard from a slogan into an experience. Conditions: (1) every count at every threshold step is precomputed offline from the existing 4,017-day and 90-cell caches — no live fetch, no invented values; (2) 28 °C is annotated as the HKO official flag, and apparent temperature is labelled a third object, never a corrected station; (3) it ships as the hub hero, not as `docs/slider/` room five; (4) exposure only — the first proposal to add a health layer kills the feature; (5) a static threshold-sensitivity figure ships beside it for people who cite rather than click. If the threshold sweep cannot be computed exactly from the caches, kill it rather than approximate.

## Ideas the parent has not had

1. **The exceedance-and-agreement figure (not a map).** One static two-panel figure: nights flagged versus threshold for HKO station, ERA5 dry-bulb, and apparent temperature over the same 4,017 matched days; beneath it, Jaccard(station, grid) as a curve in the threshold. 449 / 17 / 1,453 become three points at 28 °C on three curves. It impresses because it is the citable object — this is what a climate-health professor puts in a methods figure as the exposure-misclassification exhibit, and it proves the demo has a paper-grade backbone. It is honest because every point is a count on matched real days from the existing cache: no fitting, no health axis. Do NOT build: a smoothed fit, a "recommended corrected threshold," a second axis of any health quantity, or any city for which no station series exists in this repo.
2. **Links that carry arguments (stateful URLs).** The slider state lives in the URL hash, so a shared link reproduces exactly what the sender saw. It impresses because it is a distribution mechanic, not a feature: every threshold disagreement between two readers becomes a reproducible link. It is honest because the URL encodes only a parameter over precomputed real counts. Do NOT build: a backend, accounts, comments, or analytics.
3. **Same night, three thermometers.** A date scrubber over the real nights in the cache: for one chosen night, show station Tmin, grid Tmin, apparent temperature, and Waglan, and whether each flags at the current threshold. It impresses because it makes the abstraction concrete — a specific real night the station flags and the grid does not. It is honest because every value already exists in the daily caches. Do NOT build: a "most dangerous night" leaderboard, any admissions overlay, or any narration about harm.
4. **The refusal ledger (not a map).** One plain page listing what the panel declined to claim, with the numbers: 23/90 trend intervals became 0/90 under BH; 2,428 network edges became 26 after removing EOF1; the marine conditional 0.43 is 0.31 pooled. It impresses because reviewers and serious partners both read discipline as signal, and it is the page no one else will write. It is honest by construction: it publishes only the corrections of our own overreach. Do NOT build: any health q-values on a public page, any self-congratulation about honesty, any comparison to what a human would have claimed.

## What would actually impress YC here

The insight is not eight methods — method count is not validation and YC knows it. The insight is that a city's official heat statistic is an artifact of one instrument and one step function, and this team measured the fragility (hot-night Jaccard 0.031 between station and grid) instead of assuming it away. The demo is one slider on one URL. The distribution hole is fatal and cheap: the canonical `github.io` URL 404s until one human flips Settings → Pages → GitHub Actions, and the URL that matters institutionally — the Scholars Network University-room post — does not exist yet either. A wow behind a 404 is a launch that did not happen. The smallest shippable wow: Pages enabled, the threshold slider as the hero of the existing hub, one stateful link pasted into one blog draft and the LSN summary after Bob's pass, and the static figure as the fallback for people who will not click.

## What would embarrass us

- Any sentence transporting CHD/HF count ratios to another city, grid cell, or population.
- Presenting 1,453 apparent-temperature nights as a "correction" of HKO's 449, or the +1.47 °C offset's 378 as a recovery of the official flag.
- Quoting the 23/90 trend cells anywhere without the 0/90 BH sentence in the same breath.
- "The delta warms and cools together" as a basin claim rather than a sampled-grid description.
- k-means cluster names spoken as districts, neighbourhoods, or catchments.
- "Eight disciplines agree" as if agreement of descriptive methods were validation.
- Any revival of "an agent can do what a tired human will not." It was killed; it stays dead.
- Calling the GitHub Pages URL the Laidlaw Scholars Network URL, in any email, post, or form.
- Showing the demo to Bishai as if it were, or advanced, the 31 August deliverable.
- Health colour ramps, hospital icons, or stroke language on any public cell, tooltip, or legend.
- Inventing station series for the fifteen peer cities to extend the calibration table.

## Packing vs wow

They share no critical path except Bob's attention, and the endorsement owns that attention first. The only serial dependency for 31 August is Bishai's block on form 2a: Bob sends the worksheet and the frozen essay now, and no demo, slider, or figure appears in that email or substitutes for the University-room post. Agents build the slider and the figure in parallel because they touch only living `docs/` surfaces and existing caches — never the frozen PDFs, the 2a, or the live manuscript. If the two ever compete for an hour, the endorsement wins without discussion: a slider can still ship in September and impress in October at Chi Wah; a missed endorsement cannot be shipped late.
