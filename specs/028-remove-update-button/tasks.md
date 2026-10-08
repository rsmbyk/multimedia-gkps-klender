# Tasks 028: Remove the "Update the current state" button

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/028-remove-update-button`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): drop the label and `data-project-update`
      assertions, assert the button is absent
- [ ] Green — implementation (`multimedia/web/templates/reading/tatib.html`,
      `static/web/display.js`)
- [ ] Red — E2E (`tests/e2e/test_projector.py`): no case presses Update; the automatic follow is the
      re-read under test
- [ ] Green — E2E
- [ ] Amend spec 026: the manual-re-read in-scope clause and its scenario
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
