# Plan 008: Sidebar selection tint

- **Status:** Accepted (owner, 2026-10-05)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-009
- **Bump:** patch

## Why

The current selection fill is the full active green/blue in every sidebar. The owner asked for a
slightly softer, lighter tint on Bible books, Bible chapters, songbooks, songs, and Tata Ibadah
service rows.

## Scope / edges

**In:**

- Give those five selected-row types one dedicated, theme-aware pale accent background.
- Keep selected text readable on that background in both light and dark themes.

**Out:**

- Main-rail active states, TB/SIM language selection, search/editor buttons, drag destination
  slots, hover states, focus indicators, selection logic, and navigation behavior.

## Approach

Use the accepted theme-aware values `#B9C6B9` (light) and `#393F4F` (dark), each a 25% sRGB mix of the existing active accent into the rail surface. Use `--ink` for selected-row text rather than the contrasting active-button text token. The text/background ratios are 9.31:1 in light mode and 9.48:1 in dark mode; assert both in `tests/test_design_tokens.py`. Apply the token only to the selected-row rules inside the relevant sidebar lists: `#panelBody .book`, `#chList .ch-num`, and `#chList .songrow`. Pin the rendered backgrounds and text colors in targeted E2E coverage in both themes.

## TDD

- Domain/app tests: N/A (CSS-only).
- E2E: `tests/e2e/test_reading.py` — selected backgrounds and text for all five row types in both
themes; existing selection and navigation behavior stays intact.
- Token contrast: `tests/test_design_tokens.py` — selected-row ink/background pair in light and dark.

## Risks

- The pale fill must not inherit the white/navy text used on the saturated accent; doing so would
  make the text unreadable. Keep the selected-row text on `--ink` and measure the pair.
- Keep the new token scoped to the five sidebar row states so other active controls retain their
  existing saturated treatment.
