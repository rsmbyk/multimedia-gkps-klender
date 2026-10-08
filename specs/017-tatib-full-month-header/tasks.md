# Tasks 017: Show a full month name in the Tata Ibadah date header

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/017-tatib-full-month-header`)
- [ ] Red — add a focused test asserting `23 Agustus 2026` in the service header and the unchanged undated label
- [ ] Green — update the service header date formatter
- [ ] Verify the actual click-through reading route where the shell swaps pages in place
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on ITEM-019 and this spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold and focused tests pass
- [ ] Full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
