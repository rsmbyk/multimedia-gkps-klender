# Analysis: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md` (sha `d42e49c2a2c9`)
**Plan**: `specs/187-keyboard-parity/plan.md` (sha `25fe13993777`)
**Tasks**: `specs/187-keyboard-parity/tasks.md` (sha `cae4a2412ae3`)
**Read**: `research.md` `ff42ab029a87` · `data-model.md` `600874cbd9f3` · `quickstart.md` `443ec0b71ef2` ·
`checklists/requirements.md` `fe6faec0f4c5` · `contracts/display-state.md` `dc6583d5c1a8` ·
`contracts/keyboard.md` `af5028c5c2fe` · `contracts/README.md` `9051cc51631b`
**Date**: 2026-11-05

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MEDIUM | verification | `plan.md` | FR-008's row named only the preview's `probe.py`; that reads the preview's markup, not `obs_dock.html`, so the product's sheet could drift while the check stayed green. | applied — the row now names `test_dock_keys.py::test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view` for the product, with the probe kept as the design's check; T022 already read the product's rows |
| A2 | LOW | precision | `spec.md` | The projector's frame was written as 836 px in FR-014, US10/AC4 and SC-011, and as 835.5 px in the plan and the capture's README — one number for one measurement. | applied — the spec now says 835.5 px in all three places |
| A3 | LOW | duplication | `spec.md` | FR-013's last sentence restates the dock's groups, which FR-008 owns. | kept — it is the projector-side constraint that binds the dock's sheet to the same shape, not a second definition; deleting it would drop the cross-surface obligation |
| A4 | LOW | coverage | `spec.md` | US11's scenarios do not cover the shortcut sheet being open when the window returns. | kept — the Edge Cases bullet states it (the panel keeps the focus; the sheet has no field) |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T006-T008 |
| FR-002 | ✅ | ✅ | T009, T012 |
| FR-003 | ✅ | ✅ | T003-T005 |
| FR-004 | ✅ | ✅ | T010-T012 |
| FR-005 | ✅ | ✅ | T015-T019 |
| FR-006 | ✅ | ✅ | T020-T021 |
| FR-007 | ✅ | ✅ | T022-T025 |
| FR-008 | ✅ | ✅ | T022, T024-T025 |
| FR-009 | ✅ | ✅ | T026-T027 |
| FR-010 | ✅ | ✅ | T028-T030 |
| FR-011 | ✅ | ✅ | T013-T014 |
| FR-012 | ✅ | ✅ | T031-T033 |
| FR-013 | ✅ | ✅ | T034-T036 |
| FR-014 | ✅ | ✅ | T037-T040 |
| FR-015 | ✅ | ✅ | T041-T042 |
| SC-001 | ✅ | ✅ | T006 |
| SC-002 | ✅ | ✅ | T003 |
| SC-003 | ✅ | ✅ | T016 |
| SC-004 | ✅ | ✅ | T019 |
| SC-005 | ✅ | ✅ | T020 |
| SC-006 | ✅ | ✅ | T022-T023 |
| SC-007 | ✅ | ✅ | T026 |
| SC-008 | ✅ | ✅ | T028 |
| SC-009 | ✅ | ✅ | T014 |
| SC-010 | ✅ | ✅ | T031 |
| SC-011 | ✅ | ✅ | T037 |
| SC-012 | ✅ | ✅ | T041 |

**Coverage**: 100% (27/27 requirements, 12 of 12 success criteria) · **CRITICAL**: 0 ·
**HIGH**: 0 · **MED**: 1 · **LOW**: 3

## Applied mechanically

- A1 — the plan's FR-008 verification now names the E2E that reads the product's sheet; the preview's
  probe stays as the design's check.
- A2 — 836 px → 835.5 px in FR-014, US10/AC4 and SC-011, matching the measurement and the capture.
- Checked and left alone: every FR names a capability; every task carries a `[USn]` tag or belongs to
  Setup/Foundational/Polish; every SC names a measurement; no path in the plan or tasks points at a file
  the slice does not touch.

## Escalated

- None. No finding changed what a requirement means, so no question was asked.

## History

| Date | Run | Result |
| --- | --- | --- |
| 2026-11-05 | 1 — first analysis after Tasks | 100% coverage · 0 CRITICAL · 0 HIGH · 1 MED · 3 LOW (1 applied, 1 applied, 2 kept) |
