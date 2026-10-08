# Spec 046: Show the first two text lines in the service sidebar

- **ID:** 046
- **Status:** Draft
- **Item:** ITEM-048
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

In the Tata Ibadah sidebar, a text entry should quote its first two literal lines, for both text
kinds, so the running order shows the words rather than a bare "Text".

## Scope

### In scope

- The sidebar label for `text` and `single_screen_text` entries: the first two literal lines of the
  text, shown as up to two lines.
- The reorder grip vertically centered on a two-line row.

### Out of scope

- Passage, song and break rows; the reading pane; the projector.

## Domain rules

- **Two lines.** A text entry's sidebar label is the first two `\n`-split lines of its text.
- **Both kinds.** The multi-line Text and the Single-Screen Text kinds both do this.
- **Two rows tall.** The label may render as two lines in the row.
- **The grip centers.** A two-line row keeps its reorder grip at the row's vertical middle.
- **Others unchanged.** Passage, song and break labels are unaffected.

## Acceptance scenarios

### Scenario: A multi-line text entry

- **Given** a Text entry whose body has several lines
- **Then** its sidebar row shows the first two lines

### Scenario: A single-screen text entry

- **Given** a Single-Screen Text entry
- **Then** its sidebar row shows the first two lines of its body

### Scenario: The grip

- **Given** a two-line sidebar row
- **Then** its reorder grip is vertically centered

### Scenario: Other kinds

- **Given** a passage, song, or section break
- **Then** its sidebar label is unchanged

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_reading.py`.
- Implementation: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/_toc.html`,
  `static/styles/design/components.css`.
- Related: spec 031 (the pane's clamp), spec 039 (the hymn sidebar label).
