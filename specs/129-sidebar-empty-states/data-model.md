# Data model: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`

`n/a — no entity, field, relationship, constraint, migration or payload changes.` The block is composed per
render and typed in the browser; nothing is persisted and no endpoint changes.

## The block's own attributes

| Attribute | Values | Written by | Read by |
| --- | --- | --- | --- |
| `id` | `panelEmpty` (first column) · `chEmpty` (second column) | `base.html` | `reading.js`, `entries.js`, `offline-render.js` |
| `data-empty-title` | the section's "nothing yet" title | `views.py` (`PANEL_META`/`CH_META`) | `paintListEmpty` |
| `data-empty-hint` | the invitation that goes with it | `views.py` | `paintListEmpty` |
| `data-filter-title` | the section's "nothing matched" title | `views.py` | `paintListEmpty` |
| `data-filter-hint` | `Try a different search.` | `base.html` (one shared sentence) | `paintListEmpty` |
| `data-state` | `empty` · `filter` (absent while hidden) | `reading.js` | `components.css` (`[data-when]` rules) |
| `hidden` | present while at least one row matches | `reading.js` | the browser |

## The six copies

| Column | Section | Empty | Filtered |
| --- | --- | --- | --- |
| first | Alkitab | `No books yet.` / `Add a Bible edition to start reading.` | `No matching books.` |
| first | Kidung | `No songbooks yet.` / `Add a songbook to start collecting songs.` | `No matching songbooks.` |
| first | Tata Ibadah | `No Tata Ibadah yet.` / `Add the first service to start preparing it.` | `No matching Tata Ibadah.` |
| second | Alkitab | `No chapters.` / `This edition has no text in this book.` | `No matching chapters.` |
| second | Kidung | `No songs yet.` / `Add the first song to this songbook.` | `No matching songs.` |
| second | Tata Ibadah | `No sections yet.` / `Add the first item to start preparing the service.` | `No matching sections.` |

The Bible's second column is never filtered and never empty in practice; its row exists so the block is never
blank if it is ever shown (FR-010 keeps it hidden).

## Transitions

| From | Event | To | Who |
| --- | --- | --- | --- |
| hidden | list has no rows | `empty`, shown | boot paint, filter run, entry delete, saved render |
| hidden | list has rows, none match | `filter`, shown | `applyFilter` / `applySongFilter` |
| `empty` or `filter` | a row matches | hidden | `applyFilter` / `applySongFilter` |
| `empty` or `filter` | in-page navigation | the arriving page's copy and glyph, then the arriving filters decide | `navigate` (`reconcileNode` + the filter re-run) |
