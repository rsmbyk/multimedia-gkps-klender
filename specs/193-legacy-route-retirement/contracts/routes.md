# Contracts: Retired Addresses

**Slice**: `specs/193-legacy-route-retirement` · **Phase 1** · **Written**: 2026-11-14

The slice's one external interface is HTTP: which address answers what. Every row below is a
promise to a bookmark, to OBS's browser source, or to the archive. Query strings are kept on every
redirect; `Location` is always an absolute path on the same host; the status is 302 everywhere
except the three pre-existing `/songs/books*` moves, which stay 301.

## Retired addresses (302)

| Address (both slash forms) | Status | Destination | Requirement |
| --- | --- | --- | --- |
| `/home` | 302 | `/` | FR-001 |
| `/manage`, `/manage/…` (any depth) | 302 | `/` | FR-002 |
| `/obs/bible/dock` | 302 | `/obs/dock` | FR-003 |
| `/obs/songs/dock` | 302 | `/obs/dock` | FR-003 |
| `/obs/tatib/dock` | 302 | `/obs/dock` | FR-003 |
| `/obs/bible/source` | 302 | `/obs/blank` | FR-004 |
| `/obs/songs/source` | 302 | `/obs/blank` | FR-004 |
| `/obs/tatib/source` | 302 | `/obs/blank` | FR-004 |
| `/obs/project/source` | 302 | `/obs/blank` | FR-004 |
| `/obs/project/settings` | 302 | `/` | FR-005 |

## Pre-existing moves, re-pointed (301)

| Address | Status | Destination | Requirement |
| --- | --- | --- | --- |
| `/songs/books` | 301 | `/songs/` | FR-011 |
| `/songs/books/<id>` | 301 | `/songs/book/<id>/` | FR-011 |
| `/songs/songs/<id>` | 301 | `/songs/<id>/` | FR-011 |

These keep 301 because their moves were published as permanent before this slice; re-labelling
them now would not reach a cache that already holds them, and would only make the slice's status
codes less uniform. What changes is the destination: their old targets were `/manage/` routes,
which this release retires.

## The archive (302, one hop)

| Address | Status | Destination |
| --- | --- | --- |
| `/archive`, `/archive/` | 302 | `/` |
| `/archive/home/` | 302 | `/` |
| `/archive/manage/songs/12/` | 302 | `/` |
| `/archive/obs/songs/source` | 302 | `/obs/blank` |
| `/archive/obs/songs/dock/` | 302 | `/obs/dock` |
| `/archive/songs/` | 302 | `/songs/` |
| `/archive/songs/books`, `/archive/songs/books/12`, `/archive/songs/songs/12` | 302 | `/songs/`, `/songs/book/12/`, `/songs/12/` — the 301 targets, not the 301 addresses |
| `/archive/nowhere/` | 302 | `/nowhere/` (which then 404s as it would unarchived) |
| `/archive/%5Cevil.example` | 302 | `/` — a path a browser could read as `//evil.example` never leaves this host |

The destination is computed by `retirement.successor()` from the same module the direct routes are
built from, so no archive row is ever a second hop: `/archive/manage/songs/12/` does not pass
through `/manage/songs/12/`, and `/archive/songs/books` does not pass through the 301 at
`/songs/books`.

A query string on the archive address is carried onto the destination, exactly as on a direct
retirement.

## Live surface this slice adds (200)

| Address | Status | Body | Requirement |
| --- | --- | --- | --- |
| `/obs/blank` | 200, `Cache-Control: no-store` | transparent document; one fixed note bottom-right — `Old OBS source` at 20% white, `Switch to /obs/source/overlay` revealed on hover | FR-006, FR-006a, FR-006b |

No script, no image, no stylesheet link, no text beyond the note.

## Unchanged

| Address | Status |
| --- | --- |
| `/`, `/search`, `/songs/`, `/songs/<song>/`, `/songs/book/<book>/`, `/tatib/`, `/tatib/<service>/` | as today |
| `/obs/dock`, `/obs/source/overlay`, `/projector`, `/projector/…` | as today |
| `/bible/…`, `/media-library/…`, `/editor/…` | as today |

## Not exposed

Nothing else. No CLI, no API payload, no settings key is added: the retirement is read from a
Python module at import time, and `/obs/blank` takes no parameters.
