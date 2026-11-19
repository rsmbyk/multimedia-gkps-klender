# Data model: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`

**No entities.** The slice changes where a run of text breaks inside three boxes in the dock's runner. No
model, migration, template, script or endpoint is touched; nothing is stored or fetched differently, and the
`TataIbadah` / `ServiceEntry` rows the page reads are unchanged.

The only shape involved is the box model, and it lives in the stylesheet:

| Box | Before | After |
| --- | --- | --- |
| `.serviceline` | `overflow-wrap: normal` (computed) | `overflow-wrap: anywhere` |
| `.entryrow__t` | `min-width: 0` | `min-width: 0; overflow-wrap: anywhere` |
| `.screenerow` | `overflow-wrap: normal` (computed) | `overflow-wrap: anywhere` |

The values the fixtures use are the widest the existing columns accept — `TataIbadah.name` and
`ServiceEntry.title` 64 characters, `ServiceEntry.media_filename` 255, a Text entry's `text` unbounded — so
no fixture asks the database for a value it cannot hold.
