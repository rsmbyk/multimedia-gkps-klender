# Data model — remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Date**: 2026-10-26

No database change: no migration, no model field, no stored value. This file records the payloads the
slice adds and removes, because they are the contract between the server and the browser.

## Removed: the browser library

| Store | Held | Fate |
| --- | --- | --- |
| IndexedDB `gkps-public-library` / `chunks` + `meta` | every public chunk, keyed `bible:<pk>`, `songs:<pk>`, `service:<pk>`, with its revision and a committed generation | deleted on first load of the new code (`deleteDatabase`), never written again |
| Cache Storage `gkps-public-shell-*` | `/home/` and `/offline/projector-shell/` plus 22 static assets | deleted by the service worker's `activate`; the registration is unregistered, the worker file answers 404 |
| `localStorage` | none — the display state (`gkps-display`) is untouched | kept |

The store's shape (spec 092) is not reproduced here; it is removed whole, and its `16.89 MB` on this
database is the number that made it worth removing.

## Added: the Go To index (`GET /projector/goto/index/`)

Held in page memory by `projector-library.js`; never written to storage.

```json
{
  "schema": 1,
  "books": [
    {"id": 1, "name": "Kej",
     "editions": [
       {"v": "TB", "name": "Kejadian", "abbr": "Kej", "verses": [[1, 31], [2, 25], [3, 24]]},
       {"v": "SIM", "name": "1 Musa",  "abbr": "1Mu", "verses": [[1, 31], [2, 25], [3, 24]]}
     ]}
  ],
  "songbooks": [{"id": 1, "name": "Kidung Jemaat", "short_name": "KJ", "is_hymn_book": true}],
  "songs": [[12, 1, 152, "", "Ada Kuasa"]]
}
```

- `books[].editions[].verses` is a list of `[chapter, verse count]` pairs, ordered by chapter. The
  pair is used rather than a positional array because the chapter number is data: a book whose
  chapters do not start at 1 must still describe itself (the first implementation assumed 1..N and a
  fixture caught it). Measured invariant: every chapter's verses run 1..count with no gap (2,378
  chapter-edition pairs, 0 gaps), so the payload answers "does verse v exist" exactly, and the first
  verse of a chapter is 1.
- `songs` rows are arrays — `[id, songbook id, number, sub-number, title]` — because the row repeats
  once per song and the keys cost more than the data. `songbook id` points into `songbooks[]`;
  `number` is `""` for an unnumbered song; `sub-number` and `title` are `""` when empty.
- No verse text, no lyric, no service row. Measured size on this database: **101,883 bytes** raw —
  99.9 KB of it the songs, 27.2 KB the books — inside SC-005's 130 KB.

## Added: the chapter payload (`GET /projector/goto/chapter/<book_id>/<chapter>/`)

```json
{
  "schema": 1,
  "book_id": 40,
  "chapter": 5,
  "label": "Matius 5",
  "editions": {
    "TB":  {"name": "Matius", "verses": [{"n": 3, "title": "", "text": "…"}]},
    "SIM": {"name": "Mateus", "verses": [{"n": 3, "title": "", "text": "…"}]}
  }
}
```

- Both editions present when the database has them; an edition whose chapter is absent is omitted.
- `label` is the edition-neutral reference (`<preferred translation name> <chapter>`), used by the
  detour's cue until a verse is painted.
- The client builds each screen's `header` (`<edition name> <chapter>:<verse>` plus the verse title on
  a second line when there is one) and `line` (the trimmed text) exactly as the browser library did.

## Added: the song payload (`GET /projector/goto/song/<song_id>/`)

```json
{
  "schema": 1,
  "id": 12,
  "label": "KJ 152 Ada Kuasa",
  "screens": [{"blank": false, "header": "", "lines": [{"text": "…", "voice": ""}],
               "bait": 1, "split": 1, "split_total": 2}],
  "baits": [{"number": 1, "start": 0, "end": 2}]
}
```

- Built by the same grouping the projector already uses for a service's song entry
  (`_line_pairs`): blank lines split screens, two lines per screen, and each verse ends with a blank
  `bait_rest` screen. `baits` indexes into `screens`, as the browser's `songDetour` did.
- `label` follows the header rule: a hymn book's short name, number and sub-number uppercased, then
  the title; an ordinary songbook's title, then the songbook name.

## Removed endpoints

`/offline/manifest/`, `/offline/chunk/<kind>/<pk>/`, `/offline/projector-shell/` and
`/service-worker.js` answer 404. Nothing reads them after this slice; a stale service worker or an
old tab that still asks is answered by the 404, which is the honest answer for a removed route.

## Client shape (unchanged)

The detour the projector paints keeps its shape — `{kind: 'passage'|'song', label, …}` with
`translations` or `screens`/`baits` — so `renderDetour`, `renderDetourCue` and the step handlers keep
working. What changes is where the object comes from: a fetch on selection, and a fetch on a step that
leaves the loaded chapter.
