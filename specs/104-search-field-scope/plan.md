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
| Alkitab | reference resolution | `_bible_reference`, inserted at 1000 (258–261) | drop — owner, 2026-10-17: `Matius 5:13` / `Matius 5` / `Yoh 3:16` return no passage; the helper stays for the Go To |
| Kidung | `Song.title`, `songs.Verse.lyric` | `_song_hits` criteria/scoring | **keep** |
| Kidung | `book.name`/`book.short_name` criteria + `lookup_meta` substring | 277–288, 315 | drop — the flood: `Kidung Jemaat` → 812 songs |
| Kidung | digits branch (`number__icontains`) | 280–281 | drop — `152` → 4 songs today |
| Kidung | songbook row | `_song_hits` book loop (267–276) | drop |
| Kidung | reference resolution (`_SONG_REF_RE` + `refs` exact) | 291–302, 316 | drop — owner, 2026-10-17: `KJ 152` / `Kidung Jemaat 152` / `HAL 411` must return no song |
| Tatib | `TataIbadah.name` | `_tatib_hits` (329) | **keep** |
| Tatib | legacy `TataIbadahItem.title`/`text` (text kind) | 327–328, 343–344, 356–359 | **keep** |
| Tatib | service date exact; row section label | `_entry` meta channels; 347–348, 355, 358 | drop (display stays) |
| Tatib | `ServiceEntry.title` / text-kind `text` | — | **add** — today nothing; `if not items: continue` (345) also hides entry-only services from name matches |
| Tatib | EOS notes, section breaks | 344, spec 038 | stay out |

Owner corrections (2026-10-17):

- The songbook reference form is out — `Kidung Jemaat 152` must not return the hymn; songs match
  by title or lyrics only.
- Bible references are out too — `Matius 5:13` / `Matius 5` / `Yoh 3:16` resolve to no passage;
  only the six listed fields match ("only the fields i mentioned"). The Go To keeps its own
  reference finds.
- The home hint goes entirely — both of its examples are references that stop resolving, and the
  owner wants no helper line rather than a replacement ("just remove the home hint").

Two renderers serve the same page: `reading.js` paints the saved copy first when the library is
ready and then refreshes from the server, so both matchers must carry the same field set or the
page changes under the reader. `projector_lookup` resolves `KJ 152` / `NKB 2`-style and numeric
finds itself before `search_lib.search()` is reached (`views.py:1124–1153`); with the reference
tier leaving `search()`, its `Mat 5:2`-style finds resolve through the retained helper on that
same own path (`projector_lookup` calls it before the free-text fallback) — so the projector's
behavior is unchanged.

Evidence (live-data copy; local mirrors prod):

- `Kidung Jemaat` → songs group 814 rows (2 songbook + 812 songs); title/lyrics only: 0.
- `152` → 4 songs (number hits); title/lyrics only: 0. `KJ 152`, `Kidung Jemaat 152`, `HAL 411`
  → 1 song each today (score 200 through `refs`); title/lyrics only: 0 — after the change they
  return no song.
- `Matius 5:13` → bible 1 row, kind `reference` (score 1000); songs 0, tatib 0 — after the
  change: no passage. `Matius 5` → bible 1 `chapter` row (+ 1 Tata Ibadah text-row hit, a listed
  field, which stays); `Matius 5:13` and `Yoh 3:16` have no other matches. `Matius` → bible 7
  rows today: 1 `book` row and 6 `verse` rows matched by text (Matius 9:9, 10:3, 9:10, Kisah
  Para Rasul 1:13, Lukas 6:15, Markus 3:18) — after the change the 6 verses stay, the book row
  goes.
- Go To: `Mat 5:2` resolves today only through `search()`'s reference insert —
  `_projector_chapter_prefix('Mat 5:2')` and `_entry_song_reference_filter('Mat 5:2')` both
  return None — so the endpoint must call the helper itself to keep
  `test_library_lookup_matches_bible_book_and_chapter_prefix` (web/tests.py:2369) green.
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
  `refs` channels out of scoring, the ladder minus its meta/reference tiers; the reference helper
  stays but leaves the public match path.
