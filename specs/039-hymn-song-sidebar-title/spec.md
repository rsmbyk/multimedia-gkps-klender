# Spec 039: Show the short full title for a hymn song in the service sidebar

- **ID:** 039
- **Status:** Draft
- **Item:** ITEM-041
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

In the Tata Ibadah sidebar, a hymn song should read as its short full title — the short hymn-book
reference and the song's title, e.g. `KJ 435 Marolopolop Tondingki`.

## Scope

### In scope

- The sidebar label for a song entry from a hymn book: short reference + title.
- The sidebar filter text matching the same words.

### Out of scope

- Non-hymn songs, and the other entry kinds.
- The pane heading, unless the owner extends the scope.

## Domain rules

- **Hymn songs are short.** A song entry whose book is a hymn book labels the sidebar with
  `Song.book_number` followed by the song's title.
- **Others are unchanged.** A non-hymn song keeps its current sidebar label.
- **No title, no tail.** A hymn song with no title shows the short reference alone, with no stray
  space.
- **Still filterable.** The sidebar's filter matches the shown words.

## Acceptance scenarios

### Scenario: A hymn song in the sidebar

- **Given** a Tata Ibadah with a song entry from a hymn book, numbered 435, titled
  "Marolopolop Tondingki", with short name "KJ"
- **Then** the sidebar row reads `KJ 435 Marolopolop Tondingki`

### Scenario: A non-hymn song

- **Given** a song entry from a non-hymn songbook
- **Then** its sidebar label is unchanged

### Scenario: A title-less hymn song

- **Given** a hymn song with no title
- **Then** the sidebar row shows the short reference alone

### Scenario: Filtering

- **Given** the sidebar filter
- **When** I type part of the short full title
- **Then** the row matches

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: N/A (covered by the domain tests).
- Implementation: `multimedia/web/reading/views.py` (reusing `Song.book_number`,
  `multimedia/songs/models.py`).
- Amends: spec 006 (a song entry's sidebar label).
