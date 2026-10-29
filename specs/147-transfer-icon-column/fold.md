# Fold: a transfer row's icon column

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R20` | A transfer row keeps a 32px icon column that content cannot narrow; a name wider than the text column ellipsizes inside the space the row reserves, and every row's name and status label share one left edge — at 580px and at 382px dialogs alike, in the list the library button draws and the one the rail draws |

Counts: before 19 requirements, after 20. No requirement was modified, removed or renamed.

## Drift guard

- **Files changed in this capability**: `static/styles/design/components.css` (one declaration on
  `.media-transfers__mark`), `tests/e2e/test_media_library.py` (one helper, three tests),
  `docs/spec/reading.md` (R20, the header's `slices`), and the slice's own records under `specs/147-*`.
  `static/web/media-handoff.js` and `multimedia/web/templates/reading/base.html` are unchanged.
- **Declared no behaviour change**: no — the row's rendering changes when a name is too long for the
  dialog, which R20 states.
- **Idempotent**: re-running this fold finds `R20` already present and changes nothing.
