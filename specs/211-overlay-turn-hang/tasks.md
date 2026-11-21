# Tasks: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Plan**: `specs/211-overlay-turn-hang/plan.md`
**Verification split**: 17 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Verify the worktree is on `feat/211-overlay-turn-hang` at base `7a0e7069`, that slice
  211 and ITEM-223 are free, and that no ignore rule is needed; the preview writes no files.
- [X] T002 Re-read `static/web/obs-overlay.js:118-137, 222-229, 272-306`,
  `static/styles/design/obs-overlay.css:101-109, 202-214` and
  `multimedia/web/reading/views.py:1579-1613` immediately before editing; record the exact lines
  in the convergence note.

## Phase 2 — Foundational

- [X] T003 Add five small TEXT fixtures to `tests/e2e/test_obs_overlay.py::setUp` (after the three
  existing entries): a two-line leader turn; a three-line single-screen turn with a new `J.`
  answer; a two-line turn whose continuation wraps; a four-line turn whose second screen has no
  mark; and a cue followed by ordinary lines and a separate ordinary body. Add one helper that
  opens the nth `.screenerow`, leaving existing screen indices untouched (D004, FR-001–FR-006).

## Phase 3 — US1 (P1) 🎯 MVP — the turn reads as one block

**Goal**: the continuation's first glyph lands on the marked line's words x, with its voice intact.
**Independent test**: project the two-line leader turn at 1280×720 and compare the two glyph x
values; no ink passes the plate.

- [X] T004 [P] [US1] Write a failing
  `tests/e2e/test_obs_overlay.py::test_a_continuation_hangs_at_the_marked_words`: first glyph x of
  the continuation equals the marked words x within 1 px, the row has no `.obs-overlay__speaker`,
  and it keeps `is-leader` and the leader colour (FR-001, FR-002, FR-005, SC-001, US1/AC1, AC2).
- [X] T005 [P] [US1] Write a failing `...::test_the_widest_mark_sets_the_continuation_column`:
  the continuation, the `L.` words and the later `J.` words share one x sized by the widest mark
  (US1/AC3).
- [X] T006 [P] [US1] Write a failing
  `...::test_a_wrapped_continuation_keeps_every_row_at_the_words_column`: every glyph rect of the
  long continuation shares the words x and its right ink edge stays inside the plate's content box
  (FR-006, SC-002).
- [X] T007 [US1] In `plate()` (`static/web/obs-overlay.js:118-137`) compute one screen-wide
  `hasPaintMark` from `line.mark && line.words`, and add `is-continuation` to a row only when the
  line has no mark, has a voice, and that flag is true; leave row text and voice classes untouched
  (FR-001, FR-003, D001).
- [X] T008 [US1] In `static/styles/design/obs-overlay.css`, beside `.has-mark`, add one
  `.obs-overlay__line.is-continuation { padding-left: calc(var(--speaker-col, 0px) + .45em); }`
  rule; do not touch the grid, the variable measurement or any colour (FR-002, FR-006, D002).
- [X] T009 [US1] Re-run T004–T006 green and read the assertions back; a pass on an import or a
  timeout does not count (TDD-02).

## Phase 4 — US2 (P2) — only a real turn moves

**Goal**: a screen with no mark, a cue and an ordinary body keep today's layout.
**Independent test**: project the second screen of the four-line turn, then the cue fixture; every
line stays at the plate's content edge with no continuation class.

- [X] T010 [P] [US2] Write a failing `...::test_a_no_mark_screen_keeps_its_continuations_flush`:
  the mid-turn screen has no `.has-mark`, paints no column and keeps its lines at the content edge
  (FR-003, SC-003, US2/AC1).
- [X] T011 [P] [US2] Write a failing `...::test_a_cue_and_an_ordinary_body_stay_flush`: the cue
  line, its neighbour and the lines of the speakerless body stay flush with their ink (FR-004,
  US2/AC2, AC3).
- [X] T012 [US2] Verify both guards in T007 are needed and sufficient; run T010–T011 green without
  a second indent mechanism or a server-side change (D003).

## Phase 5 — Polish and verification

- [X] T013 [P] Re-run the two existing overlay cases named in SC-004 —
  `test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines` and
  `test_a_wrapped_speaker_line_hangs_under_its_words` — then the whole `test_obs_overlay` module;
  leave the tree alone until the run returns and record the counts.
- [X] T014 [P] Inspect the gate-1 preview at `specs/211-overlay-turn-hang/preview/index.html`: the
  readout still shows −28.8 px before / 0.0 px after at 1280×720 and the no-mark tab stays flush
  (UI/UX inspection row).
- [X] T015 Converge against the plan's traceability table: type every gap `missing` · `partial` ·
  `contradicts` · `unrequested`, mark each inspection row `checked by inspection`, append
  `converge.md`, at most three passes.
- [X] T016 Fold the typed delta for `overlay/R5` into `docs/spec/overlay.md`, keep its existing
  scenarios, write `fold.md`, and move `last folded` to the fold date with the slice id prepended
  (SDD-23).

## Phase 6 — Delivery (after Converge)

- [X] T017 Commit at Fold — spec pack, code, E2E changes, capability delta and board row together,
  only with the focused suite green (GIT-06).
- [X] T018 Stamp `VERSION` 1.35.1 → 1.35.2 and add the `## [Unreleased]` `### Fixed` line; keep
  ITEM-224 on the board as the separate token-alone fix (VER-04/07).
- [X] T019 Promote ITEM-223 in-review with the PR number and move its board row **only on the
  owner's word**; open the PR as a draft. Do not push, mark ready or close the card without that
  word (GIT-07).
- [X] T020 Report what shipped, the verification split, convergence and gaps, the folded
  capability, branch and commit count, version/changelog line, PR title and body, and that nothing
  is pushed — then ask about pushing (SDD-27).

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
