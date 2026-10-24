# Analysis: Match the Tata Ibadah date header to the songbook header

**Spec**: `specs/123-tatib-date-header-parity/spec.md`
**Plan**: `specs/123-tatib-date-header-parity/plan.md`
**Tasks**: `specs/123-tatib-date-header-parity/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | traceability | `spec.md` § Requirements | The capability cells read `new: reading header`, but this repo has no `docs/spec/` tree (checked 2026-10-24), so Fold has no delta target for the slice | **decided at gate 2** (owner, 2026-10-24): Fold records `n/a — no capability tree yet` for this slice (`fold.md`) and the tree starts as its own card, not out of a header fix |
| A2 | LOW | coverage | `spec.md` § Assumptions | The saved/offline page's only evidence is class inheritance plus its existing text pins; the style itself is not asserted offline | accepted — recorded as `inspection` in the plan, not claimed as a test |

No CRITICAL findings. No constitution findings: the repo has no `CONSTITUTION.md`.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T001, T004, T005 |
| FR-002 | ✅ | ✅ | T007 (existing pin re-run) |
| FR-003 | ✅ | ✅ | T002, T006, T007 |
| FR-004 | ✅ | ✅ | T008, T009 |
| FR-005 | ✅ | ✅ | T001, T005 |
| FR-006 | ✅ | ✅ | T009 |
| SC-001 | ✅ | ✅ | T001 |
| SC-002 | ✅ | ✅ | T007 |
| SC-003 | ✅ | ✅ | T002 |
| SC-004 | ✅ | ✅ | T001 |
| US1/AC1–AC3 | ✅ | ✅ | T001, T004, T005 |
| US2/AC1 | ✅ | ✅ | T002, T006, T007 |
| US3/AC1 | ✅ | ✅ | T008, T009 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH**: 1 (A1) · **MED/LOW**: 1 (A2)

## Applied mechanically

- `plan.md` first named `multimedia/web/tests.py::TatibHeaderTests`; the module has no such class — the header
  text pins live in `ReadingViewTests`. Corrected after reading the file.
- The `[NEEDS CLARIFICATION]` marker in the spec was replaced by the decided rule once the owner answered at
  Clarify, and the answer was recorded in § Clarifications.
- Verification split counted from the plan's table (11 test · 2 inspection · 0 manual) rather than estimated.

## Escalated

- **A1** — one question for gate 2: does this slice start `docs/spec/` with a `reading-ui` capability, or
  does Fold record `n/a` and the tree wait for its own slice?
