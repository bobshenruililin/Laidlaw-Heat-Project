# Laidlaw public companions and programme deliverables — 14 August 2026

Bob asked whether the geospatial work can contribute to Laidlaw deliverables, and noted that “we do have a website somewhere.”

## There are two “websites”

| What people say | What it actually is | Status |
|---|---|---|
| **Laidlaw Scholars website** | Programme blog in the MIT Admissions register. Drafts live in `reports/blog/`. Bob posts them on the Laidlaw site after a voice/privacy pass. | Drafts exist. Nothing is auto-published. |
| **Project GitHub Pages** | `docs/` served at `https://bobshenruililin.github.io/Laidlaw-Heat-Project/` | Workflow is in `.github/workflows/github-pages.yml`. The URL still **404s** until Bob enables Settings → Pages → GitHub Actions and this branch reaches `main`. |

They are not the same object. The programme site is where Bob writes in the first person. GitHub Pages is the public map/ribbon companion those posts (and LSN) can link.

## How today’s maps map onto frozen vs living surfaces

| Deliverable | Locked? | May these maps enter? |
|---|---|---|
| Stage 3 research report PDF (`6136e85a654502a0…`) | **Yes — frozen** | No. Do not rebuild or insert lattice numbers. |
| A0 poster PDF (`4f7c1e408ae2d31f…`) | **Yes — frozen** | No. |
| Hogan live manuscript | Live authority; weather paragraph is Hogan’s | Hogan *cards* only. Do not paste mosaic flags as HKO. |
| LSN research-project summary | Draft; Bob’s privacy pass | Yes — link the hub after the pass. No coefficients. |
| Laidlaw website blog | Drafts; Bob’s privacy pass | Yes — `a_city_is_not_a_point.md`, `the_river_has_a_temperature.md`, `a_field_has_modes.md`. 3 C’s Network object is `character_leadership_global_mindset.md` (separate deadline 2027). |
| GitHub Pages public companions | Living `docs/` | Yes — hub, field laboratory, Hong Kong lattice, PRD mosaic, peer atlas, LSN ribbon. |
| HKU 2a form + Network essay URL | Human | Worksheet only. Official DOCX stays off git. Due 31 August 2026. |

## Preview until Pages is on

Prefer **raw.githack** (correct MIME types for Leaflet JS). htmlpreview often 404s companion scripts.

- Hub: https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/index.html
- Field laboratory: https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/field/index.html
- PRD mosaic: https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/prd/index.html
- Hong Kong lattice: https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/geo/index.html
- Peer cities: https://raw.githack.com/bobshenruililin/Laidlaw-Heat-Project/cursor/peer-cities-thermal-atlas-1754/docs/peers/index.html

Local: `python3 -m http.server 8765 --directory docs`

## One human step that turns this into a programme URL

GitHub → this repo → Settings → Pages → Source: **GitHub Actions**. Merge to `main`. Then the Laidlaw blog and LSN paste can use a stable `github.io` link instead of htmlpreview.
