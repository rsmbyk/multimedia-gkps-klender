# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-adoption history in the legacy per-version format is archived in
[`docs/CHANGELOG-archive.md`](docs/CHANGELOG-archive.md).

## [Unreleased]

## [1.13.2] - 2026-10-16

### Changed

- Bible book labels follow the active TB/SIM edition, including SIM abbreviations, Simalungun
  testament headings, and the visible translation's chapter title. Both editions' book codes work
  in sidebar, projector, and passage-picker searches; the three main rail popups use Bibel,
  Doding, and Agenda in SIM.

### Fixed

- Existing SIM translation rows receive abbreviations in place, and fresh Bible seeding stores the
  same 66 codes without replacing full names or verse links.

## [1.13.1] - 2026-10-16

### Fixed

- The Bible Version choice stays selected in the Bible sidebar and returns on a compatible Bible
  chapter after switching from Kidung or Tata Ibadah in the same tab. It still resets on refresh
  and remains isolated per tab.

## [1.13.0] - 2026-10-16

### Added

- Edit requests for songbooks, songs, Tata Ibadah, service entries, reorder, and custom screen
  breaks now share per-action progress and result toasts, with modal and duplicate-action guards
  while writes are pending.

### Fixed

- Service-entry deletion stays locked until its updated reading view is applied; a failed readback
  now reconciles the accepted deletion locally. In-page navigation patches changed reading and
  sidebar components while keeping unchanged nodes mounted.
- Sidebar and service-entry Add/Edit forms open a cancellable loading dialog immediately, ignore
  repeated opens, and discard late responses after dismissal.

## [1.12.0] - 2026-10-15

### Added

- The public reading app and service projector can open from saved browser shells and an offline library of Bible, songs, and Tata Ibadah data.
- The offline library syncs changed records in the background, exposes its status, and supports local Go To search in the projector.
- Reading navigation uses the saved shell and retains independent search history state per tab.

### Changed

- Bare-number projector Go To now cycles through every matching song number across hymn books, ordered by exact, prefix, then substring match.

## [1.11.0] - 2026-10-14

### Added

- The mirrored Tata Ibadah projector now has a quiet corner cue, entry list, shortcut sheet, keyboard and mouse navigation, and temporary passage or song detours.

### Changed

- Projected headers stay at the top while text fits the remaining stage; the HUD and pointer fade after inactivity and return on activity unless the HUD was deliberately hidden.

## [1.10.11] - 2026-10-14

### Fixed

- Selecting another Bible book from the mini sidebar keeps the book panel mini while opening that book's chapter list. The selected book can still toggle its chapters, and the expand control still opens the panel.

## [1.10.10] - 2026-10-13

### Fixed

- The Preview header's verse-tabs container is no longer named `preview__tabs-host`, whose name contains the `preview__tab` substring the "a single-verse song shows no tabs" test probes for. Rendering is unchanged; the served markup now says what it means.

## [1.10.9] - 2026-10-13

### Fixed

- Opening a Tata Ibadah service from the first-level panel brings its contents pane with it again. The sidebar state preserved on a stage-only swap is the first-level panel's (`data-nav`), not the contents pane's (`data-ch`) — a regression from 1.10.1.

## [1.10.8] - 2026-10-13

### Fixed

- The scrollbars no longer carry the platform's up/down buttons, and they are slimmer and softer: 5px instead of 6px, with a lighter thumb (and a still-clearly-stronger hover) in both themes. The root cause was the standard properties and the custom pseudo-elements both being set — in Blink the standard ones win, which reinstates the platform's 10px bar with its stepper buttons and ignores every `::-webkit-scrollbar` rule; they are now gated behind `@supports not selector(::-webkit-scrollbar)`.

## [1.10.7] - 2026-10-13

### Changed

- Modals (the entry form and the entry Preview) now separate from the page properly: a deeper scrim behind them, a lift of their own, and a hairline edge, so a dialog reads as a sheet above the page instead of a barely-different panel in it. The confirm layer inside the Preview follows the same scrim.

## [1.10.6] - 2026-10-13

### Added

