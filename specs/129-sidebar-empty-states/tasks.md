# Tasks: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`
**Plan**: `specs/129-sidebar-empty-states/plan.md`
**Verification split**: 12 test · 4 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 `specs/129-sidebar-empty-states/preview/probe_empty_states.py` — the headless probe that opens
  each state, prints the copy, the glyph and the ink's offset from the pane's centre, and saves a screenshot

## Phase 2 — Foundational

- [X] T002 `static/styles/design/components.css` — the `.listempty` component (absolute over its pane,
  `place-content: center`, glyph / title / hint, `pointer-events: none`, `[hidden]` rule, mini-panel hide),
  and `position: relative` on `.panel__scrollwrap` and `.ch__wrap`
- [X] T003 `multimedia/web/reading/views.py` — `PANEL_META` and `CH_META` carry `empty_title`, `empty_hint`
  and `filter_title`; `_shell` exposes them as `panel_empty_*`, `panel_filter_title`, `ch_empty_*`,
  `ch_filter_empty_title`

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: an empty list is centred in its pane under a glyph and says which list it is.
**Independent test**: open an empty Tata Ibadah and an empty songbook; both blocks centred, each naming its
own list.

- [X] T004 [P] [US1] `multimedia/web/tests.py::ReadingViewTests::test_the_first_list_names_the_empty_and_the_filtered_case`
  and `…::test_each_section_names_its_own_first_list`
- [X] T005 [P] [US1] `multimedia/web/tests.py::ReadingViewTests::test_a_songbook_with_no_songs_says_no_songs_yet`
  and `…::test_a_service_with_no_sections_says_no_sections_yet`
- [X] T006 [US1] `multimedia/web/templates/reading/base.html` — both blocks in their panes, two glyph spans,
  the four copy attributes, `role="status"`, `hidden`
- [X] T007 [US1] `static/web/reading.js` — `paintListEmpty` and the boot paint, so a page that arrives empty
  is typed before the first keystroke
- [X] T008 [US1] `static/styles/design/components.css` — remove `.panel__empty` and `.ch__empty`
- [X] T009 [US1] `tests/e2e/test_reading.py::ReadingE2ETests::test_sidebar_empty_states_are_centred_and_typed`
  — the two empty states, the pass to the filter state and back, and the measured centring

## Phase 4 — US2 (P1)

**Goal**: a filter that matched nothing says so in its own words and under its own glyph.
**Independent test**: on a page whose list has rows, a query that matches nothing switches the block to the
miss copy; clearing it hides the block.

- [X] T010 [US2] `static/web/reading.js` — count the rows in both filters and type the block
  (`empty` / `filter` / hidden)
- [X] T011 [US2] `multimedia/web/templates/reading/base.html` — the two glyphs, `data-when` keyed
- [X] T012 [P] [US2] `static/web/entries.js` — deleting a Tata Ibadah's last row paints the empty state
  through `window.shellListEmpty`

## Phase 5 — US3 (P2)

**Goal**: a page rebuilt from the saved library carries the same copy and glyphs as the server route.
**Independent test**: render a Kidung and a Tata Ibadah route from the saved library and read both blocks.

- [X] T013 [US3] `static/web/offline-render.js` — `LIST_EMPTY`, `labelListEmpty` and `paintListEmptyStates`,
  called from both renderers
- [X] T014 [US3] `tests/e2e/test_saved_render_parity.py` — the existing parity suite still passes against the
  re-labelled blocks

## Phase 6 — Polish

- [X] T015 [P] `static/web/reading.js` — the in-page swap copies the arriving page's block with
  `reconcileNode`, so copy, glyph and state travel with a navigation
- [X] T016 Docs: `CHANGELOG.md`, `VERSION`, `docs/spec/reading.md`, `backlog/` — at Fold

## Phase 7 — Convergence

**Converged on pass 2** — see `converge.md`. No requirement gap; two partials were fixed during the run (the
divider row counted as an empty list; the miss glyph's cross moved inside the lens). The fold is
`docs/spec/reading.md` `R7`, recorded in `fold.md`.
