# Feature Specification: a small image or PDF page fills the stage

**Slice**: `specs/158-projector-media-fit`
**Branch**: `feat/158-projector-media-fit`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: "when images or pdfs are smaller than the screen, enlarge it to fit either width or height.
which one is smallest possible. also add a shortcut to switch between fit to width and fit to height
(T key) and add that to shortcut list for images and pdf" — with two projector screenshots: `images.jpeg`
painted 182×277 on a full stage, and the Receipt PDF page painted 612×792 on a full stage.

## What the projector does today

The media screens paint at their own size and only ever shrink. Measured on the compose page at
1920×1200, service 144 (`/projector?service=144`), stage `#projectorScreens` **1856×1104** at (32, 32):

| screen | media | own size | painted | share of the stage's width |
| --- | --- | --- | --- | --- |
| 3 (entry 2) | `images.jpeg` (JPEG) | 182×277 px | **182×277** at (829, 445.5) | 9.8 % |
| 19 (entry 4) | `Receipt-2773-9204.png` (PDF) page 1/1 | 612×792 pt | **612×792** at (654, 188) | 33 % |

Two causes, one per kind:

- `.screen__image { max-width: 100%; max-height: 100% }` (`static/styles/design/projector.css:77`) caps
  an image at the box and never grows it — the browser paints the img at its intrinsic size.
- `paint()` (`static/web/media-pdf.js:48`) computes `Math.min(1, width / page.width, height / page.height)`:
  the leading `1` forbids any scale above one.

The corner cue already reports the file and the page (`images.jpeg · 1/1`), so the operator sees a
correct reading of a page that is too small to read from the room.

## User Scenarios & Testing

### US1 — A small image is enlarged to fill the stage (P1)

**Why this priority**: it is the reported defect — a 182×277 photo projected at 182×277 on a 1920-wide
screen — and the same rule covers the PDF page, so one behaviour fixes both.

**Independent Test**: open the projector on a service whose entry is a small image, with the window at
1920×1200, and measure the painted box: 725×1104, whole, centred, aspect kept.

**Acceptance scenarios**

1. **Given** a stage of 1856×1104 and an image of 182×277, **When** its screen shows, **Then** the image
   is painted 725×1104 (±1 px) — the smaller of 1856/182 and 1104/277 — and the whole image is visible.
2. **Given** an image larger than the stage, **When** its screen shows, **Then** it is painted at the same
   fit, shrinking exactly as it does today.
3. **Given** a landscape image of 787×444 on that stage, **When** its screen shows, **Then** it is painted
   1856×1047 (±1 px): the width is the smaller ratio, so the width is what it fills.

### US2 — A PDF page is enlarged the same way (P1)

**Why this priority**: the second screenshot, and the half of the defect that lives in the painter.

**Independent Test**: open a Letter-sized PDF page on the same 1856×1104 stage; the canvas is 853×1104.

**Acceptance scenarios**

1. **Given** a 612×792 pt page and a stage of 1856×1104, **When** the page is painted, **Then** the canvas
   is 853×1104 (±1 px) — the smaller of 3.03 and 1.39.
2. **Given** the same page at 1024×768 (stage 960×672), **When** it is painted, **Then** the canvas is
   519×672 (±1 px).
3. **Given** a page larger than the stage, **When** it is painted, **Then** it shrinks to the same fit — the
   behaviour is one rule, not a threshold at 1:1.