- The entry Preview dialog names what it is showing: a Text entry's title, a passage's reference, or a song's heading, in a header that stays put while the body scrolls. A song's verse tabs move up beside the heading. An entry with no name still opens the headerless dialog it had before.

## [1.10.5] - 2026-10-13

### Changed

- The search-first home's helper line now reads "Try Yoh 3:16 or HAL 411"; both examples resolve against the corpus.

## [1.10.4] - 2026-10-13

### Changed

- The Bible translation switch (TB/SIM), in the reading header and in the passage picker, now fills the hovered option the way the Text screen-mode switch does, instead of only darkening its label.

## [1.10.3] - 2026-10-13

### Fixed

- The Tata Ibadah sidebar lists only the services of the mode it is showing: a dated order no longer appears under the templates (and the other way round) as a "Currently open" card. The open service is highlighted when it is in the list on screen.

## [1.10.2] - 2026-10-13

### Fixed

- The row being dragged in a Tata Ibadah's contents list now counts up with the order it is taking, instead of showing the number it had when it was picked up.

## [1.10.1] - 2026-10-13

### Fixed

- Opening a page from a second-level sidebar — and saving a service entry — keeps a collapsed or mini first sidebar as it was, instead of springing it open again.

## [1.10.0] - 2026-10-13

### Added

- Tata Ibadah uses one Text entry with Multi-line or Single-screen projection selected on Create and changed from Preview. Custom screen breaks stay editable in Preview, with confirmation before changing back to a default.

### Changed

- Existing Single-screen Text entries now use the unified Text kind while retaining their words, order, custom breaks, and projector screens.

## [1.9.4] - 2026-10-13

### Fixed

- Switching Tata Ibadah between dated orders and templates now keeps the open service and entry sidebar, with its exact service selected and visible in either list.

## [1.9.3] - 2026-10-13

### Fixed

- Switching reading menus now clears both sidebar filters and restores full lists while keeping the home search query.

## [1.9.2] - 2026-10-13

### Fixed

- Home search and both reading sidebar filters now use matching, centered clear controls with enough input space for typed text.

## [1.9.1] - 2026-10-13

### Fixed

- Tata Ibadah service-entry quicklinks can replay the stage flash after it finishes; activations during a flash no longer restart or queue another one.

## [1.9.0] - 2026-10-13

### Changed

- Mouse and pen reordering of Tata Ibadah service entries now starts from the entire sidebar row while preserving quicklink clicks, touch scrolling, and keyboard grip controls.

## [1.8.1] - 2026-10-13

### Fixed

- Song verse tabs in the Tata Ibadah Preview modal now keep equal 30 × 30px circular shapes for single- and double-digit numbers, with horizontal scrolling on narrow screens.

## [1.8.0] - 2026-10-13

### Added

- The first reading sidebar now collapses after 60 seconds without interaction when it matches the open reading page; Bible uses its mini sidebar state.

## [1.7.0] - 2026-10-13

### Added

- Tata Ibadah Text entry previews let editors place and remove projector screen breaks, with automatic two-line grouping until customized.
- Single-screen Text entry previews now use the same break controls, starting with one fitted screen and allowing custom screens across paragraph spacing.

## [1.6.8] - 2026-10-13

### Fixed

- Clicking text in a long Tata Ibadah Preview now lets arrow keys scroll its body without moving the page behind the dialog.

## [1.6.7] - 2026-10-13

### Changed

- Tata Ibadah service entries and section breaks use the approved quiet fill, inset outline, and 8px/8px/8px/12px padding in light and dark themes.

## [1.6.6] - 2026-10-12

### Changed

- Scrollbars in the public reading UI now use a slim, rounded, theme-aware style across pages, sidebars, dialogs, dropdowns, and text fields.

## [1.6.5] - 2026-10-12

### Fixed

- The Tata Ibadah date label now aligns vertically with the Project button without changing other reading headers.

## [1.6.4] - 2026-10-12

### Fixed

- Every song entry on the Tata Ibadah stage states the verses it keeps under its heading (`Bait 1-3`), not only when some verses are left out. The stage line now always matches the sidebar's second line, and a deleted song or verse still shows only its warning.

## [1.6.3] - 2026-10-12

