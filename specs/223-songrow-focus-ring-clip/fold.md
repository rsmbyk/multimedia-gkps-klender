# Fold: song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`
**Date**: 2026-11-22

## Capabilities touched

| Capability | Before | After | Operations |
| --- | --- | --- | --- |
| `reading` (`docs/spec/reading.md`) | R51 | R52 | `added` R52 with three scenarios; header's `slices` prepended with `223-songrow-focus-ring-clip`, `last folded` re-stated as 2026-11-22 |

## Delta

`### R52 — A focused song row's ring fits inside its list` states the behaviour the scrollport now
guarantees: enough room above the first row for its focus indicator, with no change to the row's
box, pitch, fills or the browser's outline rule. Its scenarios cover key-after-pointer focus, Tab
focus, and the unchanged unfocused/hover/selected states.

## Drift guard

| File | State |
| --- | --- |
| `static/styles/design/components.css` | changed — `.ch__body` top padding 0 → 3px |
| `tests/e2e/test_songrow_focus_ring.py` | added — three focus cases |
| `docs/spec/reading.md` | changed — R52 and header |
| `static/web/reading.js` | listed to prove it is untouched; focus logic unchanged |
| `templates/` (`multimedia/web/templates/`) | listed to prove no template changed |
| `static/styles/design/tokens.css` | listed to prove no token changed |

## Not folded

- The skipped candidate Clarify and its recorded assumption stay in the slice record, not in the
  capability tree: it is a decision about this slice, not a durable behaviour.
- The pre-existing empty-view regression belongs to ITEM-137, not this capability delta.
