# Plan 009: Higher-legibility selected sidebar tint

- **Status:** Accepted (owner, 2026-10-06)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-010
- **Bump:** patch

## Why

The owner asked for another selected-row color that is easier to read with black text and accepted the `#B9D7C9` mint after reviewing the preview. Spec 008's dark-theme colors remain unchanged.

## Scope / edges

**In:**

- Replace only the light-theme selected-sidebar background with `#B9D7C9`.
- Keep selected foreground on the existing light-theme `--ink` token.
- Verify the selected state on the reading sidebar rows covered by Spec 008.

**Out:**

- Dark-theme tokens, text tokens, action accents, hover/focus/drag states, and selection behavior.

## Approach

Change the light selected-background token only. `#B9D7C9` gives black text a `13.63:1` contrast ratio and current light-theme `--ink` (`#1F1F1D`) a `10.71:1` ratio. The previous `#B9C6B9` measured `11.84:1` and `9.31:1`, respectively. The mint is closer in luminance to the rail surface (`1.28:1` versus `1.48:1`); the live home-to-sidebar browser check confirmed the selected fill remains visible.

Retain the dark-theme selected background and its foreground unchanged.

## TDD

- Domain/app tests: `tests/test_design_tokens.py` asserts the exact light tint and at least `7:1` contrast.
- E2E (tool named after stack exists): `tests/e2e/test_reading.py` verifies all selected row types in both themes; visually inspect the light-theme selected row on the home → in-page reading path.

## Risks

The lighter mint improves text contrast but reduces the fill's luminance separation from the rail surface. The selected fill was visually checked in the live light-theme sidebar; unrelated states remain outside scope.
