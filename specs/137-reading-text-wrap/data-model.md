# Data model: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap`

**No entity changes.** No model, migration, payload or stored value moves. This file records the
boxes the rule applies to and the text properties each already carries, so the slice's effect is
readable without running it.

## The three roots

| Root | Where it is rendered | What lives inside it |
| --- | --- | --- |
| `.read` | `reading/base.html:405` — the reading article, its head and body | the page title (`.read__title`), eyebrow, section headings (`.read__sec`), verse and lyric lines (`.v`), Tata Ibadah body paragraphs (`.tatib__tx`), the verse reference line (`.read__sub`), the media library's own rows |
| `.search-results` | `reading/base.html:401`, drawn when the search has a query | result titles, meta lines, excerpts (`.result-row__title`, `.result-row__meta`, `.result-row__excerpt`) |
| `.preview` | `_preview_modal.html:3` — the Preview dialog | rendered lines (`.preview__line`), references (`.preview__ref`), the song heading (`.preview__song`) |

## Text properties, before and after

| Element | `white-space` | `overflow-wrap` before | `overflow-wrap` after | `overflow-x` |
| --- | --- | --- | --- | --- |
| `.read__title` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.read__eyebrow` | `normal` (the Tata Ibadah header sets `nowrap` for its date) | `normal` | `break-word` (inherited) | `visible` |
| `.read__sec` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.v` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.tatib__tx` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.read__sub` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.result-row__title` / `__meta` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.result-row__excerpt` | `normal` | `normal` | `break-word` (inherited) | `hidden` (two-line clamp) |
| `.preview__line` / `__ref` | `normal` | `normal` | `break-word` (inherited) | `visible` |
| `.book__n` | `nowrap` | `normal` | `normal` — unchanged | `hidden` (`…`) |
| `.media-library__filename` | `nowrap` | `normal` | `normal` — unchanged | `hidden` (`…`) |
| `.songrow__t` | `normal` | `anywhere` (spec 135) | `anywhere` — unchanged | `hidden` (three-line clamp) |

## What the rule changes for a reader

| Case | Before | After |
| --- | --- | --- |
| 64-character service title on `/tatib/149/` at 1440×900 | 1 line, 47px, painted 1,082px past a 400px box; the document scrolls 1,033px sideways | 4 lines, 187px, wholly inside the box; no sideways scroll |
| long song title on `/songs/1817/` | 2 lines, 93px, 444px past the box | 3 lines, 140px, inside it |
| Drive URL as a Text entry's body | 1 line, 215px past the box | 2 lines, inside it |
| a title that fits | 1 line, unchanged | 1 line, unchanged |
| a sidebar service row with a long name | 1 line ending `…` | 1 line ending `…` |
