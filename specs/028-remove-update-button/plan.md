# Plan 028: Remove the "Update the current state" button

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-030
- **Bump:** patch

## Why

The display already follows every saved change on its own: `editor:saved` fires after an entry
save/delete (`entries.js`), a sidebar editor save (`editors.js`), and a reorder write
(`reorder.js`), and `static/web/display.js` turns it into `reflow()` — a `{type:'update'}` message
that makes the projector re-read (spec 026). The separate **Update the current state** button is the
same act on a manual trigger, and is now redundant chrome under the Project / Stop projecting pair.

## Scope / edges

**In:**

- Remove the `[data-project-update]` button from `multimedia/web/templates/reading/tatib.html`.
- Remove its wiring from `static/web/display.js`: the `update` entry in `nodes()`, the
  `[data-project-update]` click branch, and the `n.update.hidden = !here` line in `sync()`.
- Keep `reflow()`, the `editor:saved` listener, and `window.gkpsDisplay.changed` (used by
  `reorder.js`) untouched — the automatic follow is what remains.
- Update `multimedia/web/tests.py` (the two assertions on the label and `data-project-update
  hidden`).
- Amend the accepted spec 026 in the same PR: its "The **Update the current state** button keeps
  working as the manual re-read" in-scope clause and its "The manual re-read still works" scenario
  no longer hold, since the button is gone.

**Out:**

- `static/web/projector.js` and the display state, channel, heartbeat, or automatic follow.
- The OBS dock / source pages, which never carried this button.

## Approach

- `tatib.html` — delete the button line; leave the `data-project-group` and the project button.
- `display.js` — drop `update` from the object returned by `nodes()`, delete the click branch that
  calls `reflow()`, and delete the `hidden` toggle in `sync()`. Fix the file header comment, which
  names "its Stop projecting and Update the current state states".
- `tests.py` — in `test_the_reading_page_offers_the_project_button_with_its_icon`, remove the
  `Update the current state` and `data-project-update hidden` assertions; the rest stand.
- Spec 026 — reword the in-scope clause and the scenario so they describe the automatic follow as
  the only re-read.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the Tata Ibadah reading page no longer renders
  `Update the current state` or `data-project-update`, and still renders the project button.
- E2E: `tests/e2e/test_projector.py` — any case that presses **Update the current state** to force a
  re-read is dropped or rewritten to assert the automatic follow instead.

## Risks

- **Losing the manual re-read.** Spec 026 kept the button for edits made from another browser or
  screen; with it gone, only same-browser saves reach the display. The owner accepted this: service
  items already reach the display on change, and the display state stays browser-local.
