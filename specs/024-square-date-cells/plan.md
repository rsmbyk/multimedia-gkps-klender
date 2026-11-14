# Plan 024: Make Tata Ibadah calendar date cells square

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-026
- **Bump:** patch

## Why

The date picker currently renders day cells about 39.4 px wide and 34 px tall. The owner wants square cells rather than short rectangles.

## Scope / edges

**In:** Equal width and height for all date cells and blank slots, responsive to the calendar's seven columns. Preserve Sunday emphasis, selected/today/focus states, and existing rounded corners.

**Out:** Changes to calendar logic, locale, defaults, submission, or other controls' shape.

**Confirmed by acceptance:** Square means a 1:1 width/height ratio, not sharp corners; retain the existing 8 px radius.

## Approach

Let each grid column determine cell width and use a 1:1 aspect ratio without minimum-height or default button padding distorting the square. Let the existing top-layer calendar accommodate the taller rows while retaining viewport-aware placement and scrolling when necessary.

## TDD

- Domain/app tests: N/A; geometry only.
- E2E: `tests/e2e/test_editor.py` — fail on unequal cell width/height, then verify all cells/blank slots across desktop/narrow widths and months with different row counts.
- Regressions: Sunday styling, selection/keyboard/clear, ISO submission, validation rerender, and popover overlap/viewport containment.
- Full browser suite remains deferred to push verification.

## Risks

Taller month grids must remain inside short viewports without clipping the date-picker focus ring or altering form height. Fractional grid widths require subpixel measurement tolerance.
