# Tasks: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Plan**: `specs/167-tata-ibadah-templates/plan.md`
**Verification split**: 66 test · 2 inspection · 0 manual

Every `test` row in the plan's traceability table becomes a pair under TDD: the failing test first, then
the implementation that turns it green. `inspection` rows never enter TDD (C-SDD-TDD). Task order is
SDD's; the red → green order inside a task is TDD's.

## Phase 1 — Setup

- [X] T001 `multimedia/tatib/models.py`: `TataIbadahKind` (SERVICE 0, TEMPLATE 1), `SlotKind` (TEXT,
      SCRIPTURE, SONG, MEDIA); `TataIbadah.kind`; `ServiceEntry.kind` widened with `FILL_IN` 5 and
      `CHOICE` 6, plus `fill_kind` and `parent` (self-FK, `related_name='options'`, CASCADE).
- [X] T002 `multimedia/tatib/migrations/0012_tataibadah_kind_and_slots.py`: add `kind` nullable, backfill
      `TEMPLATE` where `date IS NULL`, `SERVICE` elsewhere, make it non-null, add the `CheckConstraint`;
      add the two entry fields.
- [X] T003 `static/styles/design/generate.css` + its `<link>` in `base.html`: the shell only — frame,
      steps, rows, footer, chooser layer — with the spec's numbers and no behaviour.

## Phase 2 — Foundational

- [X] T004 [P] `multimedia/web/test_tatib_templates.py`: `test_kind_and_date_always_agree`,
      `test_the_type_is_set_once_and_never_changes`, `test_the_api_never_writes_the_type` (red).
- [X] T005 `models.py`: `save()`/`clean()` derive the kind on insert when no date was given, refuse a
      TEMPLATE with a date, refuse a change of kind; `multimedia/api/tatib/serializers.py`: `kind`
      read-only, `create()` derives, `update()` drops. (T004 green.)
- [X] T006 [P] `test_the_migration_types_rows_by_their_date` through `MigrationExecutor` (red).
- [X] T007 [P] `test_a_fill_in_carries_a_kind_and_no_content`,
      `test_an_option_must_match_its_choice_kind`, `test_a_service_refuses_slots_from_every_endpoint`
      (model surface), `test_a_choice_with_no_options_says_so` (stage copy) (red).
- [X] T008 `models.py`: the four slot rules in `ServiceEntry.clean()`, and `citation()`/`resolve()` for
      the two kinds. (T007 green.)
- [X] T009 [P] `test_panel_lists_by_type`, `test_two_templates_with_one_name_both_list` (red).
- [X] T010 `views.py`: `_tatib_groups` selects by `kind`; `TatibView` sets the mode from `kind` and adds
      `is_template` / `generate_url` to the context. (T009 green.)
- [X] T011 [P] `test_a_template_is_never_projected`, `test_the_dock_lists_no_template` (red).
- [X] T012 `views.py`: `service_projector` drops a template id to the empty display; `obs_dock` filters on
      `kind`. (T011 green.)

## Phase 3 — US1: the type is chosen at creation (P1) 🎯 MVP

**Goal**: a Tata Ibadah is created as a Normal service or a Template, and the type never moves.
**Independent test**: create both types from the panel's **+**; the dated list and Templates each gain
exactly their kind, and the Edit modal shows no switcher.

- [X] T013 [P] [US1] `test_new_form_offers_both_types`,
      `test_edit_refuses_to_clear_a_normal_date` (red).
- [X] T014 [US1] `editors.py`: `TataIbadahForm` gains the `kind` chip field on create, requires the date
      for Normal, hides it for Template, exposes `hide_date_clear`; `_editor_form.html` renders the chips,
      omits the `Clear date` button, and titles the modal by type. (T013 green.)
- [X] T015 [P] [US1] `tests/e2e/test_tatib_templates.py`: `test_create_normal_service`,
      `test_create_template`, `test_edit_names_the_type`.
- [X] T016 [US1] `editors.py`/`_editor_form.html`: the chip handler (Template hides the date and its
      picker) and the type-aware title; `editors.js` carries the pressed state.

## Phase 4 — US2: a template carries fill-ins and choices (P1)

**Goal**: the two slot kinds are authored on a template and nowhere else.
**Independent test**: on a template, `+ Fill-in` and `+ Choice` appear after the four kind buttons,
each asks for a title and a kind, and **Add option** puts a child row under a choice.

- [X] T017 [P] [US2] `test_a_fill_in_is_a_title_and_a_kind`, `test_options_live_under_their_choice`,
      `test_a_service_refuses_slots_from_every_endpoint` (endpoint surface) (red).
- [X] T018 [US2] `entries.py`: `FillInEntryForm`, `ChoiceEntryForm`, both in `FORMS`; `entry_form` and
      `entry_save` accept `?parent=` and store the option's parent, kind and order. (T017 green.)
