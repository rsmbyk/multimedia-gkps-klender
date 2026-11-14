# Tasks: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`
**Plan**: `specs/127-site-name-tab/plan.md`
**Verification split**: 10 test · 1 inspection · 2 manual

## Phase 1 — Setup

- [x] T001 [P] [US1] [US2] Add two pins to `multimedia/web/tests.py` (`ReadingViewTests`):
      `test_the_index_tab_names_the_site_and_stops_there` — the root's `page_title` and its rendered
      `<title>` are exactly `Multimedia GKPS Klender` — and `test_a_section_landing_puts_the_site_name_last`
      — `/bible/`'s title is `Alkitab — Multimedia GKPS Klender`. Red first: the index's title is
      `GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah` today. *(FR-001, FR-002, SC-001, SC-002,
      US1/AC4, US2/AC1)*

## Phase 2 — Foundational

- [x] T002 `n/a — nothing is shared beyond T001's pins; every title is composed where it is already composed.`

## Phase 3 — US2 (P1) 🎯 MVP

**Goal**: the index's tab is the site name alone.
**Independent test**: T001's index leg.

- [x] T003 [US2] `multimedia/web/reading/views.py`: `HomeView.page_title` and `SearchView`'s no-query branch
      read `Multimedia GKPS Klender`, dropping the trailing `— Search Alkitab, Kidung, and Tata Ibadah`.
      `/` (`IndexView`), `/home/` and `/search` without a query all render through them.
      *(FR-001, US2/AC1–AC3)*
- [x] T004 [US2] `templates/reading/home.html`'s title block and `base.html`'s `<title>` default drop the
      tagline, so a page that composes no title also stops at the name. *(FR-001, US2/AC1)*
- [x] T005 [US2] `static/web/offline-render.js` `homePage()` writes the site name alone; without it the saved
      landing renames itself when the online update lands. *(FR-004, US3/AC2)*

## Phase 4 — US1 (P1)

**Goal**: every other reading tab ends with the new name.
**Independent test**: T001's section-landing leg plus the existing chapter, song and service title pins.

- [x] T006 [US1] `views.py`: the remaining ten `page_title` strings take ` — Multimedia GKPS Klender`
      (Bible chapter/book/section, Kidung section/book/song, Tata Ibadah service/section, results, search,
      media library). The leading text is untouched. *(FR-002, FR-003)*
- [x] T007 [US1] Template defaults in `bible.html`, `book.html`, `book_index.html`, `song.html`,
      `tatib.html`, `media_library.html`. *(FR-002)*
- [x] T008 [US1] `static/web/offline-render.js`: `common()`, `listPage()` and the search-results document
      append the new name. *(FR-004, US3/AC1)*
- [x] T009 [US1] `static/web/reading.js` `syncVisibleBibleTitle()` appends the new name, so switching the
      Bible edition in place does not change the tab's name. *(FR-005, US3/AC3)*
- [x] T010 [US1] Update the assertions that pin the old name: 3 in `multimedia/web/tests.py`, 6 in
      `tests/e2e/test_reading.py`, 1 in `tests/e2e/test_offline_library.py`, 1 in
      `tests/e2e/test_saved_render_parity.py`. *(FR-006, SC-003, SC-004)*

## Phase 5 — Polish

- [x] T011 Run the touched unit module: `manage.py test multimedia.web --keepdb` — 306 tests OK, with
      `ReadingViewTests`' 43 (T001's two pins among them). (A fresh worktree needs `collectstatic` first: without `_static/`, nine unrelated
      page-render tests in the full run error on `Missing staticfiles manifest entry for 'assets/gkps.png'`.)
- [x] T012 Read the titles on the running branch: `/`, `/home/`, `/bible/`, `/bible/1/1/` (TB, then the SIM
      switch in headless Chromium), `/songs/`, `/songs/1013/`, `/tatib/`, `/search`, `/search?q=kasih`,
      `/media-library/` — all as specified in `converge.md`. *(SC-001, SC-002)*

## Phase N+1 — Convergence

- [x] T013 [Converge] Re-read every requirement against the shipped code, run the checks in `converge.md`,
      and record the evidence and any accepted gaps.
- [x] T014 [Fold] Apply the delta to `docs/spec/reading.md` — R1's tab clause takes the new suffix, R3 enters
      the tree — and add the `specs/README.md` index row. Runs only after T013 reports Converged.
- [x] T015 [Delivery] `backlog/items/ITEM-129-site-name-tab.md` and its `backlog/board.md` row; `VERSION`
      1.20.4 → 1.20.5 and the `CHANGELOG.md` entry under `[Unreleased]` → Changed. Push and the draft PR
      wait for the owner's word.

**Delivery note**: T015's artifacts are in this commit; the push and the draft PR wait for the owner's word.
