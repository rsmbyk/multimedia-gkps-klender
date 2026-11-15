# Tasks: dock live entry snap

**Spec**: `specs/196-dock-live-entry-snap/spec.md`
**Plan**: `specs/196-dock-live-entry-snap/plan.md`
**Verification split**: 9 test · 9 inspection · 2 manual

## Phase 1 — Setup

- [X] T001 Confirm the shipped state: open `preview/index.html` and read the three cases (off-top, off-bottom, partial). No setup task exists: no dependency, no ignore-file change, no route.

## Phase 2 — Foundational

All four scenarios live in one function in `sync()` because they read the same DOM nodes; they are written and run red before the change (TDD-01).

- [X] T002 Write the off-top / off-bottom / partial + reduced-motion logic inside `sync()` at `static/web/obs-dock.js:1155`. Re-use `glideScroll` and `cancelPendingCenter` exactly as they exist; add only the target computation (clientHeight measurement, edge targets, band floor). No new timers, no new flags, no new DOM nodes.

## Phase 3 — US1 (P1) off-top

**Goal**: live entry entirely above top → snaps flush at scroller's top edge
**Independent test**: T003 green

- [X] T003 [P] [US1] `static/web/obs-dock.js:1159-1167` — when the live `.entryli`'s bottom is at or above `runBody.scrollTop` (entirely above), `glideScroll(li.offsetTop)` so the entry's row sits flush at the scroller's top edge; the block stays open beneath.
- [X] T004 [US1] Re-run the E2E suite against the unmodified templates and record the red output in `analysis.md`'s History: the live entry still centred today.

## Phase 4 — US2 (P1) off-bottom

**Goal**: live entry entirely below bottom → foot rests just above NEXT band
**Independent test**: T005 green

- [X] T005 [P] [US2] `static/web/obs-dock.js:1168-1178` — when the live `.entryli`'s top is below `runBody.scrollTop + clientHeight` (entirely below), `glideScroll(liBottom - runBody.clientHeight - protrude)`, where `protrude` is the NEXT band's `bottom: -10px` magnitude (0 when the band is hidden); the li's foot lands 10px below the scroller's bottom edge, so the band stays pinned at the edge and visible (±1 px).
- [X] T006 [US2] Re-run the E2E suite and record the red output.

## Phase 5 — US3 (P2) partly visible

**Goal**: partly visible entry keeps today's centred target
**Independent test**: T007 green

- [X] T007 [P] [US3] `static/web/obs-dock.js:1159-1182` — when any part of the live `.entryli` overlaps the scroll area (neither `liBottom <= scrollTop` nor `liTop >= scrollTop + clientHeight`), fall back to today's centring target (`glideScroll` via `scheduleCenter()`).

## Phase 6 — US4 (P2) hand wins

**Goal**: wheel / pointerdown cancels a pending snap
**Independent test**: T008 green

- [X] T008 [US4] Verify `cancelPendingCenter` is already bound to `wheel` / `pointerdown` at `obs-dock.js:633-634`; no new listeners needed. Start a snap, wheel during it — scroll stays where the gesture parked it.

## Phase 7 — Polish

- [X] T009 Regenerate the preview (`openchamber_render` above) so it draws the three states; update its UI/UX numbers if anything changed.
- [X] T010 `inspection` — diff shows zero new lines in `obs-dock.js` beyond the target computation; zero CSS change; zero template change. All existing suites stay green.
- [X] T011 `manual` — in a running dock: (a) off-top snaps flush top; (b) off-bottom foot just above band; (c) partly visible centres as before; (d) wheel cancels snap; (e) reduced motion jumps instantly.