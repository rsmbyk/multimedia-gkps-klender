# Tasks 104: Restrict the search page to the listed content fields

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Commits on `fix/104-search-field-scope` (cut from `develop`; the draft and its corrections are its first commits)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): negatives — Bible references on the served page (`Matius 5:13`, `Matius 5`, `Yoh 3:16`), songbook name, bare song number, songbook references (`KJ 152`, `Kidung Jemaat 152`, `HAL 411`), book name, service date, section label, song-entry body under Tata Ibadah; positives — verse text/title, song title/lyric, service name, entry title, text-entry body, entry-only service listed by name, entry row links `#ti-e<pk>`
- [ ] Red — the served page lists no reference row: `multimedia/web/tests.py::test_search_page_resolves_bible_reference` becomes a no-row negative; flip `tests/test_web_search.py::test_bible_book_name_row` and `::test_song_reference_full_name_equals_abbreviation` to no-match negatives (the `test_bible_reference_*` pins stay green — they pin the row the Go To reads)
- [ ] Green — implementation: `multimedia/web/reading/search.py` (`_entry`/`_match_score` meta+refs channels; `_bible_hits` book loop dropped, `_song_hits` incl. deleting `_SONG_REF_RE`, `_tatib_hits`) + module docstring
- [ ] Green — the page drops `reference`/`chapter` rows: `multimedia/web/reading/views.py` `SearchView` filters them out of `results['bible']` before `_search_groups` (counts and paging follow); the Bible reference insert stays in `search.py` for the Go To
- [ ] Red — saved-copy parity: `tests/e2e/test_offline_library.py` — same queries, same groups, no excluded matches
- [ ] Green — `static/web/offline-render.js` `searchPage()` (book/songbook rows, the verse label/alias bump, and the song reference bump go)
- [ ] Red — E2E: `tests/e2e/test_reading.py` — no excluded matches on the served page (`Matius 5:13` lists nothing; `test_search_resolves_bible_reference` becomes a no-row walk; the edition-preference walk at 910/917 navigates by panel); an entry row opens its service
- [ ] Green — E2E
- [ ] Remove the home hint (red first): the six pins — `multimedia/web/tests.py::test_home_is_search_first` and `tests/e2e/test_reading.py` (229, 267, 285, 1651, 1657) — become `search-home__hint` absence checks; then delete the element in `base.html:343` and the `.search-home__hint` rules (`static/styles/design/components.css`: 831, and its half of 835–836)
- [ ] No Go To change at all: `projector_lookup` and `projector-library.js` stay byte-identical — re-run `tests/e2e/test_projector.py` and the lookup tests in `multimedia/web/tests.py` untouched
- [ ] Run the touched classes locally (`multimedia/web/tests.py` search tests; `tests/test_web_search.py`; browser E2E is the CI step)
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Create ITEM-104 and update [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
