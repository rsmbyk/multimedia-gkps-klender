# Fold: The Transfers scrollbar sits at the dialog's edges

**Capability**: `docs/spec/media-library.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R1` | The whole block is replaced. `R1` keeps the seam's one 2px line, the list as the scroll container, the fixed title and the 22px the last row keeps above the dialog's border at the end of the scroll; it gains: a short list reserves **no lane**; the list's scroll area spans the dialog's inner box on the **right and the bottom**, so the bar paints against the right border with no canvas between them and its lane ends at the bottom border; the rows, title, age headings and the list's top do not move; the dialog **clips its content to its rounded border**, so the bar's bottom end is cut by the 12px corner. Two scenarios are appended — the bar at both edges with the last row still 22px clear, and the content unmoved. |

The capability already existed (created by spec 149), so this is a `modified` operation on `R1`, not
an `added` one. `R1`'s identifier is preserved.

**Before / after counts**: requirements 1 → 1 · scenarios 3 → 5 · capabilities 1 → 1.

## Drift guard

- **Files changed in this capability**: `static/styles/design/components.css` — the
  `.media-transfers__list` rule (its `margin` and `padding`) and the `.media-transfers__dialog` rule
  (`overflow: clip`); `tests/e2e/test_media_library.py` — four new tests and one older assertion
  restated (see `converge.md`)
- **Declared no behaviour change**: no — `R1` is the change, and it is the whole of it

No other capability's requirement moved: the rules are scoped to `.media-transfers__*`, and the tests
that changed belong to this dialog. The Media Library page's own list, the service-media dialog and the
reading surfaces are untouched, so nothing else is folded.
