# Spec: Saved reading page parity

- **ID:** 122
- **Status:** Accepted
- **Item:** ITEM-122
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Opening a saved reading route through the menu or sidebars should show the same labels, headings, references, controls, and layout as opening or reloading that URL directly. The operator should not see a mismatched page while an online refresh is pending, and the saved view should remain correct offline.

## Reproduced behavior

On the current `develop` server at `localhost:63404`, after `GKPSOffline.sync()` and sidebar navigation to `/songs/1823/`, the immediate view showed `Filter books...` and `712. TOGU AU ALE JAHOWA`; the settled online view and reload showed `Filter songbooks...` and `BUKU ENDE HKBP`. Opening `/tatib/148/` likewise showed `Filter books...` before the online update changed it to `Filter Tata Ibadah...`. The supplied screenshots also show missing icons and different spacing in the empty Tata Ibadah action buttons before reload. The reproduction used a fresh isolated Playwright browser and the current local server; the mismatch occurred immediately after the sidebar click.

A wider saved-document/server-document comparison covered `/home/`, Bible list/book/chapter in TB and SIM, Kidung list/hymn book/ordinary songbook/song, Tata Ibadah list/service/template mode, and search. Confirmed meaningful differences include the Kidung and Tata Ibadah list placeholders, Bible chapter-sidebar accessible headings (`Chapters — 1 Musa` or `Chapters — Kejadian` versus `Chapters — Kejadian (1 Musa)`), hymn child-row references (`1` versus `HAL 1`), songbook/song sidebar headings, non-hymn song eyebrows (`a` versus `Lagu` in the sampled route), and empty-service action icons. The saved song sort key also retained a leading space after a title number where the server removed it, which could alter the A-Z row order. Search showed no differences in the compared fields. Pure HTML whitespace differences were excluded. Media Library and Manage do not use this saved reading renderer; they were checked for route applicability, not certified for all interaction parity.

## Scope

### In scope

- Saved Home, Bible, Kidung, Tata Ibadah, and search pages reached through menus, sidebars, search/history where those paths reuse the saved renderer, and direct offline boot.
- Filter placeholder, accessible headings, songbook row references, song eyebrow/citation, empty-service action icons and spacing, and other meaningful markup in these views that differs between saved rendering and the server page.
- Preserve the current content, selection, sidebar state, and truthful saved-source indicator while the online update runs.

### Out of scope

- Redesign, new content or sorting rules, projector/OBS, and editor save/list-refresh behavior.

## UI contract

- The existing server-rendered page for the same URL is the visual and content reference. The supplied image pairs are examples for `/tatib/148/` and `/songs/1823/`.
- No new sizes, colors, transitions, or controls. Existing hover, focus, and responsive behavior stays as rendered by the server page.
- When offline, the saved page uses the same meaningful heading, labels, icon presence, action order, and spacing as the server page.

## Acceptance scenarios

### Scenario: Open a song from the sidebar

- **Given** a synced saved library containing Buku Ende HKBP song 712
- **When** the operator opens `/songs/1823/` through the sidebar
- **Then** the first rendered song view has `Filter songbooks...` and `BUKU ENDE HKBP`, and its sidebar/stage markup matches a reload of that URL.

### Scenario: Open an empty service order

- **Given** a synced saved library containing empty Tata Ibadah `/tatib/148/`
- **When** the operator opens it through the sidebar
- **Then** the first rendered view has `Filter Tata Ibadah...`, and the Add Passage, Song, Text, Break, and Media actions match the server view in order, icons, and spacing.

### Scenario: Online and offline parity

- **Given** the same saved library
- **When** the operator opens Home, Bible, Kidung, Tata Ibadah, and search reading routes online, reloads them, then opens them with the network unavailable
- **Then** route-specific headings, labels, controls, and layout remain consistent across these paths; online refresh may update changed content without a wrong intermediate heading or placeholder.

### Scenario: Bible and songbook child sidebar

- **Given** a synced library containing a Bible book with translated name and a numbered hymn book
- **When** the operator opens a book/chapter or songbook/song through a sidebar
- **Then** child-sidebar headings and accessible names match the server page, and numbered hymn rows use the same displayed book prefix and number as after reload.

### Scenario: Ordinary songbook song

- **Given** a synced library containing an unnumbered song in the ordinary songbook `Lagu`
- **When** the operator opens that song from its sidebar
- **Then** the eyebrow identifies `Lagu`, and the child-sidebar heading matches the reloaded server page.

## Traceability

- Browser regression: `tests/e2e/test_saved_render_parity.py`, with existing navigation and offline modules as checks.
- Implementation: `static/web/offline-render.js` for route-specific saved markup; `multimedia/web/reading/offline.py` for the same song sort key as the server.
