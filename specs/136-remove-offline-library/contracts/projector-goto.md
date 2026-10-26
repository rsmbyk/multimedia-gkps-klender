# Contract — the projector's Go To, and the removed offline routes

**Slice**: `specs/136-remove-offline-library` · **Producer**: Django (`multimedia/web/reading/goto.py`)
· **Consumer**: `static/web/projector-library.js` and `static/web/projector.js`

## `GET /projector/goto/index/`

- **200** `application/json` — `{schema: 1, books, songbooks, songs}` as `data-model.md` states.
- `Cache-Control: no-store` — the index is the page's freshness, so a reload must not serve a stale
  one. No `ETag`.
- No authentication: the projector page is public to the congregation's operator surface, as the
  offline chunk endpoints were.
- **Rules**
  1. `books` holds every Bible book with a `TB` or `SIM` edition, ordered by `pk`, each with its
     editions ordered by `pk`.
  2. `editions[].verses` is `[chapter, verse count]` pairs ordered by chapter — never a positional
     array, so a book whose chapters do not start at 1 still describes itself.
  3. `songs` rows are `[id, songbook id, number, sub-number, title]`, ordered by `pk`, with no lyric.
  4. `songbooks` holds every active songbook, ordered by `pk`.
  5. Nothing in the payload is a verse's text or a song's lyric; the test asserts the key set, and
     the size test pins the byte budget (SC-005).

## `GET /projector/goto/chapter/<int:book_id>/<int:chapter>/`

- **200** — `{schema: 1, book_id, chapter, label, editions: {<EDITION>: {name, verses: [{n, title, text}]}}}`.
- **404** — unknown book, or a chapter the book does not hold.
- `Cache-Control: no-store`.
- **Rules**
  1. Only editions whose version abbreviation is `TB` or `SIM` are included, as the browser library
     did; a book with neither yields `404`.
  2. Each edition's verses are ordered by `verse` and carry `n`, `title` and `text`.
  3. `label` uses the `TB` translation's name when it exists, else the first edition's.

## `GET /projector/goto/song/<int:song_id>/`

- **200** — `{schema: 1, id, label, screens, baits}` as `data-model.md` states.
- **404** — an unknown, deleted, or orphaned song.
- `Cache-Control: no-store`.
- **Rules**
  1. Verses are the live verses of the song, ordered by number; a deleted verse is never painted.
  2. Screen grouping matches `_line_pairs`: a blank line ends a screen, two lines make one, and each
     verse ends with a blank `bait_rest` screen.
  3. `baits[].start`/`end` index into `screens`, and every bait's range covers its own screens.

## Removed routes

| Path | Contract |
| --- | --- |
| `/offline/manifest/` | 404 |
| `/offline/chunk/<str:kind>/<int:pk>/` | 404 |
| `/offline/projector-shell/` | 404 |
| `/service-worker.js` | 404 |

Nothing may answer these with a redirect or an empty 200: a service worker that still holds a cached
copy must be unregistered by the page, and a 404 is what tells an old tab the route is gone.

## The loading lock (client contract)

While a Go To fetch is in flight (`gotoBusy`), the page SHALL:

1. keep `#projectorFind` open and refuse Escape, the dismiss overlay and its own close path;
2. disable `#projectorFindInput`;
3. mark the chosen row `is-loading` and replace its count with a spinner;
4. show a spinner 8px left of `.keys` in the corner cue;
5. return from every `keydown` handler before its shortcut branches run;
6. return from the mouse-zone, cue, row and dismiss click handlers.

The lock ends when the response paints, or when it fails and the error state replaces it.

## Compatibility note

The detour object the projector paints keeps its existing shape; only its source changes. A browser
running the old `projector.js` against the new server loses Go To entirely (its `GKPSOffline` is
gone), which is expected: the page and the server ship together in one deploy.
