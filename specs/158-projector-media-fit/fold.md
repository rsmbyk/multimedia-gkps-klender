# Fold: a small image or PDF page fills the stage

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R6` | An image screen is painted at the smaller of the stage's two ratios — above 1:1 as well as below — whole, centred, aspect kept, and re-fitted when the window's size changes. Three scenarios: an image smaller than the stage, one larger, and a resize. |
| `added` | `R7` | A PDF or PowerPoint page is painted at the same ratio, at the display's pixel ratio up to the painter's 6-megapixel cap; the reader's Preview dialog keeps its own never-above-1:1 rule. Two scenarios: a Letter page on a wide stage, and the dialog left alone. |
| `added` | `R8` | `T` switches a media screen to fit width, then to fit height, alternating; the default fit is one of the two, so the first press offers the other. The fit resets on another entry and persists across one document's pages; every other screen kind is unaffected (a passage still flips TB/SIM). Three scenarios: the two states, a page turn versus another entry, a passage flip. |
| `added` | `R9` | The shortcut sheet lists `T` under a group naming images and PDFs, and keeps its 677 px height at 1080p so it still fits a 1280×720 window. One scenario: the sheet on a 720p window. |
| `added` | `R10` | The overflow left by a fit is panned by dragging and by the wheel (`deltaY`, `deltaX`, `Shift`+`deltaY`), clamped so no gap shows, reset to the centre with the fit or the screen, and never eating the corner's click (a press of 4 px or less is still a click). The pointer reads `grab`/`grabbing` while it overflows; with nothing overflowing the wheel is inert. Three scenarios: dragging a zoomed page, the wheel, a press that does not move. |

**Before**: `projector` held 5 requirements (R1…R5 — R3 spec 157's image placeholder, R4 spec 156's
playback control, R5 spec 155's recording lock). **After**: 10 (R1…R10).

## Drift guard

- **Files changed in this capability**: `static/web/projector.js` (the fit, its two states, the pan and
  the key), `static/web/media-pdf.js` (the painter's optional fit option), `static/styles/design/projector.css`
  (the fitted screen and the grab cursor), `multimedia/web/templates/reading/projector_controls.html`
  (the sheet's new group), and `tests/e2e/test_image_display.py`, `tests/e2e/test_pdf_display.py` (their
  acceptance cases). Nothing outside the projector's own surface: no view, model, endpoint or migration.
- **Declared no behaviour change**: no — R6–R10 are new behaviour over the same screens. What did not
  change, by name: the reader's Preview dialog (its sizing and its 1:1 clamp), the corner cue's contents,
  the passage `T`, the arrows, the cue's page counter, and every other screen kind.
