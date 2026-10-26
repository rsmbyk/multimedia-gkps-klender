# Tasks: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`
**Plan**: `specs/134-sidebar-save-freshness/plan.md`
**Verification split**: 2 test · 1 inspection · 5 manual

Tasks run sequentially in one slice worktree. Every `test` row in the Plan has a failing-test task before its implementation task. No parallel tasks are declared because the scenarios share the reading-shell refresh path.

## Phase 1 — Setup

- [X] T001 [US1] When Gate 2 opens Implement, move ITEM-143 from Ready to In progress in `backlog/items/ITEM-143-sidebar-save-freshness.md` and `backlog/board.md`.

## Phase 2 — Foundational

No new dependency, schema, API, or test service is required; the slice uses the current Django live-server and Playwright harness.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: Sidebar edits keep every visible active-reading representation current and leave an unrelated reading stage in place.
**Independent test**: Save edits to active Tata Ibadah, song, and songbook records, then save a Kidung songbook edit while a Bible chapter remains open.

- [X] T002 [US1] Add failing tests for active Tata Ibadah, song, and songbook row/stage/title updates plus filter and pane-state preservation in `tests/e2e/test_sidebar_save_freshness.py`.
- [X] T003 [US1] Make the FR-001 and FR-004 tests pass by reconciling saved server values while retaining filters, pane modes, scroll positions, and focus in `static/web/reading.js`.

### Checkpoint — US1

- Active Tata Ibadah, song, and songbook representations update in place.
- Filter, pane mode, scroll, and focus remain stable while the rows reconcile.

## Phase 4 — US2 (P1)

**Goal**: Search results and counts reflect edits made from an open sidebar while the current query stays active.
**Independent test**: Edit a matching song so that it still matches, then so that it no longer matches, and inspect both result sets.

- [X] T004 [US2] Add failing FR-003 tests for matching and non-matching edited titles in `tests/e2e/test_sidebar_save_freshness.py`.
- [X] T005 [US2] Make the FR-003 tests pass by reconciling current-query results, counts, and the active tab-local search snapshot in `static/web/reading.js`.

### Checkpoint — US2

- Both search cases pass with the original query and current search page retained.
- The updated active search snapshot no longer restores the pre-save result HTML.

## Phase 5 — Polish

- [X] T006 [US1] Manually verify FR-002 and SC-003 in the live preview: keep a Bible chapter open, edit a Kidung row, and inspect the stage, route, pane state, filter, scroll, and focus.
- [X] T007 [US1] Inspect the success-event dispatch and error path in `static/web/editors.js`; confirm a rejected save does not emit `editor:saved` or publish unsaved values for FR-005.
- [X] T008 [US1] Manually edit a service entry in the open Tata Ibadah preview and confirm the stage and contents list still update in place for FR-006.
- [X] T009 [US1] Manually verify SC-001 at `/tatib/1/` and `/songs/1/`: edit each record kind and check the row, stage heading, and title without reloading or reopening a sidebar.
- [X] T010 [US2] Manually verify SC-002 at `/search?q=Preview`: check both match outcomes, result text, group counts, and the unchanged query.
- [X] T011 [US2] Run the focused Django/Playwright module with `python manage.py test tests.e2e.test_sidebar_save_freshness --noinput -v 2` and run the repository's required suite before the first Fold commit.
- [X] T012 [US1] After Converge, fold the new `reading` requirement into `docs/spec/reading.md` as R11, add `fold.md`, and verify the resulting capability delta is idempotent.
- [X] T013 [US1] Prepare the SDD closing report with verification split, Converge/Fold evidence, capability delta, branch and commit count, declared patch bump and changelog line, PR title/body, and that nothing is pushed; ask the owner before pushing.
- [X] T014 [US1] After the owner authorizes the first push, open the draft PR, use `Refs #397`, record its URL and update ITEM-143 to In review in the same PR.
- [X] T015 [US1] Before merge, append the user-visible fix to `CHANGELOG.md`, apply the declared patch bump to `VERSION`, and set ITEM-143 to Done before the merge.

## Phase 6 — Convergence

Converged on pass 1 — see `converge.md`. Folded as `reading` `R11` — see `fold.md`.
