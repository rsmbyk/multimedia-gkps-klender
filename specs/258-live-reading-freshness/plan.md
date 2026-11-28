# Implementation Plan: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`
**Branch**: `feat/258-live-reading-freshness`
**Bump**: `patch`
**Preview**: `specs/258-live-reading-freshness/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0 |
| Primary dependencies | Django ORM, vanilla JS, Playwright (Python) |
| Storage | No new tables; versions from slice 254, fingerprints derived per request |
| Testing | Django test client for poll endpoints; Playwright for badge and reconciliation |
| Target platform | Reading pages and sidebars at the product's existing breakpoints |
| Project type | Server-rendered templates with vanilla JS |
| Performance goals | Four small read requests per 10 s window; no full-page polling |
| Constraints | No stage swap from sidebar changes; no persisted list state |
| Scale / scope | Four GET endpoints, one client poll loop, one badge state, three sidebar reconciliations |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | pass | No `CONSTITUTION.md` at the repo root; SDD-01 says it is optional and never auto-created. |

Re-checked after Phase 1: pass.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity; page version, list fingerprint and stale flag are derived or client-side
- `contracts/` — four read-only endpoints, including the fingerprint definition
- `quickstart.md` — focused endpoint and E2E commands plus the preview probe

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/views.py` | `test` → `multimedia/web/tests.py::FreshnessEndpointTests::test_page_version` | service and song |
| FR-002 | `multimedia/web/reading/freshness.py` | `test` → `FreshnessEndpointTests::test_list_fingerprint_shape` | three scopes |
| FR-003 | `static/web/reading.js` | `test` → `tests/e2e/test_live_reading_freshness.py::test_page_polls_at_ten_seconds` | visible page |
| FR-004 | `static/web/reading.js`, `static/styles/design/components.css` | `test` → `test_invalidation_disables_controls_and_closes_dialogs` | in place |
| FR-005 | `static/web/templates/reading/base.html` | `test` → `test_badge_wording_and_position` | top centre |
| FR-006 | `static/web/reading.js` | `test` → `test_reload_is_in_place` | document identity unchanged |
| FR-007 | `static/web/reading.js` | `test` → `test_sidebar_polls_at_ten_seconds` | three sidebars |
| FR-008 | `static/web/reading.js` | `test` → `test_reconcile_updates_removes_and_inserts` | row id keyed |
| FR-009 | `static/web/reading.js` | `test` → `test_filter_sort_scroll_survive` | panel state too |
| FR-010 | `static/styles/design/components.css` | `test` → `test_inserted_row_animation` | 180 ms sample |
| FR-011 | `multimedia/web/reading/freshness.py` | `test` → `FreshnessEndpointTests::test_template_mode_isolated` | mode scope |
| FR-012 | `static/web/reading.js` | `test` → `test_failed_poll_keeps_state` | retry next interval |
| FR-013 | `static/web/reading.js` | `test` → `test_one_request_per_endpoint_in_flight` | no pile-up |
| SC-001 | page poll path | `test` → `test_invalidation_within_ten_seconds` | second client write |
| SC-002 | invalidation path | `test` → `test_invalidation_disables_controls_and_closes_dialogs` | every dialog closed |
| SC-003 | Reload path | `test` → `test_reload_is_in_place` | no browser reload |
| SC-004 | reconciliation path | `test` → `test_unchanged_rows_keep_nodes` | node identity |
| SC-005 | insertion path | `test` → `test_alphabetical_insert_position` | G song case |
| SC-006 | sidebar state | `test` → `test_filter_sort_scroll_survive` | before/after values |
| US1/AC1–3 | page poll | `test` → `test_invalidation_within_ten_seconds` | |
| US2/AC1–3 | invalidation | `test` → `test_invalidation_disables_controls_and_closes_dialogs` | |
| US3/AC1–3 | badge and reload | `test` → `test_reload_is_in_place` | |
| US4/AC1–4 | sidebar reconciliation | `test` → `test_reconcile_updates_removes_and_inserts` | |
| US5/AC1–3 | view state | `test` → `test_filter_sort_scroll_survive` | |

**Verification split**: 24 test · 0 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/258-live-reading-freshness/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/urls.py                 four read-only poll routes
multimedia/web/reading/views.py        endpoint handlers
multimedia/web/reading/freshness.py    fingerprint helper
multimedia/web/templates/reading/      page version attributes and badge element
static/web/reading.js                  poll, invalidate, reconcile, reload
static/styles/design/components.css     badge, stale controls, inserted-row animation
tests/e2e/test_live_reading_freshness.py  user-visible acceptance
```

### Structure Decision

No new client framework: the poll loop joins the existing `reading.js` shell already responsible for in-place navigation and DOM reconciliation. The fingerprint helper lives beside the read views it serves.
