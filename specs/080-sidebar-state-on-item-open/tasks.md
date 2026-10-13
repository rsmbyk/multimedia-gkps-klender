# Tasks 080: Keep the first-level sidebar state when a page opens from a second-level list

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/080-sidebar-state-on-item-open`)
- [x] Red — E2E: `tests/e2e/test_reading.py`, new class `SidebarStateOnItemOpenTests`
      - [ ] collapsed Tata Ibadah panel + add entry keeps it collapsed
      - [ ] collapsed songbook panel + open song keeps it collapsed, list still open and selected
      - [ ] mini Bible panel + open chapter stays mini
      - [ ] main-menu switch still opens the arriving section
      - [ ] narrow width: a collapsed panel stays collapsed through a song
- [x] Green — `static/web/reading.js`: preserve `root.dataset.nav` / `root.dataset.ch` for the
      `chapter`, `song`, `service`, and `refresh` kinds
- [x] Run the targeted suites only: `tests/e2e/test_reading.py` (`SidebarStateOnItemOpenTests`) plus
      the neighbouring sidebar classes in the same module
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
