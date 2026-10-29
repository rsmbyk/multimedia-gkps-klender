# Analysis: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`
**Plan**: `specs/156-audio-play-indicator/plan.md`
**Tasks**: `specs/156-audio-play-indicator/tasks.md`
**Run**: 2026-10-29 · spec `aefc06bc9676` · plan `da0dcea3dc6f` · tasks `2c7528f6c13e`

**Metrics**: 6 FR · 4 SC · 2 stories · 16 traceability rows · 12 tasks · coverage 100% · CRITICAL 0 · HIGH 0 · MED 0 · LOW 2

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | ambiguity | `spec.md` FR-001 | "at full opacity, whenever the audio player is showing" leaves the paused-but-idle case unstated: a paused player never enters the idle state (`audioActivity()` schedules the timer only while playing), so it is always "showing" and always at opacity 1. | accepted — the Edge Cases section states it ("paused before it ever started … visible at full opacity"); no wording change, the two statements agree once read together |
| A2 | LOW | coverage | `plan.md` SC-004 | SC-004 is a comparison of two measured tables, not a command; it is filed as `inspection` while the rest of SC is `test`. | accepted — a geometry regression in the bar would also move the E2E's own `bounding_box()` on the control, and the preview's table is the record of the other numbers |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T004/T005 | 48×48 box, opacity 1 while showing |
| FR-002 | ✅ | ✅ T004/T005 | triangle / two-bar mark from `data-playing` |
| FR-003 | ✅ | ✅ T004/T005 | idle hides it; box reserved; returns on activity |
| FR-004 | ✅ | ✅ T004/T006/T007 | click and `Space` toggle; `aria-label` asserted in T004 |
| FR-005 | ✅ | ✅ T003/T006/T008 | zones cleared, fullscreen gesture exempted |
| FR-006 | ✅ | ✅ T011 | diff scope, no other screen touched |
| SC-001 | ✅ | ✅ T009 | 48 × 48 ± .5, opacity 1 / 0, three viewports |
| SC-002 | ✅ | ✅ T004 | `::before` box in both states |
| SC-003 | ✅ | ✅ T004/T007 | `data-playing` flips under a real pointer click |
| SC-004 | ✅ | ✅ T009/T011 | bar and times geometry re-read against the "today" table |
| US1/AC1–AC4 | ✅ | ✅ T004–T006 | |
| US2/AC1–AC4 | ✅ | ✅ T007–T008 | |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 2

## Applied mechanically

- The spec's FR numbering re-cut when FR-005 (the click must reach the control) was added: the former
  FR-005 "nothing else changes" became FR-006, and every reference was updated in one pass.
- `plan.md`'s verification split recomputed after the US1/US2 rows were filed as `test` (15 → 11 test).
- The tasks' `[P]` marker moved onto the two failing-test tasks only, in keeping with C-SDD-TDD's rule that
  `[P]` means order-independent rather than concurrent.

## Escalated

- None: the one intent-shaped question — whether the control dims with the chrome or hides with it — was
  put to the owner at gate 1 and answered (hide/show), and the answer is recorded in the spec's
  Clarifications and in research D005.

## History

- 2026-10-29 — first run, after gate 1 and the revision it asked for; 0 CRITICAL, coverage 100%.
