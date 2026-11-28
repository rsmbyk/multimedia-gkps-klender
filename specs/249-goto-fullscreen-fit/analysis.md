# Analyze: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`
**Plan**: `specs/249-goto-fullscreen-fit/plan.md`
**Tasks**: `specs/249-goto-fullscreen-fit/tasks.md`
**Date**: 2026-11-27
**Read**: `spec.md` @ `5faa2259a800624f`, `plan.md` @ `09a582e3dca87c89`,
`tasks.md` @ `d292eeb6ed18a224`, `research.md` @ `38f96e0c4c9072d1`,
`data-model.md` @ `31b2285f10ca61fb`, `quickstart.md` @ `a1f94df5ea83be29`,
`checklists/requirements.md` @ `ad83608462b698c9` (8 items, 0 ticked — reviewer-owned)
**Metrics**: 5 FR · 3 SC · 4 AC · 12 traceability rows · 13 tasks · 8 checklist items ·
0 CRITICAL · 1 LOW · coverage 100%

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F001 | — | Every FR, SC and scenario has a component and a `Verified by` row; each new test row has a red and a green task. | none needed |
| F002 | LOW | The fonts-ready path still clears the detour's key without fitting it, so bundled faces arriving while a detour is up leave the same stale size. | reported and recorded in §Assumptions and `quickstart.md`; not the reported trigger, and widening the slice would double the verification surface |
| F003 | — | No requirement contradicts `docs/spec/projector.md`: R14 already says the size must not depend on how a screen was reached; the detour is a screen on the stage and spec 247's fix missed its resize path. | none needed |
| F004 | — | Terminology is stable across spec, plan and tasks: "detour", "stage screen", "fit key", "signal ordering". | none needed |
| F005 | — | `checklists/requirements.md` is generated and unticked, as gate 2 expects. | none needed |
| F006 | — | The production edit is already in the worktree from the gate-1 preview; red tasks revert that one file under a trap. | recorded in the spec's Assumptions |
| F007 | — | The headless harness cannot make an OS fullscreen; CDP viewport changes deliver the same `resize` geometry signal, and the cases assert rendered sizes. | recorded in `quickstart.md` |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T004 + T006 | resize fits the stage screen |
| FR-002 | ✅ | ✅ T005 + T006 | signal-first ordering |
| FR-003 | ✅ | ✅ T004 + T006 | key follows both directions |
| FR-004 | ✅ | ✅ T007 + T009 | service screens and neighbours unchanged |
| FR-005 | ✅ | ✅ T009 | diff scope |
| SC-001 | ✅ | ✅ T004 | resize-only probe numbers |
| SC-002 | ✅ | ✅ T005 | signal-first probe numbers |
| SC-003 | ✅ | ✅ T004 + T009 | detour state, URL, service screens |
| US1/AC1 | ✅ | ✅ T004 | resize grows the detour |
| US1/AC2 | ✅ | ✅ T004 | return restores the size |
| US1/AC3 | ✅ | ✅ T005 | signal before resize |
| US1/AC4 | ✅ | ✅ T007 | no detour |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED**: 0 · **LOW**: 1 (F002)

## Applied mechanically

- The E2E assertions are relational, not the probe's absolute numbers: the test fixture's long
  passage fits at `42px` at 1440×900 and grows with a bigger stage, while the live probe's service
  reads `87 → 109px`. No acceptance criterion changed; `tasks.md` and `quickstart.md` name the
  correct source for each set.
- The no-detour guard case is green on the unmodified base as well as the slice; its docstring says
  so. The two behaviour cases each have an honest red assertion.

## Red / green evidence

- Red (merged 247 file restored under a trap): `FF.` — detour `42 → 42` with the key still
  `1376x804|…` at stage 984, in both signal orderings; guard green.
- Green (slice file restored): `...` — three cases, 0 failures, throwaway `test_gkps249`, 12.5 s.

## Escalated

- None. F002 is reported with its cost and stays open as a LOW finding; it does not change an
  acceptance criterion.

## Gate record

- **Gate 1** accepted 2026-11-27: `spec.md`, live preview at 8772, `## UI/UX` numbers, all
  assumptions, zero `[NEEDS CLARIFICATION]` markers.
- **Gate 2** accepted 2026-11-27. The eight checklist items were presented unticked and remain
  unticked: checklist items are reviewer-owned and this agent does not tick them (SDD-15), and the
  gate-2 rule that an unticked item is a change request (SDD-18) was therefore not applied. That is
  recorded here as a bypass with the owner's word behind it, not as a silent skip. Implement →
  Converge → Fold followed without re-presenting a gate.

## History

- 2026-11-27 — first run: 0 CRITICAL, 0 HIGH, 1 LOW (F002), coverage 100%.
