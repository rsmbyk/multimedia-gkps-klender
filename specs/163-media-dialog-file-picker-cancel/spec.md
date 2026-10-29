# Feature Specification: dismissing the file picker leaves the New media dialog open

**Slice**: `specs/163-media-dialog-file-picker-cancel`
**Branch**: `fix/163-media-dialog-file-picker-cancel`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1 and gate 2, 2026-10-29)
**Input**: "when you close the system file picker, the media files modal also gets closed" — with a
screenshot of the New media dialog under an open system picker at `/tatib/149/`.

## What the page does today

The New media form lives inside the editor dialog, and its file input is a descendant of that dialog
(`multimedia/web/templates/reading/_entry_form.html:36`). Choosing a file runs
`[data-media-choose]` → `input.value = ''; input.click()` (`static/web/media-entry.js:200`).

The dialog carries a `cancel` listener (`static/web/media-entry.js:19`) that reads every `cancel`
reaching it as its own Escape:

```js
editorDialog.addEventListener('cancel', function (event) {
  if (editorDialog.querySelector('form[data-entry-form="media"]')) {
    event.preventDefault(); editorDialog.close();
  }
});
```

But `<input type="file">` fires `cancel` itself: *"The `cancel` event fires on an `<input>` element
when the user cancels the file picker dialog via the Esc key or the cancel button and when the user
re-selects the same files that were previously selected… This event is not cancelable but can bubble."*
(MDN, `HTMLInputElement: cancel event`). It bubbles from the input to the dialog, so the one listener
cannot tell the two sources apart and the form is dismissed with the picker.

Measured on the slice's own server (`http://localhost:8814/tatib/149/`, 1440×900, Chromium, headless,
the input's own event replayed with `bubbles: true` — the shape the browser fires):

| dismissal, as the browser reports it | what the page does |
| --- | --- |
| picker closed without a file — `cancel` at `INPUT[file]` | dialog closes **165 ms** later; the form is gone from the page |
| a file chosen (`swatch.png` shown, Save enabled), then the picker closed again — also `cancel` at `INPUT[file]` | dialog closes; the chosen file, its name and the enabled Save go with it |
| Escape on the dialog itself — `cancel` at `#editorModal` | dialog closes — the behaviour to keep |

The cost is the whole form: the title typed, the tab in use, a file already inspected and shown with its
name, size, note and enabled Save.

## User Scenarios & Testing

### US1 — Dismissing the picker leaves the dialog as it was (P1)

**Why this priority**: the picker is the first thing an operator opens in this form, and closing it by
accident — the Esc they meant for the picker, the X on its window — currently destroys the form. It is
the whole of the reported defect.

**Independent Test**: from a Tata Ibadah service, open New media, click *Choose file to upload*, close
the picker without choosing: the dialog is still open, on the same tab, with the same Save state.

**Acceptance scenarios**

1. **Given** the New media dialog is open on Upload with no file chosen, **When** the picker is
   dismissed without a file, **Then** the dialog stays open, the Upload panel still shows its prompt,
   and Save is still disabled.
2. **Given** a file has been chosen and is shown with its name, size and note, **When** the picker is
   reopened and dismissed, **Then** the dialog stays open and still shows that file, unchanged.
3. **Given** an entry title has been typed, **When** the picker is dismissed, **Then** the title is
   still in its field.
4. **Given** the dialog is open on the Media Library tab with a row selected, **When** a `cancel` from
   the file input arrives, **Then** the dialog is still open on the Media Library tab with that row
   still selected.

### US2 — The dialog's own dismissal is unchanged (P2)

**Why this priority**: the fix must not turn into "the modal no longer closes". Escape, Cancel and the
closing motion are shipped behaviour that this listener exists to serve.

**Independent Test**: Escape on an open New media dialog closes it exactly as it does today, and still
closes a text, song, scripture or section-break form.

**Acceptance scenarios**

1. **Given** the New media dialog is open, **When** Escape is pressed with the dialog focused, **Then**
   it closes with its existing 150 ms closing motion.
2. **Given** the New media dialog is open, **When** Cancel is pressed, **Then** it closes as today.
3. **Given** any other editor form is open, **When** Escape is pressed, **Then** it closes as today:
   the guard is written on the media form's source of `cancel`, not on dismissal in general.

### Edge Cases

- **When** the person re-picks the file they already chose, **Then** the dialog stays open and keeps
  showing that file: the browser reports the re-pick as `cancel`, so no second inspect is fired and no
  selection is lost.
