# Tasks 009: Higher-legibility selected sidebar tint

- **Status:** Accepted (owner, 2026-10-06)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner (2026-10-06)
- [x] Branch from the current base (`feat/009-sidebar-tint-legibility` from `develop`)
- [x] Red — token assertion in `tests/test_design_tokens.py` failed on the previous `#B9C6B9` value
- [x] Green — update `static/styles/design/tokens.css`; all five token tests pass
- [x] Red — attempted the targeted E2E check; Django skipped it because Chromium is unavailable in the container
- [x] Green — targeted automated E2E check passes after installing Chromium and its required libraries in the test container
- [x] Manually verified all five light-theme row types and a dark-theme selected service through the live home → in-page path; dark colors remain unchanged
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] Set `VERSION` to `0.11.2`, add its changelog section, and set the ITEM `release_version` to `0.11.2`
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green, including the targeted automated E2E check
- [ ] Board, tasks, and version (if any) are complete in this PR
