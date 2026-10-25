# Tasks: A text entry is written and edited in the media modal's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`
**Plan**: `specs/133-text-modal-large-frame/plan.md`
**Verification split**: 14 test · 5 inspection · 0 manual

The branch (`feat/133-text-modal-large-frame`) was cut from `develop` and updated onto `ffa5c340` at the
owner's instruction before gate 1's record was written; the preview tree already carries T002–T005 and
T009, which the tasks below verify rather than re-author.

## Phase 1 — Setup

- [X] T001 `specs/133-text-modal-large-frame/{spec,plan,research,data-model,quickstart}.md`,
      `contracts/README.md`, `checklists/checklist.md` and `preview/{README.md,probe_modal_frame.py}`
      exist and describe the accepted behaviour — verify each against `specs/_templates/`.

## Phase 2 — Foundational

- [X] T002 `multimedia/web/templates/reading/_entry_form.html` — the form carries
      `data-editor-size="large"` when `kind == 'text'` (create and edit) or when `kind == 'media'` with no
      entry; `data-media-create` stays for the media script.
- [X] T003 `static/styles/design/components.css` — the six large-frame rules now match
      `.editor:has([data-editor-size="large"])` instead of `:has([data-media-create])`, and the
      `@media (max-width: 650px)` entry covers the mode-switch wrapper's gutters too.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: `+ Text` opens in the media dialog's frame, with a Text box that fills it.
**Independent test**: the probe's `1440x900 text` row equals its `media` row, and the textarea reads 419.

- [X] T004 [P] [US1] `multimedia/web/tests.py::ServiceEntryViewTests` —
      `test_the_large_frame_is_marked_for_both_text_forms` (red before T002).
- [X] T005 [US1] `_entry_form.html` Text field carries `data-editor-grow`; `components.css` gives that
      field `flex: 1` and its textarea `flex: 1; min-height: 0`.
- [X] T006 [US1] `preview/probe_modal_frame.py` measures `+ Text` and `+ Media` at 1440×900 and writes
      their screenshots; the numbers land in the spec's `## UI/UX`.

## Phase 4 — US2 (P1)

**Goal**: an existing text entry's Edit opens in the same frame and its Text box fills it.
**Independent test**: the probe's `edit` row reads 840×760 at (300,70) with a 507px textarea.

- [X] T007 [US2] the marker's condition covers the edit path (same template, `entry` set) — confirmed by
      T004's second assertion and by the probe's edit row.
- [X] T008 [P] [US2] `tests/e2e/test_entry_modal_frame.py::test_text_box_fills_the_frame` — 419 on create,
      507 on edit, and the box's bottom edge meeting the action row's 14px margin.

## Phase 5 — US3 (P1)

**Goal**: the dialog is placed against the window, so a scrolled service does not open it above the top edge.
**Independent test**: `y = 70` for the 760px dialog at scrollY 0 and at scrollY 556.

- [X] T009 [US3] `components.css` — `.editor { position: fixed }` with the comment that explains the
      scroll-offset fault; the date popover keeps resolving inside the dialog.
- [X] T010 [P] [US3] `tests/e2e/test_entry_modal_frame.py::test_dialog_is_centred_on_a_scrolled_page` and
      `::test_narrow_window_uses_the_small_gutters`.

## Phase 6 — Polish

- [X] T011 [P] `tests/e2e/test_entry_modal_frame.py::test_new_text_dialog_matches_new_media` — the six
      values of SC-001 compared between the two dialogs.
- [X] T012 [P] `tests/e2e/test_entry_modal_frame.py` — `multimedia/web/tests.py` counterpart:
      `test_the_large_frame_is_not_marked_for_the_other_forms` (passage, song, media edit).
- [X] T013 `backlog/items/ITEM-138-text-modal-large-frame.md` + a row on `backlog/board.md`; the anchor
      issue (`Refs`, never `Closes`) created as the card passes `Ready` — **waits for the push
      authorisation**, since it is a write on the remote; the card records the number when it exists.
- [X] T014 `VERSION` 1.20.11 → 1.20.12 and the `## [Unreleased]` line in `CHANGELOG.md`, in the same
      commit that closes the card.
- [X] T015 `docs/spec/reading.md` — fold `R10`; `converge.md` and `fold.md` written; the closing report
      names both gate records.
- [X] T016 Re-run `tests/e2e/test_unified_text_screen_mode.py` and `tests/e2e/test_entries.py`
      unmodified at the push step — the switch, the help line, the hidden `default_screen_mode` field and
      the Save guard are the proof that FR-006 held.

## Phase 7 — Convergence

Converged on pass 1, 2026-10-25 — see `converge.md`. Every traceability row was checked by its declared
method: 14 `test` rows run (`multimedia.web` + `tests.test_design_tokens` 340 green, the new browser
module 4 green, the two untouched modules 16 green), 5 `inspection` rows read off the probe's printed
values. Typed gaps: none missing, none partial, none contradicting, none unrequested.
