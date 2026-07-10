# Literature review findings memo (internal)

**Date:** 10 July 2026 (updated after critical TeX review)  
**Audience:** Project team (internal)  
**Full report:** `reports/Literature_Review_Critical.pdf`

## Strongest established findings

1. **Hong Kong AMI historically cold-dominant (daily data).** Goggins et al. (2013): below ~24°C, ~3.7% higher AMI admissions per 1°C decrease (lags 0–13); no significant heat effect in that study; NO₂ important.
2. **Hong Kong stroke historically cold-related, subtype-specific (daily data).** Goggins et al. (2012): hemorrhagic stroke showed a strong inverse temperature association (lags 0–4); ischemic stroke weaker and mainly below ~22°C (lags 0–13); pollutants not associated.
3. **Warm-climate winter excess is plausible.** Sipilä (Finland) and Lorking (Thailand) support seasonal stroke burdens outside classic temperate heat narratives.
4. **Administrative principal inpatient diagnoses can have high PPV** for AMI/IS in East Asian validation studies (Korea NHIS 2024; Tianjin 2025), supporting insistence on principal diagnosis.
5. **Official binary hot nights ≠ nighttime heat intensity.** Guo et al. (2024): HNday28 not associated with excess hospitalization risk; HNe / HNday90th were, including circulatory admissions.

## Recent Hong Kong overlap (important)

| Study | Overlap | Implication for novelty |
|---|---|---|
| Guo et al. 2024 (*Lancet Reg Health West Pac*): hot nights / nighttime heat excess and hospitalization, 2000–2019 | Direct overlap on **hot nights** and cardiovascular hospitalization | Cannot claim “first HK hot-night hospitalization study.” Official binary hot night (Tmin≥28) was **not** associated with excess risk; **intensity** (hot-night excess) was. |
| Guo et al. 2025 (*ES&T*): temperature × pollution and emergency hospitalizations, 2000–2019 | Overlap on temperature–pollution interaction | Supports staged pollution models; not monthly principal-dx AMI/IS/HS. |
| Yang/Wei/Chong et al. 2025 (*Int J Biometeorol*): cold + influenza and stroke, 1998–2019 weekly | Overlap on cold–stroke | Supports cold + flu sensitivity; weekly pooled stroke ≠ our monthly subtype design. |
| Wang et al. 2019 (*STOTEN*): extremely hot weather events / 2D3N / 5HN | Overlap on official VHD/HN spell structure | Supports spell and combination metrics as alternatives to raw monthly counts. |

## Defensible remaining contribution

> Among Hong Kong residents aged 35+, estimate **monthly** associations of **officially defined** thermal extremes (especially hot nights and cold days) with **principal-diagnosis inpatient** AMI, ischemic stroke, and hemorrhagic stroke during **2013–2023**, with age-sex population offsets, separate older-age bands, COVID handling, and staged pollution adjustment — without assuming a heat-for-cold regime shift.

## Pipeline changes prompted by this review

- Absolute humidity (Tetens) added to weather build.
- Spell-ge5 and 2D3N-window monthly indicators added as alternative exposures.
- Assumption ledger entries A33–A36 record null-interpretation and subtype rules.
- See TeX report Section 8 for the full implementation backlog.

## Files

- `reports/Literature_Review_Critical.pdf` / `reports/latex/literature_review_critical.tex`
- `literature/evidence_matrix.csv`
- `literature/goggins_comparison_table.md`
- `literature/references.bib`
- `reports/literature_review_findings_memo.md` (this file)
