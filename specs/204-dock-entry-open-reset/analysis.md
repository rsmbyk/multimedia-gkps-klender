# Analysis: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`
**Plan**: `specs/204-dock-entry-open-reset/plan.md`
**Tasks**: `specs/204-dock-entry-open-reset/tasks.md`
**Run**: 2026-11-19, after gate 1 (Accept) and the Plan → Checklist → Tasks pass.

## Artifacts read

| File | Digest |
| --- | --- |
| `spec.md` | `3e3510de63b8` |
| `plan.md` | `7f2fce313a30` |
| `research.md` | `685b814f2485` |
| `data-model.md` | `277e5d1653ae` |
| `quickstart.md` | `5eb1f019c170` |
| `tasks.md` | `b58a9d9b2c6b` |
| `checklists/requirements.md` | `808920bb12bb` |

`check_pack_consistency.py` output (re-run after Implement): **PASS COVERAGE 13/13 ids traced ·
PASS SPLIT declared 30/1/0 counted 30/1/0 · PASS ASSIGNMENT 19 plan symbols, 19 in tasks · clean.**

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | record | `specs/README.md` | The spec index has stopped being maintained: its last row is 193 while the base carries specs to 202. Adding a lone row for 204 after that gap reads as an error. | Left as found, per the process rule for an unmaintained index; the owner decides whether to backfill or retire it. Not this slice's work. |
| A2 | LOW | clarity | `spec.md` FR-003 | The on-load open path is vacuous at load — the map is empty in a fresh page — so the requirement's third path cannot fail on its own. | Kept: the rule is uniform across all three paths, and `test_the_on_load_open_keeps_only_the_live_block` pins the observable (only the live block open after a reload with a service on air). No change. |
| A3 | LOW | scope | `spec.md` A5, `obs-dock.js` `sync` L1333-1345 | A go-to adoption never calls `openService`, so overrides survive a go-to detour and are cleared at the next explicit open. While a go-to stands, the service's rows are not drawn. | Existing behaviour, out of scope (A5). Recorded so a later reader does not mistake it for a missed path; no requirement changes. |
| A4 | MED | consistency | `preview/assets/obs-dock.js` | The preview's dock script carries the drafted line gated on `window.__openReset`; after Implement the product's line is unconditional, so the two copies differ by the gate. | Planned, not a gap: T017 is the parity pass — the diff must show only the gate wrapper, and the three probes must reproduce the same numbers. |
| A5 | LOW | evidence | `spec.md` Edge Cases | The mid-crossing switch observation could not confirm a morph was in flight (`is-morph` is absent when the departing block is live and the arriving block was hand-opened). | Already worded as a no-regression observation, not a morph measurement; research D004 carries the same caveat. No change. |

**Coverage**: 100% (13/13 ids, every FR/SC, all 12 story scenarios and the empty-service edge reach a row with a kind) ·
**CRITICAL**: 0 · **HIGH**: 0 · **MED**: 1 (A4, planned) · **LOW**: 4.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T003, T009 | the clear in `openService` |
| FR-002 | ✅ | ✅ T006, T009 | liveness read first, no exception code |
| FR-003 | ✅ | ✅ T003, T008, T011 | one test per open path, one for the re-read non-trigger |
| FR-004 | ✅ | ✅ T012 | spec 198's pin re-run unchanged |
| FR-005 | ✅ | ✅ T013, T014 | bytes + channel; morph frames + scroll |
| FR-006 | ✅ | ✅ T012, T016 | the reload pin; the diff inspection |
| SC-001…SC-006 | ✅ | ✅ T003…T014 | one test per criterion, SC-005 split per event |
| SC-007 | ✅ | ✅ T002, T018 | red-first on the base; the seven-module lane |
| US1/AC1…AC6 | ✅ | ✅ T003…T008 | six scenarios, seven tests (AC6 has two paths) |
| US2/AC1…AC3 | ✅ | ✅ T011, T012 | re-read pin; crossing and reload from spec 198 |
| US3/AC1…AC3 | ✅ | ✅ T013, T014, T015 | no morph, no write, spec 200's centring pin |

## Applied mechanically

- Nothing to fix: the consistency script found no orphan id, no split mismatch and no unassigned
  test symbol, and a read of the pack found no duplicate statement, stale path or terminology
  drift. The line numbers cited in `plan.md` and `research.md` were re-read against the worktree's
  `obs-dock.js` at the base `ab46f384` (`openService` 418, call sites 392/1435/2032,
  `entryOverrides` 101, `effectiveOpen` 556, `toggleBlock` 849, `finishToggleMorph` 838,
  `refreshService` 472, timer 2013).
- The verification split was computed from the table by the script, not hand-counted: 30 test ·
  1 inspection · 0 manual (the empty-service edge row was added at Implement, finding C1 in
  `converge.md`).

## Escalated

- None. No finding changes intent, so no question was put to the owner at this stage. A1 is
  reported for a decision outside this slice; A4 is closed by T017 during Implement.

## History

- **2026-11-19** — first run, after gate 1: 0 CRITICAL, 100% coverage, 5 findings (1 MED planned,
  4 LOW recorded). Gate 2 opened on this report with all 25 checklist items unticked.
- **2026-11-19** — re-run after gate 2 and Implement: the digests above are the post-Implement ones.
  A4 is closed (the preview parity diff is the gate wrapper alone); the split grew to 30 test rows
  with the empty-service edge; the card renumbered to ITEM-216 and the base moved to `ab46f384`
  (both recorded in the spec and the plan). Still 0 CRITICAL, 100% coverage; A1 remains the owner's
  call outside this slice, A2/A3/A5 stand as recorded.
