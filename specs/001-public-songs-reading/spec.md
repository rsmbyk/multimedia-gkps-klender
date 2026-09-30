# Spec: Public song reading + design foundation

- **ID:** 001
- **Status:** Draft
- **Item:** ITEM-001
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Make the website worth opening outside a livestream. This slice gives it a real visual language
and a public song-reading experience — browse the songbooks, read a song's lyrics, search — on the
existing Django stack.

## Scope

### In scope

- Design foundation (base template, tokens, components) used by the public pages.
- Public song reading: home, book index, song list, song detail.
- Server-side song search.
- `/manage/` editor relocation with redirects from legacy paths.

### Out of scope

- Bible reading; editor/operator redesign; authentication; offline; UI translation.

## Domain rules

- A `Book` belongs to a `Language`, has a `name`, an optional `short_name`, and `is_hymn_book`.
  Books are listed **hymn books first**, then by name, then language.
- A `Song` has `number`, `sub_number`, `title`, `is_untitled`, and `key`, plus a computed
  `book_number` (`"<short_name> <number><sub_number>"`).
- A `Verse` has `number` and `lyric`, ordered by number.
- Search matches **song title** or **book number** fragments, case-insensitive.
- Reading is **public** (no login).

## Acceptance scenarios

### Scenario: Home shows search and books

- **Given** songs exist across books
- **When** I open `/`
- **Then** I see a search field and the list of books (hymn books first)
- **And** each book links to its song list

### Scenario: Browse a book's songs

- **Given** a book with songs
- **When** I open `/songs/<book_id>/`
- **Then** I see the book's songs with their book number, title, and key
- **And** each song links to its song page

### Scenario: Read a song

- **Given** a song with verses
- **When** I open `/songs/<song_id>/`
- **Then** I see the song header (book number, title, key) and its lyrics as a readable, numbered
  column
- **And** I can move to the previous/next song in the same book

### Scenario: Search songs

- **Given** songs exist
- **When** I enter a query in the home search
- **Then** I see matching songs (by title or book number), case-insensitive
- **And** an empty query returns the default (no results) state

### Scenario: Unknown ids

- **Given** the site is running
- **When** I open a song or book URL with an unknown id
- **Then** I get a 404 response

### Scenario: Editor relocation

- **Given** the editor previously lived at `/songs/...`
- **When** I open a legacy editor URL (`/songs/books`, `/songs/books/<id>`, `/songs/songs/<id>`)
- **Then** I am redirected to the matching `/manage/...` URL
- **And** the editor itself is served under `/manage/`

### Scenario: Reading works without JavaScript

- **Given** JavaScript is disabled
- **When** I open a public reading page
- **Then** the content (books, songs, lyrics) is present in the server-rendered HTML
- **And** the page does not require Fomantic for layout or legibility

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (Django test runner, `python manage.py test`)
- E2E: not yet chosen (deferred; see plan risks)
- Implementation: `multimedia/web/...`, `multimedia/web/templates/...`,
  `multimedia/web/static/web/...`, `static/...`
