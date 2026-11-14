# Tasks — Project button on the song and Bible pages

Ordered by user story; `[P]` means order-independent. The run states the order it used.

## Setup

- [X] T001 [P] [US1] Cut confirmation: the branch `feat/193-reading-project-button` is checked out at `~/Projects/multimedia-gkps-klender-193` off `origin/develop` `9a556a99` (already cut at the change request — verify with `git log --oneline -1`).

## Foundational

- [X] T002 [US1] Write the failing E2E `tests/e2e/test_reading_project.py::test_clicking_project_writes_the_song_pointer` (TDD red): the song page's button click stores `{kind:'song', song_id, index:0}` in `gkps-display` without touching `service`/`screen`/`translation`.
- [X] T003 [US1] Write the failing E2E `::test_one_click_opens_the_projector_window_once`: one click opens exactly one page on `/projector`; a second click reuses it (no second `page` event).
- [X] T004 [US2] Write the failing E2E `::test_clicking_project_writes_the_chapter_pointer` and `::test_sim_page_projects_sim` (TDD red): the chapter page writes `{kind:'passage', book_id, chapter, verse:1, translation}`; the SIM page writes `SIM`.

## US1 — Project the open song

- [X] T005 [US1] `song.html`: add `{% block read_actions %}` with the `.read__project` group — one `data-project-goto` button (`data-goto-song="{{ song.pk }}"`, projector glyph + "Project"), gated `{% if verse_rows %}` (FR-001, FR-007).
- [X] T006 [US1] `display.js`: the delegated `[data-project-goto]` branch — pointer build, content-match skip, `resume()` when hidden (A8), `goTo()` otherwise, `openProjector()` always (research D1–D4); make T002/T003 green.
- [X] T007 [P] [US1] Render pins in `multimedia/web/tests.py::ReadingViewTests`: `test_song_page_draws_project_control` (hymn + ordinary), `test_project_control_is_absent_where_it_has_nothing_to_say` (verse-less song).

## US2 — Project the open chapter

- [X] T008 [US2] `base.html`: the empty `{% block read_row_actions %}` after `.read__lang`; `bible.html` fills it, gated `{% if read_state == 'on' %}`, with `data-goto-book`, `data-goto-chapter`, `data-goto-edition` (FR-002); make T004 green.
- [X] T009 [P] [US2] Render pins: `test_bible_chapter_draws_project_control_beside_the_switch`; absence pin for the book landing page; the saved renderer still draws nothing (saved-parity suite stays green).

## Foundational (projector guard)

- [X] T010 [FR-008] Write the failing E2E `::test_repeat_click_makes_no_second_fetch` (TDD red, route interception on `/projector/goto/*`).
- [X] T011 [FR-008] `projector.js`: the `appliedGoto` guard in `applyGoto()`, cleared by `leaveDetour()`; make T010 green. Add `::test_back_returns_to_the_service` (Back repaints the service; a fresh detour after Back still fetches) and `::test_the_control_survives_in_page_navigation`.

## Polish

- [X] T012 [P] `components.css:3202`: the ≤720px rule gains `[data-project-goto]`; `inspection`: the group reads correctly inside `read__row` (no stray margin), hover/focus states unchanged.
- [X] T013 Run the targeted suites — `multimedia.web.tests.ReadingViewTests` (green), `tests.e2e.test_reading_project` (8/8 green), `tests.e2e.test_dock_goto` + `test_goto_shared_state` + `test_projector` + `test_projector_keys` (98 tests; 14 non-green are byte-identical on unmodified `develop` at `9a556a99` — pre-existing, none introduced), `tests.e2e.test_reading` (see its own result). The plan's `test_saved_render_parity` row was stale: spec 136 removed the offline library and the module is gone from `develop`. Corrected in this task line; recorded in converge.md.

## Delivery (repo conventions)

- [ ] T014 Fold: typed deltas into `docs/spec/reading.md` (R42), `docs/spec/dock.md` (R12), `docs/spec/projector.md` (R1 modified); `fold.md`; `specs/README.md` index row.
- [ ] T015 Converge + `converge.md`; `analysis.md` at zero CRITICAL and full coverage; every checklist item presented to the owner.
- [ ] T016 Pre-merge commit: `VERSION` bumped one **minor** level from `develop`'s number at merge time (declared level: minor — the number is taken at the merge, never pinned here), the `[Unreleased]` changelog line, card ITEM-197 → `In review` once the PR exists (`pr:` filled when the PR is opened), board row move, push as draft PR → ready (`Refs #507`).

## Convergence (added at Implement)

- [ ] T017 [FR-005/FR-006] `projector.js` boot: a Go To already in the state rides on top of an adoption — the adopt's settle re-applies it (the adoption's fetch used to wipe the detour the boot applied while in flight, so a cold open with a service on air could land on the service instead of the detour). Recorded for Converge; the accepted spec requires the cold open to show the detour (US1/AC2) with the service preserved underneath.
