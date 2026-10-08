# Tasks 031: Clamp a text entry in the Tata Ibadah pane

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/031-clamp-pane-text`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): more than three lines renders three plus
      "…"; blank lines count; three or fewer renders in full; legacy text rows clamp; `clipped` is
      set only when truncated
- [ ] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`)
- [ ] Red — E2E (N/A per spec out-of-scope)
- [ ] Green — E2E (N/A)
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
