# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-adoption history in the legacy per-version format is archived in
[`docs/CHANGELOG-archive.md`](docs/CHANGELOG-archive.md).

## [Unreleased]

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
