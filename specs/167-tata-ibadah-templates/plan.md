# Implementation Plan: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Branch**: `feat/167-tata-ibadah-templates`
**Bump**: `minor` — a new user-visible capability (a type, two entry kinds, a generate flow). It is stamped
against `develop` in the pre-merge commit: `develop` already reads **1.24.0** (a sibling slice took that
level), so the expected number is **1.25.0**; re-read `VERSION` immediately before stamping.
**Preview**: `static preview at specs/167-tata-ibadah-templates/preview/` — `index.html` opened directly,
`probe.py` for the measurements the spec's `## UI/UX` carries.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, DRF; server-rendered templates; vanilla JS (ES5-style IIFEs); plain CSS |
| Primary dependencies | none added — no JS library, no Python package |
| Storage | PostgreSQL; two new fields and one new FK on `multimedia.tatib`, one migration (`0012`) |
| Testing | Django `TestCase` in `multimedia/web/test_tatib_templates.py`; Playwright (Python) in `tests/e2e/test_tatib_templates.py` |
| Target platform | the deployed app (Vercel, `@vercel/python`) and the local compose stack; every browser the app supports |
| Project type | server-rendered Django app with fetched modal fragments; no build step |
| Performance goals | none new — the generate walk is one pass over a template's rows inside one transaction; the panel's two queries stay one each |
| Constraints | no new endpoint surface beyond the three in `contracts/`; media retention and the download manifest unchanged; every existing dated service keeps its list and its page |
| Scale / scope | a service order is tens of entries; a template is one page; the slice touches models, forms, three views, four templates, one new stylesheet and one new script |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: pass — one migration, no new dependency, no new storage, no endpoint that a
non-editor can reach.

## Phase 0 — Research

See `research.md`. Thirteen decisions, each with its code read: the type as a stored field derived only on
insert (D001), slot kinds with `fill_kind` + `parent` rather than new models (D002), validate-then-create
so nothing writes before **Create** (D003), one atomic generate endpoint walking the template's order
(D004), projection refused where the payload is built (D005), media left correct as it stands (D006),
copy-as-template as a server clone (D007), the switcher inside the fetched form fragment (D008), the date
that cannot be cleared (D009), legacy rows copied as legacy rows (D010), `kind` read-only in the API
(D011), one new client file (D012), two test modules (D013). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `TataIbadah.kind`, `ServiceEntry.fill_kind` and `.parent`, six invariants.
- `contracts/README.md` — the three endpoints plus the surfaces that stay unchanged.
- `quickstart.md` — the throwaway-database commands, the dev server, and six verification rows.

### The design

**Model** — `multimedia/tatib/models.py`
`TataIbadahKind` (`SERVICE=0`, `TEMPLATE=1`) and `TataIbadah.kind`; `save()` derives the kind on insert when
no date was given (so an API create with no date is still a template, A10), refuses a `TEMPLATE` carrying a
date, refuses a change of kind on an existing row, and `clean()` mirrors it for forms; a `CheckConstraint`
holds the pairing in the database. `ServiceEntryKind` gains `FILL_IN=5` and `CHOICE=6`; `fill_kind` and
`parent` arrive with `SlotKind` (text, passage, song, media). `ServiceEntry.clean()` gains the four slot
rules (template-only, `fill_kind` required, an option equals its parent's kind and lives in the same
Tata Ibadah, no second level) and `citation()`/`resolve()` answer for the two new kinds so the stage and the
preview keep one code path. Migration `0012` adds the field, backfills by date, then constrains.

**Panel** — `multimedia/web/reading/views.py`
`_tatib_groups` selects by `kind` instead of `date__isnull`; `TatibView` sets the mode from `kind`, adds
`is_template` and `generate_url` to the context, and stops rendering a projector URL for a template. The
stage builder gains one level: a choice's options render as indented child rows under it, and a fill-in or
choice renders with the kind line and the value line the preview draws.

