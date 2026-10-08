# Plan 022: Let the Tata Ibadah date picker overlap the editor modal

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-024
- **Bump:** patch

## Why

The calendar currently sits inside the modal's scrollable content. When it opens near the bottom of that scroll area, the modal clips the calendar, making dates hard or impossible to see and select. The calendar should float over the modal content while staying anchored to its field.

## Scope / edges

**In:**

- Tata Ibadah create/edit calendar opened inside the editor modal.
- Keep it visually above and interactive beyond the scroll-content clipping boundary, without changing modal content height.
- Keep the calendar aligned beneath its trigger and within the viewport; maintain placement as the modal content scrolls or the viewport changes.
- Preserve date selection/clearing, keyboard operation, dismissal, and existing Sunday defaults.

**Out:**

- Changing the date field, selected/default date rules, or service form behavior.
- Repositioning other popovers or redesigning the modal.

## Approach

Use a browser top-layer popover (or equivalent overflow-escaping mechanism) and position it from the trigger's viewport bounds. Add a focused browser regression that verifies the calendar paints and receives hit tests below the modal content clip, while remaining inside the viewport. Preserve the current in-modal dropdown behavior where there is room.

## TDD

- Domain/app tests: N/A; no date-domain rule changes.
- E2E: `tests/e2e/test_editor.py` — clipped-boundary overlap, viewport containment, and existing picker interactions.

## Risks

- Opening a top-layer calendar inside a native modal must preserve the modal's focus trap and Escape/outside-click behavior.
- Scroll and resize can invalidate a fixed position; update the position on relevant events and test the observable geometry.