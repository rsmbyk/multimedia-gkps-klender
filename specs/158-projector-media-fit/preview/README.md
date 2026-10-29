# Preview — a small image or PDF page fills the stage

**Open**: `index.html` — double-click it, or `xdg-open index.html`. It needs no server and no
network: every stylesheet, font and media file it uses sits in this folder.

## What it is

The projector's own screen markup, stylesheet and shortcut sheet, showing the behaviour spec 158
proposes: media is enlarged to the fit that shows all of it, `T` switches between fit width and fit
height, and the overflow that leaves is panned by dragging or with the wheel.

The top bar is preview chrome (`Image 182×277`, `Landscape 787×444`, `PDF page 612×792`,
`Fit (the change)`, `Today (1:1)`, `Press T`, `Shortcuts (K)`); the corner cue and the sheet are the
product's own.

## What is real, and what is substituted

| Part | Where it comes from |
| --- | --- |
| `styles/design/*.css`, incl. the cursor files | copied verbatim from `static/styles/design/`; `fonts.css` keeps its markup and only re-points its two font URLs at the repo's own `static/assets/fonts/` (so the 1.2 MB faces are not committed twice) — the sheet measures 1124×677 here and on the app, so the face is the real one |
| shortcut sheet and key glyphs | extracted from `multimedia/web/templates/reading/projector_controls.html` by `build_preview.py`, with the new **Image and PDF** group inserted after *Library Detour* |
| screen markup, cue, `.screen__image-box` / `.screen__pdf-box` | the projector's own classes and structure (`reading/projector.html`) |
| `files/image-182x277.png` (182×277), `files/image-787x444.png` (787×444) | generated stand-ins of the sizes the review used — a banded gradient, so a crop or a pan is visible |
| `files/page-612x792.pdf` page 1, 612×792 pt | a generated page (heading + 28 lines) and its 4× bitmap (`files/page-612x792.png`, rendered with `pdftoppm -r 288`), because a page opened from `file://` cannot import pdf.js's ES module |
| `preview.js` | the intended fit maths and the pan (drag, wheel, clamp), plus the preview chrome — **not** the shipping script; the product's `projector.js` gets the same rules after gate 2 |

The one substitution that matters: a preview page cannot read the local Media Library companion (its
CORS allowlist names the app's own port), so the media come from `files/` — at the review's own sizes,
182×277, 787×444 and 612×792 pt. The real files belong to the service and are not committed to the
repository; drop your own next to the stand-ins to see it with a photograph.

## The numbers it should show

At **1920×1200** (stage 1856×1104):

| screen | today | fit | after `T` |
| --- | --- | --- | --- |
| Image 182×277 | 182×277 | 725×1104 (×3.99) | 1855×2824, cut 860 above/below |
| Landscape 787×444 | 787×444 | 1855×1047 (×2.36) | 1956×1104, cut 50 left/right |
| PDF page 612×792 | 612×792 | 853×1104 (×1.39) | 1856×2401, cut 649 above/below |

At **1024×768** (stage 960×672): image 441×672 (fit width 960×1461), landscape 960×541 (fit height
1191×672), page 519×672 (fit width 960×1242). The sheet is 992×677 and stays inside the window.

## Rebuilding

```sh
python3 build_preview.py
```

It re-copies the stylesheets and fonts, regenerates the three media stand-ins and the page bitmap, and
re-extracts the sheet and key glyphs from `projector_controls.html` — so the preview follows the
template instead of drifting from it, and the repository carries no service media.

## What it cannot show

The real bytes arriving from the companion (`GKPSMediaImage.load` / `GKPSMediaPDF.load`), the page
count in the cue stepping through a multi-page document, and the missing-file icon path. Those are
unchanged by this slice.

It also cannot show the corner's mouse zones, which the real page lays over the stage (40 % / 20 % / 40 %,
for previous / show-hide words / next) and which a drag must not swallow: in the product a press that
moves 4 px or less is still their click, and only movement pans. Here there are no zones, so every
press on a zoomed page pans.
