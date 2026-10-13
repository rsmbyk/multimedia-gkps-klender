# Spec 080: Keep the first-level sidebar state when a page opens from a second-level list

- **ID:** 080
- **Status:** Accepted
- **Item:** ITEM-083
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Stop a collapsed or mini first-level sidebar from springing open when the operator opens a page by
clicking an item in the second-level list, or when adding a service entry refreshes the page.

## Scope

### In scope

- The in-page navigation state of the public reading shell (`static/web/reading.js`).
- The `chapter`, `song`, `service`, and post-save `refresh` navigations in all three sections.
- Every width the shell serves, including the narrow layout where the first panel is hidden.

### Out of scope

- Main-menu (rail) switching, the search, results, and more-results paths, and the `sync`, `lists`,
  and `mode` navigations — their state behaviour is unchanged.
- Panel sizes, the mini/mix modes themselves, filters, the idle collapse, and all server-rendered
  markup or copy.

## Domain rules

- A `chapter`, `song`, or `service` navigation swaps only the reading stage. It preserves the live
  first-panel state exactly as the operator left it: `open` stays open, `mini` stays mini, and
  `closed` stays closed. (Alkitab's own collapse control offers open and mini only; `closed` is
  reachable there on a narrow viewport, where the layout closes the panel.)
- The same navigation preserves the live second-list state: an open entry/song list stays open, a
  closed one stays closed. The narrow layout's own rule for the list — it closes when a song replaces
  it — still runs afterwards, as it does today.
- The navigation still takes the arriving page's stage-side facts (reading on/off, home state,
  section) and its list contents, filters, title, and selection.
- The `refresh` that follows an entry save is a stage-only navigation too: it preserves both sidebar
  states, so adding an entry on a page whose panel is collapsed leaves the panel collapsed.
- A main-menu (rail) switch is unchanged: it opens the arriving section's first panel, replaces the
  lists, and closes the previous second list.
- Search, results, and more-results navigations keep their current behaviour, including resetting the
  shell to the arriving page's own state.
- The idle collapse keeps its existing eligibility and interval rules (spec 072); an in-page
  navigation restarts the interval as it does today.
- The arriving page's `nav`/`ch` attributes stay in the markup: they remain the no-JS and
  full-reload state, and they still seed the shell on a fresh load or deep link.

## UI details

- **Visual reference:** [State preview](./preview.html) — the scenarios "Tata Ibadah", "Kidung", and
  "Alkitab" each start collapsed, open one item from the second-level list, and show the first panel
  untouched. The "Current build" switch in the same preview demonstrates the reported jump.
- **Size / spacing / position:** no change. Panel widths, collapse controls, tiles, and row geometry
  stay exactly as spec 055 and spec 072 left them.
- **Colors / typography:** no change.
- **States:** the only observable difference is that a collapsed first panel stays collapsed (and a
  mini Alkitab panel stays mini) after an item in the second list is opened. Hover, focus, selected,
  and `aria-expanded` states are unchanged — `syncState()` keeps reporting the panel that is really
  on screen.
- **Responsive behavior:** identical rule at every width. At narrow widths, where opening a chapter
  closes the first panel by layout, the panel is not reopened and the second list keeps the state it
  had.
- **Motion:** no change; the existing panel transition still runs only when a panel actually changes
  state.

## Acceptance scenarios

### Scenario: A collapsed Tata Ibadah panel survives an added entry

- **Given** the Tata Ibadah first panel is collapsed and a service is open on the stage
- **When** the operator adds an entry to that service
- **Then** the stage shows the new entry and the first panel is still collapsed.

### Scenario: A collapsed songbook panel survives opening a song

- **Given** the songbook first panel is collapsed and the song list on the right is open
- **When** the operator opens one of the listed songs
- **Then** the song page opens on the stage, the songbook panel is still collapsed, and the song list
  is still open with that song selected.

### Scenario: A mini Bible panel stays mini

- **Given** the Bible book panel is in its mini state and a chapter list is open
- **When** the operator opens a chapter
- **Then** the chapter opens on the stage and the panel is still mini. (Alkitab's collapse control
  toggles open and mini only, so mini is the state this section can be left in.)

### Scenario: The main menu still opens the arriving section

- **Given** the Kidung panel is collapsed on the Tata Ibadah section
- **When** the operator selects Kidung in the main rail
- **Then** the Kidung panel opens, the Tata Ibadah entry list closes, and the stage keeps the page it
  showed.

### Scenario: Narrow layout keeps a collapsed panel closed

- **Given** a 390px-wide viewport, where the first panel covers the list
- **When** the operator collapses it to reach the song list and opens a song
- **Then** the panel is still collapsed, the song is shown on the stage, and the narrow layout's own
  rule for the list (it closes when a song replaces it) still applies.

## Traceability

- Domain/app tests: N/A — no server rule changes.
- E2E: `tests/e2e/test_reading.py::SidebarStateOnItemOpenTests` — the Tata Ibadah add-entry refresh,
  the songbook→song and Bible→chapter cases, the mini Bible panel, the surviving main-menu switch, and
  the narrow layout.
- Implementation: `static/web/reading.js`.
