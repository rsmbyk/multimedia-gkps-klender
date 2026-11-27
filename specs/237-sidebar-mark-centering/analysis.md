# Analysis: sidebar mark centring

**Date**: 2026-11-24
**Spec**: `specs/237-sidebar-mark-centering/spec.md`
**Plan**: `specs/237-sidebar-mark-centering/plan.md`
**Tasks**: `specs/237-sidebar-mark-centering/tasks.md`
**Status**: zero CRITICAL; 100% of the plan's 14 traceability rows accounted for

## Metrics

`3 stories · 6 AC · 4 FR · 4 SC · 8 test rows · 6 inspection rows · 0 manual rows · 14 tasks · 0 unknowns · 11 spec checklist items · 11 plan checklist items`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | board | `spec.md`, `tasks.md` | `ITEM-252` is opened in Backlog with the spec and branch fields; only you promote it to `Ready`. | Recorded in the spec's Assumptions; gate 1 was accepted on the spec directly. No intent change. |
| A2 | LOW | version | `plan.md` | Local `develop` is three commits behind `origin/develop` (`1.36.20` vs `1.36.22`); a parallel slice can take the next patch. | The plan declares only the level (`patch`); T013 re-checks the number before delivery, and VER-04 stamps it pre-merge. No plan change. |
| A3 | LOW | chronology | `spec.md`, `tasks.md` | The CSS edit was applied before gate 1 so the change could be reviewed on the real page; TDD's red task therefore runs with the two selectors temporarily removed. | Recorded explicitly in the spec's Assumptions and in the tasks preamble; no rewrite of history. |
| A4 | LOW | collision | `tasks.md` | Unmerged slices hold spec numbers, card IDs and `R<n>` values not visible on `develop`. | T013 re-checks 237, `ITEM-252`, `reading/R49` and the patch level against every unmerged branch before delivery. |
| A5 | INFO | evidence | `preview/probe.py` | The before numbers come from reverting only the mark's `align-self` inline on the live page, not from a separate base server; all other CSS comes from the shipped page. | The page itself carries the fix, so the control is a one-property revert. Documented in `spec.md` §UI/UX and `preview/README.md`; no change. |
| A6 | LOW | gap | `plan.md`, `checklists/checklist.md` | The drag-copy row is `inspection`, not an E2E gesture: the ghost's mark is verified from the CSS selector and `reorder.js:268`, not by dragging. | CHK011 records the gap. Recommendation: keep inspection — a drag gesture adds pointer flakiness without testing the declaration; cost of leaving it is that a future script change could drop the mark from the clone unnoticed. Owner decision at gate 2. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T002–T004 | every marked row centred |
| FR-002 | ✅ | ✅ T005–T007 | x, height and clamp unchanged |
| FR-003 | ✅ | ✅ T009 | ghost copy's mark aligned like its number |
| FR-004 | ✅ | ✅ T010 | one CSS diff; other surfaces untouched |
| SC-001 | ✅ | ✅ T002, T004 | 0px centre offset on all rows |
| SC-002 | ✅ | ✅ T005, T006, T008, T010 | geometry, wrap and badge numbers |
| SC-003 | ✅ | ✅ T009 | computed alignment on the ghost rule |
| SC-004 | ✅ | ✅ T010, T011 | two themes, three widths, probe readouts |
| US1/AC1 | ✅ | ✅ T002 | centre equals number centre |
| US1/AC2 | ✅ | ✅ T004 | colours and states unchanged |
| US2/AC1 | ✅ | ✅ T005 | columns, heights, clamp |
| US2/AC2 | ✅ | ✅ T006 | 390px wrapped row |
| US3/AC1 | ✅ | ✅ T008 | badge follows the mark |
| US3/AC2 | ✅ | ✅ T009 | drag copy follows the mark |

**Coverage**: 100% (14/14) · **CRITICAL**: 0 · **HIGH/MED/LOW/INFO**: 0/0/5/1

## Applied mechanically

- Counted the plan's traceability split as 8 `test` and 6 `inspection` rows; aligned both
  checklists and `tasks.md` to the same split.
- Checked FR-001–004, SC-001–004 and all six user-story scenarios for orphan IDs; none found.
- Confirmed the live preview matches a server-rendered change and that the probe reads the
  shipped page rather than injecting the fix.
- Confirmed the plan's verification split, bump declaration and delivery steps are present.

## Escalated

No intent-changing findings. A6 is a verification-depth choice with a recommendation and a
cost; all other findings are records or mechanical tasks. Nothing blocks gate 2.

## Artifact SHAs read (sha256, first 12)

- `spec.md` `d244b63b2858`
- `plan.md` `53d476bbdaaf`
- `research.md` `8b23a8319be0`
- `data-model.md` `e5a4e40a54a6`
- `contracts/README.md` `31111809f1b6`
- `quickstart.md` `6439d11140b3`
- `tasks.md` `4c361299771c`
- `checklists/requirements.md` `66891158fb39`
- `checklists/checklist.md` `349a411e01d3`
- `preview/README.md` `efd730ea0f3d`
- `preview/probe.py` `1ad5eab8240f`

## History

- 2026-11-24 — first analysis: zero CRITICAL, 100% coverage, six recorded findings (one INFO).
