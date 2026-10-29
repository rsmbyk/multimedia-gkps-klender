# Analysis: dismissing the file picker leaves the New media dialog open

**Date**: 2026-10-29 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `d9940516b488` |
| `plan.md` | `8d13db4b6f32` |
| `research.md` | `e093687108f7` |
| `data-model.md` | `2a229c367efe` |
| `contracts/none.md` | `209a51d0509f` |
| `quickstart.md` | `def699dd18d5` |
| `tasks.md` | `646d151d9565` |
| `checklists/requirements.md` | `4ce33df8ded2` |

**Metrics**: 4 requirements · 4 success criteria · 7 story scenarios · 5 edge cases (21 traceability
rows) · 15 tasks (6 writing or driving tests) · coverage **100%** · CRITICAL **0**.
Counted from `plan.md`'s traceability table: `13 test · 7 inspection · 1 manual`, matching the declared
split; 15 tasks `T001–T015`; 8 checklist items.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | **high** | SC-004 says "the existing browser suite stays green", but it is not green on `develop`: `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` is red there (ITEM-156), and the board lists further reds (ITEM-137, 139, 140, 141, 144, 153, 159). As written the criterion is unmet before this slice starts. | **Reported at gate 2, owner decides.** Recommendation: read SC-004 as *no case that is green on `develop` turns red here*, and evidence it by running `tests.e2e.test_media_library` against a `develop` baseline and against the branch and comparing the two results. The alternative — editing SC-004 — is a change to an accepted acceptance criterion, which is the owner's, not the agent's. |
| F2 | low | FR-001 is one row carrying both directions of the rule (a descendant's `cancel` must not close; the dialog's own must). | Kept: naming both cases in the row keeps the requirement and its evidence in one line; splitting it would create two requirements that can only ever be read together. |
| F3 | low | T005's case (`Escape still closes`) is green before the fix, so it cannot be the red half of a red→green pair. | Accepted as the guard D003 describes: it is red against the wrong fix (deleting the listener), which is the candidate a hurried change would pick. Recorded, not treated as a satisfied `test` row by itself — T002–T004 carry the red. |
| F4 | none | US1 AC4's event path depends on the hidden file input still being in the page while the Upload panel is hidden — true today, because the panels toggle the `hidden` attribute rather than being removed (`media-entry.js:106`). | Recorded so a future refactor that detaches the panel knows it would take this case's premise with it. |
| F5 | none | The `cancel` event's `cancelable` flag differs by source (`true` at the dialog, `false` at the input), so it looks like a discriminator and is not one — `event.preventDefault()` at the dialog would also be a no-op on the input's event. | Recorded in `data-model.md`; the rule is written on `target`, which is the only stable difference. |

No mechanical fixes were needed at this run.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002, T005, T007 |
| FR-002 | ✅ | ✅ | T002, T003, T007 |
| FR-003 | ✅ | ✅ | T005, T009 |
| FR-004 | ✅ | ✅ | T010 |
| SC-001 | ✅ | ✅ | T002 |
| SC-002 | ✅ | ✅ | T003 |
| SC-003 | ✅ | ✅ | T005 |
| SC-004 | ✅ | ✅ | T008 (module run), F1 |
| US1 AC1…AC4 | ✅ | ✅ | T002, T003, T004 |
| US2 AC1…AC3 | ✅ | ✅ | T005, T009 |
| 5 edge cases | ✅ | ✅ | T003 (re-pick), T009, T010, plan rows 17–20 (`inspection`) |
| the live row | ✅ | ✅ | T015 (`manual`) |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH**: 1 (F1) · **LOW**: 2 (F2, F3) · notes: 2 (F4, F5).

## Applied mechanically

- **Case count reconciled before this run**: `plan.md` first said "two new cases" while its traceability
  table named four; the Technical Context, the scope row and the design sketch now all say four, and the
  library-selection case is in the sketch. The declared split was already `13 / 7 / 1` and still counts the
  same 21 rows.

## Escalated

- **F1** — the only finding that can change what an accepted criterion means. It is on screen at gate 2
  with the recommendation above.

## History

- **2026-10-29 — first run**, on the accepted spec, the plan, the checklist and the tasks: 21 traceability
  rows counted against a declared `13 / 7 / 1` (match), 15 tasks, 8 checklist items, coverage 100%, zero
  CRITICAL. Five findings — one high (SC-004's wording against a `develop` that is already red), two low
  (FR-001's two directions in one row; the escape case cannot be red before the fix), two notes (the
  library-selection case rests on a hidden panel keeping its input; `cancelable` is not the discriminator).

- **2026-10-29 — implement, T006's red run**: against the unmodified `static/web/media-entry.js`, the
  three dismissal cases failed where they are meant to — `dialog.evaluate('modal => modal.open')` was
  `False` 400 ms after the input's `cancel`, all three at that same assertion — and
  `test_escape_still_closes_the_new_media_dialog` passed, as F3 predicted (`Ran 4 tests … FAILED
  (failures=3)`).
- **2026-10-29 — implement, T008's green run**: after the guard, the same four cases plus the two
  neighbouring create-dialog cases — `Ran 6 tests … OK` in 14.6s.
- **2026-10-29 — implement, SC-004's module run**: `Ran 42 tests in 114.98s`, one failure —
  `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` (`19.709564208984375 != 12 within 1
  delta`), the pre-existing red ITEM-156 records on `develop`. No case that is green on `develop` turned
  red here.
- **2026-10-29 — convergence, the live row**: `preview/picker_probe.py` against
  `http://localhost:8814/tatib/149/` returned `OK` — the dialog, its typed title (`Closing hymn`) and its
  chosen file (`swatch.png`, Save enabled) all survived the input's `cancel`, and Escape on the dialog
  still closed it. The real system picker stays the owner's own check (`T015`).
- **2026-10-29 — rebase before delivery**: `origin/develop` had moved to `f8e0bb81` (19 commits) and taken
  `VERSION` to `1.23.0`, `reading/R28…R31` and the board through `ITEM-175`. Rebased; this slice's numbers
  are now `1.23.1` (patch), `R32` and `ITEM-176`. The four cases were re-run on the new base — `Ran 4
  tests … OK` — and the probe was re-run against the rebased tree — `OK`. The module on the new base:
  `Ran 46 tests in 292.7s`, one failure — `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
  (`19.753570556640625 != 12 within 1 delta`), ITEM-156's pre-existing red and nothing else.
