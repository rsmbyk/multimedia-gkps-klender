# Tasks: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md`
**Plan**: `specs/200-dock-centre-triggers/plan.md`
**Verification split**: `60 test · 5 inspection · 4 manual`

The 60 `test` traceability rows share the 14 E2E methods named below. Each test-first pair covers
every row mapped to that method in `plan.md`; no `test` row is left without a task. `[P]` means
order-independent, not concurrent — one agent in one thread will run them in the order written.

## Phase 1 — Setup

- [ ] T001 Verify the ignore files already cover `specs/*/preview/shots/` and that the worktree is
  on `feat/200-dock-centre-triggers` at `16a7da8a`; no new ignore rule is needed (`plan.md`
  Project Structure).
- [ ] T002 Create `tests/e2e/test_obs_dock_follow.py` with the `StaticLiveServerTestCase` shell,
  the fixture services/entries copied from the repo's existing dock suites, and the
  `StaticFilesStorage` override; the module must import and run zero tests green before any new
  test is added.

## Phase 2 — Foundational

- [ ] T003 [P] Add the page-memory `following = true` flag and the previous-notice snapshot to
  `static/web/obs-dock.js` (`dock`/module scope); no behaviour change yet — `sync()` still centres
  as today (D001/D002).
- [ ] T004 [P] Give `startMorph` its `carry` argument and thread it through `morphState` and
  `finishMorph()` so the height-only path never reaches `centerRow()`; default to today's behaviour
  until a caller passes false (D003).
- [ ] T005 [P] Add the idle interval, `lastActivity`, `holding` and the five document listeners;
  leave the fire branch as a no-op until US3 (D004).

## Phase 3 — US1 (P1) 🎯 MVP — the control

**Goal**: an operator can ask for the live row back with one control between Previous and Next.
**Independent test**: scroll the live entry out of view, press the crosshair, see the list glide to
the live row and the next advance follow without another press.

- [ ] T006 [P] [US1] Write a failing `::test_the_centre_control_centres_and_enters_following` —
  control placement, 190 ms landing within 1 px, no display write, re-entry (FR-002, US1/AC1–2/6).
- [ ] T007 [P] [US1] Write a failing
  `::test_the_control_is_disabled_without_a_live_row_and_centres_a_goto` — disabled with nothing
  live, go-to marked row centred (FR-003, US1/AC4–5, D009).
- [ ] T008 [US1] Add `#centreBtn` to `.navpair` in `multimedia/web/templates/reading/obs_dock.html`
  with the crosshair SVG, `tabindex="-1"`, title/aria-label; wire its click to `centre()` +
  `following = true`, paint `disabled` in `sync()`, and extend `liveNode()` to the off-body go-to
  row (D009). No CSS file changes (D008).
- [ ] T009 [P] [US1] Write a failing `::test_reduced_motion_jumps_instead_of_gliding` with a reduced
  motion context (FR-002, SC-005, US1/AC3).
- [ ] T010 [US1] Route all centring paths through the existing `reduceMotion.matches` instant branch;
  no new duration or easing is introduced.

## Phase 4 — US2 (P1) — items and the Next band

**Goal**: clicking what is inside an entry centres it and puts the dock back into following;
the sticky Next band also moves the pointer to the next entry.
**Independent test**: from browsing, click a screen row, then click the band, and watch both centre
with the band moving the live mark to the next entry's first row.

- [ ] T011 [P] [US2] Write a failing `::test_an_item_click_centres_and_reenters_following` — same
  entry, crossing entry, no-centre on a header (FR-004, US2/AC1–3/6).
- [ ] T012 [P] [US2] Write a failing
  `::test_the_next_band_jumps_the_pointer_and_reenters_following` — `data-live` advances by one
  entry, first row carries `aria-current`, row centred, following restored (FR-004, US2/AC4).
- [ ] T013 [US2] Add `following = true` and `snapBlocks()` to the `entryList` item/band click path;
  keep `projectScreen(Number(nextBand.dataset.screen))` as the band's projection (D006, D003).

## Phase 5 — US3 (P2) — the idle return

**Goal**: a quiet dock brings a lost live entry back after 15 s, then follows again.
**Independent test**: display on, service open here, live row off screen, nothing else open; stop
touching the dock for 15 s and see the row glide back.

- [ ] T014 [P] [US3] Write a failing `::test_the_idle_elapse_centres_and_reenters_following` — the
  full all-true case and the re-entry (FR-007, SC-003, US3/AC1/11).
- [ ] T015 [P] [US3] Write a failing `::test_each_idle_condition_holds_the_centring_back` — each of
  the six conditions false in turn, plus hidden/re-shown page (FR-008/009, US3/AC2–6/10).
