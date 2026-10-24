# Analysis: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Plan**: `specs/125-saved-song-sort-parity/plan.md`
**Tasks**: `specs/125-saved-song-sort-parity/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MED | traceability | `spec.md` § Requirements | The capability cells read `new: saved-reading`, but this repo has no `docs/spec/` tree (checked 2026-10-24), so Fold has no delta target | **decided** — the owner's 2026-10-24 decision (recorded in spec 123's `fold.md`) stands: the tree starts as its own card, and Fold records `n/a` for this slice |
| A2 | LOW | scope | `research.md` D004 | A second saved/server difference was found in the same comparison: the `/songs/` list page's saved render omits the disabled "+ Add song" button the server renders | accepted — recorded and kept out of scope; it is a candidate card, not a silent fix |
| A3 | LOW | testability | `spec.md` § FR-002 | "Never paints" is measured by frame sampling in one viewport; a narrower claim than "at every width" would need repeated runs | accepted — the hidden state is viewport-independent, and the width half of the check measures the filter in the same viewport as the control |
| A4 | LOW | consistency | `plan.md` § Traceability | `tests.e2e.test_saved_render_parity` is a class of three existing tests plus the two added here; the FR-005 row names it as a path, which reads like a single test | accepted — the task list names the class and what it covers |
| A5 | LOW | consistency | `specs/README.md` | The spec index stopped at spec 101 (60 rows; specs 102–123 have no row), so this slice's row would sit after a twenty-slice gap | accepted — left as found rather than half-repaired; backfilling or retiring the index is an owner decision, not a silent one |

No CRITICAL findings. No constitution findings: the repo has no `CONSTITUTION.md`.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T001, T004 |
| FR-002 | ✅ | ✅ | T002, T004, T005 |
| FR-003 | ✅ | ✅ | T001, T004, T006 |
| FR-004 | ✅ | ✅ | T001, T002, T013 |
| FR-005 | ✅ | ✅ | T007 |
| SC-001 | ✅ | ✅ | T002, T005 |
| SC-002 | ✅ | ✅ | T001, T006 |
| SC-003 | ✅ | ✅ | T001, T006, T007 |
| US1/AC1 | ✅ | ✅ | T002, T005 |
| US1/AC2 | ✅ | ✅ | T002, T005 |
| US1/AC3 | ✅ | ✅ | T001, T006 |
| US2/AC1 | ✅ | ✅ | T001, T006 |
| US2/AC2 | ✅ | ✅ | T007 |
| US2/AC3 | ✅ | ✅ | T001, T002 |

**Coverage**: 100% · **CRITICAL**: 0 · **MED**: 1 (A1) · **LOW**: 3 (A2–A4)

## Applied mechanically

- `spec.md` Status changed from `Draft` to `Accepted (owner, gate 1, 2026-10-24)` once the gate was answered.
- Verification split counted from the plan's table (13 test · 1 inspection · 0 manual), not estimated.
- `spec.md` SC-001's measurement was narrowed during implementation from "one filter width throughout" to
  "one filter width across the frames where that song page is on the stage": the field is 0 px wide while
  the second sidebar is closed before the section opens, so the original wording described something no
  page can show. The rule is unchanged; only the observation is stated as it can be measured.
- No unfilled clarification markers remain (grep over the pack, 2026-10-24).
- The planned item number is `ITEM-126`: `ITEM-125` is held by the Bible-edition slice on its own branch
  (spec 124), and specs 125 is free on every local and remote branch (checked 2026-10-24).
- Task bullets carry their `FR`/`SC`/`US` IDs, so the coverage table above is checkable by grep.

## Escalated

- **A1** — already decided by the owner for this repo on 2026-10-24; recorded rather than re-asked. No other
  finding needed the owner.
