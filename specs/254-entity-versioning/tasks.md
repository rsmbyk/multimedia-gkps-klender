# Tasks: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`
**Plan**: `specs/254-entity-versioning/plan.md`
**Verification split**: 27 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Confirm ignore files cover preview screenshots and the focused test command in `quickstart.md` runs from the worktree with the main checkout's venv.

**Checkpoint: Setup** — focused test command runs; no credentials in the tree.

## Phase 2 — Foundational

- [X] T002 [P] [US1] Write the red migration test in `multimedia/songs/test_migrations.py` and `multimedia/tatib/tests.py` for version 1 on all six models (covers FR-001, FR-014, SC-006).
- [X] T003 [US1] Add `version` columns and migrations in `multimedia/songs/models.py`, `multimedia/tatib/models.py` and their `migrations/`; make T002 green.
- [X] T004 [P] [US2] Write the red no-op test in `multimedia/web/tests.py` for identical-value saves and reorders (covers FR-002, SC-002).
- [X] T005 [US2] Add stored-value and ordered-ID comparison before writes in `multimedia/web/reading/views.py` and `verses.py`; make T004 green.
- [X] T006 [P] [US3] Write the red conflict tests in `multimedia/web/tests.py` for stale writes and the 409 body (covers FR-003, FR-013, SC-001).
- [X] T007 [US3] Add the shared version guard with `select_for_update()` in `multimedia/web/reading/views.py`; wire `expected_version` into form and JSON write paths; make T006 green.
- [X] T008 [P] [US4] Write the red test in `multimedia/web/tests.py` for service bumps on entry and legacy-item writes, including creates with a stale parent (covers FR-005, FR-006).
- [X] T009 [US4] Wire the service bump into `entry_save`, `entry_delete`, `entry_reorder`, `old_item_save`, `old_item_delete` and template generate/copy in `multimedia/web/reading/views.py`; make T008 green.
- [X] T010 [P] [US5] Write the red test in `multimedia/web/tests.py` for song and verse changes bumping every referencing service (covers FR-007, SC-003).
- [X] T011 [US5] Add the propagation helper in `multimedia/web/reading/views.py` and call it from `verses.py`; make T010 green.

**Checkpoint: Foundational** — all version and conflict tests pass; no write path remains unguarded (FR-015 by inspection).

## Phase 3 — US6 (P1) 🎯 MVP

**Goal**: a referenced verse, song or songbook cannot be deleted.
**Independent test**: delete endpoints refuse with a non-zero reference count.

- [X] T012 [P] [US6] Write the red delete-refusal tests in `multimedia/web/reading/test_verses.py` and `multimedia/web/tests.py` (covers FR-008, FR-009, FR-010, SC-005).
- [X] T013 [US6] Add the song and songbook guards to `editor_delete` in `multimedia/web/reading/views.py`; make T012 green.

## Phase 4 — US7 (P1)

**Goal**: every refusal notice counts distinct Tata Ibadah, including templates.
**Independent test**: one service with two qualifying entries counts once, a template counts once.

- [X] T014 [P] [US7] Write the red distinct-count test in `multimedia/web/tests.py` (covers FR-011, SC-004).
- [X] T015 [US7] Add the shared count helper in `multimedia/web/reading/views.py` and use it in the verse editor context and both delete confirmations; make T014 green.

## Phase 5 — US8 (P1)

**Goal**: the notice and disabled Delete appear in the product's real dialogs.
**Independent test**: Playwright sees the note and disabled Delete in song, songbook and verse states.

- [X] T016 [P] [US8] Write the red E2E cases in `tests/e2e/test_verse_reference_notice.py` for song and songbook confirmations (covers FR-012).
- [X] T017 [US8] Render the note in `multimedia/web/templates/reading/_editor_delete_confirm.html`, set the 560px confirmation width in `static/styles/design/components.css`, and make T016 green.

## Phase 6 — Polish

- [X] T018 Re-run the preview probe and update `specs/254-entity-versioning/preview/README.md` if measured numbers drift.
- [X] T019 Inspect every write route in `multimedia/web/urls.py` for the shared guard (FR-004, FR-015) and record the result in `specs/254-entity-versioning/converge.md` during Converge.
- [X] T020 Run the focused endpoint suite, the new E2E cases and the preview probe; report the verification split.

## Phase 7 — Convergence

- [X] T021 [US1–US8] Fix the five Converge gaps: stored-value dirty comparison, Verse reference counting, serializer exclusion, historical migration fixtures and static manifest.
- [X] T022 [US1–US8] Record the verification evidence and the seven known-red failures in `converge.md`.
