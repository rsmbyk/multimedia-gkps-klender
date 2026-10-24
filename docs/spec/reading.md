# reading

**capability**: `reading`
**last folded**: 2026-10-24
**slices**: `126-songbook-short-header`, `127-site-name-tab`, `128-songbook-hymn-separator`

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
- THEN the document title reads `<header> — Multimedia GKPS Klender`

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

### R3 — The tab names the site, and the index's tab stops at the name

Every reading page's document title SHALL name the site `Multimedia GKPS Klender` — the product name the
rest of the application already uses. The index SHALL read that name alone: the site root, the temporary
home, and the search route opened with no query, which all render the search-first landing. Every other
reading page SHALL keep the leading text it carries today and append ` — Multimedia GKPS Klender`.

The page's visible and assistive text is outside this requirement: headings, the search field's accessible
name, the logo's `alt` and the rail's labels keep the congregation name `GKPS Klender`.

#### Scenario: the index
- WHEN `/`, `/home/`, or `/search` with no query opens
- THEN the document title is exactly `Multimedia GKPS Klender`, with nothing after it

#### Scenario: a reading page
- WHEN a Bible chapter, song, Tata Ibadah service, section landing, results page or the Media Library opens
- THEN the document title is its leading text followed by ` — Multimedia GKPS Klender`

#### Scenario: the saved copy
- WHEN a route is rendered from the saved library before the online update arrives
- THEN its document title is the server page's own, name included

#### Scenario: an in-place edition switch
- WHEN the Bible edition changes without a navigation
- THEN the title becomes `<book name> <chapter> — Multimedia GKPS Klender`, so the tab does not rename
  itself while the edition does

### R4 — The Kidung panel puts hymn books first, then the ordinary songbooks A–Z, behind one separator

The Kidung panel SHALL list hymn songbooks before ordinary songbooks. Hymn songbooks SHALL keep the accepted
panel order — descending count of their non-deleted songs, the name breaking a tie. Ordinary songbooks SHALL
be ordered by their case- and diacritic-folded name, compared ordinally, with the original name breaking an
exact tie, so the order does not depend on the database's collation or the browser's locale data.

One separator SHALL be drawn between the two groups, and it SHALL be the panel's own group rule
(`2px solid var(--divider)`, `10px` margin and `10px` padding), not a new element. Neither group carries a
heading, label or caption. A group with no rows — because no songbook of that kind exists, or because the
panel filter emptied it — SHALL draw no separator.

An empty panel SHALL say so: when no group has rows — no songbook exists, or the filter matches neither —
the panel shows its empty view, on first load as well as after filtering. While one group still has rows,
only that group shows: no separator, no empty view.

The grouping and order SHALL be the same on the Kidung index, a songbook page and a song page, and the
current row and the per-row edit button SHALL stay on the rows they marked before.

#### Scenario: the panel
- WHEN `/songs/` opens
- THEN every hymn songbook precedes every ordinary songbook, with one separator between them and no heading

#### Scenario: the ordinary side
- WHEN the ordinary songbooks are listed
- THEN they read A–Z by their folded names, `Buku Ende HKBP` among the `b`s, a case-only pair broken by the
  original name

#### Scenario: an emptied group
- WHEN the panel filter leaves one group with no rows
- THEN no separator is drawn above the surviving group

#### Scenario: an empty panel
- WHEN `/songs/` opens with no active songbook, or the filter matches no row in either group
- THEN the panel body holds no group and the empty view reads “No matching songbooks.”

### R5 — A saved Kidung panel draws the same two groups

A Kidung page rendered from the saved library by `static/web/offline-render.js` SHALL draw the same two groups,
in the same order, as the server route it mirrors — the same hymn order and the same folded A–Z key — so the
panel does not reorder itself when the online update arrives.

#### Scenario: saved panel
- WHEN a Kidung route is rendered from the saved library
- THEN its panel's group count and row order equal the server page's
