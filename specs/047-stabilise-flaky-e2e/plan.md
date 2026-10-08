# Plan 047: Stabilise the flaky E2E tests

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-049
- **Bump:** none

## Why

Two Playwright tests assert on a value that is still animating, so they fail intermittently:

- `tests/e2e/test_editor.py::test_date_picker_dropdown_overlaps_the_scrollable_modal_content`
  scrolls `#editorContent` to 0 and immediately reads the calendar's box, but `date-picker.js`
  repositions the calendar on the content's `scroll` event — which lands after the read. The read
  shows the stale (pre-scroll) box, so the "calendar is anchored to the trigger" assertion fails.
- `tests/e2e/test_reading.py::test_search_state_survives_sidebar_browsing` restores the remembered
  offset with an animation and reads `window.scrollY` after a fixed 250ms — mid-animation it reads a
  value short of the target.

## Scope / edges

**In:**

- The two tests wait for the state to settle before reading it.

**Out:**

- Any application code; the picker and the scroll restore are correct.
- The other tests.

## Approach

- `tests/e2e/test_editor.py` — after scrolling the content to 0, `wait_for_function` until the
  calendar is anchored (8px below the trigger, or 8px above it), then read the box.
- `tests/e2e/test_reading.py` — after returning to the results, `wait_for_function` until
  `window.scrollY` has stopped changing (stable across several frames) and is past the top, then
  read it.

## TDD

- Both tests exist and are the red/green signal: they must pass repeatedly.
- No new tests; this is a determinism fix.

## Risks

- **A masked failure.** Waiting for the anchored condition could hide a real "never repositions"
  regression — mitigate by keeping the geometric assertions after the wait (they still fail if the
  anchor is wrong) and a bounded timeout.
