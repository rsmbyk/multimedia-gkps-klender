# Spec 036: Keep the add bar out of the item hover

- **ID:** 036
- **Status:** Accepted
- **Item:** ITEM-038
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An item's add bar is not part of the item: hovering or focusing the add buttons must not highlight
the item above or reveal its floating controls.

## Scope

### In scope

- Hovering or focusing the add bar shows only its buttons; the item above shows no highlight and no
  controls.
- Hovering the item still reveals its add bar.
- The item and its add bar do not overlap.

### Out of scope

- Where the floating controls sit and how the highlight looks (specs 033, 034).
- The add actions.

## Domain rules

- **The add bar is outside the item.** Hovering or focusing the add bar must not set the item's hover
  state: no highlight, no floating controls.
- **The item still reveals its bar.** Hovering the item still shows the add bar, as before.
- **No overlap.** The add bar's box does not intrude into the item's, so the pointer never borrows
  the item's hover.
- **One look.** The item and its add bar still read as one "add after this item" group.

## Acceptance scenarios

### Scenario: Hovering the add bar

- **Given** an item with its add bar below it
- **When** I hover the add bar
- **Then** its buttons show, and the item above is not highlighted and shows no controls

### Scenario: Focusing an add button

- **Given** the add bar
- **When** I focus one of its buttons by keyboard
- **Then** the item above is not highlighted and shows no controls

### Scenario: Hovering the item

- **Given** an item
- **When** I hover it
- **Then** its add bar is revealed as before

### Scenario: No overlap

- **Given** an item and its add bar
- **Then** the add bar's box lies outside the item's, and they still read as one group

## Traceability

- Domain/app tests: N/A (hover-region change; no server data).
- E2E: `tests/e2e/test_tatib_entry_controls.py`.
- Implementation: `static/styles/design/components.css`.
- Amends: spec 033 (the item's control reveal), spec 034 (the item's hover highlight).
- Amended by: spec 037 (the item reveals the add rows above and after it).
