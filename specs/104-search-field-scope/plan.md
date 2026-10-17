# Plan 104: Restrict the search page to the listed content fields

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-104
- **Bump:** patch

## Why

Owner request, restated: the search page must only match verse texts and titles; song titles;
song lyrics; tataibadah titles; entry titles; text entries text.

The current matcher, field by field (`multimedia/web/reading/search.py`, verified by probes
against the local copy of production data):

| Corpus | Match source today | Where | Verdict |
| --- | --- | --- | --- |
| Alkitab | `Verse.text`, `Verse.title` | `_bible_hits` criteria + body/title | **keep** |
| Alkitab | book row via names/aliases/translation names | `_bible_hits` book loop (216–226) | drop |
| Alkitab | `abbr · title` meta (exact + all-words) | `_entry`/`_match_score` meta channels | drop (display stays) |
| Alkitab | reference row | `_bible_reference`, inserted at 1000 (258–261) | **keep in the matcher, drop from the page** — the Go To's lookup fallback reads it (`views.py:1156–1159`) and the owner froze that surface; the page stops rendering it |
| Kidung | `Song.title`, `songs.Verse.lyric` | `_song_hits` criteria/scoring | **keep** |
| Kidung | `book.name`/`book.short_name` criteria + `lookup_meta` substring | 277–288, 315 | drop — the flood: `Kidung Jemaat` → 812 songs |
| Kidung | digits branch (`number__icontains`) | 280–281 | drop — `152` → 4 songs today |
| Kidung | songbook row | `_song_hits` book loop (267–276) | drop |
| Kidung | reference resolution (`_SONG_REF_RE` + `refs` exact) | 291–302, 316 | drop at the source — owner, 2026-10-17: `KJ 152` / `Kidung Jemaat 152` / `HAL 411` must list no song; the Go To resolves those itself before the matcher |
| Tatib | `TataIbadah.name` | `_tatib_hits` (329) | **keep** |
| Tatib | legacy `TataIbadahItem.title`/`text` (text kind) | 327–328, 343–344, 356–359 | **keep** |
| Tatib | service date exact; row section label | `_entry` meta channels; 347–348, 355, 358 | drop (display stays) |
| Tatib | `ServiceEntry.title` / text-kind `text` | — | **add** — today nothing; `if not items: continue` (345) also hides entry-only services from name matches |
| Tatib | EOS notes, section breaks | 344, spec 038 | stay out |

Owner corrections (2026-10-17):

- The songbook reference form is out — `Kidung Jemaat 152` must list no hymn; songs match by
  title or lyrics only.
- Bible references are out too — `Matius 5:13` / `Matius 5` / `Yoh 3:16` list no passage; only the
  six listed fields match ("only the fields i mentioned").
- The Go To is frozen — "do not touch anything on goto. only search page". So nothing on that path
  moves: `projector_lookup` and `projector-library.js` are not edited, and the matcher keeps
  building the Bible reference row its fallback reads. The page stops rendering it instead.
- The home hint goes entirely — both of its examples are references that list nothing, and the
  owner wants no helper line rather than a replacement ("just remove the home hint").

Two renderers serve the same page: `reading.js` paints the saved copy first when the library is
ready and then refreshes from the server, so both matchers must carry the same field set or the
page changes under the reader. The Go To (`projector_lookup`, `views.py:1118–1185`) is untouched:
it resolves `KJ 152` / `NKB 2`-style and numeric finds itself before `search_lib.search()` is
reached (`1124–1153`), and its `Mat 5:2`-style finds come from the reference row `search()` still
inserts — the row the page drops.

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
  return None (probed). That is why the insert stays: dropping it would change the Go To, and
  `test_library_lookup_matches_bible_book_and_chapter_prefix` (web/tests.py:2369) would fail.
- Service 142 `Ibadah Minggu` (3 entries, 0 legacy rows) is absent from `Ibadah Minggu` (80
  rows), `Votum` (56), `bangkit berdiri` (21), `dikuduskanlah` (7). Re-run these four as the A/B
  delta.
- 124 of 129 active services live on legacy rows; both row models must keep matching.
- The hint literal `Try Yoh 3:16 or HAL 411` lives in one template line (`base.html:343`), two
  selectors in `components.css` (831, 835–836), and six assertions
  (`tests.py::test_home_is_search_first`; `test_reading.py`: 229, 267, 285, 1651, 1657).

## Scope / edges

**In:**

- `multimedia/web/reading/search.py`: the per-corpus match set above, entries indexed, meta and
  `refs` channels out of scoring, the ladder minus its meta/reference tiers. The Bible reference
  insert stays (the Go To reads it).
- `multimedia/web/reading/views.py` `SearchView`: drops `reference`/`chapter` rows from the
  results before `_search_groups`, so counts, paging, and empty groups all follow the filtered
  rows.
- `static/web/offline-render.js` `searchPage()`: the same match set — book/songbook rows, the
  verse label/alias bump, and the song reference bump all go.
- The home hint line: removed — element and CSS rule go; the six assertions that pin it become
  absence checks.
- Tests: unit negatives/positives, the flipped matcher pins, one served-page E2E walk, one
  saved-copy parity E2E.

**Out:**

- The `offline.py` payload/schema (the stored rows already carry every matched field); models and
  migrations.