4. **Given** a sharp display, **When** the page is enlarged, **Then** the canvas is painted at the device
   pixel ratio (up to the painter's existing 6-megapixel cap), so the page does not blur beyond the fit.

### US3 — `T` switches between fit width and fit height (P1)

**Why this priority**: the fit alone cannot satisfy both cases on one screen — a portrait page fitted to
height leaves two thirds of a wide stage empty, and a wide scan fitted to height is small — so the
operator needs the other axis on demand.

**Independent Test**: on the image screen, press `T`: the image fills the width (1856×2824) and is cut
equally above and below; press `T` again: it returns to 725×1104.

**Acceptance scenarios**

1. **Given** a media screen showing at its fit, **When** `T` is pressed, **Then** it fills the stage's
   width, its height follows the aspect, and the excess is clipped equally above and below.
2. **Given** that state, **When** `T` is pressed again, **Then** it fills the stage's height and the
   excess is clipped equally left and right.
3. **Given** a third press, **Then** it is back at fit width — `T` alternates between exactly two states.
4. **Given** a PDF page, **When** `T` is pressed, **Then** the same two states apply to the page (853×1104
   → 1856×2402 → 853×1104), and stepping to another page of the same document keeps the chosen state.
5. **Given** a screen of another kind (text, passage, song, audio, video), **When** `T` is pressed, **Then**
   nothing about media changes: a passage still flips TB/SIM, the rest ignore it.
6. **Given** the projector window is resized while a fit width is chosen, **Then** the media is re-fitted
   at the new stage size in the same state.

### US4 — The overflow can be panned (P1)

**Why this priority**: fit width on a portrait page hides 860 px above and below; without a way to
reach them the operator has traded one unreadable page for another. Panning is what makes the two
fit states usable rather than blind crops.

**Independent Test**: on the image screen at fit width, drag upwards: the image follows the pointer
and stops at the top of the page; roll the wheel down: it moves the other way and stops at the bottom.

**Acceptance scenarios**

1. **Given** a media screen whose painted size exceeds the stage, **When** the pointer is pressed on it
   and dragged, **Then** the media moves with the pointer, in both axes, for an image and for a PDF page.
2. **Given** that state, **When** the wheel is rolled, **Then** the media pans vertically; with Shift held
   it pans horizontally instead.
3. **Given** a pan at either end, **When** the pointer keeps moving, **Then** the media stops with its edge
   on the stage's edge — no gap is ever exposed on any side.
4. **Given** a media screen that fits the stage, **When** it is dragged or the wheel is rolled, **Then**
   nothing moves: there is no overflow to pan.
5. **Given** a pan and then `T`, or a step to another entry, **Then** the new state starts centred.
6. **Given** a press that moves no more than 4 px, **Then** it is still a click to the corner's mouse
   zones — fullscreen first, then previous, next or show/hide words — so panning never swallows navigation.

### US5 — The shortcut is listed where the operator looks (P2)

**Why this priority**: an undiscoverable key is not a feature; the sheet is the only place the projector
documents its keys.

**Independent Test**: press `K`; the sheet carries a group naming images and PDFs with `T` and the two
fits, and the sheet still fits the window at 1280×720 and 1024×768.

**Acceptance scenarios**

1. **Given** the shortcut sheet (`K`), **When** it opens, **Then** a group named for images and PDFs lists
   `T` as the shortcut for fitting width and height.
2. **Given** a 1024×768 window, **When** the sheet opens, **Then** its height is at most the window's and no
   group is clipped.

### Edge Cases

- **When** the media's bytes are unavailable **Then** the missing-file icon shows as it does today, and
  `T` changes nothing (there is no size to fit).
- **When** the image is wider than tall and the width is the smaller ratio **Then** pressing `T` from the
  default goes to fit height — the default is one of the two states, and `T` always offers the other.
- **When** the shortcut sheet is open **Then** `T` does nothing (the sheet owns the keyboard).
- **When** `T` is pressed with Shift, Ctrl or Alt **Then** it is ignored, as today.
- **When** the entry changes to another media entry **Then** the fit state is the default again, not the
  previous entry's choice.
- **When** the window is shorter than the media's own height **Then** the fit is below 1 and shrinks, as it
  does today.
- **When** the media fits and the wheel is rolled over it **Then** nothing happens — it does not step the
  entry or turn the page.
- **When** the shortcut sheet is open **Then** neither dragging nor the wheel pans.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An image screen SHALL paint its image at the scale `min(stage width / image width, stage height / image height)` — above 1 as well as below — whole and centred on the stage. | `projector/R5` (new) |
| FR-002 | A PDF or PowerPoint screen SHALL paint its page at the same scale, computed from the page's own size, and at the display's pixel ratio up to the painter's existing cap. | `projector/R6` (new) |
| FR-003 | With a media screen showing, `T` SHALL switch to fit width (the media spans the stage's width, the excess height clipped equally above and below); a second `T` SHALL switch to fit height (the excess width clipped equally left and right); a third returns to fit width. | `projector/R7` (new) |
| FR-004 | The default fit state SHALL be the one `T` is not currently in: entering a media screen adopts the fit whose scale is the smaller of the two. | `projector/R7` |
| FR-005 | A media screen's fit state SHALL return to the default when a different entry's screen shows, and SHALL persist across the pages of one document. | `projector/R7` |
| FR-006 | The projector SHALL re-fit the showing media when the window's size changes, keeping the chosen state. | `projector/R5`, `projector/R6` |
| FR-007 | The shortcut sheet SHALL list `T` under a group naming images and PDFs, and SHALL keep its current height (677 px at 1080p) so it still fits a 1280×720 window. | `projector/R8` (new) |
| FR-008 | Every other screen kind SHALL behave as it does today: `T` still flips a passage's TB/SIM, and audio and video are unaffected by the fit. | — (no capability change) |
| FR-009 | While a media screen's painted size exceeds the stage on either axis, a pointer drag on the screen SHALL pan the media within the overflow, and the mouse wheel SHALL pan it too — vertically by `deltaY`, horizontally by `deltaX` or `Shift`+`deltaY` — for an image and a PDF page alike. | `projector/R9` (new) |
| FR-010 | The pan SHALL be clamped so a media edge never leaves the stage's edge, and SHALL start at the centre whenever the fit state or the screen changes. | `projector/R9` |
| FR-011 | Panning SHALL NOT eat navigation: a press that moves no more than 4 px remains a click to the corner's mouse zones (entering fullscreen when windowed, then previous, next or show/hide words). | `projector/R9` |
| FR-012 | While a media screen overflows, the pointer over the stage SHALL read `grab`, and `grabbing` while it drags. | `projector/R9` |

### Key Entities

- **Media screen** — one `.screen` holding `[data-media-image]` or `[data-media-pdf]`/`[data-media-slides]`;
  it owns the fit state for as long as it is the active screen.
- **Fit state** — `fit` (the default, the smaller ratio), `fit width`, `fit height`; it is browser-local and
  never saved or sent.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | `images.jpeg` (182×277) paints 725×1104 ±1 on a 1920×1200 window | painted box of `.screen__image` vs today's 182×277 |
| SC-002 | A 612×792 pt page paints 853×1104 ±1 on the same window | painted box of `.screen__pdf-page` vs today's 612×792 |
| SC-003 | At 1024×768 the same media paint 441×672 and 519×672 ±1 | painted boxes at a second window size |
| SC-004 | `T` on the image: 1856×2824 ±1, cut ~860 px above and below; `T` again: 725×1104 ±1 | two measurements and the visible crop |
| SC-005 | `T` on the page: 1856×2402 ±1, cut ~649 px above and below; `T` again: 853×1104 ±1 | two measurements |
| SC-006 | A 787×444 image paints 1856×1047 by default and 1956×1104 after `T` | painted boxes, landscape case |
| SC-007 | The shortcut sheet lists `T` and still fits a 1024×768 window | sheet height ≤ 768, every group's bottom inside the sheet |
| SC-008 | Dragging the fit-width image travels ±860 px vertically and not at all horizontally | painted `y` across the drag: 32 → −828 → 32 |
| SC-009 | The wheel moves the same 860 px per axis and stops at the same ends | `translate` after N notches, clamped at ±860 |
| SC-010 | A 4 px press on a zoomed page still navigates | the showing screen changes once, and no pan is recorded |

## UI/UX

Static preview at `specs/158-projector-media-fit/preview/index.html` — opened directly, no server: the
projector's own stylesheet (bundled faces included), its own sheet markup, media at the review's own
sizes (the service's real files are not committed), and a top bar that switches *Today (1:1)* against
the change. See the preview's `README.md` for what is real and what is substituted.

- **Layout / position**: the media stays centred in its screen, one element only. The stage keeps its
  `32px 32px 64px` padding, so the fitted media is measured against 1856×1104 on a 1920×1200 window.
  A fit-width or fit-height state overflows its box and is clipped by `#projectorScreens`
  (`overflow: hidden`); the overflow is panned (below), never scrolled, never stretched.
- **Pan**: the travel is half the overflow each way, because the media starts centred —

  | state on a 1920×1200 window | painted | travel |
  | --- | --- | --- |
  | image, fit width | 1856×2824 | ±860 px vertically |
  | image, fit height (landscape) | 1956×1104 | ±50 px horizontally |
  | PDF page, fit width | 1856×2402 | ±649 px vertically |

  Drag and wheel move it; the wheel's own notch is ~100 px in Chromium, so a full travel is nine
  notches. Cursor: `grab` while the media overflows, `grabbing` while it is dragged, and the corner's
  own resize cursors return as soon as the media fits again.
- **Size / spacing**: on a 1920×1200 window, the stage is 1856×1104. Painted sizes:

  | media | today | fit (default) | fit width | fit height |
  | --- | --- | --- | --- | --- |
  | `images.jpeg` 182×277 | 182×277 | **725×1104** (×3.99) | 1856×2824 (cut 860 / 860) | 725×1104 |
  | Receipt PDF page 612×792 | 612×792 | **853×1104** (×1.39) | 1856×2402 (cut 649 / 649) | 853×1104 |
  | `random.jpg` 787×444 | 787×444 | 1856×1047 (×2.36) | 1856×1047 | 1956×1104 (cut 50 / 50) |

  On a 1024×768 window (stage 960×672) the same three are: `images.jpeg` 441×672 (fit width 960×1461),
  `random.jpg` 960×541 (fit height 1191×672, cut 116 left/right), the page 519×672 (fit width 960×1242).
- **The shortcut sheet**: 1124×677 at 1920×1200 — the same 677 px it is today, because the new group
  sits in the middle column, the only one with room; the third column would have taken the sheet to
  731 px, five past a 720p window. Measured with the group in place: 992×677 at 1024×768, 1124×677 at
  1280×720 (22 px above and below), every group inside the sheet's frame.
- **Colour / typography**: unchanged — no new colour, no new type. The media keeps its own pixels; a
  private image enlarged beyond its resolution softens, which is the operator's choice to make.
- **States**: fit (default) · fit width · fit height · panned to each of the four ends · drag in
  progress (`grabbing`) · a press that moved 4 px or less (still a click) · missing media (icon, no fit) ·
  landscape media · portrait media · the shortcut sheet open at 1920×1200, 1280×720 and 1024×768.
- **Motion**: none. A fit change is an instant frame, like a page step; no transition is added.

## Assumptions

1. **"Smallest possible" is *contain*.** The fit is the smaller of the two ratios, so the whole media is
   visible and its longer axis touches the stage's edge. The request's words — "fit either width or
   height, which one is smallest possible" — read as one rule, not a threshold at 1:1.
2. **`T` has two states, not three.** The default fit *is* one of them (the smaller ratio), so the first
   `T` offers the other. A third "contain" state would leave the operator guessing which of three he is in.
3. **The fit state is per media screen.** It returns to the default when a different entry shows, and it
   survives the page steps inside one document — a page turn should not undo a deliberate zoom.
4. **Scope is the projector page.** The reading page's Preview dialog keeps today's sizing; its image
   already fits the window, its PDF page does not enlarge. Bringing the dialog to the same rule is a
   follow-up card, not this slice.
5. **No fit indicator in the corner cue.** The painted change is the feedback and the shortcut sheet names
   the key; the cue keeps its filename and page count, which is what the operator reads during a service.
6. **Clipping is a viewport, not a loss.** Fit width on a tall page shows one part of it and hides the
   rest; the hidden part is reached by dragging or the wheel (US4), never by a scrollbar — a projected
   display has none (`body` is `overflow: hidden`), and a scroll track in shot would be worse than none.
   The pan is the whole of the affordance: `grab` over the media, the media moving with the pointer.
7. **Nothing is saved.** The fit state lives in the page, like the showing screen; a reload returns to the
   default fit.
8. **The new group goes in the sheet's middle column**, after *Library Detour*. The sheet is a fixed
   677 px tall at 1080p and 731 px would hang five pixels past a 720p window; the middle column is the
   only one with room (its tallest neighbour is 15 rows against 10).
