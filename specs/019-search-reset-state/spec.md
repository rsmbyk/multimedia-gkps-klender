# Spec 019: Clear remembered search when the home is reset

- **ID:** 019
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-021
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

When the app is reset to the empty search home, the rail Search action must not reopen a result set remembered from an earlier page state or session.

## Scope

### In scope

- Clear the remembered search URL and result scroll offset on a fresh/reset unqueried `/home/` landing.
- Preserve the current in-session result restoration when the user browses from results through reading sidebars without resetting.
- Document the single search-home/result-stage model so the fix does not create a second page or route.

### Out of scope

- Changing route definitions or the intentional in-place navigation model.
- Changing the search-field clear control, which currently retains the result set.
- Adding a separate reset button or changing result ranking/pagination.

## Domain rules

- `#searchHome` and `#searchResults` are two conditional regions in one shell, not two search-page instances.
- A fresh `/home/` landing with no query is Reset: clear `gkps-search` and `gkps-search-scroll`, and point rail Search to the empty home.
- A result set remains remembered while the user leaves it for sidebar reading. Clicking Search returns to that query and scroll position unless Reset has occurred.
- Clearing the search input with the × is not Reset: retain the currently displayed results and the established remembered-result behavior.

## Acceptance scenarios

### Scenario: Reset prevents an old result from returning

- **Given** I searched for a query and the shell remembered its result URL
- **When** I reset/reload into the fresh `/home/` landing with no query
- **Then** the remembered result URL and scroll offset are cleared
- **And** clicking Search on the main rail leaves the empty search home visible

### Scenario: Sidebar browsing preserves the current result set

- **Given** a search result set is remembered
- **When** I browse a Bible, song, or Tata Ibadah page through the sidebars without resetting
- **Then** the remembered query and scroll offset remain available
- **And** the rail Search action restores that result set

### Scenario: Search clear remains distinct from reset

- **Given** search results are visible
- **When** I clear the query with the ×
- **Then** the input is empty while the current result set remains visible
- **And** the clear action does not itself erase the remembered result URL

### Scenario: There is one search shell

- **Given** the home or result state is rendered
- **Then** the same shell owns the conditional search-home and result regions
- **And** rail Search changes the shell's destination/state rather than mounting a second search page

## Traceability

- E2E: `tests/e2e/test_reading.py` (`test_search_state_survives_sidebar_browsing`, `test_search_icon_never_opens_a_stale_stored_url`, plus reset regression).
- Implementation: `static/web/reading.js` (`storedSearchUrl`, `openSearch`, initial state, and search persistence); `multimedia/web/templates/reading/base.html` holds the two conditional regions.
