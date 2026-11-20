# Analysis — spec 205 (dock centre pace)

**Date**: 2026-11-19
**Base commit**: `85319b73` (develop); artifacts read in the working tree of `fix/205-dock-centre-pace`.
**Artifacts read**: spec.md, plan.md, research.md, data-model.md, contracts/README.md, quickstart.md,
tasks.md, checklists/requirements.md, preview/probe.py, preview/README.md.

**Metrics**: FR 3 · SC 3 · stories 2 · tasks 10 · coverage 100% · CRITICAL 0 · HIGH 1 · MEDIUM 1 · LOW 1.

## Coverage (Plan traceability → tasks)

| Requirement | Task(s) | Verified by | Covered |
| --- | --- | --- | --- |
| FR-001 pace | T002, T003–T005 | test (new pace test) | yes |
| FR-001 curve | T002, T006 | test (deceleration guard) | yes |
| FR-002 | T007, T008 | inspection + toggle regression | yes |
| FR-003 reduced | T006 | test | yes |
| FR-003 clamp/cancel | T007 | inspection | yes |
| US1/AC4 | T007 | inspection | yes |
| SC-001 | T009 | manual (probe) | yes |
| SC-002 | T009 | manual (probe) | yes |
| SC-003 | T006 | test | yes |

Every FR, SC and story scenario has a task and a declared verification method. **100%.**

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | HIGH | The pace test's ≤ 280 ms threshold carries 80 ms of slack over the 200 ms glide for headless rAF jitter; develop's 400 ms still fails it. Too tight a threshold would flake; too loose would not distinguish the pace. | Accept — 280 ms separates 200 from 400 with jitter room; prove red-on-base in T004. |
| F2 | MEDIUM | The new test samples with a self-contained `evaluate` (click inside, rAF loop, resolve) — the pattern the existing green guard uses. The frozen-`scrollTop` trap (persistent loop driven by separate Python input) does not apply to this pattern. | Noted — no action; the probe (separate Python-driven reads) uses the fresh-read method for that reason. |
| F3 | LOW | The rapid-advance mean-offset gain is modest at 120 ms (16.0→13.7 px) and larger at 200–300 ms; the per-crossing clamp reversal is unchanged. | Accept — candidate for owner judgement at the live preview; the clamp is out of scope (research D4). |

## Gate checks

- Requirement coverage: 100% · entity coverage: n/a (no entities) · interface coverage: n/a (none).
- Decision provenance: research D1–D5 carry rationale + provenance.
- Constitution conformance: pass (no CONSTITUTION.md).
- Zero unknowns: yes. Verification declared: 4 test · 3 inspection · 2 manual.
- Quickstart runnability: commands run in this worktree (servers up; throwaway test DB named).

**Zero CRITICAL, full coverage — gate 2 may open.** HIGH and below are reported, not fixed silently.

## History

- 2026-11-19 — first run; 0 CRITICAL, 100% coverage; F1–F3 reported.