# Spec 018: Style Project and Stop projecting as primary and danger actions

- **ID:** 018
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-020
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the Tata Ibadah projection toggle communicate the primary start action and destructive stop action through the existing design language.

## Scope

### In scope

- Style `Project` with the existing primary button treatment when projection is inactive.
- Style `Stop projecting` with the existing danger button treatment when this service is being projected.
- Preserve readable states in light and dark themes.

### Out of scope

- Changing projection state, labels, popup behavior, or the Update control.
- Restyling other actions.

## Domain rules

- The existing projection-state attribute remains the source of truth for which treatment applies.
- `Project` uses the primary treatment while inactive; `Stop projecting` uses danger while active.
- The Update control and projection behavior remain unchanged.

## Acceptance scenarios

### Scenario: Project is the primary action

- **Given** the service is not being projected
- **Then** the Project button has the primary treatment and remains legible in light and dark themes

### Scenario: Stop projecting is the danger action

- **Given** the service is being projected in this browser
- **Then** the same toggle reads Stop projecting and has the danger treatment
- **And** activating it stops projection as before
- **And** the Update control retains its current behavior and appearance

## Traceability

- E2E: `tests/e2e/test_projector.py` (`ProjectorE2ETests`).
- Implementation: `static/styles/design/components.css`; projection state remains owned by `static/web/display.js`.
