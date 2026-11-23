# Tasks: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md`
**Plan**: `specs/236-song-modal-scrollbar/plan.md`
**Verification split**: 12 test · 4 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written.
Every `test` row in the plan is a red task and a green task. Inspection rows produce no test task.

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_song_modal_scrollbar.py` with a `StaticLiveServerTestCase`
      fixture: one songbook, one song with verses, one song without verses, one service with a
      song entry, `@tag('e2e')`, `skipUnless` on Playwright and
      `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`.
      Add a page helper at 1366×900 (dark theme) and a `MEASURE` script reading the dialog's
      `clientHeight`, `scrollHeight`, `offsetWidth - clientWidth` and computed `overflow-y`, plus
      the same for `.editor__content`. No assertions yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: the New song dialog has no scrollbar of its own.
**Independent test**: click **+ Song** on a service and read a 0px gutter with `overflow-y: clip`.

- [X] T002 [P] [US1] Write failing E2E tests for US1/AC1, US1/AC2, US1/AC3, FR-001 and SC-001:
      `test_new_song_dialog_has_no_scrollbar_gutter` (0px gutter, computed `overflow-y: clip`),
      `test_new_song_wheel_does_not_scroll_the_dialog` (wheel and a scripted `scrollTop` write leave
      the dialog at 0), and `test_new_song_results_menu_still_escapes_the_dialog` (typing opens
      the fixed menu past the dialog bottom, the dialog box is unchanged). Confirm the gutter test
      is red on the base at 5px.
- [X] T003 [US1] Add `overflow: clip` to the shared `.editor` rule in
      `static/styles/design/components.css`, with a comment naming why the dialog is not the
      scrollport; touch no other declaration.
- [X] T004 [US1] Make the T002 tests green; confirm the song results menu still paints outside the
      dialog and the dialog keeps its 480px width and 14px radius.

## Phase 3 — US2 (P1)

**Goal**: the Edit song dialog has no scrollbar in the collapsed and settled states.
**Independent test**: edit an empty-song entry, then a song with verses, read 0px gutter in both.

- [X] T005 [P] [US2] Write failing E2E tests for US2/AC1, US2/AC2 and SC-002:
      `test_edit_song_collapsed_verses_has_no_scrollbar` (song with no verses; spec 235 empty-summary state,
      gutter 0px, wheel does nothing) and `test_edit_song_with_verses_keeps_its_box` (song with
      verses; 410/410px, gutter 0px). Run them red.
- [X] T006 [US2] Make the T005 tests green with the same one-line rule; add no per-mode CSS and no
      template branch.

## Phase 4 — US3 (P2)

**Goal**: tall forms keep their own inner scrolling and other editors are unaffected.
**Independent test**: open a large text editor and a short-viewport form; the content scrolls.

- [X] T007 [P] [US3] Write failing E2E tests for US3/AC1, US3/AC2, FR-003 and SC-003:
      `test_large_form_scrolls_inside_content` (a `data-editor-size="large"` form; inner
      `scrollTop` changes under wheel, dialog `scrollTop` stays 0) and
      `test_short_viewport_scrolls_inside_content` (viewport 900×600 so the `86vh` cap engages;
      same assertion). Run them red.
- [X] T008 [US3] Make the T007 tests green without editing `.editor__content`; record the measured
      inner and outer scroll values.

## Phase 5 — Polish

- [X] T009 Record the four inspection rows in `analysis.md` and `converge.md`: FR-002 (computed
      `overflow-y: clip`, no thumb; `scrollHeight` may stay 256px), FR-004 (one-line diff, 480px
      box, 14px radius, panel animation, fixed menu), SC-004 (preview readouts before
      `246/256px, 5px`, after `246/256px, 0px`; edit `410/410px`), US3/AC3 (date popover is
      top-layer and unaffected).
- [X] T010 Rebuild and re-verify the self-contained preview with the chat-frame script before any
      `::preview` use; report PASS/FAIL.
- [X] T011 Open `ITEM-251` from the board's Backlog into `Speccing` with
      `spec: 236-song-modal-scrollbar` and `branch: fix/236-song-modal-scrollbar`, and add its row
      to `backlog/board.md`. Do not promote it to `Ready` — that is the owner's gate-1 act.
- [X] T012 Run only the targeted E2E module between pushes; leave the full browser suite to the
      push step and report the numbers.
- [X] T013 Re-check the next spec number, card ID, `R58` and the patch level against `develop` and
      every unmerged branch before delivery.
- [X] T014 At delivery only, after Converge: write the `VERSION` bump, the `## [Unreleased]`
      changelog line, the `backlog/board.md` `In review`/`Done` moves and the `reading.md` R58 fold.

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->
