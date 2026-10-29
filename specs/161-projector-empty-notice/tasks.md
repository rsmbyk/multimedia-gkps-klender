# Tasks: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`
**Plan**: `specs/161-projector-empty-notice/plan.md`
**Verification split**: 13 test · 3 inspection · 1 manual

## Phase 1 — Setup

- [x] T001 `specs/161-projector-empty-notice/preview/` — re-run `build_preview.py` and `probe.py` so the
  numbers implementation is measured against are current at the base commit; no product file changes.

## Phase 2 — Foundational

- [x] T002 `tests/e2e/test_projector.py` — extend
  `ProjectorE2ETests.test_an_empty_service_shows_its_empty_state` to read the notice's visibility as
  well as its copy, and assert the page has no `hidden` on it (FR-001). Passes on the base and after.
- [x] T003 `static/web/projector.js` — add `syncEmptyNotice()` beside `screens()`: it reads
  `screens().length` and `detour` and writes the `.projector__empty` element's `hidden`; it does
  nothing when the page has no such element (FR-005). No caller yet.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a Go To passage or song owns the whole stage; the empty notice leaves and returns with the
detour.
**Independent test**: open `other`'s projector page, press `g`, choose `Mat 5` — notice gone; `Escape`
— notice back.

- [x] T004 [P] [US1] `tests/e2e/test_projector.py` — write
  `test_the_empty_notice_leaves_the_stage_for_a_goto_passage`: the notice is visible on the empty page;
  after `_open_matius_5(page)` its box is `None`, the detour is active, and the stage's height gained
  exactly the notice's former height (FR-002, SC-001, US1/AC1–AC2). **Red on the base**: the notice
  keeps its 755×38.4 box under the detour.
- [x] T005 [US1] `static/web/projector.js` — call `syncEmptyNotice()` at the end of `renderDetour()`,
  so the first painted detour hides the notice (FR-002).
- [x] T006 [US1] `tests/e2e/test_projector.py` — write
  `test_closing_the_detour_brings_the_empty_notice_back`: `Escape` closes the detour and the notice is
  visible again, without a reload (FR-003, SC-003, US1/AC3). **Red after T005**: the notice stays
  hidden because `render()` does not sync it.
- [x] T007 [US1] `static/web/projector.js` — call `syncEmptyNotice()` at the end of `render()`, so the
  leave path, the adoption path and every re-read derive the notice from the state (FR-003, FR-004).
  Then replace `adoptService()`'s own two-line hide with the helper, so there is one writer (FR-005).
- [x] T008 [US1] `static/web/projector.js` — keep stepping and the cue untouched: verify by inspection
  that `renderDetour()` still fits the detour and paints the cue, and that `test_a_verse_step_inside_a_chapter_makes_no_request`
  stays green (US1/AC4).

## Phase 4 — US2 (P2)

**Goal**: the notice follows what the stage holds when content arrives after load.
**Independent test**: add the empty service's first entry from another tab and post `update` — the
entry paints and the notice is gone.

- [x] T009 [P] [US2] `tests/e2e/test_projector.py` — write
  `test_a_reread_with_screens_hides_the_empty_notice`: a `ServiceEntry` is created in a thread, another
  page broadcasts `{type: 'update'}`, the stage gains a screen and the notice has no box (FR-004,
  SC-004, US2/AC1). **Red on the base**; green after T007, because `reflow()` ends in `render()`.
- [x] T010 [P] [US2] `tests/e2e/test_projector.py` — write
  `test_a_reread_without_screens_keeps_the_empty_notice`: the same re-read on a service still holding
  nothing leaves the notice visible (FR-004, US2/AC2). A guard on both sides of the change.

## Phase 5 — Polish

- [x] T011 `tests/e2e/test_projector.py` — run the whole `ProjectorE2ETests` class and the module's
  Go To cases; nothing else in the page changed (FR-007).
- [x] T012 the diff — inspect the whole slice: only `static/web/projector.js`, the test module and this
  pack; no route, payload, template copy, stylesheet or fitting change (FR-007).

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->
