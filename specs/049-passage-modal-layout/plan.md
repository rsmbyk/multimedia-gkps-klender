# Plan 049: Center the TB/SIM switch and contain passage number pickers

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-051
- **Bump:** patch

## Why

In the supplied screenshot, the TB/SIM switch sits at the right edge of the Book field header, and the
Chapter, From verse, and To verse controls extend past the passage modal's content width. The modal
shows a horizontal scrollbar and the To verse control is clipped. Center the switch over the book
picker and make the three number controls fit the modal at narrow widths.

## Scope / edges

**In:**

- The scripture entry form in both add and edit passage modals.
- The TB/SIM switch on a centered row above the Book label; the Book label remains directly above the
  book-picker dropdown.
- Keep the Chapter control on its own full-width row, then place From verse and To verse together as
  a side-by-side range pair when they fit; stack that pair at 320px if needed.
- Preserve the existing form values, accessible names, translation selection, and save behavior.

**Out:**

- Changes to TB/SIM selection or book/chapter/verse data behavior.
- Picker-menu positioning or menu overflow behavior (spec 040), book filtering, and other modals.
- A broader redesign of the passage modal.

## Approach

- Put the TB/SIM switch on its own centered row above the Book label; keep the Book label directly
  above the book-picker trigger.
- Give Chapter its own row; pair From verse and To verse below it, using a narrow-screen stack where
  the pair would otherwise be cramped.
- Make the rows and picker triggers shrink or reflow within the modal's content box; keep every
  trigger fully visible and operable.
- Leave the native form-value controls and picker behavior unchanged.

## TDD

- Domain/app tests: N/A — layout-only change.
- E2E: `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_passage_form_layout_fits_modal_at_narrow_viewport` —
  from the home route, at 536×426 verify switch order/alignment, Chapter full width, paired From/To,
  no horizontal overflow, and action reachability; at 320px verify the range pair stacks and remains
  contained. Retain desktop and add/edit behavior coverage.

## Risks

- Keep the switch centered over the book picker at narrow widths while placing it above the Book label.
- A reflow can increase the modal's height; the existing vertical scroll must keep Save and Cancel
  reachable without introducing horizontal scrolling.
- Test geometry at a fresh narrow viewport and a desktop viewport; do not infer containment from the
  horizontal scrollbar alone.
