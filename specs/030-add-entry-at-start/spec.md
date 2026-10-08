# Spec 030: Add a service entry at the beginning

- **ID:** 030
- **Status:** Draft
- **Item:** ITEM-032
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

Insert a service entry at the **beginning** of a Tata Ibadah's running order, not only after an
existing row.

## Scope

### In scope

- A start affordance in the reading pane that opens the new-entry form for any kind, inserting at
  order 1.
- Server-side insertion at order 1, shifting every existing entry and legacy row so the shared order
  stays contiguous from 1.
- The insertion point surviving a form validation error.

### Out of scope

- Per-row "after" insertion, reorder, and the legacy DRF API.
- The empty state (already appends at order 1).

## Domain rules

- **One running order.** Entries and legacy rows are ordered by `order_number`, contiguous from 1;
  inserting at the start shifts every existing row by one and leaves no gap and no duplicate.
- **Start means order 1.** A new entry added at the beginning is `order_number = 1`.
- **Both tables shift together.** The shared order spans `ServiceEntry` and `TataIbadahItem`; a
  start insertion moves both.
- **The insertion point survives a rejected form.** A validation error re-renders the form still
  bound to the start position.

## Acceptance scenarios

### Scenario: Adding at the beginning

- **Given** a Tata Ibadah that already has entries and legacy rows
- **When** I add an entry from the start affordance
- **Then** the new entry is order 1, and every other row has shifted up by one

### Scenario: The order stays contiguous

- **Given** a service of mixed entries and legacy rows
- **When** I insert at the beginning
- **Then** the rows are still numbered contiguously from 1, with no gaps or duplicates

### Scenario: It shows first

- **Given** an entry added at the beginning
- **Then** the reading pane and the projector both show it before every other row

### Scenario: A rejected form keeps the place

- **Given** I open the start affordance and submit an invalid form
- **When** the form re-renders with its errors
- **Then** a corrected save still inserts at the beginning

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_reorder.py`.
- Implementation: `multimedia/web/templates/reading/tatib.html`,
  `multimedia/web/reading/views.py`, `static/web/entries.js`.
