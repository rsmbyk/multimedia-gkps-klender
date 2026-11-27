# Research: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`
**Unknowns remaining**: 0

## D001 — The fit has no fullscreen trigger

- **Decision**: add a fit on the next animation frame after `fullscreenchange` and after a change
  on `matchMedia('(display-mode: fullscreen)')`. The existing `resize` path stays.
- **Rationale**: `static/web/projector.js:477` and `:2119` make `resize` the only geometry signal
  that calls `render(true)`; `:1954–1956` listen to `fullscreenchange` only for the cursor,
  video and audio states. `fit()` at `:627` caches by a key built from the stage box and the body,
  so a stage change with no signal leaves the old inline size in place. The red probe measured a
  stage growing `1376×804 → 1376×1004` with the lines still at `87px` and the key still
  `1376x804|…` on unmodified code.
- **Alternatives considered**: a `ResizeObserver` on the stage — rejected because it adds a
  second, asynchronous geometry source beside the existing window listener and would fire during
  the arrival morph; a timed poll — rejected because it guesses at the transition.
- **Provenance**: research — `static/web/projector.js:477,627,1954,2119`; `preview/probe.py`.

## D002 — Refit the screen that is actually on the stage

- **Decision**: choose `detourNode` while `detour` is set, otherwise `screens()[current]`; call
  `fit(node, true)` and then `fitNeighbours()`.
- **Rationale**: `render()` always fits the service screen, but the Go To detour replaces it on
  the stage (`:1754–1768`) and clears the service screens' keys while it is up. A fullscreen
  transition during a detour must not refit a hidden screen. `force` is needed because a stage
  that returns to its original size can otherwise match a remembered key that was never updated
  for the detour.
- **Alternatives considered**: call `render(true)` — rejected because it repaints the cue and
  media state on every fullscreen signal, including the audio/video takeover, which owns its own
  fullscreen element.
- **Provenance**: research — `static/web/projector.js:797,1533,1768`; the accepted spec's
  US1/AC3 and US2/AC3.

## D003 — F11 needs a signal other than `fullscreenchange`

- **Decision**: listen for `change` on `(display-mode: fullscreen)` with `addEventListener` and an
  `addListener` fallback.
- **Rationale**: F11 takes the window fullscreen without setting `document.fullscreenElement`, so
  `fullscreenchange` never fires. The display-mode media feature follows both the browser's own
  control and the Fullscreen API on Chromium and Firefox. The owner named F11 alongside the F key
  and mouse zone as paths that leave the words unchanged.
- **Alternatives considered**: a `keydown` listener on `F11` — rejected because the browser eats
  the key and no key event proves the transition actually happened; checking `innerHeight ===
  screen.height` on a timer — rejected for the same polling reason as D001. Safari is not
  verified; where display-mode does not change, the existing `resize` path remains.
- **Provenance**: research — owner's Clarify answer; W3C Media Queries Level 5 `display-mode`,
  MDN `@media/display-mode`; `static/web/projector.js:1910` (the page's own gesture).

## D004 — The re-fit runs on the next frame

- **Decision**: wrap the fit in `window.requestAnimationFrame`, so the geometry read happens after
  the browser has laid out the fullscreen state.
- **Rationale**: a fullscreen signal can be queued before the new viewport is reflected in
  `stage.clientHeight`; reading it in the handler itself risks fitting against the old box. A
  later `resize` for the same transition reads the same settled box and becomes a no-op against
  the updated key.
- **Alternatives considered**: fit synchronously in the handler — rejected because the red probe
  showed the stale key survives exactly this kind of missed layout moment; a `setTimeout` —
  rejected because a frame is the browser's own "after layout" boundary.
- **Provenance**: research — `preview/probe.py` (200 ms settle in both directions); the accepted
  spec's US2/AC1.

## D005 — The fitter and the algorithm do not change

- **Decision**: no edits to `fit()`'s size walk, `setSize()`, CSS, templates, backend or endpoints.
  The only production edit is the new signal handlers in `static/web/projector.js`.
- **Rationale**: the red probe's slice run returns `87 → 93 → 87px` and heading
  `53.769 → 57.4772 → 53.769px`; the heading is still `size ÷ golden ratio`, so the existing size
  contract is preserved. The CDP resize path still gives `109px` at 1920×1080.
- **Alternatives considered**: scaling the font by viewport ratio — rejected because it would
  disagree with the fitter's "largest size that fits" rule and the frozen resize answer.
- **Provenance**: research — `spec.md` §UI/UX numbers; `preview/probe.py`; `git diff` scope.

## D006 — Tests live with the projector E2E suite

- **Decision**: add cases to `tests/e2e/test_projector.py`, reusing its 1440×900 projector fixture.
  The fullscreen signals are driven through public browser events after a stage-box change; the
  assertion reads computed font sizes, never the fitter's internal key. Targeted cases run during
  Implement; the full browser suite waits for the push step.
- **Rationale**: that module already owns the projector's fit and fullscreen acceptance cases, so
  a new module would duplicate the fixture. The headless harness cannot reproduce an OS-level
  fullscreen, but it can reproduce the missing signal, which is the defect under test.
- **Alternatives considered**: a unit test of the event handler — rejected because the seam is
  the rendered size, not the handler; a new E2E module — rejected for fixture duplication.
- **Provenance**: research — `tests/e2e/test_projector.py:311,1216,1560`; `tdd` seam rule.
