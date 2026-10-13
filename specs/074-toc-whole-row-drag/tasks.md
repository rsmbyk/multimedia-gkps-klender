# Tasks 074: Drag service entries from the whole sidebar row

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec 074 Accepted by the project owner
- [x] Branch from current `develop` as `feat/074-toc-whole-row-drag`
- [x] Red — extend `tests/e2e/test_reorder.py` for row-body drag, plain click, canceled drag, touch input pass-through, and keyboard grip
- [x] Green — expand the pointer start target in `static/web/reorder.js` and row cursor styles in `static/styles/design/components.css`
- [x] Verify save-on-drop, drag ghost, rollback, and no post-drag quicklink
- [x] Fill Traceability in `./spec.md`
- [ ] Update ITEM-077 and `backlog/board.md` in the same PR
- [ ] Set `VERSION`, changelog entry, and `release_version` in the same PR
- [ ] Conventional Commit with Codex co-author trailer; draft PR into `develop` linking this spec

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Targeted reorder E2E checks are green
- [ ] Board, ITEM, tasks, version, and changelog are complete in the same PR
