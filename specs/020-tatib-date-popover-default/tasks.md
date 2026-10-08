# Tasks 020: Use a date popover with a Sunday default

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/020-tatib-date-popover-default`)
- [ ] Red — `multimedia/web/tests.py`: nearest Sunday for Sunday and non-Sunday; existing dated/undated edit values unchanged
- [ ] Green — `multimedia/web/reading/editors.py`: local-date Sunday initial value for create only
- [ ] Red — `tests/e2e/test_editor.py`: dropdown placement, selected Sunday, clear and ISO submission
- [ ] Green — popover positioning and date-picker initialization
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in `spec.md` hold and focused tests pass
- [ ] Full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
