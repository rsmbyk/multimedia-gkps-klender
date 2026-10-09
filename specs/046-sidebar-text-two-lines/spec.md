# Spec 046: Show the first two text lines for untitled service entries

- **ID:** 046
- **Status:** Accepted
- **Item:** ITEM-048
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An untitled Text or Single-Screen Text entry in the Tata Ibadah sidebar should quote its first two
literal body lines. When an entry has a title, keep that title instead of replacing it with body text.

## Scope

### In scope

- For new service-entry `text` and `single_screen_text` kinds, an empty title uses the first two
  literal body lines as the sidebar label, shown as up to two lines.
- A non-empty title remains the sidebar label for either kind.
- The final label (retained title or body preview) is capped at 60 characters overall; blank lines
  count as literal lines and are not skipped.
- The reorder grip is vertically centered on a two-line row.

### Out of scope

- Legacy `TataIbadahItem` text rows.
- Passage, song and break rows; the reading pane; the projector.

## Domain rules

- **Untitled text kinds.** An untitled service-entry Text or Single-Screen Text label is the first two
  lines from the body split on `\n`.
- **Titled text kinds.** A non-empty title stays visible instead of being replaced by body text.
- **Literal lines.** A blank line counts toward the first two; do not skip it to find another
  non-empty line.
- **Cap.** Cap the final label (retained title or body preview) at 60 characters overall, consistent
  with the current service-entry label cap.
- **Two rows tall.** The label may render as two lines; the grip stays centered on the row.
- **Unchanged.** Legacy text rows and passage, song and break labels are unaffected.

## Acceptance scenarios

### Scenario: An untitled Text entry

- **Given** an untitled Text entry whose body has several lines
- **Then** its sidebar row shows the first two literal body lines only

### Scenario: A blank line is one of the first two lines

- **Given** an untitled text body with a blank second line and later non-empty lines
- **Then** the sidebar keeps the blank second line rather than skipping to a later line

### Scenario: An untitled Single-Screen Text entry

- **Given** an untitled Single-Screen Text entry
- **Then** its sidebar row shows the first two literal body lines

### Scenario: A titled text entry

- **Given** a titled Text or Single-Screen Text entry
- **Then** its sidebar label remains the title

### Scenario: A long text label

- **Given** a title or the first two body lines exceed 60 characters combined
- **Then** the final sidebar label is capped at 60 characters overall

### Scenario: The grip

- **Given** a two-line sidebar row
- **Then** its reorder grip is vertically centered

### Scenario: Legacy rows and other kinds

- **Given** a legacy text row, passage, song, or section break
- **Then** its sidebar label is unchanged

## Traceability

- Domain/app test: `multimedia/web/tests.py::ServiceEntryViewTests.test_service_text_sidebar_labels_use_two_literal_lines_and_respect_scope`.
- E2E test: `tests/e2e/test_reading.py::ReadingE2ETests.test_service_text_sidebar_shows_two_lines_and_centers_grip`.
- Implementation: `multimedia/web/reading/views.py` (`_tatib_stage()`),
  `multimedia/web/templates/reading/_toc.html`,
  `static/styles/design/components.css`.
- Related: spec 031 (the pane's clamp), spec 039 (the hymn sidebar label).
