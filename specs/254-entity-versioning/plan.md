# Implementation Plan: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`
**Branch**: `feat/254-entity-versioning`
**Bump**: `patch`
**Preview**: `specs/254-entity-versioning/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, Django REST Framework |
| Primary dependencies | Django ORM and ModelForm; PostgreSQL; Playwright (Python) for E2E |
| Storage | PostgreSQL via the compose stack; six new integer columns, no new tables |
| Testing | Django `TestCase` through the test client; Playwright Python E2E |
| Target platform | The existing reading site and OBS surfaces, desktop and phone widths |
| Project type | Server-rendered Django templates with vanilla JS |
| Performance goals | No new polling in this slice; version writes stay inside the existing request |
| Constraints | Anonymous writes stay allowed; public-write decision unchanged. No history table. |
| Scale / scope | Six models, every product write path to those models, one shared count helper |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | pass | No `CONSTITUTION.md` exists at the repo root; SDD-01 says it is optional and never auto-created. |

Re-checked after Phase 1: pass — no constitution file was created, and no new dependency was introduced.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — six version columns plus two derived values (expected version, distinct-service count)
- `contracts/` — `http.md` for the `expected_version` field and 409 body; no new public API route
- `quickstart.md` — focused endpoint tests, E2E notice test and the preview probe

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/{tatib,songs}/models.py` + migration | `test` → `multimedia/web/tests.py::VersionFieldTests::test_all_six_models_have_version` | version defaults to 1 |
| FR-002 | save paths in `multimedia/web/reading/views.py`, `verses.py` | `test` → `multimedia/web/tests.py::VersionFieldTests::test_identical_save_leaves_version` | stored-value comparison |
| FR-003 | shared version guard in `multimedia/web/reading/views.py` | `test` → `multimedia/web/tests.py::VersionGuardTests::test_stale_write_returns_409` | 409, no write |
| FR-004 | transaction and row-lock blocks on every guarded write | `inspection` — each guarded view locks the target row before comparing | no test for lock primitive itself |
| FR-005 | entry-create path in `multimedia/web/reading/views.py` | `test` → `multimedia/web/tests.py::VersionGuardTests::test_create_checks_parent_version` | parent version only |
| FR-006 | `TataIbadah.version` bump on entry and legacy-item writes | `test` → `multimedia/web/tests.py::ServiceVersionTests::test_child_writes_bump_service` | includes reorder |
| FR-007 | propagation helper for song and verse writes | `test` → `multimedia/web/tests.py::ServiceVersionTests::test_song_change_bumps_all_referencing_services` | dated services and templates |
| FR-008 | `verses.py` delete guard | `test` → `multimedia/web/reading/test_verses.py::test_referenced_verse_delete_refused` | existing refusal stays |
| FR-009 | `editor_delete` for song | `test` → `multimedia/web/tests.py::DeleteGuardTests::test_referenced_song_delete_refused` | |
| FR-010 | `editor_delete` for songbook | `test` → `multimedia/web/tests.py::DeleteGuardTests::test_referenced_songbook_delete_refused` | |
| FR-011 | shared distinct-service count helper | `test` → `multimedia/web/tests.py::DeleteGuardTests::test_count_is_distinct_services` | two entries in one service count once |
| FR-012 | delete confirmation template and E2E | `test` → `tests/e2e/test_verse_reference_notice.py::test_notice_and_disabled_delete_for_song_and_songbook` | 560px width from preview |
| FR-013 | conflict response body | `test` → `multimedia/web/tests.py::VersionGuardTests::test_conflict_body` | error, message, current_version |
| FR-014 | schema migration | `test` → `multimedia/songs/test_migrations.py::test_version_columns_default_to_one` | also for tatib models |
| FR-015 | all guarded write paths | `inspection` — every endpoint in `multimedia/web/urls.py` that writes a tracked row calls the shared guard | no unguarded path remains |
| SC-001 | version guard | `test` → `VersionGuardTests::test_409_leaves_row_untouched` | |
| SC-002 | dirty comparison | `test` → `VersionFieldTests::test_no_op_save_keeps_version` | |
| SC-003 | service bump helper | `test` → `ServiceVersionTests::test_one_increment_per_change` | |
| SC-004 | count helper | `test` → `DeleteGuardTests::test_count_dedupes_entries_and_counts_templates` | |
| SC-005 | delete guards | `test` → `DeleteGuardTests::test_all_three_refusals` | |
| SC-006 | migration | `test` → `test_version_columns_default_to_one` | |
| US1/AC1–3 | version columns and migrations | `test` → `VersionFieldTests` | story covered by FR-001, FR-002, FR-014 |
| US2/AC1–3 | no-op comparison | `test` → `VersionFieldTests::test_no_op_save_keeps_version` | |
| US3/AC1–3 | stale write guard | `test` → `VersionGuardTests::test_stale_write_returns_409` | |
| US4/AC1–4 | service and child writes | `test` → `ServiceVersionTests::test_child_writes_bump_service` | |
| US5/AC1–3 | song-side propagation | `test` → `ServiceVersionTests::test_song_change_bumps_all_referencing_services` | |
| US6/AC1–4 | deletion refusal endpoints | `test` → `DeleteGuardTests` | |
| US7/AC1–4 | distinct-service notice | `test` → `DeleteGuardTests::test_count_is_distinct_services` | |
| US8/AC1–3 | confirmations and verse modal | `test` → `tests/e2e/test_verse_reference_notice.py` | disabled Delete and aria link |

**Verification split**: 27 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/254-entity-versioning/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/tatib/models.py             version on TataIbadah, TataIbadahItem, ServiceEntry
multimedia/songs/models.py             version on Book, Song, Verse
multimedia/*/migrations/               add version columns
multimedia/web/reading/views.py        expected-version guard, count helper, delete guards
multimedia/web/reading/verses.py       verse write guards and propagation
multimedia/web/templates/reading/      delete confirmation notice
static/styles/design/components.css    560px confirmation width
```

### Structure Decision

No new module: the guard, count helper and propagation helper live beside the write views they protect, reusing the existing `reading` package. The shared helper avoids one copy of the check per endpoint.
