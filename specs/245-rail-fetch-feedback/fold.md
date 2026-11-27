# Fold: pending state for Search and Media Library rail tiles

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-26

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R62` | Both rail tiles fetch in place; the clicked tile locks (SVG opacity `0.45`, `aria-disabled`); a 3px bar runs at the reading stage top with `aria-busy`; the stage shows a placeholder built from the destination's real markup — Search results, Search home or Media Library; settlement clears it, a later write supersedes it, and status/reduced-motion follow R61. Four scenarios. |

Header: `last folded` stays 2026-11-26 (same day) and `245-rail-fetch-feedback` is prepended to
`slices`.

## Drift guard

- **Files changed in this capability**: `static/web/reading.js`,
  `static/styles/design/components.css`, `tests/e2e/test_navigation_pending.py`,
  `docs/spec/reading.md`, `specs/245-rail-fetch-feedback/`. Board card ITEM-260, `VERSION` 1.37.3 and the changelog line were written in the
  delivery commit after PR #627 opened; the card was opened at that point, not at gate 1.
- **Declared no behaviour change**: no — R62 describes the new client behaviour; spec, tests and
  capability file agree.
- **Honest delta from research**: `openSearch()`'s destination lines are unchanged, but the call
  now passes `source: railSearch` so the tile can lock. Recorded in `research.md` D003, the spec's
  Assumptions, `tasks.md` T015 and `converge.md`; research's earlier "do not alter" wording is
  superseded on that one point.

## Before / after

| | Before (`origin/develop`) | After |
| --- | --- | --- |
| reading `R<n>` count | 61 | 62 |
| `slices` entries | 65 | 66 |
| spec packs under `specs/` (this branch) | 244 max | 245 added |

## Number collision

The slice planned `ITEM-260`, `reading/R62` and patch `1.37.3`. Before folding, every local and
remote ref and every sibling worktree was searched: no ref carried `### R62` in `docs/spec/`,
no ref named `ITEM-260`, and `origin/develop:VERSION` was `1.37.2`. No renumbering was needed;
the board card and version bump wait for delivery.

## Post-gate documentation fixes

Mechanical only, no requirement changed: test-function names in the plan/tasks match the tests
that were written; the `sessionStorage` key in the results test was corrected; old placeholder ids
were restored; `analysis.md` SHAs were refreshed. Each is recorded in `converge.md`.

## Not folded

No requirements were excluded — Converge reported zero gaps.
