# Implementation Plan: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`
**Branch**: `feat/209-open-created-service`
**Bump**: `patch` (1.35.0 → 1.35.1)
**Preview**: n/a — no new look; gate-1 material is the live reproduction at `specs/209-open-created-service/reproduce.py`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla ES5-style JS |
| Primary dependencies | Django REST-free views, Playwright (Python) E2E |
| Storage | existing PostgreSQL/SQLite `TataIbadah` row; no schema change |
| Testing | `manage.py test tests.e2e.test_editor` with `DJANGO_DEVELOPMENT_MODE=true` (focused modules only locally) |
| Target platform | server-rendered reading app, in-page navigation stage |
| Project type | Django app with vanilla JS shell |
| Performance goals | one extra save-response field; the stage uses the same single fetch as a row click |
| Constraints | no document reload; no dock/projector state; no new model or endpoint |
| Scale / scope | one response field, one branch in the shell's save listener, focused E2E |

## Constitution Check

No `CONSTITUTION.md` exists in this repo (SDD-01); the check is recorded as not applicable.

Re-checked after Phase 1: not applicable — no principles to violate.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity added; three additive response fields documented.
- `contracts/` — the editor save response gains `created` and, for `tatib`, `record_kind`.
- `quickstart.md` — focused E2E command and the in-app reproduce probe.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/views.py`, `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_created_service_opens_on_the_stage` | URL, heading, current row, empty actions |
| FR-002 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_an_open_from_create_does_not_reload_the_document` | marker, `performance.timeOrigin`, `data-nav` |
| FR-002 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_created_service_opens_its_contents_pane` | `data-ch=open` on arrival |
| FR-003 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_an_open_from_create_keeps_the_panel_state` | mini panel and other list selection unchanged |
| FR-004 | `multimedia/web/reading/views.py`, `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_template_create_keeps_the_stage` | Template create still refreshes only |
| FR-004 | `multimedia/web/reading/views.py`, `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_an_edit_keeps_the_stage` | edit still refreshes only |
| FR-004 | `static/web/editors.js` | `inspection` — other record kinds keep their existing save event and listener path | no code change outside the additive response field |
| FR-005 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_refused_create_keeps_the_stage` | validation re-render leaves stage put |
| FR-005 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_failed_create_keeps_the_stage` | failed request leaves stage put |
| FR-006 | `static/web/generate.js`, `static/web/editors.js` | `test` → `tests/e2e/test_tatib_templates.py::test_a_fill_in_and_a_choice_settle_then_create` | generate still navigates |
| FR-006 | `static/web/editors.js` | `test` → `tests/e2e/test_tatib_templates.py::test_copy_as_template_asks_and_copies` | copy still navigates |
| SC-001 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_created_service_opens_on_the_stage` | measured values match the click-through state |
| SC-002 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_an_open_from_create_does_not_reload_the_document` | no reload, `data-nav` unchanged |
| SC-003 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_template_create_keeps_the_stage` | plus existing template/editor assertions |
| SC-004 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_refused_create_keeps_the_stage` | URL and heading unchanged |
| US1/AC1 | `tests/e2e/test_editor.py` | `inspection` — `test_add_empty_active_tatib` clicks the `.book` row explicitly after the stage is populated | avoids a strict-mode text match on row and heading |

**Verification split**: 14 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/209-open-created-service/spec.md
specs/209-open-created-service/plan.md
specs/209-open-created-service/research.md
specs/209-open-created-service/data-model.md
specs/209-open-created-service/quickstart.md
specs/209-open-created-service/tasks.md
specs/209-open-created-service/contracts/README.md
specs/209-open-created-service/contracts/save-response.md
specs/209-open-created-service/checklists/requirements.md
specs/209-open-created-service/reproduce.py
```

### Source

```
multimedia/web/reading/views.py   additive fields in editor_save's JSON answer
static/web/reading.js             one branch in the editor:saved listener
tests/e2e/test_editor.py          focused create/edit/refusal scenarios
docs/spec/reading.md              Fold target: new reading/R46
```

### Structure Decision

No new directory: the response field lives with the existing editor endpoint, the navigation branch
with the shell's save listener, and the tests with the existing sidebar-editor E2E module. The
capability tree gets one new requirement rather than a rewrite of `reading/R9`, because this is a
navigation act, not a change to list grouping.
