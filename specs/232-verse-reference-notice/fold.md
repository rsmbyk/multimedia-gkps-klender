# Fold — spec 232

**Date**: 2026-11-23
**Converged**: pass 1, 0 findings
**Capabilities touched**: `reading` only.

| Operation | Target | Delta |
| --- | --- | --- |
| modified | `reading/R40` — scenario `referenced verse cannot be deleted` | Full replacement block: the note now leads the action row with the exact copy and verse-level count, the disabled delete is neutral and is the note's `aria-describedby`, and at ≤650px the note takes its own full-width line. |

**Before / after**: `reading/R40` scenario headings 9 → 9; the referenced-verse block grows from one
WHEN/THEN pair to two (the narrow-width case). No `R<n>` added, removed or renamed.

The header `last folded` stays `2026-11-23` (already today) and `232-verse-reference-notice` is
prepended to `**slices**`. No other capability file changed.
