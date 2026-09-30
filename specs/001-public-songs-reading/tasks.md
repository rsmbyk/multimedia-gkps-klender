# Tasks 001: Public song reading + design foundation

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/001-public-songs-reading`)
- [ ] Design foundation: base template + `tokens` CSS + component styles
      (GKPS green/blue palette; no Fomantic on reading pages)
- [ ] Red — views/URLs tests (paths): `multimedia/web/tests.py`
- [ ] Green — public views + routes (home, book, song) and `/manage/` relocation + redirects
- [ ] Red — search filtering tests (paths): `multimedia/web/tests.py`
- [ ] Green — server-side song search
- [ ] Red — template-rendering tests for the reading pages (content present without JS)
- [ ] Green — public templates
- [ ] Red — E2E Playwright tests (paths): `tests/e2e/test_reading.py`
- [ ] Green — E2E
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header (`minor` → `0.6.0` on landing)
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in
      **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
