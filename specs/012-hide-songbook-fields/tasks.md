# Tasks 012: Hide short name and hymn-book fields in songbook forms

- **Status:** Accepted (owner, 2026-10-06)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner (2026-10-06)
- [x] Branch from the current base (`feat/012-hide-songbook-fields`)
- [x] Red — Django tests in `multimedia/web/tests.py` (`EditorViewTests`): form fields absent on create/edit; create uses defaults; edits and handcrafted POSTs preserve omitted values (four expected failures before implementation)
- [x] Green — restrict `SongbookForm` to visible fields in `multimedia/web/reading/editors.py`; focused `EditorViewTests` module passes (23 tests)
- [x] Add Playwright acceptance in `tests/e2e/test_editor.py` (`EditorE2ETests`): create and edit modals contain neither field; browser execution deferred to the push verification step per the owner's preference
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on ITEM-014 and this spec
- [x] Set `VERSION` to `0.11.4`, add the changelog section, and set ITEM release version for the same PR
- [ ] Update ITEM-014 + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Django tests named above are green; run the deferred Playwright tests at push verification
- [ ] Board, tasks, and version (if any) are complete in this PR
