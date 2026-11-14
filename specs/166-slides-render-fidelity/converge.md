# Converge — spec 166

**Pass 1 · 2026-10-30** · checked against `plan.md`'s traceability table.

## What was run

- `manage.py test multimedia` — **439 tests, OK** (after `collectstatic`; without a built manifest the
  nine page-rendering tests error on `Missing staticfiles manifest entry for 'assets/gkps.png'`, which
  reproduces on unmodified `origin/develop` in a checkout with no `_static/`, so it is the local
  environment and not this slice).
- `manage.py test multimedia.test_local_media` — **26 tests, OK**, including the three new cases.
- `docker build` of the slice's image, which runs `python -m multimedia.slide_fonts` — **passes**; the
  same command inside the built image prints the mapping below and exits 0.
- `docker run` with and without a font directory mounted at `/usr/share/fonts/operator`.

## Row by row

| Row | Verified by | Evidence |
| --- | --- | --- |
| FR-001 | inspection | `python -m multimedia.slide_fonts` inside the image: `Calibri → Carlito`, `Calibri Light → Carlito`, `Cambria → Caladea`, `Arial → Liberation Sans`, `Arial Narrow → Liberation Sans Narrow`, `Times New Roman → Liberation Serif`, `Courier New → Liberation Mono`, `Britannic Bold → Noto Sans`, `Berlin Sans FB Demi → Noto Sans` — nine families, none monospaced |
| FR-002 | inspection | `libreoffice --version` inside the image → **LibreOffice 25.2.3.2** |
| FR-003 | test | `test_converter_identity_changes_when_the_fonts_change`, `test_converter_without_fontconfig_keeps_its_identity`, `test_converter_version_changes_cache_key` (assertions unchanged), `test_concurrent_slide_requests_share_one_conversion`, `test_slide_display_keeps_original_identity_and_reuses_private_pdf` |
| FR-004 | inspection | a TTF mounted at `/usr/share/fonts/operator` makes `fc-match "JetBrainsMono Nerd Font"` answer the file and moves the derivative key `1ff909dc0f66d2b9` → `da61d371f6fe5fec`; unmounted, the companion behaves as before |
| FR-005 | test + build | `test_a_monospaced_answer_is_a_violation`, `test_a_metric_compatible_answer_is_not_a_violation`; the Dockerfile's `RUN python -m multimedia.slide_fonts` fails a build that regresses |
| FR-006 | test + manual | the 439-test run; `git diff --stat` touches 8 tracked files and adds 4 (image, compose, entrypoint, docs, capability, one module, one config, one card, one spec pack) — no route, payload, model, migration or projector file |
| SC-001 | manual | words on the deck's Calibri/Times New Roman pages: page 3 **0.7 pt**, page 10 **0.03 pt** (`TOK-TOK` y 83.049 vs 83.082, x identical), page 12 **0.0**, page 14 **0.7**, page 15 **0.9** |
| SC-002 | manual | page 1's title ink **477 × 199 px at (95, 90)**; the reference render puts it at (95, 91) |
| SC-003 | manual | page 2's band holds **5 words** at x **475.45**, **676.75**, **785.56**, y **470.16** — the reference's own coordinates; today's PDF holds **17** |
| SC-004 | test | the violation case above; the built image runs the guard |
| SC-005 | test | the identity cases above |
| SC-006 | test | the 439-test run |

## Findings

**F1 — `partial` — the two Office display faces still move between renders.** `Britannic Bold` and
`Berlin Sans FB Demi` are drawn in Noto Sans in the image (static, `NotoSans-Regular.ttf`) and in Noto
Sans variable on the reference machine (`NotoSans[wght].ttf`), whose taller line box puts page 2's
yellow paragraph 20 pt lower there. This is the substitute, not the layout: it is US3's subject, and
the operator's own fonts remove it. *Disposition: accepted — recorded in R2's substitute clause and in
`docs/local-media-companion.md`.*

**F2 — `partial` — three of the four pages that still differ in pixels differ by antialiasing only.**
Pages 3, 4, 10 and 15 keep a pixel distance of 4,600–9,100 (RMSE, 96 dpi) against the reference while
their words land within 0.7 pt: blurring both renders by 1.2 px collapses the distance to
1,800–2,900, and page 10's word boxes are identical to three decimals. The cause is the reference's
Type 3 embedding against the image's TrueType. *Disposition: accepted — sub-pixel, invisible at
projection size.*

**F3 — `missing` — `test_local_media.py` did not assert the absence of a monospaced face.** Plan's D007
declared it; added to `test_real_impress_converts_verified_pptx_when_installed` (the fixture deck is set
in Calibri and Times New Roman, so a `Mono` in `/BaseFont` is exactly the failure this slice removes).
*Disposition: fixed in this pass.*

**F4 — `unrequested` — none.** The diff adds nothing the spec did not ask for: no sweeper for old
derivatives, no conversion of anything but PowerPoint, no change to the projector.

## Outcome

**Converged**, with F1 and F2 as accepted gaps (both are the substitute face and the rasteriser, not the
layout the spec names) and F3 fixed. Nothing blocks Fold.
