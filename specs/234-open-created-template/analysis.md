# Analysis: a created Template opens on the reading stage

**Date**: 2026-11-23
**Spec**: `specs/234-open-created-template/spec.md` · SHA-256 `ac14075f5547c1ee9d67025b05a2a10b577c143df4062ae0f449fa645bd3098a`
**Plan**: `specs/234-open-created-template/plan.md` · SHA-256 `1e827c0d98098c7659b7a9cabe3439e1e942ef65969cd7d7b2dcf022dc928bef`
**Tasks**: `specs/234-open-created-template/tasks.md` · SHA-256 `b911ce478f4c07994444ba3bee1b963971977eb0e07367de974208002eeae25d`
**Checklist**: `specs/234-open-created-template/checklists/requirements.md` · SHA-256 `c0e29cc8d44dab3bf10aab221442908a1ef95e71684deb6e243cae8bade7ffa1`
**Metrics**: 21 requirements/decisions · 21 in plan · 21 in tasks · 19 test · 2 inspection · 0 manual

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MEDIUM | consistency | `tests/e2e/test_editor.py` | `test_a_template_create_keeps_the_stage` asserts the behaviour R46 now forbids | rewritten as `test_a_created_template_opens_on_the_stage` at T002; the old wording is kept visible in the spec's Superseded section |
| A2 | LOW | traceability | `spec.md` | R46's title names a "service" while the modified requirement also covers Templates | requirement number stays stable under SDD-03; the replacement block retitles the text at T011, not the `R46` id |
| A3 | LOW | process | worktree | the live preview edit and scripts are uncommitted before gate 2 | intentional — commits start at Fold (C-SDD-GIT); recorded in the spec's Assumptions |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002 |
| FR-002 | ✅ | ✅ | T002, T003, T005; `TatibView` supplies the stage |
| FR-003 | ✅ | ✅ | T004, T005 |
| FR-004 | ✅ | ✅ | T008 (six existing cases) |
| FR-005 | ✅ | ✅ | T007 |
| SC-001 | ✅ | ✅ | T002, T005 |
| SC-002 | ✅ | ✅ | T004 |
| SC-003 | ✅ | ✅ | T007 |
| SC-004 | ✅ | ✅ | T008 |
| US1/AC1 | ✅ | ✅ | T002 |
| US1/AC2 | ✅ | ✅ | T007 |
| US1/AC3 | ✅ | ✅ | T003 |
| US2/AC1 | ✅ | ✅ | T004 |
| US2/AC2 | ✅ | ✅ | T005 |
| US2/AC3 | ✅ | ✅ | T006 |
| US3/AC1 | ✅ | ✅ | T008 |
| US3/AC2 | ✅ | ✅ | T008 |
| US3/AC3 | ✅ | ✅ | T008 |
| US3/AC4 | ✅ | ✅ | T008 |
| D002 seam | ✅ | ✅ | T009, T011 |
| D004 level | ✅ | ✅ | T011 and the delivery commit |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 0 / 1 / 2

## Applied mechanically

- Added T006 after noticing the traceability row for `US2/AC3` had no task; no requirement text was
  changed.
- Aligned the verification split (`19 test · 2 inspection · 0 manual`) across `plan.md`, `tasks.md`
  and this report.

## Escalated

None. Every finding has a mechanical disposition; no intent-changing question was needed.
