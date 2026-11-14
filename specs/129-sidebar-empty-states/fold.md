# Fold: The sidebars say which nothing they show

**Capability**: `reading` ([`docs/spec/reading.md`](../../docs/spec/reading.md))
**Folded at**: 2026-10-25

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| added | `R7` — a sidebar list's empty state says which nothing it is | one centred block per list (glyph, title, hint); the empty copy when the list has no rows, the miss copy when rows exist and none match, nothing when one matches; the first column names its list, the second its contents; hidden in the mini panel and beside the chapter tiles; the saved render copies both. Numbered `R7` on the rebase: `R4`/`R5` are spec 128's panel grouping and `R6` is spec 130's empty-service tiles, both folded before this slice, and `R<n>` is never reused |

`R1`–`R6` are untouched: this slice adds a requirement rather than modifying one. `R2` is the
requirement FR-008 leans on — a saved page shows its server route's content — and is unchanged.

## Drift guard

- **Files changed in this capability**: `multimedia/web/templates/reading/base.html`,
  `multimedia/web/reading/views.py`, `static/styles/design/components.css`, `static/web/reading.js`,
  `static/web/entries.js`, `static/web/offline-render.js`
- **Declared no behaviour change**: no — the empty-state copy, its position and its two states are R7 itself
- **Guard result**: every changed source file is named by R7 or by the R2 clause it serves. The four test
  files (`multimedia/web/tests.py`, `tests/e2e/test_reading.py`) and the slice's docs are the record, not
  behaviour. No other reading surface was touched, so nothing outside the tree can have drifted.
