# Analysis: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md` · **Plan**: `specs/158-projector-media-fit/plan.md`
**Tasks**: `specs/158-projector-media-fit/tasks.md`
**Date**: 2026-10-29
**Artifact SHAs** (first 12 of sha256): spec `5636907fb48a` · plan `a7c035e123f2` · tasks `1dcd0d5a89c1`
· research `89a0716c80ef` · data-model `c0a7ba9e122d` · quickstart `4dbf4973313a` · contracts `15ccb7bf0426`

**Metrics**: 12 requirements · 10 success criteria · 5 stories · 21 scenarios · 21 tasks ·
coverage FR 12/12 · SC 10/10 · **0 CRITICAL · 0 HIGH** · 3 inspection rows · 0 manual.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MEDIUM | duplicate statement | `spec.md` FR-004 | FR-004 restates FR-003's default ("the default fit is the smaller ratio") as a second requirement, where one statement could carry both. | **accepted** — the default is a fact a reader and a test can check on its own (T011 asserts the size *before* `T`); merging it into FR-003 would hide it inside the toggle rule. |
| A2 | LOW | numbers vs measurement | `spec.md` SC-004, SC-005 | The criteria say 1856×2824 and 1856×2402; the preview measured 1855×2824 and 1856×2401, because the stage is 1855.5 px wide at a 1920 window and the painted size is floored. | **accepted** — every criterion carries ±1 px, and the plan's tests assert ±1. Amending the numerals to the half-pixel would be false precision. |
| A3 | MEDIUM | coverage | `tasks.md` | FR-008 ("every other screen kind behaves as today") has no task of its own — it is satisfied by *not* touching those paths. | **accepted** — a task that writes no code would be noise; it is covered by T021 (the projector module re-run) and by the diff inspection at Converge. Recorded so the gap is visible rather than passed over. |
| A4 | LOW | coverage | `plan.md` SC-003 row | SC-003's numerals (441×672 / 519×672) belong to the real files; the E2E fixture is a 12×6 PNG, which at a 960×672 stage paints 960×480. | **accepted** — the test pins the *rule* at a second window size; the real files' numbers are the preview's measurement (`spec.md §UI/UX`), and the plan's traceability says so. |
| A5 | LOW | ambiguity | `spec.md` FR-009 | The requirement named the wheel's vertical panning and `Shift` but not `deltaX`, which a trackpad produces directly. | **applied** — FR-009 now names `deltaY` vertically and `deltaX` or `Shift`+`deltaY` horizontally; plan D006 already had it. Spec SHA above is the amended one. |
| A6 | LOW | terminology | `spec.md`, `tasks.md` | "fit" is used both as the state (`fitState === 'fit'`) and as the family ("the fit"). | **accepted** — the code keeps `'fit' \| 'width' \| 'height'` and the documents say "the fit" only where "the default fit" has just been named. No drift between the two spellings of a state value. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T003–T007 | SC-001, SC-006, US1 AC1–AC3 |
| FR-002 | ✅ | ✅ T008–T010 | SC-002, US2 AC1–AC4 |
| FR-003 | ✅ | ✅ T011–T013 | SC-004, SC-005, US3 AC1–AC4 |
| FR-004 | ✅ | ✅ T011, T013 | US3 AC1 |
| FR-005 | ✅ | ✅ T012, T013 | US3 AC4 |
| FR-006 | ✅ | ✅ T003, T007 | US3 AC6 |
| FR-007 | ✅ | ✅ T018, T019 | SC-007, US5 AC1–AC2 |
| FR-008 | ✅ | ✅ (by omission) T021 + diff | US3 AC5 |
| FR-009 | ✅ | ✅ T014, T016, T017 | SC-008, SC-009, US4 AC1–AC2 |
| FR-010 | ✅ | ✅ T014, T016 | US4 AC3, AC5 |
| FR-011 | ✅ | ✅ T015, T016 | SC-010, US4 AC6 |
| FR-012 | ✅ | ✅ T014, T002 | US4 AC1 (cursor) |
| SC-001 | ✅ | ✅ T003 | |
| SC-002 | ✅ | ✅ T008 | |
| SC-003 | ✅ | ✅ T003 | |
| SC-004 | ✅ | ✅ T011 | |
| SC-005 | ✅ | ✅ T012 | |
| SC-006 | ✅ | ✅ T004 | |
| SC-007 | ✅ | ✅ T018 (+ the D007 measurement) | |
| SC-008 | ✅ | ✅ T014 | |
| SC-009 | ✅ | ✅ T014 | |
| SC-010 | ✅ | ✅ T015 | |

## History

- **2026-10-29** — first run, at gate 2: 6 findings, none CRITICAL or HIGH, coverage 12/12 and 10/10; A5
  applied to the spec (FR-009 names the wheel's axes), the rest accepted with their reasons above.
- **2026-10-29** — after gate 2, `tasks.md` was marked as tasks landed (T001–T021) and the spec's §UI/UX
  line was amended to say the preview ships media at the review's sizes rather than the service's own
  files (a receipt is not a repository fixture). Both SHAs above are the post-amendment ones; no
  requirement, criterion or finding changed.