**Forms** — `editors.py`, `entries.py`, `_editor_form.html`
`TataIbadahForm` gains a `kind` choice on create only (Normal/Template chips), requires the date for Normal,
drops the date field for Template, and exposes `hide_date_clear` so `_editor_form.html` omits the picker's
`Clear date` button on this modal. `FillInEntryForm` and `ChoiceEntryForm` join `FORMS`; `entry_form` and
`entry_save` accept `?parent=<choice pk>` and store the option with its parent, the choice's `fill_kind` and
the template's order. Both refuse a service target.

**Endpoints** — `views.py`, `multimedia/web/urls.py`
`entry_validate` (binds the kind's form, writes nothing, answers the row's value and echoes the data),
`tatib_generate` (one transaction, replays every slot, copies in the template's order, refuses an unsettled
or foreign slot) and `tatib_copy_as_template` (clones name and rows, keeps a template's slots). Shapes in
`contracts/README.md`.

**Reorder** — `static/web/reorder.js`, `entry_reorder`
A choice moves as a block: the client sends the choice followed by its options, and the endpoint keeps
them contiguous, so a drag can never leave a choice's options under another entry.

**Projection** — `projector.html` untouched; `service_projector` drops a template id to the empty display;
`obs_dock` filters on `kind`; `tatib.html` renders **Use template** where the two projector controls were.

**Client** — `static/web/generate.js` + `static/styles/design/generate.css`
One IIFE: opens the modal, fetches a kind's form into it for **Set**, posts the slot to `entry_validate`,
renders the row's value, gates **Next** on the settled count (an option-less choice can never settle), moves
to step 2 with the name prefilled and the nearest Sunday, confirms, and posts the generate request. The
chooser is a layer inside the modal and owns Escape/backdrop dismissal. `entries.js` gains the two
template-only add buttons and **Add option**. Numbers come from the spec's `## UI/UX` (frame 840×760,
header 150.7, footer 69, body 540–541, chooser 560×261.3, add bar 455.2×35.6, slot rows at the page's own
type scale).

**API** — `multimedia/api/tatib/serializers.py`
`kind` is `read_only`; `create()` derives it from the date, `update()` drops it. No new route.

**Media** — no change (D006). The two queries keep their shape; the tests pin FR-023/FR-024.

## Traceability

