# Spec: Softer selected-item tint in the reading sidebars

- **ID:** 008
- **Status:** Accepted (owner, 2026-10-05)
- **Item:** ITEM-009
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The selected row in the reading sidebars currently uses the full saturated active accent. Use a
slightly softer, lighter version of that accent for Bible books, Bible chapters, songbooks, songs,
and Tata Ibadah service rows.

## Scope

### In scope

- Give these five selected-row types one dedicated, theme-aware background:
  - Bible books: `.book[aria-current="true"]` in the Bible books list.
  - Bible chapters: `.ch-num[aria-current="true"]` in the chapter list.
  - Songbooks: `.book[aria-current="true"]` in the songbook list.
  - Songs: `.songrow[aria-current="true"]` in the song list.
  - Tata Ibadah services: `.book[aria-current="true"]` in the service list.
- **Tint values:** light `#B9C6B9`; dark `#393F4F`. Each is a 25% sRGB mix of the existing theme's `--active-bg` into `--rail-bg`.
- Use `--ink` for selected-row text, including song citations. The primary text/background contrast is 9.31:1 in light mode and 9.48:1 in dark mode.
- Keep row geometry, current-item semantics, hover/focus treatment, and navigation behavior unchanged.

### Out of scope

- Main rail active states, the TB/SIM language switch, editor/search/action buttons, drag destination slots, hover styling, focus indicators, and selection or routing behavior.
- Changing global `--active-bg` or `--active-ink` values or their use outside the five named sidebar row types.

## Domain rules

- The five named sidebar row types use the same softer selected background in each theme.
- In light mode the selected-row background is `#B9C6B9`; in dark mode it is `#393F4F`.
- Selected-row text uses the theme's `--ink`; its contrast against the background is at least 4.5:1.
- Unselected rows, hover and focus states, and unrelated active controls retain their existing styling.

## Acceptance scenarios

### Scenario: All five selected sidebar rows use the softer tint

- **Given** the Bible books, chapter, songbook, song, and Tata Ibadah service sidebars each have a current row
- **When** I view those sidebars in light or dark theme
- **Then** each current row uses the specified theme tint and readable `--ink` text, while an unselected row retains its existing appearance

### Scenario: Other active and interaction states are unchanged

- **Given** the main rail, TB/SIM switch, drag destination slot, hover, and keyboard-focus states
- **When** I use those controls in either theme
- **Then** each retains its existing styling and behavior

## Traceability

- Scenario: all five selected rows use the light/dark tint — `tests.e2e.test_reading.ReadingE2ETests.test_sidebar_selection_tint_matches_theme_for_all_current_rows`.
- Contrast: `tests.test_design_tokens.TokenContrastTests.test_light_text_pairs_meet_aa` and `test_dark_text_pairs_meet_aa`.
- Unrelated hover, focus, main-rail active, language-switch, and destination-slot rules — unchanged in `static/styles/design/components.css`; only the scoped reading-sidebar selected-row declarations change.
