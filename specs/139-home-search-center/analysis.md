# Analysis: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center` · **Date**: 2026-10-27
**Artifacts read** (sha256, first 12): `spec.md` `b5732c6fbd7e` · `plan.md` `5e7b09194d46` ·
`tasks.md` `3a552a8db0dd` · `research.md`, `data-model.md`, `contracts/none.md`, `quickstart.md`,
`checklists/requirements.md`, `preview/after.css`.

## Metrics

| Measure | Value |
| --- | --- |
| Functional requirements | 6 (FR-001 … FR-006) — all mapped in Plan's traceability and all tasked |
| Success criteria | 4 (SC-001 … SC-004) — all mapped and tasked |
| User stories / scenarios | 2 / 6 — all six in traceability |
| Key entities | 0 declared (stated in `data-model.md`) |
| Interfaces | 0 (stated in `contracts/none.md`) |
| Tasks | 14 — 1 baseline, 1 foundation, 7 test, 2 code, 3 delivery |
| Verification split | 19 test · 0 inspection · 0 manual |
| Coverage | 100% of requirements and criteria have a task and a verification |
| CRITICAL | 0 |

**Zero CRITICAL, full coverage — gate 2 condition met.**

## Findings

| # | Severity | Dimension | Finding | Disposition |
| --- | --- | --- | --- | --- |
| F1 | HIGH | Verifiability | FR-001 promised "every width from 320px to 1920px … at every height that fits", a domain no criterion can test; SC-001 names eleven pairs. The requirement claimed more than the slice verifies. | **Fixed (mechanical)** — FR-001 now names SC-001's eleven pairs as the acceptance set and states what the set covers: both layout switches, 1272px and 720px. |
| F2 | HIGH | Consistency | `quickstart.md` ran `.venv/bin/python`, which does not exist in a slice worktree (the venv lives in the main checkout). The test command as written could not run. | **Fixed (mechanical)** — both commands now use `../multimedia-gkps-klender/.venv/bin/python`. |
| F3 | MEDIUM | Consistency | `plan.md`'s verification split read "18 test" while its traceability table carries 19 rows. | **Fixed (mechanical)** — split corrected to **19 test · 0 inspection · 0 manual**. |
| F4 | MEDIUM | Consistency | `spec.md`'s Status still read *Draft* after gate 1 accepted it, so the pack disagreed with its own record. | **Fixed (mechanical)** — Status now records the acceptance, the date, and that the block-centred alternative was offered and declined. |
| F5 | LOW | Clarity | The `## UI/UX` table shows 7 of SC-001's 11 viewports. | **Accepted** — the table is the readable sample; SC-001 is the criterion and the E2E module covers all eleven. |
| F6 | LOW | Runnability | `preview/build_preview.py` takes its source URL from the command line and fails with a connection error if nothing is listening. | **Accepted** — the default is the compose `web` service, the quickstart says "from a running instance", and the preview's committed pages are readable without it. |

## Gate 2 readiness

- Zero CRITICAL; every HIGH and MEDIUM disposed of above and re-checked against the artifacts.
- 100% coverage from Plan's traceability table: each FR and SC has a component and a declared method.
- Checklist items are unticked (reviewer-owned, SDD-15) and appended, never replaced.
- `quickstart.md` runs: the preview and the probe both executed for this slice. The test command is
  marked *not yet runnable*, with its reason — the module is written in T002/T003–T011.

## History

- 2026-10-27 — first run against the pack as specified: 4 findings (2 HIGH, 2 MEDIUM), all mechanical
  fixes applied and reported as the delta above; re-run declares 0 CRITICAL and full coverage.
