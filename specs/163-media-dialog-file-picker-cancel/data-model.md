# Data Model: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`

Nothing stored changes and no state is added. What this slice draws a boundary around is one event's
route.

## Entities

### `cancel` event

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `type` | string | always `"cancel"`; both sources use the same name | FR-001 |
| `target` | EventTarget | `#editorModal` for the dialog's own Escape; `input[data-media-file]` for the picker's dismissal | FR-001 |
| `bubbles` | boolean | `true` for both sources (MDN: the input's `cancel` "can bubble") | FR-001 |
| `cancelable` | boolean | `true` at the dialog, `false` at the input — **not** usable as the discriminator, which is why the rule is written on `target` | FR-001 |

**Relationships**: the input is a descendant of the dialog, so its event reaches the dialog's listener.
**Validation**: an event closes a dialog only when `event.target` is that dialog.
**State transitions**: none — the event carries no state between occurrences.

### File input

`input[type=file][data-media-file]` (`_entry_form.html:36`, inside `form[data-entry-form="media"]`).
Unchanged: hidden, cleared and clicked by `[data-media-choose]` (`media-entry.js:200`), read by
`input.onchange` (`:201`) and cleared again on the next open.

### New media dialog

`#editorModal`, one element for every editor kind. Unchanged: `close()` is wrapped (`media-entry.js:9-18`)
to run the 150 ms `media-closing` class when a media form is present; the error dialog
(`#mediaErrorDialog`) is a sibling, not a child.

## Invariants

- **A `cancel` closes only the dialog it names.** A descendant's `cancel` changes nothing (FR-001, FR-002).
- **No form state is a casualty of the picker.** Tab, chosen file, typed title, Save state and note survive
  a dismissal (FR-002).
- **Dismissal by the dialog itself is unchanged.** Escape and Cancel still close it, with the same 150 ms
  motion (FR-003).

## Not modelled

- **The picker's own lifecycle.** It belongs to the browser and the OS; the page only ever sees the
  resulting `change` or `cancel`.
- **`dirty`/`pristine` form tracking.** There is none today; the fix preserves state by not closing, which
  needs no model.
