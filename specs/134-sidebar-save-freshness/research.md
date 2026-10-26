# Research: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`
**Unknowns remaining**: 0

## D001 — Use server-rendered saved state for visible refreshes

- **Decision**: Keep the existing successful `editor:saved` signal and reconcile the relevant visible reading regions from a fresh response to the existing Django route. Do not derive edited labels or page fragments from editor form fields.
- **Rationale**: `static/web/editors.js:216-224` dispatches `editor:saved` only after a successful JSON response. `static/web/reading.js:2003-2032` already fetches the current server page after that signal, and the existing DOM reconciler can preserve matching live nodes. The server route is the source for the saved record, related labels, document title, and search counts.
- **Alternatives considered**: Patch text from the editor response (would duplicate server rendering and can miss related headings, counts, or derived labels); reload the full document (would violate the in-place state-preservation requirements); wait for the offline library generation (its asynchronous sync is not the editor-write authority and can delay or reintroduce stale content).
- **Provenance**: Repository inspection — `static/web/editors.js:216-224`, `static/web/reading.js:1511-1580,1583-1615,2003-2032`; runtime reproduction in the disposable live preview documented at `preview/README.md`.

## D002 — Reconcile lists and stage according to the active reading context

- **Decision**: On a save, refresh the shared sidebar row and all other visible representations when the stage represents the edited section. When the operator is viewing an unrelated stage, refresh the sidebar data while leaving that stage and its route in place.
- **Rationale**: The accepted scenarios distinguish an active Tata Ibadah/song stage from a Bible stage with Kidung selected. `static/web/reading.js:1554-1580` currently returns after refreshing the stage and, for Tata Ibadah, its contents list; the shared first and second columns are reconciled afterward at `1583-1615`. The existing handler at `2009-2020` already distinguishes same-section refresh from list-only refresh, so this is an extension of the reading shell's current responsibility.
- **Alternatives considered**: Always replace the full page or stage (would disturb unrelated content and shell state); update the sidebar only (leaves an active stage heading or document title stale).
- **Provenance**: Repository inspection — `static/web/reading.js:80-95,1511-1615,2003-2029`; accepted scenarios US1/AC1–AC4.

## D003 — Refresh search results and their tab-local snapshot together

- **Decision**: When the search-results view is active, fetch the existing query's current result page, reconcile `#searchResults` in place, retain the query and current search history entry, and replace that entry's stored snapshot with the newly rendered result HTML.
- **Rationale**: `static/web/reading.js:1300-1332` stores and restores search HTML in tab-local `sessionStorage`. A fresh server fragment alone is insufficient if the old snapshot is restored afterward. The server search route already computes match membership and group counts, including a removed result.
- **Alternatives considered**: Leave search results as-is and refresh only sidebars (reproduces the confirmed stale result); create a new search history entry (would change the user's current search position); patch the visible result title locally (cannot reliably update query membership, excerpts, or group counts).
- **Provenance**: Repository inspection — `static/web/reading.js:1300-1332,1800-1870,2003-2032`, `multimedia/web/templates/reading/base.html:430-432`; live preview reproduction at `preview/README.md`.

## D004 — Preserve the reader's live shell state during reconciliation

- **Decision**: Keep the current route and search query, selected record, sidebar open/mini/closed states, filters, scroll positions, and focus target around a save refresh; reapply active filters to the saved rows after reconciliation.
- **Rationale**: The existing `applyPage` path already captures scroll and filters and restores focus for in-place updates. The new behavior must expand the refreshed regions without turning a save into main-menu navigation or detaching controls the operator is using.
- **Alternatives considered**: Rebuild the entire shell and reset its controls (would contradict FR-004); locally rename a row without updating its filter membership (would leave a row visible when it no longer matches).
- **Provenance**: Accepted spec FR-004 and edge cases; repository inspection — `static/web/reading.js:1511-1580,1615-1760`; runtime cross-section control described in `preview/README.md`.

## D005 — Keep the change inside the reading shell with no schema or external contract change

- **Decision**: Modify the shared public reading-shell refresh behavior and add Playwright E2E coverage under `tests/e2e/`. Add no database migration, API endpoint, dependency, or separate refresh service. Declare `bump: patch` for this user-visible bug fix.
- **Rationale**: The capability file `docs/spec/reading.md` has no existing requirement for this behavior, and its current requirements are folded as slices touch them. The application already exposes the server-rendered routes and `editor:saved` browser event needed for this slice. `docs/PROCESS.md` SemVer rule VER-10 maps a fix to patch.
- **Alternatives considered**: Add a new reading capability endpoint or persistent freshness state (duplicates existing route rendering and introduces storage/API surface without need); widen the slice to unrelated management, Media Library, projector, or OBS save flows (the audit found separate or read-only flows and no matching shared sidebar editor there).
- **Provenance**: Repository inspection — `docs/spec/reading.md:1-13`, `docs/ARCHITECTURE.md:15-25,92-102`, `docs/PROCESS.md` SDD-03, SDD-12, VER-10; route/editor audit and runtime preview in this slice.

## Open

None. The accepted spec has no clarification markers; the route audit, existing refresh path, server-search behavior, and preview settle the implementation choices above.
