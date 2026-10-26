# Implementation Plan: remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Branch**: `feat/136-remove-offline-library`
**Date**: 2026-10-26 · **Status**: Draft (gate 1 accepted the spec on 2026-10-26)
**bump**: `minor` — a user-facing capability is removed and the projector's Go To changes how its
content reaches the screen; no published API breaks. Reasoning and the rejected levels:
`research.md` D9.

## Technical Context

| | |
| --- | --- |
| Language | Python 3.12, Django 4.0 (templates + JSON views) |
| Front end | server-rendered templates, vanilla JS, hand-written CSS; no framework, no build step |
| Files | new `multimedia/web/reading/goto.py`; `multimedia/urls.py`; `multimedia/web/templates/reading/base.html`, `projector.html`, `projector_controls.html`; `static/web/projector.js`, `projector-library.js`, `reading.js`; `static/styles/design/projector.css`, `components.css`; deletes `static/web/offline-library.js`, `offline-status.js`, `offline-render.js`, `service-worker.js`, `static/styles/design/offline.css`, `multimedia/web/reading/offline.py` |
| Data | no migration; no stored value changes |
| Tests | Django `TestCase` for the three payloads and the removed routes (`multimedia/web/tests.py`); Playwright E2E through `LiveServerTestCase` for search, the lock, the chapter crossing and the empty storage (`tests/e2e/`) |
| Constraints | no new tokens, fonts, icons, dependencies or services; the two spinners reuse `.editor__loading-spinner`'s idiom |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01). No principle to check against;
nothing to justify in a Complexity Tracking table.

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

`research.md` records nine decisions with provenance and exits at zero unknowns: the removal's whole
surface (D1), the lookup staying client-side over a fetched index (D2), the index's exact-but-textless
shape and its measured 126.4 KB / 29.4 KB (D3), the chapter-or-song fetch (D4), the one-flag loading
mode and its two indicators (D5), the failure states (D6), the reading path's surviving behaviour
(D7), the tests and the ITEM-139 card (D8), and `minor` (D9).

## Phase 1 — Design artifacts

- `data-model.md` — the browser store removed, the three payloads added, the client detour shape kept.
- `contracts/projector-goto.md` — the three endpoints, the four removed routes and the loading lock.
- `quickstart.md` — the commands the slice runs, marked runnable or not yet.

## Design

### Server: `multimedia/web/reading/goto.py` (new)

Three JSON views, each `Cache-Control: no-store`, no authentication, `404` on a missing target:

- `index(request)` — books (editions with their per-chapter verse counts), songbooks, songs. One
  query per collection with `prefetch_related`, no per-row query. Serialised compactly
  (`separators=(',', ':')`): `JsonResponse`'s default separators add ~30% to a payload whose budget
  (SC-005) is measured in bytes.
- `chapter(request, book_id, chapter)` — both `TB`/`SIM` editions' verses for one chapter, plus the
  edition-neutral label. `404` when the book has no such chapter in any edition.
- `song(request, song_id)` — the song's live verses grouped into screens by `_line_pairs` and its
  bait ranges, reusing the projector's own grouping rather than a second implementation.

`multimedia/urls.py` routes them under `/projector/goto/…` and drops the four offline routes.

### Client: `projector-library.js`

- `load()` fetches `/projector/goto/index/` once, builds the same `books`/`songbooks`/`songs` shapes
  `lookup()` already consumes, and resolves a promise the page awaits; a failure rejects and the
  page stays in its index-loading state until `Update`.
- `lookup()` is untouched — the matcher keeps its rules, its scores and its order.
- `detour(row)` becomes `detour(row) → Promise`: it fetches the chapter or the song, maps the payload
  into the detour object the projector already paints, and builds each verse's `header`/`line` from
  the chapter payload.
- `movePassage()` becomes async and takes the index's chapter lists: a step inside the loaded
  chapter is resolved locally; a step that leaves it returns a request the page performs.

### Client: `projector.js`

- `openDetour(row)` awaits `detour()` under `beginGotoLoad()`; `requestPassage()` awaits
  `movePassage()` the same way. Both end in `endGotoLoad()`.
