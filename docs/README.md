# Public companions (`docs/`)

Exposure-only pages for the Laidlaw Heat Project. **No** CHD/HF coefficients, **no** stroke findings, **no** HA rows.

| Path | What it is |
|---|---|
| [`index.html`](index.html) | Hub |
| [`geo/`](geo/) | Hong Kong spatial thermal field (Leaflet lattice + OLS / Moran / variogram) |
| [`peers/`](peers/) | Sixteen-city climate-space atlas |
| [`lsn/`](lsn/) | HKO Headquarters monthly ribbon for the Laidlaw Scholar Network |

## Preview this branch (works before Pages is enabled)

```text
https://htmlpreview.github.io/?https://raw.githubusercontent.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/index.html
https://htmlpreview.github.io/?https://raw.githubusercontent.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/geo/index.html
https://htmlpreview.github.io/?https://raw.githubusercontent.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/peers/index.html
```

## GitHub Pages (after merge)

The repository does not yet serve `https://bobshenruililin.github.io/Laidlaw-Heat-Project/` (404 as of 14 August 2026). To turn these pages into a programme URL:

1. GitHub → Settings → Pages → Source: **GitHub Actions**, or Deploy from branch `main` / folder `/docs`.
2. Merge this branch to `main`.
3. Confirm `docs/.nojekyll` is present so Leaflet paths are not stripped.

Bob still owns the Laidlaw Scholars **website blog** (`reports/blog/`) and the LSN paste. These `docs/` pages are companions he can link from those posts after a privacy pass.
