# reading

**capability**: `reading`
**last folded**: 2026-11-14
**slices**: `190-sidebar-delete`, `189-song-verse-editing`, `188-legacy-bookmarks-to-services`, `164-dock-fluid-width`, `163-media-dialog-file-picker-cancel`, `159-preview-body-ring`, `162-song-verse-empty-state`, `151-rail-icons`, `154-audio-times-inline`, `153-preview-tabs-row`, `150-references-token-order`, `144-passage-song-icons`, `148-media-library-refresh-flicker`, `146-media-and-transfer-age-buckets`, `147-transfer-icon-column`, `145-media-size-precision`, `143-add-bar`, `142-entry-surface`, `140-stage-link-affordance`, `141-projector-window-reopen`, `139-home-search-center`, `138-sidebar-overlay-stack`, `137-reading-text-wrap`, `136-remove-offline-library`, `134-sidebar-save-freshness`, `126-songbook-short-header`, `127-site-name-tab`, `128-songbook-hymn-separator`, `129-sidebar-empty-states`, `130-empty-service-tiles`, `131-retire-break-entry`, `132-tatib-sidebar-date-buckets`, `133-text-modal-large-frame`, `135-tatib-sidebar-row-clamp`
The public reading surfaces: the search-first shell, Alkitab, Kidung, and Tata Ibadah — what each page
shows in its header, title, stage and sidebars. Every page is painted from its own server response; the
saved-copy requirements this file carried until 2026-10-26 are retired.

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

**Removed 2026-10-26 by `136-remove-offline-library`.** There is no saved copy: the browser library,
`static/web/offline-render.js` and the service worker are gone, and every page is painted from its own
server response (ADR 0007). The requirement and its scenarios described a page that no longer exists.

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

**Removed 2026-10-26 by `136-remove-offline-library`.** The saved Kidung page it constrained is gone with
the library; the server route's own grouping is R4.

### R6 — An empty Tata Ibadah quarter-centres its four add tiles

A service that holds no items and can be edited SHALL show its invitation — the heading, the hint and the
four add actions — with its centre a quarter of the way down the reading area the header leaves, not at its
middle, and never overlapping the header. The four actions SHALL be one horizontal row of square, icon-only
tiles: 52px at a full-width column, 10px apart, the glyph alone on the face, and the sentence `Add Passage`,
`Add Song`, `Add Text`, `Add Media` carried as the accessible name and the tooltip. A reading column narrower
than 300px SHALL take them three and one at full size rather than shrinking them below 44px.

The server template, the saved renderer and the rebuild that follows deleting a service's last entry SHALL
paint the same tiles. A service that holds items is outside this requirement: it keeps the header-to-body gap
and the top-aligned flow it has always had.

#### Scenario: an empty service
- WHEN a service with no items opens at any width
- THEN the block's centre sits a quarter of the way down the reading area under the header, never above it
- AND its four actions stand in one row of 52px squares, or three and one when the column is under 300px

#### Scenario: naming a tile
- WHEN a tile is hovered, focused or read by a screen reader
- THEN it is named `Add Passage`, `Add Song`, `Add Text` or `Add Media`, in that order
- AND no visible label text appears in the row

#### Scenario: the last entry deleted in place
- WHEN the only entry is deleted without a reload
- THEN the rebuilt block is the same row of tiles, in the same place

#### Scenario: the saved copy
- WHEN an empty service is rendered from the saved library
- THEN its tiles carry the same labels, one glyph each and the same square size as the server route

### R7 — A sidebar list's empty state says which nothing it is

Each of the shell's two sidebar lists SHALL show one empty-state block at a time, centred on that list's
pane — a glyph above a title above a hint — rather than a line in the pane's corner. With no rows in the
list the block SHALL carry that section's own "nothing yet" copy; with rows present but none matching the
filter it SHALL carry that list's "no matching" copy; with at least one matching row it SHALL not be shown.
The first column SHALL name its own list (books, songbooks, Tata Ibadah); the second SHALL name its
contents (songs, sections). The block is not a control: it SHALL NOT take the pointer, the wheel or focus.

The block SHALL be hidden in the collapsed mini panel and in the Bible's chapter list, where chapters are
never filtered and a book without text is a property of the edition. A page built from the saved library
SHALL carry the same copy and the same glyphs as the server route it mirrors.

#### Scenario: a list with no rows
- WHEN a Tata Ibadah has no sections, or a songbook has no songs
- THEN the block shows `No sections yet.` / `No songs yet.` with that list's invitation beneath it,
  centred on the pane

#### Scenario: a filter that matched nothing
- WHEN the list holds rows and the filter matches none of them
- THEN the block shows `No matching sections.` / `No matching songs.` under a magnifier with a cross,
  with `Try a different search.` beneath it

#### Scenario: a match, or a cleared filter
- WHEN at least one row matches, or the filter is cleared
- THEN the block is not shown

#### Scenario: a list that is both empty and filtered
- WHEN a list with no rows is filtered anyway
- THEN it keeps the "nothing yet" copy: the filter did not empty it

#### Scenario: the first column's own words
- WHEN the books, songbooks or Tata Ibadah column is filtered to nothing
- THEN its title names that column's list, never another column's

#### Scenario: the saved copy
- WHEN a route is rendered from the saved library before the online update arrives
- THEN both blocks carry the server route's copy and glyphs

#### Scenario: the collapsed panel
- WHEN the first column is collapsed to its mini rail
- THEN no block is shown

### R8 — A retired entry kind stops being offered, and what it wrote keeps working

An entry kind MAY be retired without deleting what it already wrote. A retired kind SHALL offer no creation
control on any surface — the server template, the rebuild after a deletion and the saved renderer — and the
writing endpoints SHALL refuse it with the same answer an unknown kind gets, so a stale page or a direct
request cannot create or edit one by any route. The Break kind is the first retired kind: its add row, its
empty-state tile and its edit form are gone, and `+ Break` no longer exists anywhere.

What the kind already produced SHALL keep working unchanged: an existing Break SHALL still draw its one
full-width divider on the stage and its row in the sidebar, still contribute its blank projector screen, and
still reorder by drag or keyboard and delete from its divider. Its stored kind value and its display name
SHALL be kept, because every reader — the stage, the sidebar, the projector, search and the saved page — keys
off them, and the legacy `END_OF_SECTION` row of the older table is a different shape and SHALL be untouched.

#### Scenario: no surface offers one
- WHEN a service's add rows, the start bar or an empty service's tiles are read
- THEN the offered kinds are Passage, Song, Text and Media
- AND no `+ Break` control or `Add Break` tile exists

#### Scenario: a direct request
- WHEN a save request names the retired kind, or the edit form of an existing break is asked for
- THEN the answer is `404` and nothing is created or changed

#### Scenario: an existing break
- WHEN a service holding a Break opens, projects, or is read from the saved library
- THEN the divider, its place in the order, its sidebar row and its projector screen are exactly as before
- AND its Delete still removes it and closes the order up

### R9 — The Tata Ibadah list groups by age, and today is marked

The dated Tata Ibadah list SHALL group its rows into four age buckets, in this order and under these
labels: `Upcoming` (today or later), `Last 30 days` (one to thirty days before today), `Earlier this
year` (older than thirty days and in the present calendar year) and `Older` (anything older). The present
day SHALL be the congregation's calendar day in `Asia/Jakarta`, never the server's UTC date. A bucket
holding no rows SHALL draw neither a heading nor a separator, and the buckets kept SHALL stay in the order
above.

