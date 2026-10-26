# Converge — remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Date**: 2026-10-26

## Pass 1

**Checked**: the traceability table against the code and the tests that ran during Implement;
`lookup()` compared with the base revision; every removed route; the index's byte budget measured
against the real database.

| Row | Result | Evidence |
| --- | --- | --- |
| FR-001 | converged | `reading.js`'s `navigate()` has one paint path; `tests.e2e.test_navigation_freshness` green (2 tests) |
| FR-002 | converged | cleanup block in `reading.js` + `projector-library.js`; `test_the_page_leaves_no_browser_storage` green |
| FR-003 | converged | `base.html` has no offline control; `test_the_reading_shell_carries_no_offline_control` green |
| FR-004 | converged | `multimedia.web.tests.ProjectorGotoPayloadTests.test_the_offline_routes_are_gone` green |
| FR-005 | converged | `test_goto_lists_without_a_request_per_query` green |
| FR-006 | converged | `test_the_index_carries_no_verse_text_or_lyric` green |
| FR-007 | converged | the Go To suite green — `test_projector`'s 63 tests, run as 60 + the 3 crossing/flip tests |
| FR-008 | converged | `lookup()` body compared byte-for-byte with `HEAD:static/web/projector-library.js`: **identical** (2,959 chars) |
| FR-009 | converged | `test_choosing_a_passage…`, the song/bait tests, and the detour tests green |
| FR-010 | converged | `test_a_selection_locks_the_panel_until_the_content_paints` green |
| FR-011 | converged | verse-step (local) and chapter-crossing (fetch + cue spinner geometry) tests green |
| FR-012 | converged | `test_an_empty_service_shows_its_empty_state` green; `grep -rn GKPSOffline static/` empty |
| SC-001–SC-007 | converged | each is the criterion of a green test above; SC-005 measured **101,883 bytes** on this database against the 130 KB budget |

**Findings**

| ID | Type | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | **contradicts** (code at fault) | `load()` cached its resolved promise, so the page's `Update` re-ran the index fetch through a stale promise and a song added mid-service was never findable — US2.5 would have failed silently. | Fixed: `refresh()` clears the cache and re-fetches; `reflow()` calls it. `test_update_finds_a_song_added_after_the_page_loaded` green. |
| C2 | partial | The index encoded chapters positionally (`counts[i]` = chapter `i+1`); a book whose chapters do not start at 1 was described wrongly. Found by an E2E fixture, not by the spec. | Fixed: `[chapter, verse count]` pairs. `data-model.md` and `contracts/projector-goto.md` updated; the server test asserts the pair form. |
| C3 | partial | Song rows as objects pushed the index to 173,712 bytes, over SC-005. | Fixed: rows are `[id, songbook id, number, sub-number, title]`; measured 101,883 bytes. |
| C4 | unrequested? (no) | Two projector display tests asserted the removed `/offline/chunk/service/<pk>/` request. The behaviour they protect — the display re-reads its service after a save or reorder — survives. | Retargeted to `/projector?service=<pk>`; both green. |
| C5 | partial | The E2E Bible fixture gave a chapter only verse 3, which the real database never does (measured: every chapter runs 1..N). | Fixture now follows the invariant; one assertion moved from `Matius 5:3` to `Matius 5:1`. |

No `missing` row, no `contradicts` remaining, no accepted gap. Pass 1 converged.

**Observation, not a gap**: `specs/README.md`'s index has no row for spec 134 or 135, so it stopped
being maintained before this slice. Left as found; backfilling it is an owner-requested pass, not part
of this slice.

## Outcome

**Converged at pass 1** — 2 findings were code defects fixed inside the pass (C1, C2), one a budget
defect (C3), one a test pin on a removed transport (C4), one a fixture that described impossible data
(C5). Nothing was deferred.
