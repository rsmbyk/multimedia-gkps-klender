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
| Alkitab | reference resolution | `_bible_reference`, inserted at 1000 (258–261) | keep — resolution, not a field |
| Kidung | `Song.title`, `songs.Verse.lyric` | `_song_hits` criteria/scoring | **keep** |
| Kidung | `book.name`/`book.short_name` criteria + `lookup_meta` substring | 277–288, 315 | drop — the flood: `Kidung Jemaat` → 812 songs |
| Kidung | digits branch (`number__icontains`) | 280–281 | drop — `152` → 4 songs today |
| Kidung | songbook row | `_song_hits` book loop (267–276) | drop |
| Kidung | reference resolution (`_SONG_REF_RE` + `refs` exact) | 291–302, 316 | keep |
| Tatib | `TataIbadah.name` | `_tatib_hits` (329) | **keep** |
| Tatib | legacy `TataIbadahItem.title`/`text` (text kind) | 327–328, 343–344, 356–359 | **keep** |
| Tatib | service date exact; row section label | `_entry` meta channels; 347–348, 355, 358 | drop (display stays) |
| Tatib | `ServiceEntry.title` / text-kind `text` | — | **add** — today nothing; `if not items: continue` (345) also hides entry-only services from name matches |
| Tatib | EOS notes, section breaks | 344, spec 038 | stay out |

Two renderers serve the same page: `reading.js` paints the saved copy first when the library is
ready and then refreshes from the server, so both matchers must carry the same field set or the
page changes under the reader. `projector_lookup` (`views.py:1154`) also calls
`search_lib.search()`; it consumes references and ≥95 title hits, which the narrowing keeps.

Evidence (live-data copy; local mirrors prod):

- `Kidung Jemaat` → songs group 814 rows (2 songbook + 812 songs); title/lyrics only: 0.
- `152` → 4 songs (number hits); title/lyrics only: 0.
- Service 142 `Ibadah Minggu` (3 entries, 0 legacy rows) is absent from `Ibadah Minggu` (80
  rows), `Votum` (56), `bangkit berdiri` (21), `dikuduskanlah` (7). Re-run these four as the A/B
  delta.
- 124 of 129 active services live on legacy rows; both row models must keep matching.

## Scope / edges

**In:**

- `multimedia/web/reading/search.py`: the per-corpus match set above, entries indexed, meta
  channels out of scoring, the ladder minus its meta tier.
- `static/web/offline-render.js` `searchPage()`: the same match set.
- Tests: unit negatives/positives, one served-page E2E walk, one saved-copy parity E2E.

**Out:**

- Reference resolution; the `offline.py` payload/schema (the stored rows already carry every
  matched field); models and migrations.
- Row markup, groups, counts, excerpts, `shown` paging, CSS.
- The projector Go To, editor pickers, the legacy `/api` search endpoint.

## Approach

1. **Make the meta channels display-only** — `_entry()` keeps `meta` for display but stops
   storing/feeding `lookup_meta`/`lookup_meta_exact`, and `_match_score()` drops the meta tier
   (exact/substring) and the meta fields from the all-words `combined`. The ladder is then exact
   title or `refs` (200), prefix (120), substring (95), body (35), all-words over title and body
   (16). Bible references are inserted at a hardcoded 1000 and song references ride `refs`, so
   neither depends on the removed channels.
2. **Narrow each corpus in `search.py`.**
   - `_bible_hits`: delete the book-row loop; the verse path is already text/title-only.
   - `_song_hits`: criteria become `title | live-verse lyric` (drop `book__name`,
     `book__short_name`, the digits branch); delete the songbook loop; scoring keeps title, body,
     and `refs`; `_SONG_REF_RE` id resolution stays.
   - `_tatib_hits`: criteria gain `service_entries__title` and text-kind `service_entries__text`;
     prefetch `service_entries` beside `tataibadahitem_set`; the guard becomes "has a legacy text
     row or a non-break entry"; append entry rows in the item-row shape
     (`lookup_title=entry.title or ''`, `body=entry.text` for text entries, target
     `{'tatib_id': ..., 'item_order': f'e{entry.pk}'}`); the date and section labels stop
     scoring. Keep `distinct()`; the criteria now span two relations.
3. **`offline-render.js` `searchPage()` to parity.** Delete the book-row and songbook-row `add()`
   calls; rank verse rows from `verse.title` + `verse.text` (keep the label/alias exact bump),
   song rows from `song.title` + joined lyrics (keep the `reference`/`longRef` exact bump), and
   service rows from the name + joined public rows (the existing filter already drops EOS notes
   and breaks; the date leaves scoring). The displayed meta stays; callers that must not score it
   compute the rank across permitted fields and pass it.
4. **Tests first at every step**: unit red → `search.py` green; parity red → `offline-render.js`
   green; E2E red → green.
5. **Docs and housekeeping**: refresh `search.py`'s module docstring (it still promises "book
   names and aliases"); fill Traceability; VERSION, changelog, ITEM-104, and the board in the
   implementation PR (patch).

## TDD

- Domain/app tests: `multimedia/web/tests.py` — negatives (songbook name, bare number, book name,
  date, section label, song-entry body under Tata Ibadah) and positives (verse text/title, song
  title/lyric, service name, entry title, text-entry body, entry-only service listed; an entry
  row links `#ti-e<pk>`).
- E2E: `tests/e2e/test_reading.py` — one search walk on the served page (no excluded matches;
  `Matius 5:13` still first; an entry row opens its service). `tests/e2e/test_offline_library.py`
  — the saved-copy parity walk over the same queries.

## Risks

- **Parity** — the saved copy paints first; both matchers must carry the same field set. The
  parity E2E is the real acceptance proof.
- **Legacy stay matchable** — 124 of 129 services are legacy rows; entries join them, never
  replace them.
- **Go To shares the matcher** — projector tests must stay green; its tiers (references, ≥95
  title hits) survive by design.
- **Existing tests may encode removed behavior** — update deliberately, attributing each changed
  assertion to an excluded field or the entry addition.
- **Join duplication** — criteria spanning `tataibadahitem` and `service_entries` multiplies
  rows; keep `distinct()` and prefetches, and watch the baseline queries' counts.
