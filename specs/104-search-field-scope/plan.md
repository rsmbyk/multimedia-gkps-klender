# Plan 104: Restrict the search page to the listed content fields

- **Status:** Accepted (owner, 2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-104
- **Bump:** patch

## Why

Owner request, restated: the search page must only match verse texts and titles; song titles;
song lyrics; tataibadah titles; entry titles; text entries text.

The page currently renders the shared matcher (`search(query)`) — the same function the projector
Go To uses for free-text fallbacks. It matches all of this (verified by probes against the local
copy of production data):

| Corpus | Match source today | Where | Page verdict |
| --- | --- | --- | --- |
| Alkitab | `Verse.text`, `Verse.title` | `_bible_hits` criteria + body/title | **keep** |
| Alkitab | book row via names/aliases/translation names | `_bible_hits` book loop (216–226) | not in the page matcher |
| Alkitab | `abbr · title` meta (exact + all-words) | `_entry`/`_match_score` meta channels | not in the page matcher (display stays) |
| Alkitab | reference row | `_bible_reference`, inserted at 1000 (258–261) | not in the page matcher; `search()` keeps it for the Go To |
| Kidung | `Song.title`, `songs.Verse.lyric` | `_song_hits` criteria/scoring | **keep** |
| Kidung | `book.name`/`book.short_name` criteria + `lookup_meta` substring | 277–288, 315 | not in the page matcher — the flood: `Kidung Jemaat` → 812 songs |
| Kidung | digits branch (`number__icontains`) | 280–281 | not in the page matcher — `152` → 4 songs today |
| Kidung | songbook row | `_song_hits` book loop (267–276) | not in the page matcher |
| Kidung | reference resolution (`_SONG_REF_RE` + `refs` exact) | 291–302, 316 | not in the page matcher — owner, 2026-10-17: `KJ 152` / `Kidung Jemaat 152` / `HAL 411` must list no song |
| Tatib | `TataIbadah.name` | `_tatib_hits` (329) | **keep** |
| Tatib | legacy `TataIbadahItem.title`/`text` (text kind) | 327–328, 343–344, 356–359 | **keep** |
| Tatib | service date exact; row section label | `_entry` meta channels; 347–348, 355, 358 | not in the page matcher (display stays) |
| Tatib | `ServiceEntry.title` / text-kind `text` | — | **add** — today nothing; `if not items: continue` (345) also hides entry-only services from name matches |
| Tatib | EOS notes, section breaks | 344, spec 038 | stay out |

Owner corrections (2026-10-17):

- The songbook reference form is out — `Kidung Jemaat 152` must list no hymn; songs match by
  title or lyrics only.
- Bible references are out too — `Matius 5:13` / `Matius 5` / `Yoh 3:16` list no passage; only the
  six listed fields match ("only the fields i mentioned").
- The Go To is frozen — "do not touch anything on goto. only search page". So `search()`,
  `projector_lookup`, and `projector-library.js` are not edited at all, and the page gets its own
  matcher (`search_page()`) instead of changing the shared one. That also removes the earlier idea
  of filtering reference rows inside `SearchView`. The owner confirmed the split (2026-10-17:
  "separate the goto and search page search() function to avoid future conflicts or bugs").
- The home hint goes entirely — both of its examples are references that list nothing, and the
  owner wants no helper line rather than a replacement ("just remove the home hint").

Two renderers serve the same page: `reading.js` paints the saved copy first when the library is
ready and then refreshes from the server, so both matchers must carry the same field set or the
page changes under the reader. `search_page()` is the page's only server matcher; `search()` stays
as the frozen Go To fallback and keeps its book rows, songbook references, meta tiers, and
reference insert — none of which reach the page any more.

Evidence (live-data copy; local mirrors prod):

- `Kidung Jemaat` → songs group 814 rows (2 songbook + 812 songs); title/lyrics only: 0.
- `152` → 4 songs (number hits); title/lyrics only: 0. `KJ 152`, `Kidung Jemaat 152`, `HAL 411`
  → 1 song each today (score 200 through `refs`); title/lyrics only: 0 — after the change they
  list no song.
- `Matius 5:13` → bible 1 row, kind `reference` (score 1000); songs 0, tatib 0 — the page lists
  nothing for it after the change. `Matius 5` → bible 1 `chapter` row (+ 1 Tata Ibadah text-row
  hit, a listed field, which stays); `Yoh 3:16` → bible 1 `reference` row. `Matius` → bible 7 rows
  today: 1 `book` row and 6 `verse` rows matched by text (Matius 9:9, 10:3, 9:10, Kisah Para
  Rasul 1:13, Lukas 6:15, Markus 3:18) — after the change the 6 verses stay, the book row goes.
- Go To: `Mat 5:2` resolves today only through `search()`'s reference insert —
  `_projector_chapter_prefix('Mat 5:2')` and `_entry_song_reference_filter('Mat 5:2')` both
  return None (probed). Leaving `search()` untouched keeps that behavior and its tests green.
- Service 142 `Ibadah Minggu` (3 entries, 0 legacy rows) is absent from `Ibadah Minggu` (80
  rows), `Votum` (56), `bangkit berdiri` (21), `dikuduskanlah` (7). Re-run these four as the A/B
  delta.
- 124 of 129 active services live on legacy rows; both row models must keep matching.
- The hint literal `Try Yoh 3:16 or HAL 411` lives in one template line (`base.html:343`), two
  selectors in `components.css` (831, 835–836), and six assertions
  (`tests.py::test_home_is_search_first`; `test_reading.py`: 229, 267, 285, 1651, 1657).

## Scope / edges

**In:**

- `multimedia/web/reading/search.py`: a new `search_page()` built on the six fields — verse
  text/title, song title/lyrics, service name, row title and text-entry body — with its own
  title/body scoring (the ladder minus meta and `refs`), entry rows indexed, and no book,
  songbook, or reference rows. `search()`, `_entry`, `_match_score`, `_bible_hits`, `_song_hits`,
  `_tatib_hits`, and `_bible_reference` are left as they are for the Go To's fallback.
- `multimedia/web/reading/views.py` `SearchView`: calls `search_page()` instead of `search()`.
- `static/web/offline-render.js` `searchPage()`: the same match set — book/songbook rows, the
  verse label/alias bump, and the song reference bump all go.
- The home hint line: removed — element and CSS rule go; the six assertions that pin it become
  absence checks.
- Tests: `search_page()` negatives/positives, one served-page E2E walk, one saved-copy parity E2E.

**Out:**

- The legacy `search()` and every projector path — code, behavior, and tests untouched.
- The `offline.py` payload/schema (the stored rows already carry every matched field); models and
  migrations.
- Row markup, groups, counts, excerpts, `shown` paging, CSS (beyond deleting the dead hint rule).
- The editor pickers and the legacy `/api` search endpoint.

## Approach

1. **Create `search_page()`** beside `search()`, sharing only the harmless helpers
   (`normalize`, `bible_book_index`, the date formatters). Build its rows on the six fields:
   - Alkitab: verse criteria on `text`/`title` only; one row per verse, TB preferred as today;
   - Kidung: criteria on `title | live-verse lyric` only; no songbook loop, no digits branch, no
     `_SONG_REF_RE`;
   - Tata Ibadah: service names, legacy text rows, and — new — `ServiceEntry.title` plus
     text-kind `ServiceEntry.text`; prefetch `service_entries` beside `tataibadahitem_set`; the
     guard becomes "has a legacy text row or a non-break entry"; entry rows reuse the item-row
     shape (`lookup_title=entry.title or ''`, `body=entry.text` for text entries, target
     `{'tatib_id': ..., 'item_order': f'e{entry.pk}'}`); keep `distinct()`;
   - no book rows, no songbook rows, no `_bible_reference` insert, and no meta/`refs` scoring.
     Score title and body only (200/120/95/35/16, same ladder); the display meta is built but
     never scored.
2. **Index entries** so an entry-only service lists under its own name and each entry lists under
   its title/body (the defect measured in the spec).
3. **Point `SearchView` at it.** One-line change: `results = search_page(query)`. No filtering in
   the view; counts, paging, and empty groups keep working off the returned groups. Spec 105 will
   change this function's parser and ranking, not its fields.
4. **`offline-render.js` `searchPage()` to parity.** Delete the book-row and songbook-row `add()`
   calls, the verse label/alias bump (544), and the song `reference`/`longRef` bump (560–561) —
   no references list anything on the saved copy. Score title + body only (`score()` drops its meta
   channels): verse rows on `verse.title` + `verse.text` (the label stays display-only), song rows
   on `song.title` + joined lyrics, service rows on the name + joined public rows (the existing
   filter already drops EOS notes and breaks; the date leaves scoring). Where the display title is
   not the match title (verse rows), score the match title explicitly.
5. **Remove the home hint.** Delete the `<p class="search-home__hint">` line from `base.html:343`;
   delete the `.search-home__hint` rule (`components.css:831`) and the `.search-home__hint` half
   of the paired `[data-home="results"]` selector (`components.css:835–836`); flip the six
   assertions to `search-home__hint` absence checks (`tests.py::test_home_is_search_first`;
   `test_reading.py`: 229, 267, 285, 1651, 1657).
6. **Tests first at every step**: page-matcher unit red → `search_page()` green; parity red →
   `offline-render.js` green; E2E red → green. The hint's absence checks fail while the element is
   still there, so they lead its removal.
7. **Docs and housekeeping**: split `search.py`'s module docstring — `search()` is the Go To's
   frozen fallback, `search_page()` is the page's matcher and the one this spec governs; fill
   Traceability; VERSION, changelog, ITEM-104, and the board in the implementation PR (patch).

## TDD

- Page matcher tests: `tests/test_web_search.py` — a new `search_page()` class: negatives (Bible
  references `Matius 5:13` / `Matius 5` / `Yoh 3:16`; songbook name; bare number; songbook
  references `KJ 152` / `Kidung Jemaat 152` / `HAL 411`; book name; date; section label; song-entry
  body under Tata Ibadah) and positives (verse text/title, song title/lyric, service name, entry
  title, text-entry body, entry-only service listed; an entry row links `#ti-e<pk>`). The legacy
  `search()` pins stay green untouched — that is the Go To's contract.
- App tests: `multimedia/web/tests.py` — the served page lists no reference/book/songbook row
  (`test_search_page_resolves_bible_reference` flips to a no-row negative); song-hits grouping,
  short-query, and deleted song/verse pins stay green.
- E2E: `tests/e2e/test_reading.py` — one search walk on the served page (no excluded matches, no
  reference row; an entry row opens its service); `test_search_resolves_bible_reference` becomes a
  no-row walk, and `test_bible_edition_preference_returns_after_unavailable_chapter` stops
  navigating by reference (panel clicks). `tests/e2e/test_offline_library.py` — the saved-copy
  parity walk over the same queries.
- Go To: `tests/e2e/test_projector.py`, the `multimedia/web/tests.py` lookup tests, and the legacy
  `tests/test_web_search.py` pins must pass with no code and no test change.

## Risks

- **Two matchers.** `search()` stays frozen for the Go To and `search_page()` serves the page;
  helpers may be shared but behavior must not. The untouched Go-To tests are the guard, and the
  docstring says which is which.
- **Parity** — the saved copy paints first; both page renderers must carry the same field set. The
  parity E2E is the real acceptance proof.
- **Legacy stay matchable** — 124 of 129 services are legacy rows; entries join them, never
  replace them.
- **Existing tests may encode removed behavior** — update deliberately, attributing each changed
  assertion to an excluded field or the entry addition. The reviewed search-page pins (`waktu
  pagi`, `kasih`, `di`) contain no reference query and stay green; `Matius 5:13` flips to a no-row
  negative (`multimedia/web/tests.py:84`, `tests/e2e/test_reading.py:240`), and the
  edition-preference walk (910/917) navigates by panel instead. The hint's six literal assertions
  flip to absence checks.
- **Join duplication** — criteria spanning `tataibadahitem` and `service_entries` multiplies
  rows; keep `distinct()` and prefetches, and watch the baseline queries' counts.
