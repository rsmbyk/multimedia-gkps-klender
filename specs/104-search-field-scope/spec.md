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
no book or songbook names, no Bible references, no song numbers or songbook references, no
translation codes, no dates, no section labels.

Three defects motivate it, measured against the live-data copy:

- Container-name matching floods results: `Kidung Jemaat` returns 814 song rows today — 2 songbook
  rows and 812 songs matched only because they belong to that songbook.
- References list content none of the listed fields contains: `KJ 152`, `Kidung Jemaat 152`, and
  `HAL 411` each return the hymn, and `Matius 5:13` / `Matius 5` return the passage, today (owner,
  2026-10-17 — none of them may list anything; a song matches by title or lyrics only, a verse by
  text or title only).
- Entry rows are not indexed at all: the service `Ibadah Minggu` (three entries, no legacy rows)
  never appears for `Ibadah Minggu`, `Votum`, `bangkit berdiri`, or `dikuduskanlah`, while its
  legacy-item neighbours do. A service built only from entries is invisible even under its own
  name.

This amends the field coverage of accepted spec 004; grouping, ranking mechanics, and the shell
are unchanged. No reference lists anything on the search page, and the home hint goes with them
(owner, 2026-10-17; see UI details). The projector's Go To is not part of this spec and does not
change (owner, 2026-10-17).

## Scope

### In scope

- The match set of the public search page — the server page (`multimedia/web/reading/search.py`
  plus the page's own `SearchView` grouping) and the saved copy (`static/web/offline-render.js`
  `searchPage()`) — one contract for both.
- Indexing service entries: entry titles, text-entry bodies, and listing services that carry only
  entries.
- Removing out-of-scope match sources from the page: Bible book names/aliases/translation codes,
  songbook names/codes, bare song numbers and songbook references (`KJ 152`, `Kidung Jemaat 152`,
  `HAL 411`), service dates, row section labels, and the meta and reference tiers of the ranking
  ladder.
- Listing no reference row: the page drops the Bible reference row the shared matcher still builds
  for the Go To, and the saved copy stops scoring its label/alias bump.
- The home hint `Try Yoh 3:16 or HAL 411`: removed entirely — its element and CSS rule go, and
  its six assertions become absence checks. Both of its examples are references that list
  nothing, and the owner wants no helper line.

### Out of scope

- The projector's Go To — untouched (owner, 2026-10-17: "do not touch anything on goto. only
  search page"). Its `KJ 152` / `NKB 2`-style and numeric finds resolve in `projector_lookup`
  itself before the shared matcher (views.py:1124–1153), and its `Mat 5:2`-style finds keep
  reading the matcher's Bible reference row — which is exactly why that row stays in `search()`
  and only the page drops it. No projector code, behavior, or test change.
- The look: groups, row shapes, counts, excerpts, `shown` paging, and the clear control do not
  change; the hint's removal is a one-line subtraction the owner asked for. No preview is
  presented.
- The offline library's payload (`offline.py`) and sync — the stored rows already carry every
  matched field; no model or migration changes.
- The editor pickers (the song picker keeps its own `<book> <number>` reference filter) and the
  legacy `/api` search endpoint.

## Domain rules

A query matches only these fields:

- **Alkitab** — `Verse.text` and `Verse.title`, both translations, one hit per verse as today.
- **Kidung** — `Song.title` and the lyrics of live verses (`songs.Verse.lyric`).
- **Tata Ibadah — services** — `TataIbadah.name`; a service is listed while it has at least one
  public row: a legacy text row, or an entry other than a section break.
- **Tata Ibadah — rows** — a legacy text row's `title` and `text`; an entry's `title` and, for
  text entries only, its `text` body.

These list nothing on the search page (their display is untouched):

- Bible book names, aliases, translation names, and codes: `Matius` lists no book row; `TB`/`SIM`
  are labels only — a verse matches through its text or title, never through its code.
- Bible references: `Matius 5`, `Matius 5:13`, `Matius 5:13-14`, and `Yoh 3:16` list no passage —
  a verse matches only through its text or its title.
- Songbook names and short names: `Kidung Jemaat` and `KJ` match only where a title or lyric
  itself contains them; no songbook row.
- Song numbers and songbook references: `152`, `KJ 152`, `Kidung Jemaat 152`, and `HAL 411` list
  no song — a song matches only through its title or lyrics.
- Service dates and the `Template` label.
- Row section labels (`Ibadah Minggu · Section 2`).
- End-of-section notes stay unindexed (spec 004 rule); section breaks match nothing — they show
  no label (spec 038), so there is no title to find.
- Passage and song entries: not matched by their computed citation or their rendered body.

No reference row is listed: a whole query that is a Bible reference (`Matius 5:13` → no verse;
`Matius 5` → no chapter) or a songbook reference (`KJ 152`, `Kidung Jemaat 152` → no song) lists
nothing on the page — a query matches only through the fields above. The shared matcher still
builds the Bible reference row, because the Go To's lookup fallback reads it (Out of scope); the
page drops `reference`/`chapter` rows before grouping, and the saved copy never scores the
label/alias bump. Songbook references leave at the source instead, because the Go To resolves
those itself before the matcher.

