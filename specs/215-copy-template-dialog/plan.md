# Implementation Plan: the copy confirmation as a dialog of its own, and the copy's name

**Spec**: `specs/215-copy-template-dialog/spec.md`
**Branch**: `feat/215-copy-template-dialog`
**Bump**: `minor` — the product gains something it could not do: name the template at the moment it is copied. Not `patch`, because a patch would claim nothing new is possible; not `major`, because nothing that worked stops working.
**Preview**: `static preview at specs/215-copy-template-dialog/preview/index.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla ES5-style JS (no build step), hand-written CSS |
| Primary dependencies | none new; Playwright (Python) is already the E2E lane |
| Storage | no schema change, no migration, no data touched |
| Testing | `manage.py test multimedia.web.test_tatib_templates` and `tests.e2e.test_tatib_templates` |
| Target platform | the server-rendered reading app; the editor `<dialog>` at 480px, in a top layer |
| Project type | Django app, one shared `<dialog>`, hand-written design sheets |
| Performance goals | none — one extra JSON field on an existing POST, no new request, no new asset |
| Constraints | the generate page's confirmation is untouched; spec 212's card keeps its width, padding, fill and shadow; no new design token |
| Scale / scope | 1 template, 1 view, 1 endpoint, 1 JS handler block, 1 CSS block, 1 unit test module, 1 E2E module, 2 capability requirements modified |

## Constitution Check

No `CONSTITUTION.md` exists in this repo (SDD-01), so the check is recorded as not applicable.

Re-checked after Phase 1: not applicable — no principles to violate.

## Phase 0 — Research

See [`research.md`](research.md). **Unknowns remaining: 0.** Eight decisions: the layer's DOM home (D001), the scrim's strength (D002), how the name travels (D003), what a nameless request does (D004), where the default is computed (D005), Escape and the scrim without closing the dialog (D006), the card's radius (D007), and what happens to 212's two geometry tests (D008).

## Phase 1 — Design

- [`data-model.md`](data-model.md) — no entity added, changed or removed; `TataIbadah` keeps its shape, and the only new rule is on the copy's `name` at the endpoint.
- [`contracts/README.md`](contracts/README.md) — the copy endpoint's request body, its failure table, the `copy_name` context key, and the `[data-copy-*]` hooks the JS addresses.
- [`quickstart.md`](quickstart.md) — the two focused test commands, the preview build and probe, and what each proves.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` (`.editor__confirm-layer`) | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_covers_the_window` | layer rect equals the viewport, `position: fixed` |
| FR-002 | `components.css`, `static/web/editors.js` | `test` → same test | `elementFromPoint` at the form's Save lands inside the layer; the dialog's title is still in the DOM and rendered |
| FR-003 | `multimedia/web/reading/views.py::_editor_fragment_context`, `reading/_copy_confirm.html` | `test` → `multimedia/web/test_tatib_templates.py::test_the_confirmation_offers_the_source_name_plus_copy` | 57-character trim + ` (Copy)` |
| FR-004 | `static/web/editors.js` | `test` → `tests/e2e/test_tatib_templates.py::test_the_name_selects_itself_on_the_first_click`, `::test_a_second_click_places_a_caret` | selection `[0, len]`, then a caret |
| FR-005 | `views.py::tatib_copy_as_template` | `test` → `multimedia/web/test_tatib_templates.py::test_a_copy_takes_the_posted_name` | source unchanged |
| FR-006 | `static/web/editors.js` | `test` → `tests/e2e/test_tatib_templates.py::test_a_blank_name_cannot_be_accepted` | accept `disabled` |
| FR-007 | `_copy_confirm.html` (`maxlength`), `views.py` | `test` → `multimedia/web/test_tatib_templates.py::test_a_copy_refuses_a_blank_name`, `::test_a_copy_refuses_a_name_over_64_characters` | the server refuses even when the field is bypassed |
| FR-008 | `reading/_copy_confirm.html` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_card_matches_the_preview` | the lead, the field, the three facts and the answers, in that order |
| FR-009 | `static/web/editors.js` (`cancel` listener) | `test` → `tests/e2e/test_tatib_templates.py::test_escape_closes_the_confirmation_and_not_the_dialog` | dialog stays open |
| FR-010 | `components.css` | `test` → `tests/e2e/test_tatib_templates.py::test_the_copy_confirmation_card_matches_the_preview` | 448 × 349.7, 22px, 14px radius |
| FR-011 | `static/web/editors.js` | `test` → `tests/e2e/test_tatib_templates.py::test_the_scrim_closes_the_confirmation` | a click on the card does not |
| SC-001 | as FR-001 | `test` → the same E2E test | layer rect equals `window.innerWidth/innerHeight` |
| SC-002 | as FR-001 | `test` → the same E2E test | card centre within 1px of the viewport centre, in both dialog sizes |
| SC-003 | `components.css` scrim | `inspection` — open the preview in dark and light and read the Edit dialog's title through the scrim; it must be legible, not a silhouette | pixel-sampled in research D002 |
| SC-004 | `components.css`, `editors.js` | `test` → the same E2E test | dialog height equal before open and after close, to 0.1px |
| SC-005 | `views.py::_editor_fragment_context` | `test` → `::test_the_confirmation_offers_the_source_name_plus_copy` | the field's value |
| SC-006 | `editors.js` | `test` → `::test_the_name_selects_itself_on_the_first_click` | `[0, len]` |
| SC-007 | `views.py` | `test` → `::test_a_copy_takes_the_posted_name` and `tests/e2e/...::test_the_typed_name_names_the_copy` | unit and end-to-end |
| SC-008 | `editors.js` | `test` → `::test_a_blank_name_cannot_be_accepted` | disabled for spaces-only |
| SC-009 | `views.py::_editor_fragment_context` | `test` → `::test_a_long_source_name_is_trimmed_to_fit_the_copy_name` | 64 characters ending in ` (Copy)` |
| SC-010 | `editors.js` | `test` → `::test_the_scrim_closes_the_confirmation` | scrim closes, card does not |
| US1/AC1 | `components.css` | `test` → `::test_the_copy_confirmation_covers_the_window` | same as FR-001 |
| US1/AC2 | `components.css` | `inspection` — the Edit dialog's title through the scrim, dark and light | same as SC-003 |
| US1/AC3 | `components.css` | `test` → `::test_the_copy_confirmation_covers_the_window` | `elementFromPoint` at Save |
| US1/AC4 | `components.css` | `test` → `::test_the_copy_confirmation_covers_the_window` | measured at 1440×900 and at 900×700 |
| US2/AC1 | `views.py` | `test` → `::test_the_confirmation_offers_the_source_name_plus_copy` | same as FR-003 |
| US2/AC2 | `editors.js` | `test` → `::test_the_name_selects_itself_on_the_first_click` | |
| US2/AC3 | `editors.js` | `test` → `::test_a_second_click_places_a_caret` | |
| US2/AC4 | `views.py` | `test` → `::test_a_copy_takes_the_posted_name` | |
| US2/AC5 | `editors.js` | `test` → `::test_a_blank_name_cannot_be_accepted` | |
| US2/AC6 | `views.py` | `test` → `::test_a_template_copy_keeps_its_slots` (existing) plus the E2E copy flow on a template | a template copies as a template |
| US3/AC1 | `_copy_confirm.html` | `test` → `::test_the_copy_confirmation_card_matches_the_preview` | the children's order |
| US3/AC2 | `editors.js` | `test` → `::test_the_scrim_closes_the_confirmation`, `::test_copy_as_template_asks_and_copies` | Cancel discards, accept copies |