Inside `Upcoming`, rows dated today SHALL come first and the remaining future rows SHALL follow farthest
date first; every other bucket SHALL list its newest date first. Within one date, rows SHALL break ties on
creation time, newest first.

A row dated today SHALL carry a `Today` badge between its name and its date, and no other row SHALL carry
one; the badge SHALL be drawn on the action accent (`--active-bg` fill with `--active-ink` ink), and the
row's accessible name SHALL end `— today`.

The operator dock's picker SHALL group by the same four buckets, in the same order and under the same
labels, and SHALL mark today with the same badge. It SHALL NOT tint a row for being today or for being
upcoming: the bucket heading carries the age, and the badge carries the day.

The saved copy of the page SHALL draw the same four buckets, the same row order and the same badge,
computing its present day in `Asia/Jakarta`, so a page opened a day after it was saved buckets by that day
and not by the day it was written.

The month heading and the month group key SHALL be gone from both renderers and from the in-page
reconciler; a group SHALL carry `data-bucket` with its bucket key (`upcoming`, `last-30-days`,
`earlier-this-year`, `older`). The panel filter SHALL keep working across the buckets, hiding a bucket it
empties together with that bucket's separator. Template mode (`?mode=template`) SHALL be unchanged: one
`Templates` heading over the undated services, sorted by their folded names.

#### Scenario: the four buckets
- WHEN `/tatib/` opens with a service in each age bucket
- THEN the headings run `Upcoming`, `Last 30 days`, `Earlier this year`, `Older`, in that order

#### Scenario: the boundary
- WHEN a service is dated exactly thirty days before today
- THEN it sits under `Last 30 days`
- AND a service dated one day earlier sits under `Earlier this year` when it is in the same calendar year

#### Scenario: early January
- WHEN today is early in January and a service is dated in the last days of December
- THEN it sits under `Last 30 days`, because the window is days, not months

#### Scenario: today
- WHEN a service is dated today and another is dated two months from now
- THEN the today row is the first row of `Upcoming`, above the two-month-out row
- AND only the today row carries the `Today` badge

#### Scenario: an emptied bucket
- WHEN the panel filter leaves a bucket with no visible row
- THEN that bucket's heading is hidden and the separator above the next bucket goes with it

#### Scenario: the dock
- WHEN `/obs/dock` opens against the same services
- THEN its picker shows the same four headings and the same badge
- AND no row is tinted for today or for being upcoming

#### Scenario: the saved copy
- WHEN a saved `/tatib/` page is opened
- THEN its headings, bucket keys, rows and badges equal the server route's for the day it is opened

#### Scenario: template mode
- WHEN `?mode=template` is on
- THEN the undated list still shows one `Templates` heading and no bucket

### R10 — A text entry's form is the media modal's large frame

A service entry's text form SHALL be drawn in the same dialog frame as the media create form: `840px`
wide and `760px` tall, each clamped to the window (`100vw − 32px` and `100dvh − 32px`). The frame SHALL
carry that dialog's chrome — no content padding, a title band padded `20px 26px` over a 1px divider at
21px type, top-level fields and the mode switch inset `26px` from the sides and `14px` apart, and an
action row inset `26px`, `14px` above and `20px` below, drawing no divider of its own.

Inside that frame the Text field SHALL take the height the switch, the title field and the action row
leave: the field SHALL grow and its textarea SHALL grow with it, so the box ends `14px` above the action
row and never pushes that row out of the dialog.

The frame SHALL be chosen by what the form is, not by a kind's script. A text form — Create and Edit — and
a media Create form SHALL carry `data-editor-size="large"`; the passage, song and media Edit forms and the
old-item forms SHALL NOT carry it, and SHALL keep the compact dialog: 480px wide, content padded 22px,
the action row divided by a 1px rule.

Below a 650px window the large frame's gutters SHALL fall to 18px and its title band to `16px 18px`, as
the media create form already drew them.

The editor dialog SHALL be placed against the window and not the document, so that its position does not
change with the page's scroll offset; an absolutely positioned child inside it (the date popover) SHALL
keep resolving against the dialog.

The text form's behaviour SHALL be unchanged: the Multi-line/Single-screen switch and its help line, the
Save guard that disables while the text is blank, the hidden `default_screen_mode` field, and the
re-render that follows a rejected save.

#### Scenario: the two create dialogs
- WHEN `+ Text` and `+ Media` are opened on a service at 1440×900
- THEN both dialogs measure 840×760 at (300, 70), with a 72.5px title band, fields 788px wide at x=326 and an action row at y=772 that is 38px tall

#### Scenario: the Text box inside the frame
- WHEN the New text form is open and empty
- THEN its textarea is 419px tall, ending 14px above the action row
- AND the Edit form's textarea is 507px tall on the same dialog

#### Scenario: a scrolled page
- WHEN an entry's Edit is opened on a service scrolled to the bottom of the window
- THEN the dialog is centred on the window and neither edge is clipped

#### Scenario: the other forms
- WHEN the passage, song or media-edit form is opened
- THEN it keeps the compact 480px dialog with its divided action row

#### Scenario: a narrow window
- WHEN the window is 390×844
- THEN the frame is 352×760, its title band padded `16px 18px`, its fields inset 18px, and the page behind gains no scrollbar

### R11 — A sidebar edit keeps every visible reading view current

After a successful edit of a Tata Ibadah, songbook or song from a reading-shell sidebar editor, every
currently visible representation of that record SHALL show the saved values without a page reload, a
sidebar reopen or any further navigation: its sidebar row, the stage heading and content when the stage
shows that record, and, when search results are open, the current result set and each affected group
count for the query already in the field.

The refresh SHALL stay on the current route and preserve the current query, the selected record, the
sidebar's open, mini and closed states, both filters, both scroll positions and keyboard focus — except
that a row which no longer matches an active filter or query may leave the list. An unrelated stage
SHALL keep its content and its route: editing a Kidung row while a Bible chapter is open changes the
Kidung lists only.

The document title SHALL be the title the refreshed route renders, following `R1` and `R3`; a save never
composes a tab title of its own. A save the server rejects SHALL leave every visible reading value
unchanged, and an entry edited inside an open Tata Ibadah SHALL keep its existing in-place stage and
contents refresh.

#### Scenario: a Tata Ibadah renamed from the first sidebar
- WHEN an open service is renamed in the first sidebar and saved
- THEN its first-sidebar row and stage heading show the saved name, the tab shows `<saved name> — Multimedia GKPS Klender`, and the page did not reload

#### Scenario: a song renamed from the second sidebar
- WHEN an open song's title is edited in the second sidebar and saved
- THEN its second-sidebar row and stage heading show the saved title, and the tab keeps its header-derived title (`R1`), not the song title

#### Scenario: a songbook renamed from the first sidebar
- WHEN the open song's songbook is renamed and saved
- THEN the songbook row, the song list heading and the song page's tab show the saved name, and the song itself is still on screen

#### Scenario: a Kidung edit while a Bible chapter is open
- WHEN a songbook row is renamed while the stage shows a Bible chapter
- THEN the songbook row shows the saved name and the chapter, its route, the pane states, the filter, the scroll and the focus stay as they were

#### Scenario: a search result that still matches
- WHEN a song in an open search result is renamed so that it still matches the query
- THEN the result shows the saved title, the group count is current, and the query and results page are unchanged

#### Scenario: a search result that stops matching
- WHEN the renamed song no longer matches the query
- THEN it leaves the results and the group counts are current, with the query and results page still in place

#### Scenario: a rejected save
- WHEN the server returns the form with a validation error
- THEN no reading row, heading or tab shows the unsaved values

