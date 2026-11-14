# Analysis: the active Tata Ibadah lasts only the browser session

**Date**: 2026-11-03
**Artifacts read**: the spec pack's current blobs (git hash-object, 12 chars):

| Artifact | SHA |
| --- | --- |
| `184-display-session-scope/spec.md` | c64eabacb941 |
| `184-display-session-scope/plan.md` | 0827076e8436 |
| `184-display-session-scope/tasks.md` | 10b776ca92da |
| `184-display-session-scope/data-model.md` | 11067e3627ac |
| `184-display-session-scope/research.md` | 84548ca9e02a |
| `184-display-session-scope/quickstart.md` | bc4420f0dc86 |
| `contracts/none.md` | 6a1be78ed7d8 |
| `checklists/requirements.md` | 8a106fb7004b |

**Metrics**: 10 FR · 5 SC · 2 stories · 7 scenarios · 18 tasks · 23 traceability rows · requirement
coverage **100%** · CRITICAL **0** · HIGH **0** · MEDIUM **1** (fixed) · LOW **5** (2 fixed, 3
accepted).

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F001 | LOW | The state's rules are stated twice: the overview (§The display state, after this slice) and the testable FR-001…FR-005. | Accepted — the overview is the owner's summary at gate 1, the FRs are the contract the tests read; a line-by-line comparison found no divergence. |
| F002 | LOW | The two US2 guards cannot be red first: they characterise behaviour that must not change. | Accepted — recorded at T003 as a green baseline on the untouched code; TDD-01's failing test is about new behaviour, and a "failing" guard would mean a defect, not a specification. |
| F003 | MEDIUM | `plan.md` pointed FR-007's second test at `tests/e2e/test_reading.py`; the test lives in `tests/e2e/test_projector.py:1733`. | Fixed (mechanical) — the row now names `test_projector.py::test_stop_projecting_still_releases_with_the_control_present`; verified by grep. |
| F004 | LOW | The spec cited the throwaway probe by path, which Fold deletes. | Fixed (mechanical) — the sentence now says "a throwaway probe, removed at Fold". |
| F005 | LOW | FR-006's in-page fallback is in tension with FR-004's cross-surface catch-up when cookies are unavailable. | Fixed (mechanical) — the spec's edge case now records that a cookie-less browser makes the page its own session, and names it as the cost. |
| F006 | LOW | The plan's `Preview` is `n/a` while the slice has a visible outcome (an idle start). | Accepted — no appearance changes and no new UI state; the live restart walkthrough stands in, and the spec's UI/UX says so. |

## Coverage notes

- Every FR and SC appears in the plan's traceability table and names a component and a verification
  method; every `test` row maps to at least one task.
- The one `manual` row is the OBS restart (research D008), which this suite cannot drive; it is a
  stated verification, not an untested requirement.
- The checklist's 14 items are unticked and stay the owner's (SDD-15). No item was added or removed
  after Plan.

## History

- 2026-11-03 — pass 1: 1 MEDIUM and 5 LOW findings; the MEDIUM (a stale test path) and two LOWs
  fixed mechanically before reporting, three LOWs accepted with their reasons; requirement coverage
  100%; 0 CRITICAL, 0 HIGH.
