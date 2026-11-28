## What changed

Pressing Enter while a delete confirmation is open now activates its destructive control, wherever
focus sits. One capture-phase handler activates the single marked, visible control; every existing
delete handler, feedback toast and focus-restoration path stays in charge of the write.

## Why

Keyboard users had to Tab onto the Delete button first: the live before probe recorded zero delete
requests on the stage, sidebar and verse confirmations and zero Remove-file clicks in the Media
Library when Enter was pressed with focus away. After the change each surface records exactly one.

## Scope

Sidebar record, stage entry, stage old row, verse, and Media Library removal confirmations.
Non-destructive confirmations (copy, Use template, leave-with-changes, screen-mode switch), Escape,
Cancel and scrim dismissal are unchanged. Retired Fomantic/OBS delete modals are out of scope: their
routes redirect (spec 194).

## Verification

- `tests/e2e/test_enter_delete_confirm.py` — 4 targeted Playwright pins, green.
- `specs/256-enter-confirms-delete/preview/probe-*.jsonl` — before 0 activations, after exactly 1 on
  all four surfaces.
- Gate 1 and gate 2 accepted 2026-11-28; analysis 17/17 coverage, 0 CRITICAL.

Refs #655, ITEM-278, spec 256.

_The tracker issue stays open; no `Closes`._
