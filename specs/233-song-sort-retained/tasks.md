# Tasks: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`
**Plan**: `specs/233-song-sort-retained/plan.md`
**Verification split**: 13 test · 3 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_song_sort_retained.py` with the `StaticLiveServerTestCase`
      fixture: one ordinary book, `Alpha` (modified 2020-01-01) and `Zebra` (modified 2020-01-02),
      a browser at 1440×900, and an `order()` helper reading `.songrow__t` from `#chList`. No
      behaviour is introduced here.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: a created song lands in its alphabetical slot and the sort button still says `title`.
**Independent test**: toggle to alphabetical, create `Beta`, read `Alpha, Beta, Zebra`.

- [X] T002 [P] [US1] Write a failing E2E `test_create_keeps_alphabetical_order` in
      `tests/e2e/test_song_sort_retained.py`: default `Zebra, Alpha` (`m`), toggle to `Alpha, Zebra`
      (`title`), create `Beta`, assert `Alpha, Beta, Zebra` with `data-order="title"`, and assert
      `performance.timeOrigin` plus an in-page marker are unchanged. Confirm it fails on the base
      code with `['Beta', 'Zebra', 'Alpha']`.
- [X] T003 [P] [US1] Write a failing E2E `test_create_in_default_order_leads` in the same module:
      without toggling, create `Beta`, assert the new song leads and `data-order="m"`.

## Phase 3 — US2 (P1)

**Goal**: every in-place refresh keeps the chosen order, not just create.
**Independent test**: toggle to alphabetical, perform each operation, read the rows after each.

- [X] T004 [P] [US2] Write a failing E2E `test_edit_refresh_keeps_alphabetical_order`: edit a
      song's title through its row control, assert remaining rows stay alphabetical.
- [X] T005 [P] [US2] Write a failing E2E `test_delete_refresh_keeps_alphabetical_order`: delete a
      song through its editor, assert remaining rows stay alphabetical.
- [X] T006 [P] [US2] Write a failing E2E `test_row_click_refresh_keeps_alphabetical_order`: open
      the other song row, assert the child list stays alphabetical while the stage follows.

## Phase 4 — US3 (P2)

**Goal**: the default order, other sections and hymn books are untouched.
**Independent test**: fresh load leads with `Zebra`; Alkitab/Tatib lists keep their own order.

- [X] T007 [P] [US3] Write a failing E2E `test_default_order_and_other_sections_unchanged`: fresh
      load reads `Zebra, Alpha` with `m`, then browse a section with no song rows and return,
      asserting the chapter/service lists were not reordered and the song list is unchanged.

## Phase 5 — Foundational implementation

**Goal**: one shared call makes every red test above green.

- [X] T008 Add `applySongOrder()` immediately after `reconcileChildren(chList, …)` in the shared
      page-update path of `static/web/reading.js`, with a comment recording why. Confirm all tests
      from T002–T007 turn green and the existing
      `tests/e2e/test_reading.py::test_song_sort_toggles_between_last_modified_and_alphabetical`
      stays green.

## Phase 6 — Polish

- [X] T009 Open `ITEM-247` from the board's Backlog into `Speccing` with `spec:
      233-song-sort-retained` and `branch: fix/233-song-sort-retained`; add the row to
      `backlog/board.md`.
- [X] T010 Remove the temporary `tests/e2e/test_song_sort_retain_probe.py` once its coverage lives
      in the promoted module.
- [X] T011 Re-check the next spec number, card ID, capability ID and patch version against
      `develop` and every unmerged branch before delivery.

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
