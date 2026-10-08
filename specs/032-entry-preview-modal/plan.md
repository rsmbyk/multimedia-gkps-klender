# Plan 032: Entry preview modal

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-034
- **Bump:** minor

## Why

The pane abbreviates an entry: a text is clamped to three lines (spec 031), and a passage or song is
shown by reference alone. The operator has no way to read the whole content without leaving the page.
Add a preview button on each eligible entry that opens a read-only modal with the full content.

## Scope / edges

**In:**

- A preview button on text entries that were clamped, on passages, and on songs; legacy text rows too
  (they are clamped the same way, spec 031). Section breaks carry no content and get none.
- A view-only modal, no header, the content inline with the page, the body scrollable, a sticky
  close button at the bottom, dismissed by the overlay and by Esc.
- Content per kind:
  - **Text** — the whole body (what the pane hid).
  - **Passage** — the full passage text with its reference(s) at the top.
  - **Song** — the songbook and song title, then the selected verses as tabs labelled by **verse
    number**; the tabs are centred horizontally and scroll when there are many; a single selected
    verse shows no tab row.
- Focus handled with `window.gkpsFocus.restoreQuietly`, so no row keeps a stale outline (spec 025 /
  ITEM-027, ITEM-016).

**Out:**

- Any editing from the modal (view-only).
- Fetched content — the content is rendered inline.
- Section breaks.
- The projector.

## Approach

- `multimedia/web/reading/views.py` — when building a pane item, include its preview payload inline:
  the full text for a text kind; the citation and full body for a passage; the songbook/title and
  the selected verses (number + lyric) for a song. Reuse `ServiceEntry.resolve()`,
  `_scripture_body()`, and `citation()`. A text item carries the spec 031 `clipped` flag; the button
  is shown only when it is set.
- `multimedia/web/templates/reading/tatib.html` — add the preview button to `entry__acts` (and the
  legacy-row actions) with a `data-preview-open` and a link to its inline payload.
- `multimedia/web/templates/reading/base.html` — include the one preview `<dialog>` host (no header,
  a scrollable body, a sticky close button) and load `static/web/preview.js` beside the editor
  scripts.
- `static/web/preview.js` — its own module, matching the editor modals' UX: fill the dialog from the
  trigger's inline payload, `showModal()`, close on the overlay (`event.target === dialog`) and on
  Esc (native), and on close `window.gkpsFocus.restoreQuietly(trigger)`. Reset content on close so a
  stale preview never lingers.
- `static/styles/design/components.css` — the dialog shell (no header, scrollable body, sticky
  footer close) and the centred, scrollable song tab row.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the pane renders a preview button for passages,
  songs, and clamped texts, and not for a short text or a section break; the inline payload holds the
  reference and whole body for a passage, and the title plus verse-labelled tabs for a song.
- E2E: `tests/e2e/test_entry_preview.py` — opening a preview; the body scrolls; the close button is
  reachable when scrolled; the overlay and Esc close it; no stale focus outline is left on the row.

## Risks

- **Stale focus/outline.** The exact bug the sidebars had (spec 025); the close path must restore
  focus quietly and never re-open the dialog on the same trigger without resetting.
- **Inline payload size.** A long service page carries every entry's full content; acceptable per the
  owner's choice, but watch page weight.
- **Esc ordering.** With the editor dialog also on the page, Esc must close only the top-most dialog
  (native `<dialog>` behaviour) and not disturb the other.
