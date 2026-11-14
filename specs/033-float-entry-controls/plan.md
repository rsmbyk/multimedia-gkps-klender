# Plan 033: Float the entry controls over each item, top-right

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-035
- **Bump:** patch

## Why

The entry-specific controls — preview, Edit, Delete — sit inside the per-item add bar below the
item, pushed to its far end, so acting on an entry means scanning down to the bar it happens to
share with the add actions. Move them into the item itself, floating at its top-right over the words,
with a brief backing so they stay legible.

## Scope / edges

**In:**

- The item's own element carries the controls: preview (ITEM-034 / spec 032), Edit, and Delete,
  positioned `absolute` at the top-right, drawn over the text.
- A brief surface behind the button group so it reads over the words.
- Reveal while the item is hovered **and** while a control has keyboard focus; on devices with no
  hover, the controls stay visible. (Owner's decisions: backing over the button group only; legacy
  rows included; no-hover devices always show.)
- Legacy `.tatib__eos` rows get the same top-right treatment for their Edit/Delete.

**Out:**

- The per-item add bar's four `+` actions, which stay where they are.
- The behaviour of the controls themselves (edit/delete/preview flows).

## Approach

- `multimedia/web/templates/reading/tatib.html` — move the `.entry__acts` span out of `.entry__add`
  and into the item element (`section.tatib__item`, and the `.tatib__eos` div). The eos branch must
  carry the entry's `data-entry-pk` / `data-entry-edit` / `data-entry-delete` (and the preview
  trigger) so its controls still resolve.
- `static/styles/design/components.css` — give `.tatib__item` / `.tatib__eos` `position: relative`;
  make `.entry__acts` `position:absolute; top/right` with a small rounded surface (existing tokens),
  and drop its `margin-left:auto`. Reveal on `.tatib__item:hover .entry__acts`,
  `.tatib__eos:hover .entry__acts`, and `:focus-within`; add an `@media (hover: none)` rule that
  keeps them visible.
- Keep the delayed fade the add bar uses, and make sure the reveal leaves no stale outline
  (spec 025 / ITEM-027).
- The preview button arrives with spec 032; this item only decides where the three sit.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the item element carries the three controls and the
  add bar no longer does; the eos row carries its entry controls.
- E2E: `tests/e2e/test_tatib_entry_controls.py` — hovering an item shows the controls over it;
  focusing a control by keyboard shows them; a no-hover context keeps them visible; no outline
  lingers after use.

## Risks

- **Overlap.** Floating controls can cover the first line of an item; the backing and position must
  keep the text readable.
- **Stale reveal.** Hover-only would strand keyboard users, and a mis-timed fade can leave a stray
  outline (spec 025).
- **The eos branch.** It is built differently (legacy rows); its controls need the entry attributes
  too or they will not resolve.
