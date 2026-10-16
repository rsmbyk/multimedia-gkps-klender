# Plan 092: Offline public reading and service projection

- **Status:** Accepted
- **Preview:** [Offline library status](./preview.html)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-095
- **Bump:** minor

## Why

The public reading page currently downloads another HTML page for in-app navigation. The projector downloads its whole page again after an order edit, and Go To needs server requests. Readers and operators need the saved Bible, songs, and Tata Ibadah content to remain available when the connection drops, while online visits quietly pick up changed content.

## Scope

**In:**

- Two offline page shells: the public reading site, including its home/index, and the service projector at `/obs/service/<id>/`.
- Browser-wide saved Bible, song, and public Tata Ibadah data, with complete local generations, incremental updates, and a truthful sidebar sync status.
- One saved Tata Ibadah snapshot per service, containing enough data for both public reading and projector screens; no separate service-order download for the projector.
- Data-only navigation and asynchronous content refresh for public Bible chapters, songs, and Tata Ibadah pages. The saved content appears immediately when available.
- Local projector Go To and local projector startup when its shell and selected service snapshot are available. An open projector can observe a newly committed local library generation without waiting for it before opening.
- Browser history and direct-link behavior below.

**Out:**

- The older OBS sources and docks, editor and admin pages, and automatic offline support for future standalone pages. The service worker must pass these routes through without caching or replacing their responses.
- Offline edit submission or an edit queue. Reading works offline; saves still need the server.
- A preparation gate or loading modal before the Project button opens the projector window.

## Browser navigation contract

- Add a browser-history entry only when opening **end content**: a Bible chapter such as `Kejadian 1`, a song such as `KJ 123`, or a Tata Ibadah such as `Ibadah Minggu`. This includes opening an end-content result from Search.
- Main-rail and first-level sidebar moves (opening/browsing section, book, songbook, or service-list panels; filters; and panel toggles) do not create history entries. Selecting a Tata Ibadah itself opens end content and does. The Search destination is the exception among main-rail actions.
- `/search?q=...` is used only for search results and carries the query in its URL parameters. A direct visit with a valid query must render that result set. Each submitted non-empty search creates a history entry; typing alone does not.
- The index `/` is the empty-search landing. Clearing or submitting an empty search does not create an empty search-results URL.
- The GKPS rail logo always opens the index with an empty search field. This does not erase the tab's last search. The main-rail Search action opens that index when the tab has no saved search; otherwise it restores the tab's latest search, including its displayed results, expanded/"Show more" counts, scroll position, and unsent text in the search field.
- Save the latest search separately for each browser tab, including across a same-tab reload. A newly opened tab starts without another tab's last search. A direct visit to `/search?q=...` initializes or replaces that tab's saved latest search from the URL, even if the tab previously held another search. An empty or invalid search URL resolves to the index.
- Every non-empty search submission creates a fresh `/search?q=...` history entry and runs the search again, even when the normalized query equals the previous query. Its results may reflect newer server data. Do not reuse an earlier same-query result snapshot for this new submission.
- Search a newly submitted query against the latest complete locally committed library generation; a completed background sync can change a later submission's results without delaying typing. Preserve each earlier history entry's result snapshot.
- Give each search history entry its own result snapshot and view state: result ordering/content, expanded/"Show more" counts, scroll position, and current search-field text. Before leaving an entry, update its snapshot. Back/Forward restores that entry as seen, including unsent text, without issuing a new search or replacing it with the tab's latest search. Loading more or editing the field updates the current entry rather than pushing a new one. Restoring the latest search from the rail reuses its snapshot rather than rerunning the query.
- Back and Forward restore the selected end content or search result from the saved library when offline. Direct URLs and refreshes for included public-reading routes and the service projector resolve through their cached shell and saved content.
- The current server uses `/` and a temporary `/home/` landing, plus `/search/` for results. Use the requested slashless `/search` as the canonical result URL in this work; preserve `/search/` links by redirecting with query parameters intact. A result URL without a valid non-empty query resolves to the index. Keep `/home/` links compatible with the index outside maintenance mode.

## Approach

- Publish a small revision manifest and changed-data endpoints for Bible, songs, and public Tata Ibadah. Keep the saved complete generation usable if an update fails.
- Cache the two page shells and required assets with versioned service-worker caches. Intercept only explicit public-reading and service-projector routes; avoid changing legacy OBS dock responses.
- Store content and metadata in IndexedDB. Share committed updates across same-origin tabs; update the projected Go To library on the next lookup without altering the currently shown screen.
- Render public reading and projector content from saved data, then refresh from data-only server responses when online. Preserve existing sidebar state, keyboard behavior, projector controls, and editing flows.
- Add History API handling for the contract above, including `popstate`, canonical direct links, and scroll restoration for search results and reading destinations. Keep compact per-entry state in browser history and tab-scoped result snapshots outside shared `localStorage`; avoid copying saved searches into a newly opened tab (including opener-created tabs). Do not put large result payloads in `history.state`.

