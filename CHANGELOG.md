# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-adoption history in the legacy per-version format is archived in
[`docs/CHANGELOG-archive.md`](docs/CHANGELOG-archive.md).

## [Unreleased]

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
