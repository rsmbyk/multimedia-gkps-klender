# Tasks: No empty groups after the last row is deleted

**Spec**: `specs/252-empty-date-group/spec.md` (Accepted, gate 1)
**Plan**: `specs/252-empty-date-group/plan.md`
**Verification split**: 5 test · 9 inspection · 1 manual
**Order used**: one thread, in the order listed; `[P]` marks order independence, not concurrency.

Chronology note: the live preview edit was already uncommitted in the worktree before gate 1. Implement
re-assesses those edits against the tasks below; it does not re-type them or commit anything before Fold.

## Phase 1 — Setup

- [X] T001 [Setup] Verify the slice branch is cut from `1c86096f`, the worktree is clean of commits, and ignore files cover `_static/` and `__pycache__`.

## Phase 2 — Foundational

- [X] T002 [Foundational] Confirm [contracts/none.md](contracts/none.md) and [data-model.md](data-model.md) stand: no endpoint, schema or migration work is in this slice.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: deleting the last row of a date bucket retires the bucket, including under a filter.
**Independent test**: live 8776 bucket section 1→0 while 8777 stays 1; filtered bucket visible→hidden→visible.

- [X] T003 [US1] `test` — write a failing test for FR-001's bucket case: `tests.e2e.test_empty_date_group.EmptyDateGroupE2ETests.test_deleting_the_last_service_in_a_bucket_removes_its_heading`; confirm it fails on count 1, not an import error.
- [X] T004 [US1] `test` — write a failing test for FR-001's songbook case: `…test_deleting_the_last_songbook_removes_its_unheaded_group`; confirm 2 sections survive on base.
- [X] T005 [US1] `test` — make the FR-001 bucket case pass by retiring the owning `section.group` in `static/web/editors.js:applyDelete()` when no `.book` row remains.
- [X] T006 [US1] `test` — make the FR-001 songbook case pass through the same shared client path; no per-template callback.
- [X] T007 [US1] `test` — write a failing test for FR-002: `…test_deleting_the_last_visible_row_hides_a_filtered_group`; confirm the bucket stays visible on base.
- [X] T008 [US1] `test` — make FR-002 pass by toggling `is-hidden` on the section when every survivor is filtered out.
- [X] T009 [US1] `inspection` — US1/AC1: compare `probe-results.jsonl` and `probe-results-base.jsonl` `date-bucket` after-last-delete counts (1→0 vs 1→1).
- [X] T010 [US1] `inspection` — US1/AC2: compare the same files' `date-bucket` after-reload counts (0 on both).
- [X] T011 [US1] `inspection` — US1/AC3: compare `filtered` states (`bucketHidden` false→true→false, visible rows 1→0→2).

## Phase 4 — US2 (P2)

**Goal**: the unheaded songbook group and the template-mode server render obey the same rule.

- [X] T012 [US2] `test` — write a failing test for FR-003: `…test_deleting_the_last_template_leaves_no_empty_group`; confirm the group survives on screen and on reload on base.
- [X] T013 [US2] `test` — make FR-003 pass by emitting `Templates` only when `_tatib_groups()` has templates.
- [X] T014 [US2] `inspection` — US2/AC1: songbook probe sections 2→1 on 8776 vs 2→2 on 8777.
- [X] T015 [US2] `inspection` — US2/AC2: template probe sections 1→0 on screen and reload on 8776 vs 1→1 on 8777.
- [X] T016 [US2] `inspection` — US2/AC3 and SC-003: check all ten rows of `research.md` against their cited paths and confirm no grouped surface was missed.

## Phase 5 — Polish

- [X] T017 [Polish] `test` — SC-001 red evidence: run the module from the detached base worktree and record four failures by name.
- [X] T018 [Polish] `test` — SC-001 green evidence: run the same module on the slice and record four passes.
- [X] T019 [Polish] `test` — SC-002 base evidence: copy the corrected sort test into the detached base worktree, run it there and restore the base file; 6/6 green.
- [X] T020 [Polish] `test` — SC-002 slice evidence: run both neighbouring modules on the slice; all green after A3's test-only correction.
- [X] T021 [Polish] `inspection` — FR-004: `git diff --name-only` against base and confirm only `editors.js` and `views.py` carry behaviour changes.
- [X] T022 [Polish] `inspection` — UI/UX: re-read both JSONL probes and confirm the spec table still matches the frozen numbers.
- [ ] T023 [Polish] `manual` — after deployment, delete the last service of a bucket in the live Tata Ibadah sidebar and confirm the heading goes with it.
- [X] T024 [Polish] Fold — only at Converged: first commit carrying spec pack, code, board row and `reading/R64` delta, with the suite green.
- [ ] T025 [Polish] Delivery — after a separate owner word: tracker anchor, PR, version/changelog line, card moves and report.
