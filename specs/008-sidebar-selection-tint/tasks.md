# Tasks 008: Sidebar selection tint

- **Status:** Accepted (owner, 2026-10-05)
- **Plan:** [./plan.md](./plan.md) · **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch `feat/008-sidebar-selection-tint` from the active feature line
- [x] Add light/dark sidebar selected-tint contrast assertions in `tests/test_design_tokens.py`
- [x] Add the dedicated sidebar selected-background token in `static/styles/design/tokens.css`
- [x] Add E2E computed-style coverage for Bible books, Bible chapters, songbooks, songs, and Tata Ibadah services in both themes (`tests/e2e/test_reading.py`)
- [x] Apply the sidebar token and selected text color in `static/styles/design/components.css`
- [x] Verify unrelated active, hover, focus, and destination-slot styling is unchanged
- [x] Collect static files after implementation
- [x] Run the targeted browser test in both themes without Playwright skips — verified with `python manage.py test tests.e2e.test_reading tests.test_design_tokens --noinput -v 2` (28 passed, 0 skipped)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on the ITEM and spec header
- [x] Update `VERSION`, `CHANGELOG.md`, and ITEM `release_version` in the same PR
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in the same PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [ ] All acceptance scenarios in `./spec.md` hold in light and dark themes
- [ ] Token contrast and targeted browser tests are green
- [ ] Board, tasks, and version are complete in the implementation PR
