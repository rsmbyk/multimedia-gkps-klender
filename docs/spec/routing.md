# routing

**capability**: `routing`
**last folded**: 2026-11-14
**slices**: `194-legacy-route-retirement`

Which addresses the site answers and where an address that no longer exists sends the request. The
capability was created by spec 194, the release that retired the old OBS docks and sources and the
last `/manage/` addresses; before it, the only routing behaviour written down was each surface's own
page.

### R1 — A retired address answers 302 to its successor

An address this release retires SHALL answer exactly one 302 to its live successor, with or without a
trailing slash and with the request's query string kept: the old OBS docks send `/obs/dock`, the old
OBS sources send `/obs/blank`, and `/home/` and every `/manage/…` path send `/`. No retired address
SHALL answer a 301, because the release claims nothing permanent; `/songs/` and `/tatib/` SHALL keep
answering as they do. The three `/songs/books*` moves predate this release: they SHALL keep their 301
and SHALL name the reading pages (`/songs/`, `/songs/book/<id>/`, `/songs/<id>/`), never a retired
`/manage/` address. (spec 194)

**Scenarios**

- **Given** an OBS scene that still holds an old dock source, **When** that source is opened, **Then**
  the request lands on `/obs/dock` in one 302 and the operator sees the live dock.
- **Given** a bookmark to `/home/` or to `/manage/songs/12/`, **When** it is opened, **Then** the
  request lands on `/` in one 302, query string kept.
- **Given** an address opened without its trailing slash, **When** it is retired, **Then** the slash
  form answers the 302 itself rather than a 301 from the slash-adding middleware.
- **Given** `/songs/books`, **When** it is opened, **Then** it answers 301 to `/songs/`, and the song
  list is still live after the redirect.
- **Given** `MAINTENANCE_MODE` is on, **When** `/home/` is opened, **Then** it still answers 302 to
  `/`, which serves the maintenance notice.

### R2 — The old version is reachable for one release at `/archive/…`

`/archive/<old path>` SHALL answer 302 to the live successor of that path, computed from the same
table the direct retirements are built from, so the answer is one hop: an archived `/manage/…`
address SHALL NOT pass through `/manage/…`, and an archived `/songs/books` SHALL NOT chain through
its 301. An archived path with no successor SHALL answer the path itself, which then behaves exactly
as it would unarchived. The namespace is temporary: the release after this one removes it and decides
per address between a 301 and reuse. A path a browser would read as another host — a leading `//` or
a backslash — SHALL answer `/` or a same-host path, never a protocol-relative address. (spec 194)

**Scenarios**

- **Given** `/archive/manage/songs/12/`, **When** it is opened, **Then** it answers 302 to `/` in one
  hop, and its `Location` never names `/manage/`.
- **Given** `/archive/songs/books`, **When** it is opened, **Then** it answers 302 to `/songs/`, not
  to the 301 at `/songs/books`.
- **Given** `/archive/nowhere/`, **When** it is opened, **Then** it answers 302 to `/nowhere/`, which
  answers 404 exactly as it would outside the archive.
- **Given** `/archive//evil.example`, **When** it is opened, **Then** the answer stays on this host.

### R3 — An old OBS source lands on a transparent watermark page

`/obs/blank` SHALL answer 200 with `Cache-Control: no-store` and a transparent document carrying one
corner note and nothing else: `Old OBS source` at 20% white with a soft shadow at rest, and the live
overlay's address revealed on hover. The document SHALL carry no script, image or stylesheet link, so
a browser source that cannot load an asset still paints the note. The page belongs to the live OBS
surface and outlives the retirement it was written for. (spec 194)

**Scenarios**

- **Given** an old overlay source left in a scene, **When** it is opened on air, **Then** the viewer
  sees an empty frame and the operator sees a faint corner note.
- **Given** the note over a bright slide, **When** nobody interacts, **Then** it is swallowed by the
  picture.
- **Given** the note over any picture, **When** the operator hovers it in OBS's *Interact* window,
  **Then** it turns legible and names `/obs/source/overlay`.
- **Given** a browser source that cannot reach the project's stylesheets, **When** the page loads,
  **Then** the note is still painted, because its style travels in the document.
