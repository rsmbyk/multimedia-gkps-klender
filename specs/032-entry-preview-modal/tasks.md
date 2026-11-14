# Tasks 032: Entry preview modal

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/032-entry-preview-modal`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): the preview button appears for clamped
      texts, passages, songs, and clamped legacy rows, and not for short texts or section breaks;
      the inline payloads carry the passage reference and body, and the song title and
      verse-labelled tabs
- [x] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`,
      `multimedia/web/templates/reading/base.html`, `multimedia/web/templates/reading/_preview_modal.html`,
      `static/styles/design/components.css`, `static/web/preview.js`)
- [x] Red — E2E (`tests/e2e/test_entry_preview.py`): open, verse tabs, overlay and Esc dismiss
- [x] Green — E2E
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
