# Tasks 104: Restrict the search page to the listed content fields

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner (including the home hint's new song example)
- [ ] Commits on `fix/104-search-field-scope` (cut from `develop`; the draft and its correction are its first commits)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): negatives — songbook name, bare song number, songbook references (`KJ 152`, `Kidung Jemaat 152`, `HAL 411`), book name, service date, section label, song-entry body under Tata Ibadah; positives — verse text/title, song title/lyric, service name, entry title, text-entry body, entry-only service listed by name, entry row links `#ti-e<pk>`
- [ ] Green — implementation: `multimedia/web/reading/search.py` (`_entry`/`_match_score` meta+refs channels; `_bible_hits`, `_song_hits` incl. deleting `_SONG_REF_RE`, `_tatib_hits`) + module docstring
- [ ] Red — saved-copy parity: `tests/e2e/test_offline_library.py` — same queries, same groups, no excluded matches
- [ ] Green — `static/web/offline-render.js` `searchPage()`
- [ ] Red — E2E: `tests/e2e/test_reading.py` — no excluded matches on the served page; `Matius 5:13` still first; an entry row opens its service
- [ ] Green — E2E
- [ ] Home hint: replace the song example in `base.html` and move its six assertions (`multimedia/web/tests.py::test_home_is_search_first`; five `tests/e2e/test_reading.py` sites) to the accepted literal
- [ ] No projector change expected: `projector_lookup` resolves `KJ`/`NKB` refs before the shared matcher (views.py:1124–1153) — re-run `test_projector.py` unchanged
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
