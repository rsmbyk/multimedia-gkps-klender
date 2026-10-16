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

- **Domain/app tests:** `tests/test_offline_sync.py`.
- **E2E:** `tests/e2e/test_offline_library.py` and targeted `tests/e2e/test_projector.py` cases.
- **Implementation:** `multimedia/web/reading/offline.py`, `multimedia/web/urls.py`, reading/projector templates, `static/web/offline-library.js`, `static/web/offline-render.js`, `static/web/offline-status.js`, `static/web/projector-library.js`, `static/web/projector.js`, `static/web/reading.js`, and `static/web/service-worker.js`.

## Draft amendment: persistent saved-copy badge

**Status:** Accepted. The [sticky-badge preview](./preview-saved-copy-sticky.html) was approved separately. This section supersedes only the inline placement of the saved-copy label in UI details above.

- On a public Bible chapter, song, or Tata Ibadah page showing saved content, render “Saved copy” as a viewport-fixed badge at the top-right of the reading area. It remains visible as the reader scrolls, consumes no header or content space, and is absent from the home/search and projector pages.
- Use the approved preview's compact pill: 12px text at weight 500, a 6px amber `#b0813b` dot separated by 6px, 7px vertical and 11px horizontal padding, a 1px divider-token border, 999px radius, canvas-token background, and a subtle `0 5px 18px rgba(20, 20, 18, .12)` shadow. Use existing theme tokens for readable light and dark text.
- Position it 16px below the viewport top and `clamp(24px, 5vw, 64px)` from the right. At viewport widths of 800px or less, use 12px top and 18px right. Keep it below open sidebars, popovers, and dialogs in the stacking order and above ordinary reading content.
- The badge is informational, has no focus or click target, and does not intercept pointer input. Hide it when a successful fresh response replaces the saved content, when no saved content is available, or when leaving the affected reading page. Do not show it in print.

### Scenario: saved-copy provenance remains visible

- **Given** a long public Bible chapter, song, or Tata Ibadah page rendered from the saved library
- **When** the reader scrolls through the page while the online refresh has not supplied replacement content
- **Then** the compact “Saved copy” badge stays at the top-right of the viewport without moving the reading header or blocking controls; it disappears once fresh content replaces the saved copy.

## Draft amendment: browser-offline badge color

**Status:** Accepted. The [offline-color preview](./preview-saved-copy-offline.html) was approved separately. This amendment overrides the fixed amber-dot color specified in the saved-copy badge UI details above.

- When the browser reports offline (`navigator.onLine === false`), show the badge's 6px status dot in the existing `--danger` theme token (red in light theme, lifted red in dark theme).
- When the browser reports online, show the dot in the existing amber `#b0813b` saved-copy color.
- Respond to the browser's `offline` and `online` events so the dot changes while the saved-copy badge is visible. Do not infer browser-offline state from slow, failed, or timed-out server requests.

### Scenario: saved-copy dot follows browser connectivity

- **Given** a public reading page is displaying saved content and its “Saved copy” badge
- **When** the browser reports offline, then reports online again
- **Then** the dot changes from amber to the danger theme color, then returns to amber; a delayed or failed server request alone does not change it.

## Draft amendment: separate connection and library readiness

**Status:** Accepted. The [connectivity and availability preview](./preview-connectivity-vs-availability.html) was approved separately.

- In the main-rail offline-library popover, present **Offline library** availability and **Browser connection** as two separate status fields. Do not combine them into a label such as “Ready · offline.”
- Availability describes the saved library and required shells: `Ready for offline use`, `Not ready for offline use`, or `Syncing library…`. A failed update may explain that the previous saved library remains available, while retaining its ready availability state.
- Browser connection displays `Online` or `Offline` from the browser's `navigator.onLine` state and its `online`/`offline` events. It does not change the library availability state.
- Keep the existing Last synced and Last checked fields and Sync now action. Disable the sync action while syncing or while the browser reports offline; show `Sync when online` when offline.
- Use the approved preview's separate connection row with a small status dot: green for online and the existing `--danger` token for offline. Keep the existing library status mark tied only to library availability or sync state.

### Scenario: connection and offline readiness vary independently

