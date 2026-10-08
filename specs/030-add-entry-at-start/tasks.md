# Tasks 030: Add a service entry at the beginning

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/030-add-entry-at-start`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): `after=start` inserts at order 1 and
      shifts entries and legacy rows; the order stays contiguous; a rejected form keeps `after=start`
- [ ] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`)
- [ ] Red — E2E (`tests/e2e/test_reorder.py`): add from the leading bar; it shows first in the pane
      and projector
- [ ] Green — E2E
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
