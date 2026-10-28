# Fold: a media size reads in the unit that still shows its number

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R20` | A media size reads in the largest decimal unit in which its value is at least 1, one decimal only when it is not zero, promoted when it would round to `1000`; the New media card, a Media Library row and the Total draw it through one function. |

Before: 19 requirements · after: 20.

## Drift guard

- **Files changed in this capability**: `static/web/media-size.js` (new), `static/web/media-entry.js`,
  `static/web/media-library.js`, `static/web/media-handoff.js`,
  `multimedia/web/templates/reading/base.html`, `tests/e2e/test_media_library.py`
- **Declared no behaviour change**: no — every changed file is inside the capability, and `R20` is the change.
