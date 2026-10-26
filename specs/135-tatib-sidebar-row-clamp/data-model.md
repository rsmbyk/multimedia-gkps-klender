# Data model: a Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp` · **Date**: 2026-10-26

## Stored entities — no change

No model, migration, column or stored value changes. The 64-character `title` columns stay as they
are (`tatib/models.py:29`, `:117`, `songs/models.py:85`); a body stays a `TextField` split on `\n`
at render time.

## The row payload (`toc_items` entry) — changed shape

Produced by `_tatib_stage` (`multimedia/web/reading/views.py:997-1107`) and consumed by
`_toc.html` and `static/web/offline-render.js`.

| Field | Before | After |
| --- | --- | --- |
| `label` | capped at 60 characters (legacy: 60 + `…`) | the row's whole text, lines joined by a space — used by the grip's `aria-label` |
| `label_lines` | only on untitled text rows (2 entries) | every row: one string per line, at most three, the last carrying `…` when the server dropped text |
| `two_line_label` | boolean, untitled text rows and song rows | removed |
| `titled` | `bool(title)` | unchanged |
| `song_label`, `song_reference`, `song_title`, `verse_line` | songs | unchanged |
| `txt` | the whole entry's text, uncapped | unchanged |
| `clipped` | stage-only line-clamp flag | unchanged; also drives the sidebar's literal `…` |

### Line composition per kind

| Kind | Lines the server sends |
| --- | --- |
| Text, untitled | the body's first three lines; `…` appended to the third when the body has more |
| Text, titled | the title, split on its own newlines only (it has none) — one line |
| Passage | the citation, one line |
| Song | the heading (reference + title) and the `Bait …` line, as two entries — the heading's own lines are produced by the browser, capped at two |
| Media | the title, one line |
| Section break | the kind's name, one line |
| Legacy `TataIbadahItem`, untitled | the body's first three lines; `…` on the third when there are more |
| Legacy, titled | the title, one line |

### Invariants

- `label_lines` is never empty; a row with no text falls back to the kind's display name.
- When `label_lines` holds the whole text, no line ends in `…` (nothing is hidden).
- `label` equals `label_lines` joined by a space, so a screen reader never meets a newline.
