# Spec 022: Let the Tata Ibadah date picker overlap the editor modal

- **ID:** 022
- **Status:** Accepted
- **Item:** ITEM-024
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Keep the Tata Ibadah calendar fully visible and usable when it opens inside the modal's scrollable form area.

## Scope

### In scope

- Let the open calendar paint above the modal form content, including beyond the scrollable content's clipping edge.
- Keep it positioned beneath its date trigger and within the viewport.
- Preserve the current form layout height while opening the calendar.
- Maintain alignment when the modal content scrolls or the viewport changes.
- Preserve date selection, clear, keyboard navigation, Escape/outside-click dismissal, saved dates, and create-date defaults.

### Out of scope

- Changing selected-date, nearest-Sunday, validation, or submission rules.
- Changing other modals or popovers.

## Domain rules

- Opening the calendar does not expand or shift the editor form layout.
- The calendar remains visible, hit-testable, and selectable even where its bounds extend beyond the modal's scroll-content clip.
- The calendar remains inside the viewport; it is placed below the trigger when that fits and must not be clipped when it does not.
- Closing the modal or replacing its form removes the open calendar and its positioning behavior.

## Acceptance scenarios

### Scenario: Calendar overlaps the modal's scrollable content

- **Given** the Tata Ibadah editor is open and the calendar trigger is near the bottom of its scrollable content
- **When** I open the date picker
- **Then** the calendar paints above and remains interactive beyond the content's clipping boundary
- **And** the form content height does not increase

### Scenario: Calendar remains in the viewport

- **Given** the calendar is open near a viewport edge
- **When** the modal content scrolls or the viewport changes size
- **Then** the calendar stays aligned to its trigger and fully within the viewport

### Scenario: Existing date-picker behavior remains

- **Given** I use the calendar with pointer or keyboard
- **When** I select a date, clear it, press Escape, click outside, or close the editor
- **Then** the existing selection, clearing, dismissal, and cleanup behavior remains intact

## Traceability

- Domain/app tests: N/A; no date-domain rule changes.
- E2E: `tests/e2e/test_editor.py` — `test_date_picker_dropdown_overlaps_the_scrollable_modal_content` checks clipping escape, hit testing, fixed-height form, scroll/resize repositioning, viewport bounds, Escape, and modal-close cleanup; existing picker E2Es cover selection, clear, saved dates, defaults, and validation rerender.
- Implementation: `multimedia/web/templates/reading/_editor_form.html`, `static/web/date-picker.js`, `static/web/editors.js`, and `static/styles/design/components.css`.