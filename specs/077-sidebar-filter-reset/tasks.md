# Tasks 077: Clear sidebar filters when switching main menus

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec 077 Accepted by the project owner
- [x] Branch from current `develop` as `fix/077-sidebar-filter-reset`
- [x] Red — add cross-menu, return, same-menu, and search-query cases in `tests/e2e/test_reading.py`
- [x] Green — reset both sidebar filters on successful rail section switch in `static/web/reading.js`
- [x] Verify clear-button visibility, full list restoration, and responsive navigation
- [x] Fill Traceability in `./spec.md`
- [x] Update ITEM-080 and `backlog/board.md` in the same PR
- [x] Set `VERSION`, changelog entry, and `release_version` in the same PR
- [x] Conventional Commit with Codex co-author trailer; draft PR into `develop` linking this spec

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Targeted sidebar-filter E2E checks are green
- [x] Board, ITEM, tasks, version, and changelog are complete in the same PR
