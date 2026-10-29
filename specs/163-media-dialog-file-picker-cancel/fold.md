# Fold: dismissing the file picker leaves the New media dialog open

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R32` | A dialog's `cancel` answers only the dialog's own dismissal: a `cancel` whose target is a descendant — the file input's, fired when the picker is closed without a choice or the same file is re-picked — no longer closes the New media dialog, which keeps its tab, chosen file, title, note and Save state; Escape and Cancel still close it with the same motion. Four scenarios: nothing chosen, a file chosen, the dialog dismissed, the library tab. |

**Before**: `reading` held 31 requirements (R1…R31). **After**: 32 (R1…R32).

## Drift guard

- **Files changed in this capability**: `static/web/media-entry.js` (one guard statement) and
  `tests/e2e/test_media_library.py` (four cases). No template, stylesheet, view or model.
- **Declared no behaviour change**: no — R32 is a new behaviour guarantee over an event the page already
  listened for; no pixel, copy or geometry moves.
