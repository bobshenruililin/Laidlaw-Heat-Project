# Public companions (`docs/`)

Exposure-only pages for the Laidlaw Heat Project. **No** CHD/HF coefficients, **no** stroke findings, **no** HA rows.

These pages are **not** the Laidlaw Scholars programme website. That website is the first-person blog in `reports/blog/`, which Bob posts after a voice/privacy pass. `docs/` is the map/ribbon companion those posts and the LSN summary can link. Routing: [`reports/laidlaw_public_companions_2026-08-14.md`](../reports/laidlaw_public_companions_2026-08-14.md).

| Path | What it is |
|---|---|
| [`index.html`](index.html) | Hub |
| [`prd/`](prd/) | Pearl River Delta mosaic (Leaflet + OLS / SLX / SAR-2SLS / Gi* / month slider) |
| [`geo/`](geo/) | Hong Kong spatial thermal field (Leaflet lattice + OLS / Moran / variogram) |
| [`peers/`](peers/) | Sixteen-city climate-space atlas |
| [`lsn/`](lsn/) | HKO Headquarters monthly ribbon for the Laidlaw Scholar Network |

## Preview this branch (works before Pages is enabled)

Prefer **raw.githack** (correct MIME types for JS). htmlpreview often fails to load `*_embed.js`.

```text
https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/index.html
https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/prd/index.html
https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/geo/index.html
https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/peers/index.html
```

Local: `python3 -m http.server 8765 --directory docs`

## GitHub Pages (after merge)

The repository does not yet serve `https://bobshenruililin.github.io/Laidlaw-Heat-Project/` (404 as of 14 August 2026). To turn these pages into a programme URL:

1. GitHub → Settings → Pages → Source: **GitHub Actions**, or Deploy from branch `main` / folder `/docs`.
2. Merge this branch to `main`.
3. Confirm `docs/.nojekyll` is present so Leaflet paths are not stripped.

Bob still owns the Laidlaw Scholars **website blog** (`reports/blog/`) and the LSN paste. These `docs/` pages are companions he can link from those posts after a privacy pass.
