# Implementation Plan — spec 255

**Slice**: `specs/255-use-template-progress-persist`
**Branch**: `feat/255-use-template-progress-persist`
**Spec**: accepted at Gate 1 on 2026-11-28
**Bump**: `patch` (declared here per SDD × Versioning; applied in the pre-merge delivery commit)

## Technical Context

| Item | Value |
| --- | --- |
| Language / runtime | Python 3.12 + Django 4.0 server; ES5-style vanilla JS in `static/web/generate.js` |
| Primary dependencies | None new — `localStorage` and `Date.now()` |
| Storage | `localStorage`, key `gkps:generate:<templateId>`, `v: 2`, `savedAt`, 168 h lifetime |
| Surfaces | `static/web/generate.js` (store, TTL, mark), `reading/tatib.html` (button id + dot span), `static/styles/design/components.css` (dot) |
| Test lane | Playwright E2E through `StaticLiveServerTestCase` (`tests/e2e/`) |
| Preview | `specs/255-use-template-progress-persist/preview/index.html`, all three variants |
| System boundary | Client only; no model, migration, URL, view or request change |

## Constitution Check (before Phase 0)

No `CONSTITUTION.md` exists; SDD-01 says it is never auto-created. No principles to check, so the
check passes by absence. The repo bars — no new dependencies, no template write, no new endpoint, no
colour-only state — are held by D1, D5, D7 and `contracts/none.md`.

## Phase 0 — research

`research.md` records eight decisions with rationale, alternatives and provenance. Zero unknowns.

## Phase 1 — design

`data-model.md` defines the v2 record, the 168 h rule and the button's transient state.
`contracts/none.md` declares no external interface. `quickstart.md` names the test and preview
commands.

## Constitution Check (after Phase 1)

Still passes. No dependency, endpoint or server write was added; the only new state is one JSON
value in `localStorage` plus a DOM attribute and a 7px span.

## Traceability

| ID | Component | Verified by |
| --- | --- | --- |
| US1/AC1 — survives a new browser session | `generate.js` (`saved`, `save`) | `test` — `test_progress_survives_a_new_browser_session` |
| US1/AC2 — older than seven days is gone | `generate.js` (`liveRecord`, `pruneExpired`) | `test` — `test_an_expired_record_is_ignored_and_removed` |
| US1/AC3 — an edit on day six restarts the clock | `generate.js` (`save` writes `savedAt`) | `test` — `test_a_save_on_day_six_restarts_the_clock` |
| US1/AC4 — two templates, two clocks | `generate.js` (`storageKey`) | `test` — `test_two_templates_keep_separate_clocks` |
| US2/AC1 — a live draft marks the button | `generate.js` (`paintMark`), `tatib.html` | `test` — `test_the_button_marks_a_live_draft` |
| US2/AC2 — no record, no mark | `generate.js` (`paintMark`) | `test` — `test_the_button_has_no_mark_without_a_draft` |
| US2/AC3 — the mark appears on the first save | `generate.js` (`save` → `paintMark`) | `test` — `test_the_mark_appears_after_the_first_save` |
| US2/AC4 — Create clears the mark | `generate.js` (`clearSaved` → `paintMark`) | `test` — `test_the_mark_is_gone_after_create` |
| FR-001 — localStorage, v2, timestamps | `generate.js` (`save`, `saved`) | `test` — `test_the_record_carries_a_saved_at_timestamp` |
| FR-002 — every change rewrites `savedAt` | `generate.js` (`save` call sites) | `test` — `test_every_change_refreshes_the_timestamp` |
| FR-003 — 168 h expiry, removal | `generate.js` (`liveRecord`, `pruneExpired`) | `test` — `test_an_expired_record_is_ignored_and_removed` |
| FR-004 — restore, stale ids dropped | `generate.js` (`reset`) | `test` — `test_reopening_restores_slots_step_name_and_date` |
| FR-005 — Create clears, failure keeps | `generate.js` (`submit`) | `test` — `test_the_mark_is_gone_after_create` |
| FR-006 — variant A dot geometry | `generate.js`, `tatib.html`, `components.css` | `test` — `test_the_mark_is_a_corner_dot_of_seven_pixels` |
| FR-007 — accessible name states the draft | `generate.js` (`paintMark`) | `test` — `test_the_mark_names_the_saved_draft` |
| FR-008 — live appear / clear | `generate.js` (`save`, `clearSaved`) | `test` — `test_the_mark_appears_after_the_first_save`, `test_the_mark_is_gone_after_create` |
| FR-009 — template byte-identical | no write path | `test` — `test_the_template_is_byte_identical_after_create` |
| FR-010 — storage failure is harmless | `generate.js` try/catch | `test` — `test_storage_failure_does_not_break_the_modal` |
| FR-011 — the confirmation names seven days | `_generate_modal.html` copy | `test` — `test_the_leave_confirmation_names_the_seven_day_lifetime` |
| SC-001 | E2E | `test` — `test_progress_survives_a_new_browser_session` |
| SC-002 | E2E | `test` — `test_an_expired_record_is_ignored_and_removed` |
| SC-003 | E2E | `test` — `test_a_save_on_day_six_restarts_the_clock` |
| SC-004 | E2E | `test` — `test_the_button_marks_a_live_draft`, `test_the_button_has_no_mark_without_a_draft` |
| SC-005 | E2E | `test` — `test_the_mark_is_gone_after_create` |
| SC-006 | E2E | `test` — `test_the_mark_names_the_saved_draft` |

Verification split: **24 test · 0 inspection · 0 manual**.

## Exit gate (SDD-14)

| Check | Evidence |
| --- | --- |
| Requirement coverage | All 10 FRs and 6 SCs appear above |
| Entity coverage | The record and the button state are in `data-model.md` |
| Interface coverage | `contracts/none.md` states none explicitly |
| Decision provenance | D1–D8 each carry Rationale, Alternatives, Provenance |
| Constitution conformance | No constitution; repo bars checked before and after Phase 1 |
| Zero unknowns | `research.md` ends with zero unknowns |
| Verification declared | Every row has a method and a named test; quickstart is runnable at Implement |

Plan exit passes. No code written; `tasks.md` not created here.