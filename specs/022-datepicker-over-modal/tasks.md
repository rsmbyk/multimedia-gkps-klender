# Tasks 022: Let the Tata Ibadah date picker overlap the editor modal

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/022-datepicker-over-modal`)
- [x] Red — `tests/e2e/test_editor.py`: verify calendar paints and receives hit tests beyond modal scroll-content clipping, with viewport containment and unchanged form height
- [x] Green — use a top-layer/overflow-escaping popover positioned beneath the trigger; keep placement correct during modal scroll and viewport resize
- [x] Verify selection, clearing, keyboard navigation, Escape/outside click, validation rerender, and modal-close cleanup
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on ITEM-024 and this spec
- [x] If bump is not `none`: update `VERSION`, changelog, and `release_version` in the implementation PR
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking to `./spec.md`

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Focused browser regressions pass; full browser suite is deferred to push verification
- [x] Board, tasks, and version are complete in the implementation PR