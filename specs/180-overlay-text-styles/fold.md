# Fold: the overlay reads by kind

**Capability**: `docs/spec/overlay.md`
**Folded at**: 2026-10-30

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R1` | The overlay paints from the display state alone and carries no control |
| `added` | `R2` | A song screen paints the caption — recorded here as it stands from spec 119, because the capability file starts at this slice |
| `added` | `R3` | A passage screen paints a quotation card carrying the reference and the verse's title |
| `added` | `R4` | A liturgy screen paints a script panel carrying its title and its speaker turns |
| `added` | `R5` | A speaker mark sits in a column of its own, shared by the screen's turns |
| `added` | `R6` | Blank, media, break and released screens paint nothing |
| `added` | `R7` | Text arrives and leaves; a screen step morphs the panel's box; reduced motion gets a cut |
| `added` | `R8` | A flip repaints the heading and the words together |

**Before**: the capability file did not exist — 0 requirements, no header. **After**: 8 requirements, `last folded`
2026-10-30, slice `180-overlay-text-styles` prepended.

## Drift guard

- **Files changed in this capability**: `static/styles/design/obs-overlay.css`, `static/web/obs-overlay.js`,
  `multimedia/web/templates/reading/obs_overlay.html` (unchanged, listed to prove it),
  `multimedia/web/reading/views.py` (the screen payload's `mark` / `words`).
- **Declared no behaviour change**: no — the surface changed from "every text is a caption" to "a caption, a quotation
  card or a script panel, chosen by the entry's kind", plus its motion and the speaker column. Every changed file is
  accounted for by `R1`–`R8`.
- **Not folded**: nothing — Converge closed with no accepted gaps.

## Note on the new file

The capability did not exist before this slice: the overlay's behaviour since spec 119 lived only in that slice's
record. `R2` folds the caption as it stands today rather than restating spec 119, so that a later slice touching the
overlay has one file to read; the earlier behaviour that this slice does not touch (the page's own bootstrap, the
display channel's verbs) stays where it was written.
