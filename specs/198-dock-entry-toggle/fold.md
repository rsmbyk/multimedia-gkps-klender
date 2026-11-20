# Fold — spec 198 (2026-11-18)

Run at Converged. Typed deltas into `docs/spec/<capability>.md`; idempotent.

## Capabilities touched

| Capability | File | Operations | Before → after |
| --- | --- | --- | --- |
| `dock` | `docs/spec/dock.md` | **added** R14 (headers expand/collapse their own block, chevron per state, items jump, live locked, overrides forget on reload, instant under reduce; 4 scenarios) | requirements 13 → 14; scenarios +4 |

`reading.md` is untouched: research verified no existing rule binds header projection.

## Not folded

- Nothing — every behaviour change the slice shipped is folded. The 1 `manual` row (mid-crossing feel)
  and the OBS passes are the owner's checks, carried in the closing report, not gaps.
- The fast lane's 20 reds are pre-existing (identical set on a stashed clean baseline) and belong to other
  cards, not this slice (see `converge.md`).

## Counts

- requirements added: 1 (`dock/R14`)
- requirements modified: 0
- requirements removed / renamed: 0
- `last folded` moved to 2026-11-18 and `198-dock-entry-toggle` prepended in the `slices` line.

## Delivery state

- Version: `minor` 1.32.2 → **1.33.0** applied at Fold; `CHANGELOG.md` `[Unreleased]` gained the Added line.
- ITEM-208 recreated in `backlog/items/` and its row added under **Speccing** — the owner promotes it;
  no issue anchor (BRD-10 applies only past Speccing), no PR and no push (GIT-06/GIT-07).
