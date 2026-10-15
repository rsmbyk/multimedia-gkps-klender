# Spec 091: Quiet controls for the mirrored service projector

- **ID:** 091
- **Status:** Accepted
- **Item:** ITEM-094
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor
- **Preview:** [interactive 1366×768 projector](./preview.html), [states and measurements](./preview-gallery.html)
- **Go To amendment:** Accepted; [single-suggestion preview](./preview-goto-autocomplete.html)
- **Search clear amendment:** Accepted; [two-field preview](./preview-search-clear.html)
- **Untitled Text cue amendment:** Draft, revised preview pending approval; [running-text preview](./preview-cue-running-text.html)

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
| Display | K | Open or close the keyboard shortcuts sheet |
| Display | F | Enter or leave browser fullscreen where supported |
| Find | J / G | Open the searchable service list / find a passage or song |
| Service list or find open | Up/Down, Enter, Backspace, Escape | Previous/next match; open match; delete or close when empty; close the panel |
| Detour | Escape | Return to the service screen left, after any find or popup is closed |
| Shortcut sheet or entry list | Escape | Close the open layer without navigating |

- Enter never toggles words. Ctrl+Page Up/Down remain browser tab commands. Alt+Left/Right remain browser history commands.
- J opens the same service list as the corner icon. Its search filters entry numbers, labels, and selected bait numbers, with a keyboard-selected row separate from the current projected entry. G accepts a Bible book abbreviation or full translated name plus a chapter number prefix (`Mat 2` and `Matius 2` find chapter 2 and chapters starting with 2); a complete verse reference still opens that verse. For hymns, a songbook abbreviation or full name plus a song-number prefix (`NKB 2`, `Nyanyikanlah Kidung Baru 22`, `NKB 223A`) finds numbered songs including `NKB 223A`. Reference-prefix results are scrollable and are not cut off by the title-search limit. Otherwise song results use the strongest available tier: exact title first, then title prefix, then title substring. An exact song number also matches without a book prefix. A Bible book or songbook name alone, a partial song number without a book, and verse- or lyric-body-only matches do not appear in Go To; the broader search page retains its own matching behavior. Song baits remain reachable by Shift navigation or clicking their cue numbers.
- On JS-entered fullscreen, request the browser's supported keyboard lock for a short Escape; allow a held Escape to leave fullscreen. F11 fullscreen follows browser behavior. Do not claim the page can intercept a browser-reserved key when the browser does not provide it.
- When browser fullscreen is available, any click in the projection area while windowed enters fullscreen only: it never steps or toggles the words. A fullscreen cursor indicates this on hover. Subsequent clicks navigate normally. After leaving fullscreen, the next projection-area click again enters fullscreen only. HUD buttons retain their explicit actions. If fullscreen is unavailable, windowed mouse navigation remains usable.

## UI details

The approved preview is the geometry and appearance reference; its five sample entries do not limit a real service list.

