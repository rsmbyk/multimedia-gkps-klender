# Convergence — Keep reading views current after sidebar edits

## Pass 1 — 2026-10-26

**What was checked**: every row of `plan.md`'s traceability table, each by the method it declares. The
focused browser module ran first (`tests.e2e.test_sidebar_save_freshness`, 7 tests), then the repository
fast lane (`manage.py test --exclude-tag=e2e`, 506 tests) after `collectstatic` supplied the manifest the
template tests need, then every `manual` row and SC in the live preview
(`specs/134-sidebar-save-freshness/preview/run_preview.sh`, disposable SQLite on `127.0.0.1:8770`,
1440×900), then the `inspection` row by reading `static/web/editors.js`.

| Requirement | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001, FR-004, US1/AC1–AC3, Edge — active records and preserved shell state | test | `::test_tatib_sidebar_save_refreshes_row_and_active_stage`, `::test_song_sidebar_save_refreshes_row_and_active_stage`, `::test_songbook_sidebar_save_refreshes_row_heading_and_title`, `::test_sidebar_save_preserves_filter_pane_scroll_and_focus` — green; each asserts the row text, the stage heading, `performance.timeOrigin` unchanged, and (last case) filter values, `data-nav=closed`, `data-ch=open`, both scroll offsets and focus on the saved row | met |
| FR-002, US1/AC4 — Kidung edit with a Bible stage | manual | Preview `/bible/1/1/`, Kidung selected, songbook edited to `Preview Songbook — Renamed`: row shows the new name, `#readName` stays `Matius`, the verse stays, URL unchanged, `data-nav=open`, `data-ch=open`, `#bookFilter` still `Preview`, one visible row, `document.activeElement` = the updated row (`book row-flash focus-restore-quiet`, so no pointer outline) | met |
| FR-003, US2/AC1–AC2 — matching and non-matching search result | test | `::test_search_result_edit_keeps_matching_song_and_updates_counts`, `::test_search_result_edit_removes_nonmatching_song_and_updates_counts` — green; the first also walks back through history and finds the new title, not the snapshot's old HTML | met |
| FR-005, Edge — rejected save | inspection | `editors.js` dispatches `editor:saved` only inside the success branch after `response.ok` and a JSON object (lines 216–224); `400` replaces the form HTML and returns, `403` throws, and the `catch` announces the failure without dispatching or touching reading values | met |
| FR-006, Edge — service-entry edit in an open Tata Ibadah | manual | Preview `/tatib/1/`, entry text changed to `Preview entry content — updated in place`: the stage shows the new text in place and the contents list keeps its `Opening` row; no reload, no sidebar rebuild | met |
| SC-001 — no stale representation | manual | Preview `/tatib/1/`: row, `#readName` and tab all `Preview Tata Ibadah — After`; `/songs/1/`: row and `#readName` `Preview Song — After`, tab stays `Preview Songbook — Updated — Multimedia GKPS Klender`; songbook edit on the same page: row and `#chTitle` updated; selection (`aria-current`) kept on the edited record in both sidebars | met |
| SC-002 — search settles on the current match state | manual | Preview `/search?q=Preview`: renaming to `Preview Song — Still Matching` leaves `1 result` with the new title, query `Preview` and URL unchanged; renaming to `Renamed Away` drops the songs group (the server page for that query carries none) with the query and page still in place; no reload | met |
| SC-003 — unrelated stage and browsing state survive | manual | The FR-002 preview row above: chapter, route, pane states, filter, scroll and quiet focus all survive the save | met |
| US2/AC1–AC2 | test | FR-003's two cases | met |

**Typed gaps**

- `missing` — none.
- `partial` — none.
- `contradicts` — one, and it was **spec at fault**: US1/AC2 asked the browser tab to show a saved song
  title, while `reading` R1 gives a song page the header-derived title (its songbook citation), so the
  clause could only be met by breaking R1 and making the saved view differ from a reloaded one. Asked
  through the question tool; the owner kept R1 and the scenario was amended in place with its earlier
  wording kept as superseded, together with a Clarifications entry. FR-002 now reads *the document title
  that route renders*, and `::test_song_sidebar_save_refreshes_row_and_active_stage` asserts the
  header-derived title. No code gap remains.
- `unrequested` — none. The save path and the offline saved-copy paint share one refresh branch, so the
  paint was given `backgroundRefresh: true` (the flag the codebase already uses for work that must not
  move the operator's shell); the saved copy still replaces the screen without touching panes, filters,
  scroll or the search snapshot, which is what the branch it replaced did. The refresh focus restore now
  skips the `deferFocus` path, so a deleted row still hands focus to its neighbour through `entries.js`
  as before.

**Outcome**: converged on pass 1. No open task, no requirement resting on nothing.

**Push-step evidence — the full matrix** is deferred to the owner's push word, as the previous slices did:
this repository has no CI, so the full `manage.py test` (all browser modules) is a manual run before the
merge. The pre-existing reds this work already knows about are carded — ITEM-137 (songbook empty-view
copy), ITEM-139 (three offline projector cases), ITEM-140 (projector display-off), ITEM-141 (bible edition
preference) — and are identical on the base this branch was cut from.