### Fixed

- A Tata Ibadah entry keeps its highlight and its Preview, Edit, and Delete controls while a modal opened from it is showing, so it stays clear which entry the modal is about. The highlight clears only after the modal closes.

## [1.6.2] - 2026-10-12

### Changed

- The public reading rail uses one theme button again. It cycles System, Dark, and Light, with the icon and tooltip showing the selected mode.

## [1.6.1] - 2026-10-12

### Changed

- Entry numbers in the Tata Ibadah contents list sit at the vertical middle of their row, so multi-line entries (a quoted text, or a song with its verse line) read with an even numbering column. Text position, row size, and the songbook song list are unchanged.

## [1.6.0] - 2026-10-12

### Added

- The public reading theme control now offers Light, Dark, and System. System is the default for readers without a saved preference and follows changes to the device theme while the page is open.

## [1.5.1] - 2026-10-12

### Fixed

- Service entries clear their highlight and floating controls after pointer-opened Preview, Edit, or Delete modals close with the pointer elsewhere. Real hover, visible keyboard focus, and touch controls remain available.

### Changed

- Tata Ibadah song rows now distinguish the hymn reference, song title, and selected verses with separate typography. Long titles wrap above the verse line, and dark mode keeps the smaller verse label at readable contrast.

## [1.5.0] - 2026-10-12

### Added

- Liturgy lines in a Tata Ibadah are colored by who speaks them, on the projector, on the reading page in both themes, and in the entry preview. The screen faces the congregation, so their own lines keep the ordinary off-white. A leader line (`L`, `P`, Liturgis, Paragenda, Pendeta, Pdt, Pelayan, Pemimpin, Parambilan) is a quieter warm cue (`#9C8463` on the screen, `#866B50` on the light page). A joined line (`P+K`, `L+J`, `P/J`, `PJ`, and the same joins) is a readable teal (`#8EC2CC`, light `#2B5A64`) that marks it as theirs to say. A line with no speaker keeps the previous voice within the same entry, even onto the next screen. Songs and scripture are unchanged.

### Changed

- The reading page now lifts colon speaker marks (`Paragenda:`, `Jemaat:`, `P+J:`) as well as `L.`/`P.`/`J.`, and shows each mark the way it was written.

## [1.4.0] - 2026-10-12

### Added

- The service projector rests on a blank screen after every content entry, and after every verse of a song. That blank is not a section break, so it is not a row in the order.

## [1.3.23] - 2026-10-11

### Fixed

- The single-screen text editor's Save button now follows its Text field: the client guard attached to the text form alone, so a filled single-screen field kept the button disabled until the next page load. Both text kinds share the guard now, and an empty or whitespace-only field still disables it.
- A section break no longer offers an Edit control, on the stage or in the sidebar — a break has nothing to fill in. Its Delete stays, and every other kind keeps its Edit.

### Changed

- "+ Break" adds the break at once, at its add row's position (or the end of the service from the empty-state button), instead of opening a form with no fields.
- Song entries in the Tata Ibadah sidebar now state the verses they keep on a second line (`Bait 1-3, 5, 6, 8-10`). The stage's `Bait` line uses the same run-collapsing format: three or more consecutive numbers become a range, pairs and singles stay comma-separated.

## [1.3.22] - 2026-10-11

### Changed

- Each Tata Ibadah entry is now a box that contains its floating Preview / Edit / Delete controls — at least 52px tall, its words centred on the box's centreline — replacing the 44px top band. The start bar collapses at rest and reveals with the first block like every other add row, a revealed row keeps equal 8px above and below its buttons in every state, consecutive entries sit on a uniform 12px rhythm, and the section break takes the same box with its rule centred.

## [1.3.21] - 2026-10-11

### Fixed

- The Tata Ibadah stage's entry-title links wear the theme's link colour — forest green `#1C5C3C` in light, lifted royal blue `#7C9CF0` in dark — instead of the browser's default blue, which dropped to 1.98:1 contrast on the dark canvas. The underline stays, and no other link changes.

## [1.3.20] - 2026-10-10

### Changed

