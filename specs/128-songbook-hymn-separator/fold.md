# Fold: Hymn songbooks above a single separator, the rest A–Z

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R4` | The Kidung panel lists hymn books first (descending song count), then the ordinary songbooks A–Z by folded name, with one separator between the groups, no heading, and no separator when a group has no rows; the order is the same on the index, a songbook page and a song page. |
| `added` | `R5` | A Kidung page rendered from the saved library draws the same two groups in the same order, using the same keys. |
| `modified` | `R4` | The empty view shows whenever no group has rows — first load with no songbook as well as after the filter empties both groups; while one group still has rows, only that group shows, with no separator and no empty view (FR-008, owner, 2026-10-25). |

## Drift guard

- **Files changed in this capability**: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/_songbooks_panel.html`, `static/web/offline-render.js`,
  `static/styles/design/components.css`, `static/web/reading.js`
- **Declared no behaviour change**: no — every changed file is accounted for by R4 (the panel's grouping, order
  and separator, and its empty view) or R5 (the saved renderer's matching groups); the CSS file's one added rule
  is the empty-group guard R4 names, and `reading.js`'s one added call runs the filter R4's empty states are
  computed by.
