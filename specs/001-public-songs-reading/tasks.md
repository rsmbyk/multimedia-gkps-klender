# Tasks 001: Public song reading + design foundation

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/001-public-songs-reading`)
- [x] Design foundation: base template + `tokens` CSS + component styles
      (GKPS green/blue palette; no Fomantic on reading pages)
- [x] Red — views/URLs tests (paths): `multimedia/web/tests.py`
- [x] Green — public views + routes (home, book, song) and `/manage/` relocation + redirects
- [x] Red — search filtering tests (paths): `multimedia/songs/tests.py`
- [x] Green — server-side song search
- [x] Red — template-rendering tests for the reading pages (content present without JS)
- [x] Green — public templates
- [x] Red — E2E Playwright tests (paths): `tests/e2e/test_reading.py`
- [x] Green — E2E
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`minor` → `0.6.0` on landing)
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in
      **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
