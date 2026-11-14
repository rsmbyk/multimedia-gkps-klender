# Tasks 014: Clear stale row-edit visibility after modal close

- **Status:** Accepted (owner, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/014-editor-focus-cleanup`)
- [ ] Reproduce and record the current pointer-close behavior in a focused Playwright test
- [ ] Red — `tests/e2e/test_editor.py` (cancel/save across song, songbook and Tata Ibadah; pointer-away visibility and hover positive control)
- [ ] Green — correct the shared focus restoration / modal-close path, not only one template
- [ ] Red/green — keyboard focus and other modal regressions in `tests/e2e/test_entries.py`, `tests/e2e/test_old_rows.py`, and `tests/e2e/test_projector.py` as appropriate
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on ITEM-016 and this spec; update `VERSION`, changelog, and `release_version` in the implementation PR
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the implementation PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in spec.md hold, including keyboard focus visibility
- [ ] Focused browser cases pass; full browser suite is deferred to push verification
- [ ] Board, tasks, and version are complete in the implementation PR
