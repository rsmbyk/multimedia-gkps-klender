# Tasks 032: Entry preview modal

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/032-entry-preview-modal`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): the preview button appears for clamped
      texts, passages, songs, and clamped legacy rows, and not for short texts or section breaks;
      the inline payloads carry the passage reference and body, and the song title and
      verse-labelled tabs
- [ ] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`,
      `multimedia/web/templates/reading/base.html`,
      `static/styles/design/components.css`, `static/web/preview.js`)
- [ ] Red — E2E (`tests/e2e/test_entry_preview.py`): open, scroll, sticky close, overlay and Esc
      dismiss, and no lingering focus outline
- [ ] Green — E2E
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
