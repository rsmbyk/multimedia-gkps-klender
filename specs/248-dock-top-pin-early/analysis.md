# Analysis: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`
**Plan**: `specs/248-dock-top-pin-early/plan.md`
**Tasks**: `specs/248-dock-top-pin-early/tasks.md`
**Date**: 2026-11-28

## Artifacts read

| Artifact | SHA-1 |
| --- | --- |
| `spec.md` | `205fd7c2910b68449620e8664cb4ee2cb75d9356` |
| `plan.md` | `2187d9ea12e407857e7e6c35f04959552c85bce6` |
| `tasks.md` | `32e59784193d2d2fb3fe9729d6065003d8706605` |
| `checklists/requirements.md` | `e69a5a40c5c5e0cb71622a1a962907f504bff21b` |

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MED | terminology | existing `tests/e2e/test_dock_top_pin.py` | `SAMPLER` and `test_the_top_pin_tracks_the_block_per_frame` still assert `blockBottom <= 0.5`, the superseded R19 boundary | task T009 updates them to `blockTop <= 0.5`; the losing wording is kept in the spec's Clarifications |
| A2 | MED | scope | `spec.md` US1/AC3 | the carried-over "no service pin during a Go To" claim is false on unmodified develop (manual check: pin visible, offstrip unchanged, 21 rows) | retraction kept in the spec; scenario narrowed to the `.offstrip` and recorded as research D006 and task T013 |
| A3 | LOW | process | `spec.md` §Assumptions | the code/CSS preview edit preceded the written pack by one step | disclosed as live-preview chronology, no pre-Fold commit |
| A4 | LOW | evidence | `plan.md` | full browser suite deferred to the push step by repo preference | declared in `quickstart.md`; targeted modules named and run with a throwaway DB |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T005, T006, T007, T008 |
| FR-002 | ✅ | ✅ | T009, T010, T014 |
| FR-003 | ✅ | ✅ | T011 |
| FR-004 | ✅ | ✅ | T012, T013 |
| SC-001 | ✅ | ✅ | T003, T014 (probe numbers frozen at gate 1) |
| SC-002 | ✅ | ✅ | T005, T009 |
| SC-003 | ✅ | ✅ | T015 |
| US1/AC1 | ✅ | ✅ | T005, T007 |
| US1/AC2 | ✅ | ✅ | T006, T008 |
| US1/AC3 | ✅ | ✅ | T013 (manual) |
| US2/AC1 | ✅ | ✅ | T002 share, T014 |
| US2/AC2 | ✅ | ✅ | T012 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 2 MED, 2 LOW

## Applied mechanically

- No duplicate FR/SC IDs; every capability reference resolves to `dock/R19` (modified) or an
  unchanged block. `contracts/README.md` says `none` explicitly. The checklist carries 12 unticked
  reviewer-owned items, each with a quality dimension and a section marker.

## Escalated

- None. A1 is a stale assertion caused by the owner-approved boundary change, not a conflict between
  two requirements; its task carries the update and the old wording remains in the record.

## History

- 2026-11-28 — first run: zero CRITICAL, 100% coverage, one MED stale-test finding assigned to T009.
- 2026-11-28 — second run after the Go To manual check: A2 raised to MED (a carried-over claim is
  false on develop) and kept as an explicit retraction; still zero CRITICAL and 100% coverage.
