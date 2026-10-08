# Spec 038: Remove the label from section-break entries

- **ID:** 038
- **Status:** Accepted
- **Item:** ITEM-040
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

A section break is a divider with no label; remove the label field and its uses from the
`section_break` kind.

## Scope

### In scope

- The section-break editor offers no label control.
- A section break stores no label and the pane shows none.
- Text entries keep their title; the legacy END_OF_SECTION note is untouched.

### Out of scope

- The projector's section-break screen.
- The text entry's title, and the legacy END_OF_SECTION note.

## Domain rules

- **A break carries no label.** A `section_break` entry has no title/label, in the editor or in the
  pane.
- **Shared column, scoped change.** `ServiceEntry.title` remains for other kinds; only the
  `section_break` stops using it.
- **The legacy note stands.** `TataIbadahItem` END_OF_SECTION keeps its own note.
- **The projection is unchanged.** A section break still shows a blank screen.

## Acceptance scenarios

### Scenario: No label in the editor

- **Given** I open the new section-break editor
- **Then** there is no label input

### Scenario: No label stored or shown

- **Given** I save a section break
- **Then** it stores no label, and the pane renders it with none

### Scenario: Other kinds keep their title

- **Given** a text entry
- **Then** its title control and displayed title are unchanged

### Scenario: The legacy note stands

- **Given** a legacy END_OF_SECTION row
- **Then** its note still renders

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: N/A (covered by the pane assertions).
- Implementation: `multimedia/web/reading/entries.py`, `multimedia/tatib/models.py`,
  `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/_entry_form.html`.
- Amends: spec 035 (the divider shows no label for an entry break).