- **When** the picker is dismissed while the chosen file is still being inspected, **Then** the dialog
  stays open; the inspect either lands and shows the file as it does today, or fails into the existing
  error dialog.
- **When** the error dialog (*File not supported*) is open and the picker is dismissed, **Then** the
  editor dialog stays open — the error dialog is its own and closes only itself.
- **When** the person's system prefers reduced motion, **Then** the behaviour is the same; only the
  closing motion differs, as today.
- **When** the dialog is closed from the picker's `cancel` and then reopened, **Then** nothing about the
  next open changes: the form is fetched fresh, as it is for every open.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A `cancel` event SHALL close an editor dialog only when the event's target is that dialog; a `cancel` whose target is a descendant — the media form's file input — SHALL NOT close it. | `new: reading` → R32 |
| FR-002 | Dismissing the file picker SHALL leave the New media dialog open with its tab, its chosen file, its title field, its Save state and its note exactly as they were. | `new: reading` → R32 |
| FR-003 | Escape on the dialog itself SHALL still close the New media dialog with its existing 150 ms closing motion, and SHALL still close every other editor form as today. | `reading/R10` |
| FR-004 | Nothing else changes: no markup, CSS, copy, endpoint, payload or geometry; the dialog's frame, its tabs, the picker's states and the save flow stay as they are. | `reading/R10` |

### Key Entities

- **`cancel` event** — the browser's dismissal event. Two sources reach the editor dialog: the dialog's
  own Escape, and the file input's picker being closed. `event.target` is the only thing that separates
  them; the event is not cancelable and does bubble.
- **File input** — `input[type=file][data-media-file]` (`_entry_form.html:36`), hidden, opened by
  `[data-media-choose]`. Owns the chosen file until the form is submitted.
- **New media dialog** — `#editorModal` with `form[data-entry-form="media"]`, one dialog reused by every
  editor kind; its `close()` is wrapped to run a 150 ms closing class when the media form is present.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | With the picker dismissed, the dialog is still open and the form is still in the page 500 ms later — past the 165 ms the close takes when it happens. | browser probe on the live route: `#editorModal.open` and the form's presence |
| SC-002 | A same-file re-pick leaves the dialog open and the chosen file shown. | the same probe, after a `cancel` from a re-pick |
| SC-003 | Escape on the dialog still closes it, and it is gone within 500 ms. | the same probe, Escape pressed on the dialog |
| SC-004 | The existing browser suite stays green, with its assertions unchanged. | `manage.py test tests.e2e.test_media_library` |

## UI/UX

`n/a — nothing visible changes; the slice removes a dismissal, no pixel moves.` The frame is measured to
show it does not move: at a 1440×900 viewport the New media dialog is **840×760 at (300, 70)**, its Save
button **66.6×38 at (957.8, 772)**, and both read the same after the change. The states the change does
touch are behavioural and are reachable by hand on the live route
`http://localhost:8814/tatib/149/` → *New media* → *Choose file to upload* → close the picker.

## Assumptions

- **The discriminator is the event's target.** Both sources fire the same event name, so the listener
  reads `event.target`; a flag set when the picker opens would need clearing on `change` *and* on
  `cancel`, and would be wrong when the OS closes the picker without the page hearing about it.
- **A same-file re-pick is a dismissal, because the browser says so.** It sends `cancel`, not `change`,
  so the previously chosen file stays selected and no second inspect is fired. The spec records the
  browser's behaviour rather than inventing one.
- **The guard goes on the one dialog that contains a file input.** Checked: `#editorModal` holds no
  nested `<dialog>` (`_editor_modal.html`), and `#mediaErrorDialog` is a sibling in `base.html`, so no
  other dialog's `cancel` listener can currently receive a descendant's event. The other listeners are
  left untouched, and the slice states that rather than silently widening.
- **The closing motion is not in scope.** The dialog's 150 ms close and its `prefers-reduced-motion`
  branch stay exactly as they are; only the condition that starts them changes.
- **No capability number is reused.** `reading/R31` is the latest on the branch's base (`origin/develop`, 2026-10-29);
  the requirement this slice adds is R32, folded at Fold as `new: reading`.

## Clarifications

### Session 2026-10-29

- No open items. The defect was reproduced on the running page before Specify (the input's `cancel`
  closes the dialog 165 ms later and discards the form), the mechanism was read in `media-entry.js:19`
  and the browser's published behaviour for the file input's `cancel`. Zero open markers remain.