#### Scenario: an entry inside an open service
- WHEN an entry is edited from the open Tata Ibadah
- THEN the stage and the contents list update in place, as they did before this requirement
### R12 — A Tata Ibadah contents row is three lines, ellipsized

A service-order row in the reading sidebar SHALL be capped at three visual lines of its own text, and a row that
does not show all of its text SHALL end in `…`. No row's label SHALL be cut at 60 characters: the cap is the row's
height, not a character count.

An untitled Text entry or legacy `TataIbadahItem` row SHALL carry the first three lines of its body, the third
ending `…` when the body holds more; a titled one SHALL carry its title alone. A song row SHALL carry its heading
and its `Bait …` line, the heading occupying at most two lines and the `Bait …` line always drawn — when the
heading cannot fit two lines it ends `…` and the `Bait …` line is still the third. A passage, media or section
break row SHALL obey the same three-line cap over its label as rendered.

A row of any kind SHALL wrap a run wider than the pane at the pane's edge instead of overflowing it, so no line —
and no `…` — sits past the row's right edge. The panel filter SHALL keep matching the entry's whole text, however
much of it the row shows. A page rendered from the saved library SHALL draw the same rows: the same lines, the same
wrapping and the same trailing `…` as the server route it mirrors.

#### Scenario: a row that hides text
- WHEN a text body holds more than three lines
- THEN the row shows the first three, the third ending `…`, and is three lines tall

#### Scenario: a row that fits
- WHEN a row's text fits in one, two or three lines
- THEN it ends without `…` and is exactly as tall as its own lines

#### Scenario: a 64-character title
- WHEN a title of 61 to 64 characters fits in three lines
- THEN all of it is shown, with no silent cut at 60

#### Scenario: an unbroken run
- WHEN a body or title is one unbroken string wider than the pane, such as a pasted link
- THEN it wraps inside the row at the pane's edge, and no part of it sits past the right edge

#### Scenario: a song row
- WHEN a song entry has a `Bait …` line and a heading that needs more than two lines
- THEN the heading is capped at two lines ending `…`, and `Bait …` is the third line
- AND when the heading fits, it takes one or two lines above that same `Bait …` line

#### Scenario: a song with no verse line
- WHEN a song entry's target is deleted or no verses are stored
- THEN its heading may use all three lines

#### Scenario: the saved copy
- WHEN a service page is opened from the saved library
- THEN its rows carry the same lines, breaks and trailing `…` as the server page's

### R13 — A reading page's text wraps at its pane

A run of text wider than the box that owns it SHALL wrap at the box's edge on every reading surface —
the page title, section and item headings, verse and lyric lines, body paragraphs, search result rows
and the Preview modal's lines — and SHALL NOT be painted past it. No reading route SHALL scroll
horizontally because of text.

The rule SHALL reach a surface by inheritance from that surface's own root, so a text run inside it
is covered without naming each element. Wrapping SHALL NOT change the layout's own measuring: a title
keeps the box width it has today, and the language toggle keeps the line it takes today. A run that
already fits SHALL render as it does now — the same line count, box height and width.

A surface that declares its own cut SHALL keep truncating: the sidebar's service and songbook rows and
the media library's filenames stay one line ending `…`, and a contents row keeps its three-line clamp
(R12).

#### Scenario: a title at the column's limit
- WHEN a service's or a song's 64-character unbroken title is opened at 1440×900, 1280×800 or 390×844
- THEN it wraps inside the reading pane, no part of it sits past the pane, and the document does not scroll sideways

#### Scenario: a body paragraph holding a link
- WHEN a Text entry's body is a pasted URL wider than the pane
- THEN it wraps inside the pane instead of running past it

#### Scenario: a heading and a verse
- WHEN a Bible pericope heading or a verse line holds a run wider than the pane
- THEN it wraps at the pane's edge, at every width

#### Scenario: a search result and the Preview modal
- WHEN a search result's title, or a rendered line in the Preview modal, is wider than its box
- THEN it wraps inside it

#### Scenario: text that fits
- WHEN a title or a body already fits its box
- THEN it takes the same line count, height and width as before this requirement

#### Scenario: a surface that truncates
- WHEN a sidebar service row or a media filename is longer than its row
- THEN it stays one line ending `…`, and a contents row keeps its three-line clamp


### R14 — Below 1272px the sidebars are drawers over the page; below 720px a toolbar carries them

Below 1272px the sidebars SHALL NOT take width from the stage: opening one SHALL leave the stage's
width unchanged, and the drawer SHALL be painted over the page with the rail above it, so it reads as
sliding out from under the rail. Only one section's stack SHALL be open at a time; the second level
SHALL cover its parent exactly — same left edge, same width — rather than offset beside it. A click on
the dimmed page behind the stack, and the Escape key, SHALL close the whole stack; the rail SHALL
reopen the level that was last open for its section. While a level travels, no level below it SHALL
be drawn, and a stack opening or closing SHALL move all its levels at once rather than one after
another. Above 1272px the columns SHALL push as they do
today.

Below 720px the rail's strip SHALL be replaced by a top toolbar — the drawer control at its left end
beside the logo, the light/dark control at its right — and the rail SHALL become a full-width menu
drawer under that toolbar, its destinations shown with their names. The control SHALL carry two
glyphs only: a menu glyph when nothing is open, a close glyph when anything is; it SHALL NEVER step
back one level. Choosing a section SHALL open its list over the menu, which stays underneath. A
Tata Ibadah service SHALL offer no contents drawer at this width: its rows open the service's page and
close the stack. Neither the Project control nor the projector-window control SHALL be drawn.

A row's reorder handle SHALL show on the same terms, and dragging it SHALL own the gesture rather
than becoming the list's scroll.

A row's edit control SHALL show without a pointer hover wherever the pointer cannot hover, and at the
phone width; and at that width a row SHALL stack its name over its date rather than clip the date
beside the always-visible control. Every icon in the toolbar SHALL be drawn at one size.

#### Scenario: a drawer over a 768px window
- WHEN a sidebar is opened at 1024px or 768px
- THEN the stage keeps the width it had, the drawer floats over it, and the second level covers the first exactly

#### Scenario: a level travels alone
- WHEN the second level opens over its parent, or the stack closes
- THEN no level below the travelling one is drawn, and every open level moves in the same frame

#### Scenario: the stack closes
- WHEN the dimmed page or Escape is used with a two-level stack open
- THEN every level closes and the page is whole again

#### Scenario: the rail restores
- WHEN the rail is used after a two-level stack closed
- THEN that section's first and second levels both reopen

#### Scenario: a phone's menu
- WHEN a 425px window opens the control
- THEN the rail is a full-width drawer of named destinations, and choosing one slides its list over the still-open menu

#### Scenario: a service on a phone
- WHEN a Tata Ibadah row is tapped at 425px
- THEN the service's page opens, the drawers close, and no contents drawer is offered

#### Scenario: a row on a phone
- WHEN a sidebar row is shown at the phone width, or under a touch pointer
- THEN its edit control is visible without hover, its date sits under its name, and neither runs under the control

#### Scenario: the desktop
- WHEN the window is 1440px wide
- THEN the columns push the stage exactly as they did before this requirement

### R15 — The landing page's search field sits on the window's middle

On the landing page the search field SHALL be vertically centred on the window's middle, within 1px,
at every width from 320px to 1920px — the field's own border box, not the logo-and-field block it is
part of. The logo SHALL keep its 96px box 26px above the field, whole, and the landing page SHALL stay
exactly one window tall, adding neither a vertical nor a horizontal scrollbar.

