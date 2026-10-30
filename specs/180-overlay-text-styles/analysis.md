# Analysis: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`
**Plan**: `specs/180-overlay-text-styles/plan.md`
**Tasks**: `specs/180-overlay-text-styles/tasks.md`
**Date**: 2026-10-30 · **Base commit**: `59182b12` (the branch has no commits yet; the artifacts below are the working
tree's, hashed with `git hash-object`)

**Artifacts read** · `spec.md a65d6eb5` · `plan.md 141bc52b` · `research.md 4e9f0be6` · `data-model.md ab292a13` ·
`quickstart.md 1e9b943f` · `tasks.md 6b0414b3` · `contracts/README.md 7bb94e56` ·
`checklists/requirements.md 04515589` · `obs-overlay.js 3418db5d` · `obs-overlay.css e843d9c5` ·
`reading/views.py 3cf2de4f` · `test_obs_overlay.py 9d291a8c`

**Metrics**: 27 traced rows (13 `FR-###`, 8 `SC-###`, 6 story rows) · **coverage 100 %** · **CRITICAL 0** ·
HIGH 1 · MED 2 · LOW 2

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | process | `plan.md` §Process note | The implementation predates gate 1: the owner iterated on the live surface during Preview, so `obs-overlay.css`, `obs-overlay.js` and the payload change existed before the spec was accepted. TDD's red-first order was followed per behaviour inside that loop, but the artefacts were written afterwards. | accepted as recorded — the owner's chosen working mode for this slice; Converge re-assesses every row from the code (SDD-22), so nothing rests on a ticked box |
| A2 | MED | numbering | `specs/`, `backlog/` | The slice opened as `165-overlay-text-styles` on `ITEM-178`, but `origin/develop` already carried a merged `specs/165-media-entry-rest` and `ITEM-178-media-entry-rest` — two packs on one number, which SDD-02 and BRD-05 forbid. | fixed before gate 1: renumbered to `180-overlay-text-styles` / `ITEM-180`; branch renamed `feat/180-overlay-text-styles`; every reference in spec, card, board, README and preview rewritten |
| A3 | MED | coverage | `docs/spec/` | No capability file describes the OBS overlay, so there is nothing for the requirements to fold into. | planned — this slice creates `docs/spec/overlay.md` at Fold (`R1`…), as SDD-03 allows for a capability that does not exist yet |
| A4 | LOW | drift | `tests/e2e/test_obs_overlay.py`, `multimedia/web/tests.py` | Two docstrings still name the old slice number ("specs 119 and 165", "Spec 165"). | applied mechanically — rewritten to 180 |
| A5 | LOW | consistency | `contracts/README.md` | The slice exposes no interface, while it consumes three owned elsewhere and widens one payload (`mark`/`words`). | recorded — `none` stated with the consumed interfaces named, and the payload widening called out so a reviewer can see it |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T005, T006, T007 |
| FR-002 | ✅ | ✅ | T010, T011 |
| FR-003 | ✅ | ✅ | T007, T008 |
| FR-004 | ✅ | ✅ | T014 |
| FR-004a | ✅ | ✅ | T015 |
| FR-005 | ✅ | ✅ | T009 |
| FR-006 | ✅ | ✅ | T009 |
| FR-007 | ✅ | ✅ | T012, T013 |
| FR-008 | ✅ | ✅ | T026, T027 |
| FR-009 | ✅ | ✅ | T026 |
| FR-010 | ✅ | ✅ | T003, T004, T016, T017 |
| FR-011 | ✅ | ✅ | T019, T020, T025 |
| FR-012 | ✅ | ✅ | T021, T022, T025 |
| FR-013 | ✅ | ✅ | T023, T024, T025 |
| SC-001 | ✅ | ✅ | T011 (caption untouched), inspected at 1920 |
| SC-002 | ✅ | ✅ | T009 |
| SC-002a | ✅ | ✅ | T015 |
| SC-003 | ✅ | ✅ | T007 |
| SC-004 | ✅ | ✅ | T014, T015 |
| SC-005 | ✅ | ✅ | T026 |
| SC-006 | ✅ | ✅ | T012, T013 |
| SC-007 | ✅ | ✅ | T019, T021, T023 |
| US1/AC2 | ✅ | ✅ | T007 |
| US1/AC3 | ✅ | ✅ | T008, T018 |
| US2/AC4 | ✅ | ✅ | T018 |
| US2/AC5 | ✅ | ✅ | T014 |
| US3/AC3 | ✅ | ✅ | T023, T024 |

**Coverage**: 100 % · **CRITICAL**: 0 · **HIGH/MED/LOW**: 1 / 2 / 2

## Applied mechanically

- Slice and card renumbered from 165 / ITEM-178 to 180 / ITEM-180 across the spec pack, the card, the board row, the
  specs index and the three preview pages (A2).
- Docstring drift to the old number in the two test modules (A4).
- The board row's spec cell and the specs index label still read `165` after the rename; both rewritten to `180`.
- The plan's traceability table and the spec's requirement IDs were cross-checked in both directions: no requirement
  without a row, no row without a requirement, no duplicated ID.

## Escalated

- A1 is the only finding the owner has to weigh: the slice's code preceded its paperwork. It changes nothing about
  what Converge checks — every row is assessed from the code, not from `tasks.md`'s ticks — but it does mean gate 1
  approved a spec written *after* the behaviour existed, and the owner should know that when reading the spec's
  `## UI/UX`.

## History

| Run | Date | Base | Coverage | CRITICAL | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-30 | `59182b12` | 100 % | 0 | first analysis, at gate 1 acceptance; A2 renumber applied before the run; spec.md re-read at `a65d6eb5` after the 34–90 % assumption was corrected |
