# Analysis: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`
**Plan**: `specs/197-dock-bucket-head-pin/plan.md`
**Tasks**: `specs/197-dock-bucket-head-pin/tasks.md`
**Date**: 2026-11-16 · artifacts read at these revisions (working tree, uncommitted; digest of the first 12
hex of sha256): `spec.md` 11,864 B `17d728fe582f` · `plan.md` 4,980 B `0473d8a0b14b` · `tasks.md` 3,106 B
`3fa608a17de4`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | verification | `plan.md` traceability | SC-001's 4×-pixel scan is preview evidence, not a suite assertion; the suite asserts the hit test instead (a PNG decoder does not belong in an E2E module). | accepted — recorded in the traceability row's note and in `converge.md` when it runs |
| A2 | LOW | verification | `plan.md` traceability | US1/AC2 (a row half out above the head) is `manual`; the pinned-offset hit test covers the same pixels without a second scroll path. | accepted — one manual step named in the plan |
| A3 | LOW | consistency | `spec.md` SC-003 | The label's 14px is also develop's value, so a test asserting the label alone would pass on develop and prove nothing. | applied mechanically — the test asserts the *pair* (label unchanged **and** strip owned by the head), and T002 is red on develop for the strip |
| A4 | LOW | coverage | `tasks.md` | FR-003 ("the reserve stays 37px") has no test of its own; its consequence is T006's cursor parking. | accepted — declared `inspection` at Plan, proved by T006 |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002, T003 |
| FR-002 | ✅ | ✅ | T004 |
| FR-003 | ✅ | ✅ | T007 (inspection), T006 (consequence) |
| FR-004 | ✅ | ✅ | T005 |
| FR-005 | ✅ | ✅ | T008, T009 |
| SC-001 | ✅ | ✅ | T002 (hit test) |
| SC-002 | ✅ | ✅ | T002 |
| SC-003 | ✅ | ✅ | T004 |
| SC-004 | ✅ | ✅ | T005, T006 |
| SC-005 | ✅ | ✅ | T005 |
| SC-006 | ✅ | ✅ | T008 |
| US1/AC2 | ✅ | — | `manual` step, no task by design |
| US2/AC1 | ✅ | ✅ | T006 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 3 LOW

## Applied mechanically

- A3: the label assertion was paired with the strip assertion in T004/T002 so the suite cannot pass on
  develop's stylesheet.
- The spec's "band" was renamed "strip" where it meant the space above the label, because "band" already names
  the runner's `.nextband` in this codebase.

## Escalated

None: no finding changes intent, and gate 1 already settled the two review rounds (the pin's invariant and the
air between buckets).