- A Tata Ibadah song entry from a hymn book now reads by its short reference and title on the stage and in its preview modal (`HAL 3 — Sai puji Naibata`), like the section sidebar and the pickers; other songs keep their headings.
- A song entry that keeps only some of its song's verses now states them under its heading (`Bait 1, 3`); a full selection shows nothing.

## [1.3.19] - 2026-10-10

### Changed

- Each Tata Ibadah entry now owns the height of its Preview / Edit / Delete controls: a quiet 44px band at the top of the entry holds them, so the title or first line of text always starts below them instead of under them. The section break is unchanged.

## [1.3.18] - 2026-10-10

### Changed

- The Tata Ibadah pane's hidden add rows no longer reserve space: at rest entries sit as close together as with the editors off, and the `+ Passage / + Song / …` row expands in place when its entry is hovered or focused (touch devices see the rows outright). The section break keeps its rule with tighter margins (34px → 16px).

## [1.3.17] - 2026-10-10

### Fixed

- The New song picker searches hymn songbook short/full names and their substrings alongside song titles: `kj`, `kidu`, `maat`, and `kidung jemaat` list songs from matching hymn books within the existing 200-option cap; non-hymn book names remain title-only matches.
- The New song picker resolves a combined book-and-number-prefix reference, with an optional sub-number letter and trailing title: `kj 12` includes KJ/PKJ numbers 12 and 123 (plus sub-number variants), while `kj 12a` selects only that base number/sub-number.

## [1.3.16] - 2026-10-09

### Fixed

- The New song picker now searches songbook abbreviations, and selected hymn labels retain the short reference.

## [1.3.15] - 2026-10-09

### Fixed

- The passage editor now centers TB/SIM above the Book picker and keeps Chapter and verse pickers inside the modal at narrow widths.

## [1.3.14] - 2026-10-09

### Fixed

- Passage book picker search now hides non-matching books while matching both TB and SIM names.

## [1.3.13] - 2026-10-09

### Changed

- Untitled service-entry Text and Single-Screen Text sidebar labels now show up to the first two literal body lines, preserving blank lines, titles and the 60-character cap; the reorder grip stays centered on two-line rows.

## [1.3.12] - 2026-10-09

### Changed

- Replace the passage add/edit modal's chapter and verse selects with custom pickers, preserving dynamic options, submitted values and the disabled to-verse tip.

## [1.3.11] - 2026-10-09

### Added

- Add an in-place TB/SIM toggle to the passage-book picker; switching updates the selected translation without reloading chapter or verse controls.

## [1.3.10] - 2026-10-09

### Changed

- The add-song picker lists hymn books first by book id and in song-number order, then other songbooks by name and title order; hymn options show the short reference and title, unnumbered hymns follow by title, and the closed selection remains title-only.

## [1.3.9] - 2026-10-08

### Changed

- Passage book options now list each book once with the TB name primary and SIM name dimmed on the right; selecting stores the primary translation, filtering matches either name, and editing a saved passage preserves its current translation until another book is chosen.

## [1.3.8] - 2026-10-08

### Fixed

- The entry modal's book and song menus are capped to the viewport rather than the dialog: they may overlap the dialog's edge, never leave the window, flip up when there is no room below, and stay anchored while the dialog scrolls.

## [1.3.7] - 2026-10-08

### Changed

- In the Tata Ibadah sidebar a hymn song reads as its short reference and title (e.g. `KJ 435 Marolopolop Tondingki`); other songbooks keep their label.

## [1.3.6] - 2026-10-08

### Changed

- A section-break entry no longer has a label: the editor offers no label field and the divider shows none. A text entry keeps its title and a legacy end-of-section row keeps its note.

## [1.3.5] - 2026-10-08

### Changed

- Hovering (or focusing) an entry reveals the add row above it and the add row below it, so either side can be inserted into.

## [1.3.4] - 2026-10-08

### Fixed

- Hovering an item's add row no longer counts as hovering the item above: the row starts below the item, so the item is not highlighted and its controls stay hidden.

## [1.3.3] - 2026-10-08

### Changed

- A section break draws one clear full-width divider, the same for a legacy end-of-section row and a section_break entry, with its note beneath it.

