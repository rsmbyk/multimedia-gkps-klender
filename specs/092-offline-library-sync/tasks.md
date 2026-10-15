# Tasks 092: Offline public reading and service projection

- **Status:** Accepted; in progress
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)
- **Item:** ITEM-095

## Checklist

- [x] Owner explicitly Accepts this Draft before implementation.
- [x] Create `feat/092-offline-library-sync` from current `develop`; keep Spec 091's worktree and unrelated changes untouched.
- [x] Owner explicitly authorizes combining Spec 091 and Spec 092 in the existing projector PR because their Go To behavior depends on the shared local library.
- [ ] Red: targeted domain/application tests in `tests/test_offline_sync.py` for manifest revisions, changed/deleted records, snapshot completeness, atomic commit, and projector service data.
- [ ] Green: revision manifest and data-only endpoints for Bible, songs, and public Tata Ibadah; one canonical service snapshot sufficient for reading and projection.
- [ ] Red/green: browser-store tests for first sync, incremental sync, failed/interrupted sync, eviction detection, cross-tab commit notification, and stale-content fallback.
- [ ] Red/green: scoped service-worker tests for the two shells, direct offline URLs, asset version update, and pass-through of legacy OBS/editor/admin/future routes.
- [ ] Red/green: targeted E2E in `tests/e2e/test_offline_library.py` for status UI, saved-copy indicator, local content with async data refresh, full browser-history behavior, same-query resubmission, tab isolation, direct search URL, and scroll/Show more/typed-state restoration.
- [ ] Red/green: targeted E2E in `tests/e2e/test_projector.py` for immediate startup, saved service screens, offline Go To, cross-tab sync visibility, and failed refresh preserving the current screen.
- [ ] Check light/dark and narrow status UI against the approved preview; verify focus, disabled, and reduced-motion states.
- [ ] Fill final implementation/test paths in the spec Traceability section and run only targeted local checks; full suite and browser E2E belong to CI.
- [ ] Update ITEM-095 and `backlog/board.md` in the implementation PR; set `VERSION`, changelog, and `release_version` in that same PR for the minor bump.
- [x] Conventional Commit with Codex trailer and update existing draft PR #346 to carry both specs.

## Done when

- [ ] Every acceptance scenario in `spec.md` holds.
- [ ] Targeted tests and required remote CI are green at the pushed head.
- [ ] ITEM, board, tasks, version, and changelog are complete in the same PR.
