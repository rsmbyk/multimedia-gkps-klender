# Contract: the contents row (`toc_items` entry)

**Slice**: `specs/135-tatib-sidebar-row-clamp` · **Date**: 2026-10-26
**Status**: internal — no external interface changes; this is the seam between the server, the page
template and the saved copy.

## Parties

| Party | File | Role |
| --- | --- | --- |
| Producer | `multimedia/web/reading/views.py` — `_tatib_stage` | builds the list |
| Consumer A | `multimedia/web/templates/reading/_toc.html` | server-rendered page |
| Consumer B | `static/web/offline-render.js` — `servicePage` | page rebuilt from the saved library |

`reading.js` builds no row of its own: its in-place rebuild re-renders through the same template and
its drag ghost clones an existing row, so both inherit whatever the template emits.

## Shape

```python
{
  'eos': bool,            # a divider row: no label
  'anchor': str,          # 'ti-<anchor>' target
  'n': int,               # 1-based index in the order
  'entry': bool,          # a ServiceEntry (vs a legacy TataIbadahItem)
  'titled': bool,         # the row carries a title (not a continuation)
  'label': str,           # plain, lines joined by ' ' — the grip's accessible name
  'label_lines': [str],   # 1..3 lines, the last may end '…'
  'txt': str,             # whole entry text, lowercased by the consumer for the filter
  'song_label': bool,     # a song rendered as reference + title
  'song_reference': str,  # 'KJ 152', or '' for an ordinary songbook
  'song_title': str,
  'verse_line': str,      # 'Bait 1-3', or ''
  'pk': int,              # entry pk, for the grip
}
```

## Rules the consumers must hold

1. A row with `eos: true` draws the divider and no label.
2. Otherwise the label box is `.songrow__t` (plus `--song` for `song_label`), holding one `<br>`
   between consecutive `label_lines`.
3. A song row puts `song_reference` + `song_title` in `.songrow__heading` and `verse_line` in
   `.songrow__verses`, as separate blocks — no `<br>` between them.
4. Every line is escaped; `label_lines` entries are plain text, never markup.
5. `data-txt` is `txt` lowercased, so the filter matches text the row does not show.
6. The grip's `aria-label` uses `label`, never `label_lines`.

## Compatibility

`two_line_label` and the 60-character `label` are gone; both consumers change in this slice, and the
saved copy is re-rendered from the same server payload, so there is no version skew to carry.
