# Contracts: none

**Spec**: `specs/237-sidebar-mark-centering/spec.md`

No external interface is added or changed. No endpoint, request/response shape, model
field, event name, stored format or script API is touched; the only product change is
two selectors in `static/styles/design/components.css`. Existing interfaces relied on
by the verification are:

- `_toc_mark.html`'s `.songrow__mark` span and its `data-mark` values (read only);
- `#chList a.songrow` markup and `.songrow__c`, `.songrow__t` boxes (read only);
- `static/web/reorder.js:268`, which stamps the drag copy from the row's own markup
  (read only);
- the existing Playwright fixture pattern in `tests/e2e/test_sidebar_kind_marks.py`
  (read only).
