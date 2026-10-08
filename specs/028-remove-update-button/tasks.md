# Tasks 028: Remove the "Update the current state" button

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/028-remove-update-button`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): drop the label and `data-project-update`
      assertions, assert the button is absent
- [x] Green — implementation (`multimedia/web/templates/reading/tatib.html`,
      `static/web/display.js`)
- [x] Red — E2E (`tests/e2e/test_projector.py`): no case presses Update; the automatic follow is the
      re-read under test
- [x] Green — E2E
- [x] Amend spec 026: the manual-re-read in-scope clause and its scenario
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
