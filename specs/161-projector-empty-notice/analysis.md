# Analysis: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`
**Plan**: `specs/161-projector-empty-notice/plan.md`
**Tasks**: `specs/161-projector-empty-notice/tasks.md`
**Run**: 2026-10-29

## Inputs

| Artifact | sha256 (first 12) |
| --- | --- |
| `spec.md` | `3a8437238d4b` |
| `plan.md` | `44899c35830e` |
| `research.md` | `386f30e1de87` |
| `data-model.md` | `281c26604e66` |
| `quickstart.md` | `fc5c7d1d1a48` |
| `tasks.md` | `7a80d01fab25` |
| `checklists/requirements.md` | `7529cde6e263` |

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MED | consistency | `spec.md` FR-006 | FR-006 is a requirement about the suite rather than about the product — a meta-requirement. It is kept because the defect shipped with a green case that asserted the notice's copy and never its absence, and the slice's acceptance rests on the suite guarding both sides. | accepted — reported, not fixed silently |
| A2 | LOW | coverage | `plan.md` US1/AC4 | The stepping case rests on an existing case (`test_a_verse_step_inside_a_chapter_makes_no_request`) named only in the plan's Notes, not in `tasks.md`. It is exercised as part of T011's module run. | accepted — the row is `inspection`, and T011 runs the module |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002 |
| FR-002 | ✅ | ✅ | T004, T005 |
| FR-003 | ✅ | ✅ | T006, T007 |
| FR-004 | ✅ | ✅ | T007, T009, T010 |
| FR-005 | ✅ | ✅ | T003, T007 |
| FR-006 | ✅ | ✅ | T004, T006, T009, T010 |
| FR-007 | ✅ | ✅ | T011, T012 |
| SC-001 | ✅ | ✅ | T004 |
| SC-002 | ✅ | ✅ | T001 (manual readout) |
| SC-003 | ✅ | ✅ | T006 |
| SC-004 | ✅ | ✅ | T009, T010 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH**: 0 · **MED/LOW**: 2

## Applied mechanically

- The plan's declared verification split was recounted from its own rows at the first run: the draft
  said `8 test · 3 inspection · 1 manual`, the rows count `13 test · 3 inspection · 1 manual` (the
  six acceptance-scenario rows and the three `SC` rows were not in the first tally). The line now
  matches the rows.
- `data-model.md`'s state table was aligned with `research.md` D001: the adoption path is listed as
  `adoptService() → done → render()`, not as a second writer.
- `tasks.md` names the test symbols exactly as `plan.md` does; `check_pack_consistency.py` reports
  7 plan symbols, 7 assigned.

## Escalated

- None. Both findings are recorded with their recommendation and neither changes a requirement.

## History

- **2026-10-29** — gate 2: the owner ticked all 12 checklist items (the tick is the gate's record;
  the checklist digest above predates it).
- **2026-10-29** — run 1 against the accepted pack: coverage 100%, split 13/3/1 matching, 7/7 symbols
  assigned, 5/5 named paths present; 0 CRITICAL, 0 HIGH, 1 MED (FR-006, accepted), 1 LOW (US1/AC4,
  accepted).
