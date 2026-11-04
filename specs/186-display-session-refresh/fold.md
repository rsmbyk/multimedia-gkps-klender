# Fold: a surface re-reads the session it shows

**Capability**: `docs/spec/display-state.md` (R3 added)
**Folded at**: 2026-11-04

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `display-state/R3` | a surface open across the end of a browser session re-reads on visible/focus/restore, and paints idle when the state is refused; the module compares and notifies only on a change, adding no key, message or verb |

## Drift guard

- **Files changed in this capability**: `static/web/display.js` (the re-read, its export and the
  fingerprint), `static/web/projector.js` (its own re-read, because the page does not load
  `display.js`).
- **Declared no behaviour change**: no — both files carry the delta above.
- **Not moved**: `overlay.md` R1 is unchanged — the overlay already re-read on `visibilitychange` and
  `focus`, and `obs-overlay.js` is untouched by this branch (`git diff --stat`).
