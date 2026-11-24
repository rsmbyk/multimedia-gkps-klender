# Tasks: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`
**Plan**: `specs/239-media-filter-pill-hover/plan.md`
**Verification split**: 9 test · 5 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written.
Every `test` row in the plan is a red task and a green task. Inspection rows produce no
test task. The CSS edit was applied before gate 1 for the live preview (recorded in the
spec's Assumptions); it stays uncommitted, and red tasks temporarily remove only that
rule from `components.css` before restoring it.

## Phase 1 — Setup

- [X] T001 Create `tests/e2e/test_media_filter_pill_hover.py` with a `StaticLiveServerTestCase`
      fixture: `@tag('e2e')`, `skipUnless` on Playwright, and
      `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`.
      Add a 1440 × 900 page helper, a `SNAP` script reading computed `background`, `border`,
      `color` and box for `[data-media-type="image"]`, and a helper that points at any of
      the six pills. No assertions yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: an unpressed pill takes the app's control-hover pair on pointer hover.
**Independent test**: real hover on all six pills changes border and fill in both themes.

- [X] T002 [P] [US1] Write failing tests for US1/AC1, FR-001 and SC-001:
      `test_all_unpressed_pills_take_the_hover_pair` — each of the six unpressed pills
      takes `rgba(31,31,29,.08)` / `rgb(28,92,60)` in light and `rgba(255,255,255,.09)` /
      `rgb(124,156,240)` in dark. Temporarily remove the spec-239 rule from `components.css`,
      confirm red with rest values, then restore the file.
- [X] T003 [US1] Keep the gate-1 edit in `static/styles/design/components.css`: one rule
      `.media-library__chips button:not([aria-pressed="true"]):hover` with only
      `border-color: var(--focus); background: var(--icon-hover-bg);`. Touch no other
      declaration.
- [X] T004 [US1] Make T002 green with that rule; confirm the shipped selector is readable
      from the same-origin stylesheet rather than relying on a media-query override.
- [X] T005 [P] [US1] Write a failing test for US1/AC2:
      `test_pointer_leave_restores_rest_colours` — after moving the pointer away, background
      is `rgba(0, 0, 0, 0)` and border is `rgb(217,214,205)` light / `rgb(58,54,47)` dark.
      Run red with the rule removed, then restore.
- [X] T006 [US1] Make T005 green without adding a transition or an exit rule.
- [X] T007 [P] [US1] Write a failing test for US1/AC3:
      `test_hover_keeps_box_and_label` — 63.36 × 30 px and label `rgb(31,31,29)` /
      `rgb(245,243,238)` before and under hover. Run red only if a geometry declaration
      leaked into the rule; otherwise record the base failure with the rule removed.
- [X] T008 [US1] Make T007 green using the same two declarations; no padding, border-width
      or colour change on the label.

## Phase 3 — US2 (P2)

**Goal**: hover cannot muddy the selected state, keyboard focus or the row's geometry.
**Independent test**: a clicked pill reads the same colours hovered and at rest.

- [X] T009 [P] [US2] Write failing tests for US2/AC1, FR-002 and SC-002:
      `test_pressed_pill_keeps_its_accent_fill` — after clicking Images, rest and hover
      agree at `rgb(28,92,60)` fill/border and `rgb(255,255,255)` text. Run red with the
      guard removed from the selector (bare `:hover`), then restore the guard.
- [X] T010 [US2] Make T009 green with the `:not([aria-pressed="true"])` guard; leave the
      existing pressed rule untouched.
- [X] T011 [P] [US2] Write a failing test for US2/AC2:
      `test_keyboard_focus_keeps_its_outline` — Tab to a pill and read the focus-visible
      outline as 2px `--focus` with 2px offset; do not fabricate focus with a class or a
      style injection. Record the checklist `[Gap]` disposition in `analysis.md`.
- [X] T012 [US2] Make T011 green without adding a new focus rule.

## Phase 4 — Inspection rows

- [X] T013 [P] [US2] Record US2/AC3 and SC-003 by inspection: the gate-1 probe's
      63.36 × 30 px readout is identical at rest, hover and pressed, and no gap or padding
      declaration changed.
- [X] T014 [P] [FR] Record FR-003 and FR-004 by inspection: `git diff` shows one file,
      one rule, two declarations; the template, `media-library.js`, the dot span and the
      sort/icon-button rules are unchanged.
- [X] T015 [P] [SC] Record SC-004 by inspection: `preview/probe.py` light and dark hover
      values agree with `spec.md §UI/UX` after the rule is shipped.

## Phase 5 — Polish

- [X] T016 Hard-reload the live page and re-run `preview/probe.py`; confirm the frozen
      before/after numbers from gate 1 still hold.
- [X] T017 Run only `tests.e2e.test_media_filter_pill_hover` between pushes; leave the
      full browser suite to the push step and report what the narrower run proves.
- [X] T018 Re-check the next spec number, `ITEM-254`, `media-library/R6` and the patch
      level against `develop` and every unmerged branch before delivery.
- [ ] T019 At delivery only, after Converge and on your word: write the `VERSION` bump,
      the `## [Unreleased]` changelog line, the `backlog/board.md` `In review`/`Done` moves,
      and the `media-library.md` R6 Fold.

## Phase 6 — Convergence

- Pass 1 (`converge.md`): all 14 traceability rows met by their declared method; 0 gaps.
  New E2E module 5/5 green after red-on-base runs. Converged. T019 stays open for the
  delivery step and is not claimed here.
