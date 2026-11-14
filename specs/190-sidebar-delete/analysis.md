# Analysis: Sidebar Delete Buttons

**Spec**: `specs/190-sidebar-delete/spec.md`
**Plan**: `specs/190-sidebar-delete/plan.md`
**Tasks**: `specs/190-sidebar-delete/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | coverage | plan/tasks | Exact soft-delete mechanism (field vs method) per model to be confirmed against existing patterns during implementation. | Resolved in implementation: `Book`/`Song` soft-delete via `SoftDeleteModel.delete()` (their own manager hides them everywhere); a `TataIbadah` leaves the lists via `is_active=False`, the flag its readers already filter on. |
| A2 | LOW | ui | plan/tasks | FR-004 selector scoping must avoid hiding `.book__s` for non-tatib contexts (e.g. songbook short names) while ensuring tatib dated rows hide date on hover/focus reveal. | Implement with scoped selectors; verify in preview/manual. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T005,T006,T008 | delete controls on eligible rows |
| FR-002 | ✅ | ✅ T005,T006,T008 | editor/hymn guards preserved |
| FR-003 | ✅ | ✅ T005,T006,T008,T009 | alongside edit, hover/focus reveal |
| FR-004 | ✅ | ✅ T009 | hide dated tatib date on hover/focus |
| FR-005 | ✅ | ✅ T001,T010 | confirm in shared modal |
| FR-006 | ✅ | ✅ T010 | noun by kind |
| FR-007 | ✅ | ✅ T007,T008,T010 | template kind distinguishable |
| FR-008 | ✅ | ✅ T002,T003 | POST + CSRF |
| FR-009 | ✅ | ✅ T002,T003 | GET confirm + POST delete endpoints |
| FR-010 | ✅ | ✅ T010 | remove from correct panel |
| FR-011 | ✅ | ✅ T010,T011 | on-stage history replace |
| FR-012 | ✅ | ✅ T001,T004 | reuse modal classes/structure |
| FR-013 | ✅ | ✅ T009,T013 | responsive/touch preserved |
| SC-001–SC-005 | ✅ | ✅ T012,T013 | verification/inspection |

**Coverage**: 100% mapped · **CRITICAL**: 0 · **HIGH/MED/LOW**: 2 (LOW)

## Applied mechanically

- Renumbered FRs after inserting FR-004 (date hide) kept consistent across spec/plan/tasks.
- Preview updated to demonstrate FR-004 state before Gate 1.

## Escalated

- None. Gate 1 accepted by owner (2026-11-13).