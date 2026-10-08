# Plan 021: Hide the projection-lock explanation

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-023
- **Bump:** patch

## Why

The projection-lock explanation adds persistent-looking copy below the Project, Stop projecting, and Update current state controls when an entry edit is blocked.

## Scope / edges

**In:** Suppressing that explanatory message while a service is being projected.

**Out:** Changing the projection lock, Project/Stop labels, Update behavior, or other projector lifecycle notifications.

## Approach

Keep the browser-local lock and refused-action behavior, but do not render its explanatory text below the projection controls. Preserve independent feedback for projector lifecycle and Update actions.

## TDD

- E2E: `tests/e2e/test_projector.py` (`ProjectorE2ETests`) verifies blocked entry editing and absence of the lock explanation while the lock remains active.

## Risks

- The refusal message shares a status element with unrelated projector notices; suppress only the lock explanation and preserve those other notices.