| Requirement / scenario | Component | Verified by | Evidence |
| --- | --- | --- | --- |
| FR-001 — a type chosen at creation, never changed | `TataIbadah.kind`, `save()` | `test` → `test_the_type_is_set_once_and_never_changes` | an update that posts another kind is refused |
| FR-002 — Normal has a date, Template has none, enforced | model `clean`/`save` + constraint | `test` → `test_kind_and_date_always_agree` | four combinations, two accepted |
| FR-003 — switcher on New; date required for Normal, absent for Template; no control empties it | `TataIbadahForm`, `_editor_form.html` | `test` → `test_new_form_offers_both_types` | `[data-date-picker-clear]` absent (E2E) |
| FR-004 — Edit carries no switcher, names the type, refuses a cleared date | `TataIbadahForm`, `_editor_form.html` | `test` → `test_edit_refuses_to_clear_a_normal_date` | 400 + message |
| FR-005 — the panel picks its list by type | `_tatib_groups` | `test` → `test_panel_lists_by_type` | template under Templates, service in a bucket |
| FR-006 — existing rows typed at migration, no entry converted | migration `0012` | `test` → `test_the_migration_types_rows_by_their_date` | pre/post state through `MigrationExecutor` |
| FR-007 — add rows offer the two slot buttons on a template only | `tatib.html`, `entries.js` | `test` (E2E) → `test_a_template_page_offers_fill_in_and_choice` | six buttons in order; four on a service |
| FR-008 — a fill-in is a title/note plus one kind, no content | `FillInEntryForm`, model rules | `test` → `test_a_fill_in_carries_a_kind_and_no_content` | save + refusal of content |
| FR-009 — a choice is a title, one kind, ordered options as child rows | `ChoiceEntryForm`, `?parent=`, stage | `test` → `test_options_live_under_their_choice` | order preserved, child rows |
| FR-010 — never writable on a Normal, whatever the surface | model + every entry endpoint | `test` → `test_a_service_refuses_slots_from_every_endpoint` | model, save-new, validate |
| FR-011 — Use template replaces the projector controls, Media files stays | `tatib.html` | `test` (E2E) → `test_a_template_page_has_no_project_controls` | count 0, Media files present |
| FR-012 — no projector payload, absent from the dock | `service_projector`, `obs_dock` | `test` → `test_a_template_is_never_projected` | empty payload; dock list |
| FR-013 — Use template opens the order view-only, ordinary rows muted and inert | `_generate_modal.html`, `generate.css` | `test` (E2E) → `test_the_generate_modal_shows_the_order` | opacity .52, no controls |
| FR-014 — a fill-in is settled by Set and can change | `generate.js`, `entry_validate` | `test` (E2E) → `test_a_fill_in_settles_from_its_kind_modal` | value in the row, Change works |
| FR-015 — a choice is settled by Choose, each option previewable; an option-less choice is disabled | `generate.js`, chooser layer | `test` (E2E) → `test_a_choice_settles_and_an_empty_one_cannot` | `disabled`, label `No options` |
| FR-016 — Next is disabled until every slot settles, with a count | `generate.js` | `test` (E2E) → `test_next_gates_on_the_settled_count` | `disabled` at each step |
| FR-017 — Next shows the normal form, name prefilled, nearest Sunday | `generate.js`, `TataIbadahForm` | `test` (E2E) → `test_step_two_prefills_name_and_sunday` | input values |
| FR-018 — Create confirms and creates atomically | `tatib_generate` | `test` → `test_generate_replaces_slots_in_order` | rows + order |
| FR-019 — the template is unchanged; abandoning stores nothing | `tatib_generate` | `test` → `test_generate_leaves_the_template_untouched` | field-by-field read |
| FR-020 — Edit offers Copy as template with a confirmation | `_editor_form.html`, `generate.js` | `test` (E2E) → `test_copy_as_template_asks_and_copies` | both types |
| FR-021 — the copy keeps name and entries, no conversion, no date | `tatib_copy_as_template` | `test` → `test_a_copy_converts_nothing` | kinds unchanged |
| FR-022 — the app lands on the new template, panel on Templates | `generate.js` | `test` (E2E) → `test_a_copy_opens_on_templates` | mode + list |
| FR-023 — a template's media is a use and is never auto-deleted | `media_references` (unchanged) | `test` → `test_a_template_only_file_is_never_expired` | `unused_since` stays null |
| FR-024 — a template's media is never auto-downloaded | `media_manifest` (unchanged) | `test` → `test_a_template_only_file_is_not_in_the_manifest` | `files == []` |
| US1 AC1–AC2 — the switcher renders, Normal saves with its date | `_editor_form.html` | `test` (E2E) → `test_create_normal_service` | chips `aria-pressed`, dated list |
| US1 AC3 — no control empties the date | the same | `test` (E2E) → `test_create_normal_service` | no `[data-date-picker-clear]` |
| US1 AC4 — Template hides the date and saves without one | the same | `test` (E2E) → `test_create_template` | no date field, Templates list |
| US1 AC5 — Edit names the type and edits only what it owns | `_editor_form.html` | `test` (E2E) → `test_edit_names_the_type` | title text, no chips |
| US1 AC6 — a cleared date is refused | `TataIbadahForm` | `test` → `test_edit_refuses_to_clear_a_normal_date` | message |
| US1 AC7 — the migration keeps every list | migration `0012` | `test` → `test_the_migration_types_rows_by_their_date` | counts before/after |
| US2 AC1 — six buttons in order, four on a service | `tatib.html` | `test` (E2E) → `test_a_template_page_offers_fill_in_and_choice` | order read from the DOM |
| US2 AC2–AC3 — the two slot modals ask for title and kind | `_slot_form.html` | `test` (E2E) → `test_add_fill_in_and_add_choice` | rows drawn |
| US2 AC4 — Add option opens the kind's modal, option is a child row | `entries.js`, `?parent=` | `test` (E2E) → `test_an_option_lands_under_its_choice` | indentation + order |
| US2 AC5 — an option of another kind is refused | `ServiceEntry.clean` | `test` → `test_an_option_must_match_its_choice_kind` | error key |
| US2 AC6 — an option-less choice says so | stage + row | `test` (E2E) → `test_a_choice_with_no_options_says_so` | copy |
| US2 AC7 — a service refuses slots from any endpoint | model + views | `test` → `test_a_service_refuses_slots_from_every_endpoint` | three surfaces |
| US3 AC1 — Use template opens, order view-only | `generate.js` | `test` (E2E) → `test_the_generate_modal_shows_the_order` | muted rows |
| US3 AC2 — fixed rows inert | the same | `test` (E2E) → `test_the_generate_modal_shows_the_order` | no controls inside |
| US3 AC3 — Set opens the kind's modal | `entry_validate` | `test` → `test_validate_answers_the_row_and_writes_nothing` | 0 rows written |
| US3 AC4 — Choose lists options with Preview | chooser layer | `test` (E2E) → `test_a_choice_settles_and_an_empty_one_cannot` | options + preview |
| US3 AC5 — dismissing the chooser closes the chooser alone | `generate.js` | `test` (E2E) → `test_closing_the_chooser_keeps_the_modal` | modal still open |
| US3 AC6 — Next gated, count shown | `generate.js` | `test` (E2E) → `test_next_gates_on_the_settled_count` | status line |
| US3 AC7 — step 2 is the normal form, nearest Sunday | `generate.js` | `test` (E2E) → `test_step_two_prefills_name_and_sunday` | values |
| US3 AC8 — Create confirms, lands on the service | `tatib_generate` | `test` (E2E) → `test_create_lands_on_the_service` | URL + heading |
| US3 AC9 — entries follow the order, slots replaced in place | `tatib_generate` | `test` → `test_generate_replaces_slots_in_order` | ordered kinds |
| US3 AC10 — abandoning stores nothing | `tatib_generate` | `test` → `test_abandoning_creates_nothing` | count unchanged |
| US4 AC1 — Copy as template in the Edit modal, both types | `_editor_form.html` | `test` (E2E) → `test_copy_as_template_asks_and_copies` | button count 2 |
| US4 AC2 — the confirmation names the consequence | `_copy_confirm.html` | `inspection` — copy reads "no date, cannot become a normal Tata Ibadah" and both answers are present | preview `06-copy-confirm.png` |
| US4 AC3 — name and entries kept, nothing converted | `tatib_copy_as_template` | `test` → `test_a_copy_converts_nothing` | kinds + order |
| US4 AC4 — a template copy keeps slots and options | the same | `test` → `test_a_template_copy_keeps_its_slots` | counts |
| US4 AC5 — lands on the new template with Templates | `generate.js` | `test` (E2E) → `test_a_copy_opens_on_templates` | `?mode=template` |
| US4 AC6 — cancelling creates nothing | `_copy_confirm.html` | `test` (E2E) → `test_cancelling_a_copy_creates_nothing` | count unchanged |
| US5 AC1 — a template page has no projector controls | `tatib.html` | `test` (E2E) → `test_a_template_page_has_no_project_controls` | 0 + Use template |
| US5 AC2 — a service page keeps both | the same | `test` (E2E) → `test_a_service_page_keeps_its_controls` | 2 |
| US5 AC3 — `/projector?service=<template>` is empty | `service_projector` | `test` → `test_a_template_is_never_projected` | `screens == []` |
| US5 AC4 — the dock omits templates | `obs_dock` | `test` → `test_the_dock_lists_no_template` | ids |
| Edge — a template with no slots still generates | `tatib_generate` | `test` → `test_a_template_without_slots_copies_straight` | Next enabled, copy made |
| Edge — a deleted resolved song refuses the create | `tatib_generate` | `test` → `test_a_deleted_resolution_refuses_the_create` | 400 names the row |
| Edge — legacy `TataIbadahItem` rows are copied as legacy rows | `tatib_generate` | `test` → `test_legacy_rows_are_copied_as_legacy_rows` | type + order |
| Edge — duplicate template names both list | `_tatib_groups` | `test` → `test_two_templates_with_one_name_both_list` | 2 rows |
| Edge — a template's Media files dialog works as on a service | `tatib.html` | `inspection` — the same dialog markup renders on a template with `service_media` | preview `01-template-page.png` |
| Edge — a settled media fill-in references the identity like a direct entry | `entry_validate` → `tatib_generate` | `test` → `test_a_media_slot_keeps_its_identity` | `media_id` equal |
| Edge — a choice and its options move together in the running order | `reorder.js`, `entry_reorder` | `test` → `test_a_choice_moves_with_its_options` | option ids follow the choice |
| SC-001 — no row disagrees with its date | constraint + writers | `test` → `test_kind_and_date_always_agree` | 0/0 via the quickstart query |
| SC-002 — no projection control, no payload | `tatib.html`, `service_projector` | `test` → `test_a_template_page_has_no_project_controls` | both surfaces |
| SC-003 — Next gates at 1…0 unsettled | `generate.js` | `test` (E2E) → `test_next_gates_on_the_settled_count` | each step |
| SC-004 — generating leaves the template unchanged | `tatib_generate` | `test` → `test_generate_leaves_the_template_untouched` | all fields |
| SC-005 — pre-slice services keep their lists | migration `0012` | `test` → `test_the_migration_types_rows_by_their_date` | both lists |
| SC-006 — the generated order matches the template's | `tatib_generate` | `test` → `test_generate_replaces_slots_in_order` | pair of lists |

