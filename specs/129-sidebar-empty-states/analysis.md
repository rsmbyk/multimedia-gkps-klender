# Analysis: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`
**Plan**: `specs/129-sidebar-empty-states/plan.md`
**Tasks**: `specs/129-sidebar-empty-states/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | traceability | `plan.md` | US3's independent test claims saved-versus-server equality, but the parity suite asserts titles and controls, not the two blocks' copy. | accepted — the renderer is written to the same six strings, and the parity suite proves nothing regressed; a copy-level saved/server assertion is named as the gap in `converge.md` |
| A2 | LOW | wording | `spec.md` | FR-007 and US2/AC3 both describe the arriving page's block, from two directions. | applied — FR-007 owns the mechanism, US2/AC3 stays the observable behaviour |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002, T006, T009 |
| FR-002 | ✅ | ✅ | T006 |
| FR-003 | ✅ | ✅ | T007, T010 |
| FR-004 | ✅ | ✅ | T003, T004, T005 |
| FR-005 | ✅ | ✅ | T006, T011 |
| FR-006 | ✅ | ✅ | T007, T009 |
| FR-007 | ✅ | ✅ | T015 |
| FR-008 | ✅ | ✅ | T013 |
| FR-009 | ✅ | ✅ | T012 |
| FR-010 | ✅ | ✅ | T002, T007 |
| FR-011 | ✅ | ✅ | T008 |
| SC-001 | ✅ | ✅ | T009 |
| SC-002 | ✅ | ✅ | T009, T004, T005 |
| SC-003 | ✅ | ✅ | T004, T005 |
| SC-004 | ✅ | ✅ | T013, T014 |
| SC-005 | ✅ | ✅ | the suites named in `quickstart.md` |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 1 HIGH, 1 LOW

## Applied mechanically

- Renamed the spec's `[NEEDS CLARIFICATION]` markers into the Assumptions list, since the request settled both
  open points (no add action in the block; the sidebar keeps its own wording rather than the stage's).
- Aligned the section names used across the four files (`No sections yet.` in the template default, the views'
  `CH_META`, and the renderer's `LIST_EMPTY`); the template's `|default:` fallbacks now read the same strings.

## Escalated

- The slice's sequencing: the owner asked for the fix in a working session, so the branch carries the
  implementation before gate 1. Recorded in `spec.md` rather than hidden, and gate 1 still decides the copy
  and the numbers.
