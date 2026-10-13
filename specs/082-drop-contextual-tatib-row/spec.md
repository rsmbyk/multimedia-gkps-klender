# Spec 082: Drop the extra Tata Ibadah row for the open service

- **ID:** 082
- **Status:** Accepted
- **Item:** ITEM-085
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The Tata Ibadah sidebar lists the mode it shows and nothing else: the open service is highlighted when
it belongs to that list, and no extra row is invented for it when it does not.

## Scope

### In scope

- The Tata Ibadah first-panel rows for both list modes (dated orders and templates).
- The open service's highlight and its edit control.

### Out of scope

- The mode toggle itself, the filter reset, the pane's scroll position, and the selection/reveal rules
  from spec 078 that apply to a service the list does contain.
- The Alkitab and Kidung panels, the global search page, and the reading stage.

## Domain rules

- The panel renders exactly the services of the current mode: dated services in dated mode, templates
  in template mode, in the existing order and grouping.
- The open service is marked as selected on its own row when it appears in the current mode's groups.
- When the open service does not appear in the current mode's groups, no row is added for it: the
  panel shows the mode's own list and no selection.
- There is no synthetic group, no appended "Currently open" row, and therefore no "· Currently open"
  copy anywhere in the panel.
- `current` is the only selection signal the panel needs. The `contextual` flag and the special cases
  built on it are removed.
- Every editor-enabled service row carries its hover edit control, including the row of the service
  that is currently open.
- Switching modes still preserves the open service, the stage, and the entry pane; when the arriving
  list contains the open service, that row is selected and brought into view exactly as spec 078
  describes.

## UI details

- **Visual reference:** [Tata Ibadah list preview](./preview.html) — switch the list mode with
  "Current build" off and the open service simply stops being highlighted when it leaves the list.
- **Size / spacing / position:** unchanged. No divider, card, or group is added or removed: the list
  ends after the last service of the mode.
- **Colors / typography:** unchanged; the selected row keeps `--sidebar-selected-bg`, and the
  "· Currently open" suffix and the group caption it used are gone.
- **States:** selected (in the mode's list), unselected, hover, and focus are unchanged. The absent
  service has no state at all — nothing to hover, focus, or reveal.
- **Responsive behavior:** unchanged at every width; the narrow layout shows the same two lists.
- **Motion:** unchanged. The panel's existing reveal-on-switch scroll and flash keep their behaviour
  and simply have no target when the open service is not in the list.

## Acceptance scenarios

### Scenario: A dated order is open while the panel shows templates

- **Given** a dated service is open on the stage and the panel is switched to templates
- **When** the panel renders
- **Then** it lists only templates, with no row for the dated service, no divider group for it, and no
  "Currently open" text.

### Scenario: A template is open while the panel shows dated orders

- **Given** a template is open on the stage and the panel is switched to dated orders
- **When** the panel renders
- **Then** it lists only dated services and shows no row for the template.

### Scenario: The open service is in the shown list

- **Given** a dated service is open and the panel shows dated orders
- **When** the panel renders
- **Then** that service's own row is highlighted, counting once in the markup, and it carries its edit
  control like any other row.

### Scenario: Starting from the list instead of a page

- **Given** no service is open and the panel shows either mode
- **When** the panel renders
- **Then** no row is highlighted, exactly as today.

### Scenario: Mode switching keeps the rest of the state

- **Given** the open service is in the arriving mode's list
- **When** the operator switches modes
- **Then** the stage and entry pane are unchanged, and the open service's own row is selected and
  revealed.

## Traceability

- Domain/app tests: `multimedia/web/tests.py::ServiceEntryViewTests`, replacing
  `test_open_service_has_one_contextual_row_in_opposite_mode`.
- E2E: `tests/e2e/test_reading.py` — the two `test_tatib_mode_switch_*` cases.
- Implementation: `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/_tatib_panel.html`.
