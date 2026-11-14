# Tasks 088: A stage-only swap preserves the first panel, not the second

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from `develop` (`fix/088-sidebar-state-guard-beyond-nav`)
- [x] Red — the regression on the branch: `ReadingE2ETests.test_service_text_sidebar_shows_two_lines_and_centers_grip`
      fails (`#chList .songrow[data-i="e240"]` resolves but is hidden: the contents pane never opened),
      while `SidebarStateOnItemOpenTests` passes — recorded before touching `reading.js`
- [x] Green — `static/web/reading.js`: `nav` stays behind the stage-only guard, `ch` is applied for every
      stage swap, with the comment that says why
- [x] Confirm spec 080's own cases stay green: `SidebarStateOnItemOpenTests` (all five, including the
      390px case) and the two tests spec 080 adjusted
- [x] Run the targeted suites only: that class plus the regression test, then the whole
      `ReadingE2ETests` class and `test_tatib_hover.py` as the neighbouring paths (75 tests, OK)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
