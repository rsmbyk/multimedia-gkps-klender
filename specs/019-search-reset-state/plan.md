# Plan 019: Clear remembered search when the home is reset

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-021
- **Bump:** patch

## Why

Resetting/reloading to the empty home view leaves the prior result URL in local storage, so clicking the rail Search action restores an old session's results. The cause is remembered state, not duplicate search routes or two mounted search pages.

## Scope / edges

**In:** Lifecycle of the remembered result URL and scroll offset when the shell initializes a fresh, unqueried home at `/home/`.

**Out:** Changing the search route, URL behavior, clear-× behavior, or the accepted ability to return to a result set while browsing sidebars.

## Approach

- Keep the existing single shell and its two conditional stage regions (`#searchHome` and `#searchResults`); they are home and result states, not duplicate pages.
- Treat a fresh home landing at `/home/` with no query as Reset. Clear `gkps-search` and `gkps-search-scroll`, and ensure the rail Search href resolves to the empty home.
- Do not clear remembered results when leaving a result set to browse a reading sidebar; Search still restores that result until an explicit reset.
- Keep the search-field × behavior unchanged: it clears the input but retains the visible result set.

## TDD

- E2E: `tests/e2e/test_reading.py` — query → in-place browse → fresh home reset → rail Search remains empty; existing result-set/sidebar restoration test remains green.

## Risks

- Clear state only on the explicit home reset path; clearing on every page with `home_state='landing'` would break result restoration during ordinary reading navigation.
- The shell intentionally does not change the address bar for in-page navigation, so test the actual home/reset path and stored scroll state, not only DOM visibility.
