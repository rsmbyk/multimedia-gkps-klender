# Research: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`
**Unknowns remaining**: 0

## D001 — The resize path never fitted the detour

- **Decision**: call the existing stage-screen fit from the window `resize` listener, after
  `render(true)`.
- **Rationale**: `static/web/projector.js:712` fits only `active && !detour`, and
  `fitNeighbours()` at `:653` returns early while `detour` is set. The detour is fitted once in
  `showDetour()` (`:1768`), so a later geometry change never touches it. The red probe measured the
  detour at `87px` with its key still `1376x804|…` while the stage grew to 1856×984.
- **Alternatives considered**: change `render()` to fit the detour — rejected because render
  drives arrival, navigation, translation and display-state writes; a resize hook keeps those
  paths untouched. Remove the detour guard from `fitNeighbours()` — rejected because it would fit
  the hidden service screens, which R14 says to leave unfitted while the detour is up.
- **Provenance**: research — `static/web/projector.js:653,712,1768`; `preview/probe.py`.

## D002 — Reuse spec 247's stage-screen fit

- **Decision**: call `syncFullscreenFit()` from `resize`, the same next-frame helper already
  registered for `fullscreenchange` and the display-mode query.
- **Rationale**: that helper chooses `detourNode` while `detour` is set, otherwise
  `screens()[current]`, fits it, and re-fits neighbours in idle time. One name for "fit whatever
  is on the stage" keeps the three geometry signals on the same answer. Its `force` argument is
  harmless on resize: a screen whose key already matches is not repainted with a different size.
- **Alternatives considered**: a separate detour-only fit function — rejected because two copies
  of the stage-screen choice would disagree as soon as one path changes.
- **Provenance**: research — `static/web/projector.js:1962–1978`, spec 247 fold.

## D003 — Both signal orderings are covered

- **Decision**: test `resize` alone and `fullscreenchange` followed by `resize`.
- **Rationale**: with F11 the browser changes the viewport and emits no `fullscreenElement`; with
  the page's own gesture some browsers deliver `fullscreenchange` before the new viewport is
  reflected in layout, so the first fit reads the old stage and only the later resize can give the
  final answer. The probe reproduced both as stale on the merged build.
- **Alternatives considered**: assume `fullscreenchange` always comes last — rejected by the
  owner's retest and by spec 247's own note about reading the settled stage.
- **Provenance**: research — `preview/probe.py`; owner's report.

## D004 — No other path is widened

- **Decision**: leave `document.fonts.ready`, media fit, cue, controls and endpoints alone; record
  the fonts-ready detour gap in the spec as a known, unaddressed case.
- **Rationale**: the reported trigger is geometry, not font loading. A second change would double
  the verification surface for a state the owner did not report.
- **Alternatives considered**: also fit the detour in the fonts-ready handler — rejected as scope
  creep; it remains visible as an accepted gap.
- **Provenance**: research — `static/web/projector.js:2147–2155`.

## D005 — E2E cases use the existing projector module

- **Decision**: add three cases to `tests/e2e/test_projector.py`: detour fit on resize, detour fit
  when the fullscreen signal comes first, and a no-detour guard. Drive the viewport with CDP and
  read computed sizes; assert no internals.
- **Rationale**: the module already owns the projector's fit and Go To cases and its `_open_matius_5`
  helper opens the detour deterministically. Targeted cases run now; the full suite waits for the
  push step.
- **Alternatives considered**: a new module — rejected for fixture duplication; a unit test of
  the listener — rejected because the seam is the rendered size.
- **Provenance**: research — `tests/e2e/test_projector.py:2126`, `tdd` seam rule.
