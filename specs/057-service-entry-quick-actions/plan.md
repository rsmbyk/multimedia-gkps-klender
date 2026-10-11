# Plan 057: Service entry quick fixes

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-059
- **Bump:** patch

## Why

The operator found four frictions while preparing a Tata Ibadah: Save stays disabled in the
single-screen text form, a break needs a dialog, a break offers an Edit it doesn't need, and the
sidebar hides which verses a song uses.

## Root causes (read from the code)

- **Save.** `static/web/entries.js` `wireTextSave` (~line 580) selects
  `[data-entry-form="text"]`. The single-screen form renders `data-entry-form="single_screen_text"`
  (`multimedia/web/templates/reading/_entry_form.html:3`), so the guard never attaches and the
  server-rendered `disabled` stays.
- **Break dialog.** `tatib.html` lines 37, 115 and 140 open the editor with
  `data-entry-open="section_break"`, which loads the New form. The break form has no fields
  (`multimedia/web/reading/entries.py:62`).
- **Break Edit.** The `item.eos` branch in `multimedia/web/templates/reading/tatib.html` (~line
  44) renders an Edit button beside Delete for break entries.
- **Sidebar verses.** `multimedia/web/reading/views.py` builds the sidebar `label`, and
  `_toc.html` renders a two-line label only for text kinds (`two_line_label`). The `Bait` subtitle
  (views.py ~line 745) lists stored numbers without grouping them.

## Approach

1. **Formatter first (TDD).** Add a pure function `format_verses(numbers)` in
   `multimedia/web/reading/` (next to the existing stage helpers) that implements the spec's
   grouping rule. Test it with the spec's examples before wiring anything.
2. **Save guard.** Include `single_screen_text` in the `wireTextSave` selector. Keep the
   server-side `disabled` for the empty case.
3. **Instant break.** Add a POST endpoint that creates a `section_break` at the given position
   (`after` anchor or end), CSRF-checked, mirroring the existing entry create/delete endpoints.
   Point the three "+ Break" buttons at it with a small handler in `static/web/entries.js` that
   refreshes the page's regions in place, the same way `editor:saved` does. Keep the modal path
   for every other kind.
4. **No break Edit.** Remove the Edit button from the `item.eos` branch in `tatib.html` and from
   any other break row; keep Delete.
5. **Sidebar verse line.** In `views.py`, build a second label line for song rows from
   `format_verses(row.verses)`. Render it through the existing `songrow__t--lines` structure.
   Keep the `subtitle`/`Bait` rule of spec 054 and format its numbers with `format_verses`.

## Risks

- The instant-break endpoint must not change the position of other entries; add a test that
  orders entries before and after the insert.
- Removing the break Edit must not remove Edit for songs, passages or text entries; the template
  check must stay per kind.
- The verse line makes sidebar rows taller; the row-height tests in the E2E suite may need a
  targeted update, to be confirmed when implemented.
