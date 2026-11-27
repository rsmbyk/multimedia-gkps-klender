# Contracts — spec 241

**Spec**: `specs/241-tatib-reorder-kept/spec.md`

## Interfaces exposed by this slice

none — the reorder endpoint, its payload, the sidebar grips and the stage markup are unchanged.
The only contract tightened is an internal one: `applyPaneOrder(what)` now reads the pane itself
and ignores pks with no node, and `endDrag()` clears `drag` before it calls that function.

## Not exposed

No new event, storage key, URL parameter or route. `shell:page` still resets the gesture's caches,
and `gkpsEditFeedback` still reports the one write.
