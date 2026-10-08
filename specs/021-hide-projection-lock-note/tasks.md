# Tasks 021: Hide the projection-lock explanation

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/021-hide-projection-lock-note`)
- [ ] Red — `tests/e2e/test_projector.py`: entry action remains blocked and lock explanation is not rendered
- [ ] Green — suppress only refused-action copy; preserve lock and other projector status feedback
- [ ] Verify Project/Stop and Update behavior remains unchanged
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in `spec.md` hold and focused tests pass
- [ ] Full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
