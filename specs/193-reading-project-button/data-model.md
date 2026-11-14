# Data model — Project button on the song and Bible pages

**No model changes.** No migration, no field, no endpoint. The slice reads three things the
templates already receive and writes nothing to the database.

## What the templates read

| Template | Existing context used | Source |
| --- | --- | --- |
| `reading/song.html` | `song.pk` (the Go To pointer's `song_id`), `verse_rows` (the verse-less gate) | `SongDetailView.get_context_data` (`views.py:2313-2360`) |
| `reading/bible.html` | `book_id`, `read_no` (the chapter), `read_lang` (the shown edition, `tb|sim`), `read_state` | `BibleView.get_context_data` (`views.py:2163-2262`) |
| `reading/base.html` | none new — the new `{% block read_row_actions %}` is empty by default | existing shell |

## Shapes the slice produces (all unchanged, restated for the reader)

**Display state** `localStorage['gkps-display']` — `{service, screen, on, translation, at, session,
goto}` (spec 184 session-stamped). Unchanged.

**Go To pointer** — `{kind: 'song', song_id, index}` or `{kind: 'passage', book_id, chapter, verse,
translation: 'TB'|'SIM'|null}` (spec 185, `gotoOf`). Unchanged; the reading pages write the same
pointer the dock's find band writes.

**Channel message** — `{type: 'goto', goto: <pointer|null>}` on `gkps-service-display`. Unchanged.

**Detour payloads** — `/projector/goto/song/<id>/` and `/projector/goto/chapter/<book>/<chapter>/`,
`no-store` JSON. Unchanged.
