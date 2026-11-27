# Tasks: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md`
**Plan**: `specs/240-entry-modal-title/plan.md`
**Verification split**: 10 test · 4 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written.
Every `test` row in the plan is a red task and a green task. Inspection rows produce no
test task. The CSS edit was applied before gate 1 for the live preview (recorded in the
spec's Assumptions); it stays uncommitted, and the red tasks run with that edit
temporarily removed under a shell trap that restores it.

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_entry_modal_title.py` with a `StaticLiveServerTestCase`
      fixture: one service holding a modern text row (pk via ORM), plus empty-service
      routing for `+ Text` and `+ Media`. Use `@tag('e2e')`, `skipUnless` on Playwright and
      `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`.
      Add a 1440×900 page helper and a `MEASURE` script that reads the title text box via
      `Range`, its padding/border and the frame box. No assertions yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: the large entry dialogs show R10's title band again.
**Independent test**: text 26/21px from the dialog, band 72.5px, one 1px rule.

- [X] T002 [P] [US1] Write failing tests for US1/AC1, FR-001 and SC-001:
      `test_large_entry_titles_have_the_band` (New text, New media and text Edit in one
      module). Run red with the gate-1 CSS edit temporarily removed: text 0/1px,
      padding `0px`, border `0px`, band 31.5px. Restore the file.
- [X] T003 [US1] Keep the gate-1 edit in `static/styles/design/components.css`: the
      headerless-large selector restoring `padding: 20px 26px` and the 1px divider, plus
      its narrow override. Touch no other declaration.
- [X] T004 [US1] Make T002 green; record US1/AC2 by inspection — frame stays 840×760,
      first field y 133.5 → 174.5px, action row and field width unchanged, using the
      probe and the existing `test_entry_modal_frame` module.

## Phase 3 — US2 (P2)

**Goal**: spec 226's verse header and every compact form stay as they are.
**Independent test**: head padding `20px 26px 14px`, title padding/border `0px`, one rule.

- [X] T005 [P] [US2] Write failing tests for FR-003 and SC-002:
      `test_verse_header_still_has_one_rule` (new and Edit verse), or reuse
      `tests/e2e/test_verse_modal_header.py` cases if they already pin the numbers;
      run them green on the fixed tree and confirm they were green on the base too
      (characterisation — no honest red for behaviour that must not change).
- [X] T006 [US2] Record US2/AC2 and FR-004 by inspection: passage, song, media Edit and
      old-item titles keep the compact 480px dialog with their divided title; no
      template, script, sr-only title or loading-state rule changed; the diff is one CSS
      file only.

## Phase 4 — US3 (P2)

**Goal**: the narrow frame uses R10's smaller band.
**Independent test**: text 18/17px, band 64.5px, divider 1px at 390×844.

- [X] T007 [P] [US3] Write a failing test for US3/AC1, FR-002 and SC-003:
      `test_narrow_title_keeps_small_gutters` at 390×844. Run red with the CSS edit
      removed, then green with it restored.
- [X] T008 [US3] Record US3/AC2 by inspection from `preview/probe.py`: before/after
      numbers at 1440 and 390px in dark theme, frame 352×760, no page scrollbar.

## Phase 5 — Polish

- [X] T009 [P] Run the existing `tests.e2e.test_entry_modal_frame` module; its
      `test_new_text_dialog_matches_new_media` was red on the base with
      `'0px' != '20px 26px'` and must now be green. This covers SC-004's frame half.
- [X] T010 [P] Run `tests.e2e.test_verse_modal_header`; all cases green, covering
      SC-004's header half. Leave the full browser suite to the push step and report it.
- [X] T011 Hard-reload the live page after collectstatic and re-run `preview/probe.py`;
      confirm the frozen before/after numbers (26/21px and 18/17px text, 72.5/64.5px band).
- [X] T012 Re-check the next spec number, `ITEM-255`, `reading/R10`, `1.36.26` and the
      base commit against `origin/develop` and every unmerged branch before delivery.
- [X] T013 At delivery only, after Converge and on your word: write the `VERSION` bump,
      the `## [Unreleased]` changelog line, the `backlog/board.md` `In review`/`Done`
      moves and the R10 modification in `docs/spec/reading.md`.

## Phase 6 — Convergence

- [X] T014 Compare code against all 14 traceability rows by their declared method,
      append `## Pass 1: Convergence` to `converge.md`, and stop at zero gaps.
