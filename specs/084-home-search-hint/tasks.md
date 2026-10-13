# Tasks 084: Refresh the home search helper line

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/084-home-search-hint`)
- [x] Red — domain/app tests: `multimedia/web/tests.py::ReadingViewTests.test_home_is_search_first`
      expects `Try Yoh 3:16 or HAL 411`
- [x] Green — `multimedia/web/templates/reading/base.html`: the `search-home__hint` sentence
- [x] Red then green — E2E: `tests/e2e/test_reading.py`, the four hint assertions
- [x] Re-verify both examples against the stack (`/search/?q=Yoh+3:16`, `/search/?q=HAL+411`) — both
      return real matches, noted in the PR test plan
- [x] Run the targeted suites only: `multimedia/web/tests.py` (`ReadingViewTests`) and
      `tests/e2e/test_reading.py` (the home/search cases)
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