## [1.3.2] - 2026-10-08

### Changed

- Hovering a service entry highlights the whole item with the shared hover tint, without moving the text.

## [1.3.1] - 2026-10-08

### Changed

- An entry's controls (preview, Edit, Delete) float at its top-right over the text on a brief backing, shown while the item is hovered or holds keyboard focus.

## [1.3.0] - 2026-10-08

### Added

- A read-only preview for a service entry: a headerless modal with the full text or passage, or a song's selected verses in numbered tabs, dismissed by Esc or a click on the overlay.

## [1.2.2] - 2026-10-08

### Changed

- A text entry's pane shows only its first three lines, hard-truncated with an ellipsis; the hidden remainder is marked so the preview can be offered.

## [1.2.1] - 2026-10-08

### Fixed

- The "add at the beginning" start bar gets its own markup, so it no longer collides with the per-item add controls.

## [1.2.0] - 2026-10-08

### Added

- Add a service entry at the beginning of a Tata Ibadah: a start bar above the first row inserts at order 1, shifting entries and legacy rows together.

## [1.1.0] - 2026-10-08

### Added

- A **Single-Screen Text** service entry kind: the whole body on one projector screen, the font shrinking to fit and only ellipsizing when it cannot shrink further.

## [1.0.2] - 2026-10-08

### Removed

- The projection pane no longer shows the **Update the current state** control; saved changes still reach the display on their own.

## [1.0.1] - 2026-10-08

### Removed

- The projection controls no longer print a status line beneath them; Update and the automatic stop-when-the-window-closes keep working without narrating.

## [1.0.0] - 2026-10-08

### Added

- Tata Ibadah forms use an accessible calendar popover with a default upcoming Sunday, keyboard selection, and a clear action.

### Changed

- **Breaking:** Songbooks no longer have a language field in their model, forms, or API responses. Same-name books are merged, their song references preserved, and names are globally unique.
- Tata Ibadah forms no longer expose first-section or active controls; new services start active and empty, while edits preserve activation.
- Dated Tata Ibadah headers show full Indonesian month names.
- Project and Stop projecting buttons use primary and danger treatments respectively.
- Resetting the reading home clears remembered search while ordinary sidebar browsing preserves it.
- The date picker shows a full, theme-aware Sunday emphasis and square date cells with rounded corners.
- The projection lock is removed: a Tata Ibadah's entries can be added, edited, deleted and reordered while it is being projected, from any tab of the projecting browser.
- A reorder is written as soon as it is dropped, or a keyboard move settles; the Save/Discard strip and the unsaved-order leave prompt are gone.
- The projector follows every saved change: an add, edit, delete or reorder makes the open display re-read by itself, without pressing Update the current state.

### Fixed

- Pointer-closing reading editors no longer leaves stale edit controls visible; automatic modal focus restoration no longer leaves row outlines or idle actions visible, while deliberate keyboard focus indicators remain visible.
- The Tata Ibadah date picker stays anchored above scrollable modal content and within the viewport.

## [0.11.4] - 2026-10-06

### Changed

- Songbook forms hide short name and hymn-book fields; edits preserve existing values, and new songbooks use model defaults.

## [0.11.3] - 2026-10-06

### Fixed

- Public hymn-book song lists now sort numerically by song number and case-insensitively
  by sub-number, with unnumbered legacy songs listed last.

## [0.11.2] - 2026-10-06

### Changed

- Light-theme selected reading-sidebar tint is now pale mint `#B9D7C9` for stronger near-black
  text contrast; dark-theme selection remains unchanged.

## [0.11.1] - 2026-10-06

### Changed

- Softer theme-aware selected-row tint for Bible books and chapters, songbooks, songs,
  and Tata Ibadah services; selected text remains readable in both themes.

## [0.11.0] - 2026-10-06

### Added

- The Tata Ibadah reading pane can edit or delete existing `TataIbadahItem` text and
  end-of-section rows in the shared editor dialog; the old OBS dock sees the same edits.

### Changed

- Old rows and new service entries share a contiguous running order. Existing services
  retain their visible order during migration; adding after either kind and deleting a row
  shift both kinds together. The pane, contents list, and service projector follow it.
