# Tasks: a text screen arrives as fast as the entries beside it

**Spec**: `specs/219-projector-fit-cost/spec.md`
**Plan**: `specs/219-projector-fit-cost/plan.md`
**Order used**: T001 → T007 in sequence, one thread. `[P]` marks order-independent work; none was run
in parallel.

## Phase 1 — Foundational

- [X] T001 Measure the defect on both builds: `preview/probe.py` written, develop's advance cost and
  layout reads recorded for the local service `Ibadah Minggu` (171 screens, 126 with words).
  `specs/219-projector-fit-cost/preview/probe.py`
- [X] T002 Measure the fitting's own fault: `preview/verify_sizes.py` written, develop's arrival size
  against its own resize size on every screen (53 of 126 disagree). `specs/219-projector-fit-cost/preview/verify_sizes.py`

## Phase 2 — US1: a text screen arrives as fast as any other

- [X] T003 Fit the arriving screen before the arrival morph's classes are added, so it is measured at
  rest. `static/web/projector.js` (`render()`)
- [X] T004 Remember a fitted screen by stage size and body, and skip the fit while the key matches.
  `static/web/projector.js` (`fit()`, `fitKey()`)
- [X] T005 Fit the screens either side of the one showing in idle time, cancelling the previous
  request, and clearing every remembered fit when the bundled faces arrive.
  `static/web/projector.js` (`fitNeighbours()`, the `document.fonts.ready` handler)
- [X] T006 Test: a paced advance costs one layout read per screen of words, and every fitted screen
  still fits and is as large as it can be. `tests/e2e/test_projector.py`
  (`test_a_text_screen_arrives_without_being_fitted`, the `COUNTER_*` helpers)

## Phase 3 — US2: the size a screen shows does not depend on how it was reached

- [X] T007 Confirm the arrival size equals develop's at-rest (resize) size on every screen.
  `specs/219-projector-fit-cost/preview/verify_sizes.py` → 0 of 126 differ

## Phase 4 — US3: a single-screen text is cut without a per-character layout

- [X] T008 Halve both loops of the single-screen cut: the rows kept, and the characters trimmed from
  the last row. `static/web/projector.js` (`truncateText()`)
- [X] T009 Confirm the cut keeps the same rows and characters on a 400-row body (116 rows, 10 711
  characters, 2 px) in 81.5 ms against 2 992 ms.

## Phase 4b — US4: holding the arrow key cuts instead of piling screens up

- [X] T013a Cut a move that arrives while a morph is still running: settle the screen leaving, paint
  the arriving screen whole, and bring the crossfade back after the 260 ms window.
  `static/web/projector.js` (`morphing`, `startMorphWindow()`), `static/styles/design/projector.css`
  (`.screen.is-quiet`)
- [X] T013b Test: a held key leaves one screen painted, and a single move still morphs.
  `tests/e2e/test_projector.py` (`test_a_held_arrow_key_cuts_instead_of_stacking_screens`,
  `test_a_single_move_still_morphs`); `test_moving_and_toggling_morph_rather_than_jump` now waits for
  the morph window before its second press, which is a held key by the old test's own timing
- [X] T013c Measure: `preview/hold_probe.py` — 7 → 1 screens painted at once, 64 → 1 overlapping frames

## Phase 5 — Polish

- [X] T010 Run the fitting tests and the whole projector browser module against the slice.
  `tests/e2e/test_projector.py`
- [X] T011 Fold the behaviour into the capability tree: `projector/R14` added.
  `docs/spec/projector.md`
- [X] T012 Card and board: `ITEM-234` at in-review. `backlog/items/ITEM-234-projector-fit-cost.md`,
  `backlog/board.md`
- [X] T014 Delivery: `VERSION` 1.36.4 → 1.36.5 and one `CHANGELOG.md` line. `VERSION`, `CHANGELOG.md`
