# Tasks: Verse modal header draws one rule

**Spec**: `specs/226-verse-modal-header-rule/spec.md`
**Plan**: `specs/226-verse-modal-header-rule/plan.md`
**Verification split**: 15 test · 3 inspection · 0 manual

## Phase 1 — Setup

- [ ] T001 Add `tests/e2e/test_verse_modal_header.py`: a `StaticLiveServerTestCase` with a book,
  a song and two verses, a Playwright Chromium fixture at 1366×900, and a `MEASURE` reader for the
  title/head boxes, computed borders, text range and both gaps.

## Phase 2 — Foundational

- [ ] T002 Confirm the base rule at `static/styles/design/components.css:541` still carries
  `padding: 20px 26px` and `border-bottom: 1px solid var(--divider)`, and that `:689` still holds
  the header reset the large selector outranks; record the base read-back.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the verse dialog paints one header rule and the title sits 16–17px above it, as in the
other editors.

**Independent test**: open `New verse` and `Edit verse 1`; the title has no border, the head has
the only one, and the title-to-rule gap is 16.5px.

- [ ] T003 [P] [US1] Write the failing E2E
  `tests/e2e/test_verse_modal_header.py::VerseModalHeaderE2ETests::test_new_verse_header_has_one_rule`
  — one ruled header descendant, title `borderBottomWidth === '0px'`; run it red.
- [ ] T004 [P] [US1] Write the failing E2E `...::test_edit_verse_header_has_one_rule` — same
  read-back from a verse's pencil; run it red.
- [ ] T005 [P] [US1] Write the failing E2E `...::test_header_gap_matches_the_other_editors` —
  21px top, 16–17px below the text, x=289 inset, 21px/640 title, 30px divider-to-label, in light
  and dark; run it red.
- [ ] T006 [P] [US1] Write the failing E2E `...::test_single_rule_follows_a_narrow_dialog` —
  390×844, one rule, head width `100vw - 32px`; run it red.
- [ ] T007 [US1] Write the failing E2E `...::test_non_verse_editor_header_is_unchanged` — the
  `New song` dialog keeps its 18px title, 0px padding, 16px gap and one rule; run it red only if
  the shared reset is touched.
- [ ] T008 [US1] In `static/styles/design/components.css:539–545`, give the large head
  `padding: 20px 26px 14px` and change the large title rule to `margin: 0; padding: 0; border: 0;
  font-size: 21px`, leaving the head's 16px bottom margin and the field's 14px top margin alone;
  make all five E2E cases green.
- [ ] T009 [US1] Re-run `specs/226-verse-modal-header-rule/preview/probe.py` against a build that
  carries the change and compare its numbers with the injected candidate report.

## Phase 4 — Polish

- [ ] T010 Inspect the diff: only the two CSS declarations and the new test file change; no
  template, script, endpoint or other editor's rule is touched.
- [ ] T011 Run the targeted E2E module and the neighbouring
  `tests.e2e.test_song_empty_placement` module; record both results.

## Phase 5 — Delivery (after Fold)

- [ ] T012 Apply `bump: patch` (VERSION 1.36.11 → 1.36.12) and the changelog line immediately
  before the merge, with `ITEM-241` moved to Done in the same commit.

## Phase 6 — Convergence

Pass 1 found zero gaps, so no convergence tasks were appended. See `converge.md`.
