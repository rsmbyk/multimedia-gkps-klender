# Analysis 213: a slot states the kind it resolves to

**Date**: 2026-11-21
**Artifacts read**: `spec.md` (10,808 B), `plan.md` (8,502 B), `tasks.md` (4,912 B),
`research.md` (9,119 B), `data-model.md` (1,226 B), `contracts/stage-markup.md` (2,172 B),
`checklists/requirements.md` (14 items), `preview/README.md`

**Metrics**: 7 FR · 5 SC · 3 user stories (9 acceptance scenarios) · 4 edge cases · 18 tasks ·
13 test / 2 inspection / 0 manual · 0 `[NEEDS CLARIFICATION]` · 1 card (ITEM-228) · 1 anchor issue
(#562) · `bump: patch`

## Findings

| # | Severity | Category | Location | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | — | Coverage | `plan.md` Traceability | every FR-001…FR-007 and SC-001…SC-005 has a row; the three US scenarios map to the same E2E plus two inspection rows | clean |
| A2 | — | Coverage | `tasks.md` | a task exists for each `test` row (T006–T015); the two `inspection` rows produce none, per SDD-16 | clean |
| A3 | LOW | Consistency | `spec.md` FR-002 vs `research.md` D003 | FR-002 says the glyphs are "drawn in the mark's own stroke language"; D003 records that they are drawn on a **12-unit** grid, not the mark's 24. The phrase is true of the stroke *style* (round caps, uniform width, `currentColor`) and false of the grid | accepted — the spec states an outcome ("a different mark, in the mark's own stroke language") and the grid is a technique, which belongs in research. The `## UI/UX` row names the grid, so a reader is not misled |
| A4 | LOW | Ambiguity | `spec.md` FR-006 | "the stage's own meta-text contrast" names no figure in the requirement; the number (5.57 / 6.59) lives in `## UI/UX` | accepted — SDD-05 puts numbers in `## UI/UX`; repeating them in the FR gives two places to drift |
| A5 | MEDIUM | Gap | `tasks.md` T006 | the red-first proof depends on reverting T002–T005, which now live in the worktree. If the revert is done sloppily (leaving the CSS), the test fails for a *style* reason rather than an absent badge and proves less | accepted with a guard: T006 states the failure must read as an absent `.slot__badge` — an assertion on the node's existence runs before any style assertion, so a leftover stylesheet cannot produce that failure |
| A6 | LOW | Ordering | `tasks.md` header | T002–T005 landed at Preview, so Implement's red-first ordering is inverted for the code and preserved for the tests | accepted and recorded in the task file's own note; SDD-06's live tier is what forced it, and hiding it would make the file read as a clean TDD run |
| A7 | — | Terminology | whole pack | "slot", "kind badge", "mark" used consistently; the badge is never called an icon, and "kind mark" stays reserved for spec 144's 20px entry mark | clean |
| A8 | LOW | Coverage | `spec.md` Edge Cases | the `.is-modal-origin` state is named in FR-006's fill states and in `## UI/UX`, but no scenario walks it | accepted — it is the same rule as `:hover` (one selector list, measured once); a scenario per CSS state would grow the story without adding a behaviour |
| A9 | LOW | Consistency | `contracts/stage-markup.md` vs `spec.md` FR-004 | the contract restates the `aria-hidden` guarantee the FR states | accepted — a contract restating a requirement it guards is the contract doing its job; the two say the same thing and cannot drift silently because the test asserts both |

**Zero CRITICAL. Coverage 100% of FR and SC.**

## Mechanical fixes applied this run

- `plan.md`'s verification split corrected from `12 test · 3 inspection` to `13 test · 2 inspection`
  after the no-options edge moved from `inspection` to `test` (the fixture carries it).
- `tasks.md` re-ticked: T006–T018 were marked `[X]` on first draft while the work did not exist. That
  is the failure SDD-22 names — a completion claim read as evidence — and the file now carries only
  the five boxes whose work is in the tree, with the rest unticked.

## Intent findings for the owner

None. No two requirements conflict, nothing needs narrowing, and no acceptance criterion is being
re-interpreted by the plan.

## History

- **2026-11-21 — pass 1**: 9 findings, 0 CRITICAL, 2 mechanical fixes applied, 0 intent items.
