# Tasks 016: Use a custom date picker for Tata Ibadah forms

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/016-tatib-custom-datepicker`)
- [ ] Red — `tests/e2e/test_editor.py`: custom picker exists on create/edit, selection posts ISO, clearing submits blank, keyboard selection/Escape, no native date input
- [ ] Red — `multimedia/web/tests.py`: optional ISO date accepted and persisted
- [ ] Green — custom calendar markup, styles, behavior, and form integration
- [ ] Verify error re-render rebinds picker state and functionality
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on ITEM-018 and this spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold and focused tests pass
- [ ] Full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
