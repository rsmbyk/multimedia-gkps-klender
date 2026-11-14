# Tasks 018: Style Project and Stop projecting as primary and danger actions

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/018-project-button-styles`)
- [ ] Red — add E2E assertions in `tests/e2e/test_projector.py` for primary/danger treatment in both projection states and theme contrast
- [ ] Green — state-driven button styles in `static/styles/design/components.css`
- [ ] Verify starting/stopping projection and Update behavior remain unchanged
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on ITEM-020 and this spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold and focused tests pass
- [ ] Full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