The section SHALL be as tall as the box the stage leaves it, so the phone layout — where the stage pads
for its toolbar — centres on the same terms as the desktop rather than 36px low. The stage's two
vertical paddings SHALL be stated once, so a layout that moves one moves the measurement with it.

The views that are not the landing SHALL NOT move: a results page's compact bar keeps its place at the
top of the stage and never recentres on a resize, and a reading page keeps its column where it was.

#### Scenario: a desktop window
- WHEN the landing page is opened at 1920×1000, 1440×900, 1280×800 or 1024×768
- THEN the field's box centre equals the window's middle within 1px, the logo sits 26px above it, and the page is one window tall

#### Scenario: a phone
- WHEN the landing page is opened at 720×900, 600×800, 390×844 or 320×568
- THEN the field is on the middle on the same terms, with the logo wholly inside the window above it

#### Scenario: the results page
- WHEN a query is submitted and the window is then resized
- THEN the compact bar stays at the top of the stage, its field 46px (or 82px at the phone width) from the stage's top, and never recentres

#### Scenario: a reading page
- WHEN a saved reading page is opened
- THEN no search section is painted, and the reading column occupies the stage exactly as before

### R16 — A service on air offers the way back to its projector window

While this page's Tata Ibadah is the browser's live service and the display is on, the reading page's
project group SHALL draw a second control immediately before Stop projecting: an icon-only button
**34 × 34 px** whose accessible name and tooltip read `Open projector window`, drawn on the desktop
widths the Project control is drawn on and never at the phone width (R14). It SHALL NOT be drawn in
any other state — off air, hidden, released, or another service live.

Pressing it SHALL open `/projector` in the browser's `gkps-projector` window at the screen that is on
air and SHALL NOT write the display state; when that window is already open it SHALL be brought
forward without loading the projector page again. Stop projecting SHALL keep releasing, and closing
the projector window SHALL keep leaving the state untouched. When the pane is narrower than the
group, the group SHALL wrap inside the pane rather than cross its right edge — the live group with
Media files measures 280.4 px in the 240 px pane of a 1280 window, and 181.7 px without it.

#### Scenario: reopening a closed window
- WHEN a service is on air at screen 4 and its projector window has been closed
- THEN the control reopens the window on `/projector` showing screen 4, and the state is unchanged

#### Scenario: an open window
- WHEN the projector window is already open
- THEN the control brings it forward without loading the page again

#### Scenario: nothing on air
- WHEN the display is released, hidden, or naming another service
- THEN the control is not drawn and Project is the only projection control

#### Scenario: a narrow desktop
- WHEN the window is 1280px wide and the service has media
- THEN the group wraps inside the 240px pane, no part of it crosses the pane's edge, and the header is 111px tall

### R17 — A stage entry link reads as text until it is pointed at

A Tata Ibadah stage's entry titles SHALL be painted in the same ink as the text around them, with no
resting underline, in both themes. Pointing at one SHALL underline it 3px below the text without
changing its colour, and keyboard focus SHALL draw the same underline. The entry's floating controls
SHALL hold a column of their own at the item's right edge, so no title or media name is drawn under
them; while the reading pane is narrower than 700px their labels SHALL collapse to icons, and the
label SHALL remain available to assistive technology.

#### Scenario: at rest
- WHEN a stage's entries are shown in either theme
- THEN every entry title is the heading's ink with no underline

#### Scenario: pointed at
- WHEN the pointer rests on an entry title, or the title is reached with the keyboard
- THEN the title gains a 3px underline and keeps its colour

#### Scenario: the controls
- WHEN an entry is hovered, at any width
- THEN its Preview / Edit / Delete controls sit in their own column and no title or media name is drawn under them

#### Scenario: a narrow pane
- WHEN the reading pane is narrower than 700px, as on a phone or a 1440px window with both sidebars open
- THEN the controls show as three icons and each still carries its name for assistive technology

### R18 — A service entry draws no box until it is pointed at

A Tata Ibadah stage's entries SHALL draw no surface at rest, in both themes: no fill and no outline
on an entry or on a section break. Pointing at an entry, reaching it with the keyboard deliberately,
or holding its editor open SHALL fill it with `--icon-hover-bg` inside the box it already owned —
`min-height: 56px`, `padding: 8px 8px 8px 12px`, a 9px radius and the reserved controls column —
and quiet focus restoration SHALL NOT fill it. A media entry SHALL keep its own geometry
(`min-height: 80px`, `padding: 16px 16px 16px 64px`, a 42px tile at `left: 13px`) and a section
break SHALL keep its 56px box, its 2px rule and its diamond.

#### Scenario: at rest
- WHEN a stage is shown with nothing hovered or focused
- THEN every entry and section break paints no background and no inset ring, in either theme

#### Scenario: pointed at
- WHEN an entry is hovered, deliberately focused, or owns the open editor
- THEN it fills with the same tint its rail's icons use, and keeps its box and its words in place

#### Scenario: every kind
- WHEN a service holds text, scripture, song, media and section-break entries
- THEN each draws no resting surface, and the media tile and the break's rule still identify them

### R19 — A service's add rows open over the seam, and nothing moves

A Tata Ibadah stage's add rows SHALL keep a fixed slot in the flow and draw their bar over that slot,
so that opening or closing a row SHALL NOT move any block: no entry's top, no section break's
position and no scroll height SHALL change on hover, on focus or while a modal is open. The bar
SHALL be centred horizontally on the column and vertically on the seam, and its hit area SHALL be no
wider than its buttons, so an entry's own preview, edit and delete controls stay reachable while the
row is open. Each seam SHALL paint a 1px line, faint at rest and stronger while its row is open.
Every row SHALL remain reachable by pointer, by a hover band of its own, and by keyboard focus.

#### Scenario: opened
- WHEN the pointer enters an entry, or deliberate focus lands inside it
- THEN both rows around it open, and every block keeps its position and the page its height

#### Scenario: the bar
- WHEN a row is open
- THEN its bar is centred on the column and on the seam, and the entry's own controls remain clickable

#### Scenario: at rest
- WHEN nothing is hovered
- THEN each seam paints a faint line and no bar is drawn

#### Scenario: keyboard
- WHEN a row's first button takes focus by Tab
- THEN the row opens and its buttons are reachable

### R20 — A transfer row keeps its icon column, and a long name ellipsizes

A row of the Transfers dialog SHALL keep a 32px column for its direction glyph, and that column SHALL
NOT be narrowed by the row's content. A name wider than the text column SHALL end in an ellipsis
inside the column the row reserves — the list's width less its padding, the 32px mark and the 12px gap
— and SHALL NOT change the row's width, its height, or the mark's width. Every row's name and status
label SHALL share one left edge, in every list the dialog draws and at every window width it is drawn
at.

#### Scenario: a list that mixes lengths
- WHEN the dialog draws rows whose names both fit and overrun the text column
- THEN every glyph shares one left edge, and every name and status label shares one left edge

#### Scenario: a long name
- WHEN a name is wider than the text column
- THEN it ends in an ellipsis, the row keeps its 72px height on a 1440px window, and the mark stays 32px

#### Scenario: a narrow window
- WHEN the window narrows until the dialog shrinks (580px → 382px at a 420px window)
- THEN the text column absorbs the loss (482px → 284px) and neither the mark nor the two left edges move

#### Scenario: the rail's own list
- WHEN the same rows are drawn from the rail rather than the library button
- THEN the geometry is the same, because one renderer draws both

### R21 — A media size reads in the unit that still shows its number

