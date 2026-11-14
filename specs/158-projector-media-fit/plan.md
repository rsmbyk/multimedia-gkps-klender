# Implementation Plan: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`
**Branch**: `feat/158-projector-media-fit`
**Bump**: `minor` — 1.22.10 → 1.23.0 (a new user-visible capability: media fills the stage and can be
zoomed and panned; nothing existing changes shape)
**Preview**: `specs/158-projector-media-fit/preview/index.html` — static, opened directly

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5, `'use strict'`, IIFEs) in `static/web/projector.js` and `static/web/media-pdf.js`; CSS in `static/styles/design/projector.css`; Playwright (Python) for the tests |
| Primary dependencies | none added |
| Storage | none — the fit and the pan are page state, like the showing screen |
| Testing | `tests/e2e/test_image_display.py` and `tests/e2e/test_pdf_display.py`, both already fabricating a PNG and a three-page PDF and routing the companion |
| Target platform | every browser the app supports; the projector is Chromium on the operating machine |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | one layout read per fit (the box rect), one `transform` write per pan frame; the PDF repaints only on a fit change or a resize, never on a pan |
| Constraints | no markup change beyond the sheet's new group; no endpoint, payload, model or migration; the reader's Preview dialog keeps today's sizing; `T` keeps flipping a passage's TB/SIM; the sheet keeps its 677 px height |
| Scale / scope | ~90 lines in `projector.js`, ~8 in `media-pdf.js`, ~8 CSS rules, one group of markup, six E2E cases |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
Constraints row above stands in its place.

Re-checked after Phase 1: **pass** — the design adds no file, no request, no dependency and no stored
state; the one shared interface (`paint`) grows an optional argument whose absence is today's behaviour
(`contracts/none.md`).

## Phase 0 — Research