- `beginGotoLoad()` sets `gotoBusy`, disables `#projectorFindInput`, marks the chosen row
  `is-loading` with its spinner, inserts `.cue-loading` before `.keys`, and paints the row's count
  away. `endGotoLoad()` reverses it. The `keydown` handler returns at its top while `gotoBusy`; the
  mouse-zone, cue, row and dismiss handlers return likewise, and `closeFind()` refuses while busy.
- Removed: the `GKPSOffline` branch in `reflow()`, `drawSavedScreens()`, the `offline:changed`
  listener, the "not saved for offline use yet" copy, and the sync on opening the panel. `reflow()`
  re-fetches the index after the page.
- `renderDetour`, `renderDetourCue` and the step handlers keep their shape; only the data source and
  the pre-fetch paint change.

### Client: `reading.js`

- `navigate()` keeps `fromServer()` as the only path: the `GKPSOfflineRender` branch, the direct-boot
  hydration call and the offline failure copy are removed. History, focus, scroll and the search
  snapshot are untouched.

### Templates and styles

- `base.html` — remove the offline rail button, the offline panel, the `Saved copy` label, the
  `offline.css` link and the three offline script tags.
- `projector.html` — remove the `offline-library.js` tag; keep `projector-library.js`.
- `projector.css` — add `.projector-find__row.is-loading`, `.projector-find__spinner`,
  `.cue-loading`, `.projector-find input:disabled` and the `goto-load-spin` keyframes, with the
  reduced-motion rule, matching the measured numbers in the spec's `## UI/UX`.

### Removed files and routes

`static/web/offline-library.js`, `offline-status.js`, `offline-render.js`, `service-worker.js`,
`static/styles/design/offline.css`, `multimedia/web/reading/offline.py`; the four routes in
`multimedia/urls.py`; `tests/test_offline_sync.py`, `tests/e2e/test_offline_library.py`,
`tests/e2e/test_saved_render_parity.py` and the offline cases in `test_projector.py`,
`test_navigation_freshness.py`, `test_pdf_display.py`, `test_powerpoint_display.py`.

### Docs

- `docs/ARCHITECTURE.md` — replace the offline section with the online-only boundary and the Go To
  fetch.
- `docs/adr/0007-remove-the-offline-library.md` (new) — supersedes ADR 0003 with its reasons; 0003
  stays in place, marked superseded in `docs/adr/README.md`.
- `docs/PRODUCT.md` — drop any offline promise it makes (checked by grep in T001).

## Traceability

