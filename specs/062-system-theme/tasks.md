# Tasks 062: System theme as the default appearance mode

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec Accepted by the project owner, including public reading scope
- [x] Branch from current `develop` (`feat/062-system-theme`)
- [x] Add Playwright scenarios in `tests/e2e/test_reading.py`
- [x] Green — reading layout, theme control, storage, and system listener; reuse existing palettes
- [x] Verify reading pages in both palettes and browser storage fallback
- [x] Fill Traceability in `./spec.md`
- [x] Set ITEM bump and release version; update `VERSION` and `CHANGELOG.md` in the implementation PR
- [x] Update ITEM and `backlog/board.md` in the implementation PR
- [x] Conventional Commit and draft PR [#315](https://github.com/rsmbyk/multimedia-gkps-klender/pull/315) linking `./spec.md`

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] New theme E2E tests are green; a pre-existing exact-geometry test fails on `develop` too
- [x] Board, tasks, and version are complete in the same PR
