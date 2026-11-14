# Spec: Consistent reading navigation across saved and server data

- **ID:** 181
- **Status:** Accepted
- **Item:** ITEM-182
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An operator opening a public reading menu, sidebar item, search result, or page while online sees current data in the same order and layout as a full server page, without a manual refresh. Saved data remains usable when the network is unavailable.

## Scope

### In scope

- Home, Bible list/book/chapter, Kidung list/songbook/song, Tata Ibadah list/service and dated/template mode, and search routes.
- Rail, first and second sidebars, reading stage, results, in-page links, browser history, normal reload, and hard reload.
- The revisioned saved library and its server/offline rendering parity for these routes.

### Out of scope

- Projector or OBS behavior, editor persistence, new UI controls, and redesign.

## Rules

- With a successful online request, the final visible content for the opened route reflects the current server state, including additions, edits, deletions, labels, row counts, ordering, and layout structure. It must match a full load of the same URL.
- A saved copy may appear immediately while current data loads. Its existing saved-source indication stays truthful until current data is applied. On request failure, keep the saved content and its indication; do not imply it is current.
- Each supported route gets an online freshness path. A missing chunk URL for a list, book, home, or search route must not prevent refresh.
- An older response or library commit cannot replace a later navigation or an active edit refresh.
- Offline routes render from one complete committed library generation. They use the server's canonical ordering rules, including same-date Tata Ibadah creation-time order and the established songbook/song orders. Required sort metadata is serialized with the saved data.
- Updating content preserves the operator's live sidebar open/mini state, filters, scroll positions, deliberate Bible edition, search context, and focus where those are already preserved by the current UI contract. Full reload and new-tab edition reset remain as specified previously.
- Browser Back/Forward into an existing search entry restores that entry's saved result generation, input, and scroll position. A new search submission uses current online data.
- Normal and hard reloads of an online route must settle to the same data, order, and layout as an in-page opening of that route.

## Acceptance scenarios

### Scenario: Online menu and sidebar navigation with an older saved library

- **Given** a complete saved generation and newer server data for Bible, Kidung, Tata Ibadah, or search
- **When** the operator opens each affected menu, first-level item, second-level item, result, or history entry from `/home/`
- **Then** the final visible view matches a full online load of that URL without manual refresh
- **And** the saved copy remains available if the current request fails.

### Scenario: Same-day Tata Ibadah ordering

- **Given** two dated services on the same day whose creation-time order differs from their ID order
- **When** the operator opens the dated service sidebar online or from a saved offline generation
- **Then** both sidebars show the same newest-created-first order and the same month grouping.

### Scenario: Content changes during navigation

- **Given** a saved view and delayed online responses
- **When** the operator opens another route before the first response completes
- **Then** the earlier response cannot replace the later route or change its sidebars, results, or stage.

### Scenario: Offline and refresh behavior

- **Given** a complete saved generation and an unavailable network
- **When** the operator opens the supported routes from the home page
- **Then** each displays its saved content and indicates its saved source where applicable
- **And** a later successful online navigation settles on current data without requiring a normal or hard reload.

## Traceability

- Domain/app tests: `multimedia/web/reading/tests.py` or an existing focused module for canonical ordering and serialized sort metadata.
- E2E: `tests/e2e/test_navigation_freshness.py`, `tests/e2e/test_offline_library.py`, and `tests/e2e/test_reading.py`.
- Implementation: `static/web/reading.js`, `static/web/offline-render.js`, `multimedia/web/reading/offline.py`.
