# Tasks 110: Give Tata Ibadah media entries more breathing room

- **Status:** Implemented and included in consolidated PR #359; 148 targeted tests and full CI passed on code head `4913119`
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner explicitly accepted this Draft on 2026-10-17.
- [x] Create `fix/108-roomier-media-entries` from the current media UI work.
- [x] Add targeted E2E checks for row height, icon/text centering, text/break row sizing, and narrow-screen overflow.
- [x] Implement the approved media-row spacing in `static/styles/design/components.css`.
- [x] Run the targeted Media Library E2E module (18 passing) and `git diff --check`.
- [x] Fill spec traceability with the targeted E2E method and implementation references.
- [x] Set the patch version from the current media stack: `VERSION` 1.14.5, `CHANGELOG.md`, and ITEM `release_version: 1.14.5`.
- [x] Update ITEM and [`backlog/board.md`](../../backlog/board.md) in consolidated PR #359.
- [x] Commit as `fix(media): give Tata Ibadah media rows more room` with the Codex co-author trailer.
- [x] Include this spec in PR #359 to `develop`; move ITEM to Done before merge.

## Done when

- [x] All acceptance scenarios hold at desktop and narrow widths; the dimension rules are theme-independent.
- [x] Targeted browser checks pass without affecting text or break rows.
- [x] Board, tasks, and version metadata are complete in consolidated PR #359.
