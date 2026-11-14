# Plan 036: Keep the add bar out of the item hover

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-038
- **Bump:** patch

## Why

The entry controls now float in the item's own row (spec 033) and the item highlights on hover
(spec 034). The add bar sits directly under the item and, today, overlaps it by 4px
(`.tatib__item + .entry__add { margin-top: -4px; padding-top: 4px }`). That overlap lets the pointer
in the add bar's edge count as hovering the item — highlighting it and revealing its controls when
the operator only meant the add buttons. The add bar is not part of the item.

## Scope / edges

**In:**

- Hovering or focusing the add bar shows only its buttons: the item above gets no hover highlight and
  no floating controls.
- Hovering the item still reveals its add bar, as before.
- The item and its add bar still read as one ("add after this item") without overlapping.

**Out:**

- The floating controls' placement (spec 033) and the highlight's design (spec 034).
- The add actions themselves.

## Approach

- `static/styles/design/components.css` — remove the `-4px` / `4px` overlap so `.entry__add`'s box
  lies fully below `.tatib__item`'s; keep the visual spacing with margin alone, so
  `.tatib__item:hover` cannot match while the pointer is on the add bar.
- If a connecting overlap is kept for looks, isolate pointer events so the add bar's area is never
  part of the item.
- Keep the existing reveal: hovering the item still shows the add bar
  (`.tatib__item:hover + .entry__add`), and hovering/focusing the add bar still shows its buttons.

## TDD

- Domain/app tests: N/A — a hover-region change with no server data.
- E2E: `tests/e2e/test_tatib_entry_controls.py` — hovering the add bar leaves the item
  un-highlighted with its controls hidden, while the add buttons show; hovering the item still
  reveals the add bar.

## Risks

- **Losing the connection.** The item and its add bar must still read as one; keep the spacing
  without the overlap.
- **Regressing the reveal.** The item→add-bar reveal and the add-bar's own reveal both still hold.
