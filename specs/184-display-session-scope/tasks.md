# Tasks: the active Tata Ibadah lasts only the browser session

**Spec**: `specs/184-display-session-scope/spec.md` · **Plan**: [`plan.md`](./plan.md)

Order used: Setup → Foundational (the marker and the US2 guards) → US1 → Polish. TDD: every row the
plan declares `test` runs red first, except the two US2 guards, which characterise behaviour that
must not change and are recorded green on the untouched code (noted at T003).

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_display_session.py` with the suite's scaffold: `@tag('e2e')`,
  `StaticLiveServerTestCase`, the static-storage override, one Tata Ibadah with a liturgy text (a
  plate on the overlay) and a second entry to step to, and the browser's start/stop in
  `setUp`/`tearDown` — `tests/e2e/test_display_session.py`
- [X] T002 [P] Add the suite's three helpers: `seed_state(context, state)` (an `add_init_script` that
  writes `localStorage['gkps-display']` before any page script), `watch_first_paint(context)` (a
  document-start `MutationObserver` counting overlay children ever attached), and `project(context)`
  (open the dock, click an entry, wait for the state to go on air) —
  `tests/e2e/test_display_session.py`

## Phase 2 — Foundational: the marker, and the behaviour that must not move

- [X] T003 [US2] Write the two characterisation guards and run them **green on the untouched code**,
  recording the baseline: `test_a_reload_inside_the_session_keeps_the_display` and
  `test_every_surface_closed_and_reopened_keeps_the_display` — `tests/e2e/test_display_session.py`
- [X] T004 Write the failing tests for the marker's write path:
  `test_the_state_carries_the_session_of_its_writer` and
  `test_the_marker_carries_no_display_data` — `tests/e2e/test_display_session.py`
- [X] T005 Make T004 pass: add `static/web/display-session.js` (`current`, `stamp`, `owns`), load it
  before the surface script in `templates/reading/base.html`, `obs_dock.html`, `projector.html` and
  `obs_overlay.html`, and stamp the session in `display.js::write` and `projector.js::write` —
  `static/web/display-session.js`, `static/web/display.js`, `static/web/projector.js`,
  `multimedia/web/templates/reading/{base,obs_dock,projector,obs_overlay}.html`
- [X] T006 Write the failing test for two surfaces minting together, then make it pass by having
  `stamp()` re-read the cookie after writing and return the value the jar holds —
  `tests/e2e/test_display_session.py`, `static/web/display-session.js`

## Phase 3 — US1: a browser that starts again starts idle

- [X] T007 Write the failing reader tests: `test_a_state_with_a_foreign_stamp_reads_as_no_state` and
  `test_a_state_written_before_this_slice_reads_as_no_state` — `tests/e2e/test_display_session.py`
- [X] T008 Make T007 pass: `display.js::read` and `projector.js::read` return the empty state unless
  `GKPSDisplaySession.owns(stored)` — `static/web/display.js`, `static/web/projector.js`
- [X] T009 Write the failing overlay tests: `test_a_state_from_an_earlier_session_paints_nothing`
  (overlay stage 0 children, dock 0 pills, projector not showing) and
  `test_first_paint_never_shows_a_prior_session_state` (0 plates ever attached the state was
  legitimate) — `tests/e2e/test_display_session.py`
- [X] T010 Make T009 pass: `obs-overlay.js::readState` validates before it returns anything, so the
  first `sync()` paints the empty stage — `static/web/obs-overlay.js`
- [X] T011 Write the failing restart test: `test_a_browser_restart_ends_the_session`, which projects
  in a `launch_persistent_context` on a temporary profile, closes the browser, launches again on the
  same profile and asserts every surface is idle while `localStorage` still holds the state —
  `tests/e2e/test_display_session.py`
- [X] T012 Make T011 pass (it should follow from T008/T010; if it exposes a gap — a surface reading
  before the marker exists, a restored cookie — fix the gap, not the test) —
  `static/web/display-session.js`
- [X] T013 Write the failing no-cookie test: `test_a_surface_without_cookie_storage_still_paints`,
  which blanks `document.cookie` before any page script, projects, and reloads: the first page paints,
  the reload starts idle — `tests/e2e/test_display_session.py`
- [X] T014 Make T013 pass: the in-page id fallback in `display-session.js` (a page that cannot read
  its marker back keeps the id in memory) — `static/web/display-session.js`

## Phase 4 — Polish

- [X] T015 Run the existing browser suites against the change and fix any regression they expose:
  `tests.e2e.test_obs_dock`, `tests.e2e.test_obs_overlay`, `tests.e2e.test_projector`,
  `tests.e2e.test_reading` — `tests/e2e/`
- [X] T016 Delete the throwaway probe `tests/e2e/test_display_session_probe.py` (its numbers are in
  the spec; its restart shape is now T011) — `tests/e2e/test_display_session_probe.py`
- [X] T017 Fold the behaviour into a new capability file `docs/spec/display-state.md` (R1, with its
  scenarios) and record the delta in `fold.md` — `docs/spec/display-state.md`,
  `specs/184-display-session-scope/fold.md`
- [ ] T018 Delivery, on the owner's word: append the `## [Unreleased]` changelog line, move `VERSION`
  1.26.1 → 1.26.2, set the card's `bump: patch`, move the board row, and commit `fix(display): the
  active Tata Ibadah ends with the browser session (184)` — `CHANGELOG.md`, `VERSION`,
  `backlog/items/ITEM-188-display-session-scope.md`, `backlog/board.md`
