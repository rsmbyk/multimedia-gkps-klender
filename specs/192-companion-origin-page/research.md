# Research: The companion's page manages this computer's origins

**Spec**: `specs/192-companion-origin-page/spec.md`
**Unknowns remaining**: 0

## D001 — Where the recorded origins live

- **Decision**: the recorded set is a JSON array persisted in the existing `settings` key/value
  table of `index.sqlite3` (key `origins`), read into an in-memory list at start and rewritten on
  every mutation.
- **Rationale**: the table already exists and holds exactly this kind of value (`retention`,
  `inventory_at` — `multimedia/local_media.py:184,231`); the library already owns the DB lifecycle
  (`_db()` context manager), so persistence, restart-survival (US2/AC5) and volume semantics
  (removed with `down -v`) come for free.
- **Alternatives considered**: a dedicated `origins` table (heavier than one row for a small
  ordered list); a JSON file beside `index.sqlite3` (a second persistence mechanism to keep
  consistent with the DB — rejected).
- **Provenance**: research (`multimedia/local_media.py:170-232`).

## D002 — How the runtime set reaches the enforcement points

- **Decision**: the recorded list lives on `LocalLibrary` as an in-memory list mutated only through
  the CRUD methods (which persist); `MediaHandler._allowed()` and `TransferManager` read
  `library.allowed_origins()` (= frozen env seeds ∪ recorded) per use, so a page change takes
  effect without a restart.
- **Rationale**: today `MediaHandler.origins` is a frozen class attribute set in `main()`
  (`local_media.py:626`) and `TransferManager.app_origins` is a frozen tuple captured at
  construction (`local_transfers.py:35`); both must see the live set. The library is already shared
  by both (`local_media.py:624-625`), so it is the natural owner; mutations ride the same
  `ThreadingHTTPServer` request threads, serialised like `_slide_lock`.
- **Alternatives considered**: mutating the class attributes on change (two places to keep in sync,
  and a restart of the *process* is still needed today — exactly what FR-003 removes).
- **Provenance**: research (`local_media.py:464-473,616-630`; `local_transfers.py:33-35,108`).

## D003 — How the page itself is served

- **Decision**: the page ships as one self-contained HTML file in the package
  (`multimedia/companion_page.html`) and `do_GET('/')` serves it as `text/html` on the loopback
  Host check alone — before any allowlist consult — with the JSON endpoints at
  `GET/POST/PUT/DELETE /v1/origins` and `GET /v1/fonts`.
- **Rationale**: the companion is a stdlib `BaseHTTPRequestHandler` app with path routing
  (`local_media.py:498-519`); a page file in the package travels inside the image with no static
  mount, and serving it before the allowlist consult satisfies US1/AC3 (the page works with an
  empty recorded set).
- **Alternatives considered**: a `/config` path (an extra name for the only page — rejected); a
  Django-side page (the companion must work when Django is down; the spec puts it on the
  companion).
- **Provenance**: research (`local_media.py:498-519,521-536`).

## D004 — The config surface's own authorisation

- **Decision**: page and config endpoints require the loopback Host (today's check) and an
  `Origin` that is either absent (top-level navigation) or the companion's own origin
  (`http://127.0.0.1:<PORT>` / the localhost form); the media session token is not consulted.
- **Rationale**: a top-level navigation sends no `Origin` header, so today's `_allowed()` — which
  requires an allowlisted `Origin` — would refuse the page itself. Same-origin fetches carry the
  companion's own origin; a cross-site page cannot produce it (browsers set `Origin`
  authentically), and the loopback Host check plus Private-Network preflight already gate remote
  pages. The token guards *allowed* origins' writes; this page *is* the configuration surface, on
  the same trust boundary as the `.env` it replaces.
- **Alternatives considered**: requiring the media token for config writes (it is handed to
  allowlisted web origins via `/v1/status` — wrong audience, and the page must work with an empty
  recorded set); no Host check (weaker than today).
- **Provenance**: research (`local_media.py:470-496,538-541,609-627`).

## D005 — How the fonts view enumerates directories

- **Decision**: `GET /v1/fonts` runs `fc-list <dir> --format '%{family}\n'` per mounted directory
  (`/usr/share/fonts/host/*`, then the operator directory) and returns unique family counts per
  directory; the launcher passes the host sources it mounted as labels through the font override
  file it already writes (an `environment` block setting `GKPS_MEDIA_FONT_LABELS`), so the page can
  show which host directory each mount came from; a directory with zero families is listed with
  `0 families`, and no directories at all is the outright none-found line.
- **Rationale**: `fc-list` is present in the image (probed in the running container:
  `/usr/bin/fc-list`, 296 files under `/usr/share/fonts/truetype`); the converter already resolves
  families through fontconfig (spec 182), so counts agree with what conversion sees. The container
  cannot know the host paths by itself — only the launcher knows them.
- **Alternatives considered**: walking directories and counting files (counts files, not families —
  disagrees with the converter's inventory); a Python font parser (new dependency); no labels
  (the page shows bare container paths — loses the slice-182 troubleshooting story).
- **Provenance**: research (`docker exec` probe of the running media container, 2026-11-14;
  `docs/local-media-companion.md:99-135`; spec 182 → `media-library/R4`).

## D006 — The refusal payload

- **Decision**: the 403 payload becomes
  `{"error": "Origin is not allowed. Record this computer's origins on the companion's page at http://127.0.0.1:<PORT>/."}`
  (message built from `PORT`), sent without CORS headers — unchanged.
- **Rationale**: FR-003 requires the refusal to name the page; the payload text is what
  `media-library.js`'s `request()` already turns into `new Error(data.error || …)`
  (`media-library.js:19`), so the surfacing (FR-008) rides the existing plumbing.
- **Alternatives considered**: a separate `config_url` field (the web app would need new plumbing
  for one string — the message already carries it).
- **Provenance**: research (`static/web/media-library.js:19,150-171`).

## D007 — Where the web app surfaces the reason

- **Decision**: `refresh()`'s failure path keeps the error instead of discarding it
  (`next.error = error.message`) and `setStatus` shows it in the status popup as the connection
  line's companion text; when absent, today's bare `Unavailable` stays.
- **Rationale**: today the failure is swallowed
  (`media-library.js:170`: `catch(function () { … status = null … })`) and the label degrades to
  `Unavailable` (`media-library.js:35`) — exactly the generic text FR-008 replaces. The popup is
  where the operator already looks for connection state.
- **Alternatives considered**: alerting (the page already alerts for transfer errors — a status
  reason is not an action); surfacing in the picker only (the popup is the connection surface).
- **Provenance**: research (`static/web/media-library.js:19,35,150-171`).

## Open

<!-- empty — Phase 0 finished -->