**Verification split**: 30 test · 2 inspection · 0 manual

The two `inspection` rows are the same claim seen twice (SC-003 and US1/AC2): whether the edit dialog
is *legible* through the scrim is a judgement a screenshot answers and an assertion does not. Its
number — the scrim's `.26` and the sampled pixel values — is in research D002, so the judgement has
evidence behind it.

## Complexity Tracking

No violations. The slice touches one endpoint, one template, one JS block and one CSS block, and adds
no abstraction: the name travels as one JSON field, the default is one f-string, and the layer is one
`position: fixed` rule.

## Project Structure

### Documentation

```
specs/215-copy-template-dialog/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/README.md
  checklists/requirements.md
  preview/{index.html,preview.css,preview.js,build.py,probe.py,fragments.json,README.md,tokens.css,components.css}
```

### Source

```
multimedia/web/
  templates/reading/_copy_confirm.html     the dialog: lead, Name field, three facts, answers
  templates/reading/_editor_form.html      unchanged (the include already sits inside .editor__body)
  reading/views.py                         _editor_fragment_context gains `copy_name`;
                                           tatib_copy_as_template reads the posted name
static/
  styles/design/components.css             .editor__confirm-layer becomes the window's layer;
                                           the card takes the Name field and 14px
  web/editors.js                           the copy block: select-on-click, blank-name guard,
                                           JSON body, cancel/scrim close without closing the dialog
multimedia/web/test_tatib_templates.py     five new endpoint and context tests
tests/e2e/test_tatib_templates.py          two rewritten geometry tests, five new behaviour tests
```

### Structure Decision

The real directories, unchanged from the repo's own layout: the markup stays in
`multimedia/web/templates/reading/`, the rules in `static/styles/design/components.css` (the sheet
`components.css` already carries this surface in, per spec 212), the behaviour in
`static/web/editors.js` (the only file that addresses `[data-copy-*]`), and the two lanes' tests where
the repo already puts them (`<app>/tests` and `tests/e2e/`). No new module, no new asset, no new
package.