The ranking ladder survives minus its meta channels and its reference tier: exact title (200),
prefix (120), title substring (95), body (35), all words across title and body (16). Meta strings
— translation code, citation, date, section label — and the song `refs` list no longer score at
any tier; they stay visible. The hardcoded reference row (score 1000) never reaches the page.

An untitled row keeps the `{service.name} · Section {n}` fallback, numbered in the service's
shared row order (legacy rows and entries interleaved as the contents pane orders them).

The saved-copy renderer applies this same match set, so no excluded field produces a match in the
saved copy and the listed fields match there too.

## UI details

The look does not change beyond the home hint's removal (below), so no new preview is presented:
the same three groups and row shapes render; only which rows match changes. Entry rows reuse the
item-row shape and link to their anchor (`#ti-e<pk>`); legacy rows keep `#ti-<order>`.

- **Home hint:** removed (owner, 2026-10-17). The `<p class="search-home__hint">` line leaves
  `multimedia/web/templates/reading/base.html` (line 343); its rule leaves
  `static/styles/design/components.css` (`.search-home__hint` at 831, plus the `.search-home__hint`
  half of the paired `[data-home="results"]` selector at 835–836); its six assertions become
  absence checks. Nothing replaces it.

## Acceptance scenarios

### Scenario: A songbook name stops matching its songs

- **Given** the live library (812 Kidung Jemaat songs)
- **When** I search `Kidung Jemaat`
- **Then** no songbook row appears, and no song is listed for merely belonging to that
  songbook — only songs whose own title or lyrics contain the words

### Scenario: Songbook numbers and references list no song

- **When** I search `152`, `KJ 152`, `Kidung Jemaat 152`, or `HAL 411`
- **Then** the songs group lists no song — a song matches only through its title or lyrics

### Scenario: Bible references and book names list nothing

- **When** I search `Matius 5:13`, `Matius 5`, or `Yoh 3:16`
- **Then** no passage and no book row appears — a verse is listed only when its text or title
  contains the query
- **When** I search `Matius`
- **Then** no book row appears, while verses whose text or title contain it still match

### Scenario: The home shows no helper line

- **Given** the landing home
- **When** it renders
- **Then** no `search-home__hint` line appears under the field, and the logo, field, clear
  control, and rail are unchanged

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

### Scenario: Out-of-scope matches list nothing

- **Given** the same service, a dated service, and a service holding a song entry
- **When** I search its date (`4 Okt 2026`), a section label, the song entry's lyric, or an
  end-of-section note's text
- **Then** no service or row is listed for those reasons

### Scenario: The saved copy lists nothing extra after a refresh

- **Given** the offline library is ready
- **When** I repeat the queries above on the saved-copy renderer
- **Then** no excluded field produces a match in its groups, and the listed fields (titles,
  lyrics, text-row bodies) match there too

### Scenario: The Go To is unchanged

- **Given** the projector's Go To find
- **When** I type `Mat 5:2`, `KJ 152`, or a bare number
- **Then** the passage and the hymn are offered exactly as today — no projector code, behavior,
  or test changes with this spec

## Traceability

- Domain/app tests: `multimedia/web/tests.py` — planned negatives
  `test_search_ignores_songbook_names_and_numbers`, `test_search_ignores_bible_book_names`,
  `test_search_ignores_bible_references`,
  `test_search_ignores_service_dates_and_section_labels`,
  `test_search_ignores_non_text_entry_bodies`; planned positives
  `test_search_matches_service_entry_titles_and_text`,
  `test_search_lists_an_entry_only_service_by_its_name`; the existing song-hits grouping, short
  queries, and deleted song/verse pins stay green, while
  `test_search_page_resolves_bible_reference` flips to a no-row negative.
- Matcher tests: `tests/test_web_search.py` — `test_bible_book_name_row` and
  `test_song_reference_full_name_equals_abbreviation` flip to no-match negatives; the
  `test_bible_reference_*` pins stay green, because they pin the row the Go To's lookup fallback
  reads — the page drops it, the matcher keeps it (Out of scope).
- E2E: `tests/e2e/test_reading.py` — planned `test_search_matches_only_the_listed_fields`;
  `test_search_resolves_bible_reference` flips to a no-row walk and
  `test_bible_edition_preference_returns_after_unavailable_chapter` stops navigating by
  reference (panel clicks); `tests/e2e/test_offline_library.py` — planned
  `test_saved_copy_search_matches_the_same_fields`.
- Go To: untouched — `tests/e2e/test_projector.py` and the projector-lookup tests in
  `multimedia/web/tests.py` pass with no code or test change (the guard that the narrowing never
  reaches that path).
- Home hint: the element and its CSS rule are removed; its six assertions —
  `multimedia/web/tests.py::test_home_is_search_first` and five `tests/e2e/test_reading.py` sites
  (229, 267, 285, 1651, 1657) — become `search-home__hint` absence checks.
- Implementation: `multimedia/web/reading/search.py` (`_entry`, `_match_score`, `_bible_hits`,
  `_song_hits`, `_tatib_hits`), `multimedia/web/reading/views.py` (`SearchView`'s reference-row
  drop), `static/web/offline-render.js` (`searchPage()`),
  `multimedia/web/templates/reading/base.html`, `static/styles/design/components.css`.