- `multimedia/web/reading/views.py` `projector_lookup`: resolves `Mat 5:2`-style references
  itself (the Go To keeps today's behavior).
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
- The projector Go To (resolves references on its own path), editor pickers, the legacy `/api`
  search endpoint.

## Approach

1. **Make the meta channels display-only** — `_entry()` keeps `meta` for display but stops
   storing/feeding `lookup_meta`/`lookup_meta_exact`/`refs`, and `_match_score()` drops the meta
   tier (exact/substring), the `refs` check, and the meta/`refs` fields from the all-words
   `combined`. The ladder is then exact title (200), prefix (120), substring (95), body (35),
   all-words over title and body (16). The reference insert is a hardcoded 1000 of its own — it
   goes in step 2, with the book and songbook channels.
2. **Narrow each corpus in `search.py`.**
   - `_bible_hits`: delete the book-row loop and the `_bible_reference` insert (258–261); the
     verse path is already text/title-only. Keep `_bible_reference`/`_BIBLE_REF_RE` as the Go
     To's resolver (step 3) — the search page stops calling them.
   - `_song_hits`: criteria become `title | live-verse lyric` (drop `book__name`,
     `book__short_name`, the digits branch); delete the songbook loop and the `_SONG_REF_RE` id
     resolution (291–302) with its `refs`/`lookup_meta` kwargs (315–316). Scoring keeps title and
     body; `KJ 152`-style queries select nothing.
   - `_tatib_hits`: criteria gain `service_entries__title` and text-kind `service_entries__text`;
     prefetch `service_entries` beside `tataibadahitem_set`; the guard becomes "has a legacy text
     row or a non-break entry"; append entry rows in the item-row shape
     (`lookup_title=entry.title or ''`, `body=entry.text` for text entries, target
     `{'tatib_id': ..., 'item_order': f'e{entry.pk}'}`); the date and section labels stop
     scoring. Keep `distinct()`; the criteria now span two relations.
3. **Keep the Go To's references.** `_bible_reference`/`_BIBLE_REF_RE` stay in `search.py` as the
   projector's resolver; `projector_lookup` calls the helper when `_projector_chapter_prefix` and
   `_entry_song_reference_filter` both miss, before the free-text fallback, and appends the
   passage exactly as the search rows did (`{'kind': 'passage', 'label': reference['title'],
   'target': reference['target']}`). The endpoint's behavior — `Mat 5:2`, `Matius 5:13-14`,
   `Yoh 3:16` — is unchanged, so its unit tests stay green as written.
4. **`offline-render.js` `searchPage()` to parity.** Delete the book-row and songbook-row `add()`
   calls, the verse label/alias bump (544), and the song `reference`/`longRef` bump (560–561) —
   no references resolve. Score title + body only (`score()` drops its meta channels): verse rows
   on `verse.title` + `verse.text` (the label stays display-only), song rows on `song.title` +
   joined lyrics, service rows on the name + joined public rows (the existing filter already
   drops EOS notes and breaks; the date leaves scoring). Where the display title is not the match
   title (verse rows), score the match title explicitly.
5. **Remove the home hint.** Delete the `<p class="search-home__hint">` line from `base.html:343`;
   delete the `.search-home__hint` rule (`components.css:831`) and the `.search-home__hint` half
   of the paired `[data-home="results"]` selector (`components.css:835–836`); flip the six
   assertions to `search-home__hint` absence checks (`tests.py::test_home_is_search_first`;
   `test_reading.py`: 229, 267, 285, 1651, 1657).
6. **Tests first at every step**: unit red → `search.py` green; parity red → `offline-render.js`
   green; E2E red → green. The hint's absence checks fail while the element is still there, so
   they lead its removal.
7. **Docs and housekeeping**: refresh `search.py`'s module docstring — drop "book names and
   aliases" and the `Kidung Jemaat 120`/`KJ 120` sentence and say the matcher is field-only, with
   reference resolution owned by the Go To; fill Traceability; VERSION, changelog, ITEM-104, and
   the board in the implementation PR (patch).

## TDD

- Domain/app tests: `multimedia/web/tests.py` — negatives (Bible references `Matius 5:13` /
  `Matius 5` / `Yoh 3:16`, songbook name, bare number, songbook references `KJ 152` /
  `Kidung Jemaat 152` / `HAL 411`, book name, date, section label, song-entry body under Tata
  Ibadah) and positives (verse text/title, song title/lyric, service name, entry title,
  text-entry body, entry-only service listed; an entry row links `#ti-e<pk>`). The existing
  `test_search_page_resolves_bible_reference` flips to a no-resolution negative.
- Matcher tests `tests/test_web_search.py` — the reference pins flip to no-match negatives
  (`test_bible_reference_resolves_first`, `test_bible_reference_accepts_alias_and_case`,
  `test_bible_reference_range_marks_both_verses`, `test_bible_chapter_reference`,
  `test_bible_reference_accepts_sim_abbreviation`, `test_bible_book_name_row`,
  `test_song_reference_full_name_equals_abbreviation`); verse-text, song, and Tata Ibadah pins
  stay green.
- E2E: `tests/e2e/test_reading.py` — one search walk on the served page (no excluded matches; an
  entry row opens its service); `test_search_resolves_bible_reference` becomes a no-resolution
  walk, and `test_bible_edition_preference_returns_after_unavailable_chapter` stops navigating by
  reference (panel clicks). `tests/e2e/test_offline_library.py` — the saved-copy parity walk over
  the same queries.
- Projector: `tests/e2e/test_projector.py` and the `multimedia/web/tests.py` lookup tests stay
  green with step 3 — that is the proof the narrowing never reaches those paths.
- Home hint: `tests.py::test_home_is_search_first` flips its hint assertion to an absence check on
  `search-home__hint`; the five `test_reading.py` sites (229, 267, 285, 1651, 1657) assert
  `.search-home__hint` has count 0.

## Risks

- **Parity** — the saved copy paints first; both matchers must carry the same field set. The
  parity E2E is the real acceptance proof.
- **Legacy stay matchable** — 124 of 129 services are legacy rows; entries join them, never
  replace them.
- **Go To resolves references itself** — `projector_lookup` handles `KJ 152`/`NKB 2`-style and
  numeric finds before `search()`, and must now resolve `Mat 5:2`-style references itself (step
  3) because `search()` stops inserting them. `test_projector.py` (client library) and the lookup
  unit tests (`Mat 5:2`, `Matius 5:13`) stay green — re-run them to prove the narrowing never
  reaches those paths.
- **Existing tests may encode removed behavior** — update deliberately, attributing each changed
  assertion to an excluded field or the entry addition. The reviewed search-page pins (`waktu
  pagi`, `kasih`, `di`) contain no reference query and stay green; `Matius 5:13` flips to a
  no-resolution negative (`multimedia/web/tests.py:84`, `tests/e2e/test_reading.py:240`), and the
  edition-preference walk (910/917) navigates by panel instead. The hint's six literal assertions
  flip to absence checks.
- **Join duplication** — criteria spanning `tataibadahitem` and `service_entries` multiplies
  rows; keep `distinct()` and prefetches, and watch the baseline queries' counts.
