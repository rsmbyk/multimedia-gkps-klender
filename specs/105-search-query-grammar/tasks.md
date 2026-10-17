# Tasks 105: Search query grammar and ranking

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/105-search-query-grammar`); spec 104's page matcher lands first
- [ ] Red — domain tests (`tests/test_web_search.py`, new `search_page()` class): tokenizing table (symbols, digits, quotes, dash, dash-in-quotes, unclosed quote), canonical table (owner's `Allah, "Tuhan. Yesus:Kristus" -kasih` → `Allah 'Tuhan Yesus Kristus' -kasih`), exclusion, exclusion-only and symbols-only notices, substring match (`kasih` matches `mengasihi` and `Kasih-Nya`), phrase adjacency (and a symbol between phrase words breaking the phrase), coverage order, order score (in-order beats reversed; best-occurrence configuration), title tie-break
- [ ] Green — `multimedia/web/reading/search.py`: `parse_query()` + `search_page()` matching and ranking (soft AND, coverage, order), excerpt anchor
- [ ] Red — app tests (`multimedia/web/tests.py`): served page shows the canonical status line and page title, the exclusion notice, and partial matches below full ones
- [ ] Green — `multimedia/web/reading/views.py` `SearchView` passes `canonical` + `notice`; `multimedia/web/templates/reading/search.html` renders them
- [ ] Red — saved-copy parity (`tests/e2e/test_offline_library.py`): one shared query table — rows, order, canonical line, notices
- [ ] Green — `static/web/offline-render.js` `searchPage()` (parser, matching, ranking, canonical, notices)
- [ ] Red — E2E (`tests/e2e/test_reading.py`): one grammar walk — quoted phrase, `-` exclusion, canonical status line
- [ ] Green — E2E
- [ ] No Go To change at all: `search()` and `projector_lookup` stay byte-identical — re-run `tests/e2e/test_projector.py` and the lookup tests in `multimedia/web/tests.py` untouched
- [ ] Run the touched classes locally (`tests/test_web_search.py`; `multimedia/web/tests.py` search tests; browser E2E is the CI step)
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump: patch` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Create ITEM-105 and update [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
