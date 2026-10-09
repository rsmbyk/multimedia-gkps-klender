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
- [x] Update ITEM-051 + [`backlog/board.md`](../../backlog/board.md) to In review and link PR #300
- [x] Conventional Commit on this feature branch
- [x] Open draft PR [#300](https://github.com/rsmbyk/multimedia-gkps-klender/pull/300) against `develop` linking `./spec.md`; set ITEM-051 to In review and add the PR link
- [ ] Before merge, set ITEM-051 to Done, move the board row to Done, and verify all merge requirements

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] The named E2E test is green at narrow and desktop widths
- [x] Board, tasks, and version (if any) are complete in the PR
