# Tasks: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md`
**Plan**: `specs/237-sidebar-mark-centering/plan.md`
**Verification split**: 8 test · 6 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written.
Every `test` row in the plan is a red task and a green task. Inspection rows produce no test task.
The CSS edit was applied before gate 1 for the live preview (recorded in the spec's
Assumptions); it stays uncommitted, and the red tasks temporarily remove only those two
selectors before restoring them.

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_sidebar_mark_centring.py` with a `StaticLiveServerTestCase`
      fixture: one service holding a text row, a passage, a media row, a fill-in with a badge,
      a two-line song entry and a section break, plus a long label that wraps at 390px.
      Use `@tag('e2e')`, `skipUnless` on Playwright and
      `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`.
      Add a 1366×900 page helper and a `MEASURE` script reading each row's number, mark, label
      and badge boxes. No assertions yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: the mark shares the number's vertical centre on every row.
**Independent test**: measure all `#chList .songrow` rows; both box centres are 0px.

- [X] T002 [P] [US1] Write failing tests for US1/AC1, FR-001 and SC-001:
      `test_mark_centre_matches_number_on_every_row` (every marked row's centre offset is
      within ±1px of 0, and equals the number's). Temporarily remove the two spec-237
      selectors from `components.css` and confirm the test is red at −4px on one-line rows,
      then restore the file.
- [X] T003 [US1] Keep the gate-1 edit in `static/styles/design/components.css`: the two
      selectors `:root[data-section="tatib"] #chList .songrow__mark` and
      `.reorder__ghost .songrow__mark` beside spec 063's number rule, with only
      `align-self: center`. Touch no other declaration.
- [X] T004 [US1] Make T002 green; record US1/AC2 by inspection — computed mark colour follows
      `--head-ink` / `--ink`, the hover and selected rules are unchanged, and no transition was
      added.

## Phase 3 — US2 (P2)

**Goal**: the row's other geometry does not move.
**Independent test**: compare mark x 42px, label x 66px, row heights and clamp before/after.

- [X] T005 [P] [US2] Write failing tests for US2/AC1, FR-002 and SC-002:
      `test_columns_heights_and_clamp_are_unchanged` (38px one-line and 53px song rows keep
      mark x 42px, label x 66px, 16px mark, three-line clamp and no horizontal overflow).
      Run red with the selectors removed.
- [X] T006 [P] [US2] Write a failing test for US2/AC2:
      `test_wrapped_song_row_keeps_centred_mark` at a 390px viewport (74px wrapped song row,
      mark centre 0px, label still clamped at three lines). Run red on the base rule.
- [X] T007 [US2] Make T005 and T006 green with the same declaration; edit no gap, padding,
      min-width or clamp rule.

## Phase 4 — US3 (P2)

**Goal**: the slot badge and drag copy follow the mark.
**Independent test**: badge bottom 9px above the row, ghost mark centred like its number.

- [X] T008 [P] [US3] Write a failing test for US3/AC1 and SC-002:
      `test_slot_badge_follows_the_mark` (11px badge at row-x 50px and 9px above the row bottom,
      still inside the mark's bottom-right corner). Run red on the base rule at 13px.
- [X] T009 [US3] Make T008 green without editing `.slot__badge`; record US3/AC2, FR-003 and
      SC-003 by inspection — `reorder.js:268` stamps the ghost from the row's markup and the
      `.reorder__ghost .songrow__mark` selector carries the same declaration as the number's.
- [X] T010 [P] [US3] Record FR-004 and SC-004 by inspection: one CSS diff, no marks in the OBS
      dock or songbook sidebar, and the probe's frozen before/after readouts in both themes at
      1440/1024/390px.

## Phase 5 — Polish

- [X] T011 Hard-reload the live page after collectstatic and re-run `preview/probe.py`; confirm
      the frozen numbers (−4 / −11.5 / −22px before, 0px after; x 42/66px; badge 13 → 9px).
- [X] T012 Run only `tests.e2e.test_sidebar_mark_centring` between pushes; leave the full browser
      suite to the push step and report what the narrower run proves.
- [X] T013 Re-check the next spec number, `ITEM-252`, `reading/R49` and the patch level against
      `develop` and every unmerged branch before delivery.
- [X] T014 At delivery only, after Converge and on your word: write the `VERSION` bump, the
      `## [Unreleased]` changelog line, the `backlog/board.md` `In review`/`Done` moves and the
      `reading.md` R49 modification.

## Phase 6 — Convergence

- Pass 1 (`converge.md`): all 14 traceability rows met by their declared method; 0 gaps.
  New E2E module 4/4 green after a red-on-base run; existing kind-marks module 12/12 green.
  Converged. T014 stays open for the delivery step and is not claimed here.
