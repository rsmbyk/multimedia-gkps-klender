# Fold: the projector's image placeholder waits for the image to fail

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R3` | The projector's image placeholder appears only when the image fails: the picture alone when the bytes arrive, the glyph alone when the load fails, neither while the fetch has not settled; the glyph is hidden by its `hidden` attribute and a screen that stops being active drops a failed state. Four scenarios. |

## Drift guard

- **Files changed in this capability**: `multimedia/web/templates/reading/projector.html` (the image box's
  placeholder gains `hidden`), `static/web/projector.js` (`renderImageScreen`'s two toggles and
  `clearImageScreen`'s reset).
- **Declared no behaviour change**: no — R3 is new, and the before/after is measured in the slice's
  preview (the picture moves from centre 920 to 960 on a 1920-wide stage; the glyph stops painting).
- **Before / after counts**: 2 requirements (`R1`, `R2`) → 3.