Every size the product prints SHALL be drawn in the largest decimal unit in which its value is at least
one — `B`, `KB` (1,000 B), `MB` (1,000 KB), `GB` (1,000 MB) — so that a non-empty file never reads as
zero, and SHALL carry one decimal only when that decimal is not zero. A value that would round to `1000`
SHALL be drawn in the next unit. The New media card, a Media Library row and the Media Library Total
SHALL draw every size through one function.

#### Scenario: a small file
- WHEN a 12,345-byte file is chosen on the card
- THEN its line reads `Image · 12.3 KB`, and a 512-byte file reads `Image · 512 B`

#### Scenario: a whole value
- WHEN a size is a whole unit
- THEN it reads `2 KB`, `1 MB` or `200 MB`, with no trailing `.0`

#### Scenario: every surface
- WHEN the same file is drawn on the card, in its library row and in the library Total
- THEN all three print the same string

### R22 — The Media Library list groups by age, not by upload day

The Media Library's list SHALL group its rows into three age buckets, in this order and under these
labels: `Last 30 days` (uploaded today or up to thirty days ago), `Earlier this year` (older than
thirty days and in the present calendar year) and `Older` (anything older). These SHALL be the Tata
Ibadah list's own windows and words (`R9`), and the present day SHALL be the congregation's, in
`Asia/Jakarta`. A bucket holding no visible row SHALL draw neither a heading nor its spacing.

A row SHALL keep its own full date — `Image · 28 Oktober 2026 · 7 KB` — so the heading only says how
old the group is. The heading SHALL be the list's existing `h2.media-library__group`, unchanged in
type, size, weight, colour, tracking and margins, carrying its bucket key as `data-bucket`
(`last-30-days`, `earlier-this-year`, `older`); the per-upload-day heading SHALL be gone.

Headings SHALL be drawn only while the list is sorted by upload date: a size sort SHALL draw none, and
an ascending date sort SHALL reverse the bucket order so the list still reads oldest first. The type
chips and the `Unused` chip SHALL still filter the list, and a bucket they empty SHALL hide its
heading. The list SHALL have no `Upcoming` and no today bucket: an upload's timestamp is never in the
future, and a file uploaded today is the newest row of `Last 30 days`.

#### Scenario: the three buckets
- WHEN the list opens over files uploaded today, twelve days ago, forty days ago and last year
- THEN the headings run `Last 30 days`, `Earlier this year`, `Older`, in that order, each over its own rows

#### Scenario: the edges
- WHEN a file was uploaded exactly thirty days ago
- THEN it sits under `Last 30 days`
- AND a file uploaded one day earlier, in the same calendar year, sits under `Earlier this year`

#### Scenario: early January
- WHEN today is early in January and a file was uploaded in the last days of December
- THEN it sits under `Last 30 days`, because the window is days, not months

#### Scenario: the sort
- WHEN the list is sorted by upload date ascending, or by file size
- THEN an ascending list draws its buckets oldest first, and a size sort draws no heading at all

#### Scenario: a filtered bucket
- WHEN a type chip or `Unused` leaves a bucket with no visible row
- THEN that bucket's heading and its spacing are not drawn, and clearing the chip restores them

#### Scenario: the row
- WHEN a row is read
- THEN it shows the same icon, filename, full date, size, service links or unused line, cloud control and remove button as before

### R23 — The transfer history groups by age, with today and the last week split out

The Transfers dialog SHALL group its rows into five age buckets, in this order and under these labels:
`Last 24 hours`, `Last 7 days`, `Last 30 days`, `Earlier this year` and `Older`. A transfer's bucket
SHALL be decided by the instant it started, and the first three rungs SHALL be rolling windows measured
from the moment the dialog draws: under twenty-four hours, under seven days, under thirty days. Beyond
thirty days the congregation's calendar year in `Asia/Jakarta` SHALL separate `Earlier this year` from
`Older`. A bucket holding no row SHALL draw no heading.

Active transfers SHALL still draw above finished ones, inside the bucket their start time gives them; a
finished row SHALL be ordered by its end time, newest first, ties by id newest first. A heading SHALL be
an `h3.media-transfers__group` under the dialog's own `h2`, carrying its bucket key as `data-bucket`
(`last-24-hours`, `last-7-days`, `last-30-days`, `earlier-this-year`, `older`), and drawn on the list's
heading numbers. A row SHALL keep its direction glyph, its name and its state — `Completed`, `Cancelled`,
`Failed`, or the percentage while active — and SHALL NOT print its own date: the heading carries the age.
The transfer rail's progress flyout SHALL keep its own shape, its active rows and its seen divider, and
SHALL draw no bucket headings.

#### Scenario: the five rungs
- WHEN the dialog opens over transfers started two hours, three days, twelve days, forty-five days and a year ago
- THEN the headings run `Last 24 hours`, `Last 7 days`, `Last 30 days`, `Earlier this year`, `Older`, in that order

#### Scenario: the edges
- WHEN a transfer started exactly twenty-four hours ago
- THEN it sits under `Last 7 days`, not `Last 24 hours`
- AND one started exactly thirty days ago sits under `Earlier this year`

#### Scenario: a running transfer
- WHEN a transfer is still active
- THEN it draws above the finished rows of the bucket its start time gives it

#### Scenario: the rail
- WHEN the dialog is opened from the transfer rail
- THEN its rows and its seen divider are drawn, and no age heading is

#### Scenario: an undatable row
- WHEN a transfer's start time cannot be read
- THEN it is drawn under `Older` rather than dropped from the history

#### Scenario: the empty history
- WHEN the companion is unavailable or holds no transfer
- THEN the dialog draws its existing empty state and no heading

### R24 — The Media Library's file list is drawn once per refresh, and holds still

