# Tasks 050: Search and label songs by songbook short name

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/050-song-picker-short-name-search`)
- [x] Red — app regression in `multimedia/web/tests.py`: song-options search matches `book.short_name` even when title/number do not
- [x] Green — implementation in `multimedia/web/reading/views.py::entry_song_options`, option template, and selected-label rendering
- [x] Red — E2E regression in `tests/e2e/test_entry_pickers.py`: abbreviation search and selected hymn reference in add/edit forms
- [x] Green — E2E search, selected-label, non-hymn label, and verse-loading behavior
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on ITEM-052 and this spec
- [x] Add `VERSION` 1.3.16, changelog `## [1.3.16]`, and `release_version: 1.3.16` on this branch
- [x] Update ITEM-052 + [`backlog/board.md`](../../backlog/board.md) in this PR (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] The named app and E2E regressions are green
- [x] Board, tasks, and version (if any) are complete in the PR
