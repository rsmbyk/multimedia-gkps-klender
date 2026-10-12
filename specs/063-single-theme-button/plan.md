# Plan 063: Restore the single theme button

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-066
- **Bump:** patch

## Why

The three separate controls from spec 062 occupy too much of the rail. The owner wants the previous one-button presentation while retaining the three appearance modes.

## Scope / edges

**In:** Public reading rail theme control, icon/tooltip/accessibility states, mode cycling, and related browser tests.

**Out:** Theme palette changes, storage-key changes, editor/OBS surfaces, projector theme, or changing System as the default.

## Approach

Use the original single `#themeBtn` position and visual treatment. On activation, cycle `system → dark → light → system`. Keep the existing `gkps-theme` preference key and system media-query listener from spec 062. Update the one button's icon, tooltip, and accessible name for the **active** preference. Remove the two extra controls and the compact-height layout rule added solely to fit three buttons.

## TDD

- Domain/app tests: N/A; this is browser presentation behavior.
- E2E: Update `tests/e2e/test_reading.py` for the cycle, current-mode labels, persistence, and System live following. Run the editor short-viewport browser test to guard rail overlap.

## Risks

- Older tests use one click on `#themeBtn` to select Dark from a light system. Keep that path.
- A dark system also initially displays dark in System mode; the active-mode icon and label must distinguish System from an explicit Dark choice.
- Keep the button usable at short viewport heights.
