# Tasks 092: Offline public reading and service projection

- **Status:** Accepted; implementation complete, remote CI pending
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)
- **Item:** ITEM-095

## Checklist

- [x] Owner explicitly Accepts this Draft before implementation.
- [x] Create `feat/092-offline-library-sync` from current `develop`; keep Spec 091's worktree and unrelated changes untouched.
- [x] Owner explicitly authorizes combining Spec 091 and Spec 092 in the existing projector PR because their Go To behavior depends on the shared local library.
- [x] Red/green: targeted domain/application tests in `tests/test_offline_sync.py` cover manifest revisions, changed/deleted records, chunk completeness, projector service data, and the versioned worker response.
- [x] Implement revision manifest and data-only endpoints for Bible, songs, and public Tata Ibadah; serialize one canonical service snapshot for reading and projection.
- [x] Red/green: browser-store E2E covers first and incremental sync, failed/interrupted generations, eviction detection, cross-tab commit notification, and saved-copy fallback.
- [x] Red/green: service-worker E2E covers the two shells, direct offline URLs, versioned cache identity, and pass-through of legacy OBS/editor/admin/future routes.
- [x] Red/green: targeted E2E covers status UI, saved-copy indicator, async content refresh, browser history, repeated searches, tab isolation, direct search URLs, and scroll/Show more/typed-state restoration.
- [x] Red/green: targeted E2E covers immediate projector startup, saved service screens, offline Go To, cross-tab updates, and failed refresh preserving the current screen and snapshot.
- [x] Check light/dark and narrow status UI against the approved preview; verify focus, disabled, and reduced-motion states.
- [x] Fill implementation/test paths in the spec Traceability section and run targeted local checks; full suite and browser E2E remain CI checks.
- [x] Update ITEM-095 and `backlog/board.md` in the implementation PR; set `VERSION`, changelog, and `release_version` in that same PR for the minor bump.
- [x] Conventional Commit with Codex trailer and update existing draft PR #346 to carry both specs.

## Done when

- [x] Every acceptance scenario in `spec.md` holds in targeted local checks.
- [ ] Targeted tests and required remote CI are green at the pushed head.
- [ ] ITEM, board, tasks, version, and changelog are complete in the same PR.

## Draft amendment: persistent saved-copy badge

- [x] Owner approves the [sticky-badge visual preview](./preview-saved-copy-sticky.html).
- [x] Owner explicitly Accepts the Draft amendment in `plan.md` and `spec.md` before implementation.
- [x] Move the public-reading saved-copy indicator out of the flowing header and style it as the fixed, click-through badge specified above, including responsive, theme, overlay, and print behavior.
- [x] Extend the targeted saved-reading browser check for persistence while scrolling, failed-refresh visibility, narrow positioning, and print hiding; existing refresh checks continue to cover fresh-content removal.
- [ ] Run targeted local checks and required remote CI at the final pushed head; update ITEM-095 and PR #346 with the amendment and validation.

## Draft amendment: browser-offline badge color

- [x] Owner approves the [offline-color preview](./preview-saved-copy-offline.html).
- [x] Owner explicitly Accepts this Draft amendment before implementation.
- [x] Update the saved-copy badge dot from amber to the danger theme token on browser `offline`, and restore amber on browser `online`; do not infer state from request failures or delays.
- [ ] Add targeted browser checks for both transitions in light/dark themes and verify a failed content refresh alone does not change the dot.
- [ ] Run targeted local checks and required remote CI at the final pushed head; update ITEM-095 and PR #346 with the amendment and validation.

## Draft amendment: separate connection and library readiness

- [x] Owner approves the [connectivity and availability preview](./preview-connectivity-vs-availability.html).
- [x] Owner explicitly Accepts this Draft amendment before implementation.
- [x] Separate browser connection status from offline-library availability in the main-rail popover, preserving sync state, timestamps, and action behavior.
- [ ] Add targeted browser coverage for online/offline crossed with ready, not-ready, syncing, and update-failed states; check light and dark themes.
- [ ] Run targeted local checks and required remote CI at the final pushed head; update ITEM-095 and PR #346 with the amendment and validation.

## Draft amendment: bottom-positioned status popover

- [x] Owner approves the [bottom-positioned preview](./preview-offline-popover-bottom.html).
- [x] Owner explicitly Accepts this Draft amendment before implementation.
- [x] Move the popover bottom offset to 12px and center the connection row's label and value in a balanced 40px row.
- [x] Align the narrow-screen browser assertion with the accepted 12px bottom offset.
- [ ] Run targeted local checks and required remote CI at the final pushed head; update ITEM-095 and PR #346 with the amendment and validation.

## Draft amendment: center saved-copy badge

- [x] Owner approves the [centered-badge visual preview](./preview-saved-copy-centered.html).
- [x] Owner explicitly Accepts this Draft amendment in `plan.md` and `spec.md` before implementation.
- [x] Center the fixed badge on the visible reading-stage center, accounting for the rail and currently visible sidebar/chapter columns; keep the 16px desktop and 12px narrow top offsets and preserve the existing badge appearance and behavior.
- [x] Add or update targeted browser coverage for wide/narrow viewports, sidebar states, resizing, and scrolling without content shift.
- [x] Run the targeted `test_failed_online_content_refresh_keeps_the_saved_reading` browser check.
- [x] Run required remote CI at the final pushed head; update ITEM-095 and PR #346 with the amendment and validation.
