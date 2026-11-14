# Implementation Plan: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`
**Branch**: `feat/131-retire-break-entry`
**Bump**: `patch`
**Preview**: `specs/131-retire-break-entry/preview/` — the running branch plus the probe that measured it

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0 templates; ES5-style browser JavaScript (no build step) |
| Primary dependencies | Django forms and views; `static/styles/design/components.css`; no new library |
| Storage | none — no model, field or migration change; existing rows keep kind `3` |
| Testing | Django `TestCase` for the endpoints and the rendered markup; Playwright (Python) E2E for the tiles, the divider's controls and the delete |
| Target platform | the reading shell at any width, light and dark themes |
| Project type | server-rendered pages + in-page navigation that swaps shell fragments |
| Performance goals | none measurable: one button fewer, one grid track fewer, no new request or script |
| Constraints | saved-page parity with the server route (spec 122); spec 130's empty-state tiles are the layout |
| Scale / scope | 3 creation surfaces, 1 stylesheet rule, 1 form map, 4 test files |

## Constitution Check

`n/a — no CONSTITUTION.md in this repository` (SDD-01: optional, never auto-created).

Re-checked after Phase 1: nothing to check against; the repo's `docs/PROCESS.md` rules were applied instead
(one slice, one branch, tests before the claim, no commit before Fold).

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the kind's lifecycle table; no persisted entity, no migration
- `contracts/` — the six endpoints' behaviour for `kind=3`, and the three surfaces that must agree
- `quickstart.md` — serve the worktree, read the four surfaces, ask the endpoints, run the suites

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `tatib.html` (three add surfaces), `components.css` (`.entry__empty-actions` 5 → 4 tracks) | `test` → `multimedia/web/tests.py::ServiceEntryKindRetirementTests::test_no_page_offers_a_break` and `…::test_an_empty_service_offers_four_tiles` | markup counts, not screenshots |
| FR-002 | `static/web/entries.js` (`EMPTY_ADD_ICONS`, `EMPTY_ADD_LABELS`, the kind list) | `test` → `tests/e2e/test_entries.py::EntryEditorE2ETests::test_editing_an_entry_and_deleting_it_after_a_confirmation` (rebuilt row: 4 tiles) | the rebuild is the only client-side list |
| FR-003 | `static/web/offline-render.js` (`addButtons`, `emptyAddButtons`) | `test` → `tests/e2e/test_saved_render_parity.py` (the empty row and add row are compared surface by surface) | saved page must match the server's four |
| FR-004 | `multimedia/web/reading/entries.py` (`FORMS`, `KINDS`, `TITLES`, `SectionBreakEntryForm`), `views.py::entry_save`/`entry_form`'s existing `Http404` | `test` → `ServiceEntryKindRetirementTests::test_the_break_kind_cannot_be_created` | three shapes: bare, with `after`, with a title |
| FR-005 | the same map, through `views.py::entry_save` and `entry_form` | `test` → `ServiceEntryKindRetirementTests::test_an_existing_break_cannot_be_edited` | `404` + row byte-identical after |
| FR-006 | `views.py` (`_service_items` divider block, `_projector_data`), `tatib.html`, `_toc.html` | `test` → `tests/e2e/test_tatib_section_break.py` and `multimedia/web/tests.py::…::test_a_section_break_renders_the_same_divider_as_a_legacy_row` | untouched code, existing assertions |
| FR-007 | `views.py::entry_delete` (unchanged), `entries.js::confirmDelete` | `test` → `tests/e2e/test_tatib_section_break.py::…::test_a_break_deletes_from_its_divider` | dialog → `POST 200` → row gone, order compacted |
| FR-008 | `entries.js` drag/arrow path (unchanged) | `test` → `tests/e2e/test_reorder.py::…::test_dragging_a_section_break_from_its_divider_reorders_the_row` | existing, must stay green |
| FR-009 | `static/web/offline-render.js` (the divider and the sidebar row) | `test` → `tests/e2e/test_offline_library.py` (saved Tata Ibadah) | existing saved-page assertions |
| FR-010 | `multimedia/tatib/models.py` (unchanged) | `test` → `ServiceEntryKindRetirementTests::test_the_kind_and_its_rows_survive` | value `3`, `get_kind_display()` |
| FR-011 | `tatib.html` legacy controls, `views.py` legacy rows (unchanged) | `test` → `test_tatib_section_break.py` (legacy note) + `multimedia/web/tests.py` legacy control tests | untouched |
| SC-001 | the running branch | `test` → the markup tests + the E2E tile counts | four `data-entry-open` values, none `section_break` |
| SC-002 | `entry_save` | `test` → `test_the_break_kind_cannot_be_created` (three POSTs) | 0 rows created |
| SC-003 | the running branch | `test` → the delete E2E, `tests/e2e/test_projector.py` (the `break` screen) | one divider, one screen, one Delete |
| SC-004 | the running branch | `test` → the tile geometry test (`test_entries.py`, four 52px squares, one row) + `preview/probe_break_controls.py` re-run | add row 28px/6px; tiles 52px/10px |
| SC-005 | whole app | `test` → `manage.py test multimedia.web`, then `tests.e2e.test_entries`, `test_reorder`, `test_tatib_section_break`, `test_edit_request_feedback` | the rest of `tests/e2e` at the push step |

**Verification split**: 16 test · 0 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| The four kinds are listed in three places | the template, the live shell and the cached shell render in different environments with no shared module | a global constant would not reach an already-cached old `entries.js`, and a template tag would be one file for four strings |
| The endpoint answers `404` for a retired kind | the kind is now unknown to the writing map, which is what makes the refusal hold for every endpoint | a bespoke `410` would be a second place to remember the retirement |

## Project Structure

### Documentation

```
specs/131-retire-break-entry/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/templates/reading/tatib.html     three add surfaces, one kind fewer
static/styles/design/components.css              .entry__empty-actions: five tracks -> four
static/web/entries.js                            the rebuild's list, the icons/labels, addBreak removed
static/web/offline-render.js                     addButtons / emptyAddButtons: one kind fewer
multimedia/web/reading/entries.py                FORMS / KINDS / TITLES, SectionBreakEntryForm removed
multimedia/web/tests.py                          the retirement tests (create, edit, kind survives, markup)
tests/e2e/test_entries.py                        tile counts and labels 5 -> 4
tests/e2e/test_tatib_section_break.py            the add test becomes a no-control test; a delete test is added
tests/e2e/test_edit_request_feedback.py          the non-modal Break write test goes with the behaviour
specs/131-retire-break-entry/preview/probe_break_controls.py   the measurement probe
```

### Structure Decision

No new file on the reading pages. The retirement is a removal from lists that already exist, plus one grid
track in the shared component sheet; the probe is a slice artefact under `preview/`, not app code.
