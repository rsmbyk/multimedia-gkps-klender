# Analysis: The first sidebar's idle rule, restored and set to fifteen minutes

**Spec**: `specs/199-sidebar-activity/spec.md`
**Plan**: `specs/199-sidebar-activity/plan.md`
**Tasks**: `specs/199-sidebar-activity/tasks.md`

**Date**: 2026-11-18
**Artifact SHAs** (`git hash-object`): spec `09e3e58` · plan `721a3f6` · research `bf6b808` ·
data-model `a8e1378` · quickstart `fa0523f` · tasks `e97a4e0`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | coverage | `spec.md` SC-002 / `plan.md` | SC-002 names keyboard scrolling among the paths the existing idle E2E keep green, but no existing test presses a key to scroll; `keydown` is asserted by inspection (US1/AC3), and the scroll a key produces is pinned by the new scroll test. | reported — no change: the method is declared as inspection in the traceability table, and a dedicated PageDown test would pass before and after, proving nothing about this slice |
| A2 | LOW | consistency | `tasks.md` T002 | US3/AC4 asks for the drawer to be *scrolled* at 390 px; the existing narrow test only waits. T002 now scrolls `#chBody` inside the drawer and asserts it moved, so the row is a real scroll rather than an elapsed wait. | fixed mechanically before this report (test step extended) |
| A3 | LOW | terminology | `spec.md` A10 / `plan.md` D002 | The spec calls the 1 s re-check both "expiry re-check" and "expiry poll"; the plan adds "backstop". One thing, three names. | reported — no change: the Clarifications and A10 define it at first use, and rewriting accepted prose at Plan is churn |
| A4 | LOW | measurability | `spec.md` US1/AC4 | "scrolling reaches either end and produces no scroll event" cannot be asserted, only inspected: there is no event to observe. `plan.md` declares it inspection and names what to look at (the handler runs only on an event). | reported — accepted as declared; un-tested but verifiable |

**CRITICAL**: 0 · **HIGH/MED**: 0 · **LOW**: 3 open (A1, A3, A4) + 1 applied (A2)

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T004, T005, T006, T010 |
| FR-002 | ✅ | ✅ | T004, T006 |
| FR-003 | ✅ | ✅ | T002 (focus test), T006 (handler kept) |
| FR-004 | ✅ | ✅ | T010 |
| FR-005 | ✅ | ✅ | T008, T009 |
| FR-006 | ✅ | ✅ | T002 (section mismatch, narrow) |
| FR-007 | ✅ | ✅ | T011 (inspection) |
| FR-008 | ✅ | ✅ | T002, T003 |
| FR-009 | ✅ | ✅ | T006, T011 |
| FR-010 | ✅ | ✅ | T007, T008, T009 |
| SC-001 | ✅ | ✅ | T004 |
| SC-002 | ✅ | ✅ | T002, T005 (keyboard by inspection) |
| SC-003 | ✅ | ✅ | T010 |
| SC-004 | ✅ | ✅ | T008 |
| SC-005 | ✅ | ✅ | T002, T011 |
| SC-006 | ✅ | ✅ | T007 |
| SC-007 | ✅ | ✅ | T008 |
| SC-008 | ✅ | ✅ | T012 |
| US1/AC1–AC4 | ✅ | ✅ | AC1 T004, AC2 T005, AC3 T011, AC4 T011 |
| US2/AC1–AC4 | ✅ | ✅ | AC1 T007, AC2 T008, AC3 T008, AC4 T008 |
| US3/AC1–AC4 | ✅ | ✅ | AC1–AC2 T010, AC3 T008, AC4 T002 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 3

## Applied mechanically

- **A2** — T002's narrow test extended to scroll `#chBody` inside the drawer and assert it moved,
  so US3/AC4 is exercised rather than inferred. The plan's US3/AC4 row and T002's description were
  updated together; no requirement changed.
- Test counts aligned across the artifacts: 4 new E2E tests, 9 existing idle tests touched
  (7 rescaled in T002, 2 reshaped in T008), 26 test rows + 5 inspection + 1 manual in the split.
- Path and ID sweep: every file named in `plan.md`/`tasks.md` exists (`static/web/reading.js`,
  `tests/e2e/test_reading.py`, `docs/spec/reading.md`), the line anchors cited
  (`reading.js:64`, `:130-139`; `test_reading.py:143`, `:404-477`, `:489`, `:507`) match the files
  at this revision, and `R44`/`R45` are free in `docs/spec/reading.md` (last is `R43`).

## Escalated

None. No finding changes what a requirement means, which of two rules wins, or what an acceptance
criterion asserts; the three open findings are method declarations the gate can see.

## History

- **2026-11-18** — pass 1 against spec `09e3e58`, plan `721a3f6`, tasks `e97a4e0`: 100% coverage,
  0 CRITICAL, 4 findings (1 applied, 3 LOW reported).
