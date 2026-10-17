# Tasks 104: Restrict the search page to the listed content fields

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Commits on `fix/104-search-field-scope` (cut from `develop`; this draft is its first commit)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): negatives — songbook name, bare song number, book name, service date, section label, song-entry body under Tata Ibadah; positives — verse text/title, song title/lyric, service name, entry title, text-entry body, entry-only service listed by name, entry row links `#ti-e<pk>`
- [ ] Green — implementation: `multimedia/web/reading/search.py` (`_entry`/`_match_score` meta channels; `_bible_hits`, `_song_hits`, `_tatib_hits`) + module docstring
- [ ] Red — saved-copy parity: `tests/e2e/test_offline_library.py` — same queries, same groups, no excluded matches
- [ ] Green — `static/web/offline-render.js` `searchPage()`
- [ ] Red — E2E: `tests/e2e/test_reading.py` — no excluded matches on the served page; `Matius 5:13` still first; an entry row opens its service
- [ ] Green — E2E
- [ ] Run the touched classes locally (`multimedia/web/tests.py` search tests; browser E2E is the CI step)
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Create ITEM-104 and update [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
