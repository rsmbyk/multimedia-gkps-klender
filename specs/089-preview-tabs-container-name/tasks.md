# Tasks 089: Name the preview's tabs container so it cannot be mistaken for a tab

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from `develop` (`fix/089-preview-tabs-container-name`)
- [x] Red — `multimedia/web/tests.py::ServiceEntryViewTests.test_a_song_preview_has_no_tabs_for_a_single_verse`
      fails on the branch (`'preview__tab' unexpectedly found`), its positive twin passes (2 tests, 1 failure)
- [x] Green — container renamed in `multimedia/web/templates/reading/_preview_modal.html` and in the three
      `components.css` selectors; `preview.js` untouched (it uses the `data-preview-tabs-host` attribute)
- [x] Confirm the positive twin still passes:
      `test_a_song_preview_lists_its_short_reference_and_verse_tabs`
- [x] Confirm `tests/e2e/test_entry_preview.py` stays green (the header and tab cases from spec 085)
- [x] Run the targeted suites only: the pair plus `tests/e2e/test_entry_preview.py` (14 tests, OK), and
      `grep` for the old name across `static/`, `multimedia/`, `tests/` — nothing left
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
