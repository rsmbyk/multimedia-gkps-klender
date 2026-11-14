# Research: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`
**Unknowns remaining**: 0

## D001 — Guard on the event's target, do not stop the event at the input

- **Decision**: the first statement of the dialog's `cancel` listener is
  `if (event.target !== editorDialog) return;` (`static/web/media-entry.js:20`).
- **Rationale**: the browser fires one event name from two sources, and `event.target` is the only
  property that separates them — the dialog's own Escape targets `#editorModal`, the picker's dismissal
  targets `input[data-media-file]`. Stating the rule on the target also covers a `cancel` from any
  descendant added later (a nested dialog), which a listener written per source would miss.
- **Alternatives considered**: `input.addEventListener('cancel', e => e.stopPropagation())` — works, but
  it hides the event from every other listener on the page (including a future document-level one) to fix
  one dialog, and it says nothing about descendants that do not exist yet; a flag set in `choose()` before
  `input.click()` and cleared on `change` — needs clearing on both outcomes, and is wrong when the OS
  closes the picker without the page seeing either; recording the picker's open state on the element —
  same failure, one more place to keep true.
- **Provenance**: research (code read of `media-entry.js:9-24`, `:200-201`; the event targets measured on
  the live route: `INPUT[file]` for the picker, `#editorModal` for Escape).

## D002 — Test the event path, not the native picker

- **Decision**: the E2E cases send the input's own `cancel` — `dispatch_event('cancel', {'bubbles': True})`
  — rather than trying to drive a system file chooser, which no browser automation can open or dismiss.
- **Rationale**: the browser's behaviour is published (MDN, `HTMLInputElement: cancel event`: "fires on an
  `<input>` element when the user cancels the file picker dialog via the Esc key or the cancel button …
  not cancelable but can bubble"), and the event the page reacts to is exactly a bubbling `cancel` at the
  input. The case therefore pins the page's half of the contract, which is the half this slice changes.
- **Alternatives considered**: a real headful browser with the OS dialog dismissed by a keystroke — not
  portable, not deterministic, and it would be skipped in CI; asserting only that the dialog stays open
  without recording the event's shape — a case that passes whether or not the browser is involved.
- **Provenance**: research (MDN; the measured close, 165 ms after the input's event, replayed on
  `http://localhost:8814/tatib/149/`).

## D003 — Keep a case that fails if the fix goes too far

- **Decision**: `test_escape_still_closes_the_new_media_dialog` asserts the dialog's own Escape still
  closes it, and it is green before the fix as well as after.
- **Rationale**: the cheapest way to stop the dismissal is to delete the listener, which would leave the
  New media dialog unclosable by Escape — a worse defect than the one reported. A guard that cannot pass
  after a wrong fix is what makes the correct one falsifiable; a passing-before case is still a failing
  case against the wrong candidate.
- **Alternatives considered**: no guard, relying on the review — the failure would ship silently, because
  no existing case presses Escape in the *media* form (`test_editor.py` covers text, song, songbook and
  Tata Ibadah forms, which never contain a file input).
- **Provenance**: research (read of `tests/e2e/*.py` for `Escape`; no media-form case exists).

## D004 — The live readout runs on this worktree's own server

- **Decision**: the live verification is a `manual` row on `http://localhost:8814/tatib/149/`, taken
  before the merge, with the real system picker.
- **Rationale**: unlike slice 150, the companion admits this origin —
  `GKPS_MEDIA_ALLOWED_ORIGINS` carries `http://localhost:8814`, and a real 4×4 PNG was inspected and
  chosen through the page there while specifying. A worktree server on a port outside that list is
  refused (measured: `127.0.0.1:8768` → 403), which is why the route is named with the port it must use.
- **Alternatives considered**: waiting for the merge and reading it on the compose page — nothing needs
  the merge here, and the check is worth more before delivery; widening the companion's allow-list — out
  of scope and a change to a running service's boundary.
- **Provenance**: research (the companion's allow-list in `docker inspect`; the 403 at `:8768` and the 200
  at `:8814`; the chosen file measured in the browser).

## Open

<!-- empty: Phase 0 finished, zero unknowns -->
