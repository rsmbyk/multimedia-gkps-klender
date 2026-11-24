# Tasks — spec 241

**Spec**: `specs/241-tatib-reorder-kept/spec.md` · **Plan**: `plan.md`

## Setup

- [X] T001 Confirm the worktree and branch `fix/241-tatib-reorder-kept` from `develop` (GIT-02).
- [X] T002 Read `docs/spec/reading.md` (`R11`, `R14`, `R57`) and record the capability deltas in the spec header.

## Foundational

- [X] T003 Write the failing test for `US2/AC1` in `tests/e2e/test_reorder.py` — an edit leaves the contents in server order; read the assertion before making it pass (TDD-02).
- [X] T004 Write the failing test for `US1/AC1,AC2` — a drop after an edit is written, both lists agree, and a reload keeps it.
- [X] T005 Write the failing test for `US1/AC3` — an add-then-drag keeps every entry on the stage.

## US1 — A drop after a save is the order that is written

- [X] T006 Make `US1/AC1,AC2` pass: in `static/web/reorder.js` `endDrag()`, clear `drag` before `applyPaneOrder(order())` so a rewrite-raised `pointercancel`/`blur` cannot rewind the drop.
- [X] T007 Make `US1/AC3` pass: in `applyPaneOrder()`, read the pane at call time, build `moving` only from known pks, and move only children whose position changed instead of `replaceChildren`.
- [X] T008 Re-run the whole `tests/e2e/test_reorder.py` module; all 32 cases green.

## US2 — The song sorter leaves the Tata Ibadah contents alone

- [X] T009 Make `US2/AC1` pass: in `static/web/reading.js` `songRowEls()`, require a `.songrow` carrying `data-t`, `data-o` and `data-m`, and return from `applySongOrder()` with fewer than two song rows.
- [X] T010 Make `US2/AC1` robust: swap only song rows among their own slots, leaving non-song children in place.
- [X] T011 Re-run `tests/e2e/test_song_sort_retained.py`; all six cases stay green.

## US3 — An abandoned gesture restores the pre-drag order

- [X] T012 Confirm by inspection that `cancelDrag()` still restores `current.order` and posts nothing, and that `applyPaneOrder()`'s fresh read leaves the next gesture a current cache.

## Polish

- [X] T013 Re-run `multimedia.web.tests` after `collectstatic`; compare its single failure with unmodified develop.
- [X] T014 Re-run `tests/e2e/test_reading.py` and `tests.e2e.test_entries`; compare failures with unmodified develop.
- [X] T015 Drive the live preview at `http://127.0.0.1:8791/tatib/322/` and record the measured before/after in `preview/README.md`.
- [ ] T016 Write `analysis.md` with artifact SHAs, metrics, findings and history.
- [ ] T017 Converge: compare the present code with the traceability table and append `converge.md`.
- [ ] T018 Fold: write the `R57` modification and the `R58` block into `docs/spec/reading.md` and record `fold.md`.
- [ ] T019 Open `ITEM-256`, move the board row, and report; commit only after a green suite (GIT-06).
