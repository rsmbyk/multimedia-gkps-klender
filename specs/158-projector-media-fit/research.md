# Research: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`
**Unknowns remaining**: 0

## D001 — The painted size is set in CSS pixels by the script, not by `object-fit`

- **Decision**: the fit is computed in `projector.js` and written onto the element as an inline
  `width`/`height` in px; the screen carries `is-fitted`, and the CSS drops the `max-width/max-height`
  caps for that state.
- **Rationale**: `object-fit: contain` fills the box but cannot express *fit width* (fill the width,
  overflow the height); `object-fit: cover` crops by the *larger* ratio, which is the opposite of what
  `T` asks. Inline sizes also give the pan a number to clamp against, and give the tests a box to measure.
- **Alternatives considered**: `object-fit` + two wrapper rules — rejected, it cannot produce a
  fit-width state at all; `transform: scale()` on a natural-size element — rejected, it leaves the
  layout box at the natural size, so clipping and centring stop agreeing with what is painted.
- **Provenance**: research — measured in the spec-158 static preview at 1920×1200 and 1024×768.

## D002 — `paint()` gains an optional fit option; the reader's dialog keeps its clamp

- **Decision**: `GKPSMediaPDF.paint(document, page, canvas, width, height, signal, options)` where
  `options = {fit: 'contain' | 'width' | 'height', upscale: boolean}`. Omitted, it behaves exactly as
  today (`contain`, no scale above 1). The projector passes `{fit: mode, upscale: true}`; the reader's
  Preview dialog passes nothing.
- **Rationale**: the leading `Math.min(1, …)` is the defect on the projector and the *specified*
  behaviour of the dialog (spec 117's preview follows the page's own size). One implementation with an
  explicit option keeps both true without a second painter.
- **Alternatives considered**: removing the clamp outright — rejected by the spec's scope assumption
  (the dialog is a follow-up card); duplicating the painter for the projector — rejected, two
  painters drift.
- **Provenance**: research — `static/web/media-pdf.js:48`, `static/web/preview.js:213`, spec 117 §Preview.

## D003 — The fit state is per active media screen and lives in the page

- **Decision**: three closures in `projector.js` — `fitState` (`'fit' | 'width' | 'height'`), `fitPan`,
  and the painted/overflow sizes — reset whenever the active media host changes (the renderers already
  early-return on the same host, so the reset sits beside that test).
- **Rationale**: the spec's FR-005 — a page turn inside one document keeps a deliberate zoom, another
  entry starts at the fit. Storing per host in the page matches how the showing screen is already kept.
- **Alternatives considered**: `localStorage` — rejected, nothing is saved (assumption 7); per-screen
  map keyed by index — rejected, the screens array is rebuilt on every render.
- **Provenance**: research — `static/web/projector.js:212` (`if (host === imageHost) return`) and
  `:281` for the PDF.

## D004 — Pan is a `transform: translate()` clamped to half the overflow

- **Decision**: the media element gets `transform: translate(x, y)` with
  `|x| ≤ (paintedW − stageW)/2` and `|y| ≤ (paintedH − stageH)/2`; the state resets to `0,0` when the
  fit or the host changes.
- **Rationale**: the media is centred in its box, so its overflow is split evenly above/below or
  left/right; half the overflow is exactly the travel that brings either edge to the stage's edge. A
  transform keeps the flex centring and cannot introduce a scrollbar.
- **Alternatives considered**: `overflow: auto` on the box with `scrollLeft/scrollTop` — rejected: a
  scroll track is visible in the projection, and the centred flex item gives no scroll range to start
  from.
- **Provenance**: research — the preview's pan, measured: image at fit width travels ±860 px on a
  1920×1200 window, the Letter page ±649 px, the landscape ±50 px.

## D005 — A drag rides the corner's mouse zones, and 4 px decides drag vs click

- **Decision**: pointer handlers live on `.mouse-zones` (which covers the stage at `z-index: 2`); a
  press that moves more than 4 px pans and sets a flag that the existing click handler consumes; a
  press that stays inside 4 px falls through to today's click (fullscreen first, then previous / next /
  show-hide words). Pointer capture is taken **only once the 4 px is passed**: capture retargets the
  compatibility `click` to the captured element, so capturing on `pointerdown` would send an un-moved
  click to `.mouse-zones` instead of the zone that owns the gesture — and no click would navigate.
- **Rationale**: the zones already own pointer events over the whole stage; raising the media above
  them would trade navigation for panning. A movement threshold is what every canvas viewer uses to
  keep click and drag apart.
- **Alternatives considered**: disabling the zones while a media overflows — rejected at gate 1 (the
  owner kept click-to-navigate); a separate transparent layer — rejected, a third element over the
  stage to keep in step with the other two.
- **Provenance**: research — `static/web/projector.js:885-921` (the click handler and the
  fullscreen-first rule), `.mouse-zones` at `projector.css` (`inset: 0 0 64px; z-index: 2`).

## D006 — The wheel pans; it never navigates or turns a page

- **Decision**: a `wheel` listener on `.mouse-zones` with `{passive: false}`, active only while the
  showing media overflows; `deltaY` pans vertically, `shift` + `deltaY` horizontally, `deltaX` pans
  horizontally. With no overflow the event is not touched at all.
- **Rationale**: the owner's answer at Clarify — "pans the page, exactly like dragging (both kinds)".
  Leaving the event alone when nothing overflows keeps today's inert wheel, and avoids a page turn
  firing from a stray scroll mid-service.
- **Alternatives considered**: page turn at the end of the travel — offered at Clarify and declined.
- **Provenance**: owner decision (Clarify, 2026-10-29); research for the listener shape.

## D007 — The shortcut group goes in the sheet's middle column

- **Decision**: a new group **Image and PDF**, one row (`Fit Width / Fit Height` · `T`), inserted after
  *Library Detour* in the middle column of `projector_controls.html`.
- **Rationale**: measured on the running page, the sheet is 1124×677 with the group in the middle
  column — the same height as today, so it still fits a 1280×720 window (22 px above and below). In the
  third column it becomes 731 px, five past 720p.
- **Alternatives considered**: the third column beside *Display* — rejected on that measurement; a row
  inside *Display* — 713 px, three pixels inside 720p, too tight to be safe.
- **Provenance**: research — measured on the compose page at 1920×1200, 1366×768, 1280×720, 1024×768.

## D008 — Verification is Playwright E2E; the repo has no JS unit runner

- **Decision**: each `Verified by: test` row names a case in `tests/e2e/test_image_display.py` or
  `tests/e2e/test_pdf_display.py`; both modules already fabricate a PNG (`_png`) and a three-page PDF
  (`_pdf`) and route the companion, so a stage-sized measurement needs no new fixture.
- **Rationale**: the projector is user-visible acceptance, which the repo's TDD custom puts in
  Playwright E2E; there is no JavaScript test harness to add unit coverage for `fitMedia()`.
- **Alternatives considered**: a Python unit test over the maths — rejected, the maths is in the page
  and would have to be mirrored to be tested; a `node` harness — rejected, it adds a toolchain the repo
  does not have.
- **Provenance**: research — `docs/PROCESS.md` (TDD custom), `tests/e2e/test_image_display.py:20-71`.

## Open

<!-- empty: Phase 0 finished, nothing blocks Phase 1 -->