- **Projector stage:** Reference output 1366×768px; background `#14130F`, body `#F5F3EE`, header `#FFD166`. Padding: 32px top/left/right and 64px bottom. The header stays at the top of the remaining 1302×672px text stage. Body text uses the remaining height, starts at 200px, and shrinks to fit. Header font size is body size divided by the golden ratio (about 0.618×). The minimum gap from header to body is one em of header size. Wrapped line height is 1.37; separate literal entry lines have a 0.45em gap. Long lines wrap and the fitting calculation accounts for both kinds of line.
- **HUD geometry:** A single 24px-high row centered at y=736px in the reference output's 64px bottom band. The cue starts 32px from the left and ends 84px from the right, uses 16px text, weight 650, and a dim `#6E6A62` base. Current highlights use `#E8E4DC`. Its list icon is 24×24px, followed by a center dot; cue parts and arrows share the same vertical center. The keyboard icon is 34×24px, 32px from the right, with a 20px bottom inset. Both controls align vertically. Hover is a slight lightening; pressed controls dim or use the darker active fill. Keyboard focus has a visible light outline.
- **Shortcut sheet:** Opens centered over the unchanged verse with a dim backdrop; `#14130F` surface, `#3a372f` 1px border, 10px radius, 20px vertical/24px horizontal padding, and 32px column gap. Group headings are 14px. Rows use 14px descriptions, 3px vertical padding, and restrained separators; groups have 24px vertical separation. Keys are 28px high and 28px wide for letters, symbols, and arrows; named keys, Ctrl/Command-style, Shift, Enter, and Backspace are 56px wide; Space is 84px. Letter labels are 14px, named labels 12px, and symbol marks 16px, all regular weight. The sheet groups service, song, passage, library passage, library detour, display, find, and fullscreen controls as in the preview. It fades and moves 8px with a slight scale change over 180ms on open and close; the backdrop fades with it. Clicking the dim backdrop or Escape closes it without projector navigation. While open or closing, projector and HUD navigation clicks are blocked. Reduced-motion users get no animation.
- **Service entry list:** The icon-only button or J opens a 360px-wide, at-most-560px-high scrollable panel, 32px from the left and 58px from the bottom. It uses the projector `#14130F` surface, `#3a372f` border, 10px radius, and quiet shadow. A small search field stays at the top and filters entry numbers, labels, and selected bait numbers. Rows have a numeric column, a short title, and a 10px second line only when useful (such as selected baits). The current projected row has only a muted inset marker; the keyboard-selected row uses a stronger `#36322b` fill, while hover uses a lighter `#26231f` fill. When both states coincide, the row shows the marker and selected fill together. Opening the list selects and scrolls to the current entry. Up/Down cycles filtered rows, centers intermediate choices in the space below the search header, and reaches the full top/bottom scroll limits on the first/last match; Enter jumps, and Backspace on an empty search or Escape closes it. A slight dark overlay covers the rest of the output and catches clicks with one close cursor; clicking it closes the list without navigation. The list fades and moves 6px with a slight scale change over 180ms on open and close, while its overlay fades; reduced-motion users get no animation. A row click jumps to that entry and closes the list. Underlying HUD and screen controls cannot be clicked through the overlay, including during closing.
- **Mouse areas:** Above the 64px bottom band only, invisible left/middle/right regions occupy 40%/20%/40% of width and perform previous step / show-hide words / next step. A muted left/right arrow or show/hide cursor indicates the action. The bottom band remains reserved for the HUD. Cue bait numbers jump to that bait; translation label acts like T; the arrow plus next-entry text is one next-entry button. Each has a modest hover and pressed treatment.
- **Go To popup:** Passage/song search opens over a transparent, full-output click overlay so projected words remain readable. Clicking outside the popup closes it without triggering a HUD or screen navigation action. Hymn results display the short songbook abbreviation, number and optional uppercase sub-number before the title (for example `KJ 152 Ada Kuasa` or `NKB 223A Haleluya`); non-hymn results keep their title label.
- **Inactivity:** Pointer disappears after two seconds without movement or click and reappears on movement or click. Corner cue and keyboard button fade after 30 seconds without mouse or keyboard activity, with a 180ms transition, and reappear on the first activity. They do not auto-hide while the shortcut sheet, service-entry list, or Go To popup is open. The manual C-hidden state never reappears merely from activity.
- **Responsive behavior:** Preserve these proportions and centered content when the viewport differs from 1366×768. The lyric font shrinks to fit available space; controls and their overlays stay inside the projector output and the shortcut sheet/list remain scrollable rather than clipping content. No title, key row, or list action becomes unreachable. Fullscreen uses the same layout rules.

## Accepted amendment: one-suggestion Go To

This amendment changes only the G passage/song popup. The preceding Spec 091 behavior remains Accepted. The owner accepted this amendment after approving the [interaction preview](./preview-goto-autocomplete.html), which uses illustrative results.

### Behavior

