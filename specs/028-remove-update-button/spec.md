# Spec 028: Remove the "Update the current state" button

- **ID:** 028
- **Status:** Draft
- **Item:** ITEM-030
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The display follows every saved change by itself (spec 026), so the separate **Update the current
state** control is redundant. Remove it and its shell wiring, leaving the automatic follow as the
only re-read.

## Scope

### In scope

- No **Update the current state** control renders on a Tata Ibadah reading page, in any projection
  state.
- `static/web/display.js` no longer reads, toggles, or binds a `[data-project-update]` node.
- The automatic re-read is unchanged: a saved add / edit / delete / reorder still tells the running
  display to re-read.

### Out of scope

- The display state, channel, heartbeat, or watchdog (spec 006 / 026).
- `static/web/projector.js`.
- The OBS dock / source pages.

## Domain rules

- **The display still follows every saved change.** Removing the manual control must not remove or
  alter the `editor:saved` → `reflow()` path; a saved change still reaches the running display.
- **The display's state is unchanged.** It still lives only in the browser that started it.

## Acceptance scenarios

### Scenario: The manual control is gone

- **Given** a Tata Ibadah reading page, projecting or not
- **Then** no **Update the current state** control is rendered

### Scenario: The automatic follow still works

- **Given** the projector is open and showing a Tata Ibadah
- **When** I add, edit, delete, or reorder an entry in the shell
- **Then** the display re-reads and follows without any control being pressed

### Scenario: Project and Stop are unaffected

- **Given** a Tata Ibadah reading page
- **Then** the project button still toggles between **Project** and **Stop projecting** as before

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_projector.py`.
- Implementation: `static/web/display.js`,
  `multimedia/web/templates/reading/tatib.html`.
- Amends: spec 026 (its manual-re-read clause and scenario).
