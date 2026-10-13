# Plan 082: Drop the extra Tata Ibadah row for the open service

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-085
- **Bump:** patch

## Why

`_tatib_groups()` appends a synthetic group whenever the open service is missing from the list mode
being shown:

```python
if selected_service and not any(
        row['id'] == selected_id for group in groups for row in group['services']):
    detail = (format_date_short(selected_service.date) if selected_service.date else 'Template')
    groups.append({'label': '', 'key': '', 'services': [{
        'id': selected_id, 'name': selected_service.name,
        'date_display': detail, 'current': True, 'contextual': True}]})
```

In template mode that puts a dated "Ibadah Minggu · 4 Okt 2026 · Currently open" card under the last
template, below a divider (the owner's screenshot); in dated mode the same happens to a template. The
owner's call: the list should show one list — the mode's own — and simply highlight the open service
when it is in it.

This supersedes the contextual row of spec 078 (ITEM-081). Everything else spec 078 introduced stays:
the stage and the entry pane survive a mode switch, and an in-list selection is reselected and
revealed.

## Scope / edges

**In:**

- `multimedia/web/reading/views.py::_tatib_groups()` and its `selected_service` argument.
- `multimedia/web/templates/reading/_tatib_panel.html`: the `contextual` flag, the "· Currently open"
  copy, and the edit control it suppressed.
- Both list modes, and the tests that pinned the removed behaviour.

**Out:**

- The `aria-current` highlight itself, the mode toggle, filter reset, scroll and visibility rules from
  spec 078, and the search page.

## Approach

Delete the append block and the `contextual` flag; keep `current` as the only selection signal. The
panel keeps rendering one row per service in the mode's own groups, with `aria-current="true"` on the
open one. Every editor-enabled row keeps its edit control, since there is no longer a synthetic row to
exempt.

## TDD

- Domain/app tests: `multimedia/web/tests.py`, replacing
  `test_open_service_has_one_contextual_row_in_opposite_mode` with the new rule (one row at most, no
  "Currently open" copy, no synthetic row in either mode).
- E2E (Playwright): `tests/e2e/test_reading.py`, updating
  `test_tatib_mode_switch_keeps_open_service_and_reveals_its_row` and
  `test_tatib_mode_switch_keeps_template_and_no_page_state`.

## Risks

- Spec 078's reveal-on-mode-switch test currently asserts the synthetic row is visible and labelled;
  it has to be rewritten around the in-list case, not deleted, or the reveal behaviour would lose its
  coverage.
- The template hides the edit control with `and not service.contextual`; dropping the flag must not
  drop the control along with it.
