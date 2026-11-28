# Implementation Plan — spec 253

**Slice**: `specs/253-use-template-progress`
**Branch**: `feat/253-use-template-progress`
**Spec**: accepted at Gate 1 on 2026-11-28
**Bump**: `patch` (declared here per SDD × Versioning; applied in the pre-merge delivery commit)

## Technical Context

| Item | Value |
| --- | --- |
| Language / runtime | Python 3.12 + Django 4.0 server; ES5-style vanilla JS in `static/web/generate.js` (no build step) |
| Primary dependencies | None new — browser `sessionStorage`, already in every target browser |
| Storage | `sessionStorage`, key `gkps:generate:<templateId>`, one record per template |
| Test lane | Playwright E2E through `StaticLiveServerTestCase` (`tests/e2e/`), per the repo's TDD scope block |
| Preview | Static page built from the repo's own CSS and modal markup; `static preview at specs/253-use-template-progress/preview/index.html` |
| System boundary | Client only: no model, migration, URL, view or request payload change |

## Constitution Check (before Phase 0)

No `CONSTITUTION.md` exists at the repo root and SDD-01 says it is never auto-created. There are no
constitutional principles to check; the check passes by absence. The repo's own quality bars — no new
dependencies, template stays byte-identical, no new server interface — are satisfied by research D1,
D2 and the `contracts/none.md` declaration.

## Phase 0 — research

`research.md` records eight decisions, each with rationale, alternatives and provenance. Zero unknowns.
No question was deferred, so no owner input is pending.

## Phase 1 — design

`data-model.md` defines the client record and its write/remove/read points. `contracts/none.md`
declares no external interface. `quickstart.md` links both and names the E2E and preview commands.

## Constitution Check (after Phase 1)

Still passes. Phase 1 introduced no dependency, no new endpoint and no write to a server record;
the only state is a versioned JSON value in `sessionStorage`, removed on successful Create.

## Traceability

Every FR, SC and story scenario, with its component and verification method.

| ID | Component | Verified by |
| --- | --- | --- |
| US1/AC1 — settled slot written immediately | `static/web/generate.js` (`save`) | `test` — `tests/e2e/test_use_template_progress.py::test_settling_a_slot_writes_progress_for_that_template` |
| US1/AC2 — reopen restores slots, step, name, date | `static/web/generate.js` (`restore`, `open`) | `test` — `::test_reopening_restores_slots_step_name_and_date` |
| US1/AC3 — two templates independent | `static/web/generate.js` (`storageKey`) | `test` — `::test_two_templates_hold_separate_progress` |
| US1/AC4 — session boundary clears progress | browser `sessionStorage` | `test` — `::test_a_new_browser_context_starts_empty` |
| US2/AC1 — close paths show the confirmation | `_generate_modal.html` layer + `generate.js` (`attemptClose`) | `test` — `::test_cancel_backdrop_and_escape_each_show_the_leave_confirm` |
| US2/AC2 — Stay keeps modal and slots | `generate.js` (`data-leave-stay`) | `test` — `::test_stay_keeps_the_modal_and_the_settled_rows` |
| US2/AC3 — Leave closes without discarding | `generate.js` (`data-leave-accept`) | `test` — `::test_leave_closes_and_the_progress_survives` |
| US2/AC4 — a clean modal closes silently | `generate.js` (`attemptClose` dirty check) | `test` — `::test_a_clean_modal_closes_without_a_confirm` |
| FR-001 | `generate.js` (`storageKey`) | `test` — `::test_progress_is_keyed_by_template_id` |
| FR-002 | `generate.js` (`save` call sites) | `test` — `::test_every_slot_name_and_date_change_rewrites_progress` |
| FR-003 | `generate.js` (`save` payload) | `test` — `::test_the_saved_record_holds_slots_step_name_and_date` |
| FR-004 | `generate.js` (`restore`) | `test` — `::test_reopening_restores_slots_step_name_and_date` |
| FR-005 | `generate.js` (`restore` id filter) | `test` — `::test_a_slot_removed_from_the_template_is_ignored_on_restore` |
| FR-006 | `_generate_modal.html` + `generate.js` (`attemptClose`) | `test` — `::test_cancel_backdrop_and_escape_each_show_the_leave_confirm` |
| FR-007 | `generate.js` (`data-leave-stay`, `data-leave-accept`) | `test` — `::test_stay_keeps_the_modal_and_the_settled_rows` |
| FR-008 | `generate.js` (`submit` success) | `test` — `::test_a_successful_create_clears_that_templates_progress` |
| FR-009 | no write path added | `test` — `::test_the_template_is_byte_identical_after_close_and_create` |
| SC-001 | E2E | `test` — `::test_two_templates_hold_separate_progress` |
| SC-002 | E2E | `test` — `::test_a_reload_restores_progress` |
| SC-003 | E2E | `test` — `::test_a_clean_modal_closes_without_a_confirm` |
| SC-004 | E2E | `test` — `::test_cancel_backdrop_and_escape_each_show_the_leave_confirm` |
| SC-005 | E2E | `test` — `::test_a_successful_create_clears_that_templates_progress` |

Verification split: **22 test · 0 inspection · 0 manual**.

## Exit gate (SDD-14)

| Check | Evidence |
| --- | --- |
| Requirement coverage | All 9 FRs and 5 SCs appear above |
| Entity coverage | The one new entity (template progress) is in `data-model.md`; unchanged entities named |
| Interface coverage | `contracts/none.md` states none explicitly |
| Decision provenance | Every D1–D8 in `research.md` has a Rationale, Alternatives and Provenance |
| Constitution conformance | No constitution; repo quality bars checked before and after Phase 1 |
| Zero unknowns | `research.md` ends with zero unknowns; no deferred question |
| Verification declared | Every row has a method and a named test; quickstart commands are runnable at Implement |

Plan exit passes. No code has been written and `tasks.md` is not created here.
