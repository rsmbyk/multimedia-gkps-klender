---
id: ITEM-030
status: done
title: 'Remove the Update the current state button'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/028-remove-update-button/spec.md
branch: fix/028-remove-update-button
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/278
archived_at:
archive_reason:
bump: patch
release_version: 1.0.2
---

# ITEM-030: Remove the Update the current state button

## Summary

The service entries already reach the display on every saved change: the `editor:saved` seam in
`static/web/display.js` asks the projector to re-read after each add, edit, delete, and reorder
(spec 026). With that, the separate **Update the current state** control is redundant chrome. Remove
it from the reading page and its shell wiring, leaving the automatic follow as the only re-read.

## Notes

- The control is `[data-project-update]` in `multimedia/web/templates/reading/tatib.html`
  (label "Update the current state", `hidden` until a service is projecting).
- `static/web/display.js` holds everything around it: the `update` node in `nodes()`, the
  `data-project-update` click branch that calls `reflow()`, and `n.update.hidden = !here` in
  `sync()`.
- Keep `reflow()` — `editor:saved` and `window.gkpsDisplay.changed` (used by `reorder.js`) both
  call it, so the automatic re-read stays intact.
- Spec 026 kept the button on purpose, as the manual re-read for edits made from another browser or
  screen. Removing it drops that manual path; the spec writer should confirm the automatic follow
  is sufficient and amend spec 026 ("The **Update the current state** button keeps working") and its
  "The manual re-read still works" scenario accordingly.
- Test to update: `multimedia/web/tests.py`
  `test_the_reading_page_offers_the_project_button_with_its_icon` asserts both the label and
  `data-project-update hidden`.

## Acceptance sketch

- No **Update the current state** control renders on a Tata Ibadah reading page, in any projection
  state.
- A saved add / edit / delete / reorder still makes the open display re-read by itself.

## Links

- Spec: [028 — Remove the "Update the current state" button](../../specs/028-remove-update-button/spec.md)
- Related items: ITEM-028 (live projection editing), ITEM-029 (remove the projection status note)
