# Spec 104: Restrict the search page to the listed content fields

- **ID:** 104
- **Status:** Draft
- **Item:** ITEM-104
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The owner restricts what a query may match on the public search page: a verse's text or title, a
song's title or lyrics, a service's title, a row's title, and a text row's body. Nothing else —
no book or songbook names, no song numbers, no translation codes, no dates, no section labels.

Two defects motivate it, measured against the live-data copy:

- Container-name matching floods results: `Kidung Jemaat` returns 814 song rows today — 2 songbook
  rows and 812 songs matched only because they belong to that songbook.
- Entry rows are not indexed at all: the service `Ibadah Minggu` (three entries, no legacy rows)
  never appears for `Ibadah Minggu`, `Votum`, `bangkit berdiri`, or `dikuduskanlah`, while its
  legacy-item neighbours do. A service built only from entries is invisible even under its own
  name.

This amends the field coverage of accepted spec 004; grouping, ranking mechanics, the shell, and
reference resolution are unchanged.

## Scope

### In scope

- The match set of the public search page, server (`multimedia/web/reading/search.py`) and
  saved-copy (`static/web/offline-render.js` `searchPage()`) — one contract for both.
- Indexing service entries: entry titles, text-entry bodies, and listing services that carry only
  entries.
- Removing out-of-scope match sources: Bible book names/aliases/translation codes, songbook
  names/codes, bare song numbers, service dates, row section labels, and the meta tier of the
  ranking ladder.

### Out of scope

- Reference resolution (`Matius 5`, `Matius 5:13`, `Yoh 3:16`, `KJ 152`, `Kidung Jemaat 152`,
  `HAL 411`) — not a field match; keeps working exactly as today and ranks first.
- The look: groups, row shapes, counts, excerpts, `shown` paging, and the clear control do not
  change. No preview is presented.
- The offline library's payload (`offline.py`) and sync — the stored rows already carry every
  matched field; no model or migration changes.
- The projector's Go To find (shares the matcher but consumes references and strong title hits,
  which survive), the editor pickers, and the legacy `/api` search endpoint.

## Domain rules

A query matches only these fields:

- **Alkitab** — `Verse.text` and `Verse.title`, both translations, one hit per verse as today.
- **Kidung** — `Song.title` and the lyrics of live verses (`songs.Verse.lyric`).
- **Tata Ibadah — services** — `TataIbadah.name`; a service is listed while it has at least one
  public row: a legacy text row, or an entry other than a section break.
- **Tata Ibadah — rows** — a legacy text row's `title` and `text`; an entry's `title` and, for
  text entries only, its `text` body.

These stop matching (their display is untouched):

- Bible book names, aliases, translation names, and codes: `Matius` yields no book row; `TB`/`SIM`
  are labels only — a verse matches through its text or title, never through its code.
- Songbook names and short names: `Kidung Jemaat` and `KJ` match only where a title or lyric
  itself contains them; no songbook row.
- Song numbers: `152` alone matches no song.
- Service dates and the `Template` label.
- Row section labels (`Ibadah Minggu · Section 2`).
- End-of-section notes stay unindexed (spec 004 rule); section breaks match nothing — they show
  no label (spec 038), so there is no title to find.
- Passage and song entries: not matched by their computed citation or their rendered body.

Reference resolution is unchanged and is not a field match: a whole query that is a Bible
reference or a songbook name/code plus a number resolves to that passage or song
(`Matius 5:13` → the verse; `KJ 152` and `Kidung Jemaat 152` → the same song) and ranks first.

The ranking ladder survives minus its meta tier: exact title or reference (200), prefix (120),
title substring (95), body (35), all words across title and body (16). Meta strings — translation
code, citation, date, section label — no longer score at any tier; they stay visible.

An untitled row keeps the `{service.name} · Section {n}` fallback, numbered in the service's
shared row order (legacy rows and entries interleaved as the contents pane orders them).

The saved-copy renderer applies this same match set, so a query's groups hold the same rows in
the saved copy as after the server refresh.

## UI details

The look does not change, so no new preview is presented: the same three groups and row shapes
render; only which rows match changes. Entry rows reuse the item-row shape and link to their
anchor (`#ti-e<pk>`); legacy rows keep `#ti-<order>`.

## Acceptance scenarios

### Scenario: A songbook name stops matching its songs

- **Given** the live library (812 Kidung Jemaat songs)
- **When** I search `Kidung Jemaat`
- **Then** no songbook row appears, and no song is listed for merely belonging to that
  songbook — only songs whose own title or lyrics contain the words

### Scenario: A bare song number stops matching, the reference still resolves

- **When** I search `152`
- **Then** the songs group lists no song
- **When** I search `KJ 152` or `Kidung Jemaat 152`
- **Then** the same single song resolves first, exactly as today

### Scenario: Bible references keep resolving, book names stop

- **When** I search `Matius 5:13`, `Matius 5`, or `Yoh 3:16`
- **Then** the reference resolves first as today
- **When** I search `Matius`
- **Then** no book row appears, while verses whose text or title contain it still match

### Scenario: Verse texts and titles still match

- **Given** a verse whose text (or title) contains the phrase
- **When** I search it
- **Then** the verse row appears, exactly as today

### Scenario: Song titles and lyrics still match

- **Given** the song `Di Waktu Pagi` and a phrase from a lyric line
- **When** I search either
- **Then** the song is listed under Kidung

### Scenario: Entry titles and text-entry bodies match

- **Given** the entry-only service `Ibadah Minggu` with its text entry `Votum` (`Marilah kita
  bangkit berdiri…`)
- **When** I search `Votum`, `bangkit berdiri`, or `Ibadah Minggu`
- **Then** the service and its rows are found, and the entry row links to the entry's anchor
  (`#ti-e<pk>`)

### Scenario: Out-of-scope matches stay out

- **Given** the same service, a dated service, and a service holding a song entry
- **When** I search its date (`4 Okt 2026`), a section label, the song entry's lyric, or an
  end-of-section note's text
- **Then** no service or row is listed for those reasons

### Scenario: The saved copy matches after a refresh

- **Given** the offline library is ready
- **When** I repeat the queries above on the saved-copy renderer
- **Then** its groups hold the same rows as the server-rendered page

## Traceability

- Domain/app tests: `multimedia/web/tests.py` — planned negatives
  `test_search_ignores_songbook_names_and_numbers`, `test_search_ignores_bible_book_names`,
  `test_search_ignores_service_dates_and_section_labels`,
  `test_search_ignores_non_text_entry_bodies`; planned positives
  `test_search_matches_service_entry_titles_and_text`,
  `test_search_lists_an_entry_only_service_by_its_name`; the existing search-page pins (song-hits
  grouping, bible reference, short queries, deleted song/verse hidden) stay green.
- E2E: `tests/e2e/test_reading.py` — planned `test_search_matches_only_the_listed_fields`;
  `tests/e2e/test_offline_library.py` — planned `test_saved_copy_search_matches_the_same_fields`.
- Implementation: `multimedia/web/reading/search.py` (`_entry`, `_match_score`, `_bible_hits`,
  `_song_hits`, `_tatib_hits`), `static/web/offline-render.js` (`searchPage()`).
