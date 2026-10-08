# Spec 037: Reveal the add rows before and after a hovered item

- **ID:** 037
- **Status:** Draft
- **Item:** ITEM-039
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Let the operator insert on either side of the item they are pointing at: hovering an item reveals the
add row above it and the add row below it.

## Scope

### In scope

- Hovering an item reveals the add row immediately above it and the one immediately below it.
- Keyboard focus within an item reveals the same pair.
- The first item's "above" row is the leading start bar (spec 030).

### Out of scope

- The add actions and endpoints.
- The item highlight and floating controls (specs 033, 034), beyond coherence.
- The behaviour of a bar that is hovered or focused directly (spec 036).

## Domain rules

- **Both sides.** Hovering an item reveals the add row above it and the add row below it.
- **Focus too.** Keyboard focus within an item reveals the same pair.
- **Direct hover stays as spec 036.** Hovering or focusing a bar shows only that bar and does not
  highlight the item.
- **The first item has an above row.** The leading start bar (spec 030) is the first item's "above"
  row.

## Acceptance scenarios

### Scenario: Hovering a middle item

- **Given** a Tata Ibadah with items on both sides of one entry
- **When** I hover that entry
- **Then** the add row above it and the add row below it are revealed

### Scenario: Keyboard focus

- **Given** an item's controls hold keyboard focus
- **Then** the add rows above and below the item are revealed

### Scenario: The first item

- **Given** the first item in the service
- **When** I hover it
- **Then** the leading start bar above it is revealed, together with the bar below it

### Scenario: Moving onto a bar

- **Given** an item hovered with both bars shown
- **When** the pointer moves onto one of the bars
- **Then** only that bar is shown, and the item is not highlighted (spec 036)

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_tatib_entry_controls.py`.
- Implementation: `static/web/entries.js`, `static/styles/design/components.css`,
  `multimedia/web/templates/reading/tatib.html`.
- Related: spec 030 (the leading start bar), spec 036 (the add bar is outside the item hover),
  specs 033 / 034 (item hover: controls and highlight).
