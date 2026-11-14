# Phase 1 — Data model

**No model change. No migration.** Nothing is stored, fetched or validated differently: the mark is a
function of a fact the page already has.

## What the mark reads

`_tatib_stage` (`multimedia/web/reading/views.py:1012`) builds one dict per stage item and already
carries everything the template needs:

| key | source | used by the mark for |
| --- | --- | --- |
| `kind` | `entry_forms.kind_name(row.kind)` — `scripture` \| `song` \| `text` \| `media` \| `section_break` | choosing the glyph; absent on legacy rows, which are never marked |
| `title` | `row.resolve()[0]` (references, hymn labels) | the mark is drawn only when the row has a heading to sit in |
| `subtitle` | the song's `Bait …` line | nothing — the mark ignores it |
| `deleted_target` | `row.target_deleted` | nothing — the mark survives it (FR-007 of the spec's edge cases) |

## Derived facts, stated once

- **Marked kinds** = `{scripture, song}`. Every other kind renders exactly as today.
- **Glyph** = `scripture → open book`, `song → flagged note`; both are 24-viewBox stroke paths, so the set
  is data in the template, not a lookup table in Python.
- **Seat** = the row's absolute 24px left, 20 × 20, vertically centred; the row's own `padding-left`
  becomes 64px — the media row's number, reused rather than a new token.
- **Invariants** — the mark carries no text, no `tabindex`, no pointer events, and
  `aria-hidden="true"`; the row's accessible name is unchanged.

## What does *not* change

- `ServiceEntry`, `TataIbadah`, the media model, any serializer, any endpoint, any query.
- The sidebar's service list (`_tatib_panel.html`) and the OBS dock's entry list (`obs-dock.js`) — the
  spec's FR-008 keeps them as they are.
- The projector (`_projector_data`) and the preview modal (`_entry_preview`) — both build their own
  markup and neither draws stage rows.
