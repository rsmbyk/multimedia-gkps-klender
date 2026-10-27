# Tasks: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center` · **Branch**: `feat/139-home-search-center`
**Order used**: T001 → T002 → T003–T006 (red) → T007–T008 → T009–T011 (green) → T012–T014.
`[P]` marks order-independent work, not concurrency: one agent, one thread.

## Phase 1 — Setup

- [X] T001 Run the branch's neighbouring suites as a baseline and record them — `tests.e2e.test_reading`,
  `tests.e2e.test_drawer_shell` — so a later red is known to be this slice's (`specs/139-home-search-center/`,
  the run's output quoted in `converge.md`).

## Phase 2 — Foundational (the measuring helper every story consumes)

- [X] T002 Write `tests/e2e/test_home_search_center.py`: class `HomeSearchCenterE2ETests` on
  `StaticLiveServerTestCase`, `override_settings(STATICFILES_STORAGE=…)` and the `@tag('e2e')` /
  Playwright-skip pair the neighbouring modules carry; one song fixture for the reading-view check; a
  `CENTRE` script returning the field's, the logo's, the section's and the stage's rects plus the
  document's `scrollHeight`/`scrollWidth`; an `at(width, height)` helper; and `WIDTHS`, the eleven
  (width, height) pairs the spec names.

## Phase 3 — US1: the field is the page's middle line

- [X] T003 [P] [US1] Write the failing E2E `test_the_field_is_on_the_window_middle`: at each of the
  eleven widths, `abs(field.cy - innerHeight / 2) <= 1` (FR-001, SC-001, US1.1, US1.3, US1.4).
- [X] T004 [P] [US1] Write the failing E2E `test_the_logo_stays_whole_above_the_field`: `logo.top >= 0`
  and `field.top - logo.bottom == 26` at each width, measured from rects (FR-002, SC-003, US1.2, edge
  320×568).
- [X] T005 [P] [US1] Write the failing E2E `test_the_landing_page_is_one_window_tall`:
  `scrollHeight === innerHeight` and `scrollWidth === clientWidth` at each width (FR-003, SC-002).
- [X] T006 [P] [US1] Write the failing E2E `test_the_field_does_not_travel`: `scrollY === 0` on load, no
  `transition` on the section's `height`, and the field's centre identical 400ms after paint (FR-006).
- [X] T007 [US1] Change `static/styles/design/components.css`: `.stage` declares `--stage-pad-top` /
  `--stage-pad-bottom` and expresses its `padding` with them; `.search-home` fills that box as a grid;
  `.search-home__inner` becomes three rows with the form in the middle and the landing-only margin;
  `.search-home__logo` and `.search-home__form` are pinned to rows 1 and 2 (plan.md §Design (a) and (b)).
- [X] T008 [US1] Change the phone block (`@media (max-width: 720px)`, `:root .stage`) to set
  `--stage-pad-top: calc(var(--topbar-h) + 18px)` and pad from it, so the section measures the toolbar's
  padding (FR-004).
- [X] T009 [P] [US1] Write the E2E `test_the_phone_layout_centres_too`: at 720, 600, 390 and 320 the
  section's box equals the stage's content box (`--stage-pad-top` measured from the stage), and the field
  is on the middle (FR-004, US1.2).

## Phase 4 — US2: the views that are not the landing keep their geometry

- [X] T010 [P] [US2] Write the E2E `test_the_results_bar_keeps_its_place`: submit a query, then assert
  the field's top edge is 46 at 1440×900 and 82 at 390×844, the bar is 88px tall, the results section
  starts at 128 / 164, and none of them moves when the window is resized afterwards (FR-005, SC-004,
  US2.1, edge "never recentres").
- [X] T011 [P] [US2] Write the E2E `test_the_reading_page_is_unchanged`: open a song page, assert the
  search section is not painted and `.read` occupies the stage's content box — same left, top and width
  (FR-005, SC-004, US2.2).

## Phase 5 — Polish

- [X] T012 Add the `CHANGELOG.md` line under `[Unreleased]` → `### Changed`, as the plan's `bump` states.
- [X] T013 Rebuild the static preview from the branch's own server and re-run `preview/probe_preview.py`
  so the recorded numbers come from the shipped stylesheet, not from `after.css`.
- [X] T014 Record the card's state after Implement: `status: in-progress` and the `Ready` row on
  `backlog/board.md`, with `branch:` set and `pr:` left empty — C-SDD-BOARD and C-BOARD-GIT put the
  move to `In review` at delivery, once a push has opened the PR. (The task first read "move to In
  review"; corrected in `converge.md` pass 1, F4.)
