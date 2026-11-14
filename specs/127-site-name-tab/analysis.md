# Analysis: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`
**Plan**: `specs/127-site-name-tab/plan.md`
**Tasks**: `specs/127-site-name-tab/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | underspecification | `spec.md` §FR-001 | FR-001 first named only `/`, but `multimedia/web/urls.py` sends `/home/` to the same view and returns the same landing from `/search` when `q` is absent — two of the three index routes fell outside the requirement, and the request's screenshot is of one of them. | fixed mechanically before the plan: FR-001, US2's scenarios and T003 widened to all three routes |
| A2 | LOW | coverage | `plan.md` §Traceability (FR-006) | FR-006 (visible and assistive text unchanged) is verified by inspection — a template grep — rather than a test. | accepted: the visible strings are already pinned by `test_home_is_search_first`'s `Search Alkitab, Kidung, and Tata Ibadah` and the rail `data-tip` assertions, which T011 re-runs |
| A3 | LOW | environment | `tasks.md` T011 | The unit suite needs `collectstatic` in a fresh worktree; without `_static/`, nine unrelated page-render tests error on the static manifest. | recorded in T011 and `quickstart.md`, so the next reader does not chase nine phantom failures |

Passes: duplication — no title string is defined twice within one producer; ambiguity — every FR names an
exact string; consistency — the FR/SC/US rows agree across spec, plan and tasks; constitution — no
`CONSTITUTION.md` exists (checked 2026-10-24).

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T001, T003, T004, T005 |
| FR-002 | ✅ | ✅ | T006, T007, T008 |
| FR-003 | ✅ | ✅ | T006, T010 |
| FR-004 | ✅ | ✅ | T005, T008 |
| FR-005 | ✅ | ✅ | T009 |
| FR-006 | ✅ | ✅ | T010, T011 |
| SC-001 | ✅ | ✅ | T001, T012 |
| SC-002 | ✅ | ✅ | T006, T012 |
| SC-003 | ✅ | ✅ | T010, T013 |
| SC-004 | ✅ | ✅ | T011 |
| US1 | ✅ | ✅ | T006–T008, T012 |
| US2 | ✅ | ✅ | T003–T005 |
| US3 | ✅ | ✅ | T005, T008, T009 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 1 / 0 / 2

## Applied mechanically

- A1 — FR-001 widened from `/` alone to `/`, `/home/` and the blank `/search`; US2 gained the two extra
  scenarios and T003 names both view branches.
- A3 — the `collectstatic` prerequisite written into T011 and `quickstart.md`.
- `reading/R3` reserved in the spec's Assumptions: `docs/spec/reading.md` holds R1 and R2 today, and the
  draft may not invent a number Fold has not applied.

## Escalated

- none — no finding needed the owner's intent; both scope readings were settled in `## Clarifications`
  before the draft was presented at gate 1.
