# Spec 027: Remove the projection status note

- **ID:** 027
- **Status:** Accepted (owner, 2026-10-08)
- **Item:** ITEM-029
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Stop the projection controls from printing a danger-coloured status line beneath themselves. The
line looks like an error but only narrates the display lifecycle; the owner does not want it.

## Scope

### In scope

- Do not render a status note beneath the Project / Stop projecting controls.
- Remove the two messages it showed: the Update acknowledgement and the window-gone notice.

### Out of scope

- The Project / Stop projecting toggle and its labels.
- The Update action (the display still re-reads on Update and on every saved change).
- Stopping the display automatically when the projector window closes.
- Other status or error copy: the reorder failure line, the deleted-target warning, editor field
  validation, and the empty states.

## Domain rules

- The projection controls render no status line, in any projection state.
- Pressing **Update the current state** still asks the display to re-read the page; it shows no note.
- Closing the projector window still stops the display and returns the button label to "Project"; it
  shows no note.

## Acceptance scenarios

### Scenario: The controls carry no status line

- **Given** a Tata Ibadah page with the projection controls
- **When** the page renders
- **Then** no note element exists beneath the Project / Stop projecting controls
- **And** starting, updating, and stopping projection never adds one

### Scenario: Update still re-reads the page

- **Given** the display is projecting this Tata Ibadah
- **When** I press **Update the current state**
- **Then** the projector re-reads the page
- **And** no status line appears under the controls

### Scenario: Closing the window still stops the display

- **Given** the display is projecting in a browser
- **When** the projector window is closed
- **Then** the display stops and the button label returns to "Project"
- **And** no status line appears under the controls

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (`ServiceProjectorTests`).
- E2E: `tests/e2e/test_projector.py` (`ProjectorE2ETests`).
- Implementation: `multimedia/web/templates/reading/tatib.html`, `static/web/display.js`,
  `static/styles/design/components.css`.
