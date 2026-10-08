# Plan 037: Reveal the add rows before and after a hovered item

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-039
- **Bump:** patch

## Why

An item's add row sits only below it, and only that one is revealed on hover
(`.tatib__item:hover + .entry__add`). When the operator is on an item, they should be able to insert
on **either** side of it, so hovering it should reveal the add row above it too.

## Scope / edges

**In:**

- Hovering an item reveals the add row immediately above it and the add row immediately below it.
- Keyboard focus within an item reveals the same pair.
- The first item's "above" row is the leading start bar (spec 030); the last item's "below" row is its
  own trailing bar.

**Out:**

- The add actions and their endpoints.
- The floating controls (spec 033) and the item highlight (spec 034), beyond staying coherent with
  them.
- Bar behaviour when hovered directly — that stays as spec 036 defines it (only that bar shows; no
  item highlight).

## Approach

- The bars already exist: one `.entry__add` after each item, plus the leading start bar (spec 030).
  No new markup is strictly needed except confirming the leading bar is present for item one.
- **CSS cannot select a preceding sibling**, so add a small JS hover/focus toggle: on entering an
  item, add a reveal class to the item's preceding and following `.entry__add`; on leaving, remove it.
  `static/web/entries.js` already delegates item actions and owns the add bars, so it is the natural
  home; `static/web/reading.js` swaps the pane, so re-bind via delegation, not held nodes.
- `static/styles/design/components.css` — replace the single `.tatib__item:hover + .entry__add`
  reveal with a class-based reveal (for example `.entry__add.is-revealed`), keeping the delayed fade.
- Move the pointer off the item onto a bar: the item's reveal clears and, per spec 036, only that bar
  shows.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the pane still renders a bar after each item and the
  leading start bar (spec 030).
- E2E: `tests/e2e/test_tatib_entry_controls.py` — hovering an item reveals the bars above and below
  it; focus does the same; hovering a bar shows only that bar with no item highlight.

## Risks

- **Delegation.** The pane is swapped in place (`reading.js`), so the hover handling must be delegated
  or re-bound, not attached to nodes that get replaced.
- **Flicker.** The pointer crossing from the item to an adjacent bar must not flicker the pair on and
  off; the delayed fade and a sensible enter/leave scope should smooth it.
- **First/last item.** The first item's "above" row is the start bar, which only exists when the
  service has items (spec 030).
