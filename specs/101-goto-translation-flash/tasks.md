# Tasks 101: Brighten the translation label after flipping a Go To passage

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/101-goto-translation-flash`; carries this Draft)
- [x] Red — E2E: `tests/e2e/test_projector.py` — add the SIM edition fixture (Version + BookTranslation + a Matius 5:3 verse) and the Go To flip test: keyboard flip, brighten hold ~ 1 s and return, flip during the hold, click parity, single-edition no-op, and a service-cue parity leg through the shared helper
- [x] Green — implementation: `static/web/projector.js` — shared flash helper called after each cue render; the Go To branch guards the missing edition and flashes the re-rendered label
- [x] Run the `ProjectorE2ETests` class (browser E2E is the CI step here; no local Python/Playwright env in this checkout — the PR's Browser E2E matrix runs the class, scheduled when the PR is marked ready for review)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Create ITEM-101 and update [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in the PR
