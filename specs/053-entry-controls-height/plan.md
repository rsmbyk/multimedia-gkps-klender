# Plan 053: Give each entry the height of its floating controls

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-055
- **Bump:** patch

## Why

`.entry__acts` is `position: absolute; right: 8px; top: 8px` (`components.css:1501-1507`): the
Preview / Edit / Delete group (measured 36px tall on `/tatib/142/`) overlays the item's own box.
On entries without a title — most Text and Scripture entries — it lands on the first text line;
on titled entries it crowds the title. The owner wants the item's height to account for the
controls: reserve the band, start the words below it.

## Scope / edges

**In:**

- A top band (~44px: 8px offset + 36px controls) on every item that renders `.entry__acts`.
- A modifier in `tatib.html` so items without controls (editor off) reserve nothing.
- E2E in `tests/e2e/test_tatib_entry_controls.py`, incl. the existing over-the-text assertion.

**Out:**

- `tatib__eos` items, other panes, the add rows, spec 052's margin change.
- Control styling, position within the band, and reveal triggers.

## Approach

- Template: where the `entry__acts` span is emitted, also set `tatib__item--acts` on the enclosing
  `.tatib__item` — one condition, `item.preview or item.entry or item.old_item`, so the band
  appears exactly where the controls do.
- CSS: `.tatib__item--acts { padding-top: 44px; }` with the controls keeping `top: 8px` — they
  now sit inside the padding, above every word. The band scales with them if the controls change,
  since both derive from the same offset + height.
- The hover fill (spec 034) already paints the item's whole box, so the band is included with no
  extra rule.
- E2E: every entry's words start below the band; the untitled entry's controls never touch its
  text; the item's height includes band + first line; the band tracks the controls' own condition
  (the section break reserves none). The old over-the-text assertion is rewritten, not kept.

## TDD

- Domain/app tests: N/A (no server data).
- E2E (Playwright via `LiveServerTestCase`): `tests/e2e/test_tatib_entry_controls.py` — no overlap
  on titled and untitled entries; reveal/touch behavior unchanged; editor-off items carry no band.

## Risks

- **Taller items at rest.** Every entry grows ~44px; the pane is longer than today. Accepted by the
  owner's request — the band is spent space, and spec 052's collapse still nets a much tighter pane
  than the current one.
- **Title position moves.** Titles drop below the band, changing the pane's rhythm; owner reviews
  at Accept.
- **Existing geometry assertions.** `test_hovering_the_item_reveals_its_controls_over_the_text`
  encodes the old overlap; it must be rewritten, not just re-run.
