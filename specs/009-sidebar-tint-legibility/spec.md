# Spec: Higher-legibility selected sidebar tint

- **ID:** 009
- **Status:** Accepted (owner, 2026-10-06)
- **Item:** ITEM-010
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Use a different light-theme selected-row tint that supports near-black text more comfortably while retaining a recognizable selected state.

## Scope

### In scope

- Change the light-theme selected-row background set by Spec 008 from `#B9C6B9` to `#B9D7C9`.
- Keep the existing light-theme `--ink` foreground (`#1F1F1D`) and all selected-row behavior.
- Keep all Spec 008 row types covered: Bible books and chapters, songbooks, songs, and Tata Ibadah services.

### Out of scope

- Dark-theme colors, text-token values, action accents, hover/focus/drag states, and selection behavior.

## Domain rules

- In light theme, every selected row in scope uses the same accepted background `#B9D7C9` and the existing `--ink` foreground.
- The accepted background has `10.71:1` contrast with light-theme `--ink` (`#1F1F1D`) and `13.63:1` with pure black. For reference, `#B9C6B9` measures `9.31:1` and `11.84:1`, respectively.
- Dark-theme selected colors and foreground remain unchanged.
- Unselected rows and all unrelated active, hover, focus, and drag destination states remain unchanged.
- The selected fill must remain perceptibly distinct from the light rail surface in the running UI.

## Acceptance scenarios

### Scenario: Light-theme selected rows use the accepted mint with readable text

- **Given** the reading sidebar is in light theme
- **When** a Bible book or chapter, songbook, song, or Tata Ibadah service is selected
- **Then** its background is `#B9D7C9`, its foreground remains `--ink`, and their contrast is at least `7:1`

### Scenario: Dark-theme selection is unchanged

- **Given** the reading sidebar is in dark theme
- **When** a row in scope is selected
- **Then** its background and foreground match the existing Spec 008 values

### Scenario: Unrelated states are unchanged

- **Given** a sidebar row is unselected, hovered, focused, or a drag destination
- **When** its state is rendered
- **Then** its existing styling and behavior are unchanged

### Scenario: Selected state remains discernible in the live light theme

- **Given** the user opens the home page and navigates in-page to a reading sidebar in light theme
- **When** a row in scope is selected
- **Then** the mint fill is visibly distinguishable from the rail surface and the near-black label is legible

## Traceability

- Domain/app tests: `tests.test_design_tokens.TokenContrastTests.test_light_sidebar_selected_tint_is_high_contrast_mint`; `tests.test_design_tokens.TokenContrastTests.test_light_text_pairs_meet_aa`.
- E2E: `tests.e2e.test_reading.ReadingE2ETests.test_sidebar_selection_tint_matches_theme_for_all_current_rows`.
- Implementation: `static/styles/design/tokens.css`; selected-row rules in `static/styles/design/components.css`.
