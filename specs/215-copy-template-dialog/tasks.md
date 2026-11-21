# Tasks: the copy confirmation as a dialog of its own, and the copy's name

**Spec**: `specs/215-copy-template-dialog/spec.md`
**Plan**: `specs/215-copy-template-dialog/plan.md`
**Verification split**: 30 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Record the baseline: `manage.py test multimedia.web.test_tatib_templates` and `DJANGO_DEVELOPMENT_MODE=true manage.py test tests.e2e.test_tatib_templates` on this branch before any edit, and write down both counts. The slice must move the E2E count up by the tests it adds and leave the unit count's own failures unchanged.

## Phase 2 — Foundational

- [X] T002 Rewrite `multimedia/web/templates/reading/_copy_confirm.html` to the accepted markup: the heading, the lead, `.editor__field` with `#copyName` carrying `value="{{ copy_name }}"` and `maxlength="64"` plus `data-copy-name`, the three facts as `.confirm__facts`, and the two answers. Keep the layer node and every `[data-copy-*]` hook. Verified by US1's and US2's tests: it provides the elements both stories measure, and has no assertion of its own.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the confirmation is a layer of the window with its card centred on the window, the Edit dialog open and inert behind it.
**Independent test**: open a service's Edit modal, press Copy as template — the layer's box is the viewport's, the card is centred on the window, the dialog's height is unchanged and its Save is unreachable.

- [X] T003 [US1] Rewrite `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_covers_the_form` as `test_the_copy_confirmation_covers_the_window`: at 1440×900 and at 900×700, layer rect equals `innerWidth`/`innerHeight`, `position: fixed`, the card's centre within 1px of the viewport's; the dialog's height equal before open and after close; `elementFromPoint` at the form's Save inside the layer. Run it and read the failure — it must fail on the layer's box, not on a selector.
- [X] T004 [US1] `static/styles/design/components.css`: `.editor__confirm-layer` becomes `position: fixed; inset: 0; z-index: 40; place-items: center; padding: 24px; border-radius: 0` with the light scrim, plus the light-theme override. Update the block's comment to say what it now is and why the scrim is light.
- [X] T005 [US1] Run T003's test to green, then the whole E2E module to see what else the layer's move broke.

## Phase 4 — US2 (P1)

**Goal**: the copy is named in the confirmation — default `<source> (Copy)`, one click selects it, an empty name cannot be accepted, and the record takes what was typed.
**Independent test**: from `9 Agustus 2026`, the field reads `9 Agustus 2026 (Copy)`; typing `Model Minggu` and accepting creates a template by that name and leaves the source alone.

- [X] T006 [P] [US2] `multimedia/web/test_tatib_templates.py::test_the_confirmation_offers_the_source_name_plus_copy` — the editor fragment for a service renders `value="9 Agustus 2026 (Copy)"`.
- [X] T007 [US2] `views.py::_editor_fragment_context` — add `copy_name` (`f"{source.name[:57]} (Copy)"`) beside `copy_url`, for the same condition. Green on T006.
- [X] T008 [P] [US2] `multimedia/web/test_tatib_templates.py` — four endpoint tests: `test_a_copy_takes_the_posted_name` (and the source is unchanged), `test_a_copy_with_no_name_is_named_after_its_source`, `test_a_copy_refuses_a_blank_name`, `test_a_copy_refuses_a_name_over_64_characters`. The last two must fail on the status code, not on a parse error.
- [X] T009 [US2] `views.py::tatib_copy_as_template` — read `{"name": …}` from the body the way `entry_reorder` does; absent → the default; present → trim, refuse `""` and `> 64`. Green on T008.
- [X] T010 [P] [US2] `tests/e2e/test_tatib_templates.py::test_the_name_selects_itself_on_the_first_click` — after a real click on `[data-copy-name]`, `selectionStart` is 0 and `selectionEnd` is the value's length.
- [X] T011 [US2] `static/web/editors.js` — select the whole value when the field takes focus, and swallow the `mouseup` that would collapse it. Green on T010.
- [X] T012 [P] [US2] `tests/e2e/test_tatib_templates.py::test_a_second_click_places_a_caret` — a second click inside the field gives a caret, not a selection.
- [X] T013 [US2] `editors.js` — clear the select-on-focus flag after the first `mouseup`, and restore it on `blur`. Green on T012.
- [X] T014 [P] [US2] `tests/e2e/test_tatib_templates.py::test_a_blank_name_cannot_be_accepted` — spaces-only disables the accept button; one character re-enables it.
- [X] T015 [US2] `editors.js` — `input` on the field toggles `[data-copy-accept]`'s `disabled`. Green on T014.
- [X] T016 [US2] `editors.js` — send `JSON.stringify({name: …})` with `Content-Type: application/json`, keeping the CSRF and `X-Requested-With` headers and the existing failure path.
- [X] T017 [US2] `tests/e2e/test_tatib_templates.py::test_the_typed_name_names_the_copy` — type a name, accept, and the created row carries it while the source keeps its own. Extend `test_copy_as_template_asks_and_copies` rather than duplicating its navigation.

## Phase 5 — US3 (P2)

**Goal**: the dialog says what is about to happen, in the order the accepted preview set.
**Independent test**: read the card top to bottom — heading, lead, Name, three facts, two answers — and Cancel discards while Copy as template copies.

- [X] T018 [US3] `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_card_matches_the_preview` — rewritten: the card is 448 × 349.7, 22px padding, 14px radius, and its children come in the accepted order with the three fact strings. Fails on the old card's 176.3 and its missing field.
- [X] T019 [US3] `components.css` — the card's own rules: 14px radius, the facts list, and the field's spacing inside the card. Green on T018.

## Phase 6 — Polish

- [X] T020 [P] `tests/e2e/test_tatib_templates.py::test_escape_closes_the_confirmation_and_not_the_dialog` — Escape with the confirmation open leaves `#editorModal` open and the layer hidden. Then `editors.js`: a `cancel` listener that `preventDefault`s while the layer is open.
- [X] T021 [P] `tests/e2e/test_tatib_templates.py::test_the_scrim_closes_the_confirmation` — a click on the layer's own edge closes it; a click on the card's heading does not. Then `editors.js`: close when `event.target` is the layer.
- [X] T022 Rebuild the preview (`preview/build.py`) and re-run `preview/probe.py`; re-read the spec's `## UI/UX` numbers against the output and correct any that drifted.
- [X] T023 [P] The two `inspection` rows (SC-003, US1/AC2): open the preview in dark and light. Found that the dialog is a dimmed silhouette, not a readable one — the card is taller than the dialog — which became Converge's finding #3.
- [X] T024 Delivery: `VERSION` 1.35.5 → 1.36.0, the `## [Unreleased]` changelog line, the board row to In review, and the capability delta for `reading` R37 and R47 written at Fold.

## Phase 7 — Convergence

- [X] T025 Check every traceability row by the method it declared, both lanes run, `converge.md` written.
- [X] T026 Finding #3 (FR-002's *legible* half) reported to the owner, who chose the reword; R47 corrected in
  the capability file at Fold rather than claiming a legibility the surface does not have.
- [X] T027 Fold: R37 and R47 replaced whole in `docs/spec/reading.md`, `fold.md` written, header's slice list
  and `last folded` updated.