# Spec 077: Clear sidebar filters when switching main menus

- **ID:** 077
- **Status:** Accepted
- **Item:** ITEM-080
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make each newly selected main menu open with unfiltered sidebars so stale text from another section never hides its rows.

## Scope

### In scope

- The first-sidebar `bookFilter` and second-sidebar `songFilter` in the new reading shell.
- Section changes through the main icon rail, including Search, Alkitab, Kidung, and Tata Ibadah.

### Out of scope

- The home search query, filters inside editors or pickers, within-section navigation, and Tata Ibadah dated/template mode changes.

## Domain rules

- A successful main-rail switch to a different menu sets both sidebar filter values to empty and reapplies their empty-filter state before the destination lists are shown.
- Both clear controls hide because their fields are now empty. Returning to the previous menu starts with full lists.
- Selecting the already active menu to open or close its sidebar does not clear its filters. Navigating among books, songs, chapters, or Tata Ibadah pages within the same section also does not clear them.
- A dated/template switch is handled by Spec 078; it is not a main-menu switch. The global home search query follows its existing search-result restoration behavior.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](../072-sidebar-idle-collapse/preview.html), “Idle & menu switching” scenario.
- **Size / spacing / colors:** No change to fields, labels, lists, or menu icons.
- **States:** On a different main-menu selection, both fields become visibly empty, any cross buttons hide, and all destination rows are available. Focus follows the existing destination menu behavior.
- **Responsive behavior:** Apply the same reset on desktop and narrow sidebar layouts.
- **Motion:** None added.

## Acceptance scenarios

### Scenario: Switch to another main menu

- **Given** text in either or both sidebar filters
- **When** the operator selects a different main-rail menu
- **Then** both filter values are empty, their clear buttons are hidden, and the destination sidebars show unfiltered rows.

### Scenario: Return to a previous menu

- **Given** a sidebar filter was filled before leaving that menu
- **When** the operator returns through the rail
- **Then** no old filter text or hidden-row state returns.

### Scenario: Stay within a menu

- **Given** a filled sidebar filter
- **When** the operator closes/reopens the same menu or navigates within it
- **Then** the filter remains until deliberately cleared; a Tata Ibadah dated/template toggle follows Spec 078 instead.

### Scenario: Search query

- **Given** an existing global search query
- **When** the operator changes a reading menu
- **Then** the query's existing search-result restoration behavior remains intact.

## Traceability

- Domain/app tests: N/A.
- E2E: `tests/e2e/test_reading.py` covers cross-menu resets, same-menu retention, returning to a menu, and Search query preservation.
- Implementation: `static/web/reading.js` resets both filters after a successful main-menu page swap.
