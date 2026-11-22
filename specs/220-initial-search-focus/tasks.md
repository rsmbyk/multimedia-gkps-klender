# Tasks: focus only the empty search landing

**Spec**: `specs/220-initial-search-focus/spec.md` (Accepted, Gate 1 2026-11-22)
**Plan**: `specs/220-initial-search-focus/plan.md`
**Branch**: `fix/220-initial-search-focus`

`[P]` means order-independent, not concurrent: one agent, one thread.

## Phase 1 — Setup

- [X] T001 [P] [US1] Confirm the worktree is on `fix/220-initial-search-focus` cut from `origin/develop` and `VERSION` reads `1.36.4` — `VERSION`
- [X] T002 [P] [US1] Confirm the target is free of focus code: `grep -n 'focusLandingSearch\|onLanding' static/web/reading.js` returns nothing — `static/web/reading.js`

## Phase 2 — Foundational (the failing tests come first)

- [X] T003 [US1] Write the five tests in `ReadingE2ETests`: landing focus on all five landing routes, the Search-rail in-place arrival, results never auto-focused, submit moves focus out, reading routes untouched — `tests/e2e/test_reading.py`
- [X] T004 [US1] Run the five tests and record the red output: the landing focus test fails with `activeElement` `BODY`, the results and reading tests already pass — this is the defect being fixed

## Phase 3 — US1: the empty search landing is ready for typing

- [X] T005 [US1] Add `onLanding()` and `focusLandingSearch()` beside the search section of the shell — `static/web/reading.js`
- [X] T006 [US1] Call `focusLandingSearch()` from the init block after `syncState()` and `revealCurrent()` — `static/web/reading.js`
- [X] T007 [US1] In `applyPage()`, capture `previousHome` before the stage swap; after `syncState()`, focus the arriving landing and blur the field only on a `landing → results` transition — `static/web/reading.js`
- [X] T008 [US1] Run the five tests and see them green
- [X] T009 [US1] Re-measure the preview and the served page at 1440×900 and 390×844: field box and centre, results offsets, `scrollY` 0, no overflow — record any drift in `converge.md`

## Phase 4 — Polish and delivery

- [X] T010 Re-assess every traceability row by its declared method; write `converge.md` (pass 1)
- [X] T011 Fold: `docs/spec/reading.md` — `modified` block for `R15` (focus clause), `added` block for `R50`; write `fold.md`
- [X] T012 Apply the declared bump: `VERSION` `1.36.4 → 1.36.6` and one `### Fixed` line under `## [Unreleased]` in `CHANGELOG.md`
- [X] T013 Board: card `status: in-review`, `bump: patch`, `pr:` filled once the PR number exists; move the row to In review — `backlog/items/ITEM-235-search-landing-focus.md`, `backlog/board.md`
- [X] T014 Open the PR (draft, then ready) with the title and body from the closing report, and report — nothing pushed until the owner says so