# Tasks: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md` · **Plan**: `plan.md`

Order used: T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011. No `[P]` task
this run: one agent, one thread, and the tests all touch one function.

## Phase 1 — Setup

- [x] T001 Branch and worktree on `feat/165-media-entry-rest` from `develop` `59182b12`; test database
      `gkps164` exported (see `quickstart.md`).

## Phase 2 — Foundational

- [x] T002 Record the before-numbers for services 149, 146 and 144 from `_projector_data` (six, three
      and 167 screens) so the tests below assert a known starting point, not a remembered one.

## Phase 3 — US1: a media entry rests after its screen (P1)

- [x] T003 Red — `multimedia/web/test_media.py`, new class `MediaEntryRestTests`:
      `test_each_family_ends_on_one_rest` (image, audio, video, pdf, slides — each entry is a media
      screen then a blank, the blank carrying no payload key).
- [x] T004 Red — `…::test_a_media_entry_without_a_file_keeps_its_one_rest` (one screen, blank).
- [x] T005 Red — `…::test_the_rest_carries_only_the_built_in_blank` (keys `{blank, header, lines,
      entry_index}`; no `bait`, `bait_rest`, `split`, `split_total`, `translation`).
- [x] T006 Red — `…::test_the_entry_range_extends_over_the_rest` (`start` unchanged, `end == start + 1`,
      `type`/`label` unchanged) and `…::test_four_images_in_a_row_build_ten_screens` (the service-149
      shape: ranges `(0,1)(2,3)(4,5)(6,7)(8,9)`, blanks at 1, 3, 5, 7, 9, last screen blank).
- [x] T007 Red — rewrite the four cases that pin today's rule: `test_powerpoint_entry_has_slide_preview_and_projector_screen`,
      and the three renamed with it (`test_image_and_pdf_each_have_a_screen_and_a_rest`,
      `test_audio_has_a_screen_and_a_rest_in_order`, `test_video_has_a_screen_and_a_rest_in_service_order`) —
      each keeps its payload assertion and moves `start == end` to `start + 1 == end`, the last screen
      blank. Seen red: `AssertionError: 1 != 2` and the rest-shape case's `IndexError` on `screens[1]`.
- [x] T008 Green — `multimedia/web/reading/views.py`: `_MEDIA_SCREEN_KEYS` beside `_blank_screen()`, and
      the media branch rebuilt as `[screen, _blank_screen()] if screen else [_blank_screen()]`.
- [x] T009 Green — run `multimedia.web.test_media` (21 → 26 cases) and `multimedia.web.test_obs_dock`.

## Phase 4 — US2: the dock steps and lists the rest (P1)

- [x] T010 Red — `tests/e2e/test_obs_dock.py::ObsDockE2ETests::test_a_media_entry_lists_and_steps_its_rest`:
      a service with an image entry; open the dock, make the media entry live, read its inner rows
      (`IMAGE`, `Rest`), press the forward arrow, assert `gkps-display.screen` is the rest and the
      projector shows `.screen.is-blank`.
- [x] T011 Green — no production change expected (D3); if the case fails, the failure names the seam
      that was missed rather than a rule to invent.

## Phase 5 — US3: nothing else moves (P2)

- [x] T012 Red/Green — `tests/e2e/test_projector.py::ProjectorTests::test_a_media_entry_steps_onto_its_rest`:
      plain `→` from a media screen lands on a blank; `End` on that entry stays on the media screen.
- [x] T013 Green — the media display modules: `tests.e2e.test_image_display`, `test_video_display`,
      `test_pdf_display`, `test_powerpoint_display`, `test_audio_display`; plus `tests.e2e.test_obs_dock`
      and `tests.e2e.test_projector` in full.

## Phase 6 — Polish

- [x] T014 Fold `projector/R11` into `docs/spec/projector.md` (typed delta `added`, header `last folded`
      and the slice ID; `#gkps #projector #spec-164`).
- [x] T015 `VERSION` 1.23.2 → 1.23.3 and one `### Changed` line at the top of `[Unreleased]` in
      `CHANGELOG.md`.
- [ ] T016 Card `ITEM-178` → `done` is a separate `chore/board-177` PR after the merge; this PR leaves it
      *In review* with the PR link.
- [x] T017 Convergence pass over every traceability row (`converge.md`), then the closing report.

## Done when

- [x] Every acceptance scenario in `spec.md` holds by the method it declared
- [x] The named tests are green, and the four rewritten ones were seen red first
- [ ] Fold, version, changelog and board are complete in this PR