## Validation and risks

- Test cold/returning visits, reconnect, failed or interrupted sync, browser storage loss, deploy updates, direct offline links, browser Back/Forward, and URL query restoration.
- Verify that every end-content route creates one history entry, while first-level navigation creates none; test search submission and empty search separately. Cover repeated same-query submissions with changed results, logo versus Search rail behavior, independent/new tabs, direct search URLs replacing the tab's saved search, Show more, unsent field text, scroll, and Back/Forward restoration of distinct same-query entries.
- Test that old OBS docks, editor/admin routes, and unrelated future pages still use their existing behavior.
- Keep existing projector screens visible if a later refresh fails. Do not mark the site offline-ready unless both shells and a complete data generation are actually present.

## Draft amendment: persistent saved-copy badge

- **Status:** Accepted; the [visual preview](./preview-saved-copy-sticky.html) was approved separately.
- **Why:** The current inline “Saved copy” label scrolls out of view, so the reader can lose track of whether the displayed content came from local storage.
- **Scope:** Change only the public reading page's saved-copy indicator placement and presentation. Keep its provenance rules, wording, sync behavior, and live-content layout unchanged.
- **Approach:** Show a small, noninteractive badge fixed near the top-right of the reading viewport whenever saved content is being displayed. Remove its inline space above the reading header. Keep it visible through content scrolling and below open panels or dialogs. Hide it as soon as fresh content replaces the saved copy.
- **Validation:** Check long Bible, song, and Tata Ibadah pages; successful and failed online refresh; light/dark themes; narrow viewports; and scrolling with sidebar or modal overlays.

## Draft amendment: browser-offline badge color

- **Status:** Accepted; the [offline-color preview](./preview-saved-copy-offline.html) was approved separately.
- **Why:** Make the browser's offline state visible at a glance while saved reading content remains on screen.
- **Scope:** Change only the status dot on the saved-copy badge. The browser's online/offline status is the sole trigger; request duration or failure does not affect the color.
- **Approach:** Use the existing danger color token while the browser reports offline, and the existing amber saved-copy color while it reports online. Update immediately on the browser's `offline` and `online` events.
- **Validation:** Check both transitions in light and dark themes and confirm a failed or delayed content request alone leaves the amber dot unchanged.

## Draft amendment: separate connection and library readiness

- **Status:** Accepted; the [connectivity and availability preview](./preview-connectivity-vs-availability.html) was approved separately.
- **Why:** “Ready · offline” combines two independent facts: whether the browser reports a connection and whether the saved library is usable offline.
- **Scope:** Clarify both states in the main-rail offline-library popover while preserving the existing sync action and timestamps.
- **Approach:** Label the library availability (`Ready for offline use`, `Not ready for offline use`, or `Syncing library`) separately from a `Browser connection` row (`Online` or `Offline`). Base availability on the saved library and required shells; base connection only on the browser's online/offline state.
- **Validation:** Review ready/online, ready/offline, not-ready/offline, syncing/offline, and update-failed/online combinations in light and dark themes.

## Draft amendment: bottom-positioned status popover

- **Status:** Accepted; the [bottom-positioned preview](./preview-offline-popover-bottom.html) was approved separately.
- **Why:** The status popover should sit lower, and the connection row's text should appear centered between its separators.
- **Scope:** Change only the popover's bottom offset and the connection row's vertical spacing and alignment.
- **Approach:** Set the popover 12px above the viewport bottom. Give the connection row a 40px height, center its label and value within that height, and place the following metadata divider immediately after the row so spacing around the row is balanced.
- **Validation:** Check the approved layout at desktop and narrow widths and confirm the row's labels share the same vertical center between its dividers.

## Draft amendment: center saved-copy badge

- **Status:** Accepted; the [centered-badge preview](./preview-saved-copy-centered.html) and this Draft amendment were approved by the owner.
- **Why:** Centering the fixed badge in the entire viewport leaves it visually offset from the reading page when navigation columns occupy the left side.
- **Scope:** Change only the saved-copy badge's horizontal position. Preserve its wording, appearance, browser-offline dot, visibility rules, and fixed top placement.
- **Approach:** Center the badge on the currently visible reading stage, excluding the main rail and any sidebar or chapter column that pushes the stage. Keep it fixed 16px from the top on wider screens and 12px from the top at widths of 800px or less. Recalculate its center when the viewport or reading-stage layout changes, including sidebar open/closed changes. Retain the existing 12px type, 6px dot and gap, 7px/11px padding, border, pill radius, shadow, theme colors, and click-through behavior.
- **Validation:** Check the badge against the reading-stage center with navigation columns open and closed, at wide and narrow widths, and while scrolling; confirm it does not shift reading content or cover reading controls.
