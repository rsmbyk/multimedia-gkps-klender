# Tasks 023: Make Sundays more prominent in the Tata Ibadah date picker

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/023-emphasize-sundays`)
- [x] Red — `tests/e2e/test_editor.py`: Sunday dates/header are visually distinct from weekdays and existing selection/today indicators remain
- [x] Green — mark Sunday dates and apply theme-aware emphasis without changing date behavior
- [x] Verify existing Tata Ibadah date-picker interactions and light/dark theme styling
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on ITEM-025 and this spec
- [x] If bump is not `none`: prepare `VERSION`, changelog, and `release_version` (0.11.6)
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md); remain In progress until a PR is opened
- [ ] Conventional Commit + draft PR linking to `./spec.md` (only when requested)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Focused browser regressions pass; full browser suite is deferred to push verification
- [ ] Board, tasks, and version land with the implementation in the same PR