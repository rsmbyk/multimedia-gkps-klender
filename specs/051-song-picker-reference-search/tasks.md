# Tasks 051: Search songs by songbook reference and title

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/051-song-picker-reference-search`)
- [x] Red — app regressions in `multimedia/web/tests.py`: book full name, book-name substring, title matches kept alongside book matches, whole book listed (each observed failing before its matching implementation)
- [x] Green — add the hymn-book-name condition to the picker's free-text filter and draw the reference parser's aliases from hymn books only
- [x] Red — E2E book-filter regression in `tests/e2e/test_entry_pickers.py`
- [x] Red — app regressions in `multimedia/web/tests.py`: short/full book names + number, reference + title, number-prefix ranges across KJ/PKJ, substring book phrases, and exact sub-number suffixes
- [x] Green — implement combined-reference matching with hymn-book substring aliases, number-prefix ranges, optional exact sub-number suffix, and optional title condition
- [x] E2E — add and edit picker regressions in `tests/e2e/test_entry_pickers.py` for short/full references, number prefixes, sub-number suffixes, and title suffix
- [x] Green — targeted app and E2E acceptance tests pass for add and edit pickers
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on ITEM-053 and this spec
- [x] Add `VERSION` 1.3.17, changelog `## [1.3.17]`, and `release_version: 1.3.17` on this branch
- [x] Update ITEM-053 + [`backlog/board.md`](../../backlog/board.md) in this PR (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] The named app and E2E regressions are green
- [x] Board, tasks, and version (if any) are complete in the PR
