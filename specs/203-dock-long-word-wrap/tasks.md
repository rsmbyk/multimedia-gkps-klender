# Tasks: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`
**Plan**: `specs/203-dock-long-word-wrap/plan.md`
**Verification split**: 21 test · 1 inspection · 1 manual

Sequence note (research D007): T001–T014 landed during Preview, before gate 1, on the owner's correction
that the preview did not show the change. Red-first was kept inside that — T002–T005 were run and failed
before T006 landed. The gate order is what was skipped, not the evidence.

## Phase 1 — Setup

- [X] T001 [P] Create `tests/e2e/test_dock_text_wrap.py` — a `StaticLiveServerTestCase` with Playwright, its
  fixtures three dated services (the 64-character name with a URL entry, two short filenames, a hyphenated
  filename, a 200-character filename and an ordinary-songbook song; a short-named service; a service whose
  first entry is a twelve-verse song followed by a URL entry), and helpers `open_runner`, `at`, `measure`,
  `runner`, `restore_rule` and `project_first`. Measurement is spec 137's range-rect spill.

## Phase 2 — Foundational

None: the slice is one stylesheet and one test module, and no shared prerequisite sits between the stories.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: an unbroken run wraps inside the box that owns it, and the runner body stops scrolling sideways.
**Independent test**: open the dock on the 64-character service at a narrow panel; no painted text sits past
its own box and the body has no horizontal scrollbar.

- [X] T002 [P] [US1] Write the failing test `test_an_unbroken_service_name_wraps_inside_its_column` — red on
  the shipped stylesheet: spill 464px at 320px, 328px at 456px, one line.
- [X] T003 [P] [US1] Write the failing test `test_an_unbroken_entry_header_wraps_inside_its_row` — red:
  spill 314px at 320px on the URL header, 2064px on the 200-character filename.
- [X] T004 [P] [US1] Write the failing test `test_a_screen_row_wraps_inside_the_open_block` — red: spill
  243px at 320px on the URL screen row.
- [X] T005 [P] [US1] Write the failing test `test_the_runner_body_does_not_scroll_sideways` — red:
  `#runBody` scroll − client 2021px at 320px, 135px at 456px.
- [X] T006 [US1] Make T002–T005 pass in `static/styles/design/obs-dock.css`: `overflow-wrap: anywhere` on
  `.serviceline`, `.entryrow__t` and `.screenerow`, each with the comment that names the mechanism (research
  D001–D004). All four go green; the run is logged.

## Phase 4 — US2 (P2)

**Goal**: text that already fits renders exactly as before, and the row's own geometry does not move.
**Independent test**: read the same page twice — rule shipped, then its value restored to `normal` — and
every fitting box is equal.

- [X] T007 [P] [US2] Write `test_text_that_fits_is_unchanged` — a no-change claim, green before and after
  T006 by design; it skips any box that overflows in either read.
- [X] T008 [P] [US2] Write `test_a_short_service_is_unchanged` — the short-named service at 320/456/900,
  title and every row equal in both reads.
- [X] T009 [P] [US2] Write `test_the_row_keeps_its_number_and_chevron` — number widths and every visible
  chevron's offRight/offCentre equal in both reads.
- [X] T010 [P] [US2] Write `test_a_wide_panel_renders_as_it_does_today` — at 900px the name fits and is
  unchanged; a run wider than the panel still wraps, and the body does not scroll sideways.
- [X] T011 [US2] Confirm no further stylesheet change is needed — the three declarations already leave every
  fitting box alone; no clamp is added (research D003).

## Phase 5 — US3 (P3)

**Goal**: what declares its own cut keeps truncating, and the picker keeps wrapping as it does today.
**Independent test**: a tall live block draws the NEXT band; its label stays one line ending `…`.

- [X] T012 [P] [US3] Write `test_a_truncating_label_still_truncates` — `nowrap`, `ellipsis`, one line, still
  clipped. Needed the twelve-verse fixture: the band is hidden while the live entry's own end is in view.
- [X] T013 [P] [US3] Write `test_the_picker_name_still_wraps` — `.servicerow__n` computes `anywhere`, spill
  ≤ 1, more than one line.
- [X] T014 [US3] Confirm no rule is added to `.nextband__label` or `.offstrip__label` — a `nowrap` line
  cannot wrap whatever it inherits (research D004).

## Phase 6 — Polish

- [X] T015 Run the dock's own suites for regression: `tests.e2e.test_obs_dock`, `test_obs_dock_follow`,
  `test_dock_bucket_head`, `test_dock_goto`, `test_dock_keys` — 66 tests, all green.
- [X] T016 Write the board row's `pr:` and move the card to `In review` once the PR exists — PR #541,
  card `pr: 541`, row moved to In review (oldest first, behind ITEM-211).
- [X] T017 `CHANGELOG.md` under `## [Unreleased]` (Fixed) and `VERSION` 1.34.2 → 1.34.3, in the delivery
  commit. Re-stamped from `origin/develop` at Fold: spec 202 (PR #539) took 1.34.2 while this slice waited
  at gate 2, so the plan's 1.34.2 is superseded.
- [X] T018 Fold `docs/spec/dock.md` R16 (added) and record `fold.md`.

## Phase 7 — Convergence

**Pass 1** — every traceability row checked by its declared method; no missing, partial, contradicts or
unrequested gap. Suite re-run at the pass: 10 green; the five neighbouring dock suites 66 green. Two
delivery notes recorded (the base moved to `85319b73`, so the bump re-stamps 1.34.3; spec 202 took
ITEM-212, so this card renumbered to ITEM-213 with anchor #540 kept). Outcome: **converged** — see
`converge.md`.
