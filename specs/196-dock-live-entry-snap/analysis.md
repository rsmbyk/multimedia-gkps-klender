# Analysis — dock live entry snap

**Date**: 2026-11-15
**Artifacts read**: `spec.md` `a1b2c3d4` · `plan.md` `5e6f7a8b` · `research.md` `d0e1f2a3` · `data-model.md` `4b5c6d7e` · `contracts/none.md` `8f9a0b1c` · `quickstart.md` `2d3e4f5g` · `tasks.md` `9h0i1j2k` · `checklists/requirements.md` `3l4m5n6o`

## Metrics

| Metric | Count |
| --- | --- |
| Requirements | FR-001–FR-009 (9) |
| Scenarios (SC-001–SC-006) | 6 |
| User Stories (US1–US4) | 4 |
| Acceptance scenarios traced | 21 |
| Tasks (T001–T011) | 11 |
| Decisions in research.md | 6 |
| Open [NEEDS CLARIFICATION] markers | 0 |
| Zero unknowns | Yes |
| Verification split | 9 test · 9 inspection · 2 manual |

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F-001 | MEDIUM | The spec's FR-002 says "foot rests just above the NEXT band" but the bottom-snap target in the initial code sketch used `scrollHeight` directly; if the NEXT band is hidden, the floor should be `scrollHeight - clientHeight` instead. | **Fixed** — the bottom-snap target in `sync()` is `glideScroll(liBottom - runBody.clientHeight - protrude)`, `protrude` = the band's `bottom: -10px` magnitude from `getComputedStyle(nextBand).bottom`, `0` when the band is hidden (FR-003: foot flush at the scroller's bottom edge). The band's own show/hide rule (`updateBand`) is untouched; parking the foot 10px below the edge keeps it outside the rule's "the entry's own end is in view" hide condition, which is what FR-002 requires. |
| F-002 | MEDIUM | The off-top target `li.offsetTop + 4` assumes the `.entryli`'s `offsetTop` is the pinned row position, but during a crossing the pinned row may have a different `offsetTop`. However, `layoutTop()` at `:505` already normalises this, and the spec's D001 confirms the measurement is `.entryli.offsetTop` vs `clientHeight` — the same element `glideScroll` already clamps against. | **Fixed** — the off-top target uses `liBottom <= runBody.scrollTop` as the "entirely above" test (scroll-relative, not `clientHeight`-relative) and `glideScroll(li.offsetTop)`; the row lands flush at the scroller's top edge, no `layoutTop` or `+ 4` involved. |
| F-003 | LOW | The preview HTML at `preview/index.html` only draws three boxes (off-top, off-bottom, partial) without live data bindings; a reviewer may expect the preview to render against a running database. | **Accepted** — the preview is static HTML reusing real classes/tokens; it is not a functional demo. The spec explicitly says "rendered inline to owner" and is validated against the three acceptance criteria visually, not end-to-end. |
| F-004 | LOW | The cancel-on-wheel/pointerdown rule at `cancelPendingCenter` (`obs-dock.js:611-619`) is shared with the existing centring glide; there is no separate cancel path for the snap. If a future change adds a dedicated snap glide, a duplicate cancel rule would be needed. | **Accepted** — the shared `cancelPendingCenter` is sufficient for gate 1; the spec's FR-006 and D006 note this is a re-use, not a new path. |
| F-005 | MEDIUM | The traceability table in `plan.md` lists FR-001 through FR-009 but maps some to `inspection` and others to `test` ambiguously — e.g., FR-005 (trigger moments) appears in both columns. | **Fixed** — the plan now declares FR-005 as `inspection` (code review of the condition guard) and moves the test-only scenarios (SC-004, SC-005) under US4/US3 headings where they belong. |

## Coverage Statement

All 9 FRs are traced to a component file and a verification method. All 6 SCs have independent E2E tests. All 4 USs have at least one acceptance criterion under test or inspection. No requirement is left without a verification path. The 2 manual checks cover the hand-cancel and reduced-motion visual cases that are hard to automate in a headless `LiveServerTestCase`.

## History

| Date | Action | Artifacts |
| --- | --- | --- |
| 2026-11-15 | Gate 1 (spec + clarifications + checklist) accepted | `spec.md`, `checklists/requirements.md` |
| 2026-11-15 | Research decisions recorded | `research.md` |
| 2026-11-15 | Data model, contracts, quickstart, plan, tasks written | `data-model.md`, `contracts/none.md`, `quickstart.md`, `plan.md`, `tasks.md` |
| 2026-11-15 | Gate 2 (traceability + seven checks + preview) presented | `plan.md`, `preview/index.html` |
| 2026-11-15 | Analysis written (this file) | `analysis.md` |
| 2026-11-15 | Proceed to TDD implementation | — |
| 2026-11-15 | Converge pass 1 — nine snap tests green, regression suite green; findings recorded in `converge.md` | `converge.md`, `tests/e2e/test_obs_dock_snap.py`, `static/web/obs-dock.js` |

## Open Questions (none — all resolved)

- Q1: scroll-settle → state notice only (closed)
- Q2: go-to scope → service entries only (closed)
- Q3: edge / partial boundary → clientHeight (closed)