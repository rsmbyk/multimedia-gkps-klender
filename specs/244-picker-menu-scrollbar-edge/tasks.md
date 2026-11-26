# Tasks: picker popout scrollbar edge

**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`
**Plan**: `specs/244-picker-menu-scrollbar-edge/plan.md`
**Verification split**: 14 test · 5 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written.
Every new `test` row has a red and a green task. Inspection rows produce no test task. The CSS fix
was made in the worktree before gate 1 so the live preview could show the real code path; the tasks
below prove it and keep it uncommitted until Fold.

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_picker_menu_scrollbar_edge.py` with a `StaticLiveServerTestCase`
      fixture: one dated Tata Ibadah with one text entry, `@tag('e2e')`, a `skipUnless` on
      Playwright and `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`.
      Add a page helper that walks `/` → Tata Ibadah tile → first service → hover start bar →
      `+ Passage` at 1440×900, dpr 1, and a `MEASURE` script returning each open menu's border box,
      its scrollport's box, `clientHeight`/`scrollHeight`, `offsetWidth - clientWidth`, computed
      `overflow`, and the first option and filter boxes. No assertions yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: the picker menu's scrollbar is the menu's right and bottom edge.
**Independent test**: open the Book search menu and read a 1px gap (the border) between scrollport
and menu on both sides.

- [X] T002 [P] [US1] Write failing E2E tests for FR-001, SC-001 and US1/AC1:
      `test_scrollport_reaches_menu_edges` — Book menu right/bottom 938/892 against scrollport
      937/891, with `menu.right - options.right == 1` and `menu.bottom - options.bottom == 1`.
      Confirm it is red on the unmodified base at 929/883 (9px inset).
- [X] T003 [US1] Bring the already-applied rule in `static/styles/design/components.css` into the
      implemented state: `.editor__picker-options` keeps `margin: 0 -8px -8px; padding: 0 8px 8px`,
      and `.editor__picker-menu` keeps `overflow: clip`; touch no other declaration.
- [X] T004 [US1] Make T002 green and record the measured before/after values in the test docstring.
- [X] T005 [P] [US1] Write failing E2E tests for US1/AC2:
      `test_scrollport_reaches_menu_edges_for_all_pickers` — Chapter (436px, right 938) and From
      verse (213px, right 715) menus, both ending 1px inside their menu's right and bottom edges;
      assert the filter remains inside the menu's 8px padding. Run them red on the base.
- [X] T006 [US1] Make T005 green with the same two declarations; no per-picker CSS and no change to
      `placeMenu()` in `static/web/entries.js`.

## Phase 3 — US2 (P2)

**Goal**: only the bar's lane moves; the picker's content and interactions stay where they were.
**Independent test**: first option and chapter filter boxes match the frozen numbers; one-option
menu reserves no lane.

- [X] T007 [P] [US2] Write failing E2E tests for FR-003, SC-002 and US2/AC1–AC2:
      `test_option_and_filter_boxes_are_unchanged` — first book option
      `511,464.1 → 929,503.1`, chapter filter `511,510.1 → 929,548.1`; compare against the frozen
      base numbers in the spec's `## UI/UX`. Run it red only if the boxes move.
- [X] T008 [US2] Make T007 green; the compensating padding, not a JS layout change, is what holds
      the boxes still.
- [X] T009 [P] [US2] Write failing E2E tests for FR-006, SC-003 and US2/AC3:
      `test_one_option_menu_has_no_scrollbar_lane` — pick Obaja, open Chapter, assert
      `scrollHeight == clientHeight` and `offsetWidth - clientWidth == 0`, with one visible option.
      Run it red on the base if a lane is reserved there.
- [X] T010 [US2] Make T009 green; confirm the short menu's bottom edge still ends 1px inside the
      menu.
- [X] T011 [US2] [P] Re-run the accepted spec 238 modules (`tests.e2e.test_passage_search_pickers`,
      `tests.e2e.test_song_entry_pickers`) as the regression confirmation for FR-005, SC-004 and
      US2/AC4. Defer the full browser suite to the push step.

## Phase 4 — Polish

- [X] T012 Record the five inspection rows in `analysis.md` and `converge.md`: FR-002 (computed
      5px pseudo-element rules unchanged; lane at the scrollport's outer columns), FR-004
      (computed `overflow: clip`, 10px radius, no new scroll container), FR-007 (`--scroll-thumb`
      and transparent track unchanged), US1/AC3 (scrolled bar tip follows the corner in the live
      preview), US1/AC4 (dark theme, flipped placement and 213px menu keep the same box rule).
- [X] T013 Create `ITEM-259` in `Speccing` with
      `spec: 244-picker-menu-scrollbar-edge` and `branch: fix/244-picker-menu-scrollbar-edge`, and
      add its row to `backlog/board.md`. Do not promote it to `Ready`; that is the owner's gate act.
- [X] T014 Run only the focused E2E module between pushes; report the red-first evidence and the
      focused green result with a throwaway database name so a parallel session is never locked.
- [X] T015 Re-check spec 244, ITEM-259, `reading/R59`, the next patch number and the live preview
      listener (port + process cwd) against `origin/develop` and every unmerged worktree before
      delivery.
- [ ] T016 At delivery only, after Converge: write `VERSION` `1.37.2`, the `## [Unreleased]`
      changelog line, the board's `In review`/`Done` moves and the `reading/R59` modification at
      Fold.

## Phase 5 — Convergence

<!-- written by Converge only; absent until it runs -->
