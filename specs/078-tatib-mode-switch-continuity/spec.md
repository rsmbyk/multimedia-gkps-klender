# Spec 078: Preserve the open Tata Ibadah during list-mode switches

- **ID:** 078
- **Status:** Accepted
- **Item:** ITEM-081
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Keep the currently open Tata Ibadah and its service-entry sidebar in context when the operator switches the first sidebar between dated orders and templates.

## Scope

### In scope

- The existing calendar/document mode toggle in the Tata Ibadah first sidebar.
- Preservation of the currently open stage and second-level service-entry list.
- Selection and reveal of the exact open Tata Ibadah row in the first sidebar.

### Out of scope

- Main-rail menu switching, changing which service is open, or editing template/date data.

## Domain rules

- A mode change updates the first sidebar's dated/template list while the same Tata Ibadah page remains on the stage.
- If the service-entry sidebar was open, it stays open with the same entries, filter, and scroll position. A closed second sidebar stays closed.
- After the list swap, select the row for the exact open service ID using the existing current-row semantics and scroll that row into view within the first sidebar. Do not scroll the page.
- Dated orders and templates are disjoint. If the open service is absent from the chosen list, append one contextual row after that list with its real name, date (or “Template”), and “Currently open” cue. It links to the exact open service and is highlighted; never duplicate a service already in the chosen list.
- Clear the first-sidebar filter on mode change only if it would hide the selected row; leave the service-entry filter and global search query untouched.
- When no service page is open, the toggle only changes the list; do not invent a selected service or open a second sidebar.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](../072-sidebar-idle-collapse/preview.html), “Dated / template orders” scenario. The current row appears after the templates and the service-entry sidebar stays visible.
- **Size / position:** Keep the existing first and second sidebar widths, mode-toggle size/placement, row height, corner radius, and service-entry list layout. The contextual row uses ordinary service-row geometry after the destination list; no extra pinned panel.
- **Colors / typography:** Apply existing `--sidebar-selected-bg` and `--ink` to the selected row; use the existing muted date metadata style for “Currently open” and date/template detail.
- **States:** Mode icon and accessible label update as they do today. The exact open row has `aria-current="true"`; other rows do not. After a mode switch, reveal the selected row with at least 8px breathing room inside the first sidebar. If already fully visible, do not move the list.
- **Responsive behavior:** Keep the service-entry panel's open state across narrow layouts even if only one sidebar can be shown at a time; show it again when that level is surfaced.
- **Motion:** Reuse existing sidebar scroll animation and honor reduced motion. No new highlight flash.

## Acceptance scenarios

### Scenario: Dated order to templates

- **Given** a dated Tata Ibadah page is open with its service-entry sidebar expanded
- **When** the operator switches the first sidebar to Templates
- **Then** the page and service entries stay open, one contextual row for that dated page is selected after the template list, and the first sidebar scrolls enough to show it.

### Scenario: Template to dated orders

- **Given** a template Tata Ibadah page is open with its service-entry sidebar expanded
- **When** the operator switches to dated orders
- **Then** the same template page and entries remain, one contextual row identifies the open template, and that selected row becomes visible in the first sidebar.

### Scenario: Return to the matching mode

- **Given** the open service was represented as a contextual row in the opposite mode
- **When** the operator switches back to its own mode
- **Then** the ordinary list row is selected and revealed, and no contextual duplicate remains.

### Scenario: Filter and no-page edges

- **Given** a first-sidebar filter would hide the selected service, or no service page is open
- **When** the mode changes
- **Then** the filter is cleared only when needed to reveal an open service; with no open service, the list changes without selecting a row or opening service entries.

## Traceability

- Domain/app tests: `multimedia/web/tests.py` covers both opposite-mode contextual rows, matching-mode uniqueness, and identity.
- E2E: `tests/e2e/test_reading.py` covers stage and entry-pane continuity, filtering and scroll, row reveal, both directions, no-service state, narrow layout, and reduced motion.
- Implementation: `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/_tatib_panel.html`, and `static/web/reading.js`.
