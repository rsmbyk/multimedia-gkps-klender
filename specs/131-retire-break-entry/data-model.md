# Data model: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`

`n/a — no field, relationship, constraint, index or migration change.` The retired kind keeps its stored value
(`ServiceEntryKind.SECTION_BREAK = 3`), its column and its rows; only the paths that **write** a new one stop.

## The kind's lifecycle after the slice

| Operation | Before | After | Where |
| --- | --- | --- | --- |
| Create (page) | `+ Break` in every add row, one `Add Break` tile | no control on any surface | `tatib.html`, `entries.js`, `offline-render.js` |
| Create (endpoint) | `POST /editor/entry/new/save/?tatib=N` with `kind=3` → `200` + row | `404`, no row | `entries.py` (`FORMS`) → `views.py::entry_save` |
| Read (stage) | one `.tatib__eos` divider, 56px box, no label | unchanged | `views.py::_service_items` → `tatib.html` |
| Read (sidebar) | one `.toc__eos` row with a grip | unchanged | `_toc.html` |
| Read (projector) | one blank screen, entry type `break` | unchanged | `views.py::_projector_data` |
| Read (saved page) | the same divider and add rows from the cache | divider unchanged, Break control gone | `offline-render.js` |
| Update (form) | `GET /editor/entry/<pk>/edit/` → a one-field form | `404` | `entries.py` (`FORMS`) → `views.py::entry_form` |
| Update (endpoint) | `POST /editor/entry/<pk>/save/` → `200` | `404`, row unchanged | `views.py::entry_save` |
| Delete | `POST /editor/entry/<pk>/delete/` → `200`, order compacted | unchanged, and proven | `views.py::entry_delete` |
| Reorder | drag / arrow keys → `/editor/entry/reorder/` | unchanged | `entries.js`, `views.py::entry_reorder` |

## What is deliberately not modelled

- **No `retired` flag, no `deleted_at`, no new column.** The kind's rows are ordinary rows the readers already
  understand; a flag would have to be read by every renderer to no visible effect.
- **No migration.** Existing `kind=3` rows are not touched, converted or renumbered.
- **No endpoint to "restore" the kind.** Reversing the decision is restoring the map entry in `entries.py`.

## Attributes the three creation surfaces agree on

| Attribute | Values | Written by | Read by |
| --- | --- | --- | --- |
| `data-entry-open` | `scripture` · `song` · `text` · `media` | the three surfaces | `entries.js`'s delegated click handler |
| `data-entry-tatib` | the service id | the three surfaces | the same handler |
| the empty row's grid | `repeat(4, minmax(0, 52px))`, `repeat(3, 52px)` under 300px | `components.css` | the browser |
