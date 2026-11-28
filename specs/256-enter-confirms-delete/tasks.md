# Tasks: Enter accepts a delete confirmation

**Spec**: `specs/256-enter-confirms-delete/spec.md`
**Plan**: `specs/256-enter-confirms-delete/plan.md`
**Verification split**: 10 test · 7 inspection · 0 manual.

## Phase 1 — Setup

- [X] T001 `preview/serve.py` serves the real worktree on 8768 with isolated `gkps256` and collectstatic
- [X] T002 `preview/run-tests.py` runs named tests with the same run-time credential and no stored secret

## Phase 2 — Foundational

- [X] T003 [P] `tests/e2e/test_enter_delete_confirm.py` pins all four surfaces; run red against the unmodified code (4 failures: 3 timeouts, 1 assertion)

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: Enter deletes from every stage/sidebar/verse confirmation, independent of focus.
**Independent Test**: open the stage-entry confirmation, blur, press Enter → one POST and closed dialog.

- [X] T004 [P] [US1] `static/web/enter-delete.js` — capture-phase handler with hidden/closed/disabled/repeat/modifier guards and default suppression
- [X] T005 [US1] `data-enter-delete` on the sidebar submit button, the entries.js and songs_verse.js confirm buttons
- [X] T006 [US1] `reading/base.html` loads the handler once for every live surface

## Phase 4 — US2 (P2)

**Goal**: The Media Library's destructive removal follows the same key rule.
**Independent Test**: open `#mediaRemoveDialog`, blur, press Enter → one Remove-file click.

- [X] T007 [P] [US2] `data-enter-delete` on `#mediaConfirmRemove` in `media_library.html`

## Phase 5 — Polish

- [X] T008 [P] `preview/probe.py` plus `probe-results-baseline.jsonl` and `probe-results-after-fixed.jsonl`; README names every state
- [X] T009 the spec pack itself, with checklist validation before gate 1

## Phase 6 — Verification

- [X] T010 run the four tagged E2E pins green; check `node --check` on all three touched scripts
- [X] T011 Analyze: write `analysis.md`, confirm zero CRITICAL and 100% coverage before gate 2

## Phase 7 — Delivery (after gate 2 only)

- [X] T012 rebase the slice onto `origin/develop` and re-read ITEM id, `R<n>` and `VERSION`
- [ ] T013 card ITEM-278 → In review, then Done in the same PR that delivers the code
- [X] T014 Fold `reading/R68` into `docs/spec/reading.md`; patch `VERSION` and `CHANGELOG.md`
- [ ] T015 squash-merge with PR title/body; no push before the owner's word

## Phase 8 — Convergence

<!-- written by Converge only; absent until it runs -->