- Row markup, groups, counts, excerpts, `shown` paging, CSS (beyond deleting the dead hint rule).
- The projector Go To — code, behavior, and tests untouched (owner: "do not touch anything on
  goto") — the editor pickers, and the legacy `/api` search endpoint.

## Approach

1. **Make the meta channels display-only** — `_entry()` keeps `meta` for display but stops
   storing/feeding `lookup_meta`/`lookup_meta_exact`/`refs`, and `_match_score()` drops the meta
   tier (exact/substring), the `refs` check, and the meta/`refs` fields from the all-words
   `combined`. The ladder is then exact title (200), prefix (120), substring (95), body (35),
   all-words over title and body (16). This is the only shared-scoring change the Go To's fallback
   sees: its ≥95 filter is unaffected because meta's only ≥95 tier is the exact citation, which
   `_entry_song_reference_filter` intercepts earlier — the untouched lookup tests are the proof.
2. **Narrow each corpus in `search.py`.**
   - `_bible_hits`: delete the book-row loop only. The `_bible_reference` insert (258–261) and the
     helper stay exactly as they are: the Go To's lookup fallback reads that row, and the owner
     froze that path. The verse path is already text/title-only.
   - `_song_hits`: criteria become `title | live-verse lyric` (drop `book__name`,
     `book__short_name`, the digits branch); delete the songbook loop and the `_SONG_REF_RE` id
     resolution (291–302) with its `refs`/`lookup_meta` kwargs (315–316). Scoring keeps title and
     body; `KJ 152`-style queries select nothing. Safe for the Go To: it resolves those itself
     before `search()` is reached.
   - `_tatib_hits`: criteria gain `service_entries__title` and text-kind `service_entries__text`;
     prefetch `service_entries` beside `tataibadahitem_set`; the guard becomes "has a legacy text
     row or a non-break entry"; append entry rows in the item-row shape
     (`lookup_title=entry.title or ''`, `body=entry.text` for text entries, target
     `{'tatib_id': ..., 'item_order': f'e{entry.pk}'}`); the date and section labels stop
     scoring. Keep `distinct()`; the criteria now span two relations.
3. **Drop reference rows from the page.** In `SearchView.get_context_data`, filter
   `kind in ('reference', 'chapter')` out of `results['bible']` before `_search_groups`, with a
   comment naming the Go To as the reason the row exists. Group counts, `shown` paging, and the
   empty-group skip then follow the filtered rows; nothing else in the page path changes, and
   `projector_lookup` keeps calling `search_lib.search(query)` unchanged.
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
6. **Tests first at every step**: unit red → `search.py` green; parity red → `offline-render.js`
   green; E2E red → green. The hint's absence checks fail while the element is still there, so
   they lead its removal.
7. **Docs and housekeeping**: refresh `search.py`'s module docstring — drop "book names and
   aliases" and the `Kidung Jemaat 120`/`KJ 120` sentence and say the matcher is field-only for
   the page, with the reference row kept for the Go To; fill Traceability; VERSION, changelog,
   ITEM-104, and the board in the implementation PR (patch).

## TDD

- Domain/app tests: `multimedia/web/tests.py` — negatives (Bible references `Matius 5:13` /
  `Matius 5` / `Yoh 3:16` on the served page, songbook name, bare number, songbook references
  `KJ 152` / `Kidung Jemaat 152` / `HAL 411`, book name, date, section label, song-entry body
  under Tata Ibadah) and positives (verse text/title, song title/lyric, service name, entry title,
  text-entry body, entry-only service listed; an entry row links `#ti-e<pk>`). The existing
  `test_search_page_resolves_bible_reference` flips to a no-row negative.
- Matcher tests `tests/test_web_search.py` — `test_bible_book_name_row` and
  `test_song_reference_full_name_equals_abbreviation` flip to no-match negatives; the
  `test_bible_reference_*` pins stay green: they pin the row the Go To's fallback reads, which the
  page drops rather than the matcher.
- E2E: `tests/e2e/test_reading.py` — one search walk on the served page (no excluded matches, no
  reference row; an entry row opens its service); `test_search_resolves_bible_reference` becomes a
  no-row walk, and `test_bible_edition_preference_returns_after_unavailable_chapter` stops
  navigating by reference (panel clicks). `tests/e2e/test_offline_library.py` — the saved-copy
  parity walk over the same queries.
- Go To: `tests/e2e/test_projector.py` and the `multimedia/web/tests.py` lookup tests must pass
  with no code and no test change — that is the proof the narrowing never reaches those paths.
- Home hint: `tests.py::test_home_is_search_first` flips its hint assertion to an absence check on
  `search-home__hint`; the five `test_reading.py` sites (229, 267, 285, 1651, 1657) assert
  `.search-home__hint` has count 0.

## Risks

- **Parity** — the saved copy paints first; both page renderers must carry the same field set. The
  parity E2E is the real acceptance proof.
- **Legacy stay matchable** — 124 of 129 services are legacy rows; entries join them, never
  replace them.
- **The Go To is frozen** — `projector_lookup` and `projector-library.js` are not edited, and the
  matcher keeps the Bible reference row its fallback reads. Two things must not leak: the page's
  filter (step 3) must run before grouping, and the meta-channel removal must stay
  behavior-neutral for the ≥95 filter. `test_projector.py` plus the lookup unit tests, unmodified,
  are the guard.
- **Existing tests may encode removed behavior** — update deliberately, attributing each changed
  assertion to an excluded field or the entry addition. The reviewed search-page pins (`waktu
  pagi`, `kasih`, `di`) contain no reference query and stay green; `Matius 5:13` flips to a no-row
  negative (`multimedia/web/tests.py:84`, `tests/e2e/test_reading.py:240`), and the
  edition-preference walk (910/917) navigates by panel instead. The hint's six literal assertions
  flip to absence checks.
- **Join duplication** — criteria spanning `tataibadahitem` and `service_entries` multiplies
  rows; keep `distinct()` and prefetches, and watch the baseline queries' counts.