**Verification split: 67 test · 2 inspection · 0 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-024 each carry a row; all 38 story scenarios, all six SCs and the reorder edge are mapped |
| Entity coverage | `TataIbadah.kind`, `ServiceEntry.fill_kind`/`.parent`, six invariants, what is deliberately not modelled |
| Interface coverage | `contracts/README.md` names three endpoints, their shapes, their errors and the surfaces left unchanged |
| Decision provenance | D001–D013 in `research.md`, each with its code read |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 67 `test` · 2 `inspection` · 0 `manual` |
| `quickstart.md` runnable | yes — migrate, collectstatic and both suites run on this worktree against a throwaway database |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/167-tata-ibadah-templates/
  spec.md  plan.md  research.md  data-model.md  quickstart.md
  contracts/README.md
  preview/  (index.html, preview.css, preview.js, probe.py, README.md)
  tasks.md  analysis.md  converge.md  fold.md  checklists/   — the stages after this one
```

### Source

```
multimedia/tatib/models.py                     kinds, fill_kind, parent, save/clean rules
multimedia/tatib/migrations/0012_*.py          the field, the backfill, the constraint
multimedia/web/reading/views.py                panel by kind, stage nesting, entry_validate,
                                               tatib_generate, tatib_copy_as_template, projector guard, dock
