# Spec 092: Offline public reading and service projection

- **ID:** 092
- **Status:** Accepted
- **Item:** ITEM-095
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor
- **Preview:** [offline library status](./preview.html)

## Intent

Keep public Bible, song, and Tata Ibadah reading and the service projector usable after an initial online visit. Navigation should use a saved shell and saved content immediately, while later online checks update changed records without blocking the reader or projector. Search navigation must work as browser history and retain distinct per-tab result states.

## Scope

### In scope

- Exactly two offline-capable shells: public reading routes (including `/` and `/search?q=...`) and `/obs/service/<id>/`. Cache only their required versioned assets.
- Complete public Bible translations, hymn and non-hymn songs, public Tata Ibadah data, and one reading/projection-ready snapshot per service in persistent browser storage.
- Initial and incremental sync, cross-tab commit notification, status control and saved-copy indicator, data-only reading navigation, local projector Go To, direct URLs, and browser history.

### Out of scope

- Legacy OBS sources/docks, editor/admin routes, automatic coverage of future pages, offline saves or an edit queue, and a Project-button preparation overlay. Existing online editor writes keep their current behavior.
- Changing the song-only scope of bookmarks or introducing offline bookmark edits.

## Domain rules

- On the first online visit, download complete Bible, song, and public Tata Ibadah data plus both shells and required assets. A sync generation is usable only after all required records validate and commit. Failed or interrupted downloads leave the previous complete generation intact. If none exists, do not claim offline readiness.
- Later visits and explicit Sync now check a server revision manifest, fetch only changed or removed records, and atomically publish a complete new generation. Timestamp Last checked after a check and Last synced after a successful commit; neither proves readiness by itself. Detect missing/evicted shell or content storage before showing Ready.
- Store one service snapshot sufficient to render public reading and projector screens. The projector opens immediately using the currently available service path, with no sync wait or preflight overlay. If its cached shell and service snapshot are available, it can open offline. Same-browser editor updates and committed background syncs may update an open projector; preserve its current screen where possible. A failed refresh leaves the displayed screens intact.
- Public reading renders a saved chapter, song, or service immediately when available. When online, request only current content data asynchronously, apply a valid fresher response, and save it. If that request fails, retain the saved content and show its saved-copy provenance; do not replace it with an error page. If no saved content exists and the request fails, show a clear unavailable state rather than a false saved copy.
- Projector Go To searches only locally committed complete Bible/song data and opens content from that same saved library. It does not issue a lookup or content fetch per keystroke/selection. A newly committed generation becomes available to the next lookup without interrupting the active projected screen. The former per-selection Go To fetch-failure state is removed.
- A service worker intercepts only the explicit public-reading and service-projector navigation allowlist and their versioned assets. It serves a saved shell for direct URL, reload, or offline navigation after successful initial installation. Other routes, especially legacy OBS docks, pass through unchanged. A new deployment prepares new assets before activation; an already open page is not forcibly interrupted.
- A pasted address-bar URL starts a new document navigation. For included routes the service worker may supply the saved shell, which then resolves the URL from saved content. In-app navigation reuses the running shell and updates content and history without downloading another HTML page.

## Browser navigation and search

- End-content navigation to a Bible chapter, song, or Tata Ibadah creates a history entry. First-level sidebar and main-rail browsing does not, except navigation to Search. Back/Forward and direct links resolve the selected content and preserve sidebar state. `/` is the empty-search index; `/search?q=...` is the canonical results URL. Keep `/search/` and `/home/` compatible with existing links, preserving search query parameters.
- Clicking the GKPS logo shows `/` with an empty search field without deleting the tab's last search. The Search rail opens `/` if this tab has not searched; otherwise it restores this tab's latest result set, expanded/Show more state, scroll position, and unsent field text.
- Each tab has independent search memory; a newly opened tab starts empty unless its direct URL is a valid `/search?q=...`. A direct search URL replaces that tab's latest saved search with results for that URL. Do not propagate another tab's search state through shared `localStorage` or an opener-copied session.
- Each submitted non-empty search creates a new history entry and computes fresh results from the latest complete local library generation, even when the query repeats exactly. Typing alone, clearing the field, and Show more do not push an entry. Empty submission resolves to the index, not an empty results URL.
- Each search history entry retains its own result set/order, expanded counts, scroll position, and current typed field value. Snapshot it before leaving or changing entries. Back/Forward restores that snapshot without rerunning the search, including when a later same-query search produced different results. The Search rail restores the latest tab search snapshot rather than replacing an older history entry's state.
- Keep history metadata compact; store potentially large result snapshots in tab-scoped storage. Restoring a search URL after reload uses its entry snapshot if present and the URL query otherwise. Browser history and tab memory may be discarded with the tab, without affecting the shared offline library.

