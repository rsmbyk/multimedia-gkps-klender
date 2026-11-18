# Analysis: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md` · **sha256** `b4c597d6fff6`
**Plan**: `specs/200-dock-centre-triggers/plan.md` · **sha256** `5c328726552a`
**Tasks**: `specs/200-dock-centre-triggers/tasks.md` · **sha256** `7c13ba91f310`
**Other artifacts read**: `research.md` `f657d2271345` · `data-model.md` `c10886cdfa49` ·
`checklists/requirements.md` `eff1eec9e8a0c1f4`
**Date**: 2026-11-18

## Metrics

`14 FR · 7 SC · 31 acceptance scenarios · 7 edge cases · 69 traceability rows
(60 test · 5 inspection · 4 manual) · 36 tasks · 14 E2E methods`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | coverage | `plan.md`/`tasks.md` | 60 `test` rows are served by 14 E2E methods; grouping them by method avoids 60 near-identical fixtures | accepted — the plan names the grouping and each method lists the rows it covers; no task dropped |
| A2 | MED | correctness | `research.md` D002 | The notice discriminator treats "same service, null goto, screen changed" as an advance; a re-read that also changed the stored screen index would be mistaken for one | covered — R13's re-read lands where the operator already is, so `screen` is unchanged; `test_other_state_notices_never_centre` (T021) asserts it; no design change |
| A3 | LOW | testing | `tasks.md` T014 | One E2E test waits the real 15 s; no shortened production clock (the `?idle=` override stays in the preview) | accepted — a shipped timing hook would test the hook, not the dock; the wait is isolated in one method |
| A4 | MED | behaviour | `spec.md` FR-006 | In browsing, the crossing morph still changes block heights, which can carry the live row out of view without centring it | accepted as designed — "leave the list where the operator put it" includes that reflow; M1 watches it live so the feel is visible |
| A5 | LOW | honesty | `preview/README.md` | The mode readout exists only in the preview; the real dock has no such indicator | accepted — stated in the preview's "what this is not" section, not added to the product |
| A6 | LOW | gate | `checklists/requirements.md` | All 17 checklist items are unticked; SDD-15 makes them reviewer-owned | presented unticked at Gate 2; an owner who will not tick an item is a change request |
| A7 | LOW | naming | `plan.md` | The gate-1 preview calls the new trigger "an item click"; FR-004 also names the sticky Next band explicitly | consistent — the band is an item, and the spec, card and tasks say so; no change |

## Coverage

Read from `plan.md`'s traceability table, not re-derived from task text. Every row has a component
and a verification method; every `test` row names an E2E method that has a red-first pair in
`tasks.md`.

| Requirement group | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 … FR-014 (14) | ✅ | ✅ | 17 plan rows (FR-004 band and FR-006's three modes split out) |
| SC-001 … SC-007 (7) | ✅ | ✅ | 7 plan rows |
| US1/AC1 … AC7 (7) | ✅ | ✅ | 7 plan rows — T006–T010, T019 |
| US2/AC1 … AC6 (6) | ✅ | ✅ | 6 plan rows — T011–T013 |
| US3/AC1 … AC11 (11) | ✅ | ✅ | 11 plan rows — T014–T018 |
| US4/AC1 … AC8 (8) | ✅ | ✅ | 8 plan rows — T019–T023 |
| Edge cases (7) | ✅ | ✅ | 7 plan rows — T009, T013, T016, T017, T024, T029 |
| Inspection I1–I3 (3) | ✅ | ✅ | 3 plan rows — T026–T028 |
| Manual M1–M3 (3) | ✅ | ✅ | 3 plan rows — T029 |
| **Total** | **69/69** | **69/69** | **100% coverage** |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH**: 0 · **MED**: 2 (A2, A4 — both dispositioned, not
open) · **LOW**: 5

## Applied mechanically

- Fixed the dangling "no" at the end of the `US1/AC7` traceability note.
- Replaced the verification-split placeholder with the measured `60 test · 5 inspection · 4 manual`
  (69 rows) and recorded the 14-method grouping.
- No duplicate IDs, stale paths or terminology drift remained in the plan/task tables.

## Escalated

None — no finding changes intent, scope or an accepted requirement, so no owner question was needed.

## History

- 2026-11-18 — first run against the gate-1-accepted spec: 0 CRITICAL, full coverage; seven LOW/MED
  findings recorded with dispositions; no mechanical fix touched the spec.
