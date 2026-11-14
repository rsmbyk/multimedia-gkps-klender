# Tasks 048: Make the passage book search hide non-matching books

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/048-book-picker-filter`)
- [x] Red — domain/app tests: N/A per spec (client-side visibility behavior)
- [x] Green — implementation (`static/styles/design/components.css`)
- [x] Red — E2E (`tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_book_picker_filter_hides_nonmatching_books_and_restores_all`):
      failed as expected without the CSS override
- [x] Green — E2E (same focused test passed with the override)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] Add `VERSION`, changelog `## [X.Y.Z]`, and `release_version` on this branch
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) on this branch (In review while PR
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in the PR
