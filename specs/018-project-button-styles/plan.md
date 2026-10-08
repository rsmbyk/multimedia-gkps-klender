# Plan 018: Style Project and Stop projecting as primary and danger actions

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-020
- **Bump:** patch

## Why

Projection start is the primary action; stopping an active projection is destructive and should use the danger treatment.

## Scope / edges

**In:** Styling the existing Project/Stop projecting toggle in both display states and themes.

**Out:** Changing labels, projection behavior, update control, or unrelated buttons.

## Approach

Use the existing design tokens and state attribute set by `static/web/display.js` to give the inactive Project state the primary treatment and active Stop projecting state the danger treatment. Verify computed styles in the actual service page and projector state.

## TDD

- E2E: `tests/e2e/test_projector.py` (`ProjectorE2ETests`) pins state-driven style and retained behavior.

## Risks

The active/inactive label is changed dynamically, so state-dependent styles must follow the same state transition and remain legible in light and dark themes.
