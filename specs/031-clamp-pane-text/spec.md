# Spec 031: Clamp a text entry in the Tata Ibadah pane

- **ID:** 031
- **Status:** Draft
- **Item:** ITEM-033
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Show only the first three lines of a text entry in the Tata Ibadah pane and hard-truncate the rest
with a trailing "…", so a long text cannot push the running order down the page. The whole text
stays reachable through the entry preview (spec 032).

## Scope

### In scope

- A text entry's pane rendering shows at most three lines; a longer body is hard-truncated with a
  literal "…".
- Blank lines count toward the three.
- Both text entries and legacy text rows are clamped.
- A truncated entry is marked so the preview affordance is offered (spec 032).

### Out of scope

- Scripture and song rows, and the other reading panes.
- The projector, which still shows the full body.
- The preview modal's content (spec 032).

## Domain rules

- **Three lines, then "…".** A pane text shows its first three lines; if there is more, the trailing
  content is dropped and a literal "…" follows the third.
- **Blank lines count.** An empty line counts toward the three (it still occupies a row).
- **Short texts are untouched.** Three lines or fewer render in full, with no "…".
- **Clipped means hidden words exist.** An entry is marked clipped exactly when it was truncated, and
  only then is the preview offered (spec 032).
- **The projector is unaffected.** The full body still reaches the display.

## Acceptance scenarios

### Scenario: A long text is clamped

- **Given** a text entry with more than three lines
- **When** the Tata Ibadah pane renders
- **Then** only the first three lines show, the rest is gone, and the third line ends with "…"

### Scenario: Blank lines count

- **Given** a text whose first three lines include a blank line
- **Then** the blank line counts toward the three

### Scenario: A short text is untouched

- **Given** a text entry with three lines or fewer
- **Then** it renders in full, with no "…"

### Scenario: The preview is offered only when clipped

- **Given** a text entry that was truncated
- **Then** the preview affordance is offered for it
- **Given** a text entry that was not truncated
- **Then** no preview affordance is offered for the hidden-words reason

### Scenario: The other panes and rows are unaffected

- **Given** scripture and song rows, and the Bible and Kidung panes
- **Then** they render as before

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: N/A (covered by the domain tests).
- Implementation: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/tatib.html`.
- Related: spec 032 (the preview that reveals the hidden text).
