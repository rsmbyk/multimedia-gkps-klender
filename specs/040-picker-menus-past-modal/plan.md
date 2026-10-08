# Plan 040: Let the entry modal picker menus extend past the modal

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-042
- **Bump:** patch

## Why

The book and song menus are `position: absolute` inside the dialog's scroll container
(`.editor__content { overflow-y: auto }`), so `placeMenu()` must clamp them to the dialog's box and
the options scroll in a cramped menu. The date picker already escapes the dialog
(`.editor__date-calendar { position: fixed }`, ITEM-024 / spec 022); the picker menus should do the
same, capped to the viewport.

## Scope / edges

**In:**

- The book picker (passage) and song picker (song) menus in the entry modals — add and edit alike.
- Menu positioned against the viewport: overlaps the dialog edge, never leaves the window, flips
  up/down, options scroll.

**Out:**

- The chapter / from-verse / to-verse selects, which are native controls.
- The date picker, which already behaves this way.
- Other modals and the projector.

## Approach

- `static/styles/design/components.css` — make `.editor__picker-menu` `position: fixed` (drop
  `left:0; right:0; top: calc(100% + 6px)`), raise its `z-index` above the dialog backdrop, and give
  it a viewport-based `max-height` like `.editor__date-calendar`.
- `static/web/entries.js` — `placeMenu()` currently measures `content` (`.editor__content`); measure
  the viewport instead, and set `left` / `width` from the trigger's rectangle plus `top` (or `bottom`
  when flipped). Keep the up/down choice and the options' own scroll.
- Reposition (or close) the fixed menu when the dialog's content scrolls and when the window
  resizes, so it stays anchored; the date picker's positioning code is the model.
- The same fragment and JS serve add and edit, so both follow.

## TDD

- Domain/app tests: N/A — client behaviour; the fragment's markup is unchanged.
- E2E: `tests/e2e/test_entry_pickers.py` — open the book menu in a passage modal and the song menu in
  a song modal near the dialog's bottom edge; the menu extends past the dialog, stays in the window,
  flips when there is no room below, and its options scroll.

## Risks

- **Detachment on scroll.** A fixed menu can drift when the dialog's content scrolls; reposition or
  close it.
- **Width and placement.** The menu must match the trigger's width and align to it, not the old
  `left:0; right:0` absolute box.
- **Two modals, one code path.** Add and edit share the fragment; verify both.
