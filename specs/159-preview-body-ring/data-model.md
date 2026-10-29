# Data Model: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md`

Nothing is stored and no payload moves. The only thing this slice models is a transient state the DOM
carries for as long as one preview dialog is open.

## Entities

### Preview body — the focus state

| State | Where it lives | Entered by | Leaves by |
| --- | --- | --- | --- |
| **has focus** | the DOM's own focus | the dialog opening (first focusable element), a pointer click on non-interactive content (`preview.js:470-474`), or Tab | Tab away, Escape, the dialog closing |
| **ring painted** | `:focus-visible` matching + `components.css:2093` | the element holding focus when the keyboard is in use — a key press, or focus arriving by Tab | focus leaving, or the class below |
| **ring suppressed** | `class="is-shortcut"` on `.preview__body` | the space press that operates the player (`preview.js:579-592`) | a `Tab` inside the dialog, opening a preview, closing the dialog |

**Relationships**: one dialog → one body element (`#previewContent`), reused by every preview it opens;
the suppress flag is the body's, so it belongs to the dialog's lifetime, not to one preview's.

**Validation**: the flag may only be set by the space handler and only while an audio or video preview
is open — an image or PDF preview never sets it (its body has no ring to lose, and it has no shortcut).

**State transitions**: `suppressed: absent → present` on the first space press · `present → absent` on
Tab, on open, on close. There is no third state and no timer.

## Invariants

- **Focus never moves because of a space press.** The body keeps DOM focus while the flag is set
  (FR-001, FR-003); only the paint changes.
- **The flag cannot outlive its dialog.** Opening a preview clears it, so a suppressed body never greets
  the next preview (D002).
- **A Tab always restores the paint.** Whatever the flag's state, one Tab inside the dialog makes the
  ring available again (FR-002).

## Not modelled

- **The player's state.** `data-playing`, the label and the progress are `media-audio.js` /
  `media-video.js`'s; the shortcut only calls their `toggle()`.
- **The dialog's own focus policy.** Which element `showModal()` focuses is the browser's and the
  template's (`tabindex="0"` on the body), untouched by this slice.
- **The ring's geometry and colour.** Unchanged — `2px`, offset `-2px`, `--focus`.
