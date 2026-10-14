# Tasks 090: Keep the Bible book sidebar mini when selecting a book

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from current `develop` (`fix/090-bible-mini-book-selection`)
- [x] Red — add a Playwright regression in `tests/e2e/test_reading.py` for a different book clicked from mini, chapter pane and selection, same-book toggle, explicit expand, and selection while open
- [x] Green — update `static/web/reading.js` to preserve the first-sidebar state for Bible book tile navigation while using the arriving chapter-pane state
- [x] Run the new case, `SidebarStateOnItemOpenTests`, and the spec 088 contents-pane regression (7 tests, OK)
- [x] Fill Traceability in `./spec.md` with the final test and implementation references
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: update `VERSION`, `CHANGELOG.md`, and `release_version` in this PR
- [ ] Update ITEM and [`backlog/board.md`](../../backlog/board.md) in this PR
- [ ] Conventional Commit and draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in `spec.md` hold
- [ ] Targeted E2E passes
- [ ] Board, tasks, and version are complete in this PR
