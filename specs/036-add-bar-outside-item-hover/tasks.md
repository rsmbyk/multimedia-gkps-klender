# Tasks 036: Keep the add bar out of the item hover

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/036-add-bar-outside-item-hover`)
- [ ] Red — domain/app tests (N/A per spec out-of-scope)
- [ ] Green — implementation (`static/styles/design/components.css`)
- [ ] Red — E2E (`tests/e2e/test_tatib_entry_controls.py`): hovering the add bar leaves the item
      un-highlighted with controls hidden; the add buttons show; hovering the item still reveals the
      add bar
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
