# Contracts: song verse editing on the song page

**Spec**: `specs/189-song-verse-editing/spec.md`

## Interfaces exposed by this slice

| Interface | Kind | Defined in | Consumed by |
| --- | --- | --- | --- |
| `POST /editor/verse/new/save/` | HTTP, CSRF | `contracts/verse.md` | song page add modal |
| `POST /editor/verse/<pk>/save/` | HTTP, CSRF | `contracts/verse.md` | song page edit modal |
| `POST /editor/verse/<pk>/delete/` | HTTP, CSRF | `contracts/verse.md` | edit confirmation |
| `POST /editor/verse/reorder/` | HTTP, CSRF | `contracts/verse.md` | song page grip ghost drop |
| `GET /editor/entry/song/<pk>/verses/` (picker) | HTTP | `contracts/verse.md` | service entry form (ID value, current-number label) |
| Resolved body / `Bait …` line | derived read (not wire) | `contracts/verse.md` | stage, projector, list, summary line |

All writes enforce: ordinary songbook only, live song only, POST + CSRF, permutation of live verse IDs belonging to the named song, lyric non-blank. Failures: 403/404/400 whole-refusal, page re-reads (FR-013).

## Not exposed

- Live internal renumbering steps and FLIP/ghost geometry — pure front-end, not a contract.
- Migration script name — internal; only its effect (IDs + same lyrics) is observable.
- Setlist payload shape — frozen deliberately (FR-015); no new read exposed.
- Display write beyond lyric text — `static/web/projector.js` `reflow()` behaviour unchanged.
