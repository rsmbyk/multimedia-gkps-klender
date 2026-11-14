# Plan 034: Highlight a whole service entry item on hover

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-036
- **Bump:** patch

## Why

Hovering an entry reveals the add bar below it and, with spec 033, its floating controls — but the
item itself never changes, so the row under the pointer is not obvious. Highlight the whole item on
hover, the way the sidebars highlight a row.

## Scope / edges

**In:**

- A hover background on `.tatib__item`, using the theme-aware `--icon-hover-bg` (already used by
  `.book:hover` / `.songrow:hover`), and on the legacy `.tatib__eos` row.
- The highlight also shows on keyboard focus within the item.
- The highlight must not move the text. (Owner's decisions: bleed to a comfortable row inset; legacy
  rows included; keyboard focus included.)

**Out:**

- The sidebar selected/`aria-current` tints (spec 008–010).
- The Bible and Kidung panes.
- Any change to the items' contents or order.

## Approach

- `static/styles/design/components.css` — add `.tatib__item:hover`, `.tatib__eos:hover`, and a
  `:focus-within` state that set `background: var(--icon-hover-bg)`, with a small border-radius.
- **No layout shift.** The items carry tight margins (`.tatib__item + .tatib__item { margin-top:
  2px }`); give the highlight padding and a matching negative margin (or inset it) so adding the
  background never nudges the text.
- A short fade, dropped under `prefers-reduced-motion`.
- Shares the hover state with spec 033's floating controls; the two must agree, and neither may
  leave a stale highlight/outline (spec 025).

## TDD

- Domain/app tests: N/A — this is a visual state with no server data change.
- E2E: `tests/e2e/test_tatib_hover.py` — the hovered item gets the background; the text does not
  move; `:focus-within` highlights; reduced-motion drops the fade.

## Risks

- **Layout shift.** The classic padding mistake; keep the negative margin equal to the padding.
- **Two hovers at once.** The highlight and spec 033's control reveal fire on the same hover; keep
  them visually coherent and both free of stale state.
