# Tasks: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)
**Plan**: `specs/152-transfer-scrollbar-edge/plan.md`
**Verification split**: 12 test · 12 inspection · 0 manual

`[P]` means order-independent, not concurrent — run in one thread.

## Phase 1 — Setup

- [X] T001 Record the baseline on `develop` @ `24a6d6d2`: the list's box `453 → 987` with its bottom at `683.8`, the bar's lane `982 → 986`, 22px of canvas to the right border and 23px to the bottom one, rows `453 → 982` — measured by `preview/probe.py` against the unmodified stylesheet, at 1440×760 and 420×820

## Phase 2 — Foundational

- [X] T002 Confirm the list already carries its class and its `overflow-y: auto` (`multimedia/web/templates/reading/base.html:456`, `.media-transfers__list` in `components.css`), so the slice needs no markup change — record the check in `data-model.md`

## Phase 3 — US1: the scrollbar is the dialog's edges (P1) 🎯 MVP

**Goal**: the bar's right edge is the dialog's border, and its lane runs to the bottom border.
**Independent test**: `test_the_transfer_list_reaches_the_dialog_edges` alone, on the fake companion's fifteen jobs.

- [X] T003 [P] [US1] Write `test_the_transfer_list_reaches_the_dialog_edges` in `tests/e2e/test_media_library.py` — red: the dialog's border box is 23px wider and 23px taller than the list's box, not 1px; it also asserts the dialog reports `overflow: clip`
- [X] T004 [US1] Make T003 pass: add `margin: 0 -22px -22px; padding: 0 22px 22px` to `.media-transfers__list` and `overflow: clip` to `.media-transfers__dialog` in `static/styles/design/components.css`
- [X] T005 [US1] Re-measure the painted result with `preview/probe.py` (headed Chromium): the canvas between the bar's right edge and the border goes 22px → 0px, the lane's bottom 23px → 1px, and the bottom-right corner holds the bar inside the radius — the numbers a headless test cannot see (D007)

## Phase 4 — US2: nothing but the bar moves (P2)

**Goal**: the rows, the title, the age headings, the list's top and the scroll's end stay where they are.
**Independent test**: `test_the_transfer_content_keeps_its_insets` on the same fifteen jobs.

- [X] T006 [P] [US2] Write `test_the_transfer_content_keeps_its_insets` — red only if the padding does not restore the content box; it pins `row.left − dialog.left == 23` and `dialog.right − row.right == 23 + the bar's width`
- [X] T007 [P] [US2] Write `test_a_short_transfer_list_has_no_reserved_gutter` — red only if a lane is reserved on a two-row list; it pins `offsetWidth − clientWidth == 0` and the row's 23px right inset
- [X] T008 [P] [US2] Write `test_the_dialog_frame_and_scroll_end_do_not_move` — red only if the rules leak onto the dialog or the list's top; it pins the title's and the heading's 23px inset, `list.top − title.bottom == 14`, and the last row 22px above the dialog's border at `scrollTop = scrollHeight`
- [X] T009 [US2] Re-run the three tests and the module's existing transfer tests; confirm the two rules are the whole of the change (`git diff --stat` touches one stylesheet outside the pack)
- [X] T010 [US2] Re-measure the short state, the dark theme and the narrow viewport with `preview/probe.py`; every distance except the bar's must equal the baseline from T001

## Phase 5 — Polish

- [X] T011 Run the targeted suites green: `tests.e2e.test_media_library` (whole module) and `tests.test_design_tokens`
- [X] T012 Card ITEM-165, its board row (`Ready` → `In progress`) and the `specs/README.md` index row — re-check `spec:`, `branch:` and `issue:` against what exists
- [X] T013 Bump `VERSION` 1.22.10 → 1.22.11 and write the `CHANGELOG.md` line under `## [Unreleased]`
- [X] T014 Fold `docs/spec/media-library.md` — `R1` is modified, not added

## Phase 6 — Convergence

Converged in one pass: one `contradicts` finding (spec 149's long-list test measured against the
dialog's padding edge, which FR-001 replaced) — restated, not weakened — and one accepted LOW gap (the
corner cuts the thumb's last ~2px). See `converge.md`.

## Acceptance

- `manage.py test tests.e2e.test_media_library tests.test_design_tokens` — **48 tests, 1 failure**:
  `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` (`19.9998779296875 != 12`), ITEM-156,
  red on unmodified `develop` as well. Run twice (196s and 235s) with the same result.
- The four new tests: green, T003 red before the rule (`right = 22`, `overflow = visible`).
- `preview/probe.py`, headed Chromium, four states: `canvas bar → right border` **22 → 0**,
  `list bottom inside dialog border box` **23 → 1**, `thumb bottom → dialog bottom edge` **24.4 → ~2.4**,
  content distances equal between the columns.
- The worktree's dev server (`8832`): shipped dialog at 1440×760 light and dark, 420×820 and two rows —
  right 1, bottom 1, rows 23 / 28 (23 in the short state).
