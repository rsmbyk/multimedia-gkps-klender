# Tasks: A passage cue carries its current and end verse

**Spec**: `specs/229-cue-verse-counter/spec.md`
**Plan**: `specs/229-cue-verse-counter/plan.md`
**Verification split**: 20 test · 3 inspection · 0 manual

## Phase 1 — Setup

None — the worktree, branch, spec pack and preview already exist.

## Phase 2 — Foundational

- [X] T001 Write a failing unit test in `multimedia/web/tests.py::ServiceProjectorTests` for the
      scripture screen's `verse` and the entry's `verse_start`/`verse_end`; add the fields in
      `multimedia/web/reading/views.py` (`_scripture_screens()` and the scripture branch of
      `_projector_data()`) until it passes. [FR-001]

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a service passage's cue shows `current/end` after the reference.
**Independent test**: open a projector on a `Matius 5:3-5` service, step the three verses and read
`.cue-verse`; a song cue carries no such span.

- [X] T002 [P] [US1] Write the failing E2E
      `tests/e2e/test_projector.py::ProjectorE2ETests::test_the_service_passage_cue_counts_the_current_and_end_verse`:
      a service with verses 3–5, read `3/5`, step twice, assert `4/5` then `5/5` and an unchanged
      `Matius 5:3-5` reference. [FR-002, FR-003, SC-001, US1/AC1, US1/AC2]
- [X] T003 [P] [US1] Write the failing E2E
      `ProjectorE2ETests::test_a_single_verse_passage_counts_one_of_one` for the existing `Matius 5:3`
      entry, asserting `3/3`. [FR-006, US1/AC3]
- [X] T004 [P] [US1] Write the failing E2E
      `ProjectorE2ETests::test_non_scripture_cues_carry_no_verse_counter`: step to a song and a text
      entry and assert `.cue-verse` count 0. [FR-006, US1/AC5]
- [X] T005 [US1] Implement the counter in `static/web/projector.js` `renderCue()`: build `n/n` from
      `screenData[current].verse` and `entry.verse_end`, and append a `<span class="cue-verse">`
      inside the label between the reference's dot and the flip, for passage entries only. [FR-002,
      FR-003, FR-006]

## Phase 4 — US2 (P2)

**Goal**: a passage Go To's cue counts the verse against the loaded chapter.
**Independent test**: open a chapter Go To, step a verse and cross into another chapter; read the
counter before and after.

- [X] T006 [P] [US2] Write the failing E2E
      `tests/e2e/test_goto_shared_state.py::GotoSharedStateE2ETests::test_the_go_to_cue_counts_the_verse_and_the_chapter_length`:
      assert `1/3`, step to `2/3` and `3/3`, flip the edition and assert the counter is unchanged,
      then add a second chapter and cross into it and assert the end number follows it. [FR-004,
      FR-005, SC-002, US2/AC1, US2/AC2, US2/AC3]
- [X] T007 [US2] Implement the counter in `static/web/projector.js` `renderDetourCue()`: derive the
      last verse from `detour.editions[translation]` (TB then first edition as fallback), append the
      same span inside the Go To label, and print nothing when the chapter has no verses. [FR-004,
      FR-005, FR-006]

## Phase 5 — Polish

- [X] T008 Run the cue geometry and flip tests in `tests/e2e/test_projector.py` and the Go To suites;
      confirm no CSS, token, state or endpoint changed and record the results. [FR-007, SC-003,
      SC-004, US1/AC4, US2/AC4]
- [X] T009 Fold `docs/spec/projector.md` as `R16`; write `converge.md` and `fold.md` with the
      typed delta and the measured read-back.

## Phase 6 — Delivery (owner's word only)

- [X] T010 Close `ITEM-244` and record the PR in its card and the board row; apply `bump: patch`
      (VERSION and the `## [Unreleased]` line) in the pre-merge commit.
