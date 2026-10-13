# Tasks 081: Renumber the drag copy while a row is being reordered

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/081-reorder-index-while-dragging`)
- [x] Red — E2E: `tests/e2e/test_reorder.py`
      - [x] the copy reads the live position while dragging down and up
      - [x] the copy's number matches the row's number after the drop
      - [x] a section break advances the count and still paints nothing
      - [x] cancel / no-op press leaves the original numbers
- [x] Green — `static/web/reorder.js`: `renumber()` hands the dragged row's number to the drag copy
- [x] Keep `tests/e2e/test_toc_number_centering.py::test_drag_copy_keeps_the_number_centered` green
- [x] Run the targeted suites only: `tests/e2e/test_reorder.py` and
      `tests/e2e/test_toc_number_centering.py`
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