- Existing entry reorder keeps old rows in their positions and repairs the shared order
  after a legacy API reorder. Old OBS pages, API routes, and response shapes stay in place.

## [0.10.0] - 2026-10-06

### Added

- Service entries let one Tata Ibadah hold text, scripture, song, and section-break items in
  one ordered list, with add/edit/delete controls in its reading pane.
- A separate service projector at `/obs/service/<id>/` displays the running order and keeps
  its browser-local display state separate from the existing OBS docks and sources.
- The Bible TB/SIM selector now has a persistent selected state and a transform-only moving
  highlight, synchronized on initial load and in-place reading navigation.

### Changed

- Service-entry reorder remains a draft until Save or Discard, and warns before a navigation
  can discard unsaved changes. The existing `TataIbadahItem` rows and API remain compatible.
- Songs, songbooks, and verses are soft-deleted: ordinary browse/search/API paths hide deleted
  targets, saved service entries retain their references and show a warning, and admin deletion
  records the actor and time without removing rows.
- Existing bookmark and song API payloads do not expose soft-delete metadata; writes and reorder
  reject deleted targets.

## [0.9.0] - 2026-10-03

### Added

- Sidebar editors (spec 005): a full-width accent add button below the filter in the
  songbook, song and Tata Ibadah sidebars, and a hover/focus-revealed edit control on every
  row of those lists. Each opens a modal — a native `<dialog>` in the reading design — that
  creates or edits the record through a server-rendered form, refreshes the page's regions
  in place on save, and shows validation errors beside their fields without closing.
- Songbook fields: name, short name, language, hymn flag. Song fields: number, sub-number,
  title, key — with the number required for a hymn. Tata Ibadah fields: name, date, active,
  plus an optional first section on create, because a service used to appear in the public
  lists only once it had one. (Since spec 006 every active service is listed, empty ones
  included, so an empty service can be opened and filled; its page says it is empty.)
- `SIDEBAR_EDITORS_REQUIRE_LOGIN` (default off): set it true to hide every editor control
  from anonymous visitors and refuse their writes with 403, without touching the UI code.

### Changed

- Hymn songbooks and the songs inside them are read-only: they render no edit control at
  all, checked against the data rather than a list of names, and their write endpoints
  refuse the request even when it is hand-crafted. That now includes *adding* a song: a
  hymn book shows no add button, and a hand-crafted create is refused like any other
  hymn-book write (found in review, where the create path had been left open).
- The forms mirror the models' own rules, so a duplicate short name, a duplicate
  `(book, number, sub_number)` and a numberless hymn are refused server-side; CSRF is
  required on every write.
