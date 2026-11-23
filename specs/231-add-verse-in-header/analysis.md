# Analysis: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`
**Plan**: `specs/231-add-verse-in-header/plan.md`
**Tasks**: `specs/231-add-verse-in-header/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | process | `spec.md` | The gate-1 material was a live preview of the real code path, so the template/CSS change was applied before the pack was written; no commit exists. | reported — recorded in Assumptions; Converge re-assesses the code |
| A2 | LOW | scope | `tasks.md` | Two `test` rows describe E2E modules that will be written but run only at the push step. | reported — owner's standing instruction; fast tests are the in-between evidence |
| A3 | MED | spec | `spec.md` | US1/AC5 and SC-006 claimed Project is gated on edit permission. The new template test showed Project is present on a hymn song on unmodified `develop`; only Add verse is permission-gated. | corrected — the wrong assumption was mine, no product behaviour changes; the losing wording is kept as a superseded note in AC5 |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| US1/AC1 | ✅ | ✅ | T003, T006, T007 |
| US1/AC2 | ✅ | ✅ | T004 |
| US1/AC3 | ✅ | ✅ | T005 |
| US1/AC4 | ✅ | ✅ | T012 (manual) |
| US1/AC5 | ✅ | ✅ | T008 |
| US2/AC1 | ✅ | ✅ | T009 |
| US2/AC2 | ✅ | ✅ | T010 |
| US2/AC3 | ✅ | ✅ | T010 |
| FR-001 … FR-007 | ✅ | ✅ | T006–T011 |
| SC-001 … SC-006 | ✅ | ✅ | T003–T010, T012 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 1 MED, 2 LOW (A3 corrected before Converge)

## Applied mechanically

- Aligned the verification split line in `plan.md` and `tasks.md` to the same 14 test / 6 inspection / 1 manual count.
- Kept the two LOW findings as reported items rather than resolving them by editing artifacts.

## Escalated

- None. No intent-changing finding needs an owner decision; both findings are reported with their cost of leaving them.
