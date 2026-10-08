# Plan 045: Make the passage modal's chapter/verse dropdowns custom

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-047
- **Bump:** patch

## Why

The passage modal mixes a custom book picker with native chapter/verse selects, so it looks and
behaves unevenly. Replace the three native selects with the same custom dropdown component.

## Scope / edges

**In:**

- Chapter, from-verse and to-verse in the passage modal become custom dropdowns, matching the book
  picker's look and interaction, in the add and edit modals.
- Their dynamic filling (`fillChapters`, `loadVerses`, `syncTo`) drives the custom controls.
- The to-verse's disabled state and its hover note survive.
- Their values still POST as `chapter` / `verse_start` / `verse_end`.

**Out:**

- The book picker itself.
- The song modal and the sidebar editors, unless the scope is widened.

## Approach

- `static/web/entries.js` — factor the picker's open/close/select plumbing so it can serve the
  chapter and verse controls too (the book picker's `wirePickerMenus()` and its option rendering are
  the model). Keep `fillChapters` / `loadVerses` / `syncTo` writing options into the custom menus
  instead of native `<select>`s, and keep each control's hidden value input in step.
- `multimedia/web/templates/reading/_entry_form.html` — render chapter / verse_start / verse_end as
  the custom picker markup (trigger + menu + hidden value), keeping the `.editor__end-wrap` tip on the
  to-verse.
- `static/styles/design/components.css` — reuse the `.editor__picker` styles; adjust only if the
  narrow controls need it.
- `static/web/entries.js` `placeMenu()` already serves picker menus (and spec 040 widens placement);
  the new controls ride on it.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the fragment renders the three controls as the custom
  picker markup (with values POSTing), in add and edit.
- E2E: `tests/e2e/test_entry_pickers.py` — open each control, pick a value, see it reflected; the
  to-verse disables with its note; the form still saves the right chapter/verses.

## Risks

- **Value plumbing.** A custom control that loses its hidden input silently breaks the save; verify
  each posts.
- **Dynamic refills.** Options are rebuilt as the book/chapter changes; the custom menus must follow
  and not keep stale options.
- **The disabled tip.** The to-verse's note is tied to the native control's disabled state; port it
  deliberately.
