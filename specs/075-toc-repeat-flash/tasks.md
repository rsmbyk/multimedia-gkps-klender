# Tasks 075: Repeat a service-entry flash after it finishes

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec 075 Accepted by the project owner
- [x] Branch from current `develop` as `fix/075-toc-repeat-flash`
- [x] Red — add before/after animation and stage-replacement cases in `tests/e2e/test_reading.py`
- [x] Green — manage stage-flash completion and guard in `static/web/reading.js`
- [x] Verify click, keyboard activation, reduced motion, and no post-drag flash
- [x] Fill Traceability in `./spec.md`
- [x] Update ITEM-078 and `backlog/board.md` in the same PR
- [x] Set `VERSION`, changelog entry, and `release_version` in the same PR
- [x] Conventional Commit with Codex co-author trailer; draft PR into `develop` linking this spec

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Targeted quicklink E2E checks are green
- [x] Board, ITEM, tasks, version, and changelog are complete in the same PR
