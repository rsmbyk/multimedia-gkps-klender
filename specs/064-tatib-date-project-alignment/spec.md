# Spec: Center the Tata Ibadah date and Project button

- **ID:** 064
- **Status:** Accepted
- **Item:** ITEM-067
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the Tata Ibadah date label and Project button read as one vertically aligned header row. Their current shared flex row already centers items, but the date label's bottom margin visually offsets it from the button.

## Scope

### In scope

- Center the date label and Project button vertically in the existing Tata Ibadah header row.
- Preserve the date label on the left, the Project button on the right, and the service title beneath them.

### Out of scope

- Changing the Project button's styling, state behavior, or interaction.
- Changing non-Tata Ibadah reading headers or the service title row.

## Domain rules

- The date and Project button remain in the existing header row.
- The alignment change applies only to Tata Ibadah.

## UI details

Approved preview: the date label on the left and the existing Project button on the right of the same header row, vertically centered; the service title remains below. Approved in this task conversation on 2026-10-12.

- **Size / spacing:** Keep the existing 34 px Project button height and 12 px header-row gap. Remove the date label's 10 px bottom margin for Tata Ibadah only.
- **Position / layout:** Keep `.read__head-top` as a flex row with `align-items: center`; date label left, Project control right. Their bounding-box centers align within 1 px. Keep the service title on its existing second row.
- **Colors / typography:** No changes. Retain the current date label and Project button typography, colors, borders, and dimensions.
- **States:** No changes to hover, focus-visible, start-projecting, or stop-projecting states.
- **Responsive behavior:** Keep the current header row and spacing at desktop and 390 px viewport widths; the date and button remain side by side without overlap, and the service title remains below.
- **Motion:** No new motion; retain existing button transitions.

## Acceptance scenarios

### Scenario: Date and Project button are vertically centered on desktop

- **Given** a Tata Ibadah page at a 1440 px viewport width
- **When** its header is displayed
- **Then** the date label and Project button share a row and their bounding-box centers differ by no more than 1 px
- **And** the service title remains below that row

### Scenario: Date and Project button remain centered on a narrow viewport

- **Given** a Tata Ibadah page at a 390 px viewport width
- **When** its header is displayed
- **Then** the date label and Project button share a row without overlap and their bounding-box centers differ by no more than 1 px
- **And** the service title remains below that row

### Scenario: Other reading headers keep their existing spacing

- **Given** a Bible or song reading page
- **When** its header is displayed
- **Then** its date/eyebrow spacing and header layout remain unchanged

## Traceability

- Domain/app tests: N/A; presentation-only CSS.
- E2E: `tests/e2e/test_reading.py` — Tata Ibadah header geometry at 1440 px and 390 px, plus existing reading header spacing coverage.
- Implementation: `static/styles/design/components.css` — Tata Ibadah-only date eyebrow margin reset.
