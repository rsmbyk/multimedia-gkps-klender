# Tasks 019: Clear remembered search when the home is reset

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/019-search-reset-state`)
- [ ] Red — `tests/e2e/test_reading.py`: query, leave for a sidebar page, fresh `/home/` reset, then rail Search stays on empty home and stored URL/scroll keys are absent
- [ ] Green — clear remembered search only on explicit reset initialization in `static/web/reading.js`
- [ ] Keep `test_search_state_survives_sidebar_browsing` and `test_search_icon_never_opens_a_stale_stored_url` green
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on ITEM-021 and this spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Focused browser regressions pass; full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
