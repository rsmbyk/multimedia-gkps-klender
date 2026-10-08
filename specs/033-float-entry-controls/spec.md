# Spec 033: Float the entry controls over each item, top-right

- **ID:** 033
- **Status:** Accepted
- **Item:** ITEM-035
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Put an entry's own controls — preview, Edit, Delete — at the item's top-right, drawn over its text
with a brief backing, instead of leaving them at the far end of the shared add bar.

## Scope

### In scope

- The three controls render at the item's top-right, over the text.
- A brief background behind the button group.
- The controls are visible while the item is hovered or holds keyboard focus; always visible where
  there is no hover.
- Legacy `.tatib__eos` rows get the same treatment.

### Out of scope

- The add bar's four `+` actions, and the controls' own behaviour.

## Domain rules

- **The controls belong to the item.** Preview, Edit, and Delete float at their item's top-right,
  over the text, not in the add bar.
- **Readable over the words.** A brief backing sits behind the button group so the controls stay
  legible whatever the text beneath.
- **Reachable without a pointer.** The controls show on hover, on keyboard focus, and always where
  the device has no hover.
- **The add bar adds.** It keeps the four `+` actions and no longer carries the controls.
- **No stale state.** Revealing and using the controls leaves no lingering outline or hover state
  (spec 025).

## Acceptance scenarios

### Scenario: Hovering an item

- **Given** an entry in the Tata Ibadah pane
- **When** I hover it
- **Then** its preview, Edit, and Delete controls appear at its top-right over the text, over a brief
  backing

### Scenario: Keyboard reach

- **Given** I tab to a control in an item
- **Then** the item's controls are visible, not hidden behind the hover rule

### Scenario: No-hover device

- **Given** a device with no hover
- **Then** the controls stay visible

### Scenario: The add bar still adds

- **Given** an item
- **Then** the add bar below it offers the four add actions and does not carry the controls

### Scenario: A legacy row

- **Given** a legacy TataIbadahItem row
- **Then** its Edit/Delete float at its top-right as for an entry

### Scenario: No stale outline

- **Given** I used a control and the pointer has left
- **Then** no lingering outline or hover state remains

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_tatib_entry_controls.py`.
- Implementation: `multimedia/web/templates/reading/tatib.html`,
  `static/styles/design/components.css`.
- Related: spec 032 (the preview button), spec 025 (quiet modal focus).
- Amended by: spec 036 (the add bar is outside the item's hover).
