# Plan 075: Repeat a service-entry flash after it finishes

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-078
- **Bump:** patch

## Why

Clicking a service-entry quicklink again after its stage flash has finished may leave the old animation class in place, so the entry does not flash again. Restarting during an active flash also obscures the first cue.

## Scope / edges

**In:** Tata Ibadah second-sidebar quicklinks to service entries and the corresponding stage flash.

**Out:** list reveal flashes, search-result navigation, projection, and reorder persistence.

## Approach

Give the stage flash one active lifecycle in `static/web/reading.js`: start after a valid quicklink activation, ignore further quicklink flashes until the current animation ends, then remove the class and release the guard. Clear the guard if navigation replaces the target. Preserve the current scroll-to-entry and visual animation.

## TDD

- Domain/app tests: N/A; browser interaction state.
- E2E: targeted repeated clicks in `tests/e2e/test_reading.py` before and after animation completion, including a different row and keyboard activation.

## Risks

- A removed/replaced stage node must not leave the guard stuck.
- Reduced-motion users should not be blocked by a nonexistent animation.