- Opening G focuses an empty query. As the operator types, keep the query text in the input and show only the first result from the existing Go To lookup, with a `current / total` counter. Do not render a scrolling list of result rows.
- Up and Down move the current suggestion backward and forward through **every** returned match, including large book-and-number prefix sets. The suggestion label and counter update together. Down after the last wraps to the first; Up before the first wraps to the last. Cycling never inserts the suggestion into, or otherwise changes, the typed query.
- Editing the query starts a new lookup and resets the selection to the first match. An older response must not replace results for a newer query or a closed popup. While loading, do not leave a stale suggestion selectable.
- Enter or clicking the visible suggestion opens that passage or song through the existing detour path, then closes G. With no result, Enter does nothing. Escape, Backspace on an empty input, or clicking the transparent outside overlay closes G without opening a detour or navigating the service. Keep the projector's existing HUD visibility and click interception rules while G is open.
- Preserve the endpoint's current reference matching, title ranking, hymn labels, and result order. The counter uses the full number returned by the endpoint; reference-prefix results are not truncated to the twelve-result title-search limit. J's searchable service list remains a list.

### UI details

- Keep the G popup at the existing 32px left and 58px bottom offsets, at most 400px wide and inside the viewport. Keep its 16px padding, `#14130F` surface, 1px `#3a372f` border, 10px radius, and quiet shadow. The transparent full-output overlay leaves projected words undimmed.
- Keep the normal projector sans-serif font at 11px and regular weight for the label, input, suggestion, and counter. The label is muted above the input. Below the input, show one 8px-padded suggestion row with a 6px gap; its text truncates within the row and `1 / 44`-style counter aligns on the right. No terminal prompt, glyph prefix, or monospaced type is added.
- Use the existing dark input (`#2a2722`) and light border focus state. The current suggestion row uses the same restrained dark fill; hover lightens to `#36322b`. Empty-query and no-match states show short muted guidance with `0 / 0` and no selectable row. A 10px muted footer may show Up/Down, Enter, and Escape hints.
- Keep this compact layout at smaller viewports: the popup width becomes at most viewport width minus 64px, and the input, suggestion, counter, and footer remain visible. Selection changes have no additional motion; reduced-motion behavior is unchanged.

### Amendment acceptance scenarios

- **Given** G is open and `NKB 2` returns 44 matches, **when** the operator presses Down, **then** only one suggestion is visible, it changes in server order, and the counter advances from `1 / 44` to `2 / 44` without changing `NKB 2` in the input.
- **Given** the first or last match is selected, **when** the operator presses Up or Down across that boundary, **then** selection wraps to the opposite end and every intermediate result remains reachable.
- **Given** a suggestion is selected, **when** the operator presses Enter or clicks it, **then** only that detour opens and G closes. Escape, empty-input Backspace, and outside clicks close G without changing the projected service position.
- **Given** a new query or a closed popup, **when** an older lookup response arrives, **then** it neither replaces the current suggestion nor opens a detour. Zero results show `0 / 0` and Enter does nothing.

## Accepted amendment: projector search clear controls

The owner approved the [interactive preview](./preview-search-clear.html) for the J service-list search and G Go To search and explicitly accepted this amendment. Reuse the public reading sidebar's 20×20 SVG path (`M5.5 5.5l9 9M14.5 5.5l-9 9`) with a 1.8px round-capped stroke, rendered at 14×14 inside a 26×26 circular button on the right side of each input. The button is vertically centered in a positioned field wrapper, 5px from its right edge. Give the input enough right padding that text never overlaps the button. Suppress the browser-native search cancel icon so only one clear control appears.

Use the projector's muted `#8e8a80` icon color and transparent resting background. Hover uses `#36322b` behind the icon and `#e8e4dc` for the stroke. Keyboard focus shows a 2px `#e8e4dc` outline with 1px offset. Keep the existing 400px G popup and 360px J list geometry, input colors, labels, and result layouts; at smaller viewports the control remains inside each field. The clear button is hidden when the field is empty, including on initial open, and appears immediately when text is entered.

Clicking or keyboard-activating clear empties only its field, fires that input's existing `input` behavior, and returns focus to that field. J re-renders the unfiltered service entries; G returns to the empty-query guidance and `0 / 0` count, invalidating any pending lookup. Clearing does not close either popup, navigate the projector, or trigger an underlying mouse zone. The existing search matching, arrow selection, Enter action, Escape, and overlay dismissal remain unchanged.

