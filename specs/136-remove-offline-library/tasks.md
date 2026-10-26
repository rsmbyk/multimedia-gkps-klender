# Tasks — remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Date**: 2026-10-26
**Order used**: Setup → Foundational → US1 → US2 → US3 → US4 → US5 → Polish, one agent in one
thread. `[P]` marks order-independent work, not concurrent work.

## Phase 1 — Setup

- [ ] T001 [P] Inventory the removal by grep and confirm no reference survives outside the pack: `grep -rn -i 'offline\|GKPSOffline\|service-worker' multimedia static tests docs --include='*.py' --include='*.html' --include='*.js' --include='*.css' --include='*.md'`; record any site not already listed in `research.md` D1.
- [ ] T002 [P] Confirm the slice's identifiers against the base: spec `136` free in every worktree and `origin/develop`; `ITEM-146` free; `VERSION` `1.20.14`; the tracker anchor for ITEM-146 (the card passes `Speccing` when the owner promotes it — backfill `issue:` then).

## Phase 2 — Foundational

- [ ] T003 Delete the offline front-end modules: `static/web/offline-library.js`, `offline-status.js`, `offline-render.js`, `service-worker.js`, `static/styles/design/offline.css`.
- [ ] T004 Delete the offline server module `multimedia/web/reading/offline.py` and its four routes in `multimedia/urls.py` (`offline-manifest`, `offline-chunk`, `offline-projector-shell`, `offline-worker`); keep the `reading_views` import.
- [ ] T005 Create `multimedia/web/reading/goto.py` with the three views and route them under `/projector/goto/` in `multimedia/urls.py`, each `Cache-Control: no-store`, `404` on a missing target.
- [ ] T006 Add `static/styles/design/projector.css` rules: `.projector-find__row.is-loading`, `.projector-find__spinner`, `.cue-loading`, `.projector-find input:disabled`, `@keyframes goto-load-spin`, and the reduced-motion rule — the spec's measured numbers (12px row spinner, 14px cue spinner, `right: 74px`, `bottom: 25px`, 800ms linear).

## Phase 3 — US1: the app keeps no local copy (P1)

- [ ] T007 [P] [US1] Write the failing tests: `multimedia/web/tests.py::test_the_offline_routes_are_gone` (four 404s) and `tests/e2e/test_projector.py::test_the_page_leaves_no_browser_storage` (worker registrations empty, `caches.keys()` empty, no `gkps-public-library`).
- [ ] T008 [US1] Make T007 green: remove the offline link, the rail button, the offline panel, the `Saved copy` label and the three offline script tags from `multimedia/web/templates/reading/base.html`; unregister any existing service worker and delete `gkps-public-library` in `static/web/reading.js`'s boot (one small block, so a returning browser is cleaned).
- [ ] T009 [US1] Remove the saved-copy branch from `static/web/reading.js` `navigate()` (`GKPSOfflineRender`, the `status()` probe, the offline failure copy) and the direct-boot hydration at the file's end; leave history, focus, scroll and the search snapshot.
- [ ] T010 [US1] Remove the saved-service fallback from `static/web/projector.js`: the `GKPSOffline` branch in `reflow()`, `drawSavedScreens()`, the `offline:changed` listener, the "not saved for offline use yet" copy, and the `GKPSOffline.sync()` calls; remove the `offline-library.js` tag from `projector.html`.
- [ ] T011 [US1] Delete the offline tests: `tests/test_offline_sync.py`, `tests/e2e/test_offline_library.py`, `tests/e2e/test_saved_render_parity.py`, and the offline cases in `tests/e2e/test_navigation_freshness.py`, `test_pdf_display.py`, `test_powerpoint_display.py`, `test_projector.py`.
- [ ] T012 [US1] Rewrite `tests/e2e/test_navigation_freshness.py` to the surviving behaviour: one document request per navigation, and the stage's content is the server's.
- [ ] T013 [P] [US1] Write the failing E2E `test_the_reading_shell_carries_no_offline_control` (no `#offlineSyncButton`, no `#offlineSyncPanel`, no `#offlineSavedSource`, no offline script) and make it green.
- [ ] T039 [US1] Write the failing E2E `test_a_returning_browser_loses_its_library`: seed the old `gkps-public-library` database and a service-worker registration, load `/home/`, and assert the database is deleted and the worker unregistered.
- [ ] T040 [US1] Write the failing E2E `test_an_empty_service_shows_its_empty_state`: the projector for a service with no items reads its empty copy and names no saved copy.

## Phase 4 — US2: Go To searches an index held in the page (P1)

- [ ] T014 [P] [US2] Write the failing server tests in `multimedia/web/tests.py`: `test_the_index_carries_no_verse_text_or_lyric`, `test_the_index_stays_under_one_hundred_and_thirty_kilobytes`, and `test_the_index_lists_every_book_edition_and_active_song`.
- [ ] T015 [US2] Make T014 green: implement `goto.index` — books with editions and per-chapter verse counts, songbooks, songs; ordered by `pk`; `prefetch_related` so the view issues no per-row query.
- [ ] T016 [P] [US2] Write the failing E2E `test_goto_lists_without_a_request_per_query`: one index request when the projector loads, no request while typing ten queries, and no request for an empty query.
- [ ] T017 [US2] Make T016 green: rewrite `static/web/projector-library.js` `load()` to fetch `/projector/goto/index/` into the `books`/`songbooks`/`songs` shapes `lookup()` consumes; do not edit `lookup()`.
- [ ] T018 [US2] `openFind()` waits for the index: while it has not arrived the panel shows `Loading search…`, the field is disabled, the row carries the spinner; a failed index leaves that state with the row reporting the search is unavailable, and `reflow()` re-fetches the index.
- [ ] T019 [P] [US2] Write the failing E2E `test_update_finds_a_song_added_after_the_page_loaded` and make it pass through T018's `reflow()` re-fetch.

