# Tasks 049: Center the TB/SIM switch and contain passage number pickers

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/049-passage-modal-layout`)
- [x] Red — E2E: `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_passage_form_layout_fits_modal_at_narrow_viewport`
      failed before implementation: at 536px the switch ended below the Book label.
- [x] Green — implementation: `multimedia/web/templates/reading/_entry_form.html`, `static/styles/design/components.css`
- [x] Green — focused E2E: layout at 536×426, 320×720 and 1200×900; existing add/edit and TB/SIM picker tests
      in `tests/e2e/test_entries.py` and `tests/e2e/test_entry_pickers.py` (5 tests passed).
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on ITEM-051 and this spec
- [x] Add `VERSION` 1.3.15, changelog `## [1.3.15]`, and `release_version: 1.3.15` on this branch
- [x] Update ITEM-051 + [`backlog/board.md`](../../backlog/board.md) to In progress on this branch
- [x] Conventional Commit on this feature branch
- [ ] Open a draft PR against `develop` linking `./spec.md`; set ITEM-051 to In review and add the PR link (Done before merge)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] The named E2E test is green at narrow and desktop widths
- [ ] Board, tasks, and version (if any) are complete in the PR
