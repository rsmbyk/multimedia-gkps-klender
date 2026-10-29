# Fold: The Transfers list draws each boundary once

**Capability**: `docs/spec/media-library.md` (created by this slice)
**Folded at**: 2026-10-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R1` | The Transfers dialog draws each boundary once, and the list scrolls inside the dialog: one 2px `--divider` line at the session seam with 9px either side, 1px borders elsewhere, the title fixed, and the 22px bottom padding kept at the end of the scroll |

The capability did not exist before this slice, so the delta is a single `added` block rather than a
modification of `docs/spec/reading.md` — the Transfers dialog belongs to the Media Library, not to the
public reading surfaces that file describes.

## Drift guard

- **Files changed in this capability**: `multimedia/web/templates/reading/base.html` (one class on
  `#mediaTransfersList`), `static/styles/design/components.css` (the `.media-transfers*` block)
- **Declared no behaviour change**: no — `R1` is the change, and it is the whole of it

The template and stylesheet files carry many other surfaces; the delta is scoped to the
`.media-transfers*` rules and the one `base.html` line they need. No other capability's requirement
moved, so nothing else is folded.
