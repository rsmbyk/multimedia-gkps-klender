# Analysis: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`
**Plan**: `specs/185-dock-goto/plan.md`
**Tasks**: `specs/185-dock-goto/tasks.md`

**Run**: 2026-11-04 · artifacts read at `spec.md` db3bfdfeac95 · `plan.md` 64c78122571c ·
`research.md` 0a84e30afad8 · `data-model.md` acb1afa3c2b6 · `quickstart.md` 27d9c38e173d ·
`tasks.md` 912ed6542658 · `contracts/display-state.md` 2ad98d8e0a3a ·
`checklists/requirements.md` ecb0fe78f2a4.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MEDIUM | coverage | `tasks.md` | SC-006 (the dock uses the projector's own lookup) had a `test` row in Plan and no task carrying it. | applied — the test joined T006, and T007 now names the label agreement it proves |
| A2 | LOW | stale reference | `research.md` | D001 cited `display.js:99-131`; the verb block is lines 96–132. | applied — corrected |
| A3 | LOW | verification | `plan.md` | FR-013 ("no new endpoint, no new key") is an `inspection` row, so nothing runs it locally; it is read at Converge against the diff. | reported — the inspection is named in the traceability row and belongs to Converge |
| A4 | LOW | wording | `plan.md` | The Bump line cites the neighbourhood by count (23 of 26 `patch`), which will drift as plans are added. | accepted — it names the two governing neighbours (183, 184) as well |

## Coverage

Coverage reads Plan's traceability table, not the task list re-derived.

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002, T003 |
| FR-002 | ✅ | ✅ | T003, T004 |
| FR-003 | ✅ | ✅ | T002, T027 |
| FR-004 | ✅ | ✅ | T006, T007 |
| FR-005 | ✅ | ✅ | T006, T007 |
| FR-006 | ✅ | ✅ | T008, T009 |
| FR-007 | ✅ | ✅ | T010, T011 |
| FR-008 | ✅ | ✅ | T020, T021 |
| FR-009 | ✅ | ✅ | T022, T023 |
| FR-010 | ✅ | ✅ | T016, T017 |
| FR-011 | ✅ | ✅ | T014, T015 |
| FR-012 | ✅ | ✅ | T018, T019 |
| FR-013 | ✅ | ✅ | T002 (no new key), T015 (existing endpoints); inspection at Converge |
| FR-014 | ✅ | ✅ | T014, T015 |
| FR-015 | ✅ | ✅ | T020, T021 |
| FR-016 | ✅ | ✅ | T028, T029 |
| FR-017 | ✅ | ✅ | T010, T011 |
| FR-018 | ✅ | ✅ | T012, T013 |
| FR-019 | ✅ | ✅ | T024, T025 |
| SC-001 | ✅ | ✅ | T006, T008 |
| SC-002 | ✅ | ✅ | T020 |
| SC-003 | ✅ | ✅ | T014 |
| SC-004 | ✅ | ✅ | T026 |
| SC-005 | ✅ | ✅ | T026 (the stored-JSON read) |
| SC-006 | ✅ | ✅ | T006, T007 |
| US1/AC1 | ✅ | ✅ | T006, T007 |
| US1/AC2 | ✅ | ✅ | T006, T007 |
| US1/AC3 | ✅ | ✅ | T008, T009 |
| US1/AC4 | ✅ | ✅ | T012, T013 |
| US1/AC5 | ✅ | ✅ | T006, T007 |
| US2/AC1 | ✅ | ✅ | T014, T015 |
| US2/AC2 | ✅ | ✅ | T020, T021 |
| US2/AC3 | ✅ | ✅ | T014, T015 |
| US2/AC4 | ✅ | ✅ | T016, T017 |
| US3/AC1 | ✅ | ✅ | T020, T021 |
| US3/AC2 | ✅ | ✅ | T010, T011 |
| US3/AC3 | ✅ | ✅ | T010, T011 |
| US4/AC1 | ✅ | ✅ | T026, T027 |
| US4/AC2 | ✅ | ✅ | T026, T027 |
| US4/AC3 | ✅ | ✅ | T026, T027 |
| Edge cases (14) | ✅ | ✅ | carried by the requirements above; the corrupt-state and concurrent-start ones by T002 and T004 |

**Coverage**: 100% of the 40 traceability rows · **CRITICAL**: 0 · **HIGH/MED/LOW**: 0 / 1 / 3

## Applied mechanically

- A1: `test_the_same_lookup_answers_both_surfaces` added to T006; T007 widened to name the label
  agreement. Delta re-read against `plan.md`'s SC-006 row, which already pointed at that module.
- A2: the line range in `research.md` D001 corrected to `96-132`.
- Terminology: "find band", "go to block", "the layer" are used with one meaning across spec, plan,
  contracts and tasks; the classes (`.findband`, `.offblock`, `.findscrim`) appear only where the
  code port is described, and match the preview's own names.
- Paths: every `file:line` in `research.md` was re-opened on this branch (`display.js:42-56`,
  `display.js:96-132`, `projector.js:1321-1437`, `obs-overlay.js:292-300`, `obs-dock.js:836-878`).

## Escalated

None. No finding changes a requirement's meaning, so nothing was asked.
