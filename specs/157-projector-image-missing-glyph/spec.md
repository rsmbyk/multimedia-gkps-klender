# Feature Specification: the projector's image placeholder waits for the image to fail

**Slice**: `specs/157-projector-image-missing-glyph`
**Branch**: `fix/157-projector-image-missing-glyph`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: a report against `/projector` — "why is there that icon beside the image in projector page?" — with a screenshot of an image screen at 1920×1200

## What the page does today

An image screen carries the picture and, 80px to its right, the "image unavailable" glyph. The glyph is
the screen's own placeholder (`screen__image-missing`), and it is meant to appear only when the bytes
fail. Two faults keep it on every image screen:

```django
{% if screen.image_sha256 %}<div class="screen__image-box" data-media-image="{{ screen.image_sha256 }}">
  <img class="screen__image" alt="" hidden>
  <svg class="screen__image-missing" viewBox="0 0 48 48" aria-hidden="true">…</svg>   ← no `hidden`
</div>{% endif %}
```

`renderImageScreen` (`static/web/projector.js:211`) then tries to hide it with a property:

```js
image.hidden = true;
missing.hidden = true;        // ← an expando on an SVGSVGElement
…
missing.hidden = false;       // ← the failure branch, equally inert
```

`hidden` lives on `HTMLElement`, not on `SVGElement`: there is no such descriptor on the element's
prototype chain, so the assignment lands as a plain JS property, the `hidden` **attribute** the CSS keys
on (`.screen__image-missing[hidden] { display: none }`, `projector.css:78`) is never written, and the
glyph stays painted. Measured in Chromium against a real `SVGSVGElement`: after `svg.hidden = true`,
`hasAttribute('hidden')` is `false` and `display` is `block`.

The same file does it correctly for the other four kinds — audio (`:111`), video (`:159`) and PDF/slides
(`:286`) all use `setAttribute('hidden', '')` / `removeAttribute('hidden')` on a glyph that starts
`hidden` in the markup. Its preview-modal counterparts (`static/web/preview.js`) are correct too: those
placeholders are `<div>`s.

Measured on the reported screenshot, 1920×1200, an 800×456 image:

| | the picture | the glyph |
| --- | --- | --- |
| box | x 520–1319 | drawing x 1330–1389, in an 80px box from 1320 |
| vertical centre | y 584 | y 583.5 |

One flex row (`screen__image-box`, `align-items: center`), so the glyph's 80px box is part of what is
centred: the pair spans 520–1400 and the picture itself sits **40px left of the page's middle**.

**Why the suite did not see it.** `tests/e2e/test_image_display.py::test_missing_preview_and_projector_icon`
asserts that the glyph **is visible** when the bytes 404 — and passes today for the wrong reason, because
the glyph is visible no matter what. `test_projector_displays_image_only_on_its_screen` reads the
`<img>`'s natural size and never looks at the glyph. No case ever asserted the loaded state's absence.

## User Scenarios & Testing

### US1 — An image screen shows the picture alone, and the glyph only when the bytes fail (P1)

**Why this priority**: it is the reported symptom, it is on screen for the whole time an image is
projected, and it costs the congregation 40px of symmetry on every image.

**Independent Test**: open the preview, press `Image loaded`, then `Bytes failed (404)`: the left board
shows the picture plus the glyph and an image 40px off the middle; the right board shows the picture
alone, on the middle, and the glyph alone when the bytes fail.

**Acceptance scenarios**

1. **Given** an image screen whose bytes arrive, **When** the screen is the active one, **Then** the
   picture is painted, the placeholder's computed `display` is `none`, and the picture's centre is the
   stage's middle.
2. **Given** an image screen whose fetch fails, **When** it is the active one, **Then** the placeholder
   is painted 80×80 on the middle and no picture is.
3. **Given** an image screen that has just become active and whose fetch has not settled, **Then** the
   screen paints neither the picture nor the placeholder.
4. **Given** a screen that failed while it was active, **When** the operator moves to another screen and
   back, **Then** it is drawn afresh — nothing of the failed state survives the move.

### US2 — The suite cannot pass this again by accident (P2)

**Why this priority**: the green test is what let the defect ship; a case that asserts the glyph is
visible without asserting when it is not tests nothing.

**Independent Test**: run the image-display module against the code this slice starts from; the case
described here must be red there and green after.

**Acceptance scenarios**

1. **Given** a projector image screen whose bytes arrive, **When** the case reads the active screen,
   **Then** the placeholder is not visible and the picture is.
2. **Given** the same screen with the companion answering 404, **Then** the placeholder is visible and
   the picture is not.

### Edge Cases

- **When** the image decodes but the object URL is revoked on a move, **Then** the arrived screen starts
  from its own empty state: no glyph, no stale picture.
- **When** the companion answers 200 with bytes that are not an image, **Then** the load rejects and the
  glyph is painted — the failure branch, unchanged.
- **When** the fetch is aborted (the operator moved on), **Then** the abort changes nothing: the screen
  it left is already cleared, and the arriving one is cleared by its own render.
- **When** a screen holds an image whose natural size is wider than the stage, **Then** the only box that
  changes is the glyph's: it takes no space while hidden, so the picture scales and centres as before.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An image screen whose bytes arrive SHALL paint the picture and SHALL NOT paint the placeholder: by default the placeholder is hidden, and it becomes visible only on a failed load. | `new: projector` → R3 |
