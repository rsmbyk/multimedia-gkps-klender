# Spec 091: Quiet controls for the mirrored service projector

- **ID:** 091
- **Status:** Accepted
- **Item:** ITEM-094
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor
- **Preview:** [interactive 1366×768 projector](./preview.html), [states and measurements](./preview-gallery.html)

## Intent

An operator at a single mirrored laptop must be able to identify the current service screen, see what follows, jump to an entry, and operate the projector entirely by keyboard or entirely by mouse without opening a visible editor or dock. The controls stay quiet enough for the congregation-facing display.

## Scope

### In scope

- The Tata Ibadah service projector page: lyric/header fitting, one-line corner HUD, service entry list, shortcut sheet, pointer and HUD inactivity, keyboard and mouse navigation, passage translation, and find/library detours.
- Direct jumps within the active service order and its selected song baits; an unplanned passage or song temporarily opened through G.
- The existing projector fullscreen path where supported by the browser.

### Out of scope

- OBS projector sources and old docks; service-editor layout or saved service content.
- A second-screen operator interface, phone remote, neighboring-song navigation during a library-song detour, and browser-reserved Ctrl+Page Up/Down.
- Persisting a projector-only TB/SIM flip to `ServiceEntry.book_translation`.

## Domain rules

- The projector uses the active service's ordered entries. A direct entry jump starts at that entry's first screen (and first selected bait for a song). The next-entry cue follows the real order and remains present on lyric rests and section breaks.
- A service passage cue shows its full reference including ending verse and a TB/SIM label. T or a click on that label flips only the projected translation at the same place; the new label brightens for about one second. Neither the saved entry nor the service order changes.
- A hymn song cue uses short songbook, number, and sub-number; a non-hymn song uses its title. A service song lists only selected lyric baits; a song opened by G lists all its baits. The current bait is highlighted. The split counter counts lyric screens inside the current bait, not its blank rest.
- A titled Text cue uses its title. An untitled Text cue uses its first non-empty body line, set obliquely wherever it serves as current or next-entry identity. A Text split counter counts that entry's lyric screens.
- A blank rest remains associated with its preceding bait or entry. It adds no “rest” label or split counter. Between baits, the next bait number is highlighted; after the final bait, the arrow and next entry are highlighted. A section break leaves its own label dim and highlights the arrow and next entry.
- A G library detour remembers the exact service screen left. Escape returns there. An unplanned passage may walk verses, chapters, and books; a song may walk its baits. Its cue shows the way back to the service. Ctrl does not leave a detour.
- Mouse clicks and keyboard commands invoke the same display, step, bait, entry, and translation operations. Hiding words does not hide the corner. C explicitly hides the corner and keyboard button until C restores them; ordinary activity does not undo that choice.

## Keyboard controls

| Context | Keys | Action |
| --- | --- | --- |
| Service | Right, Down, Page Down / Left, Up, Page Up | Next / previous projected step, including built-in blank rests |
| Service | Home / End | First / last screen within the current unit; no service-wide jump |
| Service song | Shift+Right or Shift+Page Down / Shift+Left or Shift+Page Up | Next / previous selected bait |
| Service song | Shift+Home / Shift+End | First / last selected bait |
| Service | Ctrl+Right / Ctrl+Left | Next / previous entry directly |
| Service | Ctrl+Home / Ctrl+End | First / last service entry |
| G passage | Plain arrows and Page Up/Down; Home/End | Walk verses; first/last verse of current chapter |
| G passage | Shift+Left/Right or Shift+Page Up/Down; Shift+Home/End | Previous/next chapter; first/last chapter of book, landing on verse 1 |
| G passage | Ctrl+Left/Right; Ctrl+Home/End | Previous/next book; first/last book, landing on chapter 1 verse 1 |
| Song or G song | Shift+Left/Right or Shift+Page Up/Down; Shift+Home/End | Previous/next bait; first/last bait |
| Passage | T | Flip TB/SIM on the current passage without saving it |
| Display | Space | Toggle words only; leave HUD and keyboard button available |
| Display | C | Hide or restore the corner HUD and keyboard button, except while typing in find |
| Find | J / G / B | Find within service labels / passage or song library / current song baits |
| Find open | Up/Down, Enter, Backspace, Escape | Previous/next match; open match; delete or close when empty; close find |
| Detour | Escape | Return to the service screen left, after any find or popup is closed |
| Shortcut sheet or entry list | Escape | Close the open layer without navigating |

