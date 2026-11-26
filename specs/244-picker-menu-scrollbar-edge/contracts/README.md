# Contracts: picker popout scrollbar edge

**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`

## Interfaces exposed by this slice

none — the change is one CSS rule set on `.editor__picker-menu` / `.editor__picker-options`; no
endpoint, payload, event, DOM attribute or script API changes, so there is nothing for another
component to consume.

## Not exposed

- The scrollbar's drawing stays the app-wide spec 087 contract (5px, `--scroll-thumb`, no steppers);
  the slice only moves the scrollport it is painted against.
- `placeMenu()`'s inline width/height/top/bottom contract with the picker menus stays as it is.
- No new CSS custom property or class name: existing selectors carry the change.