| ID | Requirement / scenario | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | a reading page paints from its own response; no saved copy first | `reading.js` `navigate()` | `test` — `tests/e2e/test_navigation_freshness.py::test_a_reading_navigation_paints_the_servers_page` |
| FR-002 | no service worker, cache entry or library database remains | `offline-library.js` deleted; `service-worker.js` deleted; page unregisters | `test` — `tests/e2e/test_projector.py::test_the_page_leaves_no_browser_storage` |
| FR-003 | the rail control, panel and `Saved copy` label are gone | `base.html` | `test` — same module, `test_the_reading_shell_carries_no_offline_control` |
| FR-004 | the four routes answer 404 | `multimedia/urls.py` | `test` — `multimedia/web/tests.py::test_the_offline_routes_are_gone` |
| FR-005 | the projector fetches the index once, in page memory | `goto.index`, `projector-library.js` `load()` | `test` — `tests/e2e/test_projector.py::test_goto_lists_without_a_request_per_query` |
| FR-006 | the index carries no paintable text | `goto.index` | `test` — `multimedia/web/tests.py::test_the_index_carries_no_verse_text_or_lyric` |
| FR-007 | queries answer from the index with today's rows, labels and order | `projector-library.js` `lookup()` | `test` — `tests/e2e/test_projector.py::test_goto_returns_the_same_rows_as_the_saved_library_did` |
| FR-008 | the matcher keeps its rules, not the page grammar | `lookup()` unchanged | `inspection` — `projector-library.js:119-180` is byte-identical apart from `load()` |
| FR-009 | a selection fetches the whole chapter or song and paints it | `goto.chapter`, `goto.song`, `detour()` | `test` — `tests/e2e/test_projector.py::test_a_verse_step_inside_a_chapter_makes_no_request` (the passage is fetched and painted by `_open_matius_5`); `::test_goto_click_opens_the_selected_suggestion` (a song) |
| FR-010 | the lock: row spinner, field disabled, close refused, keys and clicks refused | `projector.js` `beginGotoLoad()` | `test` — `tests/e2e/test_projector.py::test_a_selection_locks_the_panel_until_the_content_paints` |
| FR-011 | verse steps local; chapter/book steps fetch under the same lock | `movePassage()`, `requestPassage()` | `test` — `tests/e2e/test_projector.py::test_a_verse_step_inside_a_chapter_makes_no_request`; `::test_a_chapter_crossing_locks_the_cue_and_paints_the_next_chapter` |
| FR-012 | the projector renders from its response alone | `projector.html`, `projector.js` | `test` — `tests/e2e/test_projector.py::test_an_empty_service_shows_its_empty_state` |
| SC-001 | a session leaves nothing stored | page + routes | `test` — FR-002's test |
| SC-002 | one index request per page load, not per query | `load()` | `test` — FR-005's test counts requests |
| SC-003 | the rows equal today's for a fixed query list | `lookup()` | `test` — FR-007's test |
| SC-004 | the four routes are gone | `urls.py` | `test` — FR-004 |
| SC-005 | the index is ≤ 130 KB raw / ≤ 30 KB gzipped | `goto.index` | `test` — `multimedia/web/tests.py::test_the_index_stays_under_one_hundred_and_thirty_kilobytes` |
| SC-006 | the lock holds during a throttled fetch | `beginGotoLoad()` | `test` — FR-010's test |
| SC-007 | a navigation is one request and one paint | `navigate()` | `test` — FR-001's test |
| US1.1 | browsing leaves no worker, cache or database | page | `test` — SC-001 |
| US1.2 | a page is painted from its own response | `navigate()` | `test` — FR-001 |
| US1.3 | the rail carries no offline control | `base.html` | `test` — FR-003 |
| US1.4 | the projector reads no saved service | `projector.js` | `inspection` — no `GKPSOffline` reference remains (`grep -rn GKPSOffline static/`) |
| US1.5 | the empty state promises no saved copy | `projector.html` | `test` — FR-012 |
| US2.1 | one index request when the projector loads | `load()` | `test` — FR-005 |
| US2.2 | typing changes the suggestion with no request | `lookup()` | `test` — FR-005's request count |
| US2.3 | `G` before the index arrives is in the loading state | `openFind()`, `load()` | `test` — `tests/e2e/test_projector.py::test_goto_opened_before_the_index_shows_the_loading_state` |
| US2.4 | the index is in memory, not storage | `load()` | `test` — FR-002's storage check after a Go To query |
| US2.5 | `Update` re-fetches the index | `reflow()` | `test` — `tests/e2e/test_projector.py::test_update_finds_a_song_added_after_the_page_loaded` |
| US3.1 | choosing a passage locks, then paints | `openDetour()` | `test` — FR-009/FR-010 |
| US3.2 | choosing a song paints every bait | `detour()`, `song` | `test` — `test_goto_click_opens_the_selected_suggestion` and `multimedia/web/tests.py::test_a_song_carries_its_screens_and_baits` |
| US3.3 | the panel closes and the page regains focus on success | `closeFind()` | `manual` — choose a result on `/projector?service=144`; the panel closes and typing reaches the page |
| US3.4 | no shortcut fires while loading | `keydown` guard | `test` — FR-010 |
| US3.5 | no click changes the screen while loading | mouse zones | `test` — FR-010 |
| US3.6 | both editions are in hand, the flip makes no request | `chapter` payload | `test` — `tests/e2e/test_projector.py::test_the_translation_flip_makes_no_request`; `::test_goto_passage_translation_flip_brightens_the_label` |
| US3.7 | song bait steps make no request | `song` payload | `test` — FR-009 (song half) |
| US4.1 | a verse step inside the chapter is local | `movePassage()` | `test` — FR-011 |
| US4.2 | the last verse steps into a fetched next chapter | `requestPassage()` | `test` — FR-011 (crossing half) |
| US4.3 | the first verse steps into a fetched previous chapter | `requestPassage()` | `test` — `tests/e2e/test_projector.py::test_a_previous_chapter_crossing_locks_and_paints` |
| US4.4 | Shift/Ctrl steps and Home/End fetch under the lock | `requestPassage()` | `test` — `tests/e2e/test_projector.py::test_a_book_change_locks_and_paints_the_first_chapter`; `::test_a_chapter_crossing_locks_the_cue_and_paints_the_next_chapter` |
| US4.5 | the cue indicator sits left of the keyboard icon | `projector.css` `.cue-loading` | `test` — `::test_a_chapter_crossing_locks_the_cue_and_paints_the_next_chapter` asserts the spinner's rect |
| US5.1 | references and chapters list as today | `lookup()` | `test` — FR-007 |
| US5.2 | book abbreviations of both editions list as today | `lookup()` | `test` — FR-007 |
| US5.3 | songbook numbers list as today | `lookup()` | `test` — FR-007 |
| US5.4 | bare numbers keep today's tiers and ties | `lookup()` | `test` — `tests/e2e/test_projector.py::test_goto_bare_number_matches_substrings_across_books_in_tiers` (kept) |
| US5.5 | title fragments keep the twelve-row cap | `lookup()` | `inspection` — the `.slice(0, 12)` in the unchanged `lookup()`; the byte-identical comparison of the function against the base revision is the evidence |
| US5.6 | a query that matches nothing says so | `paintFind()` | `test` — `tests/e2e/test_projector.py::test_goto_empty_result_and_overlay_dismissal` (kept) |
| Edge | a failed selection restores the panel and says so | `endGotoLoad()`, error copy | `test` — `::test_a_failed_selection_restores_the_panel` |
| Edge | a failed index leaves the panel loading and the row reporting | `load()` | `test` — `::test_goto_opened_before_the_index_shows_the_loading_state` (failure half) |
| Edge | an empty query makes no request | `refreshFind()` | `test` — `::test_goto_lists_without_a_request_per_query` |
| Edge | a missing edition verse leaves the flip to the other edition | `chapter` payload | `test` — `multimedia/web/tests.py::test_a_chapter_omits_an_edition_that_lacks_it` |
| Edge | a song with no verses paints nothing new | `song` payload | `test` — `multimedia/web/tests.py::test_a_song_without_live_verses_carries_no_screens` |
| Edge | offline navigation shows the browser's error, no saved page | `navigate()` | `manual` — load `/home/` then disable the network and open a chapter; the browser's error page is what shows |

