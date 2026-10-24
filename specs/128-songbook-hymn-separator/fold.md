# Fold: Hymn songbooks above a single separator, the rest A–Z

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R4` | The Kidung panel lists hymn books first (descending song count), then the ordinary songbooks A–Z by folded name, with one separator between the groups, no heading, and no separator when a group has no rows; the order is the same on the index, a songbook page and a song page. |
| `added` | `R5` | A Kidung page rendered from the saved library draws the same two groups in the same order, using the same keys. |

## Drift guard

- **Files changed in this capability**: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/_songbooks_panel.html`, `static/web/offline-render.js`,
  `static/styles/design/components.css`
- **Declared no behaviour change**: no — every changed file is accounted for by R4 (the panel's grouping, order
  and separator) or R5 (the saved renderer's matching groups); the CSS file's one added rule is the empty-group
  guard R4 names.
