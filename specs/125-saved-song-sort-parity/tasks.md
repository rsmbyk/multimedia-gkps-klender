# Tasks: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Plan**: `specs/125-saved-song-sort-parity/plan.md`
**Verification split**: 13 test · 1 inspection · 0 manual

## Phase 1 — Setup

- [ ] T001 [P] [US2] Add `test_saved_song_pages_match_the_server_sort_control` to
      `tests/e2e/test_saved_render_parity.py` (`SavedRenderParityTests`): for a hymn song, an ordinary song,
      a hymn book and an ordinary book route, compare `#songSort.hidden` between
      `GKPSOfflineRender.render(url)` and a `no-store` fetch of the same route, and compare
      `#songFilter`'s placeholder alongside. Red today: the saved hymn song route reports
      `hidden=false` where the server reports `hidden=true` (measured 2026-10-24 on
      `/songs/<hymn song>/`, four hymn songbooks in the library). *(FR-001, FR-003, FR-004, SC-002,
      SC-003, US2/AC1, US2/AC3)*
- [ ] T002 [P] [US1] Add `test_hymn_song_sidebar_open_never_paints_the_sort_control` to the same class:
      install a `requestAnimationFrame` sampler recording `#songSort`'s `hidden` and rendered width and
      `#songFilter`'s width, then click home → Kidung → the hymn songbook → its first song with the library
      synced and the network on; assert no sample ever had the control visible and that the filter width
      never changed. Then repeat the path with the context offline and assert the settled control is
      hidden. Red today: the sampler records the control at 38 px, `hidden=false`, for about 220 ms
      (`#songFilter` 293 px inside that window, 339 px outside it). *(FR-002, SC-001, US1/AC1, US1/AC2)*

## Phase 2 — Foundational

- [ ] T003 `n/a — nothing is shared beyond Phase 1's pins; both tests ride the class's existing fixtures and its library-sync helper.`

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: opening a hymn-book song from the sidebar never paints the sort control.
**Independent test**: T002 alone.

- [ ] T004 [US1] In `static/web/offline-render.js` `songPage()`, pass `!book.is_hymn_book` instead of
      `true` as `common()`'s `songListOpen` argument, with a comment naming the server rule
      (`show_song_sort = not book.is_hymn_book`, spec 011). No other caller changes. *(FR-001–FR-003)*
- [ ] T005 [US1] Re-run T002 green: no visible frame, one filter width, offline settled hidden.
      *(FR-002, SC-001, US1/AC1, US1/AC2)*

## Phase 4 — US2 (P2)

**Goal**: the saved song page matches the server for this control, and nothing else moves.
**Independent test**: T001 green across the four routes.

- [ ] T006 [US2] Re-run T001 green: equal `hidden` state on the hymn song and unchanged presence on all
      four routes. *(FR-001, FR-003, FR-004, SC-002, SC-003, US1/AC3, US2/AC1)*
- [ ] T007 [US2] Inspect `listPage()`'s existing rule (`#songSort.hidden = … || selected.is_hymn_book`) —
      no edit expected — and re-run `tests.e2e.test_saved_render_parity` and
      `tests.e2e.test_offline_library` unchanged. *(FR-005, US2/AC2)*

## Phase 5 — Polish

- [ ] T008 Write `backlog/items/ITEM-126-saved-song-sort-parity.md`, its `backlog/board.md` row, and the
      `specs/README.md` index row. (`ITEM-125` is held by the Bible-edition slice on its own branch.)
- [ ] T009 Bump `VERSION` with a patch and add the `CHANGELOG.md` entry under `[Unreleased]` → Fixed
      (take develop's current number at merge time; the neighbouring slice bumps the same level).
- [ ] T010 Tick this list, fill `analysis.md`'s dispositions, and open the draft PR with the repository's
      body template once the owner asks to push, linking the spec.

## Phase N+1 — Convergence

- [ ] T011 [Converge] Re-read the spec against the shipped code: confirm FR-005 by re-running the class's
      field comparison over every route in its list, and record the pass in `converge.md`.
