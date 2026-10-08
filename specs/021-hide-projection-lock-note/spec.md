# Spec 021: Hide the projection-lock explanation

- **ID:** 021
- **Status:** Superseded by [spec 026](../026-live-projection-editing/spec.md) (owner, 2026-10-08)
- **Item:** ITEM-023
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

> Spec 026 removes the projection lock entirely, so there is no longer a blocked entry action to
> keep quiet about. The rest of this spec — leaving the Project / Stop projecting / Update
> behavior and lifecycle feedback alone — still stands.

## Intent

Remove the explanatory projection-lock text shown below the Project, Stop projecting, and Update current state controls when entry editing is refused.

## Scope

### In scope

- Do not show `This browser is displaying a Tata Ibadah. Stop projecting first.` beneath the projection controls.
- Keep the browser-local lock active so entry create/edit/delete remains blocked while projecting.
- Preserve other projector lifecycle and Update feedback.

### Out of scope

- Changing projection behavior, control labels, or Update behavior.
- Changing unrelated status messages.

## Domain rules

- A blocked entry action remains blocked during projection.
- The blocked action does not display the lock explanation under the projection controls.
- Other projector status messages remain available.

## Acceptance scenarios

### Scenario: Entry editing is blocked without the explanation

- **Given** this browser is projecting a Tata Ibadah
- **When** I try to add, edit, or delete an entry
- **Then** the entry operation remains blocked
- **And** the projection-lock explanation is not shown beneath the controls

### Scenario: Other projector feedback remains

- **Given** I update the current display or the projector window stops
- **Then** the existing independent status feedback remains unchanged

## Traceability

- E2E: `tests/e2e/test_projector.py` (`ProjectorE2ETests`).
- Implementation: `static/web/display.js`, `multimedia/web/templates/reading/tatib.html`, and relevant projection styles.
