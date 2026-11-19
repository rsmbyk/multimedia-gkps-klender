# Analysis: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`
**Plan**: `specs/201-sidebar-date-focus/plan.md`
**Tasks**: `specs/201-sidebar-date-focus/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MED | tooling | `plan.md` D003 | Headless Chromium on the app's HTTP origin reports `(hover: hover)` false, so a computed-style E2E alone would pass on the defective base; the plan injects the selector text outside the guard and asserts it separately. | accepted with documented workaround |
| A2 | LOW | scope | `spec.md` US2 | The Today badge shares the same declaration block as the date; it cannot be fixed independently, so US2 is P2 but not independently shippable. | accepted — both states in one rule |
| A3 | LOW | wording | `docs/spec/reading.md` R41/R9 | Both blocks say "hovered or focused" and do not say which focus; the Fold clarifies them rather than adding new requirements. | planned as typed `modified` deltas |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T003/T004/T005 |
| FR-002 | ✅ | ✅ | T007 |
| FR-003 | ✅ | ✅ | inspection in T009 |
| FR-004 | ✅ | ✅ | inspection in T005/T009 |
| SC-001 | ✅ | ✅ | T003 |
| SC-002 | ✅ | ✅ | T004/T007 |
| SC-003 | ✅ | ✅ | T006 |
| US1/AC5 | ✅ | ✅ | T004 |
| US2/Edge 3 | ✅ | ✅ | T008 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 3

## Applied mechanically

- Checklists start at CHK001; task IDs are consecutive; the spec's four FRs and three SCs each have a traceability row.

## Escalated

- none.
