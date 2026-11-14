# Tasks 044: Add a TB/SIM toggle to the passage modal book picker

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/044-passage-translation-toggle`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): add/edit fragments carry both translations'
      IDs/names and reflect TB for a new form or the stored edition for an edit
- [x] Green — server form data (`multimedia/web/reading/entries.py`): expose both translations per
      book and preserve the selected edition on re-render
- [x] Red — E2E (`tests/e2e/test_entry_pickers.py`): switching swaps names and selected value;
      chapter/verse options and values stay put; selecting another book follows the active edition;
      a book without TB/SIM keeps its existing fallback selectable
- [x] Green — modal markup, toggle behavior, and styling (`multimedia/web/templates/reading/_entry_form.html`,
      `static/web/entries.js`, `static/styles/design/components.css`)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`patch`)
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
