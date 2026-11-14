# Spec 049: Center the TB/SIM switch and contain passage number pickers

- **ID:** 049
- **Status:** Accepted
- **Item:** ITEM-051
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the passage modal's book controls fit and read cleanly at narrow widths: center the TB/SIM switch
over the book picker and stop the chapter/verse controls from overflowing the modal.

## Scope

### In scope

- The scripture entry form in add and edit passage modals.
- The TB/SIM switch is centered over the book picker and appears above the Book label; the Book label
  remains directly above the dropdown.
- The Chapter control on its own full-width row, followed by From verse and To verse together as a
  side-by-side pair when they fit; stack the pair at 320px if needed to avoid horizontal overflow.
- Existing accessible names, selected translation, form values, and save behavior remain unchanged.

### Out of scope

- Changes to TB/SIM or book/chapter/verse selection semantics.
- Open picker-menu positioning and viewport capping (spec 040), book filtering, or other modal forms.
- A broader visual redesign of the passage modal.

## Domain rules

- **Order above dropdown.** The TB/SIM switch is above the Book label, and the Book label is directly
  above the book-picker trigger. The switch's horizontal centerline aligns with the trigger's
  centerline; the label remains associated with the picker.
- **Contained number controls.** Chapter, From verse, and To verse labels and triggers remain within
  the modal content width; the modal and page do not gain horizontal overflow.
- **Verse-range grouping.** Chapter has its own full-width row; From verse and To verse are adjacent
  as a pair below it when they fit. At 320px, the pair stacks rather than overflowing or squeezing the
  controls too narrowly.
- **Behavior is unchanged.** The toggle state, accessible names, selected book/translation, chapter and
  verse options, native form values, and save behavior continue to work in add and edit forms.

## Acceptance scenarios

### Scenario: Center the translation switch above the book picker

- **Given** the add or edit passage modal
- **When** the scripture form is displayed
- **Then** the TB/SIM switch is above the Book label and horizontally centered over the book-picker trigger
- **And** the Book label remains directly above and associated with the picker

### Scenario: Keep number controls inside a narrow modal

- **Given** the passage modal at 536×426 CSS pixels (the supplied screenshot size) or at a
  320px-wide viewport
- **When** the chapter and verse controls are displayed
- **Then** the Chapter, From verse, and To verse labels and triggers are fully inside the modal content
- **And** the modal content and page have no horizontal overflow

### Scenario: Keep the controls contained at desktop width

- **Given** the passage modal at desktop width
- **When** the chapter and verse controls are displayed
- **Then** all three controls remain inside the modal content without overlap

### Scenario: Keep Chapter separate from the verse range

- **Given** the passage modal at the supplied 536×426 viewport
- **When** the chapter and verse controls are displayed
- **Then** Chapter occupies its own full-width row
- **And** From verse and To verse appear together side by side below it

### Scenario: Keep the verse range usable at 320px

- **Given** the passage modal at a 320px-wide viewport
- **When** the chapter and verse controls are displayed
- **Then** From verse and To verse stack if needed to keep both controls inside the modal
- **And** the modal content and page have no horizontal overflow

### Scenario: Keep the actions reachable if the modal content scrolls

- **Given** the passage modal at a short viewport where the content exceeds its maximum height
- **When** I scroll the modal content to the bottom
- **Then** Save and Cancel are fully visible and usable

### Scenario: Preserve add and edit behavior

- **Given** an add or edit passage form with a selected translation, book, chapter, and verse range
- **When** I use the TB/SIM switch or save the form
- **Then** the existing selections and save behavior remain unchanged

## Traceability

- Domain/app tests: N/A — layout-only change.
- E2E: `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_passage_form_layout_fits_modal_at_narrow_viewport` —
  cover home-to-service navigation, switch above Book, Chapter on its own row, From/To paired at
  536×426 and stacked at 320px, horizontal containment, and action reachability on scroll; retain
  existing picker and save-flow coverage.
- Implementation: `multimedia/web/templates/reading/_entry_form.html` and
  `static/styles/design/components.css`.
- Related: spec 044 (TB/SIM toggle), spec 045 (custom chapter/verse dropdowns), and spec 040 (picker
  menus past the modal).