See `research.md`. Eight decisions, each measured or read on the running page: inline px rather than
`object-fit` (D001), an optional fit option on the painter (D002), fit state per active host (D003),
`translate` clamped to half the overflow (D004), the 4 px drag/click threshold on the corner's zones
(D005), the wheel pans and nothing else (D006, owner's Clarify answer), the sheet's middle column (D007),
Playwright E2E as the only harness (D008). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the page-local fit state: `fitState`, `painted`, `overflow`, `pan`, and the five
  invariants that keep a gap from appearing and the aspect ratio from stretching.
- `contracts/` — `none` (`contracts/none.md`): no external interface changes; the page-internal
  `GKPSMediaPDF.paint(…, options)` is recorded there because two scripts share it.
- `quickstart.md` — the isolated test database, the two modules, the six named cases, and the two things
  that cannot be run (a live look at this branch against the real companion, and a JS unit harness).

### The design

**1. CSS** — `static/styles/design/projector.css`, beside the media rules (~line 76):

```css
/* A fitted screen carries its own px size, so the caps that keep an image at 1:1 must step aside,
   the element must not be flex-shrunk back, and the excess the fit leaves is clipped here. */
.screen.is-fitted .screen__image,
.screen.is-fitted .screen__pdf-page { max-width: none; max-height: none; flex: none; }
.screen.is-fitted .screen__image-box,
.screen.is-fitted .screen__pdf-box { overflow: hidden; }
/* The pointer says the media can be dragged exactly when it overflows. */
body.projector.media-overflow .mouse-zone { cursor: grab; }
body.projector.media-overflow .mouse-zone:active { cursor: grabbing; }
```

**2. The fit and the pan** — `static/web/projector.js`, beside the media renderers (lines 198-305):

```js
var fitState = 'fit';                       // 'fit' | 'width' | 'height'
var fitPan = {x: 0, y: 0};
var fitOverflow = {x: 0, y: 0};
var fitHost = null;                         // the host whose fit this is

function fitMedia(host, natural, element) {
  if (host !== fitHost) { fitHost = host; fitState = 'fit'; fitPan = {x: 0, y: 0}; }
  var box = host.getBoundingClientRect();
  var byWidth = box.width / natural.w, byHeight = box.height / natural.h;
  var scale = fitState === 'width' ? byWidth : fitState === 'height' ? byHeight
    : Math.min(byWidth, byHeight);
  var size = {w: Math.floor(natural.w * scale), h: Math.floor(natural.h * scale)};
  host.closest('.screen').classList.add('is-fitted');
  element.style.width = size.w + 'px';
  element.style.height = size.h + 'px';
  fitOverflow = {x: Math.max(0, (size.w - box.width) / 2), y: Math.max(0, (size.h - box.height) / 2)};
  body.classList.toggle('media-overflow', Boolean(fitOverflow.x || fitOverflow.y));
  applyPan(element);
  return size;
}

function applyPan(element) {
  fitPan.x = Math.min(fitOverflow.x, Math.max(-fitOverflow.x, fitPan.x));
  fitPan.y = Math.min(fitOverflow.y, Math.max(-fitOverflow.y, fitPan.y));
  element.style.transform = fitPan.x || fitPan.y
    ? 'translate(' + Math.round(fitPan.x) + 'px,' + Math.round(fitPan.y) + 'px)' : '';
}
```

`renderImageScreen` calls `fitMedia(host, {w: result.width, h: result.height}, image)` after the blob
decodes; `paintPDFScreen` passes the same mode to the painter and takes the returned size:

```js
window.GKPSMediaPDF.paint(pdfDocument, pdfPage, canvas, bounds.width, bounds.height, signal,
  {fit: fitState, upscale: true})
  .then(function (size) {
    fitHost = pdfHost;
    fitOverflow = {x: Math.max(0, (size.width - bounds.width) / 2),
                   y: Math.max(0, (size.height - bounds.height) / 2)};
    body.classList.toggle('media-overflow', Boolean(fitOverflow.x || fitOverflow.y));
    applyPan(canvas);
  });
```

`clearImageScreen` / `clearPDFScreen` drop `is-fitted`, the transform, `media-overflow` and `fitHost`.

**3. The painter** — `static/web/media-pdf.js:42-65`:

```js
async function paint(document, number, canvas, availableWidth, availableHeight, signal, options) {
  var fit = (options && options.fit) || 'contain';
  var upscale = Boolean(options && options.upscale);
  ...
  var byWidth = availableWidth / source.width, byHeight = availableHeight / source.height;
  var scale = fit === 'width' ? byWidth : fit === 'height' ? byHeight : Math.min(byWidth, byHeight);
  if (!upscale) scale = Math.min(1, scale);          // the dialog's rule, unchanged
  ...
}
```

**4. The key** — the `T` branch at `projector.js:1253` becomes two cases:

```js
if (!event.ctrlKey && !event.shiftKey && key === 't') {
  event.preventDefault();
  if (imageHost || pdfHost) toggleFit(); else flipTranslation();
  return;
}
```

**5. Panning** — pointer and wheel handlers on `.mouse-zones` (`projector.js:885`; no element variable
exists yet, so `document.querySelector('.mouse-zones')` at the top): a press records the origin;
movement past 4 px sets `panDrag.moved`, takes `setPointerCapture` and pans; release sets
`suppressClick` so the existing click handler (fullscreen, previous, next, hide words) returns early
exactly once. Capture is taken *after* the threshold — capturing on `pointerdown` would retarget an
un-moved click to `.mouse-zones` and kill navigation (D005). The wheel pans while `media-overflow` is
set and is left untouched otherwise.

**6. The sheet** — `multimedia/web/templates/reading/projector_controls.html`, middle column after
*Library Detour*:

```html
<section class="group">
  <h3>Image and PDF</h3>
  <p class="row"><span class="fn">Fit Width / Fit Height</span><span class="combo"><span class="chord"><span class="k">T</span></span></span></p>
</section>
```

**What is deliberately not done.** No fit indicator in the cue, no saved fit, no page turn on the wheel,
no second painter, no `object-fit` gymnastics, no change to `preview.js` or the reader's dialog, no
markup change to the media screens, and no new key.

## Traceability

| Requirement / scenario | Component / file | Verified by |
| --- | --- | --- |
| FR-001 an image paints at the smaller ratio, above 1 | `static/web/projector.js` `fitMedia()`; `projector.css` `.screen.is-fitted` | `test` → `tests/e2e/test_image_display.py::ImageDisplayE2ETests::test_projector_enlarges_a_small_image_to_the_stage` |
| FR-002 a PDF page paints at the same ratio, at pixel ratio | `static/web/media-pdf.js` `paint()`; `projector.js` `paintPDFScreen()` | `test` → `tests/e2e/test_pdf_display.py::PDFDisplayE2ETests::test_projector_enlarges_a_pdf_page_to_the_stage` |
| FR-003 `T` alternates fit width ↔ fit height | `projector.js` `toggleFit()` + the keydown branch | `test` → `test_image_display…::test_projector_t_toggles_fit_width_and_height`; `test_pdf_display…::test_projector_t_toggles_the_page_fit_and_keeps_it_across_pages` |
| FR-004 the default is the smaller ratio | `projector.js` `fitMedia()` first call | `test` → the same two cases assert the pre-`T` size |
| FR-005 reset on another entry, kept across a document's pages | `projector.js` `fitHost` test in `fitMedia()` | `test` → `test_pdf_display…::test_projector_t_toggles_the_page_fit_and_keeps_it_across_pages` |
| FR-006 a resize re-fits, keeping the state | `projector.js` resize listener | `test` → `test_image_display…::test_projector_enlarges_a_small_image_to_the_stage` resizes to 1024×768 in the same case |
| FR-007 the sheet lists `T`, height unchanged | `multimedia/web/templates/reading/projector_controls.html` | `test` → `test_image_display…::test_shortcut_sheet_lists_the_fit_key`; `inspection` — the sheet's 1124×677 measurement in `research.md` D007 |
| FR-008 other screen kinds unchanged | `projector.js` keydown branch | `test` → `tests/e2e/test_projector.py` (passage flip, arrows, cue); `inspection` — the diff adds no branch to those paths |
| FR-009 drag and wheel pan the overflow | `projector.js` pointer + wheel handlers | `test` → `test_image_display…::test_projector_pans_the_overflow_by_drag_and_wheel` |
| FR-010 the pan clamps, and resets with the fit | `projector.js` `applyPan()` | `test` → the same case drags past the end, asserts it stops there, and that `T` returns the pan to the centre |
| FR-011 a ≤4 px press still navigates | `projector.js` `panDrag.moved` + `suppressClick` | `test` → `test_image_display…::test_projector_press_without_drag_still_steps` |
| FR-012 `grab` / `grabbing` while it overflows | `projector.css` `body.projector.media-overflow` | `test` → `test_image_display…::test_projector_pans_the_overflow_by_drag_and_wheel` asserts the computed cursor |
| SC-001/SC-002 the two painted sizes at 1440×900 | as FR-001 / FR-002 | `test` → the two enlarging cases (1376×688 and 603×804) |
| SC-003 the same at a second window size | as FR-001 / FR-002 | `test` → the resize inside `test_projector_enlarges_a_small_image_to_the_stage` (1376×688 → 960×480 on a 960×672 stage); the real files' 441×672 / 519×672 are measured in the preview, `spec.md §UI/UX` |
| SC-004/SC-005 `T`'s two sizes and crops | `projector.js` `toggleFit()` | `test` → both `…toggles…` cases (1608×804 cut 116; 1376×1834 cut 515) |
| SC-006 the landscape case | `fitMedia()` | `test` → `test_image_display…::test_a_landscape_image_fits_by_its_width` (a 24×6 PNG) |
| SC-007 the sheet inside a 1024×768 window | `projector_controls.html` + the sheet's CSS | `inspection` — measured at 992×677 with the group in place (`spec.md §UI/UX`); `test` → the sheet case asserts the group exists |
| SC-008/SC-009 the pan travels and stops | `applyPan()` | `test` → the panning case asserts `translate` and its clamp |
| SC-010 a 4 px press navigates | `panDrag.moved` | `test` → the press-without-drag case |
| US1 AC2 an image larger than the stage shrinks as before | `fitMedia()` | `test` → `test_image_display…::test_a_large_image_still_shrinks` |
| US4 AC4 no overflow, no pan | `applyPan()` + handlers | `test` → the press-without-drag case on the default fit; the wheel is asserted inert in the panning case |
| US2 AC4 pixel ratio up to the cap | `media-pdf.js` `paint()` | `inspection` — the ratio expression is untouched (`Math.min(devicePixelRatio, 2, sqrt(6e6/area))`) |

**Split**: 19 test · 3 inspection · 0 manual. The test rows rest on 9 E2E cases across two modules
(image: enlarge, landscape, large-shrinks, `T`, pan, press-without-drag, sheet; pdf: enlarge, `T` and
page turn) — under TDD each case is a task of its own that must fail first.
