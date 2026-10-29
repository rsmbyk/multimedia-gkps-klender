# Analysis: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)
**Plan**: `specs/152-transfer-scrollbar-edge/plan.md`
**Tasks**: `specs/152-transfer-scrollbar-edge/tasks.md`

**Run**: 2026-10-29 (revision 2) · artifacts read at `spec.md 2c8a0be1d7f4` ·
`plan.md 5d1f7bb0c9a2` · `research.md 91f4c6ff2a08` · `data-model.md 8b0d2c4ae113` ·
`quickstart.md d76805978750` · `tasks.md c3b0e1a94d27` · `checklists/requirements.md 4f6ce2b0915c` ·
`contracts/none.md bf7e99a36a13`

**Metrics**: 17 requirement/SC/US/edge ids · 100% covered by a traceability row · 12 test ·
12 inspection · 0 manual · no CRITICAL, no HIGH.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | measurability | `plan.md` | FR-002 and SC-001 are declared `inspection` because headless Chromium paints no bar, so the slice's headline numbers rest on a hand-run probe rather than on the suite | accepted — the alternative (a headed browser in the E2E module) makes the module depend on a display server and changes how every other test in it runs. The mechanism the paint depends on is `test`-covered (FR-001, FR-003, FR-007); `converge.md` quotes the probe's columns and the command that produced them |
| A2 | LOW | consistency | `spec.md` | The UI/UX table quotes whole-pixel columns (`982 → 986`) from the live app at 1440×760, while `preview/preview.html` reports 22.3px at some widths because the page centers the pair with a fractional offset | accepted — the sub-pixel is the page's own centering, not the product's; the probe measures the product's dialog at integer offsets and `spec.md` says which instrument each number came from |
| A3 | LOW | clarity | `tasks.md` | T006–T008 are written as "red only if …", which is honest for two of them (they pin behaviour the rules would break, and pass on develop today) but reads as a weaker red-first than T003's | accepted — a pin that passes before the change is the point (spec 149's `test_a_short_transfer_list_keeps_its_natural_height` is the same shape); the plan marks them `test` because they fail if the rules are wrong, not because they fail today |
| A4 | LOW | coverage | `spec.md` | The narrow viewport is an edge case and an SC-005 state, but no FR names a minimum width at which the 22px inset holds | accepted — the inset is the dialog's own padding at every width by construction; the probe measures 420×820, and a narrower width only shortens the rows, not the inset |
| A5 | LOW | consistency | `spec.md` | Revision 2 changed FR-004 from "the list's bottom edge is unchanged" to "the scroll's end is unchanged", which is the opposite of what revision 1 said about the same 22px; a reader comparing the two drafts sees a reversal | accepted and recorded — the reversal *is* the owner's gate-1 revision, kept visible in `§Clarifications` and in `research.md` D002/D006 rather than silently rewritten; the status line says revision 2 |
| A6 | LOW | coverage | `plan.md` | FR-007 (the corner clip) is verified by a `test` on the mechanism (`overflow: clip`) plus `inspection` of the corner shots — the one requirement whose *outcome* has no test at all | accepted — the outcome is a painted corner, which no headless assertion can see; the mechanism is pinned and the shots are cited with the command that produced them |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T003 · T004 |
| FR-002 | ✅ | ✅ | T005 |
| FR-003 | ✅ | ✅ | T006 · T009 |
| FR-004 | ✅ | ✅ | T008 · T009 |
| FR-005 | ✅ | ✅ | T007 · T009 |
| FR-006 | ✅ | ✅ | T009 |
| FR-007 | ✅ | ✅ | T003 · T004 · T005 |
| SC-001 | ✅ | ✅ | T005 |
| SC-002 | ✅ | ✅ | T003 · T004 |
| SC-003 | ✅ | ✅ | T006 · T007 |
| SC-004 | ✅ | ✅ | T008 |
| SC-005 | ✅ | ✅ | T005 · T010 |
| SC-006 | ✅ | ✅ | T005 |
| US1/AC1–AC4 | ✅ | ✅ | T004 · T005 |
| US2/AC1–AC4 | ✅ | ✅ | T006–T008 · T010 |
| Edge cases (6) | ✅ | ✅ | T005 · T010 |
| Baseline / markup check | ✅ | ✅ | T001 · T002 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 0 / 0 / 6

## Applied mechanically

- none — no requirement lacked a task, no path or id was stale, and the split declared in `tasks.md`
  equals the split counted from `plan.md`'s rows (12 / 12 / 0).

## Escalated

- none — no finding needed the owner's reading of intent; the one reversal (A5) was the owner's own
  instruction at gate 1 and is recorded, not fixed.

## History

- 2026-10-29 — first run, before gate 2: 4 findings (0 CRITICAL, 0 HIGH, 0 MED, 4 LOW), coverage 100%,
  split 11 test · 13 inspection · 0 manual.
- 2026-10-29 — second run, after the gate-1 revision (bottom edge + corner clip): 6 findings
  (0 CRITICAL, 0 HIGH, 0 MED, 6 LOW), coverage 100%, split 12 test · 12 inspection · 0 manual.
