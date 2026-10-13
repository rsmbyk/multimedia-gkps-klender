# Spec 084: Refresh the home search helper line

- **ID:** 084
- **Status:** Accepted
- **Item:** ITEM-087
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Point the search-first home at two examples that resolve: a New Testament verse and a Simalungun hymn.

## Scope

### In scope

- The `search-home__hint` sentence on the reading home.

### Out of scope

- The search field's placeholder and label, the search rules and ranking, the results page, and the
  sidebars.

## Domain rules

- The home shows the helper line `Try Yoh 3:16 or HAL 411`.
- Both examples resolve against the corpus: `Yoh 3:16` returns the Yohanes 3:16 reference as an Alkitab
  hit, and `HAL 411` returns the HAL song 411.
- The line keeps its current behaviour otherwise: it is shown on the landing home and hidden while the
  results of a search are on screen.

## UI details

- **Visual reference:** [Home hint preview](./preview.html) — the landing home with the new line, and
  the two examples resolving beside it.
- **Size / spacing / position:** unchanged — `margin: 18px 0 0`, `font-size: 13px`, centred under the
  search field, inside the existing `search-home__inner`.
- **Colors / typography:** unchanged — `var(--head-ink)`, the shell's sans-serif at 13px.
- **States:** none. The line is static text with no hover, focus, or selected state; it stays hidden
  under `[data-home="results"]`.
- **Responsive behavior:** unchanged; the sentence wraps within the home column as it does today, and
  it is short enough to stay on one line at 390px.
- **Motion:** none.

## Acceptance scenarios

### Scenario: The home shows the new examples

- **Given** the operator opens the reading home
- **When** the page renders
- **Then** the line under the field reads `Try Yoh 3:16 or HAL 411`, and neither the old verse nor the
  old hymn reference appears.

### Scenario: Both examples resolve

- **Given** the home's own examples
- **When** each is searched
- **Then** `Yoh 3:16` returns the Yohanes 3:16 reference and `HAL 411` returns its song — no example on
  the home leads to an empty result set.

### Scenario: The line is absent from results

- **Given** a search has been run and the result set is on screen
- **When** the home block is shown above it
- **Then** the helper line is not displayed, exactly as today.

## Traceability

- Domain/app tests: `multimedia/web/tests.py::ReadingViewTests.test_home_is_search_first` (the hint
  string).
- E2E: `tests/e2e/test_reading.py` (the landing home and the return-to-home paths).
- Implementation: `multimedia/web/templates/reading/base.html`.
