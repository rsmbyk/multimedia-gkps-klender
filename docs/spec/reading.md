# reading

**capability**: `reading`
**last folded**: 2026-10-28
**slices**: `148-media-library-refresh-flicker`, `143-add-bar`, `142-entry-surface`, `140-stage-link-affordance`, `141-projector-window-reopen`, `139-home-search-center`, `138-sidebar-overlay-stack`, `137-reading-text-wrap`, `136-remove-offline-library`, `134-sidebar-save-freshness`, `126-songbook-short-header`, `127-site-name-tab`, `128-songbook-hymn-separator`, `129-sidebar-empty-states`, `130-empty-service-tiles`, `131-retire-break-entry`, `132-tatib-sidebar-date-buckets`, `133-text-modal-large-frame`, `135-tatib-sidebar-row-clamp`

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

### R22 — The Media Library's file list is drawn once per refresh, and holds still

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