- Song lists sort *last modified* (newest first, the file's own order breaking a tie) or
  *alphabetically*, whose key ignores a title's own leading `435. `. Without that, the two
  orders would be identical: every song in the corpus imports with one `modified` timestamp,
  so all rows tie and the alphabetical order is what the list already shows. The song list's
  add button also moved out of the toolbar to a full-width row below the filter, so the sort
  control keeps the place it has in the accepted mockup.
- Hovering a row's edit control no longer drops the row's hover styling, and the control
  carries a pointer cursor like the rest of the row.
- Escape inside an editor's modal closes only the modal: the page's own Escape handling
  looked through it and closed the sidebar behind it too.
- The Tata Ibadah mode toggle works when it is reached by clicking through from the home. Its
  link was relative (`?mode=template`), which only resolves on `/tatib/`; swapped into the home
  it became `/home/?mode=template` -- the search home -- so the panel closed and Alkitab
  appeared. It is absolute now, and it is synced (or removed) with its section, so it keeps the
  slot the mockup gives it instead of leaving the collapse there.
- Closing a sidebar no longer reveals a row's edit control: the row link kept focus, and
  `:focus-within` counted as hover.
- A rail tile's label no longer appears when a sidebar closes. Closing the panel returns focus
  to its tile on purpose (that is the focus management, and it is right), but the label was
  raised by *any* focus; it now answers keyboard focus only, via `:focus-visible`. Any tooltip
  still up when a sidebar's state changes is cleared at the transition.
- The add buttons are inserted from the page that arrives when the shell swaps a section in
  place. They sit outside the swapped regions, and the search-first home has no such button
  to update, so they used to be missing for anyone who landed on the home and clicked through
  to a section -- the path the site is designed around. Regression-tested on that path.

### Security

- **Accepted risk (owner decision, 2026-10-03): anyone may write through these forms.** The
  corpus of a publicly reachable deployment is editable by anyone who can reach it. The
  login hook above is the documented mitigation and the first thing to switch on before the
  site is exposed beyond the team.

## [0.8.0] - 2026-10-03

### Added

- Search-first public site: an icon rail (Search, Alkitab, Kidung, Tata Ibadah, theme
  toggle) and a landing page whose search spans the whole corpus — Bible books,
  references, and verse text; songbooks, titles, and lyrics; Tata Ibadah titles and
  public contents — with grouped results, counts, excerpts, and exact reference
  resolution (`Matius 5:13`, `Kidung Jemaat 120` ≡ `KJ 120`).
- Public reading views for Bible chapters (verse numbers, TB/SIM translation toggle) and
  Tata Ibadah service orders (year+month groups, Templates view, section quicklinks).
- Song-list sort control on non-hymn songbooks — *recently updated* (default, by a new
  `Song.modified` stamp; migration 0012) ↔ *alphabetical* — applied in place.
- Dark mode by rail toggle, persisted and applied before first paint, with the palette
  AA-safe in light and dark.

### Changed

- Public pages rebuilt on the design language from spec 001: hand-written CSS with no
  framework, a narrow rail with nested sidebars (mini collapse for Bible, wide song list
  for Kidung), keyboard/touch ergonomics, and print that yields reading content only.
- The shell now navigates in place: rail destinations, sidebar picks, search submits,
  result opens and *Show more* swap the affected regions under one URL, so panel
  animations play and the address bar never changes. Switching sections keeps the reading
  stage and returning rebuilds that section's lists from it.
- Sidebar clicks no longer scroll their lists: a row clipped at an edge is nudged only
  enough to become fully visible, and only reveals (opening the sidebar on the page being
  read, or opening a search result) centre a row.
- Reveals do that consistently now: the panel tile and the list row are both centred for
  every section — Tata Ibadah services included, whose rows were never revealed before — and
  the travel is animated so the rows before the target are seen. A Tata Ibadah contents item
  is flashed rather than selected, since quicklinks never carry a current state.
- The rail search icon only ever restores a real result set: a stored URL that is not one (an
  older build could leave a reading page there) is discarded instead of being opened.
- The brand logo now takes the same route as the search icon — back to the last result set
  rather than starting a fresh search.
- Every search and filter field has a clear (×) control, shown while the field holds a value;
  clearing re-runs the filter (or keeps the result set) and returns focus to the field.
- The last result set survives browsing away through the sidebars, and returning to it
  resumes the scroll offset it was left at.
- Search behaviors: any non-empty query searches — the minimum length and its inline
  message are gone — an empty submit is inert and keeps the last result set; the rail
  search icon restores the last result set, the logo starts a fresh search.

## [0.7.0] - 2026-10-01

### Added

- Maintenance mode (`MAINTENANCE_MODE`): the site root `/` serves a short notice
  (HTTP 503) while the reading home stays reachable at `/home/`.
- `[devops]` Local Docker Compose stack (`web` + `db`) on low-conflict ports
  from the IANA dynamic range, overridable via `WEB_PORT` / `DB_PORT` in `.env`.
  Container-internal ports stay conventional (`8000` / `5432`).

### Changed

- The public home moved from `/` to `/home/` while maintenance is on; `/` serves
  the home again when `MAINTENANCE_MODE` is off.

## [0.6.0] - 2026-09-30

### Added

- Public song-reading site at `/`: browse songbooks, read a song's lyrics, search by title or
  book number.
- A design language defined from scratch (`static/styles/design/`), with a palette drawn from
  the GKPS logo; public pages no longer depend on Fomantic UI.

### Changed

- The content editor moved from `/songs/…` to `/manage/…`; legacy paths redirect (301).
