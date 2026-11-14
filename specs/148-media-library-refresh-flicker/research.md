# Research: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`
**Unknowns remaining**: 0

## D001 — The list is drawn once per refresh, after the references are known

- **Decision**: `refresh()` assembles the next state (files, references, protected set, status) and
  calls `render()` **once**, at the end of every path — success, references failure, transport
  failure. No pass is drawn with `uses = null` while references are merely unknown.
- **Rationale**: the jolt *is* that first pass. Measured on the running page (1920×1100, layout
  sampled every animation frame): the intermediate pass draws 8 rows at 97px instead of
  119/101/123/101/101/101/101/97px, so `#mediaFileList` is 956px instead of 1024px; row 2's top moves
  377 → 355 (−22px), row 3 → 452 (−26), row 4 → 601 (−52), row 5 → 698 (−56). The two passes are
  16–85 ms apart on a click and 16–31 ms apart on the page's first load (four loads measured:
  first paint at 40/48/54/96 ms, references drawn 16/17/17/31 ms later). One draw removes the pass
  that carries every one of those numbers.
- **Alternatives considered**:
  - *Keep the last known `uses` and still draw twice* — leaves the first load without a previous value,
    so the largest jolt (the page opening) survives; it also keeps a pass whose only purpose is to be
    replaced.
  - *`min-height` on the `used by` block* — hides the geometry but still flashes `Service uses
    unavailable` over a file whose references are known (FR-001), and raises every row's settled height
    by the difference, which the spec's UI/UX forbids.
  - *Draw skeleton rows of the settled height until data arrives* — new markup, and it puts an empty
    list on screen first, which US2's third scenario forbids.
  - *Differencing `render()`* — a redesign of the renderer for a defect the call sequence causes; the
    2s poll's rebuild was measured inert and FR-004 keeps it.
- **Provenance**: research (running page, frame sampler in `preview/frame_sampler.py`; code read of
  `static/web/media-library.js:146-159`).

## D002 — State is assigned at the same moment it is drawn

- **Decision**: `refresh()` builds `nextFiles`, `nextUses`, `nextProtected` and applies them — with
  `setStatus()` — in the same step that calls the single `render()`, instead of assigning `files` at
  the top of the promise chain as it does today (`:148`).
- **Rationale**: the 2s status poll (`static/web/media-handoff.js:155` → `media:status` at
  `media-library.js:161`) can call `render()` at any point in the refresh's lifetime. If `files` were
  already the new list while `uses` was still the previous map, a poll landing in that window would
  draw new rows against old references — a one-frame inconsistency of the same family as the defect.
  Assigning late means every poll during a refresh redraws the *last complete* state, which is exactly
  what is on screen.
- **Alternatives considered**: a `refreshing` flag read by the poll's `render()` — a second piece of
  state to keep true; the ordering above removes the window without any flag.
- **Provenance**: research (code read; the poll's 2s cadence measured by counting `render()` calls).

## D003 — The references failure keeps its placeholder, and keeps its one draw

- **Decision**: when the references request fails, draw once with `uses = null` — the current
  `Service uses unavailable` copy — and do not retry inside `refresh()`.
- **Rationale**: the placeholder is the honest degraded state and the spec keeps it (FR-003, US2 AC2).
  What it loses is the second draw it used to cause. The page's own retry path is the 2s poll, which
  re-renders from the last complete state and never re-runs `refresh()`; a retry loop here would give
  the references endpoint a second caller for no stated requirement.
- **Alternatives considered**: retry once after a delay; leave the list empty. Both are scope the
  request did not ask for.
- **Provenance**: research (spec FR-003 / US2 AC2).

## D004 — The seam is E2E, sampling frames

- **Decision**: five Playwright cases in `tests/e2e/test_media_library.py::MediaLibraryE2ETests`, using
  the module's existing companion stubs: a `MutationObserver` on `#mediaFileList` counts child
  replacements, and a `requestAnimationFrame` sampler records every row's `top` and the placeholder
  count from the triggering click to the settled list. The references response is held for 200 ms with
  `page.route('**/media-library/references/', …)` where a test needs the window open.
- **Rationale**: the defect is a transient — a settled-DOM assertion passes straight through it (the
  sampler found it only because it samples every frame). At 60fps the intermediate pass is 1–2 frames,
  so the hold makes the failing window deterministic instead of lucky. `page.route` on the
  companion's origin is already this module's idiom (`test_media_library.py:64-128`); the same-origin
  references route is the one addition.
- **Alternatives considered**: a unit test of `render()` — `refresh()` is a closure inside an IIFE and
  the behaviour is a sequence across two fetches, so a unit test would have to re-implement the
  sequence it is testing. A count-only test (no sampling) would miss FR-002 for a fix that still moved
  rows inside one draw.
- **Provenance**: research (existing test module read; sampler behaviour measured on the live page).

## Open

<!-- empty: Phase 0 finished, zero unknowns -->
