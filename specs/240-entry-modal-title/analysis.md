# Analysis: entry modal title band

**Date**: 2026-11-24
**Spec**: `specs/240-entry-modal-title/spec.md`
**Plan**: `specs/240-entry-modal-title/plan.md`
**Tasks**: `specs/240-entry-modal-title/tasks.md`
**Status**: zero CRITICAL; 100% of the plan's 14 traceability rows accounted for

## Metrics

`3 stories · 6 AC · 4 FR · 4 SC · 14 traceability rows · 10 test · 4 inspection · 0 manual · 14 tasks · 0 unknowns · 11 spec checklist items · 11 plan checklist items`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | board | `spec.md`, `tasks.md` | Card `ITEM-253` was taken by spec 238 while this slice was at gate 1; the claim was moved to `ITEM-255` and the in-flight branches were re-read. | Recorded in `spec.md` §Assumptions and T012. No intent change. |
| A2 | LOW | version | `plan.md` | Spec 239 landed on `origin/develop` during gate 1 and took `1.36.25`; this slice now targets `1.36.26`. | Plan header updated; T012 re-checks the number again before delivery. |
| A3 | LOW | chronology | `spec.md`, `tasks.md` | The CSS edit was applied before gate 1 so the change could be reviewed on the real page; red tasks temporarily remove it under a trap. | Recorded in the spec's Assumptions and the tasks preamble; no rewrite of history. |
| A4 | LOW | collision | `tasks.md` | Unmerged slices hold IDs not visible on `develop` (238 holds `ITEM-253`, 239 held `ITEM-254`). | T012 re-checks spec 240, `ITEM-255`, `reading/R10` and the patch level against `origin/develop` and every unmerged branch. |
| A5 | INFO | evidence | `preview/probe.py` | The "before" column comes from a browser-local override; all other CSS comes from the shipped page. | The page itself carries the fix, so the control reverts one declaration. Documented in §UI/UX, `research.md` D003 and CHK011. Owner decision at gate 2 whether a second base server is required; recommendation: keep the override. |
| A6 | LOW | verification | `tasks.md` | T005 uses existing spec-226 cases as a characterisation guard; they were green on the base, so there is no honest red for unchanged behaviour. | Recorded in the task and in `plan.md` rows US2/AC1, FR-003, SC-002. Recommendation: keep as green baseline; cost of leaving it is only that the guard cannot distinguish a new regression from an old one — the fresh failing tests cover the new behaviour. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T002–T004 | band restored in all three large dialogs |
| FR-002 | ✅ | ✅ T007–T008 | narrow `16px 18px`, divider retained |
| FR-003 | ✅ | ✅ T005, T010 | verse header's single rule preserved |
| FR-004 | ✅ | ✅ T006, T009 | compact forms, loading and sr-only titles unchanged |
| SC-001 | ✅ | ✅ T002, T004 | 26/21px text, 72.5px band, 1px rule |
| SC-002 | ✅ | ✅ T005, T006 | zero ruled descendants; compact dialogs unchanged |
| SC-003 | ✅ | ✅ T007 | 18/17px text, 64.5px band |
| SC-004 | ✅ | ✅ T009–T011 | frame, verse and probe readouts; full suite deferred |
| US1/AC1 | ✅ | ✅ T002 | text offsets and divider in three dialogs |
| US1/AC2 | ✅ | ✅ T004 | frame, field and action-row numbers |
| US2/AC1 | ✅ | ✅ T005 | verse header head/title numbers |
| US2/AC2 | ✅ | ✅ T006 | compact dialogs unchanged |
| US3/AC1 | ✅ | ✅ T007 | narrow title numbers |
| US3/AC2 | ✅ | ✅ T008 | probe numbers and no page scrollbar |

**Coverage**: 100% (14/14 plan rows) · **CRITICAL**: 0 · **HIGH/MED**: 0/0 · **LOW/INFO**: 4/1

## Applied mechanically

- Counted the plan's verification split as 10 `test` and 4 `inspection` rows; aligned
  both checklists, `tasks.md` and `quickstart.md` to the same split.
- Checked FR-001–004, SC-001–004 and all six story scenarios for orphan IDs; none.
- Updated the card claim to `ITEM-255` and the version target to `1.36.26` after the
  parallel-slice recheck, in every artifact that named the old values.
- Confirmed the live preview carries the fix and that no interface is added.

## Escalated

No intent-changing findings. A5 and A6 each carry a recommendation and the cost of
leaving them as recorded; nothing blocks gate 2.

## Artifact SHAs read (sha256, first 12)

- `spec.md` `c728ce7b9dcf`
- `plan.md` `929a5ffafedd`
- `research.md` `c62f405e73e9`
- `data-model.md` `333a74d1345e`
- `contracts/none.md` `e284ccd7eec7`
- `quickstart.md` `60657186e2fa`
- `tasks.md` `ab22d2e393c9`
- `checklists/requirements.md` `970ea702fe0b`
- `checklists/checklist.md` `b068a9e575c9`
- `preview/README.md` `44dd12dd091d`
- `preview/probe.py` `6d7a9168dec9`

## History

- 2026-11-24 — first analysis: zero CRITICAL, 100% coverage, five recorded findings (one INFO).
