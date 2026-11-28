# Fold: spec 256 — Enter accepts a delete confirmation

**Date**: 2026-11-28
**Converged**: pass 1, `specs/256-enter-confirms-delete/converge.md`.

## Capabilities touched

- `docs/spec/reading.md` — one `added` operation: `R67`, "Enter accepts an open delete confirmation",
  with three scenarios. Header prepended `256-enter-confirms-delete` to `slices`; `last folded` was
  already 2026-11-28.

## Operations

| Operation | Target | Detail |
| --- | --- | --- |
| added | `reading/R67` | Key rule, guard list, five named surfaces and three scenarios |
| code | `static/web/enter-delete.js` | One capture-phase handler with hidden/closed/disabled/repeat/modifier guards |
| code | four marked controls + `reading/base.html` | Marker attributes on destructive buttons; one script tag |
| test | `tests/e2e/test_enter_delete_confirm.py` | Four Playwright pins; red before implementation, green after |
| board | `ITEM-278` + `backlog/board.md` | Card created at `Ready` with spec/branch/bump; no anchor issue or PR number yet |
| pack | `specs/256-enter-confirms-delete/` | Spec, checklist, research, design, plan, tasks, analysis, converge, live preview and probes |

## Counts

- `docs/spec/reading.md` requirements: **66 to 67**; scenarios added: **3**.
- Slice list: **70 to 71** entries; `last folded` unchanged at 2026-11-28.
- Verification split: **10 test · 7 inspection · 0 manual**, as declared at gate 2.
- Findings folded: none — zero CRITICAL, zero `missing` / `partial` / `contradicts` / `unrequested`.

## Not folded

- Tracker anchor, PR number, the card's `In review` / `Done` moves, `VERSION` and `CHANGELOG.md` are
  delivery steps waiting for separate owner words. `VERSION` is still 1.37.12 here; the post-rebase
  re-check found sibling slice 254 holding 1.37.13, so the delivery commit takes 1.37.14.
