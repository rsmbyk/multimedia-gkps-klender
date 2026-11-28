# Implementation Plan: No empty groups after the last row is deleted

**Spec**: `specs/252-empty-date-group/spec.md` — Accepted at gate 1, 2026-11-28.
**Branch**: `fix/252-empty-date-group`
**Bump**: `patch` — declared here, shown at gate 2, applied only in the pre-merge delivery commit.
**Preview**: live, measured before gate 1; values frozen in the spec's `## UI/UX`.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0.1; ES5-style vanilla JS |
| Existing patterns | in-place sidebar delete in `static/web/editors.js`; grouped templates under `multimedia/web/templates/reading/` |
| Storage | none — groups are derived render state |
| Testing | `tests.e2e.test_empty_date_group.py`, `StaticLiveServerTestCase` + Playwright Python |
| Constraints | no new dependency, route or schema; no commit before Fold; no push without a separate word |

## Constitution Check (before Phase 0)

No `CONSTITUTION.md` at the repo root — nothing to check. Complexity Tracking: empty (no violation
needs justification).

## Phase 0 — Research

See `research.md`: ten grouped surfaces surveyed, four decisions D001–D004 with rationale, alternatives
and provenance, zero unknowns. No question tool call was needed: the owner's report and the codebase
settled every item. The ambiguity scan found no category research could not decide.

## Phase 1 — Design

`data-model.md` (no state), `contracts/none.md`, `quickstart.md` (runnable commands). The preview components
are the design: the live 8776 worktree is the real delete path, 8777 is the unmodified control, and the
probe results are the accepted `UI/UX` values. The design follows those components rather than inventing
a new rendering.

## Constitution Check (after Phase 1)

Unchanged: still no constitution; no Complexity Tracking entry added.

## Traceability

Verification split: **5 test · 9 inspection · 1 manual**.

| Requirement / scenario | Component | Verified by |
| --- | --- | --- |
| US1/AC1 — last service in a bucket | preview 8776 `date-bucket` `after-last-delete`; `static/web/editors.js` | `inspection` — `probe-results.jsonl` vs `probe-results-base.jsonl`; section count 1→0 vs 1→1 |
| US1/AC2 — fresh render agrees | preview 8776 `date-bucket` `after-reload`; `multimedia/web/reading/date_buckets.py:57` | `inspection` — both servers report `last-30-days` = 0 after reload |
| US1/AC3 — filtered bucket | preview 8776 `filtered` states; `static/web/reading.js:949-963` | `inspection` — `bucketHidden` false→true→false, visible rows 1→0→2 |
| US2/AC1 — last songbook | preview 8776 `songbooks`; shared `applyDelete()` | `inspection` — sections 2→1 vs control 2→2 |
| US2/AC2 — no empty Templates | preview 8776 `templates`; `_tatib_groups()` | `inspection` — sections 1→0 on screen and reload vs control 1→1 |
| US2/AC3 — other grouped surfaces | `research.md` survey table | `inspection` — look at each cited path/line for a delete path or an empty-group guard |
| FR-001 — client retires section | `static/web/editors.js` `applyDelete()` | `test` — `tests.e2e.test_empty_date_group.EmptyDateGroupE2ETests.test_deleting_the_last_service_in_a_bucket_removes_its_heading` and `…test_deleting_the_last_songbook_removes_its_unheaded_group` |
| FR-002 — hide filtered group | `static/web/editors.js` | `test` — `…test_deleting_the_last_visible_row_hides_a_filtered_group` |
| FR-003 — no empty Templates render | `multimedia/web/reading/views.py` `_tatib_groups()` | `test` — `…test_deleting_the_last_template_leaves_no_empty_group` |
| FR-004 — other surfaces unchanged | two edited files only | `inspection` — `git diff --name-only` against base, checked with the survey |
| SC-001 — red→green | four-pin module | `test` — `preview/run-tests.py tests.e2e.test_empty_date_group` on base and slice |
| SC-002 — neighbours | `tests.e2e.test_deleted_stage`, `tests.e2e.test_song_sort_retained` | `test` — run both modules on the slice; with A3's test-only selector correction both are green, and the same corrected test is green on unmodified base |
| SC-003 — audit coverage | `research.md` | `inspection` — ten rows, each with file/line evidence |
| UI/UX values | preview probe outputs | `inspection` — read both JSONL files; numbers match the spec table |
| Production confirmation | live sidebar after deployment | `manual` — open Tata Ibadah, delete the last service of a bucket, confirm heading disappears |

## Plan exit gate (seven checks)

1. Requirement coverage — every FR/SC/scenario has a row: pass.
2. Entity coverage — `n/a`, no stored entities: pass.
3. Interface coverage — `contracts/none.md`: pass.
4. Decision provenance — D001–D004 each name rationale, alternatives and provenance: pass.
5. Constitution conformance — no constitution, no violations: pass.
6. Zero unknowns — research exit: pass.
7. Verification declared — split above, with file/function or explicit steps: pass. Runnability of
   `quickstart.md`: all commands executed on this machine before gate 1.

No code is written in Plan and `tasks.md` is not created here; both were handled after gate 1.
