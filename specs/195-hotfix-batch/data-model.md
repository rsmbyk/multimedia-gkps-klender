# Data model — spec 195

No model changes. No migration.

- `ServiceEntry.verses` — JSON list of verse IDs, unchanged (spec 189). US4 changes only what the picker submits.
- `gkps-display` (localStorage) — shape unchanged (`service, screen, on, translation, at, session, goto`). US6 adds no write.
- The overlay's/dock's per-service screen cache — in-memory only; gains invalidation (message + timed re-read).

## Contracts

`contracts/` — **none**. Every interface this slice touches is the project's own client↔server pair, consumed only by this repo's scripts:

- `GET /editor/entry/song/<pk>/verses/` — JSON shape changes `verses: [numbers]` → `verses: [{id, number}]`; the only consumer is `entries.js` (changed in the same slice).
- `GET /projector?service=<id>` — unchanged; the poll is a new reader of an existing page.