- Enter never toggles words. Ctrl+Page Up/Down remain browser tab commands. Alt+Left/Right remain browser history commands.
- J matches this service's entry labels. G uses the existing passage/song picker syntax and search data. B targets available baits on the current song.
- On JS-entered fullscreen, request the browser's supported keyboard lock for a short Escape; allow a held Escape to leave fullscreen. F11 fullscreen follows browser behavior. Do not claim the page can intercept a browser-reserved key when the browser does not provide it.
- When browser fullscreen is available, any click in the projection area while windowed enters fullscreen only: it never steps or toggles the words. A fullscreen cursor indicates this on hover. Subsequent clicks navigate normally. After leaving fullscreen, the next projection-area click again enters fullscreen only. HUD buttons retain their explicit actions. If fullscreen is unavailable, windowed mouse navigation remains usable.

## UI details

The approved preview is the geometry and appearance reference; its five sample entries do not limit a real service list.

- **Projector stage:** Reference output 1366×768px; background `#14130F`, body `#F5F3EE`, header `#FFD166`. Padding: 32px top/left/right and 64px bottom. The header stays at the top of the remaining 1302×672px text stage. Body text uses the remaining height, starts at 200px, and shrinks to fit. Header font size is body size divided by the golden ratio (about 0.618×). The minimum gap from header to body is one em of header size. Wrapped line height is 1.37; separate literal entry lines have a 0.45em gap. Long lines wrap and the fitting calculation accounts for both kinds of line.
- **HUD geometry:** A single 24px-high row centered at y=736px in the reference output's 64px bottom band. The cue starts 32px from the left and ends 84px from the right, uses 16px text, weight 650, and a dim `#6E6A62` base. Current highlights use `#E8E4DC`. Its list icon is 24×24px, followed by a center dot; cue parts and arrows share the same vertical center. The keyboard icon is 34×24px, 32px from the right, with a 20px bottom inset. Both controls align vertically. Hover is a slight lightening; pressed controls dim or use the darker active fill. Keyboard focus has a visible light outline.
- **Shortcut sheet:** Opens centered over the unchanged verse with a dim backdrop; `#14130F` surface, `#3a372f` 1px border, 10px radius, 20px vertical/24px horizontal padding, and 32px column gap. Group headings are 11px. Rows use 11px descriptions, 3px vertical padding, and restrained separators; groups have 24px vertical separation. Keys are 28px high and 28px wide for letters, symbols, and arrows; named keys, Ctrl/Command-style, Shift, Enter, and Backspace are 56px wide; Space is 84px. Letter labels are 11px, named labels 9px, and symbol marks 13px, all regular weight. The sheet groups service, song, passage, library passage, library detour, display, find, and fullscreen controls as in the preview. Clicking the dim backdrop or Escape closes it without projector navigation. While open, projector and HUD navigation clicks are blocked.
- **Service entry list:** The icon-only button at the far left of the cue opens a 360px-wide, at-most-560px-high scrollable panel, 32px from the left and 58px from the bottom. It uses the projector `#14130F` surface, `#3a372f` border, 10px radius, and quiet shadow. Rows have a numeric column, a short title, and a 10px second line only when useful (such as selected baits). The current row has a muted inset marker; row hover uses `#2a2722`. The panel scrolls its current row into view. A slight dark overlay covers the rest of the output and catches clicks with one close cursor; clicking it or pressing Escape closes the list without navigation. A row click jumps to that entry and closes the list. Underlying HUD and screen controls cannot be clicked through the overlay.
- **Mouse areas:** Above the 64px bottom band only, invisible left/middle/right regions occupy 40%/20%/40% of width and perform previous step / show-hide words / next step. A muted left/right arrow or show/hide cursor indicates the action. The bottom band remains reserved for the HUD. Cue bait numbers jump to that bait; translation label acts like T; the arrow plus next-entry text is one next-entry button. Each has a modest hover and pressed treatment.
- **Inactivity:** Pointer disappears after two seconds without movement or click and reappears on movement or click. Corner cue and keyboard button fade after 30 seconds without mouse or keyboard activity, with a 180ms transition, and reappear on the first activity. They do not auto-hide while the shortcut sheet or entry list is open. The manual C-hidden state never reappears merely from activity.
- **Responsive behavior:** Preserve these proportions and centered content when the viewport differs from 1366×768. The lyric font shrinks to fit available space; controls and their overlays stay inside the projector output and the shortcut sheet/list remain scrollable rather than clipping content. No title, key row, or list action becomes unreachable. Fullscreen uses the same layout rules.

