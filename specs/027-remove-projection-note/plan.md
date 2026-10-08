# Plan 027: Remove the projection status note

- **Status:** Accepted (owner, 2026-10-08)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-029
- **Bump:** patch

## Why

When the operator presses **Update the current state**, or the projector window is closed, a
danger-coloured line appears directly beneath the Project / Stop projecting controls. It is styled
red, so it reads like an error, though it is informational ("The display is re-reading this Tata
Ibadah.", "The projector window is gone, so the display stopped."). The owner wants that line gone.

## Scope / edges

**In:** Removing the status line under the projection controls and the two messages it shows.

**Out:** Changing the Project / Stop projecting toggle, the Update action itself (the display still
re-reads), the automatic stop-when-the-window-closes behaviour, or any other status/error copy — the
reorder failure line, the deleted-target warning, editor field validation, and the empty states all
stay.

## Approach

Delete the `data-project-note` element; remove the `say()` helper, its `noteTimer`, and its two call
sites in `static/web/display.js`; drop the now-unused `.read__project-note` CSS. The underlying
actions are untouched: Update still asks the display to re-read, and closing the window still stops
the display and flips the button label back to "Project".

## TDD

- Domain/app tests: `multimedia/web/tests.py` (`ServiceProjectorTests`) — the button-contract test
  must no longer require `data-project-note`.
- E2E: `tests/e2e/test_projector.py` (`ProjectorE2ETests`) — stop-on-close and Update-re-read must
  still pass with no note assertions.

## Risks

- The removed line was the only explicit confirmation that the display stopped because the window
  closed. The button label reverting to "Project" remains the signal; the owner accepted this by
  requesting the removal.
- This is a copy/behaviour change, so it takes a numbered spec even though it is small (specs/README
  rule 8).
