# Tasks 113: Enable Media Library sharing in a fresh session

- **Status:** In review — draft PR #361; targeted Django and browser regressions passed
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from current `develop`: `fix/113-media-library-share-csrf`
- [x] Red — Django regression tests in `multimedia/web/test_media.py`
- [x] Green — ensure the Media Library response sets the CSRF cookie in `multimedia/web/reading/views.py`
- [x] Red — E2E regression in `tests/e2e/test_media_library.py`
- [x] Green — verify direct-open Share online flow in E2E
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Named Django and E2E tests are green
- [x] Board, tasks, and version (if any) are complete in this PR
