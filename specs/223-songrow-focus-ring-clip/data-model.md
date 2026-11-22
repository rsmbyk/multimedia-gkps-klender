# Data Model: song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`

Nothing is stored and no payload moves. The slice models one transient DOM state and one geometric
relationship between an outline and the box that clips it.

## Entities

### Song row — focus state

| State | Where it lives | Entered by | Leaves by |
| --- | --- | --- | --- |
| **unfocused** | the DOM's focus | page load, a click elsewhere | Tab, a click on the row |
| **pointer-focused** | the DOM's focus, `:focus-visible` false | a pointer click on the row | Tab, a key press, focus elsewhere |
| **keyboard-focused** | `:focus-visible` true, the UA outline painted | Tab onto the row, or any key pressed while pointer-focused | focus leaving the row |

**Relationships**: one `#chBody` scrollport → many `.songrow` links; the clip belongs to the
scrollport, not to any row, so the fix is on the container.

## The geometry invariant

For every focused row, `row.top - host.top >= outlineWidth + outlineOffset` when the outline is
drawn outside the row. At the base these values are `0px` and `1px + 1px = 2px`, so the invariant is
false and the top edge is clipped. With candidate A they are `3px` and `2px`, so it holds with 1px
to spare. The bottom edge is covered by the existing 8px bottom padding.

## Invariants

- The row's box, text, pitch, hover fill and selected fill never change.
- The outline's own declaration is never touched; only the room around the row changes.
- The list stays scrollable, with the same last row; its scroll extent may grow by the 3px reserved
  at the top.

## Not modelled

- The browser's focus heuristic itself — owned by the browser and the product's existing focus code.
- Which row `aria-current` marks — owned by the reading stage.
- Candidate B's inset ring — a preview comparison, not shipped.
