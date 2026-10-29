# Tasks: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`
**Plan**: `specs/163-media-dialog-file-picker-cancel/plan.md`
**Verification split**: 13 test · 7 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Confirm the failure before touching anything: on this branch, `/tatib/149/` with the media form
  open closes it **165 ms** after the file input's `cancel`, and the form leaves the page. No setup task
  exists: no dependency, no ignore-file change, no route.

## Phase 2 — Foundational

All four cases stand on one replay — the file input's own `cancel`, and Escape on the dialog — so they are
written and run here, before the fix.

- [X] T002 [P] [US1] Write
  `test_dismissing_the_file_picker_leaves_the_new_media_dialog_open` in `tests/e2e/test_media_library.py`:
  open the media form from a service page, type a title, send the input's `cancel`
  (`dispatch_event('cancel', {'bubbles': True})`), wait 400 ms, then assert the dialog is open, the form is
  in the page, the title is kept, the upload prompt is still shown and Save is still disabled.
- [X] T003 [P] [US1] Write `test_a_dismissed_picker_keeps_the_chosen_file` in the same file: choose a file
  through `input[data-media-file]` against `connected_page`'s companion stub, assert it is shown with Save
  enabled, send the input's `cancel`, wait 400 ms, and assert the name and the enabled Save survive.
- [X] T004 [P] [US1] Write `test_a_picker_dismissal_keeps_the_library_selection` in the same file: switch to
  the Media Library tab, select its one row, send the input's `cancel` (the input stays in the page while
  the Upload panel is hidden), and assert the dialog is open, the tab is still `library` and the row is
  still `aria-selected="true"`.
- [X] T005 [P] [US2] Write `test_escape_still_closes_the_new_media_dialog` in the same file: open the media
  form, press Escape on `#editorModal`, and assert it is closed within 400 ms.
- [X] T006 Run T002–T004 against the **unmodified** `static/web/media-entry.js` and record the red output in
  `analysis.md`; run T005 in the same pass and record that it is green — it is the case that fails only
  against a wrong fix.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: dismissing the picker leaves the dialog and its form exactly as they were.
**Independent test**: T002, T003 and T004 green; the live route keeps the dialog when the real picker is
dismissed.

- [X] T007 [US1] In `static/web/media-entry.js:20`, make the dialog's `cancel` listener return unless
  `event.target` is `editorDialog`; leave the wrapped `close()`, the form check, `event.preventDefault()`
  and `editorDialog.close()` exactly where they are.
- [X] T008 [US1] Re-run T002–T004: green. Re-run T005: still green.

## Phase 4 — US2 (P2)

**Goal**: the fix does not turn into "the modal no longer closes".
**Independent test**: T005 green against both the unmodified and the patched file; Cancel and the other
editor kinds untouched.

- [X] T009 [US2] `inspection` — read the two other ways the dialog closes: `.editor__cancel`
  (`_entry_form.html:237`, handled by `entries.js`'s `data-editor-close`) and the wrapped `close()` above
  the guard. Neither takes part in a `cancel` event, so neither can be affected.

## Phase 5 — Polish

- [X] T010 `inspection` — read the diff: one statement added to `media-entry.js`; no template, CSS, copy,
  endpoint or payload change (FR-004). Re-run
  `…::test_media_create_picker_defaults_to_upload_and_save_stays_disabled` and
  `…::test_empty_library_keeps_tall_create_modal_and_quiet_empty_state`.
- [X] T011 Add the index row to `specs/README.md`, naming 163 and `Accepted`.
- [X] T012 Bump `VERSION` `1.22.11` → `1.22.12` and add one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`.
- [X] T013 Fold: add R32 to `docs/spec/reading.md` and move the header's `last folded` and `slices`.
- [ ] T014 Delivery, after the report: open the PR as a draft, then read `ITEM-176`'s state — if it is still
  in `Backlog`, stop and say so; only the owner moves a card to `Ready` (`BRD-04`, `C-BOARD-GIT`).

## Phase 6 — Convergence

- [ ] T015 [Convergence] `manual` — on `http://localhost:8814/tatib/149/` with the real system picker: open
  *New media*, click *Choose file to upload*, dismiss the picker with Escape — the dialog stays, title and
  any chosen file intact; press Escape on the dialog — it closes with its usual motion.
