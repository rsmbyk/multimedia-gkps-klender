# Spec 035: Give the section break a clear separation

- **ID:** 035
- **Status:** Draft
- **Item:** ITEM-037
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Give a section break one clear, consistent separation on the Tata Ibadah page, so it unmistakably
divides the parts of the service.

## Scope

### In scope

- One divider treatment for the legacy END_OF_SECTION row and the `section_break` entry.
- A rule across the reading column, slightly stronger than the plain divider, with the break's
  label/note kept under it.
- The divider's entry controls keep working (spec 033).

### Out of scope

- The projector's section-break screen, the TOC, and the other panes.
- The other entry kinds.

## Domain rules

- **One divider.** A legacy END_OF_SECTION and a `section_break` entry render the same clear
  separation.
- **The note stays.** Where a break carries a note — the legacy END_OF_SECTION — it shows under the
  rule. (An entry `section_break` has no label; spec 038.)
- **It divides, gently.** The rule reads across the reading column, a touch stronger than the plain
  divider, without shouting.
- **Still editable.** The divider carries its controls like any other entry.
- **The projection is untouched.** The projector still shows a blank section-break screen.

## Acceptance scenarios

### Scenario: A section break divides

- **Given** a Tata Ibadah with a section break between two entries
- **When** the pane renders
- **Then** a clear rule separates the entries, with the break's note beneath it where it has one

### Scenario: Both shapes agree

- **Given** a legacy END_OF_SECTION row and a `section_break` entry
- **Then** they render the same separation

### Scenario: Still editable

- **Given** a section break in the pane
- **Then** it carries its edit/delete controls like any other entry

### Scenario: Projection unchanged

- **Given** a section break
- **Then** the projector still shows a blank screen for it

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_tatib_section_break.py`.
- Implementation: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/tatib.html`,
  `static/styles/design/components.css`.
- Amends: spec 006 (a `section_break` entry's pane rendering).
- Amended by: spec 038 (an entry `section_break` carries no label).
