# Tasks: Sidebar Delete Buttons

**Spec**: `specs/190-sidebar-delete/spec.md`
**Plan**: `specs/190-sidebar-delete/plan.md`
**Verification split**: targeted test/inspection/manual (endpoints + UI states)

## Phase 1 — Setup

- [x] T001 Create `multimedia/web/templates/reading/_editor_delete_confirm.html` confirm fragment for shared editor modal (heading, hint, cancel/delete actions).

## Phase 2 — Foundational

- [x] T002 Add delete confirm/delete endpoints and helpers in `multimedia/web/reading/views.py` for kinds `songbook`, `song`, `tatib`, `template` (GET confirm, POST delete, CSRF/protected, kind validation).
- [x] T003 Wire routes `web-editor-delete-confirm` and `web-editor-delete` in `multimedia/web/urls.py`.
- [x] T004 Add modal dataset `data-editor-delete-confirm` in `multimedia/web/templates/reading/_editor_modal.html`.

## Phase 3 — US1/US2 (Songbooks & Songs)

**Goal**: Delete controls for non-hymn songbooks and non-hymn songs with confirm flow.
**Independent test**: Hover eligible rows reveals delete beside edit; confirm removes row via POST.

- [x] T005 [US1] Update `_songbooks_panel.html` to render `.row-delete` for eligible non-hymn songbooks.
- [x] T006 [US2] Update `_song_list.html` to render `.row-delete` for eligible songs (not in hymn book).

## Phase 4 — US3 (Tata Ibadah services/templates) + FR-004

**Goal**: Delete controls for tatib/template rows with correct noun/kind and hide dated row date on hover/focus.
**Independent test**: Dated service hover hides date and reveals actions; template delete uses `Delete template`.

- [x] T007 [US3] Update `views.py` `_tatib_groups` to include row kind (`template` vs service) for client noun selection.
- [x] T008 [US3] Update `_tatib_panel.html` to render `.row-delete` and `data-editor-kind` on tatib/template rows.
- [x] T009 [US3] Update `components.css`: `.row-delete` styles/reveal parity with `.row-edit`; hide `.book__s` on hovered/focused tatib rows with actions (FR-004), scoped to avoid unrelated rows.

## Phase 5 — Client delete flow

**Goal**: Open confirm, submit delete, remove row, handle on-stage/history replace.
**Independent test**: Confirm POST deletes; row removed from correct panel; on-stage delete replaces history.

- [x] T010 [US1–US3] Extend `editors.js` with `nounFor`, `urlForDeleteConfirm`, `openDeleteConfirm`, `wasOnStage`, `applyDelete`, and delegated click handling for `[data-editor-delete]`.
- [x] T011 [US1–US3] Expose `window.gkpsNavigate` and `window.gkpsStage` from `reading.js` for delete/apply flow.

## Phase 6 — Verification & Polish

- [x] T012 Run syntax/checks: `node --check` JS, Python parse, `manage.py check`; verify URL resolution for delete routes.
- [x] T013 Manual/preview verification against FR-001–FR-013 and SC-001–SC-005 (hover/focus states, confirm nouns, hymn/restricted excluded, FR-004 date hidden). Targeted Django/Playwright tests if feasible. — Done: owner click-through on the live branch server (2026-11-14) and accepted; real-flow delete verified with a throwaway record (POST 200, row removed, modal closed, cleanup).
- [x] T014 [Converge] Endpoint tests for the declared `test` rows (FR-008/009): 10 tests in `multimedia/web/tests.py` `SidebarRecordDeleteTests` — method enforcement, kind mismatches, hymn/deleted guards, soft-delete and deactivate outcomes, fragment noun. Green with the editors and reading suites (91 tests).