# Tasks 027: Remove the projection status note

- **Status:** Accepted (owner, 2026-10-08)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/027-remove-projection-note`)
- [x] Red — `multimedia/web/tests.py`: button contract no longer expects a note element
- [x] Red — `tests/e2e/test_projector.py`: Update and window-close no longer expect the note
- [x] Green — remove `data-project-note`, `say()`/`noteTimer` in `static/web/display.js`, and the
      `.read__project-note` rules in `static/styles/design/components.css`
- [x] Verify Update still re-reads and closing the window still stops the display
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in `spec.md` hold and focused tests pass
- [ ] Board, tasks, and version (if any) are complete in this PR