| FR-002 | An image screen whose fetch fails SHALL paint the placeholder and SHALL NOT paint a picture, in the screen the operator is on. | `new: projector` → R3 |
| FR-003 | A screen that stops being active SHALL drop its failed state, so a later visit draws it from its own empty state. | `new: projector` → R3 |
| FR-004 | The image placeholder SHALL be toggled the same way the audio, video, PDF and slides placeholders already are — through the `hidden` attribute — so the file has one mechanism. | `new: projector` → R3 |
| FR-005 | The E2E case SHALL assert both outcomes: the placeholder absent when the picture loaded, present when the bytes fail. | `new: projector` → R3 |
| FR-006 | Nothing else changes: no route, payload, template geometry, size, colour or copy; the audio, video, PDF and slides placeholders keep their behaviour and their cases. | `new: projector` → R3 |

### Key Entities

- **Image screen** — one `section.screen` holding `div.screen__image-box[data-media-image]`, its
  `<img class="screen__image">` and its `svg.screen__image-missing`. Rendered by the server, one per
  image entry, and shown one at a time.
- **Placeholder** — that `<svg>`: 80×80, `#3b3933` stroke on the canvas, an image frame with a diagonal
  slash. Decorative (`aria-hidden`), takes no pointer, holds no text.
- **Load outcome** — three states the screen can be in: *pending* (nothing painted), *loaded* (picture),
  *failed* (placeholder). Set by `window.GKPSMediaImage.load`'s promise and the player's error callback.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | With the bytes loaded, the active image screen's placeholder has computed `display: none`, and the picture's centre is the stage's middle (±1px). | `preview/probe.py`, `loaded`: `920 ÷ 960` **today**, `960 ÷ 960` after |
| SC-002 | With the fetch answered 404, the placeholder is painted 80×80 on the middle and no picture is. | `preview/probe.py`, `failed`: `80×80 at x 920–1000`, image `—` |
| SC-003 | Before the fetch settles, the screen paints neither. | `preview/probe.py`, `pending`: today paints the glyph, the slice paints nothing |
| SC-004 | The image-display E2E module carries a case that is red on the code this slice starts from and green after it. | `manage.py test tests.e2e.test_image_display` |
| SC-005 | The other four placeholders and their cases are untouched. | the same module's audio, video and PDF cases re-run unchanged |

## UI/UX

Static preview at `specs/157-projector-image-missing-glyph/preview/preview.html` — two boards, each a
real `.projector__screen` at 1920×1200 scaled to 45%, one running develop's four lines and one running
this slice's. Numbers below are the probe's, on that 1920×1200 stage, with a 1600×900 picture:

| | Today | This slice |
| --- | --- | --- |
| placeholder computed `display` — loaded | `block` | `none` |
| placeholder carries `hidden` — loaded | `false` | `true` |
| placeholder box — loaded | 80×80 at x 1720–1800 | no box in the flow |
| picture box — loaded | 1600×900 at x 120–1720 | 1600×900 at x 160–1760 |
| picture centre ÷ stage middle — loaded | **920** ÷ 960 | **960** ÷ 960 |
| picture offset from the middle — loaded | **−40px** | **0px** |
| placeholder box — failed | 80×80 at x 920–1000 | 80×80 at x 920–1000 |
| what is painted — pending | the placeholder | nothing |

- **Layout / position**: both children of `.screen__image-box` stay in one flex row, centred; the
  placeholder keeps its place at the picture's right and its 80×80 box. Hidden, it leaves the flow, and
  the picture alone is what the box centres.
- **Size / spacing**: unchanged — 80×80 box, 60×65 drawing inside it (the viewBox insets it 7/48 and
  5/48), `stroke-width` 1.35; no gap is declared, so none is added.
- **Colour / typography**: unchanged — `#3b3933` on `--canvas`, `fill: none`, round caps.
- **States**: *pending* nothing · *loaded* picture only · *failed* placeholder only. Hover, focus, active
  and disabled do not apply: the placeholder is decorative and holds no pointer.
- **Motion**: none; the placeholder appears and disappears instantly, and the screen's own 220ms morph is
  untouched.
- **Responsive**: no rule here is size-dependent. At 1280×720 the same measurement gives the picture
  1109×624 at x 45–1154, centre **600** today and **640** (the middle) after the change — the same 40px.

## Assumptions

- **The mechanism is the attribute, not a class or an inline style.** `hidden` is what the stylesheet
  already keys on and what the other four placeholders already use; adding a second mechanism would
  leave two ways to say the same thing.
- **The placeholder keeps its markup position.** It stays the second child of the image box, so a
  corrected flow centres the picture exactly; no new wrapper, no `position: absolute`.
- **The failure branch keeps its shape.** A failed load still shows the glyph rather than a text line —
  that is the state the glyph exists for, and this slice only makes it reachable.
- **A move clears the failed state, like video does.** `clearVideoScreen` resets its placeholder when the
  screen is left; the image path gets the same treatment, so two screens cannot disagree about it.
- **The test change is part of the slice, not a follow-up.** The reported defect is only observable once
  a case asserts the loaded state; a fix without it would leave the same blind spot.
- **No capability file is created.** `projector` exists (`docs/spec/projector.md`, R1–R2) and this is a
  new requirement in it, R3 — folded at Converge, not before.
- **`bump: patch`.** A fix to shipped behaviour with no new capability.

## Clarifications

### Session 2026-10-29

- No open items. The mechanism was reproduced before Specify: a page carrying the real markup and the
  frozen `projector.css` at 1920×1200 measures the picture at x 520–1320 with an 80px box at 1320–1400,
  matching the reported screenshot (520–1319 and a drawing from 1330) to the pixel; `svg.hidden = true`
  leaves the attribute unset and the element displayed. The test module's blind spot was read at
  `tests/e2e/test_image_display.py:87-105`. Zero open markers remain.
