# Analyze: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`
**Plan**: `specs/247-projector-fullscreen-fit/plan.md`
**Tasks**: `specs/247-projector-fullscreen-fit/tasks.md`
**Date**: 2026-11-27
**Read**: `spec.md` @ `559faa7dc3ef20fb`, `plan.md` @ `0c86f399eee0d3f5`,
`tasks.md` @ `78beecc61bea9266`, `research.md` @ `a914cde580dcb4ba`,
`data-model.md` @ `f13c40c726fc9582`, `quickstart.md` @ `e97abc92b320ef39`,
`checklists/requirements.md` @ `3f03d6304a487039` (12 items, 0 ticked — reviewer-owned)
**Metrics**: 6 FR · 4 SC · 7 AC · 17 traceability rows · 19 tasks · 12 checklist items ·
0 CRITICAL · 0 HIGH · 4 LOW · coverage 100%

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F001 | — | Every FR, SC and story scenario has a component and a `Verified by` row in `plan.md`, and each new test row has a red and a green task. | none needed |
| F002 | LOW | The headless harness cannot produce an OS-level fullscreen, so the E2E cases change the stage box and dispatch the browser signals; the probe's numbers and the owner's live report cover the real gestures. | reported, not fixed — the seam is the rendered size after a public signal, not the OS transition |
| F003 | LOW | Safari's `(display-mode: fullscreen)` behaviour is unverified; the display-mode listener may not fire there. | reported, not fixed — the existing `resize` path stays, and the accepted spec records the limit |
| F004 | LOW | US1/AC3 (Go To detour on the stage) is verified `manual` rather than by a new E2E case. | reported; a future regression in the detour branch would not be caught by the targeted module |
| F005 | — | Terminology is stable: "fit", "remembered fit", "stage", "fullscreen signal" each name one thing across spec, plan and tasks. | none needed |
| F006 | — | No requirement contradicts `docs/spec/projector.md`: R14 speaks of arrival, jump and resize but not fullscreen, so this is a modified block with a regression note, not a new `R<n>`. | none needed |
| F007 | LOW | The production edit is already in the worktree from the gate-1 preview; red tasks temporarily revert that one file under a trap. | reported, not fixed — the chronology is stated in the spec's Assumptions and in `tasks.md` |
| F008 | — | `checklists/requirements.md` is generated and unticked, as gate 2 expects. | none needed |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T004 + T008 | re-fit on `fullscreenchange` |
| FR-002 | ✅ | ✅ T009 + T011 | re-fit on display-mode change |
| FR-003 | ✅ | ✅ T005 + T008 | settled stage and remembered key |
| FR-004 | ✅ | ✅ T006 + T008 | neighbours fitted in idle time |
| FR-005 | ✅ | ✅ T010 + T012 | existing paths and controls unchanged |
| FR-006 | ✅ | ✅ T012 | diff scope |
| SC-001 | ✅ | ✅ T003 + T004 | lines 87 → 93 → 87 |
| SC-002 | ✅ | ✅ T003 + T004 | heading 53.769 → 57.4772 → 53.769 |
| SC-003 | ✅ | ✅ T010 + T011 | 87 → 109 → 87 under CDP resize |
| SC-004 | ✅ | ✅ T004 + T012 | URL, index and text unchanged |
| US1/AC1 | ✅ | ✅ T004 | grows without resize |
| US1/AC2 | ✅ | ✅ T005 | repeat signal is a no-op |
| US1/AC3 | ✅ | ✅ T013 (manual) | detour on the stage |
| US1/AC4 | ✅ | ✅ T007 | unchanged stage |
| US2/AC1 | ✅ | ✅ T010 | resize-driven agreement |
| US2/AC2 | ✅ | ✅ T009 | F11 display-mode signal |
| US2/AC3 | ✅ | ✅ T012 + T011 | keys, zones, cue and takeover |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 4 LOW (F002, F003, F004, F007)

## Applied mechanically

- The E2E assertions were written relationally, not with the preview's absolute numbers. The
  fixture's long text fits at `42px` at 1440×900 and `49px` in the grown stage, while the live
  probe's service fits at `87 → 93px`; `tasks.md`, `quickstart.md` and this report name the correct
  source for each set. No acceptance criterion changed.
- Three of the six new cases are characterisation guards, green on the unmodified base: the repeat
  signal (FR-003), the unchanged stage (US1/AC4) and the resize-driven path (SC-003). Their
  docstrings say so; the three behaviour cases each have an honest red assertion.
- `quickstart.md` now names the six targeted cases rather than the whole projector module, whose
  known-red display-off tests are outside this slice.

## Red / green evidence

- Red (base `projector.js` restored under a trap): `F.F.F.` — three failures naming the exact wrong
  values (`42 not greater than 42` for active lines at stage 1004, `125 not greater than 125` for
  the neighbour, `42 not greater than 42` on the display-mode-only signal); three guard cases green.
- Green (slice file restored): `......` — six cases, 0 failures, throwaway `test_gkps247`, 20.7 s.

## Escalated

- None. F002–F004 and F007 are reported with their cost and stay open as LOW findings; none
  changes an acceptance criterion or a requirement.

## Gate record

- **Gate 1** accepted 2026-11-27: `spec.md`, live preview at 8771, `## UI/UX` numbers, all
  assumptions, zero `[NEEDS CLARIFICATION]` markers.
- **Gate 2** accepted 2026-11-27. The twelve checklist items were presented unticked and remain
  unticked: checklist items are reviewer-owned and this agent does not tick them (SDD-15), and the
  gate-2 rule that an unticked item is a change request (SDD-18) was therefore not applied. That is
  recorded here as a bypass with the owner's word behind it, not as a silent skip. Implement →
  Converge → Fold followed without re-presenting a gate.

## History

- 2026-11-27 — first run: 0 CRITICAL, 0 HIGH, 4 LOW (F002, F003, F004, F007), coverage 100%.
