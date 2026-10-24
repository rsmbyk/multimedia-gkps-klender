# Tasks: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Plan**: `specs/125-saved-song-sort-parity/plan.md`
**Verification split**: 13 test · 1 inspection · 0 manual

## Phase 1 — Setup

- [x] T001 [P] [US2] Add `test_saved_song_pages_match_the_server_sort_control` to
      `tests/e2e/test_saved_render_parity.py` (`SavedRenderParityTests`): for a hymn song, an ordinary song,
      a hymn book and an ordinary book route, compare `#songSort.hidden` between
      `GKPSOfflineRender.render(url)` and a `no-store` fetch of the same route, and compare
      `#songFilter`'s placeholder alongside. **Red against develop**: the saved hymn song route reports
      `hidden=false` where the server reports `hidden=true` (`AssertionError: False != True` on
      `/songs/2077/`, 2026-10-24). *(FR-001, FR-003, FR-004, SC-002, SC-003, US2/AC1, US2/AC3)*
- [x] T002 [P] [US1] Add `test_hymn_song_sidebar_open_never_paints_the_sort_control` to the same class:
      install a `requestAnimationFrame` sampler recording `#songSort`'s `hidden` and rendered width and
      `#songFilter`'s width, then click home → Kidung → the hymn songbook → its first song with the library
      synced and the network on; assert no sample ever had the control visible and that the filter width
      never changed on that route. Then repeat the path with the context offline and assert the settled
      control is hidden. **Red against develop**: the sampler recorded seven frames with `hidden=false`,
      `sortWidth=38`, `filterWidth=293` on `/songs/2079/` (2026-10-24). *(FR-002, SC-001, US1/AC1,
      US1/AC2)*

## Phase 2 — Foundational

- [x] T003 `n/a — nothing is shared beyond Phase 1's pins; both tests ride the class's existing fixtures and its library-sync helper.`

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: opening a hymn-book song from the sidebar never paints the sort control.
**Independent test**: T002 alone.

- [x] T004 [US1] In `static/web/offline-render.js` `songPage()`, pass `!book.is_hymn_book` instead of
      `true` as `common()`'s `songListOpen` argument, with a comment naming the server rule
      (`show_song_sort = not book.is_hymn_book`, spec 011). No other caller changes. *(FR-001–FR-003)*
- [x] T005 [US1] Re-run T002 green: no visible frame, one filter width on the song route, offline settled
      hidden. *(FR-002, SC-001, US1/AC1, US1/AC2)*

## Phase 4 — US2 (P2)

**Goal**: the saved song page matches the server for this control, and nothing else moves.
**Independent test**: T001 green across the four routes.

- [x] T006 [US2] Re-run T001 green: equal `hidden` state on the hymn song and unchanged presence on all
      four routes. *(FR-001, FR-003, FR-004, SC-002, SC-003, US1/AC3, US2/AC1)*
- [x] T007 [US2] Inspect `listPage()`'s existing rule (`#songSort.hidden = … || selected.is_hymn_book`) —
      unchanged, as expected — and re-run `tests.e2e.test_saved_render_parity` plus the saved-sidebar and
      non-hymn-row classes of `tests.e2e.test_offline_library`: 7 tests green. *(FR-005, US2/AC2)*

## Phase 5 — Polish

- [x] T008 Write `backlog/items/ITEM-126-saved-song-sort-parity.md` and its `backlog/board.md` row. The
      `specs/README.md` index stopped at spec 101 twenty slices ago, so it is left as found rather than
      given a single row after a long gap (`analysis.md` A5). (`ITEM-125` is held by the Bible-edition
      slice on its own branch.)
- [x] T009 Bump `VERSION` 1.20.2 → 1.20.3 and add the `CHANGELOG.md` entry under `[Unreleased]` → Fixed.
- [x] T010 Tick this list and fill `analysis.md`'s dispositions.

## Phase N+1 — Convergence

- [x] T011 [Converge] Re-read the spec against the shipped code and re-run the class's field comparison
      over every route in its list; recorded in `converge.md` pass 1 — one `partial` gap on FR-004, fixed
      as T013.
- [x] T013 [Converge] Add `sortHidden` to the `fields()` map of
      `test_saved_reading_routes_match_server_fields`, so the fifteen routes it covers compare the control
      too; class green (5 tests). *(FR-004)*
- [x] T012 Open the draft PR with the repository's body template, record the URL on the card, and move
      it to `In review`. *(draft PR [#374](https://github.com/rsmbyk/multimedia-gkps-klender/pull/374))*
