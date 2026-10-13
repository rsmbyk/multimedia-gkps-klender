# Spec 088: A stage-only swap preserves the first panel, not the second

- **ID:** 088
- **Status:** Accepted
- **Item:** ITEM-091
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Opening a Tata Ibadah service from the first-level panel has to bring its contents pane with it. Spec
080 made a stage-only swap preserve the sidebar's state and, in doing so, preserved **both** levels of
it: the first-level panel (what the operator reported) and the second-level pane (which the arriving
page legitimately changes). This separates them.

## Scope

### In scope

- The stage-only navigation kinds — `chapter`, `song`, `service`, `refresh` — and which of the two
  sidebar states (`data-nav`, `data-ch`) the live page keeps.

### Out of scope

- Every other navigation kind (rail, search, results, more, sync, lists, mode): unchanged from spec 080.
- Anything visual; the panes look the same, they are simply left in the right state.

## Domain rules

- N/A — browser state only.

## UI details

- **Nav state:** on a stage-only swap the live `data-nav` (first-level sidebar: `open` / `mini` /
  `closed`) is preserved, exactly as spec 080 requires.
- **Contents state:** the arriving page's `data-ch` (second-level pane) is applied. For a chapter or a
  song opened from the second-level list it equals what the live page already has, so nothing moves; for
  a service opened from the first-level panel it is what opens the contents.
- Both attributes stay in the served markup, so the no-JS and first-paint behaviour is untouched.

## Acceptance scenarios

### Scenario: A service opened from the first-level panel

- **Given** the Tata Ibadah panel open on its service list, its contents pane not yet open
- **When** a service is opened from that list
- **Then** the arriving contents pane is open and its rows are visible, and the first-level panel keeps
  whatever state it had.

### Scenario: An item opened from the second-level list

- **Given** the second-level list open and the first-level panel collapsed (or mini)
- **When** a chapter or a song is opened from the list
- **Then** the first-level state is preserved — spec 080's cases, unchanged.

### Scenario: A main-menu switch

- **Given** any state
- **When** a rail item is clicked
- **Then** both states follow the arriving page, as before.

## Traceability

- E2E: `tests/e2e/test_reading.py` — `ReadingE2ETests.test_service_text_sidebar_shows_two_lines_and_centers_grip`
  (the regression; red before this slice) and `SidebarStateOnItemOpenTests` (spec 080's five cases, which
  must stay green).
- Implementation: `static/web/reading.js` — `applyPage()`'s stage-only guard.
