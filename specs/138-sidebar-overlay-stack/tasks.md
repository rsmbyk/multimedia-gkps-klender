# Tasks: the sidebars are a drawer stack

**Slice**: `specs/138-sidebar-overlay-stack` · **Branch**: `feat/138-sidebar-overlay-stack`
**Order used**: T001 → T002 → T003–T004 → T005–T006 → T007–T008 → T009–T011 → T012–T013 →
T014–T017. `[P]` marks order-independent work, not concurrency: one agent, one thread.

## Phase 1 — Setup

- [ ] T001 Run the neighbouring suites as a baseline — `tests.e2e.test_reading`,
  `tests.e2e.test_navigation_freshness`, `tests.e2e.test_song_label_typography` — so a later red is
  known to be this slice's.

## Phase 2 — Foundational (the measuring harness every story consumes)

- [ ] T002 Write `tests/e2e/test_drawer_shell.py`: `DrawerShellE2ETests` on `StaticLiveServerTestCase`, fixtures (a service with two entries, a songbook with songs, a Bible chapter), and helpers —
  `at(width)`, `stage_width()`, `box(selector)`, `state()` returning the four attributes, and
  `demo()` (each width's state machine, using the control and the rail as a person would).

## Phase 3 — US1: a drawer over the page

- [ ] T003 [P] [US1] Write the failing E2E `test_the_stage_keeps_its_width_when_a_drawer_opens` and
  `test_the_columns_layout_is_unchanged_above_the_breakpoint`: at 1024 and 768 the stage's width is
  identical with both drawers open and closed; at 1440 it narrows by the panel's and the song
  list's widths as it does today (FR-001, FR-013, FR-014, SC-001, US1.1, US1.4).
- [ ] T004 [US1] Make T003 pass: the `≤1272px` block in `components.css` — the three custom
  properties to `0`, the drawers fixed at the rail's edge, the resting transform.

## Phase 4 — US2: one stack, and only one

- [ ] T005 [P] [US2] Write the failing E2E `test_the_second_level_covers_its_parent`,
  `test_a_drawer_rests_behind_the_rail` and `test_only_one_sections_stack_is_open`: equal left edges
  and widths; the rail's `z-index` above both drawers and a resting drawer entirely behind it; a
  section switch leaving only the new section's stack (FR-002, FR-003, FR-004, SC-002, SC-003,
  SC-004, US1.2, US2.1, US2.2).
- [ ] T006 [US2] Make T005 pass: the rail's z-index, the child's z-index and geometry, and the
  section switch's close-then-open in `reading.js`.

## Phase 5 — US3: the backdrop closes, the rail restores

- [ ] T007 [P] [US3] Write the failing E2E `test_the_backdrop_closes_the_stack`,
  `test_the_rail_reopens_the_last_level` and `test_escape_closes_the_stack`: a click on the backdrop
  leaving all three levels closed and the stage's scroll unchanged; the rail reopening level 1+2
  when 2 was last; Escape closing the whole stack (FR-005, FR-006, SC-005, SC-006, US3.1–US3.4).
- [ ] T008 [US3] Make T007 pass: the backdrop element and its handler, `restoreLast()` per section,
  and the Escape handler.

## Phase 6 — US4: a phone gets a toolbar and a real menu

- [ ] T009 [P] [US4] Write the failing E2E `test_the_phone_shows_the_toolbar_and_no_strip`,
  `test_the_phone_drawers_span_the_window`, `test_the_control_opens_and_closes_the_stack`,
  `test_the_menu_lists_the_sections_with_their_names` and
  `test_the_project_control_is_hidden_on_a_phone` (FR-007–FR-012, FR-017, SC-007–SC-010, US4.1–US4.6).
- [ ] T010 [P] [US4] Write the failing E2E `test_a_service_offers_no_contents_drawer_on_a_phone`,
  `test_a_sections_list_opens_over_the_menu`, `test_a_service_row_on_a_phone_opens_the_page` and
  `test_a_selected_menu_row_paints_its_name_in_the_icon_ink` (FR-016, FR-018–FR-020).
- [ ] T011 [US4] Make T009 and T010 pass: the `.topbar` markup in `base.html`, the `≤720px` block,
  `data-rail` and the control's two glyphs, the level-2 refusal, and the post-navigation close.

## Phase 7 — US5 and polish

- [ ] T012 [P] [US5] Write the failing E2E `test_the_page_behind_a_drawer_does_not_scroll`,
  `test_each_drawers_own_back_control_steps_one_level`, `test_a_rows_edit_control_shows_without_hover`,
  `test_a_phone_row_is_two_lines`, `test_the_toolbar_icons_share_one_size`,
  `test_a_navigation_keeps_the_open_stack` and
  `test_resizing_across_the_breakpoint_leaves_a_fitting_state` (FR-015, FR-021–FR-023, US5.1,
  US5.2, the navigation and resize edges).
- [ ] T013 [US5] Make T012 pass: `data-drawer-open`, the two chevrons' phone behaviour, the touch
  exemption, the row grid and the one icon size.

## Phase 8 — Polish and delivery

- [ ] T014 Re-run the matrix (T001's modules, `tests.e2e.test_drawer_shell`, the prototype scripts)
  and record the numbers.
- [ ] T015 Fold the capability — `docs/spec/reading.md` gains `R14` — and write `fold.md` (added: one
  requirement; the header moves `last folded` to 2026-10-27 and prepends `138-sidebar-overlay-stack`).
- [ ] T016 Apply `bump: minor` in the pre-merge commit: `VERSION` `1.21.1` → `1.22.0`, one
  `CHANGELOG.md` line under `## [Unreleased]` → `### Changed`, the card's `release_version` empty.
- [ ] T017 Write the PR title and body; move the card to `In review` once the push has created the
  PR, and `Done` before the merge.
- [ ] T018 Migrate the neighbouring E2E that reach a sidebar at 720px or below — `tests/e2e/test_reading`
  clicks `.rail [data-panel=…]` directly and expects the pushed column, which this slice replaces.
  One module-level helper (`click_section`) opens the drawer's control first; 36 call sites use it.
  Each affected test's assertions are then re-read against `R14`, not merely re-pointed.