multimedia/web/reading/editors.py              TataIbadahForm: the two chips and the date rules
multimedia/web/reading/entries.py              FillInEntryForm, ChoiceEntryForm, ?parent= options
multimedia/web/urls.py                         the three routes
multimedia/web/templates/reading/_editor_form.html      chips, no Clear date, copy control
multimedia/web/templates/reading/_tatib_panel.html      unchanged markup, templates list already exists
multimedia/web/templates/reading/tatib.html             Use template, the two slot buttons, option rows
multimedia/web/templates/reading/_generate_modal.html   the modal, its steps and chooser
multimedia/web/templates/reading/_slot_form.html        the fill-in and choice forms
static/web/generate.js                         the flow
static/web/entries.js                          the slot add buttons and Add option
static/web/reorder.js                          a choice moves with its options
static/styles/design/generate.css              the modal and the slot rows
multimedia/api/tatib/serializers.py            kind read-only, derive on create
multimedia/web/test_tatib_templates.py         the unit suite
tests/e2e/test_tatib_templates.py              the browser suite
docs/spec/reading.md                           the new requirements, at Fold
backlog/items/ITEM-181-tata-ibadah-templates.md  the card
backlog/board.md, specs/README.md              the rows
VERSION, CHANGELOG.md                          1.24.0 and its line, at delivery
```

### Structure Decision

No new app: the type, the slots and the generate flow all belong to `multimedia.tatib` and its reading
surface, which already owns the service order, the entry editors and the projector. The only new files are
the two client assets, the two fragments, the two test modules, the migration and this spec pack — each in
the directory the repo already uses for that kind of file.
