# Tasks 056: Give the stage entry links a theme-aware colour

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/056-entry-link-colours`)
- [x] Red — domain/app test (`tests/test_design_tokens.py`): add `('--link', '--canvas')` to
      `TEXT_PAIRS` — fails with `--link missing from :root`.
- [x] Green — implementation (`static/styles/design/tokens.css`: `--link` in both theme blocks;
      `static/styles/design/components.css`: `.entry__jump { color: var(--link); }`).
- [x] Red — E2E (`tests/e2e/test_reading.py`): `test_tatib_stage_entry_links_follow_the_theme` —
      light `rgb(28, 92, 60)`, toggled dark `rgb(124, 156, 240)`, underline present.
- [x] Green — targeted runs (`tests/test_design_tokens.py`, the one E2E module); full suite is
      the push step.
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