- **Given** the offline-library popover is open
- **When** the browser is online or offline and the saved library is ready, not ready, syncing, or retaining a prior generation after an update failure
- **Then** the popover shows the browser connection separately from library availability, including combinations such as Ready + Offline and Not ready + Offline; changing connectivity does not imply that library content became unavailable or ready.

## Draft amendment: bottom-positioned status popover

**Status:** Accepted. The [bottom-positioned preview](./preview-offline-popover-bottom.html) was approved separately. This amendment overrides the popover's existing bottom offset and connection-row spacing only.

- Position the offline-library popover 12px above the viewport bottom, retaining its existing left anchor, maximum width, and narrow-screen side clearance.
- Make the Browser connection row 40px high, with its label and value vertically centered on the same axis. Keep the top divider at the row start and place the Last synced/Last checked divider immediately after the row, with no extra top margin, so the row's text is centered between the dividers.

### Scenario: bottom popover and centered connection row

- **Given** the offline-library popover is open
- **When** it is displayed at desktop or narrow viewport width
- **Then** its bottom edge is 12px above the viewport edge and both Browser connection texts share the vertical center of the row between its dividers.

## Draft amendment: center saved-copy badge

**Status:** Accepted. The owner approved the [centered-badge preview](./preview-saved-copy-centered.html) and this Draft amendment.

- On a public reading page displaying saved content, center the fixed “Saved copy” badge horizontally over the currently visible reading stage, excluding the main rail and any sidebar or chapter column that pushes the stage. Do not center it over the whole browser viewport.
- Keep the badge 16px from the viewport top at widths above 800px and 12px from the top at widths of 800px or less. Keep its center aligned as the viewport is resized or the reading-stage layout changes, including navigation-column open/closed transitions.
- Preserve the existing compact pill without changing its appearance: 12px text at weight 500, a 6px dot with 6px internal gap, 7px vertical and 11px horizontal padding, 1px divider-token border, 999px radius, canvas-token background, and the existing subtle shadow. Preserve the amber and danger dot states, visibility rules, stacking, and pointer-events behavior.
- Do not add layout space or move the reading header or content.

### Scenario: badge centers on the reading stage

- **Given** a public Bible chapter, song, or Tata Ibadah page displays a saved-copy badge
- **When** the reading stage is shown with navigation columns open or closed, the viewport is resized, or the reader scrolls
- **Then** the badge remains fixed at the existing top offset and its horizontal center matches the visible reading-stage center rather than the whole viewport; no reading content shifts.

## Draft amendment: show SIM names in the offline Bible sidebar

**Status:** Accepted. The owner approved the [sidebar preview](./preview-bible-sidebar-sim-labels.html) and accepted this Draft amendment. This changes only the label source in the offline-generated Bible sidebar; the row design remains as shown in the preview.

- When the offline shell builds an expanded Bible book list from saved data, keep the TB translation name as the main label and show the saved `SIM` translation name in the existing secondary-label slot.
- Do not use the internal book abbreviation (for example, `Kej`) as the expanded-row secondary label. If a book has no saved `SIM` translation, omit that secondary label.
- Keep the internal book abbreviation in the existing mini-sidebar abbreviation slot. Do not change the online/server-rendered sidebar, row styles, book order, selected state, navigation, or fetch behavior.
- Use the SIM name for the sidebar's secondary search field and combined accessible label, so filtering and assistive technology describe the same text shown in the row.

### Scenario: cached SIM name appears in the expanded sidebar

- **Given** the saved library contains TB and SIM translations for a Bible book and the browser is offline
- **When** the Bible sidebar is open in its expanded state
- **Then** the row shows the TB name as primary and the SIM translation name as secondary (for example, “Kejadian” and “1 Musa”), with the existing appearance and book order unchanged.

### Scenario: mini sidebar retains its abbreviation

- **Given** the offline Bible sidebar is collapsed to mini mode
- **When** a book has a cached SIM translation
- **Then** its tile continues to show the internal abbreviation (for example, `Kej`) and does not show the SIM name in the tile.

### Scenario: no saved SIM translation

- **Given** a saved Bible book has no SIM translation
- **When** the offline renderer builds its expanded sidebar row
- **Then** the row has no secondary translation label, while the mini tile continues to use the internal abbreviation.

### Scenario: sidebar filtering uses the SIM name

