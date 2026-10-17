# Tasks 103: Local Media Library and service media entries

- **Status:** Accepted implementation and Compose amendment included in consolidated PR #359; 148 targeted tests passed, exact-head GitHub CI pending
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts this Draft; implementation authorized on 2026-10-17.
- [x] Spec/ITEM 102 landed on `develop`; rebased `feat/103-local-media-library` onto `ad3ed42` and checked the distinct 102/103 references. Recheck against `develop` before opening the implementation PR.
- [x] Document the Docker-managed media volume, companion startup, loopback origin rules, and local index in `docs/ARCHITECTURE.md`, `docs/local-media-companion.md`, and ADR 0004.
- [x] Focused domain/application tests for media identity, immutable entry reference, import validation, local deduplication, missing state, and cleanup.
- [x] Server metadata/reference migration, service-entry forms/endpoints, and local companion. Large file bodies bypass Vercel.
- [x] Focused browser E2E for entry Create/Edit, library controls, disconnected/missing state, and blank media projector navigation.
- [x] Review the live Library view against the approved preview in disconnected and connected states, and check small-screen and reduced-motion behavior. Both Chrome and OBS dock use the same loopback companion and Docker-managed volume.
- [x] Run 53 targeted local tests and push the implementation; full CI fast checks and all Browser E2E shards passed at implementation commit [`e7e26ac`](https://github.com/rsmbyk/multimedia-gkps-klender/commit/e7e26ac).
- [x] Re-run the consolidated media, saved-renderer, Compose, and projector Django modules after integrating Spec 106: 148 tests passed.
- [x] Fill Traceability in `./spec.md`; complete final acceptance review before marking Done.
- [ ] Keep ITEM-103 and `backlog/board.md` in consolidated PR [#359](https://github.com/rsmbyk/multimedia-gkps-klender/pull/359); mark Done before merge.
- [x] Apply `bump: minor` in this PR: `VERSION` and changelog 1.14.0, matching the current `develop` 1.13.4 line.
- [x] Conventional Commits with Codex trailers and consolidated PR [#359](https://github.com/rsmbyk/multimedia-gkps-klender/pull/359) to `develop` using the repository PR template.

## Done when

- [x] All acceptance scenarios in `spec.md` hold, including blank media Preview/projector behavior.
- [ ] The full consolidated PR checks, board, tasks, and version records are complete before merge.

## Accepted Compose amendment — 2026-10-17

- [x] Owner accepts the Docker-managed volume amendment before implementation.
- [x] Add the media companion to `docker-compose.yml` with a named volume for media bytes and the SQLite index.
- [x] Change the companion endpoint from `47863` to `63174` consistently in its listener, browser clients, Compose mapping, documentation, and tests; preserve API paths and payloads.
- [x] Require `GKPS_MEDIA_PRODUCTION_ORIGIN` in the project-root `.env`, combine it in Compose with both local origins (`localhost` and `127.0.0.1` at the effective `WEB_PORT`), then pass the exact allowlist to the companion as `GKPS_MEDIA_ALLOWED_ORIGINS`; fail closed if the production origin is missing or invalid.
- [x] Remove the folder-location field from the connected status response and popup; keep connection, count, and total size.
- [x] Update `docs/ARCHITECTURE.md`, `docs/local-media-companion.md`, ADR 0004, and Compose/operator documentation to describe the Docker-managed volume and its persistence/removal behavior.
- [x] Add targeted tests for Compose configuration and consistent port `63174` usage, volume-root persistence, the production origin, both local loopback origins, and status fields; rerun the focused Media Library tests and E2E class.
- [x] Verify `docker compose down`/`up` preserves files and index, while explicit named-volume removal deletes them.