## Acceptance scenarios

### Scenario: Header and lyric fitting

- **Given** a passage or text with a header and literal lines that may wrap
- **When** it is projected at the reference size or a smaller viewport
- **Then** the header remains top-aligned, its font is body font divided by the golden ratio, and body text begins no closer than the header's one-em bottom margin and fits above the 64px bottom band.

### Scenario: Corner identity and rests

- **Given** passages, selected-bait hymns, non-hymn songs, titled and untitled texts, built-in rests, and section breaks in the service
- **When** the operator advances through them
- **Then** the cue shows the specified current identity, split or selected-bait state, and real next entry; rests add no label and highlight the upcoming bait or entry; a break highlights its outgoing arrow and entry.

### Scenario: Keyboard-only operation

- **Given** a projector with no mouse activity
- **When** the operator uses plain, Shift, and Ctrl navigation, Home/End, Space, T, J/G/B, Escape, and C in their applicable contexts
- **Then** each command follows the keyboard table; no plain Home/End skips the service, Enter does not hide words, and browser-reserved shortcuts are not claimed.

### Scenario: Mouse-only operation

- **Given** a projector with no keyboard activity
- **When** the operator uses the 40/20/40 areas, bait numbers, translation label, next-entry cue, and entry list
- **Then** stepping, word visibility, bait and entry jumps, and translation work without a keyboard; clicking in the bottom band does not trigger a screen zone.

### Scenario: Safe overlays

- **Given** the shortcut sheet or service-entry list is open
- **When** the operator clicks behind it, on its backdrop, or on a list row
- **Then** no underlying projector action fires; a backdrop click closes only the layer; a row click jumps only to that entry; the HUD remains visible while the layer is open.

### Scenario: Inactivity and intentional hiding

- **Given** no layer is open and C has not hidden the HUD
- **When** pointer activity stops for two seconds and all input stops for thirty seconds
- **Then** the pointer disappears first, followed by the corner and keyboard button; movement or a click restores the pointer and either mouse or keyboard activity restores the HUD.
- **Given** C intentionally hid the HUD
- **When** the mouse moves or a key other than C is pressed
- **Then** the HUD stays hidden; C restores it.

### Scenario: Library detour and fullscreen

- **Given** the operator is midway through a service entry
- **When** G opens an unplanned passage or song, the operator navigates it, then taps Escape
- **Then** the projector returns to the exact service screen left, subject to the browser's fullscreen keyboard-lock support; a held Escape can still leave JS fullscreen.

## Traceability

- Domain/app tests: `multimedia/web/tests.py::ServiceProjectorTests` covers screen boundaries, labels, translation payloads, lookup, and detours.
- E2E: `tests/e2e/test_projector.py::ProjectorE2ETests` covers fitting, keyboard and mouse jumps, and overlay interception.
- Implementation: `multimedia/web/reading/views.py`, `multimedia/urls.py`, the service projector templates, `static/web/projector.js`, and `static/styles/design/projector.css`.
