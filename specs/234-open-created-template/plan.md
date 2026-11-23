# Implementation Plan: a created Template opens on the reading stage

**Spec**: `specs/234-open-created-template/spec.md`
**Branch**: `feat/234-open-created-template`
**Bump**: `patch`
**Preview**: `specs/234-open-created-template/preview/` — live at `http://127.0.0.1:8774/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla ES5-style browser JavaScript |
| Primary dependencies | none added — the existing `static/web/reading.js` shell |
| Storage | no schema change; `record_kind` and `created` already arrive in the save response |
| Testing | Django runner; Playwright Python E2E through `StaticLiveServerTestCase`, throwaway database `gkps234` |
| Target platform | the reading pages in a desktop browser (review viewport 1440×900) |
| Project type | server-rendered Django templates with an in-place JS shell |
| Performance goals | one extra string concatenation on create; no extra fetch, no reload |
| Constraints | R46's other clauses stand; dated create, edits, refusals, generate and copy keep their paths |
| Scale / scope | one condition in one listener; one E2E class; R46 is modified at Fold |

## Constitution Check

No `CONSTITUTION.md` at the repository root — the constitution is optional and never auto-created
(SDD-01), so there are no principles to check. The table is empty by absence, not by waiver.

Re-checked after Phase 1: n/a — no constitution exists.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity changes; documents the existing kind/response fields read by the
  client.
- `contracts/` — `none` — no new interface; the save response and `navigate()` already exist.
- `quickstart.md` — preview and E2E commands against the dedicated database.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/reading.js` → `editor:saved`; `tests/e2e/test_editor.py` | `test` → `EditorE2ETests.test_a_created_template_opens_on_the_stage` | rewrite of the superseded assertion |
| FR-002 | `reading/views.py` → `TatibView`; `tests/e2e/test_editor.py` | `test` → `test_an_empty_created_template_shows_its_add_actions`, `test_a_created_template_restores_focus_to_its_row` | name, current row, actions, child pane |
| FR-003 | `static/web/reading.js` → `navigate(..., {kind:'service'})`; `tests/e2e/test_editor.py` | `test` → `test_a_created_template_open_does_not_reload_the_document` | marker, `timeOrigin`, `data-nav` |
| FR-004 | `tests/e2e/test_editor.py`, `tests/e2e/test_tatib_templates.py` | `test` → `test_a_created_service_opens_on_the_stage`, `test_an_edit_keeps_the_stage`, `test_a_refused_create_keeps_the_stage`, `test_a_failed_create_keeps_the_stage`, `test_a_fill_in_and_a_choice_settle_then_create`, `test_copy_as_template_asks_and_copies` | existing cases stay green |
| FR-005 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_from_template_list_opens_on_the_stage` | mode button still pressed |
| SC-001 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_opens_on_the_stage`, `test_a_created_template_restores_focus_to_its_row` | URL, name, current row, `data-ch` |
| SC-002 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_open_does_not_reload_the_document` | marker alive, `timeOrigin` equal |
| SC-003 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_from_template_list_opens_on_the_stage` | `#tatibMode` pressed |
| SC-004 | `tests/e2e/test_editor.py`, `tests/e2e/test_tatib_templates.py` | `test` → the six FR-004 cases above | |
| US1/AC1 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_opens_on_the_stage` | one save, no second click |
| US1/AC2 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_from_template_list_opens_on_the_stage` | |
| US1/AC3 | `tests/e2e/test_editor.py` | `test` → `test_an_empty_created_template_shows_its_add_actions` | invitation and add actions |
| US2/AC1 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_open_does_not_reload_the_document` | |
| US2/AC2 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_restores_focus_to_its_row` | quiet focus and `row-flash` |
| US2/AC3 | `tests/e2e/test_editor.py` | `test` → `test_a_created_template_opens_its_contents_pane` | `data-ch="open"` |
| US3/AC1 | `tests/e2e/test_editor.py` | `test` → `test_a_created_service_opens_on_the_stage` | dated create unchanged |
| US3/AC2 | `tests/e2e/test_editor.py` | `test` → `test_an_edit_keeps_the_stage` | edits unchanged |
| US3/AC3 | `tests/e2e/test_editor.py` | `test` → `test_a_refused_create_keeps_the_stage`, `test_a_failed_create_keeps_the_stage` | errors unchanged |
| US3/AC4 | `tests/e2e/test_tatib_templates.py` | `test` → `test_a_fill_in_and_a_choice_settle_then_create`, `test_copy_as_template_asks_and_copies` | generate/copy unchanged |
| D002 seam | `static/web/reading.js`, `multimedia/web/reading/views.py` | `inspection` — only the `editor:saved` condition and URL change; `editor_save` keeps returning `record_kind` | |
| D004 level | `plan.md`, `CHANGELOG.md` at delivery | `inspection` — one user-visible fix, so `patch` and one `Fixed` line | |

**Verification split**: 19 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

### Documentation

```
specs/234-open-created-template/
  spec.md plan.md research.md data-model.md quickstart.md tasks.md
  contracts/README.md checklists/requirements.md analysis.md
  preview/ (README.md, probe.py, measure.py, serve.py, setup_db.py, clear_records.py,
            inspect_db.py, debug_chip.py, with_db.py)
```

### Source

```
static/web/reading.js                     # one condition and URL choice in editor:saved
tests/e2e/test_editor.py                  # new create cases; superseded template assertion rewritten
docs/spec/reading.md                      # R46 modified at Fold
backlog/board.md, backlog/items/ITEM-249-created-template-opens.md
VERSION, CHANGELOG.md                     # patch line at delivery
```

### Structure Decision

The behaviour lives in one listener of the existing shell, so no new module, template, endpoint or
migration is introduced. The E2E cases stay in the module that already tests spec 209's dated
create; the temporary preview scripts stay under this slice's `preview/` folder rather than in the
repo's shared `preview/` tooling, because they are tied to the dedicated `gkps234` database.