**Verification split: 48 test · 3 inspection · 2 manual.** Untested is allowed; unverifiable is not.

## Delivery

- Branch `feat/136-remove-offline-library`, squash into `develop`, PR body = the squash message.
- Board: ITEM-146 `Speccing` → gate 1 → `Ready` (owner) → `In progress` here → `In review` with the
  PR number → `Done` before the merge. The card's `issue:` is backfilled when the card passes
  `Speccing` — the agent creates the anchor.
- `VERSION` 1.20.14 → 1.21.0 in the pre-merge commit, with one `Removed` changelog line and one
  `Added` line under `## [Unreleased]` (Keep a Changelog's sections).
- ADRs: `0007-remove-the-offline-library.md` supersedes 0003; `docs/adr/README.md` marks it.

## Risks

- **The two matchers.** The Go To's rules must not drift toward `search_page()`'s grammar while the
  data source moves. Mitigation: `lookup()` is not edited; the parity test pins its rows.
- **The lock and the existing shortcuts.** A guard at the top of `keydown` is only correct if every
  handler that can navigate goes through it. Mitigation: the E2E test presses the navigation keys,
  Space, `K`, `J`, `G` and Escape during a throttled fetch.
- **The index's freshness.** A song added mid-service is invisible until `Update`; acceptable and
  stated, but it reverses a behaviour today's test pinned. Mitigation: `reflow()` re-fetches, and the
  test asserts that path.
- **The preview's fidelity.** The loading states are posed, not fetched (the page's script is
  stripped). Mitigation: the E2E tests are the behavioural evidence; the preview is the look.
- **A stale service worker on a returning browser.** The old worker's cache is deleted on its next
  `activate`; until then a cached shell could answer a navigation. Mitigation: the page unregisters
  the worker and the routes 404, so the stale shell cannot load the removed library scripts.