- **Given** either field is empty, **when** its popup opens, **then** its clear button is absent and the native cancel glyph is suppressed.
- **Given** text is entered in J or G, **when** the clear button is clicked or activated with Enter/Space, **then** only that query is emptied, focus stays in its input, and the corresponding results reset without closing the popup.
- **Given** a pending G lookup, **when** the field is cleared and the old response arrives, **then** empty guidance and `0 / 0` remain visible.

## Draft amendment: clip untitled Text cue labels

The [revised running-text preview](./preview-cue-running-text.html) shows two adjacent untitled Text entries and awaits owner approval. This amendment remains Draft until explicitly accepted. When an entry has `type: text` and `untitled: true`, the corner cue displays a prefix of its first-line `label`, followed by `…` only when more characters exist. Start with a **shared** limit of 50 Unicode characters for current and next labels. Lower that limit for both together, to no fewer than one character, **only if** their combined inline cue would overflow the available space before the keyboard clearance. Choose the largest shared limit that fits; remeasure after viewport resize and when the cue content changes. The ellipsis is in addition to the chosen limit. Keep the full `entry.label` in projector data, the J service list, and search matching. Titles, song and passage references, section breaks, and library detours keep their existing text.

Apply the same rule when such an entry appears as the **next-entry hint**. The shortened string is presentation-only: it must not affect current/next navigation or screen counts. Let each label's resting width follow its truncated text rather than pre-allocating a fixed percentage of the viewport. Keep the count and arrow non-shrinking, the 16px HUD type and 24px alignment box, and the existing muted colors. Keep the cue 32px from the left and set its right edge to `calc(66px + 10vw)` from the viewport edge: the keyboard button is 34px wide and 32px from the edge. Keep the next-entry group directly inline after the count with its existing small margin. The cue's right boundary reserves a **minimum** 10vw clearance before the keyboard button only when the inline content fills the available width; shorter content may leave a larger natural gap.

At rest, both labels remain clipped with an ellipsis. Hovering one label reveals its **full** first line through a slow leftward run that repeats for as long as the pointer stays over it. Leaving immediately stops the animation and restores the clipped label; the other label never starts moving from that hover. No browser title tooltip is attached to either label. The count, arrow, next-entry target, and keyboard button stay fixed throughout. Under `prefers-reduced-motion: reduce`, labels remain still and clipped. Other cue content keeps its existing hover behavior.

- **Given** an untitled Text first line is shorter than the current responsive limit, **when** it is current or next, **then** the cue shows it without an added ellipsis.
- **Given** an untitled Text first line exceeds the current responsive limit, **when** it is current or next, **then** both positions use the same limit and J and its search still use the full first line.
- **Given** the viewport narrows, **when** the 50-character versions no longer fit, **then** their shared character limit decreases just enough for the inline cue to fit while the screen count and arrow remain visible and the gap from the next group to the keyboard button stays at least 10vw. If both fit, the limit remains 50.
- **Given** two adjacent untitled Text entries have long first lines, **when** one is current and one is next, **then** both labels clip independently and neither pushes the count or arrow out of the HUD.
- **Given** a clipped label is hovered, **when** the pointer remains, **then** its full text runs repeatedly without moving the count, arrow, or other label. Leaving restores the clipped state without a browser tooltip; reduced-motion preference keeps the label still.

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
- **When** the operator uses plain, Shift, and Ctrl navigation, Home/End, Space, T, J/G, Escape, C, K, and F in their applicable contexts
- **Then** each command follows the keyboard table; no plain Home/End skips the service, Enter does not hide words, and browser-reserved shortcuts are not claimed.

### Scenario: Mouse-only operation

- **Given** a projector with no keyboard activity
- **When** the operator uses the 40/20/40 areas, bait numbers, translation label, next-entry cue, and entry list
- **Then** stepping, word visibility, bait and entry jumps, and translation work without a keyboard; clicking in the bottom band does not trigger a screen zone.

### Scenario: Safe overlays

- **Given** the shortcut sheet, service-entry list, or Go To popup is open
- **When** the operator clicks behind it, on its backdrop, or on a list row
- **Then** no underlying projector action fires; a backdrop click closes only the layer; a row click jumps only to that entry; the HUD remains visible while the layer is open. The Go To overlay leaves the projected words undimmed.

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
