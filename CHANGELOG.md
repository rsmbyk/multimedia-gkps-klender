# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-adoption history in the legacy per-version format is archived in
[`docs/CHANGELOG-archive.md`](docs/CHANGELOG-archive.md).

## [Unreleased]

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
