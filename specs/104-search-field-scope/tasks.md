# Tasks 104: Restrict the search page to the listed content fields

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Commits on `fix/104-search-field-scope` (cut from `develop`; the draft and its corrections are its first commits)
- [ ] Red — page matcher tests (`tests/test_web_search.py`, new `search_page()` class): negatives — Bible references (`Matius 5:13`, `Matius 5`, `Yoh 3:16`), songbook name, bare song number, songbook references (`KJ 152`, `Kidung Jemaat 152`, `HAL 411`), book name, service date, section label, song-entry body under Tata Ibadah; positives — verse text/title, song title/lyric, service name, entry title, text-entry body, entry-only service listed by name, entry row links `#ti-e<pk>`
- [ ] Green — `search_page()` in `multimedia/web/reading/search.py`: the six fields only, entries indexed, its own title/body scoring; `search()` (the Go To's fallback) is left byte-identical
- [ ] Red — app tests (`multimedia/web/tests.py`): the served page lists no reference row (`test_search_page_resolves_bible_reference` flips to a no-row negative), no book row, no songbook row
- [ ] Green — `SearchView` calls `search_page()`; no result filtering in the view
- [ ] Red — saved-copy parity: `tests/e2e/test_offline_library.py` — same queries, same groups, no excluded matches
- [ ] Green — `static/web/offline-render.js` `searchPage()` (book/songbook rows, the verse label/alias bump, and the song reference bump go)
- [ ] Red — E2E: `tests/e2e/test_reading.py` — no excluded matches on the served page (`Matius 5:13` lists nothing; `test_search_resolves_bible_reference` becomes a no-row walk; the edition-preference walk at 910/917 navigates by panel); an entry row opens its service
- [ ] Green — E2E
- [ ] Remove the home hint (red first): the six pins — `multimedia/web/tests.py::test_home_is_search_first` and `tests/e2e/test_reading.py` (229, 267, 285, 1651, 1657) — become `search-home__hint` absence checks; then delete the element in `base.html:343` and the `.search-home__hint` rules (`static/styles/design/components.css`: 831, and its half of 835–836)
- [ ] No Go To change at all: `search()`, `projector_lookup`, and `projector-library.js` stay byte-identical — re-run `tests/e2e/test_projector.py`, the lookup tests in `multimedia/web/tests.py`, and the legacy `tests/test_web_search.py` pins untouched
- [ ] Run the touched classes locally (`tests/test_web_search.py`; `multimedia/web/tests.py` search tests; browser E2E is the CI step)
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Create ITEM-104 and update [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
