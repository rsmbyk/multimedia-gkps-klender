# Tasks: the add bar opens over the seam, and nothing moves

**Slice**: `specs/143-add-bar` · **Plan**: [`plan.md`](./plan.md) · **Bump**: `patch`

`[P]` means order-independent, not concurrent — run in one thread. The CSS and JS below landed
before the pack, as the live preview the spec was written against; the tests are the slice's own
implementation work and came after.

## Phase 1 — Setup

- [X] T001 Record the baseline: on the commit before the change, 13 of 42 E2E tests assert the in-flow model; the twelve this slice owns are listed in `analysis.md`

## Phase 2 — US1: the entry under the pointer never moves (P1)

- [X] T002 Give `.entry__add` and `.entry__start` a 20px slot in the flow and no padding, keeping the page height exactly as it was (`components.css`)
- [X] T003 Draw the bar absolutely inside that slot — `left: 50%; top: 50%; transform: translate(-50%, -50%); width: max-content; height: 34px` — revealed by opacity only (`components.css`)
- [X] T004 Move the seam line from the bar to the row's `::before`, full column width, so the bar's hit area stays as wide as its buttons (`components.css`)
- [X] T005 Rewrite `test_opening_a_row_moves_nothing` from `test_a_revealed_row_keeps_equal_gaps_above_and_below`: sweep entries 0, 1, 3 and assert every block's document top is unchanged and the page height holds (`tests/e2e/test_tatib_entry_controls.py`)
- [X] T006 Rewrite `test_focus_moves_nothing_either` from `test_focus_keeps_the_same_gaps`, same measurement on the keyboard path
- [X] T007 Rewrite `test_hovering_the_first_entry_moves_it_once_then_settles` as `…_does_not_move_it`, and assert the start bar is open (`tests/e2e/test_tatib_hover.py`)

## Phase 3 — US2: the bar is usable where it is drawn (P1)

- [X] T008 Add `test_the_bar_does_not_cover_the_entry_controls`: `elementFromPoint` at the Edit button's top edge, middle and bottom edge
- [X] T009 Rewrite `test_tabbing_into_a_collapsed_row_expands_it` as `test_tabbing_into_a_row_opens_it`, asserting the bar's opacity and `pointer-events`
- [X] T010 Retarget the five reveal tests at the bar's opacity rather than the row's height (`test_hovering_an_item_reveals_the_add_rows_around_it`, `…focus_within…`, `…moving_onto_an_add_row…`, `…hovering_the_item_still…`, `…the_add_row_is_not_part_of_the_item`)
- [X] T011 Update the three no-hover rule inspections to look for `.entry__add-inner` / `.entry__start-inner`

## Phase 4 — US3: the seam is legible without being loud (P2)

- [X] T012 Paint the seam at `.15` of `color-mix(--focus 40%, --divider)` at rest and `.6` open; add `test_the_seam_is_a_hint_at_rest_and_brightens_when_opened`
- [X] T013 Make a hovered add button solid-bordered and opaque; add `test_a_hovered_button_is_solid_and_opaque`
- [X] T014 Set the gaps: 20px between blocks, 34px of head margin, 8px either side of the section break; rewrite `test_the_start_bar_collapses_and_reveals_with_equal_gaps` as `test_the_start_bar_opens_without_moving_the_first_entry` and `test_at_rest_the_rows_and_the_bar_reserve_nothing` as `test_the_row_keeps_its_slot_and_the_bar_floats_over_it`
- [X] T015 Mute the section break's rule and diamond to `color-mix(--divider 62%, --canvas)`; update `test_the_divider_takes_the_same_box` for the 8px margins

## Phase 5 — Polish

- [X] T016 `preview/README.md` — the states to click, and where the "before" stylesheet can be recovered
- [X] T017 Card ITEM-154, board row and `specs/README.md` index row
- [X] T018 Bump `VERSION` 1.22.3 → 1.22.4 and write the `CHANGELOG.md` line
- [X] T019 Fold `docs/spec/reading.md` — R19 added

## Acceptance

- `tests.e2e.test_tatib_entry_controls` + `tests.e2e.test_tatib_hover` — **39/40**, the one red being
  ITEM-153's touch-controls error, identical on `develop`. `tests.test_design_tokens` 6/6.
- Live check on `/tatib/142/` and `/tatib/144/`: 0.0px of movement per entry, the seam hinted at rest,
  the bar centred, the entry's controls clickable while a row is open.
