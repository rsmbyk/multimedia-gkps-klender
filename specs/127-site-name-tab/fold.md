# Fold: The tab names the site, and the index's tab stops at the name

**Capability**: `reading` ([`docs/spec/reading.md`](../../docs/spec/reading.md))
**Folded at**: 2026-10-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| modified | `R1` — a song page's header cites its songbook by its short name | the tab scenario now reads `<header> — Multimedia GKPS Klender`; the citation rule is untouched |
| added | `R3` — the tab names the site, and the index's tab stops at the name | the two shapes: the index routes read the site name alone, every other reading page appends ` — Multimedia GKPS Klender`; visible and assistive text stay `GKPS Klender` |

## Drift guard

- **Files changed in this capability**: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/{base,home,bible,book,book_index,song,tatib,media_library}.html`,
  `static/web/offline-render.js`, `static/web/reading.js`
- **Declared no behaviour change**: no — the two shapes are R1's tab clause and R3 itself
- **Guard result**: every changed title file is named by R1 or R3. The templates' `alt`, `aria-label` and
  maintenance strings are outside the tree's title clauses and are recorded in `research.md` D005 as
  deliberately unchanged, so their absence from the delta is a decision rather than an omission.
