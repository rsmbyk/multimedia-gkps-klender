# Tasks: the overlay's text wraps inside the box that owns it

**Spec**: [`spec.md`](./spec.md) · **Plan**: [`plan.md`](./plan.md) · **Branch**:
`fix/183-overlay-text-wrap` · **Version bump**: `patch` (1.26.0 → 1.26.1)

One agent, one thread; `[P]` marks order-independent tasks, not concurrent ones. The order actually
used is the order below. T014–T018 were added when the owner widened the scope at gate 2; the tasks
before them were re-run rather than trusted.

## Setup

- [X] T001 Create the slice worktree `../multimedia-gkps-klender-183` on `fix/183-overlay-text-wrap`
  from `develop` (0f17dd16), with a throwaway database `gkps183` and the fixture in `scratch/seed183.py`
- [X] T002 Add the board card `backlog/items/ITEM-187-overlay-text-wrap.md` and its row in
  `backlog/board.md` — the card exists before the work, per the board's own rule

## US1 — a run with no space in it wraps inside the box that owns it

- [X] T003 [US1] Write the failing acceptance cases in `tests/e2e/test_obs_overlay_wrap.py`: the
  120-character run at 1080p, the pasted link after the mark `L.`, and the report at 1280×720 and
  960×540. Red on the unfixed sheet — 733.85px, 747.48px and `overflow-wrap: normal` (recorded in
  `converge.md`)
- [X] T004 [US1] Add `overflow-wrap: break-word` to `.obs-overlay__line` — the narrow first pass, later
  superseded (T016)
- [X] T005 [US1] Re-run the module green: 7 tests, `OK`, 19.57s

## US2 — text that fits is unchanged

- [X] T006 [US2] Add `test_a_body_that_fits_draws_the_same_box_with_the_rule_removed` — the control
  body measured, the declaration neutralised on the live page, the control measured again
- [X] T007 [US2] Add `test_the_rule_is_inherited_from_the_stage` — `break-word` on the stage and on
  the plate, the kicker, the row, the words column and the caption

## US3 — the surface keeps every other thing it does

- [X] T008 [US3] Add `test_the_mark_keeps_its_own_column` — `nowrap` on the mark, `grid` on the row
- [X] T009 [US3] Inspect `static/web/obs-overlay.js` `modelOf` / `paint` for blank, media and break
  screens (no test: the slice changes no code on that path)

## Revision — the owner widened the scope at gate 2

- [X] T014 [US1] Add the three failing cases for the wider scope — the song caption, the passage's
  long verse title, and a 64-character entry title as the plate's kicker — and re-point the
  inheritance case at the stage. Red on the body-only sheet: 2,035.20px (caption), 230.79px (title),
  `'normal' != 'break-word'` on the stage (recorded in `converge.md` pass 2)
- [X] T015 [US1] Extend the fixture with the seventh state — a 64-character entry title — and rebuild
  it in `scratch/seed183.py` and in the test's own `setUp`
- [X] T016 [US1] Move the declaration from `.obs-overlay__line` to `.obs-overlay__stage`; delete the
  narrow scope's own pinning test (`test_the_caption_and_the_heading_are_outside_this_slice`) with it
- [X] T017 [US1] Correct the kicker case: a 64-character kicker at `.5em` cannot outgrow the plate, so
  the test asserts its ink and the plate's growth, not a second row (research D007)
- [X] T018 [US3] Add the caption's own look to its test — weight 800, `text-align: center`,
  `text-wrap: balance`, the outline present (FR-006 / SC-006)

## Polish

- [X] T011 Build the review page `specs/183-overlay-text-wrap/preview/index.html` from the live page's
  own DOM (`preview/build_preview.py`), and the measurement probe (`preview/probe.py`) — rebuilt with
  the seventh state and a `hashchange` listener so deep links work
- [X] T012 [P] Write `research.md`, `data-model.md`, `contracts/none.md`, `quickstart.md`,
  `checklists/requirements.md`
- [ ] T013 Delivery: `VERSION` 1.26.1 · `CHANGELOG.md` line · Fold into `docs/spec/overlay.md` · board
  row to In review · one commit · PR body from this slice's own report

## Dependencies

T003 → T004 → T005 (red before green). T006–T009 depend on T004. T014 → T016 (the wider cases must be
red on the narrow sheet before the declaration moves). T017 depends on T015. T011–T012 depend on a
green module; T013 waits for gate 2.