## UI details

- Match the [approved interactive preview](./preview.html) and existing reading theme tokens. Put a 44×44px icon-only sync button in the main rail immediately above the theme toggle, with the existing 8px footer-button gap and a 9×9px status dot at its lower-right (4px from each edge). The rail is 80px wide normally and 64px at the existing narrow breakpoint. Do not resize existing rail buttons.
- Anchor a 320px maximum-width status popover 10px to the right of the rail and 72px above the viewport bottom; keep it inside the viewport with at least 12px clearance on narrow screens. Use 16px vertical/17px horizontal padding, 1px divider-token border, 10px radius, and the existing canvas/ink tokens. It does not dim the reading page.
- Use a 14px semibold state title beside a 10px status mark; 12px detail, Last synced, and Last checked text; 17px top separation and a 12px top-padded divider before metadata; a full-width Sync now button with 8px vertical/10px horizontal padding. The saved-copy label beside reading content is 12px with a 6px amber mark and 6px internal gap.
- Ready uses green `#2d8460`; syncing and failed-update-with-saved-copy use amber `#b0813b`; no complete saved copy uses `--danger`. Resting icon color uses `--icon`; hover fills `--icon-hover-bg`; open uses `--active-bg`/`--active-ink`. Keyboard focus has a 2px `--focus` outline at 3px offset. Keep text readable in light and dark themes.
- The popover shows Ready, Syncing, Ready offline, Update failed with saved copy, or Not ready offline, with matching last-sync/check text. Sync now is disabled while already syncing or disconnected; progress is a 3px bar with a 1.1s sweep during sync. Reduced-motion users see a static bar. Clicking the icon toggles the popover; outside click closes it. The icon and button have accessible names and expanded/disabled states.

## Acceptance scenarios

### Scenario: first complete offline save

- **Given** a first online public visit with no saved library
- **When** the initial download completes and both allowed shells and all required data commit
- **Then** the status reports Ready with a sync time; after disconnection, a direct Bible, song, service, or included projector URL can load its shell and content.

### Scenario: interrupted or incremental sync

- **Given** a complete saved generation
- **When** a revision check finds changed records and their download fails partway
- **Then** the previous generation remains readable, the status reports the failed update with saved copy, and a later retry can commit changed records without downloading unchanged content.

### Scenario: current content while online

- **Given** saved reading content
- **When** the reader opens it online
- **Then** it appears immediately, a data-only refresh can update it asynchronously, and a failed refresh leaves the saved text visible with saved-copy provenance.

### Scenario: projector and Go To offline

- **Given** a saved projector shell, service snapshot, and complete local library
- **When** the operator opens the projector offline and uses Go To
- **Then** the window opens without a preflight wait; service screens and Go To content come from saved data, with no per-selection network dependency.

### Scenario: direct URL and unsupported routes

- **Given** installed offline shells
- **When** a reader pastes an included reading URL in the address bar while offline
- **Then** a new document loads from the saved shell and resolves that URL locally; legacy OBS docks and editor/admin routes retain their existing network behavior.

### Scenario: independent search tabs and repeated query

- **Given** a tab displaying search results with more rows expanded, unsent field text, and a nonzero scroll position
- **When** Search is clicked after reading content, the same query is submitted again, or another tab opens
- **Then** Search restores that tab's latest snapshot, the repeat submission creates a distinct freshly computed history entry, and the other tab starts with no copied last search.

### Scenario: direct search and history restoration

- **Given** different result sets saved in two history entries for the same query
- **When** the reader uses Back/Forward or pastes a different `/search?q=...` URL
- **Then** Back/Forward restores each entry's own results, expanded counts, scroll, and typed text; the pasted URL starts a new document and replaces only that tab's latest search.

### Scenario: rail destinations

- **Given** a tab with a saved last search
- **When** the GKPS logo opens the index and then Search is clicked
- **Then** the index shows an empty field and Search restores the saved last search; browsing first-level sidebars adds no history entry.

## Traceability

- **Domain/app tests:** `multimedia/web/tests/test_offline_sync.py`, `multimedia/web/tests/test_reading_data.py` (create or adapt during implementation).
- **E2E:** `tests/e2e/test_reading.py` and `tests/e2e/test_projector.py` targeted classes for offline, status, direct navigation, and search history.
- **Implementation:** reading views/URLs and templates, `static/web/reading.js`, `static/web/projector.js`, new scoped service worker and browser library store, and narrow revision/data endpoints. Final paths recorded during implementation.