- **Given** the offline expanded Bible sidebar includes a saved SIM name
- **When** the reader filters using that Simalungun name
- **Then** the corresponding book remains visible and its accessible label includes the same SIM name.

## Draft UI details: offline Bible sidebar labels

- **Preview:** [Offline Bible sidebar SIM labels](./preview-bible-sidebar-sim-labels.html).
- **Size / spacing:** Preserve the existing book-row dimensions, 14.5px primary text, and 12.5px secondary text; do not add or remove row spacing.
- **Position / layout:** Keep the SIM name in the current right-hand secondary-label position. Keep the abbreviation centered in the mini tile.
- **Colors / typography:** Preserve existing theme tokens, weight, and dimmed secondary color.
- **States:** Preserve current resting, hover, selected, focus, and mini-sidebar states.
- **Responsive behavior:** Preserve existing sidebar widths and breakpoints; allow the current row clipping behavior to apply to the longer SIM name.
- **Motion:** None added.

## Draft amendment: follow the selected Bible translation in the sidebar

**Status:** Accepted. The owner accepted the [interactive preview](./preview-bible-sidebar-translation-follow.html): only the expanded labels swap and mini tiles keep the existing TB abbreviations.

- On a normal full page load or refresh, start the Bible reading switch in TB. A deliberate SIM choice remains active through in-page Bible navigation, and a full page refresh resets it to TB. An explicit edition URL may select its requested edition on direct load.
- In TB, each expanded Bible row uses its TB book name as the primary label and its SIM book name as the secondary label. In SIM, reverse the two labels. Apply the same rule to server-rendered and saved-copy Bible sidebars, including a sidebar opened after the edition switch.
- Keep the existing `Book.name` abbreviation in `.book__a` for the mini sidebar in both editions. Do not derive a SIM abbreviation or clip its full name into the mini tile.
- Keep both translated names searchable in either edition. Update the row's accessible label and mini-tile tooltip to describe the current primary and secondary names after a switch.
- If a book has no SIM translation, show its TB name as the only expanded label in both editions. A missing SIM version for the current chapter keeps the existing disabled-switch behavior.
- Change visible row text in place when the edition changes. Preserve each row's link, selection, focus, order, filter value, scroll position, and open/mini state. Other public reading sections do not change.

### Scenario: switch from TB to SIM

- **Given** a Bible chapter is open in TB and the expanded sidebar shows `Kejadian · 1 Musa`
- **When** the reader selects SIM
- **Then** the chapter shows SIM text and the same sidebar row shows `1 Musa · Kejadian`, with the same selection, position, and link.

### Scenario: mini sidebar keeps the shared code

- **Given** the Bible sidebar is in mini mode and its `Kejadian` tile shows `Kej`
- **When** the reader switches between TB and SIM
- **Then** the tile continues to show `Kej`; its tooltip and accessible name reflect the current primary book name.

### Scenario: switch back, navigate, and refresh

- **Given** the reader selected SIM
- **When** the reader switches to TB, navigates between Bible chapters in-page, or fully refreshes the page
- **Then** switching to TB restores TB primary labels, in-page navigation retains a deliberate edition choice, and full refresh starts in TB.

### Scenario: saved copy and missing SIM

- **Given** the public Bible sidebar comes from saved data and one book has no SIM translation
- **When** the reader changes edition on a chapter that supports both translations
- **Then** rows with both names swap as above, while the book without SIM keeps its TB name alone; neither case requires a network response.

## Draft UI details: translation-following Bible sidebar

- **Preview:** [Interactive TB/SIM sidebar](./preview-bible-sidebar-translation-follow.html).
- **Size and spacing:** Keep the current 296px expanded sidebar, 38px minimum row height, 14.5px primary name, 12.5px secondary name, and 44px mini tile. Do not change row padding or gap.
- **Position:** Keep the primary name on the left and secondary name on the right. Mini abbreviations remain centered.
- **Colors and states:** Keep existing theme colors and resting, hover, selected, and focus treatments. The switch changes label content only.
- **Responsive behavior:** Retain the existing sidebar breakpoints and row clipping behavior. A long translated primary name can use the existing primary-label ellipsis.
- **Motion:** Do not add label-swap animation or move the sidebar; the existing reading switch motion remains.
