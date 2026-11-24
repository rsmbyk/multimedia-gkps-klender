# Contracts: none

**Spec**: `specs/236-song-modal-scrollbar/spec.md`

No external interface is added or changed. No endpoint, request/response shape, model field,
event name, stored format or script API is touched; the only product change is one declaration in
`static/styles/design/components.css`. Existing interfaces relied on by the verification are:

- the rendered `#editorModal` / `.editor__content` markup from
  `multimedia/web/templates/reading/_editor_modal.html` and `reading/_entry_form.html` (read only);
- the song results menu anchored to `#entry-song-search`, whose fixed positioning is preserved
  (`reading/R48`, read only);
- the existing Playwright fixture pattern in `tests/e2e/test_entry_pickers.py` (read only).
