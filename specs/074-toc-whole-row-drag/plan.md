# Plan 074: Drag service entries from the whole sidebar row

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-077
- **Bump:** minor

## Why

The current reorder gesture starts only from the small grip at the right of a service-entry row. The accepted preview makes the whole row a practical pointer target while retaining the grip as a visible cue.

## Scope / edges

**In:** reorderable ServiceEntry rows, including section-break rows, in the Tata Ibadah second sidebar.

**Out:** legacy rows that cannot be reordered, other reading lists, and the reorder API or persistence format.

## Approach

Expand the existing pointerdown start target in `static/web/reorder.js` from `[data-move-grip]` to the row containing a movable entry. Preserve the current 3px drag threshold, ghost, drop order, save-on-drop, and click-swallow logic. Keep the grip button for keyboard ArrowUp/ArrowDown movement. Apply grab/grabbing cursors to the row without obscuring link focus.

## TDD

- Domain/app tests: existing reorder endpoint coverage remains.
- E2E: extend `tests/e2e/test_reorder.py` for drag from title/number/blank row space, plain click, canceled drag, and keyboard grip.

## Risks

- A short click must still jump to its entry; a completed drag must not click it.
- Touch scrolling must remain reliable; the grip remains the touch drag target.
