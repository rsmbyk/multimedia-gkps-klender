# reading

**capability**: `reading`
**last folded**: 2026-10-24
**slices**: `126-songbook-short-header`

The public reading surfaces: the search-first shell, Alkitab, Kidung, and Tata Ibadah — what each page shows
in its header, title, stage and sidebars, and what the saved copy of a page must show before the online update
replaces it.

**This file starts at spec 126.** No capability tree existed while specs 001–125 landed, so the requirements
they shipped are not folded here; they live in their dated slice records under `specs/` and are folded as a
slice touches them. `R<n>` is stable within this file and is never reused or renumbered.

### R1 — A song page's header cites its songbook by its short name

The song route's header (`.read__eyebrow`, above the title) SHALL name a hymn-book song by its songbook's
short name and the song's number — `PKJ 4` — never by the songbook's full name. A song of an ordinary
(non-hymn) songbook SHALL show that songbook's full name, because its songs carry no numbers and the name is
the whole citation.

#### Scenario: hymn song with a short name
- WHEN `/songs/<id>/` opens for a song of a hymn songbook with a short name
- THEN the header reads `PKJ 4` (short name, a space, the number, the sub-number uppercased)

#### Scenario: sub-number
- WHEN the song carries a sub-number (`number=24`, `sub_number='a'`)
- THEN the header reads `KJ 24A`

#### Scenario: songbook without a short name
- WHEN the hymn songbook's short name is empty
- THEN the header reads the full songbook name followed by the number, never a bare number

#### Scenario: unnumbered hymn song
- WHEN a hymn book holds a song with no number
- THEN the header reads the songbook's short name alone, with no trailing space

#### Scenario: ordinary songbook
- WHEN the song belongs to a songbook that is not a hymn book, with or without a short name set
- THEN the header reads that songbook's full name

#### Scenario: the tab follows the header
- WHEN a song page opens
- THEN the document title reads `<header> — GKPS Klender`

### R2 — A saved reading page shows its server route's header and title

A reading page built from the synced library by `static/web/offline-render.js` SHALL show the same header
text and the same document title as the server route it mirrors, so the page does not change under the
operator when the online update arrives.

#### Scenario: saved song page, hymn songbook
- WHEN a hymn song is rendered from the saved library
- THEN the saved header and title equal the server page's for that song

#### Scenario: saved song page, ordinary songbook
- WHEN a song of an ordinary songbook is rendered from the saved library
- THEN the saved header and title equal the server page's, which is the songbook's full name

#### Scenario: offline
- WHEN the saved render is the final page because the network is unavailable
- THEN it carries the same header it would have shown online
