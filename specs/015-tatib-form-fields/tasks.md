# Tasks 015: Remove first-section and active controls from Tata Ibadah forms

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/015-tatib-form-fields`)
- [ ] Red — `multimedia/web/tests.py` (`EditorViewTests`): fields absent on create/edit, posted omitted fields ignored, new default active, inactive value preserved, no legacy item created
- [ ] Green — update TataIbadahForm and save behavior in `multimedia/web/reading/editors.py`
- [ ] Red/green — `tests/e2e/test_editor.py`: create/edit fields absent; saved empty service remains discoverable and fillable
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on ITEM-017 and this spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold and focused tests pass
- [ ] Full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
