# Implementation Plan: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`
**Branch**: `feat/225-open-created-songbook-song`
**Bump**: `patch` (1.36.10 → 1.36.11)
**Preview**: n/a — no new look; gate-1 material is the live reproduction in `reproduce.py`/`probe_click.py`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla ES5-style JS |
| Primary dependencies | Django views, Playwright (Python) E2E |
| Storage | existing `Book`/`Song` rows; no schema change |
| Testing | `manage.py test tests.e2e.test_editor` (focused modules locally) |
| Target platform | server-rendered reading app with in-page navigation |
| Performance goals | no extra request: the create already returns id/kind/created |
| Constraints | no document reload; no new endpoint; no change to other save paths |
| Scale / scope | one branch in the shell's save listener, focused E2E, capability fold |

## Constitution Check

No `CONSTITUTION.md` exists in this repo (SDD-01); the check is recorded as not applicable;
re-checked after Phase 1: not applicable.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity added; the existing save response is the boundary fact.
- `contracts/save-response.md` — no field added; documents the fields used.
- `quickstart.md` — focused E2E command and the two live probes.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_created_songbook_opens_in_the_panel` | current row, `data-ch=open` |
| FR-002 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_created_song_opens_on_the_stage` | URL, heading, row, `data-read` |
| FR-003 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_an_open_from_create_does_not_reload_the_document` | marker, timeOrigin, `data-nav` |
| FR-003 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_created_songbook_keeps_the_stage` | songbook open does not swap stage |
| FR-004 | `static/web/reading.js` | `test` → existing spec-209 scenarios in `tests/e2e/test_editor.py`, plus new edit scenario | other paths unchanged |
| FR-005 | `static/web/reading.js` | `test` → `tests/e2e/test_editor.py::test_a_refused_songbook_create_keeps_the_selection` | validation re-render leaves state put |
| SC-001..004 | `static/web/reading.js` | `test` → the new scenarios above | measured values match click-through state |

**Verification split**: 6 test · 0 inspection · 0 manual.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/225-open-created-songbook-song/spec.md
specs/225-open-created-songbook-song/plan.md
specs/225-open-created-songbook-song/analysis.md
specs/225-open-created-songbook-song/research.md
specs/225-open-created-songbook-song/data-model.md
specs/225-open-created-songbook-song/quickstart.md
specs/225-open-created-songbook-song/tasks.md
specs/225-open-created-songbook-song/fold.md
specs/225-open-created-songbook-song/converge.md
specs/225-open-created-songbook-song/reproduce.py
specs/225-open-created-songbook-song/probe_click.py
specs/225-open-created-songbook-song/contracts/save-response.md
specs/225-open-created-songbook-song/checklists/requirements.md
```

### Source

```
static/web/reading.js          one branch in the editor:saved listener
tests/e2e/test_editor.py       focused create/edit/refusal scenarios
docs/spec/reading.md           Fold target: new reading/R53
backlog/board.md               Ready → In review → Done with the slice
VERSION, CHANGELOG.md          patch bump and release note
```

### Structure Decision

No new directory: the navigation branch belongs with the shell's existing save listener, and the
tests with the sidebar-editor E2E module. The capability tree gets one new requirement for the two
create-open acts, since both are the same navigation rule applied to a different row kind.
