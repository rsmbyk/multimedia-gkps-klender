# Analysis: focus only the empty search landing

**Date**: 2026-11-22
**Artifacts read**: `spec.md` `b3a9560c5c20` · `plan.md` `acadce10471d` · `research.md` `062479b06721` · `tasks.md` `03c3c320c8bf` · `checklists/requirements.md` `58d94a30e131`

**Metrics**: 6/6 FR covered · 5/5 SC covered · 7/7 acceptance scenarios traceable · **0 CRITICAL** · 0 HIGH · 2 LOW

## Coverage

| Requirement | Task | Verified by | Status |
| --- | --- | --- | --- |
| FR-001 (load, five landing routes) | T005, T006 | `test` | covered |
| FR-001 (in-page arrival) | T005, T007 | `test` | covered |
| FR-002 (value, selection, scroll) | T005 | `test` | covered |
| FR-003 (submit blurs; results never focus) | T007 | `test` | covered |
| FR-004 (reading routes unfocused) | T005 | `test` | covered |
| FR-005 (nothing else changes) | T005–T007 | `inspection` | covered |
| FR-006 (only 139's focus clause superseded) | T011 | `inspection` | covered |
| SC-001 … SC-005 | T003, T004, T008 | `test` | covered |

No requirement without a task; no task without a requirement.

## Findings

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | LOW | FR-003's sentence "blurred so it is no longer the active element as the compact field" carries a stray "as" — the meaning is unambiguous from AC5 and SC-003, but the clause reads awkwardly. | **reported, not fixed** — a spec is frozen after Gate 1 (BRD-09); folding the wording would need a re-entry at Specify. Carried here so the next touch of `reading/R15` can clean it. |
| A2 | LOW | SC-002's Search-rail test depends on no remembered search existing in the tab; a test that runs after another test in the same context could restore a snapshot and land on results instead of the landing. | **handled in T003** — the test opens a fresh `browser.new_context()` and asserts the landing state before asserting focus, so a stale snapshot fails loudly rather than silently testing the wrong surface. |

## Mechanical fixes applied

None needed: no requirement lacks a task, no terminology drift (the spec, plan and tasks all say
*landing* and use `#searchQuery`), no stale path, and no duplicate requirement.

## History

- 2026-11-22 — pass 1: 0 CRITICAL, 100% coverage, 2 LOW reported (A1 frozen-wording, A2 test isolation).