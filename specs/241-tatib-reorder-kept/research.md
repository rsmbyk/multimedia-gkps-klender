# Research — spec 241

**Spec**: `specs/241-tatib-reorder-kept/spec.md`
**Date**: 2026-11-24

## Decision

1. Scope `applySongOrder()` to rows whose `.songrow` carries `data-t`, `data-o` and `data-m`.
   With fewer than two such rows it returns without touching `#chList`; with several it swaps
   only those rows among their own slots, leaving other children in place.
2. End the drag *before* rewriting the pane: `endDrag()` sets `drag = null` just before
   `applyPaneOrder(order())`, so a `pointercancel`/`blur` raised by the rewrite cannot call
   `cancelDrag()` and rewind the drop.
3. `applyPaneOrder()` reads the pane at call time, builds the moving units only from pks that
   exist, never emits an undefined node, and moves only children whose position changed.

## Rationale

- The captured stacks on the base commit were `applyPaneOrder <- endDrag` (n=59), then
  `applyPaneOrder <- cancelDrag` (n=56, missing the dragged unit), then `window.blur`, then the
  POST carrying the pre-drag order. Nulling `drag` first makes the second path inert.
- The sidebar's order after an edit was `[4, 1, 2, 3]` where the server returned
  `[1, 2, 3, 4]`: `applySongOrder()`'s `appendChild` moved every `.songrow` (contents rows
  included) to the end, leaving the `toc__eos` break at the top.
- The stage lost a section after an add-then-drag because `nodes` was cached before the add and
  `applyPaneOrder()` mapped `body.children` one-to-one against it. Reading at apply time and
  skipping unknown pks removes both the loss and any `undefined` child.

## Alternatives

| Alternative | Rejected because |
| --- | --- |
| Re-render the service from the server after every save and drop | breaks the in-place refresh contract (spec 134/225) and is far slower than a client reorder |
| Remove `applySongOrder()` from the shared refresh path | would restore the spec 233 regression: a chosen song sort would silently revert |
| Guard `cancelDrag()` with a one-shot flag instead of ending the gesture first | leaves the stale node cache and the one-to-one pane map, so a section can still vanish |
| Identify song rows by a section or route check | `#chList` is shared across sections; the row's own data attributes are the stable discriminator |

## Provenance

- Base commit `c06e8c97`, Chromium at 1440×900, `/tmp/opencode/diag_*.py` timelines.
- `tests/e2e/test_reorder.py` red/green evidence (three new tests).
- Server rendering verified complete for every service inspected, including service 322;
  the fault is client-side.
