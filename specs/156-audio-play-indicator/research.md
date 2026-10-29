# Research: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`
**Unknowns remaining**: 0

## D001 — The geometry moves into `projector.css`, not `components.css` into the page

- **Decision**: the 48px box, the radius and both glyphs are written fresh in `projector.css`, beside the
  video control; `projector.html` keeps its three stylesheets.
- **Rationale**: `.screen__audio-play`'s size and mark exist today only in `components.css`, which the
  projector page does not load — and loading it would bring 2,700+ lines of reading-app panels, dialogs
  and rails onto a page whose whole design is four blocks of type and a 500px bar.
- **Alternatives considered**: linking `components.css` on the projector (rejected: repaints the page and
  re-introduces the Fomantic-era cascade the projector deliberately avoids); moving the shared audio
  player rules out of `components.css` into a shared sheet (rejected: touches every reading surface for a
  one-screen fix, and spec 154 is editing that same block in flight).
- **Provenance**: research

## D002 — The control is lifted above the pointer zones, and only the control takes pointers

- **Decision**: `.screen__audio-box` gets `position: relative; z-index: 3; pointer-events: none` and
  `.screen__audio-play` gets `pointer-events: auto`.
- **Rationale**: `.mouse-zones` sits at `z-index: 2` over `inset: 0 0 64px` (`projector.css:427`) and
  swallows every pointer event before the screen's own content. The video screen already solved exactly
  this: `.screen__video-box` is `z-index: 3; pointer-events: none` with `pointer-events: auto` on its play
  control (`projector.css:117`). Measured before the change: a pointer at the player's centre resolved to
  `div.mouse-zone--display`, never to the control.
- **Alternatives considered**: dropping the zones while an audio screen shows (rejected: they are the
  operator's navigation, and the video screen keeps them); making the whole player `pointer-events: auto`
  (rejected: the bar would stop toggling the words over a 500×118 area).
- **Provenance**: research

## D003 — The windowed fullscreen reservation skips the audio control

- **Decision**: the capture-phase click listener at `projector.js:909` returns early when the click's
  target is inside `[data-audio-play]`; every other click still enters fullscreen.
- **Rationale**: measured on the live page — with the mark painted, a pointer click produced
  `pointerdown`/`pointerup` on the control but no `click` at all, because that listener calls
  `preventDefault()` **and** `stopImmediatePropagation()`. The first click was spent entering fullscreen,
  which is invisible in a headless run and would look like a dead button to an operator.
- **Alternatives considered**: excluding the whole audio player (rejected: it would also claim the bar and
  the times, and clicking the empty area around them should still enter fullscreen); removing the
  reservation entirely (rejected: it is the projector's documented fullscreen gesture).
- **Provenance**: research

## D004 — The glyphs are the app audio player's own, at its own size

- **Decision**: copy the `::before` geometry from `components.css:2122–2123` verbatim — a 12×16 triangle
  from a 12px left border with 8px transparent shoulders at `left: 20px; top: 16px`, and a 14×18 pause
  block at `left: 17px; top: 15px` built from a two-stop gradient — on the same 48px circle.
- **Rationale**: the projector's audio player and the preview's audio player are the same control in two
  places; a redrawn mark would drift the moment either changes. At 48px the absolute offsets are correct
  as written (they were already tuned for a 48px circle).
- **Alternatives considered**: the video control's 58px and its proportionally larger mark (rejected: that
  size belongs to a control over a full-frame video); SVG icons (rejected: the app's play/pause marks are
  CSS-only everywhere, and a new asset would need the static pipeline).
- **Provenance**: research

## D005 — The idle state hides the control instead of dimming it

- **Decision**: keep `.screen__audio-box.is-idle .screen__audio-play { opacity: 0; pointer-events: none }`;
  the bar keeps `.52` and the times `.4`, and the 48px of height stays reserved.
- **Rationale**: the owner's answer at gate 1 — the bar and the times dim, the control shows and hides.
  Reserving the height keeps the bar at y 603.05 in both states, so nothing jumps when the control returns.
- **Alternatives considered**: dimming the control to match the bar (rejected by the owner); keeping it at
  full strength (also rejected — the earlier draft's assumption).
- **Provenance**: `owner decision` (gate 1, 2026-10-29); research could not have chosen between them.

## D006 — Verification rides the existing E2E harness

- **Decision**: two Playwright cases in `tests/e2e/test_audio_display.py`, using that module's own fake
  companion (`page.route('http://127.0.0.1:63174/v1/files/<sha>')`) and its generated WAV.
- **Rationale**: the module already builds a service with a real audio entry and asserts the projector's
  audio states; the new behaviour is measured in the same window, with no new fixture.
- **Alternatives considered**: a new module (rejected: duplicates the fixture); a unit test on the CSS
  (impossible — the behaviour is layout and pointer routing).
- **Provenance**: research

## Open

<!-- empty: Phase 0 finished -->
