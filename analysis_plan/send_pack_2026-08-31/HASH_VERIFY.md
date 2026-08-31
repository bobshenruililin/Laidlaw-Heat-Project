# Horizons Stage 3 lock — 31 August 2026

**Mode:** Ship. Not a Stage 3 rebuild. Not a Gate 3 freeze.

The files Bob uploaded for Horizons on 31 August are the **22 August** programme essay and poster (fold-back lock, git `8b91f3c`). They are **not** the 24 August Hogan-aligned rebuild that currently lives on `main` under `outputs/`.

Do **not** commit the endorsed form PDF (ink signature).

| Object | Bytes | SHA-256 | Role |
|---|---:|---|---|
| Endorsed form `2a. Laidlaw - Report Form (HKU)DB.pdf` | 335,946 | `722ba1f70f246c2d6401611ec0151f10635acdfdeb5e55554c468f71e5346761` | Attach. Local only. |
| Essay (uploaded) | 407,146 | `c083d4096a0924b1534b021c66126251d5f4c8b2acb8121ca3b1573c7512cd3f` | Attach. Matches 22 Aug lock. |
| Poster (uploaded) | 93,978 | `0ef58e0951bb2ffdf69108b5a81e69ec55d4775d564e32456d8d6c57f67c790c` | Attach. Due 15 Sep; OK today. |
| Hogan PDF (uploaded) | 679,857 | `b172ed31659d6cd6f4117415de7f25119cd875d893844dbbe7c2e67650387ce9` | **Do not attach.** 14-page live file. |
| `outputs/ShenRuililin_Laidlaw_Stage3Report.pdf` on `main` | 408,186 | `605cd8db43072cb58f44ee82c29a7c98048deded464f0e7167d6fbfad2219eb7` | Repo current essay. **Not** the Horizons object. |
| `outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf` on `main` | 94,273 | `a972206e61932650593378a2191fae132755a40135f904a74ea5501cccfdc8c5` | Repo current poster. **Not** the Horizons object. |
| `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.pdf` | 784,756 | `436fb4ff1b278ec82471da401755fbc6aa9d1c6acc1cf6f78d5c61fc6f9fcf7f` | 27 Aug Bishai print. **Not** for Horizons. |

Recover the 22 August essay from git if the upload is lost:

```bash
git show 8b91f3c:outputs/ShenRuililin_Laidlaw_Stage3Report.pdf > /tmp/ShenRuililin_Laidlaw_Stage3Report.pdf
git show 8b91f3c:outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf > /tmp/ShenRuililin_Laidlaw_Stage3Poster.pdf
```

Default: send the uploaded 22 August files with the signed form (student date 23 August). If Professor Bishai explicitly said he examined the 24 August PDF from Email A, send that essay (`605cd8db43072cb5`) instead. Do not mix hashes in the spreadsheet.
