# Tasks 057: Built-in blank after each entry and each song verse

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/057-built-in-projection-breaks`)
- [x] Red — domain/app tests: `multimedia/web/tests.py` (screen sequence for text, song verses, scripture, section break)
- [x] Green — implementation: `multimedia/web/reading/views.py` (`_projector_screens`, song verse grouping)
- [x] Red — E2E: `tests/e2e/test_projector.py` only if a step-through already exists; otherwise N/A
- [x] Green — E2E
- [x] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header (minor, unless Accept changes it)
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
