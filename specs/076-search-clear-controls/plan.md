# Plan 076: Make reading search clear controls consistent

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-079
- **Bump:** patch

## Why

The clear buttons in the new reading shell's search and sidebar filters vary in size and can appear misaligned. The accepted preview uses a single, slightly larger cross control.

## Scope / edges

**In:** the existing clear control on the home search, first-sidebar filter, and second-sidebar filter.

**Out:** date-picker Clear date action, picker-internal search fields without a custom clear button, legacy pages, docks, and webs.

## Approach

Consolidate `.field-clear` geometry in `static/styles/design/components.css`: one 26px circular hit area and one 14px SVG cross in all three contexts. Keep each field's established right inset, with the home search's larger offset to clear its submit button. Verify input right padding avoids text overlap.

## TDD

- Domain/app tests: N/A; CSS and existing button behavior.
- E2E: extend `tests/e2e/test_reading.py` for computed size/position in all three fields, focus, clear behavior, and light/dark themes.

## Risks

- A larger button can overlap typed text or the home Search button unless padding and offsets are checked.
