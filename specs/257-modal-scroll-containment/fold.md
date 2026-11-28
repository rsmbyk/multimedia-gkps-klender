# Fold: spec 257 — an open modal keeps the scroll to itself

**Date**: 2026-11-28
**Converged**: pass 1, `specs/257-modal-scroll-containment/converge.md`.

## Capabilities touched

- `docs/spec/reading.md` — one `added` operation: `R66`, "An open modal keeps the scroll to itself",
  with four scenarios. Header moved `last folded` to 2026-11-28 and prepended
  `257-modal-scroll-containment` to `slices`.

## Operations

| Operation | Target | Detail |
| --- | --- | --- |
| added | `reading/R66` | Full requirement block with the end-of-view, nothing-to-scroll, nested-picker and close scenarios |
| code | `static/styles/design/components.css` | Root hold for `dialog[open]` and `overscroll-behavior: contain` on the ten named modal scrollports |
| test | `tests/e2e/test_modal_scroll_containment.py` | Seven Playwright behaviours; 7 named failures on base, 7 passes on the slice |
| board | `ITEM-277` + `backlog/board.md` | Card created at `Ready` with spec/branch/bump; no anchor issue or PR number yet |
| pack | `specs/257-modal-scroll-containment/` | Spec accepted at gate 1, checklist, research, design, plan, tasks, analysis, converge, preview and probes |

## Counts

- `docs/spec/reading.md` requirements: **65 → 66**; scenarios added: **4**.
- Slice list: **69 → 70** entries; `last folded` unchanged at 2026-11-28 (already today).
- Verification split: **7 test · 6 inspection · 1 manual**, as declared at gate 2.
- Findings folded: none — zero CRITICAL, zero `missing` / `partial` / `contradicts` / `unrequested`.

## Not folded

- `T020` manual production check — deferred until the change is deployed.
- `T022` delivery — tracker anchor, PR, version and changelog line, and the card's `In review` / `Done`
  moves all wait for separate owner words. `VERSION` and `CHANGELOG.md` are untouched here.
