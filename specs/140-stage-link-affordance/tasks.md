# Tasks: The stage's entry links read as text until hovered

**Slice**: `specs/140-stage-link-affordance` · **Branch**: `feat/140-stage-link-affordance`
**Order used**: T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009.
`[P]` marks order-independent work, not concurrency: one agent, one thread.
**Verification split**: 13 test · 4 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Run the test this slice retires as a baseline,
  `tests.e2e.test_reading.ReadingE2ETests.test_tatib_stage_entry_links_follow_the_theme`, and record
  that it passes on the branch's starting tree — so the later rewrite is known to be this slice's.

## Phase 2 — Foundational

None. The slice has one behaviour and one rule; there is no shared prerequisite to build first.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the stage's entry titles read as ink at rest and gain an underline on hover and keyboard
focus.
**Independent test**: open `/tatib/144/`; at rest every title is ink with no line; hovering one
underlines it 3px under the text; tabbing to it does the same.

- [X] T002 [P] [US1] Rewrite the test in `tests/e2e/test_reading.py` as
  `ReadingE2ETests.test_stage_entry_links_read_as_ink_until_hovered`, replacing
  `test_tatib_stage_entry_links_follow_the_theme`: in the light theme every `.entry__jump` computes
  `text-decoration-line: none` and the same `color` as its `.read__sec`; the first one under hover
  computes `underline` with `text-underline-offset: 3px` and an unchanged colour; `:focus-visible`
  gives the same line; after switching to dark, the resting colour is `rgb(245, 243, 238)` and the
  hover line survives (FR-001–FR-003, SC-001–SC-003, US1.1–US1.3).
- [X] T003 [US1] Make T002 pass: the `.entry__jump` rule in `static/styles/design/components.css` —
  `color: inherit; text-decoration: none` at rest, underline with a 3px offset on `:hover` and
  `:focus-visible` — and the two `--link` comments in `static/styles/design/tokens.css` reworded to
  name the media library (FR-001–FR-004).
- [X] T004 [US1] Prove the test is red for the right reason: restore the spec 056 rule in the working
  tree only, run T002, and record the assertion that fails (`color` and
  `text-decoration-line: underline`); then restore the new rule (TDD-02).
- [X] T005 [US1] Inspection pass on the live page: hover the long `…581. Sangap di Jahowa` title and
  check both wrapped lines carry the line; move the pointer off and check the line is gone
  (US1.4, US1.5).

## Phase 4 — US2 (P2)

**Goal**: nothing outside the stage's titles changes.
**Independent test**: hover a search result (it underlines as before), open the media library (its
"used by" links keep `--link`), and read the diff (one rule, two comments).

- [X] T006 [P] [US2] Run `tests.test_design_tokens` and `tests.e2e.test_media_library` on the slice;
  inspect a search result's hover underline and the media library's link colour (FR-004, SC-005,
  US2.1–US2.3).

## Phase 5 — Polish and delivery

- [X] T007 Re-run the targeted set — `tests.e2e.test_reading`, `tests.test_design_tokens`,
  `tests.e2e.test_media_library` — and record the counts.
- [X] T008 Fold the capability: `docs/spec/reading.md` gains `R16` (added), the header moves
  `last folded` to 2026-10-27 and prepends `140-stage-link-affordance`; write `fold.md`.
- [ ] T009 Apply `bump: patch` in the pre-merge commit: `VERSION` `1.22.0` → `1.22.1`, one
  `CHANGELOG.md` line under `## [Unreleased]`, card `release_version` left empty; then the PR title
  and body, the card to `In review` once the push has created the PR (the owner's word governs the
  push), and `Done` before the merge.

## Phase 6 — Convergence (pass 1)

The Converge gap: at a 1280px window with both sidebars open the old push layout left the stage 260px
wide, and the 252px controls covered the title outright, so the pointer could not reach it. The owner
chose to fix it in this slice and set the rule: labels wherever the window has room, icons on a phone.

- [X] T010 [US1] Reserve the controls' column on `.tatib__item--acts` — 264px from 700px of reading
  pane, `106px` below it, keyed on the pane as a container (`.read__body`) — so a title or media name
  never runs under the buttons (gap: `partial` FR-002, US1/AC2). A window-keyed first attempt (labels
  from 721px) was replaced: at a 1440px window the pane is 400px, and reserving 264px wrapped every
  title on the page.
- [X] T011 [US1] Wrap each action's word in `.entry__ctrl-label` in `tatib.html` and collapse it below
  700px of pane with the visually-hidden pattern, so a narrow pane gets icons while a screen reader
  still hears each button's name (owner's decision, `research.md` D006).
- [X] T012 [US1] Extend the E2E: at 1440 (pane 400px) the labels are visually hidden and the title
  ends before the controls; at 1920 (pane 880px) the labels come back and the title is still clear; at
  390 the title is clear and the underline still appears on hover. A mutation check (label rule
  disabled) failed the wide assertion, proving the test bites.
- [X] T013 [US1] Rebuild the static preview for the chosen design — `preview/controls.html` at 528px
  and 820px plus `preview/phone.html` in a 390px frame — and record the measured geometry.
