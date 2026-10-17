# Tasks 103: Local Media Library and service media entries

- **Status:** Accepted by owner on 2026-10-17 — implementation authorized
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts this Draft; implementation authorized on 2026-10-17.
- [x] Spec/ITEM 102 landed on `develop`; rebased `feat/103-local-media-library` onto `ad3ed42` and checked the distinct 102/103 references. Recheck against `develop` before opening the implementation PR.
- [x] Document the per-user OS data folder, companion startup, loopback origin rules, and local index in `docs/ARCHITECTURE.md`, `docs/local-media-companion.md`, and ADR 0004.
- [x] Focused domain/application tests for media identity, immutable entry reference, import validation, local deduplication, missing state, and cleanup.
- [x] Server metadata/reference migration, service-entry forms/endpoints, and local companion. Large file bodies bypass Vercel.
- [x] Focused browser E2E for entry Create/Edit, library controls, disconnected/missing state, and blank media projector navigation.
- [x] Review the live Library view against the approved preview in disconnected and connected states, and check small-screen and reduced-motion behavior. Both Chrome and OBS dock use the same loopback companion and OS-user folder.
- [ ] Run targeted local tests only, then push for full CI and browser E2E at the exact head.
- [x] Fill Traceability in `./spec.md`; complete final acceptance review before marking Done.
- [ ] Keep ITEM-103 and `backlog/board.md` in the same PR; mark In review with PR link, then Done before merge.
- [ ] Apply `bump: minor` in that PR: update `VERSION`, changelog version section, and ITEM `release_version` based on the then-current integration line.
- [ ] Conventional Commit with Codex trailer and a draft PR to `develop` using the repository PR template.

## Done when

- [ ] All acceptance scenarios in `spec.md` hold, including blank media Preview/projector behavior.
- [ ] The full PR, tests, board, tasks, and version records are complete before merge.