The Media Library page SHALL draw its file list once per refresh — on the first load, on **Share
online**, on **Remove**, on a saved setting, and on every later re-read — and SHALL NOT draw an
intermediate state in which a file's known service references are replaced by the one-line `Service
uses unavailable` placeholder. No row SHALL change position during a refresh: every frame from the
triggering action to the settled list shows each row where it finally sits. The page SHALL NOT draw
the list before its references are known; when that read fails it SHALL draw once, with `Service uses
unavailable`, and keep it. The 2s status poll SHALL keep re-reading the companion and SHALL stay
visually inert while the data has not changed. Nothing else about the page changes: the files and
their order, the rows' markup and heights, the filters, the sort, the Unused toggle, the cloud
control's states and the page's title.

#### Scenario: a refresh from an action
- WHEN the owner clicks Share online, opens Remove and cancels, or saves a Media Library setting
- THEN the list is drawn once, and every row's top has a single value from the click to the settled list

#### Scenario: the first load
- WHEN the page opens
- THEN the list appears once, already carrying its service references, and never grows after it appears

#### Scenario: references unavailable
- WHEN the references read fails
- THEN the list is drawn once with `Service uses unavailable` and stays where it is

#### Scenario: a running transfer
- WHEN a transfer is running and the 2s poll re-reads the companion
- THEN the list is redrawn from the same data and no row moves

### R25 — A passage and a song carry a kind mark of their own

A Tata Ibadah stage SHALL mark a passage row and a song row with a small decorative glyph — the rail's
Bible mark for a passage, the rail's beamed note for a song — and SHALL NOT mark a text row, a section
break or a media row. The glyph SHALL sit on the media chip's centre line and the row's title SHALL
take the media title's column, so a media file, a passage and a song share one left rail: the mark
centred, the words from 64px. The glyph SHALL be smaller than the 42px chip and SHALL carry no tint of
its own, so a media file is never mistaken for a passage or a song. The mark SHALL be hidden from
assistive technology, take no pointer, and add no height of its own; a song's title MAY take one more
line where the narrower column wraps it.

#### Scenario: a passage
- WHEN a service holds a passage entry
- THEN its row draws a 20px open book with a Latin cross above it — the same path the rail's Alkitab
  button draws — centred on the media chip's centre line, with the reference starting on the media
  title's column

#### Scenario: a song
- WHEN a service holds a song entry
- THEN its row draws the rail's beamed pair, and its `Bait` line keeps the same left edge as the title

#### Scenario: every other kind
- WHEN the service also holds a text entry, a section break and a media file
- THEN none of them draws a mark, and a text row keeps its own 12px edge

#### Scenario: a deleted target
- WHEN a song's songbook or an included verse was deleted
- THEN the row still draws its song mark, because the mark states the kind, not the availability

#### Scenario: pointed at, and in the dark
- WHEN the row is hovered, or a modal opened from it is up, in either theme
- THEN the mark keeps the stage's meta ink and stays legible on the hover fill

### R26 — The Media Library's references write carries its own refresh's token

The Media Library page SHALL send its service-references write with the write token supplied by the same
refresh's `/status` response, so that the first refresh after the page opens is authenticated and its list
is drawn once, already carrying its references. The token SHALL be in place before the write is sent, and
the head controls SHALL still be applied once, from that same response. No endpoint, payload, header name
or copy changes.

#### Scenario: the first refresh
- WHEN the page opens and its first refresh runs
- THEN the references write carries that refresh's token, and the list is drawn once with its references

#### Scenario: a later refresh
- WHEN any later refresh runs
- THEN it still writes with its own token and still draws once

#### Scenario: the token cannot be had
- WHEN the `/status` read fails
- THEN the page degrades as before — no write, one draw, the disconnected copy

### R27 — An audio file's Preview reads its times as `current / total`

An audio file's Preview SHALL read its two times as one pair — the played time, a `/`, the total — on one
line under the seek bar, right-aligned so the pair's right edge is the bar's right edge. The played time
SHALL NOT sit at the bar's left end. Both numbers SHALL keep updating in place as the audio plays and as
it is seeked, without the line moving or the pair's right edge shifting. The separator SHALL be text, so
assistive technology reads one value rather than two adjacent numbers. Nothing else about the preview
changes: the dialog's width, the 48px play button, the filename line, the 6px bar, the 7px gap above the
line, the 12px type, `var(--head-ink)`, the unavailable state — and the projector's own audio bar
(`.screen__audio-times`), which already read `current / total`.

#### Scenario: the pair
- WHEN an audio entry's Preview opens and the file's duration is known
- THEN the line under the bar reads `0:00 / 5:02` — both numbers together, 5px either side of the slash,
  the total's right edge on the seek bar's

#### Scenario: playing and seeking
- WHEN the audio plays, or the bar is seeked
- THEN both numbers update in place and the pair's right edge does not move

#### Scenario: read aloud
- WHEN the line is read by assistive technology
- THEN it is one value — played, then total — not two numbers run together

#### Scenario: a long file
- WHEN the duration runs past an hour
- THEN the pair reads as the clock does elsewhere (`62:03`), still on one line and right-aligned

#### Scenario: the file cannot be served
- WHEN the local companion cannot serve the file
- THEN the player stays hidden and the line is not drawn, as before

### R28 — The preview's header gives a song's verse tabs a row of their own

The entry preview's pinned header SHALL draw the entry's identity on a title band and, when the entry is a
song with more than one shown verse, the verse tabs on a band of their own beneath it — a sibling of the
title band, never a child. The title SHALL take the header's whole content width before it ellipsizes on
one line. The header SHALL draw exactly one rule: beneath the tab band when one is shown, otherwise beneath
the title band as it always has. The dialog SHALL open with keyboard focus on its scrolling body, never on
a verse tab; while a visible tab band is shown and no screen-mode footer is, `Tab` on the body SHALL move
focus to the selected tab and `Shift+Tab` on that tab SHALL move it back to the body. A preview without
verse tabs SHALL keep its 52px title band, its own rule and its body exactly where they are.

#### Scenario: a long title
- WHEN a song whose title is wider than the dialog opens
- THEN the title fills the header's content width and ellipsizes once, and the tabs stand on the row below it

#### Scenario: one rule
- WHEN a song preview is drawn
- THEN the title band draws no rule, the tab band draws one 14px under the tabs, and the lyrics start 22px below it

#### Scenario: the first focus
- WHEN any preview opens, by pointer or by keyboard
- THEN focus is on the scrolling body and no verse tab carries a focus ring; a keyboard open paints the body's own ring

#### Scenario: the tabs stay reachable
- WHEN the body of a song preview has focus
- THEN `Tab` moves to the selected verse tab and `Shift+Tab` on that tab returns to the body

#### Scenario: no verse tabs
- WHEN a passage, text, image, audio, video or PDF preview opens
- THEN the title band keeps its rule and the body sits directly under it, unchanged

### R29 — The rail names its sections with the marks the stage draws

The main rail SHALL draw one mark per section, and a section's mark SHALL be the same drawing wherever
the product repeats it: the Bible — an open book with a Latin cross above it — on the rail, in the
Alkitab panel's empty state, on a passage row and on the empty stage's Add Passage tile; the beamed
note on the rail, in the Kidung panel's empty state, on a song row and on the Add Song tile; a
clipboard — a board, a clip above it and three rule lines — on the Tata Ibadah rail button and in that
panel's empty state.

No rail mark SHALL reuse a media family's mark. An audio file SHALL draw a five-bar waveform in every
place that mark is drawn (the stage's chip, the Media Library list, the service-media dialog and the
upload preview), and the image, video, PDF and PowerPoint marks and the `missing` fallback SHALL keep
their own shapes.

Every mark SHALL be inline SVG painted with `currentColor`, carry no tint or fill of its own, be hidden
from assistive technology, take no pointer, and sit in the box its surface already authors: 24px in
the 44px rail button, 24px on an empty stage's tile, 20px on a stage row, 23px inside the 42px media
chip. The rail SHALL keep its five destinations in their order, and the Search and Media Library marks
SHALL NOT change.

#### Scenario: the Bible, at every size
- WHEN the rail, the Alkitab panel's empty state, a passage row and the Add Passage tile are drawn
- THEN all four draw the same open book with a Latin cross, at 24px, 48px, 20px and 24px respectively

#### Scenario: a song, at every size
- WHEN the rail, the Kidung panel's empty state, a song row and the Add Song tile are drawn
- THEN all four draw the same beamed pair

#### Scenario: the service order
- WHEN the Tata Ibadah rail button and that panel's empty state are drawn
- THEN both draw a clipboard, and neither draws a page, a folder or a document

#### Scenario: an audio file beside a song
- WHEN a stage holds a song entry and an audio media file
- THEN the song draws the beamed pair and the file draws the five-bar waveform

#### Scenario: the other families
- WHEN the Media Library lists an image, a video, a PDF, a PowerPoint or a file of unknown family
- THEN each draws the mark it drew before this requirement

#### Scenario: the theme
- WHEN the theme changes
- THEN every mark repaints with its own element's ink and needs no repaint of its own

### R30 — A song entry names a song that has no verses

The song entry's Verses field SHALL tell a picked song that carries no verses apart from no song picked at
all: with no song picked the field reads `Pick a song first`, and with a song picked whose live verses are
empty it reads `This song has no verses`. The second line SHALL be in the server's own form fragment, not
only written by the page's script, and the field SHALL stay disabled there — an empty verse menu is not
offered — because there is nothing to choose.

The other lines SHALL stay as they are: `All verses` when every verse is included, `Verses n, …` when some
are, and `No verses: keep at least one` when a song's boxes were all cleared. A refusal caused by the
chosen song carrying no verses SHALL name the song — `This song has no verses: pick another song.` — while
a refusal caused by clearing every box of a song that has verses SHALL keep
`Keep at least one verse in the service.`

#### Scenario: a song with no verses is picked
- WHEN a song whose live verses are empty is picked in the song entry
- THEN the Verses field reads `This song has no verses`, its trigger is disabled, and no checkbox is drawn

#### Scenario: nothing is picked
- WHEN the song entry opens with no song chosen
- THEN the Verses field reads `Pick a song first`

#### Scenario: the first paint of an edit
- WHEN the server renders the form of a stored song entry whose song has no live verses
- THEN its markup carries `This song has no verses` before any script runs

#### Scenario: the stored verses survive
- WHEN an entry stores verse numbers the song no longer carries
- THEN those numbers remain choices, the field is not in the no-verses state, and the entry stays saveable

#### Scenario: saving a verse-less song
- WHEN Save is pressed with a song that carries no verses chosen
- THEN the field's error reads `This song has no verses: pick another song.` and nothing is written

#### Scenario: clearing a song's boxes
- WHEN every box of a song that has verses is cleared and Save is pressed
- THEN the error reads `Keep at least one verse in the service.`

#### Scenario: the verses cannot be loaded
- WHEN the verses request fails for a picked song
- THEN the failure notice is shown and the field keeps the line it had

### R31 — A preview's play shortcut leaves no focus ring on the dialog

The Preview dialog's body SHALL draw its keyboard focus indicator — a 2px `--focus` ring inset 2px —
whenever the reader reaches it with Tab, and SHALL paint nothing on it after a key that operates the
player, which in an audio or video preview is the space bar. The body SHALL keep DOM focus while the
ring is suppressed, so arrow-key scrolling and the guard at its edges are unchanged, and the ring SHALL
return on the reader's next Tab. A preview opened from the keyboard SHALL show the ring until the first
space press takes it away.

#### Scenario: the play shortcut
- WHEN a pointer opens an audio or a video preview and space is pressed
- THEN the player toggles and no ring is painted on the body or on the dialog's edge

#### Scenario: a keyboard open, then the shortcut
- WHEN the preview was opened from the keyboard, so the ring is showing, and space is pressed
- THEN the ring is gone, the body still holds focus, and playback toggled

#### Scenario: a reader who navigates
- WHEN the reader presses Tab inside the dialog, whatever was painted before
- THEN the body's 2px `--focus` ring is drawn again once the body holds focus

### R32 — A dialog's `cancel` answers only the dialog's own dismissal

An editor dialog SHALL close on a `cancel` event only when that event's target is the dialog itself. A
`cancel` whose target is a descendant SHALL NOT close it — the New media form's file input fires one when
the person closes the file picker without choosing, or re-picks the file already chosen — and the form
SHALL keep its tab, its chosen file, its typed title, its note and its Save state. Dismissing the dialog
itself SHALL keep closing it with its existing motion, and the other editor forms SHALL be unaffected.
Nothing about the dialog's frame, its markup or its copy changes.

#### Scenario: the picker is dismissed with nothing chosen
- WHEN the New media dialog is open on Upload and the person closes the file picker without a file
- THEN the dialog stays open, the upload prompt is still shown and Save is still disabled

#### Scenario: the picker is dismissed with a file chosen
- WHEN a file has been chosen and the person closes the picker again
- THEN the dialog stays open and still shows that file, its name, its size and its note, with Save enabled

#### Scenario: the dialog is dismissed
- WHEN Escape is pressed while the New media dialog has focus
- THEN it closes with its 150ms closing motion, as before

#### Scenario: the dialog is on the Media Library tab
- WHEN a row is selected there and a `cancel` arrives from the file input
- THEN the dialog stays open on that tab with that row still selected

### R33 — The dock fills whatever size it is given

The operator dock's panel SHALL take the dock viewport's full width and height at every width of 320px
and up: no maximum width and no horizontal auto margin, so no strip of background is left beside it, and
the page SHALL NOT scroll horizontally at any width.

The picker SHALL stay a single column at every width: its body keeps block layout, no rule lays its age
buckets out side by side, and every row SHALL span the picker body's content width — the panel's width
less the body's 8px side padding — with its name at the row's left padding and its date right-aligned on
its right padding. A bucket head SHALL keep sticking to the top of the picker's scroller, as at the
narrow width it was drawn for.

No other metric SHALL change: the head's padding, the row's 40px minimum height and 10px padding, the
`Today` and `On screen` badges, the transport's 40px arrows and the 5px scrollbar keep their values, and
every box at a width of 560px or less SHALL be identical to the dock spec 119 delivered. The runner is
not re-flowed by this requirement: it already filled the panel, and its entries are a sequence.

#### Scenario: a wide dock
- WHEN `/obs/dock` opens in a 1440px dock
- THEN the panel is 1440 wide with its left edge at 0
- AND each picker row is 1424 wide, its name at the row's left padding and its date at its right

#### Scenario: four buckets in a wide dock
- WHEN the picker holds four age buckets in a 1920px dock
- THEN the buckets are stacked in one column, not laid out side by side

#### Scenario: a narrow dock
- WHEN the same page opens in a 420px dock
- THEN the panel is 420 wide and every box is where it was before this requirement

#### Scenario: the scroller
- WHEN the picker is scrolled past a bucket's rows
- THEN that bucket's head stays at the top of the scroller

### R34 — A Tata Ibadah is a service or a template

Every Tata Ibadah SHALL carry a type — Normal or Template — chosen when it is created and never changed
afterwards. A Normal one SHALL carry a date and a Template SHALL carry none; the pairing SHALL hold in the
model, in every writing endpoint and in the database, and no edit SHALL change a record's type. The New Tata
Ibadah modal SHALL carry the switcher (Normal selected), ask for the date only on a Normal, and offer no
control that empties it; the Edit modal SHALL name the type instead of offering the choice. The panel SHALL
choose its list from the type: dated services by date, templates under Templates. Rows that existed before
this requirement SHALL keep the type they behaved as — a date meant Normal — and no entry is converted.

#### Scenario: creating both types
- WHEN the New Tata Ibadah modal opens
- THEN it offers Normal and Template, and Normal is selected
- AND choosing Template hides the date field and saves a template with no date

#### Scenario: an edit cannot move the type
- WHEN a Normal Tata Ibadah's date is cleared in the Edit modal and Save is pressed
- THEN the save is refused and the date it had is kept

### R35 — A template carries fill-ins and choices

A template's add rows SHALL offer `+ Fill-in` and `+ Choice` after the four kind buttons — `+ Text`, `+ Song`,
`+ Passage`, `+ Media`, in that order — past a hairline; a Normal Tata Ibadah SHALL NOT offer either, and every
writing endpoint SHALL refuse both on one. A fill-in
SHALL be a title/note and one kind — passage, song, text or media — with no content of its own. A choice
SHALL be a title, one kind, and an ordered list of options, each a complete entry of that kind added from the
choice's own row as an indented child row, its mark in the gutter and its title in the slot's own type, and
the row SHALL state how many options it holds — `No options yet` when it holds none, the row then carrying
`+ Add option` itself so the first one can be created. A choice may hold no
options: the template is allowed to be unfinished, and such a choice cannot be settled at generation.

#### Scenario: adding an option
- WHEN a choice row's `+ Add option` is pressed
- THEN that kind's New modal opens, and the saved entry appears under the choice in its own order

#### Scenario: an option of the wrong kind
- WHEN a text entry is attached to a song choice
- THEN the save is refused

### R36 — A template creates a dated service in two steps

A template's page SHALL replace the projector controls with **Use template**, and that button SHALL open a
modal showing the order view-only: ordinary entries muted and inert, every fill-in and choice live. A fill-in
SHALL be settled by **Set**, which opens that kind's New modal and only validates — nothing is written to the
template — and a choice by **Choose**, which lists its options with their Preview. **Next** SHALL stay
disabled until every slot is settled, with the count on screen; step 2 SHALL be the normal Tata Ibadah form,
the name prefilled and the date at the nearest Sunday; **Create** SHALL ask for confirmation and SHALL create
the service in one transaction, copying the template's order with each slot replaced in place and each
legacy row copied as a legacy row. Generating or abandoning SHALL leave the template byte-identical.

#### Scenario: a settled order
- WHEN every fill-in and choice is settled and **Next** is pressed
- THEN the form asks for a name and a date, and **Create** makes the service

#### Scenario: a choice with no options
- WHEN a choice has no options
- THEN its control is disabled and labelled `No options`, and **Next** stays disabled

### R37 — Any Tata Ibadah copies as a template

The Edit modal SHALL offer **Copy as template** for a Normal service and a template alike, after a
confirmation that names the consequence. The copy SHALL keep the name and every entry in order as ordinary
editable entries — nothing is converted to a fill-in or a choice — and a template source SHALL also bring
its fill-ins, choices and options. The copy SHALL have no date and SHALL be a template, and the app SHALL
land on it with the panel on Templates.

#### Scenario: copying a service
- WHEN a dated service is copied as a template
- THEN the copy is undated, its entries keep their kinds and order, and it opens under Templates

### R38 — A template never reaches a screen, and its media is kept but not fetched

A Template SHALL never be projectable: its page carries no projector control, the projector route SHALL
answer the empty display for its id, and the operator dock's list SHALL omit it. A file referenced by a
template SHALL count as used, so it is never auto-deleted however old it is, and it SHALL NOT be
auto-downloaded: only files referenced by an active service dated today or later enter the download
manifest, so a template's file waits for the dated service that uses it.

#### Scenario: projecting a template
- WHEN `/projector?service=<template id>` is opened
- THEN it shows the empty display, never the template's order

#### Scenario: a template's media file
- WHEN a file is referenced only by templates
- THEN it is never auto-deleted and it does not enter the download manifest

### R39 — The old bookmarks stand as services

A migration SHALL create one dated service for every active bookmark that carries a date and at least
one song: the bookmark's own name and date, its items as song entries in the bookmark's order, each
with the same verse numbers. A bookmark that is deleted, undated or holds no songs SHALL NOT convert.
A service already standing under the same name and date SHALL NOT stop the conversion — the bookmark
still gets a service of its own beside it, and the standing service is left as it was, so a name and
date may carry two services. The name comparison is case-sensitive. The bookmark rows SHALL NOT be
written.

#### Scenario: a converted bookmark
- WHEN a bookmark dated 2026-10-11 with nine songs is converted
- THEN the service list holds a 2026-10-11 service carrying nine song entries in the same order with
  the same verses

#### Scenario: a service already on that day
- WHEN a service already stands under the bookmark's name and date
- THEN the bookmark becomes a second service of that name and date, and the first one keeps its own
  entries untouched

#### Scenario: a bookmark that stays behind
- WHEN a bookmark is deleted, undated, or holds no songs
- THEN no service is created for it and the bookmark itself is unchanged

### R40 — A song's verses are added, edited, removed and reordered on its page

The song page SHALL render verse controls only for ordinary (non-hymn) songbooks where editing is
allowed: one add control after the last verse, and a grip and edit control per verse row painted only
while the row is hovered or focused. With a single verse the grip SHALL render disabled — one verse
has nowhere to move. A hymn song's page and a restricted reader's page SHALL render none.
A verse that any service entry references SHALL NOT be deletable. Entries name verses by ID and display
the current numbers; reordering renumbers live rows 1…n and never moves a reference. Reordering is
pointer-only drag: grabbing a grip collapses verses to 44px one-line rows for the gesture, a ghost copy
rides the pointer one to one (service sidebar shape) while the real row stays as a tinted placeholder,
others slide one slot per crossing with no rebound, numbers renumber as rows cross, and the drop writes
at once with no Save and no confirmation. The slot is read from the current cursor height against the
grab-frozen midpoints of the other verses, not from the origin slot.

#### Scenario: adding a verse
- WHEN the reader presses `Add verse` and saves a lyric on an ordinary song
- THEN the verse is appended numbered one past the last, the stage shows it without reload

#### Scenario: editing a lyric
- WHEN the reader saves an edit
- THEN the verse keeps its number and only that lyric changes

#### Scenario: reordering from the grip
- WHEN the reader drags a verse so the live cursor passes another verse's frozen midpoint
- THEN the dragged verse takes that slot, numbers read `from→now` while dragging, rows it passes move exactly one slot once, and the drop writes the order at once with no confirmation

#### Scenario: referenced verse cannot be deleted
- WHEN the edit modal opens for a verse a service names
- THEN delete is disabled and the modal states how many services name the song

#### Scenario: service survives reorder
- WHEN a song is reordered
- THEN a service entry naming its verses still projects the same lyrics, labelled by their current numbers

#### Scenario: single verse has nowhere to go
- WHEN a song has one verse and the row is hovered
- THEN the edit control works and the grip renders disabled

#### Scenario: hymn and restricted pages
- WHEN the page is a hymn song's or editing is restricted
- THEN no verse control is drawn and every endpoint refuses the write

### R41 — Sidebar records are deleted through a confirmed, guarded action

Where editing is allowed, a non-hymn songbook row, a song of a non-hymn songbook, and every Tata Ibadah
service and template row SHALL carry a delete control beside the edit control — the same 26px box,
hidden at rest, revealed while the row is hovered or focused, drawn outright on touch screens. A dated
service row SHALL hide its displayed date while the row is hovered or focused for that reveal, so the
controls never cover it; the row's accessible label keeps the date. Clicking delete SHALL open the
shared editor modal on a confirm state fetched from the server — naming the record and its kind's noun
(`song`, `songbook`, `Tata Ibadah`, `template`) — and only the confirmed submit SHALL POST to the
record's delete endpoint with the CSRF token. Hymn songbooks, their songs, a song of an already-deleted
songbook, and a record named through the wrong kind SHALL be refused by the endpoints. A deleted song
or songbook soft-deletes; a deleted service or template leaves the lists by its active flag. On success
the row leaves its sidebar and a neighbour takes focus; when the deleted record was the one on stage,
the shell swaps to the parent list with the history entry replaced, so Back never revisits the removal.

#### Scenario: revealing the delete control
- WHEN an eligible row is hovered or keyboard-focused (on a touch screen, drawn outright)
- THEN the trash control is drawn beside the pencil, and a dated service row's date is hidden for that reveal

#### Scenario: confirming the delete
- WHEN the trash control is clicked
- THEN the shared modal shows the record's name and its kind's noun with Delete and Cancel, and no request is made until Delete is pressed

#### Scenario: a confirmed delete lands
- WHEN the confirm submits and the server answers ok
- THEN the row leaves its sidebar and a neighbour takes focus; if the record was on stage the shell returns to the parent list with the history entry replaced

#### Scenario: refused and restricted records
- WHEN the row is a hymn songbook or a hymn song, the songbook is already deleted, editing is restricted, or the kind does not match the record
- THEN no control is drawn where the row can be identified, and the endpoints answer 404 or 403


