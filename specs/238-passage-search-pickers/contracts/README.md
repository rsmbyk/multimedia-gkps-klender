# Contracts: none

**Spec**: `specs/238-passage-search-pickers/spec.md`

No external interface is added or changed. No endpoint, request/response shape, model field,
stored format or event name is touched. The posted form still carries `book_translation`,
`chapter`, `verse_start` and `verse_end` through the same hidden selects, and the existing
`/editor/entry/chapter/<pk>/<n>/` fetch is unchanged.

Existing interfaces relied on by this slice (read only):

- `_entry_form.html`'s `[data-entry-picker]` blocks and `.editor__picker-menu` structure;
- `entries.js`'s `placeMenu()`, `closeMenus()` and `wirePickerMenus()`;
- the hidden selects' `data-initial` attributes for the edit path;
- `tests/e2e/test_song_entry_pickers.py` as the green behavioural baseline;
- `preview/run.py`, which reads the database URL from the compose web container.

The change alters two *internal* contracts: Book answers `[data-menu-anchor]` rather than
`[data-picker-trigger]`, and the three numeric popovers gained an in-menu search field. Both are
template/JS contracts inside one file pair; `tests/e2e/test_entry_pickers.py` is migrated.
