# Fold: the empty notice leaves the stage

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R2` | **Was**: the page paints the response's screens and a service with no items shows its empty state. **Now**: the empty state is painted only while the stage holds nothing — a Go To detour on the stage hides the notice and takes its room (the detour is fitted to the full stage), closing the detour brings the notice back, and a re-read that ends with screens hides it in the same render while one that ends with none leaves it visible. The response-only rule is unchanged. |

## Drift guard

- **Files changed in this capability**: `static/web/projector.js` (the notice's one writer and its
  three call sites), `multimedia/web/templates/reading/projector.html` (read, not changed — the
  notice it renders), `docs/spec/projector.md` (this fold), plus the slice's tests and pack.
- **Declared no behaviour change**: no — the delta above is the behaviour change; every changed file
  inside the capability maps to `R2`'s modification, and no file changed without one.

## Not folded

none — every requirement converged and was folded. The edge case where a service loses its last
entry while the page is open stays declared in the slice and is **not** behaviour the tree claims:
the notice is server-rendered only when the response carries no screens.
