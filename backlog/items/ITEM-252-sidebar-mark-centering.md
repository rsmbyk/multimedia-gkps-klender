---
id: ITEM-252
status: done
title: 'The service entry kind mark sits above the row centre'
type: fix
priority: P2
effort: S
created: 2026-11-24
updated: 2026-11-24
spec: 237-sidebar-mark-centering
branch: fix/237-sidebar-mark-centering
pr: 615
issue:
closed_at: 2026-11-24
closed_reason: merged into develop (PR #615)
bump: patch
release_version:
---

# ITEM-252: The service entry kind mark sits above the row centre

## Summary

The Tata Ibadah contents row centres its order number, but the kind mark added beside it
keeps baseline alignment. On a two-line song row the glyph sits 11.5px above centre,
breaking the number-and-icon rail the reader scans. Give the mark the same centring as
the number, including on the drag copy.

## Notes

The rows are a flex line with `align-items: baseline`; spec 063 already gave
`.songrow__c` its `align-self: center` under `:root[data-section="tatib"] #chList` and
`.reorder__ghost`. Spec 214 added `.songrow__mark` without that declaration. One more
selector pair on the same rule is enough — no markup, script or token change. The
slot's corner badge is positioned against the mark and follows it.

## Acceptance sketch

- One-line rows: mark centre 0px instead of −4px; two-line song row: 0px instead of −11.5px.
- Mark x 42px, label x 66px, row heights 38/53/74px unchanged; both themes.
- Drag copy's mark centred like its number; slot badge stays on the mark's corner.

## Links

- Spec: [237-sidebar-mark-centering](../specs/237-sidebar-mark-centering/spec.md)
- Related items: —