- [X] T019 [US2] `tatib.html` + `entries.js`: the two buttons after a hairline in every add bar, the
      slot rows, and the indented option rows in the stage (`_tatib_stage` gains one level).
- [X] T020 [US2] `reorder.js` + `entry_reorder`: a choice moves as a block — the client sends the
      choice followed by its options, and the server keeps them together; `test` →
      `test_a_choice_moves_with_its_options`.
- [X] T021 [P] [US2] E2E: `test_a_template_page_offers_fill_in_and_choice`,
      `test_add_fill_in_and_add_choice`, `test_an_option_lands_under_its_choice`,
      `test_a_choice_with_no_options_says_so`.

## Phase 5 — US3: a template creates a dated service (P1)

**Goal**: **Use template** settles every slot, then creates the service in the template's order.
**Independent test**: a template with both kinds generates a service; the template's rows are unchanged.

- [X] T022 [P] [US3] `test_validate_answers_the_row_and_writes_nothing` (red).
- [X] T023 [US3] `views.py`: `entry_validate` (bind the kind's form against the template, write nothing,
      answer `value` + echoed `data`) and its route. (T022 green.)
- [X] T024 [P] [US3] `test_generate_replaces_slots_in_order`, `test_generate_leaves_the_template_untouched`,
      `test_abandoning_creates_nothing`, `test_a_template_without_slots_copies_straight`,
      `test_a_deleted_resolution_refuses_the_create`, `test_legacy_rows_are_copied_as_legacy_rows`,
      `test_a_media_slot_keeps_its_identity` (red).
- [X] T025 [US3] `views.py`: `tatib_generate` — one transaction, every slot re-validated, the template's
      order walked over entries and legacy rows — and its route. (T024 green.)
- [X] T026 [US3] `_generate_modal.html`: the frame, the two steps, the order rows (fixed muted, slots
      live), the footer, the chooser layer and the create confirmation.
- [X] T027 [US3] `generate.js`: open/close, **Set** → the kind's form into the editor modal → post to
      `entry_validate` → the row's value, **Change** to redo it.
- [X] T028 [US3] `generate.js`: the chooser (options, Preview, **Choose**), the option-less choice's
      disabled control, and dismissal — `Cancel`, Escape, backdrop close the chooser alone.
- [X] T029 [US3] `generate.js`: the settled count, **Next**'s gate, step 2's name and nearest Sunday,
      **Create**'s confirmation and the POST to `tatib_generate`.
- [X] T030 [P] [US3] E2E: `test_the_generate_modal_shows_the_order`,
      `test_a_fill_in_settles_from_its_kind_modal`, `test_a_choice_settles_and_an_empty_one_cannot`,
      `test_closing_the_chooser_keeps_the_modal`, `test_next_gates_on_the_settled_count`,
      `test_step_two_prefills_name_and_sunday`, `test_create_lands_on_the_service`.

## Phase 6 — US4: any Tata Ibadah copies as a template (P2)

**Goal**: the Edit modal's **Copy as template** clones a service or a template into a template.
**Independent test**: copy a service and a template; both open on Templates with their entries intact.

- [X] T031 [P] [US4] `test_a_copy_converts_nothing`, `test_a_template_copy_keeps_its_slots` (red).
- [X] T032 [US4] `views.py`: `tatib_copy_as_template` (clone name and rows, a template's slots included,
      answer `{id, url}`) and its route. (T031 green.)
- [X] T033 [US4] `_editor_form.html` + `_copy_confirm.html` + `generate.js`: the header control, the
      confirmation naming the consequence, and the navigation to `?mode=template`.
- [X] T034 [P] [US4] E2E: `test_copy_as_template_asks_and_copies`, `test_a_copy_opens_on_templates`,
      `test_cancelling_a_copy_creates_nothing`.

## Phase 7 — US5: a template never reaches a screen (P2)

**Goal**: no projection control, no payload, no dock row for a template.
**Independent test**: a template's page shows **Use template** and the projector answers empty.

- [X] T035 [P] [US5] `test_a_template_page_has_no_project_controls` (E2E),
      `test_a_service_page_keeps_its_controls` (E2E), `test_a_template_is_never_projected` (unit, shared
      with T011).
- [X] T036 [US5] `tatib.html` + `TatibView`: **Use template** in place of both projector controls, the
      Media files dialog kept, the generate modal included on a template only.

## Phase 8 — Polish

- [X] T037 [P] `test_a_template_only_file_is_never_expired`, `test_a_template_only_file_is_not_in_the_manifest`
      (FR-023/FR-024 hold with no change to the queries).
- [X] T038 [P] `specs/167-tata-ibadah-templates/preview/probe.py`: re-run and align any state the
      implementation moved; the spec's `## UI/UX` numbers stay the reference.
- [X] T039 `docs/spec/reading.md`: R34–R38 at Fold, with the capability numbers re-read against
      `origin/develop` first.

## Phase 9 — Convergence

<!-- written by Converge only; absent until it runs -->
