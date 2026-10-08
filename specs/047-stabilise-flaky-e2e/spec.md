# Spec 047: Stabilise the flaky E2E tests

- **ID:** 047
- **Status:** Accepted
- **Item:** ITEM-049
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none

## Intent

Make two intermittently failing Playwright tests deterministic by waiting for the state they assert
on, instead of racing a fixed pause.

## Scope

### In scope

- The date-picker geometry test and the search-state test wait for the animation to settle.

### Out of scope

- Application code; the behaviour under test is correct.

## Domain rules

- **Wait for the state, not the clock.** A test that asserts on a value an animation changes waits
  until that value settles before reading it.
- **Keep the assertion.** The geometric/offset assertions stay; only the timing is fixed, so a real
  regression still fails.
- **Bounded.** Each wait has a timeout so a genuine hang fails rather than passing.

## Acceptance scenarios

### Scenario: The date picker re-anchors

- **Given** the passage modal's calendar open over the scrollable content
- **When** the content is scrolled to the top
- **Then** the test waits for the calendar to re-anchor, and the geometry assertions hold

### Scenario: The search offset restores

- **Given** a remembered result offset
- **When** the results are restored
- **Then** the test waits for the scroll to settle, and the resume assertions hold

### Scenario: Repeated runs

- **Given** the two tests
- **When** they run repeatedly
- **Then** they pass every time

## Traceability

- Domain/app tests: N/A (test-only change).
- E2E: `tests/e2e/test_editor.py`, `tests/e2e/test_reading.py`.
- Implementation: `tests/e2e/test_editor.py`, `tests/e2e/test_reading.py`.
