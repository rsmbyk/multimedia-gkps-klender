# Tasks 103: Local Media Library and service media entries

- **Status:** Accepted by owner on 2026-10-17 — implementation authorized
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts this Draft; implementation authorized on 2026-10-17.
- [ ] Reconcile spec/ITEM 103 with current `develop` and the parallel spec/ITEM 102 branch before opening a PR; update `feat/103-local-media-library` onto the integration base after 102 lands.
- [ ] Document the decided per-user OS data folder, companion packaging, loopback pairing/origin rules, local index, and Windows/macOS/Linux startup path; update `docs/ARCHITECTURE.md` and an ADR when chosen.
- [ ] Red: focused domain/application tests for media identity, immutable entry reference, import validation, local deduplication, missing state, and cleanup (`multimedia/tatib/tests.py`, `multimedia/web/tests.py`, new companion tests).
- [ ] Green: server metadata/reference migration, service-entry forms/endpoints, and local companion. Keep all large file bodies off Vercel.
- [ ] Red: focused browser E2E for entry Create/Edit, library controls, disconnected/missing state, and blank media projector navigation (new media E2E module plus `tests/e2e/test_projector.py`).
- [ ] Green: UI integration matching both approved previews, including responsive/dark/reduced-motion behavior and Chrome/OBS-dock sharing of one local folder.
- [ ] Run targeted local tests only, then push for full CI and browser E2E at the exact head.
- [ ] Fill Traceability in `./spec.md` and check all acceptance scenarios.
- [ ] Keep ITEM-103 and `backlog/board.md` in the same PR; mark In review with PR link, then Done before merge.
- [ ] Apply `bump: minor` in that PR: update `VERSION`, changelog version section, and ITEM `release_version` based on the then-current integration line.
- [ ] Conventional Commit with Codex trailer and a draft PR to `develop` using the repository PR template.

## Done when

- [ ] All acceptance scenarios in `spec.md` hold, including blank media Preview/projector behavior.
- [ ] The full PR, tests, board, tasks, and version records are complete before merge.