- [ ] T016 [P] [US3] Write a failing
  `::test_the_clock_counts_scrolls_presses_and_keys_but_not_pointer_movement` — wheel and click
  restart, pointer movement does not and the elapse still centres (FR-007, SC-006, US3/AC7–8).
- [ ] T017 [P] [US3] Write a failing `::test_a_held_press_suspends_the_clock` — pointer held past
  the threshold holds the clock at full and the list still; release restarts (US3/AC9).
- [ ] T018 [US3] Implement the fire branch: re-read all six conditions in the firing tick, glide when
  they all hold, set `following = true`, restart the count; guard `visibilitychange` (D004).

## Phase 6 — US4 (P1) — following vs browsing

**Goal**: advances follow while following, and leave the list alone while browsing; the transport
buttons never change the mode.
**Independent test**: advance three times (centres), scroll, advance (does not), press the centre
control, advance (centres again).

- [ ] T019 [P] [US4] Write a failing
  `::test_advances_follow_when_following_and_not_when_browsing` — arrows, keys, chips, transport,
  crossing, open blocks and hidden words in both modes (FR-006, SC-002/007, US4/AC1–3/7).
- [ ] T020 [P] [US4] Write a failing
  `::test_scrolling_and_expanding_another_entry_end_following` — the two exits, neither centring
  itself (FR-012, US4/AC4/8, US2/AC5).
- [ ] T021 [P] [US4] Write a failing `::test_other_state_notices_never_centre` — display switch,
  re-read, reload, service open, go-to rows and layer close (FR-014, US4/AC7).
- [ ] T022 [P] [US4] Write a failing
  `::test_the_dock_does_not_follow_a_service_it_is_not_showing` — picker, other service, go to
  (FR-013, US4/AC6).
- [ ] T023 [US4] Implement D002's notice discriminator in `sync()`, D005's two exits, and pass
  `carry = following` into `startMorph()`; leave `cancelPendingCenter` mode-neutral (D007).

## Phase 7 — Motion and geometry

- [ ] T024 [P] Write a failing `::test_centring_stays_one_motion_and_clamps_at_the_ends` — no
  reversal, no visible move when already centred, clamp at both list ends (SC-004, FR-010).
- [ ] T025 Keep the one-motion and clamp rules intact while implementing T019–T024: no change to
  `layoutTop`, `overflow-anchor`, the same-frame scroll clamp or the 190/230 ms durations; the
  crossing's `carry` is the only new branch (D008, SC-004).

## Phase 8 — Polish and verification

- [ ] T026 Inspection I1 — read `obs_dock.html` and `obs-dock.css`: one `#centreBtn` between prev
  and next, `navbtn` face, `tabindex="-1"`, stroked crosshair `viewBox="0 0 20 20"` stroke 1.8,
  no new CSS rule; compare box numbers with the gate-1 preview (FR-001, SC-001).
- [ ] T027 Inspection I2 — read `static/web/display.js`: no new field, verb or channel message;
  the stored record shape is byte-identical (D001, contracts: none).
- [ ] T028 Inspection I3 — read `obs-dock.js`: no `localStorage` write or `postMessage` for the
  mode, and `following` is not read by any other surface (D001).
- [ ] T029 Manual M1–M3 in `quickstart.md`: feel of the glide/crossing, dark-mode focus fill, and
  the real 15 s wait.
- [ ] T030 Run every new test red against `16a7da8a` (`develop`) before its implementation task
  lands; record any test that fails on an import instead of the behaviour (SC-006, TDD-02).
- [ ] T031 Converge against `plan.md`'s traceability table: type every gap `missing` · `partial` ·
  `contradicts` · `unrequested`, append `converge.md`, at most three passes.
- [ ] T032 Fold the typed delta for `dock/R15` into `docs/spec/dock.md`, write `fold.md`, and move
  `last folded` to the fold date with the slice ID prepended (SDD-23).

## Phase 9 — Delivery (after Converge)

- [ ] T033 Commit at Fold — spec pack, code, E2E suite, capability delta and board row together,
  only with the focused suites green (GIT-06, C-TDD-GIT).
- [ ] T034 Stamp `VERSION` 1.33.0 → 1.34.0 and add the `## [Unreleased]` `### Added` line naming
  the operator control and the following mode, immediately before the merge (VER-04/07, VER-10).
- [ ] T035 Set ITEM-210 to `in-review` with the PR number and move its board row, then open the PR
  **as a draft**; do not push, mark ready, or close the card without the owner's word (GIT-07,
  C-BOARD-GIT).
- [ ] T036 Report: shipped behaviour, verification split, convergence and gaps, capability folded,
  branch and commit count, version/changelog line, PR title and body, and the statement that
  nothing is pushed — then ask about pushing (SDD-27).

## Phase 10 — Convergence

<!-- written by Converge only; absent until it runs -->
