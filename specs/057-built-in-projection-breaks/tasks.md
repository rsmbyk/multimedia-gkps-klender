# Tasks 057: Built-in blank after each entry and each song verse

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/057-built-in-projection-breaks`)
- [ ] Red — domain/app tests: `multimedia/web/tests.py` (screen sequence for text, song verses, scripture, section break)
- [ ] Green — implementation: `multimedia/web/reading/views.py` (`_projector_screens`, song verse grouping)
- [ ] Red — E2E: `tests/e2e/test_projector.py` only if a step-through already exists; otherwise N/A
- [ ] Green — E2E
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header (minor, unless Accept changes it)
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
