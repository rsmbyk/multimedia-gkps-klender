# Tasks 101: Brighten the translation label after flipping a Go To passage

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/101-goto-translation-flash`; carries this Draft)
- [ ] Red — E2E: `tests/e2e/test_projector.py` — add the SIM edition fixture (Version + BookTranslation + a Matius 5:3 verse) and the Go To flip test: keyboard flip, brighten hold ~1 s and return, click parity, repeat flip, single-edition no-op
- [ ] Green — implementation: `static/web/projector.js` — shared flash helper called after each cue render; the Go To branch guards the missing edition and flashes the re-rendered label
- [ ] Run the `ProjectorE2ETests` class locally (targeted; full-suite and browser E2E runs are the push/CI step)
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Create ITEM-101 and update [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in the PR
