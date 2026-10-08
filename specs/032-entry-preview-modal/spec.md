# Spec 032: Entry preview modal

- **ID:** 032
- **Status:** Draft
- **Item:** ITEM-034
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Let the operator read a service entry's whole content — a text's hidden words, a passage's full
text, or a song's selected lyrics — in a read-only modal, without leaving the Tata Ibadah page.

## Scope

### In scope

- A preview button on: text entries that were clamped (spec 031), passages, songs, and legacy text
  rows that were clamped.
- A view-only modal with no header, the content inline with the page, a scrollable body, and a
  sticky close button at the bottom.
- Closing on an overlay click and on Esc.
- No stale focus outline or hover state left on the trigger (spec 025).

### Out of scope

- Editing anything from the modal.
- Fetching content on open (the content is rendered inline).
- Section breaks, and the projector.

## Domain rules

- **The button follows the content.** A preview is offered where the pane hid or abbreviated
  something: a clamped text (including a legacy text row), a passage, a song. A short text that was
  not clamped, and a section break, get no preview.
- **View-only.** The modal shows content; it has no inputs and changes nothing.
- **Headerless, scrollable, sticky close.** The modal carries no title bar; a long body scrolls; the
  close button stays at the bottom of the modal.
- **Dismissal.** A click on the overlay and the Esc key close it.
- **Content per kind.**
  - A **text** shows its whole body.
  - A **passage** shows its full text with the reference(s) at the top.
  - A **song** shows its songbook and title, then its selected verses as tabs labelled by verse
    number, centred horizontally and scrollable when many; a single selected verse shows no tab row.
- **No stale focus.** After closing, focus returns to the trigger without leaving a lingering
  outline/hover state (spec 025).

## Acceptance scenarios

### Scenario: Previewing a clamped text

- **Given** a text entry clamped in the pane
- **When** I open its preview
- **Then** the modal shows the whole text

### Scenario: No preview without hidden text

- **Given** a text entry that the pane did not clamp
- **Then** it offers no preview for hidden text

### Scenario: Previewing a passage

- **Given** a passage entry
- **When** I open its preview
- **Then** the modal shows the full passage text with its reference at the top

### Scenario: Previewing a song

- **Given** a song entry with several selected verses
- **When** I open its preview
- **Then** the modal shows the songbook and title, and one tab per selected verse labelled by its
  number, centred and horizontally scrollable when many

### Scenario: A single-verse song

- **Given** a song entry with one selected verse
- **When** I open its preview
- **Then** the verse shows with no tab row

### Scenario: Dismissing

- **Given** the preview is open
- **When** I click the overlay, or press Esc
- **Then** it closes, and the trigger keeps no lingering focus outline

### Scenario: A section break

- **Given** a section break entry
- **Then** it offers no preview

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_entry_preview.py`.
- Implementation: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/tatib.html`,
  `multimedia/web/templates/reading/base.html`, `static/web/preview.js`,
  `static/styles/design/components.css`.
- Related: spec 031 (the clamp that creates the hidden text), spec 025 (quiet modal focus).