## Phase 5 — US3: choosing a result fetches it under the loading mode (P1)

- [ ] T020 [P] [US3] Write the failing server tests: `test_a_chapter_carries_both_editions_verses`, `test_an_unknown_chapter_is_not_found`, `test_a_chapter_omits_an_edition_that_lacks_it`, `test_a_song_carries_its_screens_and_baits`, `test_a_song_without_live_verses_carries_no_screens`.
- [ ] T021 [US3] Make T020 green: implement `goto.chapter` and `goto.song`, reusing `_line_pairs` for the song grouping and the `TB`-first label rule.
- [ ] T022 [P] [US3] Write the failing E2E `test_a_selection_locks_the_panel_until_the_content_paints`: during a throttled fetch the field is disabled, the chosen row is `is-loading` with its spinner, Escape and the dismiss overlay do nothing, no key or click changes the screen, and the chapter paints at the end.
- [ ] T023 [US3] Make T022 green: `detour(row)` returns a promise that fetches the chapter or song and maps it to the existing detour shape; `openDetour()` awaits it between `beginGotoLoad()` and `endGotoLoad()`; the guard at the top of `keydown` and the early returns in the mouse-zone, cue, row and dismiss handlers respect `gotoBusy`.
- [ ] T024 [US3] Add the error state: a failed fetch ends the lock, re-enables the field, puts `Could not load — try again` in the suggestion slot and removes the corner spinner (`tests/e2e/test_projector.py::test_a_failed_selection_restores_the_panel`).
- [ ] T025 [P] [US3] Write the failing E2E `test_choosing_a_passage_paints_the_chapter`, `test_choosing_a_song_paints_its_baits`, `test_the_translation_flip_makes_no_request`; make them green through T023.

## Phase 6 — US4: chapter and book navigation shares the loading mode (P2)

- [ ] T026 [P] [US4] Write the failing E2E `test_a_verse_step_inside_a_chapter_makes_no_request` and `test_a_chapter_crossing_locks_the_cue_and_paints_the_next_chapter` (asserting the corner spinner's rect is left of `.keys` and its centre level), `test_a_previous_chapter_crossing_locks_and_paints`, `test_a_book_change_locks_and_paints_the_first_chapter`.
- [ ] T027 [US4] Make T026 green: `movePassage()` resolves inside the loaded chapter from the chapter payload and returns a fetch request when it leaves it; `requestPassage()`/`detourStep()`/`detourBoundary()` await it under the same lock.

## Phase 7 — US5: the matcher keeps its rules (P2)

- [ ] T028 [P] [US5] Keep the matcher's existing tests (`test_goto_bare_number_matches_substrings_across_books_in_tiers`, `test_goto_cycles_one_suggestion_through_all_reference_results`, `test_goto_empty_result_and_overlay_dismissal`, `test_goto_accepts_tb_and_sim_book_abbreviations`) and make them pass against the fetched index.
- [ ] T029 [US5] Add the parity test `test_goto_returns_the_same_rows_as_the_saved_library_did`: a fixture library, a fixed query list, the labels and order pinned.
- [ ] T030 [P] [US5] Add `test_goto_title_fragment_caps_at_twelve_rows`.

## Phase 8 — Polish

- [ ] T031 [P] Docs: rewrite `docs/ARCHITECTURE.md`'s offline section to the online-only boundary and the Go To fetch. `docs/PRODUCT.md` carries no offline promise (grepped, 2026-10-26) — no edit there.
- [ ] T032 [P] Write `docs/adr/0007-remove-the-offline-library.md` (decision, reasons, supersedes 0003) and mark 0003 superseded in `docs/adr/README.md`.
- [ ] T033 Run the slice's suites: `multimedia.web.tests`, `tests.e2e.test_projector`, `tests.e2e.test_navigation_freshness`, `tests.e2e.test_pdf_display`, `tests.e2e.test_powerpoint_display` (targeted; the full matrix belongs to the push step).
- [ ] T034 Rebuild the preview and re-run its probe after the code lands; update `## UI/UX` in `spec.md` if a measured number moved.
- [ ] T035 [P] Converge against the traceability table; write `converge.md`.
- [ ] T036 Fold: `docs/spec/reading.md` removes R2, R5 and R3's saved-copy scenario; `docs/spec/projector.md` opens with R1 (Go To fetches on selection under the loading mode); write `fold.md`.
- [ ] T037 Board and release: ITEM-146 `In progress` → `In review` (with the PR number) → `Done` before the merge; `VERSION` 1.21.0; `CHANGELOG.md` under `## [Unreleased]` — one `Removed` line (the saved offline copy) and one `Added` line (Go To fetches on selection).
- [ ] T038 First commit at Fold: the spec pack, the code, the board row and card, the capability delta, `VERSION` and the changelog, all with the suite green. Nothing is pushed.
