# Tasks: The first sidebar's idle rule, restored and set to fifteen minutes

**Spec**: `specs/199-sidebar-activity/spec.md`
**Plan**: `specs/199-sidebar-activity/plan.md`
**Verification split**: 26 test · 5 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 [P] Confirm the branch and the harness before any edit: `git branch --show-current` reads
  `fix/199-sidebar-activity`, the database answers on 59075 (the sibling compose project owns that
  port; this worktree's `db` service is stopped), and the nine idle E2E baselines were run before the
  constant moved.

## Phase 2 — Foundational

The delay is shared by every story's clocks, so it moves before the new assertions are written; the
seven simple idle tests are rescaled first and go red against the old constant (TDD-01).

- [X] T002 [P] Rescale the seven simple idle tests in `tests/e2e/test_reading.py` to the new span:
  `test_matching_idle_bible_sidebar_collapses_to_mini`, `test_idle_collapsed_bible_sidebar_
  reopens_without_navigating`, `test_rail_activity_restarts_sidebar_idle_timeout`,
  `test_sidebar_timeout_waits_while_filter_has_focus`,
  `test_sidebar_for_other_section_stays_open_when_stage_is_bible`,
  `test_narrow_layout_keeps_matching_sidebar_open` (now on `web-index` with the drawer opened to
  Tata Ibadah: the Bible chapter fixture holds one book and its panel does not overflow, so the
  drawer scroll is real and asserted) and
  `test_matching_idle_tatib_sidebar_closes_without_navigating` — 899 000 + 1 000 where they pin
  both sides, 900 000 where they only advance past it. Red at the old constant.
- [X] T003 Set `IDLE_COLLAPSE_DELAY = 900000` at `static/web/reading.js:64`; leave the 720 px
  `mqNarrow` cut-off and every guard untouched. T002 goes green.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a scroll of the first panel restarts the interval however it was produced, including a
scrollbar-thumb drag, which emits `scroll` and no `wheel`.
**Independent test**: open the Bible panel, wait 30 s, fire `scroll` at its scroller — still open at
899 s, mini at 900 s.

- [X] T004 [P] [US1] Write the failing test `test_panel_scroll_restarts_sidebar_idle_timeout` in
  `tests/e2e/test_reading.py`: `page.clock.install`, load `web-bible-chapter` (Mat 5),
  `run_for(30000)`, assert `#panelBody` really overflows (the suite's baseline shelf is one book, so
  the test adds 40 for its own fixture), then dispatch `new Event('scroll')` at the scroller — the
  non-bubbling event a thumb drag emits. `fast_forward(899000)` → `data-nav="open"`, `run_for(1000)`
  → `mini`. Red when capture is removed (`{ passive: true }` only): the bubble listener on `#panel`
  never sees it. Assigning `scrollTop` instead was tried and retracted: Chromium flushes its own
  `scroll` at an arbitrary frame, which landed inside the fake wait.
- [X] T005 [P] [US1] Write `test_panel_wheel_restarts_sidebar_idle_timeout`: `WheelEvent('wheel',
  { bubbles: true })` on `#panelBody` at 30 s, open at wheel + 899 s, mini at + 900 s. Green before
  the fix — the regression guard for the working path. The event is dispatched directly because a
  real `mouse.wheel` through a faked clock is not repeatable under a loaded suite.
- [X] T006 [US1] Rewrite the activity wiring in `static/web/reading.js`: one `ACTIVITY_EVENTS`
  array with the six names, one `forEach` binding each name to `.rail` and `#panel` with
  `{ capture: true, passive: true }`, `noteSidebarActivity` unchanged, the `focusout` handler kept
  (it now also clears `deferralHeld`). T004 and T005 green; no `document`/`window` activity listener
  added.

## Phase 4 — US2 (P1)

**Goal**: an interaction that holds the collapse gives a full interval at the moment it ends —
before expiry (a short reorder drag) and after it (a drag or dialog that outlived the interval).
**Independent test**: drag a Tata Ibadah grip at 14:00 and release at 14:05; open at release +
899 s, closed at + 900 s.

- [X] T007 [P] [US2] Write the failing test `test_short_drag_restarts_sidebar_idle_timeout` in
  `tests/e2e/test_reading.py`: `web-tatib-service`, `fast_forward(840000)`, grip down, one 12 px
  move, `run_for(5000)`, `mouse.up()`, `fast_forward(899000)` → `open`, `run_for(1000)` → `closed`.
  Added its name to the `self.idle_drag_entry` fixture condition. Red before the observer (the old
  60 s deadline from page load had long passed).
- [X] T008 [P] [US2] Reshape the two existing deferral tests to measure from the end:
  `test_dialog_defers_sidebar_idle_collapse_then_restarts` and
  `test_drag_defers_sidebar_idle_collapse_then_restarts` — hold across `fast_forward(900000)`, end
  it, assert open at 899 000 and collapsed after a short settle. The dialog pin carries 5 s of
  slack because closing a dialog also returns focus to its opener, which restarts again a few fake
  milliseconds after `[open]` goes. Both are guards — the existing 1 s poll already made them pass
  before the fix; `T007` is the row that goes red first.
- [X] T009 [US2] Add the deferral-end restart in `static/web/reading.js`: a module-scope
  `deferralHeld`, set when the observer sees a deferral begin (or the expiry path finds one) and
  cleared with `scheduleIdleCollapse()` when the four conditions are all false; a `MutationObserver`
  on `document.body` (`attributes: true, subtree: true, attributeFilter: ['class', 'open']`); and a
  cleared flag on a `focusout` that leaves the panel. Restart on the condition clearing, never on
  `pointerup`, `dragend`, a click or a `#chapters` listener. The 1 s expiry poll stays as backstop.
  T007 and T008 green.

## Phase 5 — US3 (P2)

**Goal**: the activity surface stays exactly the rail and the first panel; the second sidebar and
the stage restart nothing, and the narrow drawer arms nothing.
**Independent test**: scroll the second sidebar and wheel over the stage at 30 s; the panel
collapses at 900 s all the same.

- [X] T010 [P] [US3] Write `test_second_sidebar_and_stage_activity_does_not_restart_sidebar_idle_
  timeout` in `tests/e2e/test_reading.py`: Bible page, `run_for(30000)`, `#chBody.scrollTop = 240`
  (assert > 0), real `mouse.move(900, 450)` + `wheel(0, 300)` over the stage,
  `fast_forward(869000)` → `open`, `run_for(1000)` → `mini`. Guard: green on both sides, and it
  fails if any listener widens the surface.

## Phase 6 — Polish

- [X] T011 Inspection pass against the declared rows: `grep -n IDLE_COLLAPSE_DELAY
  static/web/reading.js` gives the declaration at `900000` and its one read, with no `60000` left;
  the six names occur once and bind only to `.rail`/`#panel`; the `visibilitychange` pair is
  unchanged; the two `window`/`document` listeners still in the file (results-page scroll snapshot,
  Escape stack) predate the slice and are not activity reporters (FR-007, FR-009, SC-005).
- [X] T012 Full `tests.e2e.test_reading.ReadingE2ETests` — 82 tests, all slice tests green; the one
  red test (`test_the_panel_shows_its_empty_view_when_no_songbook_exists`) reproduces on unmodified
  develop and is tracked as ITEM-137. Fast lane: 642 tests, the same 11 pre-existing failures as
  develop after `collectstatic` (before it, nine environment-only manifest errors appeared). No
  template, CSS, model or view in `git diff --stat`.
- [X] T013 Fold `docs/spec/reading.md`: added `R44` (interval, activity surface, deferral end,
  fifteen minutes) and `R45` (deferral conditions and their end), added 199 to the slices line, and
  recorded `fold.md` (SDD-23).
- [X] T014 `CHANGELOG.md` under `## [Unreleased]` — `Fixed` for the scroll and deferral-end repair,
  `Changed` for the fifteen-minute wait — and `VERSION` 1.33.0 → 1.33.1, in the Fold commit.
- [X] T015 Board and tracker: card moved to `in progress` with its branch and backfilled anchor
  issue; the board row moved out of `Speccing`. `pr:` and `Done` wait for the push that opens the PR
  (C-BOARD-GIT). Nothing pushed without the owner's word.

## Phase 7 — Convergence

**Pass 1** — every traceability row checked by the method it declared; no `missing`, `partial`,
`contradicts` or `unrequested` gap. Two observed consequences recorded: a direct `WheelEvent` and a
non-bubbling `scroll` stand in for the physical gestures (the fake clock cannot drive a real
scrollbar deterministically), and the dialog pin carries five seconds of slack for its focus return.
Suite: 82 reading E2E with one pre-existing red (ITEM-137, reproduced on develop), 642 fast-lane
tests with the same 11 pre-existing failures as develop. Outcome: **converged** — see `converge.md`.